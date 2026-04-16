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

1. **Observation:** [to be filled based on execution results]
   **Thesis implication:** [to be filled]
   **Next action:** Feed classification to 01_04 (Data Cleaning).

---

*All SQL queries above are the exact code used to produce these results (I6).*
*Standard races ['Prot', 'Rand', 'Terr', 'Zerg'] derived from 01_02_04 census (I7).*
*This step classifies replays but does not drop any rows (I9).*