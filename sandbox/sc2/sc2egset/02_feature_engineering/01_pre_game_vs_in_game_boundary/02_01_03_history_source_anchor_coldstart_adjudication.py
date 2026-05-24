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
# # Step 02_01_03 — History-enriched source/anchor/cold-start ADJUDICATION: sc2egset
#
# **ADJUDICATION ONLY (non-batching sequence step 3 of 9 for the 02_01_03
# readiness chain).** This notebook resolves 8 coupled pre-materialization
# decisions (Q1-Q8) for the 6 tranche-2 `history_enriched_pre_game` feature
# families and persists ONE artifact pair (33-column CSV + §1-§14 MD) under
# `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
# No `def` / `class` / `lambda` appears in any cell; every probe, falsifier,
# and writer lives inside the adjudicator module and is imported here.
#
# **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_03 ·
# **Dataset:** sc2egset · **Predecessor PRs:** #239 (ROADMAP stub) →
# #240 (scaffold plan) → #241 (scaffold + validator).

# %% [markdown]
# ## Lineage position — artifact #3 of N for Step 02_01_03 readiness
#
# The Step 02_01_03 readiness chain is constructed in serialized PRs per
# `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical
# work" (sequence steps 1-9):
#
# 1. PR #239 — ROADMAP stub block inserted (`reports/ROADMAP.md` lines
#    2274-2523; declares the 6 tranche-2 family rows, strict-`<` cutoff,
#    G-L-1/3/4/7 halt gates, G-CS-2..6 cold-start gates, RISK-20 cross-region
#    adjudication gating, §10 audit re-run gating).
# 2. PR #240 — Layer-1 planning PR for the scaffold + ONE validation module
#    (Layer-1 author of `planning/current_plan.md` + critique for #241).
# 3. PR #241 — Layer-2 SCAFFOLD + ONE validation module
#    (`validate_history_enriched_pre_game_materialization.py` + mirrored
#    tests + jupytext scaffold). SHA-256 of the PR #241 validator module is
#    re-asserted on every row of this adjudication CSV (N4 binding).
# 4. **THIS PR (#242) — Layer-2 ADJUDICATION** (this notebook).
#    Persists ONE adjudication CSV+MD pair. NO feature value is computed
#    or materialised. NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml`
#    / `PHASE_STATUS.yaml` flip. NO `research_log` entry (dataset or root).
#    NO ROADMAP body edit. NO spec or cleaning-layer YAML patch.
# 5. *Future* — Materialization-execution PLAN PR (Layer-1; analogue of
#    PR #235 for tranche-1). Records `_MATERIALIZATION_QUERY`, projected
#    column list, post-mat audit schema, falsifier roll-call.
# 6. *Future* — Materialization-execution PR (Layer-2; analogue of PR #236).
#    First Parquet artifact for the 6 history-enriched families.
# 7. *Future* — Post-materialization CROSS-02-01-v1.0.1 audit PR.
# 8. *Future* — Step 02_01_03 closure PR (analogue of PR #237).
#
# Materialization remains blocked until Q5 (cross-region) and Q6 (rating
# reconstruction) `deferred_blocker` decisions are upgraded to `bind_now`
# in a successor adjudication PR with the required empirical evidence.

# %% [markdown]
# ## Non-materialization disclaimer (verbatim)
#
# **This adjudication PR does NOT:** materialise any feature value · write any
# Parquet · write any `leakage_audit_*.json` / `leakage_audit_*.md` · flip
# `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` ·
# append a `research_log.md` entry (dataset or root) · edit the dataset
# `ROADMAP.md` body · patch any file under `reports/specs/` ·
# patch any cleaning-layer YAML · patch any view schema under
# `data/db/schemas/` · close Step 02_01_03 · start Step 02_01_04 · start
# Phase 03 · start any baseline modelling.
#
# **What this PR DOES:** persists exactly ONE artifact pair (33-column CSV
# + §1-§14 MD) under
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
# `materialized_output_paths` is `""` on every row. The 33-column CSV row
# schema is exactly the `HistoryEnrichedAdjudicationDecision` dataclass field
# order followed by the `notes` field (declared last).

# %%
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_enriched_pre_game_source_layer import (  # noqa: E501
    ADJUDICATION_CSV_REL,
    ADJUDICATION_MD_REL,
    EXPECTED_PR241_VALIDATOR_SHA256,
    HELPER_TO_FALSIFIER_KEY,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
    POST_GAME_TOKEN_EXEMPT_FIELDS,
    POST_GAME_TOKEN_SCOPED_FIELDS,
    STRICT_LT_HISTORY_FILTER,
    adjudicate_history_enriched_pre_game_source_layer,
)

