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
# # Step 02_02_01 — Symmetry & difference feature materialization + non-vacuous CROSS-02-01 audit: sc2egset
#
# **MATERIALIZATION + POST-MAT AUDIT (non-batching sequence steps 7-8 of 9).**
# This notebook OVERWRITES the PR #266 scaffold (preserved at git SHA
# `88c2b98f`) per `sandbox/README.md` single-notebook-per-Step contract.
# It materialises the 33 symmetry/difference feature candidates authorised
# by PR #268 binding adjudication into ONE Parquet artifact (44,418 rows × 37
# projected columns = 3 identity + 1 context anchor + 33 audited features),
# and runs the FIRST non-vacuous CROSS-02-01-v1.0.1 §3 leakage audit for
# Step `02_02_01`.
#
# **33 materialised feature columns (PR #268 binding adjudication):**
# F1 = 10 signed differences `focal_minus_opponent_<stem>_diff`;
# F2 = 10 symmetric pair means `<stem>_pair_mean`;
# F3 = 10 symmetric pair absolute differences `<stem>_pair_abs_diff`;
# F5 = 3 cross-region Boolean pair transforms
# `cross_region_pair_{or,and,xor}`.
#
# **Dropped families:** F4 (`matchup_h2h_*_pair_*`) per B1 ban / PR #268
# `MATCHUP_HISTORY_TRANSFORM_DECISION`. F6 (`race_pair_*`) DEFERRED to
# Step `02_05` per PR #268 `RACE_PAIR_DECISION`. `sum` EXCLUDED redundant;
# `product` DEFERRED; `ratio` EXCLUDED; `reconstructed_rating` EXCLUDED per
# PR #255 omit-closure.
#
# **This PR does NOT:** flip STEP_STATUS / PIPELINE_SECTION_STATUS /
# PHASE_STATUS · edit ROADMAP · append root research_log.md · start Phase
# 03 · close Step 02_02_01. Closure is deferred to a separate U2.B-style
# PR per PR #237 / PR #262 precedent.
#
# **Phase:** 02 · **Pipeline Section:** 02_02 · **Step:** 02_02_01 ·
# **Dataset:** sc2egset · **Predecessors:** PR #268 (binding adjudication)
# → PR #269 (Layer-1 planning) → THIS Layer-2 execution PR.

# %% [markdown]
# ## Hypothesis + falsifier + sanity-check declaration (data-analysis-lineage.md)
#
# - **Assumption being tested:** the 33 symmetry/difference feature columns
#   derived by row-preserving algebraic transforms over the 02_01_03 Parquet
#   carry no temporal leakage — because every source column in
#   `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS` is itself leakage-free per the
#   02_01_03 CROSS-02-01 audit, and the F1/F2/F3 transforms are pure
#   row-wise arithmetic; the F5 Boolean transforms over
#   `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES` are likewise non-leaking.
# - **Measurement claim:** the materialised Parquet has exactly 44,418 rows
#   × 37 projected columns (3 identity + 1 context + 33 audited features);
#   the CROSS-02-01 audit returns `verdict = "PASS"`; the `features_audited`
#   list equals the canonical 33-tuple in F1→F2→F3→F5 family order; the
#   `validator_passed` field is `True`; SHA-256 of the output Parquet is
#   stable across two consecutive runs (deterministic re-write check).
# - **Falsifiers (24-step halting chain from materialization module):**
#   `validator_module_sha_pin_mismatch`, `adjudicator_module_sha_pin_mismatch`,
#   `adjudication_csv_sha_pin_mismatch`, `adjudication_md_sha_pin_mismatch`,
#   `parent_parquet_02_01_02_sha_mismatch`, `parent_parquet_02_01_03_sha_mismatch`,
#   `parent_audit_02_01_02_canonical_sha_mismatch`,
#   `parent_audit_02_01_03_canonical_sha_mismatch`,
#   `binding_difference_family_numeric_pair_count_drift`,
#   `binding_symmetric_pair_aggregate_transforms_drift`,
#   `binding_cross_region_pair_transforms_drift`,
#   `source_column_missing_in_02_01_03_parquet`,
#   `expected_output_row_count_module_constant_drift`,
#   `audit_pinned_row_count_drift`, `output_row_count_drift`,
#   `output_distinct_focal_match_count_drift`,
#   `output_feature_column_count_drift`, `output_total_column_count_drift`,
#   `identity_columns_not_byte_identical_to_02_01_03`,
#   `forbidden_token_in_emitted_column_name`,
#   `no_parent_mutation_check_failed`, `audit_verdict_not_pass`,
#   `non_deterministic_re_write`, `per_feature_traceability_proof_failed`.
# - **Sanity check:** `result.row_count == 44_418`;
#   `result.distinct_focal_match_count == 22_209`;
#   `result.validator_passed is True`;
#   `result.leakage_audit_verdict == "PASS"`;
#   `len(result.feature_column_names) == 33`; first/last identity rows of
#   output Parquet byte-identical to 02_01_03 Parquet.
# - **Expected artifact:**
#   `02_02_01_symmetry_difference_features.parquet` + audit pair under
#   `reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}`.
# - **Lineage source:** PR #268 binding adjudication CSV+MD authorise this
#   materialisation; PR #269 Layer-1 plan binds the 11-file diff manifest,
#   the 24-falsifier chain, and the SHA pins on the upstream artifacts.
# - **Downstream decision:** the future U2.B-style closure PR consumes
#   these artifacts to flip `STEP_STATUS.yaml` to `02_02_01: complete`.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.materialize_symmetry_difference_features import (
    AUDIT_PR,
    CONTEXT_COLUMNS,
    EXECUTED_AT_UTC_DATE,
    EXPECTED_DISTINCT_FOCAL_MATCH_COUNT,
    EXPECTED_OUTPUT_ROW_COUNT,
    IDENTITY_COLUMNS,
    SPEC_VERSION,
    STEP,
    SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH,
    SYMMETRY_DIFFERENCE_AUDIT_MD_PATH,
    SYMMETRY_DIFFERENCE_OUTPUT_PATH,
    _EXPECTED_FEATURE_COLUMN_COUNT,
    _EXPECTED_TOTAL_COLUMN_COUNT,
    _HALTING_FALSIFIERS,
    _PARQUET_COMPRESSION,
    _PARQUET_VERSION,
    materialize_symmetry_difference_features,
)

