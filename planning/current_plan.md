---
category: A
branch: feat/data-cleaning-01-04
date: 2026-04-16
datasets: [aoe2companion, aoestats, sc2egset]
phase: "01"
pipeline_section: "01_04 — Data Cleaning"
critique_required: true
---

# Active Plan: 01_04_00 — Source Normalization to Canonical Long Skeleton

Produces one `matches_long_raw` VIEW per dataset — 10 canonical columns, one row per
player per match, lossless format conversion only. No filtering, no cleaning, no
feature computation. This step runs before 01_04_01 to unify grain so all downstream
cleaning operates against the same structural contract.

## Canonical output schema

```
match_id              VARCHAR     -- dataset-native match identifier
started_timestamp     (varies)    -- match start time (I3 as-of anchor); see per-dataset notes
side                  INTEGER     -- source slot encoding (0 or 1); NOT outcome-aware
player_id             (varies)    -- dataset-native player identifier
chosen_civ_or_race    VARCHAR     -- civilization (AoE2) or race (SC2)
outcome_raw           INTEGER     -- 1 = win, 0 = loss, NULL = unknown
rating_pre_raw        (varies)    -- pre-match rating if available, NULL if not
map_id_raw            VARCHAR     -- raw map identifier
patch_raw             (varies)    -- patch/version if available
leaderboard_raw       (varies)    -- ladder/queue identifier; NULL for sc2egset (tournament data)
```

`side` reflects source encoding exactly. Any correlation between side and outcome
is a FINDING to document (I5 symmetry audit), not a bug to fix at this stage.

`leaderboard_raw` preserves the dataset-native leaderboard identifier so downstream
1v1 scoping does not require joining back to source tables. For sc2egset (esports
tournament replays with no matchmaking ladder), it is NULL.

## Scope

Per-dataset DuckDB VIEW creation only. Lossless projection of source tables into a
unified 10-column long skeleton (`matches_long_raw`). No filtering, no cleaning, no
feature computation. Coexists with existing 01_04_01 VIEWs — does not replace them.

---

## Problem Statement

The three datasets enter 01_04_01 at different structural grains: aoe2companion and
sc2egset are already long (one row per player per match); aoestats raw tables are
effectively wide when pivot-joined (p0_*/p1_* style in matches_1v1_clean). Writing
cleaning logic against divergent grains forces parallel implementations and makes
cross-dataset comparisons unreliable. Normalising all three to a shared long skeleton
before any cleaning ensures the same SQL logic applies uniformly downstream.

---

## Assumptions & Unknowns

- team values in aoe2companion matches_raw: assumed to use 1 and 2 for 1v1 sides
  (team=0 appears in only 449 rows). Verified empirically during execution.
- players_raw in aoestats is already per-player per-match (long grain). Confirmed
  by inspection of 01_04_01 notebook SQL — the join produces one row per player.
- sc2egset details_timeUTC: unknown whether to access as struct dot notation
  (rm.details.timeUTC) or flattened column. Resolved at execution time — struct
  dot notation required.
- aoestats players_raw total: 107,627,584 rows (known from 01_04_01 artifact).
  Used as independent lossless validation anchor.

---

## Literature Context

Long (player-row) format is standard in esports/sports prediction literature.
The Raddar NCAA tournament solution doubles every match to enforce swap invariance.
Bradley-Terry (1952) establishes that log-odds of win = difference of player
strengths — naturally expressed in focal/opponent long format. Xie (AoE2 Medium
post) documents exactly the wide-format slot-leakage bug that this step's I5
symmetry audit is designed to detect.

---

## Execution Steps

### T01 — aoe2companion matches_long_raw VIEW

**Files:**
- Create: `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_00_source_normalization.py`

**SQL:**
```sql
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    matchId                                           AS match_id,
    started                                           AS started_timestamp,
    CASE WHEN team IN (1, 2) THEN team - 1 ELSE NULL END AS side,
    profileId                                         AS player_id,
    civ                                               AS chosen_civ_or_race,
    CASE WHEN won = TRUE  THEN 1
         WHEN won = FALSE THEN 0
         ELSE NULL END                                AS outcome_raw,
    rating                                            AS rating_pre_raw,
    map                                               AS map_id_raw,
    NULL                                              AS patch_raw,
    internalLeaderboardId                             AS leaderboard_raw
FROM matches_raw
```

Notes:
- Already long (one row per player per match). Pure column rename + projection.
- aoe2companion uses `team=1` and `team=2` as the two 1v1 sides (team=0 has only
  449 rows in the entire dataset). Re-encoded 0-based: team=1 → side=0,
  team=2 → side=1. Team-game values (3+) and sentinel (255) become NULL.
  Census median=2.0, p95=5.0 reflects the predominance of team=2 rows (1v1 opponents).
