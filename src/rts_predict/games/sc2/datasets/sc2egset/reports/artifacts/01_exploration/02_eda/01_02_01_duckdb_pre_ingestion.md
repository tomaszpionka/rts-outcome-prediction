# Step 01_02_01 -- DuckDB Ingestion Investigation: sc2egset

**Type:** Investigation only (no persistent DuckDB tables)

## Summary

Tested DuckDB `read_json_auto` on 7 sample .SC2Replay.json files spanning
the file-size distribution (2.1 MB to 143.1 MB). All 11 root keys parsed
successfully. Measured event array storage requirements and performed a
full census of 70 map_foreign_to_english_mapping.json files.

## read_json_auto behavior

| Root key | DuckDB type | Notes |
|---|---|---|
| ToonPlayerDescMap | STRUCT (single file) / MAP(VARCHAR, STRUCT) (batch) | Dynamic player-ID keys; single-file parse creates file-specific STRUCT. With union_by_name=true, promoted to MAP. |
| details | STRUCT | gameSpeed, isBlizzardMap, timeUTC |
| gameEvents | STRUCT[] | Large typed array, highly variable size |
| gameEventsErr | BOOLEAN | Always false in sample |
| header | STRUCT | elapsedGameLoops, version |
| initData | STRUCT | gameDescription with nested options |
| messageEvents | STRUCT[] | Small array, usually 1 element |
| messageEventsErr | BOOLEAN | Always false in sample |
| metadata | STRUCT | baseBuild, dataBuild, gameVersion, mapName |
| trackerEvents | STRUCT[] | Large typed array with nested stats |
| trackerEvtsErr | BOOLEAN | Always false in sample |

## Event array storage estimate (7 sampled files)

| Array | Mean elements | Median elements | Max elements | Estimated total (22,390 files) |
|---|---|---|---|---|
| gameEvents | 79,221 | 24,825 | 431,109 | 326.8 GB |
| trackerEvents | 5,865 | 1,745 | 33,392 | 40.7 GB |
| messageEvents | 34 | 1 | 228 | 0.1 GB |
| **Total** | | | | **367.6 GB** |

## Batch ingestion test

- Directory: 2018_Cheeseadelphia_8 (64 files)
- Elapsed: 1.66 seconds
- Row count: 64 (1 row per file)
- Memory: Completed within 24 GB limit

## Proposed table split strategy

**Split-table approach recommended.** Event arrays dominate file size (~95%).

1. **replays_metadata_raw:** header, details, metadata, initData,
   ToonPlayerDescMap, error flags, filename
2. **replay_events_raw:** Deferred -- load events on-demand per analysis
   due to estimated 367.6 GB storage

## map_foreign_to_english_mapping.json census

- **Files found:** 70 (one per tournament directory)
- **Combined size:** 4.1 MB
- **Structure:** All 70 files identical -- dict with 1,488 keys mapping
  foreign map names to English map names
- **Cross-file consistency:** All same root type (dict), all same key set
- **DuckDB parse:** read_json_auto produces MAP(VARCHAR, VARCHAR), 1 row
- **Proposed DDL:** Single `map_aliases_raw` table; since all 70 are
  identical, only one file needs loading

## Recommended DDL (FUTURE ingestion step)

```sql
-- Metadata table (feasible now)
CREATE TABLE replays_metadata_raw AS
SELECT header, details, metadata, initData, ToonPlayerDescMap,
       gameEventsErr, messageEventsErr, trackerEvtsErr, filename
FROM read_json_auto('raw/*/_data/*.SC2Replay.json',
     union_by_name=true, filename=true,
     maximum_object_size=536870912);

-- Map aliases (trivial)
CREATE TABLE map_aliases_raw AS
SELECT unnest(map_keys(json)) AS foreign_name,
       unnest(map_values(json)) AS english_name, filename
FROM read_json_auto('raw/*/map_foreign_to_english_mapping.json',
     filename=true);
```
