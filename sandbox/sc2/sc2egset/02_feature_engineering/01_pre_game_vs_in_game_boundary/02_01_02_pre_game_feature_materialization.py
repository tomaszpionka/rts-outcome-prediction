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
# **MATERIALIZATION + POST-MAT AUDIT (non-batching sequence steps 6-8 of 9).**
# This notebook now materialises the 5 tranche-1 pre_game families into ONE
# Parquet artifact (44,418 rows × 11 projected columns) and runs the
# post-materialization CROSS-02-01-v1.0.1 leakage audit. The 11 projected
# columns partition into 3 IDENTITY (focal_match_id, focal_player,
# opponent_player), 1 CONTEXT row-identity anchor (started_at), and 7 audited
# PRE_GAME features (focal_race, opponent_race, race_pair, map_type,
# patch_version, focal_is_mmr_missing, opponent_is_mmr_missing). Only the 7
# PRE_GAME columns enter `features_audited`.
#
# `started_at` is projected as a row-identity anchor only (CROSS-02-00
# Section 5.1 = CONTEXT; PR #234 Q2(a) use_as_window_bound = false) and is
# excluded from `features_audited`.
#
# **This PR does NOT:** flip STEP_STATUS / PIPELINE_SECTION_STATUS /
# PHASE_STATUS · edit ROADMAP · patch any spec or cleaning-layer YAML · start
# Step 02_01_03 · start Phase 03 · close Step 02_01_02. Closure is deferred
# to a separate U2.B closure PR.
#
# **Lineage:** the original PR #233 SCAFFOLD + ONE VALIDATION MODULE cells
# are preserved below (for back-compat regression); the materialization +
# audit cells run AFTER the scaffold validator passes.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_02 ·
# **Dataset:** sc2egset · **Predecessors:** 02_01_01 (closed),
# PR #229/#230/#233/#234.

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
# ## Materialization + post-mat audit (non-batching steps 6-8 of 9)
#
# The cells below execute the Layer-2 deliverable authorised by merged
# PR #235. Cells: imports (with `SET TimeZone = 'UTC'` on the DuckDB
# session per CROSS-02-00 Section 3.3) → PR #234 frozen-inputs context →
# materialization call → audit call → closing.

# %%
import datetime as _dt

from rts_predict.games.sc2.datasets.sc2egset.materialize_pre_game_features import (
    EXPECTED_AUDITED_FEATURE_COLUMNS,
    EXPECTED_OUTPUT_COLUMNS,
    EXPECTED_OUTPUT_ROW_COUNT,
    PROJECTED_CONTEXT_COLUMNS,
    PROJECTED_IDENTITY_COLUMNS,
    materialize_pre_game_features,
    run_post_materialization_audit,
)

# %% [markdown]
# ### PR #234 frozen-inputs context
#
# All three coupled decisions from PR #234 are BINDING for this materialization:
#
# - **Q1 source layer = `matches_flat_clean`** (cleaned-raw, 1v1-scoped
#   native; 22,209 replays × 2 player-rows = 44,418).
# - **Q2(a) Phase-02 row-identity anchor = `started_at TIMESTAMP`** from MHM,
#   `use_as_window_bound = false`, `use_as_row_identity = true`. The anchor is
#   CONTEXT per CROSS-02-00 Section 5.1, not PRE_GAME; it is NOT a model feature.
# - **Q3 = RATIFY** cleaning-layer convention: read `race` (3-value:
#   {Prot, Terr, Zerg}); `selectedRace` excluded.
#
# The 11 output columns partition as:
# - 3 identity: `focal_match_id`, `focal_player`, `opponent_player`.
# - 1 context anchor: `started_at` (CONTEXT; not a feature).
# - 7 audited PRE_GAME features (the contents of `features_audited`):
#   `focal_race`, `opponent_race`, `race_pair`, `map_type`, `patch_version`,
#   `focal_is_mmr_missing`, `opponent_is_mmr_missing`.
#
# PR #234 CSV (`02_01_02_source_anchor_race_adjudication.csv`) carries SHA-256
# bonds for every provenance input; the materialization module re-hashes
# these and writes them into the audit JSON for evidence bonding.