- `rating` is confirmed pre-game (validated in 01_03_03). No `ratingDiff` or
  `finished` included (I3 safe).
- No `patch` column in source — NULL placeholder keeps schema consistent.
- `internalLeaderboardId` (INTEGER) is the numeric ladder ID. Ranked 1v1 values
  are 6 (rm_1v1) and 18 (qp_rm_1v1), as established in 01_04_01. This column
  allows downstream 1v1 scoping without rejoining matches_raw.
- `started` is TIMESTAMP, nullable: true in source. NULLs pass through.

**Validation:**
```sql
-- Lossless check
SELECT COUNT(*) FROM matches_long_raw;
SELECT COUNT(*) FROM matches_raw;
-- Must be equal
```

---

### T02 — aoestats matches_long_raw VIEW

**Files:**
- Create: `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_00_source_normalization.py`

**SQL:**
```sql
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    p.game_id                              AS match_id,
    m.started_timestamp                    AS started_timestamp,
    CAST(p.team AS INTEGER)                AS side,
    CAST(p.profile_id AS BIGINT)           AS player_id,
    p.civ                                  AS chosen_civ_or_race,
    CASE WHEN p.winner = TRUE  THEN 1
         WHEN p.winner = FALSE THEN 0
         ELSE NULL END                     AS outcome_raw,
    p.old_rating                           AS rating_pre_raw,
    m.map                                  AS map_id_raw,
    m.patch                                AS patch_raw,
    m.leaderboard                          AS leaderboard_raw
FROM players_raw p
INNER JOIN matches_raw m ON p.game_id = m.game_id
WHERE p.profile_id IS NOT NULL
  AND m.started_timestamp IS NOT NULL
```

Notes:
- `players_raw` is already per-player per-match (long), so this is a JOIN +
  projection, NOT a UNION ALL unpivot.
- `team` (BIGINT in source) → `side INTEGER`. Values 0 and 1 for 1v1 matches.
- `profile_id` CAST from DOUBLE to BIGINT (safe: max=24,853,897 < 2^53).
- `old_rating` (pre-game) used; `new_rating`, `match_rating_diff` excluded (I3).
- `WHERE` clause matches the filter in `player_history_all` VIEW (same grain).
- `leaderboard` (VARCHAR) is the ladder name. Ranked 1v1 value is `'random_map'`,
  as established in 01_04_01. Allows downstream 1v1 scoping without rejoining.
- `started_timestamp` is TIMESTAMP WITH TIME ZONE in source. Type unification
  deferred to Phase 02.

**Validation (independent anchor check):**
```sql
-- Step 1: Independently-known total
SELECT COUNT(*) AS total_players FROM players_raw;
-- Known from 01_04_01 artifact: 107,627,584

-- Step 2: Count independently-known exclusions
SELECT COUNT(*) AS null_profile FROM players_raw WHERE profile_id IS NULL;
SELECT COUNT(*) AS orphan_or_null_ts
FROM players_raw p
LEFT JOIN matches_raw m ON p.game_id = m.game_id
WHERE m.started_timestamp IS NULL OR m.game_id IS NULL;

-- Step 3: VIEW count
SELECT COUNT(*) AS view_count FROM matches_long_raw;

-- Lossless assertion: view_count = total_players - null_profile - orphan_or_null_ts
-- Cross-check: total_players must equal 107,627,584 (from 01_04_01 players_raw.yaml)
```

---

### T03 — sc2egset matches_long_raw VIEW

**Files:**
- Create: `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_00_source_normalization.py`

**SQL:**
```sql
CREATE OR REPLACE VIEW matches_long_raw AS
SELECT
    regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1) AS match_id,
    rm.details_timeUTC                                                   AS started_timestamp,
    rp.playerID - 1                                                      AS side,
    rp.toon_id                                                           AS player_id,
    rp.race                                                              AS chosen_civ_or_race,
    CASE WHEN rp.result = 'Win'  THEN 1
         WHEN rp.result = 'Loss' THEN 0
         ELSE NULL END                                                   AS outcome_raw,
    rp.MMR                                                               AS rating_pre_raw,
    rm.metadata_mapName                                                  AS map_id_raw,
    rm.metadata_gameVersion                                              AS patch_raw,
    NULL                                                                 AS leaderboard_raw
FROM replay_players_raw rp
INNER JOIN replays_meta_raw rm
  ON regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1)
   = regexp_extract(rm.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1)
```

Notes:
- Defined directly from raw tables, bypassing the dependency on `matches_flat`
  from 01_04_01.
- Uses the exact same hex-hash regex as `matches_flat`: `([0-9a-f]{32})\.SC2Replay\.json$`
  applied to `filename`. `match_id` values will be compatible with `matches_flat.replay_id`.
  The 01_04_01 `matches_flat` VIEW wraps this in `NULLIF(..., '')` for empty-string
  protection; executor should verify whether the same guard is needed here.
