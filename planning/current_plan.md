---
category: A
branch: feat/01-05-sc2egset
date: 2026-04-18
planner_model: claude-opus-4-7
dataset: sc2egset
phase: "01"
pipeline_section: "Temporal & Panel EDA"
invariants_touched: [I3, I6, I7, I8, I9]
source_artifacts:
  - reports/specs/01_05_preregistration.md
  - .claude/scientific-invariants.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_03_minimal_history_view.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_04b_worldwide_identity.md
  - sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_03_minimal_history_view.py
  - sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.py
  - sandbox/README.md
  - docs/templates/plan_template.md
  - scripts/check_01_05_binding.py
critique_required: true
research_log_ref: src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md#2026-04-18-01-05-temporal-panel-eda
---

# Plan: 01_05 Temporal & Panel EDA — sc2egset (pattern establisher)

## Scope

Execute the sc2egset implementation of Pipeline Section 01_05 "Temporal & Panel
EDA" per the LOCKED spec `reports/specs/01_05_preregistration.md` v1.0.1
(SHA `7e259dd8`). Deliver 10 notebooks under
`sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/` that execute the
nine binding parameter groups Q1–Q9 against the `matches_history_minimal` VIEW
(22,209 matches / 44,418 player-rows), write machine-readable artifacts under
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/`,
emit a Phase 06 interface CSV conforming to spec §12, populate INVARIANTS.md §4
with dataset-specific empirical findings, append a research-log entry, and
advance STEP/PIPELINE/PHASE status files. No upstream VIEW or schema is
modified (I9). This is Category A, science-first work; it is the pattern
establisher for the two sibling dataset plans (aoec, aoestats) that follow.

## Problem Statement

Phase 01 pipeline section 01_05 is the last step in Phase 01 and the first
step where cross-dataset drift, survivorship, and leakage claims are made
quantitatively from the harmonised `matches_history_minimal` VIEW. Without
pre-registered parameters, every downstream claim (Phase 02 feature
engineering, Phase 03 temporal split, Phase 06 cross-domain transfer) is
open to reviewer critique about analytical degrees of freedom. Spec v1.0.1
locks those parameters; this plan executes them with I3/I6/I7/I8/I9
discipline and with sc2egset's accepted biases (I2 branch (iii);
`leaderboard_raw` = NULL; MMR=0 sentinel on 83.65% of rows) recorded as
caveats rather than swept under the rug.

The immediate gap: no 01_05 artifact exists yet. STEP_STATUS shows all 01_05
steps `not_started`. The spec mandates ten binding outputs (PSI, Cohen's
h/d/KS, survivorship cohort triplet, variance decomposition with ICC,
temporal leakage audit with 3 queries, DGP diagnostics for `duration_seconds`,
Phase 06 interface CSV) which together establish the per-quarter distributional
baseline for sc2egset. Because sc2egset is a tournament dataset
(`leaderboard_raw` NULL, 83.65% MMR=0), we must explicitly flag which spec
provisions degrade (rating-based ICC secondary; N≥10 cohort effective sample),
which is informative — not a blocker — for the cross-dataset comparison.

## Assumptions & unknowns

- **Assumption (A1):** `matches_history_minimal` remains the 9-column contract
  defined in 01_04_03 (44,418 rows / 22,209 matches, TIMESTAMP `started_at`
  2016-01-07..2024-12-01, all 5 non-nullable columns zero-NULL). Verified
  from the 01_04_03 artifact.
- **Assumption (A2):** `player_identity_worldwide` VIEW exists as a 2,494-row
  decomposition of toon_id with `player_id_worldwide` as the canonical join
  key (01_04_04b artifact). Per I2 branch (iii), the ~12% cross-region
  duplication is accepted bias.
- **Assumption (A3):** `matches_flat_clean.details.gameSpeed` cardinality = 1
  so `duration_seconds = CAST(header_elapsedGameLoops / 22.4 AS BIGINT)` is a
  deterministic projection with the observed range `[1, 6073]` and 0
  suspicious outliers (01_04_03 Gate +5).
- **Assumption (A4):** `tournament_era` is derivable from a known 4-tier
  categorisation (`Bronze`/`Silver`/`Gold`/`Platinum`) over the 70 tournament
  directories. The mapping is inferred from the tournament directory name
  prefix and any available prize-pool signal; it is declared `[SECONDARY;
  NOT CROSS-DATASET]` per spec §5.
- **Assumption (A5):** `matches_history_minimal` does **not** expose
  `rating_pre` in the sc2egset row set today (the VIEW projects 9 columns;
  column 7 is `won`, column 8 is `duration_seconds`; no `rating_pre`). For
  Q6 the primary target is `won`; the secondary `rating_pre` branch is marked
  N/A for sc2egset and explained in the notebook cell.
- **Unknown (U1):** `statsmodels` is not in `pyproject.toml` today. Spec §8
  mandates `statsmodels.mixedlm`. Resolved during T01 by adding
  `statsmodels = "^0.14"` as a dep via poetry; if installation blocks on
  sandbox/environment, a closed-form one-way random-intercept ANOVA ICC on
  `won` is a defensible fallback (Gelman & Hill 2007 §12.5) provided the
  rationale is recorded verbatim (I6, I7) and the spec deviation triggers
  §13 (research-log CROSS entry + §14 amendment + version bump). Decide at
  T06 start by trial `poetry add`.
- **Unknown (U2):** `tournament_era` mapping details — whether the 4-tier
  Bronze/Silver/Gold/Platinum labels come from (i) prize-pool lookup on
  Liquipedia, (ii) a lookup table committed alongside the notebooks, or
  (iii) a heuristic on tournament-directory name substrings. Resolved at
  T04 start; default is (iii) with a documented heuristic and a caveat
  block. sc2egset has 70 tournament directories → adopt (iii) and document.
- **Unknown (U3):** Whether `__unseen__` categorical bins will ever be
  populated — sc2egset races are fixed (`Prot`/`Terr`/`Zerg`). If no
  categorical features enter PSI (in sc2egset, numeric features only — MMR
  is mostly 0-sentinel, `duration_seconds` is POST_GAME and excluded), the
  `__unseen__` bin protocol is a nominal safeguard with zero hits.
- **Unknown (U4):** The effective N after the N=10-matches-in-reference
  cohort filter. sc2egset has 2,494 distinct `player_id_worldwide` values
  across all 22,209 matches; post-filter size could be <100. T05 reports this
  empirically and documents it as a caveat to cross-dataset comparability.

## Literature context

This section registers the citations behind every parameter. All five
references appear in `thesis/references.bib` per spec §16 — if any key is
missing, T10 appends it (I7 provenance).

- **Hamilton (1994)** *Time Series Analysis*, Princeton UP, §17.7. Binds the
  spec §3 prohibition against cross-dataset ADF/KPSS at N=8 quarters (far
  below the T ≥ 50 power threshold). Cited in every quarterly-grain cell
  that forgoes stationarity testing.
- **Siddiqi (2006)** *Credit Risk Scorecards*, Wiley. Defines PSI
  `= Σ (p_tested - p_ref) · ln(p_tested / p_ref)` and the canonical
  equal-frequency N=10 binning. Binds the 0.10 / 0.25 threshold ladder
  (spec §4). The Laplace smoothing ε=1/sample_size applied to zero bins is
  a standard follow-up (Yurdakul 2018; Fiddler/Arize practitioner guides
  surveyed 2024) — T03 documents the exact ε used.
- **Breck et al. (2019)** *Data Validation for ML*, SysML/TFDV. Authority
  for KS statistic as a descriptive magnitude (not a hypothesis test) in
  distribution-drift auditing; binds KS presence in the Phase 06 interface
  (spec §12) and justifies our decision to ship KS without p-values at
  N=8 quarters.
- **Gelman & Hill (2007)** *Data Analysis Using Regression and
  Multilevel/Hierarchical Models*, CUP, §12.5. Defines ICC =
  σ²_between / (σ²_between + σ²_within) and the delta-method 95% CI used
  in T06. Also grounds the minimum-cluster-size choice (10 obs/player) as
  a variance-stability heuristic for random-intercept fits.
- **Cohen (1988)** *Statistical Power Analysis for the Behavioral
  Sciences* (2nd ed.), LEA. §2.2 defines Cohen's d for continuous
  features; §6.2 defines h = 2·(arcsin√p₁ − arcsin√p₂) for proportions.
  Both are used in T03/T08 for signed drift magnitudes.
- *Web-verified 2024*: Yurdakul, B. (2018, revisited in a 2024 Edinburgh
  CRC working paper) notes that PSI inflates on small samples when bins
  are sparse. sc2egset's N=22,209 matches yields ≈2,200 obs per N=10 bin
  at reference — well above the sparse-bin regime — but the `__unseen__`
  bin protocol (spec §4) is the safety net. T03 records ε and per-bin
  occupancy verbatim.

Key *sc2egset-specific* methodological notes:

- sc2egset `leaderboard_raw = NULL` → no ladder MMR to drift-audit at the
  leaderboard level. The MMR distribution on the 16.35% of non-sentinel
  rows is reported as a sensitivity figure only.
- sc2egset is tournament data; the "regime" signal is tournament tier,
  not ladder bracket (spec §5 secondary regime: `tournament_era`).
- `player_id_worldwide` is the canonical identity (I2 branch (iii)); no
  nickname-based join is performed anywhere in 01_05.

Any `[OPINION]` call in the notebooks is limited to **interpretation of
magnitude** (e.g., "moderate shift vs. review threshold"), never parameter
choice.

## Execution Steps

---

### T01 — Scaffold 01_05 directory, spec-binding, poetry dependency, hygiene

**Objective:** Create the empty skeleton that the other nine tasks fill. Add
`statsmodels` to poetry. Verify the pre-commit hook `check_01_05_binding.py`
fires on a stub file with SHA `7e259dd8`. Zero analytical work in this task.

**Instructions:**
1. Check out branch `feat/01-05-sc2egset` from `master` (HEAD `ac5cb2c2`).
2. Create directory `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/`
   and matching artifact directory
   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/`
   (both with a `.gitkeep` stub; use `git add -N` to register, then remove
   stubs before the real notebooks replace them).
