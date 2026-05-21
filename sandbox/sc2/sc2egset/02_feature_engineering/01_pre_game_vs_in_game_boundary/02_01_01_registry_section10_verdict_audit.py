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
# STEP_STATUS/PHASE_STATUS.**
#
# artifact persisted in evidence-persistence PR — 02_01_01_section10_verdict_audit.{csv,md}
# Step 02_01_01 STILL OPEN; status YAMLs intentionally NOT flipped
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
# ## Persist §10 verdict-audit evidence (PERSIST falsifier)

# %%
import hashlib
import subprocess
from datetime import datetime, timezone

import pandas as pd

from rts_predict.games.sc2.datasets.sc2egset.validate_registry_section10_verdicts import (
    DATASET_SIDE_BLOCKED_SYNONYM,
    HISTORY_STRICT_CUTOFF,
    INGAME_CUTOFF,
    SECTION10_VERDICTS,
    SLOT_IDENTITY_FEATURE_ID,
    Section10Rules,
    derive_section10_verdict,
)

# Paths (reuse existing pattern: _REPORTS_DIR from the path-resolution cell above)
ARTIFACT_DIR = (
    _REPORTS_DIR
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
)
ARTIFACT_CSV = ARTIFACT_DIR / "02_01_01_section10_verdict_audit.csv"
ARTIFACT_MD = ARTIFACT_DIR / "02_01_01_section10_verdict_audit.md"

# For SHA-256 provenance — paths resolved via _REPORTS_DIR which is an absolute Path
_REPO_ROOT = _REPORTS_DIR.parents[4]  # reports/ -> sc2egset/ -> datasets/ -> sc2/ -> games/ -> src/ -> repo
# Actually resolve via git for reliability
_REPO_ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=str(_REPORTS_DIR)
).decode().strip()

VALIDATOR_PATH_ABS = (
    _REPORTS_DIR.parents[0]  # sc2egset/
    / "validate_registry_section10_verdicts.py"
)

# Deterministic provenance
audit_executed_at_utc_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


validator_module_sha256 = hashlib.sha256(VALIDATOR_PATH_ABS.read_bytes()).hexdigest()
registry_csv_sha256 = hashlib.sha256(REGISTRY_CSV_PATH.read_bytes()).hexdigest()
tracker_csv_sha256 = hashlib.sha256(TRACKER_CSV_PATH.read_bytes()).hexdigest()

VALIDATOR_MODULE = "src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py"
SPEC_REVISION_CROSS_02_03 = "CROSS-02-03-v1.0.1"
SOURCE_PR = "PR #228"
AUDIT_PR = "PR #229"

# Re-run audit (fresh; result from the gate-assertions cell is also in scope but re-derive for clarity)
result_persist = validate_registry_section10_verdicts(REGISTRY_CSV_PATH, TRACKER_CSV_PATH)
assert result_persist.passed is True
assert result_persist.rows_audited == 26
assert result_persist.halting_falsifier is None
assert result_persist.materialized_column_count == 0
assert len(result_persist.stricter_drifts) == 0
assert len(result_persist.looser_drifts) == 0
assert len(result_persist.independent_trigger_hits) == 0

# Load registry in stable order for joinability + per_family fields
registry_df = pd.read_csv(REGISTRY_CSV_PATH, dtype=str, keep_default_na=False)
assert len(registry_df) == 26

# Build per-row Section10Verdict objects by calling derive_section10_verdict
# directly (RegistryVerdictAuditResult has no per_row_verdicts field; derive
# individually using the same protocol_rules as validate_registry_section10_verdicts)
_TRACKER_BLOCKED_TOKEN_LITERAL = "blocked_until_additional_validation"
_protocol_rules = Section10Rules(
    verdicts=SECTION10_VERDICTS,
    blocking_triggers=(
        "missing_grain",
        "missing_prediction_setting",
        "ambiguous_temporal_anchor",
        "history_lacking_strict_lt",
        "tracker_absent_or_blocked",
        "aoe2_source_label_regression",
        "pseudocount_without_derivation",
        "feature_table_generation_attempted_before_audit",
    ),
    history_cutoff=HISTORY_STRICT_CUTOFF,
    ingame_cutoff=INGAME_CUTOFF,
    slot_identity_feature_id=SLOT_IDENTITY_FEATURE_ID,
    sc2_tracker_blocked_token=_TRACKER_BLOCKED_TOKEN_LITERAL,
    tracker_eligibility_csv_path=TRACKER_CSV_PATH,
)

