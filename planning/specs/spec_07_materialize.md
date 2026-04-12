---
task_id: "T07"
task_name: "Update materialize_plan.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - ".claude/commands/materialize_plan.md"
read_scope: []
category: "C"
---

# Spec: Update materialize_plan.md

## Objective

Add pre-flight check requiring critique existence for Category A/F
before materialization proceeds.

## Instructions

1. In the `## Pre-flight` section, after the existing checks (branch,
   plan exists, Suggested Execution Graph present), add a new check:

   "4. Read the plan's frontmatter to extract `category` and
   `critique_required`. If `category` is A or F (or `critique_required`
   is true), verify `planning/current_plan.critique.md` exists and is
   non-empty. If missing, HALT with message: 'Category A/F requires
   adversarial critique before materialization. Dispatch
   reviewer-adversarial to produce
   `planning/current_plan.critique.md` first.'"

## Verification

- Pre-flight section includes critique existence check
- Check references correct file path (`planning/current_plan.critique.md`)
- Check halts with actionable message mentioning reviewer-adversarial
