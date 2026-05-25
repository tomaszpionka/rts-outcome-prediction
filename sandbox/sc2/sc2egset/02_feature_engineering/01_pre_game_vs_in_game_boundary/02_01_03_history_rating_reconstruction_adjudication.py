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
# # SC2EGSet Step 02_01_03 — Q6 Rating-Reconstruction Successor Adjudication
#
# **Q6-ONLY SUCCESSOR ADJUDICATION (Layer-2 execution).** This notebook
# upgrades the PR #242 Q6 `deferred_blocker` row by recording a
# binding / recommendation / re-deferral verdict over a complete
# `Q6_RATING_POLICY_CANDIDATES` set (omit / rolling-baseline / Elo /
# Glicko-or-Glicko-2 / TrueSkill-or-TrueSkill-like /
# deferred-with-survey) and persists ONE artifact pair (31-column CSV
# x 8 rows + multi-section MD) under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
#
# **Hypothesis (Q6 question, verbatim binding from PR #242 §2 row Q6):**
# Can `reconstructed_rating` (the `history_enriched_pre_game` family
# bound by §6.2 row 4 of `reports/specs/02_02_feature_engineering_plan.md`)
# be materialized safely now, and if yes, with which rating-model family?
#
# **Falsifier reference:** 45 falsifier helpers are declared in the
# adjudicator module (`adjudicate_history_rating_reconstruction.py`) and
# enumerated in `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN`.
# All 45 keys are exercised by the entrypoint before any write; a single
# fired falsifier halts the notebook before the artifact pair is written.
# The complete roll-call appears in the produced MD §15.
#
# **Scope:** Q6-only. Q5 (`cross_region_fragmentation_handling`) was
# resolved by PR #243 with
# `Q5_selected_policy=sensitivity_indicator_co_registration` and is NOT
# re-adjudicated here. The `q6_q5_re_adjudication_drift` falsifier halts
# the entrypoint if any Q6 row carries a Q5 verdict-bearing token.
#
# **No materialization:** this notebook does NOT materialize any rating
# value, does NOT write any Parquet, does NOT run the
# CROSS-02-01-v1.0.1 post-materialization leakage audit, does NOT close
# Step 02_01_03, and does NOT append to any status YAML or research_log.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessor PRs:** #239 (ROADMAP stub) →
# #240 (Layer-1 scaffold plan) → #241 (Layer-2 scaffold + validator) →
# #242 (8-question parent adjudication) → #243 (Q5 successor) →
# **THIS PR (Q6 successor adjudication)** → future materialization PRs.

