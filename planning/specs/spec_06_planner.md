---
task_id: "T06"
task_name: "Update planner.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - ".claude/agents/planner.md"
read_scope: []
category: "C"
---

# Spec: Update planner.md

## Objective

Same contract reference addition as T05, adapted for the infrastructure
planner (Category B/C/D/E).

## Instructions

1. Add to constraints section: "Plan output must conform to
   `docs/templates/planner_output_contract.md`. Read it before producing
   output."
2. Add: "For Category B/D where critique is applicable, instruct the
   parent session that adversarial review is available. Do NOT produce
   the critique yourself."

## Verification

- Agent references output contract in constraints
- Agent does NOT claim to produce critique
