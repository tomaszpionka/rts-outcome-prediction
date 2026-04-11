# Category C Plan: Template Hierarchy Restructuring

**Category:** C (chore)
**Branch:** `chore/template-hierarchy`
**Date:** 2026-04-11

---

## Scope

Fill four empty template YAMLs, create three new status template YAMLs, enhance
three existing status files per dataset, retract premature dataset strategy
commitments in AoE2 ROADMAPs, and update cross-cutting references.
Total: 5 new files, 4 populated-from-empty files, 13 modified files.

## Prerequisite observation

The project has a well-defined three-level hierarchy (Phase > Pipeline Section >
Step) documented in `docs/TAXONOMY.md` and `docs/PHASES.md`. The template system
currently has complete schemas only at the leaf level (`step_template.yaml`,
`research_log_entry_template.yaml`). The Phase and Pipeline Section levels have
empty placeholders. Status tracking files exist but lack the upward linking
fields needed to derive Pipeline Section and Phase status from Step status.

The derivation direction is: Steps are authoritative, Pipeline Section status is
derived from Steps, Phase status is derived from Pipeline Sections. This matches
the existing STEP_STATUS.yaml comment: "Phase is complete when ALL its steps are
complete."

**Premature dataset strategy retraction.** The AoE2 game-level ROADMAP and both
AoE2 dataset ROADMAPs contain premature methodological commitments — PRIMARY /
SUPPLEMENTARY VALIDATION role assignments, Phase 06 exclusion for aoestats, and
"lightweight Phase 02-05 replication pass" scope restrictions — made when only
Step 01_01_01 (File Inventory) was complete. These decisions require Phase 01
Decision Gate (01_06) evidence: schema completeness, null rates, player identity
coverage, temporal density. Per `docs/PHASES.md` lines 53-57: "Whether
generalisation holds is itself a finding produced by Phase 01 and Phase 02 — not
an assumption baked into the Phase structure." Per lines 262-265: all dataset
ROADMAPs implement Phases 01-07. The premature commitments are retracted as part
of this chore and replaced with provisional language.

---

## Execution steps

### Step 0: Retract premature AoE2 dataset strategy commitments

**Purpose:** Remove unfounded methodological commitments from AoE2 ROADMAPs
before creating templates and status files that would propagate them.

**0a. `src/rts_predict/aoe2/reports/ROADMAP.md` — rewrite Dataset Strategy**

Replace the current "Dataset Strategy" section (lines 21-41) with provisional
language:

```markdown
## Dataset Strategy (provisional — to be confirmed by Phase 01 Decision Gates)

**Planning indicators (2026-04-11, based on file inventory only — not verified
Phase 01 findings):**

1. aoe2companion has more files (4,154 vs 349) and spans a longer date range
   (2020-2026 vs 2022-2026) based on file inventory.
2. aoe2companion files have daily granularity; aoestats files have weekly
   granularity.
3. Pre-Phase-01 DuckDB ingestion suggests ~277M vs ~30.7M rows — these counts
   are unverified planning context (see provenance caveats in each dataset
   ROADMAP).

**Status:** Role assignment (PRIMARY vs SUPPLEMENTARY VALIDATION) requires
Phase 01 Decision Gate (01_06) evidence: schema completeness, null rates,
player identity coverage, temporal density. Until then, both datasets run
full Phases 01-07 independently with no scope restrictions.

**Decision point:** Pipeline Section 01_06 (Decision Gates) for each dataset
will produce the comparative evidence needed to formalize roles. The decision
will be recorded in `reports/research_log.md` with full derivation per
Invariant 6.
```

**0b. `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md` — remove role banner**

Replace the "Role: SUPPLEMENTARY VALIDATION" blockquote (lines 11-13) with:

```markdown
> **Role: TO BE DETERMINED.** Role assignment (PRIMARY vs SUPPLEMENTARY
> VALIDATION) will be formalized at the Phase 01 Decision Gate (01_06) based
> on comparative data quality findings. Until then, this dataset runs all
> Phases at full scope per `docs/PHASES.md`.
```

**0c. `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md` — remove role banner**

Replace the "Role: PRIMARY" blockquote (lines 11-12) with:

