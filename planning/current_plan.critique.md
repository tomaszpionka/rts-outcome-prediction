---
plan_ref: planning/current_plan.md
created: 2026-05-23
category: A
base_ref: 93240b19a7dc75e4a9c74d2c392f0c25091bc3ea
reviewer_model: reviewer-adversarial (Opus, Category A pre-execution methodology gate)
verdict: APPROVE-WITH-NITS
blockers: 0
authorizes_layer1_materialization: true
chat_second_pass_required_before_materialization: true
revision_rounds: 2
---

# Critique — SC2EGSet Step 02_01_02 materialization-execution plan (Category A pre-execution gate)

> Produced by `@reviewer-adversarial` in two passes. Pass 1 over the original
> planner-science draft returned HOLD-WITH-BLOCKERS (2 blockers, 7 nits N1-N7).
> Pass 2 (lightweight) over the user-revised plan returned APPROVE-WITH-NITS
> (zero blockers, 3 cosmetic nits). The revision applied Option X
> (features_audited = 7 PRE_GAME columns excluding the started_at anchor) + nits
> N1-N4 via a focused @planner-science revision turn. Nits N5-N7 are deferred to
> Layer-2 PR planning per the user's bounded-revision instruction.

## Verdict

**APPROVE-WITH-NITS — zero blockers; no required `current_plan.md` edit beyond
what the revision already applied. Authorizes materializing the Layer-1 draft
planning PR this turn.**

## Pass 1 — original-plan adversarial verdict (HOLD-WITH-BLOCKERS)

Outcome A defensibility: **PASS**. Sequenced choice — planning-only Layer 1 (2 files) authorising a future Layer 2 materialization PR — is consistent with the non-batching rule.

Eight user-mandated challenges:

1. **Feature/audit count consistency** — FAIL (BLOCKER 1). Plan said 7 (prose), 8 (T05 JSON + T03 test + Gate Conditions), and 11 (T01 cell 5 assertion) — three mutually inconsistent values.
2. **PR #233 design drift (focal/opponent_matchup → race_pair)** — PASS-WITH-NIT (N1). Validator allows the 11-tuple; symmetric `race_pair` improves Invariant I5 satisfaction. Add T04 regression assertion.
3. **Identity columns NOT features + `started_at` classification** — FAIL (BLOCKER 2). `started_at` was listed in `features_audited` despite being CONTEXT per CROSS-02-00 §5.1 line 360.
4. **Source-layer binding (MFC vs registry replay_players_raw/matches_flat)** — PASS-WITH-NIT (N2). MFC is the cleaned 1v1-scoped projection over registry-cited upstreams per `matches_flat_clean.yaml:178-189`. Add 1-paragraph binding justification to audit MD §2.
5. **No strict `<` filter** — PASS. SQL contains only equality JOINs + ORDER BY on started_at.
6. **Closure sequencing (U2.B)** — PASS. PR #229 → PR #230 precedent + non-batching step 8 supports separate closure PR.
7. **ChatGPT second-pass timing (U3.A)** — PASS-WITH-NIT (N3). Projection SQL is final at Layer-1 merge time. Clarify Gate Condition 12 to require verbatim quote of verdict.
8. **Non-batching discipline** — PASS-WITH-NIT (N4). Disambiguate File Manifest "11 files" arithmetic.

Two blockers: B1 feature-count contradiction; B2 `started_at` classified as feature. Both fixable by ~3-line edits across T02/T03/T05/T01/Gate Condition.

Seven nits: N1-N4 (recommended for application alongside the blocker fix); N5-N7 (Layer-2 / cosmetic, deferred).

## Pass 2 — revised-plan lightweight adversarial verdict (APPROVE-WITH-NITS)

Both blockers CLOSED; all four N1-N4 nits APPLIED; constraint-5 (no Option Y leakage) ENFORCED; zero scope creep.

