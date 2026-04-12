---
task_id: "T02"
task_name: "Rewrite plan_critique_template.md"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "docs/templates/plan_critique_template.md"
read_scope:
  - ".claude/scientific-invariants.md"
category: "C"
---

# Spec: Rewrite plan_critique_template.md

## Objective

Replace the entire file with a critique template that enumerates all 8
invariants, adds temporal discipline assessment, adds citations, and
clarifies the critique is produced by reviewer-adversarial.

## Instructions

1. Read `.claude/scientific-invariants.md` for invariant names.
2. Replace the entire file with new template structure:

   Frontmatter: `plan_ref` (planning/current_plan.md), `created`,
   `reviewer_model`, `category` (mirrors plan).

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

## Verification

- Template enumerates all 8 invariants by number and name
- Template has `## Citations` and `## Temporal discipline assessment`
- Header clarifies "Produced by reviewer-adversarial"
- Uses `plan_ref` (not `plan_id`) and `category` (not `scope`)