```markdown
> **Role: TO BE DETERMINED.** Role assignment (PRIMARY vs SUPPLEMENTARY
> VALIDATION) will be formalized at the Phase 01 Decision Gate (01_06) based
> on comparative data quality findings. Until then, this dataset runs all
> Phases at full scope per `docs/PHASES.md`.
```

**0d. `reports/research_log.md` — update the dataset strategy decision entry**

The existing "AoE2 Dataset Strategy Decision" entry (2026-04-11) must be
amended. Add a "### Retraction" section at the bottom of the entry:

```markdown
### Retraction (2026-04-11)

The PRIMARY / SUPPLEMENTARY VALIDATION role assignments and the aoestats Phase
06 exclusion are retracted. These commitments were made before Phase 01 EDA and
rely on unverified row counts and structural observations (file granularity)
rather than schema completeness, null rates, or feature availability — evidence
that Phase 01 Steps 01_02 through 01_06 are designed to produce. Per
docs/PHASES.md, whether generalisation holds between datasets is a Phase 01/02
finding, not a prior assumption. Both datasets now run full Phases 01-07
independently. Role assignment is deferred to Pipeline Section 01_06 (Decision
Gates).
```

---

### Step 1: Create `docs/templates/phase_template.yaml`

**Purpose:** Template for how a Phase appears in a dataset ROADMAP.md. This is
not a status file template — it is the ROADMAP authoring template (the Phase
block that a ROADMAP author copies when adding a new Phase to a dataset ROADMAP).

**Fields (using `value:` + `required:` pattern):**

```yaml
# -- Identity --
phase_number:
  value: "<NN>"           # Two-digit zero-padded
  required: true

name:
  value: "<phase name from docs/PHASES.md>"
  required: true

# -- Source --
source_manual:
  value: "<docs/ml_experiment_lifecycle/NN_MANUAL_NAME.md>"
  required: true

canonical_reference:
  value: "docs/PHASES.md"
  required: true
  # This is always docs/PHASES.md. Included to make the derivation explicit.

# -- Dataset context --
dataset:
  value: "<sc2egset | aoe2companion | aoestats>"
  required: true

# -- Pipeline Sections --
pipeline_sections:
  value:
    - number: "<NN_NN>"
      name: "<pipeline section name from docs/PHASES.md>"
  required: true
  # The list must match docs/PHASES.md exactly. ROADMAPs do not invent,
  # rename, or omit Pipeline Sections.

# -- Gate --
gate:
  exit_criteria:
    value: "<what must hold for this Phase to be considered complete>"
    required: true
  is_gate_marker:
    value: false
    required: true
    # true only for Phase 07

# -- Status derivation rule --
status_derivation:
  description: >
    Phase status is derived from Pipeline Section statuses (which are
    themselves derived from Step statuses):
      complete    -- all Pipeline Sections are complete
      in_progress -- any Pipeline Section is in_progress or complete
      not_started -- no Pipeline Section has started
  required: false
  # Informational. Not a field to be filled in -- it documents the rule.
```

**Comment header:** Follows the pattern from step_template.yaml. References
TAXONOMY.md, PHASES.md, scientific-invariants.md.

**Special case for Phase 07:** The template includes `is_gate_marker` field. When
true, `pipeline_sections` is empty and `gate/exit_criteria` describes the gate
condition from PHASES.md.

---

### Step 2: Create `docs/templates/pipeline_section_template.yaml`

**Purpose:** Template for how a Pipeline Section appears within a Phase in a
dataset ROADMAP. This defines the Pipeline Section block structure that ROADMAP
authors use.

**Fields:**

```yaml
# -- Identity --
section_number:
  value: "<NN_NN>"        # Phase_Section, zero-padded
  required: true

name:
  value: "<pipeline section name from docs/PHASES.md>"
  required: true

# -- Hierarchy context --
phase:
  value: "<NN -- phase name>"
  required: true

manual_section:
  value: "<manual_filename.md, section or part number>"
  required: true

canonical_reference:
  value: "docs/PHASES.md"
  required: true

# -- Dataset context --
dataset:
  value: "<sc2egset | aoe2companion | aoestats>"
  required: true

# -- Steps --
steps:
  value:
    - step_number: "<NN_NN_NN>"
      name: "<step name>"
  required: true
  # Steps are defined in full using docs/templates/step_template.yaml.
  # This field is a summary index; full Step definitions are fenced
  # YAML blocks in the ROADMAP.

# -- Gate --
gate:
  exit_criteria:
    value: "<what must hold for this Pipeline Section to be complete>"
    required: true

# -- Status derivation rule --
status_derivation:
  description: >
    Pipeline Section status is derived from Step statuses:
      complete    -- all Steps are complete
      in_progress -- any Step is in_progress or complete
      not_started -- no Step has started
  required: false
```

