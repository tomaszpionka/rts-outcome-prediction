# Planning Index

## Active plan
- thesis/phase02-registry-methodology-section-4-5 (2026-05-17) — Phase 02 registry methodology framing for Chapter 4 §4.5 (TQ-03); provisional §4.5 writing; Step/Phase closure NOT claimed (draft PR #219)

## Archive

| Branch | Date | Category | Description | Plan file | Merged PR |
|--------|------|----------|-------------|-----------|-----------|
| phase02/sc2egset-feature-registry-scaffold | 2026-05-07 | A | SC2EGSet Step 02_01_01 notebook scaffold + one validation module | current_plan.md | #212 (merged 2026-05-08 at master 18d30a81) |
| phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start | 2026-05-08 | A | SC2EGSet Step 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation | current_plan.md | #213 (merged 2026-05-09 at master 7b26b40f) |
| phase02/sc2egset-feature-registry-v8-source-grain-well-formedness | 2026-05-09 | A | SC2EGSet Step 02_01_01 V-8 source-grain structural well-formedness validation | current_plan.md | #214 (merged 2026-05-10 at master 664c869a) |
| phase02/sc2egset-feature-registry-v9-symmetry | 2026-05-10 | A | SC2EGSet Step 02_01_01 V-9 per-player construction / focal-opponent symmetry validation (spec-D10 sub-clause 1) | current_plan.md | #215 (merged 2026-05-10 at master 396f162c) |
| phase02/sc2egset-registry-artifact-provisional-v9 | 2026-05-10 | A | SC2EGSet Step 02_01_01 provisional registry artifact validated through V-9; first on-disk CSV+MD; Step closure NOT claimed | current_plan.md | #216 (merged into master) |

## Agent routing

| Role | Reads |
|------|-------|
| Executor | `planning/current_plan.md` (task T01, T02, … as directed) |
| Reviewer-adversarial (final gate, Cat A/F) | `planning/current_plan.md` + diff |
| Reviewer-deep (final gate, Cat B/D) | `planning/current_plan.md` + diff |
| Reviewer (final gate, Cat C/E) | diff only |
