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
# # Step 02_01_01 — Registry §10 verdict audit: sc2egset
#
# **INCREMENT 1 of N — scaffold + PM-1 only; design-time §10 verdict audit;
# NOT materialization; does NOT close Step `02_01_01`; does NOT flip
# STEP_STATUS/PHASE_STATUS; NO artifact written.**
#
# **Phase:** 02 — Feature Engineering
# **Pipeline Section:** 02_01 — Pre-Game vs In-Game Boundary
# **Step:** 02_01_01 (closure increment 1/N)
# **Dataset:** sc2egset
#
# ## Data-analysis lineage 7-tuple (per `.claude/rules/data-analysis-lineage.md`)
#
# | Field | Value |
# |-------|-------|
# | **Assumption** | Every registry row's recorded `status` matches the §10 verdict derivable from CROSS-02-03-v1.0.1 rules + row evidence fields. |
# | **Measurement claim** | Independent §10 verdict derivation for 26 rows; bidirectional drift comparison to recorded `status`; independent §10.2 trigger evaluation. |
# | **Sanity check** | S-1: CSV exists; S-2: 26 rows; S-3: unique IDs; S-4: derive-before-compare; S-5: materialized_column_count == 0; S-6: no write side effects. |
# | **Falsifier** | Any F-1a / F-1b / F-2 / F-3 / F-4 / F-5 / F-6 / F-7 hit halts immediately. |
# | **Expected report** | RegistryVerdictAuditResult with passed=True, rows_audited=26, materialized_column_count=0. |
# | **Lineage source** | `02_01_01_feature_family_registry.csv` + `tracker_events_feature_eligibility.csv` + CROSS-02-03-v1.0.1 §10. |
# | **Downstream decision** | Confirms the 26-row registry is consistent with §10 protocol; gates future feature-generation notebooks. |

# %% [markdown]
# ## Hypothesis
#
# Every one of the 26 feature-family rows in the on-disk registry carries a
# `status` value that exactly matches (modulo the `blocked_until_additional_validation`
# / `blocked_until_validation` synonym) the verdict derivable from
# CROSS-02-03-v1.0.1 §10 rules applied to the row's evidence fields. No row
# triggers an unmitigated §10.2 blocking condition that its recorded `status`
# does not already reflect.

# %% [markdown]
# ## Falsifiers
#
# - **F-1** (overall — bidirectional EQUALITY): derived §10 verdict MUST equal
#   recorded `status` (modulo synonym). Any discrepancy halts.
# - **F-1a** (stricter drift — HALT): derived verdict is more restrictive than
#   recorded status (registry is optimistic / stale).
# - **F-1b** (looser drift — HALT): derived verdict is less restrictive than
#   recorded status (registry is overly conservative or derivation is missing
#   a caveat path).
# - **F-2** (independent §10.2 trigger — HALT): §10.2 trigger fires on a row
#   recorded as `allowed` / `allowed_with_caveat` (evaluated without reading `status`).
# - **F-3** (POST-GAME token leakage — HALT): `allowed_cutoff_rule` contains
#   `won`, `final_state`, `match_result`, or `post_game`.
# - **F-4** (invalid cutoff operator — HALT): history row's `allowed_cutoff_rule`
#   contains `<=` instead of strict `<`.
# - **F-5** (D13 tracker contradiction — HALT): tracker CSV says
#   `blocked_until_additional_validation` but registry says `allowed`/`allowed_with_caveat`.
# - **F-6** (slot-identity gate misuse — HALT): `slot_identity_consistency` is
#   NOT classified `sanity_gate_not_model_input`.
# - **F-7** (controlled-vocab drift — HALT): any row's `status` is not in the
#   recognised vocabulary.

# %%
import logging

from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
    RegistryVerdictAuditResult,
    load_registry_rows,
    validate_registry_section10_verdicts,
)

setup_notebook_logging()
logger = logging.getLogger(__name__)

# %% [markdown]
# ## Path resolution

# %%
_REPORTS_DIR = get_reports_dir("sc2", "sc2egset")

REGISTRY_CSV_PATH = (
    _REPORTS_DIR
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
    / "02_01_01_feature_family_registry.csv"
)

TRACKER_CSV_PATH = (
    _REPORTS_DIR
    / "artifacts"
    / "01_exploration"
    / "03_profiling"
    / "tracker_events_feature_eligibility.csv"
)

print(f"Registry CSV path : {REGISTRY_CSV_PATH}")
print(f"Registry CSV exists: {REGISTRY_CSV_PATH.exists()}")
print(f"Tracker CSV path  : {TRACKER_CSV_PATH}")
print(f"Tracker CSV exists : {TRACKER_CSV_PATH.exists()}")

