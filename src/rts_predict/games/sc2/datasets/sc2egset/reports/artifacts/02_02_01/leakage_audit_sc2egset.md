# Step 02_02_01 — CROSS-02-01-v1.0.1 §3 Leakage Audit

Audit date: 2026-05-30. Verdict: **PASS**. Features audited: 33. Row count: 44,418. Distinct focal_match_count: 22,209.

## §1 — Input artifact lineage (SHAs)

All parent artifacts are byte-stable at the SHAs pinned in §1; SHA recomputation at end-of-run confirms no parent mutation (see §5).

| Artifact | Type | SHA-256 |
| --- | --- | --- |
| `02_01_02_pre_game_features.parquet` | raw bytes | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` |
| `02_01_03_history_enriched_pre_game_features.parquet` | raw bytes | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` |
| `02_01_02_leakage_audit_sc2egset_json_canonical` | canonical JSON | `1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78` |
| `02_01_03_leakage_audit_sc2egset_json_canonical` | canonical JSON | `183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92` |
| `02_02_01_symmetry_difference_feature_adjudication.csv` | raw bytes | `93688970e54b87e800c94bc0ae1ffde6905a5669e0b19a3cf0e614d98af256ba` |
| `02_02_01_symmetry_difference_feature_adjudication.md` | raw bytes | `2245746d730b4b363f17ddb596354cd2746f52e1301a39512b397bb384fdc52d` |

Validator module SHA-256 (raw): `d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753`
Adjudicator module SHA-256 (raw): `94b383631e9b827994f2d31e7a5b526cdc39eaafc8789e3fcc300997897b7117`

## §2 — Row identity / alignment policy and proof

44,418 rows × 37 columns; one-to-one row alignment with 02_01_03 (`focal_match_id`, `focal_player`, `opponent_player`, `started_at` byte-identical to upstream). distinct_focal_match_count = 22,209. The row count is asserted from both the module constant `EXPECTED_OUTPUT_ROW_COUNT = 44_418` AND runtime equality vs the 02_01_03 audit JSON's `row_count` field (Round 1 / N2 defence-in-depth).

## §3 — Per-feature traceability table

Per-family counts: F1=10, F2=10, F3=10, F5=3. All 33 features trace to the audited 24-tuple or Boolean pair sources. F5 (`either, both, xor`) is rank-2 over the 2-dim Boolean source for LogReg with regularisation; retained for tree models per PR #267 Round 2 N3.

