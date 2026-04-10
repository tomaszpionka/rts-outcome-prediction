# Notebook Template Fix Plan

**Category:** C (Chore)
**Branch:** `chore/notebook-template-v2`
**Date:** 2026-04-10
**Triggered by:** Adversarial review at `temp/notebook_fix/notebook_template_review.md`

---

## Problem Statement

The current notebook template (`temp/notebook_fix/notebook_template.md`) is not
fit for purpose. An adversarial review identified six critical gaps:

1. Template front-matter format (markdown table) contradicts all three existing
   notebooks (bold key-value pairs).
2. No existing notebook has the Conclusion/Thesis mapping/Follow-ups sections
   the template prescribes.
3. Template is DuckDB-centric but all three existing notebooks are
   filesystem-only (no DuckDB).
4. No temporal leakage verification section for Phase 02+ notebooks.
5. No environment/version pinning.
6. Step numbering example (`1.8`) does not match project taxonomy (`01_01_01`).

The template must be revised before Phase 02 notebooks are generated.

---

## Decision 1: Template Format (YAML, not MD)

**Choice:** `docs/templates/notebook_template.yaml`

**Rationale:**
- The two existing templates in `docs/templates/` are both YAML
  (`step_template.yaml`, `raw_data_readme_template.yaml`). Following
  the established convention reduces cognitive load.
- YAML supports structured comments (`# required: true/false`),
  conditional field documentation, and machine-parseable field names.
  A markdown template conflates content and structure.
- The template is not itself a notebook -- it is a schema that describes
  what a notebook should contain. YAML is the right format for schemas.
- The executor agent reads the YAML and produces the `.py` (jupytext
  percent-format) file. The YAML is never rendered directly.

**File location:** `docs/templates/notebook_template.yaml`

**The old template** at `temp/notebook_fix/notebook_template.md` will NOT be
deleted by this chore. It remains in `temp/` as historical context. A
`.gitignore` entry or future cleanup can remove it.

---

## Decision 2: Front-matter Format (Bold Key-Value Pairs)

**Choice:** Adopt the bold key-value style that the three existing notebooks
already use. Do NOT use a markdown table.

**Rationale:**
- Three notebooks already exist with the bold key-value format. The
  template should codify what works, not force a retroactive reformat.
- Bold key-value pairs are more readable in the jupytext `.py` format
  (where every line is a `#` comment) than a markdown table with
  alignment pipes.
- The step_template.yaml already defines the machine-parseable metadata
  for each Step. The notebook front-matter is a human-readable header,
  not a data interchange format.

---

## Decision 3: Conditional Sections (DuckDB vs. Non-DuckDB)

**Choice:** The template defines TWO setup/cleanup patterns and documents
when each applies:

- **Pattern A (DuckDB notebooks):** `get_notebook_db("{game}", "{dataset}")`
  in setup, `con.close()` in cleanup.
- **Pattern B (filesystem-only notebooks):** No DuckDB setup. Cleanup cell
  is optional (only needed if other resources require explicit release).

The template marks Pattern A cells with a comment: `# DuckDB notebooks only`.
The template marks Pattern B as the default for Phase 01 file inventory
notebooks.

**Rationale:** All three existing notebooks are Pattern B. Phase 02+
notebooks will predominantly be Pattern A. Both patterns must be documented.

---

## Decision 4: Parameterized Placeholders

All game/dataset-specific values use `{game}` and `{dataset}` placeholders,
never hardcoded values. This prevents copy-paste errors flagged in Finding #4
of the review.

Placeholders used throughout the template:
- `{game}` -- "sc2" or "aoe2"
- `{dataset}` -- "sc2egset", "aoe2companion", or "aoestats"
- `{phase_nn}` -- two-digit phase number, e.g., "01"
- `{phase_name}` -- phase name, e.g., "Data Exploration"
- `{section_nn_nn}` -- pipeline section number, e.g., "01_01"
- `{section_name}` -- pipeline section name
- `{step_nn_nn_nn}` -- step number, e.g., "01_01_01"
- `{step_name}` -- descriptive step name
- `{question}` -- one-sentence scientific question
- `{slug}` -- descriptive filename slug

---

## Decision 5: Invariant Declaration Mechanism

Each notebook front-matter includes an `Invariants applied` field listing
which of the 8 scientific invariants are active for that notebook, mirroring
the `scientific_invariants_applied` field from `step_template.yaml`.