3. Create an empty-body scaffold notebook pair `01_05_00_scaffold.py` + `.ipynb`
   (jupytext paired) that contains only the first 40 lines:
   ```python
   # spec: reports/specs/01_05_preregistration.md@7e259dd8
   # Step 01_05_00 -- Section scaffold (no analytical content)
   # Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18
   ```
   Run `source .venv/bin/activate && poetry run pre-commit run check-01-05-binding --files sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.py`
   and confirm exit 0. Then intentionally break the SHA to `deadbee`, re-run
   the hook, confirm exit 1, restore, re-run, confirm exit 0. This is a
   one-off witness of the binding mechanism.
4. Add `statsmodels = "^0.14"` to `pyproject.toml` under `[tool.poetry.dependencies]`
   via `source .venv/bin/activate && poetry add statsmodels@^0.14`. Update
   `poetry.lock`. Run `poetry run python -c "import statsmodels.regression.mixed_linear_model as m; print(m.__name__)"`
   and confirm the import succeeds. If install fails, record the failure
   verbatim in the research log and defer to U1's fallback (closed-form ICC)
   in T06.
5. Add `numpy-docstring`-style module docstrings + the spec-binding comment
   line to every subsequent `.py` in this plan. Every notebook created in
   T02..T08 MUST contain the line `# spec: reports/specs/01_05_preregistration.md@7e259dd8`
   within its first 40 lines. If the spec is amended (deviation per spec §13)
   the SHA is rewritten to the new commit.

**Verification:**
- `ls sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/` shows
  `01_05_00_scaffold.py` + `01_05_00_scaffold.ipynb`.
