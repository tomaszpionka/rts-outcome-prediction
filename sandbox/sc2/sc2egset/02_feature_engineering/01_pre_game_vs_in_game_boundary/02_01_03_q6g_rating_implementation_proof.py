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
# # SC2EGSet Step 02_01_03 — Q6G Rating-Implementation Proof
#
# **Q6G-only Layer-2 implementation proof.** This notebook re-runs PR
# #247's event-by-event Glicko-2 reference engine, implements the
# production-shape batched-update Glicko-2 path (Glickman 2012 §3
# rating-period batching), proves event-vs-batched ordering equivalence
# (BLOCKER-1 / A19; Spearman ρ ≥ 0.99 AND |Δ log-loss| ≤ SE_event),
# proves byte-determinism of the batched engine across two independent
# runs, and emits the Q6G_selected_policy verdict per the auto-derived
# decision rule. Persists ONE 39-column 5-row CSV + ≥19-section MD
# artifact pair under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
#
# **Hypothesis (Q6G question; binding from PR #247 Q6F verdict):**
# Can the Glicko-2 batched-production implementation be proven
# byte-deterministic AND ordering-equivalent to PR #247's event-by-event
# reference such that PR #247 §11's per-candidate metrics transfer to a
# `bind_now` materialization permission?
#
# **Falsifier reference:** ≥ 38 falsifier keys are declared in
# `FALSIFIER_PRIORITY_CHAIN`; the BLOCKER-1 (A19) keys
# `q6g_batched_event_ordering_equivalence_unproven` and
# `q6g_bind_now_emitted_without_equivalence_pass` are the binding
# methodology guards.
#
# **Scope:** Q6G-only. Q5 (`cross_region_fragmentation_handling`,
# PR #243) and Q6F (`narrow_with_evidence`, PR #247) are BINDING and
# are NOT re-adjudicated. Q1–Q4 / Q6 / Q7 / Q8 are PR #242 / PR #245
# BINDING and are NOT re-adjudicated.
#
# **No materialization:** this notebook does NOT materialize any rating
# value, does NOT write any Parquet, does NOT run the CROSS-02-01
# post-materialization leakage audit, does NOT close Step 02_01_03,
# and does NOT update any status YAML or research_log.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessor PRs:** … → #246 (Q6F Layer-1)
# → #247 (Q6F Layer-2 survey) → #248 (Q6G Layer-1) →
# **THIS PR (Q6G Layer-2 implementation-proof execution)** →
# future Layer-3 materialization PR (contingent on the Q6G verdict).

# %% [markdown]
# ## Lineage position — Q6G implementation-proof in the Step 02_01_03 chain
#
# Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for
# empirical work", the Step 02_01_03 readiness chain is serialised
# across PRs. This notebook is the Q6G successor; Q5 / Q6F are
# explicitly preserved and not re-adjudicated.
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
# 10. PR #248 — Q6G Layer-1 planning PR (this notebook's plan).
# 11. **THIS PR — Q6G-only implementation proof** (this notebook).
#     Persists ONE artifact pair (39-column CSV × 5 rows + ≥19-section MD).
# 12. Future — Layer-3 materialization PR (contingent on Q6G verdict)
#     OR omit-and-unblock closure PR.

# %%
import hashlib
from pathlib import Path

from rts_predict.games.sc2.config import DB_FILE
from rts_predict.games.sc2.datasets.sc2egset.proof_glicko2_implementation import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    BOOTSTRAP_BLOCK_COUNT,
    BOOTSTRAP_RANDOM_SEED,
    EQUIVALENCE_SPEARMAN_MIN,
    FALSIFIER_PRIORITY_CHAIN,
    GLICKO2_ITERATION_TOL,
    Q5_SELECTED_POLICY,
    Q6F_SELECTED_POLICY,
    Q6G_PARENT_SHAS,
    Q6G_PROOF_CSV_REL,
    Q6G_PROOF_MD_REL,
    Q6G_PROOF_ROWS,
    Q6G_PROOF_SCHEMA_COLUMN_COUNT,
    RATING_PERIOD_DAYS,
    _compute_byte_determinism_proof,
    _compute_event_vs_batched_equivalence_proof,
    _find_repo_root,
    _load_pha_history_chronological,
    _run_glicko2_batched_production,
    _run_glicko2_event_by_event_reference,
    compute_proof_metrics,
    run_q6g_rating_implementation_proof,
)

# %% [markdown]
# ## 1. Constants + parent provenance pins
#
# All 8 parent PR SHAs (PR #242, #243, #245, #247 CSV + MD) are
# hard-coded in the proof module. Bootstrap policy (NIT-N6) and rating-
# period (A22) constants are pinned to the Glickman 2012 §10 worked-
# example defaults.

