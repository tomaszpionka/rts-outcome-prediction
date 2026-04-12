---
task_id: "T05"
task_name: "Update planner-science.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG03"
file_scope:
  - ".claude/agents/planner-science.md"
read_scope: []
category: "C"
---

# Spec: Update planner-science.md

## Objective

Add output contract reference and critique-flagging instruction. Do NOT
instruct the planner to produce the critique itself.

## Instructions

1. Add to constraints section: "Plan output must conform to
   `docs/templates/planner_output_contract.md`. Read it before producing
   output."
2. Add: "For Category A/F, after producing the plan, instruct the parent
   session that adversarial critique is required before materialization.
   Do NOT produce the critique yourself — reviewer-adversarial handles it."

## Verification

- Agent references output contract in constraints
- Agent does NOT claim to produce critique
- Agent flags critique need for A/F