# %% [markdown]
# ## Context — PR #269 plan frozen-input snapshot
#
# - **Step:** `02_02_01`
# - **Spec version:** `CROSS-02-01-v1`
# - **Executed at UTC date:** `2026-05-30`
# - **Input Parquet (02_01_02; PR #236):**
#   `02_01_02_pre_game_features.parquet`
#   (SHA256 `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39`).
# - **Input Parquet (02_01_03; PR #259):**
#   `02_01_03_history_enriched_pre_game_features.parquet`
#   (SHA256 `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071`).
# - **PR #266 validator module SHA256:**
#   `d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753`.
# - **PR #268 adjudicator module SHA256 (computed at run time).**
# - **PR #268 adjudication CSV SHA256 (computed at run time).**

# %% [markdown]
# ## Verify module-level constants (self-assertion echo)

# %%
print("STEP:", STEP)
print("SPEC_VERSION:", SPEC_VERSION)
print("EXECUTED_AT_UTC_DATE:", EXECUTED_AT_UTC_DATE)
print("AUDIT_PR:", AUDIT_PR)
print("IDENTITY_COLUMNS:", IDENTITY_COLUMNS)
print("CONTEXT_COLUMNS:", CONTEXT_COLUMNS)
print("EXPECTED_OUTPUT_ROW_COUNT:", EXPECTED_OUTPUT_ROW_COUNT)
print("EXPECTED_DISTINCT_FOCAL_MATCH_COUNT:", EXPECTED_DISTINCT_FOCAL_MATCH_COUNT)
print("_EXPECTED_FEATURE_COLUMN_COUNT:", _EXPECTED_FEATURE_COLUMN_COUNT)
print("_EXPECTED_TOTAL_COLUMN_COUNT:", _EXPECTED_TOTAL_COLUMN_COUNT)
print("_PARQUET_COMPRESSION:", _PARQUET_COMPRESSION)
print("_PARQUET_VERSION:", _PARQUET_VERSION)
print("len(_HALTING_FALSIFIERS):", len(_HALTING_FALSIFIERS))
print("SYMMETRY_DIFFERENCE_OUTPUT_PATH:", SYMMETRY_DIFFERENCE_OUTPUT_PATH)
print("SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH:", SYMMETRY_DIFFERENCE_AUDIT_JSON_PATH)
print("SYMMETRY_DIFFERENCE_AUDIT_MD_PATH:", SYMMETRY_DIFFERENCE_AUDIT_MD_PATH)

