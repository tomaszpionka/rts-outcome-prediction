---
# raw_data_readme v2 -- conforms to docs/templates/raw_data_readme_template.yaml

# -- Section A: Identity -------------------------------------------------------

game: aoe2
dataset: aoestats
raw_directory: src/rts_predict/games/aoe2/datasets/aoestats/data/raw/

# -- Section B: Provenance -----------------------------------------------------

source_name: "aoestats.io weekly DB dumps"
source_url: "https://aoestats.io"
source_type: cdn_download
data_creator: "aoestats.io (community statistics service)"
sampling_mechanism: >
  exhaustive -- all matches recorded by aoestats.io for the covered date range;
  selection criteria used by the source service are not publicly documented.
manifest_path: "src/rts_predict/games/aoe2/datasets/aoestats/data/api/db_dump_list.json"
citation: aoestats_io
license: "Unknown -- no license file in source; check with data_creator before redistribution"
acquisition_date: "2026-04-06"
acquisition_script: "src/rts_predict/games/aoe2/datasets/aoestats/data/acquisition.py"

# -- Section C: Content and Layout ---------------------------------------------

description: >
  Three subdirectories: matches/ (172 `.parquet` files), players/ (171
  `.parquet` files), overview/ (1 `.json` file). Dotfiles excluded
  (.gitkeep x3, one per subdir). 2 root files (README.md,
  _download_manifest.json) not counted in subdirectory totals.
file_format: "parquet, JSON"

# File counts and sizes from 01_01_01 artifact. Dotfiles excluded.
subdirectory_layout:
  - directory: "matches/"
    contents: "`.parquet` files named `{date}_{date}_matches.parquet`"
    file_pattern: "{start_date}_{end_date}_matches.parquet"
    file_count: 172
    size_mb: 610.55
  - directory: "players/"
    contents: "`.parquet` files named `{date}_{date}_players.parquet`"
    file_pattern: "{start_date}_{end_date}_players.parquet"
    file_count: 171
    size_mb: 3162.86
  - directory: "overview/"
    contents: "`.json` file named `overview.json`"
    file_pattern: "overview.json"
    file_count: 1
    size_mb: 0.02

total_files: 344
total_size_mb: 3773.61

# -- Section D: Temporal Coverage ----------------------------------------------

temporal_grain: "filename-derived weekly cadence ({date}_{date} prefix pattern)"
# Dates from 01_01_01 artifact date_analysis.matches
date_range_start: "2022-08-28"
date_range_end: "2026-02-07"

# Gaps from 01_01_01 artifact date_analysis.matches
known_gaps:
  - prev_end: "2024-07-20"
    next_start: "2024-09-01"
    gap_days: 43
  - prev_end: "2024-09-28"
    next_start: "2024-10-06"
    gap_days: 8
  - prev_end: "2025-03-22"
    next_start: "2025-03-30"
    gap_days: 8

gap_analysis_status: not_started
# coverage_notes: stripped -- forward references to Phase 01 profiling steps not yet complete

# -- Section E: Acquisition Filtering ------------------------------------------

acquisition_filters:
  - rule: "Manifest entries with num_matches == 0 are skipped during download"
    justification: >
      Weeks with zero matches contain no usable data. Downloading them would
      consume storage without adding information. The filter is implemented in
      acquisition.py (filter_download_targets function).
    excluded_count: 16
    excluded_count_source: >
      manifest comparison: 188 total manifest entries minus 172 downloaded
      match files = 16 zero-match weeks excluded.

# -- Section F: Verification ---------------------------------------------------

checksum_status: full
checksum_source: "db_dump_list.json manifest -- match_checksum and player_checksum fields (MD5)"
checksum_verified: true
# MD5 checksums are verified during download (acquisition.py download_file function
# raises ValueError on checksum mismatch) and checked for idempotent re-runs
# (acquisition.py is_already_downloaded function computes MD5 before skipping).
verification_date: "2026-04-06"

# -- Section G: Immutability and Artifact Link ---------------------------------

immutability:
  status: true
  enforcement_mechanism: none_documented

inventory_artifact: "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"

# -- Section H: Known Limitations ----------------------------------------------

known_biases: >
  The selection criteria used by aoestats.io to include matches in its database
  are not publicly documented. It is unknown whether all ranked or casual matches
  are captured, or whether filtering is applied at the source. This limits claims
  about population representativeness.

representativeness_notes: >
  Coverage is limited to matches recorded by the aoestats.io service. The
  service audience and any server-side filters applied before publication are
  not known, making it difficult to assess which parts of the AoE2 player
  population are under- or over-represented.
---

# aoestats -- Raw Data

Weekly database dumps from aoestats.io. Files downloaded on 2026-04-06 from
[https://aoestats.io](https://aoestats.io).
This directory holds the raw data layer and must never be modified.

**License:** Unknown -- no license file in source
**Acquisition date:** 2026-04-06
**Acquisition script:** `src/rts_predict/games/aoe2/datasets/aoestats/data/acquisition.py`
**Manifest:** `src/rts_predict/games/aoe2/datasets/aoestats/data/api/db_dump_list.json`

> **File counts and sizes:** From 01_01_01 artifact. Dotfiles excluded
> (.gitkeep x3, one per subdir). 2 root files not counted in subdirectory totals.

## Subdirectory Layout

| Directory | Contents | Pattern | File count | Size (MB) |
|-----------|----------|---------|-----------|-----------|
| `matches/` | `.parquet` files | `{date}_{date}_matches.parquet` | 172 | 610.55 |
| `players/` | `.parquet` files | `{date}_{date}_players.parquet` | 171 | 3162.86 |
| `overview/` | `.json` file | `overview.json` | 1 | 0.02 |

**Total files:** 344 (excluding dotfiles and root files)
**Total size:** 3773.61 MB

## Temporal Coverage

- **Grain:** filename-derived weekly cadence (`{date}_{date}` prefix pattern)
- **Date range:** 2022-08-28 to 2026-02-07 (from artifact `date_analysis.matches`)
- **Gap analysis status:** not_started
- **Known gaps (matches/):** 2024-07-20 to 2024-09-01 (43 days); 2024-09-28 to 2024-10-06 (8 days); 2025-03-22 to 2025-03-30 (8 days)

## Acquisition Filtering

16 zero-match weeks from the manifest were excluded during download.
These correspond to manifest entries with `num_matches == 0`. The manifest
contained 188 total entries; 172 non-zero entries were downloaded.

## Verification

MD5 checksums are available in the manifest (`match_checksum` and
`player_checksum` fields) and were verified during download. The acquisition
script raises an error on checksum mismatch and checks MD5 for idempotent
re-downloads.

## Known Limitations

- Source selection criteria not documented; representativeness unknown
- players/ has one fewer file than matches/ (172 vs 171: one additional gap week in players)

## Inventory Artifact

`src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json`
