# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
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
# # SC2EGSet Step 02_01_03 — Q6H Final Rating-Path Decision
#
# **Q6H-only Layer-2 final rating-path decision.** This notebook
# exercises the Q6H decision module verbatim: it verifies the 10 parent
# PR SHA pins, builds the 5 decision rows (4 candidates + 1 emergent
# verdict), applies the binding decision rule (A12; R2.5), and writes
# the 38-column CSV + 19-section MD artifact pair under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
#
# **Q6H question:** Given that PR #249's batched-vs-event Glicko-2
# equivalence proof FAILED both bounds while the byte-determinism proof
# PASSED, and the event-by-event reference reproduced PR #247 §11's
# metrics to within 1e-4, what is the FINAL rating-path policy for the
# `reconstructed_rating` family?
#
# **Canonical default (A9(b)):** Branch (ii) reaches the verdict —
# `recommendation_only_event_by_event_glicko2`,
# `materialization_permission =
# recommendation_only_blocked_pending_phase_03_or_later_decision`.
#
# **Falsifier reference:** ≥ 37 falsifier keys are declared in
# `FALSIFIER_PRIORITY_CHAIN` (40 total in 4 groups: parent-SHA pins,
# decision-set / 5-family integrity, decision-rule order-of-operations,
# non-recurrence / non-creep).
#
# **Scope:** Q6H-only. Q5 / Q6F / Q6G remain BINDING and are NOT
# re-adjudicated. After Q6H is merged, NO further Q6X PRs are
# authorised.
#
# **No materialization:** this notebook does NOT materialize any
# feature value, does NOT write any Parquet, does NOT run the
# CROSS-02-01 post-materialization leakage audit, does NOT close
# Step 02_01_03, and does NOT update any status YAML or research_log.

# %% [markdown]
# ## Lineage position — Q6H final decision in the Step 02_01_03 chain
#
# 1. PR #239 — ROADMAP stub.
# 2. PR #240 — Layer-1 scaffold + validator planning PR.
# 3. PR #241 — Layer-2 scaffold + validation module.
# 4. PR #242 — 8-question parent adjudication; Q6 deferred_blocker.
# 5. PR #243 — Q5-only successor; sensitivity_indicator_co_registration.
# 6. PR #244 — Q6 Layer-1 planning PR.
# 7. PR #245 — Q6 Layer-2 successor; deferred_blocker_with_algorithm_survey_required.
# 8. PR #246 — Q6F Layer-1 planning PR.
# 9. PR #247 — Q6F-only algorithm survey; narrow_with_evidence.
# 10. PR #248 — Q6G Layer-1 planning PR.
# 11. PR #249 — Q6G Layer-2 implementation proof; recommendation_only_glicko2.
# 12. PR #250 — Q6H Layer-1 planning PR (this notebook's plan).
# 13. **THIS PR — Q6H Layer-2 final rating-path decision** (this notebook).
#     Persists ONE artifact pair (38-column CSV × 5 rows + ≥19-section MD).

# %%
import hashlib
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.decide_history_rating_path import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    FALSIFIER_PRIORITY_CHAIN,
    Q5_SELECTED_POLICY,
    Q6F_SELECTED_POLICY,
    Q6G_SELECTED_POLICY,
    Q6H_DECISION_CSV_REL,
    Q6H_DECISION_MD_REL,
    Q6H_DECISION_ROWS,
    Q6H_DECISION_SCHEMA,
    Q6H_DECISION_SCHEMA_COLUMN_COUNT,
    Q6H_FIVE_FAMILY_POST_OMIT_SET,
    Q6H_PARENT_SHAS,
    Q6H_PATH_DECISION_RULE,
    Q6H_PATH_DECISION_RULE_SHA256,
    build_q6h_decision_result,
    run_q6h_rating_path_decision,
    write_q6h_decision_artifacts,
)
from rts_predict.games.sc2.datasets.sc2egset import (
    decide_history_rating_path as q6h_mod,
)

print("Module loaded.")
print(f"  schema columns:        {Q6H_DECISION_SCHEMA_COLUMN_COUNT}")
print(f"  decision rows:         {len(Q6H_DECISION_ROWS)}")
print(f"  parent SHA pins:       {len(Q6H_PARENT_SHAS)}")
print(f"  five-family-post-omit: {len(Q6H_FIVE_FAMILY_POST_OMIT_SET)}")
print(f"  falsifier keys:        {len(FALSIFIER_PRIORITY_CHAIN)}")
print(f"  decision-rule SHA256:  {Q6H_PATH_DECISION_RULE_SHA256}")

