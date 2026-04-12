---
category: "A"
branch: "feat/rerun-01-01-01"
date: "2026-04-12"
planner_model: "claude-opus-4-6"
---

# Category A Plan: Rerun Phase 01 Step 01_01_01 (File Inventory) -- Context Leak Cleanup

**Phase/Step:** Phase 01, Pipeline Section 01_01, Step 01_01_01
**Datasets:** sc2egset, aoe2companion, aoestats

## Scope

Codify a new scientific invariant (artifact-chain discipline), create a
dataset reports README template, strip all context leaks from existing
documents, rerun the 01_01_01 file inventory notebooks for all 3 datasets,
and repopulate all downstream documents strictly from artifacts.

## Problem Statement

The existing research log entries for 01_01_01 contain context leaks --
conclusions that require content-level knowledge that a file inventory
cannot produce. The same leaks propagated into ROADMAP source data sections,
raw/README.md files, and the root CROSS log. There is no general invariant
preventing these leaks, and the dataset-level `reports/README.md` files
lack a template -- creating a vector for future leaks.

A file inventory (01_01_01) should report ONLY filesystem-level observations:
- Directory tree structure (names, nesting)
- File counts per directory
- File extensions and types
- File sizes
- Date strings extracted from filenames (pattern-based, not content-based)
- Gaps in date sequences from filenames

It should NOT report:
- What the files contain (01_01_02 Schema Discovery)
- Whether data is "daily" or "weekly" (frequency interpretation)
- Whether a file is a "snapshot" (role interpretation)
- Whether the data is "structurally sound" (content analysis)
- What the files represent ("replays," "matches," "players") beyond literal
  extension/filename strings

## Context Leaks Identified

| Location | Leaks |
|----------|-------|
| sc2egset research_log.md | "structurally sound," "non-empty," "replay files," "tournament directories," "tournament coverage" |
| aoe2companion research_log.md | Interpretive phrasing beyond file-level scope |
| aoestats research_log.md | Same pattern |
| aoe2companion ROADMAP Source data | "Daily" (x2), "Single-file snapshot" (x2), populated file counts and date ranges |
| aoestats ROADMAP Source data | "Weekly" (x2), "Single-file snapshot," "documented download failure," populated file counts |
| sc2egset ROADMAP Source data | "~22,000 competitive 1v1 replays" (content-level claim) |
| sc2egset raw/README.md | "Per-replay JSON files" (x70), "tournament" as semantic label, `temporal_grain: per_game` |
| aoe2companion raw/README.md | "Daily match," "Daily rating," "Leaderboard snapshot," `temporal_grain: daily` |
| aoestats raw/README.md | "Weekly match," "Weekly player," "Overview JSON reference," `temporal_grain: weekly` |
| sc2egset reports/README.md | Does not exist -- no template |
| aoe2companion reports/README.md | Incomplete, no template conformance |
| aoestats reports/README.md | Incomplete, no template conformance |
| Root CROSS log | "structurally sound" |

## Pipeline Context

```
01_01_01: File Inventory
  Input:  raw/ directory
  Output: file tree, counts, types, sizes, filename-derived dates, gaps
  Scope:  filesystem-level only -- do not open files

01_01_02: Schema Discovery
  Input:  raw/ files (open and read headers/schemas)
  Output: column names, types, sample rows, format details
  Scope:  file-content-level -- do not analyze data semantics
```

Each step's research log entry reports ONLY what that step's artifacts
contain. No forward-referencing, no interpretive conclusions beyond scope.
This will be codified as Invariant #9.

## Pre-verified Facts

- `inventory_directory()` in `src/rts_predict/common/inventory.py` is
  confirmed filesystem-only: calls `glob()` and `stat()`, never opens files.
- Raw data is immutable; artifact numbers will not change on rerun.
- All 3 notebooks exist and have jupytext `.py` pairs.
- The existing invariants are numbered 1-8. Adding #9 requires updating
  three agent files that reference "8 invariants":
  - `.claude/agents/reviewer-deep.md:197`
  - `.claude/agents/planner-science.md:33`
  - `.claude/agents/reviewer-adversarial.md:42`
