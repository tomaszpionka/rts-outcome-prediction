---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-24
plan_base_ref: a16d78c25f16aaf8fad4f2c362445212aac1a16b
plan_branch: feat/sc2egset-02-01-03-roadmap-stub
plan_step: "02_01_03 (Layer-1 ROADMAP-only stub design)"
plan_category: A
planning_pr: "PR #238"
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 6
---

# Reviewer-Adversarial Critique — Step 02_01_03 ROADMAP-Only Stub Planning PR

## Verdict

**APPROVE-WITH-NITS.** Outcome A (Layer-1 planning PR materializing only `planning/current_plan.md` + `planning/current_plan.critique.md` for a future ROADMAP-only Layer-2 execution PR that inserts Step `02_01_03` under Pipeline Section `02_01`) is the correct next atomic unit. All 10 substantive challenges resolve to OK on direct repository evidence at `a16d78c25f16aaf8fad4f2c362445212aac1a16b`. Six nits are documentation/clarification refinements for the future Layer-2 execution PR's ROADMAP block draft text — they have been incorporated into the Future ROADMAP block within `planning/current_plan.md`, and none block the Layer-1 planning PR.

## Per-challenge findings

| # | Challenge | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Outcome A vs D (hygiene defect first?) | OK | CROSS-02-02 §6.1 amendment is pre_game-scoped (race vs selectedRace vocabulary clarification); tranche-2 = §6.2 families. PR #237 closure entry explicitly defers the §6.1 amendment as a future Category E spec-only PR target. PR #236 audit JSON: `features_audited` length 7 over 5 closed tranche-1 families; `verdict: PASS`; this satisfies the 02_01_02 ROADMAP `continue_predicate` clause "NON-vacuous PASS." PR #237 closed the status-chain — no contradiction. Outcome A is correct. |
| 2 | Phase 03 barred (Outcome C blocked) | OK | `PHASE_STATUS.yaml`: Phase 02 `in_progress`, Phase 03 `not_started`. Per `docs/PHASES.md`, Phase 02 has 8 canonical pipeline sections (`02_01..02_08`); `PIPELINE_SECTION_STATUS.yaml` shows 1 of 8 complete (`02_01: complete` only). Phase 03 placeholder reads "Steps to be defined when Phase 02 gate is met." Phase 03 baseline planning is barred. |
| 3 | Closure evidence sufficient | OK | `research_log.md` top entry 2026-05-24: `closure_status: closed`, `status_yaml_state: complete`, `leakage_audit_state: post_materialization_pass`, `features_audited_count: 7`, `row_count: 44418`. Audit JSON: `verdict: "PASS"`, `audit_pr: "PR #236"`, `future_leak_count: 0`, `post_game_token_violations: 0`, `normalization_fit_scope: training_fold_only`. All three closure fields and the audit predicate clauses are cleared. |
| 4 | ROADMAP lacks 02_01_03 block | OK | `grep -n "step_number" ROADMAP.md` shows the last Phase 02 block is `02_01_02` at line 2102. Next heading: `## Phase 03 — Splitting & Baselines (placeholder)` at line 2276. No `02_01_03` exists. |
| 5 | Family scope correct (6 history) | OK | Registry CSV rows 7–12 are exactly the 6 history_enriched_pre_game families named in the plan: `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `reconstructed_rating`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`. §10 verdict audit CSV confirms 5 `allowed` + 1 `allowed_with_caveat` (the caveat is on `cross_region_fragmentation_handling`, leakage mode `cross_region_history_drop` — matches plan exactly). No `in_game_snapshot` or `blocked_or_deferred` rows are pulled in. |
| 6 | Temporal/leakage framing | OK | All three ml-protocol.md failure modes are present in the plan's halt_predicate enumeration: (a) rolling-target-inclusion (G-L-7), (b) h2h-target-inclusion (G-L-7), (c) normalization fit-scope (G-CS-6 / Invariant I3 normalization-leakage). Plus rating-outcome (G-L-4), tracker exclusion (Invariant I3 Amendment 2), asymmetric construction (Invariant I5/RISK-24), cross-region-history-drop (RISK-20, the `allowed_with_caveat` mode). Plan also covers cold-start magic-number gate (G-CS-1..G-CS-5). The strict-`<` framing is verbatim in the registry (`history_time < target_time`) and in CROSS-02-02 §6.2. **NIT N1**: G-L-3 ("target-match final state") was initially only implicit in the strict-`<` rule — now enumerated explicitly in the Future ROADMAP block per N1 resolution. |
| 7 | Non-batching discipline | OK | Layer-2 execution PR declares no notebook, no validator, no source, no test, no artifact, no status YAML flip, no research_log; only ROADMAP block + version/CHANGELOG/INDEX tail + 2 persisted planning files. Mirrors `data-analysis-lineage.md` "Non-batching rule" sequence step 1. Layer-1 PR is 2 files only (`current_plan.md` + critique). |
| 8 | File manifest correct | OK | 6-file Layer-2 manifest exactly matches PR #232 precedent (verified via `gh pr view 232`: `CHANGELOG.md`, `planning/INDEX.md`, `planning/current_plan.critique.md`, `planning/current_plan.md`, `pyproject.toml`, `ROADMAP.md` — 6 files). The planning/INDEX.md update at Layer-2 must archive both PR #237 AND the Layer-1 planning PR (since the Layer-1 PR's 2-file scope cap precludes it updating INDEX.md itself). Manifest is correct. |
| 9 | Version bump correct | OK | `pyproject.toml` confirmed at `3.70.1`. `.claude/rules/git-workflow.md` requires minor bump for feat/. PR #232 precedent: `3.66.0 → 3.67.0` (minor, feat-family) — confirmed via PR body. Layer-2 bump `3.70.1 → 3.71.0` is correct. |
| 10 | Status YAMLs untouched | OK | PR #232's diff confirmed no STEP_STATUS.yaml change (`02_01_02` row was added later by PR #237 only). Plan's "Files NOT touched (negation)" list includes STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml. Layer-2 Gate Condition specifies "status YAMLs byte-unchanged". Repo policy unchanged; correct precedent followed. |
| 11 | Other blockers | NIT | See nits N1–N6 below. None block APPROVE. |

