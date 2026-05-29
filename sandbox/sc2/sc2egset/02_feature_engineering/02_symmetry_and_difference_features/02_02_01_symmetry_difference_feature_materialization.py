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
# # Step 02_02_01 — Symmetry & difference feature scaffold + one validation module: sc2egset
#
# **SCAFFOLD + ONE VALIDATION MODULE (non-batching sequence steps 2-4 of 9).**
# Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for
# empirical work", this notebook executes sequence step 2 ("Notebook
# scaffold + one validation module") and prepares for step 3 ("Execute and
# report") and step 4 ("User review"). It performs NO feature
# materialisation, NO artifact emission, NO status / ROADMAP /
# `research_log` mutation.
#
# The notebook filename uses the `_materialization` suffix because the
# per-Step notebook is OVERWRITTEN at materialisation per
# `sandbox/README.md` single-notebook-per-Step contract (mirrors PR #241
# → PR #259 lineage for Step 02_01_03; the PR #241 scaffold notebook was
# already named `..._materialization.{py,ipynb}` and was overwritten in
# place at PR #259, not renamed).
#
# **Phase:** 02 · **Pipeline Section:** 02_02 · **Step:** 02_02_01 ·
# **Dataset:** sc2egset · **Branch:**
# `feat/sc2egset-02-02-01-symmetry-difference-scaffold` ·
# **Predecessors:** PR #259 (five-family materialisation) → PR #262
# (Step 02_01_03 closure) → PR #263 (Layer-1 ROADMAP plan) → PR #264
# (Layer-2 ROADMAP-only stub) → PR #265 (Layer-1 scaffold plan) → THIS
# Layer-2 execution PR.

# %% [markdown]
# ## Hypothesis + falsifier + sanity-check declaration (data-analysis-lineage.md)
#
# - **Assumption being tested:** every candidate symmetry/difference
#   feature family enumerated below traces to a focal/opponent paired
#   column in the byte-stable `02_01_02` 7-tuple or `02_01_03` 24-tuple,
#   every candidate carries an explicit `direction` annotation
#   (`focal_minus_opponent` or `symmetric`), and slot-orthogonality
#   (Invariant I5) holds at the design-contract layer.
# - **Measurement claim:** the validator returns `passed = True` with
#   `halting_falsifier = None`; `materialized_output_paths == ()`;
#   `artifact_directory_absence_ok == True`; the two input artifact
#   SHA256 values match the embedded constants (PR #259 Parquet
#   `053900e7…`; PR #236 Parquet `24db73fb…`); the two parent audit JSONs
#   align with the embedded `IDENTITY_COLUMNS` / `CONTEXT_ANCHOR_COLUMNS`
#   / `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_0{2,3}` tuples; every
#   candidate's `direction` is in `VALID_DIRECTION_LITERAL_VALUES`; every
#   candidate's `source_columns` trace to the audited union.
# - **Falsifiers (14-step halting priority chain from T01):**
#   `input_parquet_missing`, `input_parquet_sha_mismatch`,
#   `parent_audit_json_missing`, `audit_json_misaligned`,
#   `artifact_directory_present`, `direction_annotation_invalid`,
#   `source_column_traceability_violation`,
#   `reconstructed_rating_in_candidates`,
#   `slot_dependent_token_present`, `target_leak_token_in_candidate`,
#   `aoe2_vocabulary_in_candidate`, `tracker_sourced_candidate`,
#   `direction_name_inconsistent`, `materialization_output_path_present`.
# - **Sanity check:** module-load echo of every constant; `result.passed
#   is True`; `len(DESIGNED_DIFFERENCE_SPECS) >= 1`; no path under
#   `reports/artifacts/02_02_01/` or
#   `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
#   exists at notebook entry AND at notebook exit (artifact-free promise).
# - **Expected artifact:** NONE for this scaffold notebook. The expected
#   user-facing output is a printed validation report from the T01
#   validator. NO Parquet, NO CSV, NO MD, NO JSON.
# - **Lineage source:** PR #264 ROADMAP stub authorises this scaffold;
#   PR #265 Layer-1 plan binds the 7-file diff manifest, the
#   14-falsifier chain, the 8 reviewer-adversarial nits N1-N8, and the
#   SHA pins on the upstream Parquets.
# - **Downstream decision:** the future source-anchor / column-naming
#   adjudication PR (analogous to PR #234 for `02_01_02`) consumes this
#   scaffold's candidate-family enumeration and binds the final
#   transform set. The subsequent materialisation PR (analogous to
#   PR #259) emits the Parquet + CROSS-02-01 audit pair.