# %% [markdown]
# ## Bound constants imported from the adjudicator module (no inline redefinition)
#
# - `EXPECTED_PR241_VALIDATOR_SHA256` — the N4 binding SHA re-asserted on
#   every row.
# - `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS` — N1 deterministic 4-tuple
#   `(APM, SQ, supplyCappedPercent, header_elapsedGameLoops)`.
# - `STRICT_LT_HISTORY_FILTER` — B-X2 canonical strict-`<` expression
#   (`TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`).
# - `POST_GAME_TOKEN_SCOPED_FIELDS` — B-X1 the 3 scoped fields scanned for
#   POST-GAME tokens.
# - `POST_GAME_TOKEN_EXEMPT_FIELDS` — B-X1 the 7 prose / evidence fields
#   exempt from POST-GAME token scanning (negated rationale allowed).
# - `HELPER_TO_FALSIFIER_KEY` — N-X1 mapping; every value also appears in
#   the falsifier priority chain.
# - `ADJUDICATION_CSV_REL` / `ADJUDICATION_MD_REL` — canonical artifact paths.

# %%
print("EXPECTED_PR241_VALIDATOR_SHA256:", EXPECTED_PR241_VALIDATOR_SHA256)
print("IN_GAME_HISTORICAL_AGGREGATED_COLUMNS:", IN_GAME_HISTORICAL_AGGREGATED_COLUMNS)
print("STRICT_LT_HISTORY_FILTER:", STRICT_LT_HISTORY_FILTER)
print("POST_GAME_TOKEN_SCOPED_FIELDS:", sorted(POST_GAME_TOKEN_SCOPED_FIELDS))
print("POST_GAME_TOKEN_EXEMPT_FIELDS:", sorted(POST_GAME_TOKEN_EXEMPT_FIELDS))
print("HELPER_TO_FALSIFIER_KEY entries:", len(HELPER_TO_FALSIFIER_KEY))
print("ADJUDICATION_CSV_REL:", ADJUDICATION_CSV_REL)
print("ADJUDICATION_MD_REL:", ADJUDICATION_MD_REL)

# %% [markdown]
# ## Q1 — Source layer (target/history asymmetry; N-X4 subfield disambiguation)
#
# # Hypothesis: the 6 tranche-2 history-enriched families bind to an
# # **asymmetric** target/history source pair — target = `matches_flat_clean`
# # (RATIFY tranche-1 PR #234 Q1 BINDING; cleaned-raw, 1v1-scoped, 44,418 rows);
# # history = `player_history_all` (per ROADMAP `inputs.duckdb_tables` line
# # 2367 + CROSS-02-02 §6.2 rows 1-4 + 6 verbatim source bindings; 44,817 rows).
# # Verdict = `extend_with_evidence`; binding = `binding_for_materialization`.
# # Recorded subfields per N-X4: `selected_target_source_layer`,
# # `selected_history_source_layer`, `target_history_asymmetry = "asymmetric"`,
# # `source_layer_divergence_reason` (matches_flat operationally vs registry),
# # `history_source_extension_reason` (player_history_all added in tranche-2).
# # Falsifier: `q1_source_layer_evidence_inconsistent` AND
# # `q1_single_row_violation` (only ONE Q1 row may exist; N5 + N-X4 enforce
# # subfield completeness).

# %% [markdown]
# ## Q2 — Target temporal anchor (RATIFY tranche-1 PR #234 Q2(a))
#
# # Hypothesis: the strict-`<` history filter resolves the target row's
# # temporal position using `matches_history_minimal.started_at TIMESTAMP`
# # (RATIFY tranche-1 PR #234 Q2(a) BINDING; CROSS-02-00 §3.1 canonical
# # cross-dataset dtype; 0 NULLs, 0 cross-row inconsistency).
# # Verdict = `ratify_with_evidence`; binding = `binding_for_materialization`.
# # Falsifier: `q2_target_anchor_type_mismatch` halts on any non-TIMESTAMP.

# %% [markdown]
# ## Q3 — Historical row time column (B-X2 canonical TRY_CAST form binding)
#
# # Hypothesis: the historical row time column for the strict-`<` filter is
# # `player_history_all.details_timeUTC` (VARCHAR upstream; TRY_CAST to
# # TIMESTAMP for chronological fidelity). The canonical strict-`<` filter
# # expression is exactly `STRICT_LT_HISTORY_FILTER`:
# #
# #     TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at
# #
# # The ROADMAP §02_01_03 raw form (`ph.details_timeUTC < target.started_at`)
# # is recorded as provenance only (`STRICT_LT_FILTER_ROADMAP_RAW`); any
# # executable site adopting the bare form is rejected by
# # `strict_lt_filter_divergence`.
# # Verdict = `bind_now`; binding = `binding_for_materialization`.
# # Falsifiers: `q3_history_time_column_invalid`, `q3_strict_lt_smoke_failed`,
# # `strict_lt_filter_divergence`.

