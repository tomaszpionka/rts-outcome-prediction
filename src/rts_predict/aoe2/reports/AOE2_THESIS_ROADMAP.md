# AoE2 Thesis Roadmap

This roadmap will be created after the SC2 pipeline reaches a sufficient phase
(target: after SC2 Phase 3 — classical ML baseline is complete and evaluated).

Per ARCHITECTURE.md "Adding a new game", step 3: write the game-specific roadmap
once the data acquisition and profiling plan is confirmed.

## Pending actions

- [ ] Complete SC2 Phase 0–3 pipeline
- [ ] Profile aoe2companion data (Phase 0 equivalent)
- [ ] Define AoE2-specific feature groups
- [ ] Write full roadmap mirroring SC2_THESIS_ROADMAP.md structure

## CLI entry point

No `cli.py` exists yet. A `aoe2` entry point in `pyproject.toml` will be added
once a minimal CLI command is implemented (see ARCHITECTURE.md "Adding a new
game" checklist, step 4).
