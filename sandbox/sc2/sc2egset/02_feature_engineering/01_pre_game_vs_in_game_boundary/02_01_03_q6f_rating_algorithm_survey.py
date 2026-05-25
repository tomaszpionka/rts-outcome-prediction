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
# # SC2EGSet Step 02_01_03 — Q6F Rating-Algorithm Survey
#
# **Q6F-only Layer-2 algorithm survey.** This notebook computes
# forward-only per-row rating predictions over the
# `player_history_all` (PHA) stream for 4 rating algorithm candidates
# (rolling baseline / Elo / Glicko-2 / TrueSkill) plus 2 carry-forward
# references (omit / deferred), scores them against the actual decisive
# outcomes with proper scoring rules (log-loss + Brier with bootstrap
# CIs; AUC reported with CI as a secondary metric only), and emits one
# 44-column CSV + multi-section MD artifact pair under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
#
# **Hypothesis (Q6F question, verbatim binding from PR #245 Q6_selected_policy row):**
# Which rating reconstruction policy, if any, can be justified for later
# materialization under forward-only, cold-start (G-CS-4), deterministic,
# and deployable constraints?
#
# **Falsifier reference:** 38 falsifier keys are declared in the survey
# module (`survey_history_rating_algorithms.py`) and enumerated in
# `FALSIFIER_PRIORITY_CHAIN`. Parent PR #242 / #243 / #245 SHA pins are
# the highest priority; a mismatch halts the entrypoint before any write.
#
# **Scope:** Q6F-only. Q5 (`cross_region_fragmentation_handling`) was
# resolved by PR #243 with
# `Q5_selected_policy=sensitivity_indicator_co_registration` and is NOT
# re-adjudicated here. Q1-Q4 / Q6 / Q7 / Q8 are PR #242 / PR #245
# BINDING and are NOT re-adjudicated.
#
# **No materialization:** this notebook does NOT materialize any rating
# value, does NOT write any Parquet, does NOT run the CROSS-02-01
# post-materialization leakage audit, does NOT close Step 02_01_03, and
# does NOT update any status YAML or research_log.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessor PRs:** #239 (ROADMAP stub) →
# #240 (Layer-1 scaffold plan) → #241 (Layer-2 scaffold + validator) →
# #242 (8-question parent adjudication) → #243 (Q5 successor) →
# #244 (Q6 Layer-1 plan) → #245 (Q6 Layer-2 successor) →
# #246 (Q6F Layer-1 plan) → **THIS PR (Q6F Layer-2 algorithm survey)** →
# future materialization PRs.

# %% [markdown]
# ## Lineage position — Q6F algorithm survey in the Step 02_01_03 chain
#
# Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for
# empirical work", the Step 02_01_03 readiness chain is serialised across
# PRs. This notebook is the Q6F successor; Q5 is explicitly out of scope.
#
# 1. PR #239 — ROADMAP stub block inserted.
# 2. PR #240 — Layer-1 scaffold + validator planning PR.
# 3. PR #241 — Layer-2 SCAFFOLD + ONE validation module.
# 4. PR #242 — 8-question parent adjudication; Q6 bound deferred_blocker.
# 5. PR #243 — Q5-only successor adjudication (cross_region).
# 6. PR #244 — Q6 Layer-1 planning PR.
# 7. PR #245 — Q6-only successor adjudication; verdict =
#    `deferred_blocker_with_algorithm_survey_required`.
# 8. PR #246 — Q6F Layer-1 planning PR (this notebook's plan).
# 9. **THIS PR — Q6F-only algorithm survey** (this notebook). Persists
#    ONE artifact pair (44-column CSV × 8 rows + 18-section MD).
# 10. Future — Layer-3 materialization-execution PR (or omit-and-unblock
#     closure PR) depending on the Q6F verdict.

# %%
import hashlib
from pathlib import Path

import duckdb

from rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    BOOTSTRAP_BLOCK_COUNT,
    BOOTSTRAP_RANDOM_SEED,
    EXPECTED_PR242_CSV_SHA256,
    EXPECTED_PR242_MD_SHA256,
    EXPECTED_PR243_CSV_SHA256,
    EXPECTED_PR243_MD_SHA256,
    EXPECTED_PR245_CSV_SHA256,
    EXPECTED_PR245_MD_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PARENT_PR245_CSV_REL,
    PARENT_PR245_MD_REL,
    PHA_FORWARD_ONLY_STREAM_QUERY,
    Q5_SELECTED_POLICY,
    Q6F_ALLOWED_VERDICTS,
    Q6F_CANDIDATE_INCLUSION,
    Q6F_DECISION_IDS,
    Q6F_HYPERPARAMETER_DEFAULTS,
    Q6F_RATING_ALGORITHM_CANDIDATES,
    Q6F_SCHEMA_COLUMN_COUNT,
    Q6F_SELECTION_DECISION_RULE,
    Q6F_SURVEY_CSV_REL,
    Q6F_SURVEY_MD_REL,
    STRICT_LT_HISTORY_FILTER,
    run_q6f_rating_algorithm_survey,
)

# %% [markdown]
# ## Parent-artifact SHA verification (read-only)
#
# Before any rating engine runs, the module verifies the PR #242 / #243 /
# #245 parent artifacts against the pinned SHA constants. A mismatch
# halts the entrypoint with `RatingSurveyError` before any write.

# %%
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
print(f"REPO_ROOT = {REPO_ROOT}")

# %%
print("Parent artifact SHAs (expected vs observed):")
for rel, expected in [
    (PARENT_PR242_CSV_REL, EXPECTED_PR242_CSV_SHA256),
    (PARENT_PR242_MD_REL, EXPECTED_PR242_MD_SHA256),
    (PARENT_PR243_CSV_REL, EXPECTED_PR243_CSV_SHA256),
    (PARENT_PR243_MD_REL, EXPECTED_PR243_MD_SHA256),
    (PARENT_PR245_CSV_REL, EXPECTED_PR245_CSV_SHA256),
    (PARENT_PR245_MD_REL, EXPECTED_PR245_MD_SHA256),
]:
    h = hashlib.sha256()
    h.update((REPO_ROOT / rel).read_bytes())
    observed = h.hexdigest()
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"  {rel}: {status}")

# %% [markdown]
# ## Q5 binding preserved (NOT re-adjudicated)
#
# PR #243 closed Q5 with
# `Q5_selected_policy=sensitivity_indicator_co_registration`; this
# survey honours the binding by keeping cross-region history rows in
# the stream (the `is_cross_region_fragmented` flag is a co-registered
# evidence dimension, not a filter).

# %%
print(f"Q5_SELECTED_POLICY = {Q5_SELECTED_POLICY}  (preserved; NOT re-adjudicated)")

# %% [markdown]
# ## Forward-only stream loader probe
#
# Read-only DuckDB probe verifies the PHA stream is non-empty and
# satisfies the strict-`<` filter inherited from PR #245.

# %%
DB_PATH = REPO_ROOT / "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
print(f"DB_PATH = {DB_PATH}")
print(f"STRICT_LT_HISTORY_FILTER = {STRICT_LT_HISTORY_FILTER!r}")

# %%
print("PHA forward-only stream query (verbatim):")
print(PHA_FORWARD_ONLY_STREAM_QUERY)

# %%
_con = duckdb.connect(str(DB_PATH), read_only=True)
print("Row count of PHA forward-only stream:")
print(_con.execute("SELECT COUNT(*) FROM player_history_all WHERE result IN ('Win','Loss')").fetchone())
_con.close()

# %% [markdown]
# ## Q6F survey configuration (literature-pinned defaults)
#
# Hyperparameters are fixed literature defaults; no tuning in this PR.

# %%
print(f"Q6F_RATING_ALGORITHM_CANDIDATES ({len(Q6F_RATING_ALGORITHM_CANDIDATES)}):")
for c in Q6F_RATING_ALGORITHM_CANDIDATES:
    inclusion = "INCLUDED" if Q6F_CANDIDATE_INCLUSION[c] else "CARRY-FORWARD"
    print(f"  {c}: {inclusion}")

# %%
print(f"Q6F_HYPERPARAMETER_DEFAULTS:")
for c, hp in Q6F_HYPERPARAMETER_DEFAULTS.items():
    print(f"  {c}: {hp}")

# %%
print(f"BOOTSTRAP_BLOCK_COUNT = {BOOTSTRAP_BLOCK_COUNT}  (deterministic block resampling)")
print(f"BOOTSTRAP_RANDOM_SEED = {BOOTSTRAP_RANDOM_SEED}")

# %% [markdown]
# ## Run the survey
#
# All rating engines run forward-only over the PHA stream; per-row
# predictions are scored with proper scoring rules (log-loss, Brier) and
# AUC; bootstrap confidence intervals are computed deterministically.

