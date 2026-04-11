---
task_id: "T10"
task_name: "Stage workflow files, delete relic, update CHANGELOG"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG05"
file_scope:
  - "CLAUDE.md"
  - "CHANGELOG.md"
  - "planning/README.md"
  - "planning/INDEX.md"
  - "planning/dags/DAG.yaml"
  - ".claude/agents/executor.md"
read_scope: []
category: "C"
---

# Spec: Stage workflow files, delete relic, update CHANGELOG

## Objective

Stage all remaining modified files, delete the root `_current_plan.md` relic,
and finalize CHANGELOG.md.

## Instructions

1. Delete `_current_plan.md` from repo root (untracked relic from planning/ migration).
2. Update `CHANGELOG.md` under `[Unreleased]` with the full set of changes for
   this branch. Include:
   - Added: 7 templates, 3 PIPELINE_SECTION_STATUS files, 3 docs/ml_experiment_phases/ files, 3 docs/research/ files
   - Changed: 6 status files (STEP/PHASE), 3 AoE2 ROADMAPs, CLAUDE.md, planning/README.md, executor.md
3. `git add` the following already-modified files:
   - `CLAUDE.md`
   - `planning/README.md`
   - `planning/INDEX.md`
   - `planning/dags/DAG.yaml`
   - `.claude/agents/executor.md`
   - `CHANGELOG.md`
4. The parent session will handle the commit.

## Verification

- `_current_plan.md` does not exist at repo root
- `CHANGELOG.md` [Unreleased] section has Added and Changed entries
- All 6 files appear in `git diff --cached --name-only`