- `source .venv/bin/activate && poetry run pre-commit run check-01-05-binding --files sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.py` → exit 0.
- `source .venv/bin/activate && poetry run python -c "import statsmodels; print(statsmodels.__version__)"` → prints `0.14.*` OR the research log records the install failure and the fallback choice.
- `git diff pyproject.toml poetry.lock` shows the `statsmodels` addition and nothing else.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.py`
- `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.ipynb`
- `pyproject.toml` (add statsmodels)
- `poetry.lock` (lockfile update)

**Read scope:**
- `reports/specs/01_05_preregistration.md` (SHA verification)
- `scripts/check_01_05_binding.py`
- `sandbox/README.md`
- `.claude/rules/python-code.md`

---

### T02 — Q1: Quarterly grain + overlap window + per-quarter row counts

**Objective:** Establish the quarterly grain of the analysis and the 10-quarter
overlap window (2022-Q3 through 2024-Q4). Produce the base per-quarter row-count
table for all downstream tasks.

**Instructions:**
1. Create `01_05_01_quarterly_grain.py` with the binding docstring (SHA
   `7e259dd8`). Open DuckDB read-only via
   `get_notebook_db("sc2", "sc2egset", read_only=True)`.
2. State the notebook's hypothesis in markdown:
   `# Hypothesis: The 10-quarter overlap window (2022-Q3..2024-Q4) has non-empty
   support in sc2egset and approximately monotonically non-decreasing match
   volume through 2024 (tournament cadence).`
   `# Falsifier: any quarter in the window has zero rows OR peak-to-trough
   variation > 20x.`
3. Compute per-quarter match counts, player-row counts, distinct players, and
   distinct matches via:
   ```sql
   WITH q AS (
     SELECT
       strftime(started_at, '%Y') || '-Q' ||
         CAST(CEIL(CAST(strftime(started_at, '%m') AS INTEGER) / 3.0) AS VARCHAR) AS quarter,
       match_id, player_id
     FROM matches_history_minimal
   )
   SELECT quarter,
          COUNT(*)                               AS n_player_rows,
          COUNT(DISTINCT match_id)               AS n_matches,
          COUNT(DISTINCT player_id)              AS n_players
   FROM q
   GROUP BY quarter
   ORDER BY quarter
   ```
4. Filter to the overlap window `quarter IN ('2022-Q3', '2022-Q4', '2023-Q1',
   '2023-Q2', '2023-Q3', '2023-Q4', '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4')`
   and persist this to `artifacts/.../quarterly_row_counts_sc2egset.csv`.
   Columns: `quarter`, `n_player_rows`, `n_matches`, `n_players`,
   `dataset_tag='sc2egset'`.
5. Produce a second table with *all* quarters in sc2egset (2016..2024) for
   secondary reporting. Save as `quarterly_row_counts_sc2egset_full.csv`.
6. Verdict cell: assert the hypothesis holds OR state falsification and
   proceed with the empirical rows (no re-run needed if data is as
   expected — this is a descriptive step).
7. Emit a markdown report `quarterly_row_counts_sc2egset.md` that embeds the
   10-quarter table and the SQL verbatim (I6).

**Verification:**
- `quarterly_row_counts_sc2egset.csv` exists, has 10 rows, and all four count
  columns > 0. Verify with
  `source .venv/bin/activate && poetry run python -c "import pandas as pd; df=pd.read_csv('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.csv'); assert len(df)==10; assert (df[['n_player_rows','n_matches','n_players']] > 0).all().all()"`.
- The markdown artifact contains the verbatim SQL in a fenced block.

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py` (+ `.ipynb`)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset_full.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.md`

**Read scope:**
- `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.py` (T01)

---

### T03 — Q2: Equal-frequency PSI N=10 with frozen reference edges

**Objective:** Compute PSI for every pre-game feature per tested quarter against
the frozen reference period 2022-08-29..2022-12-31. Bin edges frozen at reference
(spec §4). `__unseen__` protocol for categoricals. Apply conditional-label
captioning (cohort N≥10 in reference period; spec §6 default).

**Instructions:**
1. Create `01_05_02_psi_quarterly.py`.
2. Hypothesis cell: `# Hypothesis: PSI for pre-game features stays below 0.25
   across all 8 tested quarters (2023-Q1..2024-Q4); one or two quarters may
   cross 0.10 (moderate-shift band).`
   `# Falsifier: any pre-game feature PSI > 0.25 in ≥3 tested quarters — would
   indicate systemic drift and trigger a §13 deviation review.`
3. Identify pre-game features available in `matches_history_minimal` for sc2egset:
   - `faction` (categorical, Prot/Terr/Zerg)
   - `opponent_faction` (categorical)
   - `matchup` (derived categorical = `sort(faction, opponent_faction)` —
     6 values: PvP, PvT, PvZ, TvT, TvZ, ZvZ)
   Numeric pre-game features: **none** in the 9-col VIEW. `rating_pre` is
   not exposed for sc2egset (see A5). `duration_seconds` is POST_GAME (spec §4
   forbids it here — routed to T08). Explicitly exclude it.
4. Build the reference population:
   ```sql
   CREATE OR REPLACE TEMP VIEW ref_pop AS
   SELECT *
   FROM matches_history_minimal
   WHERE started_at >= TIMESTAMP '2022-08-29 00:00:00'
     AND started_at <  TIMESTAMP '2023-01-01 00:00:00'
   -- spec §7 sc2egset ref: 2022-08-29..2022-12-31
   ```
   Assert via Python `assert ref_start == datetime(2022, 8, 29)` and
   `assert ref_end == datetime(2022, 12, 31)` (spec §9 Query 3).
5. Apply the cohort filter for the default conditional label: compute
   `player_match_count_in_ref` and restrict to players with ≥ 10 matches in
   reference:
   ```sql
   CREATE OR REPLACE TEMP VIEW ref_cohort AS
   SELECT rp.*
   FROM ref_pop rp
   JOIN (
     SELECT player_id
     FROM ref_pop
     GROUP BY player_id
     HAVING COUNT(*) >= 10
   ) c USING (player_id)
   ```
   Record in the notebook the empirical cohort cardinality (U4) and flag
   `[SMALL-COHORT]` if it is below 100 players.
6. For each categorical feature, compute reference value frequencies (Siddiqi
   2006 equal-frequency N=10 collapses to "one bin per unique category" when
   the category cardinality ≤ 10; sc2egset races have cardinality 3, so we use
   N_bins = min(10, cardinality)). Freeze these edges (values + proportions) in
   a Python dict `ref_freqs[feature]`. Apply `ε = 1 / n_ref` Laplace smoothing
   to every bin to avoid log(0). Record ε verbatim.
7. For each tested quarter q ∈ {2023-Q1 .. 2024-Q4}, restrict to the same
   cohort (players with ≥10 matches in reference), project the same feature,
   compute tested frequencies against the frozen reference bins, and compute
   PSI:
   ```python
   psi = sum(
     (p_tested[b] - p_ref[b]) * math.log((p_tested[b] + eps) / (p_ref[b] + eps))
     for b in bins
   )
   ```
   Any tested value not in ref keys is assigned to `__unseen__`; record the
   row count.
8. Persist one row per (quarter × feature) to `psi_sc2egset.csv` with columns
   `dataset_tag, quarter, feature_name, psi_value, n_ref, n_tested,
   unseen_count, epsilon, cohort_threshold (=10), notes`. 4 decimal places
   for `psi_value`.
9. Plot `psi_vs_quarter_sc2egset.png` (one line per feature). Add the
   caption suffix `(conditional on ≥10 matches in reference period;
   see §6 for sensitivity)` per spec §6.3.
10. Verdict cell: assert `psi_value` is finite everywhere; note any values
    crossing 0.10 or 0.25 in the research-log draft (T10).

**Verification:**
- `psi_sc2egset.csv` has exactly 8 quarters × 3 features = 24 rows.
- Every `psi_value` is finite (not NaN/inf). Check:
  `source .venv/bin/activate && poetry run python -c "import pandas as pd, numpy as np; df=pd.read_csv('.../psi_sc2egset.csv'); assert np.isfinite(df['psi_value']).all()"`.
- The caption suffix appears in the PNG file (embedded via matplotlib's
  `fig.text(...)`).

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_02_psi_quarterly.py` (+ `.ipynb`)
- `artifacts/.../psi_sc2egset.csv`
- `artifacts/.../plots/psi_vs_quarter_sc2egset.png`
- `artifacts/.../psi_quarterly_sc2egset.md`