- sc2egset has no `reports/README.md`; the other two have unstructured ones.
- `docs/templates/raw_data_readme_template.yaml` exists (for raw/README.md).
  No equivalent exists for `reports/README.md`.

## Assumptions & Unknowns

- Raw data is immutable; artifact numbers will not change on rerun.
- `inventory_directory()` is filesystem-only (verified: glob + stat only).
- Existing notebooks execute without error (they ran successfully on
  2026-04-09; raw data has not changed since).
- Some context leaks listed in the plan may already have been cleaned in
  prior sessions. Executors verify current state before stripping.

## Literature Context

Not applicable — file inventory is a data management step, not a
methodology step. Invariant #9 (research pipeline discipline) is an
internal thesis methodology commitment analogous to Invariant #3 (temporal
discipline), which follows de Prado 2018 and Arlot & Celisse 2010 on
information leakage prevention.

## Open Questions

1. Should the 01_01_01 notebook markdown cells be audited for interpretive
   prose? Currently the plan scopes cleanup to downstream documents
   (research logs, ROADMAPs, READMEs), not the notebook itself.
2. The `coverage_notes` field in raw/READMEs may contain provenance claims
   from acquisition scripts. After stripping, should these be repopulated
   from acquisition provenance (external docs) or from artifacts?

## Execution Order Rationale

Context leaks must be stripped BEFORE notebooks rerun. If an executor reads
a ROADMAP containing "Daily" while writing a new research log entry, the
leak propagates. The correct order is:

1. **Prep:** codify invariant, create template, strip all leaks
2. **Rerun:** notebooks execute into a clean document context
3. **Populate:** new entries and README updates written from artifacts only
4. **Cross:** root log updated last

---

## Execution Steps

### T00 -- Codify Invariant #9 (research pipeline discipline)

**Objective:** Add a new scientific invariant and update stale count
references so all downstream executors see the rule in their read_scope.

**Instructions:**
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

**Verification:**
- Invariant #9 exists in `.claude/scientific-invariants.md`
- `grep -c "8 invariants\|8 universal" .claude/agents/reviewer-deep.md .claude/agents/planner-science.md .claude/agents/reviewer-adversarial.md`
  returns 0 for all three files

**File scope:**
- `.claude/scientific-invariants.md`
- `.claude/agents/reviewer-deep.md`
- `.claude/agents/planner-science.md`
- `.claude/agents/reviewer-adversarial.md`

---

### T01 -- Create dataset reports README template

**Objective:** Create `docs/templates/dataset_reports_readme_template.yaml`
so all `reports/README.md` files across datasets follow a consistent
structure with Invariant #9 annotations.

**Instructions:**
1. Read `docs/templates/raw_data_readme_template.yaml` for style reference.
2. Create `docs/templates/dataset_reports_readme_template.yaml` with these
   sections, each annotated with which step populates it:

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

3. Update `docs/templates/research_log_entry_template.yaml`:
   - Add a `step_scope` field after `dataset:` in the header fields:
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
   - Add Invariant #9 reference to the `findings` section notes:
     "Per Invariant #9, findings must not exceed the declared step_scope."

**Verification:**
- Template file exists at `docs/templates/dataset_reports_readme_template.yaml`
- Every section has a `# Source:` annotation
- Template references Invariant #9
- Research log entry template has `step_scope` field with Invariant #9 annotation

**File scope:**
- `docs/templates/dataset_reports_readme_template.yaml`
- `docs/templates/research_log_entry_template.yaml`

---

### T02 -- Strip context leaks from all datasets

**Objective:** Remove all interpretive content from research logs, ROADMAP
source data sections, reports/READMEs, and raw/READMEs across all 3 datasets.
This creates a clean context for the notebook reruns.

**Instructions:**

**Research logs (3 files):**
1. For each dataset's `reports/research_log.md`, delete the entire 01_01_01
   entry. Leave the file header and any other entries intact.