For Phase 01 file inventory notebooks, this would read:
```
**Invariants applied:** #6 (reproducibility: counts produced by auditable code), #7 (no magic numbers: pure counting, no thresholds)
```

For Phase 02+ notebooks, temporal leakage invariant #3 would be listed with
a description of how it is verified in the notebook body.

---

## Decision 6: Temporal Leakage Verification Section

A dedicated section titled `## Temporal Leakage Verification` is REQUIRED
for all notebooks in Phase 02 and later. The template marks this section
as conditional (`# Phase 02+ only`).

The section must contain:
1. A code cell that programmatically verifies no feature uses data from
   game T or later to predict game T.
2. A markdown cell interpreting the verification result.

For Phase 01 notebooks, the section is omitted entirely (not present as
an empty placeholder).

**Structural enforcement:** The template documents this as a hard rule.
Enforcement is by reviewer discipline and (future) CI lint -- see
Decision 10 below.

---

## Decision 7: Conclusion / Thesis Mapping Section

The template prescribes a `## Conclusion` section with three subsections:

1. **Artifacts produced** -- list of artifact paths written by this notebook.
2. **Thesis mapping** -- target section(s) in `thesis/THESIS_STRUCTURE.md`.
3. **Follow-ups** -- what the next Step or Pipeline Section should
   investigate based on these findings.

This replaces the current bare `## Verification` section in existing notebooks.
The Verification content (if applicable) moves into the Conclusion as a
brief statement, not a separate top-level section.

---

## Decision 8: Environment Pinning

The front-matter includes a `Commit` field recording the git short-hash at
notebook creation time. This is sufficient because:

- `poetry.lock` is committed and pinned. The git hash transitively pins
  all library versions.
- Python version is pinned in `pyproject.toml` (3.12).
- Recording the full `poetry.lock` hash in every notebook front-matter
  adds noise without additional auditability.

Format:
```
**Commit:** {git_short_hash}
```

The executor populates this at notebook creation. It does NOT auto-update
on re-runs -- it records the commit at which the notebook was authored.

---

## Decision 9: Phase-Specific Conditional Sections

The template uses YAML comments to mark sections that are phase-conditional.
The executor includes or omits these sections based on the target Phase.

| Phase | Additional required sections |
|-------|----------------------------|
| 01 | None beyond the base template |
| 02 | Feature category (pre-game vs. in-game), symmetry verification cell, cold-start handling documentation |
| 03 | Split strategy documentation, leakage verification cell, baseline comparison |
| 04 | Hypothesis statement, experiment ID, hyperparameter table |
| 05 | Statistical test justification, assumptions-checked cell, ROPE intervals |
| 06 | Transfer taxonomy classification, domain shift documentation |

These are documented in the template as a lookup table. The template body
contains the base structure; phase-conditional cells are listed in a separate
YAML block at the end of the template.

---

## Decision 10: Validation / Enforcement Strategy

Three tiers of enforcement, in order of implementation priority:

### Tier 1 — Template documentation (this chore)
The template itself documents hard rules with `# REQUIRED` / `# CONDITIONAL`
/ `# OPTIONAL` annotations. Reviewer agents check notebooks against the
template.

### Tier 2 — Pre-commit AST check (separate chore, out of scope)
A pre-commit hook that parses `.py` notebooks and validates:
- Front-matter fields present
- Cell line cap (50 lines)
- No inline `def`/`class` definitions
- Conclusion section exists

This is the "planned" check mentioned in `notebook_config.toml`. It is
NOT implemented in this chore. A separate `chore/notebook-lint` branch
will handle it.

### Tier 3 — CI notebook lint (separate chore, out of scope)
A CI job that validates all notebooks in `sandbox/` against the template
schema. This is NOT implemented in this chore.

**This chore implements Tier 1 only.** Tiers 2 and 3 are documented as
future work in the template's header comments.

---

## Template Content Specification

The YAML file has the following top-level structure:

