---
task_id: "T04"
task_name: "Update planning/README.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - "planning/README.md"
read_scope: []
category: "C"
---

# Spec: Update planning/README.md

## Objective

Add critique to the planning lifecycle and purge protocol.

## Instructions

1. Add `current_plan.critique.md` to the contents table as an ephemeral
   sibling to `current_plan.md`. Note: produced by reviewer-adversarial
   for Category A/B/D/F, not by the planner.
2. Add to the purge protocol: delete `current_plan.critique.md` after
   merge, alongside specs and DAG.
3. Add to the lifecycle description: after the plan is written and before
   materialization, reviewer-adversarial produces the critique for A/F.

## Verification

- `current_plan.critique.md` listed in contents table
- `current_plan.critique.md` listed in purge protocol
- Lifecycle mentions adversarial critique step