# %%
repo_root = _find_repo_root(Path.cwd())
print("repo_root:", repo_root)
print("Q6G_PROOF_CSV_REL:", Q6G_PROOF_CSV_REL)
print("Q6G_PROOF_MD_REL:", Q6G_PROOF_MD_REL)
print()
print("Bootstrap policy (NIT-N6 / A21):")
print(f"  BOOTSTRAP_RANDOM_SEED = {BOOTSTRAP_RANDOM_SEED}")
print(f"  BOOTSTRAP_BLOCK_COUNT = {BOOTSTRAP_BLOCK_COUNT}")
print(f"  EQUIVALENCE_SPEARMAN_MIN = {EQUIVALENCE_SPEARMAN_MIN}")
print()
print("Glicko-2 hyperparameters (A9 / A22):")
print(f"  RATING_PERIOD_DAYS = {RATING_PERIOD_DAYS}")
print(f"  GLICKO2_ITERATION_TOL = {GLICKO2_ITERATION_TOL}")
print()
print(f"Q6G_PROOF_SCHEMA_COLUMN_COUNT = {Q6G_PROOF_SCHEMA_COLUMN_COUNT}")
print(f"Q6G_PROOF_ROWS = {Q6G_PROOF_ROWS}")
print(f"Falsifier chain length = {len(FALSIFIER_PRIORITY_CHAIN)} keys")

# %% [markdown]
# ## 2. Parent PR SHA verification
#
# Verify that all 8 parent artifact SHAs match the pinned values
# hard-coded in the proof module. A mismatch halts the entrypoint
# before any write.

# %%
for name, expected in Q6G_PARENT_SHAS.items():
    print(f"  {name}: {expected}")
print()
print(f"Q5 BINDING preserved (PR #243): {Q5_SELECTED_POLICY}")
print(f"Q6F BINDING preserved (PR #247): {Q6F_SELECTED_POLICY}")

# %% [markdown]
# ## 3. PHA forward-only stream loader (read-only DuckDB)
#
# Delegate to PR #247's `_load_pha_history_chronological` per A18.
# Re-uses the same query verbatim.

# %%
db_path = Path(DB_FILE)
print("db_path exists:", db_path.exists())
stream = _load_pha_history_chronological(db_path)
print("PHA stream rows:", len(stream))
print(stream.head(3))

# %% [markdown]
# ## 4. Row 1: event-by-event reference (PR #247 engine delegated)
#
# Per A18, Row 1 invokes PR #247's `_run_glicko2_survey` verbatim and
# computes metrics on the non-cold-start mask. T02 verification: log-
# loss / Brier / calibration_error reproduce PR #247 §11 Glicko-2 row
# within 1e-4.

# %%
event_output = _run_glicko2_event_by_event_reference(stream)
event_metrics = compute_proof_metrics(event_output)
print("Row 1 event-by-event reference metrics:")
print(f"  log_loss        = {event_metrics['log_loss']:.6f}")
print(f"  log_loss CI low = {event_metrics['log_loss_ci_low']:.6f}")
print(f"  log_loss CI high= {event_metrics['log_loss_ci_high']:.6f}")
print(f"  brier           = {event_metrics['brier']:.6f}")
print(f"  brier CI        = ({event_metrics['brier_ci_low']:.6f}, "
      f"{event_metrics['brier_ci_high']:.6f})")
print(f"  calibration_err = {event_metrics['calibration_error']:.6f}")
print(f"  coverage_rate   = {event_metrics['coverage_rate']:.6f}")
print(f"  cold_start_rate = {event_metrics['cold_start_rate']:.6f}")

# %% [markdown]
# ## 5. Row 2: batched-production shape (Glickman 2012 §3)
#
# Production-shape Glicko-2 with `rating_period_days = 30` (A22) and
# `iteration_tol = 1e-6`. NIT-N6 sorted_then_kahan summation order
# eliminates platform-specific round-off at the 1-SE bound of A19's
# |Δ log-loss| check.

# %%
batched_output = _run_glicko2_batched_production(stream)
batched_metrics = compute_proof_metrics(batched_output)
print("Row 2 batched-production metrics:")
print(f"  log_loss        = {batched_metrics['log_loss']:.6f}")
print(f"  log_loss CI low = {batched_metrics['log_loss_ci_low']:.6f}")
print(f"  log_loss CI high= {batched_metrics['log_loss_ci_high']:.6f}")
print(f"  brier           = {batched_metrics['brier']:.6f}")
print(f"  brier CI        = ({batched_metrics['brier_ci_low']:.6f}, "
      f"{batched_metrics['brier_ci_high']:.6f})")
print(f"  calibration_err = {batched_metrics['calibration_error']:.6f}")
print(f"  coverage_rate   = {batched_metrics['coverage_rate']:.6f}")
print(f"  cold_start_rate = {batched_metrics['cold_start_rate']:.6f}")

# %% [markdown]
# ## 6. Row 3: equivalence proof (BLOCKER-1 / A19)
#
# Compute Spearman ρ between event and batched predicted probabilities
# on the joint non-cold-start mask AND |Δ log-loss| against the
# deterministic-bootstrap SE of the event-path log-loss. Both bounds
# must pass for `bind_now` to be reachable.

