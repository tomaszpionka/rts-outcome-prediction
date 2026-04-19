---
category: A
branch: feat/01-05-aoe2companion
date: 2026-04-18
planner_model: claude-opus-4-7
dataset: aoe2companion
phase: "01"
pipeline_section: "Temporal & Panel EDA"
invariants_touched: [I3, I6, I7, I8, I9]
source_artifacts:
  - reports/specs/01_05_preregistration.md
  - .claude/scientific-invariants.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/INVARIANTS.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PHASE_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md
  - src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_history_minimal.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_1v1_clean.yaml
  - src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml
  - sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_03_minimal_history_view.py
  - scripts/check_01_05_binding.py
  - docs/PHASES.md
  - docs/TAXONOMY.md
  - docs/templates/plan_template.md
  - docs/templates/planner_output_contract.md
  - planning/README.md
  - ARCHITECTURE.md
  - sandbox/README.md
  - .claude/ml-protocol.md
  - .claude/rules/sql-data.md
  - .claude/rules/python-code.md
critique_required: true
research_log_ref: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md#2026-04-18-01-05-temporal-panel-eda
---

# Plan: 01_05 Temporal & Panel EDA — aoe2companion

## Scope

Execute Pipeline Section 01_05 (Temporal & Panel EDA) for the aoe2companion
dataset under the binding CROSS spec `reports/specs/01_05_preregistration.md`
(LOCKED v1.0.1, SHA `7e259dd8`). Produce all nine Q1–Q9 analyses using
`matches_history_minimal` + `matches_1v1_clean` + `player_history_all` as
inputs, emit a single Phase-06 interface CSV conforming to §12, and update
the dataset's status files, INVARIANTS §4, and research log. Analysis
substrate is rm_1v1 only (leaderboards 6 + 18). Work happens entirely in
sandbox notebooks under `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/`;
artifacts land under
`src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/`.
No DuckDB table or VIEW is created, modified, or dropped.

## Problem Statement

Phase 01 for aoe2companion is 01_04-complete: `matches_1v1_clean` (51 cols,
61,062,392 player-rows / 30,531,196 matches), `player_history_all` (19 cols,
264,132,745 rows, 21 leaderboard types), and `matches_history_minimal` (9
cols, the cross-dataset harmonised substrate) are in place, identity
resolved to `profileId` (branch (i), §2), and duration augmentation
complete. The next gate before Phase 02 feature engineering is the
pre-registered temporal/panel EDA suite: distribution stability over time
(PSI), regime stratification, survivorship sensitivity, between-/within-
player variance decomposition (ICC), a temporal-leakage audit, and
data-generating-process diagnostics for post-game variables. These
findings drive (a) Phase 02 feature-window and cold-start design, (b)
Phase 03 split validation, and (c) Phase 06 cross-domain transfer
analysis. All work in this step is read-only analytical consumption of
01_04 VIEWs plus panel-model fitting on an on-disk DuckDB snapshot.

Why now: 01_04 closed with `STEP_STATUS 01_04_04: complete` on 2026-04-18;
01_05 pre-registration spec was locked the same day. The CROSS spec
forbids any deviation without §14 amendment, so the plan encodes its
parameters verbatim.

## Assumptions & unknowns

- **Assumption:** `matches_history_minimal` is the primary input substrate
  for Q1, Q2, Q3, Q4, Q6, Q7. Pre-game features (`rating`, `mapId`,
  `leaderboard_id`) not in this 9-column VIEW are obtained by joining to
  `matches_1v1_clean` on `(matchId, profileId)` where
  `match_id = 'aoe2companion::' || CAST(matchId AS VARCHAR)` and
  `player_id = CAST(profileId AS VARCHAR)`. Temporal anchor is
  `started_at` (TIMESTAMP, zero NULLs per aoec INVARIANTS §3).
- **Assumption:** `rating` in `matches_1v1_clean` is PRE_GAME per 01_03_03
  verdict (99.8% exact match with `ratings_raw` pre-match entries). Used
  as the pre-game numeric feature for PSI in Q2.
- **Assumption:** spec §1's 9-col contract requires `team`, `chosen_civ_or_race`,
  `rating_pre`, `map_id`, `patch_id`. aoec populates: `team` — N/A (aoec
  is natively player-row, no slot column); `chosen_civ_or_race` — covered
  by `faction` in `matches_history_minimal`; `rating_pre` — covered by
  `matches_1v1_clean.rating` via join; `map_id` — `matches_1v1_clean.mapId`
  via join; `patch_id` — unavailable in aoec schema (flagged in Open
  questions). PSI on `patch_id` is documented as N/A for aoec.
- **Assumption:** `statsmodels` is not currently in the venv (verified
  `ModuleNotFoundError`). T00 adds it via `poetry add statsmodels` as a
  prerequisite before T06 runs.
- **Assumption:** reservoir-sample non-determinism caveat (aoec INVARIANTS
  §3, DS-AOEC-IDENTITY-05 footnote) applies to any `USING SAMPLE reservoir
  REPEATABLE(seed)` call in this step. Documented but not re-derived.
- **Assumption:** the 4.69% NULL in `matches_raw.won` is an UPSTREAM fact;
  `matches_history_minimal.won` has zero NULLs by R03 complementarity
  filter. PSI/drift analyses operate on the VIEW where this is not a
  concern; the Open-questions section records the upstream semantics so
  reviewers don't conflate scopes.
