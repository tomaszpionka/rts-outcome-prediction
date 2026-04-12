---
task_id: "T02"
task_name: "Strip context leaks from all datasets"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01_cleanup"
file_scope:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/raw/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md"
read_scope:
  - "docs/templates/dataset_reports_readme_template.yaml"
  - "docs/templates/raw_data_readme_template.yaml"
  - ".claude/scientific-invariants.md"
category: "A"
---

# Spec: Strip context leaks from all datasets

## Objective

Remove all interpretive content from research logs, ROADMAP source data
sections, reports/READMEs, and raw/READMEs across all 3 datasets. This
creates a clean context for the notebook reruns in T03-T05.

## Instructions

**Important:** Before stripping, verify the current state of each file.
Some leaks listed below may already have been cleaned in prior sessions.
Skip text that no longer exists -- do not fail on phantom references.

### Research logs (3 files)

1. For each dataset's `reports/research_log.md`, delete the entire 01_01_01
   entry. Leave the file header and any other entries intact.

### ROADMAP source data sections (3 files)

2. For each dataset's `reports/ROADMAP.md`, locate the "Source data" section.
3. Strip all populated file counts, date ranges, and interpretive labels
   from the summary table/prose. Replace with stubs:
   - sc2egset: remove content-level claims. Replace populated data with:
     "File counts and layout from Step 01_01_01 artifacts (to be
     repopulated after rerun)."
   - aoe2companion: remove the table with "Daily," "Single-file snapshot,"
     file counts, sizes. Replace with same stub.
   - aoestats: remove the table with "Weekly," "Single-file snapshot," file
     counts, WARNING block. Replace with same stub.
4. Keep the citation/DOI (sc2egset), source name, acquisition date, and
   any external documentation unchanged. Use exact source titles verbatim
   (per Invariant #9 external documentation boundary).

### reports/READMEs (3 files -- create sc2egset)

5. Create `src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md`
   from `docs/templates/dataset_reports_readme_template.yaml`. Populate
   Section B (Acquisition) from external documentation. Leave Sections C-D
   as stubs.
6. Rewrite `aoe2companion/reports/README.md` to conform to template. Keep
   Section B populated, stub Section C (file inventory), keep Section D
   (known issues) as filesystem-level facts only, keep Section E.
7. Rewrite `aoestats/reports/README.md` to conform to template. Same rules.
   The known download failure should be restated as a filesystem fact:
   "171 files in `players/` vs 172 in `matches/`."

### raw/READMEs (3 files)

8. For each dataset's `data/raw/README.md`:
   - Strip the `description` field in Section C -- remove interpretive
     labels like "daily match parquet files," "leaderboard and profile
     snapshots," "weekly match and player parquet files," "tournament replay
     files." Replace with stub:
     `# to be repopulated from 01_01_01 artifacts`
   - Strip `temporal_grain` value -- replace with stub:
     `# to be populated from 01_01_01 artifact date_analysis`
   - Strip interpretive labels from `contents:` fields in
     `subdirectory_layout` entries (e.g., "Daily match parquet files" ->
     stub or pattern-only description)
   - Strip interpretive labels from the markdown body tables
   - Strip `coverage_notes` if it contains forward-references to steps not
     yet completed (e.g., "identified during Phase 01 profiling")
   - Keep Sections B (Provenance), E (Acquisition Filtering),
     H (Known Limitations) unchanged
   - Mark stripped fields with `# to be repopulated from 01_01_01 artifacts`

## Verification

- `grep -riE "snapshot|structurally sound|non.empty|per.game" --include="*.md"`
  across all 3 datasets' `reports/` and `data/raw/` dirs returns zero matches
  (excluding ROADMAP step definition yaml blocks)
- Separately verify "daily" and "weekly" do NOT appear as semantic role
  labels (e.g., "daily match files" is banned; `temporal_grain` stubs are OK)
- sc2egset `reports/README.md` exists and follows template
- All 3 `reports/README.md` files have consistent structure

## Context

- Per Invariant #9: all downstream documents must be clean before notebooks
  rerun to prevent context leak propagation
- `docs/templates/dataset_reports_readme_template.yaml` defines the target
  structure for reports/READMEs
- Stubs will be repopulated from fresh artifacts in T06-T08
