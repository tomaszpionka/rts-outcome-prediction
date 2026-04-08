# Chore: Migrate Report Artifacts to artifacts/ Subdirectory

**Category:** C — Chore
**Branch:** `chore/artifacts-subdir-migration`
**Today's date:** 2026-04-08

## Context

The `reports/<dataset>/` directories contain a flat mix of two kinds of files:
- **Documentation** (`ROADMAP.md`, `INVARIANTS.md`, `SUPERSEDED.md`, `.yaml`, `.gitkeep`, `archive/`) — hand-authored, stay in place
- **Artifacts** (any file whose name starts with the `XX_XX_` numeric step prefix) — machine-generated outputs, regardless of extension (`.json`, `.csv`, `.txt`, `.png`, `.md`)

All artifact files move into a new `artifacts/` subdirectory. The rule is purely naming-based: `XX_XX_*` prefix = artifact. This affects 54 files across 3 datasets.

Scope:
- `sc2/reports/sc2egset/` (36 artifacts: 26 non-MD + 10 MD)
- `aoe2/reports/aoe2companion/` (10 artifacts: 2 non-MD + 8 MD)
- `aoe2/reports/aoestats/` (8 artifacts: 1 non-MD + 7 MD)

The simplifying consequence: **all** writer functions that produce numbered step outputs now use a single `DATASET_ARTIFACTS_DIR` constant — no split between MD and non-MD paths needed.

---

## Inventory

### Artifact files to move (54 total)

**SC2EGSet (36 files):**

| Old path (repo-relative) | New path |
|---|---|
| `src/rts_predict/sc2/reports/sc2egset/00_01_source_audit.json` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_01_source_audit.json` |
| `src/rts_predict/sc2/reports/sc2egset/00_02_tournament_name_validation.txt` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_02_tournament_name_validation.txt` |
| `src/rts_predict/sc2/reports/sc2egset/00_03_replay_id_spec.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_03_replay_id_spec.md` |
| `src/rts_predict/sc2/reports/sc2egset/00_04_path_a_smoke_test.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_04_path_a_smoke_test.md` |
| `src/rts_predict/sc2/reports/sc2egset/00_05_full_ingestion_log.txt` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_05_full_ingestion_log.txt` |
| `src/rts_predict/sc2/reports/sc2egset/00_07_path_b_extraction_log.txt` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_07_path_b_extraction_log.txt` |
| `src/rts_predict/sc2/reports/sc2egset/00_08_join_validation.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_08_join_validation.md` |
| `src/rts_predict/sc2/reports/sc2egset/00_09_map_translation_coverage.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/00_09_map_translation_coverage.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_01_corpus_summary.json` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01_corpus_summary.json` |
| `src/rts_predict/sc2/reports/sc2egset/01_01_duplicate_detection.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01_duplicate_detection.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_01_player_count_anomalies.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01_player_count_anomalies.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_01_result_field_audit.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01_result_field_audit.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_02_parse_quality_by_tournament.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_02_parse_quality_by_tournament.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_02_parse_quality_summary.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_02_parse_quality_summary.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_03_duration_distribution.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution_full.png` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_03_duration_distribution_full.png` |
| `src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution_short_tail.png` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_03_duration_distribution_short_tail.png` |
| `src/rts_predict/sc2/reports/sc2egset/01_04_apm_mmr_audit.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_04_apm_mmr_audit.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_05_patch_landscape.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_05_patch_landscape.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_06_event_count_distribution.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_06_event_count_distribution.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_06_event_density_by_tournament.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_06_event_density_by_tournament.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_06_event_density_by_year.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_06_event_density_by_year.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_06_event_type_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_06_event_type_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_07_playerstats_sampling_check.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_07_playerstats_sampling_check.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_08_error_flags_audit.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_08_error_flags_audit.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_08_game_settings_audit.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_08_game_settings_audit.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_09D_playerstats_stats_field_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09D_playerstats_stats_field_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09D_tracker_event_data_field_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09D_tracker_event_data_field_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09D_tracker_event_data_key_constancy.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09D_tracker_event_data_key_constancy.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09E_game_event_data_field_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09E_game_event_data_field_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09E_game_event_data_key_constancy.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09E_game_event_data_key_constancy.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09F_event_schema_reference.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09F_event_schema_reference.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_09F_parquet_duckdb_schema_reconciliation.md` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09F_parquet_duckdb_schema_reconciliation.md` |
| `src/rts_predict/sc2/reports/sc2egset/01_09_toplevel_field_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09_toplevel_field_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09_tpdm_field_inventory.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09_tpdm_field_inventory.csv` |
| `src/rts_predict/sc2/reports/sc2egset/01_09_tpdm_key_set_constancy.csv` | `src/rts_predict/sc2/reports/sc2egset/artifacts/01_09_tpdm_key_set_constancy.csv` |

