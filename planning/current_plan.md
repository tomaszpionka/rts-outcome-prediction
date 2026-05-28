---
plan_role: planner-science (Round 3)
plan_model: claude-opus-4-7[1m]
plan_round: 3
round_1_verdict: HOLD
round_1_blockers_count: 4
round_1_nits_count: 11
round_2_verdict: HOLD
round_2_blockers_count: 4
round_2_nits_count: 2
round_3_verdict: APPROVE-WITH-NITS
round_3_blockers_count: 0
round_3_nits_count: 1
round_3_nits_resolved_in_finalization: [R3-NI-B-test-count-floor-harmonized-to-66]
plan_date: 2026-05-28
date: 2026-05-28
plan_layer: 1
chosen_outcome: A
category: A
branch: feat/sc2egset-02-01-03-five-family-materialization
base_ref: 3ab48b3025f17ce62843d7300195e8094c893a72
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_03 (host of five-family history-enriched pre_game materialization)"
non_batching_sequence_position: "Phase 02 materialization execution Layer-1 planning PR following the PR #234/#236 + PR #252/#253 + PR #254/#255 + PR #256/#257 Layer-1/Layer-2 pair precedent. Plans the future Layer-2 11-file execution PR that materialises the five history-enriched pre_game families authorised by PR #257's ROADMAP amendment and emits the FIRST non-vacuous CROSS-02-01 audit over Step 02_01_03 feature columns."
critique_required: true
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
adversarial_round_cap: "3 rounds total (planning-side) per feedback_adversarial_cap_execution.md."
adversarial_cap_symmetry: "Same 3-round cap applies to execution-side review per feedback_adversarial_cap_execution.md."
parent_layer_1_pr: "PR #256 (Step 02_01_03 / 02_01_99 ROADMAP materialization-scope amendment Layer-1; merged at master 2f8a6536)"
parent_layer_2_pr: "PR #257 (Step 02_01_03 / 02_01_99 ROADMAP materialization-scope amendment Layer-2; merged at master 3ab48b30)"
planning_pr: "PR #258"
future_execution_pr: "PR #<TBD-future-Layer-2>"
future_execution_file_count: 11
future_execution_files:
  - "src/rts_predict/games/sc2/datasets/sc2egset/materialize_history_enriched_pre_game_features.py"
  - "tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_history_enriched_pre_game_features.py"
  - "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py"
  - "sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
  - "planning/INDEX.md"
  - "CHANGELOG.md"
  - "pyproject.toml"
future_version_bump: "3.81.0 → 3.82.0"
grep_token: "materialization_scope_amendment_post_pr_255"
five_family_permitted_set:
  - focal_player_history
  - opponent_player_history
  - matchup_history_aggregate
  - cross_region_fragmentation_handling
  - in_game_history_aggregate
excluded_family: reconstructed_rating
excluded_columns:
  - reconstructed_rating_focal_pre
  - reconstructed_rating_opp_pre
  - reconstructed_rating_diff
audited_feature_column_count: 24
parquet_column_count: 28
expected_row_count: 44418
expected_distinct_focal_match_count: 22209
binding_parent_artifacts_count: 17
binding_parent_artifacts:
  - "PR #242 (e372e7b6) — 02_01_03_history_source_anchor_coldstart_adjudication.{csv,md}"
  - "PR #243 (445bae01) — 02_01_03_history_cross_region_adjudication.{csv,md}"
  - "PR #245 (ee15d362) — 02_01_03_history_rating_reconstruction_adjudication.{csv,md}"
  - "PR #247 (779dc40a) — 02_01_03_q6f_rating_algorithm_survey.{csv,md}"
  - "PR #249 (d9276194) — 02_01_03_q6g_rating_implementation_proof.{csv,md}"
  - "PR #251 (28bfc89f) — 02_01_03_q6h_rating_path_decision.{csv,md}"
  - "PR #255 (52f9c108) — 02_01_99_rating_omit_closure.{csv,md}"
  - "Registry CSV — 02_01_01_feature_family_registry.csv"
  - "PR #236 (39298c0a) — 02_01_02_pre_game_features.parquet"
  - "PR #236 (39298c0a) — 02_01_02/leakage_audit_sc2egset.json"
  - "PR #236 (39298c0a) — 02_01_02/leakage_audit_sc2egset.md"
falsifier_count: 41
test_count_floor: 66
halt_predicate_count: 26
hard_stops_layer_1:
  - "Only 2 files in this PR's diff: planning/current_plan.md, planning/current_plan.critique.md."
  - "NO ROADMAP edit, NO pyproject.toml bump, NO CHANGELOG.md edit, NO planning/INDEX.md archive flip."
  - "NO STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml byte change."
  - "NO research_log.md byte change (dataset or root)."
  - "NO spec / cleaning-layer YAML / thesis / docs / .claude / data / notebook / AoE2 byte change."
  - "NO source/test/notebook edit. NO Step 02_01_04. NO Phase 03. NO baseline modelling. NO new Q6X PR. NO merging. NO marking ready."
hard_stops_layer_2:
  - "Exactly 11-file diff: materialization module + mirrored test + overwritten scaffold notebook pair + Parquet artifact + CROSS-02-01 audit JSON+MD + research_log non-closure append + planning/INDEX.md + CHANGELOG + pyproject.toml."
  - "NO STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml row flip or addition (closure deferred to a separate U2.B-style PR per PR #237 precedent)."
  - "NO ROADMAP edit (PR #257 amendment is sufficient)."
  - "NO spec edit (CROSS-02-00/01/02/03 all LOCKED)."
  - "NO cleaning-layer YAML edit."
  - "NO reconstructed_rating family materialization; NO reconstructed_rating_* columns."
  - "NO raw scalar MMR/rating/elo/glicko/skill/mu/sigma feature."
  - "NO tracker_events_raw source read."
  - "NO target-match outcome, NO future-match leakage, NO Phase 03 split leakage, NO global batch fit."
  - "NO matchup CTE history rows from non-1v1 prior matches (restricted via matches_flat_clean join)."
  - "NO Step 02_01_04 / Phase 03 / baseline modelling."
  - "NO Q6X PR / no re-opening of Q5/Q6F/Q6G/Q6H."
  - "NO new branch (single branch shared with Layer-1)."
  - "NO root reports/research_log.md (CROSS entry) edit."
---

# Plan: SC2EGSet Step 02_01_03 five-family materialization (Layer-1, future Layer-2 materialization execution) — ROUND 3 REVISION

## Round 3 revision summary

