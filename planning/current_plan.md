# Category C Plan: Template Hierarchy Restructuring (revised)

**Category:** C (chore)
**Branch:** `chore/template-hierarchy`
**Date:** 2026-04-11 (revised — full honest inventory)

---

## Scope

Complete the template hierarchy restructuring. The prior plan claimed Steps 1-11
were done; in reality the files exist on disk with content but are **untracked
or unstaged** — never committed. Additionally, `docs/ml_experiment_phases/` and
`docs/research/` contain zero-byte stubs that need to be populated.

This plan covers ALL remaining work on this branch: committing existing content,
populating zero-byte stubs, retracting premature AoE2 commitments, and updating
cross-cutting references.

---

## True state of disk

### Has content but UNTRACKED (need `git add`):
- `docs/templates/phase_template.yaml` (2,043 bytes)
- `docs/templates/pipeline_section_template.yaml` (1,877 bytes)
- `docs/templates/dataset_roadmap_template.yaml` (2,472 bytes)
- `docs/templates/phase_status_template.yaml` (2,093 bytes)
- `docs/templates/pipeline_section_status_template.yaml` (2,204 bytes)
- `docs/templates/step_status_template.yaml` (2,405 bytes)
- `src/rts_predict/sc2/reports/sc2egset/PIPELINE_SECTION_STATUS.yaml` (1,678 bytes)
- `src/rts_predict/aoe2/reports/aoe2companion/PIPELINE_SECTION_STATUS.yaml` (1,689 bytes)
- `src/rts_predict/aoe2/reports/aoestats/PIPELINE_SECTION_STATUS.yaml` (1,756 bytes)
- `planning/dags/DAG.yaml` (materialized DAG for this plan)
- `planning/specs/spec_01_roadmap_retractions.md` (materialized spec — now stale)

### Modified but UNSTAGED (need `git add`):
- `docs/templates/research_log_template.yaml` (modified from tracked version)
- `src/rts_predict/sc2/reports/sc2egset/STEP_STATUS.yaml` (added game, pipeline_section)
- `src/rts_predict/aoe2/reports/aoe2companion/STEP_STATUS.yaml` (same)
- `src/rts_predict/aoe2/reports/aoestats/STEP_STATUS.yaml` (same)
- `src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml` (derivation chain comments)
- `src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml` (same)
- `src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml` (same)
- `src/rts_predict/aoe2/reports/ROADMAP.md` (Step 0a — retracted dataset strategy)
- `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md` (Step 0b — retracted role banner)
- `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md` (Step 0c — retracted role banner)
- `reports/research_log.md` (Step 0d — retraction entry)
- `CHANGELOG.md` (partially updated)
- `CLAUDE.md` (materialization gate added to Plan/Execute section)
- `planning/README.md` (materialization gate added to Lifecycle)
- `planning/INDEX.md` (spec link added)
- `.claude/agents/executor.md` (spec-first read order)

### Zero-byte stubs — NEED POPULATING:
- `docs/ml_experiment_phases/PHASES.md`
- `docs/ml_experiment_phases/PIPELINE_SECTIONS.md`
- `docs/ml_experiment_phases/STEPS.md`
- `docs/research/RESEARCH_LOG.md`
- `docs/research/RESEARCH_LOG_ENTRY.md`
- `docs/research/ROADMAP.md`

### Debris to remove:
- `_current_plan.md` (root relic from planning/ migration)

---

## Execution steps

### TG01: Commit existing template + status file content

All template and status files already have correct content on disk. This group
stages and commits them.

**T01 — Stage and commit 6 authoring/status templates**

Stage the 6 untracked template files in `docs/templates/` plus the modified
`research_log_template.yaml`. Verify content is non-empty and follows the
`value:` + `required:` pattern from `step_template.yaml`. Commit.

Files: `docs/templates/{phase_template,pipeline_section_template,dataset_roadmap_template,phase_status_template,pipeline_section_status_template,step_status_template}.yaml`, `docs/templates/research_log_template.yaml`

**T02 — Stage and commit 3 PIPELINE_SECTION_STATUS.yaml + 6 modified status files**

Stage the 3 untracked PIPELINE_SECTION_STATUS.yaml files and the 6 modified
STEP_STATUS.yaml / PHASE_STATUS.yaml files. Verify derivation chain comments
are consistent across all 9 files. Commit.

Files: `src/rts_predict/{sc2/reports/sc2egset,aoe2/reports/aoe2companion,aoe2/reports/aoestats}/{PIPELINE_SECTION_STATUS,STEP_STATUS,PHASE_STATUS}.yaml`

### TG02: Retract premature AoE2 dataset strategy

The edits are already on disk (executed earlier this session). Stage and commit.

**T03 — Stage and commit AoE2 ROADMAP retractions + research log**

Verify the 3 ROADMAP files contain "TO BE DETERMINED" roles (not PRIMARY /
SUPPLEMENTARY VALIDATION), the game-level ROADMAP has "provisional" language,
and `reports/research_log.md` has the retraction section. Stage and commit.

Files: `src/rts_predict/aoe2/reports/{ROADMAP.md,aoestats/ROADMAP.md,aoe2companion/ROADMAP.md}`, `reports/research_log.md`

### TG03: Populate zero-byte stubs in `docs/ml_experiment_phases/`

These files decompose `docs/PHASES.md` into one file per hierarchy level.

**T04 — Populate `docs/ml_experiment_phases/PHASES.md`**

Extract Phase-level content from `docs/PHASES.md`: the 7-Phase table, scope
rules, Phase 07 semantics, and maintenance rules. This file becomes the
reference for Phase definitions independent of Pipeline Section details.

Structure:
- Header referencing `docs/PHASES.md` as upstream source
- The 7-Phase summary table (number, name, source manual, one-line summary)
- Phase scope rule (every Phase is dataset-scoped)
- Phase 07 gate marker semantics
- Maintenance rules (never invent/renumber Phases)

**T05 — Populate `docs/ml_experiment_phases/PIPELINE_SECTIONS.md`**

Extract Pipeline Section content from `docs/PHASES.md`: the derivation rule,
the per-Phase Pipeline Section tables, and the exclusion lists. This becomes
the reference for Pipeline Section enumeration.

Structure:
- Header referencing `docs/PHASES.md` as upstream source
- Pipeline Section derivation rule (which manual sections become Pipeline Sections)
- Per-Phase Pipeline Section tables (Phases 01-06)
- Exclusion lists (what was excluded from each Phase and why)

**T06 — Populate `docs/ml_experiment_phases/STEPS.md`**

Step-level reference: not an enumeration (Steps are dataset-scoped in ROADMAPs)
but the contract that defines what a Step IS and what it must produce.

Structure:
- Header referencing `docs/TAXONOMY.md` Step definition
- Step numbering convention (NN_NN_NN)
- Step contract (one notebook, artifacts, research log entry)
- Step schema reference (pointer to `docs/templates/step_template.yaml`)
- Directory layout (sandbox + artifacts mirroring rule)

### TG04: Populate zero-byte stubs in `docs/research/`

**T07 — Populate `docs/research/RESEARCH_LOG.md`**

Reference document for the research log structure. Not the log itself (that's
`reports/research_log.md`) — this is the specification.

Structure:
- Purpose and location of the actual log (`reports/research_log.md`)
- Ordering convention (reverse chronological)
- Entry structure reference (pointer to `docs/templates/research_log_entry_template.yaml`)
- Hierarchy linking (how entries reference Phase/Step)
- Dataset tagging rules
- When entries are required (Category A mandatory, C recommended, F recommended)

**T08 — Populate `docs/research/RESEARCH_LOG_ENTRY.md`**

Human-readable rendering of `docs/templates/research_log_entry_template.yaml`,
replacing the old `reports/RESEARCH_LOG_TEMPLATE.md` which served this purpose.

Structure: mirrors the YAML template fields as markdown sections with guidance
on what each section should contain.

**T09 — Populate `docs/research/ROADMAP.md`**

Reference document for dataset ROADMAP structure.

