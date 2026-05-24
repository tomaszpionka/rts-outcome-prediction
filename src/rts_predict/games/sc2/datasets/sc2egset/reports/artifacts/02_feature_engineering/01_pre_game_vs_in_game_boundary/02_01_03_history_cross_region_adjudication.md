# SC2EGSet Step 02_01_03 — Q5 Cross-Region Retention Successor Adjudication

## §1 Non-Materialization Disclaimer

This artifact is a Q5 successor adjudication of the cross-region fragmentation operationalization for sc2egset Step 02_01_03 (tranche-2, 6 history-enriched pre_game families). It does NOT materialize any feature value, does NOT write any Parquet, does NOT run the CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT close Step 02_01_03, and does NOT append to any status YAML or research_log. Materialization remains FUTURE.

## §2 Parent PR #242 Lineage

This artifact upgrades the PR #242 parent adjudication's Q5 row (`Q5_cross_region_policy`, which closed as `verdict=deferred_blocker`). PR #242 byte-stable artifacts are referenced by SHA-256 on every row (`parent_pr242_csv_sha256`, `parent_pr242_md_sha256`, `parent_pr242_artifact_sha256`).

## §3 Q5-Only Scope (Q6 Out of Scope)

Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

## §4 Per-Option Decision Table

| decision_id | cross_region_policy | history_row_filter_on_pha_applied | anchor_semantics | verdict |
|---|---|---|---|---|
| `Q5A_strict_exclusion_retention` | `strict_exclusion` | `yes` | `toon_id_based` | `deferred_recommendation` |
| `Q5B_dual_feature_path_retention` | `dual_feature_path` | `yes` | `toon_id_based` | `deferred_recommendation` |
| `Q5C_sensitivity_indicator_retention` | `sensitivity_indicator_co_registration` | `no` | `toon_id_based` | `deferred_recommendation` |
| `Q5_selected_policy` | `sensitivity_indicator_co_registration` | `no` | `toon_id_based` | `narrow_with_evidence` |
| `Q5_per_family_impact_summary` | `(none)` | `not_applicable` | `both` | `ratify_with_evidence` |

## §5 Per-Family Retention Table (BINDING Evidence)

Family-level PHA history retention under strict_exclusion: `258849` kept / `1318070` dropped / `1576919` total (`16.4149%` retention).

## §6 SQL Probe Outputs (Verbatim per Invariant I6)

### §6.1 BINDING toon_id-membership probe (NIT-C)

```sql
SELECT COUNT(*) AS n_pha_rows_toonid_membership_anchored
FROM player_history_all ph
WHERE ph.toon_id IN (
  SELECT DISTINCT toon_id
  FROM player_history_all
  WHERE is_cross_region_fragmented = TRUE
)
```

Observed count: `37101`.

### §6.2 EQUIVALENCE nickname-anchored probe (NIT-C; 01_05_10 §3.3 SQL 3)

```sql
WITH cross_region_nicks AS (
  SELECT LOWER(nickname) AS nick
  FROM replay_players_raw
  GROUP BY 1
  HAVING COUNT(DISTINCT region) > 1
)
SELECT
  (SELECT COUNT(*) FROM cross_region_nicks) AS n_cross_region_nicknames,
  (SELECT COUNT(DISTINCT ph.toon_id)
     FROM player_history_all ph
     WHERE ph.is_cross_region_fragmented = TRUE) AS n_cross_region_toon_ids,
  (SELECT COUNT(*)
     FROM player_history_all ph
     INNER JOIN cross_region_nicks crn ON LOWER(ph.nickname) = crn.nick
     WHERE ph.details_timeUTC IS NOT NULL) AS n_player_match_pairs_nickname_anchored
```

Observed: `(n_nicknames=246, n_toon_ids=1923, n_player_match_pairs=32031)`. Expected: `(246, 1923, 32031)`.

### §6.3 Strict-exclusion retention probe (B3)

