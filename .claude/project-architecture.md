# Project Architecture

## Package Layout (`src/sc2ml/`)

- `cli.py` — pipeline orchestrator, CLI subcommands (`init`, `run`, `sanity`, `ablation`, `tune`, `evaluate`)
- `config.py` — path constants, ML hyperparameters, reproducibility settings
- `validation.py` — Phase 0 sanity checks (25+ automated checks across 5 sections)
- `data/ingestion.py` — replay JSON parsing, DuckDB loading, map translations, in-game event extraction
- `data/processing.py` — SQL view creation (`flat_players`, `matches_flat`), temporal split, series detection
- `data/cv.py` — `ExpandingWindowCV` for temporal cross-validation (sklearn-compatible)
- `features/__init__.py` — `build_features(df, groups=)` composable API, `split_for_ml()`
- `features/registry.py` — `FeatureGroup` enum + lazy-loaded compute function registry
- `features/common.py` — shared primitives (expanding-window aggregates, Bayesian smoothing)
- `features/compat.py` — backward-compatible wrappers (`perform_feature_engineering`, `temporal_train_test_split`)
- `features/group_a_elo.py` — Group A: dynamic K-factor Elo, `elo_diff`, `expected_win_prob`
- `features/group_b_historical.py` — Group B: Bayesian-smoothed winrates, cumulative APM/SQ means, variance
- `features/group_c_matchup.py` — Group C: race one-hot, spawn distance, map area, map×race winrate
- `features/group_d_form.py` — Group D: win/loss streaks, EMA stats, 7d/30d activity, head-to-head
- `features/group_e_context.py` — Group E: patch version numeric, tournament match position, series game number
- `models/baselines.py` — `MajorityClassBaseline`, `EloOnlyBaseline`, `EloLRBaseline` (all with `predict_proba`)
- `models/classical.py` — classical ML training/evaluation (LR, LightGBM, XGBoost, RF, GB)
- `models/tuning.py` — Optuna-based Bayesian optimization (`tune_lgbm_optuna`, `tune_xgb_optuna`) + LR grid search
- `models/evaluation.py` — `evaluate_model`, `compare_models` (McNemar/DeLong), `bootstrap_ci`, permutation importance, feature ablation, patch drift
- `models/reporting.py` — `ExperimentReport` with `.to_json()` and `.to_markdown()` for thesis-ready reports
- `analysis/shap_analysis.py` — SHAP values (TreeExplainer/LinearExplainer), beeswarm plots, per-matchup analysis
- `analysis/error_analysis.py` — error subgroup classification (mirrors, upsets, close Elo, short/long games)
- `gnn/model.py` — SC2EdgeClassifier (GATv2Conv-based edge classifier) — **deprioritized, appendix only**
- `gnn/pipeline.py` — graph construction from player features (node + edge features)
- `gnn/trainer.py` — GNN training loop with early stopping
- `gnn/visualizer.py` — t-SNE visualization of learned GNN embeddings
- `gnn/embedder.py` — Node2Vec embeddings via NetworkX/Gensim

**Feature count:** 66 features across 5 groups (A→14, A+B→37, A+B+C→45, A+B+C+D→62, all→66)

## Directories

- `models/` — serialized model artifacts (`.joblib`, `.pt`)
- `reports/` — ROADMAP, methodology, research log, test plan, experiment outputs
- `reports/archive/` — legacy pipeline execution logs (`01_run.md` through `09_run.md`)
- `logs/` — pipeline log file (`sc2_pipeline.log`)
- `tests/` — pytest test suite (root level)
- `src/sc2ml/data/tests/` — data subpackage tests

## External Data Paths (from `config.py`)

- `~/duckdb_work/test_sc2.duckdb` — main DuckDB database
- `~/duckdb_work/tmp/` — DuckDB temp directory
- `~/Downloads/SC2_Replays/` — raw SC2Replay JSON files

## Data Pipeline (5 Stages)

1. **Ingestion** — `slim_down_sc2_with_manifest()` strips heavy replay events; `move_data_to_duck_db()` loads JSON into DuckDB `raw` table; `load_map_translations()` populates map name lookup
2. **SQL Processing** — `create_ml_views()` creates `flat_players` (one row per player per match) and `matches_flat` (paired players per match with features)
3. **ELO Computation** — `add_elo_features()` (in `group_a_elo.py`) computes pre-match ELO with dynamic K-factor
4. **Feature Engineering** — `build_features(df, groups=)` computes feature groups A–E incrementally. Drops post-match leakage columns.
5. **Model Training** (2 active paths + 1 deprioritized):
   - `CLASSIC` — tabular ML models with temporal split (primary)
   - `NODE2VEC` — graph embeddings appended to tabular features, then classical models
   - `GNN` — end-to-end GATv2-based edge classification (**deprioritized — appendix only**, known majority-class collapse)

## Known Design Decisions

- `matches_flat` produces 2 rows per match (p1/p2 and p2/p1 perspective) — intentional data augmentation; raw row count is ~2x actual unique matches
- ELO system processes each unique `match_id` only once via `processed_matches` set, despite the paired rows
- Feature engineering's cumulative operations assume chronological sorting — **never shuffle the dataframe before feature engineering**
- The GNN uses **edge classification** (predicting match outcome from player node embeddings + edge features), not node classification — a less common PyG pattern
- DuckDB configured for 24GB RAM, 4 threads (tuned for high-memory machine)
- `processing_manifest.json` (2MB) tracks which replay files have been processed; committed to git
- LightGBM and PyTorch load conflicting OpenMP runtimes on macOS — classical model tests run in subprocess isolation (`multiprocessing.spawn`)
