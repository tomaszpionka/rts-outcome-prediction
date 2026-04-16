---
category: A
branch: feat/data-cleaning-01-04
date: 2026-04-16
planner_model: claude-opus-4-6
dataset: sc2egset
phase: "01"
pipeline_section: "01_04 — Data Cleaning"
invariants_touched: [3, 6, 7, 9]
critique_required: true
source_artifacts:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replay_players_raw.yaml"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replays_meta_raw.yaml"
  - "planning/fixes_and_next_steps.md"
  - "planning/plan_sc2egset_01_04_01.critique.md"
research_log_ref: "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
---

# Plan: sc2egset 01_04_01 — Data Cleaning (Revision 1)

<!-- REVISED — This is revision 1, incorporating BLOCKER F01 and
     WARNINGS W02–W05 from plan_sc2egset_01_04_01.critique.md,
     plus the new design constraint: prediction scope != feature scope. -->

## Scope

**Phase/Step:** 01 / 01_04_01
**Branch:** feat/data-cleaning-01-04
**Predecessor:** 01_03_04 (Event Profiling — complete, artifacts on disk)
**Revision basis:** plan_sc2egset_01_04_01.critique.md (BLOCKER F01, WARNINGS W02–W05)

Apply non-destructive cleaning to the two ESSENTIAL raw tables
(replay_players_raw, replays_meta_raw), create three VIEWs:

1. **`matches_flat`** — structural JOIN, all rows, no filters
2. **`matches_flat_clean`** — analytical VIEW for **prediction targets**: 1v1 decisive
   results only, all cleaning rules applied, PRE-GAME features only (I3)
3. **`player_history_all`** — analytical VIEW for **player history features**: all
   replays a player appears in (including non-1v1 and indecisive), after minimal
   quality exclusions, retaining in-game metrics (APM, SQ) because they are
   valid historical signals for prior matches

Produce a cleaning registry with CONSORT-style row-count accounting and
post-cleaning validation. No rows deleted. No features engineered. Raw data
untouched (I9).

<!-- REVISED — Added player_history_all VIEW and the dual-scope framing. -->

This step resolves the F01 structural blocker from `planning/fixes_and_next_steps.md`:
"F01. sc2egset: create `matches_flat` VIEW [BLOCKER for 01_04]."

## Problem Statement

sc2egset's pre-game features are split across two tables:
- `replay_players_raw`: 44,817 player rows (2 per match x 22,390 replays
  + 37 rows from non-1v1 replays)
- `replays_meta_raw`: 22,390 match rows, 31 struct leaf fields

Neither AoE2 dataset requires this join — sc2egset uniquely does. The
`matches_flat` VIEW is a structural prerequisite for all downstream work.

Nine data quality issues identified in prior steps (01_02_04, 01_03_01,
01_03_02) and deferred to this step:

1. Non-1v1 replays (24 replays) with no binary outcome
2. BW-prefixed race entries (3 rows in a 6-player replay — absorbed by issue 1)
3. MMR=0 sentinel (37,489 rows / 83.65%) — unrated players
4. MMR<0 anomalous values (159 rows / 0.35%, min=-36,400)
5. selectedRace="" empty string (1,110 rows / 2.48%) — Random selection
6. SQ=INT32_MIN sentinel (2 rows) — parse failures
7. APM=0 rows (1,132 rows / 2.53%) — very short games or parse artifacts
8. map_size=0 replays (273 replays / 1.22%) — parse artifact
9. handicap=0 (2 rows)

Additionally, I3 discipline requires that the pre-game analytical VIEW
(`matches_flat_clean`) exclude all IN_GAME and POST_GAME columns (APM, SQ,
supplyCappedPercent, elapsedGameLoops).

<!-- REVISED — Added new design constraint paragraph below. -->

**Dual-scope design constraint:** The thesis predicts only 1v1 match outcomes
(`matches_flat_clean`), but player-level features in Phase 02 should be computed
from the player's full recorded game history. For sc2egset (a curated esports
tournament collection), this means all replays a player appears in — including
the 24 non-1v1 replays and 13 indecisive replays excluded from
`matches_flat_clean` — remain valid game history in `player_history_all`.
APM, SQ, and other in-game metrics are valid historical signals for past matches
(I3 only prohibits using them for the TARGET match T). Temporal discipline
(I3) still applies: features for match T at time t use only games completed
before time t, regardless of game type.

## Assumptions & Unknowns

- **Assumption:** All 3 BW race rows belong to the single 6-player non-1v1
  replay (confirmed in 01_03_02 artifact). Excluded by the non-1v1 filter
  from `matches_flat_clean` — no separate cleaning rule needed. Retained in
  `player_history_all` as valid game history.
- **Assumption:** MMR=0 in esports context = unrated professional player
  (MNAR per Rubin 1976). Excluding 83.65% of data would destroy the dataset.
- **Assumption:** handicap=100 is standard; handicap=0 is anomalous (2 rows).
- **Assumption:** `details_gameSpeed` and `gd_gameSpeed` are constant per
  01_03_01 (cardinality=1). Excluded from `matches_flat_clean`; validated by
  assertion.
- **Assumption:** `gd_isBlizzardMap` and `details_isBlizzardMap` are identical
  columns (both cardinality=2 per 01_03_01). Verified in T01; if identical, only
  `details_isBlizzardMap` is retained.
- **Unknown:** Whether APM=0 rows correlate with very short game duration.
  Resolved by T06.
- **Unknown:** Whether map_size=0 replays are otherwise valid. Resolved by T07.
- **Unknown:** Whether MMR<0 values overlap with non-1v1 excluded replays.
  Resolved by T03.
- **Unknown:** Whether `gd_isBlizzardMap != details_isBlizzardMap` for any row.
  Resolved by T01.

## Literature Context

CRISP-DM Phase 3 (Data Preparation), Manual Section 4. Non-destructive
cleaning via exclusion flags (Section 4.2). Cleaning registry with Rule ID,
Condition, Action, Justification, Impact (Section 4.1). CONSORT-AI Extension
(Liu et al. 2020, Section 4.3). Missing data: Rubin (1976) MCAR/MAR/MNAR —
MMR=0 is MNAR (missingness depends on being a professional not ranked on
public ladder, which correlates with skill) (Section 4.5).

---

## Execution Steps

### T01 — Create matches_flat VIEW

<!-- REVISED — Applied NULLIF wrapper per W04. -->

**Objective:** Join replay_players_raw with struct-extracted fields from
replays_meta_raw using replay_id from regexp_extract. This is the F01
structural blocker resolution. The replay_id extraction uses NULLIF to convert
empty-string non-matches to NULL (fixing W04).

**Instructions:**

1. Create the `matches_flat` VIEW joining the two raw tables.
2. Run the isBlizzardMap duplication check (W03 resolution): query
   `SELECT COUNT(*) FROM matches_flat WHERE gd_isBlizzardMap != details_isBlizzardMap`.
   Record the result. If zero, document that the columns are identical and
   that `gd_isBlizzardMap` will be excluded from `matches_flat_clean` (prefer
   `details_isBlizzardMap` for consistency with other `details_` prefixed columns).
3. Run the gameSpeed constant assertion (W02 pre-check): query
   `SELECT COUNT(DISTINCT details_gameSpeed) AS n_speeds FROM matches_flat`.
   Assert result = 1.

**SQL:**

