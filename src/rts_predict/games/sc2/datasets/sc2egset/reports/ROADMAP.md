# SC2EGSet Dataset Roadmap

**Game:** SC2
**Dataset:** sc2egset
**Canonical phase list:** `docs/PHASES.md`
**Methodology manuals:** `docs/INDEX.md`
**Step definition schema:** `docs/templates/step_template.yaml`
**Research log:** `research_log.md` (sibling file — per-dataset reverse-chronological narrative)

---

> **Role: TO BE DETERMINED.** Role assignment (PRIMARY vs
> SUPPLEMENTARY VALIDATION, per dimension D1–D6 in
> `reports/specs/01_06_readiness_criteria.md` §3) will be
> formalized at the Phase 01 Decision Gate (01_06) based on
> comparative data quality findings.

## How to use this document

This file decomposes Phases into Pipeline Sections and Steps for the sc2egset
dataset. The canonical Phase definitions and Pipeline Section enumerations live
in `docs/PHASES.md`. This ROADMAP does not invent Phases or Pipeline Sections;
it only decomposes them into Steps.

Steps are defined in a planning session before Phase work begins.

Steps are numbered `XX_YY_ZZ` where `XX` = Phase, `YY` = Pipeline Section,
`ZZ` = Step within that Pipeline Section.

---

## Source data

**SC2EGSet: StarCraft II Esport Replay and Game-state Dataset** — Zenodo v2.1.0.

Raw directory layout: `raw/TOURNAMENT/TOURNAMENT_data/*.SC2Replay.json`
(two-level: 70 tournament directories, each containing a `_data/` subdirectory
with `.SC2Replay.json` files and a `map_foreign_to_english_mapping.json` metadata
file at the tournament level).

File counts from 01_01_01 artifact:
- `.SC2Replay.json` files: 22,390
- Metadata files (`.zip`, `.log`, `.json` at tournament level): 431
- Files at root level: 3
- Total files scanned: 22,821
- Total `.SC2Replay.json` size: 214,060.62 MB

Directory name prefix range: `2016_` through `2024_` (70 directories).

Source: Białecki, A. et al. (2023). *SC2EGSet: StarCraft II Esport Replay
and Game-state Dataset.* Scientific Data 10(1), 600.
https://doi.org/10.1038/s41597-023-02510-7 — version 2.1.0 from Zenodo:
https://zenodo.org/records/17829625

---

## Phase 01 — Data Exploration

Pipeline Sections per `docs/PHASES.md`:

- `01_01` — Data Acquisition & Source Inventory
- `01_02` — Exploratory Data Analysis (Tukey-style)
- `01_03` — Systematic Data Profiling
- `01_04` — Data Cleaning
- `01_05` — Temporal & Panel EDA
- `01_06` — Decision Gates

### Step 01_01_01 — File Inventory

```yaml
step_number: "01_01_01"
name: "File Inventory"
description: "Establish a complete filesystem-level census of the sc2egset raw data. This grounds all subsequent steps in verified file counts, sizes, and directory structure."
phase: "01 — Data Exploration"
pipeline_section: "01_01 — Data Acquisition & Source Inventory"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 1"
dataset: "sc2egset"
question: "How many replay files exist, how large are they, and how are they distributed across the two-level tournament directory structure?"
method: "Full census of the raw directory tree. Count files, measure sizes, and group by tournament subdirectory. Report summary statistics (min/max/median replays per tournament) and flag structural anomalies (e.g., missing subdirectories)."
stratification: "By tournament directory (each tournament has its own _data/ subdir)."
predecessors: "none — independent"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py"
inputs:
  duckdb_tables: "none — reads filesystem only"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  report: "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "Inventory counts produced by code in the notebook, saved alongside the report."
  - number: "7"
    how_upheld: "Full census — no sampling or thresholds."
gate:
  artifact_check: "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json and .md exist and are non-empty."
  continue_predicate: "Inventory artifacts exist on disk."
  halt_predicate: "Raw directory does not exist or is empty."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_01_02 — Schema Discovery

```yaml
step_number: "01_01_02"
name: "Schema Discovery"
description: "Map the internal structure of sc2egset JSON replay files — root-level keys, nested keypaths, data types — and determine whether the schema is consistent across all 70 tournament directories (spanning 2016-2024)."
phase: "01 — Data Exploration"
pipeline_section: "01_01 — Data Acquisition & Source Inventory"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 1"
dataset: "sc2egset"
question: "What is the internal structure of the replay JSON files, and does it remain stable across tournament eras or evolve over time?"
method: "Sample files from each of the 70 directories (deterministic selection, stratified by tournament). Enumerate root-level keys and full keypath trees. Compare schemas across directories to detect era-dependent variation and report a consistency verdict. No DuckDB type proposals — deferred to ingestion design."
stratification: "By directory (all 70 represented; temporal range 2016-2024)."
predecessors:
  - "01_01_01"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_02_schema_discovery.py"
inputs:
  duckdb_tables: "none — reads raw JSON files directly"
  prior_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md, Section 1"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json"
  report: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "Schema profiles produced by code in the notebook, saved alongside the report."
  - number: "7"
    how_upheld: "Sample size per directory justified by temporal stratification in the report."
  - number: "9"
    how_upheld: "Conclusions limited to structural observations — no value distributions or semantic interpretation."
gate:
  artifact_check: "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json and .md exist and are non-empty."
  continue_predicate: "Schema artifacts exist and report a consistency verdict for all 70 directories."
  halt_predicate: "More than 30% of sampled files fail to parse."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_02_01 — DuckDB Pre-Ingestion Investigation

```yaml
step_number: "01_02_01"
name: "DuckDB Pre-Ingestion Investigation"
description: "Determine how sc2egset's deeply nested JSON (11 root keys, dynamic-key maps, 3 large event arrays) behaves when loaded into DuckDB, and decide on a table split strategy before committing to full ingestion."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 2"
dataset: "sc2egset"
question: "What does the raw data look like before we commit to an ingestion strategy — are there type inference traps, storage feasibility concerns for event arrays, or structural irregularities in the mapping files that need handling?"
method: "Smoke-test size-stratified file samples into in-memory DuckDB. DESCRIBE schemas, preview rows, and assess event array storage cost (extrapolated to full corpus). Test single-table vs split-table approaches on a mid-size tournament directory. Census all 70 tournament-level mapping files for schema consistency. Produce a design artifact with proposed DDL for a future full-ingestion step."
stratification: "By root key group (metadata vs events vs player desc map); by tournament directory for map alias files."
predecessors:
  - "01_01_01"
  - "01_01_02"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.py"
inputs:
  duckdb_tables:
    - "none — investigation uses temporary in-memory DB"
  prior_artifacts:
    - "artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
    - "artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "DuckDB 1.5.1 (pinned in pyproject.toml)"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json"
  report: "artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "All smoke-test SQL, storage measurements, and census code in the notebook."
  - number: "7"
    how_upheld: "File sample selection derived from 01_01_01 per-directory size data."
  - number: "9"
    how_upheld: "Conclusions limited to type mappings, storage estimates, and structural consistency — no content profiling."
gate:
  artifact_check: "artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json and .md exist and are non-empty."
  continue_predicate: "Design artifact documents: (1) read_json_auto behavior for all 11 root keys with DuckDB types, (2) proposed table split strategy with rationale, (3) event array storage estimate with SSD feasibility verdict, (4) full census of all 70 map_foreign_to_english_mapping.json files with cross-file consistency assessment and proposed DDL."
  halt_predicate: "read_json_auto cannot parse any sample file, OR batch ingestion of a single directory fails."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_02_02 — DuckDB Ingestion

```yaml
step_number: "01_02_02"
name: "DuckDB Ingestion"
description: "Materialise raw sc2egset data into persistent DuckDB tables using the three-stream strategy determined by 01_02_01. Stream 1 (replays_meta_raw): one row per replay with metadata STRUCT columns and ToonPlayerDescMap as VARCHAR. Stream 2 (replay_players_raw): normalised from ToonPlayerDescMap, one row per (replay, player). Stream 3 (events): optional Parquet extraction for gameEvents, trackerEvents, messageEvents. Also: map_aliases_raw table from all 70 tournament mapping files. filename column stores path relative to raw_dir (no absolute paths)."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 2"
dataset: "sc2egset"
question: "Can we materialise the three-stream ingestion strategy into persistent tables and verify row counts, column types, and NULL rates?"
method: "Call ingestion module functions against the persistent DuckDB. Validate with DESCRIBE, row counts, NULL rates on key fields. Verify ToonPlayerDescMap is VARCHAR, event arrays are excluded from replays_meta, and map_aliases has tournament provenance."
stratification: "By table (replays_meta_raw, replay_players_raw, map_aliases_raw)."
predecessors:
  - "01_02_01"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_02_duckdb_ingestion.py"
inputs:
  duckdb_tables:
    - "none — creates tables"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_01_duckdb_pre_ingestion.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "DuckDB 1.5.1 (pinned in pyproject.toml)"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.json"
  report: "artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "All ingestion SQL in the module, validation SQL in the notebook."
  - number: "7"
    how_upheld: "All tables carry filename provenance column."
  - number: "9"
    how_upheld: "Conclusions limited to ingestion success, row counts, column types, and NULL rates."
  - number: "10"
    how_upheld: "filename column in all tables stores path relative to raw_dir; no absolute paths."
gate:
  artifact_check: "artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.json and .md exist and are non-empty."
  continue_predicate: "All three DuckDB tables created with expected row counts. ToonPlayerDescMap is VARCHAR. All tables have filename column. filename values are relative paths (no leading /)."
  halt_predicate: "Any table creation fails OR row count is zero."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_02_03 — Raw Schema DESCRIBE

```yaml
step_number: "01_02_03"
name: "Raw Schema DESCRIBE"
description: "Establish the definitive column-name and column-type snapshot for every sc2egset *_raw object — three persistent tables (replays_meta_raw, replay_players_raw, map_aliases_raw) and three event views (game_events_raw, tracker_events_raw, message_events_raw). Connects read-only to the persistent DuckDB populated by 01_02_02 and runs DESCRIBE on all six objects. Output feeds the data/db/schemas/raw/*.yaml source-of-truth files consumed by all downstream steps."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 2"
dataset: "sc2egset"
question: "What are the exact column names and DuckDB types for all six sc2egset *_raw objects — the three persistent tables and three event views — as materialised in the persistent DuckDB?"
method: "Connect read-only to persistent DuckDB. DESCRIBE each *_raw table and view. Write JSON artifact. Populate data/db/schemas/raw/*.yaml schema files."
stratification: "By object (3 tables: replays_meta_raw, replay_players_raw, map_aliases_raw; 3 views: game_events_raw, tracker_events_raw, message_events_raw)."
predecessors:
  - "01_02_02"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_03_raw_schema_describe.py"
inputs:
  duckdb_tables:
    - "replays_meta_raw"
    - "replay_players_raw"
    - "map_aliases_raw"
    - "game_events_raw (view)"
    - "tracker_events_raw (view)"
    - "message_events_raw (view)"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_02_duckdb_ingestion.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "DuckDB 1.5.1 (pinned in pyproject.toml)"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_03_raw_schema_describe.json"
  schema_files:
    - "data/db/schemas/raw/replays_meta_raw.yaml"
    - "data/db/schemas/raw/replay_players_raw.yaml"
    - "data/db/schemas/raw/map_aliases_raw.yaml"
    - "data/db/schemas/raw/game_events_raw.yaml"
    - "data/db/schemas/raw/tracker_events_raw.yaml"
    - "data/db/schemas/raw/message_events_raw.yaml"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "All DESCRIBE SQL embedded in notebook; JSON artifact records exact schema seen."
  - number: "7"
    how_upheld: "Column types and nullability taken from DESCRIBE output, not assumed."
  - number: "9"
    how_upheld: "Read-only step — no tables or views modified."
  - number: "10"
    how_upheld: "filename column confirmed present in all six objects."
gate:
  artifact_check: "artifacts/01_exploration/02_eda/01_02_03_raw_schema_describe.json exists and non-empty. data/db/schemas/raw/*.yaml files populated for all six objects."
  continue_predicate: "Column counts confirmed: replays_meta_raw=9, replay_players_raw=25, map_aliases_raw=4, game_events_raw=4, tracker_events_raw=4, message_events_raw=4."
  halt_predicate: "Any object cannot be described or column count is zero."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

---

### Step 01_02_04 -- Metadata STRUCT Extraction & Univariate Census

```yaml
step_number: "01_02_04"
name: "Metadata STRUCT Extraction & Univariate Census"
description: "Flatten the four STRUCT columns from replays_meta_raw into scalar fields, run a full NULL census across all raw columns, and produce univariate statistical profiles (descriptive stats, zero counts, categorical distributions, skewness/kurtosis, sentinel detection) for all sc2egset raw fields."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
dataset: "sc2egset"
question: "What are the distributions of all raw fields, what NULLs and sentinels exist, and what is the temporal coverage of the dataset?"
method: "DuckDB SQL aggregations: NULL census, GROUP BY counts, descriptive statistics, skewness/kurtosis. Categorical cardinality via value_counts. Sentinel detection via range checks (INT32_MIN for SQ). Temporal coverage via monthly GROUP BY."
predecessors: "01_02_03"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_04_univariate_census.py"
```

### Step 01_02_05 -- Univariate EDA Visualizations

```yaml
step_number: "01_02_05"
name: "Univariate EDA Visualizations"
description: "14 visualization plots for the sc2egset univariate census findings from 01_02_04. Reads the 01_02_04 JSON artifact and queries DuckDB for histogram bin data. All plots saved to artifacts/01_exploration/02_eda/plots/. Temporal annotations on in-game columns (APM, SQ, supplyCappedPercent) and post-game column (elapsed_game_loops) per Invariant #3."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
dataset: "sc2egset"
question: "What do the distributions from 01_02_04 look like visually, and do the visual patterns confirm or challenge the statistical summaries?"
method: "Read 01_02_04 JSON artifact. Query DuckDB for histogram bins (MMR, APM, SQ, supplyCappedPercent, duration). Produce 14 plots: result 2-bar, categorical 3-panel (race/highestLeague/region), selectedRace bar, MMR split view, APM histogram (IN-GAME), SQ split view (IN-GAME), supplyCappedPercent histogram (IN-GAME), duration dual-panel (POST-GAME), MMR zero-spike cross-tab, temporal coverage line, isInClan bar, clanTag top-20, map top-20 barh, player repeat frequency. Markdown artifact with SQL queries."
predecessors: "01_02_04"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_05_visualizations.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
    - "replays_meta_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  plots:
    - "artifacts/01_exploration/02_eda/plots/01_02_05_result_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_categorical_bars.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_selectedrace_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_mmr_split.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_apm_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_sq_split.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_supplycapped_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_duration_hist.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_mmr_zero_interpretation.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_temporal_coverage.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_isinclan_bar.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_clantag_top20.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_map_top20.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_05_player_repeat_frequency.png"
  report: "artifacts/01_exploration/02_eda/01_02_05_visualizations.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Three in-game columns (APM, SQ, supplyCappedPercent) carry
      'IN-GAME — not available at prediction time (Inv. #3)'.
      Post-game column (elapsed_game_loops) carries
      'POST-GAME — total duration; only known after match ends (Inv. #3)'.
  - number: "6"
    how_upheld: "All SQL queries stored in sql_queries dict and written verbatim to markdown artifact."
  - number: "7"
    how_upheld: "All bin widths, clip boundaries, sentinel thresholds derived from census JSON at runtime. No hardcoded numbers."
  - number: "9"
    how_upheld: "Visualization of 01_02_04 findings only. No new analytical computation."
gate:
  artifact_check: "All 14 PNG files and 01_02_05_visualizations.md exist and are non-empty."
  continue_predicate: "All 14 PNG files exist. Markdown artifact contains plot index table with Temporal Annotation column and all SQL queries. Notebook executes end-to-end without errors."
  halt_predicate: "Any PNG file is missing or notebook execution fails."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet"
research_log_entry: "Required on completion."
```

### Step 01_02_06 — Bivariate EDA

```yaml
step_number: "01_02_06"
name: "Bivariate EDA"
description: "9 bivariate visualization plots examining pairwise relationships between features and match result in sc2egset. Reads the 01_02_04 JSON artifact for sentinel thresholds and queries DuckDB for conditional distributions. All plots saved to artifacts/01_exploration/02_eda/plots/. Temporal annotations on in-game columns (APM, SQ, supplyCappedPercent) per Invariant #3. Statistical tests (chi-square, Mann-Whitney U, Spearman) with p-values annotated on plots."
phase: "01 — Data Exploration"
pipeline_section: "01_02 — Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
dataset: "sc2egset"
question: "Which features associate with match outcome (Win vs Loss), and how strongly? Do in-game metrics show stronger separation than pre-game features?"
method: "DuckDB queries for conditional distributions by result. Violin plots for continuous features, grouped bar charts for categorical features. Spearman correlation matrix for numeric columns. Chi-square tests for categorical-by-result associations. Mann-Whitney U for continuous-by-result comparisons. All sentinel thresholds data-derived from 01_02_04 census at runtime."
predecessors: "01_02_05"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_06_bivariate_eda.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  plots:
    - "artifacts/01_exploration/02_eda/plots/01_02_06_mmr_by_result.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_race_winrate.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_apm_by_result.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_sq_by_result.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_supplycapped_by_result.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_league_winrate.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_clan_winrate.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_numeric_by_result.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_06_spearman_correlation.png"
  report: "artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md"
  data_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.json"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: "All three in-game columns (APM, SQ, supplyCappedPercent) carry a visible annotation: 'IN-GAME -- not available at prediction time (Inv. #3)' on every plot where they appear. Spearman heatmap marks in-game columns with red asterisks in tick labels."
  - number: "6"
    how_upheld: "All SQL queries stored in sql_queries dict and written verbatim to markdown artifact."
  - number: "7"
    how_upheld: "All sentinel thresholds (MMR=0 count, SQ INT32_MIN count, Undecided/Tie counts) derived from census JSON at runtime. No hardcoded numbers. Chi-square and Mann-Whitney p-values computed, not assumed."
  - number: "9"
    how_upheld: "Bivariate analysis of existing columns only. No new feature computation. Builds on 01_02_04 census findings and 01_02_05 univariate visualizations."
gate:
  artifact_check: "All 9 PNG files, 01_02_06_bivariate_eda.md, and 01_02_06_bivariate_eda.json exist and are non-empty."
  continue_predicate: "All 9 PNG files exist. JSON artifact contains statistical test results. Markdown artifact contains plot index table with Temporal Annotation column and all SQL queries. Notebook executes end-to-end without errors."
  halt_predicate: "Any PNG file is missing or notebook execution fails."
