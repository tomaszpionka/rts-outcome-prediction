# Research Log — SC2 / sc2egset

Thesis: "A comparative analysis of methods for predicting game results
in real-time strategy games, based on the examples of StarCraft II and
Age of Empires II."

SC2 / sc2egset findings. Reverse chronological.

---

## 2026-04-15 — [Phase 01 / Step 01_02_04] Univariate Census & Target Variable EDA

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** query
**Artifacts produced:**
- `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md`
- `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json`

### What

Extracted 17 fields from the STRUCT columns in `replays_meta_raw` (details, header, initData, metadata) into a flat `struct_flat` working table, then ran a full univariate census across all six sc2egset data objects: NULL rates, cardinality, numeric descriptive statistics, sentinel detection, value distributions, temporal range, duplicate detection, and field-level pre-game/in-game/identifier/target/constant classification per Invariant #3. All SQL embedded in .md artifact (Invariant #6).

### Tables profiled

| Object | Type | Rows | Columns |
|--------|------|------|---------|
| `replay_players_raw` | table | 44,817 | 25 |
| `struct_flat` (from replays_meta_raw) | derived | 22,390 | 18 |
| `map_aliases_raw` | table | 104,160 | 4 |
| `game_events_raw` | view | 608,618,823 | 4 |
| `tracker_events_raw` | view | 62,003,411 | 4 |
| `message_events_raw` | view | 52,167 | 4 |

### NULL landscape

Remarkably clean: **0% NULLs across all columns in every table and view.** This includes replay_players_raw (all 25 cols), struct_flat (all 18 extracted fields), map_aliases_raw, and all three event views. Zero-NULL data requires sentinel detection rather than NULL-based imputation strategies.

### Target variable (`result`)

- 4 distinct values: **Loss 50.00%** (22,409 rows), **Win 49.94%** (22,382 rows), Undecided 0.05% (24 rows), Tie 0.00% (2 rows)
- Near-perfect 50/50 balance is structural: each game produces one Win and one Loss row. No class imbalance mitigation needed.
- All 26 Undecided/Tie rows come from standard 2-player replays — these 13 replays lack a definitive outcome and must be excluded in cleaning (01_04).
- Zero duplicate rows on the `filename || '|' || toon_id` composite key.

### MMR analysis

- **83.65% of rows have MMR=0** (37,489 / 44,817). MMR=0 rate is uniform across Win (84.34%) and Loss (82.99%) — confirming zero is "not reported" not outcome-correlated.
- MMR=0 by league: Unknown 93.13%, Unranked 100%, even Master 57.96% and Grandmaster 60.27% majority zero. Consistent with SC2EGSet being tournament replays where MMR is often not exposed.
- Among the **7,328 non-zero rows (16.35%):** range -36,400 to 7,464. The negative minimum may represent another sentinel convention.
- MMR is a **pre-game feature** (ladder-rating snapshot at game time) — no leakage risk. The zero-MMR issue is a data-availability problem, not temporal leakage.
- Feature engineering options: (a) use MMR only for the 16% valid subset, (b) impute from historical player averages, (c) add binary missing-MMR indicator. Strategy deferred to Phase 02.

### SQ (Spending Quotient)

- 2 rows contain the INT32_MIN sentinel (-2,147,483,648), destroying raw statistics (raw mean: -95,711). Sentinel-excluded (N=44,815): **median 123, mean 122.38, std 18.91, range [-51, 187], IQR [110, 136].**
- SQ measures macro-economic efficiency (resource spending relative to income) computed from in-game actions — **post-game metric**, classified as `in_game`. Cannot be used as a pre-game feature.

### APM (Actions Per Minute)

- No sentinel issues. 1,132 rows (2.53%) with APM=0 (very short games or parse artifacts). **Median 349, mean 355.57, std 104.87, range [0, 1,248].**
- Post-game metric computed from full replay — classified as `in_game`.

### supplyCappedPercent

- **Median 6%, mean 7.24%, range [0, 100]**, 298 rows (0.67%) at zero. Right-skewed (skewness 2.25). Post-game metric — classified as `in_game`.

### game_events_raw scale

- 608.6M rows across 22,390 replays. **23 distinct evtTypeNames.** CameraUpdate alone: 387.5M rows (63.67%).
- `event_data` column has 528.5M distinct values (extreme cardinality); excluded from top_n/bottom_n profiling to avoid OOM.
- Histograms deferred for event tables per EDA Manual (608M rows, semantically heterogeneous — univariate histograms on `loop` are not analytically meaningful without event-type stratification).

### Temporal leakage classification (Invariant #3)

