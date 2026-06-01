---
title: "SC2EGSet Step 02_03_01 MATERIALIZATION (Layer-1 planning PR; consumes PR #281 adjudication; emits first temporal-feature Parquet)"
category: A
branch: feat/sc2egset-02-03-01-temporal-materialization-plan
base_ref: master
base_sha: 51a0caf3e561da43be8e5119dad036a3dd768abe
predecessor_pr: 281
predecessor_pr_merge_sha: 51a0caf3e561da43be8e5119dad036a3dd768abe
predecessor_pr_layer: Layer-2-adjudication-execution
dataset: sc2egset
phase: "02"
pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"
step: "02_03_01"
layer: Layer-1-planning-for-materialization
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
draft_pr_file_count: 2
critique_required: true
research_log_ref: null
date: 2026-06-01
adjudication_csv_path: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.csv
adjudication_md_path: src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.md
v1_validator_path: src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py
v3_validator_path: src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py
adjudicator_module_path: src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_temporal_feature_grid.py
predecessor_parent_sha_02_01_02_parquet: 24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39
predecessor_parent_sha_02_01_03_parquet: 053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071
predecessor_parent_sha_02_01_99_csv: 831a622c6e0a98c9642e466d5c9dced0fb6b621a6d58e3008a1b0218dd03c370
predecessor_parent_sha_02_02_01_parquet: c4b48601ee0ff800f4b823af270faf03571a637ce07c51a0ef6d072691896ff3
predecessor_v1_validator_module_sha: 7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545
predecessor_v3_validator_module_sha: 8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87
predecessor_cross_02_02_spec_sha: 86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289
predecessor_cross_02_03_spec_sha: 59e3227307c51ad09fb12b485caec36aa54413d175cb46acc382c06fbb8ac546
predecessor_tracker_eligibility_csv_sha: 11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22
q8_stance: SYNTACTIC_ONLY
non_batching_rule: enforced
---

## Scope

This Layer-1 planning PR authors the plan + critique skeleton for the future Layer-2 **MATERIALIZATION-EXECUTION PR** of Step `02_03_01` — the first temporal-feature materialization step in Pipeline Section `02_03` (Temporal Features, Windows, Decay, Cold Starts) of the sc2egset dataset.

The future Layer-2 PR will consume the byte-stable predecessor artifacts pinned by PR #281 (merged 2026-06-01 at master `51a0caf3e561da43be8e5119dad036a3dd768abe`) and emit ONE temporal-feature Parquet artifact at game-id grain plus its associated metadata. The non-vacuous CROSS-02-03 §1.2 D1-D6 leakage audit is a separate Layer-3 audit-execution PR per repo precedent (PR #270 materialization → PR #272 closure ladder; PR #259 materialization → PR #262 closure ladder).

**This Layer-1 PR writes exactly two files:**

1. `planning/current_plan.md` (this document)
2. `planning/current_plan.critique.md` (reviewer-adversarial scaffold)

**Hard scope constraints (verified violations halt the PR):**

- NO ROADMAP edit (the 02_03_01 stub at master line 3135-3422 is byte-unchanged).
- NO STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS YAML edit.
- NO research_log entry (dataset-level or root CROSS-level).
- NO pyproject version bump; NO CHANGELOG entry.
- NO source module / test / notebook / artifact / spec edit.
- NO Phase 03 or baseline modeling work.
- NO concrete numerical winner (window size, decay half-life, cold-start k) pinned by this Layer-1 PR — Invariant I7 forbids magic numbers; candidate ranges named here MUST each cite an evidence-or-precedent path.
- NO empirical AoE2 transferability claim — Q8 remains SYNTACTIC_ONLY per PR #281 row 17 of the decision CSV.
- NO new validator module; V1 + V3 are inherited.
- NO INDEX archive flip for PR #281 in this Layer-1 PR — INDEX hygiene is folded into the future Layer-2 materialization PR's 9-file diff per the PR #270 → PR #272 precedent.

## Problem Statement

PR #281 (merged at master `51a0caf3`) emitted the binding adjudication CSV/MD for Step `02_03_01`, recording `DEFER_TO_MATERIALIZATION` for the three numerical-grid questions:

- **Q1 (temporal window-type kinds)**: G-L-1 fixed-game-count + G-L-2 fixed-calendar-duration kinds enumerated; concrete game counts / day counts NOT pinned at adjudication.
- **Q2 (decay-type kinds)**: G-L-3 exponential + G-L-4 step-function kinds enumerated; concrete tau half-life / step boundaries NOT pinned at adjudication.
- **Q3 (cold-start-type kinds)**: G-L-5 minimum-prior gate + G-L-6 pseudocount smoothing + G-L-7 combined kinds enumerated; concrete k-thresholds and pseudocount magnitudes NOT pinned at adjudication.

The adjudication MD §7-§9 (file: `02_03_01_temporal_feature_grid_adjudication.md`) defers all concrete numerical winners "to the future materialization PR per Invariant I7." Invariant I7 (`.claude/scientific-invariants.md`) requires every threshold be justified by either (a) empirical evidence from the dataset or (b) a cited precedent from the literature.

The materialization PR must therefore:

1. Translate Q1/Q2/Q3 candidate kinds into concrete numerical winners, each tied to an evidence-or-precedent citation path (NO magic numbers).
2. Compute the per-game-id temporal feature table for the focal-and-opponent pair structure inherited from PR #270 (`02_02_01_symmetry_difference_features.parquet`), restricted to `history_time < target_time` strictly (Invariant I3).
3. Emit one Parquet artifact at the canonical `02_03_01` artifact directory (on-disk-true path used by PR #281).
4. SHA-pin the 9 predecessor artifacts (4 parent data artifacts + 2 validator modules + 2 cross-spec MDs + 1 tracker eligibility CSV) in the materialization output's metadata, matching the PR #281 9-column SHA-pin schema.

The materialization PR does NOT execute the non-vacuous CROSS-02-03 §1.2 D1-D6 leakage audit; that runs at the separate Layer-3 audit-execution PR per the PR #259 → PR #262 ladder.

## Assumptions & Unknowns

**A1.** PR #281 decision CSV/MD remain byte-stable at master `51a0caf3` until the Layer-2 materialization PR opens. Falsified by any commit to either file between this Layer-1 merge and Layer-2 open → halt and re-run the SHA-pin block.

**A2.** V1 (`validate_temporal_feature_grid.py`) and V3 (`validate_temporal_discipline.py`) remain byte-stable. SHA pins:
- V1 module: `7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545`
- V3 module: `8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87`
- last-touching commits: V1 at `b0c90f47` (pre-PR #281), V3 at `5fa90159` (pre-PR #281).

**A3.** The four predecessor data artifacts remain byte-stable (PR #281 row 1 SHA-pin block):
- `02_01_02_pre_game_features.parquet`: `24db73fb…ff39`
- `02_01_03_history_enriched_pre_game_features.parquet`: `053900e7…a071`
- `02_01_99_rating_omit_closure.csv`: `831a622c…d370`
- `02_02_01_symmetry_difference_features.parquet`: `c4b48601…6ff3`

**A4.** The two cross-spec SHA pins remain byte-stable:
- CROSS-02-02 spec: `86af7923…b289`
- CROSS-02-03 spec: `59e32273…b546`

**A5.** The tracker_events eligibility CSV remains byte-stable: `11bd4b9e…ad8d22` at `reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`.

**A6.** The Q1/Q2/Q3 numerical-winner selection in the future materialization PR must cite — for each concrete value chosen — at least one entry from a precedent matrix defined in this plan (see §Literature Context). The materialization PR cannot invent a new precedent; it may only consume precedents named here or appended by an inline amendment.

**A7.** PR #281's Q5 boundary (in-game snapshot families DEFER_PAST_02_03_01) remains binding. Materialization scope is restricted to `pre_game` and `history_enriched_pre_game` prediction settings. The 4 PlayerStats and 1 PlayerStats-derived BLOCKED tracker families remain blocked.

**A8 (Unknown).** Whether the materialization output table grain is one row per `(match_id, focal_player_id_worldwide)` pair (mirroring 02_02_01) or one row per `match_id` with focal/opponent columns is a Layer-2 design decision. The plan recommends the per-pair grain to preserve focal/opponent symmetry (Invariant I5) and the predecessor schema lineage. Layer-2 confirms or amends with reviewer sign-off.

**A9 (Unknown).** Whether decay-type winners include both G-L-3 (exponential) and G-L-4 (step-function), or only one, is open until candidate scoring runs in the materialization sandbox notebook. The plan does NOT preselect.

**A10 (Unknown).** The audit Layer-3 PR's exact file count is open (likely 6-8 files following PR #236 precedent), but the audit is OUT OF SCOPE for this Layer-1 plan.

**A11 (Non-batching exception).** Per `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical work," the Layer-2 materialization PR collapses preflight + materialization + audit-deferral into one 9-file diff matching PR #270 / PR #259 precedent because V1 + V3 scaffold validation passed at PR #276 / PR #278 (separate prior PRs), and the CROSS-02-03 §1.2 D1-D6 audit is explicitly deferred to a separate Layer-3 PR (M5). This is not a batch of unreviewed validation modules; the materialization run is the artifact-generation step in the sequence.

## Literature Context

The future materialization PR must tie each Q1/Q2/Q3 numerical winner to a citation path. The candidate-precedent matrix below names the precedents the Layer-2 PR may invoke. The Layer-1 plan does NOT pick winners; it names the pool of allowable citations.

### Cross-game-portable family inventory (from PR #281 §5 + CROSS-02-02 §10)

- **G-L-1**: fixed-game-count history window (e.g., last N games).
- **G-L-2**: fixed-calendar-duration history window (e.g., last D days).
- **G-L-3**: exponential decay over prior matches.
- **G-L-4**: step-function decay (multi-bin half-life).
- **G-L-5**: minimum-prior cold-start gate (require k ≥ k_min prior games).
- **G-L-6**: pseudocount smoothing for cold-start cells.
- **G-L-7**: combined gate + smoothing.

### Candidate-precedent matrix (consumable by Layer-2; Layer-1 names only)

| Family | Candidate value class | Allowable precedent citation paths |
|---|---|---|
| G-L-1 (game-count window) | small N (5..10), medium N (15..30), large N (50..100) | (a) Bialecki 2023 SC2 paper rolling-window choice; (b) Esportsbench v9.0 default window; (c) prior thesis sc2egset Phase 02 Step 02_01_03 history feature window (Parquet @ `053900e7…a071`); (d) empirical distribution of player-history depth in `matches_flat_clean` (median + IQR from 01_05 panel EDA) |
| G-L-2 (calendar window) | 7d, 30d, 90d, 180d | (a) Glicko-2 rating period guidance (Glickman 2012; bib `Glickman2025`); (b) Esportsbench calendar split convention (v9.0/2026-03-31); (c) sc2egset temporal coverage 2016-01-07 to 2024-12-01 (INVARIANTS §3) + 10-quarter overlap window (INVARIANTS §4 Q1) |
| G-L-3 (exponential decay) | half-life ∈ {3 months, 6 months, 12 months} | (a) Elo (Elo 1978) K-factor literature on rating responsiveness; (b) Glickman 1999 rating-decay framework (bib `Glickman1999`); (c) prior thesis 02_01_03 Q6 rating-omit closure rationale at PR #255 — establishes that explicit decay belongs at the feature layer, not the omitted rating column |
| G-L-4 (step-function decay) | 2-bin {recent / older}, 3-bin {recent / mid / older} | (a) Bradley-Terry comparative window literature; (b) CROSS-02-02 §10 G-L-4 enumeration; (c) sc2egset quarterly grain (INVARIANTS §4 Q1 peak-to-trough 11.7x) |
| G-L-5 (k_min gate) | k_min ∈ {3, 5, 10} | (a) prior thesis Step 02_01_03 cold-start adjudication PR #242 §10 (k-threshold rationale); (b) Esportsbench veteran-filter precedent at k ≥ 3 historical matches (ml-protocol.md line ~39); (c) sc2egset cohort size N∈{5,10,20} from INVARIANTS §4 Q4 |
| G-L-6 (pseudocount) | Laplace add-1, beta(α,β) with α=β=2 | (a) standard Laplace-smoothing literature (Manning & Schütze NLP textbook); (b) Bayesian smoothing precedent for win-rate cells; (c) prior thesis 02_01_03 Q6E pseudocount rationale (if referenced; otherwise emit "no thesis precedent — propose new" disclaimer) |
| G-L-7 (combined) | gate + smoothing composed | inherits citations from G-L-5 and G-L-6 jointly |

**The Layer-2 PR MUST cite at least one precedent from the matching row before emitting any concrete value into the Parquet metadata.** Inventing a numerical value without a citation path triggers falsifier F5 below.

**Unit-choice disclaimer:** Unit choices (months for G-L-3 half-life; bin count for G-L-4) are illustrative ranges; the Layer-2 materialization PR fixes the unit (calendar days vs game-count vs rating-period) and cites the unit-fixing precedent in its `## Numerical Winners and Citations` section.

### Boundary citations (already locked at master)

- **PR #281** decision CSV/MD (master `51a0caf3`): Q1/Q2/Q3 = `DEFER_TO_MATERIALIZATION`.
- **PR #270** materialization: predecessor 02_02_01 Parquet (33 feature columns over 44,418 rows).
- **PR #259** materialization: predecessor 02_01_03 history-enriched Parquet (24 history-enriched features).
- **PR #236** materialization: predecessor 02_01_02 pre-game Parquet (7 PRE_GAME features).
- **PR #255** omit-closure: reconstructed_rating_* columns excluded — materialization must NOT resurface any `reconstructed_rating_*` column or rating-snapshot scalar (Invariant I9 + ROADMAP halt_predicate).

## Execution Steps

This section enumerates the steps the executor of the FUTURE Layer-2 materialization PR will perform. The Layer-1 PR (this document) writes only the plan + critique skeleton; the steps below are pre-declarations for the Layer-2 executor and the reviewer-adversarial pre-execution gate.

### M1 — Translate Q1/Q2/Q3 `DEFER_TO_MATERIALIZATION` families into citation-tied winners

For each of the three deferred questions, Layer-2 must:

1. Open the candidate-precedent matrix in §Literature Context.
2. For each chosen family kind (G-L-1, G-L-2, G-L-3, G-L-4, G-L-5, G-L-6, G-L-7), select at least one numerical winner from the candidate value class.
3. For each winner, cite the precedent path used (bib key + section anchor, OR empirical-anchor path with SHA pin).
4. Record the winner-and-citation pair in the materialization output's metadata (Parquet `metadata` dict; also rendered into the materialization MD §"Numerical Winners and Citations").
5. Verify no winner is unsupported. Falsifier F5 halts the run if any winner lacks a citation.

### M2 — Citation-tied numerical winners (no magic numbers)

The Layer-2 PR commits to the candidate-precedent matrix in §Literature Context as the closed pool of allowable citations. Layer-2 may not invent new precedents without an inline amendment PR. If a Layer-2 candidate has no matching precedent row, Layer-2 must:

- Either NARROW the family kind (drop the unsupportable candidate).
- Or HALT and open an amendment Layer-1 PR to extend the matrix.

The Layer-2 PR's `## Numerical Winners` section must enumerate, per chosen winner, the bib-key OR empirical-anchor path used.

### M3 — Consume PR #281 decision CSV/MD + V1/V3 validators + predecessor artifacts

Execution order at Layer-2 startup:

1. V1 preflight: invoke `validate_predecessor_artifact_provenance(repo_root)` from `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_feature_grid.py`. Falsifier F2 halts on failure.
2. V3 preflight: invoke `validate_temporal_discipline(repo_root)` from `src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py`. Falsifier F1 halts on failure.
3. SHA-pin verification: hash each of the 9 predecessor artifacts and compare to the YAML front-matter values declared in this plan. Falsifier F6 halts on mismatch.
4. Read PR #281 decision CSV: parse the 16-row × 16-column body; extract `decision`, `rationale_g_l_ref`, `rationale_d_ref` per family_kind. Verify Q1/Q2/Q3 rows are exactly `DEFER_TO_MATERIALIZATION`.
5. Read predecessor Parquets: `02_01_02`, `02_01_03`, `02_02_01`. Verify row counts match prior research_log entries (44,418 rows for cleaned tables).
6. Read `02_01_99_rating_omit_closure.csv`: verify reconstructed_rating exclusion is still binding.

### M4 — Emit the temporal feature Parquet (game-id grain; focal/opponent; history-only; target-game excluded)

Output identity: one row per `(match_id, focal_player_id_worldwide)` pair (mirroring 02_02_01 schema), totalling ≤44,418 rows.

Output columns (proposed; Layer-2 confirms exact list):

- Identity: `match_id` (string), `focal_player_id_worldwide` (string), `opponent_player_id_worldwide` (string), `started_at` (timestamp[us]).
- Per chosen Q1 family (game-count window): `prior_win_rate_g_l_1_n_<N>_focal`, `_opp` for each chosen N.
- Per chosen Q2 family (calendar window): `prior_win_rate_g_l_2_d_<D>_focal`, `_opp`.
- Per chosen Q3 family (exponential decay): `prior_win_rate_g_l_3_halflife_<H>_focal`, `_opp`.
- Per chosen Q4 family (step-function decay): `prior_win_rate_g_l_4_steps_<S>_focal`, `_opp`.
- Per chosen Q5/Q6 cold-start: `cold_start_g_l_5_k_<k_min>_focal`, `_opp` with smoothed counterpart where G-L-6/G-L-7 applies.

Semantics:

- Strict-`<` history filter: every per-pair feature uses only matches with `prior.started_at < target.started_at` (Invariant I3; not `<=`).
- Target-game exclusion: no feature uses the target match's own `won` column, duration, or any IN_GAME_HISTORICAL field of the target match (Invariant I3 + I9 + ROADMAP halt_predicate; falsifier F3).
- Focal/opponent symmetry: every feature is computed identically for both players (Invariant I5; pair-symmetric function from 02_02_01 reused).
- Non-vacuous: every feature column must have at least one non-NULL, non-constant value across the table (falsifier F4).

Metadata: the Parquet metadata dict embeds (a) the 9 SHA pins from PR #281 schema; (b) Q1/Q2/Q3 numerical winners; (c) per-winner citation paths; (d) row count + per-column NULL count.

### M5 — Audit deferral to separate Layer-3 PR

The non-vacuous CROSS-02-03 §1.2 D1-D6 design-time audit is OUT OF SCOPE for the materialization PR. Repo precedent (PR #270 materialization → PR #272 closure; PR #259 materialization → PR #262 closure) keeps audit + status closure in a separate downstream PR. The materialization PR's research_log entry MUST be a non-closure entry (`closure_status: still_open`, `leakage_audit_state: deferred_to_layer_3_audit_pr`).

### M6 — Invariant preservation

The materialization PR must preserve:

- **No DuckDB write-mutation**: read-only consumption of `matches_flat_clean` and `player_history_long` (existing VIEWs); no new DuckDB table is created; output is Parquet only.
- **Invariant I3 strict-`<` cutoff**: enforced at SQL/Python level for every per-feature aggregation.
- **Invariant I4 target-game exclusion**: no feature consumes the target match's own row in its aggregation.
- **No Phase 03 / baseline modeling**: the materialization PR does NOT train any model; it only emits the feature table.
- **No tracker-derived target-match feature**: per ROADMAP halt_predicate + INVARIANTS §3 (`duration_seconds` = POST_GAME_HISTORICAL token exclusion).

### M7 — INDEX archive folding into the Layer-2 PR

planning/INDEX.md is updated by the Layer-2 materialization PR (NOT by this Layer-1 PR), folding two archive rows into a single 9-file diff:

- PR #281 (Layer-2 adjudication execution; merged 2026-06-01 at `51a0caf3e561da43be8e5119dad036a3dd768abe`).
- This Layer-1 planning PR (to be merged as PR #<TBD> upon approval).

The Layer-2 PR's INDEX entry follows the PR #270 / PR #272 pattern: Active row moves to "Layer-2 MATERIALIZATION execution PR for Step 02_03_01"; the two predecessor rows are appended chronologically to the Archive table.

## File Manifest

### Layer-1 PR (this PR — exactly 2 files; HARD constraint):

| Path | Change | Purpose |
|---|---|---|
| `planning/current_plan.md` | new (replaces prior plan) | the file you are reading |
| `planning/current_plan.critique.md` | new (replaces prior critique) | reviewer-adversarial scaffold |

### Future Layer-2 materialization-execution PR (NOT created in this Layer-1 PR; named as proposal only):

The following file list is a PROPOSAL based on the PR #270 / PR #259 precedent. Exact paths confirmed at Layer-2 planning time; the Layer-1 PR commits to none of them.

| Path (proposal) | Change | Layer-2 purpose |
|---|---|---|
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_materialization.py` | new | jupytext-paired sandbox notebook |
| `sandbox/sc2/sc2egset/02_feature_engineering/03_temporal_features/02_03_01_materialization.ipynb` | new | jupytext .ipynb sibling |
| `src/rts_predict/games/sc2/datasets/sc2egset/materialize_temporal_features.py` | new | materialization module |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_temporal_features.py` | new | mirrored test suite (target: ≥35 tests, ≥95% branch coverage) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_features.parquet` | new | the materialised feature Parquet |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_features.md` | new | materialization MD report |
| `planning/INDEX.md` | edit | archive PR #281 + this Layer-1 PR; flip Active row |
| `CHANGELOG.md` | edit | new `[X.Y.Z]` section |
| `pyproject.toml` | edit | version bump |

**Layer-2 file count proposal: 9** (matches PR #270, PR #259, PR #281 precedent).

The materialization PR does NOT touch ROADMAP, STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS, research_log, specs, or `.claude/`. Those flips happen at the separate Layer-3 audit PR and the subsequent U2.B-style formal closure PR.

## Gate Condition

This Layer-1 PR's gate (the condition that flips this plan from draft to "ready for execution"):

**G1. Two-file diff verified.** `git diff base..HEAD --name-only` returns exactly `planning/current_plan.md` and `planning/current_plan.critique.md`. Any additional path triggers a HARD HALT.

**G2. No scope leak.** Static grep over the diff confirms: no edits under `src/`, `tests/`, `sandbox/`, `thesis/`, `docs/`, `reports/`; no edits to `pyproject.toml`, `CHANGELOG.md`, ROADMAP, STEP_STATUS, INVARIANTS; no edits to `planning/INDEX.md` (folded into Layer-2).

**G3. Critique present.** `planning/current_plan.critique.md` exists with required sections (Verdict, Substantive Findings, NITs, NOTES, Closing Statement) — filled in by reviewer-adversarial Round 1.

**G4. No magic numbers in the plan body.** No concrete numerical winner for window-size N, calendar-duration D, half-life H, step boundary S, or cold-start k_min appears in the Layer-1 plan unless paired with at least one citation path. The candidate-precedent matrix in §Literature Context is the canonical record.

**G5. Reviewer-adversarial APPROVE on Round 1 OR APPROVE-WITH-NITS with all nits applied inline before merge.** Per Category A protocol.

**G6. Master tip pinned.** `base_sha: 51a0caf3e561da43be8e5119dad036a3dd768abe` is verified in the YAML front-matter and matches the actual base commit at PR open time.

**G7. Q8 stance unchanged.** `q8_stance: SYNTACTIC_ONLY` is verified in front-matter; no empirical AoE2 transferability claim appears anywhere in the plan body.

If all G1-G7 pass, the Layer-1 PR is ready to merge. The Layer-2 materialization-execution PR opens against this plan + the critique resolution.

## Falsifiers F1-F7 (declared for the FUTURE Layer-2 materialization run)

Per `.claude/rules/data-analysis-lineage.md` "Required structure for every empirical analysis": every Layer-2 step must declare assumption, measurement claim, sanity check, falsifier, expected artifact, lineage source, and the downstream decision dependent on the result.

### F1 — Temporal-discipline (Invariant I3) falsifier

- **Assumption.** Every per-pair temporal feature uses only matches with `prior.started_at < target.started_at` (strict-`<`).
- **Measurement.** V3 (`validate_temporal_discipline.py`) invoked as a preflight gate before the materialization SQL executes.
- **Falsifier.** V3 returns any FAIL on schema-naming convention, temporal-anchor presence, or cite-string provenance → HALT.
- **Expected artifact.** V3 preflight result dict embedded in the materialization MD §"Preflight Gates".
- **Lineage.** V3 module at SHA `8e33b7ae0968cbaafa08c33b51e62196e7d4f19cadcd48b3b8d03b6aa2ae2a87`.
- **Downstream decision.** If F1 fires, no Parquet is written.

### F2 — V1 predecessor-provenance falsifier

- **Assumption.** All 4 parent data artifacts + 2 cross-spec MDs + 1 tracker CSV remain byte-stable at the PR #281 SHA pins.
- **Measurement.** V1 (`validate_temporal_feature_grid.py` via `validate_predecessor_artifact_provenance(repo_root)`) invoked as the second preflight gate after V3.
- **Falsifier.** V1 returns any FAIL on SHA-pin / row-count / column-presence → HALT.
- **Expected artifact.** V1 preflight result dict embedded in MD §"Preflight Gates".
- **Lineage.** V1 module at SHA `7945fc7fc7cf3500390c647c977702a14c3d5ab03c4ee7bbaf04d6bbe1033545`.
- **Downstream decision.** If F2 fires, no Parquet is written.

### F3 — No-target-game-leakage falsifier (Invariant I4)

- **Assumption.** No feature column reads any field of the target match's own row (the target match's `won`, `duration_seconds`, or any IN_GAME_* field).
- **Measurement.** Unit test in `tests/rts_predict/games/sc2/datasets/sc2egset/test_materialize_temporal_features.py` asserts every feature column's SQL aggregation expression contains a `WHERE prior.started_at < target.started_at` clause and never references `target.won`, `target.duration_seconds`, or any `target.in_game_*` identifier.
- **Falsifier.** Any feature column whose SQL/Python lacks the strict-`<` predicate, or that reads a target-row column → HALT.
- **Expected artifact.** Test pass record in the Layer-2 pytest log; MD §"Leakage Falsifier" lists each feature column's SQL fingerprint.
- **Lineage.** Inherits Invariant I3 + I4 from scientific-invariants.md and ml-protocol.md.
- **Downstream decision.** If F3 fires, no Parquet is written.

### F4 — Non-vacuous-temporal-window falsifier

- **Assumption.** Every feature column is non-constant across the table and has at least one non-NULL value.
- **Measurement.** Post-Parquet-write, for each feature column, compute `COUNT(DISTINCT col) > 1` AND `COUNT(col) > 0`. Both must hold AS A MINIMUM.
- **NULL-rate handling.** NULL-rate per feature column is reported in MD §"Non-Vacuous Audit"; cold-start-gated columns may have elevated NULL rates by design (G-L-5 / G-L-7) and are NOT halted by F4 alone — MD records the NULL count next to k_min so the gate behaviour is auditable.
- **Falsifier.** HALT only when `COUNT(DISTINCT col) ≤ 1` OR every value is NULL.
- **Expected artifact.** Materialization MD §"Non-Vacuous Audit" with the per-column distinct-count + non-NULL-count table.
- **Lineage.** Inherits "no trivial constants" from data-analysis-lineage.md "Sanity check" obligation.
- **Downstream decision.** If F4 fires, offending columns are dropped and the run is re-attempted; if all columns fail, the Parquet is not written.

### F5 — Magic-number falsifier (Invariant I7)

- **Assumption.** Every concrete numerical winner is paired with at least one citation path from the candidate-precedent matrix.
- **Measurement.** Static-grep over the materialization module + notebook + MD: each numerical literal in `_NUMERICAL_WINNERS` (or equivalent module-level constant) must appear in a `# CITES:` comment pointing to a bib-key or empirical-anchor path.
- **Falsifier.** Any numerical winner without a `# CITES:` annotation → HALT.
- **Expected artifact.** Materialization MD §"Numerical Winners and Citations" — a table with one row per winner.
- **Lineage.** Invariant I7 (scientific-invariants.md).
- **Downstream decision.** If F5 fires, no Parquet is written until the citation gap is closed.

### F6 — SHA-pin falsifier

- **Assumption.** The 9 predecessor artifact SHAs (PR #281 schema) are embedded verbatim in the Parquet metadata dict.
- **Measurement.** After Parquet write, re-open and read the metadata dict; assert the 9 keys are present and equal the front-matter YAML values from this plan.
- **Digest function.** SHA-256 hex over the raw file bytes (matching PR #281 adjudication CSV header schema and adjudicator module convention).
- **Falsifier.** Any of the 9 SHAs missing or mismatched → HALT and regenerate.
- **Expected artifact.** Materialization MD §"SHA-Pin Provenance" — the 9-row table.
- **Lineage.** Invariant I9 (research pipeline discipline) + repo precedent (PR #281 9-column SHA-pin schema).
- **Downstream decision.** If F6 fires, the Parquet is regenerated; if regeneration also fails, the materialization PR is paused until the SHA-pin discrepancy is reviewed.

### F7 — Cross-game scope falsifier (Q8 SYNTACTIC_ONLY)

- **Assumption.** No empirical AoE2 transferability claim appears in the materialization output. The Q8 stance remains SYNTACTIC_ONLY per PR #281 row 17.
- **Measurement.** Static-grep over MD/module/notebook with `\baoe2\b`, `\baoestats\b`, `\baoe2companion\b`, `\bcivilization\b`, `\bciv\b` word-boundary anchors (per PR #282 NIT-X2 `\b`-anchor precedent merged 2026-06-01 at master `cb84e8b5`), excluding front-matter and the Q8 stance block.
- **Falsifier.** Any empirical AoE2 claim → HALT.
- **Expected artifact.** Materialization MD §"Q8 Cross-Game Stance" — the SYNTACTIC_ONLY declaration verbatim from PR #281.
- **Lineage.** Invariant I8 (cross-game comparability) + scientific-invariants.md + PR #281 row 17.
- **Downstream decision.** If F7 fires, offending text is excised and the materialization is re-run.

## Open Questions

**OQ-1.** Should the materialization PR materialise both G-L-3 (exponential) and G-L-4 (step-function) decay families, or only one? Layer-1 defers; Layer-2 sandbox notebook evaluates candidate count empirically (block-bootstrap on log-loss / Brier proxies) before pinning winners.

**OQ-2.** Tracker-derived eligible families (PR #281 MD §6 rows 5, 6, 7, 8, 9, 10, 13, 14 = 8 `ELIGIBLE` or `ELIGIBLE_WITH_CAVEAT` aggregated decisions over `pre_game / history_enriched_pre_game`) at this step or follow-up? Layer-1 recommends DEFER to a follow-up materialization PR to keep this PR's diff scope ≤ 9 files matching PR #270 precedent; the deferral preserves PR #281 §6 aggregated decisions byte-stable.

**OQ-3.** What is the exact grain of the output Parquet — per `(match_id, focal_player_id_worldwide)` pair (mirroring 02_02_01) or per `match_id`? See assumption A8; Layer-2 confirms.

**OQ-4.** Are the cold-start indicators emitted as boolean columns or as sentinel-bearing numeric columns? Layer-1 recommends boolean (one column per chosen k_min) for tidy modelling downstream; Layer-2 confirms.

**OQ-5.** Should the materialization MD embed the candidate-scoring tables (per-candidate AUC / log-loss / Brier proxies) or only the winner-and-citation record? Layer-1 recommends the full scoring tables — they document the empirical justification for each winner under Invariant I6. Layer-2 confirms.

**OQ-6.** Does the materialization PR's pyproject bump go to `3.91.0` or to a later version? Layer-1 cannot fix the version number here — Layer-2 reads the live `pyproject.toml` at open time and applies a minor bump per `.claude/rules/git-workflow.md`.

**OQ-7.** Materialization artifact directory: confirm the on-disk-true `03_temporal_features/02_03_01/` path (used by PR #281 adjudication artifacts) over the ROADMAP halt_predicate's longer form `03_temporal_features_windows_decay_cold_starts/`; the longer form appears to be a pre-existing ROADMAP halt_predicate inconsistency from PR #274 and may require a chore-class amendment in a separate PR. Materialization PR uses the shorter form for output consistency with PR #281.