**ROADMAP source data sections (3 files):**
2. For each dataset's `reports/ROADMAP.md`, locate the "Source data" section.
3. Strip all populated file counts, date ranges, and interpretive labels
   from the summary table/prose. Replace with stubs:
   - sc2egset: remove "~22,000 competitive 1v1 replays from 70+ tournaments
     covering 2016-2024." Replace with: "File counts and layout from
     Step 01_01_01 artifacts (to be repopulated after rerun)."
   - aoe2companion: remove the table with "Daily," "Single-file snapshot,"
     file counts, sizes. Replace with same stub.
   - aoestats: remove the table with "Weekly," "Single-file snapshot," file
     counts, WARNING block. Replace with same stub.
4. Keep the citation/DOI (sc2egset), source name, acquisition date, and
   any external documentation unchanged.

**reports/READMEs (3 files -- create sc2egset):**
5. Create `src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md`
   from the template (T01). Populate Section B (Acquisition) from external
   documentation. Leave Sections C-D as stubs.
6. Rewrite `aoe2companion/reports/README.md` to conform to template. Keep
   Section B populated, stub Section C (file inventory), keep Section D
   (known issues) as filesystem-level facts only, keep Section E.
7. Rewrite `aoestats/reports/README.md` to conform to template. Same rules.
   The known download failure should be restated as a filesystem fact:
   "171 files in `players/` vs 172 in `matches/`."

**raw/READMEs (3 files):**
8. For each dataset's `data/raw/README.md`:
   - Strip the `description` field in Section C — remove interpretive labels
     like "daily match parquet files," "leaderboard and profile snapshots,"
     "weekly match and player parquet files," "tournament replay files."
     Replace with stub: `# to be repopulated from 01_01_01 artifacts`
   - Strip `temporal_grain` value — replace with stub:
     `# to be populated from 01_01_01 artifact date_analysis`
   - Strip interpretive labels from `contents:` fields in
     `subdirectory_layout` entries (e.g., "Daily match parquet files" ->
     stub or pattern-only description)
   - Strip interpretive labels from the markdown body tables
   - Strip `coverage_notes` if it contains forward-references to steps
     not yet completed (e.g., "identified during Phase 01 profiling")
   - Keep Sections B (Provenance), E (Acquisition Filtering),
     H (Known Limitations) unchanged
   - Mark stripped fields with `# to be repopulated from 01_01_01 artifacts`

**Verification:**
- `grep -riE "daily|weekly|snapshot|structurally sound|per.game" --include="*.md"`
  across all 3 datasets' reports/ and data/raw/ dirs returns zero matches
  (excluding ROADMAP step definition yaml blocks and quoted filenames)
- sc2egset `reports/README.md` exists and follows template
- All 3 `reports/README.md` files have consistent structure

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md` (create)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/raw/README.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md`

**Read scope:**
- `docs/templates/dataset_reports_readme_template.yaml` (from T01)
- `docs/templates/raw_data_readme_template.yaml`
- `.claude/scientific-invariants.md`

---

### T03 -- Rerun sc2egset 01_01_01

**Objective:** Rerun the file inventory notebook into a clean context,
write a new research log entry from artifacts only.

**Instructions:**
1. Read the notebook at
   `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`.
2. Verify the notebook calls `inventory_directory()` and writes artifacts to:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
3. Run fresh-kernel execution:
   `source .venv/bin/activate && poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
4. Sync jupytext:
   `source .venv/bin/activate && poetry run jupytext --sync sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
5. Read the produced artifacts (JSON + MD).
6. Write a new research log entry using
   `docs/templates/research_log_entry_template.yaml`. Strict rules:
   - Report: directory tree, file counts per directory, extensions, sizes,
     filename-derived date ranges, gaps
   - Do NOT interpret directory names as data semantics
   - Do NOT use words like "daily," "weekly," "snapshot," "structurally sound,"
     "replay," "tournament" (as semantic labels) unless they appear literally
     in artifact output as filenames/extensions
   - `matches/`, `_data/` etc. are directory names -- quote them as such,
     not as data claims
   - Per Invariant #9: conclusions derive from artifacts only
7. Verify `.ipynb` and `.py` pair are synced.