---

### Step 3: Create `docs/templates/dataset_roadmap_template.yaml`

**Purpose:** Template for the overall structure of a dataset-level ROADMAP.md
file. Documents what sections a ROADMAP must contain and in what order.

**Fields (structural — describes document layout):**

```yaml
header:
  game:
    value: "<game identifier>"
    required: true
  dataset:
    value: "<dataset identifier>"
    required: true
  role:
    value: "<TO BE DETERMINED | PRIMARY | SUPPLEMENTARY VALIDATION | omit if sole dataset>"
    required: false
    # Only for games with multiple datasets. Must be TO BE DETERMINED until
    # Phase 01 Decision Gate (01_06) evidence supports role assignment.
    # Role assignment requires: schema completeness, null rates, player
    # identity coverage, temporal density — not file counts alone.
  canonical_references:
    value:
      canonical_phase_list: "docs/PHASES.md"
      methodology_manuals: "docs/INDEX.md"
      step_schema: "docs/templates/step_template.yaml"
    required: true

usage_section:
  heading: "## How to use this document"
  description: >
    Prose block explaining that this ROADMAP decomposes Phases into
    Pipeline Sections and Steps. Must state that the canonical Phase and
    Pipeline Section definitions live in docs/PHASES.md, and that this
    ROADMAP does not invent them. Must describe the XX_YY_ZZ numbering.
  required: true

source_data_section:
  heading: "## Source data"
  description: >
    Dataset provenance: citation, row counts, known issues, temporal
    coverage, warnings about snapshot tables or schema drift.
    Pre-Phase-01 values are marked with a provenance caveat.
  required: true

phase_sections:
  description: >
    One ## section per Phase (01 through 07). All datasets implement all
    7 Phases per docs/PHASES.md. No Phase may be excluded from a dataset
    ROADMAP without Phase 01 Decision Gate evidence.
  active_phase_structure:
    heading: "## Phase NN -- Phase Name"
    pipeline_section_list: "Bullet list: `NN_NN` -- Pipeline Section Name"
    step_definitions: "Fenced YAML blocks per docs/templates/step_template.yaml"
  placeholder_phase_structure:
    heading: "## Phase NN -- Phase Name (placeholder)"
    body: "Pipeline Sections: see `docs/PHASES.md`. Steps to be defined when Phase NN-1 gate is met."
  gate_marker_structure:
    heading: "## Phase 07 -- Thesis Writing Wrap-up (gate marker)"
    body: "Per `docs/PHASES.md`, Phase 07 is a gate marker with no Pipeline Sections."
  required: true
```

---

### Step 4: Create `docs/templates/research_log_template.yaml`

**Purpose:** Template for the overall structure of `reports/research_log.md`
(the container, not individual entries). The entry template already exists as
`research_log_entry_template.yaml`.

**Fields:**

```yaml
document:
  path: "reports/research_log.md"
  description: >
    Unified chronological narrative of all research decisions and
    findings, tagged by dataset. Newest entries first.
  required: true

header:
  thesis_title:
    value: "<full thesis title>"
    required: true
  ordering: "Reverse chronological (newest first)"
  required: true

entry_template:
  path: "docs/templates/research_log_entry_template.yaml"
  markdown_rendering: "reports/RESEARCH_LOG_TEMPLATE.md"
  # reports/RESEARCH_LOG_TEMPLATE.md already exists on disk as a human-readable
  # rendering of the entry template. It is not modified by this PR — the YAML
  # template is the authoritative schema; the .md rendering is a convenience.
  required: true

hierarchy_linking:
  description: >
    Each entry's title includes a Phase/Step reference
    (e.g., "[Phase 01 / Step 01_01_01]") that links it to the
    Phase > Pipeline Section > Step hierarchy. Non-Phase entries
    use [CROSS] or [CHORE] tags. The Pipeline Section is
    implicit in the Step number (first two components).
  required: true

dataset_tags:
  allowed: ["sc2egset", "aoe2companion", "aoestats", "CROSS"]
  description: >
    Every entry must specify its dataset scope. CROSS is used for
    entries that span multiple datasets or are game-agnostic.
  required: true

cross_references:
  to_roadmaps: >
    Entry artifacts must match paths declared in the ROADMAP step
    definition's outputs field.
  to_step_status: >
    Completion of a research log entry is a prerequisite for marking
    a Step as complete in STEP_STATUS.yaml.
  required: true
```

