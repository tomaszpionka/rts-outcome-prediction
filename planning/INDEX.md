# Planning Index

## Active plan
- feat/sc2egset-02-01-02-roadmap-stub (2026-05-22) — Category A: ROADMAP-only stub defining Step 02_01_02 under Pipeline Section 02_01 (first pre_game feature-family materialization design; 5 allowed pre_game families; full temporal/leakage/cold-start/SQL design recorded as declaration only). NO feature value materialized, NO notebook, NO artifact, NO status YAML flip, NO Phase 03 work. Version bump 3.66.0 → 3.67.0 (PR #232, draft).

## Archive

| Branch | Date | Category | Description | Plan file | Merged PR |
|--------|------|----------|-------------|-----------|-----------|
| docs/thesis-pass2-020101-manifest-closure-reconciliation | 2026-05-22 | F | reconcile thesis/pass2_evidence/notebook_regeneration_manifest.md with the PR #230 catalog-only closure of SC2EGSet Step 02_01_01; new token catalog_only_closed_zero_materialization replaces partial_coverage_v9_baseline on the 02_01_01 row; +2 Phase-02 rows (§10 verdict-audit, CROSS-02-01 pair); PR #230 archived; CHANGELOG + version bump 3.65.0 -> 3.66.0; NO 02_01_02, NO Phase 03, NO chapter prose, NO status YAML/artifact/research_log edits | current_plan.md | #231 (merged 2026-05-22 at master e96374fe) |
| feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit | 2026-05-21 | A | SC2EGSet Phase-02 Step 02_01_01 closure via zero-materialization CROSS-02-01-v1.0.1 leakage-audit artifact pair; STEP_STATUS adds 02_01_01: complete; PIPELINE_SECTION_STATUS adds 02_01: complete; PHASE_STATUS Phase 02 -> in_progress; per-dataset research_log closure entry; CHANGELOG + version bump 3.64.0 -> 3.65.0 | current_plan.md | #230 (merged 2026-05-22 at master 0c45c490) |
| feat/sc2egset-02-01-01-section10-audit-persistence | 2026-05-21 | A | SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict-audit evidence persistence; persist CSV+MD artifacts + per-dataset research_log entry; STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / ROADMAP / INVARIANTS / registry CSV/MD / validator / validator tests / root research_log frozen; Step 02_01_01 NOT closed | current_plan.md | #229 (merged 2026-05-21 at master a14dc547) |
| feat/sc2egset-02-01-01-section10-verdict-audit | 2026-05-21 | A | SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict audit: validator + jupytext notebook scaffold; all 26 registry rows audited; materialized_column_count=0; no status/ROADMAP/research_log/artifact mutation; Step 02_01_01 NOT closed | current_plan.md | #228 (merged 2026-05-21 at master 5c7ef380) |
| docs/thesis-appendix-key-canonicalization | 2026-05-19 | F | Appendix-only bib-key canonicalization: Baek2022→BaekKim2022, Porcpine2020→Porcpine2020EloAoE, Herbrich2007→Herbrich2006 key/style normalization with 2007 retained, Glickman2025 appendix typo fix, BT2025Survey appendix repair; references.bib + chapters untouched | current_plan.md | #227 (merged 2026-05-19 at master db8aeafc) |
| docs/thesis-bialecki2023-author-correction | 2026-05-19 | F | Bialecki2023 authors 3–4 post-merge correction (overturned #225 surname+initial-blind no-edit) | current_plan.md | #226 (merged 2026-05-19 at master 637fdb93) |
| phase02/sc2egset-feature-registry-scaffold | 2026-05-07 | A | SC2EGSet Step 02_01_01 notebook scaffold + one validation module | current_plan.md | #212 (merged 2026-05-08 at master 18d30a81) |
| phase02/sc2egset-feature-registry-v1-strict-and-v7-cold-start | 2026-05-08 | A | SC2EGSet Step 02_01_01 V-1 strict + V-7 cold-start vocabulary/sentinel validation | current_plan.md | #213 (merged 2026-05-09 at master 7b26b40f) |
| phase02/sc2egset-feature-registry-v8-source-grain-well-formedness | 2026-05-09 | A | SC2EGSet Step 02_01_01 V-8 source-grain structural well-formedness validation | current_plan.md | #214 (merged 2026-05-10 at master 664c869a) |
| phase02/sc2egset-feature-registry-v9-symmetry | 2026-05-10 | A | SC2EGSet Step 02_01_01 V-9 per-player construction / focal-opponent symmetry validation (spec-D10 sub-clause 1) | current_plan.md | #215 (merged 2026-05-10 at master 396f162c) |
| phase02/sc2egset-registry-artifact-provisional-v9 | 2026-05-10 | A | SC2EGSet Step 02_01_01 provisional registry artifact validated through V-9; first on-disk CSV+MD; Step closure NOT claimed | current_plan.md | #216 (merged into master) |
| thesis/phase02-registry-methodology-section-4-5 | 2026-05-17 | F | Phase 02 registry methodology framing for Chapter 4 §4.5 (TQ-03); provisional §4.5 writing; Step/Phase closure NOT claimed | current_plan.md | #219 (merged 2026-05-17 at master 26210a5d) |
| docs/thesis-ch1-ch4-citation-literature-audit | 2026-05-17 | F | Chapters 1–4 citation & literature support audit (audit-only; verdict send_after_must_fixes; must-fix M-1/M-2/M-3) | current_plan.md | #220 (merged 2026-05-17 at master c6878627) |
| docs/thesis-esportsbench-version-harmonization | 2026-05-18 | F | Audit must-fix M-1: EsportsBench §2.5.5 v8.0/2025-12-31 → v9.0/2026-03-31/dostęp 2026-04-26 harmonisation to match Ch3 | current_plan.md | #221 (merged 2026-05-18 at master 93f02600) |
| docs/thesis-ch1-footer-bib-consolidation | 2026-05-18 | F | Audit must-fix M-2: 7 Chapter-1 footer-only sources → references.bib (append-only) + Mangat2024 footer metadata fix | current_plan.md | #222 (merged 2026-05-18 at master adf93303) |
| docs/thesis-aoestats-rowcount-scope-caveat | 2026-05-18 | F | Audit must-fix M-3 / TQ-05: §4.1.4 aoestats row-count 137=1+136 + on-disk-true [POP:]-scope caveat (ranked_ladder superseded in prose by 1v1_random_map/Tier-4) | current_plan.md | #223 (merged 2026-05-18 at master 855bdbb6) |
| docs/thesis-ch1-ch4-supervisor-handoff-package | 2026-05-18 | F | Capstone Chapters 1–4 supervisor handoff package (relay of merged audit chain #220→#221→#222→#223; user-approved Polish cover note) | current_plan.md | #224 (merged 2026-05-18 at master e095025a) |
| docs/thesis-bibliography-canonicalization | 2026-05-18 | F | bib-only canonicalization — Wu2017 dedup, Elo1978→@book, Buro2003→@inproceedings, Dimitriadis2024 metadata + cleanup report | current_plan.md | #225 (merged 2026-05-19 at master 3238addb) |

## Agent routing

| Role | Reads |
|------|-------|
| Executor | `planning/current_plan.md` (task T01, T02, … as directed) |
| Reviewer-adversarial (final gate, Cat A/F) | `planning/current_plan.md` + diff |
| Reviewer-deep (final gate, Cat B/D) | `planning/current_plan.md` + diff |
| Reviewer (final gate, Cat C/E) | diff only |