```sql
CREATE OR REPLACE VIEW matches_flat AS
SELECT
    -- Canonical join key (NULLIF converts empty-string non-match to NULL — W04 fix)
    NULLIF(
        regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
        ''
    ) AS replay_id,

    -- Player identity
    rp.filename,
    rp.toon_id,
    rp.nickname,
    rp.playerID,
    rp.userID,

    -- Player pre-game features
    rp.MMR,
    rp.race,
    rp.selectedRace,
    rp.handicap,
    rp.region,
    rp.realm,
    rp.highestLeague,
    rp.isInClan,
    rp.clanTag,

    -- Target variable
    rp.result,

    -- Player in-game metrics (I3: IN_GAME — excluded from matches_flat_clean,
    -- but RETAINED in player_history_all for historical feature computation)
    rp.APM,
    rp.SQ,
    rp.supplyCappedPercent,

    -- Player spatial (pre-game lobby assignment)
    rp.startDir,
    rp.startLocX,
    rp.startLocY,

    -- Player cosmetic
    rp.color_a, rp.color_b, rp.color_g, rp.color_r,

    -- Match metadata: details struct
    rm.details.gameSpeed            AS details_gameSpeed,
    rm.details.isBlizzardMap        AS details_isBlizzardMap,
    rm.details.timeUTC              AS details_timeUTC,

    -- Match metadata: header struct
    rm.header.elapsedGameLoops      AS header_elapsedGameLoops,
    rm.header.version               AS header_version,

    -- Match metadata: initData.gameDescription direct fields
    rm.initData.gameDescription.gameSpeed           AS gd_gameSpeed,
    rm.initData.gameDescription.isBlizzardMap       AS gd_isBlizzardMap,
    rm.initData.gameDescription.mapAuthorName       AS gd_mapAuthorName,
    rm.initData.gameDescription.mapFileSyncChecksum AS gd_mapFileSyncChecksum,
    rm.initData.gameDescription.mapSizeX            AS gd_mapSizeX,
    rm.initData.gameDescription.mapSizeY            AS gd_mapSizeY,
    rm.initData.gameDescription.maxPlayers          AS gd_maxPlayers,

    -- Match metadata: gameOptions (15 leaves)
    rm.initData.gameDescription.gameOptions.advancedSharedControl AS go_advancedSharedControl,
    rm.initData.gameDescription.gameOptions.amm                   AS go_amm,
    rm.initData.gameDescription.gameOptions.battleNet             AS go_battleNet,
    rm.initData.gameDescription.gameOptions.clientDebugFlags      AS go_clientDebugFlags,
    rm.initData.gameDescription.gameOptions.competitive           AS go_competitive,
    rm.initData.gameDescription.gameOptions.cooperative           AS go_cooperative,
    rm.initData.gameDescription.gameOptions.fog                   AS go_fog,
    rm.initData.gameDescription.gameOptions.heroDuplicatesAllowed AS go_heroDuplicatesAllowed,
    rm.initData.gameDescription.gameOptions.lockTeams             AS go_lockTeams,
    rm.initData.gameDescription.gameOptions.noVictoryOrDefeat     AS go_noVictoryOrDefeat,
    rm.initData.gameDescription.gameOptions.observers             AS go_observers,
    rm.initData.gameDescription.gameOptions.practice              AS go_practice,
    rm.initData.gameDescription.gameOptions.randomRaces           AS go_randomRaces,
    rm.initData.gameDescription.gameOptions.teamsTogether         AS go_teamsTogether,
    rm.initData.gameDescription.gameOptions.userDifficulty        AS go_userDifficulty,

    -- Match metadata: metadata struct
    rm.metadata.baseBuild           AS metadata_baseBuild,
    rm.metadata.dataBuild           AS metadata_dataBuild,
    rm.metadata.gameVersion         AS metadata_gameVersion,
    rm.metadata.mapName             AS metadata_mapName

FROM replay_players_raw rp
JOIN replays_meta_raw rm
  ON NULLIF(
         regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
         ''
     )
   = NULLIF(
         regexp_extract(rm.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1),
         ''
     );
```

**Validation:**

```sql
-- Row and replay counts
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT replay_id) AS distinct_replays
FROM matches_flat;
```

Expected: total_rows=44,817; distinct_replays=22,390.

```sql
-- NULL replay_id check (W04 — catches empty-string non-matches)
SELECT COUNT(*) AS null_replay_id FROM matches_flat WHERE replay_id IS NULL;
```

Expected: 0.

```sql
-- W03: isBlizzardMap duplication check
SELECT COUNT(*) AS mismatched_blizzard_map
FROM matches_flat
WHERE gd_isBlizzardMap != details_isBlizzardMap;
```

Expected: 0 (columns are identical; document and drop `gd_isBlizzardMap`
from downstream VIEWs).

```sql
-- W02: gameSpeed constant assertion
SELECT
    COUNT(DISTINCT details_gameSpeed)  AS n_details_gameSpeed,
    COUNT(DISTINCT gd_gameSpeed)       AS n_gd_gameSpeed
FROM matches_flat;
```

Expected: both = 1.

**Verification:**
- COUNT=44,817; DISTINCT replay_id=22,390; null_replay_id=0.
- isBlizzardMap mismatch count recorded; if 0, `gd_isBlizzardMap` dropped from T10/T11.
- Both gameSpeed cardinalities = 1.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb`

**Read scope:** (none — reads raw tables directly)

---

### T02 — Non-1v1 and indecisive result classification (R01)

<!-- REVISED — Added scope clarification per new design constraint. -->

**Objective:** Identify and count replays not suitable for binary classification.
Produce rule R01. Note: R01 exclusion applies to `matches_flat_clean`
(prediction target) ONLY. The 24 excluded replays remain in
`player_history_all` as valid player game history.

**Instructions:**

1. Run the per-replay classification query.
2. Verify classification summary matches 01_03_02 exactly.
3. Document that non-1v1 replays are excluded from prediction scope but
   retained in player history scope.

**SQL:**

```sql
-- Per-replay classification
SELECT
    replay_id,
    COUNT(*) AS player_row_count,
    COUNT(*) FILTER (WHERE result = 'Win') AS win_count,
    COUNT(*) FILTER (WHERE result = 'Loss') AS loss_count,
    COUNT(*) FILTER (WHERE result = 'Undecided') AS undecided_count,
    COUNT(*) FILTER (WHERE result = 'Tie') AS tie_count,
    CASE
        WHEN COUNT(*) = 2
             AND COUNT(*) FILTER (WHERE result = 'Win') = 1
             AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
        THEN 'true_1v1_decisive'
        WHEN COUNT(*) < 2 THEN 'non_1v1_too_few_players'
        WHEN COUNT(*) > 2 THEN 'non_1v1_too_many_players'
        WHEN COUNT(*) = 2
             AND (COUNT(*) FILTER (WHERE result = 'Undecided') > 0
                  OR COUNT(*) FILTER (WHERE result = 'Tie') > 0)
        THEN 'true_1v1_indecisive'
        ELSE 'non_1v1_other'
    END AS classification