---

### Step 5: Enhance STEP_STATUS.yaml across all 3 datasets

**What changes:** Add `pipeline_section` field to each step entry (upward link
from Step to Pipeline Section). Add `game` field to header for consistency with
PHASE_STATUS.yaml.

**sc2egset** `src/rts_predict/sc2/reports/sc2egset/STEP_STATUS.yaml`:
```yaml
game: sc2
dataset: sc2egset

steps:
  "01_01_01":
    name: "File Inventory"
    pipeline_section: "01_01"
    status: complete
    completed_at: "2026-04-09"
```

**aoe2companion** — same change: add `game: aoe2`, add `pipeline_section: "01_01"`.

**aoestats** — same change: add `game: aoe2`, add `pipeline_section: "01_01"`.

**Update derivation rule comments** in all 3 STEP_STATUS.yaml files. The existing
comments say "PHASE_STATUS.yaml is derived from this file" (a direct Step ->
Phase rule). Replace with the three-tier chain:

```yaml
# PIPELINE_SECTION_STATUS.yaml is derived from this file:
#   Pipeline section is complete    when ALL its steps are complete.
#   Pipeline section is in_progress when ANY step is in_progress or complete.
#   Pipeline section is not_started when NO step has started.
#
# Derivation chain:
#   this file -> PIPELINE_SECTION_STATUS.yaml -> PHASE_STATUS.yaml
```

This ensures all three status files describe the same derivation chain
consistently.

---

### Step 6: Populate PIPELINE_SECTION_STATUS.yaml across all 3 datasets

**What:** sc2egset already has an empty file. aoe2companion and aoestats need
the file created.

**Structure (identical across all 3 datasets, differing only in game/dataset):**

```yaml
# Pipeline Section status for <dataset>.
# Derived from STEP_STATUS.yaml.
# If this file disagrees with STEP_STATUS.yaml, this file is wrong.
#
# PHASE_STATUS.yaml is derived from this file:
#   Phase is complete    when ALL its pipeline sections are complete.
#   Phase is in_progress when ANY pipeline section is in_progress or complete.
#   Phase is not_started when NO pipeline section has started.
#
# This file is derived from STEP_STATUS.yaml:
#   Pipeline section is complete    when ALL its steps are complete.
#   Pipeline section is in_progress when ANY step is in_progress or complete.
#   Pipeline section is not_started when NO step has started.

game: <sc2|aoe2>
dataset: <dataset>

pipeline_sections:
  "01_01":
    name: "Data Acquisition & Source Inventory"
    phase: "01"
    status: in_progress
  "01_02":
    name: "Exploratory Data Analysis (Tukey-style)"
    phase: "01"
    status: not_started
  "01_03":
    name: "Systematic Data Profiling"
    phase: "01"
    status: not_started
  "01_04":
    name: "Data Cleaning"
    phase: "01"
    status: not_started
  "01_05":
    name: "Temporal & Panel EDA"
    phase: "01"
    status: not_started
  "01_06":
    name: "Decision Gates"
    phase: "01"
    status: not_started
  # Pipeline sections for Phases 02-06 added when those Phases become active.
  # Phase 07 has no pipeline sections.
  #
  # NOTE: Only Phase 01 pipeline sections are listed here. PHASE_STATUS.yaml
  # lists all 7 phases (including not_started ones). This asymmetry is
  # intentional — pipeline sections are added incrementally as Phases activate,
  # not pre-populated.
```

