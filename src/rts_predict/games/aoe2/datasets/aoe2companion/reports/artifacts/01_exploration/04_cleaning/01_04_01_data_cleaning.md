# 01_04_01 Data Cleaning Artifact — aoe2companion

**Generated:** 2026-04-16  
**Step:** 01_04_01  
**Dataset:** aoe2companion  

## Cleaning Registry

| Rule | Name | Condition | Action | Impact |
|------|------|-----------|--------|--------|
| R00 | Feature history scope | Full matches_raw, all game types, excluding profileId=-1 and duplicates | Create VIEW player_history_all as feature computation source | ~264,132,745 rows in player_history_all |
| R01 | Scope restriction | internalLeaderboardId NOT IN (6, 18) OR internalLeaderboardId IS NULL | Exclude from prediction target VIEW; retain in player_history_all | 216,027,260 rows excluded from prediction target (~78.0% of total) |
| R02 | Deduplication | Duplicate (matchId, profileId) rows; also any profileId=-1 rows | Keep first occurrence per matchId x profileId (ORDER BY started); exclude profileId=-1 | Excess rows removed: 5; profileId=-1 rows removed: 1 |
| R03 | Won complementarity | 2-row match where won not complementary; also 1-row and 3+ row matches | Exclude entire match (both rows) | Matches excluded: 5,052 |
| R04 | NULL cluster flag | All 10 game-settings columns simultaneously NULL | FLAG only (is_null_cluster = TRUE) -- retained in matches_1v1_clean | 11,184 rows flagged |
| R05 | ratings_raw.games outlier cap | ratings_raw.games > 1,775,011,321 (p99.9, empirically computed) | Winsorize to p99.9 = 1,775,011,321 in ratings_clean VIEW | 78,923 rows with games > 1M capped |

## CONSORT Flow

| Stage | N rows | N matches | Description |
|-------|--------|-----------|-------------|
| S0_raw | 277,099,059 | 74788989 | All rows in matches_raw |
| S1_scope_restricted | 61,071,799 | 30536248 | R01: internalLeaderboardId IN (6, 18) |
| S2_deduplicated | 61,071,794 | 30536248 | R02: deduplicated by (matchId, profileId) ORDER BY started; profileId=-1 excluded |
| S3_valid_complementary | 61,062,392 | 30531196 | R03: 2-row matches with complementary won only |
| excluded_S0_to_S1 | 216,027,260 | — | Out-of-scope leaderboards |
| excluded_S1_to_S2 | 5 | — | Duplicates + profileId=-1 |
| excluded_S2_to_S3 | 9,402 | — | Non-complementary won + non-2-row matches |

## Post-Cleaning Validation

- **V1 Rating coverage:** 73.8%
- **V2 No POST-GAME leakage:** PASS
- **V3 No negative ratings:** PASS
- **V7 No anonymous rows:** PASS

### V4 Leaderboard Distribution (matches_1v1_clean)

| Leaderboard | internalLeaderboardId | N rows |
|-------------|----------------------|--------|
| qp_rm_1v1 | 18 | 7,376,228 |
| rm_1v1 | 6 | 53,686,164 |

### V8 Leaderboard Diversity (player_history_all)

| Leaderboard | N rows |
|-------------|--------|
| rm_team | 102,711,158 |
| unranked | 65,939,173 |
| rm_1v1 | 53,694,518 |
| qp_rm_team | 19,707,154 |
| qp_rm_1v1 | 7,377,276 |
| rm_team_console | 3,472,383 |
| ew_team | 3,356,610 |
| unknown | 3,131,983 |
| ew_1v1 | 1,943,971 |
| rm_1v1_console | 1,600,477 |
| ew_1v1_redbullwololo | 594,890 |
| dm_team | 193,400 |
| qp_br_ffa | 167,984 |
| dm_1v1 | 94,508 |
| qp_ew_1v1 | 49,477 |
| qp_ew_team | 44,716 |
| ror_team | 23,308 |
| ror_1v1 | 15,775 |
| ew_1v1_console | 7,522 |
| ew_team_console | 5,812 |
| ew_1v1_redbullwololo_console | 650 |

## SQL Queries

### T01_scope_restriction

```sql
-- R01: Scope restriction -- count rows before/after
SELECT
    'total' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw

UNION ALL

SELECT
    'in_scope_1v1' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw
WHERE internalLeaderboardId IN (6, 18)

UNION ALL

SELECT
    'out_of_scope' AS scope,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT matchId) AS n_matches
FROM matches_raw
WHERE internalLeaderboardId NOT IN (6, 18)
   OR internalLeaderboardId IS NULL;
```

### T02_dup_stratification