**Verification:**
- Artifacts exist and are current (timestamp matches notebook execution)
- Research log entry contains only file-level observations
- `grep -iE "daily|weekly|snapshot|structurally sound" research_log.md`
  returns zero matches outside of directory name contexts
- `.ipynb` and `.py` pair synced

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/`

**Read scope:**
- `.claude/scientific-invariants.md`
- `docs/templates/research_log_entry_template.yaml`

---

### T04 -- Rerun aoe2companion 01_01_01

**Objective:** Same as T03 for aoe2companion.

**Instructions:** Same pattern as T03. Target paths:
- Notebook: `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- Artifacts: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/`
- Research log: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`

Same strict scoping rules and Invariant #9 constraint.

**Verification:** Same as T03 adapted to aoe2companion paths.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.py`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/`

**Read scope:**
- `.claude/scientific-invariants.md`
- `docs/templates/research_log_entry_template.yaml`

---

### T05 -- Rerun aoestats 01_01_01

**Objective:** Same as T03 for aoestats.

**Instructions:** Same pattern as T03. Target paths:
- Notebook: `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- Artifacts: `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/`
- Research log: `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`

Same strict scoping rules and Invariant #9 constraint.

**Verification:** Same as T03 adapted to aoestats paths.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb`
- `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/`

**Read scope:**
- `.claude/scientific-invariants.md`
- `docs/templates/research_log_entry_template.yaml`

---

### T06 -- Populate sc2egset docs from artifacts

**Objective:** Repopulate the sc2egset ROADMAP source data section,
raw/README.md, and reports/README.md strictly from fresh 01_01_01 artifacts.

**Instructions:**
1. Read the fresh artifacts (JSON + MD) from T03.
2. Update ROADMAP source data section: repopulate file counts, sizes,
   directory structure from artifacts. Use filesystem-level language only.
   No "replay," "tournament" as semantic labels -- use directory names
   and file extensions.
3. Update raw/README.md: repopulate `subdirectory_layout` entries,
   `total_files`, `total_size_mb`, `description`, and `contents:` fields
   from artifacts. Populate `temporal_grain` from artifact `date_analysis`
   (filename-derived cadence is filesystem-level). Use pattern-based
   descriptions for `contents:` fields (e.g., "`.SC2Replay.json` files").
4. Update reports/README.md: populate Section C (file inventory) from
   artifacts. Must conform to `docs/templates/dataset_reports_readme_template.yaml`.
5. Per Invariant #9: every stated fact must trace to the 01_01_01 artifact.

**Verification:**
- No interpretive labels in any of the 3 files
- reports/README.md conforms to template
- All numbers match 01_01_01 artifact values

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (Source data section)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/raw/README.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
- `docs/templates/dataset_reports_readme_template.yaml`

---

### T07 -- Populate aoe2companion docs from artifacts

**Objective:** Same as T06 for aoe2companion.

**Instructions:** Same pattern as T06. Target paths:
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
- raw/README.md: `src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md`
- reports/README.md: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md`

**Verification:** Same as T06 adapted to aoe2companion paths.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (Source data section)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
- `docs/templates/dataset_reports_readme_template.yaml`

---

### T08 -- Populate aoestats docs from artifacts

**Objective:** Same as T06 for aoestats.

**Instructions:** Same pattern as T06. Target paths:
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md`
- raw/README.md: `src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md`
- reports/README.md: `src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md`

**Verification:** Same as T06 adapted to aoestats paths.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` (Source data section)
- `src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
- `docs/templates/dataset_reports_readme_template.yaml`

---

### T09 -- Update root CROSS log

**Objective:** Replace the interpretive CROSS summary with a factual one.

**Instructions:**
1. Read `reports/research_log.md`.
2. Find the CROSS summary for 01_01_01 (line ~64).
3. Replace with factual content only:
   "Step 01_01_01 file inventory rerun completed for all 3 datasets.
   Context leaks stripped, research log entries rewritten from artifacts.
   ROADMAP source data sections, raw/README.md, and reports/README.md
   repopulated strictly from 01_01_01 artifacts per Invariant #9.
   Per-dataset findings in each dataset's research_log.md."
