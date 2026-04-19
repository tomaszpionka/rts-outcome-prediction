---
# Layer 1 — fixed frontmatter (mechanically validated)
category: A
branch: feat/01-05-aoestats
date: 2026-04-18
planner_model: claude-opus-4-7
dataset: aoestats
phase: "01"
pipeline_section: "Temporal & Panel EDA"
invariants_touched: [I3, I5, I6, I7, I8, I9]
source_artifacts:
  - reports/specs/01_05_preregistration.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_05_i5_diagnosis.json
  - src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_history_minimal.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_1v1_clean.yaml
  - src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/raw/overviews_raw.yaml
  - sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_05_i5_diagnosis.py
  - scripts/check_01_05_binding.py
  - planning/BACKLOG.md
  - docs/PHASES.md
  - docs/TAXONOMY.md
  - docs/templates/plan_template.md
  - .claude/scientific-invariants.md
critique_required: true
research_log_ref: src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md#2026-04-18-01-05-temporal-panel-eda
---

# Plan: aoestats Pipeline Section 01_05 — Temporal & Panel EDA (spec v1.0.1, SHA 7e259dd8)

## Scope

Execute Pipeline Section 01_05 (Temporal & Panel EDA) for the aoestats dataset under the pre-registered protocol in `reports/specs/01_05_preregistration.md@7e259dd8`. Produce all nine spec-bound analyses (Q1 quarterly grain, Q2 PSI, Q3 stratification + `patch_id` secondary regime, Q4 triple survivorship, Q5 drift with single-patch reference, Q6 between/within variance decomposition, Q7 `temporal_leakage_audit_v1` with aoestats-specific Query 4, Q8 POST_GAME DGP diagnostics, Q9 Phase 06 interface CSV), emit `[PRE-canonical_slot]`-tagged outputs wherever a finding conditions on `team`-mirror-propagated row position, and close the Section via research log, INVARIANTS §4 update, STEP/PIPELINE_SECTION/PHASE status ticks, ROADMAP Step insertions, and a Decision-Gate memo explicitly naming BACKLOG item F1 (`canonical_slot`) as the unblocker for aoestats Phase 02.

## Problem Statement

The aoestats 01_04 Pipeline Section closed on 2026-04-18 with Step 01_04_05 producing the ARTEFACT_EDGE verdict for the upstream `team`-slot asymmetry (CMH effect −0.72pp; team=1 has higher ELO in 80.3% of games; mean ELO diff +11.9). The UNION-ALL pivot in `matches_history_minimal` was confirmed I5-compliant (`won_rate = 0.5` exactly), but `team` itself must not be a Phase 02 feature, and any slot-conditioned figure produced before a `canonical_slot` column is added must be flagged `[PRE-canonical_slot]` (spec §9, §11; BACKLOG F1). 01_05 is the last Phase 01 Pipeline Section before the Decision Gate (01_06). It must establish: (a) whether feature distributions are stationary across the 10-quarter overlap window 2022-Q3..2024-Q4 (PSI), (b) whether a single-patch reference period (2022-08-29..2022-10-27, patch 125283) produces homogeneous reference statistics despite being asymmetric to sc2egset/aoec reference periods (§7), (c) whether player-level variance dominates match-level variance (ICC via `statsmodels.mixedlm`), (d) whether any feature-input list contains POST_GAME_HISTORICAL tokens or future-time observations (hard gate Q7.1, Q7.2), and (e) whether `canonical_slot` is ready (Q7.4 aoestats-specific; expected: absent — emit warning, do not block).

The gap: no 01_05 artifacts exist yet; all T10 status rows are `not_started`; `matches_history_minimal` is 9-column (no `canonical_slot`); the Phase 06 interface table has never been emitted. This plan closes that gap per the locked pre-registered protocol without deviating from any §3–§11 parameter.

## Assumptions & unknowns

- **Assumption:** `matches_history_minimal` (35,629,894 rows = 17,814,947 matches × 2 halves) is the canonical aoestats input for Q1/Q2/Q5/Q6, with JOIN to `matches_1v1_clean` on `match_id = 'aoestats::' || game_id` for `patch` (BIGINT) stratification. Verified by schema YAML: `matches_history_minimal.yaml` (9 cols: `match_id, started_at, player_id, opponent_id, faction, opponent_faction, won, duration_seconds, dataset_tag`) and `matches_1v1_clean.yaml` (22 cols including `patch`).
- **Assumption:** Reference period `patch = 125283` contains approximately 800k matches across 9 weekly files (spec §7), and single-patch homogeneity reduces within-reference variance relative to a 4-month multi-patch window. Verified by running Q1 row counts during T02 against `patch` filter.
- **Assumption:** `canonical_slot` is absent from `matches_history_minimal` schema (confirmed by `matches_history_minimal.yaml` read — no such column). Q7.4 probe returns 0 rows → the audit logs `canonical_slot_ready=False` with `[PRE-canonical_slot]` tag and proceeds without blocking (spec §9).
- **Assumption:** All pre-game features available for PSI are: `faction`, `opponent_faction` (categorical, 50 civs each), and — via JOIN — `p0_old_rating`, `p1_old_rating`, `avg_elo`, `map`, `patch`, `p0_is_unrated`, `p1_is_unrated`, `mirror`. `won` is TARGET (excluded from §4 PSI per spec; included only in §8 ICC). `duration_seconds` is POST_GAME_HISTORICAL (excluded from §4 PSI; included in §10 DGP diagnostics).
- **Assumption:** The 28 corrupted matches (duration > 86,400s; `is_duration_suspicious=TRUE`) are NOT removed for PSI/Q5/Q6 (they are retained unless a specific analysis documents exclusion). Q8 DGP diagnostics report the corruption rate per quarter separately per spec §10.
- **Unknown:** Exact per-quarter row counts in aoestats for 2022-Q3, 2022-Q4, 2023-Q1..2024-Q4. Resolved during T02 execution by reading the data; feeds the §12 `sample_size` column. T02 also verifies that each tested quarter has ≥ 10,000 focal-player-rows to avoid degenerate PSI on sparse bins.
- **Unknown:** Whether `mixedlm` converges for a 641,662-profile random-intercept fit on ~3.5M-row N=10 subsample. Resolved during T06 by restarting with smaller samples if `optimize` returns `ConvergenceWarning`; planner fallback is a stratified reservoir sample with ≥ 50,000 unique players (seed `RANDOM_SEED = 42`, constant in `rts_predict.common.config`).

## Literature context

Spec §16 names seven references: `hamilton1994` (ADF/KPSS power floor — justifies cross-dataset ADF prohibition at N=8), `siddiqi2006` (PSI definition, 10-bin equal-frequency method, 0.10 / 0.25 thresholds), `breck2019` (TFDV reference implementation and KS descriptive magnitude), `gelman2007` §12.5 (ICC delta-method CI), `cohen1988` (effect sizes h and d), `mantel1959` + `robins1986` (CMH used in 01_04_05 — cited here only as W3 provenance per spec §11 lock; no new CMH computations).

