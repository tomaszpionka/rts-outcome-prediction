# Q3: Stratification & Secondary Regime (tournament_era) — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## spec §5 honest statement

regime_id ≡ calendar quarter. Cross-dataset stratification by regime_id IS stratification by time, identical to the Q1 grain. It provides no additional variance reduction beyond Q1.

## Method

- Tournament tier lookup: hand-mapped 70 tournament dirs via Liquipedia tier heuristics
  (source: tournament_tier_lookup.csv; M2 fix — no ILIKE heuristic).
- Join: `substr(m.match_id, 11) = mfc.replay_id` (M8 fix — uses matches_flat_clean).
- Population: overlap window 2022-Q3..2024-Q4. [POP:tournament]

## SQL (verbatim, I6)

```sql
WITH era_map AS (
  SELECT
    mfc.replay_id,
    split_part(mfc.filename, '/', 1) AS tournament_dir
  FROM matches_flat_clean mfc
),
joined AS (
  SELECT
    m.match_id,
    m.player_id,
    m.won,
    m.started_at,
    em.tournament_dir
  FROM matches_history_minimal m
  JOIN era_map em ON substr(m.match_id, 11) = em.replay_id
  WHERE m.started_at >= TIMESTAMP '2022-07-01'
    AND m.started_at <  TIMESTAMP '2025-01-01'
)
SELECT
  tournament_dir,
  COUNT(*) AS n,
  AVG(CAST(won AS DOUBLE)) AS mean_won
FROM joined
GROUP BY tournament_dir
ORDER BY tournament_dir
```

## Tier-level win rates (overlap window)

| tier     |     n |   mean_won | notes            |
|:---------|------:|-----------:|:-----------------|
| Gold     | 17044 |        0.5 | [POP:tournament] |
| Platinum |  2728 |        0.5 | [POP:tournament] |
| Silver   |   380 |        0.5 | [POP:tournament] |

## Verdict: FALSIFIED

Max tier-to-tier win-rate diff = 0.0000.

## M7 note

All Phase 06 rows tagged [POP:tournament]: sc2egset is tournament-scraped;
between-player variance reflects competitive player population, not general playerbase.
See INVARIANTS §5 for scope documentation.
