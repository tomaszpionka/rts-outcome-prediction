---
task_id: "T08"
task_name: "Update CHANGELOG"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG04"
file_scope:
  - "CHANGELOG.md"
read_scope: []
category: "C"
---

# Spec: Update CHANGELOG

## Objective

Add entries for all template rewrites, agent updates, and materialization
update under `[Unreleased]`.

## Instructions

1. Under `[Unreleased]`, add Changed entries:
   - Rewrite `plan_template.md` — DAG-compatible, per-task structure,
     Category A-F
   - Rewrite `plan_critique_template.md` — all 8 invariants, citations,
     temporal discipline, produced by reviewer-adversarial
   - Rewrite `planner_output_contract.md` — agent-agnostic, plan-only
     output, Category A-F
   - Update `planning/README.md` — critique in lifecycle and purge
   - Update `planner-science.md` and `planner.md` — output contract
     reference, critique-flagging
   - Update `materialize_plan.md` — critique pre-flight for A/F

## Verification

- CHANGELOG has entries under `[Unreleased]`
- All 8 modified files mentioned
