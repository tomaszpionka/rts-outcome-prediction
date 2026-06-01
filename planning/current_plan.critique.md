---
title: "Reviewer-adversarial critique of Step 02_03_01 MATERIALIZATION Layer-1 plan"
critique_of: planning/current_plan.md
plan_branch: feat/sc2egset-02-03-01-temporal-materialization-plan
base_ref: master
base_sha: 51a0caf3e561da43be8e5119dad036a3dd768abe
critique_date: 2026-06-01
critique_round: 1
reviewer_agent: reviewer-adversarial
verdict: APPROVE-WITH-NITS
substantive_blockers: 0
nits: 7
notes: 4
---

## Verdict

APPROVE-WITH-NITS. The Layer-1 plan correctly separates Layer-2 (materialization) from Layer-3 (audit), respects the byte-stability of PR #281 adjudication artifacts, names candidate-precedent rows only (no concrete numerical winners — Invariant I7 honoured at Layer-1), and binds falsifiers F1-F7 to live repo modules at SHA-pinned states. Two-file diff scope is tight and verifiable. Seven NITs apply; none block APPROVE if applied inline before merge.

Confidence: HIGH

## Substantive Findings

(none — zero BLOCKERs)

I could not identify a methodology flaw in this Layer-1 plan after checking:
- the PR #281 adjudication CSV at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/02_03_01_temporal_feature_grid_adjudication.csv` — rows 2-4 confirm Q1/Q2/Q3 = `DEFER_TO_MATERIALIZATION` verbatim; the 9 SHA-pin columns in cols 8-16 match the plan's front-matter; row 14 `in_game_snapshot_features = DEFER_PAST_02_03_01` corroborates A7; row 17 `q8_aoe2_transferability = SYNTACTIC_ONLY` corroborates Q8 stance;
- the adjudication MD §3 SHA-pin table — verifies all 9 SHAs in plan front-matter byte-for-byte;
- `.claude/scientific-invariants.md` lines 131 (I3 strict-<), 149-154 (I4 prediction target), 158-170 (I5 symmetric treatment), 184-190 (I7 no magic numbers) — every binding falsifier maps to a quoted invariant;
- `.claude/ml-protocol.md` "veterans only (3+ historical matches)" — verifies the plan's G-L-5 candidate citation for `k_min ≥ 3`;
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` §3 (Temporal Range 2016-01-07 to 2024-12-01) and §4 Q1 (10 quarters 2022-Q3..2024-Q4 with 11.7x peak-to-trough), Q4 (cohort N∈{5,10,20}) — all three INVARIANTS cross-references resolve to verifiable section anchors;
- `thesis/references.bib` `Bialecki2023`, `Thorrez2024` (EsportsBench), `Glickman2025`, Glickman1999 / Glickman2013TR / Glickman1995 — all bib keys exist;
- EsportsBench v9.0 / 2026-03-31 anchor in `thesis/chapters/02_theoretical_background.md` and `thesis/chapters/03_related_work.md` — both lines use the exact phrasing "wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26"; the plan's `Esportsbench v9.0 default` citation resolves;
- `planning/INDEX.md` line 4 Active slot — confirms PR #281 is still Active at master tip `51a0caf3`, so the plan's no-INDEX-archive-flip-at-Layer-1 stance is faithful to PR #270 → PR #272 ladder precedent;
- master `git log` — confirms tip `51a0caf3e561da43be8e5119dad036a3dd768abe` matches `base_sha` in plan front-matter;
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` Step 02_03_01 block — the halt_predicate confirms "no concrete window sizes / no concrete decay half-lives / no concrete cold-start k-thresholds (Invariant I7)" is binding for this stub's downstream; the plan's "no concrete numerical winner pinned by this Layer-1 PR" is faithful.

## NITs

### NIT-1 — `pipeline_section` token discrepancy with ROADMAP halt_predicate

**Evidence:** Plan front-matter `pipeline_section: "02_03 — Temporal Features, Windows, Decay, Cold Starts"` matches ROADMAP `pipeline_section` field verbatim. But the ROADMAP halt_predicate names the artifact directory as `reports/artifacts/02_feature_engineering/03_temporal_features_windows_decay_cold_starts/`, while the actual on-disk path used by PR #281 is `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/` — the shorter form. Pre-existing inconsistency in the ROADMAP halt_predicate, not introduced by this plan.

**Required fix:** Add Open Question OQ-7 recording this and committing the materialization PR to the shorter on-disk-true form.

**Status:** Applied inline as OQ-7.

### NIT-2 — Non-batching exception citation missing

**Evidence:** Plan's M3 lists 6 sub-steps that fold V1 preflight, V3 preflight, SHA-pin verification, and predecessor Parquet reads into one Layer-2 execution. `.claude/rules/data-analysis-lineage.md` Non-batching Rule forbids batching unreviewed validation modules — the plan needed to record the exception (V1/V3 already passed at PR #276/#278; audit explicitly deferred to Layer-3).

**Required fix:** Add A11 to Assumptions & Unknowns recording the non-batching exception.

**Status:** Applied inline as A11.

### NIT-3 — SHA digest function unspecified

**Evidence:** F6 falsifier asserts "9 SHAs match front-matter YAML" without specifying digest function. PR #281 schema uses SHA-256 hex.

**Required fix:** Add explicit "Digest function: SHA-256 hex over the raw file bytes" line to F6.

**Status:** Applied inline in F6.

