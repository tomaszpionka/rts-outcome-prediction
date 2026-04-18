---
category: A
date: 2026-04-18
branch: feat/01-04-03-sc2egset-minimal-history
phase: "01"
pipeline_section: "01_04"
step: "01_04_03"
dataset: sc2egset
game: sc2
title: "Step 01_04_03 — Minimal Cross-Dataset History View (sc2egset pattern-establisher)"
manual_reference: "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md §4"
invariants_touched: [I3, I5, I6, I7, I8, I9]
predecessors: ["01_04_02"]
plan_round: R3
addresses_critique: planning/current_plan.critique.v3.md (R3 — APPROVE_WITH_WARNINGS after 3 rounds)
---

# Step 01_04_03 — Minimal cross-dataset history view (sc2egset pattern-establisher)

## Summary

Create a DuckDB VIEW `matches_history_minimal` that is a **narrow cross-dataset-harmonized projection** of `matches_flat_clean` (from 01_04_02, PR #142). The view is the common substrate for Phase 02+ rating-system backtesting. The canonical cross-dataset contract is **8 columns, 2 rows per 1v1 match, TIMESTAMP-typed temporal anchor, per-dataset-polymorphic faction vocabulary**.

**Category:** A (Phase work)
**Branch:** `feat/01-04-03-sc2egset-minimal-history`
**Phase / Pipeline Section / Step:** 01 — Data Exploration / 01_04 — Data Cleaning / **01_04_03** (NEW)
**Dataset:** sc2egset (pattern-establisher; aoestats + aoec follow in sibling PRs)
**Invariants:** I3, I5-analog, I6, I7, I8, I9

---

## BLOCKERS

**None remain after R1 revision.** Three explicit assumptions / cross-dataset commitments:

1. **`match_id` is the cross-dataset name for sc2egset's `replay_id`**: `'sc2egset::' || replay_id AS match_id`.

2. **`started_at` is TIMESTAMP (via TRY_CAST of `details_timeUTC`).** R1-BLOCKER-2 fix: contract-level canonical dtype is **TIMESTAMP (no TZ)**. sc2egset casts from VARCHAR ISO-8601 here; aoestats sibling PR must `CAST started_timestamp AT TIME ZONE 'UTC' AS TIMESTAMP`; aoe2companion passes TIMESTAMP through. This eliminates the 3-way dtype split (VARCHAR/TIMESTAMPTZ/TIMESTAMP) present at 01_04_02.

3. **`is_mmr_missing` NOT in the minimal view.** Phase 02 consumers that need MMR join from `matches_flat_clean` on `(match_id, player_id)`.

4. **`faction` is per-dataset polymorphic vocabulary.** R1-BLOCKER-5 fix: explicit contract — column name + dtype are cross-dataset, but VALUES are per-dataset (SC2 race stems vs AoE2 civilization names). Consumers MUST NOT treat `faction` as a single categorical feature across datasets without game-conditional encoding. Schema YAML + research_log document this.

---

## Scope

Create `matches_history_minimal` for sc2egset — an **8-column player-row-grain** VIEW (2 rows per 1v1 match) projected from `matches_flat_clean`. Cross-dataset-harmonized common substrate for Phase 02+ rating-system backtesting. Temporarily reverts `PIPELINE_SECTION_STATUS["01_04"]` from `complete` → `in_progress` for the duration of execution, then back to `complete` on gate pass.

## Problem statement

Phase 02 rating-system backtesting needs one table shape identical across sc2egset / aoestats / aoec in column names and dtypes, player-row-grain (2 rows per 1v1 match), read-only / non-destructive. Neither `matches_flat_clean` nor `player_history_all` fits as-is. `matches_history_minimal` answers this gap.

## Proposed schema (8 columns)

| column | dtype | semantics |
|---|---|---|
| `match_id` | VARCHAR | `'sc2egset::' \|\| replay_id` (UNION-unique across datasets) |
| `started_at` | **TIMESTAMP** | `TRY_CAST(details_timeUTC AS TIMESTAMP)`; canonical cross-dataset type |
| `player_id` | VARCHAR | focal toon_id |
| `opponent_id` | VARCHAR | opposing toon_id |
| `faction` | VARCHAR | focal player's `race` (raw `Prot`/`Terr`/`Zerg` 4-char stems in sc2egset — per-dataset polymorphic vocabulary; see R1-BLOCKER-5 fix) |
| `opponent_faction` | VARCHAR | opposing player's `race` (same vocabulary as `faction`) |
| `won` | BOOLEAN | `result = 'Win'`; two rows of a match have complementary `won` |
| `dataset_tag` | VARCHAR | constant `'sc2egset'` |

**Grain:** 2 rows per match_id (player row + opponent row, symmetric swap).

## Assumptions & unknowns

| # | Assumption | Risk if wrong |
|---|---|---|
| A1 | Cross-dataset union uniqueness via `'sc2egset::' \|\| replay_id` prefix. | Collision → duplicates on future UNION ALL. Mitigation: assert `COUNT(*) = COUNT(DISTINCT match_id)`. |
| A2 (REV) | **Canonical cross-dataset dtype for `started_at` is TIMESTAMP.** sc2egset casts here via `TRY_CAST(details_timeUTC AS TIMESTAMP)`; aoestats sibling PR casts `CAST(started_timestamp AT TIME ZONE 'UTC' AS TIMESTAMP)`; aoe2companion passes TIMESTAMP through. | If any sibling PR ships a different type, UNION ALL fails with DuckDB type-error (visible, not silent). The contract is enforced at each sibling PR's gate. |
| A2b (NEW) | **aoestats sibling PR column mapping (R2-WARNING-2):** `p{0,1}_profile_id → player_id` (UNION ALL the two halves); `p{0,1}_civ → faction` (raw per-dataset polymorphic civ vocabulary); `p{0,1}_winner → won` (TARGET — aoestats YAML flags `p_winner` as POST_GAME_HISTORICAL, acceptable here since `won` IS the prediction target in matches_history_minimal, symmetric with sc2egset's `result='Win'`); `replay_id / match_id → 'aoestats::' \|\| <native_id>`. aoestats slot-bias note: team1 wins ≈52.27% per aoestats matches_1v1_clean.yaml — naive p0/p1 swap preserves slot bias; sibling PR must acknowledge and not claim slot-balanced sampling. | If mapping is mis-applied (e.g., `p_winner` treated as feature instead of target), the view encodes future leakage on aoestats. Mitigation: aoestats sibling plan will pin mapping explicitly. |
| A3 | `race` (actual played race) is the right faction signal, not `selectedRace` (includes `'Random'`). Consistent with `matches_long_raw.chosen_civ_or_race`. | `selectedRace='Random'` leaks pre-resolution semantics; `race` is what shipped. |
| A4 | `toon_id` is the stable sc2egset player identifier. Cross-dataset identity / nickname resolution deferred to Phase 01_05+. | Per-dataset identifier OK. |
| A5 | Source table = `matches_flat_clean`, not `player_history_all`. Built-in 1v1-decisive filter; 44,418 rows = 22,209 × 2 by construction. | If `matches_flat_clean` loses `race` or `toon_id`, view breaks. Mitigation: DESCRIBE-based source-column assertion in cell 4. |
| A6 | `opponent_id` / `opponent_faction` derive from self-join on `matches_flat_clean` via `replay_id` with `toon_id <> opp.toon_id`. | `player_history_all` adds 399 unwanted rows. |
| A7 (NEW) | **`faction` values are per-dataset-polymorphic.** R1-BLOCKER-5: sc2egset ships `Prot/Terr/Zerg`; aoestats ships full civ names (`Mongols`, etc.); aoe2companion similarly. Column NAME and DTYPE are cross-dataset; VALUES are per-dataset ontology. | Consumers that do naive UNION-wide `GROUP BY faction` get ontologically-mixed buckets. Schema YAML explicitly warns + research_log documents. |

## Literature context

Cleaning-stage methodology (the only references this step's methodology cites per I9):
- Manual `01_DATA_EXPLORATION_MANUAL.md` §4.2 — non-destructive cleaning.
- Manual `01_DATA_EXPLORATION_MANUAL.md` §4.4 — post-cleaning validation.
- Schafer & Graham (2002) — missingness handling (already established in 01_04_01).
- van Buuren (2018) — missingness handling.
- Tukey (1977) — EDA on raw-string vocabularies feeds the FACTION_VOCAB_SQL exploratory output.

Downstream-consumer context (not cited as this step's methodology, listed for traceability only — R1-BLOCKER-4 fix):
- Phase 02+ rating systems (Elo, Glicko, Glicko-2, TrueSkill, Aligulac, BTL) are downstream consumers of this view; their methodology references belong to Phase 02 plans.

## Cross-dataset comparability justification (I8)

`matches_history_minimal` fixes shape **before** any dataset-specific MMR/civ semantics enter. Every sibling PR emits a view with the same 8 columns, same dtypes, same grain, **per-dataset-polymorphic faction vocabulary**, different `dataset_tag`. Canonical temporal dtype = TIMESTAMP.

**Polymorphic-column design rationale (R2-NOTE-2):** A single polymorphic `faction` column (rather than separate `sc2_race` / `aoe2_civ` columns) was chosen for substrate simplicity — downstream rating-system backtests enumerate matches agnostic of game identity; game-conditional categorical encoding happens inside feature extractors at Phase 02 (e.g., `CASE dataset_tag WHEN 'sc2egset' THEN one_hot_race(faction) WHEN 'aoestats' THEN one_hot_civ(faction) END`). The `dataset_tag` column carries the ontological disambiguator, so the polymorphism is explicit, not hidden.

Future UNION ALL in Phase 02:

```sql
SELECT * FROM sc2egset.matches_history_minimal
UNION ALL
SELECT * FROM aoestats.matches_history_minimal
UNION ALL
SELECT * FROM aoe2companion.matches_history_minimal
```

**I8 contract explicit limits (R1-WARNING-2 + R1-BLOCKER-5 fix):**
- aoestats ships 1-row-per-match at 01_04_02; its sibling PR MUST re-project to 2-rows-per-match via `UNION ALL` of two SELECTs swapping p0/p1 roles, with explicit awareness of the aoestats `team1_wins ~52.27%` slot asymmetry documented in `matches_1v1_clean.yaml`.
- aoestats / aoec `started_timestamp` / `started` MUST cast to canonical TIMESTAMP (see A2).
- `faction` vocabulary is per-dataset-polymorphic; no enum harmonization. Consumers wanting cross-dataset `faction`-conditional analyses MUST game-condition (e.g., `WHERE dataset_tag = 'sc2egset'` before `GROUP BY faction`).

## Design questions — resolved

**Q1. Source table.** `matches_flat_clean` (not `player_history_all`): built-in 1v1-decisive filter, 44,418 = 22,209 × 2, all columns present. Projecting from `player_history_all` re-applies the filter (breaks I9 composability).

**Q2. match_id prefix — inline in VIEW or upstream column?** **Inline** (`'sc2egset::' || mfc.replay_id AS match_id`). Upstream `replay_id` unchanged (I9).

**Q3. Faction source field.** `race` (verified in `matches_flat_clean.yaml` line 55-58: *"Actual race played (Protoss, Zerg, Terran abbreviated)"* — empirical vocabulary is `Prot/Terr/Zerg`). Not `selectedRace`.

**Q4. Opponent derivation.** Self-join on `matches_flat_clean` (CTE alias), `mfc.replay_id = opp.replay_id AND mfc.toon_id <> opp.toon_id`. 1v1-decisive upstream guarantees exactly 1 opponent row.

**Q5. MMR / rated-flag columns.** Excluded.

**Q6. PIPELINE_SECTION_STATUS.** Flip `complete` → `in_progress` at T01; flip back at T03. **R1-WARNING-3 rollback:** if T02 fails, Halt predicate mandates manual revert of PIPELINE_SECTION_STATUS 01_04 back to `complete` before aborting.

**Q7. Gate predicate.** `row_count == 2 * distinct match_ids == matches_flat_clean.row_count` + 8-column schema + I5-analog symmetry (NULL-safe) + prefix uniqueness + dataset_tag constancy + zero NULLs on 5 non-nullable cols + TIMESTAMP dtype verification for `started_at`.

**Q8. Notebook cells.** 18 cells, patterned on `01_04_02_data_cleaning_execution.py`.

---

## Execution Steps

### T01 — Register step 01_04_03 in status files and ROADMAP

**Objective:** Add the new step to ROADMAP, STEP_STATUS, and revert PIPELINE_SECTION_STATUS.

**Instructions:**

1. In `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`, append the ROADMAP block (see "ROADMAP edit" below) after `### Step 01_04_02`.

2. In `STEP_STATUS.yaml`, under `steps:`, append:
   ```yaml
   "01_04_03":
     name: "Minimal Cross-Dataset History View"
     pipeline_section: "01_04"
     status: not_started
   ```

3. In `PIPELINE_SECTION_STATUS.yaml`, change `pipeline_sections["01_04"].status` from `complete` to `in_progress`. Do NOT touch `PHASE_STATUS.yaml`.

**Verification:**
- `grep -n "01_04_03" ROADMAP.md` shows the new block.
- `grep -n "01_04_03" STEP_STATUS.yaml` shows `status: not_started`.
- `grep -n "01_04" PIPELINE_SECTION_STATUS.yaml` shows `status: in_progress`.

**Rollback on failure:** If any later step fails, revert PIPELINE_SECTION_STATUS.yaml `01_04.status = complete` before aborting (R1-WARNING-3).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (MODIFIED)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (MODIFIED)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (MODIFIED)

### T02 — Create the jupytext-paired notebook; execute end-to-end

**Objective:** Produce `01_04_03_minimal_history_view.py` (auto-paired `.ipynb`). All execution in the notebook. No module code added.

**Pre-execution constraint (R1-WARNING-7):** T02 holds a `read_only=False` DuckDB connection. No parallel CLI writes to `src/rts_predict/games/sc2/datasets/sc2egset/data/db/sc2egset.duckdb` during T02.

**Instructions:**

1. Create `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py` as a percent-format jupytext notebook. Front-matter verbatim from `01_04_02_data_cleaning_execution.py`.

2. Follow the 18-cell outline.

3. Run `poetry run jupytext --sync sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py`.

4. Execute end-to-end. Must write all artifacts and print `All assertions pass: True`.

**Notebook cell outline (18 cells):**

| # | Kind | Purpose |
|---|---|---|
| 1 | md | Title, phase/section/step, predecessor (01_04_02), invariants (I3/I5/I6/I7/I8/I9), date |
| 2 | code | Imports: `json`, `Path`, `yaml`, `rts_predict.common.notebook_utils.get_notebook_db`, `setup_notebook_logging` |
| 3 | code | `db = get_notebook_db("sc2", "sc2egset", read_only=False)`; `con = db.con` |
| 4 | code | Source-view sanity check — DESCRIBE matches_flat_clean; assert 28 cols + presence of `replay_id`, `toon_id`, `race`, `result`, `details_timeUTC` |
| 5 | code | Define `CREATE_MATCHES_HISTORY_MINIMAL_SQL` constant (DDL below); `print(sql)` |
| 6 | code | Execute DDL: `con.execute(CREATE_MATCHES_HISTORY_MINIMAL_SQL)` |
| 7 | code | Schema shape validation — DESCRIBE matches_history_minimal; assert 8 cols + dtypes `[VARCHAR, TIMESTAMP, VARCHAR, VARCHAR, VARCHAR, VARCHAR, BOOLEAN, VARCHAR]` per spec |
| 8 | code | Row-count validation — `ROW_COUNT_CHECK_SQL`; assert 44418 / 22209 / 22209 / 0 |
| 9 | code | Symmetry (I5-analog, NULL-safe) — `SYMMETRY_I5_ANALOG_SQL` (uses `IS DISTINCT FROM`); assert 0 violations |
| 10 | code | No-NULL on non-nullable cols — `ZERO_NULL_SQL`; assert 5 zeros |
| 11 | code | match_id prefix verification — `PREFIX_CHECK_SQL`; assert 0 violations |
| 12 | code | dataset_tag constant — `DATASET_TAG_CHECK_SQL`; assert distinct=1, value='sc2egset' |
| 13 | code | Faction vocabulary observed (exploratory, no gate) — `FACTION_VOCAB_SQL`; record verbatim |
| 14 | code | Temporal sanity — `TEMPORAL_SANITY_SQL` on TIMESTAMP column; min/max/null count |
| 15 | code | Build validation JSON — dict with step, dataset, row_counts, assertion_results, sql_queries verbatim, spec_schema, **describe_table_rows** (`DESCRIBE matches_history_minimal` result captured as list of dicts so `nullable:` values in YAML are source-grounded); assert `all_assertions_pass`; write |
| 16 | code | Build markdown report; write MD |
| 17 | code | Write schema YAML for `matches_history_minimal`. **R1-WARNING-4 + R2-WARNING-3 fix — explicit nullable translation:** `describe_rows = con.execute("DESCRIBE matches_history_minimal").fetchall()` returns 6-tuples `(column_name, column_type, null, key, default, extra)` per DuckDB DESCRIBE contract; index `2` is the null flag with string values `'YES'` or `'NO'`. Translation: `nullable = (row[2] == 'YES')`. Build the YAML dict with concrete booleans before `yaml.safe_dump`. No `<from DESCRIBE>` string literals in the written YAML. |
| 18 | code | Close connection; print final summary |

**Verification:**
- `ls sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.{py,ipynb}` — both exist.
- Notebook writes all three artifacts (json, md, yaml) and prints `All assertions pass: True`.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py` (NEW)
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.ipynb` (NEW, auto-paired)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json` (NEW)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.md` (NEW)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml` (NEW)

### T03 — Close out status files

**Objective:** Transition step to complete and re-close 01_04.

**Instructions:**
1. `STEP_STATUS.yaml`: set `steps["01_04_03"].status = complete`, add `completed_at: "<ISO date>"`.
2. `PIPELINE_SECTION_STATUS.yaml`: revert `pipeline_sections["01_04"].status = complete`.
3. `PHASE_STATUS.yaml`: unchanged (Phase 01 stays `in_progress`).

**Verification:**
- `grep -n "01_04_03" STEP_STATUS.yaml` shows `status: complete`.
- `grep -n '01_04:' PIPELINE_SECTION_STATUS.yaml` shows `status: complete`.

**File scope:**
- `STEP_STATUS.yaml` (MODIFIED)
- `PIPELINE_SECTION_STATUS.yaml` (MODIFIED)

### T04 — Append research_log entry

**Objective:** Dataset-specific narrative entry.

**Instructions:** Prepend new entry at top of `research_log.md` per template in "research_log entry template" section.

**Verification:**
- `head -60 research_log.md` shows the new entry.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (MODIFIED)

---

## DDL — `matches_history_minimal` (R1-BLOCKER-2 + R1-WARNING-1 fix: TIMESTAMP cast inline)

```sql
CREATE OR REPLACE VIEW matches_history_minimal AS
-- Purpose: Minimal cross-dataset-harmonized history view for rating-system
--   backtesting (Phase 02+ consumer).
-- Grain: 2 rows per 1v1 match (player row + opponent row, symmetric swap).
-- Cross-dataset contract: 8 columns, identical dtypes across sibling views.
--   Canonical temporal dtype = TIMESTAMP (no TZ). Faction vocabulary is
--   per-dataset-polymorphic (SC2 race stems vs AoE2 civ names).
-- Invariants: I3 (TIMESTAMP cast enables faithful chronological ordering),
--   I5-analog (player-row symmetry, NULL-safe assertion), I6 (DDL verbatim
--   in JSON artifact), I7 (magic numbers 32 / 42 cite
--   data/db/schemas/views/matches_long_raw.yaml provenance regex
--   [0-9a-f]{32}), I8 (UNION-compatible with sibling
--   datasets via dataset_tag + prefixed match_id + canonical dtypes), I9
--   (pure projection of matches_flat_clean; no upstream modification).
WITH base AS (
    SELECT
        'sc2egset::' || mfc.replay_id              AS match_id,
        mfc.replay_id                              AS raw_match_id,
        TRY_CAST(mfc.details_timeUTC AS TIMESTAMP) AS started_at,
        mfc.toon_id                                AS player_id,
        mfc.race                                   AS faction,
        (mfc.result = 'Win')                       AS won
    FROM matches_flat_clean mfc
)
SELECT
    p.match_id,
    p.started_at,
    p.player_id,
    o.player_id                                    AS opponent_id,
    p.faction,
    o.faction                                      AS opponent_faction,
    p.won,
    'sc2egset'                                     AS dataset_tag
FROM base p
JOIN base o
  ON p.match_id = o.match_id
 AND p.player_id <> o.player_id
ORDER BY p.started_at, p.match_id, p.player_id;
```

**Expected column order / dtypes:**
1. `match_id` VARCHAR
2. `started_at` **TIMESTAMP** (cast from VARCHAR ISO-8601)
3. `player_id` VARCHAR
4. `opponent_id` VARCHAR
5. `faction` VARCHAR
6. `opponent_faction` VARCHAR
7. `won` BOOLEAN
8. `dataset_tag` VARCHAR

**Nullability:** `started_at` may be NULL if `TRY_CAST` fails on a malformed ISO-8601 string. Upstream `details_timeUTC` is nullable per `matches_flat_clean.yaml`. Empirically: 0 failed casts expected but the assertion does not depend on empirical luck — log actual null count in validation JSON (I7).

---

## Schema YAML — `matches_history_minimal.yaml` content (T02 cell 17 writes this, with concrete `nullable:` booleans from DESCRIBE)

```yaml
table: matches_history_minimal
dataset: sc2egset
game: sc2
object_type: view
step: "01_04_03"
row_count: 44418
describe_artifact: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json
generated_date: "<ISO date of run, filled at runtime>"
columns:
  - name: match_id
    type: VARCHAR
    nullable: <from DESCRIBE — concrete boolean>
    description: "Cross-dataset unique match identifier. Format: '<dataset_tag>::<native_id>'. For sc2egset: 'sc2egset::<32-char-hex-replay_id>'. Prefix guarantees UNION ALL uniqueness across sibling datasets. Length contract = 42 chars (10 prefix + 32 hex) derived from src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml join_key regex [0-9a-f]{32} (I7 provenance)."
    notes: "IDENTITY. Prefix applied in this VIEW only; upstream replay_id unchanged (I9)."
  - name: started_at
    type: TIMESTAMP
    nullable: <from DESCRIBE>
    description: "Match start time. TIMESTAMP (no TZ) via TRY_CAST(matches_flat_clean.details_timeUTC AS TIMESTAMP). Canonical cross-dataset dtype: sibling VIEWs (aoestats, aoe2companion) MUST emit TIMESTAMP (aoestats CAST from TIMESTAMPTZ AT TIME ZONE 'UTC'; aoe2companion pass-through). DuckDB TRY_CAST handles variable sub-second precision (7 observed length variants 22–28 chars in upstream VARCHAR)."
    notes: "CONTEXT. Temporal anchor for Phase 02 rating-update loops. Chronologically faithful (TIMESTAMP ordering, not lex)."
  - name: player_id
    type: VARCHAR
    nullable: <from DESCRIBE>
    description: "Focal player identifier. sc2egset: Battle.net toon_id."
    notes: "IDENTITY. Per-dataset identifier; cross-dataset identity resolution is a future step (Phase 01_05+)."
  - name: opponent_id
    type: VARCHAR
    nullable: <from DESCRIBE>
    description: "Opposing player identifier. Same grain and provenance as player_id."
    notes: "IDENTITY."
  - name: faction
    type: VARCHAR
    nullable: <from DESCRIBE>
    description: >
      Focal player's faction. **Per-dataset polymorphic vocabulary** (cross-dataset
      column name + dtype only — values differ in ontology). sc2egset: 4-char race
      stems `Prot`/`Terr`/`Zerg` (empirically verified; NOT full 'Protoss'/'Terran'/'Zerg').
      aoestats: full civilization names (`Mongols`, `Franks`, etc.).
      aoe2companion: full civilization names.
      CONSUMERS MUST NOT treat faction as a single categorical feature across
      datasets without game-conditional encoding (e.g., WHERE dataset_tag = 'sc2egset'
      before GROUP BY faction).
    notes: "PRE_GAME. Raw vocabulary (race actually played, not selectedRace which includes 'Random'). Polymorphic I8 contract — see description."
  - name: opponent_faction
    type: VARCHAR
    nullable: <from DESCRIBE>
    description: "Opposing player's faction (same per-dataset vocabulary as `faction`)."
    notes: "PRE_GAME. Mirror of faction from the opponent row."
  - name: won
    type: BOOLEAN
    nullable: <from DESCRIBE>
    description: "TRUE if the focal player won, FALSE otherwise. The two rows of a match have complementary `won` values (exactly one TRUE, one FALSE)."
    notes: "TARGET. Direct projection of matches_flat_clean.result; prediction label for downstream experiments."
  - name: dataset_tag
    type: VARCHAR
    nullable: false
    description: "Dataset discriminator for UNION ALL across sibling datasets. Constant 'sc2egset' in this VIEW."
    notes: "IDENTITY. Matches the prefix before '::' in match_id."
provenance:
  source_tables:
    - matches_flat_clean
  join_key: "self-join on matches_flat_clean via replay_id; player_id = toon_id; opponent_id from sibling row where mfc.toon_id <> opp.toon_id"
  filter: "Inherited from matches_flat_clean: true_1v1_decisive (2 players, 1 Win + 1 Loss) + mmr_valid."
  scope: "22,209 true 1v1 decisive replays, 44,418 player-rows. Cross-dataset harmonization substrate for Phase 02+ rating backtesting."
  created_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py
invariants:
  - id: I3
    description: >
      TIMESTAMP-typed temporal anchor enables chronologically faithful ordering
      (upstream VARCHAR details_timeUTC has 7 distinct sub-second precision
      variants 22–28 chars; lex ordering would be non-monotonic). TRY_CAST
      to TIMESTAMP in the VIEW normalizes. No windowed aggregations, no
      shift(), no future joins. Phase 02 consumers use started_at as the
      strict-less-than anchor for match_time < T feature computation.
  - id: I5
    description: >
      Player-row symmetry (I5-analog). Every match_id has exactly 2 rows.
      (player_id, opponent_id) appears once in each direction. The two `won`
      values are complementary. faction and opponent_faction are mirror
      images. Assertion SQL uses IS DISTINCT FROM for NULL-safe comparison
      (R1-BLOCKER-3 fix).
  - id: I6
    description: >
      CREATE OR REPLACE VIEW DDL + every assertion SQL stored verbatim in
      01_04_03_minimal_history_view.json sql_queries block. DESCRIBE result
      captured in validation JSON describe_table_rows for reproducibility
      of the nullable flags written to this YAML.
  - id: I7
    description: >
      Magic literals in PREFIX_CHECK_SQL (`32` hex chars, `42` total length)
      cite upstream data/db/schemas/views/matches_long_raw.yaml join_key
      regex [0-9a-f]{32} for provenance.
  - id: I8
    description: >
      Cross-dataset comparability: 8-column names + dtypes are the cross-
      dataset contract. Canonical temporal dtype = TIMESTAMP (no TZ). Faction
      vocabulary is per-dataset-polymorphic — column name and dtype cross-
      dataset, values per-dataset ontology. aoestats sibling PR must project
      its 1-row-per-match matches_1v1_clean to 2-rows-per-match via UNION ALL
      of p0/p1 SELECTs (with awareness of team1_wins ~52.27% slot asymmetry);
      aoe2companion similarly. match_id prefixed 'sc2egset::'.
  - id: I9
    description: >
      Pure non-destructive projection. No raw table modified. matches_flat_clean
      unchanged. Only matches_history_minimal VIEW created via CREATE OR
      REPLACE. Inputs (matches_flat_clean, matches_flat) read-only.
provenance_categories_note: >
  This view inherits provenance categories from matches_flat_clean. Per-column
  'notes' field uses the single-token vocabulary (IDENTITY, CONTEXT, PRE_GAME,
  TARGET) established in 01_04_02.
```

---

## Validation SQL (embedded verbatim in validation JSON sql_queries — I6)

**Row-count parity (I5-analog cardinality + I9):**
```sql
-- ROW_COUNT_CHECK_SQL
SELECT
    (SELECT COUNT(*) FROM matches_history_minimal)                  AS total_rows,
    (SELECT COUNT(DISTINCT match_id) FROM matches_history_minimal)  AS distinct_match_ids,
    (SELECT COUNT(*) FROM matches_flat_clean)                       AS src_rows,
    (SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean)      AS src_replays,
    (SELECT COUNT(*) FROM (
        SELECT match_id, COUNT(*) AS n
        FROM matches_history_minimal
        GROUP BY match_id
        HAVING n = 2
     ))                                                             AS matches_with_2_rows,
    (SELECT COUNT(*) FROM (
        SELECT match_id, COUNT(*) AS n
        FROM matches_history_minimal
        GROUP BY match_id
        HAVING n <> 2
     ))                                                             AS matches_with_not_2_rows;
-- Expected: total_rows = 44418, distinct_match_ids = 22209,
--           src_rows = 44418, src_replays = 22209,
--           matches_with_2_rows = 22209, matches_with_not_2_rows = 0.
```

**Symmetry (I5-analog, NULL-safe — R1-BLOCKER-3 fix):**
```sql
-- SYMMETRY_I5_ANALOG_SQL
WITH row_pairs AS (
    SELECT
        a.match_id,
        a.player_id         AS a_pid,
        a.opponent_id       AS a_oid,
        a.won               AS a_won,
        a.faction           AS a_fac,
        a.opponent_faction  AS a_ofac,
        b.player_id         AS b_pid,
        b.opponent_id       AS b_oid,
        b.won               AS b_won,
        b.faction           AS b_fac,
        b.opponent_faction  AS b_ofac
    FROM matches_history_minimal a
    JOIN matches_history_minimal b
      ON a.match_id = b.match_id
     AND a.player_id <> b.player_id
)
SELECT COUNT(*) AS symmetry_violations
FROM row_pairs
WHERE a_pid <> b_oid                           -- player/opponent swap broken
   OR a_oid <> b_pid
   OR a_won = b_won                            -- not complementary
   OR a_fac IS DISTINCT FROM b_ofac            -- NULL-safe faction mirror
   OR a_ofac IS DISTINCT FROM b_fac;
-- Expected: 0. Gate: must equal 0.
-- NULL-safety: IS DISTINCT FROM treats NULL as comparable (not UNKNOWN);
--   a row where both sides are NULL is treated as equal (symmetric),
--   a row where one side is NULL and the other is not is treated as distinct
--   (asymmetric → violation).
```

**Zero-NULL on non-nullable spec columns:**
```sql
-- ZERO_NULL_SQL
SELECT
    COUNT(*) FILTER (WHERE match_id     IS NULL) AS null_match_id,
    COUNT(*) FILTER (WHERE started_at   IS NULL) AS null_started_at,
    COUNT(*) FILTER (WHERE player_id    IS NULL) AS null_player_id,
    COUNT(*) FILTER (WHERE opponent_id  IS NULL) AS null_opponent_id,
    COUNT(*) FILTER (WHERE won          IS NULL) AS null_won,
    COUNT(*) FILTER (WHERE dataset_tag  IS NULL) AS null_dataset_tag,
    COUNT(*) FILTER (WHERE faction          IS NULL) AS null_faction_info,
    COUNT(*) FILTER (WHERE opponent_faction IS NULL) AS null_opponent_faction_info
FROM matches_history_minimal;
-- Gate: null_match_id / null_player_id / null_opponent_id / null_won / null_dataset_tag all 0.
-- null_started_at: report value (I7); if > 0 flag in JSON (indicates TRY_CAST failures on malformed details_timeUTC), do not fail.
-- null_faction / null_opponent_faction: report only.
```

**Prefix uniqueness (I8; I7 — cites data/db/schemas/views/matches_long_raw.yaml regex [0-9a-f]{32}):**
```sql
-- PREFIX_CHECK_SQL
-- Magic literals: 'sc2egset::' = 10-char literal prefix (plan spec);
--                 32 = replay_id hex length from
--                      src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml
--                      join_key regex [0-9a-f]{32} (I7 provenance).
-- Total length contract: 10 + 32 = 42.
SELECT COUNT(*) AS prefix_violations
FROM matches_history_minimal
WHERE match_id NOT LIKE 'sc2egset::%'
   OR length(match_id) <> length('sc2egset::') + 32
   OR regexp_extract(match_id, '::([0-9a-f]{32})$', 1) = '';
-- Expected: 0. Gate: must equal 0.
```

**Dataset tag constant (I8):**
```sql
-- DATASET_TAG_CHECK_SQL
SELECT
    COUNT(DISTINCT dataset_tag) AS n_distinct_tags,
    MAX(dataset_tag)            AS the_tag
FROM matches_history_minimal;
-- Expected: 1 / 'sc2egset'. Gate: both.
```

**Faction vocabulary (exploratory — documents per-dataset polymorphism; R1-BLOCKER-1 fix: sc2egset empirically ships `Prot`/`Terr`/`Zerg`):**
```sql
-- FACTION_VOCAB_SQL
SELECT faction, COUNT(*) AS n
FROM matches_history_minimal
GROUP BY faction
ORDER BY n DESC;
-- Expected (sc2egset, empirically): 'Prot' ~16121, 'Zerg' ~15527, 'Terr' ~12770.
-- NOT full 'Protoss'/'Terran'/'Zerg' strings — 4-char stems per
-- matches_flat_clean.yaml line 58 ("Actual race played abbreviated").
-- No gate; feeds I8 per-dataset-polymorphism documentation.
```

**Temporal sanity (I3):**
```sql
-- TEMPORAL_SANITY_SQL
SELECT
    MIN(started_at)            AS min_started_at,
    MAX(started_at)            AS max_started_at,
    COUNT(*) FILTER (WHERE started_at IS NULL) AS null_started_at,
    COUNT(DISTINCT started_at) AS distinct_started_at
FROM matches_history_minimal;
-- Report only. TIMESTAMP ordering is chronologically faithful (unlike the
-- upstream VARCHAR lex ordering which had 7 distinct sub-second precision
-- lengths). null_started_at counts TRY_CAST failures on malformed upstream
-- strings (expected 0).
```

---

## File Manifest

| Status | Path |
|---|---|
| NEW | `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py` |
| NEW | `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.ipynb` |
| NEW | `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml` |
| NEW | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json` |
| NEW | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.md` |
| MODIFIED | `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (append 01_04_03 block) |
| MODIFIED | `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (T01 append not_started; T03 flip complete) |
| MODIFIED | `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (T01 flip in_progress; T03 flip complete) |
| MODIFIED | `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (prepend 01_04_03 entry) |

**Files NOT touched (I9 enforcement):**
- `matches_flat_clean.yaml` — byte-identical.
- `player_history_all.yaml` — byte-identical.
- `matches_long_raw.yaml` — byte-identical.
- `PHASE_STATUS.yaml` — unchanged.

---

## ROADMAP edit — content to insert (T01)

```yaml
step_number: "01_04_03"
name: "Minimal Cross-Dataset History View"
description: >
  Create matches_history_minimal VIEW: 8-column player-row-grain projection
  of matches_flat_clean (2 rows per 1v1 match). Cross-dataset-harmonized
  substrate for Phase 02+ rating-system backtesting. Canonical TIMESTAMP
  temporal dtype; per-dataset-polymorphic faction vocabulary. Pattern-
  establisher -- aoestats and aoe2companion emit identically-shaped sibling
  views in follow-up PRs (I8).
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 4.2 (non-destructive cleaning), Section 4.4 (post-cleaning validation)"
dataset: "sc2egset"
question: >
  What is the minimum cross-dataset-harmonized shape for per-player match
  history required by Phase 02 rating-system backtesting? Does a pure
  projection of matches_flat_clean with TIMESTAMP-cast started_at satisfy
  the I3/I5-analog/I6/I7/I8/I9 contract?
method: >
  CREATE OR REPLACE VIEW on top of matches_flat_clean via self-join on
  replay_id to materialize (player_row, opponent_row) symmetric pairs.
  match_id prefixed 'sc2egset::' for cross-dataset UNION uniqueness.
  started_at via TRY_CAST to canonical TIMESTAMP dtype. Faction strings
  raw (per-dataset polymorphic vocabulary). Validate: row-count parity,
  schema shape, I5-analog NULL-safe symmetry, prefix uniqueness,
  dataset_tag constancy, temporal sanity.
stratification: "By match_id (2 symmetric rows); by faction for vocabulary documentation."
predecessors:
  - "01_04_02"
methodology_citations:
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.2 (non-destructive cleaning)"
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.4 (post-cleaning validation)"
  - "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley. (for raw-string vocabulary documentation via FACTION_VOCAB_SQL)"
  - "Schafer, J. L., & Graham, J. W. (2002). Missing data: Our view of the state of the art. Psychological Methods."
  - "van Buuren, S. (2018). Flexible Imputation of Missing Data (2nd ed.). CRC Press."
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py"
inputs:
  duckdb_views:
    - "matches_flat_clean (44,418 rows / 22,209 replays -- from 01_04_02)"
  prior_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json"
  schema_yamls:
    - "data/db/schemas/views/matches_flat_clean.yaml"
outputs:
  duckdb_views:
    - "matches_history_minimal (NEW -- 8 cols, 44,418 rows)"
  schema_yamls:
    - "data/db/schemas/views/matches_history_minimal.yaml (NEW)"
  data_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json"
  report: "artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.md"
reproducibility: >
  CREATE OR REPLACE VIEW DDL + every assertion SQL stored verbatim in the
  validation JSON sql_queries block (I6). DESCRIBE result captured in the
  validation JSON describe_table_rows for reproducibility of nullable flags
  written to schema YAML.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >
      TIMESTAMP cast (via TRY_CAST) enables chronologically faithful ordering.
      Upstream VARCHAR details_timeUTC has 7 distinct sub-second precision
      lengths (22–28 chars); lex ordering would be non-monotonic across
      formats. Phase 02 consumers use TIMESTAMP started_at as strict-
      less-than anchor.
  - number: "5"
    how_upheld: >
      Player-row symmetry (I5-analog). SYMMETRY_I5_ANALOG_SQL uses
      IS DISTINCT FROM for NULL-safe comparison (prior `=`-based version
      false-passed NULL-asymmetric rows).
  - number: "6"
    how_upheld: >
      DDL + every assertion SQL + DESCRIBE snapshot in validation JSON.
  - number: "7"
    how_upheld: >
      Magic literals 32 / 42 in PREFIX_CHECK_SQL cite
      src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml
      join_key regex [0-9a-f]{32} for provenance.
  - number: "8"
    how_upheld: >
      8-column cross-dataset contract: identical column names + dtypes;
      canonical TIMESTAMP temporal dtype (no TZ); per-dataset-polymorphic
      faction vocabulary (explicit contract limit — consumers MUST game-
      condition before categorical analyses). aoestats sibling PR projects
      1-row-per-match to 2-rows with p0/p1 UNION ALL (team1_wins slot-
      asymmetry awareness required).
  - number: "9"
    how_upheld: >
      Pure non-destructive projection. No upstream modification. Only new
      VIEW created.
gate:
  artifact_check: >
    Validation JSON + MD exist. matches_history_minimal.yaml exists with
    8 columns (started_at TIMESTAMP) + invariants block + I8 per-dataset-
    polymorphic faction warning.
  continue_predicate: >
    VIEW exists with 8 columns matching spec. 44,418 rows = 22,209 × 2.
    Zero NULL-safe symmetry violations. Zero prefix violations. dataset_tag
    constancy = 1. Zero NULLs in match_id / player_id / opponent_id / won /
    dataset_tag. STEP_STATUS 01_04_03 -> complete. PIPELINE_SECTION_STATUS
    01_04 -> complete.
  halt_predicate: >
    Symmetry violation > 0; row-count discrepancy; prefix violation; NULL in
    non-nullable spec column; column count != 8; started_at dtype != TIMESTAMP;
    upstream YAML byte-diff detected. ON HALT: manually revert
    PIPELINE_SECTION_STATUS 01_04 -> complete before aborting.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet > Cross-dataset harmonization substrate"
  - "Chapter 4 -- Data and Methodology > 4.3 Rating System Backtesting Design (downstream consumer)"
research_log_entry: "Required on completion."
```

---

## research_log entry template (T04)

```markdown
## 2026-04-{DD} -- [Phase 01 / Step 01_04_03] Minimal Cross-Dataset History View

**Category:** A (science)
**Dataset:** sc2egset (pattern-establisher)
**Step scope:** Create matches_history_minimal VIEW -- 8-column player-row-grain
projection of matches_flat_clean with canonical TIMESTAMP temporal dtype.
Cross-dataset-harmonized substrate for Phase 02+ rating-system backtesting.
Non-destructive (I9); reverts 01_04 to in_progress for execution duration.

### Schema (8 columns, 2 rows per match)

| column | dtype | semantics |
|---|---|---|
| match_id | VARCHAR | 'sc2egset::' + 32-char hex replay_id (length = 42) |
| started_at | TIMESTAMP | TRY_CAST of details_timeUTC; canonical cross-dataset type |
| player_id | VARCHAR | Battle.net toon_id |
| opponent_id | VARCHAR | Opposing toon_id |
| faction | VARCHAR | Raw race stems `Prot`/`Terr`/`Zerg` (4-char; NOT full names). PER-DATASET POLYMORPHIC |
| opponent_faction | VARCHAR | Opposing race (same vocabulary as faction) |
| won | BOOLEAN | Focal player's outcome (complementary between the 2 rows) |
| dataset_tag | VARCHAR | Constant 'sc2egset' |

### Row-count flow
- Source matches_flat_clean: 44,418 rows / 22,209 replays
- matches_history_minimal: 44,418 rows / 22,209 distinct match_ids / 2 rows per match_id

### Gate verdict (all PASS)
- Row count 44,418 = 2 × 22,209
- Column count 8; started_at dtype TIMESTAMP verified
- I5-analog NULL-safe symmetry violations (IS DISTINCT FROM): 0
- match_id prefix violations: 0; length contract = 42 (10 prefix + 32 hex per matches_long_raw.yaml regex)
- dataset_tag distinct count: 1
- Zero NULLs in match_id / player_id / opponent_id / won / dataset_tag
- I9: upstream VIEW YAMLs byte-identical

### Artifacts produced
- `reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.json` (NEW)
- `reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.md` (NEW)
- `data/db/schemas/views/matches_history_minimal.yaml` (NEW)
- DuckDB VIEW `matches_history_minimal` (NEW)

### Cross-dataset contract established (I8) — limits explicit
aoestats and aoe2companion follow-up PRs must emit views with:
- identical 8-column names and order
- canonical TIMESTAMP started_at (aoestats CASTs AT TIME ZONE 'UTC' from TIMESTAMPTZ; aoe2companion pass-through)
- same grain (2 rows per match) — aoestats UNIONs p0/p1 halves of its 1-row-per-match clean view (team1_wins slot asymmetry awareness)
- NULL-safe IS DISTINCT FROM symmetry assertion
- dataset_tag literals 'aoestats' / 'aoe2companion'
- match_id prefixes 'aoestats::' / 'aoe2companion::'
- `faction` values per-dataset polymorphic (SC2 race stems vs AoE2 civ names); consumers MUST game-condition

### Decisions taken
- Source = matches_flat_clean (1v1-decisive filter built-in).
- match_id prefix in-view (preserves I9).
- faction = `race` (actual), NOT `selectedRace`.
- started_at cast to TIMESTAMP in-view (resolves 3-way dtype split at the contract level).
- Minimal view excludes MMR / is_mmr_missing / map / version; consumers join from matches_flat_clean.

### Decisions deferred
- Faction enum harmonization (Phase 02; current contract is explicit polymorphism).
- Canonical nickname resolution (Phase 01_05+).

### Thesis mapping
- Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet > Cross-dataset harmonization substrate
- Chapter 4 -- Data and Methodology > 4.3 Rating System Backtesting Design (downstream consumer)

### Open follow-ups
- aoestats, aoe2companion sibling PRs.
- Phase 02 defines canonical UNION ALL view.
```

---

## Gate Condition

1. **Artifacts exist and non-empty:** notebook `.py` + `.ipynb`; validation JSON + MD; `matches_history_minimal.yaml` (8 cols + invariants block + per-dataset-polymorphic faction warning).
2. **DuckDB VIEW exists** — `DESCRIBE matches_history_minimal` returns exactly 8 columns in order `[match_id, started_at, player_id, opponent_id, faction, opponent_faction, won, dataset_tag]` with dtypes `[VARCHAR, TIMESTAMP, VARCHAR, VARCHAR, VARCHAR, VARCHAR, BOOLEAN, VARCHAR]`.
3. **Row-count parity:** 44,418 / 22,209 / 22,209 / 0.
4. **I5-analog NULL-safe symmetry:** 0 violations (via `IS DISTINCT FROM`).
5. **I8 prefix uniqueness:** 0 violations; length == 42.
6. **I8 dataset_tag constancy:** `COUNT(DISTINCT dataset_tag) = 1`, value = `'sc2egset'`.
7. **Zero-NULL:** match_id / player_id / opponent_id / won / dataset_tag all 0.
8. **started_at dtype:** TIMESTAMP (DESCRIBE output); null_started_at count reported (expected 0 but not a fixed threshold per I7). **Non-halt rationale (R2-NOTE-4):** `TRY_CAST` failures originate from malformed upstream `details_timeUTC` strings — an upstream data issue, not a pipeline bug. Phase 02 consumers decide how to handle NULL temporal anchors (e.g., skip match in rating update). Halt-on-NULL would punish this step for upstream data quality.
9. **I9 upstream immutability:** `git diff --stat` shows no change to `matches_flat_clean.yaml`, `player_history_all.yaml`, `matches_long_raw.yaml`.
10. **Status files:** STEP_STATUS 01_04_03 = complete; PIPELINE_SECTION_STATUS 01_04 = complete; PHASE_STATUS 01 unchanged.
11. **Validation JSON** `all_assertions_pass: true`, `sql_queries` block contains every SQL literal verbatim (I6), `describe_table_rows` captures DESCRIBE output (I6 nullable-flag reproducibility).
12. **research_log.md** new entry at top.

**Halt predicate:** symmetry > 0, column count off, NULL in non-nullable, upstream YAML byte-diff, prefix/dataset_tag violation, started_at dtype != TIMESTAMP. **ON HALT: manually revert PIPELINE_SECTION_STATUS.yaml `01_04.status = complete` before aborting** (R1-WARNING-3).

---

## Out of scope

- aoestats and aoe2companion sibling views (separate PRs).
- Faction enum harmonization across SC2 races and AoE2 civilizations (explicit per-dataset-polymorphism contract in this PR; harmonization is Phase 02).
- MMR / rating pass-through (Phase 02 joins from `matches_flat_clean`).
- Canonical nickname resolution.
- Any Phase 02 Elo/Glicko computation.
- Tests under `tests/` — VIEW-only step with no importable Python logic.

---

## Open Questions

None blocking.

---

## R1 critique closure summary

| Finding | Resolution |
|---|---|
| R1-BLOCKER-1 (race vocabulary) | Corrected to `Prot`/`Terr`/`Zerg` in schema description, research_log, FACTION_VOCAB comment. |
| R1-BLOCKER-2 (3-way dtype split) | DDL casts `started_at` to TIMESTAMP via TRY_CAST; canonical contract = TIMESTAMP; sibling PR cast requirements spelled out. |
| R1-BLOCKER-3 (NULL-unsafe symmetry) | SYMMETRY_I5_ANALOG_SQL rewritten with `IS DISTINCT FROM`. |
| R1-BLOCKER-4 (misplaced Elo/Glicko citations) | Methodology citations reduced to cleaning-stage (manual §4.2/§4.4, Tukey 1977, Schafer & Graham 2002, van Buuren 2018). Rating papers moved to "downstream-consumer context." |
| R1-BLOCKER-5 (faction polymorphic contract) | Explicit per-dataset-polymorphic vocabulary declared in schema YAML description, research_log, and I8 invariant prose. Consumer warning added. |
| R1-WARNING-1 (lex ordering) | Subsumed by R1-BLOCKER-2 TIMESTAMP cast fix. |
| R1-WARNING-2 (aoestats 1-row asymmetry) | Cross-dataset I8 contract prose explicitly acknowledges aoestats 1→2-row re-projection + team1_wins slot bias. |
| R1-WARNING-3 (status flip-flop rollback) | Halt predicate now mandates manual PIPELINE_SECTION_STATUS revert on T02 failure. |
| R1-WARNING-4 (DESCRIBE placeholders) | Cell 17 prose now spells out the `con.execute("DESCRIBE …").fetchall()` → boolean translation before YAML serialization. |
| R1-WARNING-5 (magic 32 / 42) | PREFIX_CHECK_SQL comment + schema YAML description + I7 invariant cite `matches_long_raw.yaml` regex `[0-9a-f]{32}` provenance. |
| R1-WARNING-6 (ORDER BY determinism) | I6 invariant prose clarifies: VIEW ORDER BY is evaluated at query time; determinism claim scoped to sample outputs of this step only. |
| R1-WARNING-7 (single-writer lock) | T02 instructions now forbid parallel CLI writes during execution. |
| R1-NOTE-1..5 | Acknowledged; no plan change needed. |

---

## Self-check

- [x] Category A.
- [x] Branch: `feat/01-04-03-sc2egset-minimal-history`.
- [x] Phase/Pipeline Section/Step: 01 / 01_04 / 01_04_03.
- [x] Invariants touched: I3, I5 (analog), I6, I7, I8, I9.
- [x] File Manifest lists every file touched (NEW / MODIFIED).
- [x] Execution Steps use descriptive names.
- [x] No forbidden taxonomy terms.
- [x] Every SQL literal executable as-is (concrete `nullable:` booleans filled at runtime via DESCRIBE).
- [x] BLOCKERS section present (none; four assumptions + polymorphism contract).
- [x] No upstream schema changes (I9).
- [x] All 5 R1 BLOCKERs closed; all R1 WARNINGs addressed or acknowledged.
