# Step 01_04_02 -- Data Cleaning Execution Post-Cleaning Validation

**Generated:** 2026-04-17
**Dataset:** sc2egset
**Step:** 01_04_02 -- Act on DS-SC2-01..10

## Summary

Step 01_04_02 applies all 10 cleaning decisions (DS-SC2-01..10) surfaced by the
01_04_01 missingness audit. Both VIEWs are replaced via CREATE OR REPLACE DDL.
No raw tables are modified (Invariant I9). Row counts are unchanged (column-only
cleaning step). All 18 validation assertions pass.

**Final column counts:** matches_flat_clean 49 → 28 (drop 21); player_history_all 51 → 37 (drop 16, add 2, modify 1).

## Per-DS Resolutions

| DS ID | Column | Decision |
|---|---|---|
| DS-SC2-01 | MMR | DROP from both VIEWs; retain is_mmr_missing flag |
| DS-SC2-02 | highestLeague | DROP from both VIEWs |
| DS-SC2-03 | clanTag | DROP from both VIEWs; retain isInClan |
| DS-SC2-04 | result | RETAIN literal strings; ADD is_decisive_result = (result IN ('Win','Loss')) |
| DS-SC2-05 | selectedRace | NO-OP (upstream normalisation already applied by 01_04_01) |
| DS-SC2-06 | gd_mapSizeX/gd_mapSizeY | DROP gd_mapSizeX, gd_mapSizeY, is_map_size_missing from matches_flat_clean; RETAIN in player_history_all |
| DS-SC2-07 | gd_mapAuthorName | DROP from matches_flat_clean (non-predictive metadata); RETAIN in player_history_all |
| DS-SC2-08 | go_* constants (12 cols) | DROP all 12 constant go_* from both VIEWs; retain go_amm, go_clientDebugFlags, go_competitive |
| DS-SC2-09 | handicap | DROP handicap + is_handicap_anomalous from both VIEWs (near-constant, 2 anomalies in 44k) |
| DS-SC2-10 | APM | NULLIF(mf.APM, 0) AS APM + ADD is_apm_unparseable flag |

## Cleaning Registry (new rules in 01_04_02)

| Rule ID | Condition | Action | Justification | Impact |
|---|---|---|---|---|
| drop_mmr_high_sentinel | Always (column drop) | DROP MMR from matches_flat_clean and player_history_all | DS-SC2-01: ledger rate 83.95%/83.65%, Rule S4 / van Buuren 2018 | -1 col each VIEW; rated subset signal preserved via is_mmr_missing |
| drop_highestleague_mid_sentinel | Always | DROP highestLeague from both VIEWs | DS-SC2-02: ledger rate 72.04%/72.16%, Rule S4 non-primary | -1 col each VIEW |
| drop_clantag_mid_sentinel | Always | DROP clanTag from both VIEWs | DS-SC2-03: ledger rate 73.93%/74.10%, Rule S4 non-primary; isInClan retained | -1 col each VIEW |
| add_is_decisive_result | result IN ('Win','Loss') | ADD is_decisive_result BOOLEAN to player_history_all | DS-SC2-04: preserve Undecided/Tie context per Manual 4.2 | +1 col player_history_all |
| drop_mapsize_pred_view | Always | DROP gd_mapSizeX/Y/is_map_size_missing from matches_flat_clean | DS-SC2-06: redundant with metadata_mapName; retained in player_history_all | -3 cols matches_flat_clean |
| drop_mapauthor_pred_view | Always | DROP gd_mapAuthorName from matches_flat_clean | DS-SC2-07: domain-judgement non-predictive metadata | -1 col matches_flat_clean |
| drop_go_constants | n_distinct=1 in either VIEW | DROP 12 constant go_* cols from both VIEWs | DS-SC2-08: ledger constants-detection; zero information | -12 cols each VIEW |
| drop_handicap_near_constant | Always | DROP handicap + is_handicap_anomalous | DS-SC2-09: 2 anomalies in 44k = effectively constant | -2 cols matches_flat_clean (handicap + is_handicap_anomalous); -1 col player_history_all (handicap only) |
| nullif_apm_history | APM = 0 in player_history_all | APM -> NULL via NULLIF; ADD is_apm_unparseable flag | DS-SC2-10: low-rate sentinel + indicator pattern (Manual 4.2) | 1132 APM values -> NULL; +1 col player_history_all |

## CONSORT Column-Count Flow


| VIEW | Cols before | Cols dropped | Cols added | Cols modified | Cols after |
|---|---|---|---|---|---|
| matches_flat_clean | 49 | 21 | 0 | 0 | 28 |
| player_history_all | 51 | 16 | 2 | 1 (APM) | 37 |


## CONSORT Replay-Count Flow (all column-level, no row changes)


| Stage | Replays in matches_flat_clean | Rows | Replays in player_history_all | Rows |
|---|---|---|---|---|
| Before 01_04_02 (post 01_04_01) | 22,209 | 44,418 | 22,390 | 44,817 |
| After 01_04_02 column drops | 22,209 | 44,418 | 22,390 | 44,817 |


## Subgroup Impact (Jeanselme et al. 2024)

| Dropped column | Source decision | Subgroup most affected | Impact |
|---|---|---|---|
| MMR | DS-SC2-01 | Rated players (7128 of 44418 rows = 16.0%) | Lose precise skill signal; is_mmr_missing retained as proxy |
| highestLeague | DS-SC2-02 | Known-league players (~28% of rows per ledger) | Lose league-tier context; no proxy retained (dominated by is_mmr_missing) |
| clanTag | DS-SC2-03 | Players in clans (11578 of 44418 rows = 26.1%) | Lose clan-identity feature; isInClan boolean retained as proxy |
| gd_mapSizeX/gd_mapSizeY | DS-SC2-06 | All players (map-size columns dropped from matches_flat_clean only) | Lose explicit map-area; recoverable from metadata_mapName; retained in player_history_all |
| gd_mapAuthorName | DS-SC2-07 | All players | Lose map author identity (non-predictive metadata); retained in player_history_all |
| 12 go_* constants | DS-SC2-08 | None (constant columns carry no information) | N/A |
| handicap | DS-SC2-09 | 2 anomalous-game rows (0.0045%) | Effectively no-op; near-constant column |

## Validation Results

| Assertion | Status |
|---|---|
| zero_null_replay_id_clean | PASS |
| zero_null_toon_id_clean | PASS |
| zero_null_result_clean | PASS |
| zero_non_decisive_result_clean | PASS |
| zero_null_replay_id_hist | PASS |
| zero_null_toon_id_hist | PASS |
| zero_null_result_hist | PASS |
| symmetry_violations_zero | PASS |
| forbidden_cols_absent_clean | PASS |
| forbidden_cols_absent_hist | PASS |
| new_col_is_decisive_result_present | PASS |
| new_col_is_apm_unparseable_present | PASS |
| apm_nullif_count_1132 | PASS |
| is_decisive_result_false_count_26 | PASS |
| col_count_clean_28 | PASS |
| col_count_hist_37 | PASS |
| row_count_clean_unchanged | PASS |
| row_count_hist_unchanged | PASS |

## SQL Queries (Invariant I6)

All DDL and assertion SQL is stored verbatim in `01_04_02_post_cleaning_validation.json`
under the `sql_queries` key.