This Round 3 plan resolves all 4 Round 2 blockers and 2 non-blocking nits via mechanical sweep-revision of the Round 2 plan. **R3-B1 + R3-B2 (NI-1 + NI-5: T02 constants block self-contradiction)** are fixed by rewriting the T02 constants code block to declare `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 24` and `EXPECTED_PARQUET_COLUMN_COUNT: int = 28` directly with the single-source-of-truth comment `# 6 + 6 + 2 + 2 + 8 = 24 (Family 1 + Family 2 + Family 3 + Family 4 + Family 5 per FIVE_FAMILY_CANONICAL_ORDER)`, and by deleting the post-block explainer narrative paragraph that previously corrected `= 30 / = 34` to `= 24 / = 28`. **R3-B3 (NI-6: PR #243 ↔ PR #245 SHA cross-contamination)** is fixed by re-verifying every merge SHA via `gh pr view N --json mergeCommit`; PR #243's actual merge SHA is `445bae0197fa75b613443f8eafef114ff2bb6939` (NOT `ee15d362…`); both T01 line 86 and Literature Context line 904 are corrected to use `445bae01`; PR #245's SHA `ee15d362…` is retained ONLY at PR #245 attributions. All other merge SHAs verified: PR #236=`39298c0a`, PR #237=`a16d78c2`, PR #241=`3c6709bf`, PR #242=`e372e7b6`, PR #245=`ee15d362`, PR #247=`779dc40a`, PR #249=`d9276194`, PR #251=`28bfc89f`, PR #255=`52f9c108`, PR #257=`3ab48b30`. **R3-B4 (Round 2 revision summary + File Manifest count contradictions)** is fixed by sweep-replacing `30 audited → 24 audited`, `34 cols → 28 cols`, `features_audited_count: 30 → features_audited_count: 24`, `from 18 to 30 → from 18 to 24`, and the Round 2 revision summary line 11 reference to `30` for `features_audited_count`. **R3-N1 (NI-7: 16 vs 17 SHA count)** is resolved by enumerating PR #236 tranche-1 as THREE separate SHA pins (`pr236_tranche1_parquet_sha256`, `pr236_tranche1_audit_json_sha256`, `pr236_tranche1_audit_md_sha256`); BINDING parent SHA count is reconciled to **17 everywhere** (12 Q-chain + 2 omit-closure + 1 registry + 3 tranche-1 = 17); A13, S2, L7, OQ4, T01, and dispatch instructions all updated. **R3-N2** is addressed by adding a single audit MD §2 note: `matches_long_raw_yaml_sha256` is a defensive lineage-completeness pin (not a read-source pin), retained to detect future drift if a later revision joins this view. **Round 3 final-pass non-blocking nit NI-B (test-count floor inconsistency 60/63/66) is harmonized by the parent at materialization time: all `≥60 tests` / `≥60 named test cases` / `≥63 named test cases` references are swept to `≥66 named test cases` to match T05's actual enumeration. All Round 1 and Round 2 fixes are preserved**: 11-file Layer-2 diff, matchup CTE 1v1-restriction, research_log inclusion, PR #245 in the pin list, FIVE_FAMILY_CANONICAL_ORDER tuple, PR #255 q5_policy elevation, 24-column subfeature widening, custom_extensions section, join-then-filter test, audit_date pinning, notebook overwrite, Invariant I5 citation, `is_decisive_result` usage. All eight required `##` sections preserved; Outcome A, strict-<, `reconstructed_rating` exclusion, five-family vocabulary, deferred-closure pattern, branch slug, and `3.81.0 → 3.82.0` preserved.

---

## Scope

This is a **Layer-1 planning PR (Category A)** that authors exactly two planning files and zero repo edits. It plans a **future Layer-2 execution PR** that materialises the five history-enriched pre_game feature families authorised by PR #257's ROADMAP amendment, persists the FIRST non-vacuous CROSS-02-01-v1.0.1 §3 audit pair over Step `02_01_03`'s feature columns, appends a non-closure dataset `research_log.md` entry mirroring PR #236's precedent, and bumps `3.81.0 → 3.82.0`.

**This Layer-1 PR diff (exactly 2 files):**

- `planning/current_plan.md` — this plan body.
- `planning/current_plan.critique.md` — reviewer-adversarial critique log (Rounds 1–3 within the 3-round cap).

**The future Layer-2 execution PR diff (exactly 11 files; planned, NOT created in this PR; PR #236 precedent verified via `git show 51288130 --stat` = 11 files):**

1. `src/rts_predict/games/sc2/datasets/sc2egset/materialize_history_enriched_pre_game_features.py` — materialisation + audit module.
2. `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_history_enriched_pre_game_features.py` — mirrored test file (≥66 tests; ≥95% branch coverage on the new module).
3. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` — jupytext source (existing scaffold notebook **overwritten in place** per `sandbox/README.md` notebook contract; single-notebook lineage; PR #241 scaffold content remains in git history).
4. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb` — paired notebook with cleared outputs (overwritten).
5. `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet` — five-family feature artifact (one Parquet file; **44,418 rows × 28 cols = 3 identity + 1 context + 24 audited features**).
6. `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json` — non-vacuous CROSS-02-01 audit JSON.
7. `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md` — sibling MD per CROSS-02-01-v1.0.1 §3.
8. `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` — append one new entry mirroring the PR #236 30-line precedent (`closure_status: still_open`; `materialization_state: materialized`; `leakage_audit_state: post_materialization_pass`; **`features_audited_count: 24`**; `row_count: 44418`; `artifact` + `leakage_audit` field labels verbatim from PR #236 diff).
9. `planning/INDEX.md` — archive Layer-1 + Layer-2 rows.
10. `CHANGELOG.md` — new `[3.82.0]` section + reset `[Unreleased]`.
11. `pyproject.toml` — version `3.81.0 → 3.82.0`.

**Branch (this Layer-1 PR AND the future Layer-2 PR):** `feat/sc2egset-02-01-03-five-family-materialization` (matches PR #257 amendment's `Forward path` annotation at ROADMAP.md:2616-2617; two PRs share the branch per PR #234/#236, PR #240/#241, PR #244/#245, PR #252/#253, PR #254/#255, PR #256/#257 precedent).

**Phase/Step ref:** Phase 02 — Feature Engineering / Pipeline Section 02_01 — Pre-Game vs In-Game Boundary / Step `02_01_03`. No new Step number is created. **No Step is closed.** Closure is deferred to a separate future U2.B-style PR (mirroring PR #237 closing PR #236 for Step `02_01_02`).

**Category:** A — Phase 02 materialization execution planning.

**Expected future version bump:** `3.81.0 → 3.82.0` (minor; feat-family per `.claude/rules/git-workflow.md` and the PR #236 materialization precedent which bumped `3.69.0 → 3.70.0`).

**Hard stops this Layer-1 PR respects:**

- Only 2 files in this PR's diff: `planning/current_plan.md`, `planning/current_plan.critique.md`.
- NO ROADMAP edit, NO `pyproject.toml` bump, NO `CHANGELOG.md` edit, NO `planning/INDEX.md` archive flip, NO status YAML flip, NO `research_log` edit (dataset or root), NO spec edit, NO cleaning-layer YAML edit, NO source / test / notebook / artifact / sandbox / `data/` touch, NO Step `02_01_04` start, NO Phase 03 start, NO baseline modelling, NO Q6X PR, NO merging, NO marking ready, NO AoE2 edits, NO docs / `.claude` / thesis edits.

**Hard stops the future Layer-2 PR respects:**

- Exactly 11-file diff above; no twelfth file.
- NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` row flip or addition (closure is deferred per PR #237 precedent).
- The single dataset `research_log.md` entry MUST be a non-closure append per PR #236 precedent (`closure_status: still_open`); MUST NOT flip `closure_status: closed`.
- NO ROADMAP edit (the PR #257 amendment is sufficient; this PR consumes the amendment).
- NO spec edit (CROSS-02-00 / CROSS-02-01 / CROSS-02-02 / CROSS-02-03 are LOCKED).
- NO cleaning-layer YAML edit.
- NO five-family scope drift (`reconstructed_rating` MUST NOT be materialised; the three excluded columns MUST NOT appear).
- NO target-match outcome, NO future-match outcome, NO Phase 03 split leakage (per Invariant I3 + ml-protocol three failure modes).
- NO global batch fit (per-target leakage-safe aggregation only).
- NO raw scalar MMR feature (the `is_mmr_missing` missingness flag is the only MMR-derived feature permitted; raw `mmr` / `rating` / `elo` / `glicko` / `skill` / `mu` / `sigma` token in column names is forbidden per PR #236's `FORBIDDEN_SKILL_TOKENS` precedent).
- NO tracker-derived target-match features (Invariant I3; Amendment 2 of PR #208).
- NO Step `02_01_04` / Phase 03 / baseline modelling.
- NO Q6X PR / no re-opening of Q5/Q6F/Q6G/Q6H.
- NO new branch (single branch shared with Layer-1).
- NO matchup CTE history rows that come from non-1v1 prior matches (B2 fix: restrict to 1v1 via `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`).
- NO root `reports/research_log.md` (CROSS entry) edit — single-dataset scope.

---

## Execution Steps

These are the planned Layer-2 execution tasks (T01 … T08) that the future eleven-file PR will run. This Layer-1 planning PR itself does not execute any of them.

### T01 — Pre-execution verification (READ-ONLY; pinned SHA assertions)

- Verify `master HEAD` is the merge commit of this Layer-1 PR (Layer-2 begins AFTER Layer-1 merges).
- Verify `pyproject.toml` version is `3.81.0` (Layer-2 will bump to `3.82.0`).
- Verify ROADMAP amendment is intact: `grep -c "materialization_scope_amendment_post_pr_255" ROADMAP.md` returns `>=4` (heading line 2525, comment line 2527, back-reference heading 2837, back-reference comment 2839). The amendment's five-family list at ROADMAP.md:2536-2540 must match exactly; the three excluded column names at ROADMAP.md:2546-2548 must match exactly.

**SHA-pin each of the 17 BINDING parent artifacts (R3-N1 reconciliation; arithmetic now: 6 Q-chain PRs × 2 artifacts each = 12, PLUS 1 registry CSV, PLUS 1 tranche-1 Parquet, PLUS 1 tranche-1 audit JSON, PLUS 1 tranche-1 audit MD = 17):**

- Q-chain parent artifacts (12; one CSV + one MD per PR; six PRs):
  - **PR #242** (merged 2026-05-24 at `e372e7b66be66b6026fb3bc39f51d1975da0b8b1`): `02_01_03_history_source_anchor_coldstart_adjudication.csv` (`parent_pr242_csv_sha256 = f2a169ec…`) + `.md` (`parent_pr242_md_sha256 = fdaa7d6d…`) — binds Q1 source layer, Q2 anchor, Q3 strict-< filter, Q4 cold-start gates, Q7 IN_GAME_HISTORICAL aggregation, Q8 MHM consumption.
  - **PR #243** (merged 2026-05-25 at `445bae0197fa75b613443f8eafef114ff2bb6939` per `gh pr view 243 --json mergeCommit`): `02_01_03_history_cross_region_adjudication.csv` (`parent_pr243_csv_sha256 = 29d39522…`) + `.md` (`parent_pr243_md_sha256 = 026deda3…`) — binds Q5_selected_policy = `sensitivity_indicator_co_registration`. **(R3-B3 fix: SHA corrected from incorrect `ee15d362…` to PR #243's actual merge SHA `445bae01…`.)**
  - **PR #245** (merged 2026-05-25 at `ee15d3625eee60688776219f533d4a5ceefb4b76` per `gh pr view 245 --json mergeCommit`): `02_01_03_history_rating_reconstruction_adjudication.csv` (`parent_pr245_csv_sha256 = 703c9153…`) + `.md` (`parent_pr245_md_sha256 = 7efea247…`) — Q6 rating-reconstruction successor adjudication. The row in PR #255 omit-closure CSV referencing `parent_pr245_csv_sha256` / `parent_pr245_md_sha256` proves PR #245 is a binding Q-chain parent (B4 fix preserved).
  - **PR #247** (merged 2026-05-25 at `779dc40a36765d90034181fc3885ea32cab204e6`): `02_01_03_q6f_rating_algorithm_survey.csv` (`parent_pr247_csv_sha256 = 249e5591…`) + `.md` (`parent_pr247_md_sha256 = 4b49bee4…`) — Q6F rating-algorithm survey (carry-forward; reconstructed_rating omitted).
  - **PR #249** (merged 2026-05-26 at `d9276194a1684542a04494ec02df44a5a3f2338e`): `02_01_03_q6g_rating_implementation_proof.csv` (`parent_pr249_csv_sha256 = 1d9ee22e…`) + `.md` (`parent_pr249_md_sha256 = 8beed3ba…`) — Q6G implementation proof (carry-forward).
  - **PR #251** (merged 2026-05-26 at `28bfc89fae56e88bd4c039077d7971496d5f1b1c`): `02_01_03_q6h_rating_path_decision.csv` (`parent_pr251_csv_sha256 = 8b8b9575…`) + `.md` (`parent_pr251_md_sha256 = 5186e356…`) — Q6H path decision (carry-forward).
- Omit-closure (PR #255, merged 2026-05-28 at `52f9c1082b200019d080cce74e60567452020e18`): `02_01_99_rating_omit_closure.csv` + `02_01_99_rating_omit_closure.md` — the verdict `omit_reconstructed_rating_and_unblock_other_five` and `q5_policy = sensitivity_indicator_co_registration` are the direct authorisations for this PR (N2 fix; `q5_policy` field is the explicit BINDING elevation).
- Registry source-of-truth: `02_01_01_feature_family_registry.csv` (registry CSV pinned by PR #236 audit as `registry_csv_sha256 = 320b8b01…`).
- Tranche-1 artifacts (PR #236, merged 2026-05-23 at `39298c0afd3a23bfbd4603415314af784a672952`; **R3-N1: enumerated as THREE SHA pins**): `02_01_02_pre_game_features.parquet` (`pr236_tranche1_parquet_sha256 = 24db73fb…`) + `02_01_02/leakage_audit_sc2egset.json` (`pr236_tranche1_audit_json_sha256`) + `02_01_02/leakage_audit_sc2egset.md` (`pr236_tranche1_audit_md_sha256`) — consumed as audit-schema template; PR #236 audit MD inspected at the canonical path.

Layer-2 halts on any SHA drift.

- SHA-pin the four DuckDB view YAMLs read by the materialisation SQL:
  - `data/db/schemas/views/matches_flat_clean.yaml` (Q1 selected target source layer; ALSO used as 1v1 history-restriction join in matchup CTE per B2 fix).
  - `data/db/schemas/views/matches_history_minimal.yaml` (Q2 target anchor source).
  - `data/db/schemas/views/player_history_all.yaml` (Q1 selected history source layer; verified to expose `is_decisive_result` BOOLEAN at line 48–54 per N11).
  - `data/db/schemas/views/matches_long_raw.yaml` (NOT joined by default; SHA-pinned defensively per R3-N2 — documented in audit MD §2 as a lineage-completeness pin to detect future drift if a later revision joins this view).
- SHA-pin the four CROSS-02-** specs (all LOCKED): `02_00_feature_input_contract.md`, `02_01_leakage_audit_protocol.md`, `02_02_feature_engineering_plan.md`, `02_03_temporal_feature_audit_protocol.md`.

### T02 — Author `materialize_history_enriched_pre_game_features.py` (in-memory; no write yet)

The module mirrors the PR #236 `materialize_pre_game_features.py` template (frozen dataclasses, `_QUERY`-suffixed module-level SQL constants, per-falsifier `_check_*` helpers, named falsifier labels, deterministic SHA-256 lineage record). The function signatures below MUST be implemented:

```python
def materialize_five_family_history_features(
    db_path: Path,
    output_parquet_path: Path,
    cross_region_policy: str,
) -> MaterializationResult: ...

def audit_five_family_history_features(
    result: MaterializationResult,
    audit_json_path: Path,
    audit_md_path: Path,
) -> AuditResult: ...

def run_step_02_01_03(
    db_path: Path,
    output_parquet_path: Path,
    audit_json_path: Path,
    audit_md_path: Path,
) -> tuple[MaterializationResult, AuditResult]: ...
```

Module-level constants (Invariant I7; module-level UPPER_SNAKE; no magic numbers):

```python
DATASET_TAG: str = "sc2egset"
PHASE_02_STEP: str = "02_01_03"
SPEC_VERSION: str = "CROSS-02-01-v1"

# Five-family permitted set (verbatim from PR #257 ROADMAP amendment lines 2536-2540
# and PR #255 omit-closure CSV `five_family_set` column).
# N1 fix: frozenset for membership checks PLUS tuple for ordered display/audit.
FIVE_FAMILY_PERMITTED_SET: frozenset[str] = frozenset({
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "cross_region_fragmentation_handling",
    "in_game_history_aggregate",
})
FIVE_FAMILY_CANONICAL_ORDER: tuple[str, ...] = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "cross_region_fragmentation_handling",
    "in_game_history_aggregate",
)
FIVE_FAMILY_PERMITTED_COUNT: int = 5

# Excluded family + columns (verbatim from PR #257 amendment lines 2542-2548
# and PR #255 `excluded_columns` field).
EXCLUDED_FAMILY: str = "reconstructed_rating"
FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS: frozenset[str] = frozenset({
    "reconstructed_rating_focal_pre",
    "reconstructed_rating_opp_pre",
    "reconstructed_rating_diff",
})

# Forbidden skill scalars (mirrors PR #236 module constant; reused).
FORBIDDEN_SKILL_TOKENS: frozenset[str] = frozenset(
    {"mmr", "rating", "elo", "glicko", "skill", "mu", "sigma"}
)
APPROVED_MMR_MISSINGNESS_TOKENS: frozenset[str] = frozenset(
    {"is_mmr_missing", "focal_is_mmr_missing", "opponent_is_mmr_missing"}
)

# Cross-region policy (PR #243 Q5 selected_policy + PR #255 q5_policy field elevation;
# N2 fix: PR #255 omit-closure CSV's `q5_policy` column explicitly re-elevates the
# selected_policy to BINDING in the omit-closure context, beyond the byte-unchanged
# transitive argument).
CROSS_REGION_POLICY: str = "sensitivity_indicator_co_registration"

# IN_GAME_HISTORICAL columns retained for prior-match aggregation per Q7
# (PR #242 row Q7 in_game_historical_columns_in_scope = APM|SQ|supplyCappedPercent|header_elapsedGameLoops).
IN_GAME_HISTORICAL_AGGREGATED_COLUMNS: tuple[str, ...] = (
    "APM", "SQ", "supplyCappedPercent", "header_elapsedGameLoops",
)

# POST_GAME tokens (CROSS-02-01-v1.0.1 §2.2 boundary-aware token equality).
POST_GAME_TOKENS: frozenset[str] = frozenset({
    "won", "win", "loss", "result", "outcome", "winner",
    "final_state", "match_result", "post_game", "is_decisive",
})

# Source-table allowlist (Q1 BINDING; no tracker source).
ALLOWED_SOURCE_TABLES: frozenset[str] = frozenset(
    {"matches_flat_clean", "matches_history_minimal", "player_history_all"}
)
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"

# Expected row counts (PR #236 precedent; verified via tranche-1 audit JSON
# row_count=44418, distinct_focal_match_count=22209).
EXPECTED_OUTPUT_ROW_COUNT: int = 44_418
EXPECTED_DISTINCT_FOCAL_MATCH_COUNT: int = 22_209

# Sub-feature enumeration (N4/N10 fix: widen to CROSS-02-02 §6.2 row 1 verbatim
# 6-tuple per history side; reviewer-deep can subset at Phase 03 selection).
FOCAL_PLAYER_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "focal_prior_match_count",
    "focal_prior_win_rate_decisive",
    "focal_days_since_prior_match",
    "focal_prior_win_rate_race_conditional",
    "focal_prior_win_rate_map_conditional",
    "focal_prior_win_rate_matchup_conditional",
)
OPPONENT_PLAYER_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "opponent_prior_match_count",
    "opponent_prior_win_rate_decisive",
    "opponent_days_since_prior_match",
    "opponent_prior_win_rate_race_conditional",
    "opponent_prior_win_rate_map_conditional",
    "opponent_prior_win_rate_matchup_conditional",
)
MATCHUP_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "matchup_h2h_count",
    "matchup_h2h_focal_win_rate",
)
CROSS_REGION_SUBFEATURES: tuple[str, ...] = (
    "is_cross_region_fragmented_focal_history_any",
    "is_cross_region_fragmented_opponent_history_any",
)
IN_GAME_HISTORY_SUBFEATURES: tuple[str, ...] = (
    "focal_apm_prior_mean",
    "focal_sq_prior_mean",
    "focal_supply_capped_pct_prior_mean",
    "focal_elapsed_game_loops_prior_mean",
    "opponent_apm_prior_mean",
    "opponent_sq_prior_mean",
    "opponent_supply_capped_pct_prior_mean",
    "opponent_elapsed_game_loops_prior_mean",
)

# R3-B1 + R3-B2 FIX: single source of truth, 5 family terms summing to 24.
# Verification: 6 + 6 + 2 + 2 + 8 = 24 audited; 3 identity + 1 context + 24 audited = 28 parquet cols.
EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 24  # 6 + 6 + 2 + 2 + 8 = 24 (Family 1 + Family 2 + Family 3 + Family 4 + Family 5 per FIVE_FAMILY_CANONICAL_ORDER)
EXPECTED_PARQUET_COLUMN_COUNT: int = 28          # 3 identity + 1 context + 24 audited
```

T02 will additionally derive both constants from `len(FOCAL_PLAYER_HISTORY_SUBFEATURES) + len(OPPONENT_PLAYER_HISTORY_SUBFEATURES) + len(MATCHUP_HISTORY_SUBFEATURES) + len(CROSS_REGION_SUBFEATURES) + len(IN_GAME_HISTORY_SUBFEATURES)` at module-load time and assert equality with `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT == 24`, and `EXPECTED_PARQUET_COLUMN_COUNT == 24 + 3 + 1 == 28`.

### T03 — Author the per-family SQL (verbatim text below; Invariant I6)

The five SQL modules are independent CTEs joined into a single `_MATERIALIZATION_QUERY`. All five honour:

- Q1 source layer: `matches_flat_clean` for the target row; `player_history_all` for history-side rows (PR #242 Q1 BINDING).
- Q1 1v1 restriction for matchup CTE (B2 fix): the matchup CTE adds `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id` so the shared-replay self-join is restricted to 1v1 historical matches. The per-player win-rate CTEs (focal + opponent) deliberately aggregate ALL game types per Q1 BINDING and document the cross-game-type aggregation in audit MD §1 as a deliberate consequence.
- Q2 target anchor: `matches_history_minimal.started_at` TIMESTAMP (PR #242 Q2 BINDING).
- Q3 history time column: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP)` (PR #242 Q3 BINDING; canonical TRY_CAST per B-X2).
- Q4 cold-start gates: G-CS-2/3/4/5 at the registry layer; G-CS-6 is materialization-time fold-aware (DEFERRED to Phase 03; this PR's pre-materialization aggregates use no fold-aware fit).
- Q5 cross-region policy: `sensitivity_indicator_co_registration` (PR #243 Q5_selected_policy BINDING + PR #255 `q5_policy` re-elevation per N2) — co-registers BOTH `is_cross_region_fragmented_focal_history_any` AND `is_cross_region_fragmented_opponent_history_any` BOOLEAN flags per Invariant I5 symmetry (N9: cited explicitly in audit MD §1 as the methodological justification for going beyond PR #243's single-indicator text).
- Q7 IN_GAME_HISTORICAL: prior-match aggregation only; never target-match values; only the four columns APM/SQ/supplyCappedPercent/header_elapsedGameLoops (PR #242 Q7 BINDING).
- Q8 MHM consumption: target row identity + started_at anchor + cold-start enumeration only; NEVER as a feature source (PR #242 Q8 BINDING).
- N11: use `ph.is_decisive_result = TRUE` instead of inline `ph.result IN ('Win', 'Loss')` (verified to exist as BOOLEAN at `player_history_all.yaml:48`).

**Verbatim materialization SQL (planned; placed in module constant `_MATERIALIZATION_QUERY`):**

```sql
WITH mfc_focal AS (
    -- Target row: focal player row from matches_flat_clean (Q1 BINDING; 1v1-scoped).
    SELECT mfc.replay_id AS focal_replay_id, mfc.toon_id AS focal_toon_id,
           mfc.race AS focal_race, mfc.metadata_mapName AS focal_map_name
    FROM matches_flat_clean mfc
),
mfc_opponent AS (
    SELECT mfc.replay_id AS opp_replay_id, mfc.toon_id AS opponent_toon_id,
           mfc.race AS opponent_race
    FROM matches_flat_clean mfc
),
mfc_paired AS (
    SELECT f.focal_replay_id, f.focal_toon_id, o.opponent_toon_id,
           f.focal_race, o.opponent_race, f.focal_map_name
    FROM mfc_focal f
    JOIN mfc_opponent o
        ON f.focal_replay_id = o.opp_replay_id
       AND f.focal_toon_id <> o.opponent_toon_id
),
mhm_anchor AS (
    SELECT match_id, player_id, started_at
    FROM matches_history_minimal
),
targets AS (
    SELECT CONCAT('sc2egset::', p.focal_replay_id) AS focal_match_id,
           p.focal_toon_id AS focal_player,
           p.opponent_toon_id AS opponent_player,
           p.focal_race, p.opponent_race, p.focal_map_name,
           a.started_at
    FROM mfc_paired p
    JOIN mhm_anchor a
        ON a.match_id = CONCAT('sc2egset::', p.focal_replay_id)
       AND a.player_id = p.focal_toon_id
),
-- Family 1: focal_player_history — CROSS-02-02 §6.2 row 1 verbatim 6-tuple.
-- N4/N10 fix: widen from 3 to 6 sub-features per CROSS-02-02 §6.2 row 1 verbatim
-- enumeration "prior match count, prior win rate, time since prior match,
-- race-conditional win rate, map-conditional win rate, matchup-conditional win rate".
focal_player_history AS (
    SELECT t.focal_match_id, t.focal_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS focal_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS focal_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.focal_race)
            AS focal_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS focal_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_opp_h
                          WHERE ph_opp_h.replay_id = ph.replay_id
                            AND ph_opp_h.toon_id <> ph.toon_id
                            AND ph_opp_h.race = t.opponent_race))
            AS focal_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.focal_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
-- Family 2: opponent_player_history — symmetric mirror per Invariant I5.
opponent_player_history AS (
    SELECT t.focal_match_id, t.opponent_player,
        COUNT(*) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_prior_match_count,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE)
            AS opponent_prior_win_rate_decisive,
        DATE_DIFF('day',
            MAX(TRY_CAST(ph.details_timeUTC AS TIMESTAMP))
                FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at),
            t.started_at) AS opponent_days_since_prior_match,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.race = t.opponent_race)
            AS opponent_prior_win_rate_race_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND ph.metadata_mapName = t.focal_map_name)
            AS opponent_prior_win_rate_map_conditional,
        AVG(CASE WHEN ph.result = 'Win' THEN 1.0 WHEN ph.result = 'Loss' THEN 0.0 END)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at
                      AND ph.is_decisive_result = TRUE
                      AND EXISTS (
                          SELECT 1 FROM player_history_all ph_focal_h
                          WHERE ph_focal_h.replay_id = ph.replay_id
                            AND ph_focal_h.toon_id <> ph.toon_id
                            AND ph_focal_h.race = t.focal_race))
            AS opponent_prior_win_rate_matchup_conditional
    FROM targets t
    LEFT JOIN player_history_all ph
        ON ph.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.opponent_player, t.started_at,
             t.focal_race, t.opponent_race, t.focal_map_name
),
-- Family 3: matchup_history_aggregate — head-to-head 1v1-restricted (B2 FIX).
-- The shared-replay self-join is restricted to 1v1 prior matches via
-- JOIN matches_flat_clean mfc_h: this prevents 4v4/3v3/2v2 teammate-or-opponent
-- shared matches from inflating the head-to-head count.
matchup_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player, t.opponent_player,
        COUNT(*) FILTER (
            WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
              AND ph_focal.replay_id = ph_opp.replay_id
        ) AS matchup_h2h_count,
        AVG(CASE WHEN ph_focal.result = 'Win' THEN 1.0
                 WHEN ph_focal.result = 'Loss' THEN 0.0 END)
            FILTER (
                WHERE TRY_CAST(ph_focal.details_timeUTC AS TIMESTAMP) < t.started_at
                  AND ph_focal.replay_id = ph_opp.replay_id
                  AND ph_focal.is_decisive_result = TRUE
            ) AS matchup_h2h_focal_win_rate
    FROM targets t
    LEFT JOIN player_history_all ph_focal
        ON ph_focal.toon_id = t.focal_player
    LEFT JOIN player_history_all ph_opp
        ON ph_opp.toon_id = t.opponent_player
       AND ph_opp.replay_id = ph_focal.replay_id
    -- B2 FIX: restrict matchup history to 1v1 prior matches by joining
    -- matches_flat_clean (which is 1v1-scoped per Q1 BINDING).
    LEFT JOIN matches_flat_clean mfc_h
        ON mfc_h.replay_id = ph_focal.replay_id
       AND mfc_h.toon_id   = ph_focal.toon_id
    GROUP BY t.focal_match_id, t.focal_player, t.opponent_player, t.started_at
),
-- Family 4: cross_region_fragmentation_handling — Q5 sensitivity-indicator,
-- symmetric per Invariant I5 (N9 fix: explicit I5 citation in audit MD §1).
cross_region_fragmentation_handling AS (
    SELECT t.focal_match_id, t.focal_player,
        BOOL_OR(ph.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_focal_history_any,
        BOOL_OR(ph2.is_cross_region_fragmented)
            FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS is_cross_region_fragmented_opponent_history_any
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
),
-- Family 5: in_game_history_aggregate — Q7 BINDING; only the 4-column tuple
-- (APM/SQ/supplyCappedPercent/header_elapsedGameLoops); strictly-prior only.
in_game_history_aggregate AS (
    SELECT t.focal_match_id, t.focal_player,
        AVG(ph.APM) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_apm_prior_mean,
        AVG(ph.SQ) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_sq_prior_mean,
        AVG(ph.supplyCappedPercent) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_supply_capped_pct_prior_mean,
        AVG(ph.header_elapsedGameLoops) FILTER (WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS focal_elapsed_game_loops_prior_mean,
        AVG(ph2.APM) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_apm_prior_mean,
        AVG(ph2.SQ) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_sq_prior_mean,
        AVG(ph2.supplyCappedPercent) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_supply_capped_pct_prior_mean,
        AVG(ph2.header_elapsedGameLoops) FILTER (WHERE TRY_CAST(ph2.details_timeUTC AS TIMESTAMP) < t.started_at)
            AS opponent_elapsed_game_loops_prior_mean
    FROM targets t
    LEFT JOIN player_history_all ph  ON ph.toon_id  = t.focal_player
    LEFT JOIN player_history_all ph2 ON ph2.toon_id = t.opponent_player
    GROUP BY t.focal_match_id, t.focal_player, t.started_at
)
SELECT
    -- 3 identity columns (PR #236 precedent).
    t.focal_match_id, t.focal_player, t.opponent_player,
    -- 1 context anchor column (started_at; CONTEXT; EXCLUDED from features_audited).
    t.started_at,
    -- Family 1: focal_player_history (6 columns).
    fph.focal_prior_match_count, fph.focal_prior_win_rate_decisive, fph.focal_days_since_prior_match,
    fph.focal_prior_win_rate_race_conditional, fph.focal_prior_win_rate_map_conditional,
    fph.focal_prior_win_rate_matchup_conditional,
    -- Family 2: opponent_player_history (6 columns).
    oph.opponent_prior_match_count, oph.opponent_prior_win_rate_decisive, oph.opponent_days_since_prior_match,
    oph.opponent_prior_win_rate_race_conditional, oph.opponent_prior_win_rate_map_conditional,
    oph.opponent_prior_win_rate_matchup_conditional,
    -- Family 3: matchup_history_aggregate (2 columns; 1v1-restricted history).
    mha.matchup_h2h_count, mha.matchup_h2h_focal_win_rate,
    -- Family 4: cross_region_fragmentation_handling (2 columns; Invariant I5 symmetric).
    crfh.is_cross_region_fragmented_focal_history_any,
    crfh.is_cross_region_fragmented_opponent_history_any,
    -- Family 5: in_game_history_aggregate (8 columns; Q7 4-tuple × 2 sides).
    ighp.focal_apm_prior_mean, ighp.focal_sq_prior_mean,
    ighp.focal_supply_capped_pct_prior_mean, ighp.focal_elapsed_game_loops_prior_mean,
    ighp.opponent_apm_prior_mean, ighp.opponent_sq_prior_mean,
    ighp.opponent_supply_capped_pct_prior_mean, ighp.opponent_elapsed_game_loops_prior_mean
FROM targets t
LEFT JOIN focal_player_history             fph  USING (focal_match_id, focal_player)
LEFT JOIN opponent_player_history          oph  USING (focal_match_id, opponent_player)
LEFT JOIN matchup_history_aggregate        mha  USING (focal_match_id, focal_player, opponent_player)
LEFT JOIN cross_region_fragmentation_handling crfh USING (focal_match_id, focal_player)
LEFT JOIN in_game_history_aggregate        ighp USING (focal_match_id, focal_player)
ORDER BY t.started_at, t.focal_match_id, t.focal_player
```

**Output projection: 28 columns total = 3 identity + 1 context anchor (`started_at`) + 24 audited feature columns** (Family 1: 6, Family 2: 6, Family 3: 2, Family 4: 2, Family 5: 8). Expected row count: **44,418** (same as PR #236 `EXPECTED_MFC_ROW_COUNT`). `features_audited` must equal the 24-column tuple exactly (NO `started_at`, NO identity columns).

### T04 — Implement falsifiers (verbatim labels; first to fire halts)

Falsifier-priority chain — structural drift errors win over per-row content errors:

```
F-five-family-count-drift
F-five-family-set-drift
F-five-family-canonical-order-drift           # N1 fix: tuple-order mismatch with FIVE_FAMILY_CANONICAL_ORDER
F-reconstructed-rating-column-present
F-reconstructed-rating-token-leak
F-forbidden-skill-scalar-projected
F-row-count-mismatch                          # COUNT(*) != EXPECTED_OUTPUT_ROW_COUNT (44,418)
F-focal-rows-per-match-violation              # any focal_match_id has count != 2
F-symmetry-violation
F-strict-lt-operator-missing
F-equal-lt-operator-used
F-try-cast-missing
F-tracker-source-read
F-target-match-row-in-history                 # JOIN admits target row; FILTER excludes it
F-join-then-filter-invariant-violation        # N6 fix: target row IS in JOIN result, MUST be excluded by FILTER
F-post-game-token-projected
F-cross-region-policy-mismatch
F-cross-region-history-row-dropped
F-in-game-historical-column-out-of-scope
F-null-feature-non-cold-start
F-stale-output-path
F-pr257-amendment-grep-missing
F-q5-binding-sha-mismatch
F-q6h-binding-sha-mismatch
F-pr245-binding-sha-mismatch                  # B4 fix: PR #245 csv+md SHA drift halts
F-omit-closure-sha-mismatch
F-features-audited-empty
F-features-audited-not-twenty-four            # N4/N10 fix: count is now 24
F-features-audited-count-mismatch
F-context-column-counted-as-feature
F-audit-verdict-not-pass
F-encoder-fit-at-materialization-layer
F-examiner-clarity-sentence-missing
F-non-deterministic-output
F-q-chain-parent-bytes-drift                  # any of 12 Q-chain parent artifact SHAs differs
F-cross-02-spec-bytes-drift
F-view-yaml-bytes-drift
F-feature-column-not-in-permitted-family
F-reconstructed-rating-family-materialised
F-omit-closure-verdict-text-drift
F-target-match-final-state-read
F-future-match-leak
F-phase-03-split-leak
F-matchup-cte-includes-non-1v1-history        # B2 fix
F-matchup-bias-documentation-missing          # B2 partial-b fix
F-decisive-result-flag-not-used               # N11 fix
F-research-log-entry-missing                  # B1/B3 fix
F-research-log-closure-status-not-still-open  # B3 fix
F-pr236-precedent-field-labels-missing        # B3 fix
F-pr236-tranche1-md-sha-mismatch              # R3-N1: third tranche-1 SHA pin
```

Falsifier `F-features-audited-not-twenty-four`: the audit's `features_audited` list MUST equal the exact 24-tuple in T03 projection order:

```
focal_prior_match_count, focal_prior_win_rate_decisive, focal_days_since_prior_match,
focal_prior_win_rate_race_conditional, focal_prior_win_rate_map_conditional, focal_prior_win_rate_matchup_conditional,
opponent_prior_match_count, opponent_prior_win_rate_decisive, opponent_days_since_prior_match,
opponent_prior_win_rate_race_conditional, opponent_prior_win_rate_map_conditional, opponent_prior_win_rate_matchup_conditional,
matchup_h2h_count, matchup_h2h_focal_win_rate,
is_cross_region_fragmented_focal_history_any, is_cross_region_fragmented_opponent_history_any,
focal_apm_prior_mean, focal_sq_prior_mean, focal_supply_capped_pct_prior_mean, focal_elapsed_game_loops_prior_mean,
opponent_apm_prior_mean, opponent_sq_prior_mean, opponent_supply_capped_pct_prior_mean, opponent_elapsed_game_loops_prior_mean.
```

### T05 — Write the mirrored test file (≥95% branch coverage)

`tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_history_enriched_pre_game_features.py` must implement, at minimum, the following named test cases (one test per falsifier, plus integration tests):

```
test_module_constants_match_pr257_amendment_verbatim
test_five_family_permitted_set_count_is_five
test_five_family_permitted_set_excludes_reconstructed_rating
test_five_family_canonical_order_matches_pr257_amendment_order            # N1
test_excluded_columns_are_three_named_strings
test_forbidden_reconstructed_rating_token_rejected_in_column_names
test_cross_region_policy_is_sensitivity_indicator_co_registration
test_cross_region_policy_pr255_q5_policy_field_matches                    # N2
test_q7_in_game_historical_columns_are_apm_sq_supply_loops_tuple
test_post_game_token_set_matches_pr236_precedent
test_forbidden_skill_tokens_set_matches_pr236_precedent
test_strict_lt_operator_present_in_each_history_cte
test_no_lte_or_eq_operator_in_any_history_cte
test_try_cast_present_in_each_history_filter
test_no_tracker_source_in_allowlist
test_source_table_allowlist_excludes_tracker_events_raw
test_materialization_query_produces_expected_row_count_on_real_db
test_materialization_query_produces_two_focal_rows_per_match
test_materialization_query_symmetric_on_focal_opponent_swap
test_materialization_query_no_target_match_row_in_history
test_join_then_filter_invariant_target_row_admitted_but_excluded          # N6
test_matchup_cte_restricts_to_1v1_history_via_matches_flat_clean_join     # B2
test_matchup_cte_emits_zero_h2h_for_synthetic_4v4_only_shared_pair        # B2
test_per_player_win_rate_decisive_aggregates_all_game_types_per_q1         # B2
test_audit_md_section_1_documents_cross_game_type_win_rate_aggregation     # B2 (partial b)
test_is_decisive_result_flag_used_instead_of_inline_result_in_list         # N11
test_features_audited_is_exactly_twenty_four_columns                       # N4/N10
test_features_audited_excludes_started_at
test_features_audited_excludes_identity_columns
test_audit_verdict_pass_when_all_falsifiers_silent
test_audit_verdict_fail_when_reconstructed_rating_column_appears
test_audit_verdict_fail_when_post_game_token_appears
test_audit_verdict_fail_when_features_audited_empty
test_audit_artifact_json_schema_matches_cross_02_01_v1
test_audit_artifact_json_lists_custom_extensions_section                   # N5
test_audit_artifact_md_contains_verbatim_sql_per_invariant_i6
test_audit_artifact_md_section_1_cites_invariant_i5_for_symmetric_xreg     # N9
test_examiner_clarity_sentence_present_in_audit_json_notes
test_examiner_clarity_sentence_present_in_audit_md_section_1
test_audit_date_equals_materialization_execution_date                      # N7
test_pr257_amendment_grep_token_count_at_least_four
test_q5_binding_sha_pin_matches_pr243_merge_sha_445bae01                   # R3-B3: PR #243 actual SHA
test_q6h_binding_sha_pin_matches_pr251_merge_sha
test_pr245_binding_sha_pin_matches_pr245_merge_sha_ee15d362                # B4 + R3-B3 disambiguation
test_omit_closure_sha_pin_matches_pr255_merge_sha
test_omit_closure_verdict_text_is_verbatim
test_omit_closure_q5_policy_field_is_sensitivity_indicator_co_registration # N2
test_stale_output_path_fragment_rejected
test_run_step_02_01_03_idempotent_byte_identical_under_seed_42
test_run_step_02_01_03_emits_parquet_at_canonical_path
test_run_step_02_01_03_emits_audit_pair_at_canonical_path
test_run_step_02_01_03_writes_research_log_entry                           # B1/B3
test_research_log_entry_field_labels_match_pr236_precedent                 # B3
test_research_log_entry_closure_status_is_still_open                       # B3
test_research_log_entry_features_audited_count_is_twenty_four              # B3, N4/N10 (R3-B4)
test_research_log_entry_row_count_is_44418                                 # B3
test_cross_region_history_retention_is_one_hundred_percent
test_in_game_historical_aggregation_uses_only_prior_matches
test_no_global_normalization_or_encoder_fit_at_this_layer
test_no_phase_03_split_information_referenced
test_no_status_yaml_mutation_by_this_pr
test_no_roadmap_mutation_by_this_pr
test_notebook_path_is_existing_scaffold_overwrite                          # N8
test_pr236_tranche1_three_sha_pins_distinct                                # R3-N1: 3 tranche-1 SHAs
test_total_binding_parent_sha_count_is_seventeen                           # R3-N1: 17 not 16
test_matches_long_raw_yaml_pinned_defensively_not_joined                   # R3-N2
```

### T06 — Overwrite the existing jupytext-paired scaffold notebook

**N8 fix (notebook lineage rationale):** the existing scaffold notebook pair `02_01_03_history_enriched_pre_game_feature_materialization.{py,ipynb}` (PR #241, 276 lines, scaffold-only) is **overwritten in place** in this PR, per `sandbox/README.md` notebook contract (single notebook per Step; lineage preserved through git history). The PR #241 scaffold content remains accessible at SHA `3c6709bf` and is not lost. This avoids the Round 1 ambiguity of maintaining two notebooks with closely-related names; the executor's git diff `git show <Layer-2 SHA> -- sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` will document the scaffold → materialisation transition. The new notebook (sequence step 7 — artifact generation) imports `run_step_02_01_03` from the materialisation module and invokes it; it does NOT duplicate SQL.

Notebook content (jupytext percent format; required cells):
- Module docstring referencing PR #257 amendment by ROADMAP line numbers + grep token; explicit "OVERWRITES PR #241 scaffold content; scaffold preserved at SHA 3c6709bf in git history" cell.
- Banner cell stating "NO scaffold-only; this notebook PRODUCES the five-family Parquet + non-vacuous audit pair + research_log entry."
- Hypothesis/falsifier declaration cell (per `data-analysis-lineage.md` "Required structure for every empirical analysis"): measurement claim = "the 24 feature columns are leakage-free under strict-< history filter and the matchup CTE is 1v1-restricted"; falsifier = `F-audit-verdict-not-pass`; sanity check = `EXPECTED_OUTPUT_ROW_COUNT == 44418`; expected artifact = `02_01_03_history_enriched_pre_game_features.parquet` + audit pair + research_log entry.
- Cell invoking `run_step_02_01_03(...)`.
- Cell printing `MaterializationResult` and `AuditResult` for review (per `feedback_notebook_print_vs_logger.md`).
- Cell asserting `audit.verdict == "PASS"`.
- Closing cell stating "Step 02_01_03 NOT closed by this PR; closure deferred to separate PR per PR #237 precedent."

### T07 — Materialise Parquet + audit artifacts + research_log entry

`run_step_02_01_03(...)` writes exactly:

- `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet`
- `reports/artifacts/02_01_03/leakage_audit_sc2egset.json`
- `reports/artifacts/02_01_03/leakage_audit_sc2egset.md`

The materialisation script ALSO appends the `research_log.md` entry (B1/B3 fix; mirrors PR #236 precedent verified via `git show 51288130 -- src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`).

The audit JSON schema (per CROSS-02-01-v1.0.1 §3, identical baseline to PR #236):

```json
{
  "spec_version": "CROSS-02-01-v1",
  "dataset": "sc2egset",
  "phase_02_step": "02_01_03",
  "audit_date": "<materialisation-execution date in ISO YYYY-MM-DD; N7 fix: pinned convention = the date the materialisation script runs, mirroring PR #236 = 2026-05-23>",
  "future_leak_count": 0,
  "post_game_token_violations": 0,
  "normalization_fit_scope": "training_fold_only",
  "target_encoding_fold_awareness": "N/A_no_target_encoding",
  "cutoff_time_filter_structural_check": "pass",
  "reference_window_assertion": "pass",
  "features_audited": [ <24 column names verbatim, in T03 projection order> ],
  "projected_context_columns": ["started_at"],
  "projected_identity_columns": ["focal_match_id", "focal_player", "opponent_player"],
  "verdict": "PASS",
  "audit_pr": "PR #<TBD>",
  "feature_parquet_path": "src/.../02_01_03_history_enriched_pre_game_features.parquet",
  "feature_parquet_sha256": "<computed>",
  "materialize_module_sha256": "<computed>",
  "spec_02_00_sha256": "<pinned T01>",
  "spec_02_01_sha256": "<pinned T01>",
  "spec_02_02_sha256": "<pinned T01>",
  "spec_02_03_sha256": "<pinned T01>",
  "parent_pr242_csv_sha256": "<pinned T01>", "parent_pr242_md_sha256": "<pinned T01>",
  "parent_pr243_csv_sha256": "<pinned T01>", "parent_pr243_md_sha256": "<pinned T01>",
  "parent_pr245_csv_sha256": "<pinned T01>", "parent_pr245_md_sha256": "<pinned T01>",
  "parent_pr247_csv_sha256": "<pinned T01>", "parent_pr247_md_sha256": "<pinned T01>",
  "parent_pr249_csv_sha256": "<pinned T01>", "parent_pr249_md_sha256": "<pinned T01>",
  "parent_pr251_csv_sha256": "<pinned T01>", "parent_pr251_md_sha256": "<pinned T01>",
  "parent_pr255_csv_sha256": "<pinned T01>", "parent_pr255_md_sha256": "<pinned T01>",
  "registry_csv_sha256": "<pinned T01>",
  "pr236_tranche1_parquet_sha256": "<pinned T01>",
  "pr236_tranche1_audit_json_sha256": "<pinned T01>",
  "pr236_tranche1_audit_md_sha256": "<pinned T01>",
  "matches_flat_clean_yaml_sha256": "<pinned T01>",
  "matches_history_minimal_yaml_sha256": "<pinned T01>",
  "player_history_all_yaml_sha256": "<pinned T01>",
  "matches_long_raw_yaml_sha256": "<pinned T01; R3-N2: defensive lineage-completeness pin; NOT a read-source pin>",
  "row_count": 44418,
  "custom_extensions": {
    "_comment": "N5 FIX: fields beyond CROSS-02-01-v1.0.1 §3 are listed here to allow examiner to distinguish spec-mandated fields from project-extensions.",
    "fields": [
      "feature_to_family_mapping",
      "feature_column_count",
      "distinct_focal_match_count",
      "parent_artifact_shas",
      "generated_sql_provenance"
    ]
  },
  "feature_column_count": 24,
  "distinct_focal_match_count": 22209,
  "feature_to_family_mapping": { /* 24 entries; each maps a feature column to one of the 5 family names */ },
  "generated_sql_provenance": { "git_sha": "<computed>", "module_sha256": "<computed>" },
  "provenance_git_sha": "<computed>",
  "notes": "<examiner-clarity sentence verbatim from PR #236 + non-overclaim disclaimer + amendment grep token + cross-game-type win-rate aggregation acknowledgement per B2>"
}
```

The sibling MD (`leakage_audit_sc2egset.md`) embeds verbatim SQL per Invariant I6 (the entire `_MATERIALIZATION_QUERY` text from T03), narrates each falsifier with its result, lists the 24 features by family, cites all six Q-chain parent PRs (#242, #243, #245, #247, #249, #251) + PR #255 omit-closure + PR #257 amendment, includes the examiner-clarity sentence + the non-overclaim disclaimer, AND includes the following NEW §1 sentences per Round 2 (preserved verbatim in Round 3):

- **B2 win-rate aggregation acknowledgement (audit MD §1):** "Per Q1 BINDING (PR #242 row Q1_source_layer; selected_history_source_layer = `player_history_all`), the per-player history side aggregates ALL game types (1v1 + 2v2 + 3v3 + 4v4 + FFA). The `focal_prior_win_rate_decisive` and `opponent_prior_win_rate_decisive` features are therefore deliberate cross-game-type rates: a player's 4v4 win-rate contributes to their 1v1 prediction. This is a documented Q1-binding consequence, not an oversight; ranking experiments at Phase 04 will treat this as a baseline measurement of the player-level win-rate signal."
- **B2 matchup CTE 1v1-restriction (audit MD §1):** "The `matchup_history_aggregate` family CTE restricts the shared-replay self-join to 1v1 historical matches via `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`. This prevents 4v4/3v3/2v2 prior teammate-or-opponent encounters from spuriously inflating the head-to-head count. The 1v1 restriction on the matchup CTE — combined with the cross-game-type per-player win-rate above — operationalises the intuition that head-to-head is a same-game-type construct while per-player skill aggregates a player's overall activity."
- **N9 Invariant I5 citation (audit MD §1):** "The cross-region indicator pair (`is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any`) goes beyond PR #243's single-indicator text by symmetrising the indicator across focal + opponent. The methodological basis is Invariant I5 (focal/opponent symmetric construction per `.claude/scientific-invariants.md`), not PR #243's text alone."
- **R3-N2 new §2 note:** "The `matches_long_raw_yaml_sha256` is a defensive lineage-completeness pin (not a read-source pin) to detect future drift if a later revision joins this view; the current materialisation does NOT read `matches_long_raw`. Retained to prevent unnoticed view-schema drift from changing the operational meaning of any future revision."

### T08 — Final write + Layer-2 reviewer-adversarial Round 1

- Write all 11 files atomically (single commit `feat(sc2egset): Step 02_01_03 five-family materialization + non-vacuous CROSS-02-01 audit + research_log entry`).
- Files written: see the 11-file File Manifest below.
- Bump `pyproject.toml` `3.81.0` → `3.82.0`.
- `CHANGELOG.md` new `[3.82.0]` section per format below; reset `[Unreleased]` to empty 4-header skeleton.
- `planning/INDEX.md`: archive this Layer-1 row + flip Active to Layer-2 row (PR numbers back-filled at squash-merge).
- Append research_log.md entry per PR #236 precedent (field labels verbatim from PR #236 diff: `closure_status: still_open`, `materialization_state: materialized`, `leakage_audit_state: post_materialization_pass`, `features_audited_count: 24`, `row_count: 44418`, `artifact: 02_01_03_history_enriched_pre_game_features.parquet`, `leakage_audit: reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`).
- Run tests + coverage; expect `>=95%` branch coverage on the new materialisation module.
- Dispatch reviewer-adversarial Round 1 over the 11-file diff (3-round cap symmetric per `feedback_adversarial_cap_execution.md`).
- After APPROVE (Round 1 APPROVE or APPROVE-WITH-NITS with 0 blockers), mark Layer-2 PR ready; user merges.

CHANGELOG `[3.82.0]` required content:
- Statement: "FIRST non-vacuous CROSS-02-01-v1.0.1 §3 leakage audit on Step 02_01_03; five history-enriched pre_game families materialised (24 audited feature columns); single dataset research_log non-closure entry appended."
- Five families listed verbatim per `FIVE_FAMILY_CANONICAL_ORDER`.
- Excluded family + 3 excluded columns listed verbatim.
- Q5 BINDING (`sensitivity_indicator_co_registration`) re-elevated by PR #255 `q5_policy` field; Q7 BINDING (4-tuple IN_GAME_HISTORICAL aggregation) cited.
- B2 fix notation: matchup CTE 1v1-restricted via matches_flat_clean join; per-player win rates documented as deliberate cross-game-type aggregation per Q1 BINDING.
- PR #257 amendment grep token recorded.
- Six Q-chain parent PRs listed (#242, #243 at merge SHA `445bae01`, #245 at merge SHA `ee15d362`, #247, #249, #251) plus PR #255 omit-closure plus PR #257 amendment.
- **Row count 44,418; distinct focal_match_id 22,209; audited feature column count 24; total Parquet column count 28 (3 identity + 1 context + 24 audited).**
- NO-list: "No Step 02_01_03 closure; closure deferred to a separate later PR per PR #237 precedent. No ROADMAP edit. No status YAML flip. No spec edit. No cleaning-layer YAML edit. No Step 02_01_04. No Phase 03. No baseline modeling. No new Q6X PR. No `reconstructed_rating` family. No `reconstructed_rating_*` column. No raw MMR scalar feature. No tracker-derived target-match feature. No global batch fit."

### Stop conditions during Layer-2 execution (halt before write)

S1. Halt if the PR #257 amendment is missing or its grep token count is `<4`.
S2. Halt if any of the **17 BINDING parent artifact SHAs** drifts from the T01 pin (R3-N1: 12 Q-chain + 2 omit-closure + 1 registry + 3 tranche-1 = 17).
S3. Halt if any of the four CROSS-02-** spec SHAs drifts.
S4. Halt if any of the four view YAML SHAs drifts.
S5. Halt if PR #243 Q5_selected_policy is not exactly `sensitivity_indicator_co_registration`.
S6. Halt if PR #255 `q5_policy` field is not exactly `sensitivity_indicator_co_registration` (N2 fix).
S7. Halt if the omit-closure verdict (PR #255) is not exactly `omit_reconstructed_rating_and_unblock_other_five`.
S8. Halt if any `reconstructed_rating_*` column appears in any output projection.
S9. Halt if any `mmr` / `rating` / `elo` / `glicko` / `skill` / `mu` / `sigma` token appears in column names outside `APPROVED_MMR_MISSINGNESS_TOKENS`.
S10. Halt if any history CTE uses `<=`, `=`, or omits `TRY_CAST(ph.details_timeUTC AS TIMESTAMP)`.
S11. Halt if any history CTE uses inline `ph.result IN ('Win', 'Loss')` instead of `ph.is_decisive_result = TRUE` (N11 fix).
S12. Halt if matchup CTE does NOT include `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id` (B2 fix).
S13. Halt if audit MD §1 does NOT document the cross-game-type per-player win-rate aggregation (B2 partial-b fix).
S14. Halt if audit MD §1 does NOT cite Invariant I5 for the cross-region symmetrisation (N9 fix).
S15. Halt if `features_audited` ends up empty, of length != 24, or includes `started_at` / identity columns.
S16. Halt if the audit verdict is `FAIL`.
S17. Halt if the second run is not byte-identical to the first under seed 42.
S18. Halt if any `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` / ROADMAP / spec / cleaning-layer YAML byte changes.
S19. Halt if any tracker_events_raw source is read.
S20. Halt if Step `02_01_04` / Phase 03 / baseline modelling work appears in the diff.
S21. Halt if `research_log.md` entry is MISSING (B1/B3 fix; mandatory per PR #236 precedent).
S22. Halt if `research_log.md` entry's `closure_status` field is not `still_open`.
S23. Halt if `research_log.md` entry lacks any of the PR #236 30-line precedent field labels (`closure_status`, `materialization_state`, `leakage_audit_state`, `features_audited_count`, `row_count`, `artifact`, `leakage_audit`).
S24. Halt if `audit_date` ≠ the date the materialisation script runs (N7 fix).
S25. Halt if `features_audited_count` in the research_log entry ≠ 24 (R3-B4 fix).
S26. Halt if audit MD §2 does NOT document the defensive `matches_long_raw_yaml_sha256` pin (R3-N2 fix).

---

## File Manifest

### This Layer-1 PR (exactly 2 files)

| Path | Action | Rationale |
|------|--------|-----------|
| `planning/current_plan.md` | CREATE (overwrite previous PR #257 plan archive) | Authored by parent session after user approves planner-science output and reviewer-adversarial APPROVES this plan. |
| `planning/current_plan.critique.md` | CREATE (overwrite previous PR #257 critique archive) | Authored by reviewer-adversarial across Rounds 1-3. |

No other repo file touched in this Layer-1 PR.

### Future Layer-2 execution PR (exactly 11 files — B1 fix; PR #236 precedent verified via `git show 51288130 --stat` returning 11 files including 30-line research_log entry)

| Path | Action | Bytes-affected (estimate) |
|------|--------|---------------------------|
| `src/rts_predict/games/sc2/datasets/sc2egset/materialize_history_enriched_pre_game_features.py` | CREATE | ~900-1100 lines (mirrors PR #236 template; widened sub-features per N4/N10 add ~150 lines). |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_history_enriched_pre_game_features.py` | CREATE | ~1300-1600 lines (≥66 named test cases per T05). |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` | OVERWRITE (PR #241 scaffold content preserved in git history at SHA `3c6709bf`; N8 fix) | ~300-400 lines (jupytext source). |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.ipynb` | OVERWRITE (paired) | ~300-400 lines (paired ipynb with cleared outputs). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_features.parquet` | CREATE | binary Parquet; **44,418 rows × 28 cols = 3 identity + 1 context + 24 audited features**; estimate ~1-2 MB. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json` | CREATE | ~8-11 KB (17 parent SHAs + custom_extensions section + defensive `matches_long_raw` pin). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md` | CREATE | ~18-25 KB (verbatim SQL embedded per I6; 3 new §1 sentences per Round 2 + 1 new §2 note per R3-N2). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | EDIT — append one new entry mirroring PR #236 30-line precedent (B1/B3 fix). | +28-32 lines (mirrors PR #236's 30-line diff; new entry block under the date heading `## 2026-MM-DD — Materialize Step 02_01_03 five-family history-enriched pre_game tranche + first non-vacuous CROSS-02-01 audit`; **`features_audited_count: 24`** per R3-B4). |
| `planning/INDEX.md` | EDIT — archive Layer-1 row + flip Active to Layer-2. | +2 lines / -1 line. |
| `CHANGELOG.md` | EDIT — new `[3.82.0]` section + `[Unreleased]` reset. | +50-70 lines. |
| `pyproject.toml` | EDIT — version `3.81.0` → `3.82.0`. | 1 line touched. |

### Forbidden files (both PRs)

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` — PR #257 amendment is sufficient.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` — closure deferred.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` — derived.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` — derived.
- `reports/research_log.md` (root) — no CROSS entry needed for this single-dataset materialization.
- Any other file under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/` (Q-chain parents must remain byte-unchanged; PR #257 amendment must remain byte-unchanged).
- Any file under `reports/artifacts/02_01_02/` (tranche-1 audit must remain byte-unchanged).
- Any `reports/specs/02_*.md` — all CROSS-02-** specs are LOCKED.
- Any `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/*.yaml` — view schemas are Phase 01 artifacts.
- Any `src/rts_predict/**/cleaning/**` YAML.
- Any other `src/rts_predict/games/sc2/datasets/sc2egset/*.py` source file.
- Any `tests/**` file other than the one mirrored test file.
- Any sandbox notebook other than the OVERWRITTEN scaffold pair (PR #233 tranche-1 notebook stays byte-unchanged).
- Any `data/**` file.
- Any AoE2 path (`src/rts_predict/games/aoe2/**`).
- `docs/INDEX.md`, `docs/PHASES.md`, `docs/TAXONOMY.md`, any `docs/**` file.
- Any `.claude/**` file.
- Any `thesis/**` file.

**Note (B1/B3 fix):** the dataset `research_log.md` is REMOVED from the Forbidden-files list; it is now in the REQUIRED 11-file Layer-2 diff per PR #236 precedent.

---

## Problem Statement

After PR #257 (merged 2026-05-28 at master `3ab48b3025f17ce62843d7300195e8094c893a72`), the SC2EGSet ROADMAP records the materialization-scope amendment authorising five-family materialisation for Step `02_01_03`. The amendment's continue-predicate at `ROADMAP.md:2577-2590` explicitly states: "Feature materialization for Step 02_01_03 may proceed in a future PR only when ALL of the following hold: (1) the materialized columns cover exactly the five permitted families … (2) no column with name matching `reconstructed_rating_*` is materialized; (3) the CROSS-02-01 post-materialization audit is NON-vacuous … and returns `verdict = PASS`; (4) all Q5/Q6F/Q6G/Q6H parent artifact bytes are unchanged; (5) PR #255 omit-closure artifact bytes are unchanged." All five continue-predicate conditions are STRUCTURALLY EXPRESSIBLE as Layer-2 falsifiers; this plan enumerates them as the explicit gate condition.

The strategic intent declared in the user prompt — "accelerate toward correct finalization of the master's thesis pipeline by moving from governance/adjudication to actual data production" — demands that this PR cross from the Q-chain governance phase (PR #239 → #241 → #242 → #243 → #245 → #247 → #249 → #251 → #253 → #255 → #257) into the EVIDENCE phase: produce real feature values, run a real audit, persist the FIRST non-vacuous Step `02_01_03` artifact pair, and append the lineage entry to the dataset `research_log.md`.

**Methodological tension this plan must resolve:** the materialization PR's defensibility rests on three independent props that must NOT collapse into each other. (i) The Q-chain provenance — the five families are the *result* of a 7-PR adjudication and must be cited at each parent SHA. (ii) The CROSS-02-01 audit gate — `features_audited` must be exactly the 24 materialised feature columns (NOT `started_at`, NOT identity), `verdict == "PASS"`, audit JSON and MD both present at the canonical path. (iii) The continue-predicate compliance — every PR #257 condition (1)-(5) must be falsifier-tested. This plan binds all three by routing every load-bearing decision (five-family count, excluded columns, Q5 policy, Q7 IN_GAME_HISTORICAL set, strict-< filter form, TRY_CAST canonicalisation, source-table allowlist, 1v1-restricted matchup CTE per B2) to a named module-level constant whose value comes from a specific PR artifact's specific row, and by mirroring each constant in a named test case.

**Why Outcome B (direct execution without planning) is rejected:** `.claude/rules/data-analysis-lineage.md` sequence step 2 (notebook scaffold + one validation module) was already discharged by PR #241; sequence step 7 (artifact generation) is the next non-batching slot and per the rule must follow user review of the validation results.

**Why Outcome D (audit-only without materialisation) is rejected:** the audit MUST be non-vacuous (per PR #257 amendment continue-predicate (3) and per CROSS-02-01-v1.0.1 §3 schema definition).

**Why Outcome E (closure without materialisation) is rejected:** PR #237 precedent for Step `02_01_02` requires the materialisation artifact + the non-vacuous audit + the research_log entry to exist on disk BEFORE the closure PR fires.

**Why Outcome G (Phase 03) is rejected:** `PHASE_STATUS.yaml` records Phase 02 `in_progress`; Phase 03 `not_started`; PR #257 ROADMAP entries explicitly bar Phase 03.

---

## Assumptions & Unknowns

Assumptions are tagged **BINDING** (re-asserted at Layer-2 execution time via SHA-pin or grep token) vs **WORKING** (defensible at plan-time, may be refined at Layer-2 execution time without re-planning).

### Binding assumptions

- **A1 (BINDING)** PR #257 merge commit on master is `3ab48b3025f17ce62843d7300195e8094c893a72`. Layer-2 T01 must verify.
- **A2 (BINDING)** PR #257 amendment is intact: `grep -c "materialization_scope_amendment_post_pr_255" ROADMAP.md >= 4`.
- **A3 (BINDING)** PR #257 amendment's five-family list at `ROADMAP.md:2536-2540` matches the canonical Q6H order exactly: `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`.
- **A4 (BINDING)** PR #257 amendment's excluded column list at `ROADMAP.md:2546-2548`: `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`.
- **A5 (BINDING)** PR #257 amendment's excluded family at `ROADMAP.md:2542` is exactly `reconstructed_rating`.
- **A6 (BINDING)** PR #255 CSV records `decision_verdict = omit_reconstructed_rating_and_unblock_other_five`, `q6_omission_status = intentionally_omitted_under_branch_iii`, `q6_not_silently_satisfied = TRUE`, `future_roadmap_scope_amendment_required = TRUE`, `future_materialization_pr_required = TRUE`.
- **A7 (BINDING)** PR #243 Q5_selected_policy = `sensitivity_indicator_co_registration` AND PR #255 `q5_policy = sensitivity_indicator_co_registration` (N2 fix: PR #255's `q5_policy` field is the explicit BINDING re-elevation, beyond PR #243's recommendation-only binding).
- **A8 (BINDING)** PR #242 Q7 records `in_game_historical_columns_in_scope = APM|SQ|supplyCappedPercent|header_elapsedGameLoops`.
- **A9 (BINDING)** PR #242 Q3 strict-< filter form: `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`.
- **A10 (BINDING)** PR #242 Q1: `selected_target_source_layer = matches_flat_clean`, `selected_history_source_layer = player_history_all`. No tracker_events_raw in allowlist. (B2 consequence: per-player history aggregates ALL game types per Q1; this is a deliberate Q1-binding consequence documented in audit MD §1.)
- **A11 (BINDING)** PR #242 Q2: `target_anchor = matches_history_minimal.started_at TIMESTAMP`; CONTEXT classification per CROSS-02-00-v3.0.1 §5.1.
- **A12 (BINDING)** Expected row count is 44,418 (matches PR #236); expected distinct `focal_match_id` count is 22,209.
- **A13 (BINDING — REVISED PER R3-N1)** All **17 BINDING parent artifact SHAs** are pinned at Layer-2 T01:
  - **12 Q-chain SHAs**: 6 PRs × 2 artifacts each: PR #242 csv+md, PR #243 csv+md (PR #243 merge SHA = `445bae01…` per R3-B3), PR #245 csv+md (PR #245 merge SHA = `ee15d362…`), PR #247 csv+md, PR #249 csv+md, PR #251 csv+md.
  - **PLUS 2 omit-closure SHAs** (PR #255 csv+md).
  - **PLUS 1 registry CSV SHA** (PR #229/#230 closed registry CSV, pinned by PR #236 audit as `registry_csv_sha256`).
  - **PLUS 1 tranche-1 Parquet SHA** (`pr236_tranche1_parquet_sha256`).
  - **PLUS 1 tranche-1 audit JSON SHA** (`pr236_tranche1_audit_json_sha256`).
  - **PLUS 1 tranche-1 audit MD SHA** (`pr236_tranche1_audit_md_sha256`).
  - **Total: 12 + 2 + 1 + 3 = 17.** R3-N1 reconciles the Round 2 "16" count, which collapsed the tranche-1 JSON+MD pair into a single line; this Round 3 plan enumerates the audit JSON SHA and audit MD SHA as TWO separate pins (the canonical CROSS-02-01-v1.0.1 §3 schema mandates BOTH artifacts; their bytes are independent).
  - Layer-2 halts on any drift.
- **A14 (BINDING)** All 4 CROSS-02-** spec SHAs are pinned.
- **A15 (BINDING)** Audit `features_audited` is exactly the 24-tuple in T03 projection order (N4/N10 fix: widened from 18 to 24). Length is 24 exactly. Excludes `started_at` and identity columns.
- **A16 (BINDING)** Audit `verdict` is `"PASS"`.
- **A17 (BINDING)** No `reconstructed_rating_*` column appears anywhere except the `FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS` constant.
- **A18 (BINDING)** No raw scalar MMR / rating / elo / glicko / skill / mu / sigma column appears in the output projection.
- **A19 (BINDING)** No tracker_events_raw source is read.
- **A20 (BINDING)** Run is deterministic: byte-identical Parquet on second invocation under seed 42 + DuckDB's deterministic ORDER BY.
- **A21 (BINDING — corrected from Round 1)** No `STEP_STATUS.yaml` row addition or flip. Closure deferred to a separate U2.B-style PR per PR #237 precedent.
- **A22 (BINDING — REVISED PER B3 + R3-B4)** Per PR #236 precedent (verified via `git show 51288130 -- src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` returning a 30-line entry), a single dataset `research_log.md` entry MUST be appended with the following field labels verbatim:
  - `closure_status: still_open`
  - `materialization_state: materialized`
  - `leakage_audit_state: post_materialization_pass`
  - **`features_audited_count: 24`** (R3-B4 fix: canonical post-widening value is 24, not 18 or 30)
  - `row_count: 44418`
  - `artifact: 02_01_03_history_enriched_pre_game_features.parquet`
  - `leakage_audit: reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`

  The entry section title MUST follow PR #236's pattern: `## <materialization_execution_date_ISO> — Materialize Step 02_01_03 five-family history-enriched pre_game tranche + first non-vacuous CROSS-02-01 audit`. The entry MUST include the PR #236 sub-headings: **Category** (= A), **Dataset** (= sc2egset), **Branch**, **PR**, **Step scope**, **What**, **Why**, **How (reproducibility)**, **Findings**, **What this means**, **Decisions taken**, **Decisions deferred**, **Thesis mapping**, **Open questions / follow-ups**, **Acknowledged trade-offs**, **Scope notes**.
- **A23 (BINDING)** No ROADMAP edit. PR #257 amendment is the authoritative record.
- **A24 (BINDING)** No spec edit. All CROSS-02-** specs are LOCKED.
- **A25 (BINDING)** Version bump is `3.81.0 → 3.82.0` (minor).
- **A26 (BINDING)** Step `02_01_03` remains OPEN after this PR merges. Closure requires (a) materialisation + audit + research_log entry on disk, (b) reviewer-adversarial gate on the audit verdict, (c) a separate U2.B-style closure PR adding `02_01_03: complete` to `STEP_STATUS.yaml`.
- **A27 (BINDING)** Both Layer-1 and Layer-2 PRs share branch `feat/sc2egset-02-01-03-five-family-materialization`.
- **A28 (BINDING — NEW PER B2)** The matchup CTE restricts shared-replay self-join to 1v1 prior matches via `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`. Per-player history CTEs deliberately aggregate ALL game types per Q1 BINDING; this cross-game-type aggregation is documented in audit MD §1 as a Q1-binding consequence, not silently absorbed.
- **A29 (BINDING — NEW PER N11)** Every history CTE uses `ph.is_decisive_result = TRUE` instead of inline `ph.result IN ('Win', 'Loss')`. The `is_decisive_result` BOOLEAN column was added to `player_history_all` in 01_04_02 (DS-SC2-04) and is verified to exist at `data/db/schemas/views/player_history_all.yaml` lines 48-54.
- **A30 (BINDING — NEW PER N7)** `audit_date` = the date the materialisation script runs (ISO YYYY-MM-DD), mirroring PR #236 which used the materialisation execution date `2026-05-23` (not the merge date).
- **A31 (BINDING — NEW PER R3-N2)** `matches_long_raw_yaml_sha256` is a defensive lineage-completeness pin. The current materialisation does NOT read `matches_long_raw`. The pin exists to detect future drift if a later revision joins this view; this rationale is documented in audit MD §2.

### Working assumptions

- **W1 (WORKING)** The exact 24-column projection (6+6+2+2+8 by family) is the planner's best estimate of a CROSS-02-02 §6.2-row-1-verbatim minimal sub-feature set. Reviewer-adversarial may add/remove individual columns within a family provided the audit `features_audited` count and the falsifier `F-features-audited-not-twenty-four` constant are co-amended. Family vocabulary (the 5 family names) is BINDING (A3); sub-feature subset within a family is WIDENED to 6 per CROSS-02-02 §6.2 row 1 (N4/N10) but may be widened further (e.g., EWMA variants) in a future Step 02_01_05-style extension.
- **W2 (WORKING)** The cross-region indicator pair is the planner's interpretation of Q5_selected_policy `sensitivity_indicator_co_registration`. PR #243 records 1 indicator at per-target level; this plan symmetrises across focal + opponent per Invariant I5 (N9 fix: cited explicitly in audit MD §1). Reviewer may collapse to a single shared indicator if I5 is deemed inapplicable; default is symmetric pair.
- **W3 (WORKING)** The matchup-history aggregation joins `player_history_all` to itself on `replay_id` to identify shared prior matches AND restricts to 1v1 via `matches_flat_clean` (B2 fix). An alternative would be a `(focal_player, opponent_player)` join through `matches_flat_clean.replay_id` directly with EXISTS subquery; equivalent results, current form is preferred for SQL readability.
- **W4 (WORKING)** `audit_date` is set at materialisation script execution time (ISO `YYYY-MM-DD`); convention is PINNED per N7 to "the date the materialisation script runs, mirroring PR #236 = 2026-05-23".
- **W5 (WORKING)** Output Parquet file size is estimated 1-2 MB (28 cols × 44,418 rows; mostly DOUBLE + BOOLEAN + VARCHAR; Snappy compression).
- **W6 (WORKING)** PR-numbering: this Layer-1 PR is expected to be PR #258; the future Layer-2 PR is expected to be PR #259. Back-filled in `planning/INDEX.md` at squash-merge time.
- **W7 (WORKING)** Test count is ≥66 named test cases (T05 list, expanded per Round 2 + Round 3 nits); branch coverage target is ≥95% per `pyproject.toml` `fail_under = 95`.

### Unknowns (resolved at Layer-2 T01 or by user pre-Layer-2)

- **U1** Whether reviewer-adversarial Round 3 of this Layer-1 PR returns APPROVE / HOLD. Cap is 3 rounds; this is Round 3 (LAST round before user escalation).
- **U2** Whether the user wishes any deviation from PR #236 precedent for the research_log entry. Default per A22: full PR #236-precedent entry with `features_audited_count: 24` (R3-B4 fix).
- **U3** Whether the 24-column projection should be widened beyond CROSS-02-02 §6.2 row 1 (e.g., EWMA-weighted variants). Default: keep the 24-column CROSS-02-02-row-1-verbatim set; expansion is a future Step `02_01_05`-style extension.
- **U4** Whether the matchup-history CTE's 1v1 restriction should also apply to the per-player history CTEs (forcing those to 1v1 too). Default per A10 + A28: no; per-player history aggregates ALL game types per Q1 BINDING, documented as a cross-game-type aggregation in audit MD §1.
- **U5** Whether to also overwrite the older PR #241 scaffold notebook or maintain a parallel notebook. Default per N8: OVERWRITE the existing scaffold in place; scaffold content preserved at git SHA `3c6709bf`.

---

## Literature Context

Three categories of context inform this materialisation's methodology:

**1. Project-internal precedent (the dominant authority basis).**

- **PR #236** (`feat/sc2egset-02-01-02-pre-game-materialization-execution`, merged 2026-05-23 at `39298c0afd3a23bfbd4603415314af784a672952` per `gh pr view 236 --json mergeCommit`) is the direct template. PR #236 materialised the 5 pre_game tranche-1 families into one Parquet (44,418 × 11 = 3 identity + 1 context + 7 audited) with the FIRST non-vacuous CROSS-02-01-v1.0.1 audit, AND appended a 30-line `research_log.md` entry. Every structural decision in this plan mirrors PR #236: module-level UPPER_SNAKE constants per Invariant I7; `_QUERY`-suffixed module-level SQL constants per python-code rule; frozen dataclasses (`MaterializationResult`, `AuditResult`); falsifier-priority chain with first-fire halting; SHA-256 lineage records; examiner-clarity sentence + non-overclaim disclaimer; deferred closure to a separate U2.B PR; **30-line non-closure research_log entry with closure_status: still_open** (B1/B3 fix). This plan's increase from 7 to 24 audited columns reflects the wider scope (5 history families vs 5 pre_game families, each with the CROSS-02-02 §6.2 row 1 verbatim 6-tuple per side per N4/N10).
- **PR #237** (`chore/sc2egset-02-01-02-formal-closure`, merged 2026-05-24 at `a16d78c25f16aaf8fad4f2c362445212aac1a16b` per `gh pr view 237 --json mergeCommit`) is the precedent for separating closure from materialisation.
- **PR #257** (`feat/sc2egset-02-01-03-five-family-scope-amendment`, merged 2026-05-28 at `3ab48b3025f17ce62843d7300195e8094c893a72` per `gh pr view 257 --json mergeCommit`) is the direct authority anchor.
- **PR #241** (`feat/sc2egset-02-01-03-scaffold`, merged 2026-05-24 at `3c6709bfc21baba893d34a3b87c308d7f8ba787e` per `gh pr view 241 --json mergeCommit`) authored the scaffold notebook this PR OVERWRITES per `sandbox/README.md` notebook contract (N8 fix; PR #241 content preserved at git SHA `3c6709bf`).
- **PR #242** (merged 2026-05-24 at `e372e7b66be66b6026fb3bc39f51d1975da0b8b1` per `gh pr view 242 --json mergeCommit`) binds Q1, Q2, Q3, Q4, Q7, Q8.
- **PR #243** (merged 2026-05-25 at **`445bae0197fa75b613443f8eafef114ff2bb6939`** per `gh pr view 243 --json mergeCommit`; **R3-B3 fix: prior Round 2 attribution to `ee15d362…` was incorrect — that is PR #245's SHA**) binds Q5 cross-region policy: `sensitivity_indicator_co_registration` with 100% PHA history retention.
- **PR #245** (merged 2026-05-25 at `ee15d3625eee60688776219f533d4a5ceefb4b76` per `gh pr view 245 --json mergeCommit`) is the Q6 rating-reconstruction successor adjudication. Binding: PR #255 omit-closure CSV references `parent_pr245_csv_sha256` and `parent_pr245_md_sha256`, proving PR #245 is a binding Q-chain parent (B4 fix preserved).
- **PR #247** (merged 2026-05-25 at `779dc40a36765d90034181fc3885ea32cab204e6` per `gh pr view 247 --json mergeCommit`) is the Q6F rating-algorithm survey.
- **PR #249** (merged 2026-05-26 at `d9276194a1684542a04494ec02df44a5a3f2338e` per `gh pr view 249 --json mergeCommit`) is the Q6G implementation proof.
- **PR #251** (merged 2026-05-26 at `28bfc89fae56e88bd4c039077d7971496d5f1b1c` per `gh pr view 251 --json mergeCommit`) is the Q6H path decision.
- **PR #255** (merged 2026-05-28 at `52f9c1082b200019d080cce74e60567452020e18` per `gh pr view 255 --json mergeCommit`) is the omit-closure (verdict `omit_reconstructed_rating_and_unblock_other_five`; `q5_policy = sensitivity_indicator_co_registration`).
- **PR #233** established the scaffold-then-materialisation rhythm for tranche-1.

**2. Methodology rules (binding governance).**

- **`.claude/rules/data-analysis-lineage.md`** — sequence step 7 (artifact generation); step 8 (research_log / STEP_STATUS / manifest) is now split: this PR appends `research_log.md` (per PR #236 precedent + B1/B3 fix), the closure PR adds `STEP_STATUS.yaml`.
- **`.claude/scientific-invariants.md`** — Invariants I3, I5, I6, I7, I9, I10 directly applied. Invariant I5 is explicitly cited per N9 as the methodological basis for symmetrising the cross-region indicator beyond PR #243's single-indicator text.
- **`.claude/ml-protocol.md`** — Three leakage failure modes each tested by named falsifier.
- **`reports/specs/02_00_feature_input_contract.md`** (LOCKED CROSS-02-00-v3.0.1) — §3.2, §3.3, §5.1, §5.4 directly applied.
- **`reports/specs/02_01_leakage_audit_protocol.md`** (LOCKED CROSS-02-01-v1.0.1) — §3 schema, §5 gate condition. N5 fix: the audit JSON's custom_extensions section makes 5 fields beyond §3 explicit (`feature_to_family_mapping`, `feature_column_count`, `distinct_focal_match_count`, `parent_artifact_shas`, `generated_sql_provenance`).
- **`reports/specs/02_02_feature_engineering_plan.md`** (LOCKED CROSS-02-02-v1.0.1) — §6.2 row 1 enumerates the 6 history families AND the 6-sub-feature tuple per side ("prior match count, prior win rate, time since prior match, race-conditional win rate, map-conditional win rate, matchup-conditional win rate"). This PR materialises 5 (excluding `reconstructed_rating` per PR #257) AND honours the 6-sub-feature enumeration per N4/N10.
- **`reports/specs/02_03_temporal_feature_audit_protocol.md`** (LOCKED CROSS-02-03-v1.0.1) — §4 D1-D15 pre-satisfied by registry.
- **`.claude/rules/git-workflow.md`** — minor bump for feat-family; PR body via `.github/tmp/pr.txt`; commit message via `.github/tmp/commit.txt`; HEREDOC-free.
- **`.claude/rules/python-code.md`** — type hints; Google-style docstrings; ≤~50 lines/function; module-level UPPER_SNAKE; `_QUERY` suffix; DuckDB `?` parameter binding; mirrored test tree; ≥95% branch coverage.
- **`sandbox/README.md`** — single-notebook-per-Step contract; OVERWRITE-in-place lineage preferred over parallel-notebook divergence (N8 fix).

**3. External authority (light citation; the materialisation makes no new empirical claim about the world).**

- **Hollander & Wolfe (1999)** *Nonparametric Statistical Methods* §11.2 — cited only via Q5 parent (PR #243's W=30 noise-floor argument).
- **De Prado (2018)** *Advances in Financial Machine Learning* Ch. 7 — cited via Invariant I3.
- **Demsar (2006)** *Statistical Comparisons of Classifiers* — cited via Invariant I8.

The materialisation is therefore a **direct execution of a methodologically-adjudicated design**, not an exploratory study.

---

## Gate Condition

This Layer-1 PR is approved-to-merge when **all** of the following are TRUE:

1. **2-file diff exactly.** `git diff --name-only master...HEAD` outputs exactly two lines.
2. **planner-science plan present.** `planning/current_plan.md` contains all eight required `##` sections.
3. **Reviewer-adversarial APPROVE recorded.** Round 1/2/3 verdict of `APPROVE` or `APPROVE-WITH-NITS` with `0` blockers (3-round cap; this Round 3 plan is iteration 3 of the cap and is the LAST round before escalation).
4. **No edits outside the 2-file diff.**
5. **No PR-state mutation.** Layer-1 PR remains in `draft` state; user merges manually post-APPROVE.

The future Layer-2 PR is approved-to-merge when **all** of the following are TRUE:

- **L1.** **11-file diff exactly** (B1 fix).
- **L2.** Materialisation module, mirrored test file, OVERWRITTEN scaffold notebook pair (N8 fix), Parquet, audit JSON+MD pair, research_log.md append (B1/B3 fix), planning/INDEX.md flip, CHANGELOG section, pyproject.toml bump all exist.
- **L3.** Output Parquet at canonical path with row count 44,418, distinct `focal_match_id` 22,209, and **28 columns** in T03 projection order.
- **L4.** Audit JSON at canonical path with `spec_version = "CROSS-02-01-v1"`, `verdict = "PASS"`, `features_audited` = **24-tuple** exactly (N4/N10 fix), **`feature_column_count = 24`**, `row_count = 44418`, `distinct_focal_match_count = 22209`, custom_extensions section listing 5 fields beyond §3 (N5 fix), audit_date = materialisation execution date (N7 fix), **all 17 parent artifact SHAs** present and matching T01 pin (R3-N1 reconciliation).
- **L5.** Audit MD at canonical path with verbatim `_MATERIALIZATION_QUERY` per Invariant I6; examiner-clarity sentence + non-overclaim disclaimer + cross-game-type aggregation acknowledgement (B2) + Invariant I5 citation for symmetric cross-region (N9) + defensive `matches_long_raw` pin note (R3-N2); cites all six Q-chain parent PRs (#242 at `e372e7b6`, #243 at `445bae01`, #245 at `ee15d362`, #247 at `779dc40a`, #249 at `d9276194`, #251 at `28bfc89f`) + PR #255 at `52f9c108` + PR #257 at `3ab48b30`.
- **L6.** PR #257 amendment grep token count `>=4`; five-family list at ROADMAP.md:2536-2540 byte-unchanged; excluded-column list at ROADMAP.md:2546-2548 byte-unchanged.
- **L7.** All **17 BINDING parent artifact SHAs** unchanged from T01 pin (R3-N1 reconciliation); 4 CROSS-02-** spec SHAs unchanged; 4 view YAML SHAs unchanged (including the defensive `matches_long_raw_yaml_sha256` per R3-N2).
- **L8.** `pyproject.toml` version `3.81.0 → 3.82.0`.
- **L9.** CHANGELOG `[3.82.0]` section per T08.
- **L10.** `planning/INDEX.md` archive flip recorded.
- **L11.** NO `reconstructed_rating_*` column anywhere.
- **L12.** NO raw MMR/rating/elo/glicko/skill/mu/sigma scalar anywhere.
- **L13.** NO tracker_events_raw source read.
- **L14.** NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` byte changed.
- **L15.** `research_log.md` entry IS present with `closure_status: still_open`, **`features_audited_count: 24`** (R3-B4 fix), and all PR #236 field labels. Root `reports/research_log.md` (CROSS) is NOT touched.
- **L16.** NO ROADMAP / spec / cleaning-layer YAML / `data/` / `docs/` / `.claude/` / `thesis/` / AoE2 path byte changed.
- **L17.** Tests pass; coverage `>=95%` branch on new materialisation module; lint/type clean.
- **L18.** Reviewer-adversarial verdict APPROVE or APPROVE-WITH-NITS with 0 blockers (3-round cap symmetric).
- **L19.** Second deterministic re-run produces byte-identical Parquet.
- **L20.** Draft → ready transition is user-driven post-APPROVE.
- **L21.** Matchup CTE includes `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id` (B2 fix; halt otherwise).
- **L22.** Per-player history CTEs use `ph.is_decisive_result = TRUE` (N11 fix; halt if inline `ph.result IN ('Win', 'Loss')` is found).
- **L23.** Audit MD §2 documents the defensive `matches_long_raw_yaml_sha256` pin (R3-N2 fix).

---

## Open Questions

These are unresolved at Layer-1 planning time. Layer-2 execution may resolve them or defer.

- **OQ1** Should the 24-column projection be widened (e.g., add `focal_prior_match_count_last_30_days` or EWMA-weighted variants per CROSS-02-02 §6.2 implicit aggregations beyond the row 1 verbatim 6-tuple) or narrowed? **Resolution:** keep 24-column CROSS-02-02-row-1-verbatim set (N4/N10 fix); further expansion is a future Step 02_01_05-style extension.
- **OQ2** Should `matchup_h2h_focal_win_rate` denominator restrict to decisive results? **Resolution:** yes, decisive-only per `ph.is_decisive_result = TRUE` (N11 fix).
- **OQ3** Should the cross-region sensitivity indicator be a single shared `is_cross_region_fragmented_any` flag or symmetric pair? **Resolution:** symmetric pair per Invariant I5; N9 fix adds explicit I5 citation in audit MD §1.
- **OQ4** Should a `research_log.md` entry land in the materialisation PR or only in the future closure PR? **REVISED PER B3:** in this PR per PR #236 precedent. **Resolution:** include in materialisation PR, mirroring PR #236 field labels verbatim per A22 with `features_audited_count: 24` (R3-B4 fix).
- **OQ5** Should cold-start handling encode NULL aggregates as zero / NULL / a sentinel? **Resolution:** preserve as NULL.
- **OQ6** Should the Parquet artifact include partition keys or be a single file? **Resolution:** single file.
- **OQ7** Should the audit MD include a per-family feature table or only the consolidated 24-column list? **Resolution:** include both, plus the three Round 2 §1 sentences (B2 win-rate, B2 matchup CTE, N9 Invariant I5) plus the one Round 3 §2 note (R3-N2 defensive pin).
- **OQ8** Whether the `pyproject.toml` bump is `3.81.0 → 3.82.0` (minor; planned). **Resolution:** Layer-2 T01 reads current version; if a chore PR lands between this Layer-1 and Layer-2, bump from observed current.
- **OQ9** Whether the Layer-2 PR is created as `--draft`. **Resolution:** `--draft`.
- **OQ10** Whether reviewer-adversarial Round 1 (Layer-2 execution side) receives a "compressed Layer-2 scope" instruction or "full critique". **Resolution:** full critique.
- **OQ11 (NEW per N8)** Whether to keep the PR #241 scaffold notebook alongside or overwrite in place. **Resolution:** overwrite in place per `sandbox/README.md` single-notebook-per-Step contract; PR #241 content preserved at git SHA `3c6709bf`.
- **OQ12 (NEW per B2)** Whether to also restrict per-player history CTEs to 1v1. **Resolution:** no; per-player history aggregates ALL game types per Q1 BINDING; documented as cross-game-type aggregation in audit MD §1 per B2 partial-b fix.
- **OQ13 (NEW per R3-N2)** Whether to remove the defensive `matches_long_raw_yaml_sha256` pin (currently unused). **Resolution:** retain per R3-N2; audit MD §2 documents the defensive-pin rationale.

---

## Reviewer-adversarial dispatch instructions for THIS Layer-1 PR (Round 3 onward)

These are the instructions the parent session uses to dispatch reviewer-adversarial after this Round 3 plan is approved by the user. They are part of the plan because reviewer-adversarial reads the plan, not the dispatch prompt.

**Agent:** reviewer-adversarial (Opus).
**Inputs to review (READ-ONLY):** `planning/current_plan.md` (this file), `planning/current_plan.critique.md` (Round 1 + Round 2 critique log; reviewer-adversarial appends Round 3 critique), `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2525-2618 + 2837-2849, all **17 BINDING parent artifact SHAs** (CSVs/MDs/Parquet/JSON/MD), all 4 CROSS-02-** specs, all 4 view YAMLs, PR #236 squash-merge commit `39298c0a` for research_log precedent.

**Mandate:**
- Verify all 4 Round 2 blockers (R3-B1: T02 constants block declares `= 24 / = 28` directly; R3-B2: single-source-of-truth comment `# 6+6+2+2+8 = 24`; R3-B3: PR #243 attributed to `445bae01…`, not `ee15d362…`; R3-B4: all `30 audited`/`34 cols`/`from 18 to 30`/`features_audited_count: 30` swept to `24`/`28`/`from 18 to 24`/`features_audited_count: 24`) are resolved.
- Verify both Round 2 nits (R3-N1: BINDING parent SHA count reconciled to 17; R3-N2: defensive `matches_long_raw` pin documented in audit MD §2) are addressed.
- Confirm internal self-consistency on: audited feature column count (`24` everywhere), parquet column count (`28` everywhere), PR #243 merge SHA (`445bae01` everywhere), BINDING parent SHA count (`17` everywhere), `features_audited_count` (`24` everywhere), file counts (Layer-1 = 2, Layer-2 = 11).
- If APPROVE / APPROVE-WITH-NITS with 0 blockers → parent materialises to `planning/current_plan.md`.
- If HOLD with blockers → parent escalates to user per 3-round cap (this is Round 3, the LAST round).

---

## Gate-condition summary (per Round 1 / Round 2 format)

**Layer-1 PR gate:** 2-file diff (current_plan.md + current_plan.critique.md), 8 required `##` sections present, reviewer-adversarial APPROVE/APPROVE-WITH-NITS with 0 blockers (3-round cap; this is Round 3 of 3 — LAST round before user escalation), draft state preserved, user merges manually.

**Layer-2 PR gate:** **11-file diff exactly** (B1 fix; including research_log.md); Parquet at canonical path with **44,418 rows × 28 cols** (3 identity + 1 context + 24 audited); audit JSON+MD at canonical path with `verdict = "PASS"` and `features_audited` = **24-tuple** (N4/N10 fix); research_log.md non-closure entry per PR #236 precedent with **`features_audited_count: 24`** (B3 + R3-B4 fix); **17 BINDING parent SHAs** verified — 12 Q-chain (PR #242, #243 at `445bae01` per R3-B3, #245 at `ee15d362`, #247, #249, #251) + 2 omit-closure (PR #255) + 1 registry + 3 tranche-1 (PR #236 Parquet + audit JSON + audit MD as three separate pins per R3-N1); matchup CTE 1v1-restricted via `matches_flat_clean` join (B2 fix); `ph.is_decisive_result = TRUE` used (N11 fix); audit MD §1 includes 3 sentences (B2 win-rate, B2 matchup CTE, N9 I5 citation); audit MD §2 includes defensive `matches_long_raw` pin note (R3-N2 fix); custom_extensions section in audit JSON (N5 fix); audit_date pinned to materialisation execution date (N7 fix); scaffold notebook overwritten in place at sandbox path with PR #241 lineage preserved at git SHA `3c6709bf` (N8 fix); FIVE_FAMILY_CANONICAL_ORDER tuple (N1 fix); PR #255 `q5_policy` field re-elevation (N2 fix); no `reconstructed_rating_*`, no MMR scalar, no tracker source, no STEP_STATUS/ROADMAP/spec/cleaning-YAML byte change; tests pass with ≥95% branch coverage on the new materialisation module (≥66 named test cases); reviewer-adversarial Layer-2 APPROVE with 0 blockers (3-round cap symmetric); deterministic byte-identical Parquet re-run under seed 42; user-driven draft → ready transition; version bump `3.81.0 → 3.82.0` (minor; feat-family).

---

**Critique gate:** This is Round 3 of the 3-round adversarial cap (LAST round before user escalation). Adversarial critique by reviewer-adversarial is required before execution begins. Per the planner contract, this planner-science session does NOT produce the critique; the parent session must dispatch reviewer-adversarial Round 3 against this revised plan. If reviewer-adversarial Round 3 returns HOLD with any remaining blockers, the parent escalates to the user rather than open the planning PR.

Relevant file paths:
- Round 2 source: `/tmp/planner_round2.md` (read by this planner; not modified)
- Plan target (Layer-1 PR, only after user approval): `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.md`
- Critique target (only after reviewer-adversarial Round 3): `/Users/tomaszpionka/Projects/rts-outcome-prediction/planning/current_plan.critique.md`
- PR #236 research_log precedent (verbatim mirror source): `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (at squash-merge SHA `39298c0a`)
- PR #257 amendment (consumed by this Layer-2 PR): `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2525-2618 + 2837-2849
- Scaffold notebook to be overwritten (PR #241 content preserved at git SHA `3c6709bf`): `/Users/tomaszpionka/Projects/rts-outcome-prediction/sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_enriched_pre_game_feature_materialization.py` and `.ipynb`
