---
task_id: "T01"
task_name: "Rewrite plan_template.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "docs/templates/plan_template.md"
read_scope:
  - "docs/templates/dag_template.yaml"
  - "planning/current_plan.md"
category: "C"
---

# Spec: Rewrite plan_template.md

## Objective

Replace the entire file with a DAG-compatible template derived from the
working plan at `planning/current_plan.md`, not the ChatGPT draft.

## Instructions

1. Read `docs/templates/dag_template.yaml` for the real DAG schema.
2. Read `planning/current_plan.md` for real-world precedent.
3. Replace the entire file with the new template structure:

   Frontmatter fields:
   - `category` (A-F), `branch`, `date`, `planner_model`, `dataset`,
     `phase`, `pipeline_section`, `invariants_touched`,
     `source_artifacts` (required A/F, optional B/D, omit C/E),
     `critique_required` (true A/F, optional B/D, false C/E),
     `research_log_ref` (optional, A/F only)

   Sections (with conditional markers per category):
   - `## Scope` (required all)
   - `## Problem Statement` (required all)
   - `## Assumptions & unknowns` (required A/F, optional B/D, omit C/E)
   - `## Literature context` (required A/F, omit B-E)
   - `## Execution Steps` (required all — per-task structure, see below)
   - `## File Manifest` (required all)
   - `## Gate Condition` (required A, recommended all)
   - `## Out of scope` (required A/F, recommended all)
   - `## Open questions` (required A/F, optional all)
   - `## Suggested Execution Graph` (required all — YAML per dag_template.yaml)

4. Document the per-task structure for `## Execution Steps`:
   ```
   ### TNN — <task name>
   **Objective:** <1-3 sentences>
   **Instructions:** <numbered steps>
   **Verification:** <commands, conditions>
   **File scope:** <files this task writes>
   **Read scope:** <files this task reads>
   ```
   Add a note: "File scope and Read scope map to spec YAML frontmatter
   (`file_scope`, `read_scope`), not to markdown sections."

5. Replace `## Proposed DAG` with `## Suggested Execution Graph` using
   `jobs > task_groups > tasks` hierarchy. Every task must include
   `spec_file`, `file_scope`, `parallel_safe`, `depends_on`.

## Verification

- Template contains `## Suggested Execution Graph` (not `## Proposed DAG`)
- YAML uses `jobs > task_groups > tasks` hierarchy
- Template contains `## Execution Steps` and `## File Manifest`
- Template uses `category:` A-F (not `scope:`)
- Frontmatter includes `planner_model` and `source_artifacts`
- Per-task structure documented with mapping note
