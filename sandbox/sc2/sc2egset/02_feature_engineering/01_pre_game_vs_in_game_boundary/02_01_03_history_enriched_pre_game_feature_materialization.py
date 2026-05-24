# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 02_01_03 — History-enriched pre_game feature-family materialization SCAFFOLD: sc2egset
#
# **SCAFFOLD + ONE VALIDATION MODULE (non-batching sequence step 2 of 9).**
# This notebook is **scaffold-only**: it declares the DESIGN CONTRACT for the
# 6 tranche-2 `history_enriched_pre_game` families and exercises the
# `validate_history_enriched_pre_game_materialization` validator. NO feature
# value is materialised. NO Parquet is written. NO `STEP_STATUS.yaml`,
# `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml` is mutated. NO
# `research_log.md` entry is appended.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessors:** 02_01_02 (closed, PR #237 closure);
# transitive 02_01_01 (closed). **Lineage position:** artifact #2 of N for
# Step 02_01_03 readiness (PR #239 ROADMAP stub preceded; this scaffold is
# the second non-batching deliverable; future PRs will produce tranche-2
# source/anchor/cold-start adjudication, materialization-execution plan,
# materialization-execution, audit, and closure).

# %% [markdown]
# ## NO materialization, NO artifact banner
#
# This scaffold does NOT:
# - materialize any feature value;
# - execute any projection SQL against the DuckDB;
# - write any file under `reports/artifacts/02_01_03/`;
# - update `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`;
# - append a `research_log.md` entry (dataset or root);
# - close Step 02_01_03;
# - begin Step 02_01_04 or Phase 03;
# - patch any cleaning-layer YAML or spec;
# - re-execute the §10 verdict audit or the CROSS-02-01 leakage audit.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.validate_history_enriched_pre_game_materialization import (  # noqa: E501
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
    validate_history_enriched_pre_game_materialization,
)

# %% [markdown]
# ## Tranche-2 history_enriched_pre_game families — design table
#
# The 6 tranche-2 families are the closed 02_01_01 registry CSV's
# `history_enriched_pre_game` rows (rows 7-12). All carry
# `prediction_setting=history_enriched_pre_game`,
# `source_table_or_event_family=matches_flat` (registry-recorded; view-vs-raw
# refinement is deferred — see view-vs-raw cell below),
# `temporal_anchor=details_timeUTC`,
# `allowed_cutoff_rule=history_time < target_time` (strict-`<`, never `<=`),
# `per_player_construction=symmetric`. 5 rows carry `status=allowed`; the
# `cross_region_fragmentation_handling` row carries `status=allowed_with_caveat`.
#
# | family_id | candidate_leakage_modes | cold_start_handling | status |
# |-----------|------------------------|---------------------|--------|
# | sc2egset.history_enriched_pre_game.focal_player_history | rolling_includes_target_game | G-CS-2 | allowed |
# | sc2egset.history_enriched_pre_game.opponent_player_history | rolling_includes_target_game | G-CS-2 | allowed |
# | sc2egset.history_enriched_pre_game.matchup_history_aggregate | h2h_includes_target_game | G-CS-3 | allowed |
# | sc2egset.history_enriched_pre_game.reconstructed_rating | rating_uses_target_game_outcome | G-CS-4 | allowed |
# | sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling | cross_region_history_drop | G-CS-5 | allowed_with_caveat |
# | sc2egset.history_enriched_pre_game.in_game_history_aggregate | rolling_includes_target_game | G-CS-2 | allowed |

# %% [markdown]
# ## Context and input artifacts
#
# This notebook binds to four predecessor artifacts (all read-only):
#
# - **Closed 02_01_01 registry CSV** (authoritative catalog for the 6 tranche-2 families):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
# - **PR #229 §10 design-time verdict-audit CSV** (per-family design-time verdicts; rows 7-12 cover tranche-2):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv`
# - **PR #234 source/anchor/race adjudication CSV** (tranche-1 reference; format precedent for the future tranche-2 adjudication PR):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_source_anchor_race_adjudication.csv`
# - **PR #236 materialised 02_01_02 Parquet** (tranche-1 evidence; read as upstream evidence only, NOT re-materialised):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet`

