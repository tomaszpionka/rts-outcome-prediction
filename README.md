# SC2-ML: StarCraft II Match Prediction

Master's thesis project: "A comparative analysis of methods for predicting game results in real-time strategy games, based on the examples of StarCraft II and Age of Empires II."

Predicts professional SC2 match outcomes from replay data using classical ML (LightGBM, XGBoost, Logistic Regression), with planned extensions to in-game temporal models (LSTM, TCN) and a dual-stream fusion architecture.

## Quick Start

```bash
poetry install
poetry run sc2ml --help
poetry run pytest tests/ -v --cov=sc2ml
```

## Documentation

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | AI assistant instructions and project rules |
| `reports/methodology.md` | Full thesis methodology specification (RQs, features, models, evaluation) |
| `reports/ROADMAP.md` | Progress tracking with checkboxes — single source of truth for project state |
| `reports/research_log.md` | Reverse-chronological thesis narrative |
| `reports/test_plan.md` | Test coverage augmentation plan |
| `CHANGELOG.md` | Code version history |
| `.claude/` | Coding, workflow, and ML experiment standards |
| `src/sc2ml/data/README.md` | Data schema reference (raw JSON → DuckDB views → features) |