thesis_mapping:
  - "Chapter 4 — Data and Methodology > 4.1.1 SC2EGSet"
  - "Chapter 5 — Results > feature importance discussion"
research_log_entry: "Required on completion."
```

### Step 01_02_07 -- Multivariate EDA

```yaml
step_number: "01_02_07"
name: "Multivariate EDA"
description: "Multivariate analysis of all numeric features (cluster-ordered Spearman heatmap) and pre-game feature space visualization (MMR faceted by selectedRace and highestLeague). Addresses the degenerate PCA case: only 1 pre-game numeric feature (mmr), so standard PCA is skipped in favor of a scientifically defensible alternative. Produces 2 PNG files and a markdown artifact."
phase: "01 -- Data Exploration"
pipeline_section: "01_02 -- Exploratory Data Analysis (Tukey-style)"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 2.1, 3.4"
dataset: "sc2egset"
question: "What is the joint covariance structure of all numeric features, and what multivariate structure exists in the pre-game feature space?"
method: "Spearman rank correlation on all 4 numeric columns (mmr, apm, sq, supplyCappedPercent), cluster-ordered via scipy hierarchical clustering. Two-panel heatmap: all rows vs MMR>0. Pre-game multivariate view: MMR distribution faceted by selectedRace x highestLeague."
predecessors: "01_02_06"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/02_eda/01_02_07_multivariate_eda.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
    - "artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.json"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  plots:
    - "artifacts/01_exploration/02_eda/plots/01_02_07_spearman_heatmap_all.png"
    - "artifacts/01_exploration/02_eda/plots/01_02_07_pregame_multivariate_faceted.png"
  report: "artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: "Axis tick labels on Spearman heatmap annotated with I3 classification. Pre-game faceted plot uses only pre-game features."
  - number: "6"
    how_upheld: "All SQL queries stored in sql_queries dict and written verbatim to markdown artifact."
  - number: "7"
    how_upheld: "All sentinel thresholds derived from census JSON at runtime. No hardcoded numbers."
  - number: "9"
    how_upheld: "Multivariate visualization of existing columns only. No new feature computation."
gate:
  artifact_check: "Both PNG files and 01_02_07_multivariate_analysis.md exist and are non-empty."
  continue_predicate: "Both PNG files exist. Markdown artifact contains plot index, column classification table, all SQL queries, and PCA-alternative justification. Notebook executes end-to-end without errors."
  halt_predicate: "Any PNG file is missing or notebook execution fails."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet"
research_log_entry: "Required on completion."
```

---

## Phase 01 — Pipeline Section 01_03: Systematic Data Profiling

### Step 01_03_01 -- Systematic Data Profiling

```yaml
step_number: "01_03_01"
name: "Systematic Data Profiling"
description: "Column-level and dataset-level profiling of all three sc2egset raw tables (replay_players_raw, replays_meta_raw struct-flat fields, map_aliases_raw). Detects dead fields, constant columns, near-constant columns, IQR outliers. Produces QQ plots and ECDFs for key numeric columns. Cross-table linkage check via replayId."
phase: "01 -- Data Exploration"
pipeline_section: "01_03 -- Systematic Data Profiling"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 3"
dataset: "sc2egset"
question: "What is the full column-level and dataset-level quality profile of all sc2egset raw tables, including dead fields, constant columns, outlier rates, and distribution shapes?"
method: "DuckDB SQL aggregations: NULL/zero census per column per table, cardinality, descriptive stats, skewness/kurtosis, IQR outlier detection (Tukey fence at 1.5*IQR). QQ plots against normal distribution for 5 key columns. ECDFs for 3 key columns. Cross-table linkage via replayId derived from filename. Completeness heatmap across all tables."
predecessors: "01_02_05"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_01_systematic_profiling.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
    - "replays_meta_raw"
    - "map_aliases_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
  plots:
    - "artifacts/01_exploration/03_profiling/plots/01_03_01_completeness_heatmap.png"
    - "artifacts/01_exploration/03_profiling/plots/01_03_01_qq_plots.png"
    - "artifacts/01_exploration/03_profiling/plots/01_03_01_ecdf_key_columns.png"
  report: "artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: "Every column carries I3 temporal classification. elapsed_game_loops annotated as POST-GAME (reclassified 2026-04-15). APM, SQ, supplyCappedPercent annotated as IN-GAME."
  - number: "6"
    how_upheld: "All SQL queries stored in sql_queries dict and written verbatim to markdown artifact."
  - number: "7"
    how_upheld: "IQR fence multiplier 1.5 cited to Tukey (1977). All sentinel thresholds derived from census JSON at runtime."
  - number: "9"
    how_upheld: "Profiling of existing tables only. No new feature computation. Builds on 01_02_04 census and all 01_02 EDA findings."
gate:
  artifact_check: "All 5 artifacts (JSON, 3 PNGs, MD) exist and are non-empty."
  continue_predicate: "JSON contains critical_findings key with constant_columns list of exactly 5 entries. MD contains I3 classification table. All PNG files exist."
  halt_predicate: "Any artifact is missing or notebook execution fails."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_03_02 -- True 1v1 Match Identification

```yaml
step_number: "01_03_02"
name: "True 1v1 Match Identification"
description: "Profile every replay to determine which are genuine 1v1 matches (exactly 2 active player rows with decisive Win/Loss results) vs non-1v1 (team games, observer contamination, incomplete replays). Produces a replay-level classification without dropping any rows (cleaning deferred to 01_04)."
phase: "01 -- Data Exploration"
pipeline_section: "01_03 -- Systematic Data Profiling"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 3"
dataset: "sc2egset"
question: "Which of the 22,390 replays are genuine 1v1 matches, and what characterises the non-1v1 replays?"
method: "DuckDB SQL: per-replay player row counts, cross-reference with max_players struct field, selectedRace/result analysis of non-2-player rows, observer setting profiling. Multi-signal classification of each replay."
predecessors: "01_03_01"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_02_true_1v1_identification.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
    - "replays_meta_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
    - "artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
  external_references:
    - ".claude/scientific-invariants.md"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json"
  report: "artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "All SQL queries stored in sql_queries dict and written verbatim to markdown artifact."
  - number: "7"
    how_upheld: "Standard race list derived dynamically from 01_02_04 census categorical_profiles.selectedRace at runtime (list comprehension + assertion guard). All other thresholds from census JSON."
  - number: "9"
    how_upheld: "Classification and profiling only. No rows dropped, no new features computed, no cleaning decisions made."
  - number: "3"
    how_upheld: "elapsed_game_loops annotated as POST-GAME wherever referenced. No temporal features computed."
gate:
  artifact_check: "artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json and .md exist and are non-empty."
  continue_predicate: "JSON contains: true_1v1_decisive_count, true_1v1_indecisive_count, total_replay_count, observer_row_analysis, players_per_replay_distribution, max_players_distribution, replay_classification. MD contains comparison summary table. true_1v1_decisive_count + true_1v1_indecisive_count + sum(non_1v1 categories) = total_replay_count."
  halt_predicate: "Any artifact is missing, or classification totals do not sum to 22,390."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_03_03 -- Table Utility Assessment

```yaml
step_number: "01_03_03"
name: "Table Utility Assessment"
description: >-
  Empirical assessment of all 6 raw data objects (replay_players_raw,
  replays_meta_raw, map_aliases_raw, game_events_raw, tracker_events_raw,
  message_events_raw) for prediction pipeline utility. Verify the
  replay_id join key between the two core tables. Enumerate all 31 struct
  leaf fields of replays_meta_raw. Characterize loop=0 initialization
  events. Assess map_aliases_raw necessity. Produce evidence-backed
  utility verdicts.
phase: "01 -- Data Exploration"
pipeline_section: "01_03 -- Systematic Data Profiling"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 3"
dataset: "sc2egset"
question: >-
  Which data objects are essential, utility-conditional, in-game-only,
  or low-utility? What is the replay_id join key between replay_players_raw
  and replays_meta_raw? Are map names already in English? What do loop=0
  events represent?
method: >-
  DuckDB SQL: DESCRIBE both core tables; extract all 31 struct leaf fields;
  verify replay_id join via regexp_extract; cross-reference metadata.mapName
  against map_aliases_raw; query loop=0 evtTypeName distributions; COUNT
  tracker_events_raw and message_events_raw; sample game_events_raw (COUNT
  from schema YAML). All verdicts data-derived.
predecessors: "01_03_02"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_03_table_utility.py"
inputs:
  duckdb_tables:
    - "replay_players_raw"
    - "replays_meta_raw"
    - "map_aliases_raw"
    - "game_events_raw"
    - "tracker_events_raw"
    - "message_events_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
    - "artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
    - "artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - ".claude/rules/sql-data.md"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_03_table_utility.json"
  report: "artifacts/01_exploration/03_profiling/01_03_03_table_utility.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      All event views classified IN_GAME (loop >= 0). timestamp
      (details.timeUTC) classified PRE_GAME. header.elapsedGameLoops
      reclassified POST_GAME. No feature computation performed.
  - number: "6"
    how_upheld: "All SQL queries stored verbatim in sql_queries dict and saved to artifact."
  - number: "9"
    how_upheld: "Profiling only. No rows dropped. No cleaning decisions made."
gate:
  artifact_check: >-
    artifacts/01_exploration/03_profiling/01_03_03_table_utility.json and
    .md exist and are non-empty.
  continue_predicate: >-
    JSON contains: table_verdicts (6 entries), join_key (matched_replay_ids
    == 22390, orphan counts == 0), struct_leaf_fields.confirmed_31_fields ==
    true, map_name_analysis, event_row_counts, tracker_events_loop_range.
    MD contains utility verdict table and all SQL queries.
  halt_predicate: "Any artifact is missing or join verification fails."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_03_04 -- Event Table Profiling

```yaml
step_number: "01_03_04"
name: "Event Table Profiling"
description: >-
  Deep structural profiling of the three event views (tracker_events_raw
  62M rows, game_events_raw 608M rows, message_events_raw 52K rows).
  These are unique to sc2egset -- neither AoE2 dataset has in-game event
  logs. Profiles event type distributions, per-replay density,
  PlayerStats periodicity, UnitBorn unit-type diversity, and event_data
  JSON schemas. No features extracted, no tables created (I9).
phase: "01 -- Data Exploration"
pipeline_section: "01_03 -- Systematic Data Profiling"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 3"
dataset: "sc2egset"
question: >-
  What are the event type distributions for all three event views? What
  is the per-replay event density? Is PlayerStats periodic or variable?
  How many distinct unit types appear in UnitBorn? What JSON keys exist
  in event_data for each event type?
method: >-
  DuckDB SQL: GROUP BY evtTypeName distributions for all three views;
  per-replay density via GROUP BY filename; PlayerStats periodicity via
  LAG window function; UnitBorn unit types via json_extract_string;
  event_data JSON key sampling per type. Game events sampled at 10%
  BERNOULLI for density. All SQL stored verbatim (I6).
predecessors: "01_03_03"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_04_event_profiling.py"
inputs:
  duckdb_tables:
    - "tracker_events_raw"
    - "game_events_raw"
    - "message_events_raw"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
    - "artifacts/01_exploration/03_profiling/01_03_03_table_utility.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - ".claude/rules/sql-data.md"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_04_event_profiling.json"
  report: "artifacts/01_exploration/03_profiling/01_03_04_event_profiling.md"
reproducibility: "Code and output in the paired notebook."
scientific_invariants_applied:
  - number: "6"
    how_upheld: "All SQL queries stored verbatim in sql_queries dict and saved to artifact."
  - number: "9"
    how_upheld: "Profiling only. No rows dropped. No cleaning decisions made. No tables created."
  - number: "3"
    how_upheld: "All three event views classified IN_GAME_ONLY. No features extracted."
gate:
  artifact_check: >-
    artifacts/01_exploration/03_profiling/01_03_04_event_profiling.json and
    .md exist and are non-empty.
  continue_predicate: >-
    JSON contains: tracker_events (type_distribution with 10 types,
    per_replay_density, playerstats_periodicity, unitborn_unit_types with
    >=20 distinct types, event_data_keys for 5+ types), game_events
    (type_distribution with 23 types, event_data_keys for 2+ types),
    message_events (type_distribution, coverage). Exact totals:
    tracker=62,003,411; game=608,618,823; message=52,167.
    All SQL in sql_queries dict (I6).
  halt_predicate: "Any artifact is missing or exact row counts do not match."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet (StarCraft II)"
research_log_entry: "Required on completion."
```

### Step 01_03_05 -- Tracker Events Semantic Validation

```yaml
step_number: "01_03_05"
name: "Tracker Events Semantic Validation"
description: >-
  Semantic validation of tracker_events_raw across the 10 event families
  catalogued in 01_03_04. Examines loops/sec time semantics, player-id
  mapping per event type, PlayerStats cumulative-vs-instantaneous
  semantics, cross-gameVersion schema stability, unit-lifecycle
  ordering, coordinate units, and leakage-boundary discipline to decide
  GATE-14A6 (per thesis/pass2_evidence/phase02_readiness_hardening.md
  §14A.6). Validation only; no features extracted, no tables created
  (I9).
phase: "01 -- Data Exploration"
pipeline_section: "01_03 -- Systematic Data Profiling"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 3"
dataset: "sc2egset"
question: >-
  For each tracker_events_raw event family, are the event-data field
  semantics, player-id mapping, cadence, coordinate units, and
  lifecycle semantics sufficiently understood to derive Phase 02
  in-game-history features without parser-assumption risk? Which
  feature families are eligible_for_phase02_now, eligible_with_caveat,
  blocked_until_additional_validation, or not_applicable_to_pre_game?
method: >-
  Eight validation modules V1-V8 executed SQL-first against
  tracker_events_raw, replay_players_raw, and replays_meta_raw with
  s2protocol decoder source as primary citation authority and the
  SC2EGSet datasheet as secondary (cited by section number only -- no
  text extraction, no new Python dependency). V1 game-loop / time
  semantics; V2 player-id mapping per event type with neutral/global
  slicing; V3 PlayerStats field semantics with strict
  cumulative-classification rule; V4 event-type coverage and schema
  stability with rare-family safeguard; V5 unit-lifecycle ordering;
  V6 coordinate semantics (descriptive only unless source-confirmed);
  V7 leakage boundary (tracker events never pre-game per Invariant
  I3); V8 four-status per-prediction-setting eligibility verdict
  feeding gate_14a6_decision. Auto-downgrade rule: any field whose
  source authority cannot confirm the relevant property downgrades the
  candidate verdict.
stratification: >-
  Per event type (10 types from 01_03_04). Per gameSpeed value
  (re-confirmed cardinality 1, "Faster", in V1). Per gameVersion year
  cohort for V4 schema-stability checks (Pass A 1% Bernoulli + Pass B
  per-event-type stratified resample for rare families with <1000
  events in any non-trivial gameVersion cohort). Per (filename,
  playerId) partitioning for V3 PlayerStats cadence to remove the
  two-players-at-same-loop artifact noted in research_log.md lines
  992-994.
predecessors:
  - "01_03_04"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.py"
inputs:
  duckdb_tables:
    - "tracker_events_raw"
    - "replay_players_raw"
    - "replays_meta_raw"
  schema_yamls:
    - "data/db/schemas/raw/tracker_events_raw.yaml"
    - "data/db/schemas/raw/replay_players_raw.yaml"
    - "data/db/schemas/raw/replays_meta_raw.yaml"
  prior_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_04_event_profiling.json"
    - "artifacts/01_exploration/03_profiling/01_03_03_table_utility.json"
  external_references:
    - ".claude/scientific-invariants.md"
    - "thesis/pass2_evidence/phase02_readiness_hardening.md"
    - "thesis/pass2_evidence/methodology_risk_register.md"
    - "data/raw/SC2EGSet_datasheet.pdf"
    - "https://github.com/Blizzard/s2protocol"
outputs:
  data_artifacts:
    - "artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.json"
    - "artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv"
  report: "artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.md"
reproducibility: >-
  Every reported number is reproduced inline in the .md from the
  captured sql_queries dict per Invariant 6. Loop-to-seconds factor
  (22.4) cited to s2protocol as primary authority (not the Liquipedia
  community-grey reference, which is contextual only). Thresholds
  cited to s2protocol or to planning/current_plan.md amendment list
  per Invariant 7. No random seeds needed because the analysis is
  deterministic SQL.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      V7 explicitly enforces the < cutoff rule and classifies
      tracker_events as IN_GAME, never PRE_GAME. Per-feature
      eligibility verdict makes the temporal class explicit via the
      status_pre_game CSV column.
  - number: "6"
    how_upheld: >-
      Every reported number is accompanied by the SQL that produced
      it; saved verbatim into the JSON artifact's sql_queries dict.
  - number: "7"
    how_upheld: >-
      Loop-to-second factor cited to s2protocol source in V1; no
      other constants introduced; thresholds derived from observed
      distributions or cited to planning/current_plan.md amendment
      list.
  - number: "9"
    how_upheld: >-
      No future-step knowledge consumed; only 01_03_04 and earlier
      artifacts plus external source documentation. No tables
      created.
  - number: "10"
    how_upheld: >-
      filename column already verified in 01_03_04 to be relative
      paths; no new ingestion performed.
gate:
  artifact_check: >-
    artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.json,
    .md, and tracker_events_feature_eligibility.csv exist on disk and
    are non-empty. JSON parses without error.
  continue_predicate: >-
    JSON contains 8 verdict blocks (V1..V8) and a top-level
    gate_14a6_decision field with one of three values: closed,
    narrowed (with enumerated blocked families), or unable_to_decide.
    CSV has one row per (event_family, candidate_feature_family) with
    explicit per-prediction-setting columns (status_pre_game,
    status_in_game_snapshot, status_post_game_or_blocked) populated
    from {eligible_for_phase02_now, eligible_with_caveat,
    blocked_until_additional_validation, not_applicable_to_pre_game}.
    Every tracker-derived row carries status_pre_game =
    not_applicable_to_pre_game. All SQL stored in sql_queries dict
    (I6). A single PlayerStats snapshot family eligible is NOT enough
    to declare gate_14a6_decision = closed unless every
    planned-for-Phase-02 family is also eligible/caveated.
  halt_predicate: >-
    Any of the following forces gate_14a6_decision = unable_to_decide
    and halts the PR to user before T13: V1 fails to confirm a single
    canonical loop-to-seconds factor; V2 finds an event type whose
    semantically-player-attributed records cannot be mapped at all
    (player-attributed slice match rate below 95% with no documented
    neutral/global handling); V8 cannot produce verdicts due to
    evidence insufficiency across the board.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.3.2 SC2 in-game telemetry feature eligibility"
  - "Phase 02 (Feature Engineering) -- decides which tracker-derived feature families enter scope"
research_log_entry: "Required on completion."
```

