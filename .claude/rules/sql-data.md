---
paths:
  - "src/rts_predict/games/*/datasets/*/data/**/*.py"
  - "sandbox/**/*.py"
---

# SQL & Data Pipeline Constraints

## Replay ID (canonical join key)
```sql
regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1) AS replay_id
```
- Path A: extract from `filename`; Path B: extract from `match_id`
- ALL downstream tables use `replay_id` as FK to `raw`
- NEVER join on `filename` or `match_id` directly

## Tournament Identity
```sql
split_part(filename, '/', -3) AS tournament_dir
```
Derived from filesystem path structure. Validated by pre-Phase audit;
pending re-validation in Phase 01 Step 01_01_02. Must be persistent column on `raw`.

## View Design
- Every view: comment block with purpose + row multiplicity
- Use `replay_id` as join key, `canonical_nickname` as player identifier
- `matches_flat` = TWO rows per game — always `COUNT(DISTINCT replay_id)`
- Create views ONLY after dependent tables are validated

## Temporal Discipline (mirrors Invariant #3)
- Features for game at time T use ONLY `match_time < T`
- NEVER `.shift()` on unsorted data
- Filter by sequence number or timestamp, NEVER by row position

## Notebook Query Pattern
- DuckDB SQL is the primary query layer — aggregations, NULL census, GROUP BY, STRUCT access
- Pull results to pandas with `.df()` for display and light analysis helpers (`.describe()`, `.value_counts()`, etc.)
- NEVER load full raw tables into pandas (`SELECT * FROM large_table` → `.df()` is prohibited)
- All SQL that produces a reported result must appear verbatim in the markdown artifact (Invariant #6)

## Data Handling
- NEVER silently drop rows — log count and reason
- Assert shapes and dtypes after every major transformation
- Use `pd.Categorical` for known-cardinality columns (race, matchup, result)
- When reading large files: specify `dtype` and `usecols` upfront
