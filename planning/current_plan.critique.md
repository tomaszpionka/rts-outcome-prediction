---
plan_ref: .github/tmp/01_05/plan_aoe2companion.md
spec_ref: reports/specs/01_05_preregistration.md @ 7e259dd8 (v1.0.1 LOCKED)
reviewer: reviewer-adversarial
date: 2026-04-18
---

# Critique: 01_05 Temporal & Panel EDA — aoe2companion

## Summary
Two BLOCKERS and ten MAJORS. Most consequential: (1) mixedlm on Bernoulli → LPM-ICC wrong scale; (2) spec 1 9-col contract silently renamed without 14 amendment. Also: T07 Q1 unrelated tautology, spec 5 leaderboard_id deviated (rm_1v1/rm_team → rm_1v1/qp_rm_1v1), PSI thresholds uncalibrated at N~60M, population selection bias unflagged.

## Blockers

### B-01 — mixedlm on Bernoulli won is wrong estimator
Spec 8: mixedlm("won ~ 1", ..., groups="player_id"). MixedLM linear (Gaussian). won BOOLEAN. Silent coercion to {0,1} = LPM with observed-scale variance ~p(1-p); not canonical latent-scale Bernoulli-GLMM ICC tau^2/(tau^2+pi^2/3) (Nakagawa & Schielzeth 2010). Gelman-Hill 12.5 delta-method presupposes linear model.
Fix: (a) GLMM via BinomialBayesMixedGLM logit-link, report latent ICC; (b) Keep mixedlm as LPM, rename output icc_lpm, add logistic-GLMM cross-check. Spec 14 amendment required.

### B-02 — Spec 1 9-col contract renames unreconciled
Spec: {match_id, started_at, player_id, team, chosen_civ_or_race, rating_pre, won, map_id, patch_id}. VIEW: {match_id, started_at, player_id, opponent_id, faction, opponent_faction, won, duration_seconds, dataset_tag}. Only 4 of 9 match. Plan unilaterally reinterprets.
Fix: Spec 14 amendment v1.0.2 aliasing: faction AS chosen_civ_or_race, mapId AS map_id, rating AS rating_pre, team/patch_id NULL. T09 emits contract names. Gate verifies feature_name values.

## Majors

### M-01 — T07 Query 1 unrelated to I3
Tautology: match_id primary key → single started_at → no match in both windows.
Fix: Declare N/A for 01_05 with 14 note; or assert bin-edge rows have started_at<2023-01-01.

### M-02 — Spec 5 secondary regime substituted
Spec names rm_1v1/rm_team. Plan substitutes rm_1v1/qp_rm_1v1 (ranked vs quickplay) — different populations.
Fix: Add rm_team as third cohort, OR commit to rm_1v1/qp_rm_1v1 via 14 with reframing.

### M-03 — Cohen's h against p=0.5, not reference period
Plan: h = 2*(asin(sqrt(p_q)) - asin(sqrt(0.5))). Spec 3 table: h is drift vs reference. R03 complementarity forces p~0.5 but cross-dataset comparability requires reference comparator.
Fix: h = 2*(asin(sqrt(p_q)) - asin(sqrt(p_ref))). Document h~0 result honestly.

### M-04 — PSI thresholds 0.10/0.25 uncalibrated at N=60M
Siddiqi calibrated on 10^3-10^5. Yurdakul 2018: "0.25 reasonable for 100-200, too conservative for larger." At 10^6-10^7 per bin the threshold too permissive.
Fix: Cite Yurdakul; consider bootstrap null; report raw PSI without "escalate/flag" verdicts until 14.

### M-05 — Cohen's d interpretation absent at extreme N
At N=60M, CI on d ~ ±10^-4. Any drift "significant" yet trivial. Sullivan & Feinn 2012 JGME 4(3):279-282.
Fix: Mandatory "Interpretation at large N" paragraph T03/T08 MD. Frame d/h/PSI via substantive significance. Required for negative findings.

### M-06 — Reservoir non-determinism mitigation weak
aoec INVARIANTS 3: REPEATABLE(seed) not bit-deterministic across rebuilds. "Methodological-equivalence" doesn't persist sample.
Fix: Persist icc_sample_profileIds_50k.csv (+25k, +100k). T06 query uses WHERE profileId IN (SELECT FROM read_csv_auto(...)). Record hash of reference rows.

### M-07 — Population selection bias unflagged
Ladder-only cohort. Not overall AoE2, not tournament. Not flagged.
Fix: T10 "Population scope" paragraph; Phase 06 compare conditional on ranked-ladder across datasets.

### M-08 — KS computation at 60M unspecified
ks_2samp materializes arrays → memory hit.
Fix: Subsample 100k ref + 100k test per quarter (seed=42, persisted); DuckDB quantile approximation fallback.

### M-09 — is_null_cluster not segmented in PSI
10-col NULL cluster <0.02% across 70 months. Plan doesn't exclude; spans schema-era boundary → tied __unseen__ bins.
Fix: Apply WHERE is_null_cluster = FALSE consistently (ref+test). Or segment (cheap).

### M-10 — Step numbering inconsistency
T10 enumerates 01_05_01..09 but leakage notebook is 01_05_aoec_leakage_audit.py (no index).
Fix: Rename to 01_05_08_leakage_audit.py (keep aoec in binding) OR add STEP_STATUS notebook_path field.

## Minors
- m-01: ICC hypothesis has "no verdict" zone [0.02,0.05) ∪ (0.20,0.50]. Partition or document.
- m-02: 75% threshold in T05 unsourced. Cite Clauset et al. 2009 or drop.
- m-03: cohort_threshold per-row semantics undefined (unconditional/ICC rows).
- m-04: ICC sample-size sensitivity combination rule undocumented.
- m-05: 3-round iteration cap not stated per notebook.
- m-06: statsmodels@^0.14 pin unjustified.
- m-07: Sawilowsky 2009 extends Cohen for large N; cite as secondary.
- m-08: T09 ">=128" too loose; derive exact.

## Citations validated
- Yurdakul (2018) WMU #3208 — scholarworks.wmich.edu/dissertations/3208/
- Sullivan & Feinn (2012) — PMC3444174
- statsmodels MixedLM — Lindstrom-Bates JASA 1988 (linear)
- Nakagawa & Schielzeth (2010) — Biol Rev 85(4):935-956 (binary ICC)
- Sawilowsky (2009) — JMASM 8(2):597-599
- Cohen (1988) — author's own caveat against literal thresholds

## Open questions for executor
1. B-01 — 14 to GLMM, or icc_lpm rename?
2. B-02 — aliasing (spec names) or native with Manual 06 transform?
3. M-02 — rm_1v1/qp_rm_1v1 (14) or include rm_team?
4. M-06 — persist profileId CSVs (recommended) or methodological-equivalence?
5. M-07 — explicit ranked-ladder scope? Chapter 4 implications.
6. M-09 — filter or segment is_null_cluster?
7. CROSS research log for 14 amendments — BEFORE execution.

## Verdict: REVISE BEFORE EXECUTION
B-01/B-02 cannot be fixed by correct execution. M-01 through M-09 produce defensible-but-fragile artifacts.