# %% [markdown]
# ## Q4 — Cold-start policy (G-CS-2..G-CS-5; G-CS-6 distinguished)
#
# # Hypothesis: tranche-2 cold-start is handled by 4 scaffold-registry gates
# # bound here (G-CS-2 focal+opponent+in_game_history_aggregate; G-CS-3
# # matchup_history_aggregate; G-CS-4 reconstructed_rating; G-CS-5 cross-
# # region fragmentation handling) plus G-CS-6 distinguished as a
# # materialization-time fold-aware fit gate per CROSS-02-02 §9 + ROADMAP
# # lines 2334-2338 (G-CS-6 is DEFERRED to the future materialization PR;
# # not bound here). Notes explicitly cite `match_time < T` discipline so
# # the three ML-protocol leakage modes (rolling, h2h, co-occurring) are
# # forbidden by construction.
# # Verdict = `extend_with_evidence`; binding = `binding_for_materialization`.
# # Falsifiers: `q4_cold_start_gates_incomplete` (any G-CS-2..5 missing),
# # `q4_cold_start_leakage` (notes omit `match_time < T` wording).

# %% [markdown]
# ## Q5 — Cross-region fragmentation policy (RISK-20; DEFERRED)
#
# # Hypothesis: cross-region fragmentation operationalization (RISK-20)
# # cannot be bound now without retention-impact measurement evidence. The
# # three CROSS-02-02 §6.2 row 5 options (strict_exclusion, dual_feature_path,
# # sensitivity_indicator_co_registration) must all be enumerated in the
# # decision row's `cross_region_policy` field. Verdict = `deferred_blocker`;
# # binding = `deferred_blocker`. MATERIALIZATION BLOCKED until upgraded to
# # `bind_now` in a successor adjudication PR with empirical evidence.
# # Falsifier: `q5_cross_region_three_options_not_enumerated`.

# %% [markdown]
# ## Q6 — Rating reconstruction model family (N3 default deferred; N-X3 evidence gate)
#
# # Hypothesis: rating-algorithm choice (Elo / Glicko / Glicko-2 / TrueSkill
# # / rolling-winrate baseline) cannot be pinned without empirical evaluation
# # of which family handles the unrated / no-rating-history regime best
# # (~83.95% MMR-missing density per the dataset research_log + registry CSV
# # `is_mmr_missing_flag` family). N-X3 strengthens the evidence gate:
# # `evidence_paths` MUST be non-empty even when `deferred_blocker`, and
# # `notes` MUST contain the exact substring `deferred_blocker because:`
# # plus the three forward-only phrases (`no target-match outcome`,
# # `no future results`, `no global batch fit`). Verdict = `deferred_blocker`;
# # binding = `deferred_blocker`. MATERIALIZATION BLOCKED.
# # Falsifiers: `q6_rating_default_deferred_violated`,
# # `q6_rating_forward_only_missing`.

# %% [markdown]
# ## Q7 — IN_GAME_HISTORICAL prior-match aggregation (N1 + N2 canonical strict-`<`)
#
# # Hypothesis: `in_game_history_aggregate` aggregates the 4 IN_GAME_HISTORICAL
# # columns (`APM | SQ | supplyCappedPercent | header_elapsedGameLoops` —
# # exactly `IN_GAME_HISTORICAL_AGGREGATED_COLUMNS`) over PRIOR matches only
# # via the canonical strict-`<` filter (`STRICT_LT_HISTORY_FILTER`).
# # Verdict = `bind_now`; binding = `binding_for_materialization`.
# # `in_game_historical_policy = "prior_match_only_strict_lt"`. No target-
# # match tracker / no target-match game-state consumption.
# # Falsifiers: `q7_in_game_historical_columns_drift` (N1; column set must
# # match deterministic 4-column form), `q7_no_target_match_tracker_missing`,
# # `in_game_historical_strict_lt_violated` (N2), `strict_lt_filter_divergence`
# # (B-X2; the bound expression here also goes through canonical-form check).