```yaml
# Notebook Template v2
#
# Canonical template for sandbox notebooks (jupytext .py:percent format).
# Used by executor agents to generate notebooks for Phase work.
#
# Authoritative sources:
#   Taxonomy          docs/TAXONOMY.md
#   Canonical Phases  docs/PHASES.md
#   Invariants        .claude/scientific-invariants.md
#   Sandbox contract  sandbox/README.md
#   Cell rules        sandbox/notebook_config.toml
#   Step schema       docs/templates/step_template.yaml
#
# Enforcement:
#   Tier 1 (current): Template documentation + reviewer discipline
#   Tier 2 (planned): Pre-commit AST-based cell validation
#   Tier 3 (planned): CI notebook lint against this schema
#
# Format: YAML with fenced jupytext cell content in multiline strings.
# Placeholders use {curly_braces}. All are listed in the placeholders block.
```

### Section-by-section content

#### Block 1: Placeholders registry

```yaml
placeholders:
  game:
    description: "Game identifier"
    allowed: ["sc2", "aoe2"]
    required: true
  dataset:
    description: "Dataset identifier"
    allowed: ["sc2egset", "aoe2companion", "aoestats"]
    required: true
  phase_nn:
    description: "Two-digit phase number"
    example: "01"
    required: true
  phase_name:
    description: "Phase name from docs/PHASES.md"
    example: "Data Exploration"
    required: true
  section_nn_nn:
    description: "Pipeline section number"
    example: "01_01"
    required: true
  section_name:
    description: "Pipeline section name from docs/PHASES.md"
    example: "Data Acquisition & Source Inventory"
    required: true
  step_nn_nn_nn:
    description: "Step number"
    example: "01_01_01"
    required: true
  step_name:
    description: "Descriptive step name from ROADMAP"
    example: "File Inventory"
    required: true
  slug:
    description: "Filename slug (lowercase, underscores)"
    example: "file_inventory"
    required: true
  question:
    description: "One-sentence scientific question from ROADMAP"
    required: true
  invariants_applied:
    description: "Comma-separated list of invariant numbers and short descriptions"
    example: "#6 (reproducibility), #7 (no magic numbers)"
    required: true
  git_short_hash:
    description: "Git short hash at notebook creation time"
    example: "a1b2c3d"
    required: true
  roadmap_path:
    description: "Relative path to the dataset ROADMAP"
    example: "src/rts_predict/sc2/reports/sc2egset/ROADMAP.md"
    required: true
```

#### Block 2: Cell definitions (the notebook body)

Each cell is defined as a YAML mapping with keys:
- `cell_id`: sequential identifier (e.g., "cell_01")
- `cell_type`: "markdown" or "code"
- `required`: true/false
- `condition`: when this cell is included (e.g., "always", "duckdb_only", "phase_02_plus")
- `content`: multiline string with the cell content in jupytext percent format
- `notes`: guidance for the executor

##### Cell 01 -- Front-matter (markdown, REQUIRED, always)

```yaml
cell_01_frontmatter:
  cell_type: markdown
  required: true
  condition: always
  content: |
    # Step {step_nn_nn_nn} -- {step_name}: {dataset}

    **Phase:** {phase_nn} -- {phase_name}
    **Pipeline Section:** {section_nn_nn} -- {section_name}
    **Dataset:** {dataset}
    **Question:** {question}
    **Invariants applied:** {invariants_applied}
    **ROADMAP reference:** `{roadmap_path}` Step {step_nn_nn_nn}
    **Commit:** {git_short_hash}

    {description_paragraph}
  notes: |
    - Use bold key-value pairs, NOT a markdown table.
    - The description paragraph is 1-3 sentences explaining what the
      notebook does concretely. Include layout notes if the data
      structure is non-obvious.
    - All fields are mandatory. Do not omit any.
```

##### Cell 02 -- Imports and setup (code, REQUIRED, always)

```yaml
cell_02_imports:
  cell_type: code
  required: true
  condition: always
  content: |
    import logging
    from pathlib import Path

    from rts_predict.common.notebook_utils import get_reports_dir
    # ... other imports from src/rts_predict/ ...

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
  notes: |
    - All imports from src/rts_predict/. No inline definitions.
    - logging setup is mandatory for auditability.
    - Do NOT import get_notebook_db here unless this is a DuckDB notebook.
```

##### Cell 03 -- Paths and config (code, REQUIRED, always)