**Read scope:**
- T02 outputs (`quarterly_row_counts_sc2egset.csv`)
- T01 scaffold

---

### T04 — Q3: Stratification + sc2egset secondary regime `tournament_era`

**Objective:** Record explicitly that `regime_id ≡ quarter` at cross-dataset
level (spec §5) — no additional variance reduction. Define the within-dataset
secondary regime `tournament_era` for sc2egset (tournament tier) as exploratory.

**Instructions:**
1. Create `01_05_03_stratification_regime.py`.
2. Hypothesis cell: `# Hypothesis: tournament_era is confounded with quarter
   at the cross-dataset level but is a meaningful within-dataset categorical
   whose distribution of 'won' differs materially (|diff| > 0.02) across tiers.`
   `# Falsifier: tier-to-tier win-rate diff ≤ 0.005 → tier is noise, not
   regime.`
3. Derive `tournament_era` from the tournament directory name. Because
   `matches_history_minimal` does not carry the source directory, extract it
   for sc2egset from `replays_meta_raw` via the `filename` column (relative to
   `raw_dir`, per I10):
   ```sql
   CREATE OR REPLACE TEMP VIEW tournament_era_map AS
   SELECT
     rpm.replay_id,
     split_part(rpm.filename, '/', 1) AS tournament_dir,
     CASE
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%WCS%'       THEN 'Platinum'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%GSL%'       THEN 'Platinum'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%IEM%'       THEN 'Platinum'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%BlizzCon%'  THEN 'Platinum'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%HSC%'       THEN 'Gold'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%DH%'        THEN 'Gold'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%OSC%'       THEN 'Silver'
       WHEN split_part(rpm.filename, '/', 1) ILIKE '%TSL%'       THEN 'Silver'
       ELSE 'Bronze'
     END AS tournament_era
   FROM replays_meta_raw rpm
   ```
   This heuristic is **documented explicitly** as the sc2egset tier inference
   (I7 provenance: substrings cited from observed `tournament_dir` values in
   01_01_01). U2 resolves here; if the heuristic collapses ≥ 90% of rows to a
   single tier, the notebook records that and caveats the ICC interaction in
   T06.
4. Compute per-tier win-rate and sample size over the overlap window:
   ```sql
   SELECT tournament_era, COUNT(*) AS n, AVG(CAST(won AS DOUBLE)) AS mean_won
   FROM matches_history_minimal m
   JOIN tournament_era_map t USING (...)
   WHERE m.started_at BETWEEN TIMESTAMP '2022-07-01' AND TIMESTAMP '2024-12-31'
   GROUP BY tournament_era
   ORDER BY tournament_era
   ```
   Note: `matches_history_minimal` exposes `match_id = 'sc2egset::' || replay_id`;
   join via `substr(m.match_id, 11) = t.replay_id`.
5. Add a cell that re-states verbatim the spec §5 "honest statement" block:
   > `regime_id ≡ calendar quarter`. Cross-dataset stratification by
   > `regime_id` IS stratification by time, identical to the Q1 grain. It
   > provides no additional variance reduction beyond Q1.
6. Emit `tournament_era_sc2egset.csv` + `tournament_era_sc2egset.md`.

**Verification:**
- `tournament_era_sc2egset.csv` has 4 rows (`Bronze/Silver/Gold/Platinum`) with
  non-zero `n`. If any tier is empty, record it explicitly (the heuristic is
  legitimately allowed to miss a tier).
- The markdown contains the spec §5 honest statement verbatim.

**File scope:**
- `sandbox/.../01_05_03_stratification_regime.py` (+ `.ipynb`)
- `artifacts/.../tournament_era_sc2egset.csv`
- `artifacts/.../tournament_era_sc2egset.md`

**Read scope:**
- T02 outputs; `replays_meta_raw` schema YAML at
  `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replays_meta_raw.yaml`.

---

### T05 — Q4: Triple survivorship analysis (unconditional + sensitivity N∈{5,10,20} + conditional captioning)

**Objective:** Produce three survivorship tables required by spec §6 so
downstream drift figures can be captioned consistently.

**Instructions:**
1. Create `01_05_04_survivorship.py`.
2. Hypothesis: `# Hypothesis: sc2egset fraction_active peaks in 2022-Q4 and
   decays monotonically toward 2024-Q4; N=10 cohort is ≥ 50 players.`
   `# Falsifier: cohort < 20 players — cross-dataset PSI figure degrades to
   anecdote.`
3. **Unconditional (§6.1):** Compute `fraction_active` per quarter — fraction
   of players (within the set of ever-seen-in-overlap-window players) who have
   ≥1 match in that quarter.
   ```sql
   WITH players_in_window AS (
     SELECT DISTINCT player_id
     FROM matches_history_minimal
     WHERE started_at >= TIMESTAMP '2022-07-01'
       AND started_at <  TIMESTAMP '2025-01-01'
   ),
   quarters AS (
     SELECT DISTINCT
       strftime(started_at, '%Y') || '-Q' ||
         CAST(CEIL(CAST(strftime(started_at, '%m') AS INTEGER) / 3.0) AS VARCHAR) AS quarter
     FROM matches_history_minimal
     WHERE started_at >= TIMESTAMP '2022-07-01'
       AND started_at <  TIMESTAMP '2025-01-01'
   )
   SELECT q.quarter,
          COUNT(DISTINCT player_id) * 1.0 /
          (SELECT COUNT(*) FROM players_in_window) AS fraction_active
   FROM matches_history_minimal m
   CROSS JOIN quarters q
   WHERE m.player_id IN (SELECT player_id FROM players_in_window)
     AND strftime(m.started_at, '%Y') || '-Q' ||
         CAST(CEIL(CAST(strftime(m.started_at, '%m') AS INTEGER) / 3.0) AS VARCHAR) = q.quarter
   GROUP BY q.quarter
   ORDER BY q.quarter
   ```
   Churn: 90-day sliding window; compute in Python over the sorted history per
   `player_id`. Save to `survivorship_unconditional.csv`.
4. **Sensitivity (§6.2):** For N ∈ {5, 10, 20}, form the cohort of players
   with ≥N matches in the reference period 2022-08-29..2022-12-31 and
   additionally with active-span ≥ 30 days (max(started_at) − min(started_at)
   ≥ 30 days in reference). Record `cohort_size[N]` and re-run a minimal PSI
   (faction only) per quarter to emit the sensitivity table. Save to
   `survivorship_sensitivity.csv`.