- **Unknown:** whether `patch_id` can be reconstructed from an external
  aoe2companion API endpoint — resolves by: user decision deferred to
  Phase 02 (out-of-scope here; §15 of spec confirms `patch_id`
  reconstruction is not an 01_05 activity).
- **Unknown:** whether mixedlm converges on 50k sampled players given
  ~19 observations/player in the reference period — resolves by: T06
  executor (if non-convergence, retry with `method='lbfgs'` and a 25k
  sub-sample; documented in Open questions).
- **Unknown:** whether any quarter in the overlap window contains zero
  rm_1v1 matches (data gap) — resolves by: T02 executor (if a quarter
  has <1,000 1v1 rows, that quarter's PSI and Cohen's h are reported as
  `NULL` in the Phase-06 interface with a `sample_too_small` note).

## Literature context

Five anchor references (per spec §16); each binds specific decisions.

- **Hamilton (1994)** §17.7 — prohibits ADF/KPSS at N=8 tested quarters
  (cross-dataset). Q1 grain = calendar quarter; we report descriptive
  summaries only across quarters, no unit-root p-values.
- **Siddiqi (2006)** — PSI definition, equal-frequency binning (N=10),
  threshold table (0.10 flag, 0.25 escalate). Binds Q2 directly.
- **Breck et al. (2019)** "Data Validation for Machine Learning" (SysML) —
  TFDV's PSI implementation is the reference for descriptive KS magnitude
  alongside PSI. Binds the KS row in the Phase-06 metric table.
- **Gelman & Hill (2007)** §12.5 — delta-method CI for ICC. Binds Q6
  reporting (ICC point + 95% CI).
- **Cohen (1988)** §2.2 (d) and §6.2 (h) — effect-size definitions and
  thresholds. Binds Q5 drift comparison (Cohen's h for binary, Cohen's d
  for continuous features; small/medium/large thresholds 0.2/0.5/0.8 for d
  and 0.2/0.5/0.8 for h per Cohen).

For panel-data fits at very large N (~264M rows), the methodological
literature on scalable random-intercept estimation (Bates et al. 2015,
`lme4` paper; Jiang 2017 *Asymptotic Analysis of Mixed Effects Models*)
recommends fitting on a representative player-level subsample when
full-N fits exceed memory; we apply this by sampling 50k players (plus
25k/100k sensitivity) with a fixed seed (RANDOM_SEED=42 per ml-protocol).
Non-convergence fallback strategy follows `statsmodels` documentation for
`MixedLM.fit(method=['lbfgs', 'bfgs', 'cg'])`. This departure from
full-N is declared here, not a spec deviation — spec §8 requires the
method (mixedlm, random-intercept on `player_id`), not the sample size.

## Execution Steps

### T00 — Prerequisite: install statsmodels

**Objective:** Add `statsmodels` to the Poetry environment. T06 uses
`statsmodels.formula.api.mixedlm`; the venv currently raises
`ModuleNotFoundError: No module named 'statsmodels'` (verified).

**Instructions:**
1. Run `source .venv/bin/activate && poetry add statsmodels@^0.14` from
   the repo root.
2. Confirm `source .venv/bin/activate && poetry run python -c "import statsmodels; print(statsmodels.__version__)"`
   prints `0.14.x`.
3. Commit the `pyproject.toml` and `poetry.lock` changes on
   `feat/01-05-aoe2companion` with message
   `chore(01-05): add statsmodels for mixedlm ICC (Q6)`.

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from statsmodels.formula.api import mixedlm; print(mixedlm)"` succeeds.

**File scope:**
- `pyproject.toml`
- `poetry.lock`

**Read scope:**
- (none)

---

### T01 — Scaffold 01_05 directory tree + spec-binding template

**Objective:** Create the sandbox and artifacts directory tree for 01_05,
plus a shared notebook header template enforcing the spec-binding line
required by `scripts/check_01_05_binding.py`. No analysis happens in T01.

**Instructions:**
1. Create directory `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/`.
2. Create directory `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/`.
3. Create empty marker file `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/.gitkeep`.
4. Create `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/README.md`
   listing the 7 notebook filenames (T02–T08) and their spec §§ binding.
5. Every notebook created in T02–T08 must contain the literal line
   `# spec: reports/specs/01_05_preregistration.md@7e259dd8` within its
   first 40 lines (per §13 and the regex in `scripts/check_01_05_binding.py`).

**Verification:**
- `ls sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/` returns `.gitkeep` and `README.md`.
- `ls src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/` exists.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/.gitkeep`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/README.md`

**Read scope:**
- `reports/specs/01_05_preregistration.md`
- `scripts/check_01_05_binding.py`

---

### T02 — Q1 Quarterly grain + per-quarter row counts + overlap window

**Objective:** Establish the quarterly grain (§3), validate the overlap
window 2022-Q3..2024-Q4 (§2), and report per-quarter row counts for
rm_1v1 (lb=6), qp_rm_1v1 (lb=18), and the union. Provides the sample-size
denominator for every downstream Q2/Q5/Q6 computation.

**Instructions:**
1. Create paired notebook
   `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py`
   (+ `.ipynb`) with spec-binding header and hypothesis/falsifier frame:
   - `# Hypothesis: rm_1v1 volume is non-zero in every quarter of the
     overlap window (2022-Q3..2024-Q4) and of the reference period
     (2022-08-29..2022-12-31).`
   - `# Falsifier: any quarter in {2022-Q3, 2022-Q4, 2023-Q1, 2023-Q2,
     2023-Q3, 2023-Q4, 2024-Q1, 2024-Q2, 2024-Q3, 2024-Q4} has < 1,000
     rm_1v1 matches.`