FROM matches_flat
GROUP BY replay_id;
```

```sql
-- Classification summary
SELECT classification, COUNT(*) AS n_replays
FROM (
    SELECT replay_id,
        CASE
            WHEN COUNT(*) = 2
                 AND COUNT(*) FILTER (WHERE result = 'Win') = 1
                 AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
            THEN 'true_1v1_decisive'
            WHEN COUNT(*) < 2 THEN 'non_1v1_too_few_players'
            WHEN COUNT(*) > 2 THEN 'non_1v1_too_many_players'
            WHEN COUNT(*) = 2
                 AND (COUNT(*) FILTER (WHERE result = 'Undecided') > 0
                      OR COUNT(*) FILTER (WHERE result = 'Tie') > 0)
            THEN 'true_1v1_indecisive'
            ELSE 'non_1v1_other'
        END AS classification
    FROM matches_flat GROUP BY replay_id
) t
GROUP BY classification ORDER BY n_replays DESC;
```

Expected (from 01_03_02): 22,366 true_1v1_decisive, 13 indecisive, 8 too_many,
3 too_few. Total = 22,390.

**Cleaning rule R01:**
- Condition: Replay is not true_1v1_decisive
- Action: EXCLUDE entire replay from `matches_flat_clean` (prediction targets).
  RETAIN in `player_history_all` (player game history).
- Justification: Binary classification requires 2 players with 1 Win + 1 Loss.
  Non-1v1 and indecisive replays are still valid game history for player feature
  computation. Source: 01_03_02 artifact.
- Impact: 24 replays, ~85 player rows excluded from prediction scope.

**Verification:** Classification summary matches 01_03_02 exactly. Sum = 22,390.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW must exist)

---

### T03 — MMR sentinel analysis (R02, R03)

<!-- REVISED — R03 changed to REPLAY-LEVEL exclusion per BLOCKER F01 fix. -->

**Objective:** Characterize MMR=0 (37,489 rows, 83.65%) and MMR<0 (159 rows,
0.35%). Produce rules R02 (flag MMR=0) and R03 (exclude replays containing
any MMR<0 player).

**CRITICAL FIX (BLOCKER F01):** R03 must apply at the REPLAY level, not the
ROW level. If one player in a 1v1 has MMR<0, the ENTIRE replay is excluded
from `matches_flat_clean`. Row-level filtering would orphan the opponent's row,
breaking the 2-players-per-replay invariant and corrupting all downstream
wide-format pivots.

**Instructions:**

1. Run MMR counts scoped to true_1v1_decisive replays.
2. Run tournament-stratified MMR=0 analysis.
3. Run MMR<0 value distribution.
4. Count how many REPLAYS (not rows) contain at least one MMR<0 player.
   This is the CONSORT-relevant exclusion count.
5. Check overlap: how many MMR<0 rows belong to the 24 non-1v1 replays
   already excluded by R01?

**SQL:**

```sql
-- MMR counts (in true_1v1_decisive replays)
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE MMR = 0) AS mmr_zero,
    COUNT(*) FILTER (WHERE MMR < 0) AS mmr_negative,
    COUNT(*) FILTER (WHERE MMR > 0) AS mmr_positive,
    ROUND(100.0 * COUNT(*) FILTER (WHERE MMR = 0) / COUNT(*), 4) AS mmr_zero_pct,
    ROUND(100.0 * COUNT(*) FILTER (WHERE MMR < 0) / COUNT(*), 4) AS mmr_negative_pct
FROM matches_flat
WHERE replay_id IN (
    SELECT replay_id FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
);
```

```sql
-- MMR=0 tournament stratification
SELECT
    regexp_extract(filename, '^([^/]+)', 1) AS tournament,
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE MMR = 0) AS mmr_zero,
    COUNT(*) FILTER (WHERE MMR > 0) AS mmr_positive,
    COUNT(*) FILTER (WHERE MMR < 0) AS mmr_negative,
    ROUND(100.0 * COUNT(*) FILTER (WHERE MMR = 0) / COUNT(*), 2) AS mmr_zero_pct
FROM matches_flat
WHERE replay_id IN (
    SELECT replay_id FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
)
GROUP BY tournament ORDER BY tournament;
```

```sql
-- MMR<0 value distribution
SELECT MMR, COUNT(*) AS cnt,
       regexp_extract(filename, '^([^/]+)', 1) AS tournament_sample
FROM matches_flat
WHERE MMR < 0
GROUP BY MMR, tournament_sample
ORDER BY MMR
LIMIT 30;
```

```sql
-- BLOCKER F01 FIX: Count REPLAYS (not rows) with at least one MMR<0 player
-- This is the correct unit for the CONSORT flow
SELECT COUNT(*) AS replays_with_mmr_negative
FROM (
    SELECT replay_id
    FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) FILTER (WHERE MMR < 0) > 0
);
```

```sql
-- Overlap check: MMR<0 rows in non-1v1 replays vs 1v1 replays
SELECT
    CASE
        WHEN replay_id IN (
            SELECT replay_id FROM matches_flat
            GROUP BY replay_id
            HAVING COUNT(*) = 2
               AND COUNT(*) FILTER (WHERE result = 'Win') = 1
               AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
        ) THEN 'true_1v1_decisive'
        ELSE 'non_1v1_or_indecisive'
    END AS scope,
    COUNT(*) AS mmr_neg_rows,
    COUNT(DISTINCT replay_id) AS mmr_neg_replays
FROM matches_flat
WHERE MMR < 0
GROUP BY scope;
```

**Decision rationale:**
- MMR=0: FLAG, do not exclude. 83.65% of esports data — professionals lack
  public ladder ratings. Excluding would destroy the dataset. MNAR mechanism.
- MMR<0: EXCLUDE at REPLAY level. Negative MMR is impossible in SC2 matchmaking.
  Any replay containing a player with MMR<0 is fully excluded from
  `matches_flat_clean`. Row-level filtering would leave orphaned opponent rows.
  Source: 01_03_01 sentinel_summary (min=-36,400). CONSORT flow records
  replays excluded, not individual rows.

**Cleaning rule R02:**
- Condition: MMR = 0
- Action: FLAG (`is_mmr_missing = TRUE`)
- Justification: MNAR — professional players on private accounts. 83.65%.
- Impact: 37,489 rows in true_1v1_decisive scope.

**Cleaning rule R03 (REVISED — replay-level):**
- Condition: ANY player in the replay has MMR < 0
- Action: EXCLUDE entire replay from `matches_flat_clean`
- Justification: Impossible in SC2 matchmaking. Data corruption or unknown
  sentinel. Replay-level exclusion prevents orphaned rows. Source: 01_03_01
  sentinel_summary (min=-36,400), critique BLOCKER F01.
- Impact: N replays excluded (count determined at execution; 159 MMR<0 rows
  across an unknown number of replays).

**Verification:** MMR=0 count matches 01_03_01 (37,489). MMR<0 count matches
(159). Replay-level R03 exclusion count recorded for CONSORT.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T04 — selectedRace normalization (R04)

**Objective:** Map selectedRace="" to 'Random'. Produce rule R04.

**Instructions:**

1. Cross-reference empty selectedRace with actual race column.
2. Confirm overlap with APM=0.
3. Document normalization rule.

**SQL:**

```sql
-- Cross-reference empty selectedRace with actual race
SELECT selectedRace, race, COUNT(*) AS cnt
FROM matches_flat
WHERE selectedRace = ''
GROUP BY selectedRace, race
ORDER BY cnt DESC;
```

```sql
-- Confirm all APM=0 for empty selectedRace
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE APM = 0) AS apm_zero,
    COUNT(*) FILTER (WHERE APM > 0) AS apm_nonzero
FROM matches_flat
WHERE selectedRace = '';
```

Expected: 1,110 total rows; all have APM=0 (per 01_03_02).

**Cleaning rule R04:**
- Condition: selectedRace = '' (empty string)
- Action: NORMALIZE — map to 'Random' in both `matches_flat_clean` and
  `player_history_all`
- Justification: Empty string = Random race resolved post-game. `race` column
  holds actual race played. Source: 01_03_02.
- Impact: 1,110 rows (2.48%).

**Verification:** Count matches 01_03_01 sentinel_summary (1,110). All APM=0.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T05 — SQ sentinel correction (R05)

**Objective:** Flag 2 rows with SQ=INT32_MIN. Produce rule R05.

**Instructions:**

1. Query the 2 sentinel rows.
2. Document the flag-and-nullify rule.

**SQL:**

```sql
SELECT replay_id, filename, nickname, playerID, MMR, APM, SQ, result
FROM matches_flat
WHERE SQ = -2147483648;
```

**Cleaning rule R05:**
- Condition: SQ = -2147483648 (INT32_MIN)
- Action: FLAG — set SQ to NULL in `matches_flat_clean` and `player_history_all`;
  add `is_sq_sentinel = TRUE`
- Justification: INT32_MIN is a parse-failure sentinel. Source: 01_03_01.
- Impact: 2 rows (0.0045%). Note: SQ is IN_GAME (I3), so SQ does not appear
  in `matches_flat_clean` at all. The sentinel correction matters for
  `player_history_all` where SQ IS included as a valid historical metric.

**Verification:** Exactly 2 rows match.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T06 — APM=0 investigation (documentation only)

<!-- REVISED — Per W05: APM investigation is for documentation only.
     No apm_zero_flag is added to any VIEW. APM is IN_GAME (I3). -->

**Objective:** Cross-reference 1,132 APM=0 rows with game duration. This is a
documentation-only investigation. NO APM-derived columns are added to
`matches_flat_clean`. APM IS included in `player_history_all` (where APM=0
is a valid historical observation, not a flag to create).

**Instructions:**

1. Run the APM=0 vs game duration analysis.
2. Run the APM=0 vs selectedRace="" overlap check.
3. Characterize the ~22 APM=0 rows with non-empty selectedRace.
4. Record findings in the notebook and artifact. Do NOT add `apm_zero_flag`
   or any other APM-derived column to any VIEW.

**SQL:**

```sql
-- Game duration by APM group (in true_1v1_decisive)
SELECT
    CASE WHEN APM = 0 THEN 'APM=0' ELSE 'APM>0' END AS apm_group,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT replay_id) AS n_replays,
    ROUND(MEDIAN(header_elapsedGameLoops), 0) AS median_loops,
    MIN(header_elapsedGameLoops) AS min_loops,
    MAX(header_elapsedGameLoops) AS max_loops