### Step 01_04_00 -- Source Normalization to Canonical Long Skeleton

```yaml
step_number: "01_04_00"
name: "Source Normalization to Canonical Long Skeleton"
description: >
  Creates the matches_long_raw VIEW: a canonical 10-column long skeleton with one row
  per player per match. Structural INNER JOIN of replay_players_raw x replays_meta_raw
  using the 32-char hex hash extracted from filename (same key as matches_flat in 01_04_01).
  NULLIF guard converts empty-string non-matches to NULL. No filtering, no cleaning,
  no feature computation. leaderboard_raw is NULL for all rows (SC2EGSet is an esports
  tournament dataset with no matchmaking ladder -- deliberate NULL, not missing data).
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 4"
dataset: "sc2egset"
question: >
  Can replay_players_raw JOIN replays_meta_raw be projected losslessly into the canonical
  10-column long skeleton that all downstream cleaning steps will operate against?
method: >
  INNER JOIN of replay_players_raw x replays_meta_raw on NULLIF-guarded hex-hash regexp
  key. Lossless check compares VIEW count against the same JOIN computed directly on raw
  tables. Side derived as playerID - 1 (0-based). started_timestamp taken from
  rm.details.timeUTC (struct dot notation, VARCHAR). leaderboard_raw = NULL constant.
predecessors:
  - "01_04_01"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_00_source_normalization.py"
outputs:
  duckdb_views:
    - "matches_long_raw"
  data_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json"
  report: "artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md"
  schema_yaml: "data/db/schemas/views/matches_long_raw.yaml"
gate:
  artifact_check: >
    JSON artifact exists with row_count, schema, lossless_check, symmetry_audit,
    and all SQL queries verbatim. matches_long_raw VIEW is queryable and returns 44,817 rows.
    Distinct side values include 0 and 1 (main players); schema YAML exists.
  continue_predicate: >
    Lossless check PASSED (matches_long_raw rows == direct JOIN count).
    STEP_STATUS.yaml has 01_04_00: complete.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >
      MMR retained (PRE_GAME per 01_04_01 analysis). APM, SQ, supplyCappedPercent,
      header_elapsedGameLoops excluded. I3 preserved.
  - number: "5"
    how_upheld: >
      Player-row-oriented VIEW. No slot-based pivoting. Both players in any match
      are represented with the same 10-column structure.
  - number: "6"
    how_upheld: "All SQL queries written verbatim to JSON artifact under sql_queries."
  - number: "9"
    how_upheld: >
      No features computed. No rows filtered beyond INNER JOIN unmatched exclusion.
      Raw data untouched.
research_log_entry: "Required on completion."
```

### Step 01_04_01 -- Data Cleaning

```yaml
step_number: "01_04_01"
name: "Data Cleaning — VIEW DDL + Missingness Audit (insight-gathering)"
description: >
  Two-part step with one execution pass.
  PART A (already executed in PRs #138/#139): non-destructive cleaning of
  replay_players_raw and replays_meta_raw via three DuckDB VIEWs (matches_flat,
  matches_flat_clean, player_history_all) — all DDL changes resolved in prior PRs.
  PART B (this revision): consolidated missingness audit over the analytical VIEWs
  (matches_flat_clean, player_history_all). Two coordinated census passes per VIEW —
  SQL NULL census plus sentinel census driven by per-column _missingness_spec — plus
  a runtime constants-detection check, feed one missingness ledger (CSV+JSON) per
  VIEW. The audit gathers insights for downstream cleaning decisions in 01_04_02+;
  it does NOT execute decisions, modify VIEWs, drop columns, or impute. Ends with
  an explicit "Decisions surfaced for downstream cleaning" section listing
  per-dataset open questions.
phase: "01 — Data Exploration"
pipeline_section: "01_04 — Data Cleaning"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Sections 3 (Profiling) and 4 (Cleaning)"
dataset: "sc2egset"
question: >
  What is the complete missingness picture (NULL + sentinel-encoded + constant
  columns) per analytical VIEW column, classified by mechanism (Rubin 1976
  MCAR/MAR/MNAR), and which open questions must downstream 01_04 steps resolve
  before Phase 02 imputation design?
method: >
  Three-step per-VIEW audit (matches_flat_clean, player_history_all):
  Step 1 (kept verbatim): SQL NULL census per column via
  COUNT(*) FILTER (WHERE col IS NULL) over the full VIEW.
  Step 2 (NEW): sentinel census per column driven by _missingness_spec dict
  (per-column override is preferred; auto-detection from prior census artifacts is
  the secondary fallback). Sentinel SQL per column matches the spec's declared
  sentinel value(s).
  Step 3 (NEW): runtime constants detection — SELECT COUNT(DISTINCT col) per VIEW
  column; columns with n_distinct=1 get mechanism="N/A" + recommendation="DROP_COLUMN".
  Per-row recommendation derived from pct_missing_total = pct_null + pct_sentinel
  via the decision tree in temp/null_handling_recommendations.md §3.1, applying
  Rules S1-S6, with two override layers: (a) F1 zero-missingness override and
  (b) target-column override per Rule S2. The notebook produces RECOMMENDATIONS
  only; downstream 01_04 steps decide and execute.
  Reads the empirical sentinel patterns from
  artifacts/01_exploration/02_eda/01_02_04_univariate_census.json — the audit
  consolidates prior findings; it does not re-derive them.
predecessors:
  - "01_03_04"
methodology_citations:
  - "Rubin, D.B. (1976). Inference and missing data. Biometrika, 63(3), 581-592. — MCAR/MAR/MNAR taxonomy."
  - "Little, R.J. & Rubin, D.B. (2019). Statistical Analysis with Missing Data, 3rd ed. Wiley. — Authoritative mechanism classification."
  - "van Buuren, S. (2018). Flexible Imputation of Missing Data, 2nd ed. CRC Press. — Warns against rigid percentage thresholds; threshold S4 used as starting heuristic only."
  - "Schafer, J.L. & Graham, J.W. (2002). Missing data: Our view of the state of the art. Psychological Methods, 7(2), 147-177. — Listwise deletion acceptable at <5% MCAR (boundary citation, not threshold derivation)."
  - "Sambasivan, N. et al. (2021). Everyone wants to do the model work, not the data work: Data Cascades in High-Stakes AI. CHI '21. — Rationale for surfacing decisions explicitly rather than deferring."
  - "Davis, J. et al. (2024). Methodology and Evaluation in Sports Analytics. Machine Learning, 113, 6977-7010. — Domain precedent for sports outcome data quality protocols (retained for future Phase 02/03 reference; not load-bearing in this audit step)."
  - "scikit-learn v1.8 documentation. Imputation of missing values; sklearn.impute.MissingIndicator. — Missingness-as-signal principle for Phase 02."
  - "Wirth, R. & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. — Cleaning report convention adopted in artifact format."
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §3 (Profiling) and §4 (Cleaning) — pipeline phase boundary (Phase 01 documents, Phase 02 transforms)."
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py"
inputs:
  duckdb_tables:
    - "replay_players_raw (44,817 rows)"
    - "replays_meta_raw (22,390 rows)"
  duckdb_views:
    - "matches_flat (44,817 rows / 22,390 replays)"
    - "matches_flat_clean (44,418 rows / 22,209 replays)"
    - "player_history_all (44,817 rows / 22,390 replays)"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.json (sentinel and zero-distribution evidence)"
    - "artifacts/01_exploration/03_profiling/* (column-level mechanism evidence — see prior steps)"
outputs:
  duckdb_views:
    - "matches_flat (unchanged)"
    - "matches_flat_clean (unchanged)"
    - "player_history_all (unchanged)"
  schema_yamls:
    - "data/db/schemas/views/player_history_all.yaml (unchanged from PR #138/#139)"
  data_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json (extended with missingness_audit block)"
    - "artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv (NEW — one row per (view, column); full-coverage Option B; zero-missingness columns tagged RETAIN_AS_IS / mechanism=N/A; constant columns tagged DROP_COLUMN / mechanism=N/A)"
    - "artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json (NEW — same content, machine-readable)"
  report: "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md (extended)"
reproducibility: >
  Code and output in the paired notebook. All SQL verbatim in JSON sql_queries.
  Audit re-runs deterministically from raw tables.
key_findings_carried_forward:
  - "157 replays excluded due to MMR<0 (PR predecessor — kept)"
  - "MMR=0 sentinel covers 83.66% of true_1v1_decisive rows (audit confirms)"
  - "highestLeague='Unknown' covers ~72% (audit confirms)"
  - "clanTag='' covers ~74% (audit confirms via sentinel pass)"
  - "matches_flat_clean's 1v1_decisive filter excludes ~0.06% Undecided/Tie rows from result (CONSORT verified each run; Rule S2 enforced upstream of the audit)"
decisions_surfaced:
  - id: "DS-SC2-01"
    column: "MMR (sentinel=0, ~83.66%)"
    question: >
      Convert MMR=0 to NULL and drop the column from matches_flat_clean
      (per Rule S4 / >80%), OR retain MMR=0 as an explicit `unranked` categorical
      encoding alongside `is_mmr_missing`, OR run the analysis on the rated subset
      only as a sensitivity arm (per Sambasivan 2021 cascade-prevention)?
    mechanism_note: >
      Resolve MMR mechanism contradiction: this plan classifies MMR=0 as
      MAR-primary (tournament replays without ladder MMR — missingness depends
      on observed replay source); MNAR (private pro accounts) is documented as a
      sensitivity branch. Source: 01_03_01 + 01_03_03 cleaning_registry rules.
  - id: "DS-SC2-02"
    column: "highestLeague (sentinel='Unknown', ~72.16%)"
    question: >
      Drop the column entirely (Rule S4 / >50% non-primary), OR retain 'Unknown'
      as its own category (Phase 02 decides if predictive)?
  - id: "DS-SC2-03"
    column: "clanTag (sentinel='', ~74%)"
    question: >
      Drop the column (likely non-predictive at this rate), OR retain as a derived
      `is_in_clan` boolean only?
  - id: "DS-SC2-04"
    column: "result in player_history_all (Undecided/Tie sentinel; non-zero rate in player_history_all)"
    question: >
      How should NULL-target rows in player_history_all be handled when computing
      player history features (e.g., expanding-window win-rate)? Drop these rows,
      mark them as a DRAW outcome category, or retain with NaN target value (so
      games-played counts include them but win-rate denominators exclude)?
  - id: "DS-SC2-05"
    column: "selectedRace (sentinel='', ~2.48%)"
    question: >
      Already converted to 'Random' in VIEWs (PR predecessor); the audit confirms
      zero residual empty-string occurrences in the cleaned VIEWs.
  - id: "DS-SC2-06"
    columns: "gd_mapSizeX / gd_mapSizeY (sentinel=0, ~1.22%)"
    question: >
      VIEWs already CASE-WHEN to NULL (PR predecessor); audit confirms ledger
      reports the converted NULLs, not the original sentinel.
  - id: "DS-SC2-07"
    column: "gd_mapAuthorName"
    question: >
      Drop column on grounds of being a non-predictive metadata field even before
      missingness considered? Decision deferred to 01_04_02+.
  - id: "DS-SC2-08"
    columns: "go_* constants surfaced by runtime constants-detection branch"
    question: >
      Confirm the runtime constants-detection branch reports n_distinct=1 for the
      go_* columns flagged in 01_03_03 (and which exact columns are identified as
      constant in matches_flat_clean vs player_history_all). Drop these per
      Rule S4 / N/A-mechanism in 01_04_02+?
  - id: "DS-SC2-09"
    column: "handicap (sentinel=0, ~0.0045% — 2 anomalous rows)"
    question: >
      NULLIF the 2 anomalous handicap=0 rows + listwise deletion per Rule S3
      (negligible rate), OR retain 0 as an explicit `is_anomalous_handicap` flag?
      B6 deferral note — same pattern as DS-AOESTATS-02: audit will recommend
      CONVERT_SENTINEL_TO_NULL via W3 branch; spec marks
      carries_semantic_content=True (0 is documented as "anomalous game"
      indicator, semantically meaningful); downstream chooses without prejudice
      from the ledger.
  - id: "DS-SC2-10"
    column: "APM in player_history_all (sentinel=0, ~2.53%; 97.9% overlap with selectedRace='')"
    question: >
      Convert APM=0 to NULL via NULLIF in 01_04_02+ (per audit recommendation)
      OR retain APM=0 as a categorical encoding for "extremely short / unparseable
      game"? B6 deferral note — audit will recommend CONVERT_SENTINEL_TO_NULL
      via W3 branch; spec marks carries_semantic_content=True (APM=0 documented
      as correlating with selectedRace='' — meaningful game-state signal);
      downstream chooses without prejudice from the ledger.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >
      No new feature computation. No use of game T data. Audit is read-only over
      VIEWs whose I3 compliance was established in the predecessor PRs.
  - number: "6"
    how_upheld: >
      All three SQL templates (NULL census, sentinel census, constants detection)
      stored verbatim in JSON sql_queries. The per-column sentinel queries are
      reconstructible from the template + the _missingness_spec dict (also stored
      in the artifact).
  - number: "7"
    how_upheld: >
      Thresholds (5%/40%/80%) follow the operational starting heuristics in
      temp/null_handling_recommendations.md §1.2; cite Schafer & Graham 2002 for
      the <5% MCAR boundary and van Buuren 2018 for the warning against rigid
      global thresholds. Each threshold-driven recommendation surfaces as a
      downstream decision per §3.1; the audit recommends, the downstream step
      decides. Per-column mechanism justifications cite either a prior step's
      artifact (with path) or a sentinel-meaning interpretation explicitly grounded
      in domain context.
  - number: "9"
    how_upheld: >
      All facts derive from this step's SQL or from cited predecessor artifacts.
      No raw tables, no VIEWs, no schema YAMLs are modified. Audit is purely
      additive: extends artifact JSON, adds two new ledger files. No future-step
      citations.
gate:
  artifact_check: >
    JSON has "missingness_audit" block with two VIEW sub-blocks, each containing
    a "ledger" array (one row per column in the VIEW — full-coverage Option B) and the
    "_missingness_spec" used. The two new ledger files (CSV + JSON) exist at the
    paths above. MD has a "Missingness Ledger" section per VIEW + a final
    "Decisions surfaced for downstream cleaning (01_04_02+)" section reproducing
    DS-SC2-01..10 with current observed rates filled in.
  continue_predicate: >
    Every column in the VIEW appears in the ledger (full-coverage Option B).
    Every column with non-zero missingness has a _missingness_spec entry; zero-
    missingness rows carry mechanism=N/A, recommendation=RETAIN_AS_IS, and
    justification="Zero missingness observed; no action needed." regardless of
    spec. Constant columns (n_distinct=1) carry mechanism=N/A,
    recommendation=DROP_COLUMN with constants-detection justification.
    Every ledger row has non-empty mechanism_justification, recommendation,
    recommendation_justification, and explicit carries_semantic_content boolean.
    Existing zero-NULL assertions (replay_id, toon_id, result in both VIEWs) still
    pass. STEP_STATUS.yaml has 01_04_01: complete.
  halt_predicate: >
    Any column in the VIEW missing from the ledger (full-coverage violation);
    any column with non-zero missingness lacking a _missingness_spec entry; any
    ledger row missing mandatory fields; any zero-NULL identity assertion failure;
    any contradictory pairing of mechanism="N/A" with non-N/A justification.
research_log_entry: >
  Required on completion: list per-VIEW row counts in ledger, reference the
  artifact paths, summarise decisions surfaced for downstream resolution.
```

### Step 01_04_02 -- Data Cleaning Execution

