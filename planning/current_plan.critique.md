---
title: "Reviewer-adversarial critique — SC2EGSet Step 02_02_01 symmetry/difference feature materialization + non-vacuous leakage audit (Layer-1 planning PR)"
plan_ref: planning/current_plan.md
category: A
branch: feat/sc2egset-02-02-01-symmetry-difference-materialization
base_ref: master
base_sha: b84ed6d6bf89414d33b7a1b9ee05f34e82d00457
predecessor_pr: 268
dataset: sc2egset
phase: "02"
pipeline_section: "02_02 — Symmetry & Difference Features"
adversarial_cap: 3
rounds_run: 1
final_verdict: APPROVE-WITH-NITS
blockers: 0
nits: 6
date: 2026-05-30
---

## Adjudication outcomes (cross-reference)

The planner selected **Outcome A** — `02_02_01` symmetry/difference feature materialization + non-vacuous leakage audit planning PR — and rejected B–G with repo-evidence justification. The reviewer ratified Outcome A.

- **B — Direct execution without planning** — Rejected: `.claude/rules/data-analysis-lineage.md` §"Non-batching rule" bans `notebook + artifact + next step` in one execution; PR #258 → PR #259 precedent ladder requires Layer-1 plan first.
- **C — Additional adjudication / source-anchor PR** — Rejected: PR #268 closed all 8 open questions from PR #265 with `validator_passed=True`; binding adjudicator constants leave zero unresolved scope; no concrete defect surfaced in lookup.
- **D — Status-chain update PR** — Rejected: STEP_STATUS has no `02_02_01` row, no on-disk Parquet, no audit; closure requires those artifacts to exist first per PR #237 / PR #262 precedent.
- **E — Phase 03 planning** — Rejected: Phase 02 in_progress; ROADMAP line 3119 halts on Phase 03 start; CLAUDE.md "NEVER begin a new phase until all prior phase artifacts exist on disk."
- **F — Reopen 02_01 / Q6 / reconstructed_rating** — Rejected: ROADMAP lines 3076–3082 + PR #255 / PR #257 / PR #259 / PR #262 chain establish binding `reconstructed_rating` exclusion; no defect.
- **G — Hold** — Rejected: all 20 precondition predicates PASS (item 13 audit-JSON-missing was a lookup-agent path-confusion that direct verification corrected; item 19 dirty `02_01_03_q6h_rating_path_decision.ipynb` is unrelated stale notebook output from Step 02_01_03 work and does not affect this planning workflow).

## Round 1 — verdict: APPROVE-WITH-NITS (0 blockers, 6 nits)

### Round 1 BLOCKERs

**None.** The plan's methodology is sound; the 33-feature contract is mathematically correct; the two-PR Layer-1/Layer-2 sequence respects `.claude/rules/data-analysis-lineage.md`; the LogReg basis argument is valid; identity alignment / byte-determinism / parent non-mutation falsifiers are well-specified; temporal discipline is inherited unchanged.

### Round 1 NITs (6 — all wording / format fixes; applied inline in Layer-1 plan body)