2. Use `get_notebook_db("aoe2", "aoe2companion", read_only=True)` and
   `get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"`.
3. Run SQL:
   ```sql
   SELECT
       CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
              CAST(CEIL(EXTRACT(MONTH FROM started_at) / 3.0) AS VARCHAR)) AS quarter,
       COUNT(DISTINCT match_id) AS n_matches,
       COUNT(*) AS n_player_rows
   FROM matches_history_minimal
   WHERE started_at >= TIMESTAMP '2020-07-01'
     AND started_at <  TIMESTAMP '2026-05-01'
   GROUP BY 1
   ORDER BY 1;
   ```
4. Run a parallel query stratified by `internalLeaderboardId` joining
   `matches_1v1_clean` to `matches_history_minimal` for lb-level counts.
5. Produce two artifacts:
   - `01_05_01_quarterly_grain.json` — per-quarter counts, reference
     period counts, overlap-window row count, all SQL verbatim under
     `sql_queries`.
   - `01_05_01_quarterly_grain.md` — human-readable table, hypothesis
     verdict, SQL verbatim (I6).
6. Print `# Verdict:` line in the notebook. If any quarter in the overlap
   window has < 1,000 matches, set a flag `low_volume_quarters: [...]`
   in the JSON and carry it forward to T03 as a caption.

**Verification:**
- Both artifacts exist and are non-empty.
- JSON contains keys `quarters`, `reference_period_counts`,
  `overlap_window_counts`, `low_volume_quarters`, `sql_queries`.
- `# Verdict:` line present in notebook; hypothesis either confirmed
  or falsifier captured with a documented revised approach.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.md`

**Read scope:**
- (none from sibling tasks)

---

### T03 — Q2 PSI N=10 equal-frequency, frozen reference edges, pre-game features only

**Objective:** Compute PSI per pre-game feature per tested quarter
vs. reference period 2022-08-29..2022-12-31 (§7), N=10 equal-frequency
bins, edges frozen on reference (§4). Scope: pre-game numeric features
only (`rating`). Pre-game categorical features (`faction`, `mapId`,
`internalLeaderboardId`) use a sibling "categorical PSI" computed on
relative-frequency vectors (no binning). `__unseen__` bin handling per
spec §4.

**Instructions:**
1. Create notebook `01_05_02_psi_shift.py` with spec-binding line and
   hypothesis/falsifier:
   - `# Hypothesis: max PSI across pre-game features and tested quarters
     is < 0.25 (spec §4 escalate threshold).`
   - `# Falsifier: any (feature × quarter) cell exhibits PSI >= 0.25.`
2. Compute frozen reference-period bin edges for `rating` on
   `matches_1v1_clean` joined to `matches_history_minimal`:
   ```sql
   WITH ref AS (
       SELECT rating
       FROM matches_1v1_clean
       WHERE started >= TIMESTAMP '2022-08-29'
         AND started <  TIMESTAMP '2023-01-01'
         AND rating IS NOT NULL
   )
   SELECT quantile_cont(rating, list_value(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9))
   FROM ref;
   ```
3. Persist the 9 percentile cutpoints to a runtime dict keyed by feature;
   include an assertion `assert ref_start == datetime(2022, 8, 29) and
   ref_end == datetime(2022, 12, 31)` per spec §9 Query 3.
4. For each tested quarter (2023-Q1..2024-Q4, 8 quarters) compute:
   - Per-feature bin shares using the frozen edges (numerics) or
     relative-frequency vectors (categoricals, with `__unseen__` bin).
   - PSI = Σ (p_test_i − p_ref_i) · ln(p_test_i / p_ref_i).
   - Cohen's h for the binary feature `won` (per-quarter win-rate vs. 0.5):
     `h = 2*(asin(sqrt(p_q)) - asin(sqrt(0.5)))`.
   - Cohen's d for `rating` per-quarter (pooled SD).
   - KS magnitude (descriptive, via `scipy.stats.ks_2samp`).
5. Conditional-label caption: every figure, table, and csv row gets the
   suffix `(conditional on >=10 matches in reference period; see §6)` (§6.3).
6. Pre-game features scope: `rating` (numeric), `faction` (categorical),
   `mapId` (categorical, joined from `matches_1v1_clean`),
   `internalLeaderboardId` (categorical, 6 vs. 18). POST_GAME features —
   `duration_seconds`, `is_duration_suspicious`, `is_duration_negative` —
   are EXCLUDED from Q2 (§4 forbidden scope; handled in T08).
7. Emit:
   - `01_05_02_psi_shift.json` — per-(feature, quarter) PSI + Cohen's
     h/d + KS, plus `__unseen__` counts and `low_volume_quarters` passed
     from T02. All SQL verbatim under `sql_queries`.
   - `01_05_02_psi_shift.md` — table, SQL, literature citations (Siddiqi
     2006, Cohen 1988, Breck et al. 2019), `# Verdict:` line.
   - `01_05_02_psi_shift_per_feature.csv` — long-format (feature, quarter,
     psi, cohen_h, cohen_d, ks_stat, n_ref, n_test, unseen_count) for
     T09 Phase-06 interface emission.

**Verification:**
- JSON contains `frozen_reference_edges`, `psi_matrix`, `effect_sizes`,
  `unseen_bin_counts`, `sql_queries`, `assertion_passed: true`.
