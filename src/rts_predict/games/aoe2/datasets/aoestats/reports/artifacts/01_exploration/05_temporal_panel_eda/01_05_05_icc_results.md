# Variance Decomposition ICC -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_05

## M7 Branch-v Limitation

ICC computed on `profile_id`; per INVARIANTS §2, within-aoestats migration/collision unevaluable (branch v). aoec namespace bridge (VERDICT A 0.9960) supports stability but doesn't audit fragmentation. ICC = upper bound on per-player variance share.

## ICC Results (Primary: 50k stratified sample)

| Method | ICC | CI lo | CI hi |
|--------|-----|-------|-------|
| LMM observed-scale | 0.0259 | - | - |
| ANOVA observed-scale (Wu/Crespi/Wong 2012) | 0.0268 | - | - |

*Bootstrap CI per Ukoumunne et al. 2012 PMC3426610.*
*Stratified reservoir by n_matches_in_reference_period deciles (critique M3).*

## Falsifier verdict

**Q6 skill-signal hypothesis:** FALSIFIED
