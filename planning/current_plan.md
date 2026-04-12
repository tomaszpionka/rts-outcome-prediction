# Category C Plan: Plan Template Rewrite & Planner Output Contract

**Category:** C (chore)
**Branch:** `chore/plan-template-rewrite`
**Date:** 2026-04-11 (revised 2026-04-12)

---

## Scope

Rewrite `plan_template.md`, `plan_critique_template.md`, and
`planner_output_contract.md` to be compatible with the existing
DAG/spec/materialization pipeline. The current drafts (authored by ChatGPT)
are structurally incompatible — a plan conforming to them would fail
`/materialize_plan`. This chore makes them production-ready.

Additionally, update the materialization pre-flight to enforce critique
existence for Category A/F, and update planner agents to reference the
new contract.

**Source documents for this plan:**
- `plan_templating.md` — adversarial review with 18 findings (6 blockers)
- `templating_plan_review.md` — plan review with 1 blocker, 5 warnings
- `spec_mechanics_audit.md` — DAG execution mechanics investigation

---

## Problem Statement

The three draft templates have 7 blocking incompatibilities with the
materialization pipeline:

1. The plan template's DAG uses a flat `nodes:` list instead of the real
   `jobs > task_groups > tasks` hierarchy
2. The plan template is missing `## Execution Steps`, `## Suggested Execution
   Graph`, and `## File Manifest` — the three sections `/materialize_plan`
   consumes
3. No `spec_file` field in the DAG tasks
4. The contract forbids the word "task" — which the taxonomy defines and every
   DAG requires
5. The contract cites a non-existent "section 4.1"
6. The contract is scoped only to planner-science, not planner
7. The contract requires the planner to produce both plan AND critique
   (self-review), when the critique should be produced by reviewer-adversarial
   for independent external review

Beyond compatibility, the critique template lacks:
- A Citations section (scientific claims must be traceable)
- Explicit enumeration of all 8 invariants (partial example invites skipping)
- A temporal discipline assessment (the single most fatal thesis flaw)

---

## Design Decisions

Three decisions made during the planning session (2026-04-12), validated
by adversarial review:

**D1 — Critique producer split.** The planner produces the plan only.
Reviewer-adversarial produces the critique as a separate step for Category
A/B(optional)/D(conditional)/F. Enforcement: `/materialize_plan` pre-flight
checks critique existence for A/F.

**D2 — Mechanical per-task structure.** Each step in `## Execution Steps`
uses rigid structure (Objective / Instructions / Verification / File scope /
Read scope) that maps directly to the spec template. File scope and Read scope
map to spec YAML frontmatter, not to markdown sections. `/materialize_plan`
extracts each block into a spec file with minimal interpretation.

**D3 — Frontmatter disposition.** `plan_id` dropped (linked by filename
convention). `planner_model` and `source_artifacts` kept. `review_gates`
dropped (redundant with DAG). `scope` system replaced with `category` A-F.
`revision` tracking deferred. `research_log_ref` added as optional A/F field.

---

## Execution Steps

### T01 — Rewrite `docs/templates/plan_template.md`

**Objective:** Replace the entire file with a DAG-compatible template
derived from the working plan at `planning/current_plan.md`, not the
ChatGPT draft.

**Instructions:**
1. Read `docs/templates/dag_template.yaml` for the real DAG schema
2. Read `planning/current_plan.md` for real-world precedent
3. Replace the entire file with the new template structure:

   Frontmatter fields:
   - `category` (A-F), `branch`, `date`, `planner_model`, `dataset`,
     `phase`, `pipeline_section`, `invariants_touched`,
     `source_artifacts` (required A/F, optional B/D, omit C/E),
     `critique_required` (true A/F, optional B/D, false C/E),
     `research_log_ref` (optional, A/F only)

   Sections (with conditional markers):
   - `## Scope` (required all)
   - `## Problem Statement` (required all)
   - `## Assumptions & unknowns` (required A/F, optional B/D, omit C/E)
   - `## Literature context` (required A/F, omit B-E)
   - `## Execution Steps` (required all — per-task structure, see below)
   - `## File Manifest` (required all)
   - `## Gate Condition` (required A, recommended all)
   - `## Out of scope` (required A/F, recommended all)
   - `## Open questions` (required A/F, optional all)
   - `## Suggested Execution Graph` (required all — YAML per dag_template.yaml)

4. Document the per-task structure for `## Execution Steps`:
   ```
   ### TNN — <task name>
   **Objective:** <1-3 sentences>
   **Instructions:** <numbered steps>
   **Verification:** <commands, conditions>
   **File scope:** <files this task writes>
   **Read scope:** <files this task reads>
   ```
   Add a note: "File scope and Read scope map to spec YAML frontmatter
   (`file_scope`, `read_scope`), not to markdown sections."