```sql
WITH base AS (
  SELECT
    target.match_id       AS target_match_id,
    target.player_id      AS target_player,
    target.started_at     AS target_started_at,
    ph.replay_id          AS history_replay_id,
    ph.toon_id            AS history_toon_id,
    ph.details_timeUTC    AS history_time,
    ph.is_cross_region_fragmented AS history_is_xr
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
)
-- 3.A OPTION (a) fix (PR #243 Dispatch 3): the base CTE is a LEFT JOIN on
-- player_history_all, so cold-start target rows (no prior PHA history)
-- contribute a row with history_is_xr IS NULL. Those NULL rows cannot be
-- counted as kept (FALSE) or dropped (TRUE), so including them in
-- history_rows_total would falsely break the kept + dropped == total smoke
-- invariant. Restrict history_rows_total to rows with an actual matched
-- history record (history_is_xr IS NOT NULL); the cold-start NULL rows are
-- not a retention measurement.
SELECT
  COUNT(*) FILTER (WHERE history_is_xr = FALSE)                            AS history_rows_kept,
  COUNT(*) FILTER (WHERE history_is_xr = TRUE)                             AS history_rows_dropped,
  COUNT(DISTINCT history_toon_id) FILTER (WHERE history_is_xr = TRUE)      AS players_affected,
  COUNT(DISTINCT target_match_id) FILTER (WHERE history_is_xr = TRUE)      AS matches_affected,
  COUNT(*) FILTER (WHERE history_is_xr IS NOT NULL)                        AS history_rows_total
FROM base
```

Observed: `{'history_rows_kept': 258849, 'history_rows_dropped': 1318070, 'players_affected': 1906, 'matches_affected': 20397, 'history_rows_total': 1576919}`.

### §6.4 Dual-feature-path branch probe

```sql
WITH base AS (
  SELECT
    target.match_id  AS target_match_id,
    target.player_id AS target_player,
    target.started_at,
    ph.is_cross_region_fragmented AS history_is_xr,
    ph.replay_id     AS history_replay_id
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
),
branched AS (
  SELECT
    target_match_id,
    target_player,
    COUNT(*) FILTER (WHERE history_is_xr = FALSE) AS nonxr_branch_count,
    COUNT(*) FILTER (WHERE history_is_xr = TRUE)  AS xr_branch_count
  FROM base
  GROUP BY target_match_id, target_player
)
SELECT
  COUNT(*)                                              AS n_target_rows,
  SUM(CASE WHEN nonxr_branch_count > 0 THEN 1 ELSE 0 END) AS n_nonxr_nondegenerate,
  SUM(CASE WHEN xr_branch_count > 0 THEN 1 ELSE 0 END)    AS n_xr_nondegenerate,
  SUM(nonxr_branch_count)                                 AS total_nonxr_rows,
  SUM(xr_branch_count)                                    AS total_xr_rows
FROM branched
```

Observed: `{'n_target_rows': 44418, 'n_nonxr_nondegenerate': 7047, 'n_xr_nondegenerate': 34901, 'total_nonxr_rows': 258849, 'total_xr_rows': 1318070}`.

### §6.5 Sensitivity-indicator probe (target-time anchored)

```sql
WITH base AS (
  SELECT
    target.match_id  AS target_match_id,
    target.player_id AS target_player,
    target.started_at,
    BOOL_OR(ph.is_cross_region_fragmented) AS sensitivity_flag,
    COUNT(*)                                AS history_rows_in_window
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
  GROUP BY target.match_id, target.player_id, target.started_at
)
SELECT
  COUNT(*)                                                AS n_target_rows,
  SUM(CASE WHEN sensitivity_flag = TRUE  THEN 1 ELSE 0 END) AS n_flag_true,
  SUM(CASE WHEN sensitivity_flag = FALSE THEN 1 ELSE 0 END) AS n_flag_false,
  SUM(CASE WHEN sensitivity_flag IS NULL THEN 1 ELSE 0 END) AS n_flag_null,
  SUM(history_rows_in_window)                             AS total_history_rows
FROM base
```

Observed: `{'n_target_rows': 44418, 'n_flag_true': 34901, 'n_flag_false': 7047, 'n_flag_null': 2470, 'total_history_rows': 1579389}`.

### §6.6 Family-level impact probe

```sql
WITH base AS (
  SELECT
    ph.is_cross_region_fragmented AS history_is_xr,
    ph.toon_id                    AS history_toon_id
  FROM matches_flat_clean mfc
  JOIN matches_history_minimal target
    ON target.match_id  = 'sc2egset::' || mfc.replay_id
   AND target.player_id = mfc.toon_id
  LEFT JOIN player_history_all ph
    ON ph.toon_id = mfc.toon_id
   AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
)
SELECT
  COUNT(*) FILTER (WHERE history_is_xr = FALSE)                            AS history_rows_kept,
  COUNT(*) FILTER (WHERE history_is_xr = TRUE)                             AS history_rows_dropped,
  COUNT(DISTINCT history_toon_id) FILTER (WHERE history_is_xr = TRUE)      AS players_affected,
  COUNT(*)                                                                 AS history_rows_total
FROM base
```