# %% [markdown]
# ## Context — PR #265 plan binding-input snapshot
#
# - Input Parquet (02_01_02; PR #236):
#   `02_01_02_pre_game_features.parquet` (719,068 B; SHA256
#   `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39`).
# - Input Parquet (02_01_03; PR #259):
#   `02_01_03_history_enriched_pre_game_features.parquet`
#   (2,451,869 B; SHA256
#   `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071`).
# - Parent audit JSON (02_01_02; PR #236):
#   `reports/artifacts/02_01_02/leakage_audit_sc2egset.json`
#   — 7-tuple `features_audited`; identity = `(focal_match_id,
#   focal_player, opponent_player)`; context = `(started_at,)`.
# - Parent audit JSON (02_01_03; PR #259):
#   `reports/artifacts/02_01_03/leakage_audit_sc2egset.json`
#   — 24-tuple `features_audited`; same identity + context projection.
#
# Full canonical paths live in the validator module's
# `INPUT_02_01_0{2,3}_PARQUET_RELPATH` and
# `INPUT_02_01_0{2,3}_AUDIT_JSON_RELPATH` constants.

# %% [markdown]
# ## Candidate symmetry & difference feature families (manual §3)
#
# Per `02_FEATURE_ENGINEERING_MANUAL.md` §3 (Bradley-Terry; difference
# features as default for pairwise prediction): for latent strengths
# β_i, `P(i > j) = 1 / (1 + e^(β_j − β_i))`, so the logit of win
# probability equals the **difference** of latent strengths.
#
# Six candidate families (CANDIDATE-only at scaffold stage; binding
# decision deferred to future source-anchor adjudication PR analogous to
# PR #234):
#
# - **Family 1 — Numeric difference** (`direction="focal_minus_opponent"`).
#   Default per manual §3 line 51. `focal_<base> - opponent_<base>` for
#   each numeric pair in the 02_01_03 24-tuple.
# - **Family 2 — Absolute difference** (`direction="symmetric"`).
#   `abs(focal_<base> - opponent_<base>)`. Sign-cancellation hedge for
#   tree models without monotone constraints.
# - **Family 3 — Symmetric pair mean/sum/product**
#   (`direction="symmetric"`). Hue & Vert 2010 symmetric-kernel tabular
#   approximation; invariant under focal/opponent swap.
# - **Family 4 — Matchup-history pair operations**
#   (`direction="focal_minus_opponent"`). Built from
#   `*_prior_win_rate_matchup_conditional` and related conditional rates.
# - **Family 5 — Cross-region BOOLEAN-pair** (`direction="symmetric"`).
#   Built from the two `is_cross_region_fragmented_*_history_any` flags;
#   XOR/OR/AND ops only — NEVER numeric subtraction.
# - **Family 6 — Race-pair encoded interaction**
#   (`direction="symmetric"`). CANDIDATE-only; `race_pair` is a 9-class
#   categorical from 02_01_02. Binding 02_02-vs-02_05 boundary decision
#   taken in future source-anchor adjudication PR. Marker name
#   `race_pair__defer_to_02_05`.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.validate_symmetry_difference_feature_materialization import (  # noqa: E501
    BLOCKED_FAMILY_FRAGMENTS,
    BLOCKED_SLOT_TOKEN_REGEX,
    CONTEXT_ANCHOR_COLUMNS,
    EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES,
    FORBIDDEN_AOE2_VOCABULARY,
    IDENTITY_COLUMNS,
    INPUT_02_01_02_AUDIT_JSON_RELPATH,
    INPUT_02_01_02_PARQUET_RELPATH,
    INPUT_02_01_02_PARQUET_SHA256,
    INPUT_02_01_03_AUDIT_JSON_RELPATH,
    INPUT_02_01_03_PARQUET_RELPATH,
    INPUT_02_01_03_PARQUET_SHA256,
    POST_GAME_TOKENS,
    TRACKER_SOURCE_PREFIX,
    UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02,
    UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03,
    VALID_DIRECTION_LITERAL_VALUES,
    CandidateFeatureSpec,
    validate_symmetry_difference_feature_materialization,
)

# %% [markdown]
# ## Repo-root + input path resolution

