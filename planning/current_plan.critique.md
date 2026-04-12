# Adversarial Critique — Plan: Rerun 01_01_01

**Plan:** planning/current_plan.md
**Phase:** 01 (Data Exploration) / Step 01_01_01 Rerun
**Date:** 2026-04-12
**Verdict:** REVISE BEFORE EXECUTION

---

## Lens assessments

- **Temporal discipline:** N/A — Phase 01 file inventory; no features, no model inputs.
- **Statistical methodology:** N/A — no statistical analysis, models, or evaluation.
- **Feature engineering:** N/A — no features constructed.
- **Thesis defensibility:** ADEQUATE — see findings below.
- **Cross-game comparability:** MAINTAINED — identical treatment across all 3 datasets.

## Findings

### 1. [WARNING] Invariant #9 "external source documentation" boundary

The invariant text allows referencing "External source documentation (paper
citations, acquisition provenance, Zenodo metadata)" but did not define a
test for what qualifies.

**Resolution (applied to plan):** Added explicit boundary definition to
Invariant #9 text — use exact source titles verbatim, not paraphrased
interpretive labels. Citations deferred to thesis chapters.

### 2. [WARNING] Raw README `description` field — surviving leak vector

The `description` field in Section C of each raw README contained
interpretive labels ("daily match parquet files," "tournament replay files").
The plan did not address this field.

**Resolution (applied to plan):** Added `description` field to T02 strip
list. T06-T08 repopulate from artifacts.

### 3. [WARNING] `temporal_grain: unknown` contradiction

Setting `temporal_grain: unknown` when the 01_01_01 artifact contains
date_analysis with cadence information creates an internal contradiction.

**Resolution (applied to plan):** Changed to populate `temporal_grain` from
artifact `date_analysis`. Filename-derived date cadence is filesystem-level
observation, not content-level interpretation.

### 4. [WARNING] Gate verification regex false positives/negatives

The regex `complete\b` matches `gap_analysis_status: complete` (legitimate
template value). The regex also missed interpretive terms like "tournament,"
"replay" as semantic labels.

**Resolution (applied to plan):** Removed `complete\b` from regex. Clarified
that "daily/weekly" are now permitted in `temporal_grain` fields but banned
as semantic role labels for files.

### 5. [NOTE] Third agent file missed

`.claude/agents/reviewer-adversarial.md:42` references "the 8 universal
methodology invariants." Plan only updated two agent files.

**Resolution (applied to plan):** Added to T00 file scope and instructions.

### 6. [NOTE] Research log entry template lacks Invariant #9 annotation

The template that guides research log entry authoring did not reference
Invariant #9 or include a scope field.

**Resolution (applied to plan):** T01 now updates the research log entry
template with a `step_scope` field annotated with Invariant #9.

### 7. [NOTE] `coverage_notes` forward-references

The aoe2companion raw README `coverage_notes` field says "identified during
Phase 01 profiling" — a potential forward reference.

**Resolution (applied to plan):** Added to T02 strip list — strip
`coverage_notes` if it contains forward-references to unfinished steps.

### 8. [NOTE] Stale leak references in Context Leaks Identified table

Some leaks listed in the plan may reference text that has already been
cleaned or differs from current file state. Executors should verify current
state before stripping.

**Resolution:** T02 spec instructs executor to verify current state of each
file before stripping. Stale references are non-blocking — executor skips
text that no longer exists.

---

## Post-revision verdict

All 8 findings addressed in plan revision. **APPROVED FOR MATERIALIZATION.**