# %% [markdown]
# ## Lineage position — Q6-only rating-reconstruction successor in the Step 02_01_03 chain
#
# Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for
# empirical work", the Step 02_01_03 readiness chain is serialised across
# PRs. This notebook is the Q6 successor; Q5 is explicitly out of scope.
#
# 1. PR #239 — ROADMAP stub block inserted.
# 2. PR #240 — Layer-1 scaffold + validator planning PR.
# 3. PR #241 — Layer-2 SCAFFOLD + ONE validation module
#    (`validate_history_enriched_pre_game_materialization.py` + mirrored
#    tests + jupytext scaffold). The SHA-256 of the PR #241 validator
#    module is re-asserted on every Q6 row of this successor CSV.
# 4. PR #242 — 8-question parent adjudication. Q6 was bound
#    `deferred_blocker` pending rating-family empirical evaluation.
# 5. PR #243 — Q5-only successor adjudication
#    (`02_01_03_history_cross_region_adjudication.{csv,md}`).
#    Q6 remained `deferred_blocker`.
# 6. **THIS PR — Q6-only successor adjudication** (this notebook).
#    Persists ONE artifact pair (31-column CSV x 8 rows + multi-section
#    MD). Q6 selected verdict = `deferred_blocker` (Q6F selected);
#    materialization remains BLOCKED pending algorithm-survey PR.
# 7. Future — algorithm-survey Step (if Q6F is overturned, binds a
#    specific rating-model family).
# 8. Future — Tranche-2 materialization-execution Layer-1 plan PR.
# 9. Future — Tranche-2 materialization-execution Layer-2 PR.
# 10. Future — Post-materialization CROSS-02-01-v1.0.1 audit PR.
# 11. Future — Step 02_01_03 closure PR.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction import (  # noqa: E501
    ALLOWED_COMPLEXITY_DEPLOYABILITY,
    ALLOWED_LEAKAGE_RISK,
    ALLOWED_MATERIALIZATION_PERMISSION,
    ALLOWED_Q6_BINDING_LEVELS,
    ALLOWED_Q6_VERDICTS,
    ALLOWED_RATING_EVIDENCE_LEVELS,
    CROSS_02_02_SPEC_REL,
    DATASET_RESEARCH_LOG_REL,
    EXCLUDED_METHODS_CONSIDERED,
    EXPECTED_MMR_MISSING_DENSITY_MFC_PCT,
    EXPECTED_MMR_MISSING_DENSITY_PHA_PCT,
    EXPECTED_PR241_VALIDATOR_SHA256,
    EXPECTED_PR242_CSV_SHA256,
    EXPECTED_PR242_MD_SHA256,
    EXPECTED_PR243_CSV_SHA256,
    EXPECTED_PR243_MD_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    FEATURE_FAMILY_REGISTRY_CSV_REL,
    HELPER_TO_FALSIFIER_KEY,
    HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS,
    MATCHES_FLAT_CLEAN_YAML_REL,
    MATCHES_HISTORY_MINIMAL_YAML_REL,
    NON_RATING_HISTORY_FAMILIES,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    PARENT_PR243_CSV_REL,
    PARENT_PR243_MD_REL,
    PR241_VALIDATOR_MODULE_REL,
    Q5_SELECTED_POLICY,
    Q5_SELECTED_POLICY_VERDICT,
    Q6_ADJUDICATION_SCHEMA,
    Q6_DECISION_IDS,
    Q6_RATING_POLICY_CANDIDATES,
    PLAYER_HISTORY_ALL_YAML_REL,
    RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL,
    RATING_RECONSTRUCTION_ADJUDICATION_MD_REL,
    RAW_MMR_HYBRID_REJECTION_TOKEN,
    STRICT_LT_HISTORY_FILTER,
    run_rating_reconstruction_adjudication,
)

