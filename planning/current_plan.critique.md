---
plan_ref: .github/tmp/01_05/plan_aoestats.md
spec_ref: reports/specs/01_05_preregistration.md @ 7e259dd8 (v1.0.1 LOCKED)
reviewer: reviewer-adversarial
date: 2026-04-18
---

# Critique: 01_05 Temporal & Panel EDA — aoestats

## Summary
Three BLOCKERS, eight MAJORS, six MINORS. Most dangerous: (a) T07 Q7.1 vacuous gate SELECT ... WHERE 1=0; (b) PSI decile binning applied to 2-level BOOLEAN features (undefined under N=10 equal-frequency); (c) reference period coincides with dataset's earliest 9 weeks (crawler expansion confounded with drift); (d) patch-heterogeneity across 8 tested quarters never quantified.

## Blockers

### B1 — T07 Q7.1 vacuous gate (I3 / spec 9 Query 1)
Plan T07 step 1 SQL: AND b.match_id IN (SELECT match_id FROM matches_history_minimal WHERE 1=0). "Passes vacuously". Gate that cannot fail is not a gate.
Fix: Replace with probe:
  SELECT COUNT(*) FROM matches_history_minimal
  WHERE player_id IN (<T03 cohort_profile_ids>)
    AND started_at > DATE 2022-10-27;
Separate assertion proves reference edges computed from <= 2022-10-27 restriction.

### B2 — PSI N=10 on 2-level BOOLEAN features (I7 / spec 4)
Features: mirror, p0_is_unrated, p1_is_unrated (BOOLEAN); faction (50-card); map (77-card). np.quantile on {0,1} → 11 edges collapse to <=3; degenerate histograms; PSI = 0 trivial or NaN.
Fix:
1. compute_decile_edges raises ValueError if len(np.unique(values)) <= n_bins; fallback distinct-value histograms.
2. Type routing: continuous → decile; binary → exact-value freq + Cohen h (spec 3); high-card categorical → categorical-freq with __unseen__ bin.
3. metric_name=cohen_h for binary features.

### B3 — Reference coincides with dataset's earliest 9 weeks (I3 / spec 7)
Coverage 2022-08-29; reference 2022-08-29..2022-10-27 — identical start. Match count jumps 22x from 2022-Q3 (18k) to 2023-Q1 (404k) — crawler coverage growth, not play growth. PSI null H becomes (population) x (crawler expansion) x (patch heterogeneity) — all push PSI up.
Fix: Add T02.5/T03.8:
1. Weekly match count 2022-08-29..2023-03-31; flag inflection.
2. PSI p0_old_rating between reference and next 9-week (2022-10-28..2023-01-05).
3. Sensitivity: alternative reference = 2023-01-01..2023-03-31 counterfactual.
4. Gate memo T10.7 names coincidence.

## Majors

### M1 — Patch heterogeneity named, never quantified
19 patches 2022-08..2025-12; 8 quarters → ~2 patches/quarter. Chitayat et al. 2023 arxiv 2305.18477 — NOT cited.
Fix: T04.5 per-quarter share_of_row_count_by_patch; flag single-patch; decompose multi-patch. PSI stratified by patch (Simpson probe). Gate: "drift attributable to patch: X%; intra-patch: Y%."

### M2 — LMM on Bernoulli ICC without concept
T06: mixedlm("won ~ 1"). Binary. Observed 0/1 scale ≠ latent logistic sigma^2_u/(sigma^2_u + pi^2/3). Ukoumunne et al. 2012 PMC3426610 — delta fragile, bootstrap preferred.
Fix: Report LMM primary (spec-locked). Secondary GLMM (Bernoulli) latent-scale. If differ >5pp log caveat. Add bootstrap CI.

### M3 — 50k-player reservoir bias undocumented
"Stratified 50,000" magic number. "Stratified" variable unspecified → uniform → low-volume players dominate → ICC biased downward.
Fix: Report ICC + sensitivity at 20k and 100k. Stratify by n_matches_in_reference_period deciles. Cite or accept risk in gate memo.

