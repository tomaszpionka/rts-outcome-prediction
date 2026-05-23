---
plan_ref: planning/current_plan.md
created: 2026-05-23
category: A
base_ref: a4cc290f29c16378022915b51d2ae0fa52d602e8
reviewer_model: reviewer-adversarial (Opus, Category A pre-execution methodology gate)
verdict: APPROVE
blockers: 0
authorizes_layer1_materialization: true
chat_second_pass_required_before_materialization: true
revision_rounds: 2
---

# Critique — SC2EGSet Step 02_01_02 source/anchor/race-column adjudication (Category A pre-execution gate)

> Produced by `@reviewer-adversarial` in two passes. Pass 1 over the original
> planner-science draft returned APPROVE-WITH-NITS (zero blockers, 8 nits).
> Pass 2 (lightweight) over the revised plan returned APPROVE (zero blockers,
> 2 non-blocking process notes). The revision applied user-selected nits
> N1-N5 + N8 via a focused `@planner-science` revision turn; nits N6 (Layer-2
> deferred) and N7 (parent-action caveat) are recorded but not applied to the
> Layer-1 plan body.

## Verdict

**APPROVE — zero blockers; no required `current_plan.md` edit beyond what the
revision already applied. Authorizes materializing the draft planning PR this
turn.**

## Pass 1 — original-plan adversarial verdict (APPROVE-WITH-NITS)

Six user-mandated challenges (all PASS or PASS-WITH-NIT, none blocking):

