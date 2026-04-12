---
task_id: "T01"
task_name: "Create reports README template + update research log template"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG00_methodology"
file_scope:
  - "docs/templates/dataset_reports_readme_template.yaml"
  - "docs/templates/research_log_entry_template.yaml"
read_scope:
  - "docs/templates/raw_data_readme_template.yaml"
category: "A"
---

# Spec: Create reports README template + update research log template

## Objective

Create a new template for dataset-level `reports/README.md` files with
Invariant #9 annotations, and add a `step_scope` field to the research log
entry template so step scope is enforceable on all future entries.

## Instructions

### Part A: Create `docs/templates/dataset_reports_readme_template.yaml`

1. Read `docs/templates/raw_data_readme_template.yaml` for style reference.
2. Create the template with these sections, each annotated with which step
   or source populates it:

   ```yaml
   # Dataset Reports README Template (v1)
   #
   # Canonical schema for reports/README.md files across all datasets:
   #   src/rts_predict/games/<game>/datasets/<dataset>/reports/README.md
   #
   # Purpose: permanent provenance record for the dataset. Independent of
   # the phase system -- not archived when phases are reset.
   #
   # Invariant #9 compliance: each field is annotated with the step or
   # source that populates it. A field MUST NOT be populated until that
   # step's artifacts exist on disk.
   #
   # Authoritative sources:
   #   Scientific Invariants  .claude/scientific-invariants.md
   #   Raw Data Template      docs/templates/raw_data_readme_template.yaml
   #   Phase definitions      docs/PHASES.md

   # -- Section A: Identity -----------------------------------------------

   game:          # <sc2 | aoe2>
   dataset:       # <dataset_name>
   reports_dir:   # <repo-relative path to this reports/ directory>

   # -- Section B: Acquisition provenance ----------------------------------
   # Source: acquisition script execution (pre-Phase 01)

   acquisition:
     date:         # <YYYY-MM-DD>
     script:       # <CLI command or "manual download">
     branch:       # <branch name where acquisition was committed>
     source:       # <source name>
     source_url:   # <URL>
     method:       # <cdn_download | api_download | manual_download>

   # -- Section C: File inventory summary ----------------------------------
   # Source: Step 01_01_01 artifact
   # Invariant #9: MUST NOT contain interpretive labels (daily, weekly,
   # snapshot, replay, match, etc.). Report file counts, sizes, extensions,
   # and filename patterns only.

   file_inventory:
     total_files:    # <integer from 01_01_01 artifact, excluding dotfiles>
     total_size_mb:  # <number from 01_01_01 artifact>
     subdirectories: # <count of subdirectories>
     artifact_ref:   # <repo-relative path to 01_01_01_file_inventory.json>

   # -- Section D: Known issues --------------------------------------------
   # Source: acquisition script logs or 01_01_01 artifact
   # Report filesystem-level facts only. Do NOT interpret cause or meaning.
   # Example: "171 files in players/ vs 172 in matches/" (fact)
   # Not: "documented download failure" (provenance claim beyond filesystem)

   known_issues: []

   # -- Section E: Reconciliation ------------------------------------------
   # Source: acquisition script verification

   reconciliation:
     strength:   # <FULL | DEGRADED | NONE>
     reason:     # <one-line explanation>

   # -- Section F: Provenance rule -----------------------------------------

   provenance_rule: >
     Raw data is immutable. The acquisition will not be repeated.
   ```

### Part B: Update `docs/templates/research_log_entry_template.yaml`

3. Read `docs/templates/research_log_entry_template.yaml`.
4. Add a `step_scope` field after `dataset:` in the header fields section:

   ```yaml
   step_scope:
     format: "**Step scope:** filesystem | content | query | model"
     required: true
     condition: "Required for Category A entries."
     notes: >
       Per Invariant #9, a step's conclusions must derive only from its own
       artifacts and all prior steps' artifacts. The step_scope field declares
       what level of observation this step operates at, so reviewers can
       verify that findings do not exceed scope. Values:
       - filesystem: file tree, counts, sizes, filename patterns (01_01_01)
       - content: file headers, schemas, sample rows (01_01_02)
       - query: DuckDB queries on ingested data (01_01_03+)
       - model: feature engineering, model training (Phase 02+)
   ```

5. Add Invariant #9 reference to the `findings` section notes:
   "Per Invariant #9, findings must not exceed the declared step_scope."

## Verification

- `docs/templates/dataset_reports_readme_template.yaml` exists
- Every section has a `# Source:` annotation
- Template references Invariant #9
- `docs/templates/research_log_entry_template.yaml` has `step_scope` field
  with Invariant #9 annotation

## Context

- `docs/templates/raw_data_readme_template.yaml` is the style reference
- The reports README template prevents future context leaks in
  `reports/README.md` files by annotating which step populates each field
- The step_scope field in the research log template enforces Invariant #9
  at the template level