Observed: `{'history_rows_kept': 258849, 'history_rows_dropped': 1318070, 'players_affected': 1906, 'history_rows_total': 1579389}`.

## §7 Toon_id vs Nickname Anchor Semantics (NIT-C)

Two cross-region anchor semantics are evaluated: the BINDING probe (toon_id-membership; aligns with the downstream `WHERE ph.is_cross_region_fragmented = TRUE` predicate) and the EQUIVALENCE probe (lowercase nickname join; reproduces the 01_05_10 §3.3 SQL 3 idiom). The 32,031 anchor is shared ONLY by the EQUIVALENCE probe.

## §8 Target-Filter vs History-Filter Distinction (B3)

The Q5 filter is applied to PHA HISTORY rows (`WHERE NOT ph.is_cross_region_fragmented` BEFORE aggregation), NOT to MFC TARGET rows. MFC has no `is_cross_region_fragmented` column (30-col schema). The MFC-target-row drop alternative is OUT OF SCOPE per A4 + A17.

## §9 Structured Field Explanation (NIT-D)

The `history_row_filter_on_pha_applied` field replaces the round-2 vacuous prose-substring assertion with a tri-valued enum (`yes`/`no`/`not_applicable`). Per-option consistency: Q5A=`yes`, Q5B=`yes`, Q5C=`no`, Q5_selected_policy=mirror of selected_policy (or `not_applicable` for deferred verdicts), Q5_per_family_impact_summary=`not_applicable`. The SQL byte-scan portion (reject any MFC-aliased `is_cross_region_fragmented` predicate) is KEPT separately as `q5_filter_target_is_pha_history_violated_sql`.

## §10 Materialization Blocked Until Q6 Resolved

