# Step 01_03_02 -- True 1v1 Match Identification

**Dataset:** sc2egset
**Phase:** 01 -- Data Exploration
**Pipeline Section:** 01_03 -- Systematic Data Profiling
**Total replays:** 22390
**Total player rows:** 44817

---

## Players-per-replay distribution

```sql
SELECT
    players_per_replay,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM (
    SELECT
        filename,
        COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
)
GROUP BY players_per_replay
ORDER BY players_per_replay
```

|   players_per_replay |   replay_count |     pct |
|---------------------:|---------------:|--------:|
|                    1 |              3 |  0.0134 |
|                    2 |          22379 | 99.9509 |
|                    4 |              2 |  0.0089 |
|                    6 |              1 |  0.0045 |
|                    8 |              3 |  0.0134 |
|                    9 |              2 |  0.0089 |

## max_players lobby setting distribution

```sql
SELECT
    initData.gameDescription.maxPlayers AS max_players,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM replays_meta_raw
GROUP BY max_players
ORDER BY max_players
```

|   max_players |   replay_count |     pct |
|--------------:|---------------:|--------:|
|             2 |          21981 | 98.1733 |
|             4 |            403 |  1.7999 |
|             6 |              1 |  0.0045 |
|             8 |              3 |  0.0134 |
|             9 |              2 |  0.0089 |

## Observer setting distribution

```sql
SELECT
    initData.gameDescription.gameOptions.observers AS observer_setting,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct
FROM replays_meta_raw
GROUP BY observer_setting
ORDER BY observer_setting
```

|   observer_setting |   replay_count |   pct |
|-------------------:|---------------:|------:|
|                  0 |          22390 |   100 |

## max_players vs actual player row count (cross-tabulation)

```sql
SELECT
    rm.initData.gameDescription.maxPlayers AS max_players,
    pc.players_per_replay,
    COUNT(*) AS replay_count
FROM replays_meta_raw rm
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rm.filename = pc.filename
GROUP BY max_players, players_per_replay
ORDER BY max_players, players_per_replay
```

|   max_players |   players_per_replay |   replay_count |
|--------------:|---------------------:|---------------:|
|             2 |                    1 |              3 |
|             2 |                    2 |          21978 |
|             4 |                    2 |            401 |
|             4 |                    4 |              2 |
|             6 |                    6 |              1 |
|             8 |                    8 |              3 |
|             9 |                    9 |              2 |

## Empty selectedRace analysis

Total rows with selectedRace = '': 1110
Unique replays: 555

```sql
SELECT
    rp.filename,
    rp.playerID,
    rp.nickname,
    rp.selectedRace,
    rp.race,
    rp.result,
    rp.MMR,
    rp.APM,
    rp.highestLeague,
    rm.initData.gameDescription.maxPlayers AS max_players,
    rm.initData.gameDescription.gameOptions.observers AS observer_setting,
    pc.players_per_replay
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.selectedRace = ''
ORDER BY pc.players_per_replay DESC, rp.filename, rp.playerID
```

### Result distribution for empty-selectedRace rows

| result   |   count |
|:---------|--------:|
| Win      |     555 |
| Loss     |     555 |

### Race (resolved) distribution for empty-selectedRace rows

| race   |   count |
|:-------|--------:|
| Zerg   |     569 |
| Prot   |     276 |
| Terr   |     265 |

## BW race variant context

```sql
SELECT
    rp.filename,
    rp.playerID,
    rp.selectedRace,
    rp.race,
    rp.result,
    rp.APM,
    pc.players_per_replay,
    rm.initData.gameDescription.maxPlayers AS max_players
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.selectedRace IN ('BWTe', 'BWZe', 'BWPr')
ORDER BY rp.filename, rp.playerID
```

