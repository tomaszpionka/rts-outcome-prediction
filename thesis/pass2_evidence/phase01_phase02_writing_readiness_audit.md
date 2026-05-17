# Phase 01 / Phase 02 Writing Readiness Audit

**Date:** 2026-05-17
**Author:** planner-science (claude-opus-4-7), invoked by Category E docs-only PR `docs/thesis-phase01-phase02-writing-readiness-audit`
**Scope:** cross-dataset (sc2egset + aoestats + aoe2companion); cross-phase (Phase 01 + Phase 02)
**Purpose:** Map existing on-disk Phase 01/02 evidence to thesis sections; rank sections by drafting safety; enumerate claims that MUST NOT appear in the thesis until their evidence exists.

**Document type:** Pass-2 evidence (read-only consolidation; not a thesis chapter draft). Consumed by future Category F writing PRs and by `@planner-science` when scoping any Phase 02 ROADMAP work.

**Not consumed by:** Phase 02 execution (the audit does not change spec versions, ROADMAP entries, status YAMLs, or notebook lineage). The audit catalogues what is and is not currently citable; it does not extend that scope.

---

## 1. Executive summary

### 1.1 State of evidence at audit time

- **Phase 01: complete across all three datasets.** `PHASE_STATUS.yaml` shows Phase 01 = complete and Phase 02 = not_started for sc2egset, aoestats, and aoe2companion. `notebook_regeneration_manifest.md` reports 86 `confirmed_intact`, 7 `not_yet_assessed`, 0 `flagged_stale`, 0 `regenerated_pending_log` across all Phase 01 notebooks (last refresh: 2026-05-05).
- **Phase 02: SC2EGSet only.** SC2EGSet Step 02_01_01 has emitted a provisional feature-family registry artifact (CSV + MD) at `validated_through = V-9` (PR #216; merged 2026-05-16 as v3.52.0). Step closure is NOT claimed; ROADMAP, STEP_STATUS, PIPELINE_SECTION_STATUS, PHASE_STATUS untouched. aoestats and aoe2companion have ROADMAP-stub-only entries for Step 02_01_01 (PR #211, 2026-05-07); no artifact, no notebook execution.
- **Phase 02 contract triplet LOCKED.** `CROSS-02-00-v3.0.1` (input contract), `CROSS-02-01-v1.0.1` (post-materialization leakage-audit protocol), `CROSS-02-02-v1.0.1` (feature-engineering plan), `CROSS-02-03-v1.0.1` (design-time temporal feature audit protocol) all LOCKED 2026-05-06. These define the Phase 02 readiness scaffolding but do not themselves materialize features.

### 1.2 What can be written NOW (Tier 1 / Tier 2)

- **Dataset descriptions for all three corpora** (§4.1.1 SC2EGSet, §4.1.2 aoestats + aoe2companion in `04_data_and_methodology.md`) — Phase 01 sections 01_01–01_04 fully cited; CONSORT tables present; numerical claims trace to on-disk JSON/MD artifacts. Existing drafts at `DRAFTED` per `WRITING_STATUS.md`.
- **Data acquisition methodology** (file inventories, schema discovery, ingestion strategy, identity resolution, cleaning rules, missingness handling) — all backed by `01_01_*` through `01_04_*` step artifacts under each dataset's `reports/artifacts/01_exploration/`.
- **Dataset limitations and caveats** — aoestats Tier 4 semantic opacity, aoe2companion ID 6/ID 18 mixed-mode, SC2EGSet tournament-not-ladder population, SC2 MMR 83.95% missingness, AoE2 in-game telemetry absence, cross-region fragmentation (SC2). Source: `aoe2_ladder_provenance_audit.md`, `cross_dataset_comparability_matrix.md`, `phase01_closeout_summary.md`, per-dataset `INVARIANTS.md` §2.
- **Data leakage audit methodology** (Phase 01 protocol design + post-materialization gate design) — backed by `CROSS-02-01-v1.0.1` and the Phase 01 `leakage_audit_*.json` / `01_05_06/08_leakage_audit*` artifacts.
- **Phase 02 registry design rationale** (what a registry is, why a provisional artifact exists, what V-9 covers vs defers) — backed by `CROSS-02-03-v1.0.1` §4 (D1–D15) and the SC2EGSet registry MD's verbatim disclaimer.
- **Phase 01 temporal panel EDA findings** (PSI, ICC, survivorship, quarterly grain, reference window selection) — backed by `01_05_*` artifacts across all three datasets.

### 1.3 What must wait for Phase 03 (Tier 4)

- Temporal split strategy (concrete numerical split boundaries, fold sizes, purge/embargo window sizes per dataset).
- Baseline model performance (any accuracy / AUC / log-loss / Brier number).
- Statistical-comparison protocol applied to actual classifier outputs (Friedman, Wilcoxon-Holm, Bayesian-ROPE results).
- Cold-start threshold value `K`, pseudocount `m`, smoothing strength `α`. `CROSS-02-02-v1.0.1` §9 declares these as gates, not constants.

### 1.4 What must wait for AoE2 Phase 02 (Tier 5)

- Cross-game feature parity claims (e.g., "aoestats and aoe2companion share the same feature catalog as SC2EGSet").
- Cross-game model parity (e.g., "the same classifier hyper-parameters apply"). Per `CROSS-02-00-v3.0.1` §4 / Invariant I8, per-dataset encoders are required and cross-game pooled encoders are forbidden.
- Final model comparison narrative across SC2 ↔ AoE2.

### 1.5 Highest-risk overclaim areas (must NOT be drafted yet)

1. **"Phase 02 is complete" / "Step 02_01_01 is closed."** SC2EGSet registry artifact is provisional (`partial_coverage_v9_baseline`); Step 02_01_01 ROADMAP `continue_predicate` is a 3-clause conjunction satisfying only clause 1.
2. **"Final feature catalog."** Only a provisional 26-row registry exists for SC2EGSet; aoestats and aoe2companion have only ROADMAP stubs.
3. **"Leakage-free features."** Pre-materialization design-time audit (CROSS-02-03) is satisfied at `V-9` for SC2EGSet; post-materialization audit (CROSS-02-01) has NOT been re-run for Phase 02 (no Phase 02 column has been materialized yet).
4. **"SC2 tracker_events fully validated."** GATE-14A6 outcome is `narrowed`, not `closed`; 3 of 15 tracker feature families remain `blocked_until_additional_validation`.
5. **"AoE2 datasets are comparable to SC2EGSet at Phase 02 readiness."** They are NOT; AoE2 Phase 02 is ROADMAP-stub only.
6. **"Tabular ML outperforms GNN" / "GNN outperforms tabular."** No model has been trained.
7. **Any "ranked ladder" framing of aoestats or of aoe2companion combined ID 6 + ID 18 without the qualifier.** Risk-register RISK-01 through RISK-05 are explicit on this.

---

## 2. Evidence matrix by thesis section

Status values: `ready` (fully evidence-backed, can draft now) / `partial` (some sub-claims ready, some blocked) / `blocked` (waiting on later phase / dataset).

Reviewer routing: `normal` (`@reviewer`) / `reviewer-deep` (multi-spec / cross-dataset) / `reviewer-adversarial` (Phase 03+ methodology-sensitive, or methodology-claim load-bearing).

| # | Proposed thesis section | Claim type | Dataset(s) | Evidence artifact(s) | Status | Required caveat | Can draft now? | Reviewer required |
|---|------------------------|------------|------------|---------------------|--------|-----------------|----------------|-------------------|
| 1 | Problem statement / motivation (§1.1, §1.2) | framing + literature | n/a | `WRITING_STATUS.md` shows §1.1 `REVISED`; §1.2 `DRAFTABLE` | partial | Cross-game asymmetry framing (mechanics / data regime / population / feature availability) — RISK-05/06 | yes — refinement only | reviewer-deep |
| 2 | Research questions (§1.3, §1.4) | framing | n/a | `WRITING_STATUS.md` §1.3 `REVISED`; §1.4 `REVISED` | partial | RQ3 hypothesis hedged for four-confound disclaimer per RISK-06/25; AoE2 50-civ count hedged for DLC roster-instability | yes — refinement only | reviewer-deep |
| 3 | Related work — RTS prediction literature (§3.2 SC2; §3.4 AoE2) | literature | n/a | `WRITING_STATUS.md` §3.2 `DRAFTED`; §3.4 `REVISED` post-T14 | ready | None at literature-survey layer; defer model-comparison claims to Phase 05 | yes | reviewer-deep |
| 4 | Related work — research gap §3.5 (Luka 1–4) | literature synthesis | n/a | `WRITING_STATUS.md` §3.5 `DRAFTED` post-T14; 2 [REVIEW]/[NEEDS CITATION] flags remain | partial | Luka 3 EsportsBench v9.0 / 2026-03-31 verified; AoE2 absence verified; Pass-2 PDF read still required for Table 2 metric inventory | yes — Pass-2 verification ongoing | reviewer-deep |
| 5 | SC2EGSet dataset description (§4.1.1) | data-fed | sc2egset | `01_01_01_file_inventory.{json,md}`, `01_02_*` schema+EDA, `01_03_01_systematic_profile.*`, `01_03_02_true_1v1_profile.*`, `01_04_01_data_cleaning.*`, `01_04_02_post_cleaning_validation.*`, `01_04_03_minimal_history_view.*`, `01_04_04_identity_resolution.*`, `01_04_04b_worldwide_identity.*` | ready (DRAFTED) | Bialecki et al. 2023 dataset paper citation; Zenodo CC-BY 4.0 license; CONSORT flow already present; in-game telemetry caveat per GATE-14A6 | yes | reviewer-deep |
| 6 | aoestats dataset description (§4.1.2.1) | data-fed | aoestats | `01_01_01_file_inventory.{json,md}`, `01_02_*`, `01_03_01_systematic_profile.*`, `01_03_02_true_1v1_profile.*`, `01_04_*`, `01_04_03b_canonical_slot_amendment.*`, `01_04_06_old_rating_temporal_audit.*`, `01_04_07_old_rating_conditional_annotation.*` | ready (DRAFTED) | aoestats Tier 4 semantic opacity wording (NEVER "ranked ladder" without qualification) — RISK-04 | yes | reviewer-deep |
| 7 | aoe2companion dataset description (§4.1.2.2) | data-fed | aoe2companion | `01_01_01_file_inventory.{json,md}`, `01_02_*`, `01_03_01_systematic_profile.*`, `01_03_02_true_1v1_profile.*`, `01_04_*`, dual cadence (Parquet + CSV) | ready (DRAFTED) | aoe2companion ID 6 (`rm_1v1`, Tier 2) vs ID 18 (`qp_rm_1v1`, Tier 3); combined = mixed-mode (NEVER "ranked ladder only") — RISK-01/02/03 | yes | reviewer-deep |
| 8 | Dataset limitations / caveats (§4.1.3 + §4.1.4) | data-fed synthesis | all 3 | `cross_dataset_phase01_rollup.md`, `aoe2_ladder_provenance_audit.md`, `cross_dataset_comparability_matrix.md`, `methodology_risk_register.md` RISK-01..26 | ready (DRAFTED) | Five-axis bounded comparability framing (game / data regime / population / feature availability / inference) is binding — RISK-05/06 | yes | reviewer-adversarial (population framing is examiner-facing factual risk) |
| 9 | Data acquisition methodology (§4.2.1 Ingestion) | data-fed | all 3 | `01_01_*`, `01_02_01_duckdb_pre_ingestion.*`, `01_02_02_duckdb_ingestion.*`, `01_02_03_raw_schema_describe.*` | ready (DRAFTED) | Three-stream SC2 ingestion (replays_meta / replay_players / events) vs union_by_name aoestats Parquet vs aoe2companion Parquet+CSV; I10 relative-filename invariant binding | yes | reviewer-deep |
| 10 | Schema / ingestion methodology — VIEW design + I10 invariant (§4.2.1 Ingestion subsection) | data-fed + methodology | all 3 | `data/db/schemas/raw/*.yaml`, `data/db/schemas/views/*.yaml` for all 3 datasets; `CROSS-02-00-v3.0.1` §2 (input contract VIEWs) | ready (DRAFTED) | `matches_history_minimal` per-dataset row counts (44,418 sc2egset / 35,629,894 aoestats / 61,062,392 aoe2companion) + per-dataset `player_history_all` column counts (38 / 15 / 19) | yes | reviewer-deep |
| 11 | Cleaning and identity resolution (§4.2.2, §4.2.3) | data-fed | all 3 | `01_04_01_data_cleaning.{json,md,missingness_ledger.csv}`, `01_04_02_post_cleaning_validation.*`, `01_04_04_identity_resolution.*`, `01_04_04b_worldwide_identity.*` (sc2egset only), `01_04_03b_canonical_slot_amendment.*` (aoestats only), `01_04_05_i5_diagnosis.*` (aoestats only), per-dataset `INVARIANTS.md §2` | ready (DRAFTED + REVISED) | I2 5-branch procedure: sc2egset Branch (iii) `player_id_worldwide`; aoestats Branch (v) structurally-forced; aoe2companion Branch (i) API-namespace `profileId` (rename-stable, 2.57%/3.55%). aoestats `canonical_slot` skill-orthogonal slot identity. aoestats per-slot `[PRE-canonical_slot]` flag (§4.4.6). | yes | reviewer-deep |
| 12 | Temporal panel EDA findings (§4.1.3 + §4.4.5 ICC) | data-fed | all 3 | `01_05_01_quarterly_grain.*`, `01_05_02_psi_*.*`, `01_05_03_*stratification*.*`, `01_05_04_*survivorship*.*`, `01_05_05_*icc*.*`, `01_05_06_*dgp*` (or `temporal_leakage_audit`), `01_05_07_phase06_interface.*`, `01_05_08_*leakage_audit*.*`, `01_05_09_gate_memo.*` | ready (DRAFTED + REVISED) | ICC ANOVA values: sc2egset 0.0463 [0.0283, 0.0643] / aoestats 0.0268 [0.0148, 0.0387] / aoe2companion 0.003013 [0.001724, 0.004202]; reference-window selection per patch 66692 (uniqueness anchor) — §4.4.5 Tabela 4.7 | yes | reviewer-deep |
| 13 | Data leakage audit methodology — Phase 01 + Phase 02 protocol design (§4.4.3) | methodology | all 3 | `CROSS-02-01-v1.0.1`, `01_05_06/08_*leakage_audit*` for all 3 datasets, `phase01_audit_summary_2026-04-21.md` | ready (DRAFTABLE) | Phase 01 leakage audit complete; Phase 02 post-materialization audit gate (CROSS-02-01-v1.0.1 §5) is mandatory but NOT YET RUN for Phase 02 (no Phase 02 column has been materialized yet) | yes — design-only; do not claim post-Phase-02 clearance | reviewer-adversarial (methodology-claim load-bearing) |
| 14 | Phase 02 feature registry design (§4.5 conceptual) | methodology | sc2egset (lead) + cross | `CROSS-02-02-v1.0.1` (plan), `CROSS-02-03-v1.0.1` (design-time audit, D1–D15); per-dataset ROADMAP Step 02_01_01 entries | ready (DRAFTABLE) | Three prediction settings (`pre_game`, `history_enriched_pre_game`, `in_game_snapshot`); model-input grain per CROSS-02-02 §4.2; cold-start G-CS-1..G-CS-6 gates (CROSS-02-02 §9.1) | yes — design-only | reviewer-adversarial |
| 15 | Phase 02 provisional registry artifact (§4.5 artifact) — SC2EGSet only | data-fed | sc2egset | `02_01_01_feature_family_registry.csv` (26 rows), `02_01_01_feature_family_registry.md` (verbatim disclaimer + per-dimension deferred-coverage table); `notebook_regeneration_manifest.md` row with `partial_coverage_v9_baseline` token | partial | MUST cite alongside the future CROSS-02-01 post-materialization audit; registry alone does NOT constitute Phase 02 leakage clearance. Closure status `partial`. | yes — with explicit "provisional" framing | reviewer-adversarial |
| 16 | Phase 03 temporal split methodology (§4.4.1, §4.4.2) | methodology | all 3 (planned) | None yet on disk; future `03_01_*` ROADMAP entries | blocked | Phase 03 not started any dataset | NO | reviewer-adversarial (when drafted) |
| 17 | Phase 03 baseline models (§4.4.7, §5.x) | model-fed | all 3 | None | blocked | Phase 03 not started | NO | reviewer-adversarial |
| 18 | Cross-game comparability claims (§4.4.4 cross-game subsection; Chapter 6 §6.x) | methodology + framing | sc2egset + aoe2 | `cross_dataset_comparability_matrix.md` (five-axis framing) — design-only | partial | Five-axis framing IS draftable now (methodology-design layer); concrete cross-game comparisons require both datasets at Phase 05 (BLOCKED) | partial — framing yes; numbers NO | reviewer-adversarial |
| 19 | Final model results (§5.x, §6.x) | model-fed | all 3 | None | blocked | All Phase 03+ not started | NO | reviewer-adversarial |
| 20 | SC2 tracker-event eligibility decision (§4.3 SC2 telemetry scope) | data-fed methodology | sc2egset | `01_03_05_tracker_events_semantic_validation.{json,md}`, `tracker_events_feature_eligibility.csv` (15 rows) | ready (DRAFTABLE; not yet drafted in chapter prose) | GATE-14A6 outcome: `narrowed`. 12 planned-yes rows (5 eligible_for_phase02_now + 7 eligible_with_caveat) + 3 blocked. `slot_identity_consistency` is sanity gate, NOT model input. Tracker-derived features are never pre-game. | yes — with GATE-14A6 framing | reviewer-adversarial |
| 21 | Evaluation metrics design (§2.6 + §4.4.4) | literature + methodology | n/a | `WRITING_STATUS.md` §2.6 `REVISED`; §4.4.4 `REVISED` | partial | ECE explicitly demarked as descriptive (NOT proper scoring rule per Gneiting & Raftery 2007) — RISK-14; Brier + log-loss as primary | yes — refinement only | reviewer-deep |
| 22 | Within-game vs cross-game statistical comparison (§2.6.3, §4.4.4, §4.1.4) | methodology | n/a | `WRITING_STATUS.md` §4.4.4 `REVISED` PR-TG1 candidate-list framing | partial | N=2 cross-game inapplicability of Friedman per Demsar 2006 §3.1.3 (PDF location pending Pass-2 verification — F5.6 flag); candidate-set framing for within-game | yes — candidate framing only | reviewer-adversarial |

---

## 3. SC2EGSet Phase 01 review

`PHASE_STATUS.yaml` (sc2egset): Phase 01 = complete; Phase 02 = not_started.
`PIPELINE_SECTION_STATUS.yaml` (sc2egset): all of 01_01..01_06 = complete.

### 3.1 Pipeline Section 01_01 — Data Acquisition & Source Inventory

- **Steps:** 01_01_01 (File Inventory, complete 2026-04-09), 01_01_02 (Schema Discovery, complete 2026-04-12).
- **Key artifacts on disk:** `01_01_01_file_inventory.{json,md}`, `01_01_02_schema_discovery.{json,md}`.
- **Thesis-ready:** SC2EGSet replaypack count, total replays, tournament categorisation, date range (2016–2024), file size totals, source DOI to Zenodo and to Bialecki et al. 2023 Scientific Data paper. §4.1.1.1 corpus framing.
- **Background only:** byte-level schema discovery (replays_meta vs replay_players vs three event streams).
- **Caveats:** None at this step; CC-BY 4.0 license verification at Zenodo is a [REVIEW] flag in §4.1.1.

### 3.2 Pipeline Section 01_02 — Exploratory Data Analysis (Tukey-style)

- **Steps:** 01_02_01–01_02_07 (all complete 2026-04-13 to 2026-04-15).
- **Key artifacts on disk:** `01_02_01_duckdb_pre_ingestion.*`, `01_02_02_duckdb_ingestion.*`, `01_02_03_raw_schema_describe.*`, `01_02_04_univariate_census.*` (including categorical_profiles for selectedRace), `01_02_05_visualizations.md` + 14 plots, `01_02_06_bivariate_eda.*` + 9 plots, `01_02_07_multivariate_analysis.*` + 2 plots.
- **Thesis-ready:** Race distribution, MMR distribution (MMR=0 spike → 83.95% missingness ledger), APM distribution, duration distribution, replay date histogram, top-20 maps, top-20 clan tags. §4.1.1 univariate description.
- **Background only:** PCA biplot/scree (multivariate context only; not a thesis-claim source).
- **Caveats:** All in-game columns (APM, SQ, supplyCappedPercent) carry temporal annotations per Invariant I3 — citable as descriptive distributions, but never as pre-game features.

### 3.3 Pipeline Section 01_03 — Systematic Data Profiling

- **Steps:** 01_03_01 (Systematic Data Profiling), 01_03_02 (True 1v1 Match Identification), 01_03_03 (Table Utility Assessment), 01_03_04 (Event Table Profiling), 01_03_05 (Tracker Events Semantic Validation — completed 2026-05-05).
- **Key artifacts on disk:** `01_03_01_systematic_profile.*`, `01_03_02_true_1v1_profile.*`, `01_03_03_table_utility.*`, `01_03_04_event_profiling.*`, `01_03_05_tracker_events_semantic_validation.{json,md}`, `tracker_events_feature_eligibility.csv` (15 rows).
- **Thesis-ready:** 1v1 identification yield (22,379 replays after true-1v1 filter; 555 Random race replays; 26 Undecided), event table profile (62,003,411 tracker events; PlayerStats every 10s; UnitBorn coverage stable across 9 years), GATE-14A6 outcome: `narrowed`.
- **Background only:** 01_03_03 table utility assessment.
- **Caveats:** GATE-14A6 = `narrowed`, NOT `closed`. Full tracker scope is not closed. 12 planned-yes rows + 3 `blocked_until_additional_validation` rows (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`). Tracker-derived features are never pre-game (Amendment 2 / Invariant I3).

### 3.4 Pipeline Section 01_04 — Data Cleaning

- **Steps:** 01_04_00 (Source Normalization), 01_04_01 (Data Cleaning), 01_04_02 (Data Cleaning Execution + Duration Augmentation ADDENDUM 2026-04-18), 01_04_03 (Minimal Cross-Dataset History View), 01_04_04 (Identity Resolution), 01_04_04b (Worldwide Identity VIEW — decomposition-based), 01_04_05 (Cross-Region Fragmentation Phase 01 Annotation, completed 2026-04-21).
- **Key artifacts on disk:** `01_04_00_source_normalization.*`, `01_04_01_data_cleaning.{json,md,missingness_ledger.csv}`, `01_04_02_post_cleaning_validation.*`, `01_04_02_duration_augmentation.*`, `01_04_03_minimal_history_view.*`, `01_04_04_identity_resolution.*` + `01_04_04_cross_region_nicknames.csv` + `01_04_04_within_region_handle_collisions.csv`, `01_04_04b_worldwide_identity.*`, `01_04_05_cross_region_annotation.*`.
- **Thesis-ready:** Source normalization win_pct 52.27%; matches_long_raw 44,418 row count; matches_flat_clean 22,209 matches / 44,418 rows / 30 cols (post-duration ADDENDUM); 18 cleaning assertions PASS; missingness ledger (MMR 83.95%, APM 2.53%, clanTag, highestLeague); I2 Branch (iii) `player_id_worldwide` (R-S2-G-P toon_id format); migration_rate ≈ 12%; within-region collision_rate 30.6%; `is_cross_region_fragmented` BOOLEAN column on `player_history_all` (38 cols post-AMENDMENT 2026-04-21).
- **Background only:** Detailed within-region collision CSVs.
- **Caveats:** RISK-20 cross-region fragmentation: W=30 FAIL verdict (median rolling30 undercount = 16.0 games; p95 = 29.0). Phase 02 MUST NOT hard-code a retention percentage; one of three handling paths (strict exclusion / dual feature paths / sensitivity indicator) must be selected empirically in Phase 02.

### 3.5 Pipeline Section 01_05 — Temporal & Panel EDA

- **Steps:** 01_05_01 (Q1 Quarterly Grain), 01_05_02 (Q2 PSI Quarterly), 01_05_03 (Q3 Stratification), 01_05_04 (Q4 Triple Survivorship), 01_05_05 (Q6 Variance Decomposition & ICC), 01_05_06 (Q8 DGP Diagnostics), 01_05_07 (Phase 06 Interface), 01_05_08 (Q7 Temporal Leakage Audit), 01_05_09 (Exit Memo), 01_05_10 (Cross-Region History Impact, extra step).
- **Key artifacts on disk:** `quarterly_row_counts_sc2egset.{csv,md}`, `psi_sc2egset.csv` + `psi_quarterly_sc2egset.md` + `plots/psi_vs_quarter_sc2egset.png`, `tournament_era_sc2egset.{csv,md}` + `tournament_tier_lookup.csv`, `survivorship_*.csv` + `survivorship_sc2egset.md`, `variance_icc_sc2egset.{csv,md}` + `icc.json` + `plots/icc_player_vs_faction.png`, `dgp_diagnostic_sc2egset.*` + plot, `phase06_interface_sc2egset.{csv,md,schema.json}`, `leakage_audit_sc2egset.{json,md}`, `01_05_09_gate_memo.md`, `cross_region_history_impact_sc2egset.{json,md}`.
- **Thesis-ready:** Patch-regime stratification, PSI quarterly drift, survivorship sensitivity, ICC ANOVA 0.0463 [0.0283; 0.0643] (n_obs=4034, n_groups=152), 35/35 `[POP:tournament]` rows in Phase 06 interface, `ref_start=2022-08-29` / `ref_end=2022-12-31` for leakage audit.
- **Background only:** Tournament tier lookup detail.
- **Caveats:** ICC CI method UNVERIFIED for sc2egset (icc.json does not name CI method explicitly — [UNVERIFIED] in Tabela 4.7). Cross-region history-impact step `01_05_10` is supplementary; not directly thesis-cited.

### 3.6 Pipeline Section 01_06 — Decision Gates

- **Steps:** 01_06_01 (Data Dictionary), 01_06_02 (Data Quality Report), 01_06_03 (Risk Register), 01_06_04 (Modeling Readiness Decision).
- **Key artifacts on disk:** `data_dictionary_sc2egset.{csv,md}`, `data_quality_report_sc2egset.md`, `risk_register_sc2egset.{csv,md}`, `modeling_readiness_sc2egset.md`.
- **Thesis-ready:** Modeling readiness verdict (`READY_WITH_DECLARED_RESIDUALS`), risk register entries, data dictionary post-correction (37 cols + 1 amendment).
- **Background only:** Data dictionary CSV (background; used to verify column classifications).
- **Caveats:** Modeling readiness is for Phase 02 entry, NOT for thesis modeling claims. Risk register backed by `methodology_risk_register.md` (T10).

---

## 4. AoE2 Phase 01 review

### 4.1 aoestats

`PHASE_STATUS.yaml` (aoestats): Phase 01 = complete; Phase 02 = not_started.

#### 4.1.1 Pipeline Section 01_01 — Acquisition

- **Steps:** 01_01_01 (File Inventory, 172 matches/ + 171 players/ Parquet files, 3,773.61 MB, range 2022-08-28 — 2026-02-07, 3 inter-file gaps + 1 extra gap in players/), 01_01_02 (Schema Discovery).
- **Key artifacts:** `01_01_01_file_inventory.{json,md}` (provenance for 43-day gap, 8-day gaps), `01_01_02_schema_discovery.{json,md}`.
- **Thesis-ready:** File inventory + temporal coverage; weekly cadence; 43-day post-patch 2024-07 gap with `.md` + `.py` derivation pair (I9 provenance).
- **Caveats:** aoestats is **Tier 4 semantic opacity**. Source label MUST be quoted as "aoestats 1v1 Random Map records (source label `leaderboard='random_map'`; queue semantics unverified)". Never "ranked ladder". — RISK-04.

#### 4.1.2 Pipeline Section 01_02 — EDA + 01_03 Profiling

- **Steps:** 01_02_01–01_02_07; 01_03_01–01_03_03.
- **Key artifacts:** Standard 01_02_*/01_03_* JSON+MD set + plots (categorical bars, numeric histograms, ELO distributions, opening non-null, leaderboard distribution, monthly match count, schema-change boundary, IQR outlier summary, PCA biplot/scree, Spearman heatmap).
- **Thesis-ready:** profile_id cardinality 641,662 (max 24,853,897); 30,690,651 matches_raw → 17,815,944 1v1; Jaccard 0.958755; civ count 50 (full DLC roster at end of window).
- **Caveats:** Same Tier 4 source-label discipline applies everywhere.

#### 4.1.3 Pipeline Section 01_04 — Cleaning

- **Steps:** 01_04_00 (Source Normalization, 52.27% side win_pct, matches_long_raw 107,626,399), 01_04_01 (Data Cleaning, p0_civ n_distinct=50, missingness ledger sentinels), 01_04_02 (Data Cleaning Execution, matches_1v1_clean 17,814,947, R08 -997, 20–22 cols, 33 assertions PASS), 01_04_02 duration augmentation ADDENDUM, 01_04_03 (Minimal History View), 01_04_03b (canonical_slot amendment, 2026-04-20), 01_04_04 (Identity Resolution, Branch (v) structurally-forced), 01_04_05 (Team-Slot Asymmetry I5 Diagnosis, C4-04 80.3% / +11.9 ELO), 01_04_06 (old_rating Temporal Audit, FAIL verdict), 01_04_07 (old_rating CONDITIONAL_PRE_GAME Annotation, 2026-04-21).
- **Key artifacts:** `01_04_00..07_*.{json,md}` + `01_04_01_missingness_ledger.{csv,json}` + `01_04_02_post_cleaning_validation.*` + `01_04_02_duration_augmentation_validation.*` + `01_04_03b_canonical_slot_amendment.*` + `01_04_05_i5_diagnosis.*` + `01_04_06_old_rating_temporal_audit.*` + `01_04_07_old_rating_conditional_annotation.*`.
- **Thesis-ready:** Cleaning typology (R01..R08); canonical_slot derivation (hash on match_id); per-slot `[PRE-canonical_slot]` flag protocol; old_rating CONDITIONAL_PRE_GAME with N*=7 days empirical threshold + SCOPE=random_map_only.
- **Caveats:** **old_rating is CONDITIONAL_PRE_GAME, not unconditional PRE_GAME.** Use only where `leaderboard='random_map' AND (time_since_prior_match_days < 7 OR IS NULL)`. **canonical_slot is aoestats-only** — NOT in cross-dataset UNION ALL (CROSS-02-00-v3.0.1 §5.2). **`new_rating` is POST_GAME**, forbidden as feature.

#### 4.1.4 Pipeline Section 01_05 — Temporal & Panel EDA

- **Steps:** 01_05_01 (Quarterly Grain), 01_05_02 (PSI Pre-Game Features), 01_05_03 (Stratification + Patch Regime), 01_05_04 (Survivorship Triple), 01_05_05 (ICC), 01_05_06 (Temporal Leakage Audit v1), 01_05_07 (DGP Diagnostics Duration), 01_05_08 (Phase 06 Interface), 01_05_09 (Gate Memo).
- **Key artifacts:** `quarterly_grain_row_counts.{csv,json,md}`, `01_05_02_psi_summary.{json,md}` + `psi_aoestats_2023-Q1..Q4.csv` + `psi_aoestats_2024-Q1..Q4.csv` + `psi_aoestats_counterfactual_2023Q1ref.csv`, `01_05_03_patch_regime_summary.{json,md}` + `patch_*.csv` (5 files), `01_05_04_survivorship_summary.{json,md}` + `survivorship_*.csv`, `01_05_05_icc_results.{json,md}` + `icc_cohort_profile_ids_n{5,10,20}.csv`, `01_05_06_temporal_leakage_audit_v1.{json,md}`, `01_05_07_dgp_diagnostic_summary.{json,md}` + `dgp_diagnostic_aoestats_2022-Q3Q4ref..2024-Q4.csv`, `01_05_08_phase06_interface_schema_validation.{json,md}` + `phase06_interface_aoestats.csv` (137 rows), `01_05_09_gate_memo.md`.
- **Thesis-ready:** ICC ANOVA 0.0268 [0.0148; 0.0387]; n_players=744; reference window selected via patch 66692 (sole patch fully covering pre-registration window). Phase 06 interface CSV.
- **Caveats:** aoestats 744-player cohort at the reference window — defended at §4.1.2.1 + §4.4.5 via Gelman 2007 §11-12 small-cluster argument. 137 rows of `phase06_interface_aoestats.csv` carry NO `[POP:]` tag — scope implicit via spec §0 + cleaning rule R02 (`leaderboard='random_map'`); `[PRE-canonical_slot]` annotation on 30 of 136 data rows (post-F6 backfill 2026-04-19).

#### 4.1.5 Pipeline Section 01_06 — Decision Gates

- **Steps:** 01_06_01..04.
- **Key artifacts:** `data_dictionary_aoestats.{csv,md}` (post-canonical_slot amendment: 10-col contract), `data_quality_report_aoestats.md`, `risk_register_aoestats.{csv,md}`, `modeling_readiness_aoestats.md`.
- **Thesis-ready:** Modeling readiness GO-FULL (post-canonical_slot amendment 2026-04-20); risk register entries; cleaning rule R01–R08 + Tabela 4.6 typology.
- **Caveats:** Modeling readiness is Phase 02 entry, NOT modeling claim.

### 4.2 aoe2companion

`PHASE_STATUS.yaml` (aoe2companion): Phase 01 = complete; Phase 02 = not_started.

#### 4.2.1 Pipeline Section 01_01 — Acquisition

- **Steps:** 01_01_01 (File Inventory: 2073 matches/ + 2072 ratings/ Parquet+CSV, 9,387.80 MB, daily cadence, no gaps), 01_01_02 (Schema Discovery: VARCHAR inference for daily CSV).
- **Key artifacts:** `01_01_01_file_inventory.{json,md}`, `01_01_02_schema_discovery.{json,md}`.
- **Thesis-ready:** Daily-cadence dual-source ingestion (Parquet matches + CSV ratings + Parquet leaderboards + Parquet profiles); 1-day gap in ratings 2025-07-11.
- **Caveats:** aoe2companion is **mixed-mode**: `internalLeaderboardId IN (6, 18)`. ID 6 = `rm_1v1` (Tier 2 ranked candidate, ~54M rows); ID 18 = `qp_rm_1v1` (Tier 3 quickplay/matchmaking, ~7M rows; external API unavailable as of 2026-04-26). Combined = mixed-mode, NOT ranked-ladder-only. — RISK-01/02/03.

#### 4.2.2 Pipeline Sections 01_02 + 01_03

- **Steps:** standard 01_02_*/01_03_* set.
- **Key artifacts:** standard 01_02_*/01_03_* set; plots include rating null timeline, rating histogram, leaderboard distribution stratification (ID 6 vs ID 18 disaggregated).
- **Thesis-ready:** profileId cardinality 3,387,273 (cross-leaderboard); 683,790 in lb=6+18 cohort; 277,099,059 matches_raw → 40,062,975 rows_per_match=2; name cardinality discrepancy 2,308,187 vs 2,468,478 (Pass 2 to verify).
- **Caveats:** Same mixed-mode source-label discipline.

#### 4.2.3 Pipeline Section 01_04 — Cleaning

- **Steps:** 01_04_00 (Source Normalization, 277,099,059 matches_long_raw rows, side=0 449 anomalous rows), 01_04_01 (Data Cleaning, rating NULL 26.20%, civ 56 distinct, NULL-cluster 11,184 rows), 01_04_02 (Data Cleaning Execution, matches_1v1_clean 30,531,196, R01 -216M, R03 -5052, 48–51 cols), 01_04_02 duration augmentation ADDENDUM, 01_04_03 (Minimal History View, start 2020-07-31 23:30:34 UTC), 01_04_04 (Identity Resolution, Branch (i) API-namespace profileId).
- **Key artifacts:** `01_04_00..04_*.{json,md}` + `01_04_01_missingness_ledger.{csv,json}` + `01_04_02_duration_augmentation.{json,md}`.
- **Thesis-ready:** Cleaning rule R01 retains `internalLeaderboardId IN (6, 18)` (mixed-mode); migration_rate 2.57% / collision_rate 3.55% (post-rm_1v1 scope reconciliation 2026-04-19).
- **Caveats:** **Cross-dataset namespace bridge** to aoestats: VERDICT A, 0.9960 agreement on profileId ↔ profile_id alignment. Rating NULL ~26% (MAR; schema evolution).

#### 4.2.4 Pipeline Section 01_05 — Temporal & Panel EDA

- **Steps:** 01_05_01..09 (analogous to aoestats / sc2egset).
- **Key artifacts:** `01_05_01_quarterly_grain.*`, `01_05_02_psi_shift.*` + `01_05_02_psi_shift_per_feature.csv`, `01_05_03_stratification.*` + `01_05_03_stratification_per_lb.csv`, `01_05_04_survivorship.*`, `01_05_05_icc.*` + 3 icc_sample_profileIds_*k.csv, `01_05_06_dgp_duration.*` + `dgp_diagnostic_aoe2companion_*.csv`, `01_05_07_phase06_interface.*` + `01_05_phase06_interface_aoe2companion.csv` (74 rows + 74/74 `[POP:ranked_ladder]` tags), `01_05_08_leakage_audit.{json,md}`, `01_05_09_gate_memo.md`.
- **Thesis-ready:** ICC ANOVA 0.003013 [0.001724; 0.004202]; n_players_primary=5000; LPM ICC values 0.000491 (5k) and 0.002505 (10k); ANOVA-primary harmonization per cross_dataset rollup §4 item 2 (closes I8 AT RISK flag).
- **Caveats:** aoec-specific spec v1.0.2 divergences: 5k LMM sample-size cap + GLMM omission (AC-R06 LOW). Stratification artifact has T05/Q2 BLOCKER-1 propagation note: `qp_rm_1v1` (leaderboardId=18) label clarification — notebook output intact, only chapter prose may need revision.

#### 4.2.5 Pipeline Section 01_06 — Decision Gates

- **Steps:** 01_06_01..04. **01_06_01 regenerated 2026-04-27 (T16) for `classify()` keyword-priority bug fix** — `rating`/`player_history_all` was misclassified TARGET, now correctly PRE_GAME; `started`/`player_history_all` was misclassified TARGET, now correctly METADATA. **01_06_02 regenerated 2026-04-26 (T07/T08) for mixed-mode wording fix** — R01 description corrected from "Retain 1v1 ranked ladder only" to mixed-mode wording.
- **Key artifacts:** `data_dictionary_aoe2companion.{csv,md}` (post-T16 regen), `data_quality_report_aoe2companion.md` (post-T07/T08 regen), `risk_register_aoe2companion.{csv,md}`, `modeling_readiness_aoe2companion.md`.
- **Thesis-ready:** Modeling readiness verdict; data dictionary post-correction (PRE_GAME 39 / METADATA 17 / TARGET 3); risk register entry AC-R06 LOW.
- **Caveats:** ROADMAP references to `cross_dataset_phase01_rollup.md` use explicit `repo-root` qualifier (cross-dataset artifact lives at `<repo>/reports/...`, not at `<dataset>/reports/...`). Source label discipline applies to every population reference.

---

## 5. Phase 02 review

### 5.1 SC2EGSet Phase 02

- **Step 02_01_01 — Feature-family registry skeleton (sc2egset):** PROVISIONAL artifact emitted 2026-05-16 (PR #216).
- **Artifacts on disk:** `02_01_01_feature_family_registry.csv` (26 data rows, 14 columns including `block` partition); `02_01_01_feature_family_registry.md` (verbatim disclaimer + per-dimension deferred-coverage table).
- **Validation coverage:** V-1 base, V-1 strict, V-2..V-9. Maps to CROSS-02-03-v1.0.1 dimensions: D1 (admissibility); D5-history-side, D6-history-side (partial); D7 (post-game token exclusion); D10 sub-clause 1 (per-player construction symmetry); D11 (cold-start vocabulary, no magic numbers); D13 (SC2 tracker eligibility); D15 (lineage readiness).
- **Deferred to materialization step / post-materialization audit:** D2 (source classification), D3 (source vs model grain), D4-in_game (in-game temporal anchor), D5-in_game (in-game cutoff operator), D6-full (target-game exclusion full), D8 (full-replay aggregate exclusion), D9 (normalization fit-scope).
- **N/A for sc2egset:** D10 sub-clause 2 (aoestats canonical_slot), D12 (source-mode label), D14 (AoE2 source-label).
- **Manifest status token:** `partial_coverage_v9_baseline` (new vocabulary added to `notebook_regeneration_manifest.md` in PR #216).
- **Step 02_01_01 closure:** NOT claimed. ROADMAP `continue_predicate` is a 3-clause conjunction (artifact-check + CROSS-02-01 post-materialization audit re-run + per-family CROSS-02-03 §10 verdicts); this artifact satisfies clause 1 only.

### 5.2 aoestats and aoe2companion Phase 02

- **ROADMAP-stub only.** Step 02_01_01 entries exist in both ROADMAPs (added PR #211, 2026-05-07).
- **No artifact.** No notebook execution; no on-disk feature-family registry CSV/MD for either dataset.
- **No validator.** No `validate_registry_skeleton.py` analogue exists for aoestats or aoe2companion. **V-9 D10 sub-clause 2** (aoestats `canonical_slot` p0/p1 projection symmetry) is explicitly **deferred to a future aoestats-side V-N PR** (per CROSS-02-02-v1.0.1 / CROSS-02-03-v1.0.1 amendment logs and the SC2EGSet registry MD's deferred-dimension table).
- **Implication for thesis writing:** **Phase 02 readiness is asymmetric across datasets at audit time.** Any "Phase 02 is ready" claim MUST be qualified by dataset.

### 5.3 What CAN be written NOW about Phase 02 methodology (design layer)

- The four-spec Phase 02 contract triplet (CROSS-02-00, CROSS-02-01, CROSS-02-02, CROSS-02-03) and its rationale.
- The three prediction settings (`pre_game`, `history_enriched_pre_game`, `in_game_snapshot`) + the `blocked_or_deferred` reservation.
- Per-dataset prediction-setting support matrix (CROSS-02-02 §3.2): AoE2 sources do NOT support `in_game_snapshot` (structurally — no in-game replay telemetry).
- The G-CS-1..G-CS-6 cold-start gate vocabulary as gates, not constants.
- The G-L-1..G-L-9 design-time leakage check vocabulary.
- The 15-dimension CROSS-02-03 design-time audit table (D1–D15) as a methodology framework.
- The SC2EGSet provisional registry artifact AS PROVISIONAL — citable in §4.5 only alongside the (future) CROSS-02-01 post-materialization audit artifact.

### 5.4 What CANNOT yet be claimed about Phase 02

- Final feature catalog (only a provisional 26-row registry exists for SC2EGSet).
- "Phase 02 is ready" without dataset qualification (aoestats + aoe2companion have ROADMAP stubs only).
- "Step 02_01_01 is closed" (3-clause conjunction satisfies only clause 1 for SC2EGSet; aoestats + aoe2companion are not started).
- Model-ready feature matrix (no Phase 02 column has been materialized).
- Leakage-free feature columns (post-materialization audit has not been run for Phase 02).
- Cold-start threshold values (`K`, `m`, `α` deferred to Phase 02 ROADMAP step that empirically derives them).

---

## 6. Literature / theory mapping

The following sources are externally verified (via WebSearch on 2026-05-17 unless noted) and map to thesis sections. Each entry includes the source citation, the relevant thesis section, the one-sentence claim it supports, and any caveat about applicability.

### 6.1 SC2EGSet paper

- **Source:** Białecki, A., et al. (2023). "SC2EGSet: StarCraft II Esport Replay and Game-state Dataset." *Scientific Data* 10:600. DOI [10.1038/s41597-023-02510-7](https://doi.org/10.1038/s41597-023-02510-7); preprint [arXiv:2207.03428](https://arxiv.org/abs/2207.03428).
- **Relevant thesis section:** §4.1.1 (SC2EGSet description), §3.2 (StarCraft prediction literature).
- **Supports:** Origin of the SC2EGSet corpus: 55 tournament replaypacks, 17,930 game-state files extracted via s2protocol from publicly available Battle.net replays of major and premiere StarCraft II tournaments since 2016; dataset published under CC-BY 4.0 on Zenodo.
- **Caveat:** The dataset paper's own outcome-prediction experiments use a different ML pipeline (single-player vs two-player averaged economic features; SVM, XGBoost, logistic classifier) — these are background context, not a baseline this thesis must reproduce.

### 6.2 Data leakage definition (canonical)

- **Source:** Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). "Leakage in data mining: Formulation, detection, and avoidance." *ACM Transactions on Knowledge Discovery from Data* 6(4):15. DOI [10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579). Free PDF on [Semantic Scholar](https://www.semanticscholar.org/paper/Leakage-in-data-mining%3A-formulation%2C-detection%2C-and-Kaufman-Rosset/381de4becac0910d1a74c905a3d579dda3571dbd).
- **Relevant thesis section:** §4.2 (data leakage methodology), §4.4.3 (leakage audit protocol); §1.2 (problem statement framing).
- **Supports:** Canonical definition of leakage as "the introduction of information about the data mining target that should not be legitimately available to mine from"; learn-predict separation as the avoidance principle that this project's strict `<` history cutoff (Invariant I3) and post-materialization audit (CROSS-02-01) operationalize.
- **Caveat:** Kaufman et al. cover diverse leakage mechanisms (target leakage from group-level statistics, time-of-day leakage, etc.); this thesis focuses specifically on temporal leakage in per-player rolling-window features.

### 6.3 Temporal cross-validation (purging + embargo)

- **Source (primary):** López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. Ch. 7 (purged k-fold cross-validation; embargo).
- **Source (secondary, open):** [Wikipedia: Purged cross-validation](https://en.wikipedia.org/wiki/Purged_cross-validation). [Quantinsti blog explainer](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/).
- **Relevant thesis section:** §4.4.1 / §4.4.2 (Phase 03 splitting methodology — Tier 4 BLOCKED at audit time).
- **Supports:** Purging (exclude training samples whose label horizon intersects the test fold) and embargo (buffer after each test fold) as the principled response to path-dependent / serially correlated labels in time-series prediction. Directly applicable to per-player rolling-window features whose target match (game T) participates in the focal player's prior history.
- **Caveat:** López de Prado 2018 develops the protocol for financial prediction with overlapping labels (e.g., trade-execution horizons spanning multiple bars); the per-player per-game prediction setting in this thesis is analogous but not identical (label-overlap structure differs).

### 6.4 Feature store / feature registry concept

- **Source (primary):** [Feast documentation — "What is a Feature Store?"](https://feast.dev/blog/what-is-a-feature-store/) (open-source feature store).
- **Source (secondary):** Google Cloud Blog, ["How Feast feature store streamlines ML development"](https://cloud.google.com/blog/products/databases/how-feast-feature-store-streamlines-ml-development).
- **Source (industry context):** Databricks blog, ["What Is a Feature Store?"](https://www.databricks.com/blog/what-is-a-feature-store).
- **Relevant thesis section:** §4.5 (Phase 02 feature registry methodology).
- **Supports:** A feature registry as a centralized source of truth containing standardized feature definitions and metadata enabling reuse, dependency tracking, ownership, and version lineage. The SC2EGSet Step 02_01_01 provisional registry (`02_01_01_feature_family_registry.csv`) is a minimal hand-curated analogue of this industry pattern, scoped to thesis-grade reproducibility rather than online serving.
- **Caveat:** The Feast / Tecton design is online + offline serving infrastructure for production ML systems. This thesis's registry is the metadata layer only (no online serving); it adapts the metadata pattern (feature_family_id, source_grain, model_input_grain, temporal_anchor, allowed_cutoff_rule, leakage_modes, cold_start_handling, status) for a research-grade methodology audit.

### 6.5 RTS / esports outcome prediction literature

- **Source A:** Yang, P., Harrison, B. E., & Roberts, D. L. (2014). "Identifying patterns in combat that are predictive of success in MOBA games." *Foundations of Digital Games* (FDG); related work in [PLOS ONE 3-D CNN StarCraft II prediction (2022)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0264550).
- **Source B:** [Sánchez-Ruiz, A. A. (2017) "A Machine Learning Approach to Predict the Winner in StarCraft Based on Influence Maps."](https://www.sciencedirect.com/science/article/abs/pii/S1875952116300647) *Entertainment Computing* 19:29–41.
- **Source C:** [Hodge, V. J., et al. (2021). "Win Prediction in Multiplayer Esports."](https://ieeexplore.ieee.org/document/9050617) *IEEE Trans. on Games* 13(4):368–379. Cross-referenced for Dota 2 GBDT-dominance pattern (RQ1 hypothesis support in §1.3).
- **Source D:** Elbert, F., Schenk, A., & Stein, N. (2025). "Hierarchical fixed-effects econometrics applied to AoE2 win prediction." ACM EC 2025 extended abstract (arXiv:2506.04475). Referenced in §3.4.3 + §3.5.
- **Relevant thesis section:** §3.2 (SC2 prediction literature), §3.3 (MOBA + other esports), §3.4 (AoE2 prediction), §3.5 (research gap).
- **Supports:** Existing RTS prediction work uses in-game state features (production-rate snapshots, army composition, influence maps); only a few studies systematically compare a classifier family with calibration metrics. The four-corner research gap (§3.5 Luka 1–4) is narrowed against these prior works.
- **Caveat:** None of these works uses the per-player chronological hold-out protocol this thesis adopts (Invariant I1); cross-method-comparability claims must be qualified.

### 6.6 Tabular ML vs deep learning framing

- **Source:** Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). "Why do tree-based models still outperform deep learning on typical tabular data?" *NeurIPS Datasets and Benchmarks Track*. [arXiv:2207.08815](https://arxiv.org/abs/2207.08815).
- **Relevant thesis section:** §2.4 (ML methods), §1.3 (RQ1 hypothesis), §6.5 (threats to validity — model-class choice).
- **Supports:** Tree-based models (XGBoost, Random Forest) remain SOTA on medium-sized tabular datasets (~10K samples). This grounds the choice of GBDT as a primary classifier for pre-game tabular features. Provides three inductive-bias arguments (robustness to uninformative features, smoothness of decision boundaries, locality) that explain the asymmetry.
- **Caveat:** "Tabular vs GNN" is a distinct framing (graph-structured player history vs flat per-game vector); Grinsztajn et al. 2022 does not directly address graph data. Use as background for the classical-ML-as-primary choice, not as evidence against GNNs.

### 6.7 Dataset documentation / Datasheets for Datasets

- **Source:** Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). "Datasheets for Datasets." *Communications of the ACM* 64(12):86–92. DOI [10.1145/3458723](https://doi.org/10.1145/3458723). Preprint [arXiv:1803.09010](https://arxiv.org/abs/1803.09010).
- **Relevant thesis section:** §4.1 (data chapter framing), §4.1.1.1–§4.1.2.2 (per-corpus motivation / composition / collection / preprocessing / uses / distribution / maintenance), §4.1.4 (population scope).
- **Supports:** The seven-category datasheet structure (Motivation; Composition; Collection Process; Preprocessing, Cleaning, Labeling; Uses; Distribution; Maintenance) gives a defensible template for §4.1.1 / §4.1.2 narrative organization. Bialecki et al. 2023 already partially conforms for SC2EGSet; the AoE2 corpora are third-party aggregations and benefit from datasheet-style discipline to make their semantics auditable.
- **Caveat:** Datasheets for Datasets is a recommendation, not a thesis requirement. The thesis applies the seven-category structure as an organizing principle, not as a verbatim 57-question fill-in.

### 6.8 Statistical comparison of classifiers (Demsar 2006, Garcia-Herrera 2008, Benavoli 2017)

- **Source:** Demsar, J. (2006). "Statistical comparisons of classifiers over multiple data sets." *JMLR* 7:1–30.
- **Source:** García, S., & Herrera, F. (2008). "An extension on 'Statistical comparisons of classifiers over multiple data sets' for all pairwise comparisons." *JMLR* 9:2677–2694.
- **Source:** Benavoli, A., Corani, G., Demšar, J., & Zaffalon, M. (2017). "Time for a change: a tutorial for comparing multiple classifiers through Bayesian analysis." *JMLR* 18(77):1–36.
- **Relevant thesis section:** §2.6.3 (within-game), §2.6.4 (cross-game), §4.4.4 (evaluation metrics).
- **Supports:** Within-game Friedman + Wilcoxon-Holm + Bayesian signed-rank with ROPE protocol; cross-game inapplicability of Friedman at N=2 datasets.
- **Caveat:** Demsar 2006 §3.1.3 location for the N≥5 datasets recommendation is pending PDF verification (F5.6 flag) — refer to Demsar 2006 §3.2 in the meantime.

---

## 7. Drafting queue

Sections ranked safest-to-draft to must-wait, with the ROADMAP step or external source that gates each tier.

### 7.1 Tier 1 — draft now (data/source descriptions, dataset limitations, acquisition methodology, EDA summaries)

- §4.1.1 SC2EGSet description — `DRAFTED`; refinement only.
- §4.1.2.1 aoestats description — `DRAFTED`; refinement only.
- §4.1.2.2 aoe2companion description — `DRAFTED`; refinement only.
- §4.1.3 Data asymmetry acknowledgement — `DRAFTED`; refinement only (RISK-05/06 already framed).
- §4.1.4 Population scope (dataset-conditional framing) — `DRAFTED`; refinement only.
- §4.2.1 Ingestion + I10 invariant — `DRAFTED`; refinement only.
- §4.2.2 Identity resolution — `REVISED`; F3 rewrite complete.
- §4.2.3 Cleaning rules + missingness — `DRAFTED`; refinement only.
- §2.2 / §2.3 game-mechanic background — `REVISED`; refinement only.
- §3.1 traditional sports prediction — `DRAFTED`.
- §3.2 / §3.3 / §3.4 RTS/esports literature — `DRAFTED` or `REVISED`.

### 7.2 Tier 2 — draft with care (Phase 01 methodology, leakage audit methodology, Phase 02 registry design rationale)

- §4.4.5 ICC estimator choice — `DRAFTED`; 4 [REVIEW] flags retained.
- §4.4.6 `[PRE-canonical_slot]` flag — `DRAFTED`; rewritten by T11 to post-F1 state.
- §4.4.4 Evaluation metrics (within-game / cross-game subsections) — `REVISED`; candidate-list framing per PR-TG1; do NOT claim adoption.
- §4.5 Phase 02 registry methodology (NEW section, not yet drafted) — DRAFTABLE; cite CROSS-02-00..03 specs and the SC2EGSet provisional artifact AS PROVISIONAL.
- §4.3 SC2 in-game telemetry scope (NEW subsection, GATE-14A6 framing) — DRAFTABLE; cite `tracker_events_feature_eligibility.csv` 15-row contract.

### 7.3 Tier 3 — draft partially (literature review where theory is safe; model comparison is blocked)

- §3.5 Research gap (Luka 1–4) — `DRAFTED` post-T14; refinement only.
- §2.4 ML methods for classification — `DRAFTED`; refinement only (do NOT claim final model-class adoption decisions).
- §2.5 Player skill rating systems — `REVISED`; refinement only.
- §2.6 Evaluation metrics — `REVISED`; refinement only.

### 7.4 Tier 4 — must wait for Phase 03 (Splitting & Baselines)

- §4.4.1 Temporal splitting strategy (concrete fold boundaries, purge/embargo widths).
- §4.4.2 Statistical comparison protocol with concrete `α`, `ROPE` width.
- §4.4.7 Baseline definitions and Elo/Glicko domain baselines.
- §5.x Experiment results sections (all `BLOCKED`).
- §6.1–6.4 Discussion sections (all `BLOCKED`).

### 7.5 Tier 5 — must wait for AoE2 Phase 02 (and any subsequent cross-game phase)

- §4.5 Cross-dataset feature parity comparison (if drafted in §4.5; or in §4.4.4 cross-game subsection).
- Chapter 5 cross-game experimental results.
- §6.x cross-game generalization discussion.

---

## 8. Forbidden claims list

Each claim is a concrete sentence that **MUST NOT** appear in the thesis until its evidence exists. Each row enumerates: (a) the claim text, (b) why it is currently forbidden (missing evidence), and (c) what evidence would unlock it.

| # | Forbidden claim | Why forbidden (missing evidence) | What evidence unlocks it |
|---|----------------|----------------------------------|--------------------------|
| F1 | "Our system achieved F1 = X.XX / accuracy = X.XX / AUC = X.XX on the test set." | No model has been trained. Phase 03 (Splitting) and Phase 04 (Model Training) are `not_started` for all datasets. | Phase 04 + Phase 05 artifacts; per-dataset `04_*` and `05_*` ROADMAP steps complete. |
| F2 | "Tabular ML outperforms GNN" / "GNN outperforms tabular ML." | No GNN has been trained; no tabular ML has been trained; no comparison exists. | Phase 04 + Phase 05 artifacts for both model families; ablation study per `05_04` Ablation. |
| F3 | "The Phase 02 feature catalog contains [N] features across [K] families." | Only a provisional 26-row family registry exists for SC2EGSet (`partial_coverage_v9_baseline`); aoestats + aoe2companion have ROADMAP stubs only. | (i) Aoestats + aoe2companion analogous registries at V-9 or higher; (ii) materialization step (02_01_02 or successor) for each dataset; (iii) the actual feature catalog (Pipeline Section 02_08). |
| F4 | "Step 02_01_01 is closed" / "Phase 02 is ready across all datasets" / "Phase 02 is complete." | Step 02_01_01 ROADMAP `continue_predicate` is a 3-clause conjunction (artifact-check + CROSS-02-01-v1.0.1 post-materialization audit re-run + per-family CROSS-02-03-v1.0.1 §10 verdicts). SC2EGSet satisfies clause 1 only. aoestats + aoe2companion satisfy none. | (i) Materialization step that produces a `leakage_audit_<dataset>.json` artifact with `verdict = PASS`; (ii) per-family §10 verdicts recorded for every registry row; (iii) STEP_STATUS.yaml flipped to `complete` for Step 02_01_01 with a comment recording the closure. |
| F5 | "aoestats and aoe2companion are at Phase 02 parity with SC2EGSet." | aoestats + aoe2companion Phase 02 = ROADMAP-stub only; no notebook execution, no artifact, no V-9 validator. | aoestats + aoe2companion provisional registry artifacts at `partial_coverage_v9_baseline` (or higher); a published aoestats-side V-N PR closing CROSS-02-03 D10 sub-clause 2 (canonical_slot p0/p1 projection). |
| F6 | "The temporal split strategy generalizes across SC2 and AoE2." | Phase 03 not started any dataset; cross-dataset split-strategy claim has no evidence. | Per-dataset Phase 03 split-validation artifacts; cross-dataset transfer experiment per Phase 06. |
| F7 | "Our features are leakage-free." | CROSS-02-01-v1.0.1 post-materialization audit has NOT been re-run for Phase 02 (no Phase 02 feature column has been materialized yet for any dataset). | Post-materialization `leakage_audit_<dataset>_02_01_*.json` artifact with `verdict = PASS` covering all materialized columns. |
| F8 | "Post-materialization audit has cleared the Phase 02 feature set." | No Phase 02 feature set has been materialized; no post-materialization audit has been run. | Same as F7 plus a complete `features_audited` list covering every materialized column. |
| F9 | "SC2EGSet `tracker_events_raw` semantics are fully validated." | GATE-14A6 outcome is `narrowed`, not `closed`. 3 of 15 tracker feature families remain `blocked_until_additional_validation` (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`). | Future dedicated validation step for each blocked family, per `phase02_readiness_hardening.md` §14A.6 future validation route. |
| F10 | "aoestats records are ranked-ladder matches." | aoestats is Tier 4 semantic opacity; queue type (ranked vs quickplay vs custom-lobby contamination) cannot be verified from available external documentation. | External documentation from aoestats.io confirming queue mapping; OR aoestats source code / API documentation locating the upstream source. Either source is currently absent (verified via aoe2_ladder_provenance_audit.md §4.1.3–§4.1.6, 2026-04-26). |
| F11 | "aoe2companion records (combined ID 6 + ID 18) are ranked-ladder matches." | The combined scope is mixed-mode: ID 6 (`rm_1v1`, Tier 2 ranked candidate, ~54M rows) + ID 18 (`qp_rm_1v1`, Tier 3 quickplay/matchmaking, ~7M rows). External API documentation unavailable as of 2026-04-26. | Future external API documentation from aoe2companion clarifying ID 18 queue semantics; OR an explicit rewrite of the combined-scope label to "mixed-mode" — already drafted in §4.1.3 / §4.1.4 / Tabela 4.4a–4.5. |
| F12 | "We selected feature scaler parameters based on the full dataset distribution." | Invariant I3 normalization-leakage rule forbids global fit. CROSS-02-01 §2.3 + CROSS-02-02 G-CS-6 + G-L-6 require training-fold-only fit. | Training-fold-only scaler-fit code in Phase 02 + post-materialization audit verifying the fit-scope. |
| F13 | "We chose pseudocount `m = X` / cold-start threshold `K = N` because [intuition]." | CROSS-02-02-v1.0.1 §9 G-CS-1 forbids magic numbers; Invariant I7 requires empirical derivation or literature citation. | Training-fold-only empirical derivation procedure committed alongside the value in a Phase 02 ROADMAP step. |
| F14 | "We achieved [X]% calibration as measured by ECE." | ECE is not a proper scoring rule (per Gneiting & Raftery 2007); per RISK-14 + T13 §2.6.2 rewrite, ECE is descriptive only. | (i) Primary report on Brier + log-loss (proper scoring rules); (ii) ECE only as a descriptive aggregate diagnostic with explicit demarcation. |
| F15 | "Cross-game classifier comparison via Friedman omnibus test on SC2 + AoE2." | Demsar 2006 §3.2 (and possibly §3.1.3 — PDF verification pending) requires N ≥ 5–10 datasets for Friedman; N = 2 (games) is insufficient. | (i) Per-dataset rankings with effect sizes + bootstrapped CIs (Invariant I8); (ii) per-dataset 5×2 cv F-test or Nadeau-Bengio corrected t-test; (iii) Bayesian comparison via baycomp where applicable; (iv) qualitative cross-game concordance discussion. |
| F16 | "SC2 tracker-event features are pre-game features." | Tracker-derived features are never pre-game (Amendment 2 of PR #208 / Invariant I3). Every row of `tracker_events_feature_eligibility.csv` carries `status_pre_game = not_applicable_to_pre_game`. | No evidence path. This claim is permanently forbidden — tracker features are exclusively `in_game_snapshot`. |
| F17 | "The SC2EGSet sample is representative of all StarCraft II ladder players." | SC2EGSet is a tournament/professional replay corpus (`leaderboard_raw` NULL for 100% of rows). It is NOT sampled from Battle.net matchmaking. | No evidence path. Must always be framed as tournament/professional, not as ladder sample. |
| F18 | "Our identity resolution achieves [X]% accuracy." | Per-dataset identity-resolution branches differ (sc2egset Branch iii, aoestats Branch v, aoe2companion Branch i); cross-dataset comparisons of "accuracy" are not comparable. | Per-dataset migration_rate + cross_scope_collision_rate (already reported); cross-dataset namespace-bridge agreement 0.9960 (aoestats ↔ aoe2companion already reported, but framing must remain per-dataset). |

---

## 9. Recommended next writing PRs

Each PR is Category F (thesis writing) unless noted. All Category F PRs require `@reviewer-adversarial` at the final gate (per `.claude/rules/data-analysis-lineage.md` agent-routing discipline). Branches use the `docs/thesis-` prefix.

### 9.1 PR — Phase 02 registry methodology subsection (NEW §4.5)

- **Branch:** `docs/thesis-phase02-registry-methodology-subsection`
- **Deliverable file(s):** New §4.5 prose in `thesis/chapters/04_data_and_methodology.md`; entry in `thesis/chapters/REVIEW_QUEUE.md`; `WRITING_STATUS.md` row update.
- **Evidence sources:**
  - `reports/specs/02_00_feature_input_contract.md` (CROSS-02-00-v3.0.1)
  - `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1)
  - `reports/specs/02_02_feature_engineering_plan.md` (CROSS-02-02-v1.0.1)
  - `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1)
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.{csv,md}`
  - `thesis/pass2_evidence/notebook_regeneration_manifest.md` (status token `partial_coverage_v9_baseline`)
- **Reviewer routing:** `@reviewer-adversarial` (methodology-claim load-bearing).
- **What NOT to claim:**
  - Do NOT claim Step 02_01_01 is closed (F4).
  - Do NOT claim "leakage-free" (F7).
  - Do NOT claim aoestats + aoe2companion parity (F5).
  - Cite the SC2EGSet registry artifact AS PROVISIONAL alongside the (future) post-materialization audit only.

### 9.2 PR — SC2 in-game telemetry scope subsection (NEW §4.3 subsection on tracker eligibility)

- **Branch:** `docs/thesis-sc2-tracker-eligibility-scope`
- **Deliverable file(s):** New §4.3 subsection prose; updates to §4.4 in-game feature framing (GATE-14A6 acknowledgement).
- **Evidence sources:**
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_05_tracker_events_semantic_validation.{json,md}`
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` (15-row contract)
  - `thesis/pass2_evidence/phase02_readiness_hardening.md` §14A.6 POST-VALIDATION UPDATE
  - `thesis/pass2_evidence/methodology_risk_register.md` RISK-21 (MITIGATED-NARROWED)
- **Reviewer routing:** `@reviewer-adversarial` (GATE-14A6 framing is methodology-claim load-bearing).
- **What NOT to claim:**
  - Do NOT claim "full tracker scope is closed" (F9).
  - Do NOT claim tracker features as pre-game (F16).
  - Cite GATE-14A6 outcome as `narrowed`; enumerate 12 planned-yes rows + 3 blocked rows with reasons.
  - `slot_identity_consistency` is sanity gate, NOT model input.

### 9.3 PR — Population scope harmonization (sweep RISK-01–05 wording across Chapters 1–4)

- **Branch:** `docs/thesis-population-scope-harmonization-sweep`
- **Deliverable file(s):** Targeted edits in `01_introduction.md` (§1.1, §1.4), `02_theoretical_background.md` (§2.2.3, §2.3.2), `03_related_work.md`, `04_data_and_methodology.md` (§4.1.1, §4.1.2, §4.1.3, §4.1.4, Tabela 4.4a/4.4b/4.5).
- **Evidence sources:**
  - `thesis/pass2_evidence/aoe2_ladder_provenance_audit.md` §4.3 (four-tier ladder governance)
  - `thesis/pass2_evidence/cross_dataset_comparability_matrix.md` §1 (five-axis bounded comparability)
  - `thesis/pass2_evidence/methodology_risk_register.md` RISK-01..05
  - `thesis/pass2_evidence/phase01_closeout_summary.md` §2 (binding source labels)
- **Reviewer routing:** `@reviewer-adversarial` (examiner-facing population-framing factual-error risk per RISK-01 blocker).
- **What NOT to claim:**
  - Do NOT collapse aoestats + aoe2companion + SC2EGSet under unqualified "ranked ladder" or "online multiplayer" (F10, F11, F17).
  - Per-corpus T05-tier wording mandatory at every population reference.
  - Five-axis bounded comparability framing required for every cross-game claim.

### 9.4 PR — Evaluation methodology subsection (§4.4.3 leakage audit + §4.4.4 within-game/cross-game)

- **Branch:** `docs/thesis-evaluation-methodology-subsection`
- **Deliverable file(s):** Refined §4.4.3 (leakage audit methodology) + §4.4.4 (evaluation metrics + within-game/cross-game subsections, candidate framing). Bib entry add: `[KaufmanRosset2012]`, `[LopezDePrado2018]` (if not already present).
- **Evidence sources:**
  - `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1)
  - `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1)
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/leakage_audit_sc2egset.{json,md}`
  - `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_06_temporal_leakage_audit_v1.{json,md}`
  - `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_08_leakage_audit.{json,md}`
  - Kaufman et al. 2012 (canonical leakage definition); de Prado 2018 Ch. 7 (purged k-fold + embargo)
  - Demsar 2006; Garcia & Herrera 2008; Benavoli et al. 2017