## Blockers

**None.** All 10 substantive challenges resolve to OK on direct evidence verification. The Layer-1 plan as proposed is merge-eligible for the planning-only PR.

## Nits (non-blocking; all incorporated into the Future ROADMAP block in `planning/current_plan.md`)

- **N1 — G-L-3 explicit in halt_predicate.** G-L-3 ("no target-match final state for game T") is implicit in the strict-`<` rule but should be enumerated separately in the halt_predicate to mirror CROSS-02-02 §10's full G-L-1..G-L-9 vocabulary. **Status: addressed** — the Future ROADMAP block `gate.halt_predicate` now lists G-L-3 explicitly alongside G-L-1, G-L-4, G-L-7. Non-blocking because Invariant I3 strict-`<` structurally enforces it.

- **N2 — `in_game_history_aggregate` lexical-confusion note.** `sc2egset.history_enriched_pre_game.in_game_history_aggregate` is lexically confusable with `sc2egset.in_game_snapshot.*` families. **Status: addressed** — the Future ROADMAP block `description` field includes the verbatim CROSS-02-02 §6.2 row-6 note: "IN_GAME_HISTORICAL columns are RETAINED IN SCOPE for `history_enriched_pre_game` use; they remain forbidden as direct game-T pre-game features (which would be an Invariant I3 violation)." The plan Scope section also carries a lexical-confusion-note rider on family 6.

- **N3 — Lineage-position comment.** The Step 02_01_03 ROADMAP block should declare its own lineage-position framing (e.g., "artifact #1 of N for Step 02_01_03 readiness"), analogous to PR #236's audit JSON `lineage_position` framing. **Status: addressed** — the Future ROADMAP block `description` field includes: "Lineage position: ROADMAP stub is artifact #1 of N for Step 02_01_03 readiness (subsequent artifacts: notebook scaffold + one validator, tranche-2 source/anchor/cold-start adjudication, materialization-execution plan, materialization-execution, closure). This is the SECOND materialization tranche of Pipeline Section 02_01."