FROM matches_flat
WHERE replay_id IN (
    SELECT replay_id FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
)
GROUP BY apm_group;
```

```sql
-- APM=0 vs selectedRace overlap
SELECT
    COUNT(*) AS apm_zero_total,
    COUNT(*) FILTER (WHERE selectedRace = '') AS also_empty_race,
    COUNT(*) FILTER (WHERE selectedRace != '') AS has_selected_race
FROM matches_flat
WHERE APM = 0
  AND replay_id IN (
      SELECT replay_id FROM matches_flat
      GROUP BY replay_id
      HAVING COUNT(*) = 2
         AND COUNT(*) FILTER (WHERE result = 'Win') = 1
         AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
  );
```

Expected: 1,110 of 1,132 APM=0 rows have selectedRace="" (per 01_03_02).

```sql
-- Characterize ~22 APM=0 rows with non-empty selectedRace
SELECT replay_id, filename, nickname, selectedRace, race, MMR, APM, SQ, result,
       header_elapsedGameLoops
FROM matches_flat
WHERE APM = 0 AND selectedRace != ''
  AND replay_id IN (
      SELECT replay_id FROM matches_flat
      GROUP BY replay_id
      HAVING COUNT(*) = 2
         AND COUNT(*) FILTER (WHERE result = 'Win') = 1
         AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
  )
ORDER BY header_elapsedGameLoops;
```

**Documentation-only finding:** APM=0 is an in-game metric observation. 97.9%
of APM=0 rows coincide with selectedRace="" (Random). The remaining ~22 rows
are likely very short games or parse artifacts. This is recorded as a notebook
finding, not a cleaning rule applied to any VIEW.

**Verification:** APM=0 count matches 01_03_01 sentinel_summary (1,132).
selectedRace="" overlap = 1,110. No APM-derived columns in any VIEW.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T07 — map_size=0 investigation (R07)

**Objective:** Cross-reference 273 map_size=0 replays with validity criteria.
Produce rule R07.

**Instructions:**

1. Profile map_size=0 replays for result distribution, MMR, and duration.
2. Check overlap with true_1v1_decisive scope.
3. Document flag-and-nullify rule.

**SQL:**

```sql
-- Profile map_size=0 replays
SELECT
    COUNT(DISTINCT replay_id) AS n_replays,
    COUNT(*) AS n_player_rows,
    COUNT(*) FILTER (WHERE result = 'Win') AS wins,
    COUNT(*) FILTER (WHERE result = 'Loss') AS losses,
    COUNT(*) FILTER (WHERE result NOT IN ('Win', 'Loss')) AS other_results,
    COUNT(*) FILTER (WHERE MMR > 0) AS mmr_rated,
    COUNT(*) FILTER (WHERE MMR = 0) AS mmr_zero,
    ROUND(MEDIAN(header_elapsedGameLoops), 0) AS median_loops,
    MIN(details_timeUTC) AS time_min,
    MAX(details_timeUTC) AS time_max
FROM matches_flat
WHERE gd_mapSizeX = 0 AND gd_mapSizeY = 0;
```

```sql
-- Overlap with true_1v1_decisive
SELECT
    COUNT(DISTINCT mf.replay_id) AS map_zero_replays,
    COUNT(DISTINCT mf.replay_id) FILTER (
        WHERE mf.replay_id IN (
            SELECT replay_id FROM matches_flat
            GROUP BY replay_id
            HAVING COUNT(*) = 2
               AND COUNT(*) FILTER (WHERE result = 'Win') = 1
               AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
        )
    ) AS map_zero_and_1v1_decisive
FROM matches_flat mf
WHERE mf.gd_mapSizeX = 0 AND mf.gd_mapSizeY = 0;
```

**Cleaning rule R07:**
- Condition: gd_mapSizeX = 0 AND gd_mapSizeY = 0
- Action: FLAG (`is_map_size_missing = TRUE`; set mapSizeX/Y to NULL in both
  `matches_flat_clean` and `player_history_all`). Do not exclude replays if
  they are otherwise valid.
- Justification: Map size 0 is a parse artifact (0 is not a valid SC2 map
  dimension). Source: 01_02_04 open questions, 01_03_01 sentinel_summary.
- Impact: 273 replays (1.22%), ~546 player rows.

**Verification:** Replay count matches 01_03_01 sentinel_summary (273).

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T08 — handicap=0 flag (R08)

**Objective:** Flag 2 rows with handicap=0. Produce rule R08.

**Instructions:**

1. Query the 2 anomalous rows.
2. Document the flag rule.

**SQL:**

```sql
SELECT replay_id, filename, nickname, playerID, MMR, handicap, result
FROM matches_flat
WHERE handicap = 0;
```

**Cleaning rule R08:**
- Condition: handicap = 0
- Action: FLAG (`is_handicap_anomalous = TRUE`). Not excluded.
- Justification: Standard handicap=100. 2 of 44,817 rows (0.0045%) are
  anomalous. Source: 01_02_04 census.
- Impact: 2 rows (0.0045%).

**Verification:** Exactly 2 rows.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T09 — Create matches_flat_clean VIEW (prediction targets)

<!-- REVISED — BLOCKER F01: replay-level MMR<0 exclusion via mmr_valid CTE.
     W02: details_gameSpeed and gd_gameSpeed excluded.
     W03: gd_isBlizzardMap excluded (duplicate of details_isBlizzardMap).
     W05: No APM, SQ, supplyCappedPercent, elapsedGameLoops, no APM-derived flags. -->

**Objective:** Create the analytical `matches_flat_clean` VIEW for prediction
targets. Applies all cleaning rules. PRE-GAME features only (I3 compliance).
Contains only true_1v1_decisive replays with no MMR<0 corruption.

**BLOCKER F01 FIX:** R03 is implemented as a replay-level CTE (`mmr_valid`)
that requires ALL players in a replay to have MMR >= 0. This prevents orphaned
rows when one player has MMR<0 but the opponent does not.

**Instructions:**

1. Create the VIEW with the CTEs defined below.
2. Verify the column list explicitly excludes: APM, SQ, supplyCappedPercent,
   header_elapsedGameLoops, color_a/b/g/r, details_gameSpeed, gd_gameSpeed,
   gd_isBlizzardMap, and any APM-derived flags.

**SQL:**

```sql
CREATE OR REPLACE VIEW matches_flat_clean AS
WITH true_1v1_decisive AS (
    -- R01: only replays with exactly 2 players, 1 Win + 1 Loss
    SELECT replay_id
    FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1
),
mmr_valid AS (
    -- R03 (BLOCKER F01 FIX): replay-level exclusion — ALL players must have MMR >= 0
    -- If ANY player in the replay has MMR < 0, the ENTIRE replay is excluded.
    -- This prevents orphaned opponent rows that would break the 2-per-replay invariant.
    SELECT replay_id
    FROM matches_flat
    GROUP BY replay_id
    HAVING COUNT(*) FILTER (WHERE MMR < 0) = 0
)
SELECT
    -- Identity
    mf.replay_id,
    mf.filename,
    mf.toon_id,
    mf.nickname,
    mf.playerID,
    mf.userID,

    -- Target
    mf.result,

    -- Pre-game player features
    mf.MMR,
    CASE WHEN mf.MMR = 0 THEN TRUE ELSE FALSE END AS is_mmr_missing,  -- R02
    mf.race,
    CASE WHEN mf.selectedRace = '' THEN 'Random'
         ELSE mf.selectedRace END AS selectedRace,                      -- R04

    mf.handicap,
    CASE WHEN mf.handicap = 0 THEN TRUE ELSE FALSE END AS is_handicap_anomalous, -- R08
    mf.region,
    mf.realm,
    mf.highestLeague,
    mf.isInClan,
    mf.clanTag,

    -- Pre-game spatial
    mf.startDir,
    mf.startLocX,
    mf.startLocY,

    -- Pre-game map metadata
    mf.metadata_mapName,
    CASE WHEN mf.gd_mapSizeX = 0 THEN NULL ELSE mf.gd_mapSizeX END AS gd_mapSizeX, -- R07
    CASE WHEN mf.gd_mapSizeY = 0 THEN NULL ELSE mf.gd_mapSizeY END AS gd_mapSizeY, -- R07
    CASE WHEN mf.gd_mapSizeX = 0 AND mf.gd_mapSizeY = 0 THEN TRUE
         ELSE FALSE END AS is_map_size_missing,                         -- R07
    mf.gd_maxPlayers,
    mf.gd_mapAuthorName,
    mf.gd_mapFileSyncChecksum,

    -- Pre-game Blizzard map flag (W03: only details_ variant retained)
    mf.details_isBlizzardMap,

    -- Pre-game temporal anchor
    mf.details_timeUTC,

    -- Pre-game version
    mf.header_version,
    mf.metadata_baseBuild,
    mf.metadata_dataBuild,
    mf.metadata_gameVersion,

    -- Pre-game game options
    mf.go_advancedSharedControl,
    mf.go_amm,
    mf.go_battleNet,
    mf.go_clientDebugFlags,
    mf.go_competitive,
    mf.go_cooperative,
    mf.go_fog,
    mf.go_heroDuplicatesAllowed,
    mf.go_lockTeams,
    mf.go_noVictoryOrDefeat,
    mf.go_observers,
    mf.go_practice,
    mf.go_randomRaces,
    mf.go_teamsTogether,
    mf.go_userDifficulty