**Pre-game** (replay_players_raw): MMR, race, selectedRace, handicap, region, realm, highestLeague, isInClan, clanTag, startDir, startLocX, startLocY, color channels — all available before match start.

**In-game** (replay_players_raw): APM, SQ, supplyCappedPercent — computed from replay actions, post-game only.

**Pre-game** (struct_flat): time_utc, game_version_header/meta, base_build, data_build, map_name, max_players, map_size_x/y, is_blizzard_map.

**In-game** (struct_flat): elapsed_game_loops — game duration, known only after match ends.

**Constant / dead** (no predictive information): game_speed, game_speed_init (always "Faster"); gameEventsErr, messageEventsErr, trackerEvtsErr (always FALSE).

### Categorical highlights

- `race`: Protoss 36.21%, Zerg 35.02%, Terran 28.76%. 3 BW-prefixed anomalous entries.
- `selectedRace`: 1,110 rows (2.48%) with empty string (Random resolved post-game); 10 explicit "Rand" rows.
- `highestLeague`: 72.16% "Unknown" — esports replays rarely expose ladder rank.
- `region`: Europe 46.91%, US 28.34%, Unknown 12.83%, Korea 8.04%.
- `isInClan`: 25.9% True; 257 distinct clan tags.
- `handicap`: effectively constant at 100 (only 2 rows at 0) — dead column.

### map_aliases_raw

104,160 rows = 70 tournaments × 1,488 foreign names each. Maps foreign/localized tournament map names to English equivalents. Join key is `map_name` from struct_flat matched against `english_name` or `foreign_name` — **not via `filename`.** All tournaments have identical key sets.

### Decisions taken

- Field classification taxonomy established for all 25 replay_players_raw columns and 18 struct_flat columns; stored in JSON artifact under `field_classification`
- MMR=0 treated as "not reported" sentinel based on uniform distribution across result categories and league correlation
- SQ INT32_MIN sentinel identified (2 rows); sentinel-excluded statistics documented
- Event tables profiled for null/cardinality only; histogram profiling deferred

### Decisions deferred

- MMR imputation or filtering strategy — requires player identity resolution (Phase 02)
- Whether isInClan/clanTag carry win-rate signal — Phase 02 correlation analysis
- Cleaning of 13 Undecided/Tie replays, 11 non-2-player replays, 3 BW-prefixed race entries, 2 SQ sentinel rows — deferred to 01_04
- Whether to include in-game fields (APM, SQ, supplyCappedPercent) for an in-game prediction comparison framing — Phase 02 decision

### Thesis mapping

- Chapter 4, section 4.1.1 — SC2EGSet: data quality profile, target distribution, MMR availability, sentinel conventions
- Chapter 4, section 4.2.1 — Pre-game vs in-game field classification methodology

### Open questions / follow-ups

- Optimal MMR handling for 84% missing rows: imputation vs. indicator vs. subsetting (Phase 02)
- Do isInClan and clanTag carry win-rate signal beyond player identity? (Phase 02)
- The 3 BW-prefixed race entries — merge with SC2 counterparts or exclude? (01_04)
- 273 replays with map_size_x=0 and map_size_y=0 — parse artifact or real map configuration? (01_04)

---