4. Do NOT include any cross-dataset comparisons or interpretive claims.

**Verification:**
- Root CROSS log has factual 01_01_01 summary
- `grep -iE "structurally sound|non-empty|daily|weekly" reports/research_log.md`
  in the 01_01_01 section returns zero matches

**File scope:** `reports/research_log.md`
**Read scope:** none (T03-T08 must complete first)

---

## File Manifest

| File | Action | Task |
|------|--------|------|
| `.claude/scientific-invariants.md` | Add Invariant #9 | T00 |
| `.claude/agents/reviewer-deep.md` | "8 invariants" -> "9 invariants" | T00 |
| `.claude/agents/planner-science.md` | "8 invariants" -> "9 invariants" | T00 |
| `.claude/agents/reviewer-adversarial.md` | "8 universal" -> "9 universal" | T00 |
| `docs/templates/dataset_reports_readme_template.yaml` | Create | T01 |
| `docs/templates/research_log_entry_template.yaml` | Add step_scope field | T01 |
| `src/.../sc2egset/reports/research_log.md` | Delete 01_01_01 entry | T02 |
| `src/.../aoe2companion/reports/research_log.md` | Delete 01_01_01 entry | T02 |
| `src/.../aoestats/reports/research_log.md` | Delete 01_01_01 entry | T02 |
| `src/.../sc2egset/reports/ROADMAP.md` | Strip source data | T02, T06 |
| `src/.../aoe2companion/reports/ROADMAP.md` | Strip source data | T02, T07 |
| `src/.../aoestats/reports/ROADMAP.md` | Strip source data | T02, T08 |
| `src/.../sc2egset/reports/README.md` | Create from template | T02, T06 |
| `src/.../aoe2companion/reports/README.md` | Conform to template | T02, T07 |
| `src/.../aoestats/reports/README.md` | Conform to template | T02, T08 |
| `src/.../sc2egset/data/raw/README.md` | Strip + repopulate | T02, T06 |
| `src/.../aoe2companion/data/raw/README.md` | Strip + repopulate | T02, T07 |
| `src/.../aoestats/data/raw/README.md` | Strip + repopulate | T02, T08 |
| `sandbox/.../sc2egset/.../01_01_01_file_inventory.ipynb` | Rerun | T03 |
| `sandbox/.../sc2egset/.../01_01_01_file_inventory.py` | Sync | T03 |
| `sandbox/.../aoe2companion/.../01_01_01_file_inventory.ipynb` | Rerun | T04 |
| `sandbox/.../aoe2companion/.../01_01_01_file_inventory.py` | Sync | T04 |
| `sandbox/.../aoestats/.../01_01_01_file_inventory.ipynb` | Rerun | T05 |
| `sandbox/.../aoestats/.../01_01_01_file_inventory.py` | Sync | T05 |
| `src/.../sc2egset/reports/artifacts/.../01_01_01_file_inventory.json` | Regenerate | T03 |
| `src/.../sc2egset/reports/artifacts/.../01_01_01_file_inventory.md` | Regenerate | T03 |
| `src/.../aoe2companion/reports/artifacts/.../01_01_01_file_inventory.json` | Regenerate | T04 |
| `src/.../aoe2companion/reports/artifacts/.../01_01_01_file_inventory.md` | Regenerate | T04 |
| `src/.../aoestats/reports/artifacts/.../01_01_01_file_inventory.json` | Regenerate | T05 |
| `src/.../aoestats/reports/artifacts/.../01_01_01_file_inventory.md` | Regenerate | T05 |
| `reports/research_log.md` | Update CROSS summary | T09 |

## Gate Condition