All 3 datasets use the identical trailing comment. No dataset-specific
exceptions — all datasets implement Phases 01-07 per `docs/PHASES.md`.

**Note:** 01_01 is `in_progress` because step 01_01_01 is complete but the
Pipeline Section's full step list is not yet determined to be complete.

---

### Step 7: Update PHASE_STATUS.yaml for derivation chain clarity (all 3 datasets)

**What changes:** Add a comment referencing the derivation chain. No structural
changes to the fields.

Add after existing derivation comment:
```yaml
# Derivation chain:
#   STEP_STATUS.yaml -> PIPELINE_SECTION_STATUS.yaml -> this file
# Phase status is derived from pipeline section statuses.
# See PIPELINE_SECTION_STATUS.yaml for the intermediate derivation.
```

No field additions needed — the existing `phases:` map with `name` and `status`
per phase is sufficient.

---

### Step 8: Create status template YAMLs in `docs/templates/`

Three new files defining the schema for status tracking files.

**8a. `docs/templates/phase_status_template.yaml`** — schema for
PHASE_STATUS.yaml files. Fields: file_path, game, dataset, dataset_roadmap,
derived_from, phases (entry_schema with phase_number, name, status + derivation
rule).

**8b. `docs/templates/pipeline_section_status_template.yaml`** — schema for
PIPELINE_SECTION_STATUS.yaml files. Fields: file_path, game, dataset,
derived_from, feeds, pipeline_sections (entry_schema with section_number, name,
phase, status + derivation rule).

**8c. `docs/templates/step_status_template.yaml`** — schema for
STEP_STATUS.yaml files. Fields: file_path, game, dataset, feeds, steps
(entry_schema with step_number, name, pipeline_section, status, completed_at
when complete).

---

### Step 9: Update ARCHITECTURE.md references

**Game package contract table additions** (STEP_STATUS.yaml is also currently
absent from the table — a pre-existing gap that this PR fixes):
```
| `reports/<dataset>/STEP_STATUS.yaml` | Machine-readable step progress (dataset-scoped) | Per dataset |
| `reports/<dataset>/PIPELINE_SECTION_STATUS.yaml` | Machine-readable pipeline section progress (dataset-scoped) | Per dataset |
```
Note: PHASE_STATUS.yaml is already in the table. The executor adds the two rows
above adjacent to it. Net result: all three status files are listed.

**Source-of-Truth Hierarchy update:** Current tier 7 is PHASE_STATUS.yaml with
prose "Strictly derived from tiers (5) and (6). Never authoritative; never
diverges." This prose must be rewritten to describe the three-tier derivation
chain. New tier 7:

- 7a. STEP_STATUS.yaml — derived from dataset ROADMAPs (tier 6)
- 7b. PIPELINE_SECTION_STATUS.yaml — derived from STEP_STATUS.yaml (tier 7a)
- 7c. PHASE_STATUS.yaml — derived from PIPELINE_SECTION_STATUS.yaml (tier 7b)

All three remain at precedence level 7 — they are all derived status files.
Rewrite the existing tier 7 description to: "Machine-readable status files.
STEP_STATUS is derived from the dataset ROADMAP (tier 6). PIPELINE_SECTION_STATUS
is derived from STEP_STATUS. PHASE_STATUS is derived from PIPELINE_SECTION_STATUS.
None are authoritative; if any disagrees with its upstream source, it is wrong and
gets regenerated."

**Progress tracking section:** Expand the paragraph that currently only mentions
PHASE_STATUS.yaml to describe the full derivation chain.

---

### Step 10: Update CLAUDE.md

PIPELINE_SECTION_STATUS.yaml was already added to Key File Locations by the user.
Verify it is present; no further changes needed.

---

### Step 11: Update CHANGELOG.md

Add under `[Unreleased]`:

