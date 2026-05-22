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
# # Step 02_01_02 — First pre_game feature-family materialization: sc2egset
#
# **SCAFFOLD + ONE VALIDATION MODULE (non-batching sequence step 2 of 9).**
# This notebook DESIGNS the pre_game projection and RUNS one validation module
# against the closed 02_01_01 registry CSV. It is NOT materialization.
#
# **This PR does NOT:** materialize any feature value · write any artifact
# (Parquet / CSV / JSON / MD) · flip STEP_STATUS / PIPELINE_SECTION_STATUS /
# PHASE_STATUS · write a research_log entry · edit the ROADMAP · start Step
# 02_01_03 · start Phase 03 · close Step 02_01_02.
#
# **Leakage status:** the CROSS-02-01-v1.0.1 post-materialization leakage audit
# is NOT run here and remains FUTURE. The 02_01_01 leakage audit is vacuous
# (features_audited=[]) by design; it becomes non-vacuous only when a future PR
# materializes the feature table. This scaffold designs the projection; it does
# NOT clear leakage.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_02 (scaffold
# increment 1 of N) · **Dataset:** sc2egset · **Predecessors:** 02_01_01 (closed).

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.validate_pre_game_feature_materialization import (
    validate_pre_game_feature_materialization,
)

# %% [markdown]
# ## Context and input artifacts
#
# This notebook binds to three predecessor artifacts (all read-only; none mutated):
#
# - **Closed 02_01_01 registry CSV** (authoritative catalog for the 5 tranche-1 families):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
#
# - **PR #229 §10 design-time verdict-audit CSV** (per-family design-time verdicts,
#   26 rows, design-time only — NOT a leakage clearance):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv`
#
# - **PR #230 CROSS-02-01 vacuous leakage-audit JSON** (features_audited=[];
#   PASS-by-vacuity; NOT a substitute for the future post-materialization audit):
#   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json`
#
# The CROSS-02-01 post-materialization leakage audit
# (`02_01_02/leakage_audit_sc2egset.json`) does NOT exist yet and is NOT created
# by this scaffold notebook. The PR #230 leakage JSON remains unchanged
# (features_audited=[] vacuously).

# %% [markdown]
# ## Tranche-1 pre_game families — design table
#
# The 5 tranche-1 families are the closed registry CSV's pre_game rows.
# All carry status=allowed, candidate_leakage_modes=none, cold_start_handling=G-CS-1,
# allowed_cutoff_rule=snapshot_at_match_start, per_player_construction=symmetric.
#
# | family_id | source_table | source_grain | model_input_grain | temporal_anchor | allowed_cutoff_rule | candidate_leakage_modes | cold_start_handling |
# |-----------|-------------|--------------|-------------------|-----------------|---------------------|------------------------|---------------------|
# | sc2egset.pre_game.focal_race_with_opponent_race_pair | replay_players_raw | (filename, player_id_worldwide) | (focal_match_id, focal_player) | details_timeUTC | snapshot_at_match_start | none | G-CS-1 |
# | sc2egset.pre_game.map_type_encoded | matches_flat | (filename) | (focal_match_id, focal_player) | details_timeUTC | snapshot_at_match_start | none | G-CS-1 |
# | sc2egset.pre_game.patch_version_encoded | matches_flat | (filename) | (focal_match_id, focal_player) | details_timeUTC | snapshot_at_match_start | none | G-CS-1 |
# | sc2egset.pre_game.matchup_encoded | replay_players_raw | (filename, player_id_worldwide) | (focal_match_id, focal_player) | details_timeUTC | snapshot_at_match_start | none | G-CS-1 |
# | sc2egset.pre_game.is_mmr_missing_flag | replay_players_raw | (filename, player_id_worldwide) | (focal_match_id, focal_player) | details_timeUTC | snapshot_at_match_start | none | G-CS-1 |
#
# Seed 42 is reserved for any future train/test split or encoder vocabulary
# construction; it is NOT used in this scaffold-only notebook.