### M4 — [PRE-canonical_slot] tagging inverted
Plan: "aggregate NOT slot-biased; per-slot IS". Correct for faction/opponent_faction (UNION-ALL-symmetric). WRONG for p0_old_rating/p1_old_rating — those in matches_1v1_clean 1-row-per-match, NOT pivoted; JOIN pulls by raw p0/p1 (skill-correlated). W3 audit: p0_old_rating +11.9 ELO higher. p0/p1 PSI IS per-slot, MUST flag.
Conversely, Gate forces flag on symmetric faction/opponent_faction → false-positives obscure signal.
Fix:
1. Replace p0/p1 ratings with focal_old_rating = CASE WHEN half=0 THEN p0_old_rating ELSE p1_old_rating END (symmetric, no flag).
2. Or flag both ratings.
3. Remove blanket flag from symmetric faction aggregate PSI.

### M5 — Feature list expands beyond spec 1 9-col contract
Plan analyzes 15 cols (JOIN matches_1v1_clean): p0_old_rating, p1_old_rating, avg_elo, map, mirror, p0_is_unrated, p1_is_unrated, patch.
Fix: Either extend aoestats VIEW (schema amendment) OR read spec 1 as "equivalent columns may be substituted" with plan mirroring siblings. T09 pre-emission: feature_name overlap with siblings >= 6 of 8.

### M6 — Q4 canonical_slot success impossible to fail
Plan assumes absent; probe returns 0; logs flag; passes. No actionable signal.
Fix: Refactor Q7.4 as future-state contract: drop schema probe; assert every Phase 06 row with per-slot breakdown carries [PRE-canonical_slot]. Gate CAN fail if M4 lands.

### M7 — I2 branch (v) limitation not stated
INVARIANTS 2: "No name column; Steps 2/3 unevaluable; branch v applies." T06 ICC treats profile_id as stable. aoec bridge (VERDICT A 0.9960) supports stability but doesn't audit within-aoestats fragmentation.
Fix: T06 MD and T10 log: "ICC on profile_id; per INVARIANTS 2, within-aoestats migration/collision unevaluable (branch v). Bridge supports stability, doesn't audit fragmentation. ICC upper bound on per-player variance."

### M8 — 28 corrupted duration rows retained
is_duration_suspicious not in T03 feature list but affects avg_elo/rating PSI if in reference or tested quarter.
Fix: Primary PSI full data; sensitivity with WHERE NOT is_duration_suspicious. If differ <0.01 PSI, document; else flag.

## Minors
- m1: T01 assert spec SHA current: `git log --oneline -1 reports/specs/01_05_preregistration.md | grep -q 7e259dd8 || exit 1`.
- m2: T05 "192 or 189" ambiguous. Rule: n_q x n_N x n_surviving_features. Drop 189.
- m3: T04 5pp patch threshold unjustified. Cite Chitayat 2023 or Cohen h=0.1.
- m4: Verify T-codes absent from ROADMAP names.
- m5: T09 ">=64 rows" too low. Upper 8x3x8x5=960; warn if <64.
- m6: CHANGELOG: "Version bump deferred to release cut."

## Citations validated
- Chitayat et al. 2023 — arxiv.org/abs/2305.18477, AAAI-AIIDE 19(1):116-125. NOT in plan; add for B3/M1.
- Nakagawa/Johnson/Schielzeth 2017 — royalsocietypublishing.org/doi/10.1098/rsif.2017.0213
- Ukoumunne et al. 2012 — PMC3426610 (bootstrap CI)
- Mantel-Haenszel 1959 + Robins 1986 (spec 16)
- Siddiqi 2006 PSI (spec-cited; 1000/bin safely above any floor)
- Hamilton 1994 17.7 (spec-cited; accepted on authority)

## Open questions for executor
1. B3 sensitivity: run Q2 PSI with alt reference = 2023-01-01..2023-03-31 before T04-T09.
2. M4: Does T03 UNION-ALL pull old_rating as focal_old_rating (CASE) or raw p0/p1?
3. M2 practical: capacity to fit secondary GLMM in T06? Or add T06.5?
4. M5: sibling plans use same feature list? Gate includes cross-plan parity.
5. B1: exact feature-window materialisation at 01_05? If none genuinely, declare Q1 N/A vs vacuous.
6. M8: emit corruption-filter sensitivity before T03 finalises headline.

## Verdict: REVISE BEFORE EXECUTION
B1/B2/B3 addressed + M1/M2/M4 documented → defensible. As written, numerics would embarrass thesis at patch-heterogeneity-aware examiner.
