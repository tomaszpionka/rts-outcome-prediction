---
task_id: "T09"
task_name: "Populate ROADMAP.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG04"
file_scope:
  - "docs/research/ROADMAP.md"
read_scope:
  - "docs/templates/dataset_roadmap_template.yaml"
category: "C"
---

# Spec: Populate docs/research/ROADMAP.md

## Objective

Create a reference document specifying the dataset ROADMAP structure. Not a
ROADMAP itself — this is the specification for how ROADMAPs are written.

## Instructions

1. Read `docs/templates/dataset_roadmap_template.yaml`.
2. Write `docs/research/ROADMAP.md` with:
   - Purpose: dataset-level execution plans for Phases 01-07.
   - Location convention: `src/rts_predict/<game>/reports/<dataset>/ROADMAP.md`.
   - Schema: pointer to `docs/templates/dataset_roadmap_template.yaml`.
   - Relationship to `docs/PHASES.md`: ROADMAPs implement Phases and Pipeline
     Sections defined there. ROADMAPs do not invent, rename, or omit them.
   - Step definitions: each Step in a ROADMAP follows
     `docs/templates/step_template.yaml`.
   - Required sections: header, usage, source data, Phase sections (01-07).
   - Phase 07 is a gate marker with no Pipeline Sections.
   - Role field: `TO BE DETERMINED` until Phase 01 Decision Gate (01_06)
     evidence supports role assignment (for games with multiple datasets).

## Verification

- References `docs/templates/dataset_roadmap_template.yaml` as schema
- References `docs/templates/step_template.yaml` for Step definitions
- Describes the ROADMAP → PHASES.md relationship
- Mentions the TO BE DETERMINED role convention