# %% [markdown]
# ## Q8 — `matches_history_minimal` consumption (PR #239 ROADMAP-nit promoted)
#
# # Hypothesis: `matches_history_minimal` is consumed for (1) target row
# # identity / `started_at` TIMESTAMP anchor per PR #234 Q2(a) BINDING, AND
# # (2) cold-start enumeration G-CS-2/3/4/5 (the support set of
# # `(focal_player, target.started_at)` target rows). MHM is NOT a feature
# # source — no MHM column becomes a feature column unless this row is
# # updated in a successor PR. Verdict = `ratify_with_evidence`;
# # binding = `binding_for_materialization`.
# # `feature_family_id_or_scope = "NOT_A_FEATURE_SOURCE_unless_explicitly_justified"`.
# # Falsifier: `q8_mhm_documentation_missing`.

# %% [markdown]
# ## Adjudication call — read-only DuckDB + registry + PR #234 binding
#
# This cell invokes the single public entrypoint
# `adjudicate_history_enriched_pre_game_source_layer(...)` against the real
# sc2egset DuckDB (read-only), the closed 02_01_01 registry CSV, and the
# PR #234 tranche-1 adjudication CSV. The entrypoint runs every probe,
# builds the 8 Q-decisions, runs every falsifier in priority order, and
# (only if no falsifier fires) writes the 33-column CSV + §1-§14 MD pair.
# Asserts here re-validate the result and halt the notebook on any
# halting-falsifier-fired condition (halt-before-artifact per
# `.claude/rules/data-analysis-lineage.md`).

# %%
DUCKDB_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
)
REGISTRY_CSV_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
PR234_BINDING_CSV_PATH = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_02_source_anchor_race_adjudication.csv"
)
CSV_PATH = Path(ADJUDICATION_CSV_REL)
MD_PATH = Path(ADJUDICATION_MD_REL)
AUDIT_PR_LABEL = "PR #242"
AUDIT_DATE = "2026-05-24"

# %%
result = adjudicate_history_enriched_pre_game_source_layer(
    duckdb_path=DUCKDB_PATH,
    registry_csv_path=REGISTRY_CSV_PATH,
    pr234_binding_csv_path=PR234_BINDING_CSV_PATH,
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
print(
    "pr241_scaffold_validator_module_sha256:",
    result.pr241_scaffold_validator_module_sha256,
)

assert result.passed is True
assert len(result.decisions) == 8
assert result.halting_falsifier is None
assert result.falsifiers_fired == ()
assert (
    result.pr241_scaffold_validator_module_sha256
    == EXPECTED_PR241_VALIDATOR_SHA256
)

# %% [markdown]
# ## Closing — artifact #3 of N persisted; explicit deferrals
#
# **Persisted (this PR):**
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.csv`
#   (33 columns × 8 rows + 1 header; `materialized_output_paths` is `""` on
#   every row; `pr241_scaffold_validator_module_sha256` equals
#   `EXPECTED_PR241_VALIDATOR_SHA256` on every row).
# - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_source_anchor_coldstart_adjudication.md`
#   (§1 non-overclaim disclaimer · §2-§9 Q1-Q8 with verbatim SQL · §10
#   falsifier roll-call · §11 lineage · §12 explicit non-substitution ·
#   §13 materialization-blocked-until-deferred-resolved · §14 no-Step-closure-claim).
#
# **Explicitly DEFERRED to successor PRs (NOT this PR):**
# - **Q5 cross-region policy** — deferred to a future adjudication PR with
#   retention-measurement evidence; one of the 3 CROSS-02-02 §6.2 row 5
#   options must be pinned before materialization.
# - **Q6 rating reconstruction model family** — deferred to a future
#   adjudication PR with rating-family empirical evaluation evidence
#   satisfying the N-X3 strengthened gate (≥1 repo path + ≥1 citation +
#   forward-only wording + cold-start/missingness wording).
# - **Materialization SQL** (the `_MATERIALIZATION_QUERY` analogue of
#   PR #234's tranche-1 query) — deferred to the future Layer-1 plan PR
#   for the tranche-2 materialization execution.
# - **First Parquet artifact** for the 6 history-enriched families —
#   deferred to the future Layer-2 materialization-execution PR.
# - **Post-materialization CROSS-02-01-v1.0.1 audit JSON+MD** — deferred to
#   the future post-mat audit PR.
# - **Step 02_01_03 closure** (the `02_01_03: complete` row in
#   `STEP_STATUS.yaml` + `research_log` closure entry) — deferred to the
#   future closure PR (analogue of PR #237 for tranche-1).
#
# This notebook does NOT update any `STEP_STATUS.yaml` /
# `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml`. It does NOT append
# any `research_log.md` entry. It does NOT edit `ROADMAP.md`. It does NOT
# patch any spec or cleaning-layer YAML. Phase 03 work and baseline
# modelling remain barred per the existing phase status.