- **N4 — `predecessors: "02_01_02"` only.** The Future ROADMAP block `predecessors` field should be `"02_01_02"` only; `02_01_01` is a transitive predecessor (registry catalog) and must NOT be listed as a direct predecessor. **Status: addressed** — the Future ROADMAP block `predecessors` field is `"02_01_02"` (string, not list). Layer-2 Gate Condition explicitly enforces this falsifier.

- **N5 — Cross-region fragmentation adjudication gating.** The `cross_region_fragmentation_handling` family's §10 verdict is `allowed_with_caveat` with leakage mode `cross_region_history_drop`. The Future ROADMAP block `gate.halt_predicate` should gate materialization on a CROSS-02-02 §6.2 row-5-style adjudication selecting (a) strict-exclusion, (b) dual-path, or (c) sensitivity-indicator co-registration. **Status: addressed** — the Future ROADMAP block `gate.halt_predicate` now includes this falsifier explicitly, and the `stratification` field flags the deferral.

- **N6 — §10 audit re-run gating.** PR #237's deferred questions include re-running a §10-style design-time per-family verdict audit for the history_enriched_pre_game families. The Future Step 02_01_03 ROADMAP block's `continue_predicate` should explicitly require this re-run (or a non-vacuous justification for not re-running) before any tranche-3 materialization PR opens. **Status: addressed** — the Future ROADMAP block `gate.continue_predicate` now says: "a re-executed §10 audit over the 6 history rows (distinct from the PR #229 design-time audit that covered the catalog at registry-creation time) is required before tranche-3 may begin, OR a non-vacuous justification for not re-running must be recorded in the materialization PR's research_log entry."

## Recommendation

**APPROVE-WITH-NITS.** Persist the Layer-1 planning PR (2-file diff: `planning/current_plan.md` + `planning/current_plan.critique.md`). All six nits have been pre-emptively incorporated into the Future ROADMAP block draft text within `planning/current_plan.md` — the Layer-2 executor reads the plan and inherits the nit resolutions as the canonical ROADMAP block to insert. The plan is methodologically defensible and ready for user review before any Layer-2 execution.

## Bounded-prompt deviation note

The bounded autonomous prompt that authored this Layer-1 PR caps the diff at exactly 2 files (`planning/current_plan.md` + `planning/current_plan.critique.md`). Repo precedent (PR #235) historically bundled minor version bumps and INDEX.md archives with Layer-1 planning PRs. This Layer-1 PR deviates from that precedent by deferring the version bump, CHANGELOG entry, and INDEX.md archive to the Layer-2 execution PR. The deviation is intentional and disclosed in:

- the Layer-1 PR body explicitly,
- the plan body §Version Bump,
- the plan body §Execution Steps (Layer-2 inherits the dual archive of PR #237 and the Layer-1 planning PR in INDEX.md update L2-T04).

The deviation is non-blocking because it preserves all scientific content and amplifies (rather than dilutes) the non-batching discipline mandated by `.claude/rules/data-analysis-lineage.md`. The Layer-1 PR's title and body must, however, clearly distinguish the Layer-1 2-file diff from the Layer-2 6-file diff so reviewers do not mistake the diff size for the full scope.

## Reviewer credentials

- **Agent**: reviewer-adversarial (Category A pre-execution gate per `.claude/rules/data-analysis-lineage.md`).
- **Model**: claude-opus-4-7[1m].
- **Date**: 2026-05-24.
- **Base ref reviewed**: `a16d78c25f16aaf8fad4f2c362445212aac1a16b` (master HEAD post PR #237).
- **Rounds**: 1 (zero rounds of revision required; APPROVE-WITH-NITS reached on first pass).
- **Adversarial cap**: per `feedback_adversarial_cap_execution.md` (3-round symmetric cap) — 1 of 3 used.
