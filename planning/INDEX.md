# Planning Index

## Active plan
- phase02/sc2egset-feature-registry-v8-source-grain-well-formedness (2026-05-09) — SC2EGSet Step 02_01_01 V-8 source-grain structural well-formedness validation

## Archive

| Branch | Date | Category | Description | Plan file | Merged PR |
|--------|------|----------|-------------|-----------|-----------|
| phase02/sc2egset-feature-registry-scaffold | 2026-05-07 | A | SC2EGSet Step 02_01_01 notebook scaffold + one validation module | current_plan.md | #212 (merged 2026-05-08 at master 18d30a81) |
| phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start | 2026-05-08 | A | SC2EGSet Step 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation | current_plan.md | #213 (merged 2026-05-09 at master 7b26b40f) |

## Agent routing

| Role | Reads |
|------|-------|
| Executor | `planning/current_plan.md` (task T01, T02, … as directed) |
| Reviewer-adversarial (final gate, Cat A/F) | `planning/current_plan.md` + diff |
| Reviewer-deep (final gate, Cat B/D) | `planning/current_plan.md` + diff |
| Reviewer (final gate, Cat C/E) | diff only |
