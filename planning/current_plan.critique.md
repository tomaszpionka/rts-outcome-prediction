# Plan Critique — SC2EGSet Step 02_01_01 Notebook Scaffold

**Reviewer:** reviewer-deep (claude-opus-4-7)
**Date:** 2026-05-07
**Plan:** planning/current_plan.md — phase02/sc2egset-feature-registry-scaffold
**Verdict:** PASS-WITH-NOTES

## Blockers

None.

## Warnings

**W1 (resolved in plan).** V-1 sub-count 22+1+3 = 26 requires an explicit row-identity commitment for CROSS-02-02-v1.0.1 §6.1 `focal_race`/`opponent_race`: treated as ONE registry row (`focal_race_with_opponent_race_pair`). Plan A3 now makes this explicit.

**W2 (resolved in plan).** V-3 must pin `status_in_game_snapshot` as the authoritative CSV column (not `status_pre_game` or `planned_for_phase02`), and the membership check must be bidirectional. Plan V-3 now specifies both.

## Notes

**N1.** V-1..V-6 cover a subset of CROSS-02-03-v1.0.1 §3 audit-object schema fields. Six fields (`source_table_or_event_family`, `source_grain`, `model_input_grain`, `target_grain`, `candidate_leakage_modes`, `status`) are deferred to future validation modules per data-analysis-lineage.md sequence step 6. Plan validation module section now documents this explicitly.

**N2.** `per_player_construction` is a registry-introduced label (not verbatim in spec). Plan A7 documents this in the same way `sanity_gate_not_model_input` is documented as registry-introduced in A3.

**N3 (resolved in plan).** T06 must pre-fill `[Unreleased] / Added` in CHANGELOG.md with at least one bullet before T07 rolls it, to avoid an empty release block. Plan T06 now includes this step.

**N4.** T05 "pytest sanity" clarified to mean `pytest tests/ -v` for regression only; no new tests added in this PR; validation logic lives in notebook cells.

**N5.** Notebook is filesystem/CSV-only (Pattern B, per sandbox/README.md); no DuckDB connection. Cell 04 (DuckDB setup) and cleanup cell omitted. Plan A2 and T02 now state this explicitly.

**N6 (informational).** Sandbox subdirectory slug `pre_game_vs_in_game_boundary` matches Pipeline Section name in docs/PHASES.md. No `__init__.py` required — sandbox is not a Python package.

**N7 (informational).** `pyproject.toml` confirmed at version 3.47.0 at base commit `6e220ad9`. Version bump to 3.48.0 is consistent with minor-feat convention.

## reviewer-adversarial required?

No. No methodology BLOCKER raised. Methodology choices (V-1..V-6 scope, strict-< history cutoff, tracker-never-pre-game, slot_identity_consistency as sanity_gate, 26-row count, dataset_tag pinning) are all directly anchored in the locked specs and the SC2EGSet ROADMAP step 02_01_01 description.

## Plan ready to write to planning/current_plan.md?

Yes — W1, W2, N3 fixes applied in the plan text above.
