---
task_id: "T06"
task_name: "Populate STEPS.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - "docs/ml_experiment_phases/STEPS.md"
read_scope:
  - "docs/TAXONOMY.md"
  - "docs/templates/step_template.yaml"
category: "C"
---

# Spec: Populate docs/ml_experiment_phases/STEPS.md

## Objective

Create a Step-level reference document: the contract that defines what a Step IS
and what it must produce. Not an enumeration — Steps are dataset-scoped in
ROADMAPs.

## Instructions

1. Read `docs/TAXONOMY.md` (Step definition, lines 82-110) and
   `docs/templates/step_template.yaml`.
2. Write `docs/ml_experiment_phases/STEPS.md` with:
   - Header referencing `docs/TAXONOMY.md` as the terminology source and
     `docs/templates/step_template.yaml` as the schema source.
   - Step numbering convention (NN_NN_NN = Phase_Section_Step).
   - Step contract: one notebook, one+ artifacts, one research log entry.
   - Step schema: pointer to `docs/templates/step_template.yaml` with a
     summary of required fields.
   - Directory layout: sandbox notebooks + report artifacts mirroring rule,
     extracted from `docs/TAXONOMY.md` lines 112-162.
   - Ownership: Steps live in dataset ROADMAPs at
     `src/rts_predict/<game>/reports/<dataset>/ROADMAP.md`.
3. Do NOT enumerate actual Steps (those are dataset-specific).

## Verification

- File is >40 lines and <120 lines
- Contains the NN_NN_NN numbering convention
- Contains the Step contract (notebook + artifacts + research log entry)
- References both `docs/TAXONOMY.md` and `docs/templates/step_template.yaml`
- Does NOT list specific Step numbers (e.g., 01_01_01)
