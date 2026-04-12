# Planning Index

## Active plan
- [Current Plan](current_plan.md) — Phase 01 Step 01_01_02 Schema Discovery

## Execution schedule
- [DAG](dags/DAG.yaml) — machine-readable execution graph
- [DAG format docs](dags/README.md)

## Task specs
- [Parallel execution guide](specs/README.md)

### J01 — Schema discovery (all datasets)

#### TG01 — Utility code
- [spec_01](specs/spec_01_parquet_utils.md) — Create parquet_utils + tests

#### TG02 — Notebooks + artifacts + docs (depends on TG01)
- [spec_02](specs/spec_02_schema_discovery.md) — Schema discovery — all 3 datasets (parameterized)

## Agent routing

| Role | Read | Skip |
|------|------|------|
| Executor (dispatched to spec_NN) | `specs/spec_NN.md` | `current_plan.md`, `DAG.yaml` |
| Reviewer-adversarial (final gate) | `current_plan.md`, `dags/DAG.yaml`, all specs | — |
| Parent orchestrator | `dags/DAG.yaml` | `specs/` (reads only to dispatch) |