| filename                                                                                                                         |   playerID | selectedRace   | race   | result   |   APM |   players_per_replay |   max_players |
|:---------------------------------------------------------------------------------------------------------------------------------|-----------:|:---------------|:-------|:---------|------:|---------------------:|--------------:|
| 2024_03_ESL_SC2_Masters_Spring_Finals/2024_03_ESL_SC2_Masters_Spring_Finals_data/c23226fa504bfe0045e01d6363df6826.SC2Replay.json |          2 | BWTe           | BWTe   | Loss     |   338 |                    6 |             6 |
| 2024_03_ESL_SC2_Masters_Spring_Finals/2024_03_ESL_SC2_Masters_Spring_Finals_data/c23226fa504bfe0045e01d6363df6826.SC2Replay.json |          3 | BWPr           | BWPr   | Loss     |   312 |                    6 |             6 |
| 2024_03_ESL_SC2_Masters_Spring_Finals/2024_03_ESL_SC2_Masters_Spring_Finals_data/c23226fa504bfe0045e01d6363df6826.SC2Replay.json |          5 | BWZe           | BWZe   | Loss     |   482 |                    6 |             6 |

## Undecided/Tie replay context

```sql
SELECT
    rp.filename,
    rp.playerID,
    rp.selectedRace,
    rp.result,
    pc.players_per_replay,
    rm.initData.gameDescription.maxPlayers AS max_players
FROM replay_players_raw rp
JOIN replays_meta_raw rm ON rp.filename = rm.filename
JOIN (
    SELECT filename, COUNT(*) AS players_per_replay
    FROM replay_players_raw
    GROUP BY filename
) pc ON rp.filename = pc.filename
WHERE rp.result IN ('Undecided', 'Tie')
ORDER BY rp.result, rp.filename, rp.playerID
```

Total Undecided/Tie rows: 26
Unique replays: 13

## Replay classification summary

```sql
-- Summary aggregation over the per-replay classification
-- (derived from the replay_classification CTE above, re-executed for clarity)
WITH per_replay AS (
    SELECT
        rp.filename,
        COUNT(*) AS player_row_count,
        COUNT(*) FILTER (WHERE rp.result IN ('Win', 'Loss')) AS decisive_count,
        COUNT(*) FILTER (WHERE rp.result = 'Win') AS win_count,
        COUNT(*) FILTER (WHERE rp.result = 'Loss') AS loss_count,
        COUNT(*) FILTER (WHERE rp.result = 'Undecided') AS undecided_count,
        COUNT(*) FILTER (WHERE rp.result = 'Tie') AS tie_count,
        COUNT(*) FILTER (WHERE rp.selectedRace = '') AS empty_race_count,
        rm.initData.gameDescription.maxPlayers AS max_players
    FROM replay_players_raw rp
    JOIN replays_meta_raw rm ON rp.filename = rm.filename
    GROUP BY rp.filename, max_players
),
classified AS (
    SELECT *,
        CASE
            WHEN player_row_count = 2
                 AND decisive_count = 2
                 AND win_count = 1
                 AND loss_count = 1
            THEN 'true_1v1_decisive'
            WHEN player_row_count < 2
            THEN 'non_1v1_too_few_players'
            WHEN player_row_count > 2
            THEN 'non_1v1_too_many_players'
            WHEN player_row_count = 2
                 AND (undecided_count > 0 OR tie_count > 0)
            THEN 'true_1v1_indecisive'
            ELSE 'non_1v1_other'
        END AS classification
    FROM per_replay
)
SELECT
    classification,
    COUNT(*) AS replay_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS pct,
    MIN(player_row_count) AS min_players,
    MAX(player_row_count) AS max_players_actual,
    SUM(empty_race_count) AS total_empty_race_rows
FROM classified
GROUP BY classification
ORDER BY replay_count DESC
```

| classification           |   replay_count |     pct |   min_players |   max_players_actual |   total_empty_race_rows |
|:-------------------------|---------------:|--------:|--------------:|---------------------:|------------------------:|
| true_1v1_decisive        |          22366 | 99.8928 |             2 |                    2 |                    1110 |
| true_1v1_indecisive      |             13 |  0.0581 |             2 |                    2 |                       0 |
| non_1v1_too_many_players |              8 |  0.0357 |             4 |                    9 |                       0 |
| non_1v1_too_few_players  |              3 |  0.0134 |             1 |                    1 |                       0 |