- **Reviewer routing:** `@reviewer-adversarial`.
- **What NOT to claim:**
  - Do NOT claim concrete fold boundaries / split widths / `α` / ROPE values (F6, Phase 03 BLOCKED).
  - Do NOT claim ECE as primary calibration measure (F14).
  - Do NOT claim Friedman omnibus for N=2 cross-game (F15).
  - Frame everything as candidate methodology + invariant-derived constraints.

### 9.5 PR — Cross-dataset Phase 02 readiness paragraph + §4.5 honest asymmetry framing

- **Branch:** `docs/thesis-cross-dataset-phase02-readiness-paragraph`
- **Deliverable file(s):** Targeted insert at §4.5 (NEW or extension of 9.1 PR) acknowledging the dataset-asymmetric Phase 02 state at thesis-writing time. Status table cross-referencing this audit document.
- **Evidence sources:**
  - All PHASE_STATUS.yaml + STEP_STATUS.yaml across the 3 datasets
  - This audit document (`phase01_phase02_writing_readiness_audit.md`)
  - SC2EGSet provisional registry artifacts
  - aoestats + aoe2companion ROADMAP stubs for Step 02_01_01
- **Reviewer routing:** `@reviewer-adversarial` (asymmetry framing is examiner-facing methodology risk).
- **What NOT to claim:**
  - Do NOT claim parity (F5).
  - Do NOT claim closure (F4).
  - Frame as: "SC2EGSet Phase 02 has a provisional `validated_through = V-9` artifact; aoestats and aoe2companion Phase 02 are at ROADMAP stubs. The thesis reports per-dataset Phase 02 progress separately and does not collapse cross-dataset feature parity."

