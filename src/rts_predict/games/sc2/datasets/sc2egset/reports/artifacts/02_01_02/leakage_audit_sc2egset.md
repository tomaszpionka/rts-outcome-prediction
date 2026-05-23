# Leakage audit — sc2egset Step 02_01_02 (post-materialization CROSS-02-01-v1.0.1)

## 1. Non-overclaim disclaimer

Step 02_01_02 NOT closed by this PR; closure deferred to a separate PR per planning U2.B (PR #229 -> PR #230 precedent).

Feature Parquet persisted (11 projected columns: 3 identity + 1 context anchor + 7 audited PRE_GAME features). PR #230 audit JSON at `reports/artifacts/02_01_01/leakage_audit_sc2egset.json` is byte-unchanged (vacuous `features_audited == []` historical record preserved at its distinct path).

CROSS-02-01-v1.0.1 Section 5 gate condition is mechanically satisfied: `features_audited` non-empty (= 7 PRE_GAME feature columns), `verdict = PASS`, JSON + MD persisted at the spec-named paths.

**Examiner-clarity sentence (verbatim):** `started_at` is projected as a row-identity anchor only (CROSS-02-00 Section 5.1 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is excluded from `features_audited`.

This is the first non-vacuous CROSS-02-01 post-materialization audit for Step 02_01_02 (PR #<TBD>).

## 2. Materialization SQL + source-binding justification

The full `_MATERIALIZATION_QUERY` from `materialize_pre_game_features.py` is reproduced verbatim per Invariant I6:

```sql
WITH mfc_focal AS (
    SELECT
        mfc.replay_id          AS focal_replay_id,
        mfc.toon_id            AS focal_toon_id,
        mfc.race               AS focal_race,
        mfc.is_mmr_missing     AS focal_is_mmr_missing,
        mfc.metadata_mapName   AS map_type,
        mfc.metadata_gameVersion AS patch_version
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT
        mfc.replay_id          AS opp_replay_id,
        mfc.toon_id            AS opponent_toon_id,
        mfc.race               AS opponent_race,
        mfc.is_mmr_missing     AS opponent_is_mmr_missing
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT
        f.focal_replay_id,
        f.focal_toon_id,
        o.opponent_toon_id,
        f.focal_race,
        o.opponent_race,
        f.focal_is_mmr_missing,
        o.opponent_is_mmr_missing,
        f.map_type,
        f.patch_version
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
        AND f.focal_toon_id  <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT
        match_id,
        player_id,
        started_at
    FROM matches_history_minimal
)
SELECT
    CONCAT('sc2egset::', p.focal_replay_id)     AS focal_match_id,
    p.focal_toon_id                              AS focal_player,
    p.opponent_toon_id                           AS opponent_player,
    a.started_at                                 AS started_at,
    p.focal_race                                 AS focal_race,
    p.opponent_race                              AS opponent_race,
    CONCAT(p.focal_race, '_vs_', p.opponent_race) AS race_pair,
    p.map_type                                   AS map_type,
    p.patch_version                              AS patch_version,
    p.focal_is_mmr_missing                       AS focal_is_mmr_missing,
    p.opponent_is_mmr_missing                    AS opponent_is_mmr_missing
FROM mfc_paired p
JOIN mhm_anchor a
    ON a.match_id  = CONCAT('sc2egset::', p.focal_replay_id)
    AND a.player_id = p.focal_toon_id
ORDER BY a.started_at, p.focal_replay_id, p.focal_toon_id
;
```

**Registry-cell upstream-source -> MFC cleaned-view binding** (per `matches_flat_clean.yaml` lines 178-189, quoted verbatim):

```yaml
provenance:
  source_tables:
  - replay_players_raw
  - replays_meta_raw
  - player_history_all
  join_key: NULLIF(regexp_extract(filename, '([0-9a-f]{32})\.SC2Replay\.json', 1),
    '') AS replay_id
  filter: true_1v1_decisive CTE (exactly 2 players, 1 Win + 1 Loss); mmr_valid CTE
    (no MMR<0 player in replay)
  scope: True 1v1 decisive replays only. 22,209 replays, 44,418 rows (2 per replay).
  created_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_data_cleaning_execution.py
  addendum_by: sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_02_duration_augmentation.py
```

The registry CSV (`02_01_01_feature_family_registry.csv`) rows 2, 5, 6 cite `replay_players_raw` (race-pair, matchup, is_mmr_missing) and rows 3, 4 cite `matches_flat` (map, patch) as the *upstream* `source_table_or_event_family`. The Layer-2 materialization reads ALL 5 columns from `matches_flat_clean` (the cleaned, 1v1-scoped VIEW). This is consistent: per the YAML provenance block above, MFC is a cleaned + 1v1-scoped projection over `[replay_players_raw, replays_meta_raw, player_history_all]`. The 1v1 cleaning filter (`true_1v1_decisive` CTE) reduces upstream `matches_flat` (89,944 rows) to `matches_flat_clean` (44,418 rows = 22,209 1v1 replays × 2 rows). The registry's `source_table_or_event_family` cell preserves the *upstream* table binding (the registry is NOT amended by this PR); the materialization-layer binding to the cleaned VIEW is recorded here in the audit MD Section 2 as the authoritative location. This binding is consistent with PR #234 Q1 adjudication (`matches_flat_clean` ratified as the source layer).

## 3. Sanity-check SQL + results

All sanity-check queries are reproduced verbatim per Invariant I6; each is followed by the observed empirical result.

```sql
SELECT COUNT(*) FROM materialized_pre_game_features
```
-- Result: 44418

```sql
SELECT COUNT(DISTINCT focal_match_id) FROM materialized_pre_game_features
```
-- Result: 22209

```sql
SELECT focal_match_id, COUNT(*) AS cnt FROM materialized_pre_game_features GROUP BY 1 HAVING COUNT(*) <> 2
```
-- Result: 0 violating rows (expected 0)

```sql
SELECT COUNT(*) FROM materialized_pre_game_features m1
JOIN materialized_pre_game_features m2
    ON m1.focal_match_id = m2.focal_match_id
    AND m1.focal_player  = m2.opponent_player
    AND m1.opponent_player = m2.focal_player
WHERE m1.focal_race           != m2.opponent_race
   OR m1.opponent_race        != m2.focal_race
   OR m1.focal_is_mmr_missing != m2.opponent_is_mmr_missing
   OR m1.opponent_is_mmr_missing != m2.focal_is_mmr_missing
   OR m1.map_type             != m2.map_type
   OR m1.patch_version        != m2.patch_version
   OR m1.started_at           != m2.started_at
```
-- Result: 0 (expected 0; Invariant I5)

```sql
SELECT
    COUNT(*) FILTER (WHERE focal_race IS NULL) AS null_focal_race,
    COUNT(*) FILTER (WHERE opponent_race IS NULL) AS null_opp_race,
    COUNT(*) FILTER (WHERE race_pair IS NULL) AS null_race_pair,
    COUNT(*) FILTER (WHERE map_type IS NULL) AS null_map,
    COUNT(*) FILTER (WHERE patch_version IS NULL) AS null_patch,
    COUNT(*) FILTER (WHERE focal_is_mmr_missing IS NULL) AS null_focal_mmr_missing,
    COUNT(*) FILTER (WHERE opponent_is_mmr_missing IS NULL) AS null_opp_mmr_missing,
    COUNT(*) FILTER (WHERE started_at IS NULL) AS null_started_at
FROM materialized_pre_game_features
```
-- Result: (0, 0, 0, 0, 0, 0, 0, 0) (each entry must be 0)

```sql
SELECT focal_race, COUNT(*) FROM materialized_pre_game_features GROUP BY 1 ORDER BY 1
```
-- Result: race vocabulary = ['Prot', 'Terr', 'Zerg']

```sql
SELECT focal_is_mmr_missing, COUNT(*) FROM materialized_pre_game_features GROUP BY 1 ORDER BY 1
```
-- Result: FALSE=7128, TRUE=37290

```sql
SELECT COUNT(DISTINCT map_type) FROM materialized_pre_game_features
```
-- Result: 181

```sql
SELECT COUNT(DISTINCT patch_version) FROM materialized_pre_game_features
```
-- Result: 46

## 4. Cutoff structural check + anchor classification

CROSS-02-03-v1.0.1 Section 6.1 states that pre_game families which are static game-T attributes have cutoff = "none (game-T attribute)"; NO strict-`<` history-window filter applies. The 5 tranche-1 families (race-pair, map, patch, matchup, is_mmr_missing) are all static game-T attributes per the closed 02_01_01 registry CSV (allowed_cutoff_rule = `snapshot_at_match_start`). The materialization SQL contains NO `WHERE` predicate on `started_at` and NO strict-`<` between any two timestamp columns. The structural verdict therefore reports **pass-by-design**, with explicit justification recorded here.

Leak-freedom for this tranche rests on the triad: (i) only game-T pre-game columns are read; (ii) POST-GAME token absence (Section 5 below; CROSS-02-01-v1.0.1 Section 2.2); (iii) non-tracker source (Section 5 below; Invariant I3).

**Anchor classification reiteration.** Per CROSS-02-00 Section 5.1 line 360, `started_at` is CONTEXT (not PRE_GAME): "I3 temporal anchor; TRY_CAST from details_timeUTC". Per PR #234 Q2(a) the projected anchor carries `use_as_window_bound = false` and `use_as_row_identity = true`. Per PR #234 Q2(b) the Phase-03 chronological hold-out binding is a RECOMMENDATION ONLY (Phase 03 planning binds; not this PR). Therefore `started_at` is documented in the audit JSON's `projected_context_columns` field and is excluded from `features_audited` -- the 7 audited PRE_GAME feature columns enumerated in Section 1 are exactly the audited set, with no anchor and no identity column.

## 5. POST-GAME token absence + source-table allowlist

POST-GAME tokens (CROSS-02-01-v1.0.1 Section 2.2) are detected via boundary-aware token equality against every column name in the materialized Parquet. The forbidden token set is:

`['duration_seconds', 'final_state', 'is_decisive_result', 'is_duration_suspicious', 'loss', 'match_result', 'outcome', 'post_game', 'result', 'win', 'winner', 'won']`

Result: 0 hits across the 11 projected column names.

Source-table allowlist (Invariant I3; no tracker; PR #234 Q1 binding):

`['matches_flat_clean', 'matches_history_minimal']`

The materialization SQL text was scanned for any FROM/JOIN of a table outside the allowlist (substring detection for `tracker_events_raw`, `player_history_all`, `replay_players_raw`, `matches_flat ` (space-bounded to distinguish from `matches_flat_clean`), `matches_long_raw`). Result: 0 hits.

## 6. Normalization fit-scope

`normalization_fit_scope = training_fold_only` is the CROSS-02-01-v1.0.1 Section 2.3 spec-permitted value. The check is **vacuously satisfied** at this layer because no encoder or scaler is fit during materialization. Raw categorical strings (`focal_race`, `opponent_race`, `race_pair`, `map_type`, `patch_version`) and BOOLEAN values (`focal_is_mmr_missing`, `opponent_is_mmr_missing`) are retained for Phase 03 fold-aware fitting (CROSS-02-02 Section 9.1 G-CS-6 "train-fold-only fit"). The 7-features framing is reiterated: only the 7 PRE_GAME columns above are subject to encoding decisions; `started_at` is excluded because it is a CONTEXT anchor (not a feature to be encoded).

## 7. Reference-window assertion

Per CROSS-02-01-v1.0.1 Section 2.4, the reference window for sc2egset is `ref_start = 2022-08-29`, `ref_end = 2022-12-31` (Phase 01 file at `reports/artifacts/02_01_01/leakage_audit_sc2egset.json`).

The materialization output spans `started_at MIN = 2016-01-07 02:21:46.002000`, `MAX = 2024-12-01 23:48:45.251161` (PR #234 MD Section 3 confirmed empirical range). The materialized output range is strictly larger than the reference window (no contraction has occurred at the materialization layer); Phase 03 will sub-sample the reference window. Verdict = pass.

## 8. Non-substitution + lineage + Phase-03 NON-binding

This audit does **not** replace PR #229 Section 10 design-time verdicts, **does not** replace PR #230 vacuous catalog-only audit, and **does not** replace PR #234 adjudication. All four upstream artifacts remain byte-unchanged at their distinct paths.

Lineage position: this audit + the materialized Parquet form artifact #5 in the 5-artifact lineage for Step 02_01_02 readiness (PR #229 -> PR #230 -> PR #233 -> PR #234 -> this PR).

Phase-03 binding: the PR #234 Q2(b) Phase-03 chronological hold-out RECOMMENDATION (`started_at TIMESTAMP`) is projected here as a column for downstream convenience; the binding decision remains with Phase 03 planning. CROSS-02-02 Section 6.1 minor amendment (proposed in PR #234 Section 8) remains PROPOSED only -- NOT applied here.

This audit is produced under PR #<TBD> alongside the materialization Parquet at `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet`.

Step 02_01_02 NOT closed by this PR; closure deferred to a separate PR per planning U2.B (PR #229 -> PR #230 precedent).