- Markdown cites Siddiqi (2006), Cohen (1988), Breck et al. (2019).
- No POST_GAME feature appears in any output row (I3 compliance).

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift_per_feature.csv`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json`

---

### T04 — Q3 Stratification + secondary regime `leaderboard_id`

**Objective:** Produce the honest-statement block (§5) confirming
`regime_id ≡ calendar quarter` for cross-dataset purposes, and emit a
within-dataset secondary-regime analysis on `leaderboard_id`
(rm_1v1=6 vs. qp_rm_1v1=18). rm_team is out-of-analytical-scope per
01_04_01 R01 — documented but not computed.

**Instructions:**
1. Create `01_05_03_stratification.py`. Hypothesis:
   - `# Hypothesis: PSI magnitudes on pre-game features differ
     systematically between internalLeaderboardId=6 and =18 by at least
     0.05 (absolute) in at least one quarter.`
   - `# Falsifier: max |PSI(lb=6) - PSI(lb=18)| across feature-quarter
     cells is < 0.05.`
2. Re-run T03's PSI computation restricted to lb=6 and lb=18 separately,
   using the lb-specific frozen reference edges (reference period, filtered
   by `internalLeaderboardId`).
3. Emit table of `(feature, quarter, lb, psi, cohen_h, cohen_d, ks, n)`.
4. Document rm_team out-of-scope: cite 01_04_01 R01 decision rationale.
   Include a paragraph stating that the cross-dataset `regime_id ≡ quarter`
   identity is preserved; the secondary-regime analysis is flagged
   `[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]` per spec §3.
5. Emit:
   - `01_05_03_stratification.json`.
   - `01_05_03_stratification.md`.
   - `01_05_03_stratification_per_lb.csv`.

**Verification:**
- Every row in `01_05_03_stratification_per_lb.csv` has
  `leaderboard_id` in `{6, 18}`.
- MD contains the `[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]` flag.
- MD explicitly quotes the §5 honest statement `regime_id ≡ calendar quarter`.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_03_stratification.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_03_stratification.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification_per_lb.csv`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json`

---

### T05 — Q4 Triple survivorship: unconditional + sensitivity + conditional labels

**Objective:** Implement the three parallel survivorship analyses per §6:
unconditional quarterly fraction_active, N∈{5,10,20} sensitivity, and
caption propagation of the default N=10. Input is `matches_history_minimal`
(zero-NULL player_id in aoec).

**Instructions:**
1. Create `01_05_04_survivorship.py`. Hypothesis:
   - `# Hypothesis: fraction_active (quarterly) falls monotonically
     from the reference period forward for >=75% of players ever seen,
     implying non-random attrition.`
   - `# Falsifier: fraction_active has no monotonic trend (Spearman
     rank correlation with quarter-index p > 0.20) over tested quarters.`
2. SQL for unconditional `fraction_active`:
   ```sql
   WITH players AS (
       SELECT DISTINCT player_id
       FROM matches_history_minimal
       WHERE started_at >= TIMESTAMP '2022-07-01'
         AND started_at <  TIMESTAMP '2025-01-01'
   ),
   player_quarter AS (
       SELECT player_id,
              CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
                     CAST(CEIL(EXTRACT(MONTH FROM started_at)/3.0) AS VARCHAR)) AS quarter
       FROM matches_history_minimal
       WHERE started_at >= TIMESTAMP '2022-07-01'
         AND started_at <  TIMESTAMP '2025-01-01'
       GROUP BY 1,2
   )
   SELECT quarter,
          COUNT(DISTINCT pq.player_id) * 1.0 / (SELECT COUNT(*) FROM players) AS fraction_active
   FROM player_quarter pq
   GROUP BY quarter
   ORDER BY quarter;
   ```
3. Emit `survivorship_unconditional.csv` per spec §6.1 path convention:
   - CSV schema: `quarter, fraction_active, n_active, n_ever_seen`.
4. Compute 90-day trailing-window churn rate per quarter (spec §6.1
   definition) as additional column.
5. For sensitivity (§6.2), per N ∈ {5, 10, 20}:
   - Restrict the cohort to players with ≥N matches in the reference
     period AND with active span ≥30 days.
   - Re-run T03 PSI on this cohort and emit the delta-PSI table.
6. Emit `survivorship_sensitivity.csv` per spec §6.2 schema:
   - `n_threshold, feature, quarter, psi, psi_delta_from_unconditional, n_players, n_matches`.
7. Conditional-label caption for default N=10: add the string
   `(conditional on >=10 matches in reference period; see §6 for sensitivity)`
   to every figure and every MD artifact row across T03/T04/T05.
8. **Reproducibility caveat:** 264M-row `player_history_all` is used only
   for the N-match-count query; `matches_history_minimal` (61M rows) is
   the analysis substrate. Cite aoec INVARIANTS §3 reservoir-sample
   caveat in the MD.

**Verification:**
- Both CSV files exist and have correct schemas.
- `survivorship_sensitivity.csv` has ≥ 3 * 4 * 8 = 96 rows (3 N values
  × 4 features × 8 tested quarters).
