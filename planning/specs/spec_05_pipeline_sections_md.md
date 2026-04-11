---
task_id: "T05"
task_name: "Populate PIPELINE_SECTIONS.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - "docs/ml_experiment_phases/PIPELINE_SECTIONS.md"
read_scope:
  - "docs/PHASES.md"
category: "C"
---

# Spec: Populate docs/ml_experiment_phases/PIPELINE_SECTIONS.md

## Objective

Extract Pipeline Section content from `docs/PHASES.md` into a standalone
reference for Pipeline Section enumeration per Phase.

## Instructions

1. Read `docs/PHASES.md` in full.
2. Write `docs/ml_experiment_phases/PIPELINE_SECTIONS.md` with:
   - Header stating this file is derived from `docs/PHASES.md`.
   - The Pipeline Section derivation rule — from lines 66-88.
   - Per-Phase Pipeline Section tables for Phases 01-06 — from lines 91-208.
     Include the exclusion lists under each Phase.
   - Note that Phase 07 has no Pipeline Sections.
3. Do NOT include the 7-Phase summary table — that's in PHASES.md.
4. Do NOT include Phase scope rules or maintenance rules.

## Verification

- File contains all 6 per-Phase Pipeline Section tables
- Contains the derivation rule ("mirror the top-level sections")
- Contains all exclusion lists ("Excluded as meta: ...")
- Does NOT contain the 7-Phase summary table
- Header references `docs/PHASES.md` as upstream source