# %% [markdown]
# ## What `matches_history_minimal` is consumed for (PR #239 nit)
#
# The Step 02_01_03 ROADMAP block's `inputs.duckdb_tables` list includes
# `matches_history_minimal` (MHM) alongside `matches_flat_clean` (MFC) and
# `player_history_all`. The body `method` text references MFC and
# `player_history_all` directly; MHM is consumed for two distinct purposes:
#
# 1. **Cold-start enumeration G-CS-2 / G-CS-3 / G-CS-4 / G-CS-5.** MHM
#    enumerates the set of `(focal_player, target.started_at)` target rows
#    over which prior history is counted (the support set for the
#    cold-start gating decision — "does this player have ≥ K prior matches
#    by `started_at`?").
# 2. **Row-identity anchor `started_at`.** Per PR #234 Q2(a),
#    `started_at TIMESTAMP` is the BINDING Phase-02 row-identity anchor
#    (`use_as_window_bound = false`, `use_as_row_identity = true`). MHM is
#    the canonical source of `started_at` joined back onto MFC.
#
# **Resolution DEFERRED** to the future tranche-2 source/anchor/cold-start
# adjudication PR (analogous to PR #234 for tranche-1). The scaffold records
# only the consumption purpose; the validator does NOT runtime-check this
# prose (this requirement is enforced procedurally by reviewer-deep reading
# this cell, per the merged plan's Assumption A8).

# %% [markdown]
# ## View-vs-raw source layer deferral (N7 / PR #234 precedent)
#
# The 02_01_01 registry CSV records `source_table_or_event_family =
# matches_flat` (raw layer) for all 6 history families. The Step 02_01_03
# ROADMAP block's `inputs.duckdb_tables` lists `matches_flat_clean` (the
# 1v1-scoped cleaned-raw view used by tranche-1 per PR #234 Q1 = MFC) plus
# `player_history_all` and `matches_history_minimal`. This is a known
# registry-vs-ROADMAP source-layer divergence (`matches_flat` raw vs
# `matches_flat_clean` view).
#
# **The scaffold does NOT resolve this divergence.** Resolution is DEFERRED
# to the future tranche-2 source/anchor/cold-start adjudication PR (the
# tranche-2 analogue of PR #234). The validator binds to the registry CSV
# as authoritative for this scaffold layer and accepts `matches_flat` as
# the recorded source.

# %% [markdown]
# ## Three concepts distinguished (CROSS-02-00 §5.4 + CROSS-02-02 §6.2)
#
# This scaffold explicitly distinguishes three orthogonal concepts that are
# easy to conflate, and which the validator enforces are kept distinct:
#
# 1. **`history_enriched_pre_game`** (this tranche). Features derived over
#    PRIOR matches (`history_time < target_time` strict-`<`) and consumed
#    pre-game at target match T. The 6 families in this tranche.
# 2. **`in_game_snapshot`** (DEFERRED to Step 02_01_04+). Features derived
#    from target-match tracker/game events with `event.loop <= cutoff_loop`.
#    The validator's `_check_aliasing_in_tranche` rejects any
#    `in_game_snapshot` row that re-uses a tranche-2 family_id.
# 3. **`IN_GAME_HISTORICAL` columns aggregated from PRIOR matches** (used
#    only by the `in_game_history_aggregate` family in this tranche). Per
#    CROSS-02-00 §5.4 Concern 8 / T15 record, the SC2 IN_GAME_HISTORICAL
#    telemetry-scope retains four columns in scope for history-aggregation
#    use: `APM`, `SQ`, `supplyCappedPercent`, `header_elapsedGameLoops`.
#    These columns remain FORBIDDEN as direct game-T pre-game features
#    (they would be `in_game_snapshot` if read at game T); they are ONLY
#    legal as aggregates over PRIOR matches.

# %% [markdown]
# ## Projection design (SPECIFIED, NOT EXECUTED)
#
# The future materialization SQL pattern is a self-join of `matches_flat_clean`
# (target row) to `player_history_all` (history rows) on `(player_id_worldwide)`
# with the strict `ph.details_timeUTC < target.started_at` filter, producing
# `focal_*` and `opponent_*` symmetric columns. Encoders / smoothing priors
# (cold-start constants K, smoothing pseudocount m, Bayesian prior strength α)
# are SPECIFIED but NOT FIT here (G-CS-6 fold-aware fit is deferred to the
# materialization PR). NO SQL is executed in this scaffold.

# %% [markdown]
# ## Cross-region adjudication DEFERRED
#
# The `cross_region_fragmentation_handling` row carries
# `status = allowed_with_caveat` and
# `candidate_leakage_modes = cross_region_history_drop`. CROSS-02-02 §6.2 row 5
# enumerates three operationalisation options:
# (a) strict-exclusion, (b) dual-feature-path, (c) sensitivity-indicator
# co-registration. The choice is empirically conditional (retention measurement)
# and is DEFERRED to the future tranche-2 source/anchor/cold-start adjudication
# PR. The scaffold validator verifies only that the `cross_region` row
# exists with the `allowed_with_caveat` status; it does NOT pin a policy
# numeric choice.
#
# §10 verdict-audit re-run vs justification: DEFERRED to materialization PR
# per ROADMAP `continue_predicate` (lines 2464+).

