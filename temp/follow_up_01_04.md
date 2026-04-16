# Follow-up: 01_04 Data Cleaning — Open Items

Generated: 2026-04-16
Branch: feat/data-cleaning-01-04
Source: adversarial review of 01_04_00 + 01_04_01

---

## BLOCKERS (must fix before 01_04 can be marked complete)

### B1 — aoe2companion: POST-GAME columns in `matches_1v1_clean` (I3 violation)

**File:** `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

Columns to remove from `matches_1v1_clean` VIEW definition:
- `d.ratingDiff` — post-game rating change (unknowable before match T ends)
- `d.finished` — match end timestamp (post-game)

Additional fix required: the V2 leakage check currently validates `player_history_all`
only. Extend it to also assert these columns are absent from `matches_1v1_clean`.

---

### B2 — aoestats: POST-GAME columns in `matches_1v1_clean` and `player_history_all` (I3 violation)

**File:** `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

Columns to remove from `matches_1v1_clean` VIEW definition:
- `m.duration` — game length in seconds (post-game)
- `m.irl_duration` — real-world game duration (post-game)
- `p0.match_rating_diff` — rating change from player 0's perspective (post-game)
- `p1.match_rating_diff` — rating change from player 1's perspective (post-game)

Column to remove from `player_history_all` VIEW definition:
- `p.match_rating_diff` — post-game rating delta; user confirmed removal

After removal: update `forbidden_hist` set and leakage validation to also cover
`matches_1v1_clean` (currently only covers `player_history_all`).

Schema YAML to update after VIEW fix:
`src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/player_history_all.yaml`
— remove `match_rating_diff` column entry.

---

### B3 — Research log factual error (aoe2companion side encoding)

**File:** `reports/research_log.md`

The CROSS entry for 01_04_00 states:
> "1v1 scoped (leaderboard_raw IN (6, 18)): only side=1 rows appear; win_pct=47.18%"

This is wrong. After fixing the team encoding (team=1→side=0, team=2→side=1),
both sides appear with ~30M rows each:
- side=0: 29,921,254 rows, win_pct=47.18%
- side=1: 29,920,914 rows, win_pct=52.81%

Correct the narrative to match the JSON artifact at:
`src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.json`

---

## WARNINGS (fix before closing 01_04)

### W1 — sc2egset: duplicate column in `player_history_all`

**File:** `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

`max_players_check` is an exact alias of `gd_maxPlayers` in the same VIEW.
Remove `max_players_check` from the `player_history_all` VIEW SQL.

---

### W2 — aoestats: `player_history_all.yaml` references removed column

**File:** `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/player_history_all.yaml`

Once B2 removes `match_rating_diff` from the VIEW, the YAML column entry for it
must also be removed. The current YAML notes "MUST NOT be used as a predictive feature
(I3 violation)" — that note is not a substitute for removing the column from the VIEW.

---

### W3 — All three datasets: `matches_1v1_clean` has no explicit I3 validation

None of the three 01_04_01 notebooks validate POST-GAME column absence from
`matches_1v1_clean` directly. The existing checks (V2 in aoe2companion, `forbidden_hist`
in aoestats) only cover `player_history_all`. Add explicit `information_schema.columns`
assertions for `matches_1v1_clean` in all three notebooks.

---

## DEFERRED (Phase 02 scope)

- aoestats `matches_1v1_clean` wide→long restructuring to focal/opponent format
  with difference features — requires feature engineering design decisions
- Timestamp type unification across datasets (`matches_long_raw.started_timestamp`
  is TIMESTAMP / TIMESTAMPTZ / VARCHAR across the three datasets)
- aoe2companion full-dataset side imbalance (130M side=0 vs 114M side=1):
  quantify how much is from team games vs data quality
- `leaderboard_raw` value harmonization across datasets
- `player_id` type unification (INTEGER / BIGINT / VARCHAR across datasets)
