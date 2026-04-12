# Planning Index

## Active plan
- [Current Plan](current_plan.md) — Rerun 01_01_01 File Inventory + Context Leak Cleanup

## Execution schedule
- [DAG](dags/DAG.yaml) — machine-readable execution graph
- [DAG format docs](dags/README.md)

## Task specs
- [Parallel execution guide](specs/README.md)

### J00_prep — Preparation (invariant, templates, cleanup)

#### TG00_methodology — Codify Invariant #9 + create templates
- [spec_00](specs/spec_00_invariant9.md) — Codify Invariant #9
- [spec_01](specs/spec_01_templates.md) — Create reports README template + update research log template

#### TG01_cleanup — Strip all context leaks (depends on TG00)
- [spec_02](specs/spec_02_strip_leaks.md) — Strip context leaks from all datasets

### J01_sc2 — sc2egset (depends on J00_prep)

#### TG01_sc2 — Rerun sc2 notebook + research log
- [spec_03](specs/spec_03_sc2_rerun.md) — Rerun notebook + write research log

#### TG02_sc2 — Populate sc2 docs from artifacts (depends on TG01_sc2)
- [spec_06](specs/spec_06_sc2_populate.md) — Populate ROADMAP + raw/README + reports/README

### J02_aoe2c — aoe2companion (depends on J00_prep)

#### TG01_aoe2c — Rerun aoe2companion notebook + research log
- [spec_04](specs/spec_04_aoe2c_rerun.md) — Rerun notebook + write research log

#### TG02_aoe2c — Populate aoe2companion docs (depends on TG01_aoe2c)
- [spec_07](specs/spec_07_aoe2c_populate.md) — Populate ROADMAP + raw/README + reports/README

### J03_aoestats — aoestats (depends on J00_prep)

#### TG01_aoestats — Rerun aoestats notebook + research log
- [spec_05](specs/spec_05_aoestats_rerun.md) — Rerun notebook + write research log

#### TG02_aoestats — Populate aoestats docs (depends on TG01_aoestats)
- [spec_08](specs/spec_08_aoestats_populate.md) — Populate ROADMAP + raw/README + reports/README

### J04_cross — CROSS log update (depends on J01, J02, J03)

#### TG01_cross — Update root CROSS log
- [spec_09](specs/spec_09_cross_log.md) — Update CROSS log summary

## Agent routing

| Role | Read | Skip |
|------|------|------|
| Executor (dispatched to spec_NN) | `specs/spec_NN.md` | `current_plan.md`, `DAG.yaml` |
| Reviewer (post-group gate) | `dags/DAG.yaml`, diff | `current_plan.md`, `specs/` |
| Reviewer-adversarial (final gate) | `current_plan.md`, `dags/DAG.yaml`, all specs | — |
| Parent orchestrator | `dags/DAG.yaml` | `specs/` (reads only to dispatch) |