Q5 may upgrade from `deferred_blocker` (PR #242) to `bind_now`/`ratify_with_evidence`/`extend_with_evidence`/`narrow_with_evidence` in this PR per the Q5_selected_policy row. Q6 (rating policy) remains `deferred_blocker`; the future Layer-3 materialization PR must NOT proceed until Q6 is upgraded in a separate successor adjudication PR.

## §11 No Q6 Decision Here

Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

## §12 No Step Closure / No Phase 03 Start

Step 02_01_03 remains OPEN. This artifact does NOT add `02_01_03: complete` to `STEP_STATUS.yaml`. Phase 03 work remains forbidden.

## §13 Per-Decision Sections

### Q5A_strict_exclusion_retention — Cross-region option (a) strict_exclusion — per-family PHA history retention measurement

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
- **Cross-region policy:** `strict_exclusion`
- **Cross-region anchor semantics:** `toon_id_based`
- **History-row filter on PHA applied:** `yes`
- **Retention counts:**

```json
{"all_six_families": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}}
```

**Retention measurement summary:** Strict exclusion drops 1318070 PHA history rows / 1906 players / 20397 target matches at the aggregation layer; PHA history retention (258849 kept / 1576919 total) computed via WHERE NOT ph.is_cross_region_fragmented applied to HISTORY rows BEFORE aggregation.

**Rationale / notes:**

Q5A evaluates option (a) strict_exclusion (CROSS-02-02 §6.2 row 5). Counts measure PHA HISTORY rows kept/dropped under `WHERE NOT ph.is_cross_region_fragmented` applied BEFORE aggregation (round-2 B3 binding). Anchored on toon_id-membership (round-3 NIT-C / A19). Strict-< filter: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (B-X2 inherited).

VERBATIM CROSS-02-02 §6.2 row 5 line 242, Source column: `player_history_all.is_cross_region_fragmented` (CROSS-02-00 §5.4)

VERBATIM CROSS-02-02 §6.2 row 5 line 242, Constraint column: Phase 02 must implement one of: (a) strict-exclusion sensitivity arm, (b) dual feature paths (with vs without filter), or (c) sensitivity indicator co-registered alongside the history features.

VERBATIM 01_04_05 §7 strategy 1 lines 203-208: Safe-subset filter: `WHERE NOT is_cross_region_fragmented` -- restricts history to non-fragmented players; cleanest rolling-window estimates but reduces the training population to 7,716 / 44,817 rows = 17.2% of the corpus (tournament players are over-represented among the 1,923 flagged toons; see Sec.4 flag distribution). This is a material data loss; strategy (2) or (3) are usually preferable for non-catastrophic bias levels.

VERBATIM PHA YAML NOTES lines 220-226: Phase 02 rolling features over `player_id_worldwide` should apply `WHERE NOT is_cross_region_fragmented` as safe-subset filter, OR use dual feature paths, OR use as sensitivity indicator. Blanket flag (no handle-length filter) by design -- false positives bounded by short-handle count (see 01_04_05 Sec.6 conservatism argument). Empirical grounding from WP-3 (01_05_10): median_rolling30_undercount=16, p95=29 on flagged toons.

Comparison to 01_05_10 W=30 noise-floor sqrt(30) ~ 5.5 (Hollander and Wolfe 1999 §11.2): retention loss compared against this noise-floor establishes whether the discard is material vs measurement noise.

No target-match outcome read; no future matches read; no global batch fit; deterministic SQL probe via `_STRICT_EXCLUSION_HISTORY_FILTER_RETENTION_QUERY`. RISK-20 reference: risk_register_sc2egset.md (SC-R01 MEDIUM IDENTITY entry). This row replaces the empirical part of PR #242 Q5 only; the binding policy is the Q5_selected_policy row. Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.json
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
```

**Falsifiers:**

```
strict_exclusion_history_filter_retention_smoke_failed:did_not_fire
cross_region_toon_id_anchor_count_drift:did_not_fire
```

### Q5B_dual_feature_path_retention — Cross-region option (b) dual_feature_path — per-branch PHA history coverage measurement

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
- **Cross-region policy:** `dual_feature_path`
- **Cross-region anchor semantics:** `toon_id_based`
- **History-row filter on PHA applied:** `yes`
- **Retention counts:**

```json
{"all_six_families": {"history_rows_kept": 1576919, "history_rows_dropped": 0, "retention_pct": 100.0, "nonxr_branch_target_rows": 7047, "xr_branch_target_rows": 34901}}
```

**Retention measurement summary:** Dual feature path: history retention 100% (258849 non-XR + 1318070 XR PHA history rows); 7047 target rows have nondegenerate non-XR branch coverage; 34901 target rows have nondegenerate XR branch coverage.

**Rationale / notes:**

Q5B evaluates option (b) dual_feature_path (CROSS-02-02 §6.2 row 5). Both XR and non-XR PHA history branches are materialized as separate columns; history-row retention is 100% but per-branch sparsity may produce degenerate sub-features for cross-region players. Anchored on toon_id-membership (round-3 NIT-C / A19). Strict-< filter: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`.

VERBATIM 01_04_05 §7 strategy 2 lines 210-212: Dual feature paths: Compute rolling-window features for all players, then add `is_cross_region_fragmented` as a covariate in the model. The model learns to adjust for the known fragmentation bias.

No target-match outcome read; no future matches read; no global batch fit; deterministic SQL probe via `_DUAL_FEATURE_PATH_RETENTION_QUERY`. Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
```

**Falsifiers:**

```
dual_feature_path_branch_degenerate:did_not_fire
```

### Q5C_sensitivity_indicator_retention — Cross-region option (c) sensitivity_indicator_co_registration — per-target flag nondegeneracy measurement (anchored at target.started_at)

- **Verdict:** `deferred_recommendation`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
- **Cross-region policy:** `sensitivity_indicator_co_registration`
- **Cross-region anchor semantics:** `toon_id_based`
- **History-row filter on PHA applied:** `no`
- **Retention counts:**

```json
{"all_six_families": {"history_rows_kept": 1579389, "history_rows_dropped": 0, "retention_pct": 100.0, "n_flag_true": 34901, "n_flag_false": 7047, "n_flag_null": 2470}}
```

**Retention measurement summary:** Sensitivity indicator co-registration anchored at target.started_at: PHA history retention 100% (1579389 rows); per-target boolean-OR flag distribution n_true=34901 / n_false=7047 / n_null=2470.

**Rationale / notes:**

Q5C evaluates option (c) sensitivity_indicator_co_registration (CROSS-02-02 §6.2 row 5). No PHA history rows dropped; a single `is_cross_region_fragmented` flag is co-registered alongside the 6 history feature columns, anchored at target.started_at via `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` over the player's strictly-prior PHA history window. Anchored on toon_id-membership (round-3 NIT-C / A19).

VERBATIM 01_04_05 §7 strategy 3 lines 214-216: Sensitivity indicator: Use the flag to partition evaluation metrics by `is_cross_region_fragmented` and report differential model performance. Documents remaining bias for the thesis.

Co-registration semantics: for each target row, project the boolean-OR of `ph.is_cross_region_fragmented` over the player's strictly-prior PHA history window per `STRICT_LT_HISTORY_FILTER`. Flag nondegeneracy verified by `_SENSITIVITY_INDICATOR_RETENTION_QUERY`. No target-match outcome read; no future matches read; no global batch fit. Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
```

**Falsifiers:**

```
sensitivity_indicator_flag_degenerate:did_not_fire
sensitivity_indicator_post_game_token_in_scoped_field:did_not_fire
```

### Q5_selected_policy — Q5 cross-region policy selection (BINDING row; verdict emerges from per-family retention table per A14)

- **Verdict:** `narrow_with_evidence`
- **Binding level:** `recommendation_only`
- **Scope:** `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
- **Cross-region policy:** `sensitivity_indicator_co_registration`
- **Cross-region anchor semantics:** `toon_id_based`
- **History-row filter on PHA applied:** `no`
- **Retention counts:**

```json
{"all_six_families": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}}
```

**Retention measurement summary:** Selected policy: 'sensitivity_indicator_co_registration'; verdict 'narrow_with_evidence'; PHA history retention 258849/1576919 under strict_exclusion; family-impact total rows 1579389 (kept 258849 / dropped 1318070).

**Rationale / notes:**

Q5_selected_policy is the BINDING row for the Q5 successor adjudication. PROVISIONAL recommendation (round-2 N3 / A14: VERDICT EMERGES FROM TABLE): narrow_with_evidence with selected_policy=sensitivity_indicator_co_registration (option (c)). Rationale: option (c) preserves full PHA history-row retention while honoring the 01_05_10 W=30 FAIL verdict by providing the sensitivity-arm input that the Phase-03 model can use to stratify; option (a) discards the strict_exclusion-probe-reported number of PHA history rows whose cardinality the per-family table quantifies; option (b) introduces per-branch PHA sparsity that defeats the smoothing motivation of matchup_history_aggregate (G-CS-3).

VERDICT EMERGED FROM TABLE: see Q5A/Q5B/Q5C per-option retention triples; the Q5_per_family_impact_summary row records the per-family broadcast.

MATERIALIZATION GATE: the future materialization PR consumes this row's selected_policy + cross_region_policy fields as the keying input for the cross_region_fragmentation_handling family materialization SQL. The MFC-target-row drop alternative is OUT OF SCOPE per A4 + A17 (filter applies to PHA HISTORY rows, not MFC TARGET rows). Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.json
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md
```