# %% [markdown]
# ## Rating reconstruction model choice DEFERRED
#
# The `reconstructed_rating` row's cold-start handling is `G-CS-4` (no global
# rating fit; forward-in-time reconstruction from prior decisive results
# only). The choice between Elo (Elo 1978), Glicko (Glickman 1999), Glicko-2
# (Glickman 2012), and TrueSkill (Herbrich, Minka, Graepel 2006/2007) is
# DEFERRED to the materialization PR. The scaffold records only `G-CS-4`
# as the declared cold-start gate; no algorithm is pinned.

# %%
DESIGNED_COLUMN_NAMES = (
    "focal_prior_match_count",
    "opponent_prior_match_count",
    "matchup_h2h_count",
    "focal_reconstructed_rating",
    "opponent_reconstructed_rating",
    "is_cross_region_fragmented",
    "focal_apm_prior_mean",
    "opponent_apm_prior_mean",
)

DESIGNED_IN_GAME_HISTORICAL_COLUMNS = IN_GAME_HISTORICAL_AGGREGATED_COLUMNS

REGISTRY_CSV = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)

# %%
result = validate_history_enriched_pre_game_materialization(
    REGISTRY_CSV,
    DESIGNED_COLUMN_NAMES,
    DESIGNED_IN_GAME_HISTORICAL_COLUMNS,
)

print("passed:", result.passed)
print("tranche_count:", result.tranche_count)
print("tranche_family_ids:", result.tranche_family_ids)
print("missing_families_in_tranche:", result.missing_families_in_tranche)
print("extra_history_in_tranche:", result.extra_history_in_tranche)
print("pre_game_aliases_in_tranche:", result.pre_game_aliases_in_tranche)
print("in_game_aliases_in_tranche:", result.in_game_aliases_in_tranche)
print("blocked_aliases_in_tranche:", result.blocked_aliases_in_tranche)
print("wrong_prediction_setting_rows:", result.wrong_prediction_setting_rows)
print("wrong_temporal_anchor_rows:", result.wrong_temporal_anchor_rows)
print("cutoff_violations:", result.cutoff_violations)
print("tracker_source_in_history:", result.tracker_source_in_history)
print("asymmetric_construction:", result.asymmetric_construction)
print("post_game_token_hits:", result.post_game_token_hits)
print("cross_region_caveat_ok:", result.cross_region_caveat_ok)
print("in_game_historical_out_of_scope:", result.in_game_historical_out_of_scope)
print("cold_start_gate_violations:", result.cold_start_gate_violations)
print("status_violations:", result.status_violations)
print("materialized_output_paths:", result.materialized_output_paths)
print("halting_falsifier:", result.halting_falsifier)

assert result.passed is True
assert result.tranche_count == 6
assert result.materialized_output_paths == ()
assert result.halting_falsifier is None
assert result.cross_region_caveat_ok is True

# %% [markdown]
# ## Closing — scaffold + ONE validator persisted; NO feature value materialized
#
# **What was done (non-batching step 2 of 9):**
# - Persisted the SCAFFOLD jupytext notebook pair (this `.py` + paired
#   `.ipynb`).
# - Persisted the validator module
#   `validate_history_enriched_pre_game_materialization.py` with 16
#   falsifiers in a priority chain (structural before per-row).
# - Persisted the mirrored test file with ≥30 tests across 18+ classes and
#   ≥95% line coverage on the validator module.
#
# **What was NOT done (deferred to future PRs):**
# - NO feature value materialised; NO Parquet written.
# - NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` /
#   `PHASE_STATUS.yaml` flip; NO `research_log.md` entry.
# - NO §10 verdict-audit re-run (DEFERRED to materialization PR per
#   ROADMAP `continue_predicate`).
# - NO CROSS-02-01-v1.0.1 post-materialization leakage audit (DEFERRED).
# - NO cross-region fragmentation policy choice (DEFERRED to tranche-2
#   source/anchor/cold-start adjudication PR).
# - NO rating reconstruction algorithm choice (DEFERRED to materialization PR).
# - NO Step 02_01_04 work; NO Phase 03 work.
#
# **Lineage position:** artifact #2 of N for Step 02_01_03 readiness
# (PR #239 ROADMAP stub → this scaffold → future tranche-2 adjudication →
# materialization plan → materialization execution → post-mat audit →
# closure).