1. **Non-batching defensibility (Outcome A vs B)** — PASS WITH NIT. Lineage rule "halt on surprising results" applies (Random-vocabulary asymmetry was not previously documented). Nit N5: novelty framing was overclaimed (PR #233 plan already commits to RISK-26 direction; revision narrows scope to elevating + settling + reconciling).
2. **Q2 anchor scope (Phase-02 vs Phase-03)** — FAIL with actionable NIT. CROSS-02-03 §6.1 confirms anchor is row-identity only for tranche-1 static game-T attributes; Q2 was inflated to a Phase-02 deliverable. Nit N3: demote to Q2(a) BINDING + Q2(b) Phase-03 RECOMMENDATION ONLY.
3. **Q3 race-column "post-decision leak" framing** — PASS-WITH-MAJOR-NIT. Critical missed finding: the project has already adjudicated this via `matches_long_raw.yaml:101-103` and `matches_history_minimal.yaml:52-53` (race = PRE_GAME analytical canon; selectedRace = dropped). RISK-26 framing is in tension with the documented project decision, not aligned. Nit N1: reframe Q3 as cleaning-layer RATIFY-vs-AMEND with both outcomes live.
4. **MHM faction contradiction routing** — FAIL. The MHM YAML at line 52 ALREADY answers the provenance question. Nit N2: resolve OQ1 as DOCUMENTED (not BLOCKING); remove `_MHM_VIEW_DEFINITION_QUERY` constant; remove `duckdb_views()` probe.
5. **Layer-2 minimal scope** — PASS WITH NITS. 9-file manifest is justified per `python-code.md` mirrored-tree rule + PR #229 CSV+MD precedent. Nits absorbed; none blocking.
6. **Layer-1 2-file diff discipline** — PASS. Plan body proposes zero Layer-1 changes beyond the 2 planning files. Nit N7: parent must clear stale `current_plan.md` / `current_plan.critique.md` / `current_plan.critique_resolution.md` before Write.

Standard methodology checks (8 required `##` sections; YAML frontmatter; PIPELINE_SECTION_STATUS justification; falsifier list; 5-evidence-types distinctness) — ALL PASS.

Eight nits recorded: N1 cleaning-layer reconciliation (MAJOR); N2 over-scoped U4; N3 Q2 scope; N4 Random count precision; N5 novelty narrow; N6 lineage_position (Layer-2 nit only); N7 stale-file parent-action caveat; N8 planner self-improvement (MHM YAML read).

## Pass 2 — revised-plan lightweight adversarial verdict (APPROVE)

All N1-N5 + N8 PASS with verbatim evidence:

- **N1 PASS** — Problem Statement quotes `matches_long_raw.yaml:101-103` + `matches_history_minimal.yaml:52-53` verbatim; Q3 framed as RATIFY vs AMEND with both live; T04 §4 requires rationale ≥ 250 words; spec patches proposed under Q3.AMEND only.
- **N2 PASS** — OQ1 explicitly "DOCUMENTED, NOT BLOCKING"; `_MHM_VIEW_DEFINITION_QUERY` not a constant; `duckdb_views()` probe removed from T01.
- **N3 PASS** — Q2(a) BINDING row-identity + Q2(b) Phase-03 RECOMMENDATION ONLY; artifact MD §3 states "binding decision is made in Phase 03 planning, NOT in this Layer-2 artifact".
- **N4 PASS** — Plan body says "10 `Rand` rows + 1,110 blank rows (cleaned-view-normalized to `Random`)".
- **N5 PASS** — Contributions listed as (a) elevating to thesis-citable artifact, (b) settling column-name + canonicalisation + row-retention dimensions PR #233 left unspecified, (c) reconciling cleaning-layer with RISK-26; "Random handling newly discovered" explicitly disavowed.
- **N8 PASS** — MHM YAML reading performed in revision (not deferred to Layer-2 T01).

No-new-scope-creep checks — ALL PASS:
- Layer-1 diff = exactly 2 files.
- Layer-2 manifest = 9 future-PR files (unchanged at file-list level).
- No new ROADMAP / status YAML / research_log / artifact / notebook / source-test / Phase-03 file in Layer-1.
- Falsifier list keeps `F-Q3-race-post-decision-chosen` AND adds `F-Q3-prior-decision-silently-reversed`.
- YAML frontmatter complete (category A, branch, base_ref a4cc290f, date 2026-05-23, chat_second_pass true).
- Gate Condition has 12 numbered items including Q2(a)/(b) split, Q3 RATIFY/AMEND, lineage_position.
- All 8 required `##` sections present.
- Cleaning-layer YAML verbatim quotes accurate.
- CROSS-02-03 §6.1 cite accurate.

## Non-blocking nits (Layer-2 / process; carry forward)

- **N6 (Layer-2 nit, deferred):** Layer-2 artifact MD §6 should include the `lineage_position` field (the revised plan T04 §6 already records this requirement).
- **N7 (parent-action, satisfied):** Parent cleared `planning/current_plan.md`, `planning/current_plan.critique.md`, and `planning/current_plan.critique_resolution.md` before Write — confirmed by the 2-file Layer-1 diff.
- **Pass-2 process note 1:** `F-Q3-prior-decision-silently-reversed` validator may need to extract rationale prose from the artifact MD it just wrote — minor circular-IO pattern to resolve at Layer-2 planning if awkward.
- **Pass-2 process note 2:** Stale-file clearance is a parent-orchestrator responsibility; recorded in the plan's "Materialization caveats" note.

## Files inspected across both passes

- `/tmp/revised_plan.txt` (revised plan body).
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml` (lines 101-103 verbatim).
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_history_minimal.yaml` (lines 52-53 verbatim).
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml`.
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat.yaml`.
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml`.
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/replay_players_raw.yaml`.
- `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py`.
- `reports/specs/02_02_feature_engineering_plan.md` §6.1.
- `reports/specs/02_03_temporal_feature_audit_protocol.md` §6.1 (lines 233-250 verbatim).
- `thesis/pass2_evidence/methodology_risk_register.md` (RISK-26 line 479-492 verbatim).
- `planning/current_plan.md` (PR #233 plan — stale, overwritten by this PR's Layer-1 Write).
- `planning/current_plan.critique.md` (PR #233 critique — stale, overwritten by this PR's Layer-1 Write).
- `planning/current_plan.critique_resolution.md` (PR #233 critique-resolution — stale, deleted; not recreated).
