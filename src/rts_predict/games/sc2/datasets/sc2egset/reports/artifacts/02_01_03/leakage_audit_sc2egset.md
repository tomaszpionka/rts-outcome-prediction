# Leakage audit -- sc2egset Step 02_01_03 (post-materialization CROSS-02-01-v1.0.1)

## 1. Non-overclaim disclaimer + non-vacuous audit statement

Step 02_01_03 NOT closed by this PR; closure deferred to a separate U2.B-style PR per PR #237 precedent.

Feature Parquet persisted (28 projected columns: 3 identity + 1 context anchor + 24 audited history-enriched PRE_GAME features spanning the five permitted families per PR #257 ROADMAP amendment (grep token `materialization_scope_amendment_post_pr_255`)).

CROSS-02-01-v1.0.1 Section 5 gate condition is mechanically satisfied: `features_audited` non-empty (= 24 history-enriched PRE_GAME feature columns), `verdict = PASS`, JSON + MD persisted at the spec-named paths.

**Examiner-clarity sentence (verbatim):** `started_at` is projected as a row-identity anchor only (CROSS-02-00 Section 5.1 = CONTEXT; PR #242 Q2 use_as_window_bound = false) and is excluded from `features_audited`.

**B2 cross-game-type per-player win-rate aggregation acknowledgement.** Per Q1 BINDING (PR #242 row Q1_source_layer; `selected_history_source_layer = player_history_all`), the per-player history side aggregates ALL game types (1v1 + 2v2 + 3v3 + 4v4 + FFA). The `focal_prior_win_rate_decisive` and `opponent_prior_win_rate_decisive` features are therefore deliberate cross-game-type rates: a player's 4v4 win-rate contributes to their 1v1 prediction. This is a documented Q1-binding consequence, not an oversight; ranking experiments at Phase 04 will treat this as a baseline measurement of the player-level win-rate signal.

**B2 matchup CTE 1v1-restriction.** The `matchup_history_aggregate` family CTE restricts the shared-replay self-join to 1v1 historical matches via `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`. This prevents 4v4/3v3/2v2 prior teammate-or-opponent encounters from spuriously inflating the head-to-head count. The 1v1 restriction on the matchup CTE -- combined with the cross-game-type per-player win-rate above -- operationalises the intuition that head-to-head is a same-game-type construct while per-player skill aggregates a player's overall activity.

**N9 Invariant I5 citation.** The cross-region indicator pair (`is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any`) goes beyond PR #243's single-indicator text by symmetrising the indicator across focal + opponent. The methodological basis is Invariant I5 (focal/opponent symmetric construction per `.claude/scientific-invariants.md`), not PR #243's text alone.

This is the first non-vacuous CROSS-02-01 post-materialization audit for Step 02_01_03 (PR #<TBD>).

## 2. Verbatim materialization SQL + 17 binding parent provenance

The full `_MATERIALIZATION_QUERY` from `materialize_history_enriched_pre_game_features.py` is reproduced verbatim per Invariant I6:

```sql
WITH mfc_focal AS (
    SELECT mfc.replay_id AS focal_replay_id, mfc.toon_id AS focal_toon_id,
           mfc.race AS focal_race, mfc.metadata_mapName AS focal_map_name
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT mfc.replay_id AS opp_replay_id, mfc.toon_id AS opponent_toon_id,
           mfc.race AS opponent_race
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT f.focal_replay_id, f.focal_toon_id, o.opponent_toon_id,
           f.focal_race, o.opponent_race, f.focal_map_name
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
       AND f.focal_toon_id <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT match_id, player_id, started_at
    FROM matches_history_minimal
),
targets AS (
    SELECT CONCAT('sc2egset::', p.focal_replay_id) AS focal_match_id,
           p.focal_toon_id AS focal_player,
           p.opponent_toon_id AS opponent_player,
           p.focal_race, p.opponent_race, p.focal_map_name,
           a.started_at
    FROM mfc_paired p
    JOIN mhm_anchor a
        ON a.match_id = CONCAT('sc2egset::', p.focal_replay_id)
       AND a.player_id = p.focal_toon_id
),
focal_player_history AS (
    SELECT t.focal_match_id, t.focal_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS focal_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS focal_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.focal_race)
            AS focal_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS focal_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_opp_h
                          WHERE ph_opp_h.replay_id = ph.replay_id
                            AND ph_opp_h.toon_id <> ph.toon_id
                            AND ph_opp_h.race = t.opponent_race))
            AS focal_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.focal_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
opponent_player_history AS (
    SELECT t.focal_match_id, t.opponent_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS opponent_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS opponent_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.opponent_race)
            AS opponent_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS opponent_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_focal_h
                          WHERE ph_focal_h.replay_id = ph.replay_id
                            AND ph_focal_h.toon_id <> ph.toon_id
                            AND ph_focal_h.race = t.focal_race))
            AS opponent_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.opponent_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
matchup_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player, t.opponent_player,
        COUNT(*) FILTER (
            WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
              AND ph_focal.replay_id = ph_opp.replay_id
        ) AS matchup_h2h_count,
        AVG(CASE WHEN ph_focal.result = 'Win' THEN 1.0
                 WHEN ph_focal.result = 'Loss' THEN 0.0 END)
            FILTER (
                WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
                  AND ph_focal.replay_id = ph_opp.replay_id
                  AND ph_focal.is_decisive_result = TRUE
            ) AS matchup_h2h_focal_win_rate
    FROM targets t
    LEFT JOIN player_history_all ph_focal
        ON ph_focal.toon_id = t.focal_player
    LEFT JOIN player_history_all ph_opp
        ON ph_opp.toon_id = t.opponent_player
       AND ph_opp.replay_id = ph_focal.replay_id
    LEFT JOIN matches_flat_clean mfc_h
        ON mfc_h.replay_id = ph_focal.replay_id
       AND mfc_h.toon_id   = ph_focal.toon_id
    GROUP BY t.focal_match_id, t.focal_player, t.opponent_player, t.started_at
),
cross_region_fragmentation_handling AS (
    SELECT t.focal_match_id, t.focal_player,
        BOOL_OR(ph.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_focal_history_any,
        BOOL_OR(ph2.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_opponent_history_any
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
),
in_game_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player,
        AVG(ph.APM) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_apm_prior_mean,
        AVG(ph.SQ) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_sq_prior_mean,
        AVG(ph.supplyCappedPercent)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_supply_capped_pct_prior_mean,
        AVG(ph.header_elapsedGameLoops)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_elapsed_game_loops_prior_mean,
        AVG(ph2.APM) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_apm_prior_mean,
        AVG(ph2.SQ) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_sq_prior_mean,
        AVG(ph2.supplyCappedPercent)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_supply_capped_pct_prior_mean,
        AVG(ph2.header_elapsedGameLoops)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_elapsed_game_loops_prior_mean
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
)
SELECT
    t.focal_match_id, t.focal_player, t.opponent_player,
    t.started_at,
    fph.focal_prior_match_count, fph.focal_prior_win_rate_decisive,
    fph.focal_days_since_prior_match,
    fph.focal_prior_win_rate_race_conditional,
    fph.focal_prior_win_rate_map_conditional,
    fph.focal_prior_win_rate_matchup_conditional,
    oph.opponent_prior_match_count, oph.opponent_prior_win_rate_decisive,
    oph.opponent_days_since_prior_match,
    oph.opponent_prior_win_rate_race_conditional,
    oph.opponent_prior_win_rate_map_conditional,
    oph.opponent_prior_win_rate_matchup_conditional,
    mha.matchup_h2h_count, mha.matchup_h2h_focal_win_rate,
    crfh.is_cross_region_fragmented_focal_history_any,
    crfh.is_cross_region_fragmented_opponent_history_any,
    ighp.focal_apm_prior_mean, ighp.focal_sq_prior_mean,
    ighp.focal_supply_capped_pct_prior_mean,
    ighp.focal_elapsed_game_loops_prior_mean,
    ighp.opponent_apm_prior_mean, ighp.opponent_sq_prior_mean,
    ighp.opponent_supply_capped_pct_prior_mean,
    ighp.opponent_elapsed_game_loops_prior_mean
FROM targets t
LEFT JOIN focal_player_history             fph  USING (focal_match_id, focal_player)
LEFT JOIN opponent_player_history          oph  USING (focal_match_id, opponent_player)
LEFT JOIN matchup_history_aggregate        mha
       USING (focal_match_id, focal_player, opponent_player)
LEFT JOIN cross_region_fragmentation_handling crfh USING (focal_match_id, focal_player)
LEFT JOIN in_game_history_aggregate        ighp USING (focal_match_id, focal_player)
ORDER BY t.started_at, t.focal_match_id, t.focal_player
;
```

**17 BINDING parent artifact SHA-256 pins** (12 Q-chain + 2 omit-closure + 1 registry + 3 tranche-1):

| Source role | SHA-256 |
|-------------|---------|
| PR #242 csv | f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b |
| PR #242 md | fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d |
| PR #243 csv (Q5 = sensitivity_indicator_co_registration) | 29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424 |
| PR #243 md | 026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719 |
| PR #245 csv | 703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0 |
| PR #245 md | 7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419 |
| PR #247 csv | 249e5591c6505b748fe3d371284a72d8f4620f57dbe9628c908ec2fbf097c8ed |
| PR #247 md | 4b49bee405bf87d4b8920b188e2c38d185ecc077b532d64a8bdd5a90cdf143f2 |
| PR #249 csv | 1d9ee22e0523e640181fa0a7a7d2680467a267eefa376fec903f58094118b82f |
| PR #249 md | 8beed3ba6491afb6ba72ee2718b1364c9a2577b26c82237b735d219ccfdc0ea1 |
| PR #251 csv (Q6H terminal) | 8b8b9575ae63003e6dcaf6336030ad6608182a050e96ce805c0a8169cefddbc4 |
| PR #251 md | 5186e356e8a14b53cacf79b6bc32f8606ac2d1df94c87e57a8980186a06f550f |
| PR #255 csv (omit-closure; q5_policy re-elevation) | 831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370 |
| PR #255 md | c48f7035606115e7ec44440d7696a094105928642193f0c486a69118cee19e1d |
| 02_01_01 registry CSV | 320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f |
| PR #236 tranche-1 Parquet | 24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39 |
| PR #236 tranche-1 audit JSON | bdd76ca3ab953668915ec3bcc2b661cf8c3c3802e31d6583a45b59ef18f5aaf6 |
| PR #236 tranche-1 audit MD | 25030c276d80d12abbd9f14249d9e239688cae5ca634ce0f31786be5bfc059c0 |

**R3-N2 defensive lineage-completeness pin.** The `matches_long_raw_yaml_sha256` (= 9c240c0a97e9fb0d41deb857b2de2ce264f53980ee79b44193276ce55d71998b) is a defensive lineage-completeness pin (NOT a read-source pin) to detect future drift if a later revision joins this view; the current materialisation does NOT read `matches_long_raw`. Retained to prevent unnoticed view-schema drift from changing the operational meaning of any future revision.

## 3. Five-family enumeration + audited feature listing

**Five-family permitted set (canonical order; PR #257 amendment lines 2536-2540):**

- `focal_player_history`
- `opponent_player_history`
- `matchup_history_aggregate`
- `cross_region_fragmentation_handling`
- `in_game_history_aggregate`

**Excluded family (PR #257 amendment line 2542):** `reconstructed_rating`

**Excluded columns (PR #257 amendment lines 2546-2548):** `reconstructed_rating_diff`, `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`

**Family -> audited-column count mapping:**

| Family | Column count |
|--------|-------------|
| focal_player_history | 6 |
| opponent_player_history | 6 |
| matchup_history_aggregate | 2 |
| cross_region_fragmentation_handling | 2 |
| in_game_history_aggregate | 8 |
| **TOTAL** | **24** |

**24 audited feature columns (in T03 projection order):**

| # | Feature column | Family |
|---|----------------|--------|
| 1 | `focal_prior_match_count` | `focal_player_history` |
| 2 | `focal_prior_win_rate_decisive` | `focal_player_history` |
| 3 | `focal_days_since_prior_match` | `focal_player_history` |
| 4 | `focal_prior_win_rate_race_conditional` | `focal_player_history` |
| 5 | `focal_prior_win_rate_map_conditional` | `focal_player_history` |
| 6 | `focal_prior_win_rate_matchup_conditional` | `focal_player_history` |
| 7 | `opponent_prior_match_count` | `opponent_player_history` |
| 8 | `opponent_prior_win_rate_decisive` | `opponent_player_history` |
| 9 | `opponent_days_since_prior_match` | `opponent_player_history` |
| 10 | `opponent_prior_win_rate_race_conditional` | `opponent_player_history` |
| 11 | `opponent_prior_win_rate_map_conditional` | `opponent_player_history` |
| 12 | `opponent_prior_win_rate_matchup_conditional` | `opponent_player_history` |
| 13 | `matchup_h2h_count` | `matchup_history_aggregate` |
| 14 | `matchup_h2h_focal_win_rate` | `matchup_history_aggregate` |
| 15 | `is_cross_region_fragmented_focal_history_any` | `cross_region_fragmentation_handling` |
| 16 | `is_cross_region_fragmented_opponent_history_any` | `cross_region_fragmentation_handling` |
| 17 | `focal_apm_prior_mean` | `in_game_history_aggregate` |
| 18 | `focal_sq_prior_mean` | `in_game_history_aggregate` |
| 19 | `focal_supply_capped_pct_prior_mean` | `in_game_history_aggregate` |
| 20 | `focal_elapsed_game_loops_prior_mean` | `in_game_history_aggregate` |
| 21 | `opponent_apm_prior_mean` | `in_game_history_aggregate` |
| 22 | `opponent_sq_prior_mean` | `in_game_history_aggregate` |
| 23 | `opponent_supply_capped_pct_prior_mean` | `in_game_history_aggregate` |
| 24 | `opponent_elapsed_game_loops_prior_mean` | `in_game_history_aggregate` |

## 4. Temporal-filter proof + Q-chain lineage citations

**Strict-< TRY_CAST predicate (Invariant I3; PR #242 Q3 BINDING; B-X2 canonical TRY_CAST):** every per-player, matchup, cross-region, and in-game-history aggregate uses the canonical predicate

```
TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
```

verbatim, with no `<=` or `=` variant. The `is_decisive_result = TRUE` flag is used in place of inline `ph.result IN ('Win', 'Loss')` per the N11 fix (verified to exist as BOOLEAN at `player_history_all.yaml` lines 48-54).

**Q-chain lineage citations:**

- **Q1 (PR #242):** `selected_target_source_layer = matches_flat_clean`; `selected_history_source_layer = player_history_all`. The per-player history side therefore aggregates ALL game types per Q1 BINDING (documented in Section 1).
- **Q2 (PR #242):** `target_anchor = matches_history_minimal.started_at TIMESTAMP`; CONTEXT per CROSS-02-00 Section 5.1.
- **Q3 (PR #242):** strict-< TRY_CAST form ratified (above).
- **Q4 (PR #242):** cold-start gates G-CS-2/3/4/5 at the registry layer; G-CS-6 deferred to Phase 03 fold-aware fit.
- **Q5 (PR #243):** `selected_policy = sensitivity_indicator_co_registration` (BINDING); re-elevated by PR #255 `q5_policy` field. Cross-region indicator pair symmetrised per Invariant I5 (cited in Section 1).
- **Q6 (PR #245):** rating-reconstruction successor adjudication; verdict propagates to PR #255 omit-closure.
- **Q6F (PR #247):** rating-algorithm survey (`recommendation_only_blocked_pending_implementation_proof_pr`).
- **Q6G (PR #249):** rating-implementation proof (`recommendation_only_glicko2`).
- **Q6H (PR #251):** terminal rating-path decision (`recommendation_only_event_by_event_glicko2`).
- **PR #255 omit-closure:** verdict `omit_reconstructed_rating_and_unblock_other_five`; `q5_policy = sensitivity_indicator_co_registration`; the three forbidden `reconstructed_rating_*` columns enumerated.
- **PR #257 ROADMAP amendment:** `materialization_scope_amendment_post_pr_255` token inserted at ROADMAP.md:2525 (host) + 2837 (back-reference); five-family permitted set at lines 2536-2540; excluded family + columns at lines 2542-2548.

- **Q7 IN_GAME_HISTORICAL allowed-column set:** `APM`, `SQ`, `supplyCappedPercent`, `header_elapsedGameLoops` (PR #242 Q7 BINDING). Only these four columns are aggregated (×2 sides = 8 audited columns in `in_game_history_aggregate`).
