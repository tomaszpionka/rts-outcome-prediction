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
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 02_03_01 SCAFFOLD — V1 Predecessor Artifact Provenance Validation (sc2egset)
#
# **Hypothesis:** The 4 predecessor artifacts (02_01_02 pre_game Parquet, 02_01_03
# history-enriched pre_game Parquet, 02_01_99 rating omit-closure CSV, 02_02_01
# symmetry/difference features Parquet) are byte-stable at the SHA256 pins recorded
# in `validate_temporal_feature_grid.py` and accessible via relative paths from the
# repo root (Invariant I10).
#
# **Falsifier:** Any of the following → V1 validator returns FAIL:
#   - Artifact missing at expected relative path.
#   - SHA256 mismatch vs pinned value.
#   - Required identity columns absent from Parquet schema.
#   - Row count differs from 44418 (Parquet artifacts; CSV exempt).
#   - Forbidden outputs directory (`reports/artifacts/02_feature_engineering/03_temporal_features/`) exists.
#   - Any input path is absolute (Invariant I10 violation).
#
# **Sanity check:** All 4 paths resolve relative to repo root; no absolute paths.
#
# **Lineage:** Layer-1 plan PR #275 (merged at e1701709); ROADMAP stub PR #274
# (merged at 6716aa17); parent artifacts PR #236/#259/#255/#270.
#
# **Out of scope:** V3 (strict-`<` temporal-discipline) is deferred to the
# IMMEDIATELY-NEXT scaffold rung per NIT-2 of PR #275. This notebook validates
# provenance only; it does NOT compute any temporal feature, window, decay, or
# cold-start threshold.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid import (
    validate_predecessor_artifact_provenance,
)

# %%
# Run V1 validator against repo root.
# In a notebook, __file__ is not available; resolve from the notebook path via cwd.
# The sandbox notebook lives at:
#   sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_scaffold.ipynb
# so the repo root is 5 levels up from this file's parent when run as .py,
# or via Path.cwd() when run as a notebook in the repo root.
import subprocess  # noqa: PLC0415

_git_root_bytes = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
repo_root = Path(_git_root_bytes.decode().strip())
result = validate_predecessor_artifact_provenance(repo_root=repo_root)

# %%
# Report result (print, not logger, per feedback_notebook_print_vs_logger.md).
print(f"V1 validator passed: {result.passed}")
print(f"Halting falsifier: {result.halting_falsifier}")
print(f"Parent paths checked: {result.parent_paths_checked}")
print(f"SHA matches: {result.sha_matches}")
print(f"Identity columns OK: {result.identity_columns_ok}")
print(f"Row counts: {result.row_counts}")
print(f"Outputs dir absent: {result.outputs_dir_absent}")

# %% [markdown]
# **End of scaffold notebook.** No artifact emitted. V3 deferred to next scaffold rung.