```sql
-- R02: Duplicate stratification (in-scope only)
WITH in_scope AS (
    SELECT *
    FROM matches_raw
    WHERE internalLeaderboardId IN (6, 18)
),
dup_groups AS (
    SELECT matchId, profileId, COUNT(*) AS row_count
    FROM in_scope
    GROUP BY matchId, profileId
    HAVING COUNT(*) > 1
)
SELECT
    CASE WHEN d.profileId = -1 THEN 'profileId_minus1' ELSE 'real_profileId' END AS stratum,
    COUNT(*) AS n_dup_groups,
    SUM(d.row_count) AS total_dup_rows,
    SUM(d.row_count) - COUNT(*) AS excess_rows
FROM dup_groups d
GROUP BY
    CASE WHEN d.profileId = -1 THEN 'profileId_minus1' ELSE 'real_profileId' END;
```

### T02_minus1_investigation

```sql
-- profileId=-1 investigation in 1v1 scope
SELECT
    COUNT(*) AS total_minus1_rows,
    COUNT(DISTINCT matchId) AS n_matches_with_minus1
FROM matches_raw
WHERE internalLeaderboardId IN (6, 18)
  AND profileId = -1;
```

### T03_won_consistency

```sql
-- R03: Won consistency check (in-scope, 2-row matches only)
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
),
match_pairs AS (
    SELECT
        matchId,
        COUNT(*) AS n_rows,
        COUNT(*) FILTER (WHERE won = TRUE) AS n_won_true,
        COUNT(*) FILTER (WHERE won = FALSE) AS n_won_false,
        COUNT(*) FILTER (WHERE won IS NULL) AS n_won_null
    FROM in_scope_dedup
    GROUP BY matchId
    HAVING COUNT(*) = 2
)
SELECT
    CASE
        WHEN n_won_true = 1 AND n_won_false = 1 THEN 'complementary'
        WHEN n_won_true = 2 THEN 'both_true'
        WHEN n_won_false = 2 THEN 'both_false'
        WHEN n_won_null > 0 THEN 'has_null'
        ELSE 'other'
    END AS won_pattern,
    COUNT(*) AS n_matches,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct
FROM match_pairs
GROUP BY won_pattern
ORDER BY n_matches DESC;
```

### T03_match_sizes

```sql
-- Non-2-row match counts in scope after dedup
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
),
match_sizes AS (
    SELECT matchId, COUNT(*) AS n_rows FROM in_scope_dedup GROUP BY matchId
)
SELECT
    CASE WHEN n_rows = 1 THEN '1_row'
         WHEN n_rows = 2 THEN '2_rows'
         ELSE '3_plus_rows' END AS size_bucket,
    COUNT(*) AS n_matches,
    SUM(n_rows) AS total_rows
FROM match_sizes
GROUP BY size_bucket
ORDER BY size_bucket;
```

### T04_null_cluster

```sql
-- R04: NULL cluster temporal stratification (in-scope)
WITH in_scope AS (
    SELECT * FROM matches_raw WHERE internalLeaderboardId IN (6, 18)
),
null_cluster AS (
    SELECT
        matchId, started,
        CASE
            WHEN allowCheats IS NULL AND lockSpeed IS NULL AND lockTeams IS NULL
             AND recordGame IS NULL AND sharedExploration IS NULL
             AND teamPositions IS NULL AND teamTogether IS NULL
             AND turboMode IS NULL AND fullTechTree IS NULL AND population IS NULL
            THEN TRUE ELSE FALSE
        END AS is_null_cluster
    FROM in_scope
)
SELECT is_null_cluster, COUNT(*) AS n_rows,
       MIN(started) AS min_date, MAX(started) AS max_date,
       COUNT(DISTINCT DATE_TRUNC('month', started)) AS n_months
FROM null_cluster
GROUP BY is_null_cluster;
```

### T04_null_monthly

```sql
-- R04 addendum: monthly breakdown of NULL cluster (W01 temporal stratification)
WITH in_scope AS (
    SELECT * FROM matches_raw WHERE internalLeaderboardId IN (6, 18)
),
null_cluster AS (
    SELECT
        started,
        CASE
            WHEN allowCheats IS NULL AND lockSpeed IS NULL AND lockTeams IS NULL
             AND recordGame IS NULL AND sharedExploration IS NULL
             AND teamPositions IS NULL AND teamTogether IS NULL
             AND turboMode IS NULL AND fullTechTree IS NULL AND population IS NULL
            THEN TRUE ELSE FALSE
        END AS is_null_cluster
    FROM in_scope
)
SELECT
    DATE_TRUNC('month', started) AS month,
    COUNT(*) FILTER (WHERE is_null_cluster) AS null_cluster_rows,
    COUNT(*) FILTER (WHERE NOT is_null_cluster) AS normal_rows,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_null_cluster) / COUNT(*), 2) AS null_pct
FROM null_cluster
GROUP BY DATE_TRUNC('month', started)
ORDER BY month;
```

### T04_null_survival