# %% [markdown]
# ## Bound constants imported from the Q6 adjudicator module (no inline redefinition)
#
# - `EXPECTED_PR242_CSV_SHA256` / `EXPECTED_PR242_MD_SHA256` — NIT-B
#   binding SHAs for the PR #242 parent artifact pair; mismatch halts.
# - `EXPECTED_PR243_CSV_SHA256` / `EXPECTED_PR243_MD_SHA256` — NIT-B
#   binding SHAs for the PR #243 Q5-successor artifact pair; mismatch
#   halts.
# - `EXPECTED_PR241_VALIDATOR_SHA256` — the NIT-B binding SHA re-asserted
#   on every Q6 row.
# - `Q6_DECISION_IDS` — the canonical 8-row ordered tuple (Q6A / Q6B /
#   Q6C / Q6D / Q6E / Q6F / Q6_selected_policy /
#   Q6_per_family_impact_summary).
# - `Q6_RATING_POLICY_CANDIDATES` — the 6 closed enumerated candidate
#   policies.
# - `EXCLUDED_METHODS_CONSIDERED` — 3 N-1 excluded methods
#   (aligulac_style_btl / bradley_terry / neural_btl).
# - `RAW_MMR_HYBRID_REJECTION_TOKEN` — N-2 binding rejection token.
# - `STRICT_LT_HISTORY_FILTER` — verbatim forward-only filter inherited
#   from PR #242 Q3 BIND_NOW.
# - `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN` — B4:
#   both sets contain exactly 45 entries and are value-equal at import.
# - `RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL` /
#   `RATING_RECONSTRUCTION_ADJUDICATION_MD_REL` — canonical Q6 artifact
#   output paths (relative to repo root per I10).
#
# ### Per-candidate hypothesis structure (per data-analysis-lineage.md)
#
# **Q6A omit_reconstructed_rating:**
# - Assumption: dropping the reconstructed_rating family preserves
#   G-CS-4 trivially; 5 non-rating families remain materializable.
# - Measurement claim: `is_mmr_missing` flag co-registration is the
#   only skill-signal proxy; no cross-player comparability.
# - Sanity check: `materialization_permission =
#   "permitted_for_other_5_families_without_reconstructed_rating"`.
# - Falsifier: `q6_forward_only_constraint_missing_for_non_omit_candidate`
#   does NOT apply (omit row is exempt).
# - Expected artifact: Q6A row in the 8-row CSV with
#   `verdict="deferred_recommendation"`.
# - Lineage source: CROSS-02-02 §6.2 row 4; research_log lines 106/1135.
# - Downstream decision: if Q6A is selected, the 5 non-rating families
#   can materialize; `reconstructed_rating` slot is permanently empty.
#
# **Q6B rolling_win_rate_or_bayesian_smoothed_baseline:**
# - Assumption: Bayesian-smoothed forward-only win rate is a valid
#   rating proxy with no opponent-strength information.
# - Measurement claim: STRICT_LT_HISTORY_FILTER + forward-only per-pair
#   update satisfies G-L-4; `is_first_match` flag satisfies G-CS-4.
# - Sanity check: `leakage_risk = "low_if_forward_only_enforced"`.
# - Falsifier: `q6_hyperparameter_policy_missing_for_non_omit_candidate`
#   fires if alpha_prior / beta_prior are hard-coded rather than deferred.
# - Expected artifact: Q6B row with `verdict="deferred_recommendation"`.
# - Lineage source: CROSS-02-02 §6.2 row 1 (implicit in focal_player
#   history rolling features).
# - Downstream decision: if Q6B selected, algorithm-implementation-proof
#   PR must pin alpha_prior, beta_prior, window_length.
#
# **Q6C elo (Elo 1978):**
# - Assumption: constant-K Elo forward-only update is feasible over PHA;
#   no inactivity decay is acceptable.
# - Measurement claim: STRICT_LT_HISTORY_FILTER chronological ordering
#   by `TRY_CAST(ph.details_timeUTC AS TIMESTAMP)` with replay_id
#   tiebreaker; evidence level = `in_repo_plus_citation`.
# - Sanity check: `CITATION_ELO_1978` appears in evidence_paths.
# - Falsifier: `q6_external_citation_missing_when_non_omit_selected`
#   fires if Q6C is selected but Elo 1978 citation is absent.
# - Expected artifact: Q6C row with `verdict="deferred_recommendation"`.
# - Lineage source: Elo (1978); CROSS-02-02 §6.2 row 4.
# - Downstream decision: K_factor and initial_rating deferred to OQ2.
#
# **Q6D glicko_or_glicko_2 (Glickman 1999, 2012):**
# - Assumption: rating deviation (RD) that grows with inactivity matches
#   the dataset's tournament rhythm; spec-favoured path per §6.2 row 4.
# - Measurement claim: per-rating-period batched update internally;
#   forward-only across rating periods; evidence level =
#   `in_repo_plus_citation`.
# - Sanity check: `leakage_risk = "medium_if_forward_only_enforced"`
#   (within-period micro-leakage surface honestly recorded).
# - Falsifier: `q6_external_citation_missing_when_non_omit_selected`
#   fires if Q6D selected without Glickman 1999 / 2012 citations.
# - Expected artifact: Q6D row with `verdict="deferred_recommendation"`.
# - Lineage source: Glickman (1999, 2012); CROSS-02-02 §6.2 row 4.
# - Downstream decision: mu_prior, RD_prior, sigma_prior, tau,
#   rating_period_days deferred to OQ2.
#
# **Q6E trueskill_or_trueskill_like (Herbrich, Minka, Graepel 2006):**
# - Assumption: TrueSkill degenerates to Elo-like for 1v1 decisive PHA
#   scope; marginal expressiveness gain may not justify implementation
#   cost.
# - Measurement claim: Gaussian message-passing posterior update;
#   `complexity_deployability_score = "high"`.
# - Sanity check: `CITATION_HERBRICH_MINKA_GRAEPEL_2006` in evidence_paths.
# - Falsifier: `q6_hyperparameter_policy_missing_for_non_omit_candidate`
#   fires if beta / tau / draw_margin are hard-coded.
# - Expected artifact: Q6E row with `verdict="deferred_recommendation"`.
# - Lineage source: Herbrich, Minka, Graepel (2006).
# - Downstream decision: mu_prior, sigma_prior, beta, tau, draw_margin
#   deferred to OQ2.
#
# **Q6F deferred_blocker_with_algorithm_survey_required:**
# - Assumption: comparative back-testing AUC / log-loss evidence does NOT
#   exist in any prior artifact; binding a single family without this
#   evidence would violate Invariant I7.
# - Measurement claim: Q6F is a legitimate Q6 verdict per N-10, NOT a
#   planning failure; triggers a dedicated algorithm-survey Step.
# - Sanity check: `materialization_permission =
#   "blocked_pending_algorithm_survey_pr"`.
# - Falsifier: `q6_materialization_permission_drift` fires if
#   `verdict="deferred_blocker"` but `materialization_permission` is not
#   `"blocked_pending_algorithm_survey_pr"`.
# - Expected artifact: Q6F row with `verdict="deferred_blocker"`;
#   Q6_selected_policy row with `selected_policy=
#   "deferred_blocker_with_algorithm_survey_required"`.
# - Lineage source: planning Assumptions 11-17; research_log lines 106,
#   1135, 1546; CROSS-02-02 §6.2 row 4.
# - Downstream decision: materialization BLOCKED; algorithm-survey Step
#   must back-test B/C/D/E candidates before Q6 can be upgraded.