**Falsifiers:**

```
q5_evidence_sufficiency_violated:did_not_fire
```

### Q5_per_family_impact_summary — Q5 per-family impact summary (derived row; broadcasts the family-level retention over the 6 history-enriched pre_game families)

- **Verdict:** `ratify_with_evidence`
- **Binding level:** `binding_for_materialization`
- **Scope:** `all_six_history_enriched_pre_game_families`
- **Cross-region policy:** `(none)`
- **Cross-region anchor semantics:** `both`
- **History-row filter on PHA applied:** `not_applicable`
- **Retention counts:**

```json
{"sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}, "sc2egset.history_enriched_pre_game.focal_player_history": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}, "sc2egset.history_enriched_pre_game.in_game_history_aggregate": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}, "sc2egset.history_enriched_pre_game.matchup_history_aggregate": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}, "sc2egset.history_enriched_pre_game.opponent_player_history": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}, "sc2egset.history_enriched_pre_game.reconstructed_rating": {"history_rows_kept": 258849, "history_rows_dropped": 1318070, "retention_pct": 16.4149}}
```

**Retention measurement summary:** Family-level impact summary: PHA history rows kept=258849 / dropped=1318070 / total=1579389 broadcast over the 6 history-enriched pre_game families.

**Rationale / notes:**