# %% [markdown]
# ## Sanity checks S-1 / S-2 / S-3
#
# Call `load_registry_rows` which enforces:
# - S-1: CSV exists on disk.
# - S-2: Exactly 26 data rows.
# - S-3: All `feature_family_id` values are unique.

# %%
rows = load_registry_rows(REGISTRY_CSV_PATH)
print(f"Row count (S-2): {len(rows)}")
assert len(rows) == 26, f"S-2 FAIL: expected 26, got {len(rows)}"
print("S-1 PASS: registry CSV exists")
print("S-2 PASS: 26 rows loaded")
print("S-3 PASS: unique IDs confirmed by load_registry_rows")
print()
print("First 3 rows (feature_family_id, prediction_setting, status):")
for r in rows[:3]:
    print(f"  {r['feature_family_id']}: {r['prediction_setting']} / {r['status']}")

# %% [markdown]
# ## §10 Verdict audit

# %%
result: RegistryVerdictAuditResult = validate_registry_section10_verdicts(
    REGISTRY_CSV_PATH,
    TRACKER_CSV_PATH,
)

print(f"passed              : {result.passed}")
print(f"rows_audited        : {result.rows_audited}")
print(f"halting_falsifier   : {result.halting_falsifier}")
print(f"stricter_drifts     : {len(result.stricter_drifts)}")
print(f"looser_drifts       : {len(result.looser_drifts)}")
print(f"trigger_hits        : {len(result.independent_trigger_hits)}")
print(f"materialized_cols   : {result.materialized_column_count}")

# %% [markdown]
# ## Drift report

# %%
if result.stricter_drifts:
    print("HALT — F-1a STRICTER DRIFTS DETECTED:")
    for ffid, derived, recorded in result.stricter_drifts:
        print(f"  {ffid}: derived={derived}, recorded={recorded}")
else:
    print("F-1a PASS: no stricter drifts")

if result.looser_drifts:
    print("HALT — F-1b LOOSER DRIFTS DETECTED:")
    for ffid, derived, recorded in result.looser_drifts:
        print(f"  {ffid}: derived={derived}, recorded={recorded}")
else:
    print("F-1b PASS: no looser drifts")

# %% [markdown]
# ## §10.2 Independent trigger report

# %%
if result.independent_trigger_hits:
    print("HALT — F-2 INDEPENDENT TRIGGER HITS:")
    for ffid, trigger in result.independent_trigger_hits:
        print(f"  {ffid}: trigger={trigger}")
else:
    print("F-2 PASS: no independent trigger hits on allowed/caveat rows")

# %% [markdown]
# ## Vacuous clause-2 check (S-5)
#
# CROSS-02-01-v1.0.1 §4 defines "Materialization" as persisting a feature
# column to DuckDB or Parquet. The registry catalog persists **zero** feature
# columns. Therefore the clause-2 post-materialization audit column set is
# EMPTY and vacuously satisfied.

# %%
print(f"materialized_column_count = {result.materialized_column_count}")
print(
    "S-5 PASS: materialized_column_count == 0 (design-time audit; "
    "clause-2 column set EMPTY — vacuously satisfied per "
    "CROSS-02-01-v1.0.1 §4 Materialization definition)."
)

# %% [markdown]
# ## Gate assertions

# %%
assert result.passed is True, (
    f"HALT: audit did not pass. halting_falsifier={result.halting_falsifier}, "
    f"stricter={result.stricter_drifts}, looser={result.looser_drifts}, "
    f"triggers={result.independent_trigger_hits}"
)
assert result.rows_audited == 26, (
    f"HALT: expected 26 rows audited, got {result.rows_audited}"
)
assert result.materialized_column_count == 0, (
    f"HALT: materialized_column_count should be 0, got {result.materialized_column_count}"
)
print("ALL GATE ASSERTIONS PASS.")

# %% [markdown]
# ## Closure statement (S-6)
#
# This notebook is a **design-time §10 verdict audit**, not materialization.
#
# No output of this notebook writes to:
# - `reports/artifacts/` (no artifact CSV / Parquet / PNG produced)
# - `reports/STEP_STATUS.yaml`
# - `reports/PHASE_STATUS.yaml`
# - `reports/ROADMAP.md`
# - `reports/research_log.md`
# - any Phase-03 path
#
# **PM-1 does NOT close Step `02_01_01`.** It is increment 1 of N required to
# close this step. The step remains open after this PR merges.
#
# **S-6 PASS**: confirmed by code review — no `to_csv`, `to_parquet`, `open("w")`,
# or status-YAML write appears anywhere in this notebook.