Patch-heterogeneity context for the aoestats-specific single-patch reference (§7): Chung & Yeung (2022) characterise Dota 2 patch-induced behavioural disruption across 36 months ([arXiv:2207.02736](https://arxiv.org/pdf/2207.02736)); Lopes et al. (2021) quantify heterogeneous treatment effects of MOBA patches on player behaviour ([ACM FDG](https://dl.acm.org/doi/fullHtml/10.1145/3472538.3472550)). These establish that patch-induced distributional shift is a recognised confounder in online-game panel data; the single-patch reference window (2022-08-29..2022-10-27, patch 125283) controls for that confounder at the cost of reference-length asymmetry with sc2egset/aoec (9 weeks vs. 4 months). This asymmetry is spec-locked and documented as a within-reference homogeneity prioritisation ([spec §7 rationale, §14 v1.0 amendment](reports/specs/01_05_preregistration.md)).

Regarding ICC fit on a massive panel (641,662 players, ~3.5M player-matches in the reference cohort): `statsmodels.mixedlm` fits a random-intercept LMM on the formula `won ~ 1 + (1 | player_id)` ([statsmodels docs](https://www.statsmodels.org/stable/generated/statsmodels.regression.mixed_linear_model.MixedLM.html)); the ICC is computed as `σ²_player / (σ²_player + σ²_resid)` ([Gelman & Hill 2007, §12.5](https://statmodeling.stat.columbia.edu/wp-content/uploads/2007/12/gelman_hill_arm_book.pdf)). Delta-method CI for ICC is standard per [sjstats vignette](https://cran.r-hub.io/web/packages/sjstats/vignettes/mixedmodels-statistics.html).

PSI 10-bin equal-frequency deciles with frozen reference edges are the default in `scorecard` R package (Shichen Xie, v0.4.6) matching [Siddiqi (2006)](https://www.listendata.com/2015/05/population-stability-index.html) and [Fiddler AI's PSI primer](https://www.fiddler.ai/blog/measuring-data-drift-population-stability-index). `__unseen__` bin accommodation for categoricals mirrors [Breck et al. (2019) TFDV](https://mlsys.org/Conferences/2019/doc/2019/167.pdf). [OPINION] No reference directly addresses an asymmetric single-patch reference window for competitive-game PSI; the methodology here is novel but grounded in the cited panel-heterogeneity literature.

## Execution Steps

### T01 — Scaffold 01_05 directory + spec-binding + sandbox hygiene

**Objective:** Create the `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/` directory tree, initialise all ten notebook pairs (T02–T10 + the orchestrating audit in T07), and confirm each carries the spec-binding line `# spec: reports/specs/01_05_preregistration.md@7e259dd8` within the first 40 source lines. Verify the `check-01-05-binding` pre-commit hook recognises the files.

**Instructions:**
1. Create directories: `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/` and `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/` (and `.../plots/` subdir for any PNG emissions).
2. Create 9 paired `.py` / `.ipynb` files via jupytext (hard rule per `sandbox/README.md` §4): `01_05_01_quarterly_grain.{py,ipynb}`, `01_05_02_psi_pre_game_features.{py,ipynb}`, `01_05_03_stratification_patch_regime.{py,ipynb}`, `01_05_04_survivorship_triple.{py,ipynb}`, `01_05_05_variance_decomposition_icc.{py,ipynb}`, `01_05_06_temporal_leakage_audit.{py,ipynb}`, `01_05_07_dgp_diagnostics_duration.{py,ipynb}`, `01_05_08_phase06_interface.{py,ipynb}`, `01_05_09_gate_memo.{py,ipynb}`.
3. Each `.py` file opens with header block (first 40 lines): cell 0 = module docstring, cell 1 = `# spec: reports/specs/01_05_preregistration.md@7e259dd8` + `# Hypothesis: <per-notebook>` + `# Falsifier: <per-notebook>`. NO `def/class/lambda` in any cell (hard rule); all logic imports from `src/rts_predict/games/aoe2/datasets/aoestats/analysis/` modules created as needed.
4. Use `get_notebook_db()` and `get_reports_dir("aoe2", "aoestats") / "artifacts"` from `rts_predict.common.notebook_utils`; DuckDB open read-only.
5. Run `source .venv/bin/activate && poetry run python scripts/check_01_05_binding.py --all` and confirm output `check-01-05-binding OK (N file(s) checked).`

**Verification:**
- `ls sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/ | wc -l` returns 18 (9 `.py` + 9 `.ipynb`).
- `source .venv/bin/activate && poetry run python scripts/check_01_05_binding.py --all` exits 0.
- `grep -L "spec: reports/specs/01_05_preregistration.md@7e259dd8" sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/*.py` returns empty.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_02_psi_pre_game_features.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_03_stratification_patch_regime.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_triple.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_05_variance_decomposition_icc.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit.{py,ipynb}` (renamed from spec's `01_05_aoestats_leakage_audit.py` to match local numbering convention; spec §9 permits — path pattern for hook is `sandbox/*/01_exploration/05_temporal_panel_eda/*.py`).
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostics_duration.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface.{py,ipynb}`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/.gitkeep`

**Read scope:** (none — T01 is scaffolding)

---

### T02 — Quarterly grain + overlap window + per-quarter row counts (Q1)

**Objective:** Execute spec §3 (Q1 grain = calendar quarter) on the 10-quarter overlap window 2022-Q3..2024-Q4. Emit per-quarter row counts, unique-player counts, and match counts to establish sample-size context for all subsequent analyses. No ADF/KPSS (forbidden cross-dataset per §3).

**Hypothesis (in notebook, NOT ROADMAP):** `# Hypothesis: Every tested quarter 2023-Q1..2024-Q4 has >= 100,000 focal-player-rows in matches_history_minimal, supporting meaningful decile-PSI in T03.`  `# Falsifier: Any tested quarter has < 10,000 rows (PSI deciles would contain < 1,000 observations each, violating Siddiqi N>=300 per-bin floor).`

**Instructions:**
1. Connect read-only to `src/rts_predict/games/aoe2/datasets/aoestats/data/db/db.duckdb`.
2. Run the quarterly grain query:
   ```sql
   WITH quarterly AS (
     SELECT
       DATE_TRUNC('quarter', started_at) AS quarter_start,
       strftime(DATE_TRUNC('quarter', started_at), '%Y-Q') ||
         ((extract('month' FROM started_at) - 1) / 3 + 1)::VARCHAR AS quarter_iso,
       COUNT(*) AS row_count,
       COUNT(DISTINCT match_id) AS match_count,
       COUNT(DISTINCT player_id) AS player_count
     FROM matches_history_minimal
     WHERE started_at >= '2022-07-01' AND started_at < '2025-01-01'
     GROUP BY 1, 2
     ORDER BY 1
   )
   SELECT * FROM quarterly;
   ```
3. Assert `quarter_iso` values form contiguous sequence `2022-Q3, 2022-Q4, 2023-Q1, …, 2024-Q4` (10 quarters).
4. Emit CSV `quarterly_grain_row_counts.csv` and JSON `quarterly_grain_row_counts.json` with exact SQL verbatim under `sql_queries` key (I6).
5. If any tested quarter (2023-Q1..2024-Q4) has row_count < 10,000, log `# Verdict: Falsified — quarter {X} has {N} rows < 10,000` and record in research log.
6. Produce PNG `quarterly_row_counts.png` (matplotlib line + bar dual axis: row_count bar, player_count line).

**Verification:**
- `artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.{csv,json,md}` all exist and non-empty.
- JSON `sql_queries` key contains verbatim SQL (I6).
- `len(results) == 10` (10 quarters 2022-Q3..2024-Q4 inclusive).
- Notebook final cell prints `Q1 Falsifier verdict: <PASSED|FALSIFIED>`.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.{csv,json,md}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/plots/quarterly_row_counts.png`

**Read scope:** (none — reads DuckDB only)

---

### T03 — Equal-frequency PSI N=10 with frozen reference edges (Q2, spec §4)

**Objective:** Compute PSI for every pre-game feature in `matches_history_minimal` (with JOIN-pulled columns from `matches_1v1_clean`) across tested quarters 2023-Q1..2024-Q4, using the reference period 2022-08-29..2022-10-27 with `patch = 125283` (spec §7 aoestats-specific). Bin edges frozen from reference; `__unseen__` bin for categoricals. Pre-game features only; no POST_GAME_HISTORICAL, no TARGET. All outputs conditioned on cohort `N_matches >= 10 in reference period` (spec §6.3 default); carry caption suffix `(conditional on ≥10 matches in reference period; see §6 for sensitivity)` in MD artifact.

**Hypothesis:** `# Hypothesis: Rating drift (p0_old_rating, p1_old_rating) is the largest PSI contributor; PSI >= 0.10 in >= 3 of 8 tested quarters. Civ distribution (faction) is relatively stable (PSI < 0.10 in >= 5 quarters).`  `# Falsifier: Rating PSI < 0.10 across all 8 quarters AND faction PSI >= 0.25 in any quarter — would reverse expected drift ordering.`

**Instructions:**
1. Create helper module `src/rts_predict/games/aoe2/datasets/aoestats/analysis/psi.py` with pure functions:
   - `compute_decile_edges(values: pd.Series, n_bins: int = 10) -> np.ndarray` — uses `np.quantile(values, np.linspace(0, 1, n_bins + 1))`; returns edges.
   - `freeze_categorical_reference(values: pd.Series) -> list[str]` — returns sorted unique values in reference.
   - `apply_frozen_edges(values: pd.Series, edges: np.ndarray) -> pd.Series` — bins tested values into reference deciles; values outside `[min_edge, max_edge]` assigned to the nearest terminal bin.
   - `apply_frozen_categories(values: pd.Series, categories: list[str]) -> pd.Series` — returns series with `__unseen__` for any value not in `categories`.
   - `psi(ref_hist: np.ndarray, tested_hist: np.ndarray, eps: float = 1e-10) -> float` — classic Siddiqi formula: `sum((p_tested - p_ref) * log(p_tested / p_ref))`; `eps` floor per Breck et al. (2019).
2. Cohort filter: `cohort_profile_ids` = players with ≥ 10 matches in reference period (single-patch window).
3. For each tested quarter Q and each pre-game feature F ∈ {`p0_old_rating`, `p1_old_rating`, `avg_elo`, `faction`, `map`, `mirror`, `p0_is_unrated`, `p1_is_unrated`}:
   - Compute reference edges/categories from reference period restricted to `cohort_profile_ids`.
   - Compute tested histogram from Q restricted to `cohort_profile_ids`.
   - Compute PSI value; record `__unseen__` count for categoricals.
4. Notes-column tagging for `[PRE-canonical_slot]`: features `faction` / `opponent_faction` / `p0_old_rating` / `p1_old_rating` are slot-conditioned (computed per `player_id` which equals upstream p0 or p1 depending on UNION-ALL half). The UNION-ALL is I5-compliant, so the **aggregate** features are NOT slot-biased; however, any per-slot breakdown IS. T03's primary outputs are aggregate (over both halves) and do NOT carry the flag; any per-slot sensitivity cut (if produced) carries `[PRE-canonical_slot]`.
5. Assert at start of notebook: `assert ref_start == date(2022, 8, 29) and ref_end == date(2022, 10, 27), "Bad aoestats ref window"` (spec §9 Q3).
6. SQL for reference cohort:
   ```sql
   WITH ref_cohort AS (
     SELECT player_id, COUNT(*) AS n_matches
     FROM matches_history_minimal
     WHERE started_at BETWEEN '2022-08-29' AND '2022-10-27'
     GROUP BY player_id
     HAVING COUNT(*) >= 10
   )
   SELECT mhm.*, m1v1.patch, m1v1.p0_old_rating, m1v1.p1_old_rating,
          m1v1.avg_elo, m1v1.map, m1v1.mirror, m1v1.p0_is_unrated, m1v1.p1_is_unrated
   FROM matches_history_minimal mhm
   JOIN matches_1v1_clean m1v1
     ON mhm.match_id = 'aoestats::' || m1v1.game_id
   JOIN ref_cohort rc ON mhm.player_id = rc.player_id
   WHERE mhm.started_at BETWEEN '2022-08-29' AND '2022-10-27'
     AND m1v1.patch = 125283;
   ```
7. Emit `psi_aoestats_{quarter}.csv` per spec §10 naming (one file per tested quarter; header: `feature_name, psi_value, reference_bin_count, tested_bin_count, unseen_bin_count, notes`).

**Verification:**
- 8 files `psi_aoestats_2023-Q1.csv .. psi_aoestats_2024-Q4.csv` exist.
- Each file has 8 rows (one per pre-game feature).
- JSON artifact `01_05_02_psi_summary.json` contains reference-edge fingerprints (hash of edges) per feature, matching across all 8 tested quarters (proves frozen edges).
- Falsifier verdict printed: `Q2 rating-drift hypothesis: <PASSED|FALSIFIED>`.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_02_psi_pre_game_features.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/analysis/__init__.py`
- `src/rts_predict/games/aoe2/datasets/aoestats/analysis/psi.py`
- `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_psi.py` (synthetic-fixture tests; empty DF, single row, NaN handling, unseen categorical)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2023-Q1.csv` ... `psi_aoestats_2024-Q4.csv` (8 files)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.{json,md}`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.json` (from T02)

---

### T04 — Stratification + secondary regime `patch_id` (Q3, spec §5)

**Objective:** Implement spec §5 honest statement (`regime_id ≡ calendar quarter` cross-dataset) and compute the aoestats secondary within-dataset regime `patch_id` using the 19-patch map in `overviews_raw`. Non-binding, within-dataset only (spec §5). Extends to 2026-02-06 coverage for the aoestats-specific within-dataset view; this is NOT cross-dataset.

**Hypothesis:** `# Hypothesis: Per-patch win-rate by civ exhibits heterogeneity consistent with patch-driven balance changes; at least 3 civs show |Δwin_rate_quarter_vs_previous_quarter| >= 5pp in >= 1 patch transition.`  `# Falsifier: Civ win rates are stationary across all 19 patches (max |Δ| < 2pp for every civ at every patch boundary) — would undermine the patch-heterogeneity motivation for single-patch reference.`

**Instructions:**
1. Pull the 19-patch map from `overviews_raw`:
   ```sql
   SELECT UNNEST(patches) AS patch_info
   FROM overviews_raw;
   -- Then unpack STRUCT fields: number, label, release_date, total_games, ...
   SELECT p.patch_info.number AS patch_number,
          p.patch_info.label AS patch_label,
          p.patch_info.release_date AS release_date,
          p.patch_info.total_games AS total_games
   FROM (SELECT UNNEST(patches) AS patch_info FROM overviews_raw) p
   ORDER BY release_date;
   ```
2. Produce `patch_map.csv` (19 rows).
3. For each patch `P`, compute per-civ win rate over `matches_history_minimal` JOIN `matches_1v1_clean` on matching `patch` column. Output is NOT cross-dataset; label row-by-row `[WITHIN-AOESTATS-SECONDARY; NOT CROSS-DATASET]` per spec §3 naming (aoestats-adapted).
4. SQL:
   ```sql
   SELECT m1v1.patch AS patch_number,
          mhm.faction AS civ,
          COUNT(*) AS n_matches,
          AVG(CAST(mhm.won AS INTEGER)) AS win_rate
   FROM matches_history_minimal mhm
   JOIN matches_1v1_clean m1v1 ON mhm.match_id = 'aoestats::' || m1v1.game_id
   GROUP BY m1v1.patch, mhm.faction
   HAVING COUNT(*) >= 100
   ORDER BY m1v1.patch, mhm.faction;
   ```
5. Compute patch-to-patch Δwin_rate per civ; flag |Δ| ≥ 5pp.
6. Emit `patch_civ_win_rates.csv` (one row per `(patch, civ)`), `patch_transitions_flagged.csv` (Δ flags), `01_05_03_patch_regime_summary.{json,md}`.
7. `[PRE-canonical_slot]` tagging: `faction` values in `mhm` come from the UNION-ALL mirror (both halves). Aggregate win rates are symmetric → NO tag needed for the aggregate. Per-slot (p0_civ vs p1_civ) breakdowns, if produced, carry the tag. T04's primary output is aggregate.

**Verification:**
- `patch_map.csv` has 19 rows.
- `patch_civ_win_rates.csv` non-empty; every (patch, civ) pair with N >= 100 present.
- MD artifact contains the honest statement verbatim: *"`regime_id ≡ calendar quarter`. Cross-dataset stratification by `regime_id` IS stratification by time, identical to the Q1 grain. It provides no additional variance reduction beyond Q1."*
- MD artifact labels all within-aoestats outputs `[WITHIN-AOESTATS-SECONDARY; NOT CROSS-DATASET]`.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_03_stratification_patch_regime.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_map.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_civ_win_rates.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_transitions_flagged.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_patch_regime_summary.{json,md}`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.json` (T02)

---

### T05 — Triple survivorship: unconditional + sensitivity + conditional-label captioning (Q4, spec §6)

**Objective:** Produce all three spec-§6 survivorship analyses: (6.1) unconditional `fraction_active` per quarter (all players with ≥1 match in overlap window); (6.2) sensitivity N ∈ {5, 10, 20} minimum-match cohorts with active-span ≥ 30 days, with Q2 PSI rerun for each N; (6.3) conditional-label captioning on all Q2/Q5 drift artifacts (applied in T03/T05 MD outputs).

**Hypothesis:** `# Hypothesis: fraction_active decays approximately exponentially from 2022-Q3 onward, with < 30% of 2022-Q3 ever-active players still active in 2024-Q4 (exponential churn consistent with 90-day sliding window).`  `# Falsifier: fraction_active > 60% in 2024-Q4 (no meaningful churn) OR < 5% (cohort collapse) — both would invalidate the cohort N=10 default.`

**Instructions:**
1. Create helper `src/rts_predict/games/aoe2/datasets/aoestats/analysis/survivorship.py`:
   - `compute_fraction_active(db, overlap_start, overlap_end, quarters) -> pd.DataFrame` — per-quarter fraction of ever-seen players who played in that quarter.
   - `compute_n_match_cohort(db, ref_start, ref_end, n_min, span_days_min) -> list[int]` — returns profile_ids with ≥ N matches and active span ≥ span_days_min.
2. Unconditional SQL:
   ```sql
   WITH ever_seen AS (
     SELECT DISTINCT player_id
     FROM matches_history_minimal
     WHERE started_at BETWEEN '2022-07-01' AND '2024-12-31'
   ),
   quarterly_active AS (
     SELECT DATE_TRUNC('quarter', started_at) AS qtr,
            COUNT(DISTINCT player_id) AS n_active
     FROM matches_history_minimal
     WHERE started_at BETWEEN '2022-07-01' AND '2024-12-31'
     GROUP BY 1
   )
   SELECT qa.qtr,
          qa.n_active,
          (SELECT COUNT(*) FROM ever_seen) AS n_ever_seen,
          qa.n_active * 1.0 / (SELECT COUNT(*) FROM ever_seen) AS fraction_active
   FROM quarterly_active qa
   ORDER BY qa.qtr;
   ```
3. 90-day sliding-window churn:
   ```sql
   WITH last_match_per_player AS (
     SELECT player_id, MAX(started_at) AS last_match
     FROM matches_history_minimal
     WHERE started_at <= '2024-12-31'
     GROUP BY player_id
   )
   SELECT DATE_TRUNC('quarter', DATE '2022-07-01' + INTERVAL (gs.n * 3) MONTH) AS qtr,
          COUNT(*) FILTER (WHERE last_match < qtr - INTERVAL '90 days') AS churned,
          COUNT(*) AS total
   FROM GENERATE_SERIES(0, 9) AS gs(n)
   CROSS JOIN last_match_per_player;
   ```
4. Sensitivity N ∈ {5, 10, 20}: compute cohort via `compute_n_match_cohort` with `active_span_days >= 30`, then rerun PSI for each N (reuses T03's `psi.py` module). Emit delta summary: `PSI_feature_N=5` − `PSI_feature_N=20`.
5. Captioning: all MD artifacts in T03 and T05 include the literal caption `*(conditional on ≥10 matches in reference period; see §6 for sensitivity)*` below every Q2/Q5 table/figure (spec §6.3).

**Verification:**
- `survivorship_unconditional.csv` has 10 rows (quarters), `fraction_active` ∈ (0, 1] strictly.
- `survivorship_sensitivity.csv` has 8 quarters × 3 N-values × 8 features = 192 rows (or 189 — accept 8 × 3 × n_valid_features if some features dropped).
- MD artifacts in T03 and T05 contain the `(conditional on ≥10 matches in reference period; ...)` caption at least once.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_triple.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/analysis/survivorship.py`
- `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_survivorship.py`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_summary.{json,md}`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.json` (T03 — for reference edges; sensitivity reuses them)

---

### T06 — Between/within variance decomposition ICC via `statsmodels.mixedlm` (Q6, spec §8)

**Objective:** Fit random-intercept LMM `won ~ 1 + (1 | player_id)` on the reference cohort (N ≥ 10 matches in reference period); compute ICC point estimate + 95% CI via delta method (Gelman & Hill 2007 §12.5). Secondary decomposition: player × faction interaction. Minimum cluster size 10 obs/player (spec §8).

**Hypothesis:** `# Hypothesis: Player-level variance explains > 15% of total variance in won (ICC >= 0.15), consistent with the presence of meaningful skill signal for per-player prediction.`  `# Falsifier: ICC < 0.05 (player identity explains almost nothing) — would undermine the per-player prediction paradigm.`

**Instructions:**
1. Create `src/rts_predict/games/aoe2/datasets/aoestats/analysis/variance_decomposition.py`:
   - `fit_random_intercept_lmm(df: pd.DataFrame, target: str, group: str) -> statsmodels.MixedLMResults`
   - `compute_icc(result, ci_level: float = 0.95) -> tuple[float, float, float]` — returns `(icc, ci_lo, ci_hi)` via delta method.
   - Ship default `RANDOM_SEED = 42` from `rts_predict.common.config` for reproducibility.
2. Load reference cohort data (reuse T03's cohort):
   ```sql
   WITH cohort AS (
     SELECT player_id FROM matches_history_minimal
     WHERE started_at BETWEEN '2022-08-29' AND '2022-10-27'
     GROUP BY player_id HAVING COUNT(*) >= 10
   )
   SELECT mhm.player_id, mhm.faction, mhm.won, m1v1.p0_old_rating
   FROM matches_history_minimal mhm
   JOIN matches_1v1_clean m1v1 ON mhm.match_id = 'aoestats::' || m1v1.game_id
   JOIN cohort c ON mhm.player_id = c.player_id
   WHERE mhm.started_at BETWEEN '2022-08-29' AND '2022-10-27'
     AND m1v1.patch = 125283;
   ```
3. If row count > 5M, take a stratified reservoir sample (50,000 unique players) using `np.random.default_rng(42).choice(...)` before fit; document sampling in MD artifact.
4. Fit primary: `mixedlm("won ~ 1", data=df, groups=df["player_id"]).fit(method="lbfgs")`.
5. Compute ICC = var(player_random_intercept) / (var(player_random_intercept) + var(residual)). CI via delta method (see `sjstats::icc` R reference; Python implementation handles via Taylor expansion around logit-ICC).
6. Secondary: player × faction interaction. Fit `won ~ faction + (1 | player_id) + (1 | player_id:faction)` if converges; else fall back to `won ~ faction + (1 | player_id)` and report the variance component ratio.
7. Emit JSON with: point estimate, CI, sample_size, method, convergence_warnings, residual_variance, random_effect_variance.
8. Secondary continuous target `rating_pre` per spec §8: skipped if rating is NULL > 20%. Verify `p0_old_rating` NULL rate in cohort; if ≤ 20%, also fit `p0_old_rating ~ 1 + (1 | player_id)` and report ICC for rating.

**Verification:**
- `01_05_05_icc_results.json` contains keys `icc_point`, `icc_ci_lo`, `icc_ci_hi`, `n_obs`, `n_groups`, `method`.
- `n_groups >= 10,000` (cohort size sanity).
- ICC point ∈ [0, 1]; CI lo ≤ point ≤ CI hi.
- Notebook prints `Q6 skill-signal hypothesis: <PASSED|FALSIFIED>`.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_05_variance_decomposition_icc.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/analysis/variance_decomposition.py`
- `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_variance_decomposition.py`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.{json,md}`

**Read scope:**
- (none beyond DuckDB)

---

### T07 — `temporal_leakage_audit_v1` with aoestats-specific Query 4 (Q7, spec §9)

**Objective:** Hard-gate temporal-leakage audit. Four queries: (Q1) future-data check (gate = 0 rows, blocks on violation); (Q2) POST_GAME/TARGET token scan of T03's feature-input list; (Q3) normalization-fit-window assertion; (Q4 aoestats-specific) `canonical_slot` readiness probe — absent → emit `[PRE-canonical_slot]` warning, do not block.

**Hypothesis:** `# Hypothesis: All four queries pass at their respective gates. Query 1 returns 0 future-rows. Query 2 finds 0 POST_GAME/TARGET tokens in the T03 feature-input list. Query 3 assertion holds. Query 4 returns 0 rows (canonical_slot absent) — expected outcome, triggers [PRE-canonical_slot] propagation.`  `# Falsifier for Q1/Q2/Q3: any violation — BLOCKS 01_05 completion.`  `# Falsifier for Q4: if canonical_slot column IS present, re-evaluate spec §9/§11 — notify parent agent.`

**Instructions:**
1. Q7.1 future-data check:
   ```sql
   -- For aoestats, feature_source = matches_history_minimal; observation_time = started_at; match_time = started_at.
   -- Leakage would appear if any ph.started_at >= mhm.started_at in a per-player feature-window JOIN.
   -- 01_05 does not yet materialise per-player windows; this is a schema-level probe.
   SELECT COUNT(*) AS future_leak_count
   FROM matches_history_minimal a
   JOIN matches_history_minimal b
     ON a.player_id = b.player_id
     AND a.match_id <> b.match_id
     AND b.started_at >= a.started_at
     AND b.match_id IN (
       -- placeholder: any feature-source materialised by 01_05 — currently empty set.
       SELECT match_id FROM matches_history_minimal WHERE 1=0
     );
   ```
   Expected: 0 rows (01_05 materialises no per-player feature windows; gate passes vacuously).
2. Q7.2 POST_GAME token scan: parse `01_05_02_psi_summary.json`'s `feature_list` field. For each token, check against the POST_GAME_HISTORICAL/TARGET label in the relevant schema YAML (`matches_history_minimal.yaml` + `matches_1v1_clean.yaml`). Assert zero POST_GAME_HISTORICAL and zero TARGET in the list.
   - Expected POST_GAME_HISTORICAL: `duration_seconds`, `is_duration_suspicious`, `p0_winner`, `p1_winner`.
   - Expected TARGET: `won`, `team1_wins`.
   - If any appears in T03's list → BLOCK.
3. Q7.3 normalization-fit-window assertion (embedded in notebook cell; Python-level):
   ```python
   from datetime import date
   assert ref_start == date(2022, 8, 29), f"Bad aoestats ref_start: {ref_start}"
   assert ref_end == date(2022, 10, 27), f"Bad aoestats ref_end: {ref_end}"
   # Additional aoestats single-patch gate:
   assert ref_patch == 125283, f"Bad aoestats ref_patch: {ref_patch}"
   ```
4. Q7.4 aoestats-specific canonical_slot readiness:
   ```sql
   SELECT column_name
   FROM information_schema.columns
   WHERE table_name = 'matches_history_minimal'
     AND column_name = 'canonical_slot';
   ```
   - Expected: 0 rows. If 0 rows → log `canonical_slot_ready = False`, emit `[PRE-canonical_slot]` warning, **do not block** per spec §9. If ≥ 1 row → log `canonical_slot_ready = True` and immediately notify parent agent (spec §9/§11 locked per W3 commit `ab23ab1d`; a different verdict requires §14 amendment procedure).
5. Emit `01_05_06_temporal_leakage_audit_v1.{json,md}` with:
   - `query1_future_leak_count`
   - `query2_post_game_tokens_found` (list)
   - `query3_assertion_passed` (bool)
   - `query4_canonical_slot_ready` (bool)
   - `pre_canonical_slot_flag_active` (bool; mirrors Q4 result negated)
   - `verdict`: one of `PASS`, `BLOCKED_FUTURE_LEAK`, `BLOCKED_POST_GAME_TOKEN`, `BLOCKED_REF_WINDOW_MISMATCH`.

**Verification:**
- `artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.json` exists.
- Every PSI CSV from T03 references in its notes column the `pre_canonical_slot_flag_active` value from this audit.
- Notebook final cell prints `Q7 audit verdict: <PASS|BLOCKED_*>`. If any BLOCKED_*, plan gate fails.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.{json,md}`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.json` (T03)
- `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_history_minimal.yaml`
- `src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_1v1_clean.yaml`

---

### T08 — POST_GAME DGP diagnostics: `duration_seconds` (Q8, spec §10)

**Objective:** Compute DGP diagnostics for `duration_seconds` per quarter (reference + 2023-Q1..2024-Q4): summary stats (mean, median, p5, p95, IQR); Cohen's d vs reference; corruption flag rate (`is_duration_suspicious`). Output filenames use the `dgp_diagnostic_` prefix (spec §10). POST_GAME features MUST NOT appear in Q2 PSI files (already enforced in T03).

**Hypothesis:** `# Hypothesis: duration_seconds mean drifts < 5% between reference and any tested quarter; corruption rate (is_duration_suspicious=TRUE) remains < 0.001% per quarter (matches 01_04_02 finding of 28/17.8M ≈ 0.00016% total).`  `# Falsifier: Any quarter shows corruption rate > 0.01% OR mean drift > 10% — would indicate a secular DGP shift worth flagging to Phase 02.`

**Instructions:**
1. Per-quarter duration diagnostics SQL:
   ```sql
   SELECT
     DATE_TRUNC('quarter', started_at) AS quarter_start,
     COUNT(*) AS n_rows,
     AVG(duration_seconds) AS mean_duration,
     MEDIAN(duration_seconds) AS median_duration,
     QUANTILE_CONT(duration_seconds, 0.05) AS p5_duration,
     QUANTILE_CONT(duration_seconds, 0.95) AS p95_duration,
     QUANTILE_CONT(duration_seconds, 0.75) - QUANTILE_CONT(duration_seconds, 0.25) AS iqr_duration,
     COUNT(*) FILTER (WHERE duration_seconds > 86400) AS corrupt_count,
     COUNT(*) FILTER (WHERE duration_seconds > 86400) * 1.0 / COUNT(*) AS corrupt_rate
   FROM matches_history_minimal
   WHERE started_at BETWEEN '2022-07-01' AND '2024-12-31'
   GROUP BY 1
   ORDER BY 1;
   ```
2. Cohen's d: `d = (mean_tested - mean_ref) / pooled_sd`. Compute from per-quarter stats and reference-window stats; pooled SD via `sqrt((var_ref + var_tested) / 2)`.
3. To avoid the 28 corrupted rows dominating means, compute a **second** set of stats with filter `WHERE NOT is_duration_suspicious` and report both; notes column says which filter applied.
4. For each quarter Q, emit `dgp_diagnostic_aoestats_{Q}.csv` per spec §10 naming. Columns: `quarter, feature_name, mean, median, p5, p95, iqr, cohen_d_vs_ref, corrupt_count, corrupt_rate, notes`.

**Verification:**
- 8 `dgp_diagnostic_aoestats_2023-QX.csv` files (+ 1 for reference period).
- JSON aggregate `01_05_07_dgp_diagnostic_summary.json` lists `cohen_d_vs_ref` values per quarter.
- `grep -l duration_seconds artifacts/.../psi_aoestats_*.csv` returns empty (POST_GAME not in PSI files — I3 invariant).

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostics_duration.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2022-Q3Q4ref.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2023-Q1.csv` ... `dgp_diagnostic_aoestats_2024-Q4.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostic_summary.{json,md}`

**Read scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.json` (T02)

---

### T09 — Phase 06 interface CSV per spec §12

**Objective:** Aggregate all per-quarter metrics from T02, T03, T05, T06, T08 into a flat schema (one row per `dataset × quarter × feature × metric`) and emit as single CSV. Every row for `feature_name ∈ {faction, opponent_faction}` or any per-slot-breakdown row carries `[PRE-canonical_slot]` in the notes column; aggregate rows over both UNION-ALL halves do not.

**Hypothesis:** `# Hypothesis: The emitted CSV validates against the §12 schema: 9 columns, metric_value to 4 decimal places, reference_window_id = '2022-Q3-patch125283' for all rows, at least 64 rows (8 quarters × 8 features × >= 1 metric).`  `# Falsifier: Any missing column, any metric_value with > 4 or < 4 decimal places, any NULL-as-string 'NaN'.`

**Instructions:**
1. Read T03 PSI outputs (8 CSVs), T06 ICC results, T08 DGP diagnostic outputs.
2. Assemble per spec §12 schema. Use `reference_window_id = "2022-Q3-patch125283"` (aoestats single-patch reference per §7).
3. Columns (exact order per §12):
   - `dataset_tag` (constant `"aoestats"`)
   - `quarter` (ISO `YYYY-QN`)
   - `feature_name`
   - `metric_name` (one of: `psi`, `cohen_h`, `cohen_d`, `ks_stat`, `icc`)
   - `metric_value` (DOUBLE, 4 decimals; use `NULL` not string `"NaN"`)
   - `reference_window_id` (constant `"2022-Q3-patch125283"`)
   - `cohort_threshold` (INTEGER, default 10 for default rows, 5/20 for sensitivity)
   - `sample_size` (INTEGER, n obs for this cell)
   - `notes` (free-text; for any row where `feature_name ∈ {faction, opponent_faction}` OR the metric was computed on a per-slot breakdown, append `[PRE-canonical_slot]`; also record `__unseen__: N` for categorical PSI cells where applicable)
4. Emit `phase06_interface_aoestats.csv`.
5. Emit accompanying `01_05_08_phase06_interface_schema_validation.json` with verification checks: column count == 9, `dataset_tag` == `"aoestats"` on every row, all `metric_value` NaN → NULL, all `reference_window_id` == `"2022-Q3-patch125283"`.

**Verification:**
- `phase06_interface_aoestats.csv` exists with 9 columns exactly.
- `head -1 phase06_interface_aoestats.csv` equals: `dataset_tag,quarter,feature_name,metric_name,metric_value,reference_window_id,cohort_threshold,sample_size,notes`.
- `awk -F, 'NR>1 && $6 != "2022-Q3-patch125283"' phase06_interface_aoestats.csv` returns empty (ignoring header).
- For every row where `feature_name` contains `faction` or `civ` in a per-slot decomposition, `notes` contains `[PRE-canonical_slot]`.

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface.{py,ipynb}`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface_schema_validation.{json,md}`

**Read scope:**
- All T03 PSI CSVs (8 files)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.json` (T06)
- All T08 DGP diagnostic CSVs (9 files)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.json` (T07 — for `pre_canonical_slot_flag_active`)

---

### T10 — Research log + INVARIANTS §4 + STEP_STATUS/PIPELINE_SECTION/PHASE + ROADMAP + Decision-Gate memo + F1 unblocker reference

**Objective:** Close the 01_05 Pipeline Section. Update every derivative status file (STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS — cascade per the derivation chain), insert ROADMAP Step rows `01_05_01`..`01_05_09`, update `INVARIANTS.md` §4 with 01_05 empirical findings, append a per-dataset research log entry, and produce `01_05_09_gate_memo.md` that explicitly names BACKLOG F1 (`canonical_slot`) as the Phase 02 unblocker.

**Instructions:**
1. Populate `ROADMAP.md` Steps `01_05_01`..`01_05_09` using `docs/templates/step_template.yaml` (each Step = one notebook; Step names are descriptive human-readable — NO T-codes per user memory `feedback_no_plan_codes_in_docs.md`). Examples: `"Quarterly Grain and Overlap Window"`, `"PSI with Frozen Reference Edges"`, `"Stratification and Patch Regime"`, `"Triple Survivorship Analysis"`, `"Variance Decomposition (ICC)"`, `"Temporal Leakage Audit v1"`, `"Duration DGP Diagnostics"`, `"Phase 06 Interface Emission"`, `"01_05 Decision Gate Memo"`.
2. Update `STEP_STATUS.yaml`: add 9 new Step entries under `pipeline_section: "01_05"`, each with `status: complete` and `completed_at: "2026-04-18"` (executor fills exact date).
3. Update `PIPELINE_SECTION_STATUS.yaml`: set `01_05.status: complete`.
4. Update `PHASE_STATUS.yaml`: Phase 01 remains `in_progress` (01_06 Decision Gate still not_started); do NOT tick to `complete`.
5. Append research log entry at `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` with heading `## 2026-04-18 — [Phase 01 / Pipeline Section 01_05] Temporal & Panel EDA`. Include: spec binding SHA, per-task verdict (Falsifier outcomes), key PSI results, ICC point + CI, `canonical_slot` readiness = False (expected), reference window used (2022-08-29..2022-10-27 patch 125283), explicit `[PRE-canonical_slot]` flag status across outputs. Cross-reference the CROSS entry in `reports/research_log.md` if any cross-dataset coordination occurred (current expectation: none; 01_05 is per-dataset scope).
6. Update `src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md` §4 "Per-dataset empirical findings" with a new subsection `### 01_05 findings (2026-04-18)`. Summarise: PSI rating-drift > 0.10 threshold breach in N quarters, ICC point estimate, duration corruption rate stable across quarters, `canonical_slot` flag status. Keep I5 status `PARTIAL — asymmetry characterised` unchanged (only F1 can transition it to HOLDS).
7. Produce `01_05_09_gate_memo.md` (Decision Gate preparation for 01_06). Memo must:
   - Explicitly name BACKLOG item **F1 (`canonical_slot`) as the primary unblocker for aoestats Phase 02**, with citation to `planning/BACKLOG.md` F1 block.
   - Acknowledge that the 19-patch regime extends to 2026-02-06 (2-year extension beyond the cross-dataset window) and is within-dataset secondary only per spec §5.
   - Document the patch-anchored reference asymmetry (9 weeks vs. 4 months sc2egset/aoec) as spec-locked per §7 / §14.
   - List every artifact produced; link to research log anchor.
   - Recommend 01_06 decision: either adopt F1 now (preferred) OR proceed with `[PRE-canonical_slot]`-tagged Phase 02 features and amend post-hoc.
8. CHANGELOG entry under `[Unreleased] → Added`: `aoestats Pipeline Section 01_05 Temporal & Panel EDA (9 steps; spec v1.0.1 SHA 7e259dd8)`.

**Verification:**
- `grep -c "01_05_0[1-9]" src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` returns 9.
- `grep -A1 "01_05" src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml` shows `status: complete`.
- `grep "canonical_slot" src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md` matches the F1 reference.
- Research log entry references every artifact filename produced in T02–T09.
- `head -200 src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md` shows the new `### 01_05 findings` subsection under §4.

**File scope:**
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` (append 9 Steps)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` (append 9 rows)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml` (01_05 → complete)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/PHASE_STATUS.yaml` (no change; verify 01 still `in_progress`)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md` (append §4 subsection)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` (append entry)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md`
- `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.{py,ipynb}`
- `CHANGELOG.md`

**Read scope:**
- All T02–T09 outputs (CSVs, JSONs, MDs) for the research log + memo to reference.

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_02_psi_pre_game_features.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_02_psi_pre_game_features.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_03_stratification_patch_regime.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_03_stratification_patch_regime.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_triple.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_triple.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_05_variance_decomposition_icc.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_05_variance_decomposition_icc.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostics_duration.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostics_duration.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface.ipynb` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.py` | Create |
| `sandbox/aoe2/aoestats/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.ipynb` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/analysis/__init__.py` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/analysis/psi.py` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/analysis/survivorship.py` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/analysis/variance_decomposition.py` | Create |
| `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/__init__.py` | Create |
| `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_psi.py` | Create |
| `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_survivorship.py` | Create |
| `tests/rts_predict/games/aoe2/datasets/aoestats/analysis/test_variance_decomposition.py` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/.gitkeep` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_grain_row_counts.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/plots/quarterly_row_counts.png` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2023-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2023-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2023-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2023-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2024-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2024-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2024-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_aoestats_2024-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_02_psi_summary.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_map.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_civ_win_rates.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/patch_transitions_flagged.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_patch_regime_summary.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_03_patch_regime_summary.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_summary.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_04_survivorship_summary.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2022-Q3Q4ref.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2023-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2023-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2023-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2023-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2024-Q1.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2024-Q2.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2024-Q3.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_aoestats_2024-Q4.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostic_summary.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_07_dgp_diagnostic_summary.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface_schema_validation.json` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_08_phase06_interface_schema_validation.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_09_gate_memo.md` | Create |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md` | Update |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md` | Update |
| `CHANGELOG.md` | Update |

## Gate Condition

All conditions are binary and observable after T10 execution:

- [ ] `source .venv/bin/activate && poetry run python scripts/check_01_05_binding.py --all` exits 0 over all 9 aoestats 01_05 notebooks.
- [ ] All 9 sandbox `.py` and 9 `.ipynb` files exist and are jupytext-paired.
- [ ] 8 `psi_aoestats_YYYY-QN.csv` files exist (1 per tested quarter 2023-Q1..2024-Q4); POST_GAME_HISTORICAL and TARGET tokens ABSENT from every PSI CSV (grep `-l duration_seconds\|is_duration_suspicious\|p0_winner\|p1_winner\|won\|team1_wins` against PSI files returns empty).
- [ ] 9 `dgp_diagnostic_aoestats_*.csv` files exist (1 reference + 8 tested quarters).
- [ ] `01_05_06_temporal_leakage_audit_v1.json` shows `verdict: PASS`, `query4_canonical_slot_ready: false`, `pre_canonical_slot_flag_active: true`.
- [ ] `phase06_interface_aoestats.csv` has exactly 9 columns matching spec §12 schema; `reference_window_id` column values all equal `"2022-Q3-patch125283"`; every row with feature_name referencing `faction`/`opponent_faction` carries `[PRE-canonical_slot]` in the `notes` column.
- [ ] `01_05_05_icc_results.json` contains `icc_point`, `icc_ci_lo`, `icc_ci_hi` — all in `[0, 1]`; `n_groups >= 10,000`.
- [ ] `STEP_STATUS.yaml` has 9 new entries `01_05_01..01_05_09`, all `status: complete`.
- [ ] `PIPELINE_SECTION_STATUS.yaml` shows `01_05.status: complete`.
- [ ] `PHASE_STATUS.yaml` shows Phase 01 `status: in_progress` (NOT complete — 01_06 Decision Gate remains).
- [ ] `research_log.md` has a new 2026-04-18 entry under `## 2026-04-18 — [Phase 01 / Pipeline Section 01_05] Temporal & Panel EDA` referencing every emitted artifact.
- [ ] `INVARIANTS.md` §4 has the new `### 01_05 findings` subsection.
- [ ] `01_05_09_gate_memo.md` contains a literal sentence naming BACKLOG F1 as the Phase 02 unblocker.
- [ ] `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/aoe2/datasets/aoestats/analysis/ -v` passes with 100% of new tests green.
- [ ] `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/aoe2/datasets/aoestats/analysis/ tests/rts_predict/games/aoe2/datasets/aoestats/analysis/` exits 0.
- [ ] `source .venv/bin/activate && poetry run mypy src/rts_predict/games/aoe2/datasets/aoestats/analysis/` exits 0.
- [ ] All `team`-conditioned outputs in `phase06_interface_aoestats.csv` and any per-slot breakdown CSVs carry `[PRE-canonical_slot]` in the notes column.

## Out of scope

- **F1 — `canonical_slot` derivation** (BACKLOG planning/BACKLOG.md F1): explicitly deferred. 01_05 emits `[PRE-canonical_slot]`-tagged outputs per spec §9/§11 and proceeds. F1 (choice between `old_rating` vs. `profile_id` derivation, schema amendment, spec v1.1.0 bump) is a separate PR after 01_05 closes.
- **F3 — Thesis §4.2.2 revision**: F3 is blocked on F2 (all three datasets' 01_05). This plan addresses the aoestats slice only.
- **Phase 01_06 Decision Gate execution**: this plan prepares the Gate memo (T10) but does not execute 01_06 itself. That is a separate Pipeline Section with its own plan.
- **Cross-dataset coordination**: sc2egset and aoec 01_05 are separate PRs (`feat/01-05-sc2egset`, `feat/01-05-aoe2companion`) per BACKLOG F2. Any CROSS research_log entries for cross-dataset comparisons happen after all three land.
- **ADF/KPSS within-dataset extended window**: spec §3 permits aoec-only secondary ADF; aoestats has no equivalent permission. Not executed.
- **Schema amendment to `matches_1v1_clean.yaml` / `players_raw.yaml` for `team` API-ordering note**: the 01_04_05 artifact names this as `schema_amendment_required: true` but it is separately tracked (unblocks F1, not 01_05). Not executed here.
- **Identifying the 28 duration-corrupted matches as a class of DGP failure**: 01_04_02 addendum already did this; T08 reports the rate per quarter but does not re-investigate.
- **Modifying the pre-commit hook `check_01_05_binding.py`**: already exists and works; no changes.
- **Formal temporal leakage test for `p0_old_rating` / `p1_old_rating` being PRE-GAME**: deferred to Phase 02 per `INVARIANTS.md` §3 "old_rating is PRE-GAME by schema inference". T07 confirms schema-level absence from POST_GAME list; formal bivariate test is Phase 02 work.

## Open questions

- **Reference-asymmetry defensibility in Chapter 4** — spec §7 locks the 9-week single-patch aoestats reference while sc2egset and aoec use 4 months. The asymmetry is thesis-defensible (homogeneity > length), but Chapter 4 prose must address it explicitly. Resolves by: F3 authoring session (thesis writer) after F2 lands across all three datasets.
- **F1 timing choice** — whether to block 01_06 Decision Gate on F1 (clean outputs) or proceed with `[PRE-canonical_slot]` tags. Resolves by: 01_06 plan decision; `01_05_09_gate_memo.md` recommends F1 first.
- **19-patch secondary regime extension to 2026-02-06** — aoestats coverage extends beyond the 2024-Q4 cross-dataset boundary by ~14 months, giving extra patches for within-dataset heterogeneity analysis. Spec §5 authorises this as within-dataset secondary only. Resolves by: T04 executor tagging all post-2024-Q4 patch rows `[WITHIN-AOESTATS-SECONDARY; NOT CROSS-DATASET]`; no methodology change.
- **`mixedlm` convergence on 3.5M-row reference cohort** — `statsmodels.mixedlm` may fail to converge on a 641k-group random-intercept fit. Fallback: stratified reservoir to 50,000 unique players with `RANDOM_SEED = 42`. Resolves by: T06 executor during execution.
- **Whether the 28 corrupted duration rows should be excluded from PSI/Q5 of non-duration features** — currently retained per spec default. Resolves by: T03/T05 executor; if any non-duration PSI is visibly dominated by corrupt rows, emit a sensitivity row with corruption filter applied.
- **Phase 06 interface row count** — spec §12 does not fix a row count. T09 produces whatever rows emerge from T02/T03/T05/T06/T08; validation is schema-shape, not count. Resolves by: T09 schema validation JSON.

---

## Critique instruction (Category A)

For Category A or F, adversarial critique is required before execution. Dispatch `reviewer-adversarial` to produce `planning/current_plan.critique.md` against this plan and the spec commit `7e259dd8`. The critique should specifically probe:

1. Whether the reference-window JOIN `matches_history_minimal` ↔ `matches_1v1_clean` introduces selection bias (both are derived from the same 1v1 `matches_raw` base — no bias expected, but assert).
2. Whether `compute_decile_edges` handles ties gracefully when feature values are highly repeated (e.g., `mirror` is BOOLEAN with only 2 values — PSI decile binning is degenerate).
3. Whether `mixedlm` convergence fallback to a 50k-player sample introduces inferential risk versus full fit.
4. Whether the `[PRE-canonical_slot]` tagging rule correctly identifies aggregate vs. per-slot rows.
5. Whether Query 7.1 future-leakage probe is meaningful at 01_05 stage (no feature-windows yet materialised) or if it should be rewritten.
6. Whether the gate memo's F1-unblocker recommendation properly respects that F1 may not land before 01_06.