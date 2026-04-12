---
task_id: "T06"
task_name: "Populate sc2egset docs from artifacts"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02_sc2"
file_scope:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/raw/README.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md"
read_scope:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "docs/templates/dataset_reports_readme_template.yaml"
category: "A"
---

# Spec: Populate sc2egset docs from artifacts

## Objective

Repopulate the sc2egset ROADMAP source data section, raw/README.md, and
reports/README.md strictly from fresh 01_01_01 artifacts.

## Instructions

1. Read the fresh artifacts (JSON + MD) from T03.
2. Update ROADMAP source data section: repopulate file counts, sizes,
   directory structure from artifacts. Use filesystem-level language only.
   No "replay," "tournament" as semantic labels -- use directory names
   and file extensions. Use the exact dataset title "SC2EGSet: StarCraft II
   Esport Replay and Game-state Dataset" for source references.
3. Update raw/README.md: repopulate `subdirectory_layout` entries,
   `total_files`, `total_size_mb`, `description`, and `contents:` fields
   from artifacts. Populate `temporal_grain` from artifact `date_analysis`
   (filename-derived cadence is filesystem-level). Use pattern-based
   descriptions for `contents:` fields (e.g., "`.SC2Replay.json` files").
4. Update reports/README.md: populate Section C (file inventory) from
   artifacts. Must conform to
   `docs/templates/dataset_reports_readme_template.yaml`.
5. Per Invariant #9: every stated fact must trace to the 01_01_01 artifact.

## Verification

- No interpretive labels in any of the 3 files
- reports/README.md conforms to template
- All numbers match 01_01_01 artifact values
- `temporal_grain` is populated from artifact date_analysis

## Context

- Category A, Dataset: sc2egset, Phase: 01, Step: 01_01_01
- T02 stripped all leaks; T03 regenerated artifacts; this task repopulates
- Invariant #9 governs what can be stated