# %%
DUCKDB_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
)
OUTPUT_PARQUET_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_pre_game_features.parquet"
)
AUDIT_JSON_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_02/leakage_audit_sc2egset.json"
)
AUDIT_MD_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_01_02/leakage_audit_sc2egset.md"
)
AUDIT_DATE = _dt.date.today().isoformat()
AUDIT_PR_LABEL = "PR #236"

# %%
mat_result = materialize_pre_game_features(
    duckdb_path=DUCKDB_PATH,
    output_parquet_path=OUTPUT_PARQUET_PATH,
    registry_csv_path=REGISTRY_CSV,
)

print("passed:", mat_result.passed)
print("row_count:", mat_result.row_count)
print("len(column_names):", len(mat_result.column_names))
print("parquet_path:", mat_result.parquet_path)
print("distinct_focal_match_id:", mat_result.distinct_focal_match_id_count)
print("race_vocabulary:", sorted(mat_result.race_vocabulary))
print(
    "is_mmr_missing (False, True):",
    (
        mat_result.is_mmr_missing_false_count,
        mat_result.is_mmr_missing_true_count,
    ),
)
print("distinct_map_count:", mat_result.distinct_map_count)
print("distinct_patch_count:", mat_result.distinct_patch_count)
print("halting_falsifier:", mat_result.halting_falsifier)

assert mat_result.row_count == EXPECTED_OUTPUT_ROW_COUNT
assert mat_result.column_names == EXPECTED_OUTPUT_COLUMNS
assert mat_result.halting_falsifier is None
assert mat_result.materialized_output_paths != ()

# %%
audit_result = run_post_materialization_audit(
    parquet_path=OUTPUT_PARQUET_PATH,
    audit_json_path=AUDIT_JSON_PATH,
    audit_md_path=AUDIT_MD_PATH,
    duckdb_path=DUCKDB_PATH,
    audit_date=AUDIT_DATE,
    audit_pr=AUDIT_PR_LABEL,
)

print("verdict:", audit_result.verdict)
print("features_audited:", audit_result.features_audited)
print("projected_context_columns:", audit_result.projected_context_columns)
print("projected_identity_columns:", audit_result.projected_identity_columns)
print("halting_falsifier:", audit_result.halting_falsifier)

assert audit_result.verdict == "PASS"
assert len(audit_result.features_audited) == 7
assert audit_result.features_audited == EXPECTED_AUDITED_FEATURE_COLUMNS
assert audit_result.projected_context_columns == PROJECTED_CONTEXT_COLUMNS
assert audit_result.projected_identity_columns == PROJECTED_IDENTITY_COLUMNS
assert audit_result.halting_falsifier is None
assert set(audit_result.features_audited).isdisjoint(
    set(audit_result.projected_context_columns)
    | set(audit_result.projected_identity_columns)
)

# %% [markdown]
# ## Closing — feature Parquet + non-vacuous audit persisted; no closure claimed
#
# **What was done (non-batching steps 6-8 of 9):**
# - Materialised 02_01_02 feature Parquet at
#   `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_features.parquet`
#   (44,418 rows × 11 projected columns: 3 identity + 1 context anchor +
#   7 audited PRE_GAME features).
# - Persisted the FIRST non-vacuous CROSS-02-01 audit pair at
#   `reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}`
#   (`features_audited` has exactly the 7 PRE_GAME feature columns;
#   `verdict = PASS`).
#
# **What was NOT done (deferred to the U2.B closure PR):**
# - STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS are byte-unchanged.
# - `02_01_02: complete` is NOT added to STEP_STATUS.
# - The dataset's `research_log.md` records this PR as `closure_status:
#   still_open`, `leakage_audit_state: post_materialization_pass`.
# - ROADMAP body, specs, and cleaning-layer YAMLs are byte-unchanged.
# - PR #230 audit JSON at `02_01_01/leakage_audit_sc2egset.json` is
#   byte-unchanged (distinct path; vacuous record preserved).
# - Phase 03 is not started; Step 02_01_03 is not started.
#
# **Examiner-clarity sentence:** `started_at` is projected as a row-identity
# anchor only (CROSS-02-00 Section 5.1 = CONTEXT; PR #234 Q2(a)
# use_as_window_bound = false) and is excluded from `features_audited`.
#
# **Lineage position:** artifact #5 of 5 in the Step 02_01_02 readiness
# lineage (PR #229 → PR #230 → PR #233 → PR #234 → this PR).