- Every captioned figure/table carries the N=10 suffix.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json`

---

### T06 — Q6 Variance decomposition (ICC) via statsmodels.mixedlm

**Objective:** Fit the random-intercept model `won ~ 1 + (1 | player_id)`
per spec §8 on the rm_1v1 cohort restricted to players with ≥10
observations. Report ICC = τ² / (τ² + σ²) with a delta-method 95% CI per
Gelman & Hill (2007) §12.5. Secondary: `player × civ` interaction.

**Instructions:**
1. T00 must complete (statsmodels installed).
2. Create `01_05_05_icc.py`. Hypothesis:
   - `# Hypothesis: ICC for won is in the range [0.05, 0.20], consistent
     with a large but not dominant between-player variance component
     typical of competitive matchmaking systems.`
   - `# Falsifier: ICC point estimate < 0.02 or > 0.50 (either indicates
     a severe departure from published skill-rating ICCs in esports).`
3. Pull data to a pandas DataFrame via DuckDB:
   ```python
   PRIMARY_QUERY = """
   SELECT mhm.player_id, mhm.won, mhm.faction
   FROM matches_history_minimal mhm
   WHERE mhm.started_at >= TIMESTAMP '2022-07-01'
     AND mhm.started_at <  TIMESTAMP '2025-01-01'
     AND mhm.player_id IN (
       SELECT player_id
       FROM matches_history_minimal
       WHERE started_at >= TIMESTAMP '2022-08-29'
         AND started_at <  TIMESTAMP '2023-01-01'
       GROUP BY player_id HAVING COUNT(*) >= 10
     );
   """
   ```
4. **Sampling:** if `n_players > 50_000`, seed=42 draw of 50k; else use
   all. Sensitivity reruns at 25k and 100k (if cohort allows) — declared
   as sample-size sensitivity, NOT a spec deviation (spec §8 fixes the
   method, not sample size). Document methodology in MD.
5. Fit primary:
   ```python
   import statsmodels.formula.api as smf
   model = smf.mixedlm("won ~ 1", data=df, groups=df["player_id"])
   result = model.fit(method=["lbfgs", "bfgs", "cg"], reml=True)
   tau2 = float(result.cov_re.iloc[0, 0])
   sigma2 = float(result.scale)
   icc = tau2 / (tau2 + sigma2)
   ```
6. Delta-method 95% CI: standard errors from `result.bse_re` and
   `result.bse` for `scale`, variance of the ratio via Taylor expansion
   per Gelman & Hill §12.5. Full derivation in MD.
7. Secondary (`player × civ`):
   ```python
   model2 = smf.mixedlm("won ~ 1", data=df, groups=df["player_id"],
                        re_formula="~1", vc_formula={"civ": "0 + C(faction)"})
   ```
   Report variance components; document non-convergence if observed.
8. Emit:
   - `01_05_05_icc.json` — tau2, sigma2, icc, icc_ci_low, icc_ci_high,
     n_players, n_obs_per_player_median, convergence_flag, sample_size,
     sensitivity_25k_icc, sensitivity_100k_icc, sql_queries, model_summary_text.
   - `01_05_05_icc.md` — table, derivation, citations (Gelman & Hill 2007,
     Bates et al. 2015), `# Verdict:` line, sample-size sensitivity
     section.

**Verification:**
- `statsmodels` importable.
- ICC point estimate in JSON is a finite float in [0, 1].
- If primary fit's `converged == False`, the JSON records
  `convergence_flag: false` and the MD explains the fallback.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_05_icc.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_05_icc.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json`

---

### T07 — Q7 `temporal_leakage_audit_v1`: 3 queries, hard gates

**Objective:** Implement the three audit queries per spec §9 and
terminate on violation. Notebook filename MUST be
`01_05_aoec_leakage_audit.py` per spec §9 naming.

**Instructions:**
1. Create `01_05_aoec_leakage_audit.py` — spec-binding header + hypothesis:
   - `# Hypothesis: zero rows in matches_history_minimal have
     observation_time >= match_time (I3 compliance); zero POST_GAME
     tokens appear in the pre-game feature list used in T03; reference
     period window constants match spec §7 exactly.`
   - `# Falsifier: any of the above is violated -> step halts.`
2. **Query 1** — Future-data check. aoec has no distinct
   `observation_time` per row; the analogue is: no row in
   `matches_history_minimal` can inform its own features. The
   instantiation asserts that the frozen reference period window
   `[2022-08-29, 2022-12-31]` does not overlap any tested quarter
   `2023-Q1..2024-Q4`:
   ```sql
   SELECT COUNT(*) AS future_leak_count
   FROM matches_history_minimal
   WHERE started_at >= TIMESTAMP '2022-08-29'
     AND started_at <  TIMESTAMP '2023-01-01'
     AND match_id IN (
       SELECT match_id
       FROM matches_history_minimal
       WHERE started_at >= TIMESTAMP '2023-01-01'
     );
   ```
   Expected: 0 rows. Block on non-zero.
3. **Query 2** — POST_GAME token scan. Python AST scan of
   `01_05_02_psi_shift.py` and `01_05_03_stratification.py`; blocks if
   any of `{duration_seconds, is_duration_suspicious, is_duration_negative,
   ratingDiff, finished}` appears in the pre-game feature list.
4. **Query 3** — Normalization-fit-window assertion:
   ```python
   from datetime import datetime
   assert ref_start == datetime(2022, 8, 29), f"Bad ref_start: {ref_start}"
   assert ref_end == datetime(2022, 12, 31), f"Bad ref_end: {ref_end}"
   ```
   This assertion is asserted inside both T03 and T07; T07 additionally
   reads the T03 JSON and checks `frozen_reference_edges.ref_start`
   and `frozen_reference_edges.ref_end` against the literal dates.
