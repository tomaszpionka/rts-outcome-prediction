# Research Log

Thesis: "A comparative analysis of methods for predicting game results
in real-time strategy games, based on the examples of StarCraft II and
Age of Empires II."

Reverse chronological entries.

> **Phase migration note (2026-04-09):** This log was reset as part of the
> Phase 01-07 migration. Prior entries are archived at
> `reports/archive/research_log_pre_phase_migration.md` and
> `reports/archive/research_log_pre_notebook_sandbox.md`.
> All new entries use the Phase XX / Step XX_YY_ZZ format per docs/PHASES.md.

---

## 2026-04-09 — [Phase 01 / Step 01_01_01] File Inventory (all 3 datasets)

**Category:** A (science)
**Dataset:** sc2egset, aoe2companion, aoestats
**Artifacts produced:**
- `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01/01_01_01_file_inventory.json`
- `src/rts_predict/sc2/reports/sc2egset/artifacts/01_01/01_01_01_file_inventory.md`
- `src/rts_predict/aoe2/reports/aoe2companion/artifacts/01_01/01_01_01_file_inventory.json`
- `src/rts_predict/aoe2/reports/aoe2companion/artifacts/01_01/01_01_01_file_inventory.md`
- `src/rts_predict/aoe2/reports/aoestats/artifacts/01_01/01_01_01_file_inventory.json`
- `src/rts_predict/aoe2/reports/aoestats/artifacts/01_01/01_01_01_file_inventory.md`

### What
Ran `inventory_directory()` on the raw directory of each dataset. Produced
per-subdirectory file counts, sizes, and extension distributions. For
aoe2companion and aoestats, extracted dates from filenames and checked for
gaps. For aoestats, compared paired directories.

### Why
Step 01_01_01 is the first step of Phase 01 Data Exploration. Before any
DuckDB ingestion can be designed, we need an authoritative inventory of
what files exist. Per Scientific Invariant 6, these counts must be produced
by auditable code.

### How (reproducibility)
Each notebook calls `inventory_directory(RAW_DIR)` from
`rts_predict.common.inventory` and writes the result to JSON and Markdown
artifacts. The notebooks are the reproducibility record.

### Findings

**sc2egset:** 432 total files across 70 tournament subdirectories + 4 files
at root. Total size: 10,699.21 MB (~10.4 GB). Each subdirectory contains
3 `.json` files (replay data), 1 `.zip` archive, 2 `.log` files, and
optionally 1 extension-less file. No subdirectory has 0 `.json` files.
Tournament coverage spans 2016 to 2024. Files per subdir range from 6 to 7;
median is 6.0.

**aoe2companion:** 4,154 total files across 4 subdirectories + 3 files at
root. Total size: 9,388.27 MB (~9.2 GB). Breakdown:
- `matches/`: 2,074 files (1 no-ext + 2,073 `.parquet`), 6,621.52 MB
- `ratings/`: 2,073 files (1 no-ext + 2,072 `.csv`), 2,519.59 MB
- `leaderboards/`: 2 files (1 no-ext + 1 `.parquet`), 83.32 MB (snapshot)
- `profiles/`: 2 files (1 no-ext + 1 `.parquet`), 161.84 MB (snapshot)
Date range for matches: 2020-08-01 to 2026-04-04, 2,073 daily files, no gaps.
Date range for ratings: 2020-08-01 to 2026-04-04, 2,072 daily files, 1 gap
(2025-07-10 to 2025-07-12, 2 days).

**aoestats:** 349 total files across 3 subdirectories + 2 files at root.
Total size: 3,773.43 MB (~3.7 GB). Breakdown:
- `matches/`: 173 files (1 no-ext + 172 `.parquet`), 610.55 MB
- `players/`: 172 files (1 no-ext + 171 `.parquet`), 3,162.86 MB
- `overview/`: 2 files (1 no-ext + 1 `.json`), 0.02 MB
Date range for both matches and players: 2022-08-28 to 2026-02-07.
matches: 172 weekly files, 3 gaps (43 days, 8 days, 8 days).
players: 171 weekly files (1 missing — documented download failure for
2025-11-16_2025-11-22), same 3 gaps plus an 8-day gap confirming the
missing file.
Paired comparison (matches vs players): count_match=False (172 vs 171),
date_range_match=True. The asymmetry is the known missing file.

### What this means
All three raw directories are non-empty and structurally sound. The sc2egset
layout (one directory per tournament, 3 JSON files each) is uniform and
ready for schema inspection. The aoe2companion matches directory is daily
and complete (no gaps). The ratings directory has one 2-day gap in July 2025.
The aoestats asymmetry (172 match files vs 171 player files) is consistent
with the documented download failure already noted in the ROADMAP source data
section — this is not a new finding.

### Decisions taken
- None — observation only.

### Decisions deferred
- Ingestion strategy depends on what we find in schema discovery (01_01_02/03).

### Thesis mapping
- Chapter 3 — Data & Methodology > 3.1 Data Sources

### Open questions / follow-ups
- sc2egset: The 4 files at root and the extension-less files within some
  subdirectories should be inspected in 01_01_02 schema discovery.
- aoe2companion: The ratings 2-day gap (2025-07-10 to 2025-07-12) is minor
  but should be flagged in cleaning notes.
- aoestats: The 43-day gap in matches (2024-07-20 to 2024-09-01) is
  significant and should be documented in 01_01_02 analysis.

