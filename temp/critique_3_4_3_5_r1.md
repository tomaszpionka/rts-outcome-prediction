# Adversarial Critique R1 — temp/plan_3_4_3_5_v1.md

## Executive verdict: REQUIRES_REVISION_R2

Plan internal structure is honest and well-reasoned, but the "2 peer-reviewed AoE2 sources" empirical premise is falsified by independent WebSearch. One peer-reviewed AoE2 outcome-prediction paper (Elbert et al. 2025, ACM EC'25) was missed. 4-gap structure and novelty framing hold but must be rearticulated to accommodate the missed paper.

## BLOCKER-1: Missed peer-reviewed AoE2 outcome-prediction paper (Elbert et al. 2025)

**Evidence:** Elbert, N., von Schenk, A., Kosse, F., Klockmann, V., Stein, N., & Flath, C. (2025). *What Drives Team Success? Large-Scale Evidence on the Role of the Team Player Effect*. arXiv:2506.04475; accepted for presentation at ACM Conference on Economics & Computation 2025 (26th ACM EC, Stanford, July 7–10, 2025; 24.6% acceptance rate).

**What the paper does:** Uses AoE2 as primary empirical setting; large-scale panel dataset; explicitly "compares observed match outcomes with predictions based on task proficiency" (skill-based match prediction serves as baseline against which residual "team player effect" is estimated). Reports log-odds-of-winning regression β=0.43 per SD of team player effect → 54% odds increase. **This is outcome-prediction instrumentation in a peer-reviewed venue on AoE2.**

**Impact:**
- Plan Section 5 Tier 1: "2 peer-reviewed AoE2 sources" → 3
- Section 7 halt-protocol threshold (≥2 sources) no longer at floor
- §3.4 budget 5.0-7.5k may extend to 7-9k with dedicated §3.4.N sub-section for Elbert2025
- §3.5 Luka 3 novelty claim "pierwsza znana nam praca..." still defensible (Elbert2025 is causal-inference instrumentation, not ML-method-family benchmarking) but hedge language must strengthen

**Required fix:** Add Elbert2025 to Tier 1. Add §3.4.N dedicated ~600-800 char treatment framing Elbert2025 as "peer-reviewed AoE2 paper on pogranicza ekonomii obliczeniowej i analityki esportowej, predykcja wyniku jako instrument dla wyodrębnienia czynnika team-player effect — poza scope'em niniejszej tezy (czysto-ML benchmarking), ale wewnątrz peer-reviewed AoE2 literatury". Update §3.5 Luka 3 hedge. Add `@inproceedings{Elbert2025EC}` bib entry.

## WARNING-1: 86% provenance partially resolvable

Mike Xie Medium confirmed maxes at 77%, not 86%. "86%" can only be CetinTas2023. Plan's [REVIEW] flag should close on attribution direction (keep for primary-source verification). Update A1/U1.

## WARNING-2: Lin-group follow-up preprint not mentioned

Lin, C.-C. & Wu, I.-C. (2025). *Online Learning of Counter Categories and Ratings in PvP Games*. arXiv:2502.03998. Same author subset as Lin2024NCT. Not AoE2-specific, not peer-reviewed (preprint), but an adversarial examiner familiar with Lin group will ask. Add single-sentence footnote in §3.4.2 closing.

## WARNING-3: Halt-protocol dead-weight under revised premise

Plan's (a/b/c) branches designed for 2-paper world. With Elbert2025, starting state is "3 peer-reviewed + N grey-lit." Rewrite Section 7 to reflect.

## WARNING-4: §3.4 sub-numbering asymmetry with §3.3

§3.2 uses §3.2.1-§3.2.4; §3.3 uses §3.3.1-§3.3.5. §3.4 plan has §3.4.1-§3.4.4. Defensible (parallels §3.2 since both are single-game surveys, §3.3 surveys multiple genres) but plan needs to justify. Add single-sentence note in T02 voice requirements.

## WARNING-5: Tier 3 grey-lit decision punted

Plan Q1/A3 defer to Pass 2 global resolution. Make local §3.4 commitment now — include Xie2020 + porcpine1967 with explicit Tier 3 labelling (empirical grounding is concrete and consistent with §2.2/§2.5 grey-lit practice). Flag for Pass 2 reconciliation but do not defer structural spine.

## Confirmed OK

- CetinTas2023 characterization holds (NB/DT on civ/map/Elo; IEEE UBMK 2023 DOI verified)
- Lin2024NCT balance-analysis-not-prediction distinction holds (TMLR 2024 arXiv:2408.17180 abstract confirmed)
- 4-gap structure defensible vs 1-gap umbrella (preserves §1.3 RQ one-to-one)
- Voice calibration approach matches §3.1-§3.3 drafted registers
- Citation density ≥6 keys is evidence-calibrated, not padding
- Never-fabricate invariant explicit (plan line 442)

## Sources verified

- Elbert2025: https://arxiv.org/abs/2506.04475
- ACM EC'25: https://ec25.sigecom.org/ (24.6% acceptance)
- Lin2024NCT: https://arxiv.org/abs/2408.17180
- Lin&Wu2025: https://arxiv.org/abs/2502.03998
- Xie2020 (77% confirmed, no 86%): https://medium.com/@mikexie/
- CetinTas2023: ResearchGate (IEEE Xplore fetch failed)

## Unresolved questions for planner R2 (autonomous-mode decisions required)

- Q_adv_1 Elbert2025 scope: (a) dedicated sub-section ~600-800 chars, or (b) 300-char mention in §3.4.2? **→ (a) — AoE2-specific deserves dedicated treatment**
- Q_adv_2 Luka 3 hedge: stronger "pierwsza praca porównująca rodzinę klasyfikatorów uczenia maszynowego w zadaniu benchmarkowania metod predykcji wyniku meczu między dwiema grami RTS z jawną oceną probabilistyczną"? **→ YES, strengthen hedge**
- Q_adv_3 Lin2025Online: footnote in §3.4.2 closing or Out-of-scope? **→ footnote-equivalent single sentence in §3.4.2**
- Grey-lit W5: include or exclude in §3.4.3? **→ include Xie2020 + porcpine1967 with Tier 3 labelling; drop gmcirco42 Bayesian bookdown (too narrow)**
