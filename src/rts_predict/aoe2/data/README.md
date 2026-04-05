# AoE2 Data Acquisition Plan

This document specifies what to download, from where, and into which directories
for each data source. It serves as the specification for the future download
script.

No data has been downloaded yet. This README describes the intended acquisition.

---

## Source Overview

| Source | Manifest on disk | Granularity | Date range | Formats | Role |
|--------|-----------------|-------------|------------|---------|------|
| aoe2companion | `aoe2companion/api/api_dump_list.json` | Daily | 2020-08-01 to 2026-04-04 | Parquet, CSV | Primary |
| aoestats | `aoestats/api/db_dump_list.json` | Weekly | 2022-08-28 to 2026-04-04 | Parquet | Validation |

**Primary source:** aoe2companion. Rationale: longer coverage (6 years vs. 4),
daily granularity (vs. weekly), zero date gaps, known file sizes, and direct
CDN URLs. aoestats acquisition is deferred until aoe2companion Phase 0 profiling
is complete.

---

## aoe2companion: What to Download

Manifest: `aoe2companion/api/api_dump_list.json`
Each entry has a `url` field with the full CDN URL (e.g.,
`https://dump.cdn.aoe2companion.com/match-2020-08-01.parquet`).

| File pattern | Count | Total size | Download? | Target directory |
|-------------|-------|-----------|-----------|-----------------|
| `match-{date}.parquet` | 2,073 | 6.94 GB | Yes | `aoe2companion/raw/matches/` |
| `leaderboard.parquet` | 1 | 87 MB | Yes | `aoe2companion/raw/leaderboards/` |
| `profile.parquet` | 1 | 170 MB | Yes | `aoe2companion/raw/profiles/` |
| `rating-{date}.csv` | 2,072 | 2.64 GB | Yes | `aoe2companion/raw/ratings/` |
| `match-{date}.csv` | 2,072 | 43.14 GB | No (parquet preferred) | -- |
| `leaderboard.csv` | 1 | 749 MB | No (parquet preferred) | -- |
| `profile.csv` | 1 | 663 MB | No (parquet preferred) | -- |
| test files | 3 | ~5 MB | No | -- |

**Estimated download total:** ~9.8 GB
(6.94 GB matches + 0.26 GB leaderboard+profile + 2.64 GB ratings)

**Format rationale:** Parquet is preferred over CSV everywhere a parquet version
exists (smaller, typed columns, faster to query). Rating CSVs are acquired
because no parquet equivalent exists for this data type.

**Note on rating CSVs:** 1,791 files before 2025-06-27 are sparse (63–972 bytes
each, 0.20 MB combined — likely header-only or near-empty). 281 files from
2025-06-27 onward are substantive (2.64 GB combined). All files are acquired
for completeness; the pre-2025 sparse files cost negligible storage and their
presence/absence is itself a useful data point during profiling.

---

## aoestats: What to Download

Manifest: `aoestats/api/db_dump_list.json`
URL pattern: manifest provides relative paths (e.g.,
`/media/db_dumps/date_range%3D2022-08-28_2022-09-03/matches.parquet`).
Base URL: `https://aoestats.io`.

| File pattern | Count | Total size | Download? | Target directory |
|-------------|-------|-----------|-----------|-----------------|
| `matches.parquet` (weekly) | 172 (non-zero) | Unknown (no sizes in manifest) | Deferred | `aoestats/raw/matches/` |
| `players.parquet` (weekly) | 172 (non-zero) | Unknown | Deferred | `aoestats/raw/players/` |

**Zero-count entries:** 16 entries (across 4 gap ranges) have `num_matches == 0`
and must be skipped. The `num_matches` field in the manifest identifies these.

**Deferred because:** aoe2companion is the primary source with known sizes and
longer coverage. aoestats download will be planned after aoe2companion data is
profiled in Phase 0.

---

## Download Script Requirements (Specification, Not Implementation)

The future download script (`scripts/download_aoe2.py` or equivalent) must:

- Read the manifest JSON to enumerate files
- Route each file to the correct `raw/` subdir based on filename pattern:
  - `match-*.parquet` → `raw/matches/`
  - `leaderboard.parquet` → `raw/leaderboards/`
  - `profile.parquet` → `raw/profiles/`
  - `rating-*.csv` → `raw/ratings/`
- Skip entries where `num_matches == 0` (aoestats) or file type is not a
  download target (aoe2companion CSV duplicates, test files)
- Verify checksums where available:
  - aoestats provides `match_checksum` and `player_checksum`
  - aoe2companion provides `eTag`
- Be idempotent: skip files already present with matching size/checksum
- Log progress and write a download manifest for reproducibility