```yaml
step_number: "01_04_02"
name: "Data Cleaning Execution -- Act on DS-SC2-01..10"
description: >
  Acts on the 10 cleaning decisions surfaced by 01_04_01. Modifies VIEW DDL
  for matches_flat_clean and player_history_all (no raw table changes per
  Invariant I9): drops MMR (Rule S4 / 83.95%), highestLeague (Rule S4 / 72%),
  clanTag (Rule S4 / 74%), 12 go_* constants (DS-SC2-08), gd_mapAuthorName
  (DS-SC2-07 domain), gd_mapSizeX/Y from matches_flat_clean (DS-SC2-06),
  handicap (DS-SC2-09 near-constant). Modifies APM in player_history_all
  via NULLIF (DS-SC2-10) + adds is_apm_unparseable indicator. Adds
  is_decisive_result to player_history_all (DS-SC2-04). Reports CONSORT-style
  column-count flow + subgroup impact + post-cleaning invariant re-validation.
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 4"
dataset: "sc2egset"
question: >
  Which of the 10 decisions surfaced by 01_04_01 (DS-SC2-01..10) are
  resolved by DDL modifications, what is the column-count and subgroup
  impact, and do all post-cleaning invariants still hold?
method: >
  Modify CREATE OR REPLACE VIEW DDL for matches_flat_clean and player_history_all
  per per-DS resolutions (see plan Section 1). Apply column drops, the APM NULLIF,
  and two new derived columns (is_decisive_result, is_apm_unparseable). Re-run
  the assertion battery from 01_04_01 plus 01_04_02-specific assertions on the
  new column set. Produce a CONSORT-style column-count table and per-DS
  resolution log.
stratification: "By VIEW (matches_flat_clean vs player_history_all) and by DS-SC2-NN."
predecessors:
  - "01_04_01"
methodology_citations:
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.1 (cleaning registry), §4.2 (non-destructive), §4.3 (CONSORT impact), §4.4 (post-validation)"
  - "Liu, X. et al. (2020). Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. BMJ, 370."
  - "Jeanselme, V. et al. (2024). Participant Flow Diagrams for Health Equity in AI. Journal of Biomedical Informatics, 152."
  - "Schafer, J.L. & Graham, J.W. (2002). Missing data: Our view of the state of the art. Psychological Methods, 7(2)."
  - "van Buuren, S. (2018). Flexible Imputation of Missing Data, 2nd ed. CRC Press."
  - "Sambasivan, N. et al. (2021). Data Cascades in High-Stakes AI. CHI '21."
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py"
inputs:
  duckdb_views:
    - "matches_flat (44,817 rows -- structural JOIN, unchanged)"
    - "matches_flat_clean (44,418 rows / 22,209 replays -- pre-01_04_02)"
    - "player_history_all (44,817 rows / 22,390 replays -- pre-01_04_02)"
  prior_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json (cleaning_registry, missingness_audit, consort_flow)"
    - "artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv (100 rows, per-DS empirical evidence)"
    - "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md (decisions_surfaced reference)"
  schema_yamls:
    - "data/db/schemas/views/player_history_all.yaml (current -- to be updated)"
outputs:
  duckdb_views:
    - "matches_flat_clean (replaced via CREATE OR REPLACE -- 28 cols, 44,418 rows)"
    - "player_history_all (replaced via CREATE OR REPLACE -- 37 cols, 44,817 rows)"
  schema_yamls:
    - "data/db/schemas/views/matches_flat_clean.yaml (NEW)"
    - "data/db/schemas/views/player_history_all.yaml (UPDATED)"
  data_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json"
  report: "artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md"
reproducibility: >
  Code and output in the paired notebook. All DDL stored verbatim in the
  validation JSON sql_queries block (Invariant I6). All thresholds derived
  from the 01_04_01 ledger CSV at runtime (Invariant I7). Re-runs deterministically.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >
      No new feature computation. matches_flat_clean retains only PRE_GAME
      columns. player_history_all retains IN_GAME_HISTORICAL columns (APM, SQ,
      supplyCappedPercent, header_elapsedGameLoops) which are valid for
      historical computation per the I3 design constraint established in 01_04_01.
  - number: "5"
    how_upheld: >
      Symmetry assertion re-run: every replay_id in matches_flat_clean has
      exactly 1 Win + 1 Loss row. The is_decisive_result derivation in
      player_history_all is symmetric (depends only on result, not on player slot).
  - number: "6"
    how_upheld: >
      All DDL queries stored verbatim in JSON sql_queries. All assertion SQL
      stored verbatim. All per-DS rationale references the ledger row + ledger
      recommendation_justification by view+column.
  - number: "7"
    how_upheld: >
      Thresholds (5/40/80%) come from the 01_04_01 framework block (Schafer &
      Graham 2002 boundary; van Buuren 2018 warning). Per-DS empirical evidence
      (n_sentinel, pct_missing_total, n_distinct) is read from the 01_04_01
      ledger CSV at runtime, not hardcoded.
  - number: "9"
    how_upheld: >
      No raw tables modified. matches_flat (structural JOIN) unmodified.
      matches_long_raw (canonical skeleton from 01_04_00) unmodified. Only
      matches_flat_clean and player_history_all VIEWs are replaced via
      CREATE OR REPLACE. All inputs are 01_04_01 artifacts (predecessor) or
      this step's own DDL output.
gate:
  artifact_check: >
    artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json
    and .md exist and are non-empty. Both schema YAMLs
    (matches_flat_clean.yaml NEW, player_history_all.yaml UPDATED) exist with
    correct column counts.
  continue_predicate: >
    matches_flat_clean has exactly 28 columns. player_history_all has exactly
    37 columns. All zero-NULL assertions pass (replay_id, toon_id, result in
    both VIEWs). Symmetry violations = 0 in matches_flat_clean. CONSORT column-
    count table reproduces drop counts per DS-SC2-01..10. STEP_STATUS.yaml has
    01_04_02: complete. PIPELINE_SECTION_STATUS for 01_04 transitions to complete
    (no further 01_04_NN steps defined in ROADMAP).
  halt_predicate: >
    Any zero-NULL assertion fails; any symmetry violation; any forbidden column
    appears in matches_flat_clean; any expected NEW column missing from
    player_history_all; column count off by even one from spec.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet (StarCraft II) > Data Cleaning Decisions"
research_log_entry: "Required on completion."
```

#### Addendum: Duration Augmentation (2026-04-18)

```yaml
addendum_date: "2026-04-18"
addendum_title: "Duration Augmentation -- matches_flat_clean 28 → 30 cols"
addendum_scope: >
  ADDENDUM to 01_04_02. Extends matches_flat_clean VIEW from 28 → 30 columns
  by adding duration_seconds BIGINT (POST_GAME_HISTORICAL) + is_duration_suspicious
  BOOLEAN (POST_GAME_HISTORICAL). Source: player_history_all.header_elapsedGameLoops
  aggregated per replay_id / 22.4 (SC2 Faster loops/sec constant, I7). No row
  changes (I9). STEP_STATUS stays complete per addendum precedent.
new_cols:
  - name: duration_seconds
    type: BIGINT
    token: POST_GAME_HISTORICAL
    derivation: "CAST(ANY_VALUE(header_elapsedGameLoops) / 22.4 AS BIGINT) per replay_id"
    i7_provenance: "details.gameSpeed cardinality=1 in sc2egset (research_log.md:424); Blizzard SC2 Faster=22.4 loops/sec"
  - name: is_duration_suspicious
    type: BOOLEAN
    token: POST_GAME_HISTORICAL
    derivation: "duration_seconds > 86400"
    i8_provenance: "86400s canonical sanity bound; identical across sc2egset, aoestats, aoe2companion"
duration_stats:
  min_seconds: 1
  p50_seconds: 651.0
  p99_seconds: 1876.0
  max_seconds: 6073
  null_count: 0
  suspicious_count: 0
schema_version: "30-col (ADDENDUM: duration added 2026-04-18)"
new_artifact: "artifacts/01_exploration/04_cleaning/01_04_02_duration_augmentation.json"
new_artifact_md: "artifacts/01_exploration/04_cleaning/01_04_02_duration_augmentation.md"
notebook: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_duration_augmentation.py"
gates_all_pass: true
```

### Step 01_04_03 -- Minimal Cross-Dataset History View

```yaml
step_number: "01_04_03"
name: "Minimal Cross-Dataset History View"
description: >
  Create matches_history_minimal VIEW: 9-column player-row-grain projection (post-ADDENDUM 2026-04-18)
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
  schema shape, I5-analog NULL-safe symmetry (IS DISTINCT FROM), prefix
  uniqueness, dataset_tag constancy, temporal sanity.
stratification: "By match_id (2 symmetric rows); by faction for vocabulary documentation."
predecessors:
  - "01_04_02"
methodology_citations:
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.2 (non-destructive cleaning)"
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.4 (post-cleaning validation)"
  - "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley. (raw-string vocabulary documentation)"
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
      lengths (22-28 chars); lex ordering would be non-monotonic across
      formats. Phase 02 consumers use TIMESTAMP started_at as strict-
      less-than anchor.
  - number: "5"
    how_upheld: >
      Player-row symmetry (I5-analog). SYMMETRY_I5_ANALOG_SQL uses
      IS DISTINCT FROM for NULL-safe comparison. Every match_id has exactly
      2 rows; (player_id, opponent_id) pair appears in both directions; won
      values are complementary; faction / opponent_faction are mirrored.
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
      faction vocabulary (consumers MUST game-condition). aoestats sibling
      PR projects 1-row-per-match to 2-rows with p0/p1 UNION ALL (team1_wins
      slot-asymmetry awareness required).
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
    VIEW exists with 9 columns matching spec (post-ADDENDUM 2026-04-18). 44,418 rows = 22,209 x 2.
    Zero NULL-safe symmetry violations. Zero prefix violations. dataset_tag
    constancy = 1. Zero NULLs in match_id / player_id / opponent_id / won /
    dataset_tag. STEP_STATUS 01_04_03 -> complete. PIPELINE_SECTION_STATUS
    01_04 -> complete.
  halt_predicate: >
    Symmetry violation > 0; row-count discrepancy; prefix violation; NULL in
    non-nullable spec column; column count != 9; started_at dtype != TIMESTAMP;
    upstream YAML byte-diff detected. ON HALT: manually revert
    PIPELINE_SECTION_STATUS 01_04 -> complete before aborting.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.1.1 SC2EGSet > Cross-dataset harmonization substrate"
  - "Chapter 4 -- Data and Methodology > 4.3 Rating System Backtesting Design (downstream consumer)"
research_log_entry: "Required on completion."
```

### Step 01_04_04 -- Identity Resolution

```yaml
step_number: "01_04_04"
name: "Identity Resolution"
description: >
  Exploratory record-linkage census on sc2egset identity columns (toon_id,
  nickname, region, realm, userID, playerID). Classifies the Phase-01
  hypothesis "toon_id > nickname as multi-account trace" into Fellegi-
  Sunter-style agreement patterns. Produces 8-query SQL ledger + 5
  DS-SC2-IDENTITY-* decisions routed to Phase 02. No VIEW DDL; no raw
  modification (I9).
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
manual_reference: "01_DATA_EXPLORATION_MANUAL.md, Section 4 (cleaning census pattern) + Section 5 (panel-EDA feed-forward)"
dataset: "sc2egset"
question: >
  What fraction of the observed toon_id > nickname asymmetry in sc2egset
  is produced by multi-region accounts (Battle.net server-scoping), and
  what fraction by common-handle collisions? Feeds thesis §4.2.2 [REVIEW]
  marker closure.
method: >
  Five-key uniqueness census (toon_id; (region,realm,toon_id);
  LOWER(nickname); (LOWER(nickname),region); (LOWER(nickname),region,realm))
  + toon_id cross-region audit + nickname cross-region detail list with
  temporal windows + Fellegi-Sunter Class A/B/C temporal-overlap
  classification + within-region handle-collision audit + userID
  refutation cross-check + region/realm sanity + robustness cross-check
  against matches_flat_clean.
stratification: "By candidate identity key; by region/realm label."
predecessors:
  - "01_04_01"
  - "01_04_02"
  - "01_04_03"
methodology_citations:
  - "Fellegi, I. P. & Sunter, A. B. (1969). A Theory for Record Linkage. JASA 64(328)."
  - "Christen, P. (2012). Data Matching. Springer (Ch. 5 false-merge rate thresholds)."
  - "Manual 01_DATA_EXPLORATION_MANUAL.md §4.2 (non-destructive cleaning), §5 (panel-EDA feed-forward)"
  - ".claude/scientific-invariants.md Invariant #2 (canonical identifier)"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04_identity_resolution.py"
inputs:
  duckdb_views:
    - "matches_flat (44,817 rows, IDENTITY cols intact)"
    - "matches_flat_clean (44,418 rows, robustness cross-check)"
    - "matches_long_raw (44,817 rows, canonical skeleton)"
  prior_artifacts:
    - "artifacts/01_exploration/02_eda/01_02_04_univariate_census.md (2.26 baseline)"
    - "artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md"
    - "artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md (DS-SC2-01..10 precedent)"
outputs:
  duckdb_views: []  # none; exploration only (I9)
  schema_yamls: []  # none
  data_artifacts:
    - "artifacts/01_exploration/04_cleaning/01_04_04_identity_resolution.json (8 SQL queries verbatim per I6)"
    - "artifacts/01_exploration/04_cleaning/01_04_04_cross_region_nicknames.csv (246 rows)"
    - "artifacts/01_exploration/04_cleaning/01_04_04_within_region_handle_collisions.csv (451 rows)"
    - "artifacts/01_exploration/04_cleaning/plots/01_04_04_key_cardinality_bars.png"
    - "artifacts/01_exploration/04_cleaning/plots/01_04_04_toon_region_heatmap.png"
    - "artifacts/01_exploration/04_cleaning/plots/01_04_04_nickname_cross_region_stacked.png"
  report: "artifacts/01_exploration/04_cleaning/01_04_04_identity_resolution.md"
reproducibility: >
  All 8 SQL queries stored verbatim in validation JSON sql_queries block
  (I6). Deterministic census; no random sampling in sc2egset slice.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >
      No in-game columns used for identity derivation (APM/SQ excluded).
      Nickname, region, realm, toon_id all PRE_GAME or IDENTITY per 01_04_02
      classification.
  - number: "6"
    how_upheld: >
      All SQL stored verbatim in validation JSON sql_queries. 8 keys:
      single_key_census, toon_id_cross_region_audit, nickname_cross_region_audit,
      temporal_overlap_classification, within_region_handle_collision,
      userid_refutation, region_realm_sanity, robustness_crosscheck.
  - number: "7"
    how_upheld: >
      2.26 ratio baseline cites 01_02_04 census (toon_id=2495, nickname=1106);
      5% within-region collision threshold cites Christen 2012 Ch. 5;
      ±1% robustness delta cites 399/44,817=0.89% empirical basis.
  - number: "8"
    how_upheld: >
      Decision ledger language identical to aoestats + aoe2companion sibling
      01_04_04 plans; verdict rubric (A/B/C) cross-dataset consistent.
  - number: "9"
    how_upheld: >
      Pure read-only analysis. No raw-table mutation. No new VIEW created.
      All 3 sc2egset view YAMLs byte-identical post-execution.
gate:
  artifact_check: >
    JSON + MD + 2 CSVs + 3 PNGs all exist non-empty.
  continue_predicate: >
    Ratio K1/K_cs = 2.2559 within 2.257 +/- 0.05 (I7 baseline). 0 cross-region
    toon_ids (Battle.net scoping). 5 DS-SC2-IDENTITY-* decisions populated.
    I9 empty diff on all sc2egset view + raw YAMLs. STEP_STATUS 01_04_04
    -> complete; PIPELINE_SECTION 01_04 -> complete (roundtrip restore).
  halt_predicate: >
    Ratio drift > 0.05 (upstream change / SQL bug); cross-region toon_id
    count > 0 (data-pipeline bug OR Battle.net legacy). Manual revert of
    PIPELINE_SECTION_STATUS before aborting.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.2.2 Rozpoznanie tozsamosci gracza (operational evidence closes [REVIEW] marker)"
  - "Chapter 4 -- Data and Methodology > 4.4.1 Per-player split justification (feeds Phase 02 grouping-key choice)"
research_log_entry: "Required on completion."
decisions_surfaced:
  - id: "DS-SC2-IDENTITY-01"
    scope: "Phase 02 canonical player primary key"
    evidence: "K1=2495 toon_ids; K_cs=1106 case-sensitive nicks; K4=(LOWER(nick),region)=1473; K5=1487; 0 cross-region toon_ids; 294 Class A cross-region-overlap nickname pairs; 451/1473=30.6% within-region collision rate"
    recommendation: "REJECT toon_id-alone AND REJECT LOWER(nickname)-alone; use composite key with behavioral disambiguation -- deferred to Phase 02"
    routed_to: "Phase 02 / 02_07 Rating Systems"
  - id: "DS-SC2-IDENTITY-02"
    scope: "LOWER(nickname)-alone as primary key"
    evidence: "30.6% within-region LOWER(nickname) collision rate (451/1473) >> Christen 2012 5% threshold"
    recommendation: "REJECT"
    routed_to: "Phase 02 / 02_07"
  - id: "DS-SC2-IDENTITY-03"
    scope: "Class A/B temporal-overlap pairs handling"
    evidence: "294 Class A (overlap, multi-account candidate); 15,474 Class B (disjoint, migration OR different player); 317 Class C (degenerate)"
    recommendation: "Phase 02 entity-resolution: Class A MERGE candidates (pending behavioral-fingerprint disambiguation); Class B conservative-separate; Class C insufficient evidence"
    routed_to: "Phase 02 / 02_07"
  - id: "DS-SC2-IDENTITY-04"
    scope: "region='Unknown' bucket (~12.83% of rows)"
    evidence: "Unknown region is a valid value, not a sentinel -- pre-metadata-capture tournaments"
    recommendation: "Treat Unknown as distinct region value; do NOT merge with known regions"
    routed_to: "Phase 02 / 02_03 Cold Starts"
  - id: "DS-SC2-IDENTITY-05"
    scope: "Composite canonical identity VIEW design (player_identity_canonical)"
    evidence: "Multi-signal required: (region, realm, toon_id) granular base + optional nickname-based MERGE for Class A overlap + behavioral-fingerprint confirmation (APM per Hahn et al. 2020)"
    recommendation: "Design player_identity_canonical VIEW in Phase 02 after running 01_04_04 augmentation PR for sc2egset worldwide-identity classifier"
    routed_to: "Phase 02 / 02_07 + 01_04_04 augmentation PR (this branch: feat/01-04-04-sc2egset-worldwide-identity)"
```

### Step 01_04_04b -- Stub worldwide identity VIEW (decomposition-based)

```yaml
step_number: "01_04_04b"
name: "Worldwide Identity VIEW (decomposition-based)"
description: >
  Create player_identity_worldwide VIEW that decomposes toon_id (full Battle.net R-S2-G-P qualifier)
  into human-readable columns (region_code, realm_code, profile_id, region_label, realm_label,
  nickname_case_sensitive). Investigate 2 empty-toon_id outlier rows. No hashing, no composite
  encoding -- toon_id IS the worldwide identifier (region-scoped per Blizzard design).
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
parent_step: "01_04_04"
plan_version: "R4"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.py"
completed_at: "2026-04-18"
outputs:
  view: "player_identity_worldwide (2,494 rows, 7 cols)"
  schema_yaml: "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_identity_worldwide.yaml"
  artifacts:
    - "reports/artifacts/01_exploration/04_cleaning/01_04_04b_worldwide_identity.json"
    - "reports/artifacts/01_exploration/04_cleaning/01_04_04b_worldwide_identity.md"
key_findings:
  - "toon_id stores full Battle.net R-S2-G-P qualifier -- no hashing needed"
  - "273 toon_ids have multiple nicknames; VIEW picks modal nickname per toon_id"
  - "userID cardinality=16 = local Battle.net profile slot indices (0..15), NOT player IDs"
  - "2 empty-toon_id rows are observer-profile ghost entries (handicap=0, color_rgba=0)"
  - "Outliers from 2 different tournaments (IEM 2017, HSC 2019) -- not systematic"
  - "No external bridge available for cross-region toon_id merge (R2 confirmed)"
```

### Step 01_04_05 — Cross-Region Fragmentation Phase 01 Annotation

