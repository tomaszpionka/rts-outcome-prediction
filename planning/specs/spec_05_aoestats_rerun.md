---
task_id: "T05"
task_name: "Rerun aoestats notebook + write research log"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01_aoestats"
file_scope:
  - "sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb"
  - "sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/"
read_scope:
  - ".claude/scientific-invariants.md"
  - "docs/templates/research_log_entry_template.yaml"
category: "A"
---

# Spec: Rerun aoestats 01_01_01

## Objective

Same as T03 (spec_03_sc2_rerun.md) for the aoestats dataset.

## Instructions

Same pattern as spec_03. Target paths:
- Notebook: `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- Artifacts: `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/`
- Research log: `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`

Same strict scoping rules, `step_scope: filesystem`, and Invariant #9 constraint.

## Verification

Same as spec_03 adapted to aoestats paths.

## Context

- Category A, Dataset: aoestats, Phase: 01, Step: 01_01_01
- `inventory_directory()` is confirmed filesystem-only (glob + stat)
- The research log entry was deleted in T02; this task writes a fresh one
