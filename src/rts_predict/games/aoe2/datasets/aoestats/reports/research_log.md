# Research Log — AoE2 / aoestats

Thesis: "A comparative analysis of methods for predicting game results
in real-time strategy games, based on the examples of StarCraft II and
Age of Empires II."

AoE2 / aoestats findings. Reverse chronological.

---

## 2026-04-15 — [Phase 01 / Step 01_02_04] Univariate Census & Target Variable EDA

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** query
**Artifacts produced:**
- `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md`
- `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json`

### What

Full univariate census of matches_raw (30,690,651 rows, 18 cols) and players_raw (107,627,584 rows, 14 cols). Covers NULL landscape, cardinality, categorical frequency distributions, numeric descriptive statistics with skewness/kurtosis, ELO sentinel analysis, join integrity, duplicate detection, and preliminary temporal-leakage field classification per Invariant #3. All SQL embedded in .md artifact (Invariant #6). Note: overviews_raw (1 row, 9 cols) was documented in 01_02_01/01_02_03 and is not a per-match profiling target.

### Tables profiled

| Table | Rows | Columns |
|-------|------|---------|
| `matches_raw` | 30,690,651 | 18 |
| `players_raw` | 107,627,584 | 14 |

### NULL landscape

**matches_raw:** Near-zero nulls. Only `raw_match_type` has any nulls (12,504 rows, 0.04%). All other 17 columns fully populated.

**players_raw — four columns with extreme null rates (co-occurring on ~86% of rows):**
- `feudal_age_uptime`: 87.08% NULL (93.7M rows)
- `castle_age_uptime`: 87.93% NULL (94.6M rows)
- `imperial_age_uptime`: 91.49% NULL (98.5M rows)
- `opening`: 86.05% NULL (92.6M rows)

Co-occurrence confirmed: exactly 92,616,290 rows have all four NULL simultaneously — this is the pre-schema-change population (earlier weekly files lacking these columns), not individual missing values. Imputation is not meaningful for these columns.

### Target variable (`winner`)

Zero nulls across all 107.6M rows. Near-perfect 50/50 balance: 53,811,187 true (50.00%) vs 53,816,397 false (50.00%). No class imbalance mitigation required.

### Match size distribution

- 1v1 (num_players=2): 60.56% of rows — primary modelling scope
- 4-player: 16.48%; 8-player: 14.04%; 6-player: 8.92%
- Odd player counts (1, 3, 5, 7): 1,067 rows — data quality anomalies, filter in cleaning

### ELO / rating analysis