# %%
_CWD = Path.cwd().resolve()
REPO_ROOT = next(
    (parent for parent in (_CWD, *_CWD.parents) if (parent / "pyproject.toml").exists()),
    _CWD,
)
INPUT_02_01_02_PARQUET = REPO_ROOT / INPUT_02_01_02_PARQUET_RELPATH
INPUT_02_01_03_PARQUET = REPO_ROOT / INPUT_02_01_03_PARQUET_RELPATH
INPUT_02_01_02_AUDIT_JSON = REPO_ROOT / INPUT_02_01_02_AUDIT_JSON_RELPATH
INPUT_02_01_03_AUDIT_JSON = REPO_ROOT / INPUT_02_01_03_AUDIT_JSON_RELPATH

# %% [markdown]
# ## Verify constants (module-load self-assertion echo)

# %%
print("IDENTITY_COLUMNS:", IDENTITY_COLUMNS)
print("CONTEXT_ANCHOR_COLUMNS:", CONTEXT_ANCHOR_COLUMNS)
print(
    "UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02 count:",
    len(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02),
)
print(
    "UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03 count:",
    len(UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03),
)
print("VALID_DIRECTION_LITERAL_VALUES:", VALID_DIRECTION_LITERAL_VALUES)
print("INPUT_02_01_02_PARQUET_SHA256:", INPUT_02_01_02_PARQUET_SHA256)
print("INPUT_02_01_03_PARQUET_SHA256:", INPUT_02_01_03_PARQUET_SHA256)
print("BLOCKED_SLOT_TOKEN_REGEX count:", len(BLOCKED_SLOT_TOKEN_REGEX))
print("POST_GAME_TOKENS count:", len(POST_GAME_TOKENS))
print("BLOCKED_FAMILY_FRAGMENTS:", BLOCKED_FAMILY_FRAGMENTS)
print("FORBIDDEN_AOE2_VOCABULARY:", FORBIDDEN_AOE2_VOCABULARY)
print("TRACKER_SOURCE_PREFIX:", TRACKER_SOURCE_PREFIX)
print(
    "EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES:",
    EXPECTED_NO_OUTPUT_ARTIFACT_DIRECTORIES,
)

# %% [markdown]
# ## Designed CANDIDATE specs (Families 1, 3, and 6)
#
# Family 1 (numeric difference, `focal_minus_opponent`): three
# representative candidates from the 02_01_03 24-tuple. Family 3
# (symmetric pair mean, `symmetric`): three representative candidates.
# Family 6 (race-pair, `symmetric`): the explicit
# `race_pair__defer_to_02_05` deferral marker from 02_01_02.

# %%
DESIGNED_DIFFERENCE_SPECS: tuple[CandidateFeatureSpec, ...] = (
    CandidateFeatureSpec(
        column_name="focal_minus_opponent_prior_match_count_diff",
        direction="focal_minus_opponent",
        source_columns=(
            "focal_prior_match_count",
            "opponent_prior_match_count",
        ),
    ),
    CandidateFeatureSpec(
        column_name="focal_minus_opponent_apm_prior_mean_diff",
        direction="focal_minus_opponent",
        source_columns=(
            "focal_apm_prior_mean",
            "opponent_apm_prior_mean",
        ),
    ),
    CandidateFeatureSpec(
        column_name="focal_minus_opponent_days_since_prior_match_diff",
        direction="focal_minus_opponent",
        source_columns=(
            "focal_days_since_prior_match",
            "opponent_days_since_prior_match",
        ),
    ),
)

# %%
DESIGNED_SYMMETRIC_PAIR_SPECS: tuple[CandidateFeatureSpec, ...] = (
    CandidateFeatureSpec(
        column_name="prior_match_count_pair_mean",
        direction="symmetric",
        source_columns=(
            "focal_prior_match_count",
            "opponent_prior_match_count",
        ),
    ),
    CandidateFeatureSpec(
        column_name="apm_prior_mean_pair_mean",
        direction="symmetric",
        source_columns=(
            "focal_apm_prior_mean",
            "opponent_apm_prior_mean",
        ),
    ),
    CandidateFeatureSpec(
        column_name="is_cross_region_fragmented_pair_or",
        direction="symmetric",
        source_columns=(
            "is_cross_region_fragmented_focal_history_any",
            "is_cross_region_fragmented_opponent_history_any",
        ),
    ),
)

