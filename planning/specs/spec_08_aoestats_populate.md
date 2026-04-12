---
task_id: "T08"
task_name: "Populate aoestats docs from artifacts"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02_aoestats"
file_scope:
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md"
read_scope:
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "docs/templates/dataset_reports_readme_template.yaml"
category: "A"
---

# Spec: Populate aoestats docs from artifacts

## Objective

Same as T06 (spec_06_sc2_populate.md) for the aoestats dataset.

## Instructions

Same pattern as spec_06. Target paths:
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
- raw/README.md: `src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md`
- reports/README.md: `src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md`

Use exact source title "aoestats.io weekly DB dumps" for source references.

## Verification

Same as spec_06 adapted to aoestats paths.

## Context

- Category A, Dataset: aoestats, Phase: 01, Step: 01_01_01
- T02 stripped all leaks; T05 regenerated artifacts; this task repopulates
