---
# Layer 1 — fixed frontmatter (mechanically validated)
# Required fields (all categories):
category:           # A | B | C | D | E | F  (per docs/TAXONOMY.md)
branch:             # e.g. feat/sc2-phase01-ingest  (prefix per category convention)
date:               # ISO-8601 date this plan was written
planner_model:      # e.g. claude-opus-4-6

# Optional fields (include/omit per category guidance below):
dataset:            # sc2egset | aoe2companion | aoestats | null
                    #   null only if category=C or E
phase:              # NN matching docs/PHASES.md, or null
pipeline_section:   # name from docs/PHASES.md, or null
invariants_touched: # list of invariant IDs from .claude/scientific-invariants.md, or []
                    #   populate for category A/F; [] for B-E unless data/model code touched

# source_artifacts: list of paths — notebooks, SQL, prior plans, docs consulted
#   Required for category A and F.
#   Optional for category B and D (include if work builds on prior analysis).
#   Omit for category C and E.
source_artifacts: []

# critique_required:
#   true  — category A and F (adversarial critique MUST exist before execution begins)
#   optional (true/false) — category B and D
#   false — category C and E
critique_required:  # true | false

# research_log_ref: path to the research_log.md entry this plan will produce
#   Optional; category A and F only.
#   For dataset-specific work, this points to the per-dataset log:
#     src/rts_predict/games/<game>/datasets/<dataset>/reports/research_log.md#<anchor>
#   For cross-cutting (CROSS) work, point to the root index log:
#     reports/research_log.md#<anchor>
#   Do NOT point dataset-specific entries at the root log.
research_log_ref:   # e.g. src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md#2026-04-12-phase01-ingest
---

# Plan: <short title>

## Scope

<1 paragraph describing the bounded work unit this plan covers. State what
phase/step/pipeline section is being addressed (Category A/F) or what
structural change is being made (Category B-E). Must be a single logical unit.>

## Problem Statement

<!-- Required for category A and F. Recommended for category B and D. Omit for category C and E. -->

<What is being solved and why now. 1–3 paragraphs of prose.
Describe the current state, the gap, and why this work is needed.
No solution proposed here — that belongs in Execution Steps.>

## Assumptions & unknowns

<!-- Required for category A and F. Optional for category B and D. Omit for category C and E. -->

- **Assumption:** <statement>
- **Unknown:** <what cannot be known until execution, and who/what resolves it>

## Literature context

<!-- Required for category A and F. Omit for category B, C, D, E. -->

<Cite relevant papers, benchmarks, or prior work that informs the approach.
Use `[OPINION]` tag for any claim that is not backed by a citation in
the Open questions section below or an external source.>

## Execution Steps

<!--
Each task uses the following rigid structure.

File scope and Read scope govern what the executor MAY write and what it
MAY read from sibling tasks.
-->

### T01 — <task name>

**Objective:** <1–3 sentences describing what this task achieves and why.>

**Instructions:**
1. <Numbered step — concrete, unambiguous action>
2. <Next step>
3. <...>

**Verification:**
- <Command or observable condition that confirms success — e.g. `pytest tests/... -v`>
- <Another check>

**File scope:** <List of files this task WRITES>
- `path/to/file.py`

**Read scope:** <List of files this task READS that are outputs of sibling tasks>
- `path/to/other_task_output.py`

---

### T02 — <task name>

**Objective:** <1–3 sentences.>

**Instructions:**
1. <Step>

**Verification:**
- <Check>

**File scope:**
- `path/to/file.py`

**Read scope:**
- `path/to/file_written_by_T01.py`

---

<!-- Add TNN blocks for each additional task. Number sequentially: T01, T02, ... -->

## File Manifest

<!-- List every file that will be created or modified across ALL tasks.
     One row per file. Action: Create | Rewrite | Update | Delete -->

| File | Action |
|------|--------|
| `path/to/file.py` | Create |
| `path/to/other_file.md` | Update |

## Gate Condition

<!-- Required for category A. Recommended for all categories.
     Enumerate the observable conditions that confirm the plan is complete.
     Reviewers verify these after execution. -->

- <Observable, binary condition — e.g. "All tests pass with coverage >= 95%">
- <Another condition — e.g. "PHASE_STATUS.yaml shows phase 01 complete">

## Out of scope

<!-- Required for category A and F. Recommended for all categories.
     Prevents executor scope creep. Be explicit about what is NOT done here. -->

- <Deferred item and rationale>

## Open questions

<!-- Required for category A and F. Optional for all categories.
     Each question must name who or what resolves it before execution can proceed. -->

- <Question — resolves by: <agent | user decision | experiment>>