# %%
# Resolve repo root deterministically. `__file__` is set when this module is
# executed as a Python script (e.g., via `python -m`); inside a live Jupyter
# kernel `__file__` is not defined, so fall back to walking up from the
# current working directory. nbconvert sets CWD to the directory containing
# the notebook, so the fallback walks up looking for the repo
# `pyproject.toml` sentinel for resilience.
try:
    _NOTEBOOK_DIR = Path(__file__).resolve().parent
except NameError:
    _NOTEBOOK_DIR = Path.cwd().resolve()
_candidate = _NOTEBOOK_DIR
while _candidate != _candidate.parent and not (_candidate / "pyproject.toml").exists():
    _candidate = _candidate.parent
assert (_candidate / "pyproject.toml").exists(), (
    f"could not locate repo root from {_NOTEBOOK_DIR}"
)
REPO_ROOT = _candidate

DUCKDB_PATH = REPO_ROOT / "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
PARENT_PR242_CSV_PATH = REPO_ROOT / PARENT_PR242_CSV_REL
PARENT_PR242_MD_PATH = REPO_ROOT / PARENT_PR242_MD_REL
PARENT_PR243_CSV_PATH = REPO_ROOT / PARENT_PR243_CSV_REL
PARENT_PR243_MD_PATH = REPO_ROOT / PARENT_PR243_MD_REL
PR241_VALIDATOR_MODULE_PATH = REPO_ROOT / PR241_VALIDATOR_MODULE_REL
CROSS_02_02_SPEC_PATH = REPO_ROOT / CROSS_02_02_SPEC_REL
FEATURE_FAMILY_REGISTRY_CSV_PATH = REPO_ROOT / FEATURE_FAMILY_REGISTRY_CSV_REL
DATASET_RESEARCH_LOG_PATH = REPO_ROOT / DATASET_RESEARCH_LOG_REL
PLAYER_HISTORY_ALL_YAML_PATH = REPO_ROOT / PLAYER_HISTORY_ALL_YAML_REL
MATCHES_FLAT_CLEAN_YAML_PATH = REPO_ROOT / MATCHES_FLAT_CLEAN_YAML_REL
MATCHES_HISTORY_MINIMAL_YAML_PATH = REPO_ROOT / MATCHES_HISTORY_MINIMAL_YAML_REL
CSV_OUT_PATH = REPO_ROOT / RATING_RECONSTRUCTION_ADJUDICATION_CSV_REL
MD_OUT_PATH = REPO_ROOT / RATING_RECONSTRUCTION_ADJUDICATION_MD_REL
AUDIT_PR_LABEL = "PR #245"
AUDIT_DATE = "2026-05-25"