# %%
CSV_PATH = REPO_ROOT / Q6F_SURVEY_CSV_REL
MD_PATH = REPO_ROOT / Q6F_SURVEY_MD_REL
print(f"CSV_PATH = {CSV_PATH}")
print(f"MD_PATH  = {MD_PATH}")

# %%
RESULT = run_q6f_rating_algorithm_survey(
    db_path=DB_PATH,
    csv_path=CSV_PATH,
    md_path=MD_PATH,
    audit_pr=AUDIT_PR_NUMBER_PLACEHOLDER,
    write_artifacts=True,
    repo_root=REPO_ROOT,
)

# %%
print(f"Survey passed: {RESULT.passed}")
print(f"Halting falsifier: {RESULT.halting_falsifier}")
print(f"Falsifiers fired (count): {len(RESULT.falsifiers_fired)}")
print(f"Selected policy: {RESULT.selection}")
print(f"Decisions emitted: {len(RESULT.decisions)}")
print(f"Schema column count: {Q6F_SCHEMA_COLUMN_COUNT}")

# %% [markdown]
# ## Per-candidate metric summary (CI-aware proper scoring)

# %%
print(
    f"{'candidate':<60} {'log_loss':>10} {'ll_lo':>9} {'ll_hi':>9} "
    f"{'brier':>10} {'br_lo':>9} {'br_hi':>9} {'auc':>9} {'au_lo':>9} {'au_hi':>9}"
)
for c, m in RESULT.metrics_by_candidate.items():
    if not Q6F_CANDIDATE_INCLUSION[c]:
        print(f"{c:<60} {'n/a':>10} {'':>9} {'':>9} {'':>10} {'':>9} {'':>9} {'':>9} {'':>9} {'':>9}")
        continue
    print(
        f"{c:<60} {m['log_loss']:>10.6f} {m['log_loss_ci_low']:>9.6f} {m['log_loss_ci_high']:>9.6f} "
        f"{m['brier']:>10.6f} {m['brier_ci_low']:>9.6f} {m['brier_ci_high']:>9.6f} "
        f"{m['auc']:>9.6f} {m['auc_ci_low']:>9.6f} {m['auc_ci_high']:>9.6f}"
    )

# %% [markdown]
# ## Q6F_selected_policy verdict (verbatim from CSV)

# %%
SELECTED_ROW = next(d for d in RESULT.decisions if d.decision_id == "Q6F_selected_policy")
print(f"selected_policy: {SELECTED_ROW.selected_policy}")
print(f"survey_verdict: {SELECTED_ROW.survey_verdict}")
print(f"materialization_permission: {SELECTED_ROW.materialization_permission}")
print()
print("Notes:")
print(SELECTED_ROW.notes)

# %% [markdown]
# ## Falsifier roll-call (38 keys)

# %%
print(f"FALSIFIER_PRIORITY_CHAIN ({len(FALSIFIER_PRIORITY_CHAIN)} keys):")
for k in FALSIFIER_PRIORITY_CHAIN:
    status = "fired" if k in RESULT.falsifiers_fired else "did_not_fire"
    print(f"  {k}: {status}")

# %% [markdown]
# ## Decision rule (verbatim; NIT-3 / OQ1 CI-based proper-score binding)

# %%
print(Q6F_SELECTION_DECISION_RULE)

# %% [markdown]
# ## Allowed verdicts (closed set)

# %%
print(f"Q6F_ALLOWED_VERDICTS ({len(Q6F_ALLOWED_VERDICTS)}):")
for v in sorted(Q6F_ALLOWED_VERDICTS):
    print(f"  {v}")

# %% [markdown]
# ## Out-of-scope reminders (forbidden in this PR)
#
# - NO feature materialization. NO Parquet outputs. NO
#   `reconstructed_rating` feature column.
# - NO CROSS-02-01 post-materialization leakage audit.
# - NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or
#   `PHASE_STATUS.yaml` edits.
# - NO `research_log.md` or `ROADMAP.md` edits.
# - NO Step 02_01_04 work. NO Phase 03 baseline modelling.
# - NO Q5 re-adjudication.

# %%
print("Q6F survey completed; artifact pair written; no Step closure; no Phase 03 start.")
print(f"  CSV_PATH = {CSV_PATH}")
print(f"  MD_PATH  = {MD_PATH}")
print(f"  Q6F_DECISION_IDS order: {Q6F_DECISION_IDS}")
