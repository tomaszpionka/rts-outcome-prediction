# aoe2companion — Raw Data

Files downloaded from the aoe2companion CDN are stored here.

## Subdirectory layout

| Directory | Contents | Source pattern |
|-----------|----------|----------------|
| `matches/` | Daily match parquet files | `match-{date}.parquet` (2,073 files, 6.94 GB) |
| `leaderboards/` | Leaderboard snapshot | `leaderboard.parquet` (1 file, 87 MB) |
| `profiles/` | Player profile snapshot | `profile.parquet` (1 file, 170 MB) |
| `ratings/` | Daily rating CSV files | `rating-{date}.csv` (2,072 files, 2.64 GB) |

## Source

CDN: `https://dump.cdn.aoe2companion.com/`
Manifest: `../api/api_dump_list.json`

Each manifest entry has a `url` field with the full CDN download URL.

## Notes

- CSV equivalents of matches/leaderboards/profiles exist in the manifest but
  are not downloaded (parquet preferred for size and query performance).
- Rating CSVs have no parquet equivalent and are therefore downloaded.
- Files before 2025-06-27 are sparse (header-only); files from 2025-06-27
  onward are substantive.
- Do not modify files in this directory. It is the raw layer.
