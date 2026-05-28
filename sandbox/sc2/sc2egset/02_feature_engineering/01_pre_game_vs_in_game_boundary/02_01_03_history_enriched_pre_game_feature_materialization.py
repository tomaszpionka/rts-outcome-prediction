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
# # Step 02_01_03 — Five-family history-enriched pre_game feature materialization: sc2egset
#
# **MATERIALIZATION + POST-MAT AUDIT + RESEARCH_LOG APPEND (non-batching
# sequence steps 6-8 of 9).** This notebook OVERWRITES the PR #241 scaffold
# (preserved at git SHA `3c6709bf`) per `sandbox/README.md` single-notebook-
# per-Step contract. It materialises the FIVE history-enriched pre_game
# feature families authorised by PR #257's ROADMAP amendment (grep token
# `materialization_scope_amendment_post_pr_255`) into ONE Parquet artifact
# (44,418 rows × 28 projected columns = 3 identity + 1 context anchor +
# 24 audited features), runs the FIRST non-vacuous CROSS-02-01-v1.0.1 §3
# leakage audit for Step `02_01_03`, and appends a non-closure
# `research_log.md` entry mirroring PR #236's precedent.
#
# **Five permitted families (PR #257 amendment lines 2536-2540):**
# `focal_player_history`, `opponent_player_history`,
# `matchup_history_aggregate`, `cross_region_fragmentation_handling`,
# `in_game_history_aggregate`.
#
# **Excluded family (PR #257 amendment line 2542):** `reconstructed_rating`
# (verdict from PR #255 omit-closure:
# `omit_reconstructed_rating_and_unblock_other_five`).
#
# **Excluded columns (PR #257 amendment lines 2546-2548):**
# `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`,
# `reconstructed_rating_diff`.
#
# `started_at` is projected as a row-identity anchor only (CROSS-02-00
# Section 5.1 = CONTEXT) and is excluded from `features_audited`.
#
# **This PR does NOT:** flip STEP_STATUS / PIPELINE_SECTION_STATUS /
# PHASE_STATUS · edit ROADMAP · patch any spec or cleaning-layer YAML ·
# start Step 02_01_04 · start Phase 03 · close Step 02_01_03. Closure is
# deferred to a separate U2.B-style PR per PR #237 precedent.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessors:** 02_01_02 (closed, PR #237);
# PR #239 (ROADMAP stub) → PR #241 (scaffold) → PR #242 (Q1/Q2/Q3/Q4/Q7/Q8)
# → PR #243 (Q5) → PR #245 (Q6) → PR #247 (Q6F) → PR #249 (Q6G) →
# PR #251 (Q6H terminal) → PR #253 (Step 02_01_99 ROADMAP stub) →
# PR #255 (omit-closure) → PR #257 (ROADMAP amendment).

# %% [markdown]
# ## Hypothesis + falsifier + sanity-check declaration (data-analysis-lineage.md)
#
# - **Assumption being tested:** the 24 history-enriched feature columns are
#   leakage-free under the strict-< TRY_CAST history filter, and the
#   matchup CTE is 1v1-restricted via the `matches_flat_clean` join (B2 fix).
# - **Measurement claim:** the materialised Parquet has exactly 44,418 rows
#   × 28 projected columns (3 identity + 1 context + 24 audited); the
#   CROSS-02-01 audit returns `verdict = "PASS"`; the
#   `features_audited` list equals the canonical 24-tuple in projection
#   order; the `reconstructed_rating` family and its three columns are
#   ABSENT from the output.
# - **Falsifier:** `F-audit-verdict-not-pass`, `F-row-count-mismatch`,
#   `F-features-audited-not-twenty-four`,
#   `F-reconstructed-rating-column-present`,
#   `F-matchup-cte-includes-non-1v1-history`,
#   `F-decisive-result-flag-not-used`, plus the full falsifier-priority chain.
# - **Sanity check:** `COUNT(*) == EXPECTED_OUTPUT_ROW_COUNT == 44_418`;
#   `COUNT(DISTINCT focal_match_id) == 22_209`; focal/opponent symmetry
#   violations = 0 on `started_at` swap; module-load assertions on the
#   per-family sub-feature counts (6 + 6 + 2 + 2 + 8 = 24).
# - **Expected artifact:**
#   `02_01_03_history_enriched_pre_game_features.parquet` + audit pair
#   under `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` +
#   one new non-closure entry in the dataset `research_log.md`.
# - **Lineage source:** PR #257 ROADMAP amendment authorises this
#   materialisation; PR #255 omit-closure binds the verdict and the
#   `q5_policy = sensitivity_indicator_co_registration` field re-elevation.
# - **Downstream decision:** the future U2.B-style closure PR consumes
#   these artifacts to flip `STEP_STATUS.yaml` to `02_01_03: complete`.

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.materialize_history_enriched_pre_game_features import (  # noqa: E501
    CROSS_REGION_POLICY,
    EXCLUDED_FAMILY,
    EXPECTED_AUDITED_FEATURE_COLUMN_COUNT,
    EXPECTED_AUDITED_FEATURE_COLUMNS,
    EXPECTED_DISTINCT_FOCAL_MATCH_COUNT,
    EXPECTED_OUTPUT_COLUMNS,
    EXPECTED_OUTPUT_ROW_COUNT,
    EXPECTED_PARQUET_COLUMN_COUNT,
    FIVE_FAMILY_CANONICAL_ORDER,
    FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS,
    HISTORY_ENRICHED_AUDIT_JSON_RELPATH,
    HISTORY_ENRICHED_AUDIT_MD_RELPATH,
    HISTORY_ENRICHED_OUTPUT_RELPATH,
    HISTORY_ENRICHED_RESEARCH_LOG_RELPATH,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
    PROJECTED_CONTEXT_COLUMNS,
    PROJECTED_IDENTITY_COLUMNS,
    run_step_02_01_03,
)

