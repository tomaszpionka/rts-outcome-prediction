---
task_id: "T07"
task_name: "Populate aoe2companion docs from artifacts"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02_aoe2c"
file_scope:
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md"
read_scope:
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "docs/templates/dataset_reports_readme_template.yaml"
category: "A"
---

# Spec: Populate aoe2companion docs from artifacts

## Objective

Same as T06 (spec_06_sc2_populate.md) for the aoe2companion dataset.

## Instructions

Same pattern as spec_06. Target paths:
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
- raw/README.md: `src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md`
- reports/README.md: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md`

Use exact source title "aoe2companion CDN dump" for source references.

## Verification

Same as spec_06 adapted to aoe2companion paths.

## Context

- Category A, Dataset: aoe2companion, Phase: 01, Step: 01_01_01
- T02 stripped all leaks; T04 regenerated artifacts; this task repopulates