### Classification criteria

| Classification | Criterion |
|----------------|-----------|
| true_1v1_decisive | player_row_count == 2 AND win_count == 1 AND loss_count == 1 |
| non_1v1_too_few_players | player_row_count < 2 |
| non_1v1_too_many_players | player_row_count > 2 |
| true_1v1_indecisive | player_row_count == 2 AND (undecided_count > 0 OR tie_count > 0) |
| non_1v1_other | Residual category (should be 0) |

**true_1v1_decisive replays: 22366 / 22390 (99.89%)**

The `true_1v1_indecisive` category captures replays that ARE genuine 1v1 matches (exactly 2 player rows) but lack a decisive Win/Loss outcome (Undecided or Tie).
These are excluded from the prediction pipeline because they have no usable prediction target -- not because of a game-format issue. The thesis-relevant population is `true_1v1_decisive`.

---

## Observations and thesis implications

1. **Observation:** The dataset is overwhelmingly 1v1: 22,366 of 22,390 replays (99.89%) are `true_1v1_decisive` (exactly 2 player rows, 1 Win + 1 Loss). Only 11 replays (0.05%) are non-1v1 by player count (8 `non_1v1_too_many_players` with 4-9 rows; 3 `non_1v1_too_few_players` with 1 row), and 13 replays (0.06%) are `true_1v1_indecisive` (2 players but Undecided/Tie result, no usable prediction target). The `non_1v1_other` category is empty -- the classification logic is exhaustive.
   **Thesis implication:** The sc2egset corpus is practically a pure 1v1 dataset. The 24 replays to be excluded (11 non-1v1 by count + 13 indecisive) represent 0.11% attrition. The thesis population is 22,366 decisive 1v1 replays.
   **Next action:** Feed classification to 01_04 (Data Cleaning). Exclude `non_1v1_too_few_players` (3), `non_1v1_too_many_players` (8), and `true_1v1_indecisive` (13) replays from the analysis population.

2. **Observation:** All 1,110 empty-selectedRace rows belong to `true_1v1_decisive` replays (players_per_replay = 2 for all 1,110 rows; result distribution is exactly 555 Win + 555 Loss; APM = 0.0 for all). The `race` column is populated for all 1,110 (Zerg 569, Prot 276, Terr 265), confirming the race was resolved post-game. This is not an observer issue -- it is a data quality issue in the `selectedRace` field for players who selected Random pre-game.
   **Thesis implication:** The empty-selectedRace phenomenon is confined to 555 replays in the 1v1 decisive population and does not affect match classification. The APM = 0 pattern across all 1,110 rows is a sentinel value investigation item for 01_04.
   **Next action:** Investigate APM = 0 sentinel in 01_04.

3. **Observation:** The observer setting is 0 (no observers) for all 22,390 replays. The 8 `non_1v1_too_many_players` replays (4-9 player rows) are not caused by observer slots in the lobby -- they are genuine multi-player game replays (max_players matches actual player row count exactly: 4=4, 6=6, 8=8, 9=9). The 3 BW-race variant rows (BWTe, BWPr, BWZe) all belong to the single 6-player replay.
   **Thesis implication:** Observer contamination is not a concern in this dataset. The non-1v1 replays are genuine team games that inadvertently entered the esport corpus.
   **Next action:** Document in INVARIANTS.md that observer_setting = 0 is universal in sc2egset.

4. **Observation:** 403 replays have max_players = 4 but only 2 actual player rows -- these are all classified as `true_1v1_decisive`. The max_players field encodes lobby slot capacity, not active player count, as expected for SC2 maps with observer/referee slots. These are genuine 1v1 matches played on 4-slot maps.
   **Thesis implication:** max_players alone is not a reliable 1v1 filter; actual player row count is the correct criterion. The max_players field is not useful for 1v1 identification and should be excluded from features.

---

*All SQL queries above are the exact code used to produce these results (I6).*
*Standard races ['Prot', 'Rand', 'Terr', 'Zerg'] derived from 01_02_04 census (I7).*
*This step classifies replays but does not drop any rows (I9).*