# %% [markdown]
# ## Context — PR #257 ROADMAP amendment frozen-input snapshot
#
# - **Q1 source layer (PR #242 BINDING):** `matches_flat_clean` for the
#   target row; `player_history_all` for history-side rows. Per-player
#   history aggregates ALL game types per Q1 BINDING (documented in audit
#   MD §1).
# - **Q1 1v1 restriction (B2 fix):** the `matchup_history_aggregate` CTE
#   restricts the shared-replay self-join to 1v1 historical matches via
#   `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`.
# - **Q2 target anchor (PR #242 BINDING):**
#   `matches_history_minimal.started_at TIMESTAMP`; CONTEXT per CROSS-02-00
#   Section 5.1.
# - **Q3 strict-< history filter (PR #242 BINDING B-X2):** canonical
#   `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at`.
# - **Q4 cold-start gates:** G-CS-2/3/4/5 at the registry layer; G-CS-6
#   fold-aware fit DEFERRED to Phase 03.
# - **Q5 cross-region policy (PR #243 BINDING + PR #255 q5_policy
#   re-elevation):** `sensitivity_indicator_co_registration` — co-register
#   BOTH `is_cross_region_fragmented_focal_history_any` AND
#   `is_cross_region_fragmented_opponent_history_any` BOOLEAN flags per
#   Invariant I5 symmetry.
# - **Q6 (PR #245 + PR #255 omit-closure):**
#   `omit_reconstructed_rating_and_unblock_other_five` — the
#   `reconstructed_rating` family is INTENTIONALLY OMITTED, not silently
#   satisfied.
# - **Q6F/Q6G/Q6H:** rating-algorithm survey / implementation proof /
#   path-decision artifacts pinned by SHA; carry-forward only.
# - **Q7 IN_GAME_HISTORICAL allowed columns (PR #242 BINDING):**
#   `APM`, `SQ`, `supplyCappedPercent`, `header_elapsedGameLoops`
#   (×2 sides = 8 audited columns in `in_game_history_aggregate`).
# - **Q8 MHM consumption:** target row identity + `started_at` anchor +
#   cold-start enumeration only; NEVER as a feature source.
# - **N11 fix:** `ph.is_decisive_result = TRUE` is used in place of inline
#   `ph.result IN ('Win', 'Loss')` (verified to exist as BOOLEAN at
#   `player_history_all.yaml` lines 48-54).
# - **N9 Invariant I5 citation:** cross-region indicator pair symmetrised
#   per `.claude/scientific-invariants.md` Invariant I5, beyond PR #243's
#   single-indicator text.

# %% [markdown]
# ## Five permitted families and their audited-column counts
#
# | # | Family | Audited column count |
# |---|--------|---------------------|
# | 1 | `focal_player_history` | 6 |
# | 2 | `opponent_player_history` | 6 |
# | 3 | `matchup_history_aggregate` | 2 |
# | 4 | `cross_region_fragmentation_handling` | 2 |
# | 5 | `in_game_history_aggregate` | 8 |
# | **TOTAL** | | **24** |

# %%
DUCKDB_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
)
OUTPUT_PARQUET_PATH = Path(HISTORY_ENRICHED_OUTPUT_RELPATH)
AUDIT_JSON_PATH = Path(HISTORY_ENRICHED_AUDIT_JSON_RELPATH)
AUDIT_MD_PATH = Path(HISTORY_ENRICHED_AUDIT_MD_RELPATH)
RESEARCH_LOG_PATH = Path(HISTORY_ENRICHED_RESEARCH_LOG_RELPATH)
AUDIT_DATE = "2026-05-28"
AUDIT_PR_LABEL = "PR #<TBD>"
BRANCH = "feat/sc2egset-02-01-03-five-family-materialization"

# %% [markdown]
# ## Verify constants (module-load self-assertion echo)

