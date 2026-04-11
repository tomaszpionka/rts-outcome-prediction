---
task_id: "T02"
task_name: "Stage + commit 9 status files"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "src/rts_predict/sc2/reports/sc2egset/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoe2companion/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoestats/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/sc2/reports/sc2egset/STEP_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoe2companion/STEP_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoestats/STEP_STATUS.yaml"
  - "src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml"
  - "src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml"
read_scope: []
category: "C"
---

# Spec: Stage + commit 9 status files

## Objective

Stage the 3 untracked PIPELINE_SECTION_STATUS.yaml and 6 modified
STEP_STATUS.yaml / PHASE_STATUS.yaml files. Verify derivation chain consistency.

## Instructions

1. Verify each STEP_STATUS.yaml has `game:` and `pipeline_section:` fields, and
   derivation comments reference the three-tier chain.
2. Verify each PIPELINE_SECTION_STATUS.yaml has `phase:` fields per entry and
   derivation chain comments.
3. Verify each PHASE_STATUS.yaml has derivation chain comments.
4. `git add` all 9 files.
5. The parent session will handle the commit.

## Verification

- `grep "pipeline_section" src/rts_predict/*/reports/*/STEP_STATUS.yaml` returns 3 matches
- `grep "PIPELINE_SECTION_STATUS.yaml is derived" src/rts_predict/*/reports/*/STEP_STATUS.yaml` returns 3 matches
- `grep "phase:" src/rts_predict/*/reports/*/PIPELINE_SECTION_STATUS.yaml` returns 18 matches (6 per file × 3 files)
- All 9 files appear in `git diff --cached --name-only`