---

## Appendix A — On-disk file inventory (referenced in the audit)

This appendix lists by path every artifact, spec, status YAML, research log, ROADMAP, and pass-2 evidence document referenced in the audit. All paths are absolute or repo-root-relative.

### A.1 Methodology specs (LOCKED)

- `reports/specs/02_00_feature_input_contract.md` — CROSS-02-00-v3.0.1, LOCKED 2026-04-26
- `reports/specs/02_01_leakage_audit_protocol.md` — CROSS-02-01-v1.0.1, LOCKED 2026-04-26
- `reports/specs/02_02_feature_engineering_plan.md` — CROSS-02-02-v1.0.1, LOCKED 2026-05-06
- `reports/specs/02_03_temporal_feature_audit_protocol.md` — CROSS-02-03-v1.0.1, LOCKED 2026-05-06
- `reports/specs/02_04_cross_spec_consistency_report.{json,md}` — verdict PASS, 0 blockers

### A.2 Cross-dataset Phase 01 outputs

- `reports/artifacts/01_exploration/06_decision_gates/cross_dataset_phase01_rollup.md`
- `reports/artifacts/01_exploration/06_decision_gates/phase01_audit_summary_2026-04-21.md`
- `reports/research_log.md` (CROSS index)

### A.3 SC2EGSet Phase 01 + Phase 02 outputs

