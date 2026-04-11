---
task_id: "T01"
task_name: "Stage + commit 7 template files"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "docs/templates/phase_template.yaml"
  - "docs/templates/pipeline_section_template.yaml"
  - "docs/templates/dataset_roadmap_template.yaml"
  - "docs/templates/phase_status_template.yaml"
  - "docs/templates/pipeline_section_status_template.yaml"
  - "docs/templates/step_status_template.yaml"
  - "docs/templates/research_log_template.yaml"
read_scope: []
category: "C"
---

# Spec: Stage + commit 7 template files

## Objective

Stage and commit the 6 untracked template files plus the modified
research_log_template.yaml. These files already have correct content on disk —
this task verifies and commits them.

## Instructions

1. Verify each of the 7 files is non-empty and follows the `value:` + `required:`
   pattern consistent with `docs/templates/step_template.yaml`.
2. `git add` all 7 files.
3. The parent session will handle the commit.

## Verification

- All 7 files appear in `git diff --cached --name-only`
- Each file is >1KB
- `grep -c "required: true" docs/templates/phase_template.yaml` returns >0