print("REPO_ROOT:", REPO_ROOT)
print("Q6_DECISION_IDS:", Q6_DECISION_IDS)
print("Q6_RATING_POLICY_CANDIDATES:", Q6_RATING_POLICY_CANDIDATES)
print("EXCLUDED_METHODS_CONSIDERED:", EXCLUDED_METHODS_CONSIDERED)
print("RAW_MMR_HYBRID_REJECTION_TOKEN:", RAW_MMR_HYBRID_REJECTION_TOKEN)
print("STRICT_LT_HISTORY_FILTER:", STRICT_LT_HISTORY_FILTER)
print("Q5_SELECTED_POLICY:", Q5_SELECTED_POLICY, "verdict:", Q5_SELECTED_POLICY_VERDICT)
print("HELPER_TO_FALSIFIER_KEY entries:", len(HELPER_TO_FALSIFIER_KEY))
print("FALSIFIER_PRIORITY_CHAIN entries:", len(FALSIFIER_PRIORITY_CHAIN))
print("Q6_ADJUDICATION_SCHEMA columns:", len(Q6_ADJUDICATION_SCHEMA))
print("HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS:", HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS)
print("NON_RATING_HISTORY_FAMILIES:", NON_RATING_HISTORY_FAMILIES)
print("MMR missing MFC:", EXPECTED_MMR_MISSING_DENSITY_MFC_PCT, "%")
print("MMR missing PHA:", EXPECTED_MMR_MISSING_DENSITY_PHA_PCT, "%")
print("PR #242 CSV SHA:", EXPECTED_PR242_CSV_SHA256)
print("PR #242 MD SHA:", EXPECTED_PR242_MD_SHA256)
print("PR #243 CSV SHA:", EXPECTED_PR243_CSV_SHA256)
print("PR #243 MD SHA:", EXPECTED_PR243_MD_SHA256)
print("PR #241 validator SHA:", EXPECTED_PR241_VALIDATOR_SHA256)
print("ALLOWED_Q6_VERDICTS:", sorted(ALLOWED_Q6_VERDICTS))
print("ALLOWED_Q6_BINDING_LEVELS:", sorted(ALLOWED_Q6_BINDING_LEVELS))
print("ALLOWED_RATING_EVIDENCE_LEVELS:", sorted(ALLOWED_RATING_EVIDENCE_LEVELS))
print("ALLOWED_COMPLEXITY_DEPLOYABILITY:", sorted(ALLOWED_COMPLEXITY_DEPLOYABILITY))
print("ALLOWED_LEAKAGE_RISK:", sorted(ALLOWED_LEAKAGE_RISK))
print("ALLOWED_MATERIALIZATION_PERMISSION:", sorted(ALLOWED_MATERIALIZATION_PERMISSION))
print("CSV_OUT_PATH:", CSV_OUT_PATH)
print("MD_OUT_PATH:", MD_OUT_PATH)

# %%
result = run_rating_reconstruction_adjudication(
    duckdb_path=DUCKDB_PATH,
    parent_pr242_csv_path=PARENT_PR242_CSV_PATH,
    parent_pr242_md_path=PARENT_PR242_MD_PATH,
    parent_pr243_csv_path=PARENT_PR243_CSV_PATH,
    parent_pr243_md_path=PARENT_PR243_MD_PATH,
    pr241_validator_module_path=PR241_VALIDATOR_MODULE_PATH,
    cross_02_02_spec_path=CROSS_02_02_SPEC_PATH,
    feature_family_registry_csv_path=FEATURE_FAMILY_REGISTRY_CSV_PATH,
    dataset_research_log_path=DATASET_RESEARCH_LOG_PATH,
    player_history_all_yaml_path=PLAYER_HISTORY_ALL_YAML_PATH,
    matches_flat_clean_yaml_path=MATCHES_FLAT_CLEAN_YAML_PATH,
    matches_history_minimal_yaml_path=MATCHES_HISTORY_MINIMAL_YAML_PATH,
    csv_out_path=CSV_OUT_PATH,
    md_out_path=MD_OUT_PATH,
    audit_pr=AUDIT_PR_LABEL,
    audit_date=AUDIT_DATE,
    skip_probes=False,
)

print("passed:", result.passed)
print("decisions:", len(result.decisions))
print("halting_falsifier:", result.halting_falsifier)
print("falsifiers_fired:", result.falsifiers_fired)
print("csv_path:", result.csv_path)
print("md_path:", result.md_path)
print("provenance_git_sha:", result.provenance_git_sha)
print("probe keys:", list(result.probes.keys()))

assert result.passed is True, (
    f"Adjudication FAILED: halting_falsifier={result.halting_falsifier!r}, "
    f"all fired={result.falsifiers_fired}"
)
assert result.halting_falsifier is None
assert len(result.decisions) == 8
assert result.decisions[6].decision_id == "Q6_selected_policy"
assert result.decisions[7].decision_id == "Q6_per_family_impact_summary"

