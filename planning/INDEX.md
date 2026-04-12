# Planning Index

## Active plan
- [Current Plan](current_plan.md) — the authoritative Spec for this PR

## Execution schedule
- [DAG](dags/DAG.yaml) — machine-readable execution graph
- [DAG format docs](dags/README.md)

## Task specs
- [Parallel execution guide](specs/README.md)

- [spec_01](specs/spec_01_plan_template.md) — rewrite plan_template.md (DAG-compatible)
- [spec_02](specs/spec_02_critique_template.md) — rewrite plan_critique_template.md (8 invariants, citations)
- [spec_03](specs/spec_03_output_contract.md) — rewrite planner_output_contract.md (agent-agnostic, plan-only)
- [spec_04](specs/spec_04_planning_readme.md) — add critique to lifecycle and purge
- [spec_05](specs/spec_05_planner_science.md) — add contract ref, critique-flagging
- [spec_06](specs/spec_06_planner.md) — add contract ref, critique-flagging
- [spec_07](specs/spec_07_materialize.md) — add critique pre-flight for A/F
- [spec_08](specs/spec_08_changelog.md) — CHANGELOG update

## Agent routing

| Role | Read | Skip |
|------|------|------|
| Executor (dispatched to spec_NN) | `specs/spec_NN.md` | `current_plan.md`, `DAG.yaml` |
| Reviewer (post-group gate) | `dags/DAG.yaml`, diff | `current_plan.md`, `specs/` |
| Adversarial reviewer (final gate) | `current_plan.md`, `dags/DAG.yaml` | `specs/` |
| Parent orchestrator | `dags/DAG.yaml` | `specs/` (reads only to dispatch) |
