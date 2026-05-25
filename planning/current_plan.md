---
plan_role: planner-science
plan_model: claude-opus-4-7[1m]
plan_date: 2026-05-25
date: 2026-05-25
plan_layer: 1 (planning-only; 2-file diff)
chosen_outcome: A
branch: feat/sc2egset-02-01-03-q6f-rating-algorithm-survey
future_layer2_version_bump: 3.75.0 -> 3.76.0
planning_pr_version_bump: none (planning-only; matches PR #240 / #244 precedent)
this_planning_pr_category: A
category: A
parent_planning_pr: 244 (merged 2026-05-25; Q6 Layer-1 plan)
parent_execution_pr: 245 (merged 2026-05-25; Q6 Layer-2 execution; verdict deferred_blocker; materialization blocked_pending_algorithm_survey_pr)
parent_q5_pr: 243 (merged; Q5_selected_policy = sensitivity_indicator_co_registration; verdict narrow_with_evidence; BINDING)
parent_q1_q4_q7_q8_pr: 242 (merged; RATIFIED)
base_ref: ee15d3625eee60688776219f533d4a5ceefb4b76
phase_status_at_plan_time: Phase 02 in_progress; Phase 03 not_started
step_status_at_plan_time: 02_01_01 complete; 02_01_02 complete; 02_01_03 in_progress (deferred-blocker chain Q1..Q8 satisfied except Q6 which is itself a deferred_blocker_with_algorithm_survey_required verdict)
non_batching_compliance: this Layer-1 plan does not author any Q6F survey module, validator, notebook, artifact, status YAML, or research_log; the Layer-2 PR is a separate dispatch
adversarial_round_cap: 3 (symmetric per feedback_adversarial_cap_execution.md)
---

## Scope

This is the **Layer-1 planning-only PR** for the next atomic unit in SC2EGSet Step 02_01_03 after PR #245 merged. The outcome under planning is **A — Q6F rating-algorithm survey PR**.

The Layer-2 execution PR (named in the Future-Layer-2 manifest) will:

1. Survey the **4 included rating candidates** (`rolling_win_rate_or_bayesian_smoothed_baseline`, `elo`, `glicko_or_glicko_2`, `trueskill_or_trueskill_like`) by computing forward-only per-game predicted probabilities on the `player_history_all` (PHA) chronological stream, scored against actual decisive PHA results.
2. Carry-forward **2 reference candidates** (`omit_reconstructed_rating`, `deferred_blocker_with_algorithm_survey_required`) as reference rows that do not have an algorithm to evaluate but must remain in the row set so the Q6F decision can re-affirm them.
3. Persist **one (1) artifact pair** under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`:
   - `02_01_03_q6f_rating_algorithm_survey.csv` (≥36 columns, 8 rows: 4 included + 2 carry-forward + 1 Q6F_selected_policy + 1 Q6F_per_family_impact_summary)
   - `02_01_03_q6f_rating_algorithm_survey.md` (≥17 sections)
4. Emit `Q6F_selected_policy` as an emergent row whose value is one of:
   - `bind_now` -> materialization permitted for all 6 families WITH pinned algorithm + pinned hyperparameters in a future Layer-3 materialization PR;
   - `narrow_with_evidence` / `recommendation_only` -> materialization permitted but blocked pending an algorithm-implementation-proof PR;
   - `deferred_blocker` -> blocked_pending_<named_reason>; the survey itself produced no winner and the orchestrator must trigger a different unblock (e.g., a wider candidate set, a richer evidence column);
   - `omit_reconstructed_rating_and_unblock_other_five` -> 5-family Layer-3 materialization permitted **without** `reconstructed_rating`; the rating column is permanently absent from sc2egset Step 02_01_03.

This planning PR records:

- **2 files only**: `planning/current_plan.md` (this content) + `planning/current_plan.critique.md` (reviewer-adversarial Round 1 stub).
- **NO version bump** in this PR (matches PR #240 / PR #244 planning-only precedent).
- **NO survey code**, **NO survey artifact**, **NO status YAML mutation**, **NO research_log entry**, **NO ROADMAP edit**, **NO Parquet output**, **NO CROSS-02-01 audit file**.

Branch: `feat/sc2egset-02-01-03-q6f-rating-algorithm-survey`.

## Problem Statement

The Q6F target question:

> Which rating reconstruction policy, if any, can be justified for later materialization under forward-only, cold-start (G-CS-4), deterministic, and deployable constraints?

This question was emitted by PR #245 verbatim:

> Q6_selected_policy = `deferred_blocker_with_algorithm_survey_required` because the comparative back-testing evidence among Elo / Glicko-2 / TrueSkill / rolling-baseline does not exist in any prior artifact and binding a winner would violate Invariant I7 ("no magic numbers").

The Q6F survey is the **direct unblock condition** for Step 02_01_03. It is **not** the only-possible unblock: the Q6F verdict may also be `omit_reconstructed_rating_and_unblock_other_five`, which unblocks the other 5 families' materialization without producing a `reconstructed_rating` column at all.

Four distinct downstream artifacts must not be confused:

1. **The Q6F survey output (THIS planning's future Layer-2 PR).** Authors the per-candidate metrics CSV+MD; picks a winner OR re-defers OR allows omit-and-unblock-other-five. This PR does NOT materialize features. This PR does NOT train Phase-03 baselines. The metrics computed during the survey are **evaluation traces** of forward-only rating predictions on the PHA stream — they are Q6F-internal artifacts ONLY and are NOT Phase-03 baseline results.
2. **The Layer-3 `reconstructed_rating` feature materialization PR.** Actually computes per-target-match rating values, writes the 6-family Parquet, runs CROSS-02-01 audit. **OUT OF SCOPE** for the Q6F survey.
3. **The Layer-3 materialization of the OTHER 5 families if Q6F selects `omit_reconstructed_rating_and_unblock_other_five`.** Separate PR scope; recorded as recommendation only.
4. **Phase 03 baseline / model-training cold-start (G-CS-6).** OUT OF SCOPE. Phase 03 remains barred per `PHASE_STATUS.yaml` (Phase 03 = `not_started`) and per `.claude/ml-protocol.md` §4 (`create_temporal_split()` superseded).

The Q6F survey is the cleanest minimum unit that unblocks Step 02_01_03 without violating Invariant I7 (the existing PR #245 Q6 verdict explicitly cites I7 as the binding obstacle to a winner-pin).

### Why outcomes B-F are rejected

- **B — direct materialization (Layer-3 reconstructed_rating Parquet now).** REJECTED: Q6 verdict is still `deferred_blocker_with_algorithm_survey_required`; materialization_permission is `blocked_pending_algorithm_survey_pr`. Proceeding to Layer-3 materialization would silently bind a rating algorithm without evidence, violating I7.
- **C — direct survey execution without a planning PR.** REJECTED: violates `data-analysis-lineage.md` non-batching rule ("Do not batch ROADMAP + notebook + artifact + next Step in one execution"). Each empirical Step must follow the 9-step sequence; the survey is empirical (computes per-candidate AUC / log-loss / Brier), so the Layer-1 plan stage cannot be elided.
- **D — Phase 03 baselines first.** REJECTED: Phase 03 is barred until the rating-reconstruction question resolves (the spec §6.2 row 4 lists `reconstructed_rating` as part of the pre-game feature set; bypassing it to start Phase 03 would mean Phase 03 trains on a feature universe the spec disowns).
- **E — hygiene-only PR first (e.g., addressing PR #245 NIT-B and NIT-C cosmetics).** REJECTED: PR #245 reviewer-adversarial verdict was APPROVE-WITH-NITS, 0 blockers; NIT-B (filename-relative paths in evidence_paths) and NIT-C (decimal-places formatting in MMR-missingness summary) are cosmetic and were explicitly accepted in PR #245's merge. No real blocker exists; doing a hygiene PR now would delay Q6F without removing any obstacle.
- **F — hold (no PR; await user direction).** REJECTED: the repo state is consistent (master clean; STEP_STATUS in sync; PHASE_STATUS in sync; no competing open PR; PR #245's Q6 verdict explicitly names the next required step as "algorithm survey PR"). The user has standing direction (project_pending_temp_commit indicates the pre-existing temp/ triage is the only other open task, not Q6F). Holding would forfeit a known-required step.

## Assumptions & Unknowns

### Assumptions (BINDING for the future Layer-2 execution PR)

The 18 assumptions below are BINDING. The Layer-2 executor must honour them verbatim; deviation requires a fresh planning round.

1. **Parent provenance.** The 6 parent SHAs are pinned (PR #242 CSV/MD, PR #243 CSV/MD, PR #245 CSV/MD). The Layer-2 module must hard-code these as constants:
   - `parent_pr242_csv_sha256 = "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"`
   - `parent_pr242_md_sha256  = "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"`
   - `parent_pr243_csv_sha256 = "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"`
   - `parent_pr243_md_sha256  = "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"`
   - `parent_pr245_csv_sha256 = "703c915376dbcaed54e641c2473bb924cf5881864f76c7389057c819b9d8f4d0"`
   - `parent_pr245_md_sha256  = "7efea247924fdb01d8d3ab5f66a0765937ec5142f6a46a99512abdf7f4839419"`

2. **Q5 BINDING.** `Q5_selected_policy = sensitivity_indicator_co_registration`, verdict `narrow_with_evidence`. The survey honours Q5: cross-region history rows are NOT dropped from the survey input; the `is_cross_region_fragmented` flag is a co-registered evidence dimension on each survey row's `cross_region_policy` field, not a filter applied to the input stream. The `q6f_q5_re_adjudication_drift` falsifier halts the entrypoint if any survey row carries a Q5-verdict-bearing token in a verdict-bearing field.

3. **Q1-Q4 / Q6 / Q7 / Q8 BINDING.** All ratified by PR #242. Q6's `deferred_blocker_with_algorithm_survey_required` verdict (PR #245) is the trigger for THIS survey. The survey does NOT re-adjudicate Q1-Q4 / Q5 / Q7 / Q8 and does NOT re-adjudicate Q6's "an algorithm survey is required" framing; it only emits a Q6F selected_policy in its own right.

4. **Source layer.** PHA (`player_history_all`) is the rating-update signal source. PHA already restricts to decisive results per PR #242 Q1. `player_history_all.result` is the per-game label; PHA is the only allowed source for the rating-update sequence.

5. **Target anchor for evaluation.** `matches_history_minimal.started_at TIMESTAMP` per PR #242 Q2 BIND_NOW. The survey's per-match predicted probability is computed at this anchor; the rating state used is strictly the rating from PHA records with `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at`.

6. **Strict-`<` filter inherited verbatim.** `STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"` per PR #242 Q3 BIND_NOW. Every rating engine the survey runs must honour this filter; no rating engine may read a PHA record dated at or after the target match's `started_at`.

7. **Q6F candidate set.** EXACTLY 4 included candidates + 2 carry-forward references:
   - **INCLUDED** (4):
     - `rolling_win_rate_or_bayesian_smoothed_baseline` — rating proxy without opponent strength; baseline.
     - `elo` — Elo 1978; logistic expectation; constant K.
     - `glicko_or_glicko_2` — Glickman 1999 / 2012; RD-with-inactivity; §6.2 row 4 spec-favoured candidate.
     - `trueskill_or_trueskill_like` — Herbrich / Minka / Graepel 2006; 1v1 degenerates to Glicko-like.
   - **CARRY-FORWARD** (2; not surveyed because no algorithm to evaluate):
     - `omit_reconstructed_rating` — included as a reference row; the eventual `omit_reconstructed_rating_and_unblock_other_five` Q6F verdict (if selected) is its emergent re-affirmation.
     - `deferred_blocker_with_algorithm_survey_required` — included as a reference row; this row's verdict was set by PR #245 and the Q6F survey's Q6F_selected_policy row is conceptually a successor adjudication of it.

8. **N-1 carry-forward (BTL family explicit rejection).** `aligulac_style_btl`, `bradley_terry`, `neural_btl` are listed in dataset `research_log.md` lines 733-734 + 961 as part of the substrate's intended backtesting universe but EXCLUDED from this survey's candidate set with explicit rejection paragraph in MD §X (same rationale as PR #245 N-1: BTL collapses to Elo-with-race-prior in 1v1; Neural BTL needs its own model-training pipeline). The rejection MUST be re-stated verbatim in every row's `excluded_methods_considered` field. The Layer-2 executor MAY extend the included candidate set to BTL methods IF AND ONLY IF the executor produces its own substantive case with citations + test fixtures; otherwise the rejection stands.

9. **N-2 carry-forward (raw MMR hybrid rejection).** `raw_mmr_where_present_plus_is_mmr_missing` REJECTED unchanged (PR #245 N-2 rationale): violates Invariant I5 symmetric-treatment; rated/unrated partition correlated with skill; partition-as-feature would leak corpus structure. The rejection MUST be re-stated verbatim in every row's `raw_mmr_hybrid_rejection` field.

10. **Hyperparameter policy.** DEFAULT = **fixed literature defaults**:
    - Elo: `K=20` (chess-conservative) OR `K=32` (chess-default); the Layer-2 plan must pick ONE and pin it; planner recommends `K=24` as the midpoint commonly used by aoe2-tournament Elo deployments.
    - Glicko-2: `mu=1500, RD=350, sigma=0.06, tau=0.5` (Glickman 2012 reference defaults).
    - TrueSkill: `mu=25, sigma=25/3, beta=25/6, tau=25/300, draw_margin=0` (Herbrich et al. 2006 defaults; draw_margin=0 because PHA is decisive-only per PR #242 Q1).
    - Rolling baseline: `alpha=beta=1` (Laplace prior); window = expanding (all prior PHA rows for that toon_id); the Layer-2 plan may add a finite-window variant for sensitivity but must pin the primary as expanding.
    
    NO tuned variants in this survey. If the executor needs tuned hyperparameters to break a tie, it must add an OQ to a follow-up PR (e.g., "Q6G tuned-hyperparameter sensitivity") rather than tune inside Q6F. Tuning inside Q6F is barred because (a) leakage-safe nested protocols are complex enough to deserve their own Step, and (b) Q6F is a Layer-2 evidence-only step; binding a tuned hyperparameter is Layer-3 work.

11. **Player identity grouping key.** `toon_id` is the canonical PHA grouping key per PR #245 (PHA does not carry a `player_id_worldwide` column; verified at module-author time in PR #245's adjudicator). The survey MUST use `toon_id` as the rating-engine player key. The Layer-2 module must include a one-sentence comment citing PR #245 §9 confirming this choice.

12. **Survey output rows.** EXACTLY 8 rows (mirroring PR #245's 8-row shape):
    - Row 1: `Q6F_A_omit_reconstructed_rating` (carry-forward; no algorithm; emits zero-metrics)
    - Row 2: `Q6F_B_rolling_win_rate_or_bayesian_smoothed_baseline` (included; metrics computed)
    - Row 3: `Q6F_C_elo` (included; metrics computed)
    - Row 4: `Q6F_D_glicko_or_glicko_2` (included; metrics computed)
    - Row 5: `Q6F_E_trueskill_or_trueskill_like` (included; metrics computed)
    - Row 6: `Q6F_F_deferred_blocker_with_algorithm_survey_required` (carry-forward; this row's verdict represents the Q6 parent's deferral and is re-affirmed if Q6F itself defers)
    - Row 7: `Q6F_selected_policy` (BINDING; verdict emerges from the per-candidate metrics)
    - Row 8: `Q6F_per_family_impact_summary` (derived; broadcasts the Q6F decision over the 6 history-enriched pre_game families)

13. **Materialization permission outcome matrix.**
    - if `Q6F_selected_policy.verdict == bind_now`:
      `materialization_permission = "permitted_for_all_6_families_with_pinned_<algorithm>_hyperparameters_in_next_materialization_pr"`
      where `<algorithm>` is replaced with the selected candidate name verbatim.
    - if `Q6F_selected_policy.verdict in {narrow_with_evidence, recommendation_only}`:
      `materialization_permission = "recommendation_only_blocked_pending_implementation_proof_pr"`
    - if `Q6F_selected_policy.verdict == deferred_blocker`:
      `materialization_permission = "blocked_pending_<reason>"` (the survey MUST name the reason; "more data needed" is not acceptable; acceptable reasons include "no candidate clears the pinned AUC > 0.55 floor", "all candidates have AUC within bootstrap-CI of 0.5", "a wider candidate set is required").
    - if `Q6F_selected_policy.verdict == omit_reconstructed_rating_and_unblock_other_five`:
      `materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"`

14. **`materialized_output_paths` MUST be empty on every row.** No row of the survey CSV may reference any Parquet path. The survey is an adjudication-class artifact; it never produces a feature column.

15. **No status YAML / research_log / ROADMAP mutation.** Per PR #242 / PR #243 / PR #245 precedent for non-closure adjudication PRs. Closure of Step 02_01_03 is reserved for the future Layer-3 materialization PR (or a separate closure PR if `omit_reconstructed_rating_and_unblock_other_five` is selected).

16. **Test target.** ≥150 tests; ≥95% branch coverage on the survey module. This matches the PR #245 test target (315 tests at 99.54% coverage) at the lower bound. The Layer-2 executor may overshoot.

17. **Read-only against DuckDB.** The survey module opens DuckDB in read-only mode. The ONLY writes are the CSV+MD artifact pair plus the test-fixture writes (under `pytest tmp_path`). No DuckDB table is created, dropped, or altered.

18. **Evaluation traces are EPHEMERAL.** The per-game rating-history dictionaries computed during a survey run (e.g., `dict[toon_id, list[(timestamp, rating_state)]]`) live only in process memory during the survey run; they are NOT persisted to Parquet, NOT persisted to JSON, NOT persisted to any disk file other than via the aggregate metrics on each survey row. The Layer-2 module MUST not write any `.parquet` / `.json` / `.npz` / `.pkl` other than the CSV+MD pair. A falsifier (`q6f_rating_trace_persistence_violation`) checks the post-execution directory listing for any unexpected file and halts if it finds one.

### Unknowns (DEFERRED with explicit gating)

- **U1 — Final selected policy.** The executor's substantive reasoning over the survey metrics decides the verdict. The plan does NOT pre-commit a winner.
- **U2 — Exact AUC / log-loss / Brier values.** Computed during execution from the actual PHA stream.
- **U3 — Whether `omit_reconstructed_rating_and_unblock_other_five` is selected.** Depends on whether any included candidate clears the pinned AUC floor (see OQ1).
- **U4 — Whether external WebFetch is required.** DEFAULT: in-repo citations (the 4 author/year strings already pinned in PR #245's module) are sufficient. The Layer-2 executor may invoke WebFetch only for algorithmic implementation details (e.g., Glicko-2 rating-period update formula), not for the citation strings themselves.
- **U5 — Whether the `trueskill` PyPI package is added as a dependency.** OQ3 below; default is hand-coded TrueSkill 1v1 specialisation.

## Literature Context

### Internal (BINDING; read before authoring Layer-2 module)

- `reports/specs/02_02_feature_engineering_plan.md`
  - §6.2 row 4 line 241: "`reconstructed_rating (Glicko-2 or analogous)` — derived from `player_history_all.result` filtered by I3 anchor — `history_time < target_time` (strict)". This is the spec-favoured framing.
  - §9 G-CS-4 line 422: cold-start gate. "The first-match row for any `(player_id, dataset_tag)` (or per-leaderboard partition where applicable) must not be silently dropped. Missingness must be encoded as a `is_first_match` flag, an imputed value with explicit imputation rule, or a separate cold-start branch."
  - §10 G-L-4 line 455: "No `pre_game` or `history_enriched_pre_game` feature may read game T's post-game rating delta or rating-after value."
- PR #245 Q6_selected_policy row's notes verbatim (quoted above in Problem Statement).
- PR #245 Q6D row: "CROSS-02-02 §6.2 row 4 line 241 names 'Glicko-2 or analogous' first — this is the spec-favoured path." This survey honours that as a prior, not a binding.
- PR #245 module CITATION_* constants (4 author/year strings; the Layer-2 module may import them rather than re-author).
- Dataset `research_log.md`:
  - lines 733-734: rating-system backtesting universe (Elo, Glicko, Glicko-2, TrueSkill, Aligulac-style BTL)
  - line 961: cross-dataset-harmonized substrate (Elo, Glicko, Glicko-2, TrueSkill, Aligulac race-conditioned, Bradley-Terry, Neural BTL)
  - line 106 + 1135: 83.95% MFC MMR-missingness / 83.65% PHA MMR-missingness (this is the corpus's structural framing for "why a reconstructed rating is preferable to raw MMR")

### External (CITATION-ONLY; the Layer-2 module pins these as constants)

- **Elo (1978)** — *The Rating of Chessplayers, Past and Present*. New York: Arco. Pinned constant `CITATION_ELO_1978` (verbatim from PR #245 module).
- **Glickman (1999)** — "Parameter estimation in large dynamic paired comparison experiments." *Applied Statistics*, 48: 377-394. Pinned constant `CITATION_GLICKMAN_1999`.
- **Glickman (2012)** — "Example of the Glicko-2 system" (Boston University technical note). Pinned constant `CITATION_GLICKMAN_2012`.
- **Herbrich, Minka, Graepel (2006)** — "TrueSkill™: A Bayesian Skill Rating System." *NIPS 2006*: 569-576. Pinned constant `CITATION_HERBRICH_MINKA_GRAEPEL_2006`.

### When WebFetch is permitted

- For algorithmic implementation details (e.g., Glicko-2 §3 step-by-step update equations; TrueSkill §2 Gaussian factor-graph approximation). The Layer-2 executor may WebFetch these as references for the engine implementations. The plan does NOT pre-bind a Python package choice; OQ3 surfaces this.
- NOT for the citation strings themselves (already pinned in PR #245's module).
- NOT for "best K-factor for SC2" or any tuning-style query (per Assumption 10, hyperparameters are fixed literature defaults).

## Execution Steps

The future Layer-2 execution PR runs T01-T09 in order. Each step lists files, function signatures (where load-bearing), validation report, stop condition, and Sonnet/Opus routing.

The non-batching rule (`data-analysis-lineage.md` §"Non-batching rule for empirical work") REQUIRES that the Layer-2 PR itself respect a per-step sequence (scaffold → validation module → executor checkpoint → artifacts → status update). The Layer-2 PR is permitted to bundle T01-T09 in a single PR ONLY because every prior step (T01-T08) leaves the survey artifacts ungenerated; the artifacts are generated only at T06, after the rating engines (T03), metrics (T04), and per-candidate decision binding (T05) have been validated.

### T01 — Survey module shell (constants + dataclasses + schema)

- File: `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py`
- Mirror PR #245 module's dataclass + constant structure verbatim. Specifically:
  - `Q6F_RATING_ALGORITHM_CANDIDATES: tuple[str, ...]` — the 4 included + 2 carry-forward canonical strings.
  - `Q6F_CANDIDATE_INCLUSION: dict[str, bool]` — maps each candidate to True (included in numeric survey) or False (carry-forward reference).
  - `Q6F_HYPERPARAMETER_DEFAULTS: dict[str, dict[str, float]]` — pinned defaults per Assumption 10.
  - `STRICT_LT_HISTORY_FILTER: str` — imported from PR #245's module verbatim (not re-authored).
  - `CITATION_*` constants — imported from PR #245's module verbatim.
  - `Q6F_SURVEY_SCHEMA: tuple[str, ...]` — 36 column names (see File Manifest).
  - `RatingAlgorithmSurveyDecision` dataclass (1 instance per survey row; 36 fields matching schema).
  - `RatingAlgorithmSurveyResult` dataclass (top-level container).
  - `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` — ≥35 falsifier keys covering parent-SHA mismatch (×6), candidate completeness, byte-determinism, materialization creep, Q5 re-adjudication drift, status drift, research_log drift, ROADMAP drift, no_post_game_token, no_target_match_outcome_read, no_future_match_read, no_global_batch_fit, no_phase_03_baseline_creep, forward-only present per non-omit candidate, cold-start present per non-omit candidate, tie-policy present per non-omit candidate, hyperparameter present per non-omit candidate, evaluation-trace persistence violation, AUC-floor-not-pinned, rating-trace-persistence-violation, q6f_selected_policy_row_missing, q6f_per_family_impact_summary_missing, q6f_decision_count_mismatch (must == 8), q6f_decision_id_order_mismatch.
- Sonnet sufficient (mechanical scaffolding; schema is fully specified in the plan).
- Validation report: dataclass field count matches schema column count; `Q6F_RATING_ALGORITHM_CANDIDATES` length == 6; `Q6F_CANDIDATE_INCLUSION` keys match `Q6F_RATING_ALGORITHM_CANDIDATES`; assert-blocks at module load (mirroring PR #245's `assert len(HELPER_TO_FALSIFIER_KEY) == len(FALSIFIER_PRIORITY_CHAIN)` pattern).
- Stop condition: module imports cleanly; `python -c "import rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms"` returns 0; T02 may begin only after T01 checkpoint commit.

### T02 — Read-only PHA chronological loader

- File: same module; function `_load_pha_history_chronological(db_path: Path) -> pd.DataFrame`.
- Returns the full PHA stream sorted by `(toon_id, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)` — the deterministic ordering inherited from PR #245.
- Read-only DuckDB connection (`duckdb.connect(str(db_path), read_only=True)`).
- Single SQL query: `SELECT toon_id, replay_id, details_timeUTC, result, mmr FROM player_history_all WHERE result IN ('Win', 'Loss') ORDER BY toon_id, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id`. (PHA already decisive per PR #242 Q1; the `WHERE result IN (...)` is defensive belt-and-braces.)
- Returns a DataFrame; downstream rating engines consume it row-by-row.
- Sonnet sufficient.
- Validation report: row count printed; assert row count > 0; assert no NULL `details_timeUTC` after `TRY_CAST`; assert per-toon chronological monotonicity (each `toon_id` group's `details_timeUTC` is non-decreasing).
- Stop condition: validation report shows monotonicity holds; T03 may begin only after T02 checkpoint commit.

### T03 — Per-algorithm rating engines (4 engines + 1 shared cold-start scaffold)

- File: same module; 4 functions:
  - `_run_rolling_baseline_survey(stream: pd.DataFrame) -> dict[str, Any]`
  - `_run_elo_survey(stream: pd.DataFrame, k_factor: float = 24.0) -> dict[str, Any]`
  - `_run_glicko2_survey(stream: pd.DataFrame, mu: float = 1500, rd: float = 350, sigma: float = 0.06, tau: float = 0.5, rating_period_days: int = 30) -> dict[str, Any]`
  - `_run_trueskill_survey(stream: pd.DataFrame, mu: float = 25, sigma: float = 25/3, beta: float = 25/6, tau: float = 25/300, draw_margin: float = 0) -> dict[str, Any]`
- Each returns a dict with:
  - `"predicted_probabilities": np.ndarray` — one per PHA row (the ex-ante predicted P(focal wins) at the time of that row, using rating state from STRICTLY PRIOR rows; `np.nan` for any row where the focal player had no prior history).
  - `"actuals": np.ndarray` — the actual decisive outcome (1.0 for `Win`, 0.0 for `Loss`).
  - `"is_cold_start": np.ndarray` — boolean; True if the focal player's `toon_id` had no PHA row strictly prior to this one.
  - `"rating_state_at_end": dict[str, dict]` — final per-toon rating state (kept in memory for inspection during execution; NOT persisted; falsifier q6f_rating_trace_persistence_violation checks this).
  - `"runtime_ms": float` — wall-clock for the engine run.
- Each engine implements **deterministic forward-only updates**:
  - The stream is sorted chronologically; the engine processes each row in order.
  - Before processing row R, the predicted probability is computed using ONLY the rating state accumulated from rows with strictly-earlier `(toon_id, timestamp, replay_id)` per the strict-`<` filter.
  - After scoring row R, the rating state is updated using R's actual outcome (which becomes input to FUTURE rows' predictions but NEVER to R's own prediction).
  - This is the canonical forward-only rating protocol; it is leakage-safe iff the strict-`<` ordering is maintained.
- Fixed literature defaults per Assumption 10.
- **Opus REQUIRED for T03.** Subtle reasoning required: (a) forward-only semantics — the prediction MUST be computed BEFORE the rating update; reversing the order is a silent leak; (b) cold-start handling per candidate — each engine has a different initial-rating policy; (c) per-pair update — in 1v1 PHA, each PHA row represents one focal player's view of a game; the opponent's `toon_id` is required to update both ratings; the engine must look up (or join in) the opponent's prior rating; (d) Glicko-2 rating-period batching — within a period, all matches are batched, but BETWEEN periods, the state is updated forward; the period boundary must NOT cross the target match.
- Validation report: per engine, print first 10 rows' (`toon_id`, `predicted_probability`, `actual`, `is_cold_start`); assert predicted_probability NaN iff is_cold_start True (or, for engines where the cold-start prior is used to predict, predicted_probability == prior-implied probability and is_cold_start is True separately); assert no row's prediction reads the row's own `result`.
- Stop condition: per-engine validation report shows forward-only invariant holds for all 4 engines; T04 may begin only after T03 checkpoint commit.

### T04 — Metric computation

- File: same module; function `_compute_survey_metrics(engine_output: dict[str, Any]) -> dict[str, float]`.
- Computes per-candidate:
  - `metric_auc` — sklearn `roc_auc_score(actuals[~cold_start], predicted_probabilities[~cold_start])`.
  - `metric_log_loss` — sklearn `log_loss(actuals[~cold_start], predicted_probabilities[~cold_start], labels=[0, 1])`.
  - `metric_brier_or_calibration` — `brier_score_loss(actuals[~cold_start], predicted_probabilities[~cold_start])`.
  - `coverage_rate` — fraction of PHA rows with a non-NaN prediction (i.e., `1 - is_cold_start.mean()` after the cold-start mask is applied).
  - `cold_start_rate` — `is_cold_start.mean()`.
  - `runtime_summary` — formatted "<runtime_ms> ms over <row_count> rows".
- Sonnet sufficient (mechanical; sklearn metrics).
- Validation report: per candidate, print the 3 numeric metrics + 2 rates; assert AUC in [0, 1]; assert log_loss > 0; assert Brier in [0, 0.25]; assert coverage_rate + cold_start_rate ~= 1 (sum within 1e-9).
- **Forward-only sanity**: the metric is computed against future actuals, but the rating INPUT for each prediction never sees the future actual. This is the per-row contract from T03. The metric layer enforces nothing additional; it merely reports the score.
- Stop condition: 4 candidates' metrics tables printed and inspected; T05 may begin only after T04 checkpoint commit.

### T05 — Per-candidate decision rows + emergent Q6F_selected_policy

- File: same module; function `_build_survey_decisions(metrics_by_candidate: dict[str, dict[str, float]], ...) -> tuple[RatingAlgorithmSurveyDecision, ...]`.
- Returns 8 decisions in canonical order (per Assumption 12). For the 4 included candidates, each decision's metric fields are populated from T04. For the 2 carry-forward references, metric fields are populated with sentinel values:
  - `omit_reconstructed_rating`: AUC=0.5 (no-skill baseline; the omission case predicts nothing); log_loss = NaN; Brier = NaN; coverage_rate = 0.0; cold_start_rate = 1.0; runtime_summary = "not_applicable_carry_forward".
  - `deferred_blocker_with_algorithm_survey_required`: all 5 metric fields = "not_applicable_carry_forward" (string sentinel).
- The Q6F_selected_policy row's `selected_policy` value is derived per the following decision rule (this rule MUST be inlined verbatim in the module as a constant `Q6F_SELECTION_DECISION_RULE: str`):

  ```text
  Let M be the set of 4 included candidates with metric_auc populated.
  Let AUC_FLOOR = 0.55 (pinned per OQ1 default; rationale: 0.55 is a 5%-above-no-skill floor commonly used in calibration literature; any lower value is indistinguishable from no-skill within reasonable bootstrap CI).
  Let AUC_BIND_THRESHOLD = 0.60 (pinned default; rationale: 0.60 is a defensible "this algorithm provides genuine forward-only skill signal" floor for a sample of ~22K decisive matches).
  
  IF max(M.metric_auc) < AUC_FLOOR:
    selected_policy = "omit_reconstructed_rating_and_unblock_other_five"
    verdict = "omit_reconstructed_rating_and_unblock_other_five"
    materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"
    rationale = "No included candidate cleared the AUC floor of 0.55; rating reconstruction provides no detectable forward-only skill signal on the sc2egset PHA corpus; recommended to omit the reconstructed_rating family and proceed with the other 5 history-enriched pre_game families."
  ELIF max(M.metric_auc) >= AUC_BIND_THRESHOLD:
    best = argmax(M.metric_auc)
    selected_policy = "bind_now"
    verdict = "bind_now"
    materialization_permission = f"permitted_for_all_6_families_with_pinned_{best}_hyperparameters_in_next_materialization_pr"
    rationale = f"Candidate {best} achieved the highest AUC ({M[best].metric_auc:.4f}) and cleared the AUC bind threshold of 0.60; bind for materialization with the pinned literature-default hyperparameters."
  ELSE:
    # AUC_FLOOR <= max(M.metric_auc) < AUC_BIND_THRESHOLD
    best = argmax(M.metric_auc)
    selected_policy = "narrow_with_evidence"
    verdict = "narrow_with_evidence"
    materialization_permission = "recommendation_only_blocked_pending_implementation_proof_pr"
    rationale = f"Candidate {best} achieved AUC {M[best].metric_auc:.4f}, above the AUC floor (0.55) but below the bind threshold (0.60); recommendation only; an implementation-proof PR is required before Layer-3 materialization."
  ```

- **Opus REQUIRED for T05.** Substantive reasoning: (a) the decision rule above is the planner's default; the executor must re-examine it against actual numbers and may propose an alternative rule in the Layer-2 PR if the actuals reveal a pathology (e.g., all 4 AUCs are bunched within 0.001 of each other); any alternative rule must be justified in the PR description and the Layer-2 reviewer-adversarial must approve it; (b) the per-candidate rejection rationales (one per row of the per-candidate decision table) must be authored substantively — not boilerplate; (c) the Q6F_per_family_impact_summary row's `feature_availability_summary` JSON must broadcast the Q6F selected_policy decision across all 6 families correctly (it differs between `bind_now` ["all 6 unblocked"], `narrow_with_evidence` ["recommendation only; all 6 still blocked at implementation-proof"], `omit_reconstructed_rating_and_unblock_other_five` ["5 unblocked, reconstructed_rating permanently absent"], `deferred_blocker` ["all 6 blocked pending <named reason>"]).
- Validation report: 8 decisions emitted; Q6F_selected_policy row's verdict is one of the 4 allowed; per-candidate metric fields populated.
- Stop condition: 8 decisions reviewed; T06 may begin only after T05 checkpoint commit.

### T06 — Survey CSV + MD writer

- File: same module; function `write_q6f_survey_artifacts(result: RatingAlgorithmSurveyResult, csv_path: Path, md_path: Path) -> None`.
- CSV writer: byte-deterministic (sort decisions by `decision_id`; use canonical CSV dialect; explicit `lineterminator="\n"`; explicit `quoting=csv.QUOTE_MINIMAL`).
- MD writer: ≥17 sections per the MD outline in File Manifest. Mirror PR #245's MD shape but with Q6F-specific section titles.
- Sonnet sufficient.
- Validation report: byte-stability check — run the writer twice, assert the two outputs hash-identical; CSV column count == 36; CSV row count == 9 (1 header + 8 decisions); MD section count >= 17 (assert via `grep -c "^## "`).
- Stop condition: byte-stability holds; T07 may begin only after T06 checkpoint commit.

### T07 — Sandbox jupytext notebook pair

- Files:
  - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.py` (jupytext-paired Python source).
  - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.ipynb` (notebook).
- All logic imported from the survey module; the notebook cells call the public entrypoint and print outputs (per `feedback_notebook_print_vs_logger` — print() for data exploration, logger only for diagnostics).
- No `def`/`class`/`lambda` in cells (per sandbox README contract).
- Outputs cleared before commit (no embedded `outputs` field in `.ipynb`).
- Sonnet sufficient.
- Validation report: notebook executes top-to-bottom without error; final cell prints the Q6F_selected_policy.
- Stop condition: notebook runs cleanly; T08 may begin only after T07 checkpoint commit.

### T08 — Mirrored test file

- File: `tests/rts_predict/games/sc2/datasets/sc2egset/test_survey_history_rating_algorithms.py`.
- Test target: ≥150 tests; ≥95% branch coverage on the survey module.
- Test classes:
  - `TestModuleConstants` — verify `Q6F_RATING_ALGORITHM_CANDIDATES`, `Q6F_CANDIDATE_INCLUSION`, `Q6F_HYPERPARAMETER_DEFAULTS`, `Q6F_SURVEY_SCHEMA`, citation constants, schema-column count, decision-count.
  - `TestParentSHAs` — verify the 6 pinned parent SHAs against the canonical strings; failure case (mismatch) triggers `RatingAlgorithmSurveyError` with the correct falsifier key.
  - `TestRollingBaselineEngine` — synthetic 2-player, 4-row PHA fixture; assert forward-only invariant; assert cold-start handling.
  - `TestEloEngine` — synthetic fixture; assert K=24 default; assert symmetric rating updates.
  - `TestGlicko2Engine` — synthetic fixture; assert mu/RD/sigma defaults; assert rating-period batching does not leak across target.
  - `TestTrueSkillEngine` — synthetic fixture; assert 1v1-decisive degenerates to Gaussian update.
  - `TestMetricComputation` — golden-numbers fixture (predictions [0.6, 0.4, 0.5, 0.7], actuals [1, 0, 1, 1]); assert AUC, log_loss, Brier match hand-computed values within 1e-9.
  - `TestSelectionDecisionRule` — assert each of the 4 outcome branches fires correctly under synthesised metric tables.
  - `TestArtifactWriter` — byte-stability via dual-write hash comparison; CSV column count; MD section count.
  - `TestFalsifierChain` — for each falsifier in `FALSIFIER_PRIORITY_CHAIN`, construct a failing fixture and assert the matching helper raises with the correct `falsifier_key` field.
  - `TestNoMaterializationCreep` — assert `materialized_output_paths` is empty on every decision row; assert no `.parquet` is written anywhere under `tmp_path` after a full survey run.
  - `TestForwardOnlyInvariant` — synthetic fixture where the same player has 3 sequential rows; assert that the prediction for row 2 uses row 1's rating state and NOT row 2's own outcome; assert that the prediction for row 3 uses row 2's POST-UPDATE rating state.
- Sonnet sufficient (mechanically specified given T01-T05 are settled).
- Validation report: `poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_survey_history_rating_algorithms.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.survey_history_rating_algorithms --cov-branch --cov-report=term-missing`; assert ≥150 tests pass; assert ≥95% branch coverage.
- Stop condition: test suite green; T09 may begin only after T08 checkpoint commit.

### T09 — Release tail

- Files:
  - `pyproject.toml` — version `3.75.0 -> 3.76.0`.
  - `CHANGELOG.md` — new `## [3.76.0] - YYYY-MM-DD (PR #N: feat/sc2egset-02-01-03-q6f-rating-algorithm-survey)` block enumerating every file added; verdict outcome string; per Layer-2 reviewer-adversarial verdict.
  - `planning/INDEX.md` — archive PR #245 into the Archive table; new Active entry pointing to the Q6F-survey Layer-2 PR.
- Sonnet sufficient.
- Validation report: pre-commit hooks pass (ruff, mypy, plan-section-check); `git status` shows only the expected files modified.
- Stop condition: PR ready for `@reviewer-adversarial` final gate.

### Adversarial gate

The Layer-2 PR's final gate is `@reviewer-adversarial` (NOT `@reviewer-deep`) because the survey produces methodology-bearing quantitative findings that will inform thesis chapters. The 3-round adversarial cap resets for Layer-2 (per `feedback_adversarial_cap_execution.md` symmetric application).

## File Manifest

### Planning files (created in THIS Layer-1 planning-only PR — 2 files)

| Path | Purpose |
|---|---|
| `planning/current_plan.md` | This plan content (Layer-1; Q6F survey planning) |
| `planning/current_plan.critique.md` | Reviewer-adversarial Round 1 stub (populated by @reviewer-adversarial after this planning round; placeholder in this PR) |

### Future Layer-2 execution files (created in the FUTURE Q6F survey PR — 9 files; NOT this PR)

| # | Path | Purpose |
|---|---|---|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/survey_history_rating_algorithms.py` | Survey module (constants, dataclasses, engines, metrics, writer) |
| 2 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_survey_history_rating_algorithms.py` | Mirrored test file (≥150 tests, ≥95% branch coverage) |
| 3 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.py` | jupytext-paired notebook source |
| 4 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.ipynb` | jupytext-paired notebook |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.csv` | Survey CSV (36 cols × 9 rows incl. header) |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_q6f_rating_algorithm_survey.md` | Survey MD (≥17 sections) |
| 7 | `planning/INDEX.md` | Archive PR #245; new Active entry for Q6F survey Layer-2 PR |
| 8 | `CHANGELOG.md` | New `[3.76.0]` block |
| 9 | `pyproject.toml` | Version bump 3.75.0 -> 3.76.0 |

### Forbidden files (zero-diff for both this Layer-1 PR and the future Layer-2 PR)

| Path / pattern | Reason |
|---|---|
| Any `*.parquet` under any `reports/artifacts/` path | No feature materialization in Q6F |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` | No CROSS-02-01 audit until Layer-3 materialization |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | No Step closure until Layer-3 materialization (or omit-and-unblock follow-up PR) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Derived from STEP_STATUS; no closure here |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Phase 03 stays not_started |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Per PR #242/#243/#245 precedent for non-closure adjudication artifacts |
| `reports/research_log.md` | No CROSS entry; sc2egset-internal |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | ROADMAP stub for 02_01_03 already exists (PR #239); no edit |
| `reports/specs/02_*.md` | Spec edits are CROSS-02-XX-only; Q6F does not amend specs |
| `data/db/schemas/views/*.yaml` | No cleaning-layer/view changes |
| `thesis/**`, `docs/**`, `.claude/**` | Out of scope |
| `data/**` | Out of scope |
| `src/rts_predict/games/aoe2/**`, `tests/rts_predict/games/aoe2/**` | Out of scope (AoE2) |
| `planning/current_plan*.md` in the FUTURE Layer-2 PR | The next planning round overwrites these; Layer-2 inherits, does not edit |
| `sandbox/jupytext.toml` | Existing config; no edit |

### Q6F survey CSV schema (canonical column order; 36 columns)

```
decision_id
parent_decision_id
candidate_policy
algorithm_family
included_in_survey
inclusion_or_rejection_reason
initialization_policy
hyperparameter_policy
cold_start_policy
tie_policy
player_identity_policy
cross_region_policy
forward_only_constraints
metric_auc
metric_log_loss
metric_brier_or_calibration
coverage_rate
cold_start_rate
runtime_summary
complexity_deployability_score
leakage_risk_score
selected_policy
survey_verdict
materialization_permission
evidence_paths
falsifiers
audit_pr
parent_pr242_csv_sha256
parent_pr242_md_sha256
parent_pr243_csv_sha256
parent_pr243_md_sha256
parent_pr245_csv_sha256
parent_pr245_md_sha256
materialized_output_paths
notes
excluded_methods_considered
```

(36 columns. `excluded_methods_considered` is column 36; it carries the JSON list of N-1 carry-forward methods per Assumption 8. `notes` (column 35) carries the per-row substantive rationale plus the N-2 raw-MMR-hybrid rejection string per Assumption 9.)

### Q6F survey MD outline (canonical section order; ≥17 sections)

1. **§1 Non-Materialization Disclaimer** — verbatim mirroring PR #245 §1 with Q6F substitutions; explicitly state "no Parquet, no CROSS-02-01 audit, no Step closure, no Phase 03".
2. **§2 Parent PR #242 Lineage** — verbatim 2 SHAs.
3. **§3 Parent PR #243 Lineage (Q5 Preserved)** — verbatim 2 SHAs; explicit re-affirmation that Q5_selected_policy is preserved.
4. **§4 Parent PR #245 Lineage (Q6 deferred_blocker → this survey)** — verbatim 2 SHAs; quote PR #245's Q6_selected_policy notes verbatim.
5. **§5 Q6F-Only Scope** — explicit declaration that this is NOT Phase 03 modelling; the metrics are evaluation traces, not features. The Q6F survey output is an adjudication-class artifact, not a feature artifact. Explicit list of what Q6F is NOT.
6. **§6 Candidate Set + N-1 Rejection (BTL family)** — verbatim Assumption 8 rejection rationale.
7. **§7 Candidate Set + N-2 Rejection (raw MMR hybrid)** — verbatim Assumption 9 rejection rationale.
8. **§8 Algorithm Specifications per Candidate** — for each of the 4 included candidates, declare: initialization policy, hyperparameter policy (with pinned defaults), cold-start policy (G-CS-4), tie policy (decisive-only), player identity policy (toon_id per PR #245 §9).
9. **§9 Forward-Only Update Semantics** — declare the prediction-before-update protocol; cite PR #245's `STRICT_LT_HISTORY_FILTER` verbatim; declare the deterministic ordering `(toon_id, TRY_CAST(details_timeUTC AS TIMESTAMP), replay_id)`.
10. **§10 Metric Definitions** — AUC, log_loss, Brier, coverage_rate, cold_start_rate, runtime_summary; cite scikit-learn API version.
11. **§11 Per-Candidate Metric Table** — 4 rows (1 per included candidate); 6 columns (the metrics).
12. **§12 Q6F Selected Policy Binding Row** — quote the Q6F_selected_policy row's rationale verbatim from the CSV; include the rejection rationale for the 3 unselected candidates plus the 2 carry-forward references.
13. **§13 Materialization Permission Statement** — verbatim per Assumption 13 outcome matrix branch; explicit statement of which families are unblocked / blocked.
14. **§14 Non-Substitution Statement** — does NOT replace PR #229..#245.
15. **§15 Falsifier Roll-Call** — every key from `FALSIFIER_PRIORITY_CHAIN` with status (did_not_fire / fired); mirror PR #245 §15.
16. **§16 SHA Provenance** — the 6 parent SHAs plus the survey's own `pyproject_version_sha256` for self-audit.
17. **§17 No Step 02_01_03 Closure / No Phase 03 Start** — verbatim mirroring PR #245 §17.

Optional §18 if the executor judges it useful: per-candidate detailed paragraphs (1 per row), mirroring PR #245 §18 shape.

## Gate Condition

### This Layer-1 planning PR is mergeable when ALL of the following hold:

1. Diff contains exactly 2 files: `planning/current_plan.md` (this content) + `planning/current_plan.critique.md` (reviewer-adversarial Round 1 transcript).
2. No file outside the 2 planning paths is touched.
3. Pre-commit hooks pass (ruff, mypy, plan-section-check — verifies the 8 mandatory `##` sections + `## Out of scope` + `## Adversarial-Review Adjustments (Round 1)` are present).
4. `@reviewer-adversarial` Round 1 verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers.
5. PR is in DRAFT state.
6. Branch is `feat/sc2egset-02-01-03-q6f-rating-algorithm-survey`.
7. Base ref is `ee15d3625eee60688776219f533d4a5ceefb4b76` (master HEAD at plan time).

### The future Layer-2 execution PR is mergeable when ALL of the following hold:

1. Diff contains exactly the 9 future-execution files in the manifest.
2. No forbidden file is touched (per the Forbidden table).
3. All 6 parent SHAs match pinned values; SHA-mismatch falsifiers all report `did_not_fire`.
4. All 35+ falsifiers in `FALSIFIER_PRIORITY_CHAIN` report `did_not_fire`.
5. CSV is byte-deterministic (dual-write hash check passes).
6. MD has ≥17 sections.
7. CSV row count == 9 (1 header + 8 decisions); CSV column count == 36.
8. Q6F_selected_policy row exists; its `verdict` is one of `{bind_now, narrow_with_evidence, recommendation_only, deferred_blocker, omit_reconstructed_rating_and_unblock_other_five}`.
9. Q6F_selected_policy row's `materialization_permission` matches the outcome matrix branch for the verdict.
10. Q6F_per_family_impact_summary row exists; its `feature_availability_summary` JSON correctly broadcasts the Q6F decision across all 6 families.
11. `materialized_output_paths` is empty on every row (falsifier `q6f_materialization_creep` did_not_fire).
12. No status YAML / research_log / ROADMAP / Parquet / leakage_audit edit.
13. No Phase 03 reference anywhere in the diff (falsifier `q6f_phase_03_baseline_creep` did_not_fire).
14. ≥150 tests at ≥95% branch coverage on the survey module.
15. Pre-commit hooks pass.
16. Sandbox notebook executes top-to-bottom without error; outputs cleared in committed `.ipynb`.
17. `@reviewer-adversarial` final verdict is APPROVE or APPROVE-WITH-NITS with 0 blockers.
18. PR is ready for merge (not DRAFT) at gate review time.

## Open Questions

7 real ambiguities surfaced for user / reviewer-adversarial decision:

- **OQ1 — AUC floor for omit-and-unblock vs. deferred_blocker.** The plan pins AUC_FLOOR = 0.55 and AUC_BIND_THRESHOLD = 0.60 in T05's selection decision rule. Provisional answer: 0.55 (5% above no-skill) is a defensible floor; 0.60 is a defensible bind threshold. Open: should the floor be raised (e.g., to 0.58, citing the calibration literature's "weak-signal" threshold), or should both thresholds be replaced by a bootstrap-CI-based test (e.g., "lower bound of bootstrap-CI on AUC > 0.5 at α=0.05")? The bootstrap-CI variant is more rigorous but adds implementation complexity. Default for Layer-2: keep the pinned thresholds; surface a follow-up PR ("Q6F-sensitivity") if Layer-2 reveals the result is bunched within bootstrap-CI of the threshold.

- **OQ2 — Hyperparameter tuning in-scope vs. out-of-scope.** Default per Assumption 10: fixed literature defaults; no tuning. Open: if Layer-2 reveals all 4 included candidates' AUCs are bunched at ~0.51 with fixed defaults, should the survey expand scope to tune (a) K-factor for Elo, (b) tau for Glicko-2, (c) beta for TrueSkill? Tuning would require a leakage-safe nested historical-only protocol (e.g., split PHA into a tuning prefix + an evaluation suffix; tune on the prefix; evaluate on the suffix; this respects the strict-`<` filter at the partition boundary). Default for Layer-2: NO tuning; defer to a "Q6G_hyperparameter_tuning" follow-up Step if metrics are bunched.

- **OQ3 — TrueSkill Python package vs. hand-coded.** The `trueskill` PyPI package (Sublee, 2012) is mature, ~150 lines, but adds a dependency. Hand-coded TrueSkill 1v1 specialisation is ~50 lines (Gaussian update; well-documented in §2 of the Herbrich et al. paper). Default for Layer-2: hand-coded (fewer dependencies, full transparency for the thesis defense). If the executor finds the hand-coded version diverges from the published reference, fall back to the PyPI package and document the discrepancy.

- **OQ4 — Cold-start rate threshold for "deployable".** What fraction of cold-start rows is acceptable? Provisional answer: the sc2egset PHA stream has ~22,209 distinct replays and ~22,209 distinct toon_ids on the focal-player side; the first match per toon_id is necessarily cold-start, giving cold_start_rate >= 1/2 (one row per match per side). Realistic cold_start_rate is ~50% if the per-toon trajectory is short, lower if it's long. The metric should be reported but not used as a binding gate.

- **OQ5 — If `bind_now` achieved, does Layer-3 still need an implementation-proof PR?** Default per PR #245 Q6 row pattern (`permitted_for_all_6_families_with_pinned_..._hyperparameters_in_next_materialization_pr`): no — the survey's pinned algorithm + pinned hyperparameters suffice to authorise Layer-3 materialization directly. Open: should there be a separate Layer-2.5 "implementation-proof" PR that runs the chosen algorithm against a small held-out fixture (e.g., the first 100 PHA rows) and shows byte-stable rating outputs before Layer-3 batches the full corpus? Conservative default: no — Layer-3's own validation suite covers this.

- **OQ6 — Calibration plot vs. numeric calibration metric only.** Brier score is a numeric calibration proxy. A calibration plot (predicted vs. actual probability, binned) is visual evidence. The plot would be a 1-figure addition to the MD §11; the MD shape supports it. Default for Layer-2: numeric Brier only (matches PR #245's no-figure precedent); add the plot if the Layer-2 reviewer-adversarial requests it.

- **OQ7 — Provisional verdict guidance if metrics are inconclusive.** If the AUCs of the 4 included candidates are within 0.005 of each other, the planner recommends `narrow_with_evidence` with the spec-favoured candidate (`glicko_or_glicko_2` per §6.2 row 4) as the rationale-cited "winner on prior" rather than on metrics. This honours both Invariant I7 (no magic numbers; we have at least the spec citation as evidence) and the substantive reality (no candidate has earned a `bind_now` verdict). The Layer-2 executor may override.

## Out of scope

The future Layer-2 execution PR must NOT do any of the following. Each is enforced by an explicit falsifier on the `FALSIFIER_PRIORITY_CHAIN`.

- Materialise the `reconstructed_rating` feature column to Parquet (falsifier `q6f_materialization_creep`).
- Persist evaluation traces (per-game rating histories) to disk in any format (falsifier `q6f_rating_trace_persistence_violation`).
- Run any Phase 03 baseline or model-training step (falsifier `q6f_phase_03_baseline_creep`). The metrics computed in T04 are evaluation traces of forward-only rating predictions, NOT Phase-03 baselines; baselines per Phase 03 §7-§8 use a different definition (cross-validated model performance with `create_temporal_split()`'s successor) and are barred. This is the most subtle hard stop.
- Run any train/test split / temporal CV / k-fold (falsifier `q6f_train_test_split_referenced`).
- Touch `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, ROADMAP, research_log, specs, cleaning-layer YAMLs (falsifiers per file: `q6f_status_yaml_drift`, `q6f_research_log_drift`, `q6f_roadmap_drift`, `q6f_spec_drift`, `q6f_cleaning_layer_drift`).
- Re-adjudicate Q5 / Q1-Q4 / Q6 / Q7 / Q8 (falsifier `q6f_q5_re_adjudication_drift` for Q5; analogous helpers for Q1-Q4 / Q6 / Q7 / Q8).
- Start Step 02_01_04 or Phase 03 (falsifier `q6f_step_02_01_04_creep`; falsifier `q6f_phase_03_baseline_creep`).
- Include BTL / Bradley-Terry / Neural BTL as included candidates unless the executor proves a substantive case (N-1 carry-forward; default is rejection paragraph).
- Include raw-MMR-where-present hybrid as a candidate (N-2 carry-forward; rejected unchanged).
- Edit `thesis/**`, `docs/**`, `.claude/**`, `data/**`, AoE2 paths (forbidden-files table).
- Read game T's outcome as a feature INPUT for any rating-update step (it is the survey's evaluation TARGET; falsifier `q6f_target_match_outcome_read_as_input`).
- Read any future-match (`details_timeUTC >= target.started_at`) for rating computation (falsifier `q6f_future_match_leakage_referenced`).
- Run any global / batch fit over future data (falsifier `q6f_global_batch_fit_referenced`).
- Persist any algorithm-specific Python object (e.g., a `glicko2.Rating` instance, a `trueskill.Rating` instance) to disk via pickle / npz / etc. (falsifier `q6f_rating_object_persistence_violation`).
- Modify `pyproject.toml` in this planning PR (only bumped in the future Layer-2 PR; falsifier `q6f_planning_pr_version_bump_violation` on the planning PR).
- Modify `CHANGELOG.md` in this planning PR (only modified in the future Layer-2 PR).
- Modify `planning/INDEX.md` in this planning PR (only modified in the future Layer-2 PR after merge).

## Adversarial-Review Adjustments (Round 1)

`@reviewer-adversarial` Round 1 verdict: **APPROVE-WITH-NITS** (0 blockers; 4 cosmetic nits). All 11 challenge questions PASS. The most subtle risk (Q6F survey drifting into Phase 03 baseline modelling) is enforced by 4 independent falsifiers (`q6f_phase_03_baseline_creep`, `q6f_train_test_split_referenced`, `q6f_global_batch_fit_referenced`, `q6f_target_match_outcome_read_as_input`) plus the T03 prediction-before-update protocol. The evaluation-trace-vs-feature distinction is repeated at 5 locations and Assumption 18's "EPHEMERAL" framing is correct. Full reviewer text captured in `planning/current_plan.critique.md`. Round 1 of 3 adversarial cap consumed.

### Layer-2 executor binding adjustments (must apply)

None of the 4 nits rise to "must-apply binding" — all are cosmetic / wording refinements. However, **NIT-1 and NIT-3 are STRONGLY RECOMMENDED** (the Layer-2 executor SHOULD address them or document why not).

### Layer-2 executor soft adjustments (recommended)

**N-1 — Schema/prose alignment for `raw_mmr_hybrid_rejection`.**

Assumption 9 (under `## Assumptions & Unknowns`) references a "`raw_mmr_hybrid_rejection` field" but the canonical 36-column `Q6F_SURVEY_SCHEMA` carries the N-2 rejection token in the `notes` column (column 35), not in a dedicated `raw_mmr_hybrid_rejection` field. This is consistent with PR #245's pattern (which DID have a `raw_mmr_hybrid_rejection` field as a dedicated column). The Layer-2 executor should choose one path:

- (a) **Preferred:** Add `raw_mmr_hybrid_rejection` as column 37 of `Q6F_SURVEY_SCHEMA`, bringing the schema to 37 columns. Mirrors PR #245's dedicated-column pattern exactly. Update Gate Condition row-count and all schema tests accordingly.
- (b) **Alternative:** Reword Assumption 9 in the future MD §7 to say "the raw-MMR-hybrid rejection token is carried in the `notes` column per row." Keep the schema at 36 columns. Less mirroring of PR #245 but valid.

Document the choice in the Layer-2 PR body. The reviewer's mild preference is (a) for PR #245 parity.

**N-2 — Trivial column-count consistency.**

`## Scope` line says "≥36 columns" — should say "exactly 36 columns" to match the canonical schema declaration. One-word edit.

**N-3 — AUC threshold rationale citation.**

T05's `AUC_FLOOR=0.55` and `AUC_BIND_THRESHOLD=0.60` are pinned with informal rationales ("5% above no-skill ... commonly used in calibration literature" and "defensible 'genuine forward-only skill signal' floor for ~22K decisive matches"). These are borderline Invariant I7 (no magic numbers — every threshold traced to data or citation). The Layer-2 executor should choose one path:

- (a) **Preferred:** Cite a primary source for the floor (e.g., Steyerberg 2009 §5.4 on AUC interpretation; Hosmer-Lemeshow 2013 on weak-discrimination floors); pin the citation as a module-level constant.
- (b) **Alternative:** Compute bootstrap CIs on each candidate's AUC and use the lower-CI-bound > 0.5 test instead of pinning a numeric floor. Avoids the magic-number issue entirely.

OQ1 (in `## Open Questions`) already surfaces this; OQ7 provides a tie-breaking fallback. The plan's default (keep pinned thresholds, surface follow-up PR if metrics are bunched) is defensible but not maximally rigorous.

**N-4 — TrueSkill `tau` justification.**

Assumption 10 sets TrueSkill `tau=25/300` without justification (the `draw_margin=0` rationale at "PHA is decisive-only per PR #242 Q1" IS justified). The Layer-2 executor should add an inline citation to Herbrich-Minka-Graepel (2006) §4 for the default `tau` value, or document the choice as "literature default." Trivial.

### Non-issues considered and dismissed by Round 1

- **Q6F-as-next-atomic-step.** Airtight. Lines 73-79 reject B-F outcomes with cited reasons; the omit-and-unblock-other-five path is correctly subsumed under Q6F itself, not bypassed.
- **Materialization barred.** 5-layer enforcement (Assumption 14, Assumption 18, falsifier `q6f_materialization_creep`, falsifier `q6f_rating_trace_persistence_violation`, falsifier `q6f_rating_object_persistence_violation`).
- **Survey vs Phase 03 baseline.** Clean. 4 falsifiers + T03/T04 protocol enforce.
- **AUC/log-loss/Brier as evaluation targets only.** Clean. T03 "prediction-before-update" protocol explicit; 2 falsifiers enforce.
- **Candidate completeness.** 4 included + 2 carry-forward, justified.
- **BTL / Bradley-Terry / Neural BTL inclusion.** Correctly carried-forward as N-1 rejection from PR #245; executor permitted to expand IFF substantive case + citations + fixtures.
- **Raw MMR hybrid rejection.** Correctly carried-forward as N-2 rejection from PR #245.
- **Q5 binding preserved.** Falsifier `q6f_q5_re_adjudication_drift` enforces.
- **Schema sufficiency and determinism.** 36 columns with proper SHA typing; `materialized_output_paths` gated empty.
- **No status / no research_log / no ROADMAP / no Phase 03 creep.** `## Out of scope` lists 14 forbidden mutations with named falsifiers.
- **Plan-required `##` sections.** All 10 present (8 required + Out of scope + Adversarial-Review Adjustments).
- **Hyperparameter discipline.** Fixed-defaults-only declaration is defensible vs the orchestrator's nested-protocol concern; OQ2 defers tuning to a hypothetical Q6G follow-up Step.
- **Cold-start floor.** Reported but not gated, which is correct given I7.
- **PR-number normalisation workflow.** Standard PR #244/#245 precedent.
- **Branch naming.** Consistent with PR #242/#243/#245 prefix scheme.
- **N-3 player_id_worldwide handling.** PHA grouping key correctly carried forward as `toon_id` per PR #245 §9 (empirical schema constraint).
- **Critique stub format.** Matches PR #244/#245 precedent.

### Round-1 audit trail

- Round 1 of 3 adversarial cap consumed.
- Verdict: APPROVE-WITH-NITS, 0 blockers, 4 cosmetic nits.
- Reviewer: `@reviewer-adversarial`, 2026-05-25.
- Full reviewer transcript: `planning/current_plan.critique.md`.
- Round-2 / Round-3 adversarial cap held in reserve for the Layer-2 execution PR's own final gate.