```yaml
step_number: "01_04_05"
name: "Cross-Region Fragmentation Phase 01 Annotation"
description: >
  Add is_cross_region_fragmented BOOLEAN column to the player_history_all VIEW via DDL
  amendment. Flag TRUE iff a row's toon_id belongs to the set of cross-region toon_ids
  (toons whose LOWER(nickname) appears in 2+ regions in replay_players_raw). Operationalizes
  the INVARIANTS.md §2 accepted-bias framing as a Phase 02-consumable filter.
phase: "01 -- Data Exploration"
pipeline_section: "01_04 -- Data Cleaning"
category: "A"
motivation: >
  WP-3 (01_05_10) empirically FAILed the accepted-bias framing: at window=30,
  median rolling-window undercount=16.0 games, p95=29.0 games. User directive
  2026-04-21 requires a Phase 01 01_04 annotation per docs/PHASES.md discipline
  so Phase 02 consumers can apply the accepted-bias framing without re-deriving
  the cross-region set per query.
predecessor_step: "01_04_04b"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_05_cross_region_annotation.py"
completed_at: "2026-04-21"
outputs:
  view_amended: "player_history_all (38 cols post-amendment; source FROM matches_flat mf)"
  schema_yaml: "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml"
  artifacts:
    - "reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.json"
    - "reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md"
key_findings:
  - "nickname_count: 246 (no drift from INVARIANTS.md §2 — zero-tolerance check PASSED)"
  - "toon_id_count: 1,923 distinct cross-region toon_ids"
  - "rows_flagged_true: 37,101; rows_flagged_false: 7,716; total: 44,817 (row count preserved)"
  - "handle_length_breakdown: lt_5=636, 5_to_7=831, ge_8=456 (per distinct toon_id)"
  - "NULL count in is_cross_region_fragmented: 0 (BOOLEAN by construction)"
  - "flag is blanket (no length filter): false positives bounded by lt_5=636 toons"
gate:
  continue_predicate: >
    player_history_all VIEW amended to 38 cols; row count 44,817 preserved;
    is_cross_region_fragmented BOOLEAN column fully populated (zero NULLs);
    01_04_05 JSON + MD artifacts exist.
  halt_predicate: >
    nickname_count drift detected vs INVARIANTS.md §2 (zero-tolerance per WP-3/WP-4 precedent).
```

---

### Step 01_05_01 — Q1 Quarterly Grain & Overlap Window

```yaml
step_number: "01_05_01"
name: "Q1 Quarterly Grain & Overlap Window"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset_full.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.md"
gate:
  continue_predicate: "quarterly_row_counts_sc2egset.csv has 10 rows with all count columns > 0."
  halt_predicate: "Any overlap quarter has zero rows."
```

### Step 01_05_02 — Q2 PSI Quarterly (Pre-Game Features)

```yaml
step_number: "01_05_02"
name: "Q2 PSI Quarterly (Pre-Game Features)"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_02_psi_quarterly.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/psi_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/plots/psi_vs_quarter_sc2egset.png"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/psi_quarterly_sc2egset.md"
gate:
  continue_predicate: "psi_sc2egset.csv has 24 rows; all psi_value finite."
  halt_predicate: "Any psi_value is NaN or Inf."
```

### Step 01_05_03 — Q3 Stratification & Secondary Regime

```yaml
step_number: "01_05_03"
name: "Q3 Stratification & Secondary Regime"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_03_stratification_regime.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/tournament_era_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/tournament_era_sc2egset.md"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/tournament_tier_lookup.csv"
gate:
  continue_predicate: "tournament_era_sc2egset.csv exists with >= 1 non-empty tier row."
  halt_predicate: "tournament_tier_lookup.csv has fewer than 70 rows."
```

### Step 01_05_04 — Q4 Triple Survivorship Analysis

```yaml
step_number: "01_05_04"
name: "Q4 Triple Survivorship Analysis"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sc2egset.md"
gate:
  continue_predicate: "survivorship_unconditional.csv has 10 rows; sensitivity.csv has >= 3 rows."
  halt_predicate: "Any overlap quarter has fraction_active = 0."
```

### Step 01_05_05 — Q6 Variance Decomposition & ICC

```yaml
step_number: "01_05_05"
name: "Q6 Variance Decomposition & ICC"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_05_variance_icc.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/variance_icc_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/icc.json"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/plots/icc_player_vs_faction.png"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/variance_icc_sc2egset.md"
gate:
  continue_predicate: "icc.json exists; primary ICC is in [0,1]; CI: low <= icc <= high."
  halt_predicate: "Both LPM and ANOVA ICC fits fail to converge."
```

### Step 01_05_06 — Q8 DGP Diagnostics (duration_seconds)

```yaml
step_number: "01_05_06"
name: "Q8 DGP Diagnostics (duration_seconds)"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_06_dgp_diagnostics.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/plots/dgp_diagnostic_duration_trend.png"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_sc2egset.md"
gate:
  continue_predicate: "dgp_diagnostic_sc2egset.csv exists; cohen_d values finite; prefix = dgp_diagnostic_."
  halt_predicate: "Output file named without dgp_diagnostic_ prefix."
```

### Step 01_05_07 — Phase 06 Interface CSV

```yaml
step_number: "01_05_07"
name: "Phase 06 Interface CSV"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.csv"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.schema.json"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.md"
gate:
  continue_predicate: "phase06_interface_sc2egset.csv has 9 columns exactly; dataset_tag = 'sc2egset' constant."
  halt_predicate: "Schema mismatch or empty file."
```

### Step 01_05_08 — Q7 Temporal Leakage Audit

```yaml
step_number: "01_05_08"
name: "Q7 Temporal Leakage Audit"
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_sc2_leakage_audit.py"
completed_at: "2026-04-18"
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.json"
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.md"
gate:
  continue_predicate: "leakage_audit_sc2egset.json: future_leak_count=0; post_game_token_violations=[]; reference_window_assertion=PASS; halt_triggered=false."
  halt_predicate: "halt_triggered=true."
```

### Step 01_05_09 — 01_05 exit memo (retroactive)

```yaml
step_number: "01_05_09"
name: "01_05 exit memo (retroactive)"
description: "Consolidate 01_05 findings into a single exit memo for Phase 01 gate consumption.
  Artifact authored 2026-04-18 (pre-01_06) and retroactively bound to this Step in
  01_06 ROADMAP refresh. Covers Q1..Q9 parameter groups, spec deviations, and
  gate verdict for 01_05."
pipeline_section: "01_05 -- Temporal & Panel EDA"
notebook_path: null
outputs:
  artifacts:
    - "reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md"
completed_at: "2026-04-18"
gate: "memo exists on disk; covers 01_05_01..01_05_08 findings"
```

---

### Step 01_06_01 — Data Dictionary

```yaml
step_number: "01_06_01"
name: "Data Dictionary"
description: "Enumerate every column consumed downstream in Phase 02 from matches_1v1_clean,
  player_history_all, and matches_history_minimal. Assign temporal_classification
  (PRE_GAME / POST_GAME_HISTORICAL / TARGET / METADATA / IDENTIFIER) per Invariant I3.
  Produce the data_dictionary_sc2egset.csv and .md companion per spec 01_06_readiness_criteria.md §1.1."
phase: "01 -- Data Exploration"
pipeline_section: "01_06 -- Decision Gates"
dataset: "sc2egset"
spec: "reports/specs/01_06_readiness_criteria.md v1.0"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/06_decision_gates/01_06_01_data_dictionary.py"
inputs:
  - "reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json"
  - "reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/"
outputs:
  data_artifacts:
    - "reports/artifacts/01_exploration/06_decision_gates/data_dictionary_sc2egset.csv"
  report: "reports/artifacts/01_exploration/06_decision_gates/data_dictionary_sc2egset.md"
gate:
  artifact_check: "CSV and MD exist; every Phase-02 feature-candidate column has a row."
  continue_predicate: "No POST_GAME column assigned PRE_GAME classification (I3 check)."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.1.1 SC2EGSet"
research_log_entry: "Required on completion."
```

### Step 01_06_02 — Data Quality Report

```yaml
step_number: "01_06_02"
name: "Data Quality Report"
description: "Consolidate 01_02_04 null/sentinel reports, 01_03 profiling artifacts,
  01_04_01 missingness ledger, 01_04_02 cleaning registry into a CONSORT flow.
  Trace each cleaning rule back to its registry entry. Produce per spec §1.2."
phase: "01 -- Data Exploration"
pipeline_section: "01_06 -- Decision Gates"
dataset: "sc2egset"
spec: "reports/specs/01_06_readiness_criteria.md v1.0"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/06_decision_gates/01_06_02_data_quality_report.py"
inputs:
  - "reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json"
  - "reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.json"
  - "reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
outputs:
  report: "reports/artifacts/01_exploration/06_decision_gates/data_quality_report_sc2egset.md"
gate:
  artifact_check: "MD exists with CONSORT flow, rule registry, route-decision table."
  continue_predicate: "CONSORT flow balanced (sum of drops = raw - clean)."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.2.3 Cleaning rules"
research_log_entry: "Required on completion."
```

### Step 01_06_03 — Risk Register

```yaml
step_number: "01_06_03"
name: "Risk Register"
description: "Enumerate every INVARIANTS.md §5 PARTIAL/VIOLATED row, every BACKLOG
  item affecting sc2egset, and every 01_05 adversarial-audit residual. Produce
  risk_register_sc2egset.csv and .md companion per spec §1.3."
phase: "01 -- Data Exploration"
pipeline_section: "01_06 -- Decision Gates"
dataset: "sc2egset"
spec: "reports/specs/01_06_readiness_criteria.md v1.0"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/06_decision_gates/01_06_03_risk_register.py"
inputs:
  - "reports/INVARIANTS.md"
  - "planning/BACKLOG.md"
  - "reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md"
  - "reports/artifacts/01_exploration/05_temporal_panel_eda/icc.json"
outputs:
  data_artifacts:
    - "reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.csv"
  report: "reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.md"
gate:
  artifact_check: "CSV and MD exist."
  continue_predicate: "Every INVARIANTS.md §5 non-HOLDS row has a corresponding risk_id."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.4.5 ICC estimator"
research_log_entry: "Required on completion."
```

### Step 01_06_04 — Modeling Readiness Decision

```yaml
step_number: "01_06_04"
name: "Modeling Readiness Decision"
description: "Consume 01_06_01..03 artifacts; produce the verdict memo per spec §2
  four-tier taxonomy. Assign READY_WITH_DECLARED_RESIDUALS with documented HIGH/MEDIUM
  residuals and Chapter 4 anchors. Produce modeling_readiness_sc2egset.md per spec §1.4."
phase: "01 -- Data Exploration"
pipeline_section: "01_06 -- Decision Gates"
dataset: "sc2egset"
spec: "reports/specs/01_06_readiness_criteria.md v1.0"
notebook_path: "sandbox/sc2/sc2egset/01_exploration/06_decision_gates/01_06_04_modeling_readiness.py"
inputs:
  - "reports/artifacts/01_exploration/06_decision_gates/data_dictionary_sc2egset.csv"
  - "reports/artifacts/01_exploration/06_decision_gates/data_quality_report_sc2egset.md"
  - "reports/artifacts/01_exploration/06_decision_gates/risk_register_sc2egset.csv"
outputs:
  report: "reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_sc2egset.md"
gate:
  artifact_check: "MD exists with verdict, flip-predicate, BLOCKER list, HIGH/MEDIUM residuals."
  continue_predicate: "Verdict stated verbatim from spec §2 taxonomy; each HIGH/MEDIUM residual has Chapter 4 anchor."
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.1.1 SC2EGSet"
research_log_entry: "Required on completion."
```

---

## Phase 02 — Feature Engineering

Pipeline Sections: see `docs/PHASES.md`.
Steps to be defined when Phase 01 gate is met.

**Mandatory entry requirement (added 2026-04-21 per WP-2):** Before any step in Pipeline Section 02_01 exits, a leakage-audit artifact must be produced per `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1, LOCKED 2026-05-06 (patch successor of CROSS-02-01-v1, LOCKED 2026-04-21)). The audit verifies cutoff-time structural filters, POST-GAME token absence from feature lineage, normalization fit-scope, and reference-window assertion. `verdict = PASS` is required for 02_01 exit. v1 enforcement is convention-based (reviewer-adversarial gate); automated tooling enforcement is a §7 future-amendment target. Input contract: `reports/specs/02_00_feature_input_contract.md` (CROSS-02-00-v3.0.1). Protocol is reused (not re-gated) by 02_03 and 02_06.

Reuse of the CROSS-02-01-v1.0.1 audit protocol by Pipeline Sections 02_03 and 02_06 follows CROSS-02-01-v1.0.1 §6. The design-time companion gate is `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1, LOCKED 2026-05-06); the design-time feature-family plan is `reports/specs/02_02_feature_engineering_plan.md` (CROSS-02-02-v1.0.1, LOCKED 2026-05-06).

### Pipeline Section 02_01 — Pre-Game vs In-Game Boundary

```yaml
step_number: "02_01_01"
name: "Feature-family registry skeleton (sc2egset)"
description: >-
  Per-dataset declaration of Phase 02 candidate feature families for sc2egset:
  family_id, prediction_setting (pre_game / history_enriched_pre_game /
  in_game_snapshot / blocked_or_deferred), source_table_or_event_family,
  source_grain, model_input_grain, temporal_anchor, allowed_cutoff_rule,
  candidate_leakage_modes, cold_start_handling, status. Registry is a
  planning / catalog artifact; no feature value is computed. Constrained by
  reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1),
  reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1),
  reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6,
  and reports/specs/02_03_temporal_feature_audit_protocol.md
  (CROSS-02-03-v1.0.1) D1–D15. SC2 in_game_snapshot families are bound by
  src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv:
  only rows with status_in_game_snapshot ∈ {eligible_for_phase02_now,
  eligible_with_caveat} may be declared (12 of 15 rows); the three
  blocked_until_additional_validation rows (mind_control_event_count,
  army_centroid_at_cutoff_snapshot, playerstats_cumulative_economy_fields)
  remain excluded. The slot_identity_consistency row is recorded by the
  CSV as status_in_game_snapshot = eligible_for_phase02_now with
  notes_for_phase02 = "feature-engineering sanity gate; not a model input"
  and eligibility_scope = "structural validity check: per-replay assertion
  …"; the Phase 02 registry MUST therefore represent it as a registry-level
  classification sanity_gate_not_model_input — a registry-introduced
  classification derived from the CSV's notes_for_phase02 + eligibility_scope
  fields and the PR #208 Phase 02 guidance, not a verbatim CSV
  status_in_game_snapshot value. The CSV's status_in_game_snapshot value
  for that row remains eligible_for_phase02_now and is NOT being
  reclassified at the CSV layer. Tracker-derived features are never pre-game
  (Invariant I3; Amendment 2 of PR #208). History features use
  history_time < target_time (strict inequality; CROSS-02-00-v3.0.1 §3.3);
  in_game_snapshot features use event.loop <= cutoff_loop. No magic
  cold-start constants — cold-start handling is expressed only as gate
  categories per CROSS-02-02-v1.0.1 §9 (G-CS-1 through G-CS-6). Per
  .claude/rules/data-analysis-lineage.md, no generated artifact is
  evidence until the upstream notebook's assumptions, falsifiers, and
  sanity checks are reviewed BEFORE artifact generation. NOT DELIVERED IN
  THIS ROADMAP-STUB PR — this entry only declares the future step per
  .claude/rules/data-analysis-lineage.md §"Non-batching rule for empirical
  work" sequence step 1.
phase: "02 -- Feature Engineering"
pipeline_section: "02_01 -- Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Which Phase 02 candidate feature families exist for sc2egset, declared
  per CROSS-02-02-v1.0.1 §6, and what is each family's CROSS-02-03-v1.0.1
  D1–D15 design-time disposition (allowed / allowed_with_caveat /
  blocked_until_validation / sanity_gate_not_model_input)?
method: >-
  Read CROSS-02-02-v1.0.1 §6 sc2egset feature-family rows and
  tracker_events_feature_eligibility.csv; emit a per-family registry row
  per CROSS-02-03-v1.0.1 §3 audit-object schema; classify each row
  according to CROSS-02-03-v1.0.1 §4 D1–D15 with N/A for inapplicable
  dimensions; record D13 SC2-tracker-eligibility verdicts directly from
  the CSV without re-derivation; produce a planning-only catalog. No
  feature value, no notebook output, no encoder fit. The notebook
  scaffold + one validation module that materialize this registry are
  produced by a SEPARATE FUTURE PR per .claude/rules/data-analysis-lineage.md
  §"Non-batching rule" sequence steps 2–9; THIS PR delivers only step 1
  (ROADMAP stub).
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting; source event
  family. SC2 races (Prot / Terr / Zerg / Rand) are stratification axes
  declared at the family level (see RISK-26 — Random race semantics) but
  not encoded as registry rows here.
predecessors: "01_06_04"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py
inputs:
  duckdb_tables:
    - "matches_history_minimal"
    - "player_history_all"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/06_decision_gates/modeling_readiness_sc2egset.md"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1)"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) §3 / §4 D1–D15"
    - ".claude/rules/data-analysis-lineage.md"
    - ".claude/scientific-invariants.md (I3, I5, I6, I7, I8, I9, I10)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_sc2egset.csv"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_sc2egset.md"
reproducibility: >-
  All registry rows derived from CROSS-02-02-v1.0.1 §6 and the tracker
  CSV at the cited path; no magic constants (Invariant I7); cold-start
  handling expressed as gate categories per CROSS-02-02-v1.0.1 §9
  (G-CS-1 through G-CS-6) — no numeric pseudocount m, threshold K,
  smoothing strength α, or imputation constant is declared at this layer.
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every history-feature family in the registry declares
      allowed_cutoff_rule "history_time < target_time" (strict; per
      CROSS-02-00-v3.0.1 §3.3). Every in_game_snapshot family declares
      "event.loop <= cutoff_loop". No tracker-derived family is declared
      with prediction_setting pre_game or history_enriched_pre_game
      (Amendment 2 of PR #208).
  - number: "5"
    how_upheld: >-
      Every per-player family declares symmetric focal_* / opponent_*
      construction; none commits a slot-asymmetric definition. RISK-24 is
      cited; the data-dependent slot-assignment falsifier is enumerated.
  - number: "6"
    how_upheld: >-
      Registry rows trace to CROSS-02-00-v3.0.1 §5 column classifications
      and the tracker CSV verbatim; no value is paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers. Every cold-start gate is declared as a category;
      every numeric value (window length, cutoff_loop, threshold K,
      pseudocount m, smoothing strength α) is deferred to a per-dataset
      Phase 02 ROADMAP step that derives it empirically from training
      folds or cites prior literature.
  - number: "8"
    how_upheld: >-
      Every per-dataset polymorphic vocabulary (race / civ, map,
      leaderboard) carries the dataset_tag = 'sc2egset' partition note;
      no encoder is declared as fit cross-dataset.
  - number: "9"
    how_upheld: >-
      Registry is read-only against Phase 01 outputs; no model is built;
      no source-stratified evaluation claim is encoded yet.
  - number: "10"
    how_upheld: >-
      No raw-table or feature-table filename is declared with an absolute
      path; lineage uses the same relative-path convention used by the
      Phase 01 raw tables.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only
    after the future scaffold-and-validation PR materializes the registry
    CSV + MD; at that point the predicate is "the planned CSV and MD
    exist at the declared paths and are non-empty."
  continue_predicate: >-
    A future PR may begin Step 02_01_02 (or the next 02_01 step in the
    ROADMAP) only after this Step 02_01_01 has reached its CSV + MD
    artifact-check at a future PR, the CROSS-02-01-v1.0.1
    post-materialization audit gate has been re-run for any feature
    column the registry triggers materialization of, and a per-family
    CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row.
  halt_predicate: >-
    Halt before generating any registry artifact if any of the following
    hold (per .claude/rules/data-analysis-lineage.md §"Stop conditions"):
      - any sc2egset tracker-derived row is declared with
        prediction_setting pre_game or history_enriched_pre_game
        (Invariant I3 violation; Amendment 2 of PR #208 violation);
      - any blocked_until_additional_validation tracker row from
        tracker_events_feature_eligibility.csv (mind_control_event_count,
        army_centroid_at_cutoff_snapshot, playerstats_cumulative_economy_fields)
        appears in the registry as an eligible candidate;
      - any history-derived row lacks the strict history_time < target_time
        cutoff against the per-dataset anchor (sc2egset:
        ph.details_timeUTC < target.started_at);
      - any in_game_snapshot row uses event.loop > cutoff_loop or expresses
        the cutoff only in seconds without a corresponding loop value
        (V1 lps caveat);
      - any cold-start row pins a numeric pseudocount, threshold, or
        smoothing constant without a fold-aware empirical derivation or
        literature citation (Invariant I7);
      - the future notebook scaffold attempts to batch ROADMAP +
        notebook + artifact + next step in one execution, contrary to
        the non-batching rule.
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > §4.5 Feature engineering plan (sc2egset registry)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md
  §"Non-batching rule" sequence (step 1 — ROADMAP stub only — does not
  produce a research_log entry). Required on the future scaffold-and-
  validation PR per the standard step-completion protocol; entry goes
  into src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

### Step 02_01_02 — First pre_game feature-family materialization (sc2egset)

```yaml
step_number: "02_01_02"
name: "First pre_game feature-family materialization (sc2egset)"
description: >-
  First MATERIALIZATION step of Pipeline Section 02_01: materialize the 5
  pre_game feature families declared allowed in the Step 02_01_01 registry
  (focal_race_with_opponent_race_pair, map_type_encoded, patch_version_encoded,
  matchup_encoded, is_mmr_missing_flag [pre-game missingness/provenance flag, NOT
  a skill feature; KEEP-IN-TRANCHE-1 per reviewer-adversarial]) into a
  per-(focal_match_id, focal_player)
  feature table, then re-run the CROSS-02-01-v1.0.1 post-materialization
  leakage audit on the resulting non-empty features_audited set. Scope is the
  minimal lowest-risk tranche: every selected family has status=allowed,
  candidate_leakage_modes=none, cold_start_handling=G-CS-1, and
  allowed_cutoff_rule=snapshot_at_match_start in
  02_01_01_feature_family_registry.csv. The 6 history_enriched_pre_game families
  (cold-start gates G-CS-2..G-CS-5; rolling/h2h/rating leakage modes) and the 11
  in_game_snapshot families (tracker-event-bound, event.loop <= cutoff_loop
  caveats) are DEFERRED to successor Steps 02_01_03+ so that distinct
  leakage-falsifier regimes are not batched into one notebook (per
  .claude/rules/data-analysis-lineage.md "Feature-engineering discipline").
  NO feature value is materialized in this ROADMAP-stub PR -- this entry only
  declares the future step per .claude/rules/data-analysis-lineage.md
  "Non-batching rule for empirical work" sequence step 1; the notebook scaffold,
  one validation module, materialization, and the post-materialization audit are
  produced by SEPARATE FUTURE PRs (sequence steps 2-9).
