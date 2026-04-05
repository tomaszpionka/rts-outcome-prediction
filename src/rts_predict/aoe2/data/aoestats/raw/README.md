# aoestats — Raw Data

Files downloaded from aoestats.io are stored here.

## Subdirectory layout

| Directory | Contents | Source pattern |
|-----------|----------|----------------|
| `matches/` | Weekly match parquet files | `matches.parquet` per date-range subpath |
| `players/` | Weekly player parquet files | `players.parquet` per date-range subpath |

## Source

Base URL: `https://aoestats.io`
Manifest: `../api/db_dump_list.json`

URL pattern: manifest provides relative paths (e.g.,
`/media/db_dumps/date_range%3D2022-08-28_2022-09-03/matches.parquet`).
Prepend the base URL to construct the download URL.

## Coverage

- 188 weekly entries (2022-08-28 to 2026-04-04)
- 172 non-zero entries (16 entries with `num_matches == 0` are skipped)
- 30.7M matches, 108.3M player records across non-zero entries

## Notes

- Acquisition is deferred until aoe2companion Phase 0 profiling is complete.
- checksums (`match_checksum`, `player_checksum`) are available in the manifest
  for post-download verification.
- Do not modify files in this directory. It is the raw layer.