# %% [markdown]
# ## Projection design (specified, NOT executed)
#
# This section records the DESIGN of the future materialization SQL for the
# mandatory Claude/ChatGPT second-pass leakage review. NO feature value is
# computed or materialized here.
#
# ### Source binding (authoritative = closed registry CSV)
#
# Per-family source tables and grains as recorded in the closed registry CSV:
# - `focal_race_with_opponent_race_pair`, `matchup_encoded`, `is_mmr_missing_flag`:
#   source = `replay_players_raw` at grain `(filename, player_id_worldwide)`.
# - `map_type_encoded`, `patch_version_encoded`:
#   source = `matches_flat` at grain `(filename)`.
#
# **View-vs-raw divergence (DEFERRED to mandatory second-pass):** CROSS-02-02 §6.1
# names view-level sources (`matches_history_minimal.faction`,
# `player_history_all.*`) and anchor `started_at`, while the registry CSV binds
# to raw-layer sources (`replay_players_raw`, `matches_flat`) and anchor
# `details_timeUTC`. This is ONE coupled decision (view-vs-raw + anchor) that
# is NOT resolved here. The scaffold binds to the closed registry CSV and records
# the divergence for the second-pass.
#
# ### Cutoff semantics (snapshot_at_match_start)
#
# The 5 families are game-T STATIC pre-match attributes
# (CROSS-02-03 §6.1 line 235; CROSS-02-02 §6.1 "none (game-T attribute)").
# NO `history_time < target_time` window filter applies for this tranche —
# that strict-`<` filter is for the deferred history tranche (02_01_03+).
# Leak-freedom for this tranche rests on:
#   1. Game-T pre-game columns only (no post-game outcome values).
#   2. POST-GAME token absence (CROSS-02-01-v1.0.1 §2.2).
#   3. Non-tracker source (Invariant I3).
# The CROSS-02-01 §2.2 substantive check (non-vacuous, post-materialization)
# must report 0 over the materialized set in a future PR.
#
# ### Symmetric focal/opponent construction (Invariant I5)
#
# The future SQL self-joins `replay_players_raw` on `(filename, player_id_worldwide)`
# to produce both focal and opponent slots using the SAME expression. No
# privileged slot exists. The RISK-24 data-dependent slot-assignment falsifier
# (defined in `thesis/pass2_evidence/methodology_risk_register.md`, NOT the
# dataset-level `risk_register_sc2egset.csv`) is enumerated as a future gate.
#
# ### Per-family derivation notes
#
# - **race_pair / matchup**: derived from the `race` field in `replay_players_raw`
#   (Prot/Terr/Zerg/Rand). Random is a 4th valid pre-game race. The
#   eventually-played race is a post-game decision and is NOT projected (RISK-26).
# - **map_type / patch_version**: from `matches_flat` at `(filename)`, broadcast
#   to both focal and opponent slots.
# - **is_mmr_missing**: BOOLEAN missingness/provenance flag over the MMR field.
#   The MMR SCALAR is NOT projected (CROSS-02-02 §6.1 line 228: MMR absent for
#   83.95% of rows). This flag is framed as missingness/provenance, NOT skill.
#   `APPROVED_MMR_MISSINGNESS_TOKENS` allowlist + boundary-aware token equality
#   in the validator enforce this constraint (ChatGPT second-pass correction).
#
# ### Encoders SPECIFIED, not FIT
#
# Categorical encoding of race_pair / matchup / map_type / patch_version is
# specified (encoder type, dataset_tag='sc2egset' partition, vocabulary source)
# but NOT fit here. Any future fit is train-fold-only (Invariant I3 normalization
# leakage). Vocabulary sources are the closed registry CSV's `source_grain`
# and `model_input_grain` columns.

# %%
DESIGNED_COLUMN_NAMES = (
    "focal_race",
    "opponent_race",
    "race_pair",
    "focal_matchup",
    "opponent_matchup",
    "map_type",
    "patch_version",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing",
)

REGISTRY_CSV = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)

# %%
result = validate_pre_game_feature_materialization(REGISTRY_CSV, DESIGNED_COLUMN_NAMES)

print("passed:", result.passed)
print("tranche_count:", result.tranche_count)
print("tranche_family_ids:", result.tranche_family_ids)
print("extra_families_in_tranche:", result.extra_families_in_tranche)
print("is_mmr_missing_classified_as_flag:", result.is_mmr_missing_classified_as_flag)
print("tracker_in_pre_game:", result.tracker_in_pre_game)
print("history_families_in_tranche:", result.history_families_in_tranche)
print("in_game_families_in_tranche:", result.in_game_families_in_tranche)
print("asymmetric_construction:", result.asymmetric_construction)
print("post_game_token_hits:", result.post_game_token_hits)
print("unexpected_source_tables:", result.unexpected_source_tables)
print("materialized_output_paths:", result.materialized_output_paths)
print("halting_falsifier:", result.halting_falsifier)

assert result.passed is True
assert result.materialized_output_paths == ()
assert result.halting_falsifier is None

# %% [markdown]
# ## Closing — nothing persisted; no status flipped
#
# This cell summarises what this scaffold notebook did and did NOT do.
#
# **What was done (scaffold-only, non-batching step 2 of 9):**
# - Declared the design contract for the 5 tranche-1 pre_game families.
# - Ran one validation module (`validate_pre_game_feature_materialization`)
#   against the closed 02_01_01 registry CSV.
# - Confirmed: `passed=True`, `tranche_count=5`,
#   `materialized_output_paths=()`, `halting_falsifier=None`.
#
# **Nothing persisted:**
# - No Parquet / CSV / JSON / MD artifact was written.
# - No feature value was computed or materialized.
# - No DuckDB CREATE / INSERT / COPY / to_parquet / feature SELECT was executed.
#
# **No status flipped:**
# - STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS are byte-unchanged.
# - The `research_log.md` was NOT updated.
# - The ROADMAP was NOT edited.
#
# **Leakage audit unchanged:**
# - The CROSS-02-01 post-materialization leakage audit
#   (`02_01_02/leakage_audit_sc2egset.json`) does NOT exist and is NOT created.
# - The PR #230 `leakage_audit_sc2egset.json` remains unchanged
#   (`features_audited==[]`).
# - The CROSS-02-01 audit remains FUTURE — to be run in the first
#   materialization PR only.
#
# **Required before any future materialization PR:**
# - A mandatory Claude/ChatGPT second-pass leakage review over the
#   focal/opponent projection SQL, the `snapshot_at_match_start` cutoff
#   semantics, and the view-vs-raw source reconciliation.
# - This review is a DISTINCT gate from the scaffold PR's reviewer-adversarial
#   gate; it is NOT discharged by this notebook.