| feature | family | direction | source_columns | computation | traces_to_audited_24_tuple |
| --- | --- | --- | --- | --- | --- |
| `focal_minus_opponent_prior_match_count_diff` | F1_difference | focal_minus_opponent | `focal_prior_match_count`, `opponent_prior_match_count` | `focal_prior_match_count - opponent_prior_match_count` | True |
| `focal_minus_opponent_prior_win_rate_decisive_diff` | F1_difference | focal_minus_opponent | `focal_prior_win_rate_decisive`, `opponent_prior_win_rate_decisive` | `focal_prior_win_rate_decisive - opponent_prior_win_rate_decisive` | True |
| `focal_minus_opponent_days_since_prior_match_diff` | F1_difference | focal_minus_opponent | `focal_days_since_prior_match`, `opponent_days_since_prior_match` | `focal_days_since_prior_match - opponent_days_since_prior_match` | True |
| `focal_minus_opponent_prior_win_rate_race_conditional_diff` | F1_difference | focal_minus_opponent | `focal_prior_win_rate_race_conditional`, `opponent_prior_win_rate_race_conditional` | `focal_prior_win_rate_race_conditional - opponent_prior_win_rate_race_conditional` | True |
| `focal_minus_opponent_prior_win_rate_map_conditional_diff` | F1_difference | focal_minus_opponent | `focal_prior_win_rate_map_conditional`, `opponent_prior_win_rate_map_conditional` | `focal_prior_win_rate_map_conditional - opponent_prior_win_rate_map_conditional` | True |
| `focal_minus_opponent_prior_win_rate_matchup_conditional_diff` | F1_difference | focal_minus_opponent | `focal_prior_win_rate_matchup_conditional`, `opponent_prior_win_rate_matchup_conditional` | `focal_prior_win_rate_matchup_conditional - opponent_prior_win_rate_matchup_conditional` | True |
| `focal_minus_opponent_apm_prior_mean_diff` | F1_difference | focal_minus_opponent | `focal_apm_prior_mean`, `opponent_apm_prior_mean` | `focal_apm_prior_mean - opponent_apm_prior_mean` | True |
| `focal_minus_opponent_sq_prior_mean_diff` | F1_difference | focal_minus_opponent | `focal_sq_prior_mean`, `opponent_sq_prior_mean` | `focal_sq_prior_mean - opponent_sq_prior_mean` | True |
| `focal_minus_opponent_supply_capped_pct_prior_mean_diff` | F1_difference | focal_minus_opponent | `focal_supply_capped_pct_prior_mean`, `opponent_supply_capped_pct_prior_mean` | `focal_supply_capped_pct_prior_mean - opponent_supply_capped_pct_prior_mean` | True |
| `focal_minus_opponent_elapsed_game_loops_prior_mean_diff` | F1_difference | focal_minus_opponent | `focal_elapsed_game_loops_prior_mean`, `opponent_elapsed_game_loops_prior_mean` | `focal_elapsed_game_loops_prior_mean - opponent_elapsed_game_loops_prior_mean` | True |
| `prior_match_count_pair_mean` | F2_pair_mean | symmetric | `focal_prior_match_count`, `opponent_prior_match_count` | `(focal_prior_match_count + opponent_prior_match_count) / 2.0` | True |
| `prior_win_rate_decisive_pair_mean` | F2_pair_mean | symmetric | `focal_prior_win_rate_decisive`, `opponent_prior_win_rate_decisive` | `(focal_prior_win_rate_decisive + opponent_prior_win_rate_decisive) / 2.0` | True |
| `days_since_prior_match_pair_mean` | F2_pair_mean | symmetric | `focal_days_since_prior_match`, `opponent_days_since_prior_match` | `(focal_days_since_prior_match + opponent_days_since_prior_match) / 2.0` | True |
| `prior_win_rate_race_conditional_pair_mean` | F2_pair_mean | symmetric | `focal_prior_win_rate_race_conditional`, `opponent_prior_win_rate_race_conditional` | `(focal_prior_win_rate_race_conditional + opponent_prior_win_rate_race_conditional) / 2.0` | True |
| `prior_win_rate_map_conditional_pair_mean` | F2_pair_mean | symmetric | `focal_prior_win_rate_map_conditional`, `opponent_prior_win_rate_map_conditional` | `(focal_prior_win_rate_map_conditional + opponent_prior_win_rate_map_conditional) / 2.0` | True |
| `prior_win_rate_matchup_conditional_pair_mean` | F2_pair_mean | symmetric | `focal_prior_win_rate_matchup_conditional`, `opponent_prior_win_rate_matchup_conditional` | `(focal_prior_win_rate_matchup_conditional + opponent_prior_win_rate_matchup_conditional) / 2.0` | True |
| `apm_prior_mean_pair_mean` | F2_pair_mean | symmetric | `focal_apm_prior_mean`, `opponent_apm_prior_mean` | `(focal_apm_prior_mean + opponent_apm_prior_mean) / 2.0` | True |
| `sq_prior_mean_pair_mean` | F2_pair_mean | symmetric | `focal_sq_prior_mean`, `opponent_sq_prior_mean` | `(focal_sq_prior_mean + opponent_sq_prior_mean) / 2.0` | True |
| `supply_capped_pct_prior_mean_pair_mean` | F2_pair_mean | symmetric | `focal_supply_capped_pct_prior_mean`, `opponent_supply_capped_pct_prior_mean` | `(focal_supply_capped_pct_prior_mean + opponent_supply_capped_pct_prior_mean) / 2.0` | True |
| `elapsed_game_loops_prior_mean_pair_mean` | F2_pair_mean | symmetric | `focal_elapsed_game_loops_prior_mean`, `opponent_elapsed_game_loops_prior_mean` | `(focal_elapsed_game_loops_prior_mean + opponent_elapsed_game_loops_prior_mean) / 2.0` | True |
| `prior_match_count_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_prior_match_count`, `opponent_prior_match_count` | `abs(focal_prior_match_count - opponent_prior_match_count)` | True |
| `prior_win_rate_decisive_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_prior_win_rate_decisive`, `opponent_prior_win_rate_decisive` | `abs(focal_prior_win_rate_decisive - opponent_prior_win_rate_decisive)` | True |
| `days_since_prior_match_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_days_since_prior_match`, `opponent_days_since_prior_match` | `abs(focal_days_since_prior_match - opponent_days_since_prior_match)` | True |
| `prior_win_rate_race_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_prior_win_rate_race_conditional`, `opponent_prior_win_rate_race_conditional` | `abs(focal_prior_win_rate_race_conditional - opponent_prior_win_rate_race_conditional)` | True |
| `prior_win_rate_map_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_prior_win_rate_map_conditional`, `opponent_prior_win_rate_map_conditional` | `abs(focal_prior_win_rate_map_conditional - opponent_prior_win_rate_map_conditional)` | True |
| `prior_win_rate_matchup_conditional_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_prior_win_rate_matchup_conditional`, `opponent_prior_win_rate_matchup_conditional` | `abs(focal_prior_win_rate_matchup_conditional - opponent_prior_win_rate_matchup_conditional)` | True |
| `apm_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_apm_prior_mean`, `opponent_apm_prior_mean` | `abs(focal_apm_prior_mean - opponent_apm_prior_mean)` | True |
| `sq_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_sq_prior_mean`, `opponent_sq_prior_mean` | `abs(focal_sq_prior_mean - opponent_sq_prior_mean)` | True |
| `supply_capped_pct_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_supply_capped_pct_prior_mean`, `opponent_supply_capped_pct_prior_mean` | `abs(focal_supply_capped_pct_prior_mean - opponent_supply_capped_pct_prior_mean)` | True |
| `elapsed_game_loops_prior_mean_pair_abs_diff` | F3_pair_abs_diff | symmetric | `focal_elapsed_game_loops_prior_mean`, `opponent_elapsed_game_loops_prior_mean` | `abs(focal_elapsed_game_loops_prior_mean - opponent_elapsed_game_loops_prior_mean)` | True |
| `cross_region_pair_or` | F5_cross_region_pair | symmetric | `is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any` | `is_cross_region_fragmented_focal_history_any OR is_cross_region_fragmented_opponent_history_any` | True |
| `cross_region_pair_and` | F5_cross_region_pair | symmetric | `is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any` | `is_cross_region_fragmented_focal_history_any AND is_cross_region_fragmented_opponent_history_any` | True |
| `cross_region_pair_xor` | F5_cross_region_pair | symmetric | `is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any` | `is_cross_region_fragmented_focal_history_any XOR is_cross_region_fragmented_opponent_history_any` | True |