- Phase 01 artifacts (Sections 01_01..01_06): 50+ JSON+MD+CSV under `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/`. Notable: `tracker_events_feature_eligibility.csv` (15 rows, authoritative SC2 tracker contract); `phase06_interface_sc2egset.csv` (35 rows, 35/35 `[POP:tournament]`).
- Phase 02 artifacts: `02_01_01_feature_family_registry.{csv,md}` under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
- ROADMAP: `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (Phase 02 §1905+; Step 02_01_01 §1914+).
- Research log: `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (latest entry 2026-05-16 Phase 02 / Step 02_01_01 provisional artifact).
- Status YAMLs: `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`.
- Schema VIEWs: `data/db/schemas/views/matches_history_minimal.yaml` (9-col + duration ADDENDUM), `data/db/schemas/views/player_history_all.yaml` (38-col post-amendment).
- INVARIANTS: `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` §2 (Branch iii player_id_worldwide).

### A.4 aoestats Phase 01 outputs

- 40+ JSON+MD+CSV under `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/`. Notable: `01_04_03b_canonical_slot_amendment.{json,md}`, `01_04_05_i5_diagnosis.{json,md}`, `01_04_06_old_rating_temporal_audit.{json,md}`, `01_04_07_old_rating_conditional_annotation.{json,md}`, `01_05_05_icc_results.{json,md}`, `01_05_06_temporal_leakage_audit_v1.{json,md}`, `01_05_08_phase06_interface_schema_validation.{json,md}` + `phase06_interface_aoestats.csv` (137 rows).
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoestats/reports/ROADMAP.md` (Phase 02 §1748+; Step 02_01_01 stub §1757+).
- Research log: `src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md`.
- INVARIANTS: `src/rts_predict/games/aoe2/datasets/aoestats/reports/INVARIANTS.md` §2 / §3 (Branch v structurally-forced; old_rating CONDITIONAL_PRE_GAME).
- Schema VIEWs: `data/db/schemas/views/matches_history_minimal.yaml` (10-col + canonical_slot), `data/db/schemas/views/player_history_all.yaml` (15-col + time_since_prior_match_days).

### A.5 aoe2companion Phase 01 outputs

- 40+ JSON+MD+CSV under `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/`. Notable: `data_dictionary_aoe2companion.{csv,md}` (post-T16 regen); `data_quality_report_aoe2companion.md` (post-T07/T08 regen); `01_05_05_icc.{json,md}`; `01_05_03_stratification.*` + `01_05_03_stratification_per_lb.csv`; `01_05_phase06_interface_aoe2companion.csv` (74 rows, 74/74 `[POP:ranked_ladder]` — note label is artifact-historic; thesis prose uses mixed-mode per RISK-01–03).
- ROADMAP: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/ROADMAP.md` (Phase 02 §1416+; Step 02_01_01 stub §1425+).
- Research log: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md`.
- INVARIANTS: `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/INVARIANTS.md` §2 (Branch i API-namespace profileId; rename-stable 2.57%/3.55%).
- Schema VIEWs: `data/db/schemas/views/matches_history_minimal.yaml` (TABLE-materialized; 9-col + duration), `data/db/schemas/views/player_history_all.yaml` (19-col).

### A.6 Thesis pass-2 evidence (background for this audit)

- `thesis/pass2_evidence/phase01_closeout_summary.md` — Phase 02 entry conditions (2026-05-05).
- `thesis/pass2_evidence/phase02_readiness_hardening.md` — T16 decision record + GATE-14A6 (2026-04-27).
- `thesis/pass2_evidence/methodology_risk_register.md` — 26 risks (T10 + post-Round-2 patch).
- `thesis/pass2_evidence/notebook_regeneration_manifest.md` — 86 confirmed_intact / 7 not_yet_assessed / 0 flagged_stale / 0 regenerated_pending_log / + 1 `partial_coverage_v9_baseline` (SC2EGSet Phase 02).
- `thesis/pass2_evidence/aoe2_ladder_provenance_audit.md` — four-tier ladder governance.
- `thesis/pass2_evidence/cross_dataset_comparability_matrix.md` — five-axis bounded comparability.
- `thesis/pass2_evidence/dependency_lineage_audit.md`, `audit_cleanup_summary.md`, `claim_evidence_matrix.md`, `cleanup_flag_ledger.md`, `literature_verification_log.md`, `reviewer_gate_report.md`, `sec_4_1_crosswalk.md`, `sec_4_1_halt_log.md`, `sec_4_2_crosswalk.md`, `sec_4_2_halt_log.md` — supporting evidence.

### A.7 Thesis writing tracking

- `thesis/WRITING_STATUS.md` — per-section status table.
- `thesis/chapters/REVIEW_QUEUE.md` — Pass-2 pending entries.
- `thesis/chapters/01_introduction.md` through `07_conclusions.md` — chapter prose.
- `thesis/references.bib` — bibliography.
- `thesis/THESIS_STRUCTURE.md` — outline.

---

**End of audit document.**
