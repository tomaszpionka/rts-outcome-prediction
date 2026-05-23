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
# # SC2EGSet Step 02_01_02 — Source / Anchor / Race-Column Adjudication
#
# **ADJUDICATION ONLY — NON-MATERIALIZATION.**
# This notebook adjudicates three coupled pre-materialization decisions for the 5 tranche-1
# pre_game feature families and produces ONE artifact pair (CSV + MD). It persists ZERO
# feature values. It does NOT run the CROSS-02-01-v1.0.1 post-materialization leakage audit,
# does NOT flip any status YAML, does NOT write any research_log entry, does NOT edit the
# ROADMAP, and does NOT begin any Phase 03 or 02_01_03+ work.
#
# **This PR (#234) does NOT:**
# - Materialize any of the 5 pre_game feature columns.
# - Produce `reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}`.
# - Run or claim the post-materialization CROSS-02-01 audit.
# - Flip STEP_STATUS, PIPELINE_SECTION_STATUS, or PHASE_STATUS.
# - Write a research_log entry.
# - Edit the ROADMAP.
# - Patch any spec or cleaning-layer YAML.
# - Start Step 02_01_03 or any Phase 03 work.
#
# **Three decisions adjudicated:**
# - Q1 — Which source layer to use for the 5 tranche-1 pre_game families.
# - Q2 — Which temporal anchor to use: Q2(a) Phase-02 row-identity (BINDING),
#         Q2(b) Phase-03 chronological hold-out (RECOMMENDATION ONLY).
# - Q3 — Race-column: RATIFY the existing cleaning-layer convention vs AMEND (RISK-26).
#
# **Lineage position:** artifact #4 in the 5-artifact lineage for Step 02_01_02 readiness.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_pre_game_source_layer import (
    adjudicate_pre_game_source_layer,
)

# %% [markdown]
# ## Context and binding evidence artifacts
#
# This notebook binds to the following on-disk artifacts and spec documents (all read-only):
#
# **Registry CSV (authoritative catalog, closed Step 02_01_01):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/
#   01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
#
# **Cleaning-layer YAML schemas (authoritative for column provenance decisions):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml`
#   lines 101-103: `selectedRace` explicitly excluded; `race` used as PRE_GAME analytical canon.
# - `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`
#   lines 52-53: MHM `faction` is PRE_GAME; derives from `race` not `selectedRace`.
#
# **PR #229 §10 verdict CSV (design-time registry audit, read-only):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/
#   01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv`
#
# **PR #230 vacuous leakage JSON (remains FUTURE non-vacuous; byte-unchanged):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/
#   leakage_audit_sc2egset.json` (features_audited=[], verdict=PASS; vacuous)
#
# **RISK-26 register (methodology_risk_register.md lines 479-492):**
# - `thesis/pass2_evidence/methodology_risk_register.md`
# - RISK-26: the focal race feature for Random-pickers is `Random` at game-start time
#   (selectedRace), not the eventually-played race. Tension with the cleaning-layer
#   convention documented in this adjudication.
#
# **Locked Phase-02 specs:**
# - CROSS-02-00-v3.0.1: canonical join/anchor; §3.1 TIMESTAMP anchor; §5.4 MHM faction PRE_GAME.
# - CROSS-02-01-v1.0.1: post-materialization audit protocol; §4 execution timing (FUTURE).
# - CROSS-02-02-v1.0.1: §6.1 sc2egset pre_game candidates; Random is a 4th declared race.
# - CROSS-02-03-v1.0.1: §6.1 pre_game cutoff = none; anchor is row-identity not window bound.
#
# **This plan:** `planning/current_plan.md` (PR #234).

# %% [markdown]
# ## Three-decision question table
#
# | Decision | Question | Outcome type |
# |----------|----------|--------------|
# | Q1 — Source layer | Which view/table carries the 5 tranche-1 families natively with 1v1 scope? | BINDING |
# | Q2(a) — Phase-02 row-identity anchor | `details_timeUTC` VARCHAR or `started_at` TIMESTAMP? | BINDING |
# | Q2(b) — Phase-03 hold-out anchor | Which column for chronological train/test ordering? | RECOMMENDATION ONLY |
# | Q3 — Race-column | RATIFY cleaning-layer convention (race = PRE_GAME) or AMEND (restore selectedRace per RISK-26)? | BINDING |
#
# All three decisions are adjudicated by the module imported above. The notebook calls
# `adjudicate_pre_game_source_layer(...)` which runs the DuckDB peeks read-only, evaluates
# each falsifier, and writes the 3-row CSV + 8-section MD artifact pair.

# %%
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DUCKDB_PATH = _REPO_ROOT / "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
_REGISTRY_CSV_PATH = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
    / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
    / "02_01_01_feature_family_registry.csv"
)
_OUTPUT_ARTIFACT_DIR = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts"
    / "02_feature_engineering/01_pre_game_vs_in_game_boundary"
)

print(f"DuckDB path: {_DUCKDB_PATH}")
print(f"DuckDB exists: {_DUCKDB_PATH.exists()}")
print(f"Registry CSV exists: {_REGISTRY_CSV_PATH.exists()}")
print(f"Output dir: {_OUTPUT_ARTIFACT_DIR}")

# %%
result = adjudicate_pre_game_source_layer(
    duckdb_path=_DUCKDB_PATH,
    registry_csv_path=_REGISTRY_CSV_PATH,
    output_artifact_dir=_OUTPUT_ARTIFACT_DIR,
)

# %%
print(f"passed          = {result.passed}")
print(f"decisions       = {len(result.decisions)}")
print(f"halting_falsifier = {result.halting_falsifier}")
print(f"materialized_output_paths = {result.materialized_output_paths}")
print()
print(f"artifact CSV: {result.artifact_csv_path}")
print(f"artifact MD:  {result.artifact_md_path}")
print()
for decision in result.decisions:
    print(f"  {decision.decision_id}: chosen = {decision.chosen[:80]}")

# %% [markdown]
# ## Closing: non-substitution and future-gate statement
#
# **Explicit non-substitution statement:**
# This notebook and the artifact pair it produces do NOT replace, weaken, or amend:
# (a) PR #229 §10 design-time verdict-audit pair;
# (b) PR #230 CROSS-02-01 vacuous leakage-audit pair;
# (c) the FUTURE post-materialization CROSS-02-01 audit (which does not yet exist).
#
# **Nothing materialized.** No feature value was computed or written. No Parquet/CSV feature
# table was written. `materialized_output_paths` is always `()`.
#
# **Future gates (not discharged here):**
# - The CROSS-02-01-v1.0.1 post-materialization leakage audit remains FUTURE. It becomes
#   non-vacuous only after a materialization-execution PR runs the projection SQL.
# - The mandatory Claude/ChatGPT second-pass leakage review over the eventual projection SQL
#   also remains FUTURE. These are distinct gates and are not discharged by this adjudication.
# - The three decisions recorded in this artifact are frozen inputs for the next
#   (Layer-3) materialization-execution planner-science round.
