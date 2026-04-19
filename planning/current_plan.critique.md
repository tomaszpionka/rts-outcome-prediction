---
plan_ref: .github/tmp/01_05/plan_sc2egset.md
spec_ref: reports/specs/01_05_preregistration.md @ 7e259dd8 (v1.0.1 LOCKED)
reviewer: reviewer-adversarial
date: 2026-04-18
---

# Critique: 01_05 Temporal & Panel EDA — sc2egset

## Summary
Plan structurally complete. Three BLOCKERS, ten MAJORS, ten MINORS.

## Blockers

### B1 — Quarter-label SQL produces '2022-Q3.0' (empty filter)
`CAST(CEIL(INTEGER / 3.0) AS VARCHAR)` yields '3.0' → '2022-Q3.0'. Verified against DB. Plan filter matches nothing.
Fix: `CAST(CAST(CEIL(...)AS INTEGER) AS VARCHAR)` or `date_part('quarter', started_at)`.

### B2 — N>=10 cohort filter eliminates 4 of 8 tested quarters
2023-Q1/Q2/Q3 and 2024-Q1 absent. Remaining: {17,12,10,16} players.
Fix: Primary PSI uncohort-filtered; N in {5,10,20} as SENSITIVITY per spec 6.2. CROSS research-log entry before T03.

### B3 — statsmodels.mixedlm is Gaussian LMM; won is Bernoulli
MixedLM = linear (Lindstrom-Bates JASA 1988). Fitting {0,1}=LPM, not canonical latent-scale GLMM ICC tau^2/(tau^2+pi^2/3) (Nakagawa/Johnson/Schielzeth 2017 JRS Interface 14:20170213).
Fix: (a) BinomialBayesMixedGLM logit-link, report latent ICC; (b) ANOVA-ICC primary (Wu/Crespi/Wong 2012 CCT 33(5):869-880), BinomialBayesMixedGLM secondary, LMM sanity-check. Spec 14 amendment required.

## Majors

### M1 — Full-dataset N (22,209) cited but overlap is 10,076 rows / 679 players
Yurdakul citation "2,200 obs per bin" is 10x too large. Lowest quarter (2023-Q3): 244 rows.
Fix: Rewrite Scope/Problem Statement/Literature Context. Add PSI CI via Harris 2013 bootstrap or chi-square `2*n*PSI ~ chi^2_{B-1}`.

### M2 — tournament_era heuristic matches ~47% of dirs
HSC fails (dirs use `HomeStory_Cup`), GSL/BlizzCon/OSC zero. 37/70 dirs become Bronze_other.
Fix: Committed `tournament_tier_lookup.csv` (70 rows hand-mapped, Liquipedia tier) or 2-tier split.

### M3 — Spec 1 9-col contract doesn't match VIEW
Spec: match_id, started_at, player_id, team, chosen_civ_or_race, rating_pre, won, map_id, patch_id. VIEW: match_id, started_at, player_id, opponent_id, faction, opponent_faction, won, duration_seconds, dataset_tag. 5 of 9 differ. Plan only acknowledges rating_pre.
Fix: Spec 13 deviation, bump to v1.0.2 per-dataset contract. Or INVARIANTS 4 I8 partial; Phase 06 UNION joins on metric_name only.

### M4 — T10 ROADMAP risks smuggling scientific claims
Fix: ROADMAP step `question:` strictly step-scope. Grep for {hypothesis, expect, predict, below 0.25, ICC > 0.05}; expect 0.

### M5 — T05 hypothesis wrong grain
Reference cohort=152 (holds). Per-quarter {17,12,10,16} triggers falsifier.
Fix: Grain-explicit: (a) reference N>=10 >=50 (falsifier <50); (b) per-quarter cohort_q >=20 (falsifier any <20).

### M6 — T07 Query 1 is ceremonial
Self-join on same key: observation_time==match_time always. Plan acknowledges tautology.
Fix: Reframe N/A to Phase 02, or upgrade: assert bin-edge rows have started_at<2023-01-01 and tested frequencies in q.

### M7 — Tournament-data external-validity caveat missing
Fix: T10 INVARIANTS 4 + Phase 06 notes: "tournament-scraped; between-player variance reflects competitive-player population." Tag Phase 06 rows `[POP:tournament]`. Heckman 1979 in references.bib.

### M8 — T04 SQL references non-existent column
replays_meta_raw has no `replay_id`; 32-char hex is in matches_flat_clean.
Fix: Build `tournament_era_map` via matches_flat_clean join. Match-id: `substr(m.match_id, 11) = t.replay_id`.

### M9 — is_duration_suspicious upstream, not in VIEW
Fix: JOIN matches_flat_clean to compute per-quarter flag rate, or document not-projected.

### M10 — Yurdakul 2018 citation garbled
2018 = WMU #3208. 2024 Edinburgh = separate paper; Yurdakul not co-author.
Fix: Cite separately.

## Minors
- m1: VIEW exposes player_id (VARCHAR toon_id), not player_id_worldwide. 2,470 distinct (not 2,494).
- m2: eps=1/n_ref smoothing is convention; cite Yurdakul Ch.3 or report sensitivity.
- m3: Normalize POST_GAME -> POST_GAME_HISTORICAL.
- m4: Use `date_part('year',..)*10 + date_part('quarter',..)` for ordering.
- m5: Scope says "10 notebooks" but 9 actually. Correct to "9 (1 scaffold + 8 content)".
- m6: Align Gate flag with scripts/check_01_05_binding.py CLI (--all vs --check).
- m7: Label per-faction ICC rows `faction_restricted=True`; not comparable to overall.
- m8: Fix eps globally to 1/n_ref; document in notes; assert both sides.
- m9: Add Scope: "KS omitted for sc2egset — no continuous pre-game feature in minimal VIEW."
- m10: T01 step 0: `poetry run python -c "import statsmodels"`; skip add if succeeds.

## Citations validated
- Yurdakul (2018) WMU #3208
- Nakagawa/Johnson/Schielzeth (2017) JRS Interface 14:20170213
- Wu/Crespi/Wong (2012) CCT 33(5):869-880
- Hamilton (1994) 17.7 (spec-cited, accepted on authority)
- Czeisler et al. (2021) - survivorship (spec-consistent)
- statsmodels MixedLM per Lindstrom-Bates
- Heckman (1979) - add to references.bib

## Open questions for executor
1. B1 fix before or during T02? Recommend T01.5 smoke test.
2. B2 — primary uncohort-filtered (recommended) vs narrowed window?
3. B3 — ANOVA-ICC primary or amend spec? Recommend spec amendment affecting all 3 datasets.
4. M2 — CSV lookup or 2-tier?
5. M3 — spec 13 amendment (recommended) or INVARIANTS doc?
6. M6/T07 — reframe N/A or upgrade? Recommend upgrade.
7. "Pattern establisher" applies to scaffolding/binding/Phase 06 schema, NOT analytical params.

## Verdict: REVISE BEFORE EXECUTION
B1/B2/B3 must be addressed before T02. M1-M3 need CROSS research-log + spec 13 amendment.