**AoE2 Companion (10 files):**

| Old path | New path |
|---|---|
| `src/rts_predict/aoe2/reports/aoe2companion/00_01_source_audit.json` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_01_source_audit.json` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_01_source_audit.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_01_source_audit.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_02_match_schema_profile.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_02_match_schema_profile.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_03_dtype_decision.json` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_03_dtype_decision.json` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_03_rating_schema_profile.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_03_rating_schema_profile.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_04_singleton_schema_profile.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_04_singleton_schema_profile.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_05_smoke_test.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_05_smoke_test.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_06_ingestion_log.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_06_ingestion_log.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_07_rowcount_reconciliation.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_07_rowcount_reconciliation.md` |
| `src/rts_predict/aoe2/reports/aoe2companion/00_08_phase0_summary.md` | `src/rts_predict/aoe2/reports/aoe2companion/artifacts/00_08_phase0_summary.md` |

**AoE2 Stats (8 files):**

| Old path | New path |
|---|---|
| `src/rts_predict/aoe2/reports/aoestats/00_01_source_audit.json` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_01_source_audit.json` |
| `src/rts_predict/aoe2/reports/aoestats/00_01_source_audit.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_01_source_audit.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_02_match_schema_profile.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_02_match_schema_profile.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_03_player_schema_profile.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_03_player_schema_profile.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_04_smoke_test.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_04_smoke_test.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_05_ingestion_log.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_05_ingestion_log.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_06_rowcount_reconciliation.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_06_rowcount_reconciliation.md` |
| `src/rts_predict/aoe2/reports/aoestats/00_07_phase0_summary.md` | `src/rts_predict/aoe2/reports/aoestats/artifacts/00_07_phase0_summary.md` |

**Not moved (stay in place):** `ROADMAP.md`, `INVARIANTS.md`, `SUPERSEDED.md`, `ARCHIVE_SUMMARY.md`, `aoe2companion_download_report.md` (no numeric prefix), all `.yaml` files, all `.gitkeep` files, and the `archive/` subdirectory.

---

### Writer functions to update

**`src/rts_predict/sc2/config.py`**
- Add: `DATASET_ARTIFACTS_DIR: Path = DATASET_REPORTS_DIR / "artifacts"`

**`src/rts_predict/aoe2/config.py`**
- Add: `AOE2COMPANION_ARTIFACTS_DIR: Path = AOE2COMPANION_REPORTS_DIR / "artifacts"`
- Add: `AOESTATS_ARTIFACTS_DIR: Path = AOESTATS_REPORTS_DIR / "artifacts"`

**`src/rts_predict/sc2/data/audit.py`** — ALL numbered-file writers change to `DATASET_ARTIFACTS_DIR`:
- Line 18: add `DATASET_ARTIFACTS_DIR` to import
- Line 90: `run_source_audit()` — writes `00_01_source_audit.json`
- Line 142: `validate_tournament_name_extraction()` — writes `00_02_tournament_name_validation.txt`
- Line 219: `write_replay_id_spec()` — writes `00_03_replay_id_spec.md` *(was "no change" — now updates)*
- Line 324: `run_path_a_smoke_test()` — writes `00_04_path_a_smoke_test.md` *(was "no change" — now updates)*
- Line 367: `run_full_ingestion()` — reads `00_01_source_audit.json`
- Line 385: `run_full_ingestion()` — writes `00_05_full_ingestion_log.txt`
- Line 464: `run_path_b_extraction()` — writes `00_07_path_b_extraction_log.txt`
- Line 500: `validate_path_a_b_join()` — reads `00_01_source_audit.json`; writes `00_08_join_validation.md` *(MD write was "no change" — now updates)*
- Line 516: `validate_path_a_b_join()` — writes `00_08_join_validation.md` (confirm exact line)
- Line 583: `validate_map_translation_coverage()` — writes `00_09_map_translation_coverage.csv`

**`src/rts_predict/sc2/data/exploration.py`** — ALL functions writing numbered outputs use `DATASET_ARTIFACTS_DIR`. No `report_dir` split needed — this is the key simplification over the original plan.

Add `DATASET_ARTIFACTS_DIR` to import, then change default `out = output_dir or DATASET_REPORTS_DIR` → `out = output_dir or DATASET_ARTIFACTS_DIR` for every function listed:

| Function (~line) | Outputs |
|---|---|
| `run_corpus_summary()` (651) | `.json`, `.csv`, `.md`, `.md` |
| `run_parse_quality_by_tournament()` (827) | `.csv`, `.md` |
| `run_duration_distribution()` (877) | `.csv`, `.png`, `.png` |
| `run_apm_mmr_audit()` (917) | `.md` *(was "no change" — now updates)* |
| `run_patch_landscape()` (987) | `.csv` |
| `run_event_type_inventory()` (1004) | `.csv` ×4 |
| `run_playerstats_sampling_check()` (1049) | `.csv` |
| `run_tpdm_field_inventory()` (1140) | `.csv` |
| `run_tpdm_key_set_constancy()` (1170) | `.csv` |
| `run_toplevel_field_inventory()` (1223) | `.csv` |
| `run_tracker_event_data_inventory()` (1450) | `.csv` ×3 |
| `run_game_event_data_inventory()` (1552) | `.csv` ×2 |
| `run_parquet_duckdb_reconciliation()` (1857) | `.md` *(was "no change" — now updates)* |
| `run_event_schema_document()` (1966) | reads `.csv` ×4, writes `.md` — all in same `out` dir |

**`src/rts_predict/aoe2/data/aoe2companion/audit.py`** — functions receive `reports_dir` parameter; all numbered outputs go to `reports_dir / "artifacts"`:
- `run_source_audit()` (~line 210): writes `00_01_source_audit.json`, `00_01_source_audit.md` → `reports_dir / "artifacts" / ...` + `mkdir(parents=True, exist_ok=True)`
- All other numbered-output functions: same pattern (grep for `reports_dir /` + a `"00_` filename)
- `profile_rating_schema()` (~line 629): writes `00_03_dtype_decision.json` → `reports_dir / "artifacts" / ...`
- `run_phase0_pipeline()` (~line 1540): reads `00_03_dtype_decision.json` → `reports_dir / "artifacts" / ...`

