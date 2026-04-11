# Pipeline Sections Reference

Derived from [`docs/PHASES.md`](../PHASES.md), which is the canonical source
of truth for the Phase list and Pipeline Section enumeration. If this file
ever contradicts `docs/PHASES.md`, `docs/PHASES.md` takes precedence.

---

## Pipeline Section Derivation Rule

Pipeline Sections within a Phase mirror the top-level sections (`##` in
the manual's markdown) of that Phase's source manual, **excluding** sections
that are methodologically informative but are not themselves work activities:

- **Framing/introductory sections** that set up the manual's argument but
  describe no concrete activity.
- **Warning/pitfall lists** (e.g., "Seven Pitfalls", "Eight Mistakes",
  "Twelve Common Training Mistakes"). These are reference material to
  consult while executing other Pipeline Sections, not Pipeline Sections
  themselves.
- **Conclusions and references.**

Decision gates (e.g., Manual 01 §6 "Decision Gates") **are** Pipeline
Sections — they are exit-criterion methodology that must be actively
executed, not passive reference.

The rule is mechanical: open the manual's table of contents, strike
through the categories above, and the remainder is the Pipeline Section
list in the manual's own order.

---

## Phase 01 — Data Exploration

Source: `01_DATA_EXPLORATION_MANUAL.md`.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `01_01` | Data Acquisition & Source Inventory | §1 |
| `01_02` | Exploratory Data Analysis (Tukey-style) | §2 |
| `01_03` | Systematic Data Profiling | §3 |
| `01_04` | Data Cleaning | §4 |
| `01_05` | Temporal & Panel EDA | §5 |
| `01_06` | Decision Gates | §6 |

Excluded as meta: §7 "Seven Pitfalls", §8 "Conclusion".

---

## Phase 02 — Feature Engineering

Source: `02_FEATURE_ENGINEERING_MANUAL.md`.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `02_01` | Pre-Game vs In-Game Boundary | §2 |
| `02_02` | Symmetry & Difference Features | §3 |
| `02_03` | Temporal Features, Windows, Decay, Cold Starts | §4 |
| `02_04` | Feature Quality Assessment | §5 |
| `02_05` | Categorical Encoding & Interactions | §6 |
| `02_06` | Feature Selection | §7 |
| `02_07` | Rating Systems & Domain Features | §9 |
| `02_08` | Feature Documentation & Catalog | §10 |

Excluded as meta: §1 (pipeline overview — framing), §8 "Eight Mistakes",
conclusion.

---

## Phase 03 — Splitting & Baselines

Source: `03_SPLITTING_AND_BASELINES_MANUAL.md`.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `03_01` | Temporal Splitting Strategies | §2 |
| `03_02` | Purge & Embargo | §3 |
| `03_03` | Grouped Splits for Panel Data | §4 |
| `03_04` | Nested Cross-Validation | §5 |
| `03_05` | Split Validation | §6 |
| `03_06` | Baseline Definitions | §7 |
| `03_07` | Elo & Domain-Specific Baselines | §8 |
| `03_08` | Shared Evaluation Protocol | §9 |
| `03_09` | Statistical-Comparison Protocol | §10 |

Excluded as meta: §1 "Why Random Splits Produce Optimistic Results"
(framing), §11 "Bet on Sparsity Principle" (framing), §12 "Common
Baseline Mistakes", conclusion.

---

## Phase 04 — Model Training

Source: `04_MODEL_TRAINING_MANUAL.md`.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `04_01` | Training Pipelines (sklearn Pipeline + ColumnTransformer) | §1 |
| `04_02` | GNN Training | §2 |
| `04_03` | Loss Functions | §3 |
| `04_04` | Early Stopping | §4 |
| `04_05` | Learning Rate Scheduling | §5 |
| `04_06` | Hyperparameter Tuning | §6 |
| `04_07` | Nested Temporal Cross-Validation | §7 |
| `04_08` | Reproducibility | §8 |

Excluded as meta: §9 "Twelve Common Training Mistakes", conclusion.

---

## Phase 05 — Evaluation & Analysis

Source: `05_EVALUATION_AND_ANALYSIS_MANUAL.md`.

This manual is organised into four Parts (I–IV), each containing
multiple §subsections. For Pipeline Section derivation, the top-level
organising unit is the **Part** — Pipeline Sections map to Parts, not
to sub-§sections, to keep Phase 05 at a consistent granularity with
the other Phases.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `05_01` | Evaluation Metrics (threshold, probabilistic, ROC/PR, calibration, sharpness) | Part I |
| `05_02` | Statistical Comparison of Classifiers | Part II |
| `05_03` | Error Analysis | Part III |
| `05_04` | Ablation Studies & Sensitivity Analysis | Part IV |

Excluded as meta: the closing "Recommended Metric and Analysis Tiers"
section and conclusion.

---

## Phase 06 — Cross-Domain Transfer

Source: `06_CROSS_DOMAIN_TRANSFER_MANUAL.md`.

| Pipeline Section | Name | Manual Part |
|---|---|---|
| `06_01` | Transfer Learning Taxonomy | §1 |
| `06_02` | Ben-David's Bound & Transfer Feasibility | §2 |
| `06_03` | Distribution Shift Between Domains | §3 |
| `06_04` | Shared Feature Space Construction | §4 |
| `06_05` | Negative Transfer | §5 |
| `06_06` | Three-Tier Experimental Design | §6 |
| `06_07` | Transfer Evaluation & Reporting | §7 |
| `06_08` | Honest Claims With Two Domains | §8 |
| `06_09` | Component Transferability Analysis | §9 |

Excluded as meta: conclusion.

---

## Phase 07 — Thesis Writing Wrap-up

Phase 07 has no Pipeline Sections. It is a gate marker, not a set of
work activities — a dataset either has passed its Phase 07 gate or has
not; there is nothing to decompose into Pipeline Sections.

See `docs/PHASES.md` §"Phase 07 — Thesis Writing Wrap-up" for full
semantics.
