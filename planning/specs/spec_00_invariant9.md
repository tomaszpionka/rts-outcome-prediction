---
task_id: "T00"
task_name: "Codify Invariant #9"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG00_methodology"
file_scope:
  - ".claude/scientific-invariants.md"
  - ".claude/agents/reviewer-deep.md"
  - ".claude/agents/planner-science.md"
  - ".claude/agents/reviewer-adversarial.md"
read_scope: []
category: "A"
---

# Spec: Codify Invariant #9

## Objective

Add Scientific Invariant #9 (research pipeline discipline) to the invariants
file and update all agent files that reference the invariant count.

## Instructions

1. Read `.claude/scientific-invariants.md`.
2. Add a new section after `### Cross-game comparability` (Invariant #8)
   and before `## Per-dataset findings`:

   ```markdown
   ### Research pipeline discipline

   9. **A step's conclusions must derive only from its own artifacts and all
      prior steps' artifacts.** Step XX_YY_ZZ may reference:
      - Artifacts it produces during its own execution
      - Artifacts produced by any completed predecessor step (any step with a
        lower number whose artifacts exist on disk)
      - External source documentation (paper citations, acquisition provenance,
        Zenodo metadata)

      It must NOT reference:
      - Knowledge that would be produced by a future step
      - Implicit domain knowledge not grounded in an existing artifact
      - Content-level understanding of data not yet established by a completed
        step's artifact

      This applies to all downstream documents that inherit from a step's
      findings: research log entries, ROADMAP source data summaries, and
      raw/README.md files. If a document states a fact derived from the data,
      the artifact that established that fact must already exist on disk.

      **External source documentation** means information traceable to a
      specific sentence in a cited publication, API documentation page, or
      dataset metadata record. Use exact source titles and descriptions
      (e.g., "SC2EGSet: StarCraft II Esport Replay and Game-state Dataset")
      rather than paraphrased interpretive labels (e.g., "tournament replay
      files"). Exact citations are deferred to thesis chapters; in pipeline
      documents, use the source's own title verbatim.

      **Example:** Step 01_01_01 (file inventory) sees filenames and sizes. It
      cannot call files "daily match dumps" because "daily" and "match" are
      content-level conclusions -- "daily" requires confirming filename-date
      patterns against actual content cadence (01_01_02+), and "match" requires
      reading file schemas (01_01_02). It can report: "2,073 `.parquet` files
      in `matches/` named `match-{YYYY-MM-DD}.parquet`."

      See Invariant #3 for the analogous rule applied to feature computation.
   ```
3. Update `.claude/agents/reviewer-deep.md` line 197:
   "For each of the 8 invariants" -> "For each of the 9 invariants"
4. Update `.claude/agents/planner-science.md` line 33:
   "against the 8 invariants" -> "against the 9 invariants"
5. Update `.claude/agents/reviewer-adversarial.md` line 42:
   "the 8 universal methodology invariants" -> "the 9 universal methodology invariants"

## Verification

- Invariant #9 exists in `.claude/scientific-invariants.md`
- `grep -c "8 invariants\|8 universal" .claude/agents/reviewer-deep.md .claude/agents/planner-science.md .claude/agents/reviewer-adversarial.md`
  returns 0 for all three files

## Context

- This invariant is the generalized form of the context leak problem
  identified in the 01_01_01 research log entries.
- Analogous to Invariant #3 (temporal discipline for features) but applied
  to the research pipeline itself.