5. All three checks passing = step continues. Any failing check halts.
6. Emit:
   - `01_05_aoec_leakage_audit.json` — 3 checks with booleans, counts,
     SQL verbatim, AST-scan list of matched tokens.
   - `01_05_aoec_leakage_audit.md` — table, literal SQL, pass/fail per
     check, `# Verdict:` line.

**Verification:**
- JSON `checks[0].status == 'PASS'` and `future_leak_count == 0`.
- JSON `checks[1].status == 'PASS'` and `post_game_tokens_found == []`.
- JSON `checks[2].status == 'PASS'` and the two assert lines evaluated
  without exception.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_03_stratification.py`

---

### T08 — Q8 POST_GAME DGP diagnostics (`duration_seconds` + suspicious flags)

**Objective:** Report summary statistics, Cohen's d vs. reference, and
corruption-flag rate for `duration_seconds` per quarter, using the
`dgp_diagnostic_` filename prefix required by spec §10. POST_GAME
features NEVER appear in T03/T04 outputs; T08 is their sole home.

**Instructions:**
1. Create `01_05_06_dgp_duration.py`. Hypothesis:
   - `# Hypothesis: duration_seconds median and p95 are stable within
     +/- 10% across quarters after excluding is_duration_suspicious and
     is_duration_negative rows; Cohen's d on cleaned duration vs.
     reference is < 0.2 in every quarter.`
   - `# Falsifier: any quarter has |Cohen's d| >= 0.5 (medium effect)
     on cleaned duration.`
2. Per tested quarter + reference period, compute via DuckDB:
   ```sql
   SELECT
     quarter,
     AVG(duration_seconds)                              AS mean_dur,
     quantile_cont(duration_seconds, 0.5)               AS median_dur,
     quantile_cont(duration_seconds, 0.05)              AS p05,
     quantile_cont(duration_seconds, 0.95)              AS p95,
     quantile_cont(duration_seconds, 0.75)
       - quantile_cont(duration_seconds, 0.25)          AS iqr,
     COUNT(*) FILTER (WHERE is_duration_suspicious)
       * 1.0 / COUNT(*)                                 AS suspicious_rate,
     COUNT(*) FILTER (WHERE is_duration_negative)
       * 1.0 / COUNT(*)                                 AS negative_rate
   FROM matches_1v1_clean
   WHERE <quarter-filter>
   GROUP BY quarter;
   ```
3. Compute Cohen's d per quarter vs. reference period using pooled SD.
   Produce two d series: one on raw `duration_seconds`, one on cleaned
   (excluding both flags).
4. Emit one CSV per quarter per spec §10 naming:
   `dgp_diagnostic_aoe2companion_<quarter>.csv` for each of
   2023-Q1..2024-Q4 + reference period (9 files total). Plus:
   - `01_05_06_dgp_duration.json` — consolidated stats.
   - `01_05_06_dgp_duration.md` — table, SQL, citations.
5. Absolutely no PSI computation on POST_GAME features (§10 guard).

**Verification:**
- 9 CSV files matching `dgp_diagnostic_aoe2companion_*.csv` exist.
- None of the 9 files contains a PSI column.
- JSON records the 142 suspicious rows and 342 negative rows as expected
  upstream (per aoec INVARIANTS §1) — reconciliation note in MD if the
  count drifts across rebuilds per the reservoir-sample caveat.

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_reference.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q1.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q2.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q3.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q4.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q1.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q2.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q3.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q4.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json`

---

### T09 — Phase 06 interface CSV emission per §12 flat schema

**Objective:** Consolidate Q2/Q3/Q5/Q6 metric values into the single
cross-dataset flat schema defined in §12. One row per
(dataset × quarter × feature × metric).

**Instructions:**
1. Create `01_05_07_phase06_interface.py` — no new analysis; pure
   aggregation over T03/T04/T06 artifacts.
2. Emit a single CSV `01_05_phase06_interface_aoe2companion.csv` with the
   exact §12 schema:
   | dataset_tag | quarter | feature_name | metric_name | metric_value | reference_window_id | cohort_threshold | sample_size | notes |
3. `dataset_tag = 'aoe2companion'` literally.
4. `reference_window_id = '2022-Q3Q4'` per spec §12 example string for
   aoec (4-month reference window, non-aoestats).
5. `cohort_threshold = 10` for default rows; 5 and 20 for sensitivity
   rows emitted from T05's `survivorship_sensitivity.csv`.
6. `metric_value` formatted to 4 decimal places; NaN encoded as SQL
   NULL (empty CSV cell).
7. `notes` — free text, e.g. `[WITHIN-AOEC-SECONDARY; lb=18]`,
   `__unseen__: 3 rows`, `sample_too_small (n_matches < 1000)`.
8. Emit MD validation `01_05_07_phase06_interface.md` — row count by
   (feature, metric), sanity check against T03/T04/T06 source values,
   `# Verdict:` line.

**Verification:**
- CSV has header `dataset_tag,quarter,feature_name,metric_name,metric_value,reference_window_id,cohort_threshold,sample_size,notes` — exact match to §12 schema.
- All `dataset_tag` values = `aoe2companion`.
- `metric_name` values ⊆ `{psi, cohen_h, cohen_d, ks_stat, icc, icc_ci_low, icc_ci_high}`.
- MD includes row count ≥ 4 features × 8 quarters × 4 metrics = 128 minimum (plus ICC rows, sensitivity rows, and lb-split rows).

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.py`
- `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_phase06_interface_aoe2companion.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.md`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift_per_feature.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification_per_lb.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.json`

