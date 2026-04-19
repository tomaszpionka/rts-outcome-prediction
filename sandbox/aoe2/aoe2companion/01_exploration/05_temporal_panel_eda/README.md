# 01_05 Temporal & Panel EDA — aoe2companion

Spec binding: `reports/specs/01_05_preregistration.md@7e259dd8` (v1.0.1 LOCKED)

Artifacts land under:
`src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/`

## Notebooks

| Notebook | Spec §§ | Description |
|---|---|---|
| `01_05_01_quarterly_grain.py` | §2, §3 | Q1: Quarterly grain, per-quarter row counts, overlap window validation |
| `01_05_02_psi_shift.py` | §4, §7 | Q2: PSI shift (N=10 equal-frequency, frozen reference edges, pre-game features) |
| `01_05_03_stratification.py` | §5 | Q3: Stratification by leaderboard_id (rm_1v1 vs qp_rm_1v1) |
| `01_05_04_survivorship.py` | §6 | Q4: Triple survivorship — unconditional, sensitivity N={5,10,20}, captions |
| `01_05_05_icc.py` | §8 | Q6: Variance decomposition (ICC) — LPM + ANOVA + optional GLMM |
| `01_05_06_dgp_duration.py` | §10 | Q8: POST_GAME DGP diagnostics (duration_seconds + suspicious flags) |
| `01_05_07_phase06_interface.py` | §12 | Phase 06 interface CSV emission (flat schema) |
| `01_05_08_leakage_audit.py` | §9 | Q7: Temporal leakage audit (3 hard-gate queries) |

## Critique deviations (pre-authorized)

- **B-01**: ICC reports both LPM (`icc_lpm_observed_scale`) and ANOVA-based (`icc_anova_observed_scale`); optional GLMM tertiary.
- **B-02**: `feature_name` values match actual VIEW schema; `notes` column documents cross-dataset alignment is on `metric_name` only.
- **M-01**: T08 leakage audit uses meaningful bin-edge temporal check, not vacuous match-id disjointness.
- **M-02**: Secondary regime is rm_1v1 (lb=6) vs rm_team (lb=3/4); labeled `[WITHIN-AOEC-SECONDARY]`.
- **M-03**: Cohen's h computed vs reference period, not vs 0.5.
- **M-04**: PSI thresholds 0.10/0.25 flagged as uncalibrated at N>10^6 (Yurdakul 2018 WMU #3208).
- **M-05**: "Interpretation at large N" paragraphs in T03/T08 MD (Sullivan & Feinn 2012 JGME 4(3):279-282).
- **M-06**: Reservoir sample IDs persisted as CSV; reference-period hash recorded as JSON metadata.
- **M-07**: T10 decision gate notes `[POP:ranked_ladder]` scope.
- **M-08**: KS uses 100k subsample per quarter (seed=42); sample IDs persisted.
- **M-09**: `is_null_cluster = FALSE` filter applied via join to `matches_1v1_clean`.
- **M-10**: Leakage audit notebook named `01_05_08_leakage_audit.py`.