# Build stricter/looser/trigger sets from the aggregate result
stricter_set = {ffid for ffid, _, _ in result_persist.stricter_drifts}
looser_set = {ffid for ffid, _, _ in result_persist.looser_drifts}
trigger_map = {}
for ffid, trig in result_persist.independent_trigger_hits:
    trigger_map.setdefault(ffid, []).append(trig)

# Synonym map for equality_token derivation
SYNONYMS = {DATASET_SIDE_BLOCKED_SYNONYM: "blocked_until_validation"}

rows_out = []
for _, reg_row in registry_df.iterrows():
    ffid = reg_row["feature_family_id"]
    # Drop status column from derivation input (same as validator)
    row_series = reg_row.drop(labels=[s for s in ("status",) if s in reg_row.index])
    v = derive_section10_verdict(row_series, _protocol_rules)
    derived = v.derived_status
    recorded_raw = reg_row["status"]
    recorded_norm = SYNONYMS.get(recorded_raw, recorded_raw)
    if recorded_norm == derived:
        eq_token = "equal_via_synonym" if recorded_raw != recorded_norm else "equal"
    elif ffid in stricter_set:
        eq_token = "stricter_drift"
    elif ffid in looser_set:
        eq_token = "looser_drift"
    else:
        eq_token = "unrecognized"

    rows_out.append({
        "feature_family_id": ffid,
        "dataset_tag": reg_row["dataset_tag"],
        "prediction_setting": reg_row["prediction_setting"],
        "registry_recorded_status": recorded_raw,
        "derived_section10_verdict": derived,
        "equality_token": eq_token,
        "stricter_drift_flag": "true" if ffid in stricter_set else "false",
        "looser_drift_flag": "true" if ffid in looser_set else "false",
        "independent_trigger_hits": "|".join(trigger_map.get(ffid, [])),
        "triggers_fired": "|".join(v.triggers_fired),
        "rule_path": v.rule_path,
        "materialized_column_count": "0",
        "halting_falsifier": "" if result_persist.halting_falsifier is None else result_persist.halting_falsifier,
        "audit_executed_at_utc_date": audit_executed_at_utc_date,
        "validator_module": VALIDATOR_MODULE,
        "validator_module_sha256": validator_module_sha256,
        "source_pr": SOURCE_PR,
        "audit_pr": AUDIT_PR,
        "registry_csv_sha256": registry_csv_sha256,
        "tracker_csv_sha256": tracker_csv_sha256,
        "spec_revision_cross_02_03": SPEC_REVISION_CROSS_02_03,
        "git_sha": git_sha,
        "block": reg_row["block"],
    })

COLUMN_ORDER = [
    "feature_family_id", "dataset_tag", "prediction_setting",
    "registry_recorded_status", "derived_section10_verdict", "equality_token",
    "stricter_drift_flag", "looser_drift_flag", "independent_trigger_hits",
    "triggers_fired", "rule_path", "materialized_column_count",
    "halting_falsifier", "audit_executed_at_utc_date", "validator_module",
    "validator_module_sha256", "source_pr", "audit_pr",
    "registry_csv_sha256", "tracker_csv_sha256", "spec_revision_cross_02_03",
    "git_sha", "block",
]
audit_df = pd.DataFrame(rows_out, columns=COLUMN_ORDER)
assert len(audit_df) == 26
assert list(audit_df.columns) == COLUMN_ORDER

# Write CSV (deterministic)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
audit_df.to_csv(ARTIFACT_CSV, index=False, encoding="utf-8", lineterminator="\n")

# PERSIST byte-equivalence check: reload, rerun validator, compare row-by-row
reloaded = pd.read_csv(ARTIFACT_CSV, dtype=str, keep_default_na=False)
assert len(reloaded) == 26
assert list(reloaded.columns) == COLUMN_ORDER

result_rerun = validate_registry_section10_verdicts(REGISTRY_CSV_PATH, TRACKER_CSV_PATH)
assert result_rerun.passed is True
assert result_rerun.rows_audited == 26
assert result_rerun.halting_falsifier is None