> Note: The AoE2 companion has many more numbered MD outputs (`00_02_` through `00_08_`). Search for every `reports_dir / "00_` occurrence in the file and redirect to `reports_dir / "artifacts" / ...`.

**`src/rts_predict/aoe2/data/aoestats/audit.py`** — same pattern:
- All `reports_dir / "00_` occurrences → `reports_dir / "artifacts" / ...`

---

### Reference files to update

**`src/rts_predict/sc2/reports/sc2egset/ROADMAP.md`** (~50+ lines)
- All `Output:` and `Artifacts:` list items referencing numbered filenames (any extension): prefix with `artifacts/`
- `Feeding artifacts:` sections: same
- Named docs (`INVARIANTS.md`, `ROADMAP.md`, etc.) referenced in prose: no change

**`src/rts_predict/sc2/reports/sc2egset/SUPERSEDED.md`**
- Same mechanical replacement for all numbered artifact names

**`CHANGELOG.md`**
- Any full path containing `sc2egset/0` or `sc2egset/1` for non-`artifacts/` entries: add `artifacts/`
- Known: line 68 `sc2egset/01_08_error_flags_audit.csv` and line 67 `sc2egset/01_08_game_settings_audit.md`

**`ARCHITECTURE.md`** (~line 39 area)
- Update game package contract table:
  - Old: `| \`reports/<dataset>/\` | Dataset-scoped phase artifacts | Per dataset |`
  - New two rows: `reports/<dataset>/` for named docs (ROADMAP, INVARIANTS, etc.); `reports/<dataset>/artifacts/` for machine-generated step outputs (`XX_XX_*`)

