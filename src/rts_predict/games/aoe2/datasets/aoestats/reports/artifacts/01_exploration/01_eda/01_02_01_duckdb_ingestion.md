# Step 01_02_01 -- DuckDB Ingestion: aoestats

**Type:** Full ingestion with variant column census

## Tables created

| Table | Rows | Columns | DDL |
|---|---|---|---|
| matches_raw | 30,690,651 | 18 | `read_parquet('raw/matches/*.parquet', union_by_name=true, filename=true)` |
| players_raw | 107,627,584 | 14 | `read_parquet('raw/players/*.parquet', union_by_name=true, filename=true)` |
| overviews_raw | 1 | 9 | `read_json_auto('raw/overview/overview.json', filename=true)` |

## DESCRIBE matches_raw

| Column | Type |
|---|---|
| map | VARCHAR |
| started_timestamp | TIMESTAMP WITH TIME ZONE |
| duration | BIGINT |
| irl_duration | BIGINT |
| game_id | VARCHAR |
| avg_elo | DOUBLE |
| num_players | BIGINT |
| team_0_elo | DOUBLE |
| team_1_elo | DOUBLE |
| replay_enhanced | BOOLEAN |
| leaderboard | VARCHAR |
| mirror | BOOLEAN |
| patch | BIGINT |
| raw_match_type | DOUBLE |
| game_type | VARCHAR |
| game_speed | VARCHAR |
| starting_age | VARCHAR |
| filename | VARCHAR |

## DESCRIBE players_raw

| Column | Type |
|---|---|
| winner | BOOLEAN |
| game_id | VARCHAR |
| team | BIGINT |
| feudal_age_uptime | DOUBLE |
| castle_age_uptime | DOUBLE |
| imperial_age_uptime | DOUBLE |
| old_rating | BIGINT |
| new_rating | BIGINT |
| match_rating_diff | DOUBLE |
| replay_summary_raw | VARCHAR |
| profile_id | DOUBLE |
| civ | VARCHAR |
| opening | VARCHAR |
| filename | VARCHAR |

## Variant column census (pyarrow, all source files)

### matches (172 files)

| Column | Type distribution |
|---|---|
| started_timestamp | timestamp[us, tz=UTC]: 68 files, timestamp[ns, tz=UTC]: 104 files |
| raw_match_type | double: 66 files, int64: 106 files |

### players (171 files)

| Column | Type distribution |
|---|---|
| feudal_age_uptime | double: 82 files, null: 89 files |
| castle_age_uptime | double: 81 files, null: 90 files |
| imperial_age_uptime | double: 81 files, null: 90 files |
| profile_id | double: 36 files, int64: 135 files |
| opening | string: 82 files, null: 89 files |

## DuckDB auto-promotion results

- started_timestamp: TIMESTAMP WITH TIME ZONE (precision promotion)
- raw_match_type: DOUBLE (numeric promotion int64 -> double)
- feudal/castle/imperial_age_uptime: DOUBLE (NULL fill for null-typed files)
- profile_id: DOUBLE (numeric promotion). **FLAG:** Player IDs as float64
  may cause join precision issues for IDs > 2^53.
- opening: VARCHAR (NULL fill for null-typed files)

## NULL counts for variant columns (players_raw)

| Column | NULL count | % of 107,627,584 rows |
|---|---|---|
| feudal_age_uptime | 93,726,448 | 87.1% of 107,627,584 rows |
| castle_age_uptime | 94,641,831 | 87.9% of 107,627,584 rows |
| imperial_age_uptime | 98,468,904 | 91.5% of 107,627,584 rows |
| profile_id | 1,185 | ~0% of 107,627,584 rows |
| opening | 92,616,290 | 86.0% of 107,627,584 rows |

## Duration columns

DuckDB 1.5.1 maps Arrow `duration[ns]` to **BIGINT** (nanoseconds), NOT
INTERVAL. Sample values confirm reasonableness (e.g., 2971.6s, 1748.0s
when divided by 1e9).

## Missing week

172 matches files vs 171 players files. Gap: week 2025-11-16 to 2025-11-22
has matches but no player-level data.