- Invariant #9 exists in `.claude/scientific-invariants.md`
- `docs/templates/dataset_reports_readme_template.yaml` exists
- "8 invariants" count references updated in all three agent files
- 3 notebooks executed fresh-kernel without error
- 6 artifact files exist (JSON + MD per dataset) with current timestamps
- 3 per-dataset research log entries contain ONLY file-level observations
- 3 ROADMAP source data sections repopulated without interpretive labels
- 3 raw/README.md files repopulated from artifacts, no interpretive labels
- 3 reports/README.md files exist and conform to template
- Machine check: `grep -riE "snapshot|structurally sound|non.empty|per.game"`
  across all modified files returns zero matches (excluding ROADMAP step
  definition yaml blocks). Note: "daily" and "weekly" are NOW permitted in
  `temporal_grain` and date_analysis-derived fields (filesystem-level from
  artifact). The regex excludes these as they are artifact-populated values.
  Separately check that "daily|weekly" do NOT appear as semantic labels
  for file roles (e.g., "daily match files" is banned; `temporal_grain:
  daily` is allowed).
- Root CROSS log has factual summary (no interpretive claims)
- STEP_STATUS.yaml still shows 01_01_01 as complete for all 3 datasets
- `.ipynb` / `.py` pairs synced for all 3 notebooks

## Design Decisions

1. **Cleanup before rerun.** Context leaks are stripped (T02) before
   notebooks execute (T03-T05). This prevents executors from reading
   leaked content while writing new entries.

2. **Adversarial critique required.** This plan introduces Invariant #9,
   a permanent methodology commitment. The invariant text must be
   stress-tested before codification.

3. **Final reviewer is `reviewer-adversarial`.** Category A with a new
   invariant warrants adversarial final review.

4. **reports/README.md template created.** Without a template, future
   steps would populate unstructured fields with interpretive content --
   the same context leak vector this plan eliminates.

5. **ROADMAP step definitions (yaml blocks) untouched.** They describe
   *what to do*, not *what was found*.

6. **raw/README.md provenance sections (B, E, H) untouched.** Those come
   from external documentation, not from 01_01_01 findings.

7. **`temporal_grain` populated from artifact date_analysis.** Filename-
   derived date cadence (e.g., consecutive dates = daily, 7-day ranges =
   weekly) is a filesystem-level observation — the notebook extracts dates
   from filenames without opening files. The artifact's `date_analysis`
   section is the source of truth for this field.

---

## Suggested Execution Graph