- **B1 PASS** — every count occurrence normalised to 7 audited features across T01 (cell 5 assertion), T02 (dataclass docstring + new `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 7` constant + new `EXPECTED_AUDITED_FEATURE_COLUMNS` tuple), T03 (test 11 + new test 18 mutual-disjointness), T05 (JSON + MD §1/§6), Gate Conditions 2/6, Problem Statement, Evidence-distinctness ledger. Output Parquet preserved at 11 cols.
- **B2 PASS** — `started_at` explicitly NOT in `features_audited`; new `PROJECTED_CONTEXT_COLUMNS: tuple = ("started_at",)` constant + `projected_context_columns` JSON field as clearly non-feature carrier; examiner-clarity sentence "`started_at` is projected as a row-identity anchor only and is excluded from `features_audited`" appears in JSON notes + MD §1/§4 + Problem Statement + research_log + Evidence ledger.
- **N1 PASS** — T04 explicitly states the existing scaffold validator is re-invoked over the new 11-tuple `EXPECTED_OUTPUT_COLUMNS` and is expected to PASS unchanged because its column-name checks are allowlist-based (boundary-aware POST_GAME token equality + forbidden-skill token equality) with no hard-coded 9-tuple assertion.
- **N2 PASS** — T05 MD §2 includes the registry → MFC binding 1-paragraph justification with a YAML blockquote citing `matches_flat_clean.yaml:178-189` (`source_tables`, `join_key`, `filter`, `scope`).
- **N3 PASS** — Gate Condition 12 requires the ChatGPT verdict be **quoted verbatim** (not summarised) inside a Markdown blockquote prefixed with ISO YYYY-MM-DD date and model identifier.
- **N4 PASS** — File Manifest disambiguates: Layer-1 = 2 distinct files; Layer-2 = 11 distinct on-disk files presented as 12 manifest rows because the jupytext-paired notebook is 1 logical update across 2 paired files; on-disk total = 13 = 2 + 11.
- **Constraint 5 PASS** — No `CONTEXT_COLUMNS_PROJECTED` (Option Y) field exists. The two new JSON carriers `projected_context_columns` and `projected_identity_columns` are clearly non-feature by name and role. F-context-column-counted-as-feature falsifier + test 18 mutual-disjointness assertion enforce separation.

No-scope-creep checks — ALL PASS:
- Layer-1 diff = 2 files exactly.
- Layer-2 manifest unchanged file set.
- 27 falsifiers total (24 original + 3 new tightening additions: F-features-audited-not-7, F-context-column-counted-as-feature, F-examiner-clarity-sentence-missing).
- YAML frontmatter unchanged (category=A, branch, base_ref=`93240b19…`, date=2026-05-23).
- All 8 required `##` sections present.
- Decision banner (Outcome A), non-determinism classification, pipeline-section-status drift question all preserved.
- Defaults U1=raw, U2.B=separate closure, U3.A=ChatGPT during Layer 1 all preserved.

## Non-blocking nits (cosmetic; Layer-2 / process; carry forward)

- **N5 (Layer-2 nit, deferred)**: F-encoder-fit could be renamed F-encoder-fit-or-fold-leakage and made active even without an encoder fit.
- **N6 (Layer-2 nit, deferred)**: OQ7 (DuckDB UTC `SET TimeZone = 'UTC'` placement) — declare module-side placement as authoritative.
- **N7 (Layer-2 / cosmetic, deferred)**: Self-check #1 is 600+ words; one-paragraph TL;DR variant for audit MD §1.
- **Revision-cosmetic-1**: File Manifest arithmetic still has a "wait, recounting" thought-fragment; final number lands correctly. Cosmetic.
- **Revision-cosmetic-2**: T05 §4 re-asserts 7-features framing redundantly across §1/§6/T06/JSON/Problem Statement. Defensible for anchor-classification clarity. Cosmetic.
- **Revision-cosmetic-3**: Self-check #1 still 600+ words after revision. Cosmetic.

## Files inspected across both passes

- `/tmp/mat_plan.txt` (original plan body).
- `/tmp/mat_plan_v2.txt` (revised plan body).
- `reports/specs/02_00_feature_input_contract.md` (§5.1 line 360 `started_at = CONTEXT` verbatim verified).
- `reports/specs/02_03_temporal_feature_audit_protocol.md` (§6.1 lines 233-250 `pre_game` static-game-T-attribute exemption).
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` (lines 62-67 ALLOWED_PRE_GAME_SOURCE_TABLES; lines 287-315 `_is_forbidden_skill_column`; lines 466-500 `_check_no_post_game_tokens`; no hard 9-tuple assertion).
- `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_pre_game_source_layer.py` (line 105 `EXECUTED_AT_UTC_DATE` constant; lines 724-739 `_get_git_sha()` — non-determinism classification evidence).
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml` (lines 178-189 provenance block verbatim verified for N2).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (lines 2099-2272 Step 02_01_02 stub; lines 2233-2249 artifact_check + continue_predicate).
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` (lines 150-160 existing scaffold `DESIGNED_COLUMN_NAMES` 9-tuple).
- `planning/current_plan.md` (PR #234 plan — stale, overwritten by this PR's Layer-1 Write).
- `planning/current_plan.critique.md` (PR #234 critique — stale, overwritten by this PR's Layer-1 Write).
- `planning/current_plan.critique_resolution.md` (older stale file — deleted; not recreated).
