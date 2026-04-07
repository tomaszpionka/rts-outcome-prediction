SPEC — Category C — game-level ROADMAP placeholder

## Goal
Replace src/rts_predict/sc2/reports/ROADMAP.md content with a short
placeholder. The current file contains speculative Phase 3-10 content
with magic numbers and pre-decided cleaning rules that violate
.claude/scientific-invariants.md and pollute agent context.

## Action
Replace the entire contents of src/rts_predict/sc2/reports/ROADMAP.md
with the following text:

---
# SC2 Game-Level Roadmap — Phase 2+

**Status:** Not authored. All Phase ≥2 work is cross-dataset and depends
on completed Phase 1 exploration of every SC2 dataset currently in scope.

**Authoring trigger:** When every dataset under
`src/rts_predict/sc2/reports/<dataset>/` has reached its Phase 1 gate
(the four epistemic-readiness deliverables defined in
`docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md` §6.1 exist
as named artifacts), `planner-science` drafts Phase 2 here, using the
Phase 1 wrap-up reports as input. Not before.

**Methodology source of truth:** `docs/INDEX.md`.
Do not introduce phase numbers, phase names, or thresholds in this file
that are not already defined in the manuals indexed there.

**Planned phase shells (names only — content authored at trigger time):**
- Phase 2 — Cleaning & validation
- Phase 3 — Feature engineering
- Phase 4 — Splitting & baselines
- Phase 5 — Model training & hyperparameter tuning
- Phase 6 — Evaluation, calibration & error analysis
- Phase 7 — Cross-domain transfer (SC2 ↔ AoE2)
- Phase 8 — Thesis writing wrap-up

**Active dataset roadmaps:**
- `sc2egset/ROADMAP.md` — Phase 0 complete, Phase 1 in progress
---

## Hard constraints
- Do NOT touch sc2egset/ROADMAP.md. Phase 0 and Phase 1 content there
  is preserved verbatim.
- Do NOT touch PHASE_STATUS.yaml. Phase number renames are deferred.
- Do NOT touch the AoE2 game-level ROADMAP. It is already a placeholder.
- Do NOT touch any other file in the repo.

## Acceptance criteria
- src/rts_predict/sc2/reports/ROADMAP.md is exactly the text above,
  no more no less.
- ruff/mypy/pytest green.
- git diff shows changes to exactly one file.