---

### T10 — Research log + INVARIANTS §4 + status files + ROADMAP + Decision Gate memo

**Objective:** Close 01_05 for aoe2companion by updating all tracking
documents and producing the Decision Gate memo (01_06 input per spec §15
and docs/PHASES.md Pipeline Section 01_06).

**Instructions:**
1. Append a research_log.md entry dated 2026-04-18 under the anchor
   `#2026-04-18-01-05-temporal-panel-eda`, following the required
   Category-A template in `docs/templates/research_log_entry_template.yaml`.
   Include: What/Why/How, Findings (Q1–Q9 summary bullets with artifact
   paths), Decisions taken, Decisions deferred, Thesis mapping (Chapter
   4 §4.1.2 and §4.2 distribution shift), Open questions.
2. Update `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/INVARIANTS.md`
   §4 with per-quarter row counts, PSI max value, ICC point estimate
   and CI, survivorship attrition, DGP duration median stability. Cite
   artifact paths.
3. Update status files:
   - Append 9 steps `01_05_01`..`01_05_07` + `01_05_08` (T07 leakage audit)
     + `01_05_09` (T09 Phase-06 interface) in `STEP_STATUS.yaml` all
     as `status: complete` with `completed_at: "2026-04-18"` once all
     artifacts exist.
   - Append pipeline section `01_05` (Temporal & Panel EDA) in
     `PIPELINE_SECTION_STATUS.yaml` with `status: complete` once all
     9 steps are complete.
   - `PHASE_STATUS.yaml` — Phase 01 stays `in_progress` because 01_06
     Decision Gates remain; do NOT mark Phase 01 complete.
4. Update `ROADMAP.md` by appending 9 step YAML blocks under
   "Pipeline Section 01_05" using the schema from
   `docs/templates/step_template.yaml`. Step names:
   01_05_01 Quarterly Grain, 01_05_02 PSI Shift, 01_05_03 Stratification,
   01_05_04 Survivorship, 01_05_05 ICC, 01_05_06 DGP Duration,
   01_05_07 Phase06 Interface, 01_05_08 Leakage Audit, 01_05_09 Research
   Log Consolidation.
5. Decision Gate memo — save `01_05_DECISION_GATE_MEMO.md` summarising:
   (a) PSI max per feature vs. 0.25 threshold → pass/escalate verdict;
   (b) ICC point estimate with interpretation (low/medium/high
   between-player variance) and consequence for Phase 03 grouped-splits
   design; (c) survivorship attrition trend and consequence for Phase 02
   cold-start design; (d) leakage audit verdict (all PASS required).
6. Instruct parent session: "For Category A plans, adversarial
   critique is required before execution begins. Dispatch
   reviewer-adversarial to produce `planning/current_plan.critique.md`."

**Verification:**
- `grep -c "2026-04-18.*01-05" src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` returns ≥ 1.
- `grep -c "01_05" src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` returns ≥ 9.
- `grep "01_05:" src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml` returns one line.
- `PHASE_STATUS.yaml` still reports `"01": in_progress` — verifies
  01_06 gate is not prematurely marked complete.
- `01_05_DECISION_GATE_MEMO.md` exists with all 4 sub-verdicts.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/INVARIANTS.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_DECISION_GATE_MEMO.md`

**Read scope:**
- All artifacts emitted by T02–T09 (paths listed in File Manifest).

---

## File Manifest

| File | Action |
|------|--------|
| `pyproject.toml` | Update |
| `poetry.lock` | Update |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/.gitkeep` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/README.md` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_03_stratification.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_03_stratification.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_05_icc.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_05_icc.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.ipynb` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.py` | Create |
| `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.ipynb` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_shift_per_feature.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_stratification_per_lb.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_reference.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2023-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoe2companion_2024-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_dgp_duration.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_phase06_interface_aoe2companion.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_aoec_leakage_audit.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_DECISION_GATE_MEMO.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/INVARIANTS.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` | Update |

## Gate Condition

Binary observable conditions — every one must hold for 01_05 to close.

- All 9 `01_05_*` notebooks (paired `.py` + `.ipynb`) exist under
  `sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/`.
- Every notebook's first 40 lines contain the literal
  `# spec: reports/specs/01_05_preregistration.md@7e259dd8`, and
  `source .venv/bin/activate && poetry run python scripts/check_01_05_binding.py --all`
  exits 0.
- All artifacts listed in the File Manifest exist on disk under
  `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/`.
- `01_05_02_psi_shift.json` contains `frozen_reference_edges.ref_start == "2022-08-29"`
  and `frozen_reference_edges.ref_end == "2022-12-31"`.
- `01_05_aoec_leakage_audit.json` has all 3 checks `status: PASS`.
- No POST_GAME token (`duration_seconds`, `is_duration_suspicious`,
  `is_duration_negative`, `ratingDiff`, `finished`) appears in any
  T03/T04 output row.
- `01_05_phase06_interface_aoe2companion.csv` conforms to spec §12
  exact 9-column schema, every `dataset_tag == 'aoe2companion'`, and
  every `metric_value` is numeric-parseable or empty.
- `01_05_05_icc.json` reports a finite ICC point estimate ∈ [0, 1] with
  finite 95% CI bounds.
- `STEP_STATUS.yaml` lists 9 new entries under 01_05 with
  `status: complete`.
- `PIPELINE_SECTION_STATUS.yaml` contains `01_05` with
  `status: complete`.