phase: "02 -- Feature Engineering"
pipeline_section: "02_01 -- Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Can the 5 allowed pre_game feature families from the Step 02_01_01 registry be
  materialized into a per-(focal_match_id, focal_player) feature table whose
  every column passes the CROSS-02-01-v1.0.1 post-materialization leakage audit
  with a NON-vacuous (non-empty features_audited) PASS verdict, under strict
  snapshot-at-match-start cutoff and symmetric focal/opponent construction?
method: >-
  For each of the 5 pre_game families, write a DuckDB projection over
  replay_players_raw / matches_flat keyed on (filename, player_id_worldwide)
  producing focal_* and opponent_* columns symmetrically (Invariant I5). The
  cutoff is snapshot_at_match_start: every column is read from the target game's
  own pre-game metadata (race, map, patch, matchup, MMR-missing flag) -- these are
  known-at-match-start fields, NOT history aggregates and NOT tracker-derived, so
  no history_time < target_time window applies and no post-game token may appear.
  Then run the CROSS-02-01-v1.0.1 audit (02_01_leakage_audit_protocol.md section
  2.1 cutoff structural check, 2.2 POST-GAME token absence, 2.3 normalization
  fit-scope) over the materialized columns; emit a NON-vacuous
  leakage_audit_sc2egset.{json,md} with features_audited = the 5 (or expanded
  focal_*/opponent_*) materialized column names. All non-trivial logic lives in
  src/rts_predict/ and is imported by the notebook. THIS PR delivers only the
  ROADMAP stub (sequence step 1); materialization is a separate future PR.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting = pre_game. SC2 races
  (Prot / Terr / Zerg / Rand) are stratification axes for the race-pair and
  matchup families (RISK-26 Random-race semantics cited); map_type and
  patch_version partition the encoded categoricals. Corpus-wide single-number
  aggregates are not an acceptable sole output.
predecessors: "02_01_01"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py
inputs:
  duckdb_tables:
    - "matches_flat"
    - "replay_players_raw"
    - "matches_history_minimal"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1) sections 2.1/2.2/2.3, 4 (materialization)"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) section 6, section 9 (G-CS-1)"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) section 4 D2/D3/D4/D5/D6/D8, section 10"
    - ".claude/rules/data-analysis-lineage.md"
    - ".claude/ml-protocol.md (three leakage failure modes)"
    - ".claude/scientific-invariants.md (I3, I5, I6, I7, I8, I9, I10)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_matrix.parquet"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.md"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md"