print()
print("--- Decision summary ---")
for d in result.decisions:
    print(
        f"  {d.decision_id:<52} verdict={d.verdict!r:<24} "
        f"perm={d.materialization_permission!r}"
    )

# %% [markdown]
# ## SHA determinism check and artifact verification
#
# The entrypoint writes the CSV+MD byte-deterministically. Verify that the
# SHA-256 of the written artifacts matches the committed artifacts (confirming
# no drift has occurred since the T01-T06 execution pass).

# %%
import hashlib


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


EXPECTED_CSV_SHA = "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"
EXPECTED_MD_SHA = "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"

observed_csv_sha = _sha256(CSV_OUT_PATH)
observed_md_sha = _sha256(MD_OUT_PATH)

print("CSV SHA (observed):", observed_csv_sha)
print("CSV SHA (expected):", EXPECTED_CSV_SHA)
print("CSV SHA match:     ", observed_csv_sha == EXPECTED_CSV_SHA)
print()
print("MD  SHA (observed):", observed_md_sha)
print("MD  SHA (expected):", EXPECTED_MD_SHA)
print("MD  SHA match:     ", observed_md_sha == EXPECTED_MD_SHA)

assert observed_csv_sha == EXPECTED_CSV_SHA, (
    f"CSV SHA mismatch: observed={observed_csv_sha!r} expected={EXPECTED_CSV_SHA!r}\n"
    "The adjudicator is not byte-deterministic or a source file changed."
)
assert observed_md_sha == EXPECTED_MD_SHA, (
    f"MD  SHA mismatch: observed={observed_md_sha!r} expected={EXPECTED_MD_SHA!r}\n"
    "The adjudicator is not byte-deterministic or a source file changed."
)
print()
print("Artifact determinism confirmed: both SHAs match committed artifacts.")

# %% [markdown]
# ## Closing — Q6 successor artifact persisted; Q5 deferral preserved; materialization blocked
#
# **Persisted (this PR):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv`
#   (31 columns x 8 rows + 1 header; `materialized_output_paths` is `""`
#   on every row; `audit_pr` is populated; CSV SHA-256 =
#   `703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0`).
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md`
#   (18 §sections; MD SHA-256 =
#   `7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419`).
#
# **Q6_selected_policy = `deferred_blocker_with_algorithm_survey_required`**
# (verdict = `deferred_blocker`). This is a legitimate Q6 verdict per
# planning N-10, NOT a planning failure — it preserves Invariant I7
# (no magic numbers for K, prior, RD, sigma, tau, rating_period) when
# comparative empirical evidence is genuinely insufficient.
#
# **Q5 binding from PR #243 (`Q5_selected_policy=sensitivity_indicator_co_registration`,
# verdict=`narrow_with_evidence`) is preserved verbatim and NOT
# re-adjudicated by this notebook.** The `q6_q5_re_adjudication_drift`
# falsifier confirmed no Q5 token appeared in any verdict-bearing field.
#
# **Materialization permission: `blocked_pending_algorithm_survey_pr`.**
# The future Layer-3 materialization PR for the 6 history-enriched
# pre_game families must NOT proceed until the algorithm-survey Step
# resolves the Q6F deferral with a binding selection.
#
# **Explicitly DEFERRED to successor PRs (NOT this PR):**
# - **Algorithm survey Step** — back-tests Q6B/C/D/E candidates over the
#   unrated regime; selects and binds a single rating-model family.
# - **Algorithm-implementation-proof PR (OQ2)** — pins K_factor /
#   rating_period / prior / RD / sigma / tau constants for the selected
#   family.
# - **Materialization SQL** (the tranche-2 `_MATERIALIZATION_QUERY`)
#   — deferred to the future Layer-1 plan PR.
# - **First Parquet artifact** for the 6 history-enriched families
#   — deferred to the future Layer-2 materialization-execution PR.
# - **Post-materialization CROSS-02-01-v1.0.1 audit JSON+MD**
#   — deferred to the future post-mat audit PR.
# - **Step 02_01_03 closure** (the `02_01_03: complete` row in
#   `STEP_STATUS.yaml` + `research_log` closure entry) — deferred to the
#   future closure PR.
#
# This notebook does NOT update any `STEP_STATUS.yaml` /
# `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`. It does NOT
# append any `research_log.md` entry (dataset or root). It does NOT edit
# `ROADMAP.md`. It does NOT patch any spec or cleaning-layer YAML.