```yaml
cell_03_paths:
  cell_type: code
  required: true
  condition: always
  content: |
    from rts_predict.{game}.config import {CONFIG_CONSTANT}

    RAW_DIR: Path = {CONFIG_CONSTANT}
    ARTIFACTS_DIR: Path = get_reports_dir("{game}", "{dataset}") / "artifacts" / "{section_nn_nn}"
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Source directory: %s", RAW_DIR)
    logger.info("Artifacts directory: %s", ARTIFACTS_DIR)
  notes: |
    - Paths derived from config, never hardcoded.
    - ARTIFACTS_DIR always uses get_reports_dir() + "artifacts/" + section number.
    - The {CONFIG_CONSTANT} placeholder is dataset-specific (e.g.,
      REPLAYS_SOURCE_DIR for sc2egset, AOE2COMPANION_RAW_DIR for aoe2companion).
```

##### Cell 04 -- DuckDB setup (code, CONDITIONAL: duckdb_only)

```yaml
cell_04_duckdb_setup:
  cell_type: code
  required: false
  condition: duckdb_only
  content: |
    from rts_predict.common.notebook_utils import get_notebook_db

    con = get_notebook_db("{game}", "{dataset}")
  notes: |
    - Include this cell ONLY if the notebook queries DuckDB.
    - Phase 01 file inventory notebooks do NOT need this cell.
    - Phase 02+ notebooks that compute features from DuckDB DO need it.
    - The {game} and {dataset} placeholders prevent copy-paste errors.
```

##### Cells 05-N -- Analysis cells (code + markdown pairs)

```yaml
cells_05_to_n_analysis:
  cell_type: "alternating code + markdown"
  required: true
  condition: always
  content: |
    # Each analysis step is a code cell followed by a markdown interpretation cell.
    # The code cell runs the query or computation.
    # The markdown cell interprets the result: what does this number mean?
    #
    # Rules:
    #   - Max 50 lines per cell (sandbox/notebook_config.toml).
    #   - No inline def/class/lambda assignments.
    #   - Every query code cell must be followed by a markdown cell within 2 cells.
    #   - Per Invariant #6: report artifacts must embed the exact code that
    #     produced each number. If the artifact is a markdown report, the
    #     derivation code is the notebook cell itself (traceable via the
    #     paired .ipynb).
    #   - Per Invariant #7: every threshold must be justified by empirical
    #     evidence or literature citation. Add a comment or markdown note
    #     for each threshold.
  notes: |
    - The number of analysis cells varies by Step.
    - The step_template.yaml 'method' field describes the analytical approach.
    - Stratification (by tournament, by year, etc.) should be visible in
      the code cells, not hidden in helper functions.
```

##### Cell N+1 -- Temporal leakage verification (code + markdown, CONDITIONAL: phase_02_plus)

```yaml
cell_leakage_verification:
  cell_type: "code + markdown pair"
  required: false
  condition: phase_02_plus
  content: |
    # %% [markdown]
    # ## Temporal Leakage Verification
    #
    # Per Scientific Invariant #3: no feature for game T may use information
    # from game T or later. This cell programmatically verifies that
    # constraint.

    # %%
    # Verification code here. Must assert that:
    # 1. All feature computation windows end strictly before game T.
    # 2. Rolling aggregates exclude the target game's own value.
    # 3. Head-to-head counts exclude the target game.
    #
    # Example (adapt to the specific feature):
    # assert (features_df["feature_timestamp"] < features_df["game_timestamp"]).all()

    # %% [markdown]
    # **Verification result:** {describe what was checked and whether it passed}
  notes: |
    - REQUIRED for Phase 02, 03, 04, 05, 06 notebooks that touch features
      or model predictions.
    - The verification must be programmatic (an assert or check), not just
      a prose claim.
    - If the notebook does not compute features or predictions (e.g., a pure
      profiling notebook in Phase 02), document why leakage verification is
      not applicable.
```

##### Cell N+2 -- Conclusion (markdown, REQUIRED, always)

```yaml
cell_conclusion:
  cell_type: markdown
  required: true
  condition: always
  content: |
    ## Conclusion

    ### Artifacts produced
    - `{artifact_path_1}` -- {one-line description}
    - `{artifact_path_2}` -- {one-line description}

    ### Thesis mapping
    - {section path in thesis/THESIS_STRUCTURE.md, copied from ROADMAP step definition}

    ### Follow-ups
    - {what the next Step or Pipeline Section should investigate}
    - {any deferred decisions or open questions}
  notes: |
    - This section is MANDATORY for every notebook.
    - Artifacts produced must list every file written by this notebook.
    - Thesis mapping must match the thesis_mapping field in the ROADMAP
      step definition (step_template.yaml).
    - Follow-ups replace the bare "Verification" section in existing notebooks.
    - If the notebook is a pure inventory with no interpretive findings,
      the Conclusion still lists artifacts and thesis mapping.
```