FROM matches_flat mf
JOIN true_1v1_decisive t1v1 ON mf.replay_id = t1v1.replay_id  -- R01
JOIN mmr_valid mv ON mf.replay_id = mv.replay_id;             -- R03 (replay-level)
```

**Columns EXCLUDED from matches_flat_clean (I3 + W02 + W03 + W05):**
- `APM` — IN_GAME (computed from replay actions during game). No APM-derived flags either (W05).
- `SQ` — IN_GAME (spending quotient computed during game)
- `supplyCappedPercent` — IN_GAME (measured during game)
- `header_elapsedGameLoops` — POST_GAME (total game duration)
- `color_a/b/g/r` — cosmetic, no predictive value
- `details_gameSpeed` — CONSTANT column (cardinality=1 per 01_03_01) (W02)
- `gd_gameSpeed` — CONSTANT column (cardinality=1 per 01_03_01) (W02)
- `gd_isBlizzardMap` — duplicate of `details_isBlizzardMap` (W03)

**Expected row count:** Determined at execution. Approximately 44,817 minus
~85 (R01 non-1v1) minus 2 * N_replays_with_mmr_neg (R03 replay-level).

**Verification:**
- `SELECT COUNT(*) FROM matches_flat_clean` recorded
- `SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean` recorded
- `SELECT COUNT(*) FROM matches_flat_clean WHERE result NOT IN ('Win','Loss')` = 0
- `SELECT COUNT(*) FROM matches_flat_clean WHERE MMR < 0` = 0
- `SELECT COUNT(*) FROM matches_flat_clean WHERE selectedRace = ''` = 0

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)
- T02 findings (R01 replay set)
- T03 findings (R03 replay-level exclusion count)

---

### T10 — Create player_history_all VIEW (player feature history)

<!-- REVISED — NEW TASK: implements the prediction scope != feature scope design constraint. -->

**Objective:** Create the `player_history_all` VIEW containing one row per
player per replay for ALL replays in the dataset, after minimal quality
corrections. This VIEW is the base for computing player-level historical
features in Phase 02 (rolling win rates, historical APM, head-to-head records,
etc.). It includes non-1v1 replays, indecisive results, and in-game metrics
(APM, SQ) because:

- Non-1v1 and indecisive replays are valid game history (a player learned
  something from a team game or a draw).
- APM and SQ are valid historical signals for PRIOR matches. I3 only prohibits
  using them for the TARGET match T at prediction time. For match T-1, T-2,
  etc., they are legitimate post-hoc observations of past performance.
- Temporal discipline (I3) still applies: features for match T at time t use
  only games completed before time t.

The only exclusions applied are fundamental data corruption fixes:
- SQ=INT32_MIN sentinel -> NULL (R05: parse failure, not a real value)
- map_size=0 -> NULL (R07: parse artifact)
- selectedRace="" -> 'Random' (R04: normalization)

**Instructions:**

1. Create the VIEW with the SQL below.
2. Verify row count equals matches_flat (44,817) — no rows excluded.
3. Verify SQ sentinel is nullified (0 rows with SQ=-2147483648).
4. Verify selectedRace normalization (0 rows with selectedRace='').
5. Document the design rationale in the notebook: why APM/SQ are included
   here but excluded from matches_flat_clean.

**SQL:**

```sql
CREATE OR REPLACE VIEW player_history_all AS
SELECT
    -- Identity and join keys
    mf.replay_id,
    mf.filename,
    mf.toon_id,
    mf.nickname,
    mf.playerID,
    mf.userID,

    -- Result (unfiltered — includes Win, Loss, Undecided, Tie)
    mf.result,

    -- Player pre-game features
    mf.MMR,
    CASE WHEN mf.MMR = 0 THEN TRUE ELSE FALSE END AS is_mmr_missing,  -- R02

    mf.race,
    CASE WHEN mf.selectedRace = '' THEN 'Random'
         ELSE mf.selectedRace END AS selectedRace,                      -- R04

    mf.handicap,
    mf.region,
    mf.realm,
    mf.highestLeague,
    mf.isInClan,
    mf.clanTag,

    -- In-game metrics (VALID in player history for historical features)
    -- I3 note: these are excluded from matches_flat_clean (prediction targets)
    -- but are legitimate historical signals for PRIOR matches.
    mf.APM,
    CASE WHEN mf.SQ = -2147483648 THEN NULL ELSE mf.SQ END AS SQ,     -- R05: sentinel -> NULL
    mf.supplyCappedPercent,

    -- Game duration (historical signal — valid for past matches)
    mf.header_elapsedGameLoops,

    -- Pre-game spatial
    mf.startDir,
    mf.startLocX,
    mf.startLocY,

    -- Map metadata
    mf.metadata_mapName,
    CASE WHEN mf.gd_mapSizeX = 0 THEN NULL ELSE mf.gd_mapSizeX END AS gd_mapSizeX, -- R07
    CASE WHEN mf.gd_mapSizeY = 0 THEN NULL ELSE mf.gd_mapSizeY END AS gd_mapSizeY, -- R07
    mf.gd_maxPlayers,
    mf.details_isBlizzardMap,
    mf.gd_mapAuthorName,
    mf.gd_mapFileSyncChecksum,

    -- Temporal anchor (critical for I3 temporal ordering)
    mf.details_timeUTC,

    -- Version context (for patch-period stratification)
    mf.header_version,
    mf.metadata_baseBuild,
    mf.metadata_dataBuild,
    mf.metadata_gameVersion,

    -- Game options (for context)
    mf.go_advancedSharedControl,
    mf.go_amm,
    mf.go_battleNet,
    mf.go_competitive,
    mf.go_cooperative,
    mf.go_lockTeams,
    mf.go_randomRaces,
    mf.gd_maxPlayers AS max_players_check

