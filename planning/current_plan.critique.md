---
plan: current_plan.md
step: 01_04_00
verdict: PROCEED WITH FIXES
critique_date: 2026-04-16
---

# Critique: 01_04_00 Source Normalization

## Verdict: PROCEED WITH FIXES

Two blockers that would cause immediate runtime failure. Four warnings address
schema accuracy and downstream usability. All fixes are small and confined to
the SQL VIEW definitions.

## Blockers (must fix before execution)

### B1 — T03 references nonexistent column `replayID`

The plan's T03 SQL references `rp.replayID` and `rm.replayID`. Neither
`replay_players_raw` nor `replays_meta_raw` has a column called `replayID`.
Both tables have `filename` (VARCHAR). The existing `matches_flat` VIEW in
01_04_01 derives `replay_id` via:

```sql
regexp_extract(rp.filename, '([0-9a-f]{32})\.SC2Replay\.json$', 1)
```

The T03 SQL must use `filename`, not `replayID`. Also see W4.

### B2 — aoe2companion T01 passes through team values 2–254 as `side`

Census data (01_02_04_univariate_census.json, `matches_raw_numeric_stats`,
column `team`): min=0, max=255, median=2.0, p95=5.0. Team games use values
2, 3, 4, 5, etc. The plan's CASE `WHEN team = 255 THEN NULL ELSE team END`
passes these through as side=2, side=3, etc., contradicting the schema
claim that side is "0 or 1 or NULL."

The symmetry audit (T04 `WHERE side IN (0, 1)`) would silently discard
these rows with no warning. Fix: map any team value outside {0, 1} to NULL.

```sql
-- Fix for T01
CASE WHEN team IN (0, 1) THEN team ELSE NULL END AS side
```

## Warnings (fix before execution if possible)

### W1 — Schema YAML started_timestamp type is inconsistent across datasets

The YAML template claims `{type: TIMESTAMP}`. Reality:
- aoe2companion: TIMESTAMP (correct)
- aoestats: TIMESTAMP WITH TIME ZONE
- sc2egset: VARCHAR (plan line 158 acknowledges deferral)

The schema YAML column annotation should say `(varies per dataset)` matching
the pattern already used for `player_id` and `rating_pre_raw`.

### W2 — Missing leaderboard identifier column

Both AoE2 datasets' 01_04_01 VIEWs scope to 1v1 via leaderboard:
- aoestats: `m.leaderboard = 'random_map'`
- aoe2companion: `internalLeaderboardId IN (6, 18)`

Without this column in `matches_long_raw`, downstream steps must join back to
source tables to filter to 1v1. Recommend adding `leaderboard_raw` as a 10th
column, accepting that it is NULL for sc2egset (tournament data, no leaderboard).

### W3 — T02 lossless validation is tautological

The plan compares `COUNT(*) FROM matches_long_raw` against the identical query
that defines the VIEW. This always passes by construction. A meaningful check
would compare against the raw table count minus independently-known exclusions
(e.g., `COUNT(*) FROM players_raw` minus null profile_id count).

### W4 — sc2egset regex pattern must match 01_04_01

Even after fixing B1 to use `filename`, the plan uses pattern `[^/\\]+$`
(basename extraction, includes `.SC2Replay.json` suffix). The established
pattern is `([0-9a-f]{32})\.SC2Replay\.json$` (32-char hex hash only).
These produce incompatible `match_id` values. Use the hex-hash pattern.

## Notes (informational)

### N1 — `match_rating_diff` in player_history_all

`match_rating_diff` is included in aoestats `player_history_all` (01_04_01).
`matches_long_raw` correctly excludes it. No action needed for this plan, but
the downstream fix to remove it from `player_history_all` remains a pending task.

### N2 — aoe2companion `started_timestamp` nullable claim

`matches_raw` has `started` as nullable in its schema YAML. The plan's schema
YAML `nullable: false` for `started_timestamp` is incorrect for aoe2companion.
Since `matches_long_raw` applies no WHERE filter, NULLs pass through.

### N3 — sc2egset MMR pre-game provenance

The 01_04_01 notebook classifies MMR as PRE_GAME, but `replay_players_raw.yaml`
does not carry this classification explicitly. The schema YAML for
`matches_long_raw` should note the source of the PRE_GAME classification.