# Compare row-by-row, column-by-column.
# Only audit_executed_at_utc_date and git_sha may differ; audit_pr is NOT in the allowed-drift set.
ALLOWED_DRIFT = {"audit_executed_at_utc_date", "git_sha"}
mismatches = []
for i in range(26):
    for col in COLUMN_ORDER:
        if col in ALLOWED_DRIFT:
            continue
        a = audit_df.iloc[i][col]
        b = reloaded.iloc[i][col]
        if a != b:
            mismatches.append((i, col, a, b))
assert not mismatches, f"PERSIST falsifier fired: {mismatches[:5]}"

# Build companion MD
md = []
md.append("# 02_01_01 Section-10 Verdict Audit — Evidence")
md.append("")
md.append("## §1 Non-closure disclaimer")
md.append("")
md.append(
    "This artifact persists evidence but does NOT close Step `02_01_01`. "
    "Closure requires a separate later increment that flips `STEP_STATUS.yaml`, "
    "satisfies the ROADMAP `continue_predicate` three-clause gate in writing, "
    "and lands a separate closure PR. Phase 02 is `not_started` per "
    "`PHASE_STATUS.yaml` and is not advanced by this PR."
)
md.append("")
md.append("## §2 Provenance")
md.append("")
md.append(f"- `audit_executed_at_utc_date`: `{audit_executed_at_utc_date}`")
md.append(f"- `git_sha`: `{git_sha}`")
md.append(f"- `validator_module`: `{VALIDATOR_MODULE}`")
md.append(f"- `validator_module_sha256`: `{validator_module_sha256}`")
md.append(f"- `registry_csv_sha256`: `{registry_csv_sha256}`")
md.append(f"- `tracker_csv_sha256`: `{tracker_csv_sha256}`")
md.append(f"- `spec_revision_cross_02_03`: `{SPEC_REVISION_CROSS_02_03}`")
md.append(f"- `source_pr`: `{SOURCE_PR}`")
md.append(f"- `audit_pr`: `{AUDIT_PR}`")
md.append("")
md.append("## §3 Aggregate result")
md.append("")
md.append(f"- `passed`: `{result_persist.passed}`")
md.append(f"- `rows_audited`: `{result_persist.rows_audited}`")
md.append(f"- `halting_falsifier`: `{result_persist.halting_falsifier}`")
md.append(f"- `len(stricter_drifts)`: `{len(result_persist.stricter_drifts)}`")
md.append(f"- `len(looser_drifts)`: `{len(result_persist.looser_drifts)}`")
md.append(f"- `len(independent_trigger_hits)`: `{len(result_persist.independent_trigger_hits)}`")
md.append(f"- `materialized_column_count`: `{result_persist.materialized_column_count}`")
md.append("")
md.append("## §4 Falsifier roll-call")
md.append("")
md.append("| Falsifier | Description | Result |")
md.append("|---|---|---|")
md.append("| F-1 | Overall bidirectional §10 EQUALITY | did not fire |")
md.append("| F-1a | Stricter drift (derived > recorded) | did not fire |")
md.append("| F-1b | Looser drift (derived < recorded) | did not fire |")
md.append("| F-2 | Independent §10.2 trigger on allowed/caveat row | did not fire |")
md.append("| F-3 | Post-game token in `allowed_cutoff_rule` | did not fire |")
md.append("| F-4 | Invalid cutoff operator on history row | did not fire |")
md.append("| F-5 | D13 tracker contradiction | did not fire |")
md.append("| F-6 | Slot-identity gate misuse | did not fire |")
md.append("| F-7 | Controlled-vocab drift | did not fire |")
md.append("| PERSIST | Persistence byte-equivalence | did not fire |")
md.append("")
md.append("## §5 ROADMAP `continue_predicate` three-clause analysis")
md.append("")
md.append("**ROADMAP `continue_predicate` (verbatim, `ROADMAP.md` lines 2060-2066):**")
md.append("")
md.append(
    "> A future PR may begin Step 02_01_02 (or the next 02_01 step in the ROADMAP) "
    "only after this Step 02_01_01 has reached its CSV + MD artifact-check at a "
    "future PR, the CROSS-02-01-v1.0.1 post-materialization audit gate has been "
    "re-run for any feature column the registry triggers materialization of, and "
    "a per-family CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row."
)
md.append("")
md.append("| Clause | Status |")
md.append("|---|---|")
md.append(
    "| 1 — Registry CSV+MD artifact-check | SATISFIED for the registry CSV/MD by PR #216 (provisional artifact); the new PM-1 evidence artifact is incremental and does NOT itself satisfy clause 1. |"
)
md.append(
    "| 2 — Post-materialization audit gate | VACUOUSLY SATISFIED. No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121. |"
)
md.append(
    "| 3 — Per-family §10 verdict recorded for every registry row | SATISFIED in memory by PR #228 + PERSISTED ON DISK by PR #229 for all 26 rows. |"
)
md.append("")
md.append(
    "**Closure status remains OPEN** — clause-1 is satisfied; clause-3 is satisfied as of this PR; "
    "the three-clause gate is positioned to be closed only by a later explicit closure PR with status-YAML flips."
)
md.append("")
md.append("## §6 Methodology lineage")
md.append("")
md.append(
    "- Spec source: `reports/specs/02_03_temporal_feature_audit_protocol.md` §10 (CROSS-02-03-v1.0.1, LOCKED 2026-05-06); "
    "`reports/specs/02_01_leakage_audit_protocol.md` §4 lines 117–121 (Materialization)."
)
md.append(
    f"- Validator: `{VALIDATOR_MODULE}` (frozen by PR #228; SHA-256 `{validator_module_sha256}`)."
)
md.append(
    "- Notebook: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_registry_section10_verdict_audit.py` (artifact-write cell added in PR #229)."
)
md.append(
    "- Tests: `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py` "
    "(frozen by PR #228; PERSIST byte-equivalence substitutes for re-run in this PR)."
)
md.append("")
md.append("## §7 Per-row table")
md.append("")
md.append(
    "| feature_family_id | prediction_setting | registry_recorded_status | "
    "derived_section10_verdict | equality_token | block |"
)
md.append("|---|---|---|---|---|---|")
for _, r in audit_df.iterrows():
    md.append(
        f"| `{r['feature_family_id']}` | `{r['prediction_setting']}` | "
        f"`{r['registry_recorded_status']}` | `{r['derived_section10_verdict']}` | "
        f"`{r['equality_token']}` | `{r['block']}` |"
    )
