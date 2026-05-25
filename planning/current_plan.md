## Scope

**Chosen outcome: A — Q6-only rating-reconstruction successor adjudication planning PR.**

This is a Layer-1 planning-only PR. It authors exactly 2 files — `planning/current_plan.md` (this document) and `planning/current_plan.critique.md` (stub) — under the new branch `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication`. No code, no notebook, no data probe, no adjudication artifact, no status YAML mutation, no ROADMAP edit, no research_log entry are produced by this PR.

The future Layer-2 execution PR that this plan authorises will produce **one and only one** adjudication artifact pair (CSV + MD) at:
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md`

That future PR will upgrade the PR #242 Q6 `deferred_blocker` row by recording a binding / recommendation / re-deferral verdict over a complete `Q6_RATING_POLICY_CANDIDATES` set (omit / rolling-baseline / Elo / Glicko-or-Glicko-2 / TrueSkill-or-TrueSkill-like / deferred-with-survey). **Materialization remains blocked in both PRs.** The Layer-3 materialization PR is a separate downstream artifact and is not authored here.

**Branch:** `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication` (mirrors the PR #243 successor branch convention, swapping `cross-region` → `rating-reconstruction`).

**Category:** A — Phase 02 successor adjudication artifact (not materialization, not closure).

**Version bump:** `3.74.0 → 3.75.0` (minor; Cat A with a new public adjudicator module + 11 future files including a new artifact pair). The planning-only PR itself does not bump (per the planning-only precedent of PR #240 and PR #243's planning sibling); the Layer-2 execution PR bumps.

**Outcomes considered and rejected** (per orchestrator prompt):

- **B (direct materialization).** REJECTED. Q6 remains `deferred_blocker` per PR #242 §2 row Q6. The PR #242 §13 binding gate states: "the future Layer-3 materialization PR must NOT proceed until that decision is upgraded to `bind_now` / `ratify_with_evidence` / `extend_with_evidence` / `narrow_with_evidence`." Materialization without Q6 upgrade would violate that gate and Invariant I7 (no magic number for `K`, rating period, or prior).
- **C (combined Q6 adjudication + materialization in one PR).** REJECTED. Violates the data-analysis-lineage rule's *Non-batching rule for empirical work* ("Do not batch ROADMAP + notebook + artifact + next Step in one execution") and PR #242 §13's "successor adjudication PR" wording (singular adjudication first, then a separately reviewed materialization PR). The PR #243 precedent split Q5 adjudication from materialization for the same reason.
- **D (hygiene-only first).** REJECTED. No real blocker is open: pre-commit hooks pass on master (the recent merges of #242 and #243 were clean), `STEP_STATUS` / `PIPELINE_SECTION_STATUS` / `PHASE_STATUS` are consistent and accurately reflect the deferred state, `planning/INDEX.md` correctly lists PR #243 as Active, and version 3.74.0 in `pyproject.toml` matches CHANGELOG `[3.74.0]`. There is no drift to fix before Q6.
- **E (Phase 03 baselines).** REJECTED. PHASE_STATUS.yaml shows Phase 03 = `not_started`; ml-protocol §4 superseded `create_temporal_split()` is barred from any thesis experiment; the active Phase is 02; Phase 03 cannot start until Phase 02 has at least one pre_game tranche fully closed *and* the history-enriched tranche has either materialized or been formally rejected. Starting Phase 03 here would violate the CLAUDE.md rule "NEVER begin a new phase until all prior phase artifacts exist on disk."
- **F (hold).** REJECTED. State is consistent and Q6 is the unique remaining `deferred_blocker` after PR #243 resolved Q5. Holding would leave Step 02_01_03 indefinitely blocked with no methodology gain.

**Outcome A is uniquely justified** by: (i) PR #242 §13 explicitly names "successor adjudication PR" for each deferred blocker; (ii) PR #243 just resolved Q5 in the same pattern (model template available); (iii) Q6 is the *only* remaining `deferred_blocker` row; (iv) the planning/execution split is mandated by data-analysis-lineage and by CLAUDE.md "Plan / Execute Workflow."

---

## Problem Statement

**The Q6 question (verbatim binding from PR #242 §2 row Q6):**

> Can `reconstructed_rating` (the `history_enriched_pre_game` family bound by §6.2 row 4 of `reports/specs/02_02_feature_engineering_plan.md`) be materialized safely now, and if yes, with which rating-model family?

The PR #242 Q6 row is currently `verdict = deferred_blocker`, `binding_level = deferred_blocker`, `rating_policy = deferred_blocker`. Its rationale text (verbatim from `02_01_03_history_source_anchor_coldstart_adjudication.md` §2-§9 Q6 block):

> deferred_blocker because: per N3, ~83.95% MMR-missing density (verified in the dataset research log; consistent with the registry CSV `is_mmr_missing_flag` family) makes algorithm choice first-order. Pinning Elo / Glicko / Glicko-2 / TrueSkill / a rolling-winrate baseline without empirical evidence of which family handles the unrated / no-rating-history regime best would violate Invariant I7. Four candidate citations exist (Elo 1978; Glickman 1999; Glickman 2012; Herbrich, Minka, Graepel 2006) but binding one over the others requires repo evidence not yet generated. Forward-only constraint explicit: no target-match outcome; no future results; no global batch fit; per-game forward update only. Cold-start handled by initializing rating = literature-prior for new players (DEFERRED to materialization PR's training-fold-fit step); missingness handled by retaining `is_mmr_missing` as a separate companion feature (DEFERRED to materialization PR).

**Binding context the future Q6 artifact must honour (inherited, not re-litigated):**

- **§6.2 row 4 binding** (`reports/specs/02_02_feature_engineering_plan.md` line 241): `reconstructed_rating (Glicko-2 or analogous)` — source `derived from player_history_all.result filtered by I3 anchor`; cutoff `details_timeUTC`; rule `history_time < target_time` (strict); rating state computed strictly from prior decisive results. "Only if temporally disciplined. No global / batch fit; ratings must be reconstructed forward in time. Battle.net MMR is not used as the rating source for this corpus because it is structurally absent for 83.95% of rows; the reconstructed rating is the principled substitute." The §6.2 row 4 wording uses "Glicko-2 *or analogous*" — the policy choice is open within "analogous," not fixed at Glicko-2.
- **§9 G-CS-4 cold-start gate** (line 422): "Missing history must be encoded explicitly. The first-match row for any `(player_id, dataset_tag)` (or per-leaderboard partition where applicable) must not be silently dropped. Missingness must be encoded as a `is_first_match` flag, an imputed value with explicit imputation rule, or a separate cold-start branch."
- **§10 G-L-4 leakage gate** (line 455): "No `pre_game` or `history_enriched_pre_game` feature may read game T's post-game rating delta or rating-after value. A feature reads `new_rating` (aoestats) or any post-match rating field for game T."
- **MMR-missingness density** (research_log line 1135 + line 106): `is_mmr_missing` distribution = `(False=7128, True=37290)` = 83.95% TRUE in `matches_flat_clean`; 83.65% in `player_history_all`. This is not an outlier; it is structural (unrated professional corpus).
- **Q1-Q4 + Q7-Q8 BINDING (from PR #242):** target = `matches_flat_clean` (44,418 rows); history = `player_history_all` (44,817 rows); target anchor = `matches_history_minimal.started_at TIMESTAMP`; history time column = `player_history_all.details_timeUTC` (`TRY_CAST AS TIMESTAMP`); strict filter = `STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"`; cold-start gates G-CS-2..G-CS-6 declared.
- **Q5 BINDING (from PR #243):** `Q5_selected_policy = sensitivity_indicator_co_registration`; verdict `narrow_with_evidence`. Q6's artifact is *strictly forbidden* from re-adjudicating Q5.

**Distinguish three downstream artifacts that this plan does NOT author:**

1. **The Q6 adjudication output (the future Layer-2 PR's CSV + MD pair).** Selects, recommends, or re-defers a rating policy from a complete candidate set. Records the choice with falsifier discipline. Does not run rating reconstruction. Does not materialize a feature value.
2. **The Layer-3 rating-reconstruction materialization PR (downstream of the Q6 PR).** Actually runs the forward rating updates over `player_history_all.result` filtered by the strict-< rule, produces a Parquet column, and runs the CROSS-02-01-v1.0.1 leakage audit. Out of scope here; depends on Q6's selected policy.
3. **The Phase 03 model-training cold-start handling.** Tied to G-CS-6 (fold-aware fit gate). Out of scope here; depends on Phase 03 splitting design.

**Why this PR matters now:** Q6 is the *only* remaining `deferred_blocker` on Step 02_01_03. Once Q6 is upgraded (whether to `bind_now`, `narrow_with_evidence`, `recommendation_only`, or even back to `deferred_with_survey` for a more rigorous reason), the Step 02_01_03 materialization gate becomes open (for the 5 other families if Q6 selects omission, or for all 6 families if Q6 selects an algorithmic policy). Holding Q6 in its current state freezes Phase 02 progress.

---

## Assumptions & Unknowns

### Assumptions (BINDING for the future Layer-2 PR)

The future Q6 execution PR MUST honour every assumption below; the planning PR records them so the executor and reviewer-adversarial can verify them without re-deriving.

1. **Parent provenance — PR #242 (Q1-Q8 except Q5/Q6) is final and not re-litigated.** The future Q6 adjudicator module will pin:
   - `EXPECTED_PR242_CSV_SHA256 = "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"`
   - `EXPECTED_PR242_MD_SHA256  = "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"`
2. **Parent provenance — PR #243 (Q5) is final and not re-litigated.** The future Q6 adjudicator module will pin:
   - `EXPECTED_PR243_CSV_SHA256 = "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"`
   - `EXPECTED_PR243_MD_SHA256  = "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"`
3. **Q5_selected_policy is BINDING and is NOT re-adjudicated.** The Q6 artifact may reference `Q5_selected_policy = sensitivity_indicator_co_registration` in its evidence_paths but MUST NOT emit any row that contradicts, narrows, extends, or supersedes it. The `q6_q5_re_adjudication_drift` falsifier halts if any Q6 row carries a `cross_region_policy` field, mentions strict_exclusion or dual_feature_path in a verdict-bearing field, or attempts to alter Q5's binding.
4. **Source layer = PHA.** `player_history_all` is the history source; `player_history_all.result` is the rating-update signal (per PR #242 Q1 binding + §6.2 row 4 spec language).
5. **Target anchor = `matches_history_minimal.started_at` TIMESTAMP.** Inherited from PR #234 Q2(a) → PR #242 Q2 RATIFY.
6. **Strict filter = `STRICT_LT_HISTORY_FILTER`.** Verbatim: `"TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"`. Inherited from PR #242 Q3 BIND_NOW.
7. **Cross-region policy = `sensitivity_indicator_co_registration`.** Inherited from PR #243 Q5_selected_policy. Q6 must treat this as an external fact; rating reconstruction over PHA history occurs without dropping cross-region rows (per Q5C semantics).
8. **Row counts are fixed:** `matches_flat_clean = 44,418`; `matches_history_minimal = 44,418`; `player_history_all = 44,817`; `matches_flat_clean_distinct_replay_id = 22,209`. These are not re-measured for Q6; they are inherited from PR #242 §10.
9. **MMR-missingness reaffirmation:** the Q6 artifact will re-assert the 83.95% / 83.65% figures (in MD §7) but will NOT re-probe them; the citation is to research_log lines 106 / 1135 / 1546 / 1597-1599 + registry CSV `is_mmr_missing_flag` family.
10. **The 6 history-enriched pre_game families list is fixed:** `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `reconstructed_rating`, `in_game_history_aggregate`, `cross_region_fragmentation_handling`. Q6 strictly only affects `reconstructed_rating` (1 family); the per-family impact summary row (Q6_per_family_impact_summary) broadcasts the policy decision across the 6 family slots so the artifact downstream-consumer interface mirrors PR #243's Q5 artifact.
11. **`Q6_RATING_POLICY_CANDIDATES` is a closed enumerated set with exactly 6 members:**
    - `Q6A_omit_reconstructed_rating` — drop the family entirely; rely on `is_mmr_missing` + rolling-winrate features only.
    - `Q6B_rolling_win_rate_or_bayesian_smoothed_baseline` — Bayesian-smoothed forward-only win rate as a rating proxy (no opponent strength; no draws).
    - `Q6C_elo` — Elo (Elo 1978) with `K`, prior, and tie-policy deferred.
    - `Q6D_glicko_or_glicko_2` — Glicko (Glickman 1999) or Glicko-2 (Glickman 2012) with `RD`, volatility, rating-period, and prior deferred. §6.2 row 4's "Glicko-2 or analogous" language already favours this branch.
    - `Q6E_trueskill_or_trueskill_like` — TrueSkill (Herbrich, Minka, Graepel 2006) with prior, β, τ, draw-margin, and rating-period deferred.
    - `Q6F_deferred_with_algorithm_survey_required` — re-deferred with an explicit algorithm-survey pre-requirement; the survey is itself authored as a separate Step before any selection is bound.
12. **Verdict universe:** `{bind_now, ratify_with_evidence, extend_with_evidence, narrow_with_evidence, recommendation_only, deferred_blocker}`. The planning PR does NOT pre-commit a winner; the Layer-2 PR's substantive Q6 reasoning produces the verdict.
13. **Artifact-pair atomicity:** the Q6 output is exactly one CSV (with ≥30 columns, ≥8 rows) and one MD (with ≥17 §sections). No second artifact pair, no Parquet, no JSON audit, no SQL view.
14. **Read-only DuckDB usage:** the Q6 adjudicator may invoke `_probe_*` helpers for *evidence-availability* counts (e.g., does PHA contain a non-degenerate `result` distribution? does PHA contain a non-degenerate `details_timeUTC` distribution?) but must NOT compute any rating value. Probes are sanity, not algorithm runs.
15. **Materialization permission:** every Q6 row's `materialization_permission` field encodes the consequence of that row's `selected_policy`:
    - For Q6A (omit) selected: `materialization_permission = "permitted_for_other_5_families_without_reconstructed_rating"`.
    - For Q6B-Q6E selected: `materialization_permission = "permitted_for_all_6_families_with_<algorithm>_per_pinned_hyperparameters_in_separate_proof_PR"`.
    - For Q6F selected: `materialization_permission = "blocked_pending_algorithm_survey_PR"`.
16. **No materialized output paths:** `materialized_output_paths` is `""` on every row by construction (mirrors PR #243's pattern).
17. **No status YAML / no ROADMAP / no research_log mutation.** Q6 adjudication does not close Step 02_01_03. Closure is deferred per PR #237 tranche-1 closure precedent.
18. **External citation discipline:** if a Q6 row binds a non-omit, non-deferred policy (B/C/D/E), it MUST cite at least one primary source per the N-X3 strengthened gate from PR #242 (≥1 repo path + ≥1 algorithm citation + forward-only wording + cold-start/missingness wording). External primary sources allowed: Elo (1978), Glickman (1999), Glickman (2012), Herbrich/Minka/Graepel (2006). These are already in PR #242 Q6 row evidence_paths; the Q6 PR may re-pin them by author/year string (no DOI required).

### Unknowns (DEFERRED with explicit gating)

These are open at planning time and resolved during the Layer-2 execution PR.

1. **Q6 row count.** PR #243 used 5 rows (3 options + selected_policy + per_family_impact_summary). Q6 has 6 candidates → 8 rows (6 candidates + selected_policy + per_family_impact_summary). The future planner may add a candidate-comparison row if it strengthens the artifact; the *minimum* is 8.
2. **Which candidate Q6_selected_policy selects.** The plan does not pre-commit a winner. The Q6 execution PR's substantive reasoning produces the choice. Plausible outcomes include `Q6A_omit` (most conservative; preserves G-CS-4 trivially by encoding `is_mmr_missing` + omitting `reconstructed_rating`), `Q6B_rolling_baseline` (low-complexity; Bayesian-smoothed forward-only winrate), `Q6D_glicko_or_glicko_2` (the §6.2 row 4 spec-favoured path), or `Q6F_deferred_with_survey` (if the artifact concludes that even a comparative algorithm survey requires its own Step).
3. **K-factor / rating-period / volatility / RD / prior / draw-margin / β / τ.** All algorithm-specific hyperparameters are DEFERRED to a separate algorithm-implementation-proof PR (OQ2). The Q6 artifact records *which algorithm family* is selected, not the algorithmic constants.
4. **Whether materialization can proceed for the 5 other families when Q6 selects omit (OQ1).** Provisional answer: yes — omission means the `reconstructed_rating` slot is left empty in the projected feature matrix; the other 5 families' materialization is unblocked by the Q6 omit verdict. But this provisional answer is recorded as an Open Question for reviewer decision, not as a binding here.
5. **Whether external WebFetch citations are required (OQ3).** Provisional answer: no — the four primary sources (Elo 1978, Glickman 1999, Glickman 2012, Herbrich-Minka-Graepel 2006) are already in PR #242 Q6 row evidence_paths verbatim and cited in §6.2 row 4. The Q6 artifact may re-cite by author/year string. WebFetch is permitted only if the future executor finds an in-repo citation insufficient for a specific algorithmic claim.
6. **Whether an empirical MMR-missingness re-probe is needed (OQ4).** Provisional answer: no — research_log line 106 already cites the 83.95% figure with the exact DuckDB query that produced it; the registry CSV `is_mmr_missing_flag` row is the canonical reference. The Q6 artifact may reference research_log lines 106 / 1135 / 1546 by line number.
7. **Whether the per-family impact summary row should broadcast over all 6 families (OQ5).** Provisional answer: yes (for downstream-consumer interface uniformity with PR #243's Q5 artifact). Q6 strictly only affects `reconstructed_rating`, so the other 5 families' rows carry `affected_by_q6 = "no"` / `selected_policy = "not_applicable"`. NIT-D-style structured enum.
8. **Whether the Q6 execution PR should pre-emptively author the Layer-3 materialization plan (OQ6).** Provisional answer: no — one-atomic-unit policy; the Layer-3 materialization plan is authored in a separate planning PR after Q6 merges.

---

## Literature Context

**In-repo first (mandatory citations for the future Q6 artifact):**

1. **`reports/specs/02_02_feature_engineering_plan.md` §6.2 row 4** (line 241): the canonical `reconstructed_rating` binding. Source: `player_history_all.result` filtered by I3 anchor; cutoff `details_timeUTC`; rule `history_time < target_time` (strict). Quote: "Glicko-2 or analogous… No global / batch fit; ratings must be reconstructed forward in time. Battle.net MMR is not used as the rating source for this corpus because it is structurally absent for 83.95% of rows; the reconstructed rating is the principled substitute." This binds the family and favours Glicko-2 *or analogous* but does not fix the algorithm; it explicitly admits an open candidate set.
2. **`reports/specs/02_02_feature_engineering_plan.md` §9 G-CS-4** (line 422): "Missing history must be encoded explicitly. The first-match row for any `(player_id, dataset_tag)` (or per-leaderboard partition where applicable) must not be silently dropped. Missingness must be encoded as a `is_first_match` flag, an imputed value with explicit imputation rule, or a separate cold-start branch."
3. **`reports/specs/02_02_feature_engineering_plan.md` §10 G-L-4** (line 455): "No `pre_game` or `history_enriched_pre_game` feature may read game T's post-game rating delta or rating-after value."
4. **`reports/specs/02_02_feature_engineering_plan.md` §6.2 (aoe2 rows 4-5 + aoestats rows 4-5)** (lines 334, 384): `reconstructed_rating (Elo / Glicko-2)` appears in both AoE2 dataset specs — confirms cross-game commitment to forward-only reconstruction. (Citation-only; the Q6 artifact is sc2egset-scoped.)
5. **PR #242 Q6 row notes** (`02_01_03_history_source_anchor_coldstart_adjudication.md` lines 122-136): the four candidate citations (Elo 1978, Glickman 1999, Glickman 2012, Herbrich-Minka-Graepel 2006) and the "Pinning … without empirical evidence … would violate Invariant I7" rationale.
6. **Dataset research_log line 733-734** (`research_log.md`): "per-player-history key for Phase 02 rating-system backtesting (Elo, Glicko, Glicko-2, TrueSkill, Aligulac-style BTL)" — establishes the dataset is sized for rating-method backtesting.
7. **Dataset research_log line 961** (`research_log.md`): "Cross-dataset-harmonized substrate for Phase 02+ rating-system backtesting (Elo, Glicko, Glicko-2, TrueSkill, Aligulac race-conditioned, Bradley–Terry, Neural BTL)" — confirms `matches_history_minimal` was designed for this exact use.
8. **Dataset research_log line 106 + line 1135 + line 1546** (`research_log.md`): the 83.95% MMR-missing density evidence (sentinel = 0; mechanism = unrated professional). Cited verbatim with its derivation SQL by research_log.
9. **Dataset research_log line 1576-1626** (`research_log.md`): the MMR-vs-in-game multivariate analysis showing MMR is decorrelated when the zero-sentinel is included but correlates with APM (ρ=0.206) and SQ (ρ=0.159) when restricted to rated players — directly motivates why a *reconstructed* rating may unlock signal that the raw MMR cannot.
10. **PR #242 Q4 row** (cold-start gate enumeration): G-CS-4 is explicitly assigned to `reconstructed_rating` in the bound cold-start policy string.

**External primary sources (already in PR #242 Q6 row evidence_paths; re-cited by author/year only):**

- **Elo (1978)** — *The Rating of Chessplayers, Past and Present*. Original Elo formulation: forward-only update; pairwise outcome; logistic expectation; constant `K`.
- **Glickman (1999)** — "Parameter estimation in large dynamic paired comparison experiments." Glicko-1: extends Elo with rating deviation (RD) that grows with inactivity; rating period as fundamental unit.
- **Glickman (2012)** — "Example of the Glicko-2 system" / "The Glicko-2 system for rating players" (the modern formulation). Adds rating volatility σ tracking; superior to Glicko-1 for high-variance regimes; the §6.2 row 4 spec-favoured candidate.
- **Herbrich, Minka, Graepel (2006)** — "TrueSkill: A Bayesian Skill Rating System." NIPS 2006. Gaussian skill prior; factor-graph message passing; handles multi-player FFA (degenerates to Elo-like for 1v1); explicit draw-margin parameter.

**External-citation discipline for the future Q6 artifact:**

- Algorithm primary sources are CITATION-ONLY (author + year string in `notes` and in evidence_paths). The Q6 PR does NOT execute, benchmark, or implement any rating algorithm; it adjudicates the *choice* among candidate families. Algorithm implementation is a separate downstream PR.
- WebFetch is permitted only if the future executor finds in-repo citations insufficient for a specific algorithmic claim. Default = use in-repo references.
- The "no magic numbers" Invariant I7 means: if a non-omit, non-deferred policy is selected, the Q6 row's `rating_hyperparameter_policy` field must record "deferred to algorithm-implementation-proof PR" with the constants enumerated (e.g., for Glicko-2: `μ_prior, RD_prior, σ_prior, τ, rating_period_days`).

**Cross-game comparability note (Invariant I8):** Q6 binds `reconstructed_rating` semantics for sc2egset *only*. The aoe2companion and aoestats datasets' analogous adjudications are out of scope here but will be authored in their own dataset-scoped Q6 successor PRs (per Phase scope rule in docs/PHASES.md). The future Q6 artifact may note this cross-game implication in MD §17 ("forward implications") but must not bind anything for aoe2.

---

## Execution Steps

The future Layer-2 execution PR will execute the steps below in order. Each step lists: title, files (allowed / forbidden), function signatures or constants, validation report, stop condition, and whether Sonnet executor suffices or Opus is required.

The non-batching rule applies: T01-T04 may be batched as scaffolding; T05 (substantive Q6 content) MUST be a separate review checkpoint before T06-T09; T05 requires Opus.

### T01 — Adjudicator module: dataclasses, constants, schema constants

**File (create):** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py`

**Forbidden files:** any 02_01_03 Parquet, any leakage_audit_sc2egset.{json,md}, any status YAML, any spec file, any cleaning-layer YAML, any thesis/docs/.claude/data/AoE2 path.

**Stop condition:** module imports cleanly under `python -c "import rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction"`; module-import-time invariant asserts (set equality between `HELPER_TO_FALSIFIER_KEY.values()` and `FALSIFIER_PRIORITY_CHAIN`) all pass.

**Executor:** Sonnet (mechanical scaffolding; the substantive choices are deferred to T05).

**Module contents:**

```python
# Frozen dataclasses
@dataclass(frozen=True)
class RatingReconstructionAdjudicationDecision:
    decision_id: str               # one of Q6_DECISION_IDS
    parent_decision_id: str        # "Q6_rating_policy" for all rows
    decision_name: str
    verdict: str                   # one of ALLOWED_VERDICTS
    binding_level: str             # one of ALLOWED_BINDING_LEVELS
    scope: str
    candidate_policy: str          # one of Q6_RATING_POLICY_CANDIDATES
    selected_policy: str           # blank for per-candidate rows; populated on selected_policy row
    rejected_options: str          # JSON list string; blank on per-candidate rows
    rating_model_family: str
    rating_forward_only_constraints: str
    rating_cold_start_policy: str
    rating_tie_policy: str
    rating_hyperparameter_policy: str
    rating_evidence_level: str     # NIT-D structured enum
    mmr_missingness_summary: str   # references research_log lines 106/1135 verbatim
    feature_availability_summary: str
    complexity_deployability_score: str    # NIT-D structured enum
    leakage_risk_score: str                # NIT-D structured enum
    materialization_permission: str        # NIT-D structured enum (see Assumption 15)
    evidence_paths: str             # newline-joined; ≥1 repo path required for non-omit
    falsifiers: str                 # JSON list of falsifier keys that fired (empty = pass)
    audit_pr: str                   # "PR #N"
    parent_pr242_csv_sha256: str
    parent_pr242_md_sha256: str
    parent_pr243_csv_sha256: str
    parent_pr243_md_sha256: str
    pr241_scaffold_validator_module_sha256: str
    cross_02_02_spec_sha256: str
    feature_family_registry_csv_sha256: str
    dataset_research_log_sha256: str
    player_history_all_yaml_sha256: str
    matches_flat_clean_yaml_sha256: str
    matches_history_minimal_yaml_sha256: str
    materialized_output_paths: str  # always "" by construction
    notes: str

@dataclass(frozen=True)
class RatingReconstructionAdjudicationResult:
    decisions: tuple[RatingReconstructionAdjudicationDecision, ...]
    halting_falsifier: str | None
    passed: bool

# Constants (UPPER_SNAKE per Invariant I7)
Q6_RATING_POLICY_CANDIDATES = (
    "omit_reconstructed_rating",
    "rolling_win_rate_or_bayesian_smoothed_baseline",
    "elo",
    "glicko_or_glicko_2",
    "trueskill_or_trueskill_like",
    "deferred_blocker_with_algorithm_survey_required",
)

Q6_DECISION_IDS = (
    "Q6A_omit_reconstructed_rating",
    "Q6B_rolling_win_rate_or_bayesian_smoothed_baseline",
    "Q6C_elo",
    "Q6D_glicko_or_glicko_2",
    "Q6E_trueskill_or_trueskill_like",
    "Q6F_deferred_with_algorithm_survey",
    "Q6_selected_policy",
    "Q6_per_family_impact_summary",
)  # 8 rows total

ALLOWED_VERDICTS = (
    "bind_now",
    "ratify_with_evidence",
    "extend_with_evidence",
    "narrow_with_evidence",
    "recommendation_only",
    "deferred_blocker",
)

ALLOWED_BINDING_LEVELS = (
    "binding_for_materialization",
    "recommendation_only",
    "deferred_blocker",
)

ALLOWED_RATING_EVIDENCE_LEVELS = (
    "in_repo_only",          # ≥1 repo path; no external citation needed
    "in_repo_plus_citation", # ≥1 repo path + ≥1 algorithm primary citation
    "deferred",              # for Q6F or Q6_per_family_impact_summary rows
)

ALLOWED_COMPLEXITY_DEPLOYABILITY = (
    "low", "medium", "high", "not_applicable",
)

ALLOWED_LEAKAGE_RISK = (
    "low_if_forward_only_enforced",
    "medium_if_forward_only_enforced",
    "high_if_global_fit_used",
    "not_applicable",
)

ALLOWED_MATERIALIZATION_PERMISSION = (
    "permitted_for_other_5_families_without_reconstructed_rating",   # Q6A
    "permitted_for_all_6_families_with_pinned_hyperparameters_pr",   # Q6B-E
    "blocked_pending_algorithm_survey_pr",                            # Q6F
    "not_applicable",                                                 # per-family rows
)

# Parent provenance SHAs (BINDING; mismatch halts)
EXPECTED_PR242_CSV_SHA256 = "f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b"
EXPECTED_PR242_MD_SHA256  = "fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d"
EXPECTED_PR243_CSV_SHA256 = "29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424"
EXPECTED_PR243_MD_SHA256  = "026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719"
EXPECTED_PR241_VALIDATOR_SHA256 = "b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904"
# Source-file SHAs (NIT-B; pinned at planning time; mismatch halts)
EXPECTED_CROSS_02_02_SPEC_SHA256 = "<resolve at Layer-2 plan time>"
EXPECTED_FEATURE_FAMILY_REGISTRY_CSV_SHA256 = "<resolve at Layer-2 plan time>"
EXPECTED_DATASET_RESEARCH_LOG_SHA256 = "<resolve at Layer-2 plan time>"
EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256 = "<resolve at Layer-2 plan time>"
EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256 = "<resolve at Layer-2 plan time>"
EXPECTED_MATCHES_HISTORY_MINIMAL_YAML_SHA256 = "<resolve at Layer-2 plan time>"

# Inherited from PR #242 (referenced; NOT re-derived)
TARGET_SOURCE_TABLE = "matches_flat_clean"
HISTORY_SOURCE_TABLE = "player_history_all"
TARGET_ANCHOR_COLUMN = "matches_history_minimal.started_at"   # TIMESTAMP
HISTORY_TIME_COLUMN = "player_history_all.details_timeUTC"
STRICT_LT_HISTORY_FILTER = "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at"
EXPECTED_MFC_ROW_COUNT = 44418
EXPECTED_MHM_ROW_COUNT = 44418
EXPECTED_PHA_ROW_COUNT = 44817
EXPECTED_MFC_DISTINCT_REPLAY_ID_COUNT = 22209
EXPECTED_MMR_MISSING_DENSITY_MFC_PCT = 83.95   # research_log line 106
EXPECTED_MMR_MISSING_DENSITY_PHA_PCT = 83.65   # research_log line 1135

# Inherited from PR #243 (referenced; NOT re-litigated)
Q5_SELECTED_POLICY = "sensitivity_indicator_co_registration"
Q5_SELECTED_POLICY_VERDICT = "narrow_with_evidence"

# Algorithm primary-source citations (author/year strings; per N-X3 strengthened gate)
CITATION_ELO_1978 = "Elo (1978) — The Rating of Chessplayers, Past and Present"
CITATION_GLICKMAN_1999 = "Glickman (1999) — Parameter estimation in large dynamic paired comparison experiments"
CITATION_GLICKMAN_2012 = "Glickman (2012) — The Glicko-2 system for rating players"
CITATION_HERBRICH_MINKA_GRAEPEL_2006 = "Herbrich, Minka, Graepel (2006) — TrueSkill: A Bayesian Skill Rating System"

# 6 history-enriched pre_game family IDs (FIXED; for per_family_impact_summary)
HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS = (
    "focal_player_history",
    "opponent_player_history",
    "matchup_history_aggregate",
    "reconstructed_rating",       # the ONE family Q6 affects
    "in_game_history_aggregate",
    "cross_region_fragmentation_handling",
)

# 5 non-rating families (the materialization permission target if Q6A selected)
NON_RATING_HISTORY_FAMILIES = tuple(
    f for f in HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS if f != "reconstructed_rating"
)  # 5-tuple
```

**Validation report (T01 stop condition):** import succeeds; `len(HELPER_TO_FALSIFIER_KEY) == len(FALSIFIER_PRIORITY_CHAIN)` (B4 invariant); `set(HELPER_TO_FALSIFIER_KEY.values()) == set(FALSIFIER_PRIORITY_CHAIN)`; `len(Q6_RATING_POLICY_CANDIDATES) == 6`; `len(Q6_DECISION_IDS) == 8`; `len(HISTORY_ENRICHED_PRE_GAME_FAMILY_IDS) == 6`; `len(NON_RATING_HISTORY_FAMILIES) == 5`.

---

### T02 — Adjudicator module: SQL probe constants (evidence-availability, not rating runs)

**File (extend):** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py`

**Forbidden files:** same as T01.

**Stop condition:** the SQL constants compile under DuckDB's parser; the SQL strings contain no POST-GAME tokens scanned by the universal scanner (Q6 falsifier set); the probes do NOT compute Elo/Glicko/TrueSkill ratings; the probes do NOT read target-match outcomes for prediction rows.

**Executor:** Sonnet.

**Probes (read-only DuckDB; sanity / evidence-availability ONLY):**

```python
# Probe 1: PHA result distribution (1000-row LIMIT smoke; verify non-degenerate)
PROBE_PHA_RESULT_DISTRIBUTION_SQL = """
SELECT result, COUNT(*) AS n
FROM (SELECT result FROM player_history_all LIMIT 1000) sub
GROUP BY result
ORDER BY n DESC
"""
# expected: at least 2 distinct non-null values (decisive game results exist)

# Probe 2: PHA details_timeUTC strict-< ordering smoke (1000-row LIMIT)
PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_SQL = """
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE TRY_CAST(details_timeUTC AS TIMESTAMP) IS NULL) AS null_after_cast
FROM (SELECT details_timeUTC FROM player_history_all LIMIT 1000) sub
"""
# expected: null_after_cast == 0 (inherited from PR #242 Q3 BIND_NOW; re-asserted)

# Probe 3: MMR-missingness re-affirmation against matches_flat_clean
PROBE_MFC_MMR_MISSING_DENSITY_SQL = """
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE MMR = 0) AS mmr_zero
FROM matches_flat_clean
"""
# expected: total == EXPECTED_MFC_ROW_COUNT (44418); mmr_zero == 37290; ratio == 83.95%

# Probe 4: MMR-missingness re-affirmation against player_history_all
PROBE_PHA_MMR_MISSING_DENSITY_SQL = """
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE MMR = 0) AS mmr_zero
FROM player_history_all
"""
# expected: total == 44817 (or near; research_log shows 37489/44817 ≈ 83.65%)

# Probe 5: PHA per-player history depth distribution (evidence for cold-start prevalence)
PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_SQL = """
SELECT cnt_bucket, COUNT(*) AS n_players
FROM (
    SELECT CASE
        WHEN n = 1 THEN '1'
        WHEN n BETWEEN 2 AND 4 THEN '2-4'
        WHEN n BETWEEN 5 AND 9 THEN '5-9'
        WHEN n BETWEEN 10 AND 24 THEN '10-24'
        ELSE '25+'
    END AS cnt_bucket
    FROM (
        SELECT toon_id, COUNT(*) AS n FROM player_history_all GROUP BY toon_id
    ) sub
) bucketed
GROUP BY cnt_bucket
ORDER BY cnt_bucket
"""
# expected: non-degenerate distribution; the '1' bucket cardinality directly motivates
# the G-CS-4 cold-start gate (first-match rows that cannot have a reconstructed rating)
# NOTE: this is evidence-availability for the cold-start branch, not rating computation.

# Probe 6: PHA result vs MMR-presence cross-tab (evidence for whether rating
# reconstruction can run over the unrated regime)
PROBE_PHA_RESULT_VS_MMR_PRESENCE_SQL = """
SELECT
    CASE WHEN MMR = 0 THEN 'unrated' ELSE 'rated' END AS rating_regime,
    result,
    COUNT(*) AS n
FROM player_history_all
GROUP BY 1, 2
ORDER BY 1, 2
"""
# expected: 'unrated' regime contains non-degenerate result distribution
# (i.e., unrated games are decisive; reconstruction CAN run on them)
```

**Validation report:** each probe runs against `data/db/db.duckdb` and returns a non-degenerate non-error result; the smoke counts match the EXPECTED_* anchors; no probe reads `result` for any target row (probes operate over `player_history_all` only, never the target slice).

**Q6 substantive use of probes (T05):** the probes establish that rating reconstruction has sufficient input signal (decisive results exist), can run over the unrated regime (the regime where MMR is absent), and faces a real cold-start tail (per-player depth distribution). They do NOT establish *which* algorithm is best; that adjudication is content of T05.

---

### T03 — Adjudicator module: halting falsifier helpers

**File (extend):** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py`

**Forbidden files:** same as T01.

**Stop condition:** every helper is callable with the entrypoint's signature; `HELPER_TO_FALSIFIER_KEY` maps every helper to a unique falsifier key; `FALSIFIER_PRIORITY_CHAIN` contains every value of `HELPER_TO_FALSIFIER_KEY` exactly once; the universal POST-GAME token scanner does not flag any constant in the module.

**Executor:** Sonnet (mechanical, mirrors PR #242 / PR #243 helper patterns).

**Falsifier helpers (≥ 30, mirroring PR #243's 31-helper pattern):**

| # | Helper | Falsifier key | Halt reason |
|---|--------|---------------|-------------|
| 1 | `_check_parent_pr242_csv_sha256` | `parent_pr242_csv_sha256_mismatch` | PR #242 CSV byte-drifted |
| 2 | `_check_parent_pr242_md_sha256` | `parent_pr242_md_sha256_mismatch` | PR #242 MD byte-drifted |
| 3 | `_check_parent_pr243_csv_sha256` | `parent_pr243_csv_sha256_mismatch` | PR #243 CSV byte-drifted |
| 4 | `_check_parent_pr243_md_sha256` | `parent_pr243_md_sha256_mismatch` | PR #243 MD byte-drifted |
| 5 | `_check_pr241_validator_sha256` | `pr241_sha256_mismatch` | PR #241 validator drifted |
| 6 | `_check_cross_02_02_spec_sha256` | `cross_02_02_spec_sha256_mismatch` | spec drifted |
| 7 | `_check_feature_family_registry_csv_sha256` | `feature_family_registry_csv_sha256_mismatch` | registry CSV drifted |
| 8 | `_check_dataset_research_log_sha256` | `dataset_research_log_sha256_mismatch` | research_log drifted |
| 9 | `_check_player_history_all_yaml_sha256` | `player_history_all_yaml_sha256_mismatch` | PHA YAML drifted |
| 10 | `_check_matches_flat_clean_yaml_sha256` | `matches_flat_clean_yaml_sha256_mismatch` | MFC YAML drifted |
| 11 | `_check_matches_history_minimal_yaml_sha256` | `matches_history_minimal_yaml_sha256_mismatch` | MHM YAML drifted |
| 12 | `_check_q6_candidate_set_complete` | `q6_candidate_set_incomplete` | `Q6_RATING_POLICY_CANDIDATES` missing required candidate |
| 13 | `_check_q6_omit_candidate_present` | `q6_omit_candidate_missing` | `omit_reconstructed_rating` row absent |
| 14 | `_check_q6_deferred_candidate_present` | `q6_deferred_blocker_candidate_missing` | `deferred_blocker_with_algorithm_survey_required` row absent |
| 15 | `_check_decision_count` | `decision_count_mismatch` | `len(decisions) != 8` |
| 16 | `_check_decision_ids_canonical_order` | `decision_id_order_mismatch` | decisions not in `Q6_DECISION_IDS` order |
| 17 | `_check_no_post_game_token_in_scoped_fields` | `q6_post_game_token_in_scoped_field` | POST-GAME token in `selected_policy` / `rating_model_family` / `evidence_paths` / non-exempt fields |
| 18 | `_check_no_direct_target_match_outcome_reference` | `q6_direct_target_match_outcome_referenced` | scoped field references target.result / target.winner / target.outcome |
| 19 | `_check_no_future_match_reference` | `q6_future_match_leakage_referenced` | scoped field references `history_time > target_time` or similar |
| 20 | `_check_no_global_batch_fit_reference` | `q6_global_batch_fit_referenced` | scoped field permits a global/batch rating fit (verbatim: 'global fit' / 'batch fit' / 'fit on full corpus') |
| 21 | `_check_no_phase_03_baseline_creep` | `q6_phase_03_baseline_creep` | scoped field references Phase 03 baseline modeling |
| 22 | `_check_forward_only_constraint_present_when_non_omit` | `q6_forward_only_constraint_missing_for_non_omit_candidate` | non-omit candidate row missing forward-only wording in `rating_forward_only_constraints` |
| 23 | `_check_cold_start_policy_present_when_non_omit` | `q6_cold_start_policy_missing_for_non_omit_candidate` | non-omit row missing G-CS-4 wording in `rating_cold_start_policy` |
| 24 | `_check_tie_policy_present_when_non_omit` | `q6_tie_policy_missing_for_non_omit_candidate` | non-omit row missing tie/draw wording in `rating_tie_policy` |
| 25 | `_check_hyperparameter_policy_present_when_non_omit` | `q6_hyperparameter_policy_missing_for_non_omit_candidate` | non-omit row missing 'deferred to algorithm-implementation-proof PR' wording |
| 26 | `_check_evidence_level_valid` | `q6_evidence_level_field_invalid` | `rating_evidence_level not in ALLOWED_RATING_EVIDENCE_LEVELS` |
| 27 | `_check_complexity_deployability_valid` | `q6_complexity_deployability_invalid` | enum invalid |
| 28 | `_check_leakage_risk_valid` | `q6_leakage_risk_invalid` | enum invalid |
| 29 | `_check_materialization_permission_valid` | `q6_materialization_permission_invalid` | enum invalid for the selected_policy |
| 30 | `_check_external_citation_present_when_non_omit_non_deferred` | `q6_external_citation_missing_when_non_omit_selected` | `selected_policy` in {elo, glicko_*, trueskill_*} but evidence_paths lacks the corresponding citation string |
| 31 | `_check_mmr_missingness_summary_present` | `q6_mmr_missingness_summary_missing` | `mmr_missingness_summary` empty or missing the 83.95% / 83.65% figures |
| 32 | `_check_materialization_permission_consistent_with_verdict` | `q6_materialization_permission_drift` | e.g., `verdict = deferred_blocker` but `materialization_permission != blocked_*` |
| 33 | `_check_q5_not_re_adjudicated` | `q6_q5_re_adjudication_drift` | any row carries a `cross_region_policy` field or attempts to re-bind Q5 |
| 34 | `_check_no_status_yaml_path_referenced` | `q6_status_yaml_drift` | scoped field references STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS path |
| 35 | `_check_no_research_log_mutation_implied` | `q6_research_log_drift` | scoped field implies a research_log append |
| 36 | `_check_no_roadmap_path_modified` | `q6_roadmap_drift` | scoped field implies a ROADMAP edit |
| 37 | `_check_no_materialized_output_paths_populated` | `q6_materialization_creep` | any row's `materialized_output_paths != ""` |
| 38 | `_check_universal_tracker_source_in_history` | `universal_tracker_source_in_history` | tracker-events source name in any scoped field |
| 39 | `_check_per_family_impact_summary_row_present` | `q6_per_family_impact_summary_missing` | the Q6_per_family_impact_summary row absent |
| 40 | `_check_selected_policy_row_present` | `q6_selected_policy_row_missing` | the Q6_selected_policy row absent |
| 41 | `_check_selected_policy_in_candidate_set` | `q6_selected_policy_not_in_candidate_set` | `selected_policy` value not in `Q6_RATING_POLICY_CANDIDATES` |
| 42 | `_check_selected_policy_verdict_consistent` | `q6_selected_policy_verdict_invalid` | selected_policy row's verdict not in ALLOWED_VERDICTS |
| 43 | `_check_per_family_impact_broadcasts_all_6_families` | `q6_per_family_impact_broadcast_incomplete` | per_family_impact_summary row doesn't reference all 6 family IDs |

Final count target: **≥ 30 helpers** (43 above is comfortably above the floor; pruning permitted at Layer-2 execution time if a check is genuinely redundant, but the candidate-set / external-citation / Q5-no-re-adjudication / no-status-yaml-drift / no-roadmap-drift / no-materialization-creep helpers are non-negotiable).

**B4 invariant (set equality):**

```python
assert set(HELPER_TO_FALSIFIER_KEY.values()) == set(FALSIFIER_PRIORITY_CHAIN), (
    "B4 invariant violation: HELPER_TO_FALSIFIER_KEY values do not match FALSIFIER_PRIORITY_CHAIN"
)
assert len(FALSIFIER_PRIORITY_CHAIN) == len(set(FALSIFIER_PRIORITY_CHAIN)), (
    "B4 invariant violation: FALSIFIER_PRIORITY_CHAIN contains duplicates"
)
```

---

### T04 — Adjudicator module: public entrypoint with priority chain

**File (extend):** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py`

**Forbidden files:** same as T01.

**Stop condition:** entrypoint signature matches the call pattern in T07 notebook; priority-chain execution returns `(result, halting_falsifier or None)`; CSV / MD writes are gated on `result.passed`.

**Executor:** Opus (entrypoint orchestrates the falsifier discipline + the substantive Q6 row content from T05; Sonnet may scaffold the priority loop but Opus reviews).

```python
def adjudicate_history_rating_reconstruction(
    *,
    duckdb_path: Path,
    parent_pr242_csv_path: Path,
    parent_pr242_md_path: Path,
    parent_pr243_csv_path: Path,
    parent_pr243_md_path: Path,
    pr241_validator_module_path: Path,
    cross_02_02_spec_path: Path,
    feature_family_registry_csv_path: Path,
    dataset_research_log_path: Path,
    player_history_all_yaml_path: Path,
    matches_flat_clean_yaml_path: Path,
    matches_history_minimal_yaml_path: Path,
    csv_out_path: Path,
    md_out_path: Path,
    audit_pr: str,        # "PR #N" once N is known at Layer-2 time
    audit_date: str,      # "YYYY-MM-DD"
) -> RatingReconstructionAdjudicationResult:
    ...
    # 1. SHA pin checks (helpers 1-11)
    # 2. Probe DuckDB for evidence-availability (probes 1-6); abort if any probe degenerate
    # 3. Build the 8 RatingReconstructionAdjudicationDecision rows (T05 substantive content)
    # 4. Run helpers 12-43 against the row set in FALSIFIER_PRIORITY_CHAIN order
    # 5. If any falsifier fires: return (result, falsifier_key); DO NOT write CSV/MD
    # 6. If all pass: byte-deterministically write CSV (one row per Q6_DECISION_IDS in canonical order)
    # 7. Byte-deterministically write MD (sections per File Manifest)
    # 8. Return result with passed=True, halting_falsifier=None
```

---

### T05 — Per-decision binding (the substantive Q6 content)

**File (extend):** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py` (the row constructors are module-level functions returning `RatingReconstructionAdjudicationDecision` instances).

**Forbidden files:** same as T01.

**Stop condition:** all 8 rows constructible; each row's `notes` field is exempt from POST-GAME token scanning (per B-X1 carry-over); each row's `evidence_paths` contains at least one real on-disk path; non-omit non-deferred rows contain at least one of the 4 algorithm citation strings.

**Executor:** **Opus REQUIRED.** This is the only substantive-methodology step; it requires reasoning about tradeoffs, leakage protection per algorithm family, cold-start support, and the verdict-emergence discipline. A Sonnet executor must not author T05.

**Row-by-row substantive content (the Q6 PR author fills in verdicts; this plan records the row skeletons):**

**Row Q6A — `Q6A_omit_reconstructed_rating`** (candidate row):
- `verdict` ∈ ALLOWED_VERDICTS; `binding_level` typically `recommendation_only` (a candidate, not the chosen).
- `candidate_policy = "omit_reconstructed_rating"`.
- `rating_model_family = "none"`.
- `rating_forward_only_constraints = "not_applicable_omitted"`.
- `rating_cold_start_policy = "G-CS-4_trivially_satisfied_by_omission_plus_is_mmr_missing_flag"`.
- `rating_tie_policy = "not_applicable_omitted"`.
- `rating_hyperparameter_policy = "not_applicable_omitted"`.
- `rating_evidence_level = "in_repo_only"` (no algorithm citation needed for omission).
- `complexity_deployability_score = "low"`.
- `leakage_risk_score = "not_applicable"`.
- `mmr_missingness_summary` = "MMR missing in 83.95% of matches_flat_clean rows / 83.65% of player_history_all rows; is_mmr_missing flag co-registered per §6.2 row 'is_mmr_missing (PRE_GAME flag)' (line 228) remains the primary skill-signal proxy."
- `feature_availability_summary` = "5 of 6 history-enriched pre_game families remain available for materialization (focal_player_history, opponent_player_history, matchup_history_aggregate, in_game_history_aggregate, cross_region_fragmentation_handling). The reconstructed_rating slot is empty."
- `notes` includes the rationale that omission is the strongest cold-start posture (no synthetic rating fabricated for first-match rows) but loses cross-player skill comparability.

**Row Q6B — `Q6B_rolling_win_rate_or_bayesian_smoothed_baseline`** (candidate row):
- `candidate_policy = "rolling_win_rate_or_bayesian_smoothed_baseline"`.
- `rating_model_family = "bayesian_smoothed_rolling_win_rate"`.
- `rating_forward_only_constraints = "strict_lt_history_filter_per_PR_242_Q3_BIND_NOW_then_running_beta_binomial_or_empirical_bayes_update"`.
- `rating_cold_start_policy = "G-CS-4_via_global_prior_alpha_beta_with_is_first_match_flag_co_registered"`.
- `rating_tie_policy = "not_applicable_decisive_only_per_PR_242_Q1_history_filter"` (PHA already restricted to decisive results).
- `rating_hyperparameter_policy = "alpha_prior_beta_prior_window_length_deferred_to_algorithm_implementation_proof_PR"`.
- `rating_evidence_level = "in_repo_only"` (no opponent-strength model; no external citation needed; rolling winrate is in CROSS-02-02 §6.2 row 1 verbatim).
- `complexity_deployability_score = "low"`.
- `leakage_risk_score = "low_if_forward_only_enforced"`.
- `notes` notes this is a *baseline* not a true rating: it does not model opponent strength, so it cannot distinguish a 50% winrate against weak opponents from a 50% winrate against strong ones. Worth recording as a candidate because its leakage surface is the smallest.

**Row Q6C — `Q6C_elo`** (candidate row):
- `candidate_policy = "elo"`.
- `rating_model_family = "elo_per_player_id_worldwide_grouped"`.
- `rating_forward_only_constraints = "STRICT_LT_HISTORY_FILTER_then_per_pair_forward_update_chronologically_ordered_by_TRY_CAST_details_timeUTC_AS_TIMESTAMP_with_replay_id_tiebreaker"`.
- `rating_cold_start_policy = "G-CS-4_via_literature_prior_1500_for_first_match_with_is_first_match_flag_co_registered"`.
- `rating_tie_policy = "PHA_history_already_decisive_per_PR_242_Q1_no_explicit_draw_handling"`.
- `rating_hyperparameter_policy = "K_factor_and_initial_rating_deferred_to_algorithm_implementation_proof_PR"`.
- `rating_evidence_level = "in_repo_plus_citation"`.
- `evidence_paths` includes `CITATION_ELO_1978` + `reports/specs/02_02_feature_engineering_plan.md (§6.2 row 4; §9 G-CS-4)` + the dataset research_log lines 733-734 / 961 / 792 / 837.
- `complexity_deployability_score = "low"` (simplest principled rating).
- `leakage_risk_score = "low_if_forward_only_enforced"`.
- `notes` weighs Elo's lack of inactivity decay (vs Glicko-RD).

**Row Q6D — `Q6D_glicko_or_glicko_2`** (candidate row):
- `candidate_policy = "glicko_or_glicko_2"`.
- `rating_model_family = "glicko_or_glicko_2_per_player_id_worldwide_grouped"` (the PR may sub-specify).
- `rating_forward_only_constraints` = same as Q6C with the addition of "per-rating-period batched update internally; the rating period itself is a hyperparameter (deferred)".
- `rating_cold_start_policy = "G-CS-4_via_literature_prior_mu_1500_RD_350_sigma_0.06_for_first_match_with_is_first_match_flag_co_registered"` (Glicko-2 defaults; final values deferred).
- `rating_tie_policy = "PHA_history_already_decisive_per_PR_242_Q1_draw_score_0.5_not_used"`.
- `rating_hyperparameter_policy = "mu_prior_RD_prior_sigma_prior_tau_rating_period_days_deferred_to_algorithm_implementation_proof_PR"`.
- `rating_evidence_level = "in_repo_plus_citation"`.
- `evidence_paths` includes `CITATION_GLICKMAN_1999` + `CITATION_GLICKMAN_2012` + the §6.2 row 4 spec quote ("Glicko-2 or analogous").
- `complexity_deployability_score = "medium"`.
- `leakage_risk_score = "medium_if_forward_only_enforced"` (rating-period batching is a within-period micro-leakage surface that must be carefully bounded; recorded honestly).
- `notes` makes the spec-favoured-path case explicit: §6.2 row 4 names Glicko-2 first. RD's inactivity decay matches the dataset's tournament rhythm.

**Row Q6E — `Q6E_trueskill_or_trueskill_like`** (candidate row):
- `candidate_policy = "trueskill_or_trueskill_like"`.
- `rating_model_family = "trueskill_2006_1v1_subset_or_trueskill_through_time_per_player_id_worldwide_grouped"`.
- `rating_forward_only_constraints` = same as Q6D; with extra wording on Gaussian message-passing posterior update being forward-only.
- `rating_cold_start_policy = "G-CS-4_via_literature_prior_mu_25_sigma_25_over_3_for_first_match_with_is_first_match_flag_co_registered"`.
- `rating_tie_policy = "PHA_history_already_decisive_per_PR_242_Q1_draw_margin_zero_or_minimal"`.
- `rating_hyperparameter_policy = "mu_prior_sigma_prior_beta_tau_draw_margin_deferred_to_algorithm_implementation_proof_PR"`.
- `rating_evidence_level = "in_repo_plus_citation"`.
- `evidence_paths` includes `CITATION_HERBRICH_MINKA_GRAEPEL_2006`.
- `complexity_deployability_score = "high"` (Bayesian factor-graph implementation cost; mature libraries exist but more complex than Glicko-2).
- `leakage_risk_score = "medium_if_forward_only_enforced"`.
- `notes` notes the 1v1 special-case of TrueSkill degenerates to a Glicko-like update; the marginal expressiveness gain for 1v1 may not justify the complexity.

**Row Q6F — `Q6F_deferred_with_algorithm_survey`** (candidate row):
- `candidate_policy = "deferred_blocker_with_algorithm_survey_required"`.
- `verdict = "deferred_blocker"` (this is the "punt with rigour" option).
- `rating_model_family = "to_be_determined_after_algorithm_survey_step"`.
- `rating_forward_only_constraints = "binding_in_advance_no_global_batch_fit_no_target_match_outcome_no_future_match_read_for_all_candidates_survey_step_must_honour"`.
- `rating_cold_start_policy = "G-CS-4_binding_in_advance"`.
- `rating_hyperparameter_policy = "deferred_pending_algorithm_survey_step"`.
- `rating_evidence_level = "deferred"`.
- `complexity_deployability_score = "not_applicable"`.
- `leakage_risk_score = "not_applicable"`.
- `materialization_permission = "blocked_pending_algorithm_survey_pr"`.
- `notes` records why a survey is needed: e.g., the comparative empirical evidence (back-testing AUC / log-loss on the unrated regime) does not exist in any prior artifact and would require its own Step.

**Row Q6_selected_policy** (BINDING row; verdict emerges from the candidate table per A14 pattern from PR #243):
- `decision_id = "Q6_selected_policy"`.
- `parent_decision_id = "Q6_rating_policy"`.
- `selected_policy = <one of the 6 candidates>` — chosen by the Q6 executor based on the per-candidate table.
- `verdict` ∈ {`bind_now`, `narrow_with_evidence`, `recommendation_only`, `deferred_blocker`} (the Q6 plan does NOT pre-commit which).
- `rejected_options` = JSON list of the 5 unselected candidates with brief per-candidate rejection rationale.
- `materialization_permission` derived from `selected_policy` per Assumption 15.
- `evidence_paths` cumulates the per-candidate rows' evidence paths.
- `notes` documents the verdict-emergence chain explicitly (which candidates were inferior and why, per the complexity/leakage/evidence-level table).

**Row Q6_per_family_impact_summary** (derived row):
- `decision_id = "Q6_per_family_impact_summary"`.
- `parent_decision_id = "Q6_rating_policy"`.
- `verdict = "narrow_with_evidence"` (informational broadcast).
- `binding_level = "recommendation_only"`.
- `candidate_policy = "not_applicable"`.
- `selected_policy` = mirrors the Q6_selected_policy row's value.
- `rating_*` fields all `"not_applicable_per_family_summary_row"`.
- `feature_availability_summary` enumerates the 6 family IDs and for each: `affected_by_q6 = "yes"` for `reconstructed_rating`, `affected_by_q6 = "no"` for the other 5.
- `materialization_permission` derived from the selected policy per Assumption 15.
- `notes` notes this row exists for downstream-consumer interface uniformity with PR #243's `Q5_per_family_impact_summary`.

**Stop-and-halt-before-artifact rule:** if T05 produces a row that triggers ANY falsifier from T03, the Q6 PR halts and writes no artifact. The Q6 executor must re-author the offending row or escalate to the planner with the surprise finding (per data-analysis-lineage rule §"Stop conditions" and §"Non-batching rule"). Surprises are reported as observations, not silently fixed.

---

### T06 — Mirrored test file

**File (create):** `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_rating_reconstruction.py`

**Forbidden files:** same as T01.

**Stop condition:** ≥ 150 tests pass; coverage on `adjudicate_history_rating_reconstruction.py` ≥ 95% (project-wide `fail_under = 95` per pyproject); pytest finishes without warnings; no test reads the real DuckDB at module-import time.

**Executor:** Sonnet (mechanical mirroring of PR #243's test patterns; the assertion content is mechanical given T01-T05 are settled).

**Test categories (mirror PR #243's 194-test pattern, scaled):**

- **Schema tests** (~20): every required column present in CSV header; column order canonical; SHA fields are 64-char lowercase hex; `materialized_output_paths == ""` on every row; `audit_pr` populated.
- **Decision-row tests** (~30): 8 rows in canonical `Q6_DECISION_IDS` order; one row per ID; per-row enum-field validation against `ALLOWED_*` constants.
- **Falsifier roll-call tests** (~45): one positive + one negative test per helper from T03's 43 helpers (i.e., the helper is invoked and asserted both ways). Includes synthetic inputs that *should* fire the falsifier and a sanity assertion that the entrypoint halts and writes no artifact when it does.
- **SHA pinning tests** (~10): mismatch of any pinned SHA halts the entrypoint; mismatch of any pinned source-file SHA halts the entrypoint.
- **Candidate-completeness tests** (~10): missing any of the 6 candidates halts; extra candidate halts; duplicate candidate halts; selected_policy value outside the candidate set halts.
- **POST-GAME-token rejection tests** (~10): synthetic rows containing forbidden tokens halt; the `notes` field is exempt per B-X1 carry-over.
- **MMR-missingness re-affirmation tests** (~5): the entrypoint asserts the 83.95% / 83.65% figures appear in the `mmr_missingness_summary` field of every candidate row.
- **Q5-non-re-adjudication tests** (~5): any row carrying a `cross_region_policy` field-name or `strict_exclusion` / `dual_feature_path` token in a verdict-bearing field halts.
- **Status-YAML / research_log / ROADMAP drift tests** (~5): reference to any of these paths in a scoped field halts.
- **Materialization-creep tests** (~5): any non-empty `materialized_output_paths` halts; the entrypoint never writes a Parquet.
- **B4 invariant tests** (~3): set equality + no duplicates + count equality on `HELPER_TO_FALSIFIER_KEY` vs `FALSIFIER_PRIORITY_CHAIN`.
- **Determinism tests** (~5): two consecutive runs over the same DuckDB produce byte-identical CSV and byte-identical MD.

Total: ~150-160 tests.

**Validation report:** `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_rating_reconstruction.py -v --cov=src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction --cov-report=term-missing` returns ≥ 95% coverage with all tests passing.

---

### T07 — Sandbox notebook pair (jupytext)

**Files (create):**
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.py` (jupytext py:percent source)
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.ipynb` (paired notebook)

**Forbidden files:** same as T01.

**Stop condition:** notebook runs end-to-end against `data/db/db.duckdb`; jupytext pair stays in sync; no `def` / `class` / `lambda` in any cell (all logic imported from the adjudicator module); the adjudication-call cell asserts `result.passed and result.halting_falsifier is None and len(result.decisions) == 8`.

**Executor:** Sonnet.

**Cell skeleton (per sandbox/README.md):**

1. **Markdown:** Title, hypothesis (the Q6 question verbatim from Problem Statement), falsifier list (citing T03 by key), scope (Q6-only; Q5 not re-adjudicated; no materialization).
2. **Code:** imports from `rts_predict.games.sc2.datasets.sc2egset.adjudicate_history_rating_reconstruction`; pin paths via `rts_predict.common.notebook_helpers`.
3. **Markdown:** per-candidate hypothesis cells (Q6A through Q6F), each stating: assumption, measurement claim, sanity check, falsifier, expected artifact, lineage source, downstream decision. Per data-analysis-lineage §"Required structure for every empirical analysis".
4. **Code:** invoke `adjudicate_history_rating_reconstruction(...)` against the real DuckDB + PR #242 CSV/MD + PR #243 CSV/MD + the 6 source-file paths; assert `passed`, `len(decisions) == 8`, `halting_falsifier is None`; per-row NIT-B SHA binding assertion.
5. **Markdown:** Q5 deferral preservation statement; Q6 outcome statement; materialization permission statement; no Step closure claim.

---

### T08 — Manifest housekeeping

**Files (edit):**
- `CHANGELOG.md` — append `## [3.75.0] — YYYY-MM-DD (PR #N: feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication)` block following the PR #243 entry format; enumerate every file added/changed; record verdict outcome string.
- `pyproject.toml` — bump `version = "3.74.0"` → `version = "3.75.0"`.
- `planning/INDEX.md` — archive the current Active row (PR #243); promote `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication` to the new Active row with the future PR #'s description.

**Forbidden files:** same as T01.

**Stop condition:** pre-commit hook passes on all three files; CHANGELOG follows Keep a Changelog format; `planning/INDEX.md` Active row points at the Q6 PR; the archived PR #243 row records the correct merged-master SHA (resolved at PR-merge time, not at planning time).

**Executor:** Sonnet.

---

### T09 — Layer-2 final-gate dispatch

**Files:** none (no file edit; dispatch only).

**Stop condition:** reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with 0 blockers.

**Executor:** parent session dispatches `@reviewer-adversarial` (NOT `@reviewer-deep`) because the Q6 artifact is methodology-sensitive: it binds a rating-model family that will appear as a thesis-citable claim, and the adjudication choice will be defended at examination. Per `.claude/rules/data-analysis-lineage.md` agent-routing discipline, reviewer-adversarial is the correct final gate for any Q6 outcome other than `Q6A_omit` or `Q6F_deferred_with_survey` — and even those benefit from adversarial review because the omission / re-deferral verdict has thesis implications.

If reviewer-adversarial raises BLOCKERS, the Q6 PR halts; the executor fixes blockers and re-runs the gate. The 3-round adversarial cap applies (per feedback memory `feedback_adversarial_cap_execution.md`).

---

## File Manifest

### Planning files (created in THIS Layer-1 planning-only PR — 2 files)

| Path | Action | Purpose |
|---|---|---|
| `planning/current_plan.md` | overwrite | this plan document |
| `planning/current_plan.critique.md` | overwrite | critique placeholder for reviewer-adversarial |

**No other files are edited in this PR.** No CHANGELOG entry, no pyproject bump, no INDEX archive, no notebook, no module, no artifact, no test, no status YAML, no research_log, no ROADMAP, no spec, no thesis chapter, no .claude rule.

### Future Layer-2 execution files (created in the FUTURE Q6 PR — 11 files; NOT this PR)

| # | Path | Action | Purpose |
|---|---|---|---|
| 1 | `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_history_rating_reconstruction.py` | create | Q6 adjudicator module (T01-T05) |
| 2 | `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_history_rating_reconstruction.py` | create | mirrored test file (T06; ≥150 tests; ≥95% coverage) |
| 3 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.py` | create | jupytext py:percent source (T07) |
| 4 | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.ipynb` | create | paired notebook (T07) |
| 5 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.csv` | create | Q6 adjudication CSV (≥30 cols × 8 rows + header) |
| 6 | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_03_history_rating_reconstruction_adjudication.md` | create | Q6 adjudication MD (≥17 sections) |
| 7 | `planning/INDEX.md` | edit | archive PR #243 row; promote new Active (T08) |
| 8 | `CHANGELOG.md` | edit | append `[3.75.0]` block (T08) |
| 9 | `pyproject.toml` | edit | bump 3.74.0 → 3.75.0 (T08) |
| 10 | `planning/current_plan.md` | overwrite | replaced post-merge by the next planner's Layer-3 plan |
| 11 | `planning/current_plan.critique.md` | overwrite | replaced post-merge |

### Forbidden files (MUST NOT be touched in either this PR or the future Layer-2 PR)

- Any Parquet under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/`.
- Any `leakage_audit_sc2egset.{json,md}` under any subdirectory.
- Any of: `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`.
- Any `research_log.md` (root or per-dataset). **Default: no entry.** Confirmed by PR #242 + PR #243 precedent — neither adjudication PR wrote a research_log entry; both deferred to a closure PR per PR #237 tranche-1 closure precedent.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`.
- Any file under `reports/specs/` (CROSS-02-00, CROSS-02-01, CROSS-02-02, CROSS-02-03).
- Any cleaning-layer YAML under `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/` or any sister dataset's schemas.
- Any file under `thesis/`, `docs/`, `.claude/`, `data/`.
- Any file under `src/rts_predict/games/aoe2/` (cross-game scope discipline).
- `sandbox/jupytext.toml` (project-canonical location per memory).

### Q6 CSV schema (canonical column order; ≥ 30 columns)

```
decision_id
parent_decision_id
decision_name
verdict
binding_level
scope
candidate_policy
selected_policy
rejected_options
rating_model_family
rating_forward_only_constraints
rating_cold_start_policy
rating_tie_policy
rating_hyperparameter_policy
rating_evidence_level
mmr_missingness_summary
feature_availability_summary
complexity_deployability_score
leakage_risk_score
materialization_permission
evidence_paths
falsifiers
audit_pr
parent_pr242_csv_sha256
parent_pr242_md_sha256
parent_pr243_csv_sha256
parent_pr243_md_sha256
pr241_scaffold_validator_module_sha256
cross_02_02_spec_sha256
feature_family_registry_csv_sha256
dataset_research_log_sha256
player_history_all_yaml_sha256
matches_flat_clean_yaml_sha256
matches_history_minimal_yaml_sha256
materialized_output_paths
notes
```

Total: 36 columns. All SHA fields: 64-char lowercase hex; `materialized_output_paths == ""` on every row by construction; `audit_pr == "PR #N"` on every row; no `NOT_FOUND` token allowed.

### Q6 MD outline (canonical section order; ≥ 17 sections)

1. §1 Non-Materialization Disclaimer.
2. §2 Parent PR #242 Lineage (Q6 row SHA citation; verbatim Q6 row text quote).
3. §3 Parent PR #243 Lineage (Q5_selected_policy reaffirmed; non-re-adjudication statement).
4. §4 Q6-Only Scope Statement (the question being adjudicated; what is out of scope).
5. §5 Per-Candidate Decision Table (Q6A through Q6F in a 6-row markdown table).
6. §6 Candidate Policy Comparison (deployability / complexity / leakage-risk / evidence-level — 4-axis table).
7. §7 MMR-Missingness Reaffirmation (83.95% / 83.65% with research_log line citations).
8. §8 Rating-Method Literature Context (Elo 1978 / Glickman 1999 / Glickman 2012 / Herbrich-Minka-Graepel 2006 — citation-only).
9. §9 Forward-Only Update Semantics (per candidate; deterministic ordering by `(player_id_worldwide, TRY_CAST(ph.details_timeUTC AS TIMESTAMP), ph.replay_id)`; tie-handling).
10. §10 Cold-Start Policy per Candidate (G-CS-4 honoured per candidate).
11. §11 Leakage Constraints per Candidate (G-L-4 honoured; no global batch fit; no future-match read; no target-match outcome read).
12. §12 Q6 Selected Policy Binding Row (the chosen candidate + verdict + rejection rationale for the other 5).
13. §13 Materialization Permission Statement (per Assumption 15).
14. §14 Non-Substitution Statement (does NOT replace PR #229/230/234/236/237/239/240/241/242/243; does NOT alter Q5).
15. §15 Falsifier Roll-Call (every key from `HELPER_TO_FALSIFIER_KEY.values()` with `did_not_fire` per PR #242 / #243 precedent).
16. §16 SHA Provenance (every pinned SHA verbatim).
17. §17 No Step 02_01_03 Closure / No Phase 03 Start (per PR #237 closure-deferral precedent).

---

## Gate Condition

**Mergeability gate for this Layer-1 planning-only PR:**

- Exactly 2 files in the diff: `planning/current_plan.md` and `planning/current_plan.critique.md`. No other file.
- `planning/current_plan.md` contains all 8 required `##` sections per the pre-commit hook (Scope / Problem Statement / Assumptions & Unknowns / Literature Context / Execution Steps / File Manifest / Gate Condition / Open Questions). The hook rejects plans without these named sections per feedback memory `feedback_plan_required_sections.md`.
- `planning/current_plan.critique.md` is a stub (one-line placeholder); reviewer-adversarial populates it before the Layer-2 PR runs.
- Branch name = `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication`. No other branch.
- PR is DRAFT (per planning-only convention).
- Reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with 0 blockers. Nits may be inlined into the plan or carried forward as Layer-2 execution guidance.

**Mergeability gate for the future Layer-2 execution PR (recorded here for the executor's reference, NOT enforced now):**

- All 43 falsifiers from T03 fire as `did_not_fire` on the produced row set.
- CSV is byte-deterministic (two consecutive runs over the same DuckDB produce byte-identical output).
- MD contains all 17 §sections in canonical order.
- All 4 pinned parent-artifact SHAs match the verified state SHAs (PR #242 CSV `f2a169ec…`; PR #242 MD `fdaa7d6d…`; PR #243 CSV `29d39522…`; PR #243 MD `026deda3…`).
- All 6 source-file SHAs (pinned at Layer-2 plan-time) match.
- `Q6_RATING_POLICY_CANDIDATES` contains all 6 candidates exactly once.
- `Q6_selected_policy.verdict` ∈ ALLOWED_VERDICTS.
- `Q6_selected_policy.materialization_permission` is consistent with the selected_policy (per Assumption 15 mapping).
- No status YAML edit; no research_log entry; no ROADMAP edit; no Parquet; no leakage_audit file; no spec edit; no cleaning-layer YAML edit; no Phase 03 reference in any scoped field.
- ≥ 150 tests in the test file; ≥ 95% coverage on the adjudicator module.
- Pre-commit hooks (ruff + mypy + plan-required-sections) pass.
- Reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with 0 blockers, ≤ 3 rounds (per `feedback_adversarial_cap_execution.md`).
- `pyproject.toml` bumped `3.74.0 → 3.75.0`.
- CHANGELOG `[3.75.0]` block follows the PR #243 format.
- `planning/INDEX.md` archived PR #243; promoted the Q6 PR to Active.

---

## Open Questions

Surfaced for user / reviewer-adversarial decision before the Layer-2 execution PR runs. Each is a real ambiguity that the planner does not unilaterally resolve.

**OQ1 — Does Q6A (omit) unblock the other 5 history-enriched families?**

If the Q6 executor selects `Q6A_omit_reconstructed_rating`, may the future Layer-3 materialization PR proceed for the other 5 families (`focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `in_game_history_aggregate`, `cross_region_fragmentation_handling`)? The PR #242 §13 binding gate text is ambiguous on this — it says "the future Layer-3 materialization PR must NOT proceed until that decision is upgraded" but does not specify whether upgrading Q6 by *removing the family from scope* counts as upgrading. **Provisional planner answer: yes.** Materialization proceeds for the 5 surviving families with `reconstructed_rating` permanently absent from the projected feature matrix. The Q6_selected_policy row's `materialization_permission` field encodes this as `permitted_for_other_5_families_without_reconstructed_rating`. **Decision needed:** confirm this interpretation OR require a separate scope-narrowing PR before Layer-3.

**OQ2 — Algorithm-implementation-proof PR as a hard prerequisite?**

If the Q6 executor selects a non-trivial rating policy (`Q6C_elo`, `Q6D_glicko_or_glicko_2`, `Q6E_trueskill_or_trueskill_like`), is a separate algorithm-implementation-proof PR required before the Layer-3 materialization PR runs? Such a PR would pin `K` / `μ` / `RD` / `σ` / `τ` / rating-period / `β` / draw-margin and demonstrate forward-only update mechanics on a synthetic mini-corpus. **Provisional planner answer: yes** — Invariant I7 ("no magic numbers") requires those constants to be justified either empirically or by literature precedent; the Q6 adjudication itself does NOT justify them. **Decision needed:** confirm OR allow the Layer-3 materialization PR to pin its own hyperparameters in-line with a citation to the algorithm's published default values.

**OQ3 — External WebFetch citations required?**

Are external WebFetch citations to Elo (1978), Glickman (1999), Glickman (2012), Herbrich-Minka-Graepel (2006) required in the Q6 MD, or are the in-repo references in `02_02_feature_engineering_plan.md` §6.2 row 4 + PR #242 Q6 row evidence_paths sufficient? **Provisional planner answer: in-repo sufficient.** WebFetch permitted only if a specific algorithmic claim cannot be sourced from the repo. **Decision needed:** confirm OR direct the Q6 executor to fetch all 4 primary sources as part of T05.

**OQ4 — Empirical MMR-missingness re-probe?**

Should the Q6 artifact include an empirical MMR-missingness re-probe (PROBE 3 + PROBE 4 from T02) against `data/db/db.duckdb`, or trust the dataset research_log's 83.95% / 83.65% figures by citation? **Provisional planner answer: include the probes** (they are read-only, cheap, and the artifact then re-grounds the literature claim in the current data state). The probes do not compute ratings; they only count MMR-zero rows. **Decision needed:** confirm OR allow citation-only.

**OQ5 — Should `Q6_per_family_impact_summary` broadcast over all 6 families?**

Q6 strictly only affects `reconstructed_rating` (1 family). PR #243's `Q5_per_family_impact_summary` row broadcast over the 6 families for downstream-consumer interface uniformity. **Provisional planner answer: yes, broadcast** — interface uniformity with PR #243 supports a one-shape downstream consumer. The other 5 families' entries carry `affected_by_q6 = "no"`. **Decision needed:** confirm OR collapse the row to only `reconstructed_rating` (saves a row but breaks the per-family pattern established by PR #243).

**OQ6 — Should the Q6 PR pre-emptively author the Layer-3 materialization plan?**

After Q6 merges, the next planner authors a Layer-3 materialization plan. May the Q6 PR pre-emptively include a stub of that plan to avoid a separate planning round? **Provisional planner answer: no** — one-atomic-unit policy per data-analysis-lineage; the Layer-3 plan is a separate planning artifact authored after Q6 is reviewed. The Q6 PR's MD §17 "forward implications" may *describe* what the Layer-3 plan will need to address, but does not author it. **Decision needed:** confirm OR allow Layer-3 plan stub inclusion.

---

## Out of scope

The Q6 Layer-2 execution PR authorised by this plan does **not** do any of the following. Each item is explicitly forbidden so the executor cannot drift into adjacent work mid-execution.

- **No `reconstructed_rating` feature value materialised.** The Q6 PR adjudicates *which rating-model family* is bound; it does not produce a Parquet column carrying rating values. That belongs to the Layer-3 materialisation PR (separate planning round).
- **No Layer-3 materialisation plan authored in the same PR.** The Q6 PR's MD §17 ("forward implications") may describe what the next planner must address, but does not author the Layer-3 plan.
- **No algorithm benchmark.** The Q6 artifact does not run, time, accuracy-benchmark, or AUC-test any rating algorithm. If the Q6 executor concludes that comparative empirical evidence is required to bind a winner, the correct verdict is `Q6F_deferred_with_algorithm_survey` (the survey itself is a separate Step).
- **No race-conditioned rating / Bradley-Terry / Neural BTL.** These methods are listed in the dataset's research_log (lines 733-734 and 961) as the substrate's intended backtesting universe, but they are out-of-scope for the Q6 rating-family selection. See N-1 in the Adversarial-Review Adjustments section for the binding executor guidance that addresses why.
- **No raw MMR-where-present hybrid feature.** Per §6.2 row 4 spec language, raw MMR is rejected as a skill feature because of the 83.95% sentinel density. The "use raw MMR for the 16.05% rated subset only" hybrid is also out of scope; see N-2 for the binding executor guidance.
- **No Q5 re-adjudication.** Q5_selected_policy = `sensitivity_indicator_co_registration` (PR #243) is BINDING and may not be touched by Q6.
- **No Q1-Q4 / Q7 / Q8 re-adjudication.** All other PR #242 decisions are RATIFIED and may not be touched by Q6.
- **No Step 02_01_03 closure.** Closure flips `STEP_STATUS.yaml` to `02_01_03: complete` only after Layer-3 materialisation + the CROSS-02-01-v1.0.1 post-materialisation audit + the closure PR's research_log entry. None of this happens in the Q6 PR.
- **No Step 02_01_04 start.** The next 02_01 sub-step is `in_game_snapshot` family materialisation; barred until 02_01_03 is closed.
- **No Phase 03 work.** No splitting, no baseline modelling, no `ml_protocol` step execution. Phase 03 = `not_started` and must remain so.
- **No cross-dataset (aoe2, aoestats, aoe2companion) work.** Q6 is sc2egset-scoped. The analogous adjudications for the other datasets are separate future Steps.
- **No spec edits.** `reports/specs/02_00_feature_input_contract.md`, `02_01_leakage_audit_protocol.md`, `02_02_feature_engineering_plan.md`, `02_03_temporal_feature_audit_protocol.md` are READ-ONLY.
- **No cleaning-layer YAML edits.** All `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/*.yaml` are READ-ONLY.
- **No `.claude/` rule edits.** Scientific invariants, ML protocol, and data-analysis-lineage rules are READ-ONLY in this PR.
- **No thesis chapter / docs / WRITING_STATUS edits.** Q6 is a Phase 02 artifact, not a thesis chapter.
- **No `.github/` workflow edits.**
- **No `sandbox/jupytext.toml` edit.** Project-canonical location per user-approved deviation.

## Adversarial-Review Adjustments (Round 1)

`@reviewer-adversarial` Round 1 verdict: **APPROVE-WITH-NITS** (0 blockers; 10 nits). Below, the 4 highest-priority nits (N-1 through N-4) are BINDING for the Layer-2 executor; N-5 through N-10 are SOFT guidance. The full reviewer text is captured in `planning/current_plan.critique.md`.

### Binding nits (Layer-2 executor MUST apply)

**N-1 — Acknowledge omitted rating methods from the dataset's intended backtesting universe.**

The 6-candidate set in Assumption 11 (`omit / rolling-baseline / Elo / Glicko-or-Glicko-2 / TrueSkill / deferred-with-survey`) omits methods explicitly listed in dataset `research_log.md` lines 733-734 ("rating-system backtesting (Elo, Glicko, Glicko-2, TrueSkill, Aligulac-style BTL)") and line 961 ("Elo, Glicko, Glicko-2, TrueSkill, Aligulac race-conditioned, Bradley-Terry, Neural BTL"). The Q6 executor MUST either:

- (a) **Extend** `Q6_RATING_POLICY_CANDIDATES` to include `aligulac_race_conditioned_btl` and `bradley_terry_or_neural_btl` as new explicit candidates (with their own `Q6G_*` / `Q6H_*` decision rows), bringing the total decision row count to ≥10; OR
- (b) **Author** an explicit rejection paragraph in MD §5 (Per-Candidate Decision Table) and in the per-candidate row notes that names these methods and justifies their omission for sc2egset's 1v1-decisive PHA scope. Acceptable rationale shape: "BTL / race-conditioned BTL collapse to Elo-with-race-prior in 1v1; Neural BTL requires its own training/eval pipeline that exceeds Q6 successor-adjudication scope; deferred to the algorithm survey if Q6F is selected."

(a) is preferred for honest examination defensibility; (b) is acceptable if the executor's substantive reasoning shows the methods are dominated by the existing 6 candidates within sc2egset's 1v1 PHA regime.

**N-2 — Acknowledge the "raw MMR-where-present" hybrid candidate.**

The plan's §6.2-row-4-quote rejection of raw MMR ("structurally absent for 83.95% of rows") does NOT cover the *hybrid* candidate "use raw MMR for the 16.05% rated subset + cold-start the rest." The Q6 executor MUST add a Q6 row (either a new `Q6G_raw_mmr_where_present_hybrid` candidate row, OR an explicit rejection paragraph in MD §5) that enumerates this candidate and justifies its rejection. Acceptable rejection rationale shape: "Violates Invariant I5 symmetric-treatment because rated-vs-unrated rows would be fed asymmetric features; the rated/unrated partition is correlated with skill (tournament players over-represented in the rated 16.05%); the partition-as-feature would leak corpus structure into the model. Use `is_mmr_missing` flag co-registration plus a reconstructed rating instead."

**N-3 — Probe 5 must group by `player_id_worldwide`, not `toon_id`.**

`PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_SQL` (T02 Probe 5) in the plan text groups by `toon_id`. PR #243 established the canonical player-grouping key as `player_id_worldwide` (full `R-S2-G-P` toon with cross-region co-registration; Invariant I2 branch iii). Grouping by `toon_id` under-counts per-player history depth for cross-region players (their parallel-region trajectories appear as separate keys), breaking the cold-start prevalence evidence. The Layer-2 executor MUST replace `GROUP BY toon_id` with `GROUP BY player_id_worldwide` (or the canonical PHA column name resolved at Layer-2 plan time) and add a comment explicitly noting the choice and citing PR #243's player_id_worldwide binding.

**N-4 — Probes 1 & 2 LIMIT 1000 is non-deterministic without ORDER BY.**

`PROBE_PHA_RESULT_DISTRIBUTION_SQL` and `PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_SQL` (T02 Probes 1 & 2) use `LIMIT 1000` with no `ORDER BY`, leaving row selection implementation-defined and non-deterministic across runs / pages / parallelism. This breaks the T06 / Gate Condition byte-determinism guarantee. The Layer-2 executor MUST either:

- (a) Add a deterministic `ORDER BY` (e.g., `ORDER BY replay_id`) before the LIMIT clause; OR
- (b) Drop the LIMIT and probe the full `player_history_all` table (44,817 rows is trivially cheap; the determinism guarantee is preserved at zero cost).

(b) is preferred unless the executor finds a probe whose semantics genuinely require sampling.

### Soft guidance (recommended; not strictly binding)

**N-5 — Surface that Q6 probes are single-table by design.** Add one sentence to T02 explicitly stating that Q6 probes are single-table `COUNT FILTER` operations on PHA + MFC (no JOIN, no LEFT JOIN, no NULL-from-JOIN semantics), so PR #243's Dispatch-3 LEFT-JOIN-NULL trap is structurally inapplicable.

**N-6 — Justify the 36-column schema delta vs PR #243's 30-column template.** Add a one-paragraph note (in File Manifest or T05) enumerating which 6 columns are net-new vs PR #243 (`candidate_policy`, `rating_model_family`, `rating_forward_only_constraints`, `rating_cold_start_policy`, `rating_tie_policy`, `rating_hyperparameter_policy`, `rating_evidence_level`, `mmr_missingness_summary`, `feature_availability_summary`, `complexity_deployability_score`, `leakage_risk_score`, `materialization_permission` — the count exceeds 6 because Q6 carries rating-discipline-specific fields PR #243's cross-region adjudication did not need) and why each is required for rating-family adjudication.

**N-7 — Add an "Out of scope" plan section.** **Inlined above** as `## Out of scope`. The Layer-2 executor inherits the same scope discipline.

**N-8 — Pin the verbatim N-X3 strengthened-gate quote from PR #242.** Add to Assumption 18 the exact N-X3 quote from `02_01_03_history_source_anchor_coldstart_adjudication.md` line 125: "MATERIALIZATION BLOCKED until Q6 is upgraded to bind_now in a successor adjudication PR with rating-family empirical evaluation evidence satisfying the N-X3 strengthened gate (≥1 repo path + ≥1 citation + forward-only wording + cold-start/missingness wording)." This prevents the Layer-2 executor from drifting the gate language.

**N-9 — Reuse the universal `POST_GAME_TOKEN_SET` from prior adjudicators.** Helper 17 (`_check_no_post_game_token_in_scoped_fields`) MUST import the existing POST-GAME token set from `adjudicate_history_enriched_pre_game_source_layer.py` (PR #242) rather than redefining the set. This guarantees the Q6 scanner is identical to PR #242 / PR #243 and prevents silent set-drift.

**N-10 — MD §5 must mark Q6F as a legitimate verdict.** Add explicit wording to MD §5 (Per-Candidate Decision Table) that "selecting `Q6F_deferred_with_algorithm_survey` is a legitimate Q6 verdict, not a planning failure — it preserves Invariant I7 ('no magic numbers') when comparative empirical evidence is genuinely insufficient." This prevents the Layer-2 executor from feeling pressured to bind a winner under thin evidence.

### Round-1 audit trail

- Round 1 of 3 adversarial cap consumed.
- Verdict: APPROVE-WITH-NITS, 0 blockers, 10 nits.
- Reviewer: `@reviewer-adversarial`, 2026-05-25.
- Full reviewer transcript: `planning/current_plan.critique.md`.
- Round-2 / Round-3 adversarial cap held in reserve for the Layer-2 execution PR's own final gate; the planning-only PR does not consume additional rounds unless the user requests a revision.