5. Replace `## Proposed DAG` with `## Suggested Execution Graph` using
   `jobs > task_groups > tasks` hierarchy. Every task must include
   `spec_file`, `file_scope`, `parallel_safe`, `depends_on`.

**Verification:**
- Template contains `## Suggested Execution Graph` (not `## Proposed DAG`)
- YAML uses `jobs > task_groups > tasks` hierarchy
- Template contains `## Execution Steps` and `## File Manifest`
- Template uses `category:` A-F (not `scope:`)
- Frontmatter includes `planner_model` and `source_artifacts`
- Per-task structure documented with mapping note

**File scope:** `docs/templates/plan_template.md`
**Read scope:** `docs/templates/dag_template.yaml`, `planning/current_plan.md`

---

### T02 — Rewrite `docs/templates/plan_critique_template.md`

**Objective:** Replace the entire file with a critique template that
enumerates all 8 invariants, adds temporal discipline assessment, adds
citations, and clarifies the critique is produced by reviewer-adversarial.

**Instructions:**
1. Read `.claude/scientific-invariants.md` for invariant names
2. Replace the entire file with new template structure:

   Frontmatter: `plan_ref` (planning/current_plan.md), `created`,
   `reviewer_model`, `category` (mirrors plan)

   Header note: "Produced by reviewer-adversarial. Audience: Tomasz +
   viva preparation. Not consumed by executors or materialization."

   Sections:
   - `## Invariants check` — ALL 8 enumerated by number and name:
     `#1 (per-player split)` through `#8 (cross-game protocol)`,
     each with yes/no/n-a + evidence pointer
   - `## Temporal discipline assessment` (required A/F, omit C/E)
   - `## Defensibility check`
   - `## Likely supervisor / committee questions`
   - `## Known weaknesses`
   - `## Alternatives considered and rejected`
   - `## Citations` — every scientific claim must cite source;
     uncited claims labeled `[OPINION]`

**Verification:**
- Template enumerates all 8 invariants by number and name
- Template has `## Citations` and `## Temporal discipline assessment`
- Header clarifies "Produced by reviewer-adversarial"
- Uses `plan_ref` (not `plan_id`) and `category` (not `scope`)

**File scope:** `docs/templates/plan_critique_template.md`
**Read scope:** `.claude/scientific-invariants.md`

---

### T03 — Rewrite `docs/templates/planner_output_contract.md`

**Objective:** Replace the entire file with an agent-agnostic contract
that produces plans only (no self-critique) and uses correct terminology.

**Instructions:**
1. Read `docs/templates/plan_template.md` (after T01 rewrites it)
2. Read `docs/templates/plan_critique_template.md` (after T02)
3. Read `docs/TAXONOMY.md` for forbidden/required terms
4. Replace the entire file. Key changes:

   a. Agent-agnostic: "You are a planner agent" (not "planner-science")
   b. Required output: ONE file (`planning/current_plan.md`) — not two.
      The critique is NOT the planner's responsibility.
   c. After producing the plan, the planner must instruct the parent
      session: "For Category A/F, adversarial critique is required
      before materialization. Dispatch reviewer-adversarial to produce
      `planning/current_plan.critique.md`."
   d. Forbidden terms from TAXONOMY.md: Stage, Experiment (formal),
      Milestone, Workstream, Track, Initiative, Epic, Component (work
      unit), Section (unqualified). "Task" is NOT forbidden.
   e. Remove "section 4.1" reference
   f. Replace `scope` system with `category` A-F
   g. Conditional requirements by category:

      | Category | Plan sections | Critique? |
      |----------|--------------|-----------|
      | A | all | yes — reviewer-adversarial, all sections |
      | B | Scope, Execution Steps, File Manifest, DAG, Out of scope | yes — invariants + weaknesses |
      | C | Scope, Execution Steps, File Manifest, DAG | no |
      | D | Scope, Execution Steps, File Manifest, DAG, Out of scope | yes if file_scope touches `src/rts_predict/<game>/` |
      | E | Scope, Execution Steps, File Manifest, DAG | no |
      | F | all | yes — reviewer-adversarial, all sections |

   h. Document per-task Execution Steps structure (matching T01)
   i. Self-check: category A-F, DAG uses correct schema, every task
      has spec_file/file_scope/parallel_safe/depends_on, every TNN maps
      to a task in the graph, File Manifest complete, no forbidden terms,
      invariants_touched populated

