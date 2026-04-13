# Step 01_02_01 -- DuckDB Ingestion: aoe2companion

**Type:** Full ingestion

## Tables created

| Table | Rows | Columns | DDL |
|---|---|---|---|
| matches_raw | 277,099,059 | 55 | `read_parquet('raw/matches/*.parquet', filename=true, binary_as_string=true)` |
| ratings_raw | 58,317,433 | 8 | `read_csv('raw/ratings/*.csv', filename=true, header=true, types={...})` |
| leaderboards_raw | 2,381,227 | 19 | `read_parquet('raw/leaderboards/leaderboard.parquet', binary_as_string=true, filename=true)` |
| profiles_raw | 3,609,686 | 14 | `read_parquet('raw/profiles/profile.parquet', binary_as_string=true, filename=true)` |

## Column count verification

| Table | 01_01_02 columns | + filename | Actual | Status |
|---|---|---|---|---|
| matches_raw | 54 | 55 | 55 | PASS |
| ratings_raw | 7 | 8 | 8 | PASS |
| leaderboards_raw | 18 | 19 | 19 | PASS |
| profiles_raw | 13 | 14 | 14 | PASS |

## DESCRIBE matches_raw (selected columns)

| Column | Type |
|---|---|
| matchId | INTEGER |
| started | TIMESTAMP |
| finished | TIMESTAMP |
| leaderboard | VARCHAR |
| name | VARCHAR |
| profileId | INTEGER |
| rating | INTEGER |
| ratingDiff | INTEGER |
| won | BOOLEAN |
| filename | VARCHAR |

## DESCRIBE ratings_raw

| Column | Type | Gate |
|---|---|---|
| profile_id | BIGINT | PASS (expected INTEGER/BIGINT) |
| games | BIGINT | PASS (expected INTEGER) |
| rating | BIGINT | PASS (expected INTEGER) |
| date | TIMESTAMP | PASS (expected DATE/TIMESTAMP) |
| leaderboard_id | BIGINT | PASS |
| rating_diff | BIGINT | PASS (expected INTEGER) |
| season | BIGINT | PASS |
| filename | VARCHAR | -- |

**Note:** Initial `read_csv_auto` inferred all columns as VARCHAR on the
full 2072-file load. Re-ingested with explicit `types=` parameter.

## Binary column inspection (pyarrow)

All Parquet binary columns are unannotated BYTE_ARRAY (converted_type=NONE).
`binary_as_string=true` required on all Parquet reads.

- matches: 22 binary columns
- leaderboards: 4 binary columns
- profiles: 11 binary columns

## won column NULL count

| Metric | Value |
|---|---|
| Total rows | 277,099,059 |
| won IS NULL | 12,985,561 |
| won IS NOT NULL | 264,113,498 |

## File count gap

2,073 match files vs 2,072 rating files. Missing date: **2025-07-11**
(match-2025-07-11.parquet exists, rating-2025-07-11.csv does not).