# %% [markdown]
# ## Parent SHA verification (A1; 10 pinned SHAs)
#
# Verifies the 10 parent PR SHAs against the master file system. Halts
# on the first mismatch with the matching falsifier key.

# %%
repo_root = Path.cwd()
while repo_root != repo_root.parent and not (repo_root / "pyproject.toml").exists():
    repo_root = repo_root.parent
mismatches = q6h_mod._check_parent_pr_shas(repo_root)
print(f"Repo root: {repo_root}")
print(f"Parent SHA mismatches: {len(mismatches)}")
for key, msg in mismatches:
    print(f"  {key}: {msg}")
assert mismatches == [], "Parent SHA mismatch -- halting before artifact write"
print("All 10 parent SHAs verified.")

# %% [markdown]
# ## Q5 / Q6F / Q6G binding preservation
#
# Q6H does NOT re-adjudicate Q5 / Q6F / Q6G. The three binding tokens
# are re-stated here for visibility.

# %%
print("Q5 BINDING preserved:", Q5_SELECTED_POLICY)
print("Q6F BINDING preserved:", Q6F_SELECTED_POLICY)
print("Q6G BINDING preserved:", Q6G_SELECTED_POLICY)

# %% [markdown]
# ## Build decision rows A–D (the 4 candidate verdicts)
#
# Each candidate is constructed by its dedicated builder; emergent
# verdict (Row 5) is built separately from the decision-rule output.

# %%
audit_pr = AUDIT_PR_NUMBER_PLACEHOLDER

row_a = q6h_mod._build_decision_row_a_bind_event_by_event_glicko2(audit_pr)
row_b = q6h_mod._build_decision_row_b_recommendation_only_event_by_event_glicko2(
    audit_pr
)
row_c = q6h_mod._build_decision_row_c_omit_reconstructed_rating_and_unblock_other_five(
    audit_pr
)
row_d = q6h_mod._build_decision_row_d_deferred_blocker(audit_pr)

for r in (row_a, row_b, row_c, row_d):
    print(f"  {r.decision_id}: branch={r.branch_evaluated} verdict={r.verdict}")

# %% [markdown]
# ## Apply the binding decision rule under the canonical default
#
# The Layer-2 dispatch uses the A9(b) canonical default: parent PR #249
# verdict = `recommendation_only_glicko2`, no new separating anchor,
# no thesis-pragmatism override. Branch (ii) is the reached verdict.

# %%
canonical_inputs = q6h_mod._canonical_executor_inputs()
selected, verdict, permission, rationale, branch = q6h_mod._apply_q6h_decision_rule(
    canonical_inputs
)
print(f"Branch reached:           {branch}")
print(f"Selected policy:          {selected}")
print(f"Verdict:                  {verdict}")
print(f"Materialization permission:")
print(f"  {permission}")

# %% [markdown]
# ## Build the complete result (5-row decision set)

# %%
result = build_q6h_decision_result(
    audit_pr=audit_pr,
    csv_path=repo_root / Q6H_DECISION_CSV_REL,
    md_path=repo_root / Q6H_DECISION_MD_REL,
)
print(f"Decisions:           {len(result.decisions)}")
print(f"Selected policy:     {result.selected_policy}")
print(f"Branch evaluated:    {result.branch_evaluated}")
print(f"Materialization permission: {result.materialization_permission}")
print(f"Non-halting falsifiers fired: {result.falsifiers_fired}")

# %% [markdown]
# ## Writer invocation against `tmp_path`
#
# Per `sandbox/README.md` and `data-analysis-lineage.md`, the notebook
# exercises the writer against a sandbox tmp-dir rather than touching
# the canonical artifact path (the canonical artifact is written via
# the `run_q6h_rating_path_decision` entrypoint at PR-commit time, NOT
# from this notebook).

# %%
import tempfile

with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    csv_p = td_path / "q6h.csv"
    md_p = td_path / "q6h.md"
    write_q6h_decision_artifacts(result, csv_p, md_p)
    csv_bytes = csv_p.read_bytes()
    md_bytes = md_p.read_bytes()
    print(f"sandbox CSV bytes:  {len(csv_bytes)}")
    print(f"sandbox MD  bytes:  {len(md_bytes)}")
    print(f"sandbox CSV SHA256: {hashlib.sha256(csv_bytes).hexdigest()}")
    print(f"sandbox MD  SHA256: {hashlib.sha256(md_bytes).hexdigest()}")

# %% [markdown]
# ## Confirm non-materialization
#
# Q6H is an adjudication-class artifact. `materialized_output_paths`
# must be empty on every row; no Parquet may be emitted.

# %%
for d in result.decisions:
    assert d.materialized_output_paths == "", d.decision_id
print("All 5 rows have empty materialized_output_paths (A13).")