**`reports/research_log.md`**
- All occurrences of `sc2egset/0` or `sc2egset/1` without `artifacts/` in the path: add `artifacts/`

**`reports/_archive/research_log_pre_notebook_sandbox.md`**
- Same scan-and-prefix for all numbered artifact paths

**`sandbox/sc2/sc2egset/01_08_game_settings_audit.py`**
- Update comment/path strings referencing `sc2egset/01_08_*` outputs

**`sandbox/sc2/sc2egset/01_08_game_settings_audit.ipynb`**
- Corresponding cell sources

**Claude config files:** None need updating (confirmed: no numbered artifact paths in `.claude/*.md`).

---

## Steps

### Step 1 — Create artifacts/ subdirectories

```bash
mkdir -p src/rts_predict/sc2/reports/sc2egset/artifacts/
mkdir -p src/rts_predict/aoe2/reports/aoe2companion/artifacts/
mkdir -p src/rts_predict/aoe2/reports/aoestats/artifacts/
```

**Gate 1:** `ls -d src/rts_predict/*/reports/*/artifacts/` shows all three directories.

---

### Step 2 — Move artifact files (git mv)

```bash
# SC2EGSet (36 files)
git mv src/rts_predict/sc2/reports/sc2egset/00_01_source_audit.json src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_02_tournament_name_validation.txt src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_03_replay_id_spec.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_04_path_a_smoke_test.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_05_full_ingestion_log.txt src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_07_path_b_extraction_log.txt src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_08_join_validation.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/00_09_map_translation_coverage.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_01_corpus_summary.json src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_01_duplicate_detection.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_01_player_count_anomalies.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_01_result_field_audit.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_02_parse_quality_by_tournament.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_02_parse_quality_summary.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution_full.png src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_03_duration_distribution_short_tail.png src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_04_apm_mmr_audit.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_05_patch_landscape.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_06_event_count_distribution.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_06_event_density_by_tournament.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_06_event_density_by_year.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_06_event_type_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_07_playerstats_sampling_check.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_08_error_flags_audit.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_08_game_settings_audit.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09D_playerstats_stats_field_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09D_tracker_event_data_field_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09D_tracker_event_data_key_constancy.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09E_game_event_data_field_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09E_game_event_data_key_constancy.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09F_event_schema_reference.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09F_parquet_duckdb_schema_reconciliation.md src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09_toplevel_field_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09_tpdm_field_inventory.csv src/rts_predict/sc2/reports/sc2egset/artifacts/
git mv src/rts_predict/sc2/reports/sc2egset/01_09_tpdm_key_set_constancy.csv src/rts_predict/sc2/reports/sc2egset/artifacts/

# AoE2 Companion (10 files)
git mv src/rts_predict/aoe2/reports/aoe2companion/00_01_source_audit.json src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_01_source_audit.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_02_match_schema_profile.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_03_dtype_decision.json src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_03_rating_schema_profile.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_04_singleton_schema_profile.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_05_smoke_test.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_06_ingestion_log.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_07_rowcount_reconciliation.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/
git mv src/rts_predict/aoe2/reports/aoe2companion/00_08_phase0_summary.md src/rts_predict/aoe2/reports/aoe2companion/artifacts/

# AoE2 Stats (8 files)
git mv src/rts_predict/aoe2/reports/aoestats/00_01_source_audit.json src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_01_source_audit.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_02_match_schema_profile.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_03_player_schema_profile.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_04_smoke_test.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_05_ingestion_log.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_06_rowcount_reconciliation.md src/rts_predict/aoe2/reports/aoestats/artifacts/
git mv src/rts_predict/aoe2/reports/aoestats/00_07_phase0_summary.md src/rts_predict/aoe2/reports/aoestats/artifacts/
```