reproducibility: >-
  Every materialized column traces to a registry row in
  02_01_01_feature_family_registry.csv; every projection SQL is embedded verbatim
  in the report MD alongside its result (Invariant I6). No magic numbers
  (Invariant I7): pre_game families carry cold_start_handling G-CS-1 (no
  pseudocount / threshold / smoothing constant); encoder vocabularies are
  fit on training folds only (no cross-fold or cross-dataset fit). Seed 42
  convention; deterministic export; relative-path provenance (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every pre_game column is read at snapshot_at_match_start from the target
      game's own pre-game metadata; no history window and no tracker-derived
      value is used, so no information from game T or later enters. The
      post-materialization CROSS-02-01-v1.0.1 section 2.2 POST-GAME token absence
      check is run on the materialized set and must report 0 violations.
  - number: "5"
    how_upheld: >-
      The same projection produces focal_* and opponent_* columns symmetrically;
      no player slot is privileged. RISK-24 data-dependent slot-assignment
      falsifier is enumerated in the materialization notebook.
  - number: "6"
    how_upheld: >-
      Every reported count/distribution in the report MD is accompanied by its
      verbatim DuckDB SQL; no value is paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers -- pre_game families are G-CS-1 (no cold-start constant);
      any later numeric (cutoff_loop, window length) belongs to deferred
      in_game / history tranches, not this Step.
  - number: "8"
    how_upheld: >-
      The 5 pre_game families are exactly the shared cross-game pre-game
      categories (faction matchup, map) named in Invariant I8; encoders carry the
      dataset_tag = 'sc2egset' partition note and are not fit cross-dataset,
      preserving cross-game comparability for the AoE2 datasets.
  - number: "9"
    how_upheld: >-
      The Step reads only Phase 01 outputs and the CLOSED Step 02_01_01 catalog
      artifacts (all lower-numbered, on disk); it makes no source-stratified
      evaluation claim and builds no model.
  - number: "10"
    how_upheld: >-
      The materialized feature table and its provenance use the relative-path
      convention; no absolute path is written to any artifact.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only after
    the future scaffold-and-materialization PR materializes the feature table +
    the NON-vacuous CROSS-02-01-v1.0.1 audit pair; at that point the predicate is
    "the planned Parquet feature matrix, the audit JSON, and both report MDs
    exist at the declared paths and are non-empty, and the audit JSON has
    features_audited != [] with verdict = PASS."
  continue_predicate: >-
    A future PR may begin Step 02_01_03 (the next 02_01 materialization step --
    history_enriched_pre_game tranche) only after this Step 02_01_02 has reached
    its artifact-check at a future PR, the CROSS-02-01-v1.0.1 post-materialization
    audit has returned a NON-vacuous PASS (future_leak_count = 0,
    post_game_token_violations = 0 over a non-empty features_audited), and a
    per-family CROSS-02-03-v1.0.1 section 10 verdict consistent with the
    materialized columns is recorded. The §10 design-time verdict audit (PR #229)
    is a distinct artifact and does NOT substitute for this post-materialization
    CROSS-02-01 audit (PR #230 evidence remains distinct from PR #229 evidence).
  halt_predicate: >-
    Halt before generating any feature artifact if any of the following hold
    (per .claude/rules/data-analysis-lineage.md "Stop conditions"):
      - any materialized pre_game column reads a value that is not knowable at
        snapshot_at_match_start (Invariant I3 violation);
      - the CROSS-02-01-v1.0.1 section 2.2 POST-GAME token absence check reports
        any violation on the materialized set;
      - any family outside the 5 allowed pre_game rows is materialized in this
        Step (scope creep into the deferred history / in_game tranches);
      - the focal_* / opponent_* construction is asymmetric (Invariant I5);
      - any encoder is fit on validation/test folds or cross-dataset
        (normalization leakage, Invariant I3);
      - the future notebook scaffold attempts to batch ROADMAP + notebook +
        artifact + next step in one execution (non-batching rule).
thesis_mapping:
  - "Chapter 4 -- Data and Methodology > 4.5 Feature engineering plan (sc2egset pre_game materialization)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per .claude/rules/data-analysis-lineage.md
  "Non-batching rule" sequence (step 1 -- ROADMAP stub only -- produces no
  research_log entry). Required on the future scaffold-and-materialization PR per
  the standard step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

### Step 02_01_03 — History-enriched pre_game feature-family materialization (sc2egset)

```yaml
step_number: "02_01_03"
name: "History-enriched pre_game feature-family materialization (sc2egset)"
description: >-
  Second MATERIALIZATION step of Pipeline Section 02_01: materialize the 6
  history_enriched_pre_game feature families declared allowed (or
  allowed_with_caveat for cross_region_fragmentation_handling) in the closed
  Step 02_01_01 registry — focal_player_history, opponent_player_history,
  matchup_history_aggregate, reconstructed_rating,
  cross_region_fragmentation_handling, in_game_history_aggregate. Then
  re-run the CROSS-02-01-v1.0.1 post-materialization leakage audit on the
  resulting non-empty features_audited set. Strict history cutoff:
  history_time < target_time (per CROSS-02-02 §6.2 row 1 strict-less-than;
  Invariant I3; CROSS-02-00-v3.0.1 §3.3; CROSS-02-03 §5.1). Per-dataset
  history anchor: ph.details_timeUTC < target.started_at. The 6th family
  in_game_history_aggregate aggregates IN_GAME_HISTORICAL columns
  (APM/SQ/supplyCappedPercent/header_elapsedGameLoops) over PRIOR matches;
  these columns are retained in scope per CROSS-02-02 §6.2 row 6 for
  history-aggregation use while remaining forbidden as direct game-T
  pre-game features. No tracker_events_raw source for any family (Invariant
  I3; Amendment 2 of PR #208). The 5 closed pre_game families materialized
  by PR #236 are READ as upstream evidence inputs but NOT re-materialized.
  The 11 in_game_snapshot families (tracker-event-bound) are DEFERRED to a
  successor Step 02_01_04+. Lineage position: ROADMAP stub is artifact #1
  of N for Step 02_01_03 readiness (subsequent artifacts: notebook scaffold
  + one validator, tranche-2 source/anchor/cold-start adjudication,
  materialization-execution plan, materialization-execution, closure).
  This is the SECOND materialization tranche of Pipeline Section 02_01;
  tranche 1 (PR #236) materialized 5 pre_game families; tranche 3 (future
  Step 02_01_04) will materialize in_game_snapshot families. NO feature
  value is materialized in this ROADMAP-stub PR — this entry only declares
  the future step per .claude/rules/data-analysis-lineage.md "Non-batching
  rule for empirical work" sequence step 1; the notebook scaffold, one
  validation module, source/anchor/cold-start adjudication, materialization,
  and the post-materialization audit are produced by SEPARATE FUTURE PRs
  (sequence steps 2-9).
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Can the 6 allowed history_enriched_pre_game feature families from the
  closed Step 02_01_01 registry be materialized into a
  per-(focal_match_id, focal_player) feature table whose every column
  passes the CROSS-02-01-v1.0.1 post-materialization leakage audit with a
  NON-vacuous (non-empty features_audited) PASS verdict, under strict
  history_time < target_time cutoff (no <=, no closed-interval window, no
  target-match final state — covers G-L-1, G-L-3, G-L-4, G-L-7),
  symmetric focal/opponent construction (Invariant I5), and explicit
  cold-start handling per CROSS-02-02 §9 (G-CS-2 through G-CS-6)?
method: >-
  For each of the 6 history_enriched_pre_game families, write a DuckDB
  projection over matches_flat_clean joined to player_history_all keyed on
  (player_id_worldwide) and filtered by ph.details_timeUTC <
  target.started_at (STRICT inequality; Invariant I3; G-L-1 prohibits <=;
  G-L-3 prohibits target-match final state; G-L-7 prohibits rolling /
  h2h that include the target match). Produce focal_* and opponent_*
  columns symmetrically (Invariant I5). Cold-start handling per family:
  G-CS-2 (allow cold_start flag with declared threshold derivation) /
  G-CS-3 (empirical smoothing-prior derivation from training fold only) /
  G-CS-4 (no global rating fit; rating reconstructed forward in time from
  prior decisive results only) / G-CS-5 (per-source cold-start
  enumeration) / G-CS-6 (encoder + smoothing-prior fit on training folds
  only). All smoothing/threshold constants empirically derived from
  training folds only (Invariant I3 normalization discipline + G-CS-6) or
  cited from literature (Invariant I7). Run the CROSS-02-01-v1.0.1 audit
  (sections 2.1 cutoff structural check, 2.2 POST-GAME token absence, 2.3
  normalization fit-scope, 2.4 reference window) over the materialized
  columns; emit a NON-vacuous leakage_audit_sc2egset.{json,md} under
  reports/artifacts/02_01_03/ with features_audited = the full set of
  focal_* + opponent_* + matchup_* + rating_* + sensitivity column names.
  All non-trivial logic in src/rts_predict/. THIS PR delivers only the
  ROADMAP stub (sequence step 1); materialization is a separate future PR.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting =
  history_enriched_pre_game. SC2 races (Prot / Terr / Zerg) are
  stratification axes for matchup_history_aggregate (vocabulary {Prot,
  Terr, Zerg} per closed PR #234 Q3.RATIFY; Random handled per
  documented_gap noted in PR #234 §8). Cross-region fragmentation
  sensitivity arm is co-stratified (with vs without filter) per
  CROSS-02-02 §6.2 row 5 / RISK-20; the choice between (a)
  strict-exclusion, (b) dual-feature-path, (c) sensitivity-indicator
  co-registration is DEFERRED to the tranche-2 source/anchor/cold-start
  adjudication PR (analogous to PR #234 for tranche-1).
predecessors: "02_01_02"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py
inputs:
  duckdb_tables:
    - "matches_flat_clean"
    - "matches_history_minimal"
    - "player_history_all"
  schema_yamls:
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml"
    - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml"
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv"
  external_references:
    - "reports/specs/02_00_feature_input_contract.md (CROSS-02-00-v3.0.1) §3.3 strict-less-than rule, §5.4 SC2 column classification (IN_GAME_HISTORICAL distinct from IN_GAME)"
    - "reports/specs/02_01_leakage_audit_protocol.md (CROSS-02-01-v1.0.1) §2.1 / §2.2 / §2.3 / §2.4"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1) §6.2 (6 history families; row 6 IN_GAME_HISTORICAL retention note), §9 (G-CS-2 / G-CS-3 / G-CS-4 / G-CS-5 / G-CS-6), §10 (G-L-1 / G-L-3 / G-L-4 / G-L-7)"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (CROSS-02-03-v1.0.1) §3 audit object, §4 D1-D15, §5.1 strict-less-than, §6.2 history_enriched_pre_game prediction-setting rules, §10 verdicts"
    - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact)"
    - ".claude/ml-protocol.md (three leakage failure modes — rolling, h2h, co-occurring matches)"
    - ".claude/scientific-invariants.md (I3 temporal, I3 normalization, I5 symmetry, I6 SQL provenance, I7 no magic numbers, I8 cross-game, I9 step-derived conclusions, I10 relative-path)"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/methodology_risk_register.md (RISK-20 cross-region fragmentation; RISK-24 slot asymmetry; RISK-26 Random race semantics)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.md"
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md"
reproducibility: >-
  Every materialized column traces to a registry row in
  02_01_01_feature_family_registry.csv (rows 7-12); every projection SQL
  with its strict-< history filter is embedded verbatim in the report MD
  alongside its result (Invariant I6). No magic numbers (Invariant I7):
  cold-start thresholds (K), smoothing pseudocounts (m), and Bayesian
  prior strengths (alpha) are either empirically derived from training
  folds only (G-CS-1 / G-CS-3) or cited from literature; the derivation
  procedure is recorded in the materialization PR's report MD. Encoder
  and smoothing-prior fit on training folds only (G-CS-6; CROSS-02-01
  §2.3). Glicko-2 rating reconstructed forward in time match-by-match —
  no global / batch fit. Seed 42 convention; deterministic export;
  relative-path provenance (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Every history-derived column applies STRICT ph.details_timeUTC <
      target.started_at; no closed-interval, no <=, no rolling window
      that includes the target match (G-L-1, G-L-3, G-L-7). Rating
      reconstruction is forward in time only — game T's outcome never
      enters game T's rating feature (CROSS-02-02 §10 G-L-4). All
      smoothing/scaling/imputation statistics are fit on training folds
      only (Invariant I3 normalization-leakage discipline; G-CS-6). No
      tracker-derived source (Invariant I3; Amendment 2 of PR #208).
  - number: "5"
    how_upheld: >-
      Every per-player family produces focal_* and opponent_* columns
      symmetrically via the same SQL pattern; no player slot is
      privileged. RISK-24 data-dependent slot-assignment falsifier
      enumerated in the materialization notebook.
  - number: "6"
    how_upheld: >-
      Every reported count/distribution in the report MD is accompanied
      by its verbatim DuckDB SQL with the strict-< filter; no value is
      paraphrased.
  - number: "7"
    how_upheld: >-
      No magic numbers. Cold-start threshold K, smoothing pseudocount m,
      Bayesian prior strength alpha, and rating-reconstruction
      hyperparameters are each either empirically derived from training
      folds (G-CS-1/G-CS-3/G-CS-6) or cited from literature with the
      citation embedded in the materialization PR's report MD.
  - number: "8"
    how_upheld: >-
      The 6 history families are the shared cross-game history
      categories (player_history, opponent_history, matchup_history,
      reconstructed rating) named in Invariant I8; encoders + smoothing
      priors carry dataset_tag = 'sc2egset' partition and are not fit
      cross-dataset.
  - number: "9"
    how_upheld: >-
      The Step reads only Phase 01 outputs and the CLOSED Steps 02_01_01
      + 02_01_02 artifacts (all lower-numbered, on disk); builds no
      model; makes no source-stratified evaluation claim.
  - number: "10"
    how_upheld: >-
      The materialized feature table and its provenance use the
      relative-path convention; no absolute path is written to any
      artifact.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires only
    after the future scaffold-and-materialization PR materializes the
    feature table + the NON-vacuous CROSS-02-01-v1.0.1 audit pair; at
    that point the predicate is "the planned Parquet feature matrix, the
    audit JSON, and both report MDs exist at the declared paths and are
    non-empty, the audit JSON has features_audited != [] with verdict =
    PASS, and every history column projected applied a strict-<
    ph.details_timeUTC < target.started_at filter verifiable in the
    materialization SQL."
  continue_predicate: >-
    A future PR may begin Step 02_01_04 (the next 02_01 materialization
    step — in_game_snapshot tranche) only after this Step 02_01_03 has
    reached its artifact-check at a future PR, the CROSS-02-01-v1.0.1
    post-materialization audit has returned a NON-vacuous PASS
    (future_leak_count = 0, post_game_token_violations = 0 over a
    non-empty features_audited covering all 6 history families'
    materialized columns), and a per-family CROSS-02-03-v1.0.1 §10
    verdict consistent with the materialized columns is recorded. The
    §10 design-time verdict audit (PR #229) is a distinct artifact and
    does NOT substitute for this post-materialization CROSS-02-01 audit;
    a re-executed §10 audit over the 6 history rows (distinct from the
    PR #229 design-time audit that covered the catalog at registry-
    creation time) is required before tranche-3 may begin, OR a
    non-vacuous justification for not re-running must be recorded in the
    materialization PR's research_log entry.
  halt_predicate: >-
    Halt before generating any feature artifact if any of the following
    hold (per .claude/rules/data-analysis-lineage.md "Stop conditions"):
      - any materialized history column uses <= or no time filter
        (G-L-1 violation; Invariant I3);
      - any rolling aggregate or head-to-head aggregate includes the
        target match's own row (G-L-7);
      - any history column uses the target match's final state
        (G-L-3 violation);
      - any rating uses game T's outcome (G-L-4);
      - any encoder, scaler, smoothing prior, or rating-reconstruction
        hyperparameter is fit on validation/test folds, on the full
        dataset, or cross-dataset (Invariant I3 normalization-leakage;
        G-CS-6);
      - any tracker_events_raw column is read for a history family
        (Invariant I3; Amendment 2 of PR #208);
      - any family outside the 6 history_enriched_pre_game rows is
        materialized in this Step (scope creep into the deferred
        in_game_snapshot tranche);
      - any cold-start row pins a numeric pseudocount, threshold, or
        smoothing constant without a fold-aware empirical derivation or
        literature citation (Invariant I7; G-CS-1);
      - the focal_* / opponent_* construction is asymmetric (Invariant
        I5; RISK-24);
      - the cross_region_fragmentation_handling sensitivity arm is
        materialized without prior tranche-2 source/anchor/cold-start
        adjudication selecting (a) strict-exclusion, (b) dual-path, or
        (c) sensitivity-indicator co-registration (CROSS-02-02 §6.2
        row 5; RISK-20);
      - the future notebook scaffold attempts to batch ROADMAP +
        notebook + artifact + next step in one execution (non-batching
        rule);
      - any future-Step pre-emption appears (e.g., 02_01_04 in_game
        material in the same PR).
thesis_mapping:
  - "Chapter 4 — Data and Methodology > §4.5 Feature engineering plan (sc2egset history_enriched_pre_game materialization)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per
  .claude/rules/data-analysis-lineage.md "Non-batching rule" sequence
  (step 1 — ROADMAP stub only — produces no research_log entry).
  Required on the future scaffold-and-materialization PR per the
  standard step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

##### Materialization-scope amendment (post-PR #255)

<!-- amendment_id: materialization_scope_amendment_post_pr_255 -->

**Status:** materialization_scope_amendment_post_pr_255 — recorded by PR #257 (the Layer-2 execution PR materialising this amendment).

**Effect on Step 02_01_03:** the original six-family declaration above (including
`reconstructed_rating`) remains BINDING as the historical record of the closed
Q-chain. The MATERIALIZATION PATH that Step 02_01_03 will execute under is
NARROWED to exactly five families:

1. `focal_player_history`
2. `opponent_player_history`
3. `matchup_history_aggregate`
4. `cross_region_fragmentation_handling`
5. `in_game_history_aggregate`

The 6th family `reconstructed_rating` is EXCLUDED from the materialization path.

**Excluded columns (verbatim):**

- `reconstructed_rating_focal_pre`
- `reconstructed_rating_opp_pre`
- `reconstructed_rating_diff`

**Q6 omission status:** `intentionally_omitted_under_branch_iii`. The exclusion of
`reconstructed_rating` is NOT silent satisfaction of Q6 — it is the explicit
recording of Q6H Branch (iii) elevation per PR #255 row field
`q6_not_silently_satisfied = TRUE`.

**Authority basis (parent artifacts):**

- PR #243 Q5 cross-region adjudication (`02_01_03_history_cross_region_adjudication.{csv,md}`).
- PR #247 Q6F rating-algorithm survey (`02_01_03_q6f_rating_algorithm_survey.{csv,md}`).
- PR #249 Q6G rating-implementation proof (`02_01_03_q6g_rating_implementation_proof.{csv,md}`).
- PR #251 Q6H rating-path decision (`02_01_03_q6h_rating_path_decision.{csv,md}`).
- PR #253 ROADMAP stub for Step 02_01_99.
- PR #255 omit-closure decision artifact (`02_01_99_rating_omit_closure.{csv,md}`)
  with `decision_verdict = omit_reconstructed_rating_and_unblock_other_five`.

**Scope of this amendment:**

- NO feature value materialization. No `.parquet` is produced by this amendment PR.
- NO CROSS-02-01 post-materialization audit. No
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` is created.
- NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml`
  row addition or mutation.
- NO `research_log.md` entry (dataset or root).
- NO Step 02_01_04 start.
- NO Phase 03 start.
- NO new Q6X PR (Q6H is terminal per PR #251).

**Continue-predicate (updated):** Feature materialization for Step 02_01_03 may
proceed in a future PR only when ALL of the following hold:

1. The materialized columns cover exactly the five permitted families listed
   above (no more, no fewer).
2. No column with name matching `reconstructed_rating_focal_pre`,
   `reconstructed_rating_opp_pre`, or `reconstructed_rating_diff` (or any other
   `reconstructed_rating_*` token) is materialized.
3. The CROSS-02-01 post-materialization audit is NON-vacuous (`features_audited`
   covers exactly the five families' materialized columns) and returns
   `verdict = PASS`.
4. All Q5/Q6F/Q6G/Q6H parent artifact bytes are unchanged (no Q-chain
   re-adjudication).
5. PR #255 omit-closure artifact bytes are unchanged.

**Halt-predicate (updated):** Halt before any future PR proceeds if:

- any `reconstructed_rating_*` column is generated;
- the exact five-family set drifts (renamed, reordered, added to, dropped from);
- the PR #255 omit-closure artifact bytes drift from the SHA pinned at this PR's
  merge time;
- any Q5 (PR #243), Q6F (PR #247), Q6G (PR #249), or Q6H (PR #251) parent
  artifact's bytes drift;
- any target-match outcome, future-match outcome, or Phase 03 split leakage is
  introduced into any feature column;
- any `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, or
  `research_log.md` is edited in this scope-amendment PR;
- any feature `.parquet`, CROSS-02-01 audit JSON/MD, or
  `reports/artifacts/02_01_03/` file is produced in this scope-amendment PR.

**Step 02_01_03 closure status:** OPEN. This amendment does NOT close Step
02_01_03. Closure requires (a) actual five-family materialization (a separate
future PR), (b) a non-vacuous CROSS-02-01 post-materialization audit on the five
families' columns, and (c) a separate closure PR analogous to PR #237 for Step
02_01_02. Until all three conditions are met, Step 02_01_03 remains absent from
`STEP_STATUS.yaml` (status row is added by the closure PR, not by this
amendment).

**Forward path (informational, not a commitment):** the next planned PR after
this amendment merges is the five-family materialization PR (planned branch
`feat/sc2egset-02-01-03-five-family-materialization`), followed by the formal
Step 02_01_03 closure PR.

---

### Step 02_01_99 — Rating omit-closure follow-up stub (sc2egset)

```yaml
step_number: "02_01_99"
name: "Rating omit-closure follow-up to Step 02_01_03 Q6H Branch (iii) (sc2egset)"
description: >-
  ROADMAP-only stub declaring Step 02_01_99 — the rating omit-closure
  follow-up to Step 02_01_03's Q6H Branch (ii) verdict. Purpose:
  prepare a future omit-closure artifact PR (Layer-3) that may satisfy
  Q6H Branch (iii) preconditions and elevate `thesis_pragmatism` to
  TRUE under explicit reviewer-adversarial sign-off. This stub does
  NOT select Q6H Branch (iii) by itself; merely creating the stub
  does NOT close Q6 or unblock 5-family materialization. Step
  02_01_03's existing 6-family declaration (including the
  `reconstructed_rating` family) remains BINDING and byte-unchanged
  until a later approved scope amendment that lands AFTER the future
  omit-closure artifact PR merges. Authority basis: Q6H §17 verbatim:
  "Step 02_01_03 closure is deferred to a future PR (Layer-3
  materialization or omit-closure follow-up)" — this stub declares
  the omit-closure follow-up path. Branch-name deviation: the git
  branch slug `feat/sc2egset-02-01-03b-omit-closure-roadmap-stub`
  retains the historical `02-01-03b` hyphenated form for
  git-history continuity per the Layer-1 plan's A11 binding (PR #252);
  the on-disk step_number is the canonical `02_01_99`.
  NO ARTIFACT is emitted in this ROADMAP-stub PR — this entry only
  declares the future step per `.claude/rules/data-analysis-lineage.md`
  "Non-batching rule for empirical work" sequence step 1; the
  omit-closure decision artifact + scaffold + validator are produced
  by SEPARATE FUTURE PRs (sequence steps 2-7).
phase: "02 — Feature Engineering"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"
dataset: "sc2egset"
question: >-
  Under the Q6H §17 two-path admission (omit-closure or Layer-3
  materialization), is the omit-closure path methodologically
  admissible under the 4 Branch (iii) preconditions enumerated in
  decide_history_rating_path.py lines 457-481, with thesis_pragmatism
  elevated to TRUE under explicit reviewer-adversarial sign-off, the
  Q6H §15 standby paragraph re-verified as >=6 sentences AND >=3
  PR #249 §X.Y cross-references, and Branches (i) and (ii) recorded
  as blocked for materialization-scope purposes?
method: >-
  Step 02_01_99 itself does NOT execute the omit-closure decision.
  This is a ROADMAP-only stub. The future omit-closure artifact PR
  (3 PRs downstream from this stub per the canonical PR #238 -> PR
  #239 -> PR #240 -> PR #241 -> PR #242 ladder precedent) will: (a)
  read Q6H artifact pair byte-unchanged from PR #251; (b) re-verify
  Q6H §15 sentence count (>=6) and PR #249 cross-reference count
  (>=3); (c) record explicit `thesis_pragmatism = TRUE` elevation
  with rationale referencing PR #249 + PR #251 evidence; (d) obtain
  explicit reviewer-adversarial sign-off; (e) emit a CSV + MD
  decision artifact pair recording the elevation and the 5-family
  unblock per the verbatim `Q6H_FIVE_FAMILY_POST_OMIT_SET` constant
  (`focal_player_history`, `opponent_player_history`,
  `matchup_history_aggregate`, `cross_region_fragmentation_handling`,
  `in_game_history_aggregate`); (f) emit NO Parquet, NO CROSS-02-01
  audit, NO feature materialization, NO status YAML flip. The lineage
  mirrors PR #238 -> #239 -> #240 -> #241 -> #242 for Step 02_01_03.
  OQ7 wording/traceability bridge: Branch (ii) will be recorded as
  blocked-by-Layer-2-election (not evidence-deficit) in the future
  omit-closure artifact MD §N; this stub does NOT pre-determine that
  recording — it is deferred to the omit-closure artifact's own
  Layer-1 plan.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting =
  history_enriched_pre_game. Omit-closure is a single decision
  artifact, not a feature aggregation (analogous to PR #251 Q6H
  stratification).
predecessors: "02_01_03"
notebook_path: >-
  sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.py
inputs:
  duckdb_tables: []
  schema_yamls: []
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6h_rating_path_decision.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6g_rating_implementation_proof.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv"
  external_references:
    - "Q6H §17 verbatim: Step 02_01_03 closure is deferred to a future PR (Layer-3 materialization or omit-closure follow-up)"
    - "Q6H §15 standby paragraph admissibility: >=6 sentences + >=3 PR #249 §X.Y cross-references"
    - "decide_history_rating_path.py: Q6H_FIVE_FAMILY_POST_OMIT_SET constant (5 families)"
    - "decide_history_rating_path.py: Branch (iii) preconditions literal (lines 457-481)"
    - "decide_history_rating_path.py: override falsifier q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15"
    - ".claude/rules/data-analysis-lineage.md (non-batching rule; halt-before-artifact)"
    - ".claude/scientific-invariants.md (I3, I6, I7, I9, I10)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.csv"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_omit_closure_decision.md"
reproducibility: >-
  Every column in the future omit-closure CSV traces to either the
  Q6H decision module's Branch (iii) literal or the Q6H §15 paragraph.
  Every count/distribution embedded in the MD must include its
  derivation. The Branch (iii) elevation rationale must include
  explicit reviewer-adversarial sign-off SHA. Seed 42 convention.
  Relative-path provenance (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Temporal discipline is preserved by the omit-closure path: no
      feature values are computed in this ROADMAP stub. The future
      omit-closure artifact PR's decision does not produce Parquet or
      feature columns; temporal leakage discipline (strict
      history_time < target_time) applies only when the 5-family
      materialization PR executes (a separate future PR).
  - number: "6"
    how_upheld: >-
      The future omit-closure artifact MD must embed verbatim any
      count/distribution it reports with its derivation SQL or
      source reference. No value may be paraphrased.
  - number: "7"
    how_upheld: >-
      Branch (iii) preconditions are evidentiary admissibility
      criteria, not magic booleans. The substantive paragraph +
      reviewer sign-off pins prevent boolean-driven closure. No magic
      numbers in the omit-closure artifact.
  - number: "9"
    how_upheld: >-
      Step 02_01_99 conclusions derive only from its own future
      artifacts and from completed predecessor steps' artifacts
      (Q6H artifact pair from PR #251 and prior Q-chain artifacts
      from PRs #242-#249), all lower-numbered and on disk.
  - number: "10"
    how_upheld: >-
      The future omit-closure artifact uses relative paths in all
      SHA pins; no absolute path written to any artifact. This
      ROADMAP stub itself uses only relative artifact paths.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires
    only after the future omit-closure artifact PR materializes the
    CSV + MD decision pair. At that point the predicate is: (a) the
    planned CSV and MD exist at the declared paths and are non-empty;
    (b) the CSV records `decision_verdict =
    omit_reconstructed_rating_and_unblock_other_five`; (c) the MD
    §N records explicit `thesis_pragmatism = TRUE` elevation with
    rationale; (d) Q6H §15 sentence count >= 6 and PR #249
    cross-reference count >= 3 are re-verified; (e) reviewer-
    adversarial sign-off SHA is present; (f) the 5-family post-omit
    set matches Q6H_FIVE_FAMILY_POST_OMIT_SET exactly; (g) no
    Parquet, no CROSS-02-01 audit artifact, no feature column, no
    status YAML flip is present in the omit-closure artifact PR diff.
  continue_predicate: >-
    A future PR may begin the 5-family ROADMAP narrowing (amending
    Step 02_01_03's 6-family declaration to 5 families) only after
    the omit-closure artifact PR merges with a passing artifact_check.
    A future PR may begin 5-family feature materialization only after
    the 5-family ROADMAP narrowing PR merges. Step 02_01_03 closure
    (STEP_STATUS flip to `complete`) happens only after BOTH the
    omit-closure artifact AND the 5-family materialization artifact
    merge (or a documented alternative closure pathway). No direct
    skip from this stub to feature materialization, CROSS-02-01 audit,
    or status YAML flip.
  halt_predicate: >-
    Halt before generating the omit-closure artifact if any of the
    following hold:
      - Q6H §15 sentence count drops below 6 (Branch (iii)
        precondition fails);
      - Q6H §15 cross-reference count to PR #249 §X.Y drops below 3
        (Branch (iii) precondition fails);
      - the override falsifier
        `q6h_thesis_pragmatism_set_false_without_substantive_reasoning_paragraph_in_md_section_15`
        would fire (Q6H §15 paragraph has been silently removed or
        degraded);
      - `Q6H_FIVE_FAMILY_POST_OMIT_SET` count != 5 or contains
        `reconstructed_rating`;
      - Q6H artifact pair SHAs do not match PR #251 merge SHAs;
      - reviewer-adversarial sign-off is missing from the omit-closure
        artifact PR's `planning/current_plan.critique.md`;
      - the omit-closure artifact PR attempts to mutate Q6H artifact
        bytes (Q5/Q6F/Q6G/Q6H re-adjudication ban);
      - the omit-closure artifact PR attempts a 5-family ROADMAP
        narrowing (the narrowing is a SEPARATE downstream PR);
      - the omit-closure artifact PR attempts a STEP_STATUS flip
        (the flip is a SEPARATE downstream PR);
      - the future scaffold attempts to batch ROADMAP + notebook +
        artifact + next step in one execution (non-batching rule);
      - any feature artifact (.parquet, .csv, .md under
        reports/artifacts/02_feature_engineering/) is produced by
        the ROADMAP stub PR (this PR);
      - any CROSS-02-01 audit artifact
        (reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md})
        is produced by this PR;
      - STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, or
        PHASE_STATUS.yaml is edited in this PR;
      - dataset or root research_log.md is edited in this PR;
      - Step 02_01_03 ROADMAP block family list is modified in this PR;
      - reconstructed_rating is silently removed from Step 02_01_03
        in this PR;
      - Phase 03 or Step 02_01_04 is started;
      - another Q6X PR is opened (Q6H is terminal).
thesis_mapping:
  - "Chapter 4 — Data and Methodology > §4.5 Feature engineering plan (sc2egset rating omit-closure decision)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per
  .claude/rules/data-analysis-lineage.md "Non-batching rule" sequence
  (step 1 — ROADMAP stub only — produces no research_log entry).
  Required on the future omit-closure artifact PR per the standard
  step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

##### Materialization-scope amendment back-reference (post-PR #255)

<!-- amendment_id: materialization_scope_amendment_post_pr_255 (back-reference) -->

PR #255 (omit-closure decision artifact, merged 2026-05-28 at
`52f9c1082b200019d080cce74e60567452020e18`) satisfied the four preconditions
declared in this Step 02_01_99's `question` field. The downstream
`materialization_scope_amendment_post_pr_255` note is recorded against Step
02_01_03 above; see the host amendment block for the five permitted families,
the excluded family `reconstructed_rating`, the three excluded columns, and the
updated continue-predicate / halt-predicate. Step 02_01_99 itself remains a
ROADMAP-only stub; no new artifact, no new YAML row, no status flip is
introduced by the amendment.

---

### Step 02_02_01 — Symmetry & difference feature planning stub (sc2egset)

```yaml
step_number: "02_02_01"
name: "Symmetry & difference feature planning stub (sc2egset)"
description: >-
  ROADMAP-only stub declaring Step 02_02_01 — the first step of
  Pipeline Section 02_02 (Symmetry & Difference Features). Purpose:
  open the section that will transform focal/opponent paired features
  materialized by Step 02_01_03 into symmetric / difference
  representations suitable for slot-orthogonal tabular modelling per
  Invariant I5 (focal/opponent symmetry) and the
  02_FEATURE_ENGINEERING_MANUAL.md §3 Bradley-Terry argument
  ("Symmetry in Pairwise Prediction Demands Difference Features").
  NO ARTIFACT is emitted in this ROADMAP-stub PR — this entry only
  declares the future step per `.claude/rules/data-analysis-lineage.md`
  "Non-batching rule for empirical work" sequence step 1; the notebook
  scaffold + one validation module + any adjudication artifacts +
  materialization are produced by SEPARATE FUTURE PRs (sequence steps
  2-9), mirroring the PR #232 -> #233 -> #234 -> #235 -> #236 -> #237
  ladder for Step 02_01_02 and the PR #239 -> #241 -> #242 -> ... ->
  #259 -> #262 ladder for Step 02_01_03. Halt-clause section: Phase 03
  is BARRED by this stub; Step 02_02_02+ is BARRED; Step 02_01_04 is
  BARRED; no baseline modeling. Step 02_01_03's existing materialization
  artifact + audit + 5-family permitted set declared by PR #257 +
  PR #259 + PR #262 remain BINDING and byte-unchanged; this stub does
  NOT reopen 02_01, Q5, Q6, Q6X, or the omit-closure adjudication.
phase: "02 — Feature Engineering"
pipeline_section: "02_02 — Symmetry & Difference Features"
manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 3"
dataset: "sc2egset"
question: >-
  Per Invariant I5 (focal/opponent symmetry) and the
  02_FEATURE_ENGINEERING_MANUAL.md §3 Bradley-Terry argument, how
  should the focal/opponent paired columns materialized in Step
  02_01_03 (5 history-enriched families x focal/opponent symmetric
  pair columns) be transformed into symmetric / difference
  representations that (a) eliminate slot-assignment bias per
  Invariant I5, (b) inherit Invariant I3 strict
  `history_time < target_time` cutoff enforced upstream, (c) produce
  model-input columns suitable for downstream Phase 03 splitting and
  Phase 04 modeling without starting Phase 03 now, (d) encode
  differences as `focal_value - opponent_value` (slot-orthogonal) and
  NOT `player_1_value - player_2_value` (slot-dependent), and (e)
  preserve row identity (`focal_match_id`, `focal_player_id`) and the
  `started_at` temporal anchor verbatim?
method: >-
  Step 02_02_01 itself does NOT execute any symmetry / difference
  transformation. This is a ROADMAP-only stub. The future 02_02_01
  scaffold + validator + adjudication + materialization PRs (analogous
  to the PR #239 / #241 / #242 / ... / #259 ladder for Step 02_01_03)
  will: (a) read the byte-unchanged 02_01_03 history-enriched
  pre_game Parquet and the 02_01_02 pre_game Parquet from the
  canonical paths declared under inputs.prior_artifacts; (b)
  enumerate candidate symmetric / difference feature families per
  manual §3 (focal/opponent numeric differences, absolute
  differences, symmetric pair features such as mean / sum / product /
  absolute-difference, matchup-history pair features); (c) bind a
  source-anchor / column-naming decision PR analogous to PR #234;
  (d) declare a scaffold + one validation module PR analogous to
  PR #241; (e) produce a future materialization PR analogous to
  PR #259 that emits ONE Parquet artifact + ONE CROSS-02-01 audit
  pair (paths declared under outputs); (f) emit NO Parquet, NO
  CROSS-02-01 audit, NO feature column, NO status YAML flip in this
  stub PR. The race-pair encoded interactions family is declared as
  a CANDIDATE only; the binding decision whether race-pair
  interactions belong in 02_02 or in 02_05 (Categorical Encoding &
  Interactions, manual §6) is taken in the future source-anchor
  adjudication PR analogous to PR #234, NOT in this stub.
stratification: >-
  Per family: dataset_tag = sc2egset; prediction_setting =
  history_enriched_pre_game (inherits from 02_01_03; 1v1 decisive
  subset N11 preserved; FIVE_FAMILY_CANONICAL_ORDER tuple N1
  preserved). Symmetry / difference operations are row-preserving
  transforms applied to the 02_01_03 Parquet column space; row
  identity (`focal_match_id`, `focal_player_id`) and the `started_at`
  temporal anchor are carried verbatim from the upstream artifact.
predecessors: "02_01_03"
notebook_path: >-
  (planned, NOT created in this PR) sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_planning.py
inputs:
  duckdb_tables: []
  schema_yamls: []
  prior_artifacts:
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.csv"
    - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.md"
  external_references:
    - "docs/PHASES.md Phase 02 row 2: 02_02 — Symmetry & Difference Features"
    - "docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md, Section 3 (Symmetry in Pairwise Prediction Demands Difference Features; Bradley-Terry argument; four representations: difference / ratio / canonical-ordering-with-concatenation / symmetric-kernels; difference features recommended as default)"
    - "reports/specs/02_02_feature_engineering_plan.md (CROSS-02-02-v1.0.1; §5.1 focal/opponent symmetry; §10 G-L-8 no row-order leakage from slot asymmetry; §6.2 history families)"
    - "reports/specs/02_03_temporal_feature_audit_protocol.md (downstream temporal-window / decay / cold-start audit spec; explicitly scoped OUT of this stub — referenced so this stub's halt-clauses do not silently encroach on 02_03)"
    - ".claude/scientific-invariants.md Invariant I3 (temporal cutoff history_time < target_time strict)"
    - ".claude/scientific-invariants.md Invariant I5 (focal/opponent symmetry; both players treated identically by the feature pipeline; model input structured as (focal_player_features, opponent_features, context_features))"
    - ".claude/scientific-invariants.md Invariants I6 / I7 / I9 / I10 (reproducibility / no magic numbers / research-pipeline discipline / relative-path provenance)"
    - ".claude/ml-protocol.md (three leakage failure modes: rolling aggregates including game T, head-to-head including game T, co-occurring matches)"
    - ".claude/rules/data-analysis-lineage.md (Non-batching rule for empirical work; sequence step 1 ROADMAP-only stub)"
    - "PR #243 Q5 cross-region adjudication (sensitivity-indicator co-registration arm)"
    - "PR #255 omit-closure (reconstructed_rating family + three reconstructed_rating_* columns excluded)"
    - "PR #257 materialization-scope amendment (5-family permitted set; reconstructed_rating excluded)"
    - "PR #259 five-family materialization (focal/opponent symmetric column pairs proven on disk)"
    - "PR #262 Step 02_01_03 formal closure (STEP_STATUS 02_01_03: complete; completed_at 2026-05-28)"
outputs:
  data_artifacts:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_features.parquet"
  report:
    - "(planned, NOT created in this PR) src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}"
reproducibility: >-
  Every column in the future symmetry/difference Parquet must trace
  to a focal/opponent paired column in 02_01_02 or 02_01_03 via a
  named transform (difference, absolute difference, symmetric mean /
  sum / product, matchup-pair operation). No transform may inject a
  new MMR scalar, a `reconstructed_rating_*` column, a target-match
  outcome, a future-match feature, a Phase-03 split-derived feature,
  or a tracker-derived target-match feature. The future audit MD must
  embed verbatim any count / distribution it reports with its
  derivation. Seed 42 convention. Relative-path provenance
  (Invariant I10).
scientific_invariants_applied:
  - number: "3"
    how_upheld: >-
      Strict `history_time < target_time` cutoff is enforced upstream
      in Step 02_01_03's materialization query; every symmetric /
      difference column in the future 02_02 Parquet is a row-preserving
      transform of the 02_01_03 columns and inherits the cutoff
      unchanged. No transform reads a record at `target_time` or
      later.
  - number: "5"
    how_upheld: >-
      All differences are computed as `focal_value - opponent_value`
      (slot-orthogonal). No `player_1_value - player_2_value`
      (slot-dependent) encoding is permitted. The focal/opponent pair
      structure is identical regardless of which player is focal,
      satisfying `P(A wins | A focal) = 1 - P(B wins | B focal)`.
  - number: "6"
    how_upheld: >-
      The future symmetry/difference materialization PR must embed
      verbatim the SQL or pandas/duckdb expression for each
      transform in the audit MD. No value may be paraphrased.
  - number: "7"
    how_upheld: >-
      Transform definitions are evidentiary, not boolean. Each
      candidate family carries a named formula and a derivation
      pointer to the upstream 02_01_03 column it operates on. No
      magic numbers.
  - number: "8"
    how_upheld: >-
      Cross-game comparability: 02_02 is a dataset-agnostic Pipeline
      Section per docs/PHASES.md. The SC2EGSet stub uses race-only
      terminology and does NOT use AoE2 `civilization` vocabulary;
      the AoE2 placeholder dataset is barred from this stub's scope.
  - number: "9"
    how_upheld: >-
      Step 02_02_01 conclusions derive only from its own future
      artifacts and from completed predecessor steps' artifacts
      (02_01_02 + 02_01_03 Parquet + audit pairs + 02_01_99
      omit-closure decision artifact), all lower-numbered and on
      disk.
  - number: "10"
    how_upheld: >-
      The future symmetry/difference artifacts use relative paths
      in all SHA pins; no absolute path written to any artifact.
      This ROADMAP stub itself uses only relative artifact paths.
gate:
  artifact_check: >-
    NOT APPLICABLE TO THIS ROADMAP-STUB PR. The artifact_check fires
    only after the future symmetry/difference materialization PR
    emits the Parquet + CROSS-02-01 audit pair. At that point the
    predicate is: (a) the planned Parquet exists at the declared path
    and is non-empty; (b) row count equals the measured row count of
    the 02_01_03 Parquet artifact (re-measured at materialization
    time; not hard-coded here); (c) row identity columns
    (`focal_match_id`, `focal_player_id`) and the `started_at`
    temporal anchor are byte-identical to the upstream 02_01_03
    Parquet on those columns; (d) the CROSS-02-01 audit JSON declares
    `verdict = PASS` with `features_audited` equal to exactly the
    symmetric / difference columns produced; (e) no
    `reconstructed_rating_*` column is present; (f) all difference
    columns are computed as `focal_value - opponent_value` per
    Invariant I5; (g) the 02_01_02 + 02_01_03 Parquet inputs and
    audit pairs are byte-unchanged versus the SHAs declared in the
    future audit's BINDING parent artifact list; (h) no AoE2
    `civilization` term appears in any 02_02 SC2EGSet artifact;
    (i) race-pair encoded interactions are either present in 02_02
    with explicit `02_02-vs-02_05` boundary disclosure, or deferred
    to 02_05; the binding decision is recorded in the source-anchor
    adjudication PR analogous to PR #234.
  continue_predicate: >-
    A future PR may begin the 02_02_01 scaffold + one validation
    module (analogous to PR #241 for 02_01_03) only after this
    ROADMAP stub merges. A future PR may begin source-anchor /
    column-naming adjudication for 02_02 (analogous to PR #234 for
    02_01_02 or PR #242 for 02_01_03) only after the scaffold PR
    merges with a passing one-validation-module result. A future PR
    may begin 02_02 feature materialization only after the
    adjudication PR(s) merge. Step 02_02_01 closure (STEP_STATUS row
    addition `02_02_01: complete`) and PIPELINE_SECTION_STATUS row
    `02_02: complete` happen only after the materialization +
    CROSS-02-01 audit PR merges and a U2.B-style formal closure PR
    (analogous to PR #237 / PR #262) merges. The `02_02`
    PIPELINE_SECTION_STATUS row first lands when the first 02_02
    step closes, mirroring PR #230 for 02_01 (verified precedent:
    section row at-step-closure, not at-step-open). No direct skip
    from this stub to feature materialization, CROSS-02-01 audit,
    status YAML flip, dataset research_log entry, or Phase 03.
  halt_predicate: >-
    Halt before generating any 02_02 artifact if any of the following
    hold:
      - the 02_01_02 Parquet
        (`02_01_02_pre_game_features.parquet`) SHA does not match
        the PR #236 merge-SHA pin recorded in the future audit's
        BINDING parent artifact list;
      - the 02_01_03 Parquet
        (`02_01_03_history_enriched_pre_game_features.parquet`) SHA
        does not match the PR #259 merge-SHA pin;
      - either 02_01_02 or 02_01_03 audit JSON / MD SHA does not
        match the PR #236 or PR #259 merge-SHA pin;
      - a future PR attempts to mutate any 02_01_02 or 02_01_03
        artifact bytes (Q1 / Q2(a) / Q2(b) / Q3 / Q5 / Q6 / Q6F /
        Q6G / Q6H re-adjudication ban; PR #243 / PR #255 / PR #257 /
        PR #259 / PR #262 closure preservation ban);
      - a future PR silently re-includes the `reconstructed_rating`
        family or any `reconstructed_rating_focal_pre` /
        `reconstructed_rating_opp_pre` / `reconstructed_rating_diff`
        column;
      - a future PR encodes `player_1_value - player_2_value`
        (slot-dependent) instead of `focal_value - opponent_value`
        (slot-orthogonal; Invariant I5 violation + G-L-8 + RISK-24);
      - a future PR ingests a target-match outcome, a future-match
        feature, a Phase-03 split-derived feature, or a
        tracker-derived target-match feature
        (Invariant I3 + G-L-3 + G-L-7 + Amendment 2 of PR #208);
      - a future PR introduces a new MMR scalar feature
        (PR #234 `is_mmr_missing` flag precedent stands);
      - a future PR introduces the AoE2 `civilization` term into
        any SC2EGSet artifact prose or column name (Invariant I8
        cross-game comparability violation; SC2EGSet uses `race`
        exclusively);
      - the future scaffold attempts to batch ROADMAP + notebook +
        artifact + next step in one execution
        (non-batching rule violation);
      - any feature artifact (.parquet, .csv, .md under
        reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/
        or reports/artifacts/02_02_01/) is produced by this
        ROADMAP-stub PR;
      - any CROSS-02-01 audit artifact
        (reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md})
        is produced by this PR;
      - STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, or
        PHASE_STATUS.yaml is edited in this PR;
      - dataset or root research_log.md is edited in this PR;
      - Step 02_01_02, Step 02_01_03, or Step 02_01_99 ROADMAP
        blocks are modified (the existing blocks remain
        byte-identical except for line shifts caused by the
        02_02_01 insertion);
      - the §02_01_03 materialization-scope-amendment block (above
        02_01_99 block) or the 02_01_99 amendment back-reference is
        edited;
      - the PIPELINE_SECTION_STATUS `02_02` row is added in this PR
        (deferred to the first 02_02 transition PR per PR #230
        precedent);
      - Phase 03 or Step 02_01_04 or Step 02_02_02+ is started;
      - any baseline modeling is started;
      - Q5 / Q6 / Q6F / Q6G / Q6H is reopened.
thesis_mapping:
  - "Chapter 4 — Data and Methodology > §4.5 Feature engineering plan (sc2egset symmetry & difference feature planning stub)"
research_log_entry: >-
  NOT REQUIRED FOR THIS ROADMAP-STUB PR per
  .claude/rules/data-analysis-lineage.md "Non-batching rule" sequence
  (step 1 — ROADMAP stub only — produces no research_log entry).
  Required on the future 02_02_01 materialization PR per the
  standard step-completion protocol; entry goes into
  src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md.
```

---

## Phase 03 — Splitting & Baselines (placeholder)

Pipeline Sections: see `docs/PHASES.md`.
Steps to be defined when Phase 02 gate is met.

---

## Phase 04 — Model Training (placeholder)

Pipeline Sections: see `docs/PHASES.md`.
Steps to be defined when Phase 03 gate is met.

---

## Phase 05 — Evaluation & Analysis (placeholder)

Pipeline Sections: see `docs/PHASES.md`.
Steps to be defined when Phase 04 gate is met.

---

## Phase 06 — Cross-Domain Transfer (placeholder)

Pipeline Sections: see `docs/PHASES.md`.
Steps to be defined when Phase 05 gate is met.

---

## Phase 07 — Thesis Writing Wrap-up (gate marker)

Per `docs/PHASES.md`, Phase 07 is a gate marker with no Pipeline Sections.
This dataset's Phase 07 gate is met when all thesis sections fed by this
dataset have reached FINAL status in `thesis/WRITING_STATUS.md`.

