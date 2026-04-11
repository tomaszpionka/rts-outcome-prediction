---
task_id: "T04"
task_name: "Populate PHASES.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - "docs/ml_experiment_phases/PHASES.md"
read_scope:
  - "docs/PHASES.md"
category: "C"
---

# Spec: Populate docs/ml_experiment_phases/PHASES.md

## Objective

Extract Phase-level content from `docs/PHASES.md` into a standalone reference
for Phase definitions, independent of Pipeline Section details.

## Instructions

1. Read `docs/PHASES.md` in full.
2. Write `docs/ml_experiment_phases/PHASES.md` with:
   - Header stating this file is derived from `docs/PHASES.md` (the canonical
     source). If this file disagrees with `docs/PHASES.md`, this file is wrong.
   - The 7-Phase summary table (number, name, source manual, one-line summary)
     — copied from `docs/PHASES.md` lines 33-41.
   - Phase scope rule (every Phase is dataset-scoped) — from lines 47-63.
   - Phase 07 gate marker semantics — from lines 211-238.
   - Maintenance rules (never invent/renumber Phases) — from lines 240-265.
3. Do NOT include Pipeline Section tables — those go in PIPELINE_SECTIONS.md.
4. Do NOT include the Pipeline Section derivation rule.

## Verification

- File is >50 lines and <150 lines
- Contains the 7-Phase table
- Does NOT contain Pipeline Section tables (no `01_01`, `02_01`, etc.)
- Header references `docs/PHASES.md` as upstream source