**Verification:**
- Contract does NOT forbid the word "task"
- Contract does NOT cite "section 4.1"
- Contract addresses both planner agents
- Contract uses Category A-F
- Contract says planner produces plan ONLY (not critique)
- Contract tells planner to flag critique need for A/F

**File scope:** `docs/templates/planner_output_contract.md`
**Read scope:** `docs/templates/plan_template.md`, `docs/templates/plan_critique_template.md`, `docs/TAXONOMY.md`

---

### T04 — Update `planning/README.md`

**Objective:** Add critique to the planning lifecycle and purge protocol.

**Instructions:**
1. Add `current_plan.critique.md` to the contents table (ephemeral,
   sibling to plan). Note: produced by reviewer-adversarial for
   Category A/B/D/F, not by the planner.
2. Add to purge protocol: delete after merge alongside specs and DAG.
3. Add to lifecycle: after plan written, before materialization,
   reviewer-adversarial produces critique for A/F.

**Verification:**
- `current_plan.critique.md` listed in contents table
- `current_plan.critique.md` listed in purge protocol

**File scope:** `planning/README.md`
**Read scope:** none

---

### T05 — Update `.claude/agents/planner-science.md`

**Objective:** Add output contract reference and critique-flagging
instruction. Do NOT instruct the planner to produce the critique itself.

**Instructions:**
1. Add to constraints: "Plan output must conform to
   `docs/templates/planner_output_contract.md`. Read it before producing
   output."
2. Add: "For Category A/F, after producing the plan, instruct the parent
   session that adversarial critique is required before materialization.
   Do NOT produce the critique yourself — reviewer-adversarial handles it."

**Verification:**
- Agent references output contract
- Agent does NOT claim to produce critique
- Agent flags critique need for A/F

**File scope:** `.claude/agents/planner-science.md`
**Read scope:** none

---

### T06 — Update `.claude/agents/planner.md`

**Objective:** Same contract reference addition as T05.

**Instructions:**
1. Add to constraints: "Plan output must conform to
   `docs/templates/planner_output_contract.md`. Read it before producing
   output."
2. Add: "For Category B/D where critique is applicable, instruct the
   parent session that adversarial review is available. Do NOT produce
   the critique yourself."

**Verification:**
- Agent references output contract
- Agent does NOT claim to produce critique

**File scope:** `.claude/agents/planner.md`
**Read scope:** none

---

### T07 — Update `.claude/commands/materialize_plan.md`

**Objective:** Add pre-flight check requiring critique existence for
Category A/F before materialization proceeds.

**Instructions:**
1. Read the plan's frontmatter to extract `category` and
   `critique_required`
2. Add to pre-flight checks (after existing checks):
   "If `category` is A or F (or `critique_required: true`), verify
   `planning/current_plan.critique.md` exists and is non-empty.
   If missing, HALT: 'Category A/F requires adversarial critique
   before materialization. Dispatch reviewer-adversarial first.'"

**Verification:**
- Pre-flight section includes critique existence check
- Check references correct file path
- Check halts with actionable message

**File scope:** `.claude/commands/materialize_plan.md`
**Read scope:** none

---

### T08 — Update CHANGELOG

**Objective:** Add entries for all template rewrites, agent updates,
and materialization update.

**Instructions:**
1. Under `[Unreleased]`, add Changed entries:
   - Rewrite `plan_template.md` — DAG-compatible, per-task structure
   - Rewrite `plan_critique_template.md` — all 8 invariants, citations,
     temporal discipline, produced by reviewer-adversarial
   - Rewrite `planner_output_contract.md` — agent-agnostic, plan-only
     output, Category A-F
   - Update `planning/README.md` — critique in lifecycle and purge
   - Update `planner-science.md` and `planner.md` — contract reference
   - Update `materialize_plan.md` — critique pre-flight for A/F

**Verification:**
- CHANGELOG has entries under `[Unreleased]`
- All 7 modified files mentioned

**File scope:** `CHANGELOG.md`
**Read scope:** none

---

## File Manifest

| File | Action |
|------|--------|
| `docs/templates/plan_template.md` | Rewrite |
| `docs/templates/plan_critique_template.md` | Rewrite |
| `docs/templates/planner_output_contract.md` | Rewrite |
| `planning/README.md` | Update |
| `.claude/agents/planner-science.md` | Update |
| `.claude/agents/planner.md` | Update |
| `.claude/commands/materialize_plan.md` | Update |
| `CHANGELOG.md` | Update |

---

## Gate Condition