- `playerID` (1-based: 1 or 2) → `side = playerID - 1` (0-based, consistent with AoE2).
- `toon_id` (VARCHAR Battle.net identifier) → `player_id`.
- `race` (actual race played) used for `chosen_civ_or_race`, not `selectedRace`
  (which includes pre-game "Random" selection). Distinction documented in schema YAML.
- `result` in {'Win', 'Loss', 'Undecided', 'Tie'} → Win=1, Loss=0, else NULL.
- `MMR` (INTEGER; sentinel 0 = unrated) → `rating_pre_raw`. Sentinel handling deferred.
- `details_timeUTC`: confirm whether to access as `rm.details_timeUTC` (flattened) or
  `rm.details.timeUTC` (struct dot notation) in the actual DuckDB context. Executor
  must verify against the schema YAML for replays_meta_raw.
- `leaderboard_raw` is NULL for all rows. SC2EGSet is an esports tournament dataset
  with no matchmaking ladder. Deliberate NULL, not missing data.
- No `APM`, `SQ`, `supplyCappedPercent`, `header_elapsedGameLoops` (I3 safe).

**Validation:**
```sql
-- Lossless check
SELECT COUNT(*) FROM matches_long_raw;
SELECT COUNT(*) FROM replay_players_raw rp
  INNER JOIN replays_meta_raw rm
    ON regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1)
     = regexp_extract(rm.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1);
-- Must be equal

-- Verify side values
SELECT DISTINCT side FROM matches_long_raw ORDER BY side;
-- Must return only 0 and 1
```

---

### T04 — Symmetry audit (all three datasets)

Run identically in each dataset's 01_04_00 notebook after VIEW creation.

```sql
SELECT
    side,
    COUNT(*)                                             AS n_rows,
    SUM(outcome_raw)                                     AS n_wins,
    ROUND(100.0 * SUM(outcome_raw) / COUNT(*), 4)       AS win_pct,
    COUNT(*) FILTER (WHERE outcome_raw IS NULL)          AS n_null_outcome
FROM matches_long_raw
WHERE side IN (0, 1)
GROUP BY side
ORDER BY side
```

- Expected: win_pct near 50% for both sides.
- Alert (not fail): if |win_pct - 50.0| > 10.0.
- Record exact win_pct values in JSON artifact.
- For aoestats: also run scoped to 1v1 (`WHERE leaderboard_raw = 'random_map'`).
  The known asymmetry from matches_1v1_clean (side=1 wins ~52.27%) should reappear.
- For aoe2companion: also run scoped to 1v1 (`WHERE leaderboard_raw IN (6, 18)`).

---

### T05 — Schema YAMLs + artifacts

**Schema YAML** at `src/rts_predict/games/<game>/datasets/<dataset>/data/db/schemas/views/matches_long_raw.yaml`:

```yaml
object_name: matches_long_raw
object_type: view
step: 01_04_00
description: >
  Canonical long skeleton — one row per player per match. Lossless projection
  of source data into a unified 10-column schema. No filtering, no cleaning.
  Side reflects source slot encoding; any side-outcome correlation is preserved
  as-is for downstream I5 symmetry auditing.
invariants: [I3, I5, I6, I9]
columns:
  match_id:
    type: VARCHAR
    nullable: false
    notes: "Dataset-native match ID"
  started_timestamp:
    type: "(varies per dataset)"
    nullable: true
    notes: >
      I3 temporal anchor.
      aoe2companion: TIMESTAMP (source: started, nullable).
      aoestats: TIMESTAMP WITH TIME ZONE (source: started_timestamp).
      sc2egset: VARCHAR (source: details_timeUTC). Type unification deferred to Phase 02.
  side:
    type: INTEGER
    nullable: true
    notes: "Source slot (0 or 1); NULL for sentinel values or team-game values outside {0,1}"
  player_id:
    type: "(varies per dataset)"
    nullable: false
    notes: "Dataset-native player identifier. aoe2companion: INTEGER (profileId). aoestats: BIGINT (profile_id, cast from DOUBLE). sc2egset: VARCHAR (toon_id)."
  chosen_civ_or_race:
    type: VARCHAR
    nullable: true
    notes: "Civilization (AoE2) or actual race played (SC2, not selectedRace)"
  outcome_raw:
    type: INTEGER
    nullable: true
    notes: "1=win, 0=loss, NULL=unknown/undecided/tie"
  rating_pre_raw:
    type: "(varies per dataset)"
    nullable: true
    notes: "Pre-match rating. aoe2companion: INTEGER (rating, confirmed pre-game in 01_03_03). aoestats: BIGINT (old_rating). sc2egset: INTEGER (MMR; 0=unrated sentinel, handling deferred)."
  map_id_raw:
    type: VARCHAR
    nullable: true
    notes: "Raw map identifier (dataset-native, not harmonized)"
  patch_raw:
    type: "(varies per dataset)"
    nullable: true
    notes: "Patch/version. aoe2companion: NULL (no patch column in source). aoestats: BIGINT (patch). sc2egset: VARCHAR (metadata_gameVersion)."
  leaderboard_raw:
    type: "(varies per dataset)"
    nullable: true
    notes: >
      Ladder/queue identifier.
      aoe2companion: INTEGER (internalLeaderboardId; values 6=rm_1v1, 18=qp_rm_1v1 for ranked 1v1).
      aoestats: VARCHAR (leaderboard; value 'random_map' for ranked 1v1).
      sc2egset: NULL constant — tournament data with no matchmaking ladder.
```