## 2026-04-14 — [Phase 01 / Step 01_02_03] Raw schema DESCRIBE

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** query
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_03_raw_schema_describe.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replays_meta_raw.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replay_players_raw.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/map_aliases_raw.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/game_events_raw.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/tracker_events_raw.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/message_events_raw.yaml`

### What

Captured the exact DuckDB column names and types for all six sc2egset `*_raw` objects — three persistent tables and three event views — by connecting read-only to the persistent DuckDB populated in 01_02_02 and running `DESCRIBE` on each object.

### Why

Establish the source-of-truth bronze-layer schema for downstream steps. The `data/db/schemas/raw/*.yaml` files are consumed by feature engineering and documentation. Invariant #6 — DESCRIBE SQL embedded in artifact.

### How (reproducibility)

Notebook: `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_03_raw_schema_describe.py`

Read-only connection to `data/db/db.duckdb`. `DESCRIBE <object>` for all six `*_raw` tables and views.

### Findings

| Object | Type | Columns | Notable types |
|--------|------|---------|---------------|
| replays_meta_raw | table | 9 | STRUCT columns for details/header/initData/metadata; `ToonPlayerDescMap` VARCHAR; error flags BOOLEAN |
| replay_players_raw | table | 25 | `result` VARCHAR (prediction target); `MMR`/`APM`/`SQ`/`supplyCappedPercent` INTEGER; `highestLeague` VARCHAR; color channels INTEGER |
| map_aliases_raw | table | 4 | `tournament`/`foreign_name`/`english_name`/`filename` all VARCHAR, all NOT NULL |
| game_events_raw | view | 4 | `filename` VARCHAR, `loop` BIGINT, `evtTypeName` VARCHAR, `event_data` VARCHAR |
| tracker_events_raw | view | 4 | Identical 4-column schema to game_events_raw |
| message_events_raw | view | 4 | Identical 4-column schema to game_events_raw |

Key observations:
- `result` (VARCHAR, nullable) in `replay_players_raw` is the prediction target — stores string values, not a boolean; distinct values to be confirmed in 01_03
- `replay_players_raw` has 25 columns total — the full set including SQ, supplyCappedPercent, highestLeague, color channels; only 7 columns were NULL-checked in 01_02_02
- `ToonPlayerDescMap` confirmed VARCHAR (JSON text blob) in `replays_meta_raw`, as decided in 01_02_01
- All three event views share the identical 4-column generic schema; event type discriminated via `evtTypeName`
- `replay_players_raw.filename` and `map_aliases_raw` key columns all NOT NULL (confirmed by nullable=NO)
- All six schema YAMLs populated in `data/db/schemas/raw/`

### Decisions taken

- Schema YAMLs populated from this DESCRIBE output — source-of-truth for all downstream steps
- No schema modifications — read-only step

### Decisions deferred

- Full NULL profile for all 25 `replay_players_raw` columns
- Distinct values for `result` column
- Column descriptions (`TODO: fill`) in `*.yaml` — deferred to 01_03

### Thesis mapping

- Chapter 4, §4.1.1 — SC2EGSet: bronze-layer schema catalog

### Open questions / follow-ups

- What are the actual distinct values of `result`? Are 'Win'/'Loss' the only values, or are there draws/unknowns? (Investigate in 01_03)

---

## 2026-04-14 — [Phase 01 / Step 01_02_02] DuckDB ingestion

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** ingest
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.md`

### What

Materialised three `*_raw` DuckDB tables and three event DuckDB views from the
full 22,390-file sc2egset corpus (209 GB raw JSON) into the persistent database
at `src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb`. Event data
extracted to zstd-compressed Parquet under `IN_GAME_PARQUET_DIR` and registered
as DuckDB views for SQL access.

### Why

Enable SQL-based EDA for subsequent profiling (01_03) and cleaning (01_04).
All data — metadata, player stats, and in-game events — now accessible via
DuckDB queries without reading raw JSON files on every access. Invariants #6
(reproducibility), #7 (provenance), #9 (step scope), #10 (relative filenames)
upheld.

### How (reproducibility)

Notebook: `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_02_duckdb_ingestion.py`
Module: `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py`

### Findings

**Table row counts:**
| Table | Rows |
|-------|------|
| replays_meta_raw | 22,390 |
| replay_players_raw | 44,817 |
| map_aliases_raw | 104,160 |

**Event view row counts:**
| View | Rows |
|------|------|
| game_events_raw | 608,618,823 |
| tracker_events_raw | 62,003,411 |
| message_events_raw | 52,167 |

**NULL rates (tables):**
- replays_meta_raw: zero NULLs across all 6 checked columns (details, header,
  initData, metadata, ToonPlayerDescMap, filename)
- replay_players_raw: zero NULLs across all 7 checked columns (toon_id,
  nickname, MMR, race, result, APM, filename)
- map_aliases_raw: zero NULLs across all 4 columns; 70 distinct tournaments

**NULL rates (event views):**
- All three event views: zero NULLs across all 4 columns (filename, loop,
  evtTypeName, event_data)

**ToonPlayerDescMap type:** Confirmed VARCHAR (JSON text blob), not STRUCT.

**Cross-table integrity:** `orphan_player_files = 0` in both directions
(every replay_players_raw file exists in replays_meta_raw, and vice versa).
Event views also have zero orphan files — all 22,390 replay filenames
present in game_events_raw and tracker_events_raw; message_events_raw covers
22,260 files (130 replays have no message events, which is expected).

**Player count per replay:** 22,379 replays have exactly 2 players (99.95%),
3 replays have 1 player, 2 have 4, 1 has 6, 3 have 8, and 2 have 9.
11 total non-2-player replays — likely team games, FFA, or incomplete
replays; flagged for investigation in 01_04 (cleaning).

**map_aliases_raw dedup profile:** 1,488 unique foreign names, 215 unique
English names, 70 unique tournaments, 104,160 total rows. As expected from
01_02_01 — all 70 tournament mapping files have identical 1,488-entry key
sets.

**Top event types (game_events_raw):** CameraUpdate dominates at 387M events
(63.7%), followed by ControlGroupUpdate (69M), CommandManagerState (44M),
SelectionDelta (41M), Cmd (31M). These are mechanical-skill signals.

**Top event types (tracker_events_raw):** UnitBorn (22.4M), UnitDied (16.1M),
UnitTypeChange (11.0M), PlayerStats (4.6M). These are game-state signals
likely most relevant for outcome prediction features in Phase 02.

**Top event types (message_events_raw):** Chat (51.4K), Ping (714),
ReconnectNotify (41). Low volume; limited predictive value expected.

**filename column (Invariant I10):** All three tables and all three event
views store paths relative to `raw_dir` (no leading `/`). Cross-table and
cross-view join on `filename` has zero orphans, confirming the relative-path
strategy is consistent across all six data objects.

### Decisions taken

- Tables use `*_raw` suffix convention (bronze layer naming)
- `replays_meta_raw` loaded per-tournament (70 batch INSERT operations) to
  avoid OOM: a single CTAS over 22,390 files peaked at 22 GB RSS and triggered
  OS kills on a 36 GB machine. Per-tournament batching keeps peak RSS under
  5 GB.
- `_MAP_ALIASES_INSERT_QUERY` (SQL with `json_each`) replaced by pure Python
  `json.loads` + `executemany` for correctness and simplicity
- `_DEFAULT_MAX_OBJECT_SIZE` set to 160 MB (1.12x headroom over largest
  observed file at 143.1 MB)
- Event extraction uses single-pass batched approach: each JSON file read
  once, events routed to gameEvents/trackerEvents/messageEvents accumulators
  in the same loop iteration (3x I/O reduction vs sequential extraction)
- Events stored as zstd-compressed Parquet (not DuckDB tables) to avoid
  doubling storage; registered as DuckDB views for SQL access
- Event schema: 4 columns (filename, loop, evtTypeName, event_data) with
  event_data as JSON VARCHAR — flexible for downstream parsing without
  committing to a schema prematurely
- 11 non-2-player replays (3 single, 2 quad, 1 hex, 3 oct, 2 nona) retained
  as-is; deferred to cleaning step

### Decisions deferred

- Data cleaning (NULL rates and anomalies documented, not acted on). Deferred
  to pipeline section 01_04.
- Identity resolution (toon_id stored as-is). Deferred to Phase 02.
- NULL rate coverage for replay_players_raw extended columns (SQ,
  supplyCappedPercent, highestLeague, etc.) — only 7 of 25 columns checked.
  Full profiling deferred to pipeline section 01_03.

### Thesis mapping

Chapter 4, Section 4.1.1 — SC2EGSet: three-stream ingestion design,
ToonPlayerDescMap normalisation, `*_raw` bronze-layer convention, event
Parquet extraction rationale.

### Open questions

- What are the 11 non-2-player replays? Are they team games, FFA,
  observers, disconnects, or parse failures? (Investigate in 01_04)
- 130 replays have no message events — is this expected (players who never
  chatted/pinged) or a parse artefact?
- Are SQ, supplyCappedPercent, highestLeague columns fully populated or do
  they have NULLs? (Profiling in 01_03)

---

## 2026-04-13 — [Phase 01 / Step 01_02_01] DuckDB pre-ingestion investigation

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** query
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json`

### What

Investigated how DuckDB's `read_json_auto` handles SC2EGSet replay JSON files.
Tested single-file and batch (union_by_name) ingestion, measured event array
storage costs, probed ToonPlayerDescMap behaviour, and assessed mapping file
structure.

### Why

Determine the ingestion strategy for 22,390 replay files before committing to
a table layout. Invariant #7 (type fidelity) and #9 (step scope) apply.

### How (reproducibility)

Notebook: `sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py`

### Findings

- `read_json_auto` succeeds on all 7 sampled files (100% success rate), producing 11 root-level columns
- ToonPlayerDescMap is inferred as STRUCT with dynamic player-ID keys per file; with `union_by_name=true` it promotes to `MAP(VARCHAR, STRUCT(...))`
- Event arrays dominate file size: gameEvents ~327 GB, trackerEvents ~41 GB, messageEvents ~0.1 GB (total ~368 GB estimated across 22,390 files)
- Batch ingestion of 64 files from one tournament completed in 1.66 seconds within 24 GB memory limit
- Mean vs median storage estimates diverge significantly (right-skewed distribution) — median is the conservative estimate
- Mapping files (`map_foreign_to_english_mapping.json`): all 70 are flat `{str: str}` dicts with 1,488 entries each; cross-file consistency confirmed (all identical key sets)
- `read_json_auto` misinterprets mapping files as a single row with 1,488 columns — not suitable for direct DuckDB ingestion

### Decisions taken

- Three-stream split strategy: replay scalars (DuckDB), players normalised from ToonPlayerDescMap (DuckDB), events to zstd Parquet (not DuckDB)
- ToonPlayerDescMap stored as VARCHAR in `replays_meta` (text blob for provenance); normalised to per-player rows in `replay_players`
- Event Parquet extraction uses Python+PyArrow (not DuckDB) due to the heterogeneous STRUCT[] problem
- Every raw table includes `filename` column for provenance tracing

### Decisions deferred

- Whether mapping files need a DuckDB table at all — pending cross-tournament variation analysis and superset check (added to notebook section 7b)
- `profile_id` DOUBLE→BIGINT precision check deferred to aoestats investigation
- Filename uniqueness across tournaments — added as notebook section 1b, pending execution

### Thesis mapping

- Chapter 4, §4.1.1 — SC2EGSet dataset description, three-stream ingestion rationale
- Chapter 4, §4.2.1 — Ingestion and validation methodology

### Open questions / follow-ups

- Are replay filenames (MD5 hashes) unique across all 70 tournament directories? (section 1b)
- Do mapping files grow over time or are all 70 identical? (section 7b)
- What is the actual zstd compression ratio at scale? Smoke test showed 16.88x on one file.

---

## 2026-04-13 — [Phase 01 / Step 01_01_02] Schema discovery

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** content
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`

### What

Examined internal structure of SC2EGSet JSON replay files and mapping files.
Catalogued root-level keys, enumerated full keypath tree, analysed event array
struct heterogeneity, and checked schema consistency across all 70 tournament
directories.

### Why

Understand the data shape before designing ingestion. Invariant #6
(reproducibility) requires knowing exact field names and types.

### How (reproducibility)

Notebook: `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py`

### Findings

- 11 root-level keys per replay: ToonPlayerDescMap, details, gameEvents, gameEventsErr, header, initData, messageEvents, messageEventsErr, metadata, trackerEvents, trackerEvtsErr
- Schema consistent across all 70 directories (no era-dependent variation)
- 70 files checked for root schema, 210 for keypath enumeration
- Event arrays contain heterogeneous structs — gameEvents has 10+ distinct event types (CameraUpdate, SelectionDelta, Cmd, etc.), trackerEvents has 9+ (PlayerSetup, UnitBorn, PlayerStats, etc.)
- Nested sub-structures present within events (e.g., target positions, unit types)

### Decisions taken

- Systematic temporal stratification sampling: 1 file per directory for root schema, 3 per directory for keypaths
- Event array heterogeneity confirms that DuckDB's STRUCT[] union approach creates unusably wide schemas — separate extraction needed

### Decisions deferred

- Mapping file schema discovery added in this session (cell 5b) — pending notebook re-execution
- Ingestion strategy deferred to 01_02_01

### Thesis mapping

- Chapter 4, §4.1.1 — SC2EGSet schema description
- Appendix A — Full field catalog

### Open questions / follow-ups

- ToonPlayerDescMap field stability across eras (2016–2024)
- Exact sub-field types for metadata STRUCTs (details, header, initData, metadata)

---

## 2026-04-13 — [Phase 01 / Step 01_01_01] File inventory

**Category:** A (science)
**Dataset:** sc2egset
**Step scope:** filesystem
**Artifacts produced:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`

### What

Catalogued the SC2EGSet raw data directory: directory structure, file counts,
sizes, and extensions across all 70 tournament directories.

### Why

Establish the data landscape before any content inspection. Invariant #9
requires sequential step discipline.

### How (reproducibility)

Notebook: `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py`

### Findings

- Two-level layout: `raw/TOURNAMENT/TOURNAMENT_data/*.SC2Replay.json`
- 70 top-level tournament directories spanning 2016–2024
- 22,390 replay JSON files totalling 209 GB
- 431 metadata files (mapping files, summaries, processed mappings) at tournament root level
- All replay files have `.json` extension (no mixed formats)
- No directories missing `_data` subdirectory

### Decisions taken

- Layout confirmed as suitable for glob-based ingestion (`*/*_data/*.SC2Replay.json`)
- Tournament directory name serves as temporal/provenance key

### Decisions deferred

- Internal file structure deferred to 01_01_02

### Thesis mapping

- Chapter 4, §4.1.1 — SC2EGSet dataset description, data volume

### Open questions / follow-ups

- None — straightforward inventory step
