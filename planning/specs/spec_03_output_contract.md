---
task_id: "T03"
task_name: "Rewrite planner_output_contract.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02"
file_scope:
  - "docs/templates/planner_output_contract.md"
read_scope:
  - "docs/templates/plan_template.md"
  - "docs/templates/plan_critique_template.md"
  - "docs/TAXONOMY.md"
category: "C"
---

# Spec: Rewrite planner_output_contract.md

## Objective

Replace the entire file with an agent-agnostic contract that produces
plans only (no self-critique) and uses correct terminology.

## Instructions

1. Read `docs/templates/plan_template.md` (rewritten by T01) for the
   plan schema.
2. Read `docs/templates/plan_critique_template.md` (rewritten by T02)
   for the critique schema.
3. Read `docs/TAXONOMY.md` for forbidden/required terms.
4. Replace the entire file. Key changes:

   a. Agent-agnostic: "You are a planner agent" (not "planner-science").
   b. Required output: ONE file (`planning/current_plan.md`) — not two.
      The critique is NOT the planner's responsibility.
   c. After producing the plan, the planner must instruct the parent
      session: "For Category A/F, adversarial critique is required
      before materialization. Dispatch reviewer-adversarial to produce
      `planning/current_plan.critique.md`."
   d. Forbidden terms from TAXONOMY.md: Stage, Experiment (formal),
      Milestone, Workstream, Track, Initiative, Epic, Component (work
      unit), Section (unqualified). "Task" is NOT forbidden.
   e. Remove "section 4.1" reference.
   f. Replace `scope` system with `category` A-F.
   g. Conditional requirements by category:

      | Category | Plan sections | Critique? |
      |----------|--------------|-----------|
      | A | all | yes — reviewer-adversarial, all sections |
      | B | Scope, Execution Steps, File Manifest, DAG, Out of scope | yes — invariants + weaknesses |
      | C | Scope, Execution Steps, File Manifest, DAG | no |
      | D | Scope, Execution Steps, File Manifest, DAG, Out of scope | yes if file_scope touches `src/rts_predict/<game>/` |
      | E | Scope, Execution Steps, File Manifest, DAG | no |
      | F | all | yes — reviewer-adversarial, all sections |

   h. Document per-task Execution Steps structure (matching plan template).
   i. Self-check: category A-F, DAG uses correct schema, every task has
      spec_file/file_scope/parallel_safe/depends_on, every TNN maps to
      a task in the graph, File Manifest complete, no forbidden terms,
      invariants_touched populated.

## Verification

- Contract does NOT forbid the word "task"
- Contract does NOT cite "section 4.1"
- Contract addresses both planner agents
- Contract uses Category A-F
- Contract says planner produces plan ONLY (not critique)
- Contract tells planner to flag critique need for A/F