### NIT-4 — Unit ambiguity in G-L-3 / G-L-4 matrix rows

**Evidence:** Plan §Literature Context row "G-L-3 (exponential decay) | half-life ∈ {3, 6, 12 months}" — Elo K-factor is unitless; Glicko-2 rating period is days/weeks/months depending on cadence. "Months" unit is the plan's interpretive overlay, not lifted verbatim from any cited precedent.

**Required fix:** Add unit-choice disclaimer at end of matrix table: "Unit choices … are illustrative ranges; Layer-2 fixes the unit and cites the unit-fixing precedent."

**Status:** Applied inline after matrix table.

### NIT-5 — F4 non-vacuous threshold under-specified for cold-start columns

**Evidence:** F4 description states the COUNT(DISTINCT) > 1 + COUNT() > 0 gate. PR #270 emitted a stronger 50% non-null gate. The plan does not declare a NULL-rate threshold, which is the more common failure mode for cold-start features (G-L-5 gate naturally produces NaN).

**Required fix:** Refine F4 to declare NULL-rate handling — cold-start-gated columns may have elevated NULL rates by design (G-L-5 / G-L-7) and are not halted by F4 alone; MD records the NULL count next to k_min so the gate is auditable.

**Status:** Applied inline in F4.

### NIT-6 — F7 cross-game scope grep needs word-boundary anchors

**Evidence:** F7 falsifier as originally drafted: "static-grep over MD/module/notebook forbids aoe2/aoestats/aoe2companion/civilization/civ tokens outside front-matter." Bare token `civ` will match `civic`, `incivility`, etc. The PR #282 NIT-X2 precedent (merged 2026-06-01 at master `cb84e8b5`) established `\b` word-boundary anchors for predicate-checks of this kind.

**Required fix:** Refine F7 to use `\b` word-boundary anchors per PR #282 NIT-X2 precedent: `\baoe2\b`, `\baoestats\b`, `\baoe2companion\b`, `\bcivilization\b`, `\bciv\b`, excluding front-matter and Q8 stance block.

**Status:** Applied inline in F7.

### NIT-7 — OQ-2 tracker-derived families undercut by PR #281 adjudication §6

**Evidence:** Plan OQ-2 recommended "DEFER to follow-up" for tracker-derived families without citing how many PR #281 §6 rows are affected. PR #281 MD §6 enumerates 15 tracker rows; 8 carry `aggregated_decision = ELIGIBLE` or `ELIGIBLE_WITH_CAVEAT` over `pre_game / history_enriched_pre_game`. Deferring is prudent but should cite the count.

**Required fix:** Refine OQ-2 to name the 8 ELIGIBLE/ELIGIBLE_WITH_CAVEAT rows explicitly (PR #281 §6 rows 5, 6, 7, 8, 9, 10, 13, 14) and confirm the deferral preserves their byte-stability.

**Status:** Applied inline in OQ-2.

## NOTES

### NOTE-1 — INDEX archive folding precedent (non-blocking, recorded)

The plan's M7 (defer PR #281 archival to Layer-2 9-file diff) mirrors PR #270 → PR #272 and PR #259 → PR #262 ladders. INDEX line 4 currently shows PR #281 as Active; this Layer-1 PR's 2-file diff does not flip that, which is correct. No fix.

### NOTE-2 — Plan/execute two-session workflow satisfied

CLAUDE.md `## Critical Rules` "NEVER skip the plan/execute two-session workflow for non-trivial work" is satisfied: this is the plan-side of a two-session Layer-1 PR, with the future Layer-2 materialization PR being the execute-side. Plan-then-execute pairing is explicit.

### NOTE-3 — Q8 stance ratification

`q8_stance: SYNTACTIC_ONLY` exactly matches PR #281 CSV row 17 col 1. EsportsBench v9.0/2026-03-31 anchor in thesis Chapter 3 §3.5 is upstream-of-thesis source of authority for the Q8 stance. No fix.

### NOTE-4 — Falsifier F3 SQL fingerprint requirement

F3: "every feature column SQL has WHERE prior.started_at < target.started_at." PR #281 adjudication MD §4 invariant I3 anchor uses `history_time < T` mathematical notation; the plan's F3 uses SQL-level `prior.started_at < target.started_at`. These are isomorphic if `started_at` is the canonical temporal anchor per PR #234 / PR #235 (02_01_02 Q2(a) BINDING). Layer-2 executor should add a one-line citation of PR #234 Q2(a) at the F3 implementation site. Non-blocking.

## Closing Statement

ROUND 1 APPROVE-WITH-NITS. Zero substantive BLOCKERs. Seven NITs (N1-N7) and four NOTES (NOTE-1..NOTE-4) recorded. All NITs were applied inline to `planning/current_plan.md` before merge. The Layer-1 → Layer-2 → Layer-3 ladder (materialization PR → audit closure PR) is faithful to PR #270 → PR #272 and PR #259 → PR #262 precedents. PR #281 byte-stability assumed at merge time; falsifier A1 binding.

If a second adversarial round is requested, the gate predicate is: all 7 NITs visible verbatim in `planning/current_plan.md`, INDEX line 4 unchanged, two-file diff preserved, master `base_sha` re-resolved to current HEAD at PR open.

Per reviewer-adversarial Phase 03+ guidance, a Pass-2 review in Claude Chat is recommended for the future Layer-2 materialization PR (not for this Layer-1 plan PR) before merge, given the subtle temporal-leakage surface across G-L-1..G-L-7 family compositions.
