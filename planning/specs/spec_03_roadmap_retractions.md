---
task_id: "T03"
task_name: "Stage + commit AoE2 ROADMAP retractions + research log"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG02"
file_scope:
  - "src/rts_predict/aoe2/reports/ROADMAP.md"
  - "src/rts_predict/aoe2/reports/aoestats/ROADMAP.md"
  - "src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md"
  - "reports/research_log.md"
read_scope: []
category: "C"
---

# Spec: Stage + commit AoE2 ROADMAP retractions + research log

## Objective

Stage the already-edited AoE2 ROADMAP files and research log retraction entry.
Edits were made earlier in this session — verify correctness and stage.

## Instructions

1. Verify `src/rts_predict/aoe2/reports/ROADMAP.md` contains "provisional" in
   the Dataset Strategy heading and no committed PRIMARY/SUPPLEMENTARY roles.
2. Verify both dataset ROADMAPs contain "TO BE DETERMINED" role text.
3. Verify neither dataset ROADMAP contains "does not run Phase 06".
4. Verify `reports/research_log.md` has a "### Retraction" section in the
   2026-04-11 dataset strategy entry.
5. `git add` all 4 files.
6. The parent session will handle the commit.

## Verification

- `grep "provisional" src/rts_predict/aoe2/reports/ROADMAP.md` — matches heading
- `grep "TO BE DETERMINED" src/rts_predict/aoe2/reports/*/ROADMAP.md` — 2 matches
- `grep "does not run Phase 06" src/rts_predict/aoe2/reports/aoestats/ROADMAP.md` — 0 matches
- `grep "Retraction" reports/research_log.md` — matches