**Gate 2:**
- `find src/rts_predict/*/reports/*/ -maxdepth 1 -type f -name '[0-9][0-9]_*'` returns 0 results
- `find src/rts_predict/*/reports/*/artifacts/ -type f | wc -l` returns 54

---

### Step 3 — Update config constants

**`src/rts_predict/sc2/config.py`:** Add after `DATASET_REPORTS_DIR`:
```python
DATASET_ARTIFACTS_DIR: Path = DATASET_REPORTS_DIR / "artifacts"
```

**`src/rts_predict/aoe2/config.py`:** Add after `AOESTATS_REPORTS_DIR`:
```python
AOE2COMPANION_ARTIFACTS_DIR: Path = AOE2COMPANION_REPORTS_DIR / "artifacts"
AOESTATS_ARTIFACTS_DIR: Path = AOESTATS_REPORTS_DIR / "artifacts"
```

**Gate 3:**
```bash
poetry run python -c "from rts_predict.sc2.config import DATASET_ARTIFACTS_DIR; print(DATASET_ARTIFACTS_DIR)"
# must end in sc2egset/artifacts
poetry run python -c "from rts_predict.aoe2.config import AOE2COMPANION_ARTIFACTS_DIR, AOESTATS_ARTIFACTS_DIR; print(AOE2COMPANION_ARTIFACTS_DIR); print(AOESTATS_ARTIFACTS_DIR)"
```

---

### Step 4 — Update SC2 audit.py writer functions

Edit `src/rts_predict/sc2/data/audit.py`:
1. Add `DATASET_ARTIFACTS_DIR` to the import
2. Change **all** `DATASET_REPORTS_DIR` references that build numbered filenames to use `DATASET_ARTIFACTS_DIR`:
   - `run_source_audit()` → `00_01_source_audit.json`
   - `validate_tournament_name_extraction()` → `00_02_tournament_name_validation.txt`
   - `write_replay_id_spec()` → `00_03_replay_id_spec.md`
   - `run_path_a_smoke_test()` → `00_04_path_a_smoke_test.md`
   - `run_full_ingestion()` → reads `00_01_source_audit.json`; writes `00_05_full_ingestion_log.txt`
   - `run_path_b_extraction()` → `00_07_path_b_extraction_log.txt`
   - `validate_path_a_b_join()` → reads `00_01_source_audit.json`; writes `00_08_join_validation.md`
   - `validate_map_translation_coverage()` → `00_09_map_translation_coverage.csv`
3. `DATASET_REPORTS_DIR` should have **zero** remaining references in the file after this step

**Gate 4:**
```bash
poetry run ruff check src/rts_predict/sc2/data/audit.py
grep -n "DATASET_REPORTS_DIR" src/rts_predict/sc2/data/audit.py
# must return 0 results
```

---

### Step 5 — Update SC2 exploration.py writer functions

Edit `src/rts_predict/sc2/data/exploration.py`:
1. Add `DATASET_ARTIFACTS_DIR` to the import; remove `DATASET_REPORTS_DIR` from import if no longer used
2. For every function, change `out = output_dir or DATASET_REPORTS_DIR` → `out = output_dir or DATASET_ARTIFACTS_DIR`
3. No `report_dir` split needed — all numbered outputs (MD, CSV, JSON, PNG) go to `out`
4. `run_event_schema_document()`: reads CSV inputs and writes MD output all using `out = output_dir or DATASET_ARTIFACTS_DIR`