##### Cell N+3 -- Cleanup (code, CONDITIONAL: duckdb_only)

```yaml
cell_cleanup:
  cell_type: code
  required: false
  condition: duckdb_only
  content: |
    con.close()
  notes: |
    - Include ONLY if cell_04_duckdb_setup was included.
    - For filesystem-only notebooks, no cleanup cell is needed.
```

#### Block 3: Phase-conditional additional sections

```yaml
phase_conditional_sections:
  phase_02:
    description: "Feature Engineering"
    additional_front_matter_fields:
      - "**Feature category:** pre-game | in-game | context"
    additional_required_sections:
      - name: "Symmetry Verification"
        description: "Verify that features are computed identically for both players (Invariant #5)."
        cell_type: "code + markdown pair"
      - name: "Cold-Start Handling"
        description: "Document how players with < N historical games are handled."
        cell_type: markdown
    leakage_verification: required

  phase_03:
    description: "Splitting & Baselines"
    additional_front_matter_fields:
      - "**Split strategy:** {description of temporal split}"
    additional_required_sections:
      - name: "Split Validation"
        description: "Verify no temporal leakage across train/val/test boundaries."
        cell_type: "code + markdown pair"
      - name: "Baseline Comparison"
        description: "Compare against the baseline hierarchy (Dummy -> Elo -> LR)."
        cell_type: "code + markdown pair"
    leakage_verification: required

  phase_04:
    description: "Model Training"
    additional_front_matter_fields:
      - "**Experiment ID:** {unique experiment identifier}"
      - "**Hypothesis:** {what we expect and why}"
    additional_required_sections:
      - name: "Hyperparameter Table"
        description: "Table of all hyperparameters with values and justifications."
        cell_type: markdown
    leakage_verification: required

  phase_05:
    description: "Evaluation & Analysis"
    additional_front_matter_fields: []
    additional_required_sections:
      - name: "Statistical Test Justification"
        description: "Which test, why, assumptions checked."
        cell_type: "code + markdown pair"
      - name: "Assumptions Check"
        description: "Programmatic check of statistical test assumptions."
        cell_type: "code + markdown pair"
    leakage_verification: required

  phase_06:
    description: "Cross-Domain Transfer"
    additional_front_matter_fields:
      - "**Transfer direction:** {sc2 -> aoe2 | aoe2 -> sc2 | bidirectional}"
    additional_required_sections:
      - name: "Domain Shift Documentation"
        description: "Document the distributional differences between source and target."
        cell_type: "code + markdown pair"
    leakage_verification: required
```

#### Block 4: Hard rules reference

```yaml
hard_rules:
  - rule: "No inline definitions"
    source: "sandbox/README.md"
    description: "No def, class, or lambda assignments in any cell. All logic in src/rts_predict/."

  - rule: "Cell size cap"
    source: "sandbox/notebook_config.toml"
    description: "Max 50 lines per cell. Approaching the cap signals extraction to src/."

  - rule: "Read-only DuckDB"
    source: "sandbox/README.md"
    description: "Use get_notebook_db() which is read-only by default."

  - rule: "Both files committed"
    source: "sandbox/README.md"
    description: "Always stage both .ipynb and .py of a pair."

  - rule: "Artifacts to artifacts/ subdir"
    source: "sandbox/README.md"
    description: "Write to reports/<dataset>/artifacts/, never the dataset report root."

  - rule: "Markdown after code"
    source: "This template"
    description: "Every query/computation code cell must be followed by a markdown interpretation cell within 2 cells."

  - rule: "No magic numbers"
    source: ".claude/scientific-invariants.md #7"
    description: "Every threshold justified by empirical evidence or literature citation."

  - rule: "Temporal discipline"
    source: ".claude/scientific-invariants.md #3"
    description: "No feature for game T may use information from game T or later."
```

---

## Implementation Steps

### Step 1: Create the template file

**File:** `docs/templates/notebook_template.yaml`

Write the complete YAML file following the specification above. The file
should be self-contained: an executor agent reading only this file and
`sandbox/README.md` should be able to produce a conformant notebook for
any Step in any Phase.