- `avg_elo` in matches_raw: mean 1,087.6, median 1,055.0, std 309.5. 121 rows with avg_elo=0 (unrated matches; not sentinel -1). Sentinel -1 affects < 0.001% of team_0/team_1_elo rows.
- `old_rating` in players_raw: mean 1,091.1, median 1,066.0, std 286.9 — **the authoritative pre-game rating column.** 5,937 zero-valued rows.
- `new_rating`: mean 1,090.8 — post-game column (must never be used as a feature, Invariant #3).
- `match_rating_diff`: mean 0.0, symmetric, but extreme kurtosis (65.7); range [-2,185, +2,185]. Leakage status unresolved: could be (new_rating - old_rating) = post-game, or (player_elo - opponent_elo) = pre-game. Verification query documented but not yet executed.
- Usable ELO fraction: effectively 100%. Sentinel -1 affects < 0.001% of matches.

### Categorical distributions

**matches_raw:**
- `map`: 93 distinct values. Top: arabia 34.94%, arena 19.02%, nomad 6.94%, black_forest 6.42%
- `leaderboard`: random_map 58.52%, team_random_map 37.53%
- `game_type`: constant "random_map" (100%) — dead column
- `game_speed`: constant "normal" (100%) — dead column
- `starting_age`: 99.99%+ "dark" (19 non-"dark" rows) — dead column
- `patch`: 19 distinct values; largest patch_125283 at 17.83%
- `mirror` (same-civ matchup): 2.32%

**players_raw:**
- `civ`: 50 distinct civilizations. Top: franks 5.59%, mongols 5.24%, persians 4.29%, britons 4.03%
- `opening` (non-null only, 15M rows): fast_castle 27.98%, unknown 23.91%, scouts 14.10%, archers 13.15%
- `team`: perfectly balanced at 50/50

### Temporal leakage audit (Invariant #3)

**Post-game (must exclude):** `duration`, `irl_duration`, `new_rating`

**In-game (unavailable at prediction time):** `opening`, `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime`, `replay_summary_raw`

**Deferred — leakage unknown:** `match_rating_diff` — requires empirical verification before Phase 02 feature engineering

**Safe pre-game features:** `map`, `started_timestamp`, `num_players`, `avg_elo`, `team_0_elo`, `team_1_elo`, `leaderboard`, `patch`, `raw_match_type`, `mirror`, `starting_age` (matches_raw); `team`, `civ`, `old_rating` (players_raw)

### Duration distribution

Mean 2,613.7s (~43.6 min), median 2,619.7s. Extreme right skew (skewness 1,032.6) from outliers up to 5,574,815s (~64 days). 2.33% IQR outliers above 5,496s. IRL duration mean 1,537.5s (~25.6 min).

### Data quality flags

- **Orphans:** 0 player rows without a match; **212,890 match rows without any players** (0.69%) — corresponds to the 1-week file gap identified in 01_01_01
- **Duplicates:** matches_raw has 0 on game_id (30,690,651 distinct). players_raw has 489 duplicate (game_id, profile_id) pairs — negligible
- **profile_id** range: min 18, max 24,853,897 — below 2^53, no precision loss from DOUBLE promotion

### Decisions taken

- `new_rating` classified post-game and flagged for exclusion
- `game_type`, `game_speed`, `starting_age` classified as dead constant columns — will be dropped
- `opening` and age uptimes classified as in-game features (available for only ~14% of player rows)
- `match_rating_diff` leakage test deferred to a targeted verification query before Phase 02

### Decisions deferred

- `match_rating_diff` verification: `SELECT COUNT(*) FROM players_raw WHERE ABS(match_rating_diff - (new_rating - old_rating)) < 0.01` — must execute before Phase 02
- ELO=0 interpretation (0 = valid unrated or sentinel?) — low priority given 4,824 occurrences
- Imputation strategy for `opening`/age uptimes (86-91% NULL) — likely not imputable; schema change pattern
- Handling of 212,890 orphan matches without player data
- Whether to restrict modelling scope to 1v1 (60.56%) vs including team games

### Thesis mapping

- Chapter 4, section 4.1.2 — AoE2 dataset: target distribution, ELO landscape, field classification
- Chapter 4, section 4.2 — Pre-processing: post-game column exclusion, dead column identification
- Chapter 5, section 5.1 — Feature catalogue: pre-game candidates enumerated

### Open questions / follow-ups

- Is `match_rating_diff` the pre-match ELO gap (high-value pre-game feature) or the post-match rating change (leakage)? This is the critical open question. Verification query is ready.
- Should 1v1 only or all team sizes be included in the modelling scope?
- Can overviews_raw civs/openings/patches reference arrays decode numeric IDs or enrich civ metadata?
- The 86% null rate on opening/age uptimes — exclude entirely, or use for the 14% subset?

---

## 2026-04-14 — [Phase 01 / Step 01_02_03] Raw schema DESCRIBE

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** query
**Artifacts produced:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_03_raw_schema_describe.json`
- `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/matches_raw.yaml`
- `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/players_raw.yaml`
- `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/overviews_raw.yaml`

### What

Captured the exact DuckDB column names and types for all three aoestats `*_raw` tables by connecting read-only to the persistent DuckDB and running `DESCRIBE` on each table.

### Why

Establish the source-of-truth bronze-layer schema for downstream steps. The `data/db/schemas/raw/*.yaml` files are consumed by feature engineering and documentation steps. Invariant #6 — DESCRIBE SQL embedded in artifact.

### How (reproducibility)

Notebook: `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_03_raw_schema_describe.py`

Read-only connection to `data/db/db.duckdb`. `DESCRIBE <table>` for each of the three `*_raw` tables.

### Findings

| Table | Columns | Notable types |
|-------|---------|---------------|
| matches_raw | 18 | `started_timestamp` TIMESTAMP WITH TIME ZONE; `duration`/`irl_duration` BIGINT (nanoseconds); `raw_match_type` DOUBLE |
| players_raw | 14 | `winner` BOOLEAN (prediction target); `profile_id` DOUBLE; age uptimes DOUBLE; `opening` VARCHAR |
| overviews_raw | 9 | `civs`/`openings`/`patches`/`groupings`/`changelog` are STRUCT arrays; `tournament_stages` VARCHAR[] |

Key observations:
- `winner` (BOOLEAN, nullable) in `players_raw` confirmed as prediction target
- `profile_id` remains DOUBLE (promoted from int64/double variant source) — precision-loss risk flagged in 01_02_01 still open
- `duration`/`irl_duration` are BIGINT nanoseconds (Arrow `duration[ns]` promoted) — requires `/1e9` conversion for seconds in downstream queries
- `overviews_raw` has deeply nested STRUCT columns — reference metadata only, not a feature source
- All three schema YAMLs populated in `data/db/schemas/raw/`

### Decisions taken

- Schema YAMLs populated from this DESCRIBE output — source-of-truth for all downstream steps
- No schema modifications — read-only step

### Decisions deferred

- `profile_id` DOUBLE→BIGINT cast precision check — deferred to Step 01_04 (data cleaning)
- Column descriptions (`TODO: fill`) in `*.yaml` — deferred to 01_03

### Thesis mapping

- Chapter 4, §4.1.2 — AoE2 dataset: bronze-layer schema catalog

### Open questions / follow-ups

- Does `profile_id` DOUBLE cause precision loss for any actual ID values in this dataset? (deferred to 01_04)

---

## 2026-04-14 — [Phase 01 / Step 01_02_02] DuckDB Ingestion

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** ingestion
**Artifacts produced:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.json`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.md`

### What

Re-executed full ingestion of all three aoestats raw sources into the persistent DuckDB (`data/db/db.duckdb`). Supersedes the initial ingestion performed within 01_02_01 by applying Invariant I10-compliant relative filenames and renaming tables from `raw_*` prefix to `*_raw` suffix convention.

### Why

Invariant I10 required `filename` column to store paths relative to `raw_dir`. Table naming aligned with `*_raw` suffix convention used by sc2egset and aoe2companion. All ingestion SQL lives in `src/rts_predict/games/aoe2/datasets/aoestats/ingestion.py`.

### How (reproducibility)

Notebook: `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_02_duckdb_ingestion.py`

### Findings

Row counts:
- `matches_raw`: 30,690,651 rows
- `players_raw`: 107,627,584 rows
- `overviews_raw`: 1 row

Row counts match the 01_02_01 initial ingestion, confirming data integrity.

Ingestion strategy:
- `matches_raw` / `players_raw`: `read_parquet` with `union_by_name=true`, `filename=true`, loaded in file-level batches (default 10 files per batch) — `CREATE TABLE ... AS SELECT` for the first batch, `INSERT INTO ... BY NAME SELECT` for subsequent batches. Batching avoids OOM on the full 171-file / 107.6M-row `players_raw` set.
- `overviews_raw`: `read_json_auto` on singleton `overview.json`, `filename=true`
- Invariant I10 (relative filenames): enforced inline via `SELECT * REPLACE (substr(filename, {prefix_len}) AS filename)` in every CTAS and INSERT query. Post-load `UPDATE SET filename = substr(...)` was removed because it caused OOM on the 107.6M-row `players_raw` table. Only `overviews_raw` (1 row) uses post-load UPDATE.

### Decisions taken

- Tables named with `*_raw` suffix convention — consistent with sc2egset and aoe2companion
- File-level batched loading (CREATE + INSERT BY NAME) for `matches_raw` and `players_raw` to avoid OOM; default `batch_size=10` files per batch
- Invariant I10 via inline `SELECT * REPLACE` — no post-load UPDATE on large tables

### Artifact note

The `.json` artifact (`01_02_02_duckdb_ingestion.json`) is a minimal stub containing only row counts — no SQL, schema, NULL rates, or I10 verification. Both artifacts should be regenerated from a fresh notebook run. The discrepancy is tracked here.

### Decisions deferred

- None for this step

### Thesis mapping

- Chapter 4, §4.1.2 — AoE2 dataset: bronze-layer ingestion

### Open questions / follow-ups

- None specific to this step — all open questions from 01_02_01 remain active

---

> **2026-04-14 amendment:** The original 01_02_01 heading says "DuckDB pre-ingestion investigation" but the artifact (`01_02_01_duckdb_pre_ingestion.json`) has `"type": "full_ingestion"` and contains `tables_created`, DDL, DESCRIBE output, and NULL counts — it performed full ingestion, not just investigation. The body accurately states "Ingested all three raw data sources" but the heading and step scope label are misleading. The canonical ingestion is step 01_02_02, which re-executed with Invariant I10-compliant relative filenames and renamed tables (`raw_matches` → `matches_raw`, `raw_players` → `players_raw`, `raw_overviews` → `overviews_raw`). Findings in the 01_02_01 entry (variant columns, NULL counts, duration types, missing week) remain valid.

## 2026-04-13 — [Phase 01 / Step 01_02_01] DuckDB pre-ingestion investigation

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** query
**Artifacts produced:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json`

### What

Ingested all three raw data sources into DuckDB (`matches_raw`, `players_raw`,
`overviews_raw`) and validated types, null rates, and variant column behaviour
against 01_01_02 schema discovery findings.

### Why

Materialise the bronze layer. This dataset has known variant columns
(type changes across weekly Parquet files) requiring `union_by_name=true`.
Invariant #7 (type fidelity) — verify DuckDB's automatic type promotion.

### How (reproducibility)

Notebook: `sandbox/aoe2/aoestats/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py`

### Findings

- `matches_raw`: 30.7M rows, 18 columns. Two variant columns: `started_timestamp` (mixed us/ns precision across files, promoted to TIMESTAMP WITH TIME ZONE), `raw_match_type` (mixed int64/double, promoted to DOUBLE)
- `players_raw`: 107.6M rows, 14 columns. Five variant columns: `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime` (double in 82/81/81 files, null-typed in 89/90/90 files — promoted to DOUBLE with NULL fill); `profile_id` (int64 in 135 files, double in 36 files — promoted to DOUBLE); `opening` (string in 82 files, null-typed in 89 — promoted to VARCHAR)
- `overviews_raw`: 1 row, 9 columns. Contains STRUCT arrays for civs, openings, patches, groupings, changelog
- `duration` and `irl_duration` mapped from Arrow duration[ns] to BIGINT nanoseconds (not INTERVAL as might be expected)
- `profile_id` as DOUBLE: precision loss risk for IDs > 2^53, but only 1,185 NULLs out of 107.6M rows
- Missing week: `2025-11-16_2025-11-22` has matches but no player-level data (1 week gap out of 172)

### Decisions taken

- Raw layer uses `SELECT *` with `union_by_name=true, filename=true` — let DuckDB handle type promotion at bronze layer
- `profile_id` DOUBLE type flagged but not altered — precision check deferred to cleaning step
- Duration stored as BIGINT nanoseconds — will need division by 1e9 for seconds in queries

### Decisions deferred

- `profile_id` DOUBLE→BIGINT cast: need to verify no precision loss for actual ID values in the dataset
- Whether the 89 null-typed `opening` files represent a schema change or genuinely absent data
- Whether `feudal_age_uptime` NULLs (87% of rows) indicate games not reaching Feudal Age or missing data

### Thesis mapping

- Chapter 4, §4.1.2 — AoE2 dataset description, variant column handling
- Chapter 4, §4.2.1 — Ingestion validation, DuckDB type promotion behaviour

### Open questions / follow-ups

- Is `profile_id` precision loss actually occurring for any real IDs in this dataset?
- What caused the schema break in player files around week 89/172 (~mid-2024)?
- Are the age uptime NULLs meaningful (game ended before that age) or data quality issues?

---

## 2026-04-13 — [Phase 01 / Step 01_01_02] Schema discovery

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** content
**Artifacts produced:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`

### What

Full census of all 344 Parquet files plus the singleton overview JSON.
Catalogued column names, physical types, nullability, and critically —
variant columns where physical type changes across weekly files.

### Why

Map the exact schema per file, identifying type inconsistencies that will
affect DuckDB ingestion. Invariant #6 requires knowing field types.

### How (reproducibility)

Notebook: `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_02_schema_discovery.py`

### Findings

- Matches: 17 columns, 2 variant columns (`started_timestamp` mixed us/ns precision, `raw_match_type` mixed int64/double)
- Players: 13 columns, 5 variant columns (`feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime` appear as double or null-typed; `profile_id` appears as int64 or double; `opening` appears as string or null-typed)
- Overview: singleton JSON with nested STRUCT arrays (civs, openings, patches, groupings, changelog)
- `duration` and `irl_duration` are Arrow duration[ns] type (not timestamp)

### Decisions taken

- Full census used (344 files is manageable)
- Variant columns documented with exact file counts per type — critical input for ingestion

### Decisions deferred

- How to handle variant columns at ingestion — deferred to 01_02_01

### Thesis mapping

- Chapter 4, §4.1.2 — AoE2 dataset schema, variant column documentation

### Open questions / follow-ups

- Why do player files switch from having `opening`/age uptimes to not having them mid-dataset?
- Is the `profile_id` int64→double transition a data source version change?

---

## 2026-04-13 — [Phase 01 / Step 01_01_01] File inventory

**Category:** A (science)
**Dataset:** aoestats
**Step scope:** filesystem
**Artifacts produced:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`

### What

Catalogued the aoestats raw data directory: 3 subdirectories (matches, players,
overview), file counts, sizes, extensions, and temporal coverage via filename
date range parsing.

### Why

Establish the data landscape. Invariant #9 — filesystem-level inventory before
content inspection.

### How (reproducibility)

Notebook: `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py`

### Findings

- 349 total files across 3 subdirectories, 3.7 GB total
- Matches: 172 weekly Parquet files (611 MB), 2022-08-28 to 2026-02-07
- Players: 171 weekly Parquet files (3.2 GB), aligned with matches minus 1 week
- Overview: 1 singleton JSON (22 KB)
- 3 temporal gaps identified: 43-day gap at 2024-07-20→2024-09-01, plus two 8-day gaps
- File count mismatch: 172 match weeks vs 171 player weeks (1 week has matches but no players)

### Decisions taken

- Weekly granularity confirmed — files named by date range (e.g., `2022-08-28_2022-09-03`)
- Temporal gaps documented for downstream awareness

### Decisions deferred

- Internal file structure deferred to 01_01_02

### Thesis mapping

- Chapter 4, §4.1.2 — AoE2 dataset description, temporal coverage, data gaps

### Open questions / follow-ups

- Is the 43-day gap (July–September 2024) a data collection outage or intentional?