**Gate 5:**
```bash
poetry run ruff check src/rts_predict/sc2/data/exploration.py
grep -n "DATASET_REPORTS_DIR" src/rts_predict/sc2/data/exploration.py
# must return 0 results
```

---

### Step 6 — Update AoE2 writer functions

Edit `src/rts_predict/aoe2/data/aoe2companion/audit.py`:
- Find every occurrence of `reports_dir / "00_` and change to `reports_dir / "artifacts" / "00_`
- Before any first write per function, add: `(reports_dir / "artifacts").mkdir(parents=True, exist_ok=True)`
- Also update reads: `run_phase0_pipeline()` reads `00_03_dtype_decision.json` → update path

Edit `src/rts_predict/aoe2/data/aoestats/audit.py`:
- Same: find every `reports_dir / "00_` and redirect to `reports_dir / "artifacts" / "00_`

**Gate 6:**
```bash
poetry run ruff check src/rts_predict/aoe2/
grep -n 'reports_dir / "00_' src/rts_predict/aoe2/data/aoe2companion/audit.py
grep -n 'reports_dir / "00_' src/rts_predict/aoe2/data/aoestats/audit.py
# both must return 0 results
```

---

### Step 7 — Update tests

**`tests/rts_predict/sc2/data/test_audit.py`:**
- For each test monkeypatching `DATASET_REPORTS_DIR`, also patch `DATASET_ARTIFACTS_DIR` to `tmp_path / "reports" / "artifacts"` (mkdir it in fixture)
- All numbered output assertions (`.json`, `.csv`, `.txt`, `.md`) now at `tmp_path / "reports" / "artifacts" / filename`

**`tests/rts_predict/sc2/data/test_exploration.py`:**
- Same pattern: patch `DATASET_ARTIFACTS_DIR`; update ALL output assertions to `artifacts/` path
- No `report_dir` parameter changes needed (that split was dropped)

**`tests/rts_predict/aoe2/data/aoe2companion/test_audit.py`:**
- Update all output assertions: `reports_dir / "00_X"` → `reports_dir / "artifacts" / "00_X"`

**`tests/rts_predict/aoe2/data/aoestats/test_audit.py`:**
- Same pattern

**Gate 7:**
```bash
poetry run pytest tests/ -v --cov --cov-report=term-missing
# All tests pass; coverage does not decrease from current baseline
```

---

### Step 8 — Update reference files

**`src/rts_predict/sc2/reports/sc2egset/ROADMAP.md`** (~60+ lines)
- All `Output:` and `Artifacts:` list items with numbered filenames: prefix with `artifacts/` (all extensions, including `.md`)
- `Feeding artifacts:` sections: same rule
- Named docs in prose (`INVARIANTS.md`, `ROADMAP.md`): no change

**`src/rts_predict/sc2/reports/sc2egset/SUPERSEDED.md`**
- Same mechanical replacement for all numbered artifact names

**`CHANGELOG.md`**
- All full paths to numbered SC2EGSet artifacts (any extension): add `artifacts/` before the step-numbered filename

**`ARCHITECTURE.md`** (~line 39 area)
- Update game package contract table — replace the single `reports/<dataset>/` row with two rows:
  - `reports/<dataset>/` — named documentation files (`ROADMAP.md`, `INVARIANTS.md`, etc.)
  - `reports/<dataset>/artifacts/` — machine-generated step outputs (`XX_XX_*`, any extension)

**`reports/research_log.md`**
- All paths to numbered SC2EGSet artifact files: add `artifacts/`

**`reports/_archive/research_log_pre_notebook_sandbox.md`**
- Same scan-and-prefix for all numbered artifact paths