```
### Added
- `docs/templates/phase_template.yaml` — ROADMAP authoring template for Phase blocks
- `docs/templates/pipeline_section_template.yaml` — ROADMAP authoring template for Pipeline Section blocks
- `docs/templates/dataset_roadmap_template.yaml` — ROADMAP document structure template
- `docs/templates/research_log_template.yaml` — research log document structure template
- `docs/templates/phase_status_template.yaml` — schema for PHASE_STATUS.yaml files
- `docs/templates/pipeline_section_status_template.yaml` — schema for PIPELINE_SECTION_STATUS.yaml files
- `docs/templates/step_status_template.yaml` — schema for STEP_STATUS.yaml files
- PIPELINE_SECTION_STATUS.yaml for all 3 datasets (sc2egset, aoe2companion, aoestats)

### Changed
- AoE2 game-level ROADMAP: retracted premature PRIMARY/SUPPLEMENTARY role assignments, replaced with provisional language pending Phase 01 Decision Gates
- AoE2 dataset ROADMAPs (aoe2companion, aoestats): removed premature role banners, restored full Phase 01-07 scope for both datasets
- STEP_STATUS.yaml: added `game` and `pipeline_section` fields, updated derivation comments (all 3 datasets)
- PHASE_STATUS.yaml: added derivation chain comments (all 3 datasets)
- ARCHITECTURE.md: documented full status tracking hierarchy
- CLAUDE.md: added PIPELINE_SECTION_STATUS.yaml to Key File Locations
```

---

## Design decisions

1. **ROADMAP templates vs status templates are separate.** `phase_template.yaml`
   defines how a Phase appears in a ROADMAP (authoring guide).
   `phase_status_template.yaml` defines how a Phase appears in PHASE_STATUS.yaml
   (runtime status). These are different concerns at different source-of-truth
   tiers.

2. **Only Phase 01 Pipeline Sections are populated in
   PIPELINE_SECTION_STATUS.yaml.** Phases 02-06 pipeline sections are not yet
   added because those Phases are `not_started`. Adding them would create a large
   file with 44 sections all reading `not_started`. Pipeline sections are added
   when their Phase becomes active, matching how Steps are added to
   STEP_STATUS.yaml incrementally.

3. **The `value:` + `required:` pattern is used in field-level templates** for
   consistency with existing `step_template.yaml`. Document-structure templates
   (`dataset_roadmap_template.yaml`, `research_log_template.yaml`) use the
   pattern where applicable but use `heading:` + `description:` for prose-level
   layout constraints where `value:` would be semantically misleading.

4. **No changes to TAXONOMY.md.** The terminology is already complete. The
   templates implement the taxonomy; they do not extend it.

5. **PIPELINE_SECTION_STATUS.yaml for aoe2 datasets are created** (not just
   populated from empty) because unlike sc2egset which has an empty file, the
   aoe2 datasets have no file at all.

6. **All datasets are treated identically.** No dataset-specific Phase scope
   exceptions. The premature PRIMARY / SUPPLEMENTARY VALIDATION role assignments
   and the aoestats Phase 06 exclusion are retracted in Step 0 because they
   were made without Phase 01 Decision Gate evidence. Per `docs/PHASES.md`, all
   dataset ROADMAPs implement Phases 01-07. Role assignment is deferred to
   Pipeline Section 01_06 (Decision Gates) where comparative data quality
   findings will be available.

7. **The `dataset_roadmap_template.yaml` role field includes `TO BE DETERMINED`**
   as a valid value. Role assignment requires Phase 01 Decision Gate evidence
   (schema completeness, null rates, player identity coverage, temporal density).
   File counts and structural observations (daily vs weekly granularity) are
   planning indicators, not evidence for methodology commitments.

---

## File manifest

**New files (5)** — do not exist on disk:
1. `docs/templates/phase_status_template.yaml`
2. `docs/templates/pipeline_section_status_template.yaml`
3. `docs/templates/step_status_template.yaml`
4. `src/rts_predict/aoe2/reports/aoe2companion/PIPELINE_SECTION_STATUS.yaml`
5. `src/rts_predict/aoe2/reports/aoestats/PIPELINE_SECTION_STATUS.yaml`

**Populated from empty (4)** — exist on disk as 0-byte tracked files:
6. `docs/templates/phase_template.yaml`
7. `docs/templates/pipeline_section_template.yaml`
8. `docs/templates/dataset_roadmap_template.yaml`
9. `docs/templates/research_log_template.yaml`