# %%
print("FIVE_FAMILY_CANONICAL_ORDER:", FIVE_FAMILY_CANONICAL_ORDER)
print("EXCLUDED_FAMILY:", EXCLUDED_FAMILY)
print(
    "FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS:",
    sorted(FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS),
)
print("CROSS_REGION_POLICY:", CROSS_REGION_POLICY)
print(
    "IN_GAME_HISTORICAL_AGGREGATED_COLUMNS:",
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
)
print(
    "EXPECTED_AUDITED_FEATURE_COLUMN_COUNT:",
    EXPECTED_AUDITED_FEATURE_COLUMN_COUNT,
)
print("EXPECTED_PARQUET_COLUMN_COUNT:", EXPECTED_PARQUET_COLUMN_COUNT)
print("EXPECTED_OUTPUT_ROW_COUNT:", EXPECTED_OUTPUT_ROW_COUNT)
print("EXPECTED_DISTINCT_FOCAL_MATCH_COUNT:", EXPECTED_DISTINCT_FOCAL_MATCH_COUNT)

# %% [markdown]
# ## Materialise + audit + append research_log entry

# %%
mat_result, audit_result = run_step_02_01_03(
    duckdb_path=DUCKDB_PATH,
    output_parquet_path=OUTPUT_PARQUET_PATH,
    audit_json_path=AUDIT_JSON_PATH,
    audit_md_path=AUDIT_MD_PATH,
    research_log_path=RESEARCH_LOG_PATH,
    audit_date=AUDIT_DATE,
    branch=BRANCH,
    audit_pr=AUDIT_PR_LABEL,
    write_research_log=True,
)

# %%
print("mat.passed:", mat_result.passed)
print("mat.row_count:", mat_result.row_count)
print("mat.distinct_focal_match_id:", mat_result.distinct_focal_match_id_count)
print("mat.column_count:", len(mat_result.column_names))
print("mat.focal_rows_per_match_violations:", mat_result.focal_rows_per_match_violations)
print("mat.symmetry_violations:", mat_result.symmetry_violations)
print("mat.halting_falsifier:", mat_result.halting_falsifier)

assert mat_result.passed is True
assert mat_result.row_count == EXPECTED_OUTPUT_ROW_COUNT
assert mat_result.distinct_focal_match_id_count == EXPECTED_DISTINCT_FOCAL_MATCH_COUNT
assert mat_result.column_names == EXPECTED_OUTPUT_COLUMNS
assert mat_result.halting_falsifier is None

# %%
print("audit.verdict:", audit_result.verdict)
print("audit.halting_falsifier:", audit_result.halting_falsifier)
print("audit.features_audited count:", len(audit_result.features_audited))
print("audit.projected_context_columns:", audit_result.projected_context_columns)
print("audit.projected_identity_columns:", audit_result.projected_identity_columns)

assert audit_result.verdict == "PASS"
assert audit_result.halting_falsifier is None
assert len(audit_result.features_audited) == EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
assert audit_result.features_audited == EXPECTED_AUDITED_FEATURE_COLUMNS
assert audit_result.projected_context_columns == PROJECTED_CONTEXT_COLUMNS
assert audit_result.projected_identity_columns == PROJECTED_IDENTITY_COLUMNS
assert set(audit_result.features_audited).isdisjoint(
    set(audit_result.projected_context_columns)
    | set(audit_result.projected_identity_columns)
)

# %% [markdown]
# ## Closing — five-family Parquet + non-vacuous audit + research_log entry persisted
#
# **What was done (non-batching steps 6-8 of 9):**
# - Materialised five-family Parquet at the canonical path
#   (`HISTORY_ENRICHED_OUTPUT_RELPATH` constant; 44,418 rows × 28 cols =
#   3 identity + 1 context anchor + 24 audited features over the five
#   permitted families).
# - Persisted the FIRST non-vacuous CROSS-02-01-v1.0.1 §3 audit pair at
#   `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`
#   (`features_audited` = exactly the 24 history-enriched PRE_GAME feature
#   columns; `verdict = PASS`; 17 BINDING parent artifact SHAs pinned;
#   custom_extensions section enumerates fields beyond §3; defensive
#   `matches_long_raw_yaml_sha256` pin per R3-N2).
# - Appended a non-closure entry to the dataset `research_log.md` mirroring
#   PR #236's precedent (`closure_status: still_open`,
#   `materialization_state: materialized`,
#   `leakage_audit_state: post_materialization_pass`,
#   `features_audited_count: 24`, `row_count: 44418`, etc).
#
# **What was NOT done (deferred to the U2.B-style closure PR):**
# - `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`
#   are byte-unchanged.
# - `02_01_03: complete` is NOT added to `STEP_STATUS.yaml`.
# - ROADMAP body, specs, and cleaning-layer YAMLs are byte-unchanged.
# - Root `reports/research_log.md` is byte-unchanged (single-dataset
#   materialisation; no CROSS entry needed).
# - Phase 03 is not started; Step 02_01_04 is not started.
# - The PR #241 scaffold notebook content is preserved at git SHA
#   `3c6709bf` in the repo's git history; this notebook OVERWRITES the
#   scaffold in place per `sandbox/README.md` single-notebook-per-Step
#   contract.