**`sandbox/sc2/sc2egset/01_08_game_settings_audit.py`**
- Update output path strings for both `.md` and `.csv` outputs to include `artifacts/`

**`sandbox/sc2/sc2egset/01_08_game_settings_audit.ipynb`**
- Corresponding cell sources

**Gate 8:**
```bash
# Every numbered step artifact path must now include artifacts/
find src/rts_predict/*/reports/*/ -maxdepth 1 -name '[0-9][0-9]_*' -type f
# must return 0 results — no numbered files at the dataset root level

# Verify no stale references in source code or docs
grep -rn "reports/sc2egset/[0-9]" src/ reports/ sandbox/ CHANGELOG.md ARCHITECTURE.md .claude/ docs/ \
  | grep -v "artifacts/"
# must return 0 results
```

---

### Step 9 — Full suite + lint + type check

```bash
poetry run pytest tests/ -v --cov --cov-report=term-missing
poetry run ruff check src/ tests/
poetry run mypy src/rts_predict/
```

**Gate 9:** All tests pass. No lint errors. No type errors. Coverage ≥ 95%.

---

## Risk notes

1. **No `report_dir` split needed** — all writer functions use a single `DATASET_ARTIFACTS_DIR` constant. This is simpler than the original plan.
2. **AoE2 writer functions** use an explicit `reports_dir` parameter rather than a module-level constant; the `mkdir` guard must be added to each one individually.
3. **ROADMAP.md is 1600+ lines.** Use targeted regex replacements per filename extension; also cover `.md` artifact names (previously excluded).
4. **Future artifact functions** (Steps 1.10–1.16) will naturally use `DATASET_ARTIFACTS_DIR` — no second migration needed.

## Rollback

```bash
# If uncommitted:
git checkout -- src/ tests/ reports/ sandbox/ CHANGELOG.md ARCHITECTURE.md

# If committed:
git reset --hard HEAD~1
```

---

## Key files touched

| File | Change |
|---|---|
| `src/rts_predict/sc2/config.py` | Add `DATASET_ARTIFACTS_DIR` constant |
| `src/rts_predict/aoe2/config.py` | Add `AOE2COMPANION_ARTIFACTS_DIR`, `AOESTATS_ARTIFACTS_DIR` |
| `src/rts_predict/sc2/data/audit.py` | All `DATASET_REPORTS_DIR` → `DATASET_ARTIFACTS_DIR` (11 refs) |
| `src/rts_predict/sc2/data/exploration.py` | All `DATASET_REPORTS_DIR` → `DATASET_ARTIFACTS_DIR` (~14 functions) |
| `src/rts_predict/aoe2/data/aoe2companion/audit.py` | All `reports_dir / "00_` → `reports_dir / "artifacts" / "00_` |
| `src/rts_predict/aoe2/data/aoestats/audit.py` | Same |
| `tests/rts_predict/sc2/data/test_audit.py` | Patch new constant; update all numbered output assertions |
| `tests/rts_predict/sc2/data/test_exploration.py` | Same |
| `tests/rts_predict/aoe2/data/aoe2companion/test_audit.py` | Update assertions |
| `tests/rts_predict/aoe2/data/aoestats/test_audit.py` | Update assertions |
| `src/rts_predict/sc2/reports/sc2egset/ROADMAP.md` | ~60 lines: prefix ALL numbered artifact names |
| `src/rts_predict/sc2/reports/sc2egset/SUPERSEDED.md` | ~20 lines |
| `CHANGELOG.md` | Numbered artifact path lines |
| `ARCHITECTURE.md` | 3 lines |
| `reports/research_log.md` | Numbered artifact path lines |
| `reports/_archive/research_log_pre_notebook_sandbox.md` | ~10 lines |
| `sandbox/sc2/sc2egset/01_08_game_settings_audit.py` | 2 lines |
| `sandbox/sc2/sc2egset/01_08_game_settings_audit.ipynb` | 2 cells |