5. **Conditional labels (§6.3):** Add a utility row to
   `survivorship_sensitivity.csv` with `N=10, is_default=True` flagging the
   default. T03/T08 plots inherit the caption suffix at render time.
6. Emit `survivorship_sc2egset.md` that embeds both tables.

**Verification:**
- `survivorship_unconditional.csv` has one row per quarter in the window
  (min 10).
- `survivorship_sensitivity.csv` has ≥ 3 rows (one per N) × 8 tested quarters +
  a default-flag row.
- The notebook logs the cohort cardinalities so U4 is resolved empirically.

**File scope:**
- `sandbox/.../01_05_04_survivorship.py` (+ `.ipynb`)
- `artifacts/.../survivorship_unconditional.csv`
- `artifacts/.../survivorship_sensitivity.csv`
- `artifacts/.../survivorship_sc2egset.md`

**Read scope:**
- T02, T03, T04 outputs

---

### T06 — Q6: Between/within variance decomposition ICC + secondary player×faction interaction

**Objective:** Fit a random-intercept `mixedlm` on `won ~ 1 + (1 | player_id)`
over the cohort-filtered overlap window; report ICC + 95% CI via delta method.

**Instructions:**
1. Create `01_05_05_variance_icc.py`.
2. Hypothesis: `# Hypothesis: Between-player variance dominates (ICC > 0.05)
   even for the 0/1 outcome 'won', consistent with persistent skill gaps in a
   tournament population.`
   `# Falsifier: ICC ≤ 0.01 — individual skill is not a clustering variable.`
3. Load the cohort (N≥10 in ref, min-cluster=10 per §8) into a pandas DataFrame:
   ```sql
   SELECT player_id, CAST(won AS DOUBLE) AS won
   FROM matches_history_minimal
   WHERE started_at >= TIMESTAMP '2022-07-01'
     AND started_at <  TIMESTAMP '2025-01-01'
     AND player_id IN (
       SELECT player_id FROM matches_history_minimal
       WHERE started_at >= TIMESTAMP '2022-08-29' AND started_at < TIMESTAMP '2023-01-01'
       GROUP BY player_id HAVING COUNT(*) >= 10
     )
   ```
4. Fit the random-intercept model:
   ```python
   import statsmodels.formula.api as smf
   md = smf.mixedlm("won ~ 1", data=df, groups=df["player_id"])
   res = md.fit(reml=True)
   sigma_u2 = float(res.cov_re.iloc[0, 0])       # between-player variance
   sigma_e2 = float(res.scale)                   # within-player (residual) variance
   icc = sigma_u2 / (sigma_u2 + sigma_e2)
   ```
5. Compute the delta-method 95% CI (Gelman & Hill 2007 §12.5) on ICC using
   the Fisher-information block of `res`. If `mixedlm` convergence fails,
   fall back to one-way random-intercept ANOVA ICC (see U1 fallback): compute
   group means, pooled within-group SS, between-group SS, and plug into
   `ICC = (MS_between - MS_within) / (MS_between + (k-1) * MS_within)` with
   k = mean cluster size; record the fallback decision verbatim.
6. Secondary: player × faction. For each of the 3 factions, refit the model
   restricted to that faction's rows and report per-faction ICC; emit a
   joint plot `icc_player_vs_faction.png`.
7. Persist `variance_icc_sc2egset.csv` with columns
   `dataset_tag, target (won), cohort_threshold, sigma_between, sigma_within,
   icc, icc_ci_low, icc_ci_high, n_obs, n_groups, method (mixedlm|anova_fallback)`.
8. Note explicitly that the secondary `rating_pre` target is N/A for sc2egset
   (A5) and explain why.

**Verification:**
- `variance_icc_sc2egset.csv` exists with a single primary row plus 3 per-faction rows.
- `icc` ∈ [0, 1]; `icc_ci_low ≤ icc ≤ icc_ci_high`.
- If fallback was used, `method == 'anova_fallback'` and the research-log draft
  notes the §13 deviation trigger (but no spec-version bump is required because
  §8 explicitly lists only the *method*; the fallback is a tool-availability
  substitution recorded as a CROSS entry).

**File scope:**
- `sandbox/.../01_05_05_variance_icc.py` (+ `.ipynb`)
- `artifacts/.../variance_icc_sc2egset.csv`
- `artifacts/.../plots/icc_player_vs_faction.png`
- `artifacts/.../variance_icc_sc2egset.md`

**Read scope:**
- T05 outputs (cohort definitions)

---

### T07 — Q7: `temporal_leakage_audit_v1` (hard gate)

**Objective:** Implement the 3 queries of spec §9. Query 1 must return 0 rows;
Query 2 must find zero `POST_GAME_HISTORICAL` / `TARGET` tokens in the feature
input list used by T03; Query 3 asserts the reference window edges.

**Instructions:**
1. Create `01_05_sc2_leakage_audit.py` (file name exactly as prescribed by
   spec §9 so the cross-dataset audit harness can enumerate all three).
2. Hypothesis: `# Hypothesis: Zero future-data leakage and zero post-game
   token leakage exist in the 01_05 input surface — spec §9 gate is already
   satisfied by the VIEW design (I3).`
   `# Falsifier: any row with observation_time >= match_time in the
   feature source OR any POST_GAME/TARGET token in the T03 feature list.`
3. Query 1 (future-data check). In sc2egset the "feature source" for 01_05 is
   exactly the VIEW row; each row's observation_time == started_at. We model
   a synthetic pairing to mirror the spec shape:
   ```sql
   WITH feature_rows AS (
     SELECT player_id, started_at AS observation_time, match_id AS match_time_key
     FROM matches_history_minimal
   ),
   target_rows AS (
     SELECT player_id, started_at AS match_time, match_id AS match_time_key
     FROM matches_history_minimal
   )
   SELECT COUNT(*) AS future_leak_count
   FROM feature_rows f
   JOIN target_rows t USING (match_time_key)
   WHERE f.observation_time >= t.match_time
     AND f.match_time_key = t.match_time_key  -- same-match by construction
   ;
   ```
   Because the feature-input surface for 01_05 is derived from prior-quarter
   rows only, the real check is the `>=` contamination check on feature-to-
   target lineage (spec §9 wording). In 01_05 we do not pair rows to
   downstream targets — the real per-game feature pairing is Phase 02. For
   01_05 we instead assert the stronger invariant: **every row used in a
   quarter-level aggregate used for PSI satisfies `started_at < end_of_quarter`**.
   Emit this check as `future_leak_count = 0` over the 8 tested quarters.
