# Chore: Repository Reorganization — `sc2ml` to `rts_predict` Package Structure

## Context

The repository is sanitized from legacy ML code (PR #23) and ready for structural
standardization. The current layout has SC2-specific artifacts scattered at the
repo root (`reports/`, `models/`, `logs/`, `in_game_processing_manifest.json`) and
the Python package named `sc2ml` — which doesn't scale to the planned AoE2
comparative study. This reorganization:

1. Renames the package from `sc2ml` to `rts_predict.sc2` under a unified namespace
2. Moves SC2-specific artifacts into the game package directory
3. Creates the mirrored structure for AoE2 and shared code (placeholders)
4. Updates every live reference in tracked `.md` and `.py` files
5. Sets the foundation for a formal `ARCHITECTURE.md` in a follow-up session

**Category C — chore/maintenance**

---

## Branch

`chore/repo-reorganization`

---

## Target Structure

```
sc2-ml/
├── .claude/
│   ├── aoe2-plan.md                    # Updated: minor ref fixes
│   ├── coding-standards.md             # Updated: paths, commands
│   ├── git-workflow.md                 # Updated: paths, commands
│   ├── ml-protocol.md                  # Updated: report paths
│   ├── project-architecture.md         # Major rewrite
│   ├── python-workflow.md              # Updated: commands
│   ├── scientific-invariants.md        # Updated: roadmap filename
│   ├── testing-standards.md            # Updated: paths, commands
│   ├── thesis-writing.md              # Updated: report paths
│   └── settings.local.json             # No change
├── .gitignore                          # Updated: artifact paths under rts_predict
├── CHANGELOG.md                        # Updated: [Unreleased] documents this chore
├── CLAUDE.md                           # Major rewrite: all paths, commands, layout
├── README.md                           # Updated: commands, paths
├── _current_plan.md                    # Overwritten with this plan
├── pyproject.toml                      # Updated: package config, scripts, tools
├── poetry.lock                         # Regenerated
│
├── reports/                            # Cross-cutting research artifacts
│   └── research_log.md                 # Unified narrative (tagged [SC2]/[AoE2]/[CROSS])
│
├── thesis/                             # Cross-cutting thesis (no structural changes)
│   ├── THESIS_STRUCTURE.md             # Updated: SC2ML → SC2, report path refs
│   ├── WRITING_STATUS.md               # No change
│   ├── chapters/
│   ├── figures/
│   ├── tables/
│   └── references.bib
│
├── tests/                              # Root integration/infra tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── helpers.py
│   └── test_mps.py
│
└── src/
    └── rts_predict/                    # Top-level Python package
        ├── __init__.py                 # __version__, package docstring
        │
        ├── sc2/                        # StarCraft II game package
        │   ├── __init__.py             # Game-specific docstring (no __version__)
        │   ├── cli.py
        │   ├── config.py              # GAME_DIR, ROOT_DIR, REPORTS_DIR centralized
        │   ├── data/
        │   │   ├── __init__.py
        │   │   ├── ingestion.py
        │   │   ├── processing.py
        │   │   ├── exploration.py     # Remove local REPORTS_DIR, import from config
        │   │   ├── audit.py           # Remove local REPORTS_DIR, import from config
        │   │   ├── schemas.py
        │   │   ├── samples/
        │   │   │   ├── README.md
        │   │   │   ├── SC2EGSet_datasheet.pdf
        │   │   │   ├── process_sample.py
        │   │   │   ├── raw/
        │   │   │   └── processed/
        │   │   ├── sc2_events_extraction.sh
        │   │   ├── sc2_extract_in_game_events.sh
        │   │   └── tests/
        │   │       ├── __init__.py
        │   │       ├── conftest.py
        │   │       ├── test_audit.py
        │   │       ├── test_exploration.py
        │   │       ├── test_ingestion.py
        │   │       └── test_processing.py
        │   ├── reports/                # SC2-specific phase artifacts (tracked)
        │   │   ├── SC2_THESIS_ROADMAP.md   # Renamed from SC2ML_
        │   │   ├── 00_full_ingestion_log.txt
        │   │   ├── 00_join_validation.md
        │   │   ├── 00_map_translation_coverage.csv
        │   │   ├── 00_path_a_smoke_test.md
        │   │   ├── 00_path_b_extraction_log.txt
        │   │   ├── 00_replay_id_spec.md
        │   │   ├── 00_source_audit.json
        │   │   ├── 00_tournament_name_validation.txt
        │   │   ├── 01_apm_mmr_audit.md
        │   │   ├── 01_corpus_summary.json
        │   │   ├── 01_duplicate_detection.md
        │   │   ├── 01_duration_distribution.csv
        │   │   ├── 01_duration_distribution_full.png
        │   │   ├── 01_duration_distribution_zoomed.png
        │   │   ├── 01_event_count_distribution.csv
        │   │   ├── 01_event_density_by_tournament.csv
        │   │   ├── 01_event_density_by_year.csv
        │   │   ├── 01_event_type_inventory.csv
        │   │   ├── 01_parse_quality_by_tournament.csv
        │   │   ├── 01_parse_quality_summary.md
        │   │   ├── 01_patch_landscape.csv
        │   │   ├── 01_player_count_anomalies.csv
        │   │   ├── 01_playerstats_sampling_check.csv
        │   │   ├── 01_result_field_audit.md
        │   │   ├── sanity_validation.md
        │   │   └── archive/           # Old roadmap versions (18+ files)
        │   ├── models/                # SC2 model artifacts (gitignored)
        │   │   └── results/
        │   ├── logs/                  # SC2 pipeline logs (gitignored)
        │   └── tests/                 # SC2 package-root tests (cli, validation)
        │       ├── __init__.py
        │       └── test_cli.py
        │
        ├── aoe2/                      # AoE2 game package (placeholder)
        │   └── .gitkeep               # Mirrors sc2/ when populated
        │
        └── common/                    # Shared evaluation framework (future)
            └── .gitkeep               # Scientific Invariant #10 code goes here
```

---

## Execution Steps

### Step 0 — Create branch

```bash
git checkout -b chore/repo-reorganization
```

---

### Step 1 — Create new directory structure and move Python package

Use `git mv` for all tracked file moves to preserve history.

```bash
# Create rts_predict namespace package
mkdir -p src/rts_predict

# Move the entire sc2ml package to rts_predict/sc2
git mv src/sc2ml src/rts_predict/sc2

# Move aoe2 placeholder
git mv src/aoe2 src/rts_predict/aoe2

# Create common placeholder
mkdir -p src/rts_predict/common
touch src/rts_predict/common/.gitkeep
git add src/rts_predict/common/.gitkeep
```

Create `src/rts_predict/__init__.py`:
```python
"""RTS Predict: Comparative ML analysis for RTS game result prediction."""

__version__ = "0.13.2"
```

---

### Step 2 — Move SC2 reports into game package

```bash
# Create target directory
mkdir -p src/rts_predict/sc2/reports

# Move all phase artifacts
git mv reports/00_* src/rts_predict/sc2/reports/
git mv reports/01_* src/rts_predict/sc2/reports/
git mv reports/sanity_validation.md src/rts_predict/sc2/reports/

# Rename roadmap during move
git mv reports/SC2ML_THESIS_ROADMAP.md src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md

# Move archive
git mv reports/archive src/rts_predict/sc2/reports/archive

# Verify research_log.md remains at reports/
# (reports/ dir stays with just research_log.md)
```

Create gitignored artifact directories:
```bash
mkdir -p src/rts_predict/sc2/models/results
mkdir -p src/rts_predict/sc2/logs
```

---

### Step 3 — User action: move local gitignored files

> **User must run manually** (these are gitignored, not tracked):
> ```bash
> # Move model artifacts
> mv models/*.joblib src/rts_predict/sc2/models/ 2>/dev/null
> mv models/*.pt src/rts_predict/sc2/models/ 2>/dev/null
> mv models/results/* src/rts_predict/sc2/models/results/ 2>/dev/null
>
> # Move logs
> mv logs/sc2_pipeline.log src/rts_predict/sc2/logs/ 2>/dev/null
>
> # Move manifest
> mv in_game_processing_manifest.json src/rts_predict/sc2/ 2>/dev/null
>
> # Remove now-empty root dirs
> rmdir models/results models logs 2>/dev/null
> ```

---

### Step 4 — Update `src/rts_predict/sc2/config.py`

Replace `ROOT_PROJECTS_DIR` with centralized game-aware paths:

**Remove:**
```python
ROOT_PROJECTS_DIR: Path = Path(__file__).resolve().parent.parent.parent
```

**Add:**
```python
# Game-scoped directories (derived from this file's location)
GAME_DIR: Path = Path(__file__).resolve().parent                # src/rts_predict/sc2/
ROOT_DIR: Path = GAME_DIR.parent.parent.parent                  # repo root
REPORTS_DIR: Path = GAME_DIR / "reports"
```

**Update derived paths:**
```python
# Old: IN_GAME_MANIFEST_PATH: Path = ROOT_PROJECTS_DIR / "in_game_processing_manifest.json"
IN_GAME_MANIFEST_PATH: Path = GAME_DIR / "in_game_processing_manifest.json"

# Old: MODELS_DIR: Path = ROOT_PROJECTS_DIR / "models"
MODELS_DIR: Path = GAME_DIR / "models"

# Old: GNN_VIZ_OUTPUT_PATH: Path = ROOT_PROJECTS_DIR / "reports" / "gnn_space_map.png"
GNN_VIZ_OUTPUT_PATH: Path = REPORTS_DIR / "gnn_space_map.png"

# Old: RESULTS_DIR: Path = ROOT_PROJECTS_DIR / "models" / "results"
RESULTS_DIR: Path = MODELS_DIR / "results"
```

---

### Step 5 — Update Python imports in all source files

**Global find-replace patterns (in all `.py` files under `src/rts_predict/sc2/`):**

| Old | New |
|-----|-----|
| `from sc2ml.` | `from rts_predict.sc2.` |
| `import sc2ml.` | `import rts_predict.sc2.` |
| `"sc2ml.` (in test patch strings) | `"rts_predict.sc2.` |

**Files requiring import changes (all under `src/rts_predict/sc2/`):**

1. `cli.py` — 5 import refs: `from rts_predict.sc2.config import ...`, etc.
2. `data/ingestion.py` — 2 import refs
3. `data/processing.py` — 1 import ref
4. `data/audit.py` — 3 import refs + **remove local `REPORTS_DIR` definition (line 29)**, add `REPORTS_DIR` to the config import
5. `data/exploration.py` — 1 import ref + **remove local `REPORTS_DIR` definition (line 26)**, add `REPORTS_DIR` to a new config import
6. `data/samples/process_sample.py` — 1 docstring ref
7. `data/tests/conftest.py` — 1 docstring ref
8. `data/tests/test_audit.py` — 4+ import refs, 2+ patch string refs
9. `data/tests/test_exploration.py` — 20+ import refs, `REPORTS_DIR` patching refs
10. `data/tests/test_ingestion.py` — 15+ import refs, 25+ patch string refs
11. `data/tests/test_processing.py` — 1 import ref
12. `tests/test_cli.py` — 9+ import refs, `_CLI = "rts_predict.sc2.cli"`, `sys.argv` with `"sc2"` (matches new CLI name)

**`src/rts_predict/sc2/__init__.py`:**
- Remove `__version__` (now in `src/rts_predict/__init__.py`)
- Keep/update docstring

---

### Step 6 — Update `pyproject.toml`

```toml
[project.scripts]
# Old: sc2ml = "sc2ml.cli:main"
sc2 = "rts_predict.sc2.cli:main"

[tool.poetry]
# Old: packages = [{include = "sc2ml", from = "src"}]
packages = [{include = "rts_predict", from = "src"}]

[tool.coverage.run]
# Old: source = ["src/sc2ml"]
source = ["src/rts_predict"]
```

---

### Step 7 — Update `.gitignore`

Replace root-level artifact patterns with game-scoped ones:

```gitignore
# Old:
# models/*.joblib
# models/*.pt
# logs/
# in_game_processing_manifest.json

# New — game-scoped artifacts:
src/rts_predict/*/models/*.joblib
src/rts_predict/*/models/*.pt
src/rts_predict/*/logs/
src/rts_predict/*/in_game_processing_manifest.json
```

---

### Step 8 — Update all `.claude/*.md` documentation

Every occurrence of the following patterns must be updated across all `.claude/*.md` files:

| Old pattern | New pattern |
|-------------|-------------|
| `src/sc2ml/` | `src/rts_predict/sc2/` |
| `from sc2ml.` | `from rts_predict.sc2.` |
| `poetry run sc2ml` | `poetry run sc2` |
| `python -m sc2ml.cli` | `python -m rts_predict.sc2.cli` |
| `--cov=sc2ml` | `--cov=rts_predict` |
| `poetry run mypy src/sc2ml/` | `poetry run mypy src/rts_predict/` |
| `reports/SC2ML_THESIS_ROADMAP.md` | `src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md` |
| `reports/00_` | `src/rts_predict/sc2/reports/00_` |
| `reports/01_` | `src/rts_predict/sc2/reports/01_` |
| `reports/archive/` | `src/rts_predict/sc2/reports/archive/` |
| `SC2ML_THESIS_ROADMAP.md` | `SC2_THESIS_ROADMAP.md` (when just filename) |

**Files and specific changes:**

#### `.claude/coding-standards.md`
- Line 7: `poetry run mypy src/sc2ml/` → `poetry run mypy src/rts_predict/`
- Line 42: `src/sc2ml/` → `src/rts_predict/sc2/`
- Line 43: `from sc2ml.* import ...` → `from rts_predict.sc2.* import ...`

#### `.claude/git-workflow.md`
- Line 37: `--cov=sc2ml` → `--cov=rts_predict`
- Lines 87, 99: `src/sc2ml/__init__.py` → `src/rts_predict/__init__.py`
- Line 122: `--cov=sc2ml` → `--cov=rts_predict`
- Line 124: `poetry run mypy src/sc2ml/` → `poetry run mypy src/rts_predict/`

#### `.claude/project-architecture.md`
- **Major rewrite**: update entire Package Layout section to match new tree
- All path references throughout
- Line 213: `reports/SC2ML_THESIS_ROADMAP.md` → `src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md`
- Directories section: update `reports/`, `models/`, `logs/` to new locations

#### `.claude/python-workflow.md`
- Line 13: `poetry run python -m sc2ml.cli` → `poetry run python -m rts_predict.sc2.cli`
- Line 14: `--cov=sc2ml` → `--cov=rts_predict`
- Line 16: `poetry run mypy src/sc2ml/` → `poetry run mypy src/rts_predict/`

#### `.claude/testing-standards.md`
- Line 7: `--cov=sc2ml` → `--cov=rts_predict`
- Lines 20-32, 38: All `src/sc2ml/` → `src/rts_predict/sc2/`

#### `.claude/scientific-invariants.md`
- Line 87: `SC2ML_THESIS_ROADMAP.md` → `SC2_THESIS_ROADMAP.md`

#### `.claude/ml-protocol.md`
- Line 28: `log results in reports/` → `log results in the game-specific reports directory (e.g. src/rts_predict/sc2/reports/)`
- Line 47: `reports/research_log.md` — **keep as-is** (stays at root)
- Line 54: `reports/archive/XX_run.md` → `src/rts_predict/sc2/reports/archive/XX_run.md`

#### `.claude/thesis-writing.md`
- Line 92-93: `reports/01_duration_distribution_full.png` → `src/rts_predict/sc2/reports/01_duration_distribution_full.png`
- Line 113: `report artifacts (CSVs, PNGs, MDs in reports/)` → update path guidance
- Lines 262-296 (phase-to-section mapping): update report dir references

---

### Step 9 — Update `CLAUDE.md`

Every reference pattern listed in Step 8, plus:

- Package Layout section: describe `src/rts_predict/` with sub-packages
- All command examples: `poetry run sc2`, `--cov=rts_predict`, `mypy src/rts_predict/`
- Test location description: `src/rts_predict/sc2/<subpkg>/tests/`
- Version bump path: `src/rts_predict/__init__.py`
- Roadmap reference: `src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md`
- Report paths in progress tracking section

---

### Step 10 — Update `README.md`

- Command examples: `poetry run sc2 --help`, `--cov=rts_predict`
- Roadmap reference
- Any structural description

---

### Step 11 — Update `CHANGELOG.md`

- Add this work under `[Unreleased]` section
- **Historical entries**: Add a single note at the top of the changelog:
  > Note: Entries before v0.14.0 reference the old `sc2ml` package name and
  > root-level `reports/` paths. See the repo reorganization in v0.14.0.
- Do NOT rewrite historical entries — they are records of what happened at that time

---

### Step 12 — Update `reports/research_log.md`

- Add a dated entry documenting this reorganization
- Update path references in existing entries that Claude would use for context
  (recent entries from Phase 0 and Phase 1 that reference `reports/` paths)
- Add `[SC2]` tags to existing entries for consistency with new convention

---

### Step 13 — Update `thesis/THESIS_STRUCTURE.md`

- Line 19: `SC2ML roadmap phases` → `SC2 roadmap phases`
- Any `reports/` path references → `src/rts_predict/sc2/reports/`

---

### Step 14 — Clean up old root directories

```bash
# Remove old src/sc2ml (now at src/rts_predict/sc2/)
# (should be empty after git mv)

# Remove old src/aoe2 (now at src/rts_predict/aoe2/)
# (should be empty after git mv)

# Remove old root models/ dir (gitignored files moved in Step 3)
# (user does this manually since contents are gitignored)

# Remove old root logs/ dir (same)
```

---

### Step 15 — Reinstall package and regenerate lock

```bash
poetry lock --no-update
poetry install
```

---

## Verification

After all changes:

```bash
# 1. Tests pass
poetry run pytest tests/ src/ -v --cov=rts_predict --cov-report=term-missing

# 2. Linting clean
poetry run ruff check src/ tests/

# 3. Type checking clean
poetry run mypy src/rts_predict/

# 4. CLI works
poetry run sc2 --help

# 5. Verify no orphaned sc2ml references remain
grep -r "sc2ml" src/ tests/ --include="*.py" | grep -v __pycache__
grep -r "sc2ml" .claude/ CLAUDE.md README.md --include="*.md"
# (CHANGELOG.md historical entries and research_log.md old entries are expected exceptions)

# 6. Verify report artifacts are in new location
ls src/rts_predict/sc2/reports/00_source_audit.json
ls src/rts_predict/sc2/reports/SC2_THESIS_ROADMAP.md

# 7. Verify Python imports resolve
poetry run python -c "from rts_predict.sc2.config import GAME_DIR; print(GAME_DIR)"
```

---

## Scope Confirmation

This chore **DOES**:
- Rename `sc2ml` → `rts_predict.sc2` (Python package + all references)
- Move SC2 reports, models, logs, manifest into `src/rts_predict/sc2/`
- Create `rts_predict.aoe2` and `rts_predict.common` placeholders
- Centralize `REPORTS_DIR` in config.py (removes duplicate definitions in audit.py/exploration.py)
- Rename `SC2ML_THESIS_ROADMAP.md` → `SC2_THESIS_ROADMAP.md`
- Update CLI entry point from `sc2ml` to `sc2`
- Update all `.md` documentation references

This chore does **NOT**:
- Change any business logic, SQL queries, or test assertions
- Modify thesis chapter content
- Add new features or fix bugs
- Change DuckDB database paths or external data paths
- Create `ARCHITECTURE.md` (planned as a follow-up session)
- Add new tests (existing tests are updated for new import paths only)

---

## Follow-up: ARCHITECTURE.md

This reorganization sets the foundation for a formal `ARCHITECTURE.md` to be written
in a follow-up planning session. That document would describe:
- The `rts_predict` package structure and how to add a new game
- Per-game directory contracts (what each game package must contain)
- Shared evaluation protocol location and interface
- Artifact directory conventions (reports, models, logs)
- How the thesis writing workflow integrates with the per-game structure