## §4 — Leakage check sweep (boundary-aware)

Invariant I3 temporal cutoff is inherited unchanged from 02_01_03's strict-`<` filter (`TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at`). The 02_02 layer applies no new SQL filter; the parent_artifact_shas pin on 02_01_03 audit JSON canonical certifies temporal inheritance. Each of the 10 leakage_checks entries is null (no match).

| Check | Result |
| --- | --- |
| `slot_bias_token_match` | None |
| `post_game_token_match` | None |
| `tracker_raw_source_match` | None |
| `reconstructed_rating_match` | None |
| `future_match_or_phase_03_match` | None |
| `civilization_aoe2_vocabulary_match` | None |
| `matchup_h2h_pair_token_match` | None |
| `race_pair_token_match` | None |
| `pair_sum_token_match` | None |
| `pair_product_token_match` | None |

Note on F5 LogReg redundancy (PR #267 N3): the three Boolean transforms (`cross_region_pair_or`, `cross_region_pair_and`, `cross_region_pair_xor`) are rank-2 over the 2-dimensional Boolean source; for LogReg with regularisation, `or = and ∨ xor` (affine dependency). Retained for gradient-boosted tree models where the redundancy is handled by split selection rather than regularisation.

## §5 — Parent non-mutation assertion

| Artifact | Start-of-run SHA | End-of-run SHA | Equal |
| --- | --- | --- | --- |
| `02_01_02_pre_game_features.parquet` | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` | YES |
| `02_01_03_history_enriched_pre_game_features.parquet` | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` | YES |
| `02_01_02_leakage_audit_sc2egset_json_canonical` | `1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78` | `1da271c62a20bb2666863fd3737ea4fe6006cc9fec03e41ec11d013fb7e54c78` | YES |
| `02_01_03_leakage_audit_sc2egset_json_canonical` | `183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92` | `183b9000d23b5d601b995a61c5ff52aad3fd21ff164bf21f5095fbdf450c9a92` | YES |
| `02_02_01_symmetry_difference_feature_adjudication.csv` | `93688970e54b87e800c94bc0ae1ffde6905a5669e0b19a3cf0e614d98af256ba` | `93688970e54b87e800c94bc0ae1ffde6905a5669e0b19a3cf0e614d98af256ba` | YES |
| `02_02_01_symmetry_difference_feature_adjudication.md` | `2245746d730b4b363f17ddb596354cd2746f52e1301a39512b397bb384fdc52d` | `2245746d730b4b363f17ddb596354cd2746f52e1301a39512b397bb384fdc52d` | YES |

## §6 — Deterministic re-run statement

Two consecutive runs of `materialize_symmetry_difference_features(...)` produce byte-identical Parquet artifacts (SHA-256 equality verified via tmp write). Compression `zstd`, version `2.6`, data_page_version `2.0` (matches PR #259 ZSTD precedent at `materialize_history_enriched_pre_game_features.py:1041-1052`).

## §7 — Explicit no-closure / no-status-YAML disclaimer

Step 02_02_01 is NOT closed by this PR. `STEP_STATUS.yaml` has no `02_02_01` row. `PIPELINE_SECTION_STATUS.yaml` has no `02_02` row. `PHASE_STATUS.yaml` is byte-unchanged (Phase 02 in_progress; Phase 03 not_started). `ROADMAP.md` is byte-unchanged. Closure follows in a separate U2.B-style PR per PR #237 / PR #262 precedent. Phase 03 not started. No baseline modelling.