The content is fully specified in the "Template Content Specification"
section above. The executor should:

1. Write the YAML header comments (authoritative sources, enforcement tiers).
2. Write the placeholders block.
3. Write each cell definition block with content and notes.
4. Write the phase_conditional_sections block.
5. Write the hard_rules block.

### Step 2: Update sandbox/README.md

**File:** `sandbox/README.md`

Add a single line to the "Configuration pointers" section:

```
- `docs/templates/notebook_template.yaml` -- notebook cell structure and front-matter schema
```

This creates a cross-reference from the sandbox contract to the template.
No other changes to `sandbox/README.md`.

### Step 3: Verify template against existing notebooks

The executor should manually verify that each existing notebook's structure
is expressible under the new template. Specifically:

- The front-matter format (bold key-value pairs) matches cell_01.
- The import/setup pattern matches cell_02 + cell_03.
- The analysis cells match the alternating code+markdown pattern.
- The Verification section can be migrated to the Conclusion section.
- No DuckDB cells are needed (existing notebooks are Pattern B).

This is a read-only verification step. Existing notebooks are NOT modified
in this chore. They will be updated in a separate pass to add the Conclusion
section and other missing fields.

### Step 4: Update CHANGELOG.md

Add an entry under `[Unreleased]`:

```
### Added
- Notebook template v2 at `docs/templates/notebook_template.yaml` -- canonical schema for sandbox notebooks with parameterized placeholders, phase-conditional sections, and temporal leakage verification requirements
```

---

## Files Modified

| File | Action | Description |
|------|--------|-------------|
| `docs/templates/notebook_template.yaml` | CREATE | New template file |
| `sandbox/README.md` | EDIT (1 line) | Add cross-reference to template |
| `CHANGELOG.md` | EDIT | Add entry under [Unreleased] |

---

## Files NOT Modified

| File | Reason |
|------|--------|
| `temp/notebook_fix/notebook_template.md` | Historical artifact in temp/; not deleted |
| `sandbox/notebook_config.toml` | No changes needed; cell cap rule is referenced, not modified |
| `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py` | Existing notebooks updated in a separate chore |
| `sandbox/aoe2/*/01_exploration/01_acquisition/01_01_01_file_inventory.py` | Same |
| `.pre-commit-config.yaml` | AST-based lint hook is Tier 2 (separate chore) |

---

## Gate Condition

This chore is complete when:

1. `docs/templates/notebook_template.yaml` exists and contains all blocks
   specified in the Template Content Specification.
2. `sandbox/README.md` references the template in its Configuration pointers.
3. `CHANGELOG.md` has an entry for the template.
4. All existing notebooks' structures are expressible under the template
   (verified manually by the executor, documented in the PR description).

---

## Relationship to Review Findings

| Review Finding | Template Fix |
|----------------|-------------|
| #1 (front-matter divergence) | Decision 2: bold key-value pairs adopted |
| #2 (no Conclusion section) | Decision 7: Conclusion cell is REQUIRED |
| #3 (DuckDB-centric) | Decision 3: conditional DuckDB cells |
| #4 (no Invariant #6 enforcement) | Cell notes reference Invariant #6; Tier 2/3 enforcement deferred |
| #5 (no version pinning) | Decision 8: Commit field in front-matter |
| #6 (no temporal leakage section) | Decision 6: phase_02_plus conditional section |
| Review rec #2 (fix step numbering) | Decision 4: all placeholders use XX_YY_ZZ format |
| Review rec #4 (parameterize game/dataset) | Decision 4: {game}/{dataset} placeholders throughout |
| Review rec #5 (invariants applied field) | Decision 5: front-matter field |
| Review rec #8 (phase-specific sections) | Decision 9: phase_conditional_sections block |
| Review rec #9 (AST cell cap check) | Decision 10: deferred to Tier 2 (separate chore) |
| Review rec #10 (notebook lint CI) | Decision 10: deferred to Tier 3 (separate chore) |

---

## Out of Scope

1. **Updating existing notebooks** -- Existing 01_01_01 notebooks will be
   updated in a separate chore after this template is merged.
2. **Implementing the AST-based cell check** -- Tier 2 enforcement is a
   separate `chore/notebook-lint` branch.
3. **CI notebook validation** -- Tier 3 enforcement is infrastructure work.
4. **Deleting the old template** -- `temp/` cleanup is a separate concern.