**JSON artifact** at `.../reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json`:
- `step`, `name`, `dataset`, `view_name`, `row_count`
- `schema` (DESCRIBE output as list)
- `symmetry_audit` (side_0_win_pct, side_1_win_pct, n_null_per_side; plus 1v1-scoped audit)
- `sql_queries` (all SQL used — I6)
- `source_tables` (list)
- `lossless_check` (source_count, view_count, passed boolean; for aoestats also:
  total_players_raw, null_profile_count, orphan_or_null_ts_count)
- `leaderboard_raw_distribution` (value_counts top 10)

**MD artifact** at `.../reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md`

---

### T06 — Tracking updates

**STEP_STATUS.yaml** — add to each dataset (insert before `01_04_01`):
```yaml
"01_04_00":
    name: "Source Normalization to Canonical Long Skeleton"
    pipeline_section: "01_04"
    status: complete
    completed_at: "<date>"
```

**ROADMAP.md** — add `01_04_00` step block to each dataset before `01_04_01`.

**research_log.md** — add CROSS entry in `reports/research_log.md`:
```
[CROSS] [Phase 01 / Step 01_04_00] Canonical long skeleton normalization

Schema: 10 columns (match_id, started_timestamp, side, player_id,
chosen_civ_or_race, outcome_raw, rating_pre_raw, map_id_raw, patch_raw, leaderboard_raw)

  - aoe2companion: side 0 win_pct = X.XX%, side 1 win_pct = Y.YY%
    leaderboard_raw = internalLeaderboardId (INTEGER); 1v1 values: 6, 18
  - aoestats: side 0 win_pct = X.XX%, side 1 win_pct = Y.YY%
    leaderboard_raw = leaderboard (VARCHAR); 1v1 value: 'random_map'
  - sc2egset: side 0 win_pct = X.XX%, side 1 win_pct = Y.YY%
    leaderboard_raw = NULL (tournament data, no matchmaking ladder)
```

Add per-dataset entries to each dataset's `reports/research_log.md`.

---

## File manifest

| File | Action |
|------|--------|
| `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_00_source_normalization.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_00_source_normalization.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_00_source_normalization.py` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_long_raw.yaml` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_long_raw.yaml` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update |
| `reports/research_log.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` | Update |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update |

---

## Open Questions

- aoe2companion full-dataset side imbalance (130M side=0 vs 114M side=1): how much
  is from team games vs data quality? Not resolved — low priority, deferred.
- sc2egset 3-row side asymmetry (side=0: 22,390 vs side=1: 22,387): 3 replays with
  playerID=1 but no playerID=2 row (or vice versa). Likely corrupted replays.
  Deferred to 01_04_01 patching.

---

## Out of scope

- Cross-dataset civ/race/map harmonization → Phase 02
- `player_id` type unification → Phase 02
- `started_timestamp` type unification → Phase 02
- `leaderboard_raw` value harmonization across datasets → Phase 02
- Modifying existing 01_04_01 notebooks (`matches_long_raw` coexists with current VIEWs)
- Fixing side-outcome correlation (detect and document only; do not correct)

---

## Gate condition

1. `matches_long_raw` VIEW exists in all 3 DuckDB databases with exactly 10 columns.
2. Row counts are lossless vs. source for all 3 datasets.
3. For aoestats, lossless check uses independent anchor (players_raw total = 107,627,584
   minus independently-counted exclusions), not a tautological self-comparison.
4. Symmetry audit results (full dataset + 1v1-scoped) recorded in all 3 JSON artifacts.
5. All 3 schema YAMLs exist at `data/db/schemas/views/matches_long_raw.yaml`.
6. All 3 STEP_STATUS.yaml show `01_04_00: complete`.
7. CROSS entry exists in `reports/research_log.md`.
8. `leaderboard_raw` column present in all 3 VIEWs; NULL for sc2egset, populated
   for both AoE2 datasets.