# %% [markdown]
# ## Materialise 33-feature symmetry/difference Parquet + CROSS-02-01 audit

# %%
result = materialize_symmetry_difference_features()

# %%
print("result.step:", result.step)
print("result.row_count:", result.row_count)
print("result.distinct_focal_match_count:", result.distinct_focal_match_count)
print("result.validator_passed:", result.validator_passed)
print("result.leakage_audit_verdict:", result.leakage_audit_verdict)
print("len(result.feature_column_names):", len(result.feature_column_names))
print("result.output_parquet_path:", result.output_parquet_path)
print("result.output_audit_json_path:", result.output_audit_json_path)
print("result.output_audit_md_path:", result.output_audit_md_path)

# %%
assert result.step == "02_02_01"
assert result.row_count == EXPECTED_OUTPUT_ROW_COUNT
assert result.distinct_focal_match_count == EXPECTED_DISTINCT_FOCAL_MATCH_COUNT
assert result.validator_passed is True
assert result.leakage_audit_verdict == "PASS"
assert len(result.feature_column_names) == _EXPECTED_FEATURE_COLUMN_COUNT

# %% [markdown]
# ## Feature column names — 33-column F1→F2→F3→F5 family order

# %%
print("33 emitted feature column names (F1→F2→F3→F5 family order):")
for i, name in enumerate(result.feature_column_names, start=1):
    family = (
        "F1" if "_minus_opponent_" in name and name.endswith("_diff") else
        "F2" if name.endswith("_pair_mean") else
        "F3" if name.endswith("_pair_abs_diff") else
        "F5"
    )
    print(f"  {i:2d}. [{family}] {name}")

# %% [markdown]
# ## Visual sanity — first 5 rows of output Parquet

# %%
import pyarrow.parquet as pq  # noqa: E402

parquet_path = Path(SYMMETRY_DIFFERENCE_OUTPUT_PATH)
table = pq.read_table(parquet_path)
df = table.to_pandas()
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print("\nFirst 5 rows (identity + context + first 3 feature columns):")
preview_cols = list(IDENTITY_COLUMNS) + list(CONTEXT_COLUMNS) + list(result.feature_column_names[:3])
print(df[preview_cols].head(5).to_string(index=False))

# %% [markdown]
# ## Parent artifact SHA-256 provenance bonds

# %%
print("Parent artifact SHA-256 bonds (start-of-run):")
for artifact_key, sha in result.parent_artifact_sha256s.items():
    print(f"  {artifact_key}: {sha}")

# %% [markdown]
# ## Closing — 33-feature Parquet + non-vacuous CROSS-02-01 audit persisted
#
# **What was done (non-batching steps 7-8 of 9):**
# - Materialised symmetry/difference Parquet at the canonical path
#   (`SYMMETRY_DIFFERENCE_OUTPUT_PATH` constant; 44,418 rows × 37 cols =
#   3 identity + 1 context anchor + 33 audited features over the four
#   permitted families F1/F2/F3/F5).
# - Persisted the FIRST non-vacuous CROSS-02-01-v1.0.1 §3 audit pair at
#   `reports/artifacts/02_02_01/leakage_audit_sc2egset.{json,md}`
#   (`features_audited` = exactly the 33 symmetry/difference feature column
#   names; `verdict = PASS`; 24-step halting falsifier chain; per-feature
#   traceability table; parent SHA-256 provenance bonds for all 6 parent
#   artifacts; deterministic re-write check passed).
# - Appended a non-closure entry to the dataset `research_log.md` mirroring
#   PR #259's precedent (`closure_status: still_open`,
#   `materialization_state: materialized`,
#   `leakage_audit_state: post_materialization_pass`,
#   `features_audited_count: 33`, `row_count: 44418`, etc).
#
# **What was NOT done (deferred to the U2.B-style closure PR):**
# - `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`
#   are byte-unchanged.
# - `02_02_01: complete` is NOT added to `STEP_STATUS.yaml`.
# - ROADMAP body, specs, and cleaning-layer YAMLs are byte-unchanged.
# - Root `reports/research_log.md` is NOT appended (per per-dataset-only
#   research_log scoping; PR #259 precedent).
# - No Phase 03 work. No baseline modeling. No Step 02_02_02+.