```yaml
dag_id: "dag_rerun_01_01_01"
plan_ref: "planning/current_plan.md"
category: "A"
branch: "feat/rerun-01-01-01"
base_ref: "master"
default_isolation: "shared_branch"

jobs:
  - job_id: "J00_prep"
    name: "Preparation -- invariant, template, cleanup"
    task_groups:
      - group_id: "TG00_methodology"
        name: "Codify Invariant #9 + create template"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T00"
            name: "Codify Invariant #9"
            spec_file: "planning/specs/spec_00_invariant9.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - ".claude/scientific-invariants.md"
              - ".claude/agents/reviewer-deep.md"
              - ".claude/agents/planner-science.md"
              - ".claude/agents/reviewer-adversarial.md"
            read_scope: []
            depends_on: []
          - task_id: "T01"
            name: "Create reports README template + update research log template"
            spec_file: "planning/specs/spec_01_templates.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "docs/templates/dataset_reports_readme_template.yaml"
              - "docs/templates/research_log_entry_template.yaml"
            read_scope:
              - "docs/templates/raw_data_readme_template.yaml"
            depends_on: []

      - group_id: "TG01_cleanup"
        name: "Strip all context leaks"
        depends_on: ["TG00_methodology"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T02"
            name: "Strip context leaks from all datasets"
            spec_file: "planning/specs/spec_02_strip_leaks.md"
            agent: "executor"
            parallel_safe: false
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
            depends_on: []

  - job_id: "J01_sc2"
    name: "01_01_01 -- sc2egset"
    depends_on: ["J00_prep"]
    task_groups:
      - group_id: "TG01_sc2"
        name: "Rerun sc2 notebook + research log"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T03"
            name: "Rerun notebook + write research log"
            spec_file: "planning/specs/spec_03_sc2_rerun.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb"
              - "sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py"
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/"
            read_scope:
              - ".claude/scientific-invariants.md"
              - "docs/templates/research_log_entry_template.yaml"
            depends_on: []

      - group_id: "TG02_sc2"
        name: "Populate sc2 docs from artifacts"
        depends_on: ["TG01_sc2"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T06"
            name: "Populate ROADMAP + raw/README + reports/README"
            spec_file: "planning/specs/spec_06_sc2_populate.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
              - "src/rts_predict/games/sc2/datasets/sc2egset/data/raw/README.md"
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/README.md"
            read_scope:
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
              - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
              - "docs/templates/dataset_reports_readme_template.yaml"
            depends_on: []

  - job_id: "J02_aoe2c"
    name: "01_01_01 -- aoe2companion"
    depends_on: ["J00_prep"]
    task_groups:
      - group_id: "TG01_aoe2c"
        name: "Rerun aoe2companion notebook + research log"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T04"
            name: "Rerun notebook + write research log"
            spec_file: "planning/specs/spec_04_aoe2c_rerun.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb"
              - "sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.py"
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md"
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/"
            read_scope:
              - ".claude/scientific-invariants.md"
              - "docs/templates/research_log_entry_template.yaml"
            depends_on: []

      - group_id: "TG02_aoe2c"
        name: "Populate aoe2companion docs from artifacts"
        depends_on: ["TG01_aoe2c"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T07"
            name: "Populate ROADMAP + raw/README + reports/README"
            spec_file: "planning/specs/spec_07_aoe2c_populate.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md"
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/raw/README.md"
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/README.md"
            read_scope:
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
              - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
              - "docs/templates/dataset_reports_readme_template.yaml"
            depends_on: []

  - job_id: "J03_aoestats"
    name: "01_01_01 -- aoestats"
    depends_on: ["J00_prep"]
    task_groups:
      - group_id: "TG01_aoestats"
        name: "Rerun aoestats notebook + research log"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T05"
            name: "Rerun notebook + write research log"
            spec_file: "planning/specs/spec_05_aoestats_rerun.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.ipynb"
              - "sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py"
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md"
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/"
            read_scope:
              - ".claude/scientific-invariants.md"
              - "docs/templates/research_log_entry_template.yaml"
            depends_on: []

      - group_id: "TG02_aoestats"
        name: "Populate aoestats docs from artifacts"
        depends_on: ["TG01_aoestats"]
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T08"
            name: "Populate ROADMAP + raw/README + reports/README"
            spec_file: "planning/specs/spec_08_aoestats_populate.md"
            agent: "executor"
            parallel_safe: true
            file_scope:
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md"
              - "src/rts_predict/games/aoe2/datasets/aoestats/data/raw/README.md"
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/README.md"
            read_scope:
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"
              - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
              - "docs/templates/dataset_reports_readme_template.yaml"
            depends_on: []

  - job_id: "J04_cross"
    name: "01_01_01 -- CROSS log update"
    depends_on: ["J01_sc2", "J02_aoe2c", "J03_aoestats"]
    task_groups:
      - group_id: "TG01_cross"
        name: "Update root CROSS log"
        depends_on: []
        review_gate:
          agent: "reviewer"
          scope: "diff"
          on_blocker: "halt"
        tasks:
          - task_id: "T09"
            name: "Update CROSS log summary"
            spec_file: "planning/specs/spec_09_cross_log.md"
            agent: "executor"
            parallel_safe: false
            file_scope:
              - "reports/research_log.md"
            read_scope: []
            depends_on: []

final_review:
  agent: "reviewer-adversarial"
  scope: "all"
  base_ref: "master"
  on_blocker: "halt"

failure_policy:
  on_failure: "halt"
```

## Dependency Graph

```
J00_prep:
  TG00: T00 (Invariant #9) + T01 (template)  [parallel]
    |
  TG01: T02 (strip all leaks)
    |
    +---> J01_sc2:  T03 (rerun) -> T06 (populate) ----+
    |                                                   |
    +---> J02_aoe2c: T04 (rerun) -> T07 (populate) ---+-> J04_cross: T09
    |                                                   |
    +---> J03_aoestats: T05 (rerun) -> T08 (populate) +
```
