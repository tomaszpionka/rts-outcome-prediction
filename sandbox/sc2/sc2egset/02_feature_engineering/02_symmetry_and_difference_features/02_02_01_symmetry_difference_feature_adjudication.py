# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # Step 02_02_01 — Symmetry & difference feature scope adjudication: sc2egset (Round 2 / Layer-2)
#
# **Lineage:**
# - PR #264: ROADMAP stub
# - PR #265: Layer-1 scaffold plan
# - PR #266: Layer-2 scaffold execution + validator (`validate_symmetry_difference_feature_materialization.py`)
# - PR #267: Layer-1 adjudication plan (merged `af8c3d98`; Round 2 verdict APPROVE-WITH-NITS)
# - **THIS PR**: Layer-2 adjudication execution
#
# **Round 2 nits applied (N1–N6):**
# - N1: `product` wording corrected to "not LINEARLY expressible from (mean, abs_diff) alone"
# - N2: `02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135 cited; 02_05 placement is convention choice
# - N3: F5 (either, both, xor) LogReg rank-2 design matrix acknowledged in MD §4
# - N4: Unary transform recorded as open design question OQ8; no candidate emitted
# - N5: Deterministic internal-consistency assertion: abs_diff count == constant == CSV field
# - N6: MD §9.3 cross-links to §9.1 (sum) and §5 (direction), states joint (F1, F2, F3) basis

# %% [markdown]
# ## Hypothesis / Falsifier / Sanity Check
#
# **This notebook is DECISION-ONLY. No feature materialisation. No Parquet. No audit. No status update.**
#
# **Hypothesis:** The adjudicator module correctly enumerates 33 binding candidate specs
# (F1=10 + F2=10 + F3=10 + F5=3) from the PR #266 validator's frozen 24-tuple, with
# direction annotations and source-column traceability verified by the validator.
#
# **Falsifiers:**
# - `validator_passed is False` → HALT before any artifact write
# - `validator_halting_falsifier is not None` → HALT
# - Any Parquet file emitted → scope violation
# - `materialized_output_paths != ()` → scope violation
# - `binding_difference_family_numeric_pair_count != 10` → A20 resolution mismatch
#
# **Sanity check:** CSV has 23 columns, 2 rows. MD has 13 sections.
# No `NOT_FOUND` in any SHA field.
#
# **Expected artifact:** One CSV + One MD under
# `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`

# %% [markdown]
# ## Context: Parent SHA pins and lineage
#
# | Artifact | Expected SHA-256 |
# |---|---|
# | 02_01_02 Parquet | `24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39` |
# | 02_01_03 Parquet | `053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071` |
# | Validator module | `d8f34760db2e216cd8b838ab510bd252e7474e0324e4df1bec5d609a293b1753` |
#
# **Lineage position:**
# `PR #264 → PR #265 → PR #266 → PR #267 → THIS PR (adjudication only; no materialisation)`

# %% [markdown]
# ## Binding candidate enumeration table
#
# | Family | Count | Direction | Transform | Source |
# |---|---|---|---|---|
# | F1: focal_minus_opponent_<stem>_diff | 10 | focal_minus_opponent | signed difference | 10 audited numeric pairs |
# | F2: <stem>_pair_mean | 10 | symmetric | (focal + opponent) / 2 | 10 audited numeric pairs |
# | F3: <stem>_pair_abs_diff | 10 | symmetric | |focal - opponent| | 10 audited numeric pairs |
# | F4: matchup history pair ops | DROPPED | — | B1: no audited opponent counterpart | — |
# | F5: cross_region_pair_{or,and,xor} | 3 | symmetric | BOOLEAN pair transforms | 2 audited bool columns |
# | F6: race-pair categorical interactions | DEFERRED to 02_05 | — | Pipeline-Section convention | — |
#
# **Total: 33 binding candidates** (F1=10 + F2=10 + F3=10 + F5=3)
#
# **A20 note:** Plan estimated 11 numeric pairs; actual is 10
# (`matchup_h2h_count` is unpaired; `matchup_h2h_focal_win_rate` is also unpaired per B1).

# %%
from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import (
    BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS,
    BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS,
    BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS,
    MATCHUP_HISTORY_TRANSFORM_DECISION,
    SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION,
    run_symmetry_difference_feature_scope_adjudication,
)

print("BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS count:", len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS))
print("BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS:", BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS)
print("BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS:", BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS)
print("MATCHUP_HISTORY_TRANSFORM_DECISION:", MATCHUP_HISTORY_TRANSFORM_DECISION)
print("SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION:", SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION)

# %%
result = run_symmetry_difference_feature_scope_adjudication()
print("validator_passed:", result.validator_passed)
print("validator_halting_falsifier:", result.validator_halting_falsifier)
print("total_binding_candidate_count:", result.total_binding_candidate_count)
print("binding_difference_family_numeric_pair_count:", result.binding_difference_family_numeric_pair_count)
print("csv_path:", result.csv_path)
print("md_path:", result.md_path)
print("materialized_output_paths:", result.materialized_output_paths)

# %%
assert result.validator_passed is True, f"HALT: validator failed: {result.validator_halting_falsifier!r}"
assert result.validator_halting_falsifier is None, f"HALT: {result.validator_halting_falsifier!r}"
assert result.csv_path.exists(), f"HALT: CSV not found at {result.csv_path}"
assert result.md_path.exists(), f"HALT: MD not found at {result.md_path}"
assert result.materialized_output_paths == (), f"HALT: non-empty materialized_output_paths"
assert result.binding_difference_family_numeric_pair_count == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)
assert result.total_binding_candidate_count == 33, f"HALT: expected 33, got {result.total_binding_candidate_count}"

from pathlib import Path
_no_02_02_01 = result.csv_path.parents[3] / "02_02_01"
assert not _no_02_02_01.exists(), f"HALT: forbidden directory exists: {_no_02_02_01}"

print("All assertions passed.")

# %%
print("=== CSV head (first 300 chars) ===")
csv_text = result.csv_path.read_text(encoding="utf-8")
print(csv_text[:300])

print("\n=== MD head (first 800 chars) ===")
md_text = result.md_path.read_text(encoding="utf-8")
print(md_text[:800])

# %% [markdown]
# ## Closing summary
#
# **Produced:**
# - One CSV adjudication artifact (23 columns, 2 rows)
# - One MD adjudication artifact (13 sections)
# - Both emitted under `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
#
# **NOT produced (per §Scope hard-stops):**
# - **No Parquet** under `02_symmetry_and_difference_features/`
# - **No CROSS-02-01 leakage audit** (`leakage_audit_sc2egset.{json,md}` under `02_02_01/`)
# - **No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS mutation**
# - **No research_log append** (sequence step 8 at step closure)
# - **No ROADMAP edit** (02_02_01 block from PR #264 remains byte-identical)
# - **No F4 candidates** (B1 resolved: matchup history pair operations dropped)
# - **No sum or product candidates** (B2 resolved: sum=redundant, product deferred to 02_05)
# - **No unary candidate** (N4: open design question OQ8, not bound in this PR)
# - **No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modelling**