FROM matches_flat mf
WHERE mf.replay_id IS NOT NULL;  -- Safety: exclude any rows where replay_id extraction failed (W04)
```

**Columns EXCLUDED from player_history_all:**
- `color_a/b/g/r` — cosmetic, no feature value in any context
- `details_gameSpeed`, `gd_gameSpeed` — CONSTANT (cardinality=1, W02)
- `gd_isBlizzardMap` — duplicate of `details_isBlizzardMap` (W03)
- `go_clientDebugFlags`, `go_fog`, `go_heroDuplicatesAllowed`,
  `go_noVictoryOrDefeat`, `go_observers`, `go_practice`, `go_teamsTogether`,
  `go_userDifficulty`, `go_battleNet` — Note: retained for now; can be pruned
  in Phase 02 if found to be constant/near-constant in the player history
  context. Actually, let me simplify: include ALL go_ flags for completeness.
  Phase 02 feature selection will prune.

**NOTE on MMR<0 in player_history_all:** MMR<0 rows are NOT excluded from
`player_history_all`. The negative values are anomalous (data corruption) but
the REPLAY itself may be valid game history. The MMR value for those rows is
unreliable, but the other fields (race, result, toon_id, timeUTC) are usable.
Phase 02 feature engineering should treat MMR<0 as missing (equivalent to
MMR=0 sentinel) when computing historical MMR features from this VIEW.

**Verification:**

```sql
-- Row count should equal matches_flat minus any NULL replay_ids
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT replay_id) AS distinct_replays
FROM player_history_all;
```

Expected: total_rows=44,817 (assuming 0 NULL replay_ids); distinct_replays=22,390.

```sql
-- SQ sentinel fully handled
SELECT COUNT(*) FROM player_history_all WHERE SQ = -2147483648;
```

Expected: 0.

```sql
-- selectedRace normalized
SELECT COUNT(*) FROM player_history_all WHERE selectedRace = '';
```

Expected: 0.

```sql
-- APM IS present (unlike matches_flat_clean)
SELECT COUNT(*) FROM player_history_all WHERE APM IS NOT NULL;
```

Expected: 44,817 (APM is not nullable in source).

**Schema YAML (write after verification):**

Write `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`
using column list from `DESCRIBE player_history_all` output. Template:

```yaml
table: player_history_all
dataset: sc2egset
game: sc2
object_type: view
step: "01_04_01"
row_count: <fill from COUNT(*)>
describe_artifact: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json
generated_date: '<YYYY-MM-DD>'
columns:
  # Fill from DESCRIBE player_history_all — annotate each column with:
  #   description: human-readable purpose
  #   notes: I3 classification (PRE_GAME / CONTEXT / TARGET / IDENTITY / IN_GAME_HISTORICAL)
  #     IN_GAME_HISTORICAL: valid signal for prior matches; excluded from
  #     matches_flat_clean but retained here (e.g. APM, SQ, supplyCappedPercent)
provenance:
  source_tables: [replay_players_raw, replays_meta_raw]
  join_key: "NULLIF(regexp_extract(filename, '([0-9a-f]{32})\\.SC2Replay\\.json', 1), '') AS replay_id"
  filter: "replay_id IS NOT NULL (W04 fix); MMR<0 retained with flag; SQ=INT32_MIN -> NULL (R05)"
  scope: "All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean."
  created_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py
invariants:
  - id: I3
    description: "APM, SQ, supplyCappedPercent, header_elapsedGameLoops are IN_GAME
      and excluded from matches_flat_clean. They are RETAINED here as valid
      historical signals for prior matches only (I3 applies to target match T,
      not to historical records)."
  - id: I6
    description: "VIEW DDL stored verbatim in 01_04_01_data_cleaning.json sql_queries."
  - id: I9
    description: "No features computed. VIEW is a JOIN projection of replay_players_raw
      x replays_meta_raw with minimal quality corrections."
```

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T01 output (matches_flat VIEW)

---

### T11 — CONSORT flow accounting

<!-- REVISED — CONSORT now tracks REPLAYS for R03 (not rows), and includes
     player_history_all. -->

**Objective:** Row and replay counts at each filtering stage, for both
`matches_flat_clean` and `player_history_all`.

**Instructions:**

1. Compute flow counts using the Python code below.
2. Verify arithmetic consistency at each stage.
3. Record R03 exclusion in REPLAY units (not row units) per BLOCKER F01 fix.

**Python (using duckdb connection `con`):**

```python
flow = {}

# Starting points
flow['raw_player_rows'] = con.execute(
    "SELECT COUNT(*) FROM replay_players_raw"
).fetchone()[0]
flow['raw_replays'] = con.execute(
    "SELECT COUNT(*) FROM replays_meta_raw"
).fetchone()[0]
flow['matches_flat_rows'] = con.execute(
    "SELECT COUNT(*) FROM matches_flat"
).fetchone()[0]
flow['matches_flat_replays'] = con.execute(
    "SELECT COUNT(DISTINCT replay_id) FROM matches_flat"
).fetchone()[0]

# R01: non-1v1 and indecisive exclusion
r01_subquery = """SELECT replay_id FROM matches_flat GROUP BY replay_id
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE result = 'Win') = 1
       AND COUNT(*) FILTER (WHERE result = 'Loss') = 1"""

flow['after_r01_replays'] = con.execute(
    f"SELECT COUNT(*) FROM ({r01_subquery})"
).fetchone()[0]
flow['r01_excluded_replays'] = flow['matches_flat_replays'] - flow['after_r01_replays']
flow['after_r01_rows'] = con.execute(
    f"SELECT COUNT(*) FROM matches_flat WHERE replay_id IN ({r01_subquery})"
).fetchone()[0]
flow['r01_excluded_rows'] = flow['matches_flat_rows'] - flow['after_r01_rows']

# R03: MMR<0 replay-level exclusion (BLOCKER F01 FIX)
# Count in REPLAYS — the correct CONSORT unit
flow['r03_excluded_replays'] = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT replay_id FROM matches_flat
        WHERE replay_id IN ({r01_subq})
        GROUP BY replay_id
        HAVING COUNT(*) FILTER (WHERE MMR < 0) > 0
    )