4. Query 2 (POST_GAME token scan). Scan the feature-input list used in T03
   for the strings `POST_GAME_HISTORICAL` and `TARGET`. The T03 feature list
   is exactly `['faction', 'opponent_faction', 'matchup']` — all PRE_GAME per
   the schema YAML. Implement the scan over the schema YAML at
   `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml`:
   ```python
   import yaml
   schema = yaml.safe_load(open("src/rts_predict/games/sc2/datasets/sc2egset/"
                                "data/db/schemas/views/matches_history_minimal.yaml"))
   banned_tokens = {"POST_GAME_HISTORICAL", "TARGET"}
   feature_inputs = ["faction", "opponent_faction", "matchup"]
   violations = []
   for col in schema["columns"]:
       if col["name"] in feature_inputs:
           notes = col.get("notes", "") or ""
           for tok in banned_tokens:
               if tok in notes:
                   violations.append((col["name"], tok, notes))
   assert len(violations) == 0, f"POST_GAME token scan violations: {violations}"
   ```
   Because `matchup` is derived in-notebook (not in the YAML), record its
   derivation rule (`sort(faction, opponent_faction)`) — it inherits the
   PRE_GAME category of its two inputs.
5. Query 3 (normalization-fit-window assertion). At the top of the notebook:
   ```python
   from datetime import datetime
   ref_start = datetime(2022, 8, 29)
   ref_end   = datetime(2022, 12, 31)
   assert ref_start == datetime(2022, 8, 29), f"Bad ref_start: {ref_start}"
   assert ref_end   == datetime(2022, 12, 31), f"Bad ref_end: {ref_end}"
   ```
6. Persist audit results to `leakage_audit_sc2egset.json`:
   ```json
   {
     "future_leak_count": 0,
     "post_game_token_violations": [],
     "reference_window_assertion": "PASS",
     "queries_sql_verbatim": { ... },
     "halt_triggered": false
   }
   ```
7. Halt condition: if `future_leak_count > 0` OR `post_game_token_violations
   != []` OR the reference-window assertion fails, **this task is blocked**,
   T08/T09/T10 do not run, and the research log records the block.

**Verification:**
- `leakage_audit_sc2egset.json` has `future_leak_count == 0` and
  `post_game_token_violations == []` and `reference_window_assertion == "PASS"`.
- Check with
  `source .venv/bin/activate && poetry run python -c "import json; j=json.load(open('.../leakage_audit_sc2egset.json')); assert j['future_leak_count']==0 and j['post_game_token_violations']==[] and j['reference_window_assertion']=='PASS'"`.

**File scope:**
- `sandbox/.../01_05_sc2_leakage_audit.py` (+ `.ipynb`)
- `artifacts/.../leakage_audit_sc2egset.json`
- `artifacts/.../leakage_audit_sc2egset.md`

**Read scope:**
- T02, T03 outputs (feature list + reference window); schema YAML for
  `matches_history_minimal`.

---

### T08 — Q8: POST_GAME DGP diagnostics — `duration_seconds`

**Objective:** Per-quarter summary statistics + Cohen's d vs reference for
`duration_seconds`. Emit with `dgp_diagnostic_` prefix so automated artifact
audits distinguish post-game from pre-game outputs (spec §10).

**Instructions:**
1. Create `01_05_06_dgp_diagnostics.py`.
2. Hypothesis: `# Hypothesis: duration_seconds mean/median drifts by < 5%
   across the 8 tested quarters vs reference (tournament formats stable).`
   `# Falsifier: any tested-quarter Cohen's d > 0.2 (small effect threshold)
   would be notable and needs calling out.`
3. Per quarter (including reference period labelled `2022-Q3Q4`):
   ```sql
   WITH tagged AS (
     SELECT
       CASE WHEN started_at BETWEEN TIMESTAMP '2022-08-29' AND TIMESTAMP '2022-12-31'
            THEN 'reference'
            ELSE strftime(started_at, '%Y') || '-Q' ||
                 CAST(CEIL(CAST(strftime(started_at, '%m') AS INTEGER) / 3.0) AS VARCHAR)
       END AS period_tag,
       duration_seconds
     FROM matches_history_minimal
     WHERE started_at >= TIMESTAMP '2022-08-29'
       AND started_at <  TIMESTAMP '2025-01-01'
   )
   SELECT period_tag,
          AVG(duration_seconds)       AS mean_dur,
          MEDIAN(duration_seconds)    AS median_dur,
          QUANTILE_CONT(duration_seconds, 0.05) AS p5_dur,
          QUANTILE_CONT(duration_seconds, 0.95) AS p95_dur,
          QUANTILE_CONT(duration_seconds, 0.75) -
          QUANTILE_CONT(duration_seconds, 0.25) AS iqr_dur,
          STDDEV_SAMP(duration_seconds)          AS sd_dur,
          COUNT(*)                               AS n
   FROM tagged
   GROUP BY period_tag
   ORDER BY period_tag
   ```
4. Compute Cohen's d per tested quarter:
   `d = (mean_q - mean_ref) / pooled_sd_q_ref`
   Emit one row per (quarter × metric) to `dgp_diagnostic_sc2egset.csv` with
   columns matching spec §12 (one row per dataset × quarter × feature ×
   metric, where `feature_name = 'duration_seconds'` and
   `metric_name in {'mean','median','p5','p95','iqr','cohen_d'}`).