# %%
DESIGNED_RACE_PAIR_CANDIDATE_SPECS: tuple[CandidateFeatureSpec, ...] = (
    CandidateFeatureSpec(
        column_name="race_pair__defer_to_02_05",
        direction="symmetric",
        source_columns=("race_pair",),
    ),
)

# %% [markdown]
# ## Invoke the T01 validator

# %%
result = validate_symmetry_difference_feature_materialization(
    INPUT_02_01_02_PARQUET,
    INPUT_02_01_03_PARQUET,
    (INPUT_02_01_02_AUDIT_JSON, INPUT_02_01_03_AUDIT_JSON),
    DESIGNED_DIFFERENCE_SPECS,
    DESIGNED_SYMMETRIC_PAIR_SPECS,
    DESIGNED_RACE_PAIR_CANDIDATE_SPECS,
    repo_root=REPO_ROOT,
)

# %%
print("passed:", result.passed)
print("halting_falsifier:", result.halting_falsifier)
print("materialized_output_paths:", result.materialized_output_paths)
print("artifact_directory_absence_ok:", result.artifact_directory_absence_ok)
print("input_parquet_paths_present_ok:", result.input_parquet_paths_present_ok)
print("input_parquet_sha256_ok:", result.input_parquet_sha256_ok)
print("parent_audit_json_paths_present_ok:", result.parent_audit_json_paths_present_ok)
print("audit_json_alignment_ok:", result.audit_json_alignment_ok)
print("direction_annotation_valid:", result.direction_annotation_valid)
print("source_column_traceability_ok:", result.source_column_traceability_ok)
print("direction_name_consistency_ok:", result.direction_name_consistency_ok)
print("slot_token_violations:", result.slot_token_violations)
print("target_leak_token_violations:", result.target_leak_token_violations)
print("reconstructed_rating_violations:", result.reconstructed_rating_violations)
print("aoe2_vocabulary_violations:", result.aoe2_vocabulary_violations)
print("tracker_sourced_violations:", result.tracker_sourced_violations)

# %%
assert result.passed is True
assert result.halting_falsifier is None
assert result.materialized_output_paths == ()
assert result.artifact_directory_absence_ok is True

# %% [markdown]
# ## Closing — scaffold + one validation module persisted; no artifact emitted
#
# **What this notebook DID:**
#
# - Imported the T01 validator
#   (`validate_symmetry_difference_feature_materialization`) and the
#   `CandidateFeatureSpec` dataclass.
# - Echoed every module-level constant for at-a-glance audit.
# - Enumerated 6 candidate symmetric/difference feature families per
#   `02_FEATURE_ENGINEERING_MANUAL.md` §3, materialised three example
#   specs for Family 1 (numeric difference), three example specs for
#   Family 3 (symmetric pair mean / OR), and the
#   `race_pair__defer_to_02_05` deferral marker for Family 6.
# - Invoked the validator and asserted `passed is True`,
#   `halting_falsifier is None`, `materialized_output_paths == ()`,
#   `artifact_directory_absence_ok is True`.
#
# **What this notebook did NOT do (per PR #265 plan hard-stops):**
#
# - **No feature materialisation.** No Parquet, no CSV, no MD, no JSON
#   under `reports/artifacts/02_02_01/` or
#   `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`.
# - **No leakage audit artifact** (no `leakage_audit_sc2egset.{json,md}`
#   pair).
# - **No status YAML edit.** STEP_STATUS / PIPELINE_SECTION_STATUS /
#   PHASE_STATUS byte-unchanged. `02_02_01` not added to STEP_STATUS;
#   `02_02` not added to PIPELINE_SECTION_STATUS.
# - **No ROADMAP edit.** The 02_02_01 block at ROADMAP lines 2853-3131
#   remains byte-unchanged.
# - **No `research_log.md` append** (dataset or root). Per the
#   non-batching rule, research_log is appended only at step closure
#   (sequence step 8), not at scaffold (sequence step 2).
# - **No source-anchor / column-naming binding adjudication.** Candidate
#   enumeration is CANDIDATE-only; binding decision deferred to a future
#   PR analogous to PR #234 for 02_01_02.
# - **No upstream artifact mutation.** Both 02_01_02 and 02_01_03
#   Parquets byte-stable at the embedded SHA256 pins; both audit JSONs
#   byte-unchanged.
# - **No `reconstructed_rating` re-introduction.** PR #255 / PR #257
#   binding exclusion stands.
# - **No AoE2 `civilization` vocabulary** (Invariant I8 cross-game
#   hygiene).
# - **No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modelling.**