**Modified files (13):**
10. `src/rts_predict/sc2/reports/sc2egset/STEP_STATUS.yaml`
11. `src/rts_predict/aoe2/reports/aoe2companion/STEP_STATUS.yaml`
12. `src/rts_predict/aoe2/reports/aoestats/STEP_STATUS.yaml`
13. `src/rts_predict/sc2/reports/sc2egset/PIPELINE_SECTION_STATUS.yaml` (populated from empty)
14. `src/rts_predict/sc2/reports/sc2egset/PHASE_STATUS.yaml`
15. `src/rts_predict/aoe2/reports/aoe2companion/PHASE_STATUS.yaml`
16. `src/rts_predict/aoe2/reports/aoestats/PHASE_STATUS.yaml`
17. `src/rts_predict/aoe2/reports/ROADMAP.md` (retract dataset strategy)
18. `src/rts_predict/aoe2/reports/aoestats/ROADMAP.md` (retract role banner)
19. `src/rts_predict/aoe2/reports/aoe2companion/ROADMAP.md` (retract role banner)
20. `reports/research_log.md` (retraction entry)
21. `ARCHITECTURE.md`
22. `CHANGELOG.md`

---

## Gate condition

All 22 files listed in the manifest exist on disk with non-empty content. The
derivation chain is consistent: every step in STEP_STATUS.yaml has a
`pipeline_section` field, every pipeline section in PIPELINE_SECTION_STATUS.yaml
has a `phase` field, and the derived statuses are consistent (01_01 is
`in_progress` because 01_01_01 is `complete`, Phase 01 is `in_progress` because
01_01 is `in_progress`). All three datasets are treated identically — no
dataset-specific Phase scope exceptions exist. AoE2 ROADMAPs contain provisional
language for role assignment, not committed roles.

---

## Adversarial Review

**Reviewer:** reviewer-adversarial agent (two passes + premature commitment audit)
**Date:** 2026-04-11
**Final verdict:** APPROVE

### Pass 1 — template hierarchy review

8 issues found and resolved in-plan:

- **#1 CRITICAL** — STEP_STATUS.yaml derivation comments updated to three-tier
  chain (resolved in Step 5)
- **#2 MODERATE** — File manifest reclassified: 5 new + 4 populated-from-empty +
  modified (resolved in manifest)
- **#3 MODERATE** — aoestats Phase 06 asymmetry (superseded by Step 0 retraction
  — all datasets now identical)
- **#4 MODERATE** — ARCHITECTURE.md tier 7 prose rewrite (resolved in Step 9)
- **#5 MODERATE** — STEP_STATUS.yaml added to game package contract table
  (resolved in Step 9)
- **#6 MINOR** — Template pattern distinction documented (resolved in Design
  Decision #3)
- **#7 MINOR** — RESEARCH_LOG_TEMPLATE.md cross-reference clarified (resolved in
  Step 4)
- **#8 NOTE** — Population asymmetry documented in status file comments (resolved
  in Step 6)

### Pass 2 — second-pass verification

All 8 resolutions verified as adequate. One new issue found:

- **#9 WARNING** — aoestats PHASE_STATUS.yaml lists Phase 06 as `not_started`
  despite ROADMAP declaring it out of scope. Superseded by Step 0 retraction —
  Phase 06 is restored for all datasets, so the `not_started` status is now
  correct.

### Pass 3 — premature dataset strategy audit

User-initiated audit of AoE2 ROADMAPs for premature methodological commitments.
Findings:

- **BLOCKER A** — Phase 06 exclusion for aoestats contradicts `docs/PHASES.md`
  requirement that all datasets implement Phases 01-07. **Resolved by Step 0.**
- **BLOCKER B** — PRIMARY/SUPPLEMENTARY role assignment lacks Phase 01 evidence.
  Based on unverified row counts, structural observations, and circular thesis
  structure reference. **Resolved by Step 0.**
- **WARNING** — "Lightweight Phase 02-05 replication pass" undefined. **Resolved
  by Step 0 — language removed.**
- **WARNING** — Contradictions pre-framed as "Threats to Validity" rather than
  findings. **Resolved by Step 0 — language removed.**
- **WARNING** — "9x more matches" claim violates Invariant 6 (no derivation
  code). **Resolved by Step 0 — replaced with caveated planning indicators.**
- **NOTE** — `_current_plan.md` Step 6 propagated Phase 06 exclusion. **Resolved
  — all datasets now use identical trailing comment.**