```sql
-- NULL cluster survival after R01+R02+R03
WITH in_scope_dedup AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY matchId, profileId ORDER BY started) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18) AND profileId != -1
    ) sub
    WHERE rn = 1
),
valid_matches AS (
    SELECT matchId FROM in_scope_dedup
    GROUP BY matchId
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE won = TRUE) = 1
       AND COUNT(*) FILTER (WHERE won = FALSE) = 1
)
SELECT
    CASE
        WHEN d.allowCheats IS NULL AND d.lockSpeed IS NULL AND d.lockTeams IS NULL
         AND d.recordGame IS NULL AND d.sharedExploration IS NULL
         AND d.teamPositions IS NULL AND d.teamTogether IS NULL
         AND d.turboMode IS NULL AND d.fullTechTree IS NULL AND d.population IS NULL
        THEN 'null_cluster' ELSE 'normal'
    END AS cluster_status,
    COUNT(*) AS n_rows,
    COUNT(DISTINCT d.matchId) AS n_matches
FROM in_scope_dedup d
INNER JOIN valid_matches v ON d.matchId = v.matchId
GROUP BY cluster_status;
```

### T05_outlier_analysis

```sql
SELECT
    COUNT(*) AS total_rows,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY games) AS p99,
    PERCENTILE_CONT(0.999) WITHIN GROUP (ORDER BY games) AS p999,
    PERCENTILE_CONT(0.9999) WITHIN GROUP (ORDER BY games) AS p9999,
    MAX(games) AS max_val,
    COUNT(*) FILTER (WHERE games > 50000) AS n_above_50k,
    COUNT(*) FILTER (WHERE games > 100000) AS n_above_100k,
    COUNT(*) FILTER (WHERE games > 1000000) AS n_above_1M
FROM ratings_raw;
```

### T05_ratings_clean_view

```sql
CREATE OR REPLACE VIEW ratings_clean AS
SELECT
    profile_id, LEAST(games, 1775011321) AS games,
    rating, date, leaderboard_id, rating_diff, season, filename
FROM ratings_raw;
```

### T06_player_history_all_view

```sql
CREATE OR REPLACE VIEW player_history_all AS
WITH deduped AS (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE profileId != -1
    ) sub
    WHERE rn = 1
)
SELECT
    matchId,
    profileId,
    name,
    started,
    leaderboard,
    internalLeaderboardId,
    map,
    civ,
    rating,
    color,
    slot,
    team,
    startingAge,
    gameMode,
    speed,
    won,
    country,
    status,
    verified,
    filename
FROM deduped;
```

### T07_matches_1v1_clean_view

```sql
CREATE OR REPLACE VIEW matches_1v1_clean AS
SELECT
    d.matchId,
    d.started,
    d.finished,
    d.leaderboard,
    d.name,
    d.server,
    d.internalLeaderboardId,
    d.privacy,
    d.mod,
    d.map,
    d.difficulty,
    d.startingAge,
    d.fullTechTree,
    d.allowCheats,
    d.empireWarsMode,
    d.endingAge,
    d.gameMode,
    d.lockSpeed,
    d.lockTeams,
    d.mapSize,
    d.population,
    d.hideCivs,
    d.recordGame,
    d.regicideMode,
    d.gameVariant,
    d.resources,
    d.sharedExploration,
    d.speed,
    d.speedFactor,
    d.suddenDeathMode,
    d.antiquityMode,
    d.civilizationSet,
    d.teamPositions,
    d.teamTogether,
    d.treatyLength,
    d.turboMode,
    d.victory,
    d.revealMap,
    d.scenario,
    d.password,
    d.modDataset,
    d.profileId,
    d.rating,
    d.ratingDiff,
    d.color,
    d.colorHex,
    d.slot,
    d.status,
    d.team,
    d.won,
    d.country,
    d.shared,
    d.verified,
    d.civ,
    d.filename,
    CASE
        WHEN d.allowCheats IS NULL AND d.lockSpeed IS NULL AND d.lockTeams IS NULL
         AND d.recordGame IS NULL AND d.sharedExploration IS NULL
         AND d.teamPositions IS NULL AND d.teamTogether IS NULL
         AND d.turboMode IS NULL AND d.fullTechTree IS NULL AND d.population IS NULL
        THEN TRUE ELSE FALSE
    END AS is_null_cluster
FROM (
    SELECT * EXCLUDE (rn)
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) raw_rn
    WHERE rn = 1
) d
WHERE d.matchId IN (
    SELECT matchId
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY matchId, profileId
                   ORDER BY started
               ) AS rn
        FROM matches_raw
        WHERE internalLeaderboardId IN (6, 18)
          AND profileId != -1
    ) sub
    WHERE rn = 1
    GROUP BY matchId
    HAVING COUNT(*) = 2
       AND COUNT(*) FILTER (WHERE won = TRUE) = 1
       AND COUNT(*) FILTER (WHERE won = FALSE) = 1
);
```