Structure:
- Purpose (dataset-level execution plans for Phases 01-07)
- Location convention (`src/rts_predict/<game>/reports/<dataset>/ROADMAP.md`)
- Schema reference (pointer to `docs/templates/dataset_roadmap_template.yaml`)
- Relationship to `docs/PHASES.md` (ROADMAPs implement, don't invent)
- Step definition reference (pointer to `docs/templates/step_template.yaml`)

### TG05: Workflow updates + cleanup + CHANGELOG

**T10 — Stage workflow changes and clean up debris**

Stage the already-modified workflow files:
- `CLAUDE.md` (materialization gate)
- `planning/README.md` (materialization gate)
- `planning/INDEX.md` (spec link)
- `.claude/agents/executor.md` (spec-first read order)

Delete `_current_plan.md` from repo root (untracked relic).

Update `CHANGELOG.md` with the full set of changes for this branch.

Stage `planning/dags/DAG.yaml` and `planning/specs/spec_01_roadmap_retractions.md`.

Commit.

---

## File manifest

**Untracked → staged (9):**
1. `docs/templates/phase_template.yaml`
2. `docs/templates/pipeline_section_template.yaml`
3. `docs/templates/dataset_roadmap_template.yaml`
4. `docs/templates/phase_status_template.yaml`
5. `docs/templates/pipeline_section_status_template.yaml`
6. `docs/templates/step_status_template.yaml`
7. `src/rts_predict/sc2/reports/sc2egset/PIPELINE_SECTION_STATUS.yaml`
8. `src/rts_predict/aoe2/reports/aoe2companion/PIPELINE_SECTION_STATUS.yaml`
9. `src/rts_predict/aoe2/reports/aoestats/PIPELINE_SECTION_STATUS.yaml`

**Modified → staged (16):**
10. `docs/templates/research_log_template.yaml`
11-13. 3× STEP_STATUS.yaml
14-16. 3× PHASE_STATUS.yaml
17-19. 3× AoE2 ROADMAPs
20. `reports/research_log.md`
21. `CHANGELOG.md`
22. `CLAUDE.md`
23. `planning/README.md`
24. `planning/INDEX.md`
25. `.claude/agents/executor.md`

**New (populated from zero-byte, 6):**
26. `docs/ml_experiment_phases/PHASES.md`
27. `docs/ml_experiment_phases/PIPELINE_SECTIONS.md`
28. `docs/ml_experiment_phases/STEPS.md`
29. `docs/research/RESEARCH_LOG.md`
30. `docs/research/RESEARCH_LOG_ENTRY.md`
31. `docs/research/ROADMAP.md`

**Planning artifacts (2):**
32. `planning/dags/DAG.yaml`
33. `planning/specs/spec_01_roadmap_retractions.md` (stale — from prior partial execution)

**Deleted (1):**
34. `_current_plan.md`

---

## Gate condition

- All 6 authoring templates in `docs/templates/` are tracked and non-empty
- All 3 status templates in `docs/templates/` are tracked and non-empty
- All 3 PIPELINE_SECTION_STATUS.yaml files are tracked and non-empty
- All 6 STEP_STATUS/PHASE_STATUS.yaml files have `pipeline_section` / derivation chain
- All 3 AoE2 ROADMAPs have "TO BE DETERMINED" roles, no Phase scope restrictions
- All 6 files in `docs/ml_experiment_phases/` and `docs/research/` are non-empty
- `_current_plan.md` does not exist at repo root
- CHANGELOG.md has entries for all changes
- Derivation chain is consistent across all status files

---

## Suggested Execution Graph

```yaml
dag_id: "dag_template_hierarchy_full"
spec_ref: "planning/current_plan.md"
category: "C"
branch: "chore/template-hierarchy"
base_ref: "master"
default_isolation: "shared_branch"

jobs:
  - job_id: "J01"
    name: "Template hierarchy — full completion"

    task_groups:
      - group_id: "TG01"
        name: "Commit existing template + status file content"
        depends_on: []
        review_gate:
          agent: "reviewer"
          base_ref: "auto"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T01"
            name: "Stage + commit 7 template files"
            agent: "executor"
            file_scope:
              - "docs/templates/phase_template.yaml"
              - "docs/templates/pipeline_section_template.yaml"
              - "docs/templates/dataset_roadmap_template.yaml"
              - "docs/templates/phase_status_template.yaml"
              - "docs/templates/pipeline_section_status_template.yaml"
              - "docs/templates/step_status_template.yaml"
              - "docs/templates/research_log_template.yaml"
            parallel_safe: true
            depends_on: []
          - task_id: "T02"
            name: "Stage + commit 9 status files"
            agent: "executor"
            file_scope:
              - "src/rts_predict/sc2/reports/sc2egset/PIPELINE_SECTION_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoe2companion/PIPELINE_SECTION_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoestats/PIPELINE_SECTION_STATUS.yaml"
              - "src/rts_predict/sc2/reports/sc2egset/STEP_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoe2companion/STEP_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoestats/STEP_STATUS.yaml"
              - "src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml"
              - "src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml"
            parallel_safe: true
            depends_on: []

      - group_id: "TG02"
        name: "Retract premature AoE2 dataset strategy"
        depends_on: ["TG01"]
        review_gate:
          agent: "reviewer"
          base_ref: "auto"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T03"
            name: "Stage + commit AoE2 ROADMAP retractions + research log"
            agent: "executor"
            file_scope:
              - "src/rts_predict/aoe2/reports/ROADMAP.md"
              - "src/rts_predict/aoe2/reports/aoestats/ROADMAP.md"
              - "src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md"
              - "reports/research_log.md"
            parallel_safe: false
            depends_on: []

      - group_id: "TG03"
        name: "Populate docs/ml_experiment_phases/"
        depends_on: ["TG01"]
        review_gate:
          agent: "reviewer"
          base_ref: "auto"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T04"
            name: "Populate PHASES.md"
            agent: "executor"
            file_scope:
              - "docs/ml_experiment_phases/PHASES.md"
            read_scope:
              - "docs/PHASES.md"
            parallel_safe: true
            depends_on: []
          - task_id: "T05"
            name: "Populate PIPELINE_SECTIONS.md"
            agent: "executor"
            file_scope:
              - "docs/ml_experiment_phases/PIPELINE_SECTIONS.md"
            read_scope:
              - "docs/PHASES.md"
            parallel_safe: true
            depends_on: []
          - task_id: "T06"
            name: "Populate STEPS.md"
            agent: "executor"
            file_scope:
              - "docs/ml_experiment_phases/STEPS.md"
            read_scope:
              - "docs/TAXONOMY.md"
              - "docs/templates/step_template.yaml"
            parallel_safe: true
            depends_on: []

      - group_id: "TG04"
        name: "Populate docs/research/"
        depends_on: ["TG01"]
        review_gate:
          agent: "reviewer"
          base_ref: "auto"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T07"
            name: "Populate RESEARCH_LOG.md"
            agent: "executor"
            file_scope:
              - "docs/research/RESEARCH_LOG.md"
            read_scope:
              - "docs/templates/research_log_template.yaml"
            parallel_safe: true
            depends_on: []
          - task_id: "T08"
            name: "Populate RESEARCH_LOG_ENTRY.md"
            agent: "executor"
            file_scope:
              - "docs/research/RESEARCH_LOG_ENTRY.md"
            read_scope:
              - "docs/templates/research_log_entry_template.yaml"
            parallel_safe: true
            depends_on: []
          - task_id: "T09"
            name: "Populate ROADMAP.md"
            agent: "executor"
            file_scope:
              - "docs/research/ROADMAP.md"
            read_scope:
              - "docs/templates/dataset_roadmap_template.yaml"
            parallel_safe: true
            depends_on: []

      - group_id: "TG05"
        name: "Workflow updates + cleanup + CHANGELOG"
        depends_on: ["TG02", "TG03", "TG04"]
        review_gate:
          agent: "reviewer"
          base_ref: "auto"
          scope: "cumulative"
          on_blocker: "halt"
        tasks:
          - task_id: "T10"
            name: "Stage workflow files, delete relic, update CHANGELOG"
            agent: "executor"
            file_scope:
              - "CLAUDE.md"
              - "CHANGELOG.md"
              - "planning/README.md"
              - "planning/INDEX.md"
              - "planning/dags/DAG.yaml"
              - "planning/specs/spec_01_roadmap_retractions.md"
              - ".claude/agents/executor.md"
              - "scripts/hooks/log-subagent.sh"
            parallel_safe: false
            depends_on: []

final_review:
  agent: "reviewer-deep"
  scope: "all"
  base_ref: "master"
  on_blocker: "halt"

failure_policy:
  on_failure: "halt"
```

---

## Provenance

This plan supersedes the prior version (committed at 9e4279f on this branch)
which incorrectly claimed Steps 1-11 were complete. The files existed on disk
with content but were never committed. This revision is an honest inventory of
all remaining work.

The `docs/ml_experiment_phases/` decomposition and `docs/research/` population
are new scope items identified by the user — the original plan missed them.