Q5_per_family_impact_summary is the derived per-family broadcast row. The cross_region_retention_counts JSON keys are the 6 history-enriched pre_game family IDs; values are the (kept, dropped, retention_pct) triples broadcast from `_FAMILY_LEVEL_IMPACT_QUERY` over PHA HISTORY rows (round-2 B3). Anchor semantics='both' (carries data from both the toon_id-membership BINDING probe and the nickname-anchored EQUIVALENCE probe per round-3 NIT-C). history_row_filter_on_pha_applied='not_applicable' (the summary row makes no per-option commitment; the binding policy lives in Q5_selected_policy).

Q6 (rating policy) remains deferred_blocker per PR #242; out of scope for PR #243.

**Evidence paths:**

```
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.md
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/cross_region_history_impact_sc2egset.json
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_05_cross_region_annotation.md
reports/specs/02_02_feature_engineering_plan.md
src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml
src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv
```

**Falsifiers:**

```
q5_evidence_sufficiency_violated:did_not_fire
```

## §14 Falsifier Roll-Call

Every falsifier in `FALSIFIER_PRIORITY_CHAIN`:

- `parent_pr242_csv_sha256_mismatch`: did_not_fire
- `parent_pr242_md_sha256_mismatch`: did_not_fire
- `pr241_sha256_mismatch`: did_not_fire
- `cross_region_01_05_10_md_sha256_mismatch`: did_not_fire
- `cross_region_01_05_10_json_sha256_mismatch`: did_not_fire
- `player_history_all_yaml_sha256_mismatch`: did_not_fire
- `step_01_04_05_md_sha256_mismatch`: did_not_fire
- `matches_flat_clean_yaml_sha256_mismatch`: did_not_fire
- `cross_02_02_spec_sha256_mismatch`: did_not_fire
- `mfc_cross_region_column_referenced`: did_not_fire
- `cross_region_toon_id_anchor_count_drift`: did_not_fire
- `cross_region_nickname_anchor_count_drift`: did_not_fire
- `strict_lt_filter_divergence`: did_not_fire
- `decision_count_drift`: did_not_fire
- `q5_three_options_not_enumerated`: did_not_fire
- `strict_exclusion_history_filter_retention_smoke_failed`: did_not_fire
- `dual_feature_path_branch_degenerate`: did_not_fire
- `sensitivity_indicator_flag_degenerate`: did_not_fire
- `sensitivity_indicator_post_game_token_in_scoped_field`: did_not_fire
- `q5_evidence_sufficiency_violated`: did_not_fire
- `q5_post_game_token_in_scoped_field`: did_not_fire
- `q5_direct_target_match_outcome_referenced`: did_not_fire
- `q5_future_match_leakage_referenced`: did_not_fire
- `q5_global_batch_fit_referenced`: did_not_fire
- `q5_phase_03_baseline_creep`: did_not_fire
- `history_row_filter_on_pha_field_invalid`: did_not_fire
- `q5_filter_target_is_pha_history_violated_sql`: did_not_fire
- `materialization_creep`: did_not_fire
- `status_yaml_drift`: did_not_fire
- `research_log_drift`: did_not_fire
- `q6_scope_creep`: did_not_fire

## §15 SHA Provenance

- `pr241_scaffold_validator_module_sha256`: `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904`
- `parent_pr242_csv_sha256`: `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b`
- `parent_pr242_md_sha256`: `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d`
- `parent_pr242_artifact_sha256`: `8da7c3b53f028b58ac11c094b435a95a5c7097ed8e1fa5596809c7faf027c97a`
- `provenance_01_05_10_md_sha256`: `409e36acae1b09570588a090a000b821883c390112f32f04e1fa502143ede71e`
- `provenance_01_05_10_json_sha256`: `591d9170ab5a5d465cdb3cfbf9e98f99282de6043ca788d68104d581bc31ed9b`
- `player_history_all_yaml_sha256`: `7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0`
- `step_01_04_05_md_sha256`: `7bac26fd69952509a9dac323436e074902ca8ba9e0bac64021ad04de7f5dc9fe`
- `matches_flat_clean_yaml_sha256`: `9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f`
- `cross_02_02_spec_sha256`: `86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289`
