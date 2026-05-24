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
# # Step 02_01_03 — Q5 cross-region retention SUCCESSOR ADJUDICATION: sc2egset
#
# **Q5-ONLY SUCCESSOR ADJUDICATION (PR #243 Layer-2 execution).** This
# notebook upgrades the PR #242 Q5 `deferred_blocker` row to one of the three
# CROSS-02-02 §6.2 row-5 options using read-only DuckDB retention-impact
# probes against `player_history_all.is_cross_region_fragmented`, and persists
# ONE artifact pair (30-column CSV × 5 rows + multi-section MD) under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
# No `def` / `class` / `lambda` appears in any cell; every probe, falsifier,
# and writer lives inside the adjudicator module and is imported here.
#
# **Q6 rating reconstruction REMAINS `deferred_blocker`** (out of scope for
# this PR) — tracked as OQ1 in `planning/current_plan.md` for a future
# successor PR. Materialization remains blocked until Q5 AND Q6 are both
# upgraded.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessor PRs:** #239 (ROADMAP stub) →
# #240 (Layer-1 scaffold plan) → #241 (Layer-2 scaffold + validator) →
# #242 (8-question parent adjudication) → **THIS PR #243 (Q5 successor
# adjudication)** → future Q6 successor PR → future tranche-2 materialization
# Layer-1 plan PR → future Layer-2 materialization-execution PR.

# %% [markdown]
# ## Lineage position — Q5-only retention successor in the Step 02_01_03 chain
#
# Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical
# work", the Step 02_01_03 readiness chain is serialised across PRs. This
# notebook is the Q5 successor; Q6 is explicitly out of scope.
#
# 1. PR #239 — ROADMAP stub block inserted (cross-region row enumerated).
# 2. PR #240 — Layer-1 scaffold + validator planning PR.
# 3. PR #241 — Layer-2 SCAFFOLD + ONE validation module
#    (`validate_history_enriched_pre_game_materialization.py` + mirrored
#    tests + jupytext scaffold). The SHA-256 of the PR #241 validator module
#    is re-asserted on every row of this Q5 successor CSV (NIT-B binding).
# 4. PR #242 — 8-question parent adjudication
#    (`02_01_03_history_source_anchor_coldstart_adjudication.{csv,md}`).
#    Q5 was bound `deferred_blocker` pending retention-impact evidence.
# 5. **THIS PR #243 — Q5-only successor adjudication** (this notebook).
#    Persists ONE artifact pair (30-column CSV × 5 rows + multi-section MD).
#    Q6 remains `deferred_blocker`; no feature materialization.
# 6. *Future* — Q6 rating reconstruction successor adjudication PR.
# 7. *Future* — Tranche-2 materialization-execution Layer-1 plan PR
#    (records `_MATERIALIZATION_QUERY`, projected column list, post-mat audit
#    schema, falsifier roll-call).
# 8. *Future* — Tranche-2 materialization-execution Layer-2 PR
#    (first Parquet artifact for the 6 history-enriched families).
# 9. *Future* — Post-materialization CROSS-02-01-v1.0.1 audit PR.
# 10. *Future* — Step 02_01_03 closure PR.