- `PHASE_STATUS.yaml` shows `"01": in_progress` (NOT complete —
  01_06 Decision Gate remains).
- `01_05_DECISION_GATE_MEMO.md` exists and contains sub-verdicts
  for PSI, ICC, survivorship, leakage.
- `source .venv/bin/activate && poetry run pytest tests/ -v` still passes
  (no test regressions).
- `source .venv/bin/activate && poetry run ruff check src/ tests/ sandbox/aoe2/aoe2companion/01_exploration/05_temporal_panel_eda/`
  exits 0.
- Research log entry anchored at
  `#2026-04-18-01-05-temporal-panel-eda` exists.
- `git diff --name-only master..feat/01-05-aoe2companion` lists only
  files in the File Manifest (no unplanned edits).

## Out of scope

- Any modification to DuckDB tables, VIEWs, or schemas. 01_05 is
  read-only against 01_04 outputs.
- `patch_id` reconstruction from external aoe2companion API endpoints —
  deferred to Phase 02 or later (§15 confirms no spec action required
  here).
- `team` column or `canonical_slot` — aoec has no `team` column in the
  analytical substrate (natively player-row). The `canonical_slot`
  follow-up is an aoestats-only concern (spec §11, §15).
- rm_team leaderboard slice — out-of-analytical-scope per 01_04_01 R01;
  secondary regime comparison is rm_1v1 (lb=6) vs. qp_rm_1v1 (lb=18)
  only.
- ADF/KPSS stationarity tests — prohibited cross-dataset per §3
  (Hamilton 1994 §17.7 N≥50 requirement). The spec-permitted
  within-aoec secondary ADF analysis on monthly data (§3 extended window)
  is not executed here; deferred as "optional within-aoec extension"
  to a later PR if thesis chapter 4 needs it.
- Phase 02 feature engineering decisions (cold-start policy, window
  lengths, rating-update cadence) — 01_05 findings inform these but
  the decisions belong in Phase 02.
- sc2egset and aoestats sibling executions of 01_05 — separate PRs.
  This plan covers aoec only.
- Writing the `reports/research_log.md` CROSS entry — this is a per-
  dataset step; CROSS coordination happens after all three datasets
  have completed 01_05 (separate coordination PR).

## Open questions

- **Reservoir non-determinism** — T05 sensitivity sampling and T06 50k
  sub-sample cite aoec `INVARIANTS.md` §3 (DS-AOEC-IDENTITY-05 footnote).
  Is a fixed-order materialised table (e.g., ORDER BY match_id) needed
  for bit-exact cross-rebuild reproduction, or is the methodological-
  equivalence guarantee sufficient? Resolves by: user decision prior to
  T05/T06 execution (default: accept methodological-equivalence
  guarantee, document rebuild state per aoec INVARIANTS §3).
- **`won` NULL 4.69% cluster** — confirmed to apply to `matches_raw`,
  not `matches_history_minimal`. Q4 survivorship and Q6 ICC operate on
  `matches_history_minimal` where `won` is zero-NULL (R03 guarantee).
  Sanity-check: is the T05 cohort definition compatible with the fact
  that R03 drops any match with incomplete complementarity? Resolves
  by: T05 executor asserting `COUNT(*) FILTER (WHERE won IS NULL) = 0`
  on `matches_history_minimal` before cohort filtering.
- **`leaderboard_id` secondary regime design** — spec §5 lists
  `leaderboard_id` as aoec's secondary regime with values `rm_1v1 /
  rm_team`. Analytical scope excludes rm_team (R01). Decision: run
  rm_1v1 (lb=6) vs. qp_rm_1v1 (lb=18) as the within-aoec split, labeled
  `[WITHIN-AOEC-SECONDARY; rm_1v1 vs. qp_rm_1v1]` in all outputs;
  document in T04 MD that spec §5's `rm_team` label is a general
  shorthand and not binding when rm_team is out-of-scope. Resolves by:
  T04 executor noting this deviation in the MD — it is NOT a spec §14
  amendment because spec §5 lists the secondary regime as
  "within-dataset only, non-binding".
- **`patch_id` in aoec** — not present in any aoec schema.
  `01_05_phase06_interface_aoe2companion.csv` emits `NULL` rows for
  `feature_name='patch_id'` with `notes: 'patch_id not available in aoec'`
  OR omits the feature entirely. Resolves by: T09 executor — omit
  `patch_id` rows to keep the CSV truthful (spec §12 does not require
  every feature to appear in every dataset's CSV).
- **mixedlm convergence on 50k players** — resolves by T06 executor per
  the fallback strategy declared in T06 instructions (retry with
  `method=['lbfgs', 'bfgs', 'cg']`; if still divergent, fall back to
  25k and document).
- **Low-volume quarters in rm_1v1** — T02 will surface any quarter with
  <1,000 matches (falsifier case). Expected outcome: none (aoec volume
  is large), but if a quarter fails, T03 emits `NULL` PSI with
  `sample_too_small` note; T09 propagates. Resolves by: T02 executor.

---

**Critique instruction for parent session:** This is a Category A plan.
Adversarial critique is required before execution begins. Dispatch
reviewer-adversarial with:
- `plan_path = planning/current_plan.md`
- `base_ref = master`
- Scope: all sections, focus on I3/I6/I7 compliance, spec §§3–14
  conformance, and the three aoec-specific design decisions (reservoir
  non-determinism, `won` NULL scope, rm_team exclusion).

Produce `planning/current_plan.critique.md` before execution begins.