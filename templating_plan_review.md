# Plan Review: Plan Template Rewrite & Planner Output Contract

**Plan:** `planning/current_plan.md`
**Branch:** `chore/plan-template-rewrite`
**Reviewer:** reviewer-adversarial (Opus)
**Date:** 2026-04-11
**Verdict:** REVISE BEFORE EXECUTION — 1 blocker, 5 warnings

---

## Tier 1 Blocker Coverage (all 6 from plan_templating.md)

| # | Blocker | Addressed? |
|---|---------|-----------|
| 1 | Flat `nodes:` → `jobs > task_groups > tasks` | YES |
| 2 | Missing `## Execution Steps`, `## Suggested Execution Graph`, `## File Manifest` | YES |
| 3 | Missing `spec_file` in DAG tasks | YES |
| 4 | Contract forbids "task" (taxonomy defines it) | YES |
| 5 | Contract cites non-existent "section 4.1" | YES |
| 6 | Contract scoped only to planner-science | YES |

## Tier 2 Coverage

| # | Item | Addressed? |
|---|------|-----------|
| 7 | Citations in critique | YES |
| 8 | Enumerate all 8 invariants | YES |
| 9 | Align scope → Category A-F | YES |
| 10 | Gate Condition section | YES |
| 11 | File Manifest section | YES |
| 12 | Agent-agnostic contract | YES |
| 13 | Revision tracking | **NOT ADDRESSED** |

## Tier 3 Coverage

| # | Item | Addressed? |
|---|------|-----------|
| 14 | Critique in planning/README.md lifecycle | YES |
| 15 | Research log entry link | **NOT ADDRESSED** |
| 16 | Literature context section | YES |
| 17 | Temporal discipline assessment | YES |
| 18 | Group frontmatter by concern | NOT ADDRESSED (minor) |

---

## Issues

### BLOCKER: Frontmatter silently drops 4 fields

The existing `plan_template.md` defines `plan_id`, `planner_model`,
`source_artifacts`, and `review_gates`. The proposed replacement includes
none of them. This needs explicit disposition for each:

| Field | Recommendation |
|-------|---------------|
| `plan_id` | **KEEP or REPLACE.** The critique template uses `plan_ref` (file path) but the plan itself has no identifier. Either add `plan_id` back, or add `plan_ref` to BOTH templates so they share a linkage key. Without it, there is no machine-parseable link between a plan and its critique. |
| `planner_model` | **KEEP.** You need to know post-hoc whether a plan was Opus or Sonnet. Git blame tells you the committer, not the model. One field, high audit value. |
| `source_artifacts` | **KEEP for A/F, mark optional for C/E.** The existing contract says "planning without inputs is speculation." Per-task `read_scope` captures what each executor reads, but the plan-level "what did the planner consult?" is different and lost without this field. |
| `review_gates` | **DROP with justification.** Redundant with `review_gate` in the DAG YAML. Note the removal in the plan. |

### WARNING: No "Out of scope" section

The plan proposes a template that includes `## Out of scope` but the plan
itself has no such section. This leaves unstated:
- Programmatic enforcement of templates (templating_audit.md Tier 1-3)
- Revision tracking for plan iterations (#13)
- Research log entry cross-reference (#15)

Add a brief Out of Scope section stating these are deferred.

### WARNING: Category D critique condition is ambiguous

The conditional requirements table says Category D gets a critique "if
data/feature code." Who evaluates this — the planner or the reviewer? The
contract should specify. Suggestion: "The planner decides; if uncertain,
produce the critique."

### WARNING: Revision tracking not addressed

Plans go through revision cycles. The adversarial review recommended
`revision:` and `prior_revision_sha:` in frontmatter. Either add them or
explicitly defer to Out of Scope.

### WARNING: Research log entry link not addressed

Category A plans should cross-reference their research log entry for
traceability (plan → research log → thesis). Either add a
`research_log_entry:` field to frontmatter (optional, A/F only) or defer.

### WARNING: DAG uses reviewer (Sonnet) everywhere, final_review uses reviewer-deep

The dag_template.yaml default for final_review is `reviewer-adversarial`
(Opus). The plan uses `reviewer-deep`. For Category C this is fine, but
the plan should document the override rationale. More importantly: the
template's example DAG should specify the correct default for Category A
plans (which would be reviewer-adversarial).

---

## Calls for Tomasz

Before approving execution:

1. **Decide on the 4 dropped frontmatter fields.** My recommendation above:
   keep `planner_model` and `source_artifacts`, drop `review_gates` with
   a note, and either keep `plan_id` or use `plan_ref` in both templates.

2. **Add "Out of scope" to the plan** listing enforcement, revision tracking,
   and research log linking as deferred work.

3. **Clarify Category D critique condition** — who decides?

4. **Decide: revision tracking in frontmatter — now or later?**

5. **Decide: research log entry cross-reference — now or later?**

Once these 5 decisions are made, I can revise the plan in <5 minutes and
it's ready for `/materialize_plan`.

---

## What the plan gets right

- All 6 Tier 1 blockers addressed
- 6 of 7 Tier 2 items addressed
- DAG dependency chain is correct: templates → contract (reads templates) →
  agents (reference contract) → CHANGELOG
- Critique template with mandatory citations + temporal discipline section
  is the highest-value addition — this is what makes Opus plans defensible
  rather than AI slop
- Agent-agnostic contract ensures both Sonnet (chore) and Opus (science)
  planners follow the same rules