- `plan_template.md` contains `## Suggested Execution Graph` (not `## Proposed DAG`)
- `plan_template.md` DAG example uses `jobs > task_groups > tasks` hierarchy
- `plan_template.md` contains `## Execution Steps` and `## File Manifest`
- `plan_template.md` uses `category:` A-F (not `scope:`)
- `plan_template.md` frontmatter includes `planner_model` and `source_artifacts`
- `plan_critique_template.md` enumerates all 8 invariants by number and name
- `plan_critique_template.md` has `## Citations` and `## Temporal discipline assessment`
- `plan_critique_template.md` header says "Produced by reviewer-adversarial"
- `planner_output_contract.md` does NOT forbid the word "task"
- `planner_output_contract.md` does NOT cite "section 4.1"
- `planner_output_contract.md` addresses both planner agents
- `planner_output_contract.md` says planner produces plan ONLY
- `planner_output_contract.md` uses Category A-F
- `planning/README.md` lists `current_plan.critique.md` in contents and purge
- Both planner agents reference the output contract in constraints
- Both planner agents do NOT claim to produce critique
- `materialize_plan.md` has critique pre-flight check for A/F

---

## Out of Scope

Deferred for future work:
- Programmatic template enforcement (linting plans against templates)
- `revision:` / `prior_revision_sha:` frontmatter tracking (git log suffices
  for Category C; revisit before first Category A plan uses this template)
- Research log entry enforcement (field added but not validated)
- Dispatch rules in CLAUDE.md and executor.md (already implemented on this
  branch — see `spec_mechanics_audit.md` Sections 11-13)

---

## Open questions

None remaining — all 5 calls from `templating_plan_review.md` resolved.

---

## Suggested Execution Graph

```yaml
dag_id: "dag_plan_template_rewrite"
plan_ref: "planning/current_plan.md"
category: "C"
branch: "chore/plan-template-rewrite"
base_ref: "master"
default_isolation: "shared_branch"

jobs:
  - job_id: "J01"
    name: "Plan template rewrite"

    task_groups:
      - group_id: "TG01"
        name: "Rewrite plan + critique templates"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T01"
            name: "Rewrite plan_template.md"
            spec_file: "planning/specs/spec_01_plan_template.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "docs/templates/plan_template.md"
            read_scope:
              - "docs/templates/dag_template.yaml"
              - "planning/current_plan.md"
            depends_on: []
          - task_id: "T02"
            name: "Rewrite plan_critique_template.md"
            spec_file: "planning/specs/spec_02_critique_template.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "docs/templates/plan_critique_template.md"
            read_scope:
              - ".claude/scientific-invariants.md"
            depends_on: []

      - group_id: "TG02"
        name: "Rewrite planner output contract"
        depends_on: ["TG01"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T03"
            name: "Rewrite planner_output_contract.md"
            spec_file: "planning/specs/spec_03_output_contract.md"
            agent: "executor"
            parallel_safe: false
            file_scope:
              - "docs/templates/planner_output_contract.md"
            read_scope:
              - "docs/templates/plan_template.md"
              - "docs/templates/plan_critique_template.md"
              - "docs/TAXONOMY.md"
            depends_on: []

      - group_id: "TG03"
        name: "Update lifecycle, agents, and materialization"
        depends_on: ["TG02"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T04"
            name: "Update planning/README.md"
            spec_file: "planning/specs/spec_04_planning_readme.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "planning/README.md"
            depends_on: []
          - task_id: "T05"
            name: "Update planner-science.md"
            spec_file: "planning/specs/spec_05_planner_science.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - ".claude/agents/planner-science.md"
            depends_on: []
          - task_id: "T06"
            name: "Update planner.md"
            spec_file: "planning/specs/spec_06_planner.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - ".claude/agents/planner.md"
            depends_on: []
          - task_id: "T07"
            name: "Update materialize_plan.md"
            spec_file: "planning/specs/spec_07_materialize.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - ".claude/commands/materialize_plan.md"
            depends_on: []

      - group_id: "TG04"
        name: "CHANGELOG"
        depends_on: ["TG03"]
        review_gate:
          agent: "reviewer"
          scope: "cumulative"
          on_blocker: "halt"
        tasks:
          - task_id: "T08"
            name: "Update CHANGELOG"
            spec_file: "planning/specs/spec_08_changelog.md"
            agent: "executor"
            parallel_safe: false
            file_scope:
              - "CHANGELOG.md"
            depends_on: []

final_review:
  agent: "reviewer-deep"
  scope: "all"
  base_ref: "master"
  on_blocker: "halt"

failure_policy:
  on_failure: "halt"
```
