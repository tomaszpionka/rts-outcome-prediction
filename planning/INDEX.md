# Planning Index

## Active plan
- [Current Plan](current_plan.md) — the authoritative Spec for this PR

## Execution schedule
- [DAG](dags/DAG.yaml) — machine-readable execution graph
- [DAG format docs](dags/README.md)

## Task specs
- [Parallel execution guide](specs/README.md)

- [spec_01](specs/spec_01_templates.md) — stage + commit 7 template files
- [spec_02](specs/spec_02_status_files.md) — stage + commit 9 status files
- [spec_03](specs/spec_03_roadmap_retractions.md) — stage AoE2 ROADMAP retractions + research log
- [spec_04](specs/spec_04_phases_md.md) — populate docs/ml_experiment_phases/PHASES.md
- [spec_05](specs/spec_05_pipeline_sections_md.md) — populate PIPELINE_SECTIONS.md
- [spec_06](specs/spec_06_steps_md.md) — populate STEPS.md
- [spec_07](specs/spec_07_research_log_md.md) — populate docs/research/RESEARCH_LOG.md
- [spec_08](specs/spec_08_research_log_entry_md.md) — populate RESEARCH_LOG_ENTRY.md
- [spec_09](specs/spec_09_research_roadmap_md.md) — populate docs/research/ROADMAP.md
- [spec_10](specs/spec_10_cleanup.md) — workflow files, delete relic, CHANGELOG

## Agent routing

| Role | Read | Skip |
|------|------|------|
| Executor (dispatched to spec_NN) | `specs/spec_NN.md` | `current_plan.md`, `DAG.yaml` |
| Reviewer (post-group gate) | `dags/DAG.yaml`, diff | `current_plan.md`, `specs/` |
| Adversarial reviewer (final gate) | `current_plan.md`, `dags/DAG.yaml` | `specs/` |
| Parent orchestrator | `dags/DAG.yaml` | `specs/` (reads only to dispatch) |
