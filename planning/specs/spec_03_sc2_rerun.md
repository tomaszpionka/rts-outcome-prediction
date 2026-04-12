---
task_id: "T03"
task_name: "Rerun sc2egset notebook + write research log"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01_sc2"
file_scope:
  - "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb"
  - "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/"
read_scope:
  - ".claude/scientific-invariants.md"
  - "docs/templates/research_log_entry_template.yaml"
category: "A"
---

# Spec: Rerun sc2egset 01_01_01

## Objective

Rerun the sc2egset file inventory notebook into a clean context and write
a new research log entry strictly from artifacts.

## Instructions

1. Read the notebook at
   `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`.
2. Verify the notebook calls `inventory_directory()` and writes artifacts to:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
3. Run fresh-kernel execution:
   `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
4. Sync jupytext:
   `source .venv/bin/activate && poetry run jupytext --sync sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
5. Read the produced artifacts (JSON + MD).
6. Write a new research log entry using
   `docs/templates/research_log_entry_template.yaml`. Strict rules:
   - Set `step_scope: filesystem`
   - Report: directory tree, file counts per directory, extensions, sizes,
     filename-derived date ranges, gaps
   - Do NOT interpret directory names as data semantics
   - Do NOT use words like "daily," "weekly," "snapshot," "structurally
     sound," "replay," "tournament" (as semantic labels) unless they appear
     literally in artifact output as filenames/extensions
   - `matches/`, `_data/` etc. are directory names -- quote them as such
   - Per Invariant #9: conclusions derive from artifacts only
7. Verify `.ipynb` and `.py` pair are synced.

## Verification

- Artifacts exist and are current (timestamp matches notebook execution)
- Research log entry contains only file-level observations
- Research log entry includes `step_scope: filesystem`
- `grep -iE "snapshot|structurally sound|non.empty" research_log.md` in the
  01_01_01 entry returns zero matches
- `.ipynb` and `.py` pair synced

## Context

- Category A, Dataset: sc2egset, Phase: 01, Step: 01_01_01
- `inventory_directory()` is confirmed filesystem-only (glob + stat)
- The research log entry was deleted in T02; this task writes a fresh one