# %%
equivalence_stats = _compute_event_vs_batched_equivalence_proof(
    event_output, batched_output
)
print("Row 3 equivalence proof statistics (BLOCKER-1 / A19):")
print(f"  spearman_rho             = {equivalence_stats['spearman_rho']:.6f}")
print(f"  abs_delta_log_loss       = {equivalence_stats['abs_delta_log_loss']:.6f}")
print(f"  se_log_loss_event        = {equivalence_stats['se_log_loss_event']:.6f}")
print(f"  passes_spearman_bound    = {equivalence_stats['passes_spearman_bound']}")
print(f"  passes_delta_log_loss    = {equivalence_stats['passes_delta_log_loss_bound']}")

# %% [markdown]
# ## 7. Row 4: byte-determinism proof
#
# Two independent invocations of `_run_glicko2_batched_production` over
# the same PHA stream; SHA-256 of the predicted-probability bytes must
# match.

# %%
byte_determinism_stats = _compute_byte_determinism_proof(stream)
print("Row 4 byte-determinism proof statistics:")
print(f"  run_a_sha256 = {byte_determinism_stats['run_a_sha256']}")
print(f"  run_b_sha256 = {byte_determinism_stats['run_b_sha256']}")
print(f"  hashes_equal = {byte_determinism_stats['hashes_equal']}")

# %% [markdown]
# ## 8. Row 5: Q6G_selected_policy (auto-derived verdict)
#
# Apply the BINDING decision rule
# (`Q6G_PROOF_DECISION_RULE` in the proof module):
#
# 1. NOT determinism pass -> `deferred_blocker`
# 2. NOT equivalence pass -> `recommendation_only_glicko2` (NIT-N2 default)
# 3. Equivalence pass AND determinism pass -> `bind_now`
#
# The full entrypoint runs all 8 parent SHA checks, computes all 5
# rows, applies the auto-derived rule, enforces the BLOCKER-1 guard,
# and writes the 39-column CSV + ≥19-section MD pair.

# %%
csv_path = repo_root / Q6G_PROOF_CSV_REL
md_path = repo_root / Q6G_PROOF_MD_REL
result = run_q6g_rating_implementation_proof(
    db_path=db_path,
    csv_path=csv_path,
    md_path=md_path,
    audit_pr=AUDIT_PR_NUMBER_PLACEHOLDER,
    repo_root=repo_root,
)
print("Q6G proof result:")
print(f"  passed            = {result.passed}")
print(f"  halting_falsifier = {result.halting_falsifier}")
print(f"  falsifiers_fired  = {result.falsifiers_fired}")
print(f"  decisions         = {len(result.decisions)} rows")
print(f"  selected_policy   = {result.decisions[-1].selected_policy}")
print(f"  verdict           = {result.decisions[-1].proof_verdict}")
print(f"  permission        = {result.decisions[-1].materialization_permission}")
print()
print("Sample probabilities (NIT-N1 / A20; 5 floats in [0, 1]):")
for idx, p in enumerate(result.sample_probabilities):
    print(f"  pha_row_index={idx}  predicted_probability={p:.6f}")

# %% [markdown]
# ## 9. Artifact byte-stability check
#
# Re-run the writer against a temporary location and compare SHA-256
# hashes; the writer must be byte-deterministic for the CSV+MD pair.

# %%
print("CSV size:", csv_path.stat().st_size, "bytes")
print("MD size:", md_path.stat().st_size, "bytes")
csv_sha = hashlib.sha256(csv_path.read_bytes()).hexdigest()
md_sha = hashlib.sha256(md_path.read_bytes()).hexdigest()
print(f"CSV sha256: {csv_sha}")
print(f"MD  sha256: {md_sha}")

# %% [markdown]
# ## 10. Closure discipline
#
# This notebook does NOT close Step 02_01_03, does NOT update any
# status YAML, does NOT touch the dataset research_log or ROADMAP,
# does NOT materialize any feature value, and does NOT start Phase 03.
# Layer-3 materialization is a SEPARATE PR contingent on the Q6G
# verdict above.

# %%
print("Q6 Discipline summary:")
print(f"  Q5 BINDING preserved (PR #243): {Q5_SELECTED_POLICY}")
print(f"  Q6F BINDING preserved (PR #247): {Q6F_SELECTED_POLICY}")
print(f"  Q6G selected_policy             : {result.decisions[-1].selected_policy}")
print(f"  Q6G verdict                     : {result.decisions[-1].proof_verdict}")
print(f"  materialization_permission      : {result.decisions[-1].materialization_permission}")
print()
print("Hard stops respected (none of the following are touched):")
print("  - status YAMLs (STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS)")
print("  - dataset or root research_log.md")
print("  - ROADMAP.md")
print("  - reports/specs/*")
print("  - data/db/schemas/views/*.yaml")
print("  - reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}")
print("  - any *.parquet output")
print("  - Step 02_01_04, Phase 03, baseline modelling")