| # | Maps to | Concern | Fix applied in plan body |
|---|---|---|---|
| **N1** | OQ1 / audit JSON spec | `cutoff_time_filter_structural_check` value must be spec-literal `"pass"` per CROSS-02-01-v1.0.1 §3. The qualified value `"pass_inherited_from_02_01_03"` is not spec-allowed; PR #236 + PR #259 audits both use the bare `"pass"` literal. Inheritance prose belongs in `notes`. | Audit JSON spec template now uses `"pass"`; OQ1 rewritten as RESOLVED with the binding decision recorded. |
| **N2** | A9 / R6 / Falsifier 12 | Row count assertion needs defence-in-depth: both module-level constant (precedent: PR #259's `EXPECTED_OUTPUT_ROW_COUNT: int = 44_418`) AND runtime equality against 02_01_03 audit JSON's `row_count` field. Hard-coded constant alone is brittle vs upstream drift. | A9 declares `EXPECTED_OUTPUT_ROW_COUNT = 44_418` AND adds runtime equality vs audit JSON `row_count`; falsifier 12 splits into two checks (`output_row_count_drift` + `audit_pinned_row_count_drift`). |
| **N3** | "Future audit MD requirements" | 7-section MD structure is NOT a PR #259 precedent claim (PR #259's audit MD has 4 sections; PR #236's has 8). The structure itself is fine but "per PR #259 precedent" is factually wrong. | "Future audit MD requirements" reworded: "this PR introduces a new 7-section structure tailored to the 33-feature symmetry/difference family". |
| **N4** | A14 / R2 / OQ2 | Parquet writer `compression='snappy'` diverges from PR #259's `COMPRESSION 'ZSTD'`. PyArrow analog should be `compression='zstd'` for dataset-wide encoding consistency. | A14 uses `compression='zstd'`; precedent citation added (`materialize_history_enriched_pre_game_features.py:1041–1052`). |
| **N5** | T04 | Proposed YAML-block research_log template does not match PR #259's actual Markdown bold-label entry shape (`## YYYY-MM-DD — <title>` then `- **<Label>:** <value>`). | T04 template replaced with full Markdown bold-label form mirroring PR #259's research_log lines 79–103, including `### Category`, `### Step scope`, `### What`, `### Why`, `### How`, `### Findings`, `### What this means`, `### Decisions taken`, `### Decisions deferred`, `### Thesis mapping`, `### Open questions`, `### Acknowledged trade-offs`. |
| **N6** | OQ3 / audit JSON per_feature_traceability | `computation` field as Python-expression string (`df[focal_col] - df[opponent_col]`) is brittle (pandas-API-coupled) and not examiner-friendly. Symbolic formula with literal source-column names is reproducible across pandas/PyArrow drift and machine-checkable against `source_columns`. | Audit JSON per-feature `computation` field uses symbolic formula (e.g., `"focal_prior_match_count - opponent_prior_match_count"`); OQ3 rewritten as RESOLVED. |

### Round 1 item-by-item results (20 of 20 substantive PASS or PASS-WITH-NIT)

`Q1 PASS` Outcome A correct · `Q2 PASS` Direct execution barred · `Q3 PASS` Filename/path conventions repo-conventional · `Q4 PASS` Feature count exactly 33 (10×3 + 3) · `Q5 PASS` Output schema 37 columns · `Q6 PASS` Row count 44418 / distinct 22209 source-of-truth verified · `Q7 PASS-WITH-N6` Computation rules correct · `Q8 PASS` Audit JSON non-vacuous · `Q9 FAIL→N3` MD §-structure precedent misrepresented (structure itself fine) · `Q10 FAIL→N6` Per-feature traceability format · `Q11 PASS` No status YAML / closure work · `Q12 PASS` No Phase 03 / baseline · `Q13 FAIL→N5` Research_log shape · `Q14 PASS-WITH-N4` Determinism guarantees · `Q15 PASS` Dtype heterogeneity acceptable · `Q16 PASS` Halting falsifier chain sufficient · `Q17 FAIL→N1` `cutoff_time_filter_structural_check` value · `Q18 PASS-WITH-N2` Row count assertion brittleness · `Q19 STRONG` Examiner-survivable (with N6) · `Q20 STRONG` Cross-game comparability.

### Planner self-flagged Round 1 risks (10 of 10 PASS or NIT)

`R1 PASS` validator-vs-runtime gap → 22-step falsifier chain · `R2 NIT (N4)` Boolean determinism → defer-and-measure acceptable but writer config corrected · `R3 PASS` notebook overwrite collision · `R4 PASS` audit verbosity intrinsic · `R5 PASS` per-feature traceability falsifiability · `R6 NIT (N2)` row count hard-coding → defence-in-depth · `R7 PASS` coverage target ≥95% is real target, ≥40 floor is sanity check · `R8 NIT` T03 Opus budget can be Sonnet with detailed plan · `R9 PASS` audit JSON `notes` length acceptable · `R10 PASS` module location at flat dataset level.

### Methodology defensibility

- **M1 (LogReg basis spans) — PASS.** The joint `(F1, F2, F3) = (focal−opp, (focal+opp)/2, |focal−opp|)` covers linear-in-{level, signed-gap, magnitude-gap} space; F3 is non-linear in (F1, F2) over the reals (rectified-linear coordinate); LogReg cannot reconstruct `|x|` from `(x, level)` alone, so F3 is genuinely additive to the basis.
- **M2 (F4 drop rationale) — PASS.** `matchup_h2h_focal_win_rate` has no audited opponent counterpart in the 24-tuple; pairing it would yield `(x, 1−x)` → affine `2x − 1` (zero linear-model information, zero tree-split effect). PR #268 `MATCHUP_HISTORY_TRANSFORM_DECISION` binds; A18 enforces via regex.
- **M3 (F5 N3 retention) — PASS.** PR #268 adjudication MD §4 retains the LogReg rank-2 redundancy note for `(either, both, xor)` since `either = both ∨ xor`. Plan suggests mirroring this note into the new 02_02_01 audit MD §3 caption for examiners reading only the new audit; non-blocking improvement.

## Adversarial cap status

- Round 1: APPROVE-WITH-NITS — 0 BLOCKERs, 6 NITs (all applied inline).
- Round 2: **not required** (the 3-round symmetric cap permits Round 2 only if Round 1 returns HOLD).

## Files inspected by reviewer

- `/Users/tomaszpionka/Projects/rts-outcome-prediction/.github/tmp/planner_output_mat.md` (Round 1 plan body)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_feature_scope.py` (binding constants, lines 135–167)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py` (PR #266 validator)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.json` (row_count=44418, distinct=22209)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_03/leakage_audit_sc2egset.md` (4-section structure; N3 counterevidence)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.md` (8-section structure; N3 counterevidence)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/materialize_history_enriched_pre_game_features.py` (lines 115, 1041–1052; N2 + N4 precedent)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (lines 79–103; N5 precedent)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md` (line 39; N1 spec-literal `"pass"` evidence)
- `/Users/tomaszpionka/Projects/rts-outcome-prediction/src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.md` (PR #268 binding contract; line 47 N3 LogReg redundancy retention; M3 evidence)

## Sources cited

- Bradley & Terry 1952, *Biometrika*: "Rank Analysis of Incomplete Block Designs" — Bradley-Terry difference-feature argument grounding F1.
- Hue & Vert ICML 2010: "On Learning with Kernels for Unordered Pairs" — symmetric kernel theory grounding F2 / F3 / F5.
- Zaheer et al. 2017: "Deep Sets" — permutation-invariant set functions (referenced in `02_FEATURE_ENGINEERING_MANUAL.md` §3 line 56).
- Kuhn & Johnson 2019, *Feature Engineering and Selection* — Lasso-screening for polynomial / interaction features (referenced in `02_FEATURE_ENGINEERING_MANUAL.md` §6 line 135; cited in `product` deferral rationale).