""".format(r01_subq=r01_subquery)).fetchone()[0]

flow['r03_excluded_rows'] = flow['r03_excluded_replays'] * 2  # 1v1: 2 rows per replay

# Final clean counts
flow['clean_rows'] = con.execute(
    "SELECT COUNT(*) FROM matches_flat_clean"
).fetchone()[0]
flow['clean_replays'] = con.execute(
    "SELECT COUNT(DISTINCT replay_id) FROM matches_flat_clean"
).fetchone()[0]

# player_history_all counts
flow['history_rows'] = con.execute(
    "SELECT COUNT(*) FROM player_history_all"
).fetchone()[0]
flow['history_replays'] = con.execute(
    "SELECT COUNT(DISTINCT replay_id) FROM player_history_all"
).fetchone()[0]

# Verify arithmetic
assert flow['clean_replays'] == (
    flow['after_r01_replays'] - flow['r03_excluded_replays']
), "CONSORT arithmetic failure: R01+R03 replay counts do not sum correctly"
assert flow['clean_rows'] == flow['clean_replays'] * 2, (
    "CONSORT row count failure: clean rows should be exactly 2x clean replays"
)
print("CONSORT flow verified.")
```

**Verification:** Arithmetic consistency at each stage. R03 recorded as
replay-level exclusion (not row-level).

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T09 output (matches_flat_clean VIEW)
- T10 output (player_history_all VIEW)

---

### T12 — Post-cleaning validation

<!-- REVISED — Added gameSpeed constant assertion (W02), isBlizzardMap
     deduplication check (W03), NULL replay_id check (W04), explicit I3
     column exclusion list including APM-derived flags (W05),
     player_history_all validation. -->

**Objective:** Validate all three VIEWs against invariants and cleaning rules.

**Instructions:**

1. Run all validation queries below.
2. Run the Python I3 assertion.
3. Run the symmetry check on matches_flat_clean.
4. Run player_history_all structural checks.

**SQL for matches_flat_clean:**

```sql
-- Result distribution (~50/50)
SELECT result, COUNT(*) AS cnt,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),4) AS pct
FROM matches_flat_clean GROUP BY result ORDER BY result;

-- Race distribution (only Protoss, Zerg, Terran)
SELECT race, COUNT(*) AS cnt FROM matches_flat_clean GROUP BY race ORDER BY cnt DESC;

-- selectedRace (no empty strings)
SELECT selectedRace, COUNT(*) AS cnt FROM matches_flat_clean
GROUP BY selectedRace ORDER BY cnt DESC;

-- MMR stats (rated-only)
SELECT COUNT(*) AS rated_rows,
       MIN(MMR) AS mmr_min, MAX(MMR) AS mmr_max,
       ROUND(AVG(MMR), 2) AS mmr_mean
FROM matches_flat_clean WHERE is_mmr_missing = FALSE;

-- Null rate on critical columns (W04: replay_id NULL check)
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE replay_id IS NULL) AS null_replay_id,
    COUNT(*) FILTER (WHERE result IS NULL) AS null_result,
    COUNT(*) FILTER (WHERE race IS NULL) AS null_race,
    COUNT(*) FILTER (WHERE selectedRace IS NULL) AS null_selectedRace,
    COUNT(*) FILTER (WHERE toon_id IS NULL) AS null_toon_id,
    COUNT(*) FILTER (WHERE details_timeUTC IS NULL) AS null_timeUTC
FROM matches_flat_clean;

-- W02: Verify gameSpeed constants are NOT in matches_flat_clean
-- (This is checked by the Python I3 assertion below which checks column names)

-- W03: Verify gd_isBlizzardMap is NOT in matches_flat_clean
-- (Also checked by the Python assertion below)
```

**Python I3 + W02/W03/W05 assertion:**

```python
clean_cols = set(con.execute("DESCRIBE matches_flat_clean").df()['column_name'])

# I3: in-game and post-game metrics
forbidden_i3 = {'APM', 'SQ', 'supplyCappedPercent', 'header_elapsedGameLoops'}

# W02: constant columns
forbidden_w02 = {'details_gameSpeed', 'gd_gameSpeed'}

# W03: duplicate column
forbidden_w03 = {'gd_isBlizzardMap'}

# W05: no APM-derived flags
forbidden_w05 = {'apm_zero_flag', 'is_apm_zero'}

# Cosmetic
forbidden_cosmetic = {'color_a', 'color_b', 'color_g', 'color_r'}

all_forbidden = forbidden_i3 | forbidden_w02 | forbidden_w03 | forbidden_w05 | forbidden_cosmetic
violations = all_forbidden & clean_cols
assert len(violations) == 0, f"Forbidden columns in matches_flat_clean: {violations}"
print("Column exclusion validation passed (I3, W02, W03, W05, cosmetic)")
```

**Symmetry check:**

```sql
SELECT COUNT(*) AS replays_not_symmetric
FROM (
    SELECT replay_id,
           COUNT(*) FILTER (WHERE result = 'Win') AS wins,
           COUNT(*) FILTER (WHERE result = 'Loss') AS losses
    FROM matches_flat_clean
    GROUP BY replay_id
    HAVING wins != 1 OR losses != 1
);
```

Expected: 0.

**SQL for player_history_all:**

```sql
-- Row count should match matches_flat
SELECT COUNT(*) AS history_rows,
       COUNT(DISTINCT replay_id) AS history_replays,
       COUNT(DISTINCT toon_id) AS unique_players
FROM player_history_all;

-- SQ sentinel fully nullified
SELECT COUNT(*) AS sq_sentinel_rows
FROM player_history_all WHERE SQ = -2147483648;
-- Expected: 0

-- selectedRace normalized
SELECT COUNT(*) AS empty_selected_race
FROM player_history_all WHERE selectedRace = '';
-- Expected: 0

-- APM is present
SELECT
    COUNT(*) FILTER (WHERE APM IS NOT NULL) AS apm_present,
    COUNT(*) FILTER (WHERE APM = 0) AS apm_zero_count
FROM player_history_all;
-- APM should be present for all rows

-- Non-1v1 replays ARE included
SELECT
    CASE
        WHEN replay_id IN (
            SELECT replay_id FROM matches_flat_clean
        ) THEN 'in_prediction_scope'
        ELSE 'history_only'
    END AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT replay_id) AS n_replays
FROM player_history_all
GROUP BY scope;
-- 'history_only' should show ~85 rows / 24 replays (plus any R03-excluded)
```

**Verification:**
- Result distribution ~50/50 in matches_flat_clean
- Only 3 SC2 races in `race`
- selectedRace no empty strings in both VIEWs
- No NULLs in replay_id, result, race, selectedRace, toon_id in matches_flat_clean
- I3 + W02 + W03 + W05 assertion passes
- Symmetry check = 0
- player_history_all contains all 44,817 rows and 22,390 replays
- player_history_all has 0 SQ sentinel rows
- player_history_all includes replays NOT in matches_flat_clean

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

**Read scope:**
- T09 output (matches_flat_clean VIEW)
- T10 output (player_history_all VIEW)

---

### T13 — Produce artifacts and update tracking

<!-- REVISED — Artifact includes player_history_all VIEW, updated cleaning
     registry, and revised CONSORT flow. -->

**Objective:** Produce the JSON and MD artifacts, update research log and
tracking files.

**Instructions:**

1. Write the JSON artifact with the schema below.
2. Write the MD artifact summarizing all cleaning rules, CONSORT flow, and
   validation results.
3. Prepend research log entry.
4. Update STEP_STATUS.yaml.
5. Update ROADMAP.md with 01_04_01 step definition.

**Artifact JSON:**

```json
{
  "step": "01_04_01",
  "dataset": "sc2egset",
  "revision": 1,
  "revision_basis": "plan_sc2egset_01_04_01.critique.md",
  "cleaning_registry": [
    {
      "rule_id": "R01",
      "condition": "Replay is not true_1v1_decisive (player_count != 2 OR result not Win+Loss)",
      "action": "EXCLUDE from matches_flat_clean; RETAIN in player_history_all",
      "justification": "Binary classification target requires 2 players with 1 Win + 1 Loss. Non-1v1 and indecisive replays are valid game history. Source: 01_03_02.",
      "impact": "24 replays excluded from prediction scope, retained in history"
    },
    {
      "rule_id": "R02",
      "condition": "MMR = 0",
      "action": "FLAG (is_mmr_missing = TRUE)",
      "justification": "MNAR — professional players on private accounts. 83.65%. Source: 01_03_01.",
      "impact": "37,489 rows"
    },
    {
      "rule_id": "R03",
      "condition": "ANY player in replay has MMR < 0 (replay-level exclusion)",
      "action": "EXCLUDE entire replay from matches_flat_clean; RETAIN in player_history_all (MMR<0 treated as unreliable)",
      "justification": "Impossible in SC2 matchmaking. Replay-level exclusion prevents orphaned rows (BLOCKER F01 fix). Source: 01_03_01, critique F01.",
      "impact": "N replays (computed at execution)"
    },
    {
      "rule_id": "R04",
      "condition": "selectedRace = '' (empty string)",
      "action": "NORMALIZE to 'Random' in both VIEWs",
      "justification": "Empty string = Random race selection. Source: 01_03_02.",
      "impact": "1,110 rows (2.48%)"
    },
    {
      "rule_id": "R05",
      "condition": "SQ = -2147483648 (INT32_MIN)",
      "action": "FLAG (SQ -> NULL; is_sq_sentinel = TRUE in player_history_all). SQ excluded from matches_flat_clean per I3.",
      "justification": "Parse-failure sentinel. Source: 01_03_01.",
      "impact": "2 rows (0.0045%)"
    },
    {
      "rule_id": "R07",
      "condition": "gd_mapSizeX = 0 AND gd_mapSizeY = 0",
      "action": "FLAG (mapSize -> NULL; is_map_size_missing = TRUE in both VIEWs)",
      "justification": "Parse artifact; 0 is not a valid SC2 map dimension. Source: 01_02_04, 01_03_01.",
      "impact": "273 replays (~546 rows)"
    },
    {
      "rule_id": "R08",
      "condition": "handicap = 0",
      "action": "FLAG (is_handicap_anomalous = TRUE)",
      "justification": "Standard handicap = 100. Source: 01_02_04.",
      "impact": "2 rows (0.0045%)"
    }
  ],
  "consort_flow": {
    "raw_player_rows": null,
    "raw_replays": null,
    "matches_flat_rows": null,
    "matches_flat_replays": null,
    "after_r01_replays": null,
    "r01_excluded_replays": null,
    "r01_excluded_rows": null,
    "r03_excluded_replays": null,
    "r03_excluded_rows": null,
    "clean_rows": null,
    "clean_replays": null,
    "history_rows": null,
    "history_replays": null
  },
  "validation": {},
  "views_created": ["matches_flat", "matches_flat_clean", "player_history_all"],
  "design_constraint": {
    "prediction_scope": "matches_flat_clean — 1v1 decisive results only",
    "feature_history_scope": "player_history_all — all replays, all game types, including in-game metrics",
    "rationale": "Player features computed from full game history; prediction targets restricted to 1v1 decisive"
  },
  "i3_compliance": {
    "matches_flat_clean_excluded": [
      "APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops",
      "details_gameSpeed", "gd_gameSpeed", "gd_isBlizzardMap",
      "color_a", "color_b", "color_g", "color_r"
    ],
    "player_history_all_includes_ingame": [
      "APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops"
    ],
    "rationale": "I3 prohibits in-game metrics for TARGET match T. For prior matches in player_history_all, they are valid historical signals."
  },
  "critique_fixes": {
    "F01_blocker": "R03 changed from row-level WHERE to replay-level CTE (mmr_valid)",
    "W02_constant_cols": "details_gameSpeed and gd_gameSpeed excluded from matches_flat_clean",
    "W03_isBlizzardMap": "gd_isBlizzardMap excluded; verified identical to details_isBlizzardMap",
    "W04_regexp_extract": "NULLIF wrapper applied in matches_flat VIEW definition",
    "W05_apm_flag": "No APM-derived columns in any VIEW; investigation is documentation-only"
  },
  "sql_queries": {}
}
```

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Create (jupytext-paired) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update (prepend entry) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Update (add 01_04_01) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update (add 01_04_01 step definition) |

## Gate Condition

<!-- REVISED — Added player_history_all and critique-fix verification. -->

- `matches_flat` VIEW exists; returns 44,817 rows / 22,390 distinct replays.
- `matches_flat` has ZERO rows with replay_id IS NULL (W04 fix verified).
- `matches_flat_clean` VIEW exists; returns expected row count.
- `matches_flat_clean` has ZERO rows with result NOT IN ('Win','Loss').
- `matches_flat_clean` has ZERO rows with MMR < 0.
- `matches_flat_clean` has ZERO rows with selectedRace = ''.
- `matches_flat_clean` does NOT contain columns: APM, SQ, supplyCappedPercent,
  header_elapsedGameLoops, details_gameSpeed, gd_gameSpeed, gd_isBlizzardMap,
  color_a/b/g/r, apm_zero_flag, is_apm_zero (I3 + W02 + W03 + W05).
- Symmetry check = 0 (every replay has exactly 1 Win + 1 Loss row).
- `player_history_all` VIEW exists; returns 44,817 rows / 22,390 distinct replays.
- `player_history_all` has ZERO rows with SQ = -2147483648.
- `player_history_all` has ZERO rows with selectedRace = ''.
- `player_history_all` DOES contain APM and SQ columns (valid historical signals).
- `player_history_all` includes replays NOT in matches_flat_clean (non-1v1, indecisive).
- CONSORT flow records R03 exclusion in REPLAY units (not row units).
- JSON artifact exists; contains cleaning_registry (R01–R08 minus R06),
  consort_flow, validation, critique_fixes, design_constraint, sql_queries
  (all verbatim, I6).
- MD artifact exists; non-empty.
- `schemas/views/player_history_all.yaml` exists; `object_type: view`; `row_count` populated; IN_GAME_HISTORICAL annotation present on APM/SQ columns.
- STEP_STATUS.yaml: `01_04_01: complete`.

## Out of Scope

- Feature engineering (Phase 02, I9).
- In-game analytical view (`matches_flat_clean_ingame`) — deferred to Phase 02.
- Identity resolution (Invariant I2 — toon_id to canonical nickname) — Phase 02.
- Temporal split design (Phase 03).
- Imputation of MMR=0 — Phase 02 decision.
- Treatment of MMR<0 in player_history_all (flagged as unreliable; imputation
  strategy is Phase 02).
- Cleaning rules for AoE2 datasets (separate 01_04_01 plans).
- R06 is NOT a cleaning rule — APM=0 is a documentation-only finding (W05).

## Open Questions

- **Q1:** MMR<0 and non-1v1 overlap — do any of the 159 MMR<0 rows belong to
  the 24 excluded replays? Affects CONSORT arithmetic. Resolves by T03.
- **Q2:** APM=0 rows with non-empty selectedRace (~22 rows) — short games or
  parse failures? Resolves by T06 (documentation only).
- **Q3:** map_size=0 and non-1v1 overlap — do any of the 273 replays belong to
  the excluded 24? Resolves by T07.
- **Q4 (NEW):** For player_history_all, should MMR<0 values be treated as NULL
  (equivalent to MMR=0 sentinel) during Phase 02 feature computation? The
  current VIEW retains the raw negative values for traceability; Phase 02
  feature engineering must decide. Resolves by: Phase 02 plan.

## Scientific Invariants

| # | Invariant | How upheld |
|---|-----------|------------|
| I3 | No post-game features in prediction VIEW | matches_flat_clean excludes APM, SQ, supplyCappedPercent, elapsedGameLoops, details_gameSpeed, gd_gameSpeed, gd_isBlizzardMap, color channels. Python assertion confirms. player_history_all includes in-game metrics as valid HISTORICAL signals for prior matches only. |
| I6 | All SQL verbatim | Every query in T01–T12 stored as literal string in notebook and JSON artifact. |
| I7 | No magic numbers | R01: true_1v1_decisive criteria from 01_03_02. R03: MMR<0 threshold from impossibility argument + 01_03_01 sentinel_summary. R07: map_size=0 from 01_02_04/01_03_01. W02 constant assertion from 01_03_01 cardinality=1. |
| I9 | Step scope | Cleaning + VIEW creation only. No features engineered. |

---

**Adversarial critique required before execution begins.**
Dispatch `reviewer-adversarial` to produce `planning/plan_sc2egset_01_04_01.critique.md` (revision 1).