md.append("")
md.append("## §8 Cited code / SQL")
md.append("")
md.append("Validator entry point (frozen by PR #228):")
md.append("")
md.append("```python")
md.append("def validate_registry_section10_verdicts(")
md.append("    registry_csv_path: Path,")
md.append("    tracker_csv_path: Path,")
md.append(") -> RegistryVerdictAuditResult:")
md.append('    """Entry point: load registry rows and run the full §10 verdict audit."""')
md.append("```")
md.append("")
md.append("Notebook call site (PR #229):")
md.append("")
md.append("```python")
md.append("result_persist = validate_registry_section10_verdicts(REGISTRY_CSV_PATH, TRACKER_CSV_PATH)")
md.append("assert result_persist.passed is True")
md.append("assert result_persist.rows_audited == 26")
md.append("assert result_persist.materialized_column_count == 0")
md.append("```")
md.append("")
ARTIFACT_MD.write_text("\n".join(md), encoding="utf-8")

from pathlib import Path as _Path
_repo_root_path = _Path(_REPO_ROOT)
print(f"PERSIST PASS: persisted CSV byte-equivalent on reload modulo {{audit_executed_at_utc_date, git_sha}}")
print(f"Wrote: {ARTIFACT_CSV.relative_to(_repo_root_path)}")
print(f"Wrote: {ARTIFACT_MD.relative_to(_repo_root_path)}")

# %% [markdown]
# ## Closure statement (S-6)
#
# This notebook is a **design-time §10 verdict audit**, not materialization.
#
# The artifact-write cell above writes exclusively to `reports/artifacts/02_feature_engineering/`.
# No output of this notebook writes to:
# - `reports/STEP_STATUS.yaml`
# - `reports/PHASE_STATUS.yaml`
# - `reports/ROADMAP.md`
# - `reports/research_log.md`
# - any Phase-03 path
#
# **PM-1 does NOT close Step `02_01_01`.** It is increment 1 of N required to
# close this step. The step remains open after this PR merges.
#
# **S-6 PASS**: confirmed by code review — no STEP_STATUS, PHASE_STATUS,
# ROADMAP, or research_log write appears anywhere in this notebook.
