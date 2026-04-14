# Step 01_02_01 -- DuckDB Pre-Ingestion: aoe2companion


## Binary column inspection


- `matches`: 22 binary columns
- `leaderboards`: 4 binary columns
- `profiles`: 11 binary columns

## Smoke test


- matches: 491,099 rows, 55 cols
- ratings: 266,508 rows, 8 cols

## matches NULL rates


- Total rows: 277,099,059
- won NULLs: 12,985,561 (4.69%)
- matchId NULLs: 0

## matchId uniqueness


- Total rows: 277,099,059
- Distinct matchIds: 74,788,989
- Avg rows/match: 3.71 (expected ~2 for player-in-match)

## Won NULL root cause

- H1 (schema heterogeneity): REJECTED
- H2 (genuine NULLs): SUPPORTED
- Files with NULLs: 2073 of 2073
- Total NULLs: 12,985,561