# %% [markdown]
# ## Non-materialization disclaimer (verbatim from `planning/current_plan.md` §Scope)
#
# **This Q5 successor PR does NOT:** materialise any feature value · write
# any Parquet · write any `leakage_audit_*.json` / `leakage_audit_*.md` ·
# flip `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` /
# `PHASE_STATUS.yaml` · append a `research_log.md` entry (dataset or root) ·
# edit the dataset `ROADMAP.md` body · patch any file under `reports/specs/`
# · patch any cleaning-layer YAML · patch any view schema under
# `data/db/schemas/` · close Step 02_01_03 · start Step 02_01_04 · start
# Phase 03 · start any baseline modelling · upgrade Q6 (rating reconstruction
# remains `deferred_blocker`) · unblock materialization (Q5 alone is
# insufficient — Q6 must also be upgraded before materialization).
#
# **What this PR DOES:** persists exactly ONE artifact pair (30-column CSV
# × 5 rows + multi-section MD) at
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.{csv,md}`.
# `materialized_output_paths` is `""` on every row.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_cross_region_retention import (  # noqa: E501
    ADJUDICATION_CSV_REL,
    ADJUDICATION_MD_REL,
    ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS,
    ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED,
    ALLOWED_Q5_BINDING_LEVELS,
    ALLOWED_Q5_VERDICTS,
    CROSS_REGION_COLUMN_NAME,
    CROSS_REGION_COLUMN_SOURCE_TABLE,
    EXPECTED_CROSS_REGION_NICKNAME_COUNT,
    EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED,
    EXPECTED_CROSS_REGION_TOON_ID_COUNT,
    EXPECTED_PR241_VALIDATOR_SHA256,
    FALSIFIER_PRIORITY_CHAIN,
    HELPER_TO_FALSIFIER_KEY,
    PARENT_PR242_CSV_REL,
    PARENT_PR242_MD_REL,
    Q5_DECISION_IDS,
    Q5_OPTION_NAMES,
    STEP_01_05_10_JSON_REL,
    STEP_01_05_10_MD_REL,
    adjudicate_history_cross_region_retention,
)

# %% [markdown]
# ## Bound constants imported from the Q5 adjudicator module (no inline redefinition)
#
# - `EXPECTED_PR241_VALIDATOR_SHA256` — the NIT-B binding SHA re-asserted on
#   every Q5 row.
# - `CROSS_REGION_COLUMN_SOURCE_TABLE` / `CROSS_REGION_COLUMN_NAME` — B1: the
#   cross-region column lives on `player_history_all`, not `matches_flat_clean`.
# - `Q5_DECISION_IDS` — the canonical 5-row ordered tuple (Q5A / Q5B / Q5C /
#   Q5_selected_policy / Q5_per_family_impact_summary).
# - `Q5_OPTION_NAMES` — the 3 CROSS-02-02 §6.2 row-5 options
#   (`strict_exclusion` / `dual_feature_path` /
#   `sensitivity_indicator_co_registration`).
# - `ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS` — NIT-C enum
#   (`toon_id_based` / `nickname_based` / `both`).
# - `ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED` — NIT-D structured tri-valued
#   enum (`yes` / `no` / `not_applicable`).
# - `EXPECTED_CROSS_REGION_*` — 01_05_10 nickname-anchored numeric anchors
#   used by the EQUIVALENCE probe.
# - `HELPER_TO_FALSIFIER_KEY` / `FALSIFIER_PRIORITY_CHAIN` — B4: both sets
#   contain exactly 31 entries and are value-equal at module import.
# - `ADJUDICATION_CSV_REL` / `ADJUDICATION_MD_REL` — canonical Q5 successor
#   artifact paths; `PARENT_PR242_*_REL` and `STEP_01_05_10_*_REL` are the
#   pinned upstream evidence paths.

# %%
print("EXPECTED_PR241_VALIDATOR_SHA256:", EXPECTED_PR241_VALIDATOR_SHA256)
print("CROSS_REGION_COLUMN_SOURCE_TABLE:", CROSS_REGION_COLUMN_SOURCE_TABLE)
print("CROSS_REGION_COLUMN_NAME:", CROSS_REGION_COLUMN_NAME)
print("Q5_DECISION_IDS:", Q5_DECISION_IDS)
print("Q5_OPTION_NAMES:", Q5_OPTION_NAMES)
print("ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS:", sorted(ALLOWED_CROSS_REGION_ANCHOR_SEMANTICS))
print("ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED:", sorted(ALLOWED_HISTORY_ROW_FILTER_ON_PHA_APPLIED))
print("ALLOWED_Q5_VERDICTS:", sorted(ALLOWED_Q5_VERDICTS))
print("ALLOWED_Q5_BINDING_LEVELS:", sorted(ALLOWED_Q5_BINDING_LEVELS))
print("EXPECTED_CROSS_REGION_NICKNAME_COUNT:", EXPECTED_CROSS_REGION_NICKNAME_COUNT)
print("EXPECTED_CROSS_REGION_TOON_ID_COUNT:", EXPECTED_CROSS_REGION_TOON_ID_COUNT)
print(
    "EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED:",
    EXPECTED_CROSS_REGION_PLAYER_MATCH_PAIR_COUNT_NICKNAME_ANCHORED,
)
print("HELPER_TO_FALSIFIER_KEY entries:", len(HELPER_TO_FALSIFIER_KEY))
print("FALSIFIER_PRIORITY_CHAIN entries:", len(FALSIFIER_PRIORITY_CHAIN))
print("PARENT_PR242_CSV_REL:", PARENT_PR242_CSV_REL)
print("PARENT_PR242_MD_REL:", PARENT_PR242_MD_REL)
print("STEP_01_05_10_MD_REL:", STEP_01_05_10_MD_REL)
print("STEP_01_05_10_JSON_REL:", STEP_01_05_10_JSON_REL)
print("ADJUDICATION_CSV_REL:", ADJUDICATION_CSV_REL)
print("ADJUDICATION_MD_REL:", ADJUDICATION_MD_REL)

# %% [markdown]
# ## Q5A — `strict_exclusion` retention probe
#
# # Hypothesis: filtering history rows on
# # `player_history_all.is_cross_region_fragmented = FALSE` (B3: filter applied
# # to HISTORY rows, NOT TARGET rows) and aggregating the 6 tranche-2 family
# # signals over the remaining rows yields a non-degenerate retention table
# # (some rows kept AND some rows dropped) bounded by the canonical strict-`<`
# # PHA history window. The retention measurement excludes cold-start target
# # rows (LEFT-JOIN-NULL on `is_cross_region_fragmented`) per the PR #243
# # Dispatch 3 OPTION (a) fix; the kept + dropped == total invariant is
# # measured strictly over rows that have a matched history record.
# # Verdict on Q5A row = `narrow_with_evidence`;
# # `cross_region_policy = "strict_exclusion"`;
# # `history_row_filter_on_pha_applied = "yes"` (NIT-D structured field).
# # Falsifiers: `_check_strict_exclusion_history_filter_retention_smoke`
# # (B3 retention identity); `q5_three_options_not_enumerated` (NIT-A scope);
# # `q5_history_row_filter_on_pha_applied_invalid` (NIT-D enum guard).

# %% [markdown]
# ## Q5B — `dual_feature_path` branch-nondegeneracy probe
#
# # Hypothesis: splitting PHA history rows on `is_cross_region_fragmented` and
# # routing each branch into a dedicated feature column path yields BOTH a
# # non-degenerate non-XR branch (`history_is_xr = FALSE` rows present) AND a
# # non-degenerate XR branch (`history_is_xr = TRUE` rows present) for the
# # observed target population. The filter is applied to the PHA history rows
# # (B3) at branch-routing time; the target row itself is preserved in both
# # branches. Verdict on Q5B row = `narrow_with_evidence`;
# # `cross_region_policy = "dual_feature_path"`;
# # `history_row_filter_on_pha_applied = "yes"` (per-branch routing predicate).
# # Falsifier: `_check_dual_feature_path_branches_nondegenerate` (a degenerate
# # branch invalidates the dual-path operationalization).

# %% [markdown]
# ## Q5C — `sensitivity_indicator_co_registration` flag-nondegeneracy + anchor probe
#
# # Hypothesis: projecting the boolean OR of `is_cross_region_fragmented` over
# # the PHA history window into a per-target sensitivity indicator (anchored
# # at `target.started_at`, B-X2 strict-`<`) yields a non-degenerate flag (BOTH
# # `TRUE` and `FALSE` present) without filtering PHA history rows themselves.
# # The anchor must be `target.started_at` and the Q5C notes must avoid all
# # POST-GAME tokens to preserve pre-game discipline (Invariant #3).
# # Verdict on Q5C row = `narrow_with_evidence`;
# # `cross_region_policy = "sensitivity_indicator_co_registration"`;
# # `history_row_filter_on_pha_applied = "no"` (the flag is co-registered;
# # PHA rows themselves are not filtered).
# # Falsifiers: `_check_sensitivity_indicator_flag_nondegenerate` (flag must
# # be non-degenerate); `_check_sensitivity_indicator_anchor_target_time`
# # (notes must cite target-time anchoring; POST-GAME tokens forbidden in
# # scoped fields).

# %% [markdown]
# ## Q5_selected_policy — verdict EMERGES from the per-family table (A14)
#
# # Hypothesis: the selected Q5 policy and verdict EMERGE from the per-family
# # retention table (Q5_per_family_impact_summary); they are not pre-asserted.
# # The provisional selected policy reported here is
# # `sensitivity_indicator_co_registration` with verdict `narrow_with_evidence`
# # — chosen because it preserves the full PHA history population while
# # co-registering the cross-region signal at target-time, which (a) avoids
# # the strict-exclusion retention loss measured in Q5A and (b) avoids the
# # dual-path branch fragmentation measured in Q5B while (c) still surfacing
# # the cross-region fragmentation signal to the downstream feature consumer.
# # `cross_region_policy = "sensitivity_indicator_co_registration"`;
# # `history_row_filter_on_pha_applied = "no"`. The verdict-emergence
# # discipline (A14 / N3) requires the per-family table FIRST, then the
# # selected_policy row reports the table's verdict.
# # Falsifiers: `_check_q5_selected_policy_verdict_emergence_marker_present`;
# # `_check_q5_selected_policy_binding_level_consistent`;
# # `q5_three_options_not_enumerated` (selected row must also cite all 3).

# %% [markdown]
# ## Q5_per_family_impact_summary — 6-family aggregate (NIT-D `not_applicable`)
#
# # Hypothesis: the family-level summary aggregates strict-exclusion retention
# # impact across the 6 tranche-2 family IDs (the impact is the product of
# # the row-level retention rate from Q5A with each family's known weight per
# # the registry CSV); the per-family weights are recorded in the MD §rationale
# # block, not re-derived here. The summary row's
# # `cross_region_policy = "strict_exclusion"` is used as the worst-case
# # baseline for cross-family impact estimation; the row is informational only
# # and does NOT itself bind a policy — `history_row_filter_on_pha_applied`
# # is therefore `"not_applicable"` (NIT-D tri-valued enum).
# # Falsifier: `q5_per_family_impact_summary_pha_filter_invalid` rejects
# # any value other than `"not_applicable"` for this row.

# %% [markdown]
# ## Adjudication call — read-only DuckDB + PR #242 parent + 01_05_10 evidence
#
# This cell invokes the single public entrypoint
# `adjudicate_history_cross_region_retention(...)` against the real sc2egset
# DuckDB (read-only), the PR #242 parent artifact pair, and the 01_05_10
# evidence MD+JSON. The entrypoint runs every retention/anchor/SHA probe,
# builds the 5 Q5 decisions in `Q5_DECISION_IDS` order, runs every falsifier
# in `FALSIFIER_PRIORITY_CHAIN` order, and (only if no falsifier fires)
# writes the 30-column CSV × 5 rows + multi-section MD artifact pair. The
# asserts here re-validate the result and halt the notebook on any
# halting-falsifier-fired condition (halt-before-artifact per
# `.claude/rules/data-analysis-lineage.md`).

# %%
# Resolve repo root deterministically. `__file__` is set when this module is
# executed as a Python script (e.g., via `python -m`); inside a live Jupyter
# kernel `__file__` is not defined, so fall back to walking up from the
# current working directory. nbconvert sets CWD to the directory containing
# the notebook, so `parents[5]` of CWD is also the repo root. The fallback
# walks up looking for the repo `pyproject.toml` sentinel for resilience.
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
DUCKDB_PATH = REPO_ROOT / (
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
)
PARENT_PR242_CSV_PATH = REPO_ROOT / PARENT_PR242_CSV_REL
PARENT_PR242_MD_PATH = REPO_ROOT / PARENT_PR242_MD_REL
STEP_01_05_10_MD_PATH = REPO_ROOT / STEP_01_05_10_MD_REL
STEP_01_05_10_JSON_PATH = REPO_ROOT / STEP_01_05_10_JSON_REL
CSV_PATH = REPO_ROOT / ADJUDICATION_CSV_REL
MD_PATH = REPO_ROOT / ADJUDICATION_MD_REL
AUDIT_PR_LABEL = "PR #243"
AUDIT_DATE = "2026-05-24"

# %%
result = adjudicate_history_cross_region_retention(
    duckdb_path=DUCKDB_PATH,
    parent_pr242_csv_path=PARENT_PR242_CSV_PATH,
    parent_pr242_md_path=PARENT_PR242_MD_PATH,
    step_01_05_10_md_path=STEP_01_05_10_MD_PATH,
    step_01_05_10_json_path=STEP_01_05_10_JSON_PATH,
    csv_path=CSV_PATH,
    md_path=MD_PATH,
    audit_pr=AUDIT_PR_LABEL,
    audit_date=AUDIT_DATE,
)

print("passed:", result.passed)
print("decisions:", len(result.decisions))
print("halting_falsifier:", result.halting_falsifier)
print("falsifiers_fired:", result.falsifiers_fired)
print("csv_path:", result.csv_path)
print("md_path:", result.md_path)
print("provenance_git_sha:", result.provenance_git_sha)

# Per-row NIT-B binding: every decision must carry the pinned PR #241
# validator SHA-256. The CrossRegionAdjudicationResult dataclass does not
# expose the SHA at the result level; it is recorded on each decision row.
for _d in result.decisions:
    assert (
        _d.pr241_scaffold_validator_module_sha256
        == EXPECTED_PR241_VALIDATOR_SHA256
    ), (
        f"NIT-B binding drift: decision {_d.decision_id!r} carries "
        f"{_d.pr241_scaffold_validator_module_sha256!r}, "
        f"expected {EXPECTED_PR241_VALIDATOR_SHA256!r}"
    )

assert result.passed is True
assert len(result.decisions) == 5
assert result.halting_falsifier is None
assert result.falsifiers_fired == ()

# %% [markdown]
# ## Closing — Q5 successor artifact persisted; explicit deferrals preserved
#
# **Persisted (this PR #243):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.csv`
#   (30 columns × 5 rows + 1 header; `materialized_output_paths` is `""` on
#   every row; `pr241_scaffold_validator_module_sha256` equals
#   `EXPECTED_PR241_VALIDATOR_SHA256` on every row; `audit_pr = "PR #243"`
#   on every row).
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_cross_region_adjudication.md`
#   (non-materialization disclaimer · PR #242 lineage · Q5-only scope (Q6
#   out of scope) · per-option decision table · per-family retention table ·
#   verbatim SQL · toon_id-vs-nickname anchor semantics · target-filter vs
#   history-filter distinction · structured field explanation ·
#   materialization-blocked statement · falsifier roll-call · SHA provenance).
#
# **Explicitly DEFERRED to successor PRs (NOT this PR):**
# - **Q6 rating reconstruction model family** — remains `deferred_blocker`;
#   tracked as OQ1 in `planning/current_plan.md` for a future Q6 successor
#   adjudication PR with rating-family empirical evaluation evidence (N-X3
#   strengthened gate: ≥1 repo path + ≥1 citation + forward-only wording +
#   cold-start/missingness wording).
# - **Materialization SQL** (the tranche-2 `_MATERIALIZATION_QUERY` analogue
#   of PR #234's tranche-1 query) — deferred to the future Layer-1 plan PR
#   for the tranche-2 materialization execution.
# - **First Parquet artifact** for the 6 history-enriched families —
#   deferred to the future Layer-2 materialization-execution PR.
# - **Post-materialization CROSS-02-01-v1.0.1 audit JSON+MD** — deferred to
#   the future post-mat audit PR.
# - **Step 02_01_03 closure** (the `02_01_03: complete` row in
#   `STEP_STATUS.yaml` + `research_log` closure entry) — deferred to the
#   future closure PR.
#
# This notebook does NOT update any `STEP_STATUS.yaml` /
# `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`. It does NOT append
# any `research_log.md` entry (dataset or root). It does NOT edit
# `ROADMAP.md`. It does NOT patch any spec or cleaning-layer YAML.
# Materialization remains blocked until BOTH Q5 AND Q6 are upgraded.
# Phase 03 work and baseline modelling remain barred per the existing phase
# status.
