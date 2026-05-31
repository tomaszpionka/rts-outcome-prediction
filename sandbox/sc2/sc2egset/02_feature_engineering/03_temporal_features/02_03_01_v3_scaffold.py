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
# # Step 02_03_01 V3 SCAFFOLD — strict-< Temporal-Discipline Validator (sc2egset)
#
# **Hypothesis:** The four predecessor artifacts (02_01_02 pre_game, 02_01_03
# history-enriched, 02_01_99 omit-closure, 02_02_01 symmetry/difference) satisfy
# strict-`<` temporal discipline at the schema layer: (a) `started_at` temporal
# anchor present; (b) history columns follow `^(focal|opponent)_.*_prior_` naming;
# (c) no forbidden naming patterns (`_including_target`, `_h2h_with_target`, etc.);
# (d) cross-spec citation provenance preserved in validator module docstring.
#
# **Falsifier:** Any of the following → V3 validator returns FAIL:
#   - H1: Artifact missing or SHA mismatch vs pinned values.
#   - H2: `started_at: timestamp[us]` column missing from any Parquet schema.
#   - H3: Forbidden history-column naming pattern detected, OR no `^(focal|opponent)_.*_prior_` columns.
#   - H4: Required CROSS-02-03 / CROSS-02-02 / Invariant I3 cite-string missing from validator docstring.
#   - H5: Forbidden V3 outputs directory exists.
#   - H6: SC2-specific or AoE2-specific term in V3 module public surface.
#   - H7: Empirical AoE2 transferability claim in V3 docstring/comments.
#
# **Sanity check:** V3 is DESIGN-TIME ONLY. Validator reads schema metadata +
# Parquet footer + file SHA + provenance docstring text. NO data-value reads.
# NO DuckDB queries. NO recomputation. NO feature materialization.
#
# **Lineage:** Layer-1 plan PR #277 (merged at 73fa5a5c); V1 scaffold rung PR #276
# (merged at 37c3a8855); ROADMAP stub PR #274 (merged at 6716aa17); 4 parent
# artifacts PR #236/#259/#255/#270.
#
# **Out of scope:** V3 does NOT pin concrete window sizes, decay half-lives, or
# cold-start k-thresholds (OQ-1 deferred). V3 does NOT decide tracker_events
# family inclusion (OQ-2 deferred). V3 does NOT decide in-game temporal scope
# vs 02_01_03 (OQ-3 deferred). V3 cites CROSS-02-02 and CROSS-02-03 with
# distinct roles (OQ-4 boundary preserved, no conflation). V3 makes NO empirical
# AoE2 transferability claim (Q8 syntactic-only). Phase 03 + baselines BARRED.

# %%
import subprocess  # noqa: PLC0415
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
    validate_temporal_discipline,
)

# %%
# Run V3 validator against repo root.
# In a notebook __file__ is not available; resolve via git rev-parse.
_git_root_bytes = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
repo_root = Path(_git_root_bytes.decode().strip())
result = validate_temporal_discipline(repo_root=repo_root)

# %%
# Report result per `feedback_notebook_print_vs_logger.md`: print() for data exploration.
print(f"V3 validator passed: {result.passed}")
print(f"Halting falsifier: {result.halting_falsifier}")
print(f"H1 artifact provenance OK: {result.artifact_provenance_ok}")
print(f"H2 temporal anchor present: {result.temporal_anchor_present}")
print(f"H3 history naming valid: {result.history_naming_valid}")
print(f"H3 forbidden columns absent: {result.forbidden_columns_absent}")
print(f"H4 cite strings present: {result.cite_strings_present}")
print(f"H5 outputs dir absent: {result.outputs_dir_absent}")
print(f"H6 cross-game vocabulary OK: {result.cross_game_vocabulary_ok}")
print(f"H7 no AoE2 empirical claim: {result.no_aoe2_empirical_claim}")

# %% [markdown]
# **End of V3 scaffold notebook.** No artifact emitted. V3 is design-time only;
# value-level leakage gated by CROSS-02-01 post-materialization audits.
# Adjudication of concrete grid values deferred to a future adjudication PR.
