# SC2EGSet Dataset Roadmap

**Game:** SC2
**Dataset:** sc2egset
**Canonical phase list:** `docs/PHASES.md`
**Methodology manuals:** `docs/INDEX.md`
**Step definition schema:** `docs/templates/step_template.yaml`

---

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

**SC2EGSet v2.1.0** — StarCraft II Esport Replay and Game-state Dataset.
~22,000 competitive 1v1 replays from 70+ tournaments covering 2016–2024.

Citation: Białecki, A. et al. (2023). *SC2EGSet: StarCraft II Esport Replay
and Game-state Dataset.* Scientific Data 10(1), 600.
https://doi.org/10.1038/s41597-023-02510-7 — version 2.1.0 from Zenodo:
https://zenodo.org/records/17829625

**Game loop timing:** The SC2 engine runs at 16 game loops per game-second
(Normal speed). All competitive play uses Faster speed (1.4× multiplier),
giving **22.4 game loops = 1 real-time second**. Use `game_loops / 22.4 / 60`
for real-time minutes. The older formula `game_loops / 16.0 / 60` produces
game-minutes (internal engine time) — both are valid but must be clearly
labelled. All artifacts in this ROADMAP use real-time minutes unless
explicitly noted.

---

## Phase 01 — Data Exploration (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `01_01` — Data Acquisition & Source Inventory
- `01_02` — Exploratory Data Analysis (Tukey-style)
- `01_03` — Systematic Data Profiling
- `01_04` — Data Cleaning
- `01_05` — Temporal & Panel EDA
- `01_06` — Decision Gates

Steps will be defined in a planning session before Phase 01 work begins.
The library modules that support Phase 01 (ingestion, exploration, audit)
will require rework; Step definitions must not presuppose specific function
signatures or exploration approaches.

---

## Phase 02 — Feature Engineering (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `02_01` — Pre-Game vs In-Game Boundary
- `02_02` — Symmetry & Difference Features
- `02_03` — Temporal Features, Windows, Decay, Cold Starts
- `02_04` — Feature Quality Assessment
- `02_05` — Categorical Encoding & Interactions
- `02_06` — Feature Selection
- `02_07` — Rating Systems & Domain Features
- `02_08` — Feature Documentation & Catalog

Steps to be defined when Phase 01 gate is met.

---

## Phase 03 — Splitting & Baselines (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `03_01` — Temporal Splitting Strategies
- `03_02` — Purge & Embargo
- `03_03` — Grouped Splits for Panel Data
- `03_04` — Nested Cross-Validation
- `03_05` — Split Validation
- `03_06` — Baseline Definitions
- `03_07` — Elo & Domain-Specific Baselines
- `03_08` — Shared Evaluation Protocol
- `03_09` — Statistical-Comparison Protocol

Steps to be defined when Phase 02 gate is met.

---

## Phase 04 — Model Training (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `04_01` — Training Pipelines (sklearn Pipeline + ColumnTransformer)
- `04_02` — GNN Training
- `04_03` — Loss Functions
- `04_04` — Early Stopping
- `04_05` — Learning Rate Scheduling
- `04_06` — Hyperparameter Tuning
- `04_07` — Nested Temporal Cross-Validation
- `04_08` — Reproducibility

Steps to be defined when Phase 03 gate is met.

---

## Phase 05 — Evaluation & Analysis (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `05_01` — Evaluation Metrics (threshold, probabilistic, ROC/PR, calibration, sharpness)
- `05_02` — Statistical Comparison of Classifiers
- `05_03` — Error Analysis
- `05_04` — Ablation Studies & Sensitivity Analysis

Steps to be defined when Phase 04 gate is met.

---

## Phase 06 — Cross-Domain Transfer (placeholder)

Pipeline Sections per `docs/PHASES.md`:

- `06_01` — Transfer Learning Taxonomy
- `06_02` — Ben-David's Bound & Transfer Feasibility
- `06_03` — Distribution Shift Between Domains
- `06_04` — Shared Feature Space Construction
- `06_05` — Negative Transfer
- `06_06` — Three-Tier Experimental Design
- `06_07` — Transfer Evaluation & Reporting
- `06_08` — Honest Claims With Two Domains
- `06_09` — Component Transferability Analysis

Steps to be defined when Phase 05 gate is met.

---

## Phase 07 — Thesis Writing Wrap-up (gate marker)

Per `docs/PHASES.md`, Phase 07 is a gate marker with no Pipeline Sections.
This dataset's Phase 07 gate is met when all thesis sections fed by this
dataset have reached FINAL status in `thesis/WRITING_STATUS.md`.