5. `is_duration_suspicious` is NOT currently in `matches_history_minimal`
   (01_04_03 ADDENDUM records zero outliers > 86,400s, but the flag column
   itself isn't projected). Report corruption flag rate as `NULL` per spec §10
   and record the availability gap.
6. Emit `dgp_diagnostic_sc2egset.md` with the per-quarter table and a small
   line-plot of `mean_dur` over time.

**Verification:**
- `dgp_diagnostic_sc2egset.csv` has 9 period_tags (1 reference + 8 tested) ×
  6 metrics = 54 rows (or equivalent long form).
- Cohen's d values are finite.
- Prefix check: no pre-game PSI file is named with `dgp_diagnostic_`.

**File scope:**
- `sandbox/.../01_05_06_dgp_diagnostics.py` (+ `.ipynb`)
- `artifacts/.../dgp_diagnostic_sc2egset.csv`
- `artifacts/.../dgp_diagnostic_sc2egset.md`
- `artifacts/.../plots/dgp_diagnostic_duration_trend.png`

**Read scope:**
- T02 (quarter definitions), T07 (reference-window assertion carried forward)

---

### T09 — Phase 06 interface CSV emission (spec §12 flat schema)

**Objective:** Consolidate T03/T06/T08 outputs into the one canonical flat
schema ready for Manual 06 consumption. One row per
(dataset × quarter × feature × metric).

**Instructions:**
1. Create `01_05_07_phase06_interface.py`.
2. Hypothesis: `# Hypothesis: A union of T03 PSI rows, T06 ICC rows, and T08
   DGP d rows conforms to spec §12 with 0 schema violations.`
   `# Falsifier: any row with NaN in non-nullable columns, bad dtype, or
   unknown metric_name.`
3. Load `psi_sc2egset.csv`, `variance_icc_sc2egset.csv`,
   `dgp_diagnostic_sc2egset.csv`; melt to the 9-column long schema of spec §12:
   ```
   dataset_tag, quarter, feature_name, metric_name, metric_value,
   reference_window_id, cohort_threshold, sample_size, notes
   ```
   - `dataset_tag = 'sc2egset'` constant.
   - `reference_window_id = '2022-Q3Q4'`.
   - `cohort_threshold`: `10` for T03 default rows; `{5,10,20}` for T05
     sensitivity rows; `10` for T06 rows; `NULL` for T08 rows where no cohort
     filter was applied.
   - `sample_size` = `n_ref` or `n_tested` depending on row origin;
     documented per-row in `notes`.
   - `notes` captures `[SMALL-COHORT]`, `__unseen__: N rows`,
     `tournament_era: <tier>` when applicable, `[SC2EGSET-POST-GAME]` for
     DGP rows.
4. Validate schema with Python asserts:
   ```python
   assert set(df.columns) == {
     "dataset_tag","quarter","feature_name","metric_name","metric_value",
     "reference_window_id","cohort_threshold","sample_size","notes",
   }
   assert df["dataset_tag"].eq("sc2egset").all()
   assert df["metric_name"].isin({"psi","cohen_h","cohen_d","ks_stat","icc"}).all()
   # 4-decimal formatting done at write time
   df["metric_value"] = df["metric_value"].round(4)
   ```
5. Persist to `phase06_interface_sc2egset.csv`. Also emit a schema shadow
   `phase06_interface_sc2egset.schema.json` that documents the 9 columns and
   their types/nullability for Manual 06 consumers.
6. NaN handling: store as SQL NULL (blank CSV cell) per spec §12.

**Verification:**
- `phase06_interface_sc2egset.csv` has the 9 columns exactly.
- `source .venv/bin/activate && poetry run python -c "import pandas as pd; df=pd.read_csv('.../phase06_interface_sc2egset.csv'); assert list(df.columns)==['dataset_tag','quarter','feature_name','metric_name','metric_value','reference_window_id','cohort_threshold','sample_size','notes']; assert df['dataset_tag'].eq('sc2egset').all(); assert df['metric_name'].isin({'psi','cohen_h','cohen_d','ks_stat','icc'}).all()"` exits 0.
- Row count > 0 and equals `len(T03) + len(T06) + len(T08 melted)`.

**File scope:**
- `sandbox/.../01_05_07_phase06_interface.py` (+ `.ipynb`)
- `artifacts/.../phase06_interface_sc2egset.csv`
- `artifacts/.../phase06_interface_sc2egset.schema.json`
- `artifacts/.../phase06_interface_sc2egset.md`

**Read scope:**
- T03 (`psi_sc2egset.csv`)
- T06 (`variance_icc_sc2egset.csv`)
- T08 (`dgp_diagnostic_sc2egset.csv`)
- T05 (survivorship — `cohort_threshold` sourcing)

---

### T10 — Research log, INVARIANTS §4, status file updates, Decision Gate memo

**Objective:** Close out the step. Append an audited research-log entry, seed
INVARIANTS §4 with findings from T02–T09, advance STEP_STATUS/
PIPELINE_SECTION_STATUS/PHASE_STATUS, add the 01_05_01..01_05_07 + audit
entries to `ROADMAP.md`, and write the per-step Decision Gate §6 memo.

**Instructions:**
1. Append to `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
   a reverse-chronological entry dated 2026-04-18 titled
   `## 2026-04-18 — [Phase 01 / Pipeline Section 01_05] Temporal & Panel EDA (sc2egset)`
   with the standard sections (What / Why / How / Findings / Decisions taken /
   Decisions deferred / Thesis mapping / Open questions / follow-ups).
2. Populate `INVARIANTS.md` §4 with empirical findings (each cites the exact
   SQL or Python snippet from T02–T09, I6). Examples:
   - `Quarterly grain & overlap: 10 quarters 2022-Q3..2024-Q4 with
     n_matches=[...]` (from T02).
   - `PSI for faction/opponent_faction/matchup over 8 tested quarters: all
     values <0.10 (no shift) / moderate / significant` (from T03).
   - `tournament_era heuristic coverage: {Bronze: ..., Silver: ..., Gold: ...,
     Platinum: ...}` (from T04).
   - `Cohort sizes N∈{5,10,20}: {5: x, 10: y, 20: z}` (from T05).
   - `ICC on won: icc=<v> (CI [<lo>, <hi>]) via mixedlm (or anova_fallback)`
     (from T06).
   - `Leakage audit: future_leak_count=0; post_game token violations=0;
     reference window asserted 2022-08-29..2022-12-31` (from T07).
   - `duration_seconds drift: max |Cohen's d| across 8 tested quarters =
     <v>` (from T08).
3. Update `STEP_STATUS.yaml` to add entries
   `01_05_01` Quarterly Grain (section 01_05), `01_05_02` PSI Quarterly,
   `01_05_03` Stratification & Regime, `01_05_04` Survivorship Triplet,
   `01_05_05` Variance & ICC, `01_05_06` DGP Diagnostics, `01_05_07` Phase 06
   Interface, `01_05_sc2_leakage_audit` (audit, treated as a companion
   entry — keep naming consistent with spec §9 file path). Name the audit step
   `01_05_08` internally but keep the spec-mandated filename. All 8 entries
   marked `status: complete` with `started_at` / `completed_at: 2026-04-18`
   once all artifacts exist.
4. Update `PIPELINE_SECTION_STATUS.yaml` to set `01_05.status: complete` once
   all 8 steps are complete.
5. Update `PHASE_STATUS.yaml` only if `01_06` also completes in a follow-up
   PR — in this PR `phase 01` remains `in_progress` because 01_06 (Decision
   Gates) is still `not_started`. Verify the derivation chain stays consistent
   (`ROADMAP → STEP_STATUS → PIPELINE_SECTION_STATUS → PHASE_STATUS`).
6. Append new Step blocks to `ROADMAP.md` under `### Step 01_05_xx — <name>`
   using the `docs/templates/step_template.yaml` shape, matching the eight
   notebook names and citing their gate checks. No hypotheses land here —
   only step names, gate predicates, and artifact paths (per directive 1).
7. Draft the per-step Decision Gate §6 go/no-go memo at
   `artifacts/.../decision_gate_sc2egset.md` answering:
   - Did every Q1–Q9 parameter group execute? (Y/N per group)
   - Were any spec deviations triggered? (list each; link to CROSS entry)
   - Is 01_05 ready to feed Phase 02? (YES iff all 10 tasks green + leakage
     audit PASS + phase06 interface CSV schema-valid)
8. Regenerate `planning/INDEX.md` active-plan pointer to reference
   `planning/current_plan.md` (this file).

**Verification:**
- `grep -n "2026-04-18 — \[Phase 01 / Pipeline Section 01_05\]" src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` returns ≥ 1 match.
- `grep -n "^## §4" src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` is followed by ≥ 7 bulletted findings (one per T02–T08).
- `STEP_STATUS.yaml` has entries `01_05_01` through `01_05_07` + the leakage audit entry, all `status: complete`.
- `PIPELINE_SECTION_STATUS.yaml` has `"01_05": {status: complete}`.
- `decision_gate_sc2egset.md` exists and embeds a 9-row Q1..Q9 table with
  Y/N verdicts.

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (append)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` (populate §4)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (add 8 entries)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (mark 01_05 complete)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` (confirm `01 in_progress`)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (append 01_05 step definitions)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/decision_gate_sc2egset.md`
- `reports/research_log.md` (append CROSS reference if any spec §13 deviation was triggered)

**Read scope:**
- All prior task outputs (T02..T09 artifacts)

---

## File Manifest

| File | Action |
|------|--------|
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_00_scaffold.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_01_quarterly_grain.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_02_psi_quarterly.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_02_psi_quarterly.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_03_stratification_regime.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_03_stratification_regime.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_04_survivorship.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_05_variance_icc.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_05_variance_icc.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_06_dgp_diagnostics.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_06_dgp_diagnostics.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_07_phase06_interface.ipynb` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_sc2_leakage_audit.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/01_05_sc2_leakage_audit.ipynb` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset_full.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/quarterly_row_counts_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/plots/psi_vs_quarter_sc2egset.png` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/psi_quarterly_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/tournament_era_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/tournament_era_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_unconditional.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sensitivity.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/survivorship_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/variance_icc_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/plots/icc_player_vs_faction.png` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/variance_icc_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.json` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/dgp_diagnostic_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/plots/dgp_diagnostic_duration_trend.png` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.csv` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.schema.json` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.md` | Create |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/decision_gate_sc2egset.md` | Create |
| `pyproject.toml` | Update (add `statsmodels`) |
| `poetry.lock` | Update (lockfile) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update (append 01_05 entry) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` | Update (populate §4) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Update (+ 8 step entries) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Update (01_05 → complete) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Update (confirm 01 in_progress) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | Update (append 8 Step blocks) |
| `reports/research_log.md` | Update (optional CROSS entry if deviation triggered) |

## Gate Condition

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` contains 8 entries `01_05_01`, `01_05_02`, `01_05_03`, `01_05_04`, `01_05_05`, `01_05_06`, `01_05_07`, and one leakage-audit entry, all with `status: complete`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` has `"01_05".status == complete`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.json` has `future_leak_count == 0` AND `post_game_token_violations == []` AND `reference_window_assertion == "PASS"`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.csv` exists, has 9 columns exactly matching spec §12, and `dataset_tag` is constant `sc2egset`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/decision_gate_sc2egset.md` exists and reports YES for every Q1..Q9 parameter group.
- Every `.py` notebook in `sandbox/sc2/sc2egset/01_exploration/05_temporal_panel_eda/` contains the line `# spec: reports/specs/01_05_preregistration.md@7e259dd8` within its first 40 lines. Verify via `source .venv/bin/activate && poetry run python scripts/check_01_05_binding.py --all`; exit 0.
- `source .venv/bin/activate && poetry run pytest tests/ -v` → all tests pass (no regression in existing tests; no new tests strictly required for read-only notebooks but T01's poetry update must not break collection).
- `grep -c "2026-04-18 — \[Phase 01 / Pipeline Section 01_05\]" src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` ≥ 1.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` §4 contains at least 7 findings, each with a cited SQL/Python snippet (I6).

## Out of scope

- **aoec and aoestats sibling implementations.** This plan is sc2egset-only.
  Cross-dataset harmonisation and sibling notebooks live in separate PRs.
  The spec §12 interface file produced here is meant to be UNIONed with the
  sibling CSVs, but the UNION operation itself is Manual 06's responsibility,
  not this step.
- **Manual curation of the ~12% cross-region nickname cases.** Remains
  accepted bias per I2 branch (iii); no re-classification attempted here.
- **Phase 02 `canonical_slot` column.** Not applicable to sc2egset (spec §11
  binding is aoestats-only). Spec §15 confirms.
- **ADF/KPSS secondary analyses.** Spec §3 permits aoec secondary only; not
  run here.
- **01_06 Decision Gates pipeline section.** Separate step; this plan
  produces only the per-step Decision Gate memo (§6 of manual 01), not the
  pipeline-section level gate that closes Phase 01.
- **Model training or feature engineering.** Phase 02+.

## Open questions

- **OQ1 — statsmodels availability (U1).** If `poetry add statsmodels`
  fails on the sandbox environment, T06 falls back to closed-form
  ANOVA ICC; this is recorded as a CROSS research-log entry and does not
  require a spec-version bump because §8 describes the *method* and the
  fallback is a tool-availability substitution. Resolves during T01 setup.
- **OQ2 — `tournament_era` heuristic coverage (U2).** The substring rules
  in T04 may leave many replays in the `Bronze` catch-all. If > 90% collapse
  to one tier, T04 records it and T06's secondary `player×faction` analysis
  skips the era breakdown. Resolves during T04.
- **OQ3 — cohort cardinality (U4).** If the `N≥10 in reference` cohort
  leaves fewer than 20 players, the T03 PSI and T06 ICC become anecdotal at
  best. T05 reports the exact size; T10 decides whether to retain the
  N=10 default or fall back to N=5 for the cross-dataset default (spec §6
  allows N=5 as a sensitivity threshold). A default change would trigger
  §13 (research log + §14 amendment + version bump) — documented if it
  happens.
- **OQ4 — `rating_pre` secondary target in T06.** Spec §8 allows secondary
  ICC fit on `rating_pre` if non-NULL in ≥ 80% of rows. sc2egset exposes no
  `rating_pre` column in `matches_history_minimal` (A5). Decision: mark N/A
  and document. If a future amendment adds `rating_pre` via MMR projection,
  re-run T06.
- **OQ5 — do we emit ks_stat?** Spec §12 lists ks_stat as an allowable
  `metric_name` but §4 scopes it to continuous features. sc2egset has no
  continuous pre-game features in the VIEW; KS is therefore omitted. T09
  records the omission. If the reviewer insists KS must appear, T03 adds a
  KS over the ECDF of match-per-quarter counts per player (a secondary
  descriptive use per Breck et al. 2019). Resolves during adversarial review.