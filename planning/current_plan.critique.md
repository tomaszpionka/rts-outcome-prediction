---
plan_ref: planning/current_plan.md
created: 2026-05-22
category: A
base_ref: e96374fef43ce06d03098d9bea8296b4ff74a409
gate_reviewer: reviewer-deep (Layer-1 draft-PR gate)
adversarial_status: DEFERRED to Layer-2 / scaffold turn (reviewer-deep recommendation)
---

# Critique — SC2EGSet Step 02_01_02 ROADMAP-only stub plan (Layer-1 gate)

> Produced by `@reviewer-deep` as the draft-PR gate for the Layer-1 planning PR.
> Per the orchestration routing rule, reviewer-adversarial is escalated only on a
> reviewer-deep blocker OR a material leakage/status/Phase-03 effect; reviewer-deep
> found neither and recommends **DEFER-TO-LAYER-2** (see escalation section). The
> full Category A reviewer-adversarial pre-execution critique is therefore produced
> before the FUTURE Layer-2 EXECUTION turn, not for this stub-only draft PR.

## Verdict

**APPROVE-WITH-NITS — zero blockers.** The plan is correct under repo taxonomy,
the non-batching rule, the source-of-truth hierarchy, and SemVer policy. Every
load-bearing claim traces to an on-disk artifact the reviewer verified. The
framing is honest — it never overclaims leakage clearance, and it actively
preserves the PR #229 / PR #230 evidence distinction that the source artifacts
themselves enforce. The three nits are non-blocking and belong in the Layer-2
execution spec, not in a re-plan; they are folded into plan tasks T01 (N1), T03
(N2), and the Layer-2 final gate (N3).

## Per-check results (the 10 required gate checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Outcome A correct under taxonomy + non-batching rule | PASS | docs/TAXONOMY.md Step §: `{PHASE}_{SECTION}_{STEP}`, sequential within section → `02_01_02` legit under `02_01`. data-analysis-lineage.md mandates "ROADMAP stub only" as sequence step 1. PR #230 research_log: closure "does NOT authorise the start of `02_01_02`; the gate to **design** it is now open." |
| 2 | No batching of ROADMAP + notebook + artifact + status/log | PASS | Layer 2 = 6 files; T04 forbids any STEP_STATUS/artifact/notebook/spec/research_log/thesis in the diff; stub `outputs` marked "(planned, NOT created)"; `research_log_entry` + `gate.artifact_check` explicitly deferred. |
| 3 | Does not start Phase 03 | PASS | T01 inserts the stub *before* `## Phase 03` (ROADMAP ~line 2101); stub `phase: "02 -- Feature Engineering"`; out-of-scope excludes Phase 03. |
| 4 | No overclaim of empirical leakage clearance | PASS | On-disk `leakage_audit_sc2egset.json` `features_audited:[]`, verdict PASS on §5(a) vacuity; `.md` self-describes as non-substituting for a future post-materialization audit. The plan mirrors this: `continue_predicate` requires a future *non-vacuous* CROSS-02-01 PASS; literal "NO feature value is materialized in this ROADMAP-stub PR" present. |
| 5 | Uses the closed 02_01_01 artifacts correctly | PASS (path nit N1) | All cited inputs exist on disk (registry CSV/MD, §10 verdict CSV/MD, leakage_audit JSON/MD, the 4 LOCKED specs, matches_history_minimal.yaml, step_template.yaml). Stub `outputs` correctly marked "(planned, NOT created)". See N1 on the registry path-naming. |
| 6 | Keeps PR #229 §10 and PR #230 CROSS-02-01 evidence distinct | PASS | Distinction enforced by the source artifacts (leakage_audit_sc2egset.md §5 lines 82-90; .json notes). Plan out-of-scope keeps them distinct; §10 design-time verdict (26 catalog rows) ≠ future post-materialization CROSS-02-01 audit (non-empty features_audited). |
| 7 | Planned files minimal + repo-consistent | PASS | All 6 Layer-2 files exist on disk today (edits, not surprise creations); no forbidden path in either layer; Layer 1 = exactly the 2 planning files. |
| 8 | Version bump 3.66.0 → 3.67.0 (minor) follows git-workflow SemVer | PASS | git-workflow.md: "minor for feat/refactor/docs". feat/ branch → minor correct; on-disk pyproject = 3.66.0 → 3.67.0 is the next minor. |
| 9 | Materializable into a draft PR WITHOUT execution this turn | PASS | Layer 1 commits only the 2 planning files; no ROADMAP/status/artifact touch this turn. Matches the PR #231 draft-PR-first precedent (commits 2c78c6e4 / af1fc934). |
| 10 | Any blocker explicit | PASS | Plan flags its own highest-risk item (the 5-family scope decision) and routes it to adversarial review before the future scaffold PR. No hidden blocker; none found. |

## Additional verifications

- **Stub under section 02_01; stub-only PR does not change PIPELINE_SECTION_STATUS — PASS.**
  STEP_STATUS has `02_01_01: complete`, no `02_01_02` row; PIPELINE_SECTION_STATUS
  has `02_01: complete` (only Phase-02 section). Adding NO STEP_STATUS row leaves
  the derivation untouched → `02_01` stays `complete`. The "status reopen
  disclosure" is real and on disk in BOTH places the plan cites: CHANGELOG.md
  line 53 (PR #230 block) and per-dataset research_log.md line 18. Not invented.
  Sub-concern resolved: `02_01 = complete` (sole listed section) is consistent
  with PHASE_STATUS Phase 02 = `in_progress` — PIPELINE_SECTION_STATUS lists
  sections incrementally (1-of-8 canonical sections added; phase `in_progress`
  when ANY section is in_progress or complete). NOT a derivation bug.
- **Stub field schema matches the closed 02_01_01 block + step_template.yaml — PASS.**
  Closed block (ROADMAP ~1914-2097) uses the same field set; stub conventions
  (`predecessors: "02_01_01"`, invariants I3/I5/I6/I7/I8/I9/I10, gate triad,
  outputs marked planned) match both the closed block and step_template.yaml. All
  cited invariant IDs valid (I3 temporal, I5 symmetric, I6 report-with-code, I7
  magic numbers, I8 cross-game, I9 pipeline discipline, I10 provenance).
- **5 pre_game families exist with the claimed classification — PASS.**
  Registry CSV verified one-for-one: `focal_race_with_opponent_race_pair`,
  `map_type_encoded`, `patch_version_encoded`, `matchup_encoded`,
  `is_mmr_missing_flag` — all `prediction_setting=pre_game`, `status=allowed`,
  `cold_start_handling=G-CS-1`, `candidate_leakage_modes=none`,
  `allowed_cutoff_rule=snapshot_at_match_start`. The 6 deferred
  `history_enriched_pre_game` families carry genuine leakage modes — deferring
  them to isolate distinct leakage-falsifier regimes is methodologically sound.

## Methodology critique

- **Reproducibility chain (fragile link, → N1).** The closed `02_01_01` ROADMAP
  block (~lines 2006/2008) names `02_01_01_feature_family_registry_sc2egset.csv`,
  but the on-disk artifact is `02_01_01_feature_family_registry.csv` (no
  `_sc2egset`). The catalog exists; only the closed block's *declared path*
  drifts. The new `02_01_02` stub must cite the registry by its TRUE on-disk name
  in its own `inputs` (the plan already does so) and must NOT propagate the stale
  path. Quarantining the stale string out of scope is correct (editing the closed
  block would break gate (a)).
- **Temporal discipline.** Nothing in this diff feeds a model — it is a ROADMAP
  stub. The riskiest *recorded* operation is the tranche selection; the 5 chosen
  families all declare `snapshot_at_match_start` + `candidate_leakage_modes=none`
  (race/map/patch/matchup/mmr-missing are match-setup facts known at T, not
  post-game outcomes). No `.shift()`, window, or normalization stat is computed
  here. Safe.
- **Honest framing.** The plan says `02_01_01` materialized "no feature *value/
  column*" — TRUE (registry is a catalog; leakage_audit JSON `features_audited:[]`
  confirms). It never says "no artifact exists". No overstatement found.
- **Cross-game generalization.** The 5 pre_game families (race/civ, map, patch,
  matchup, mmr-missing) are match-setup facts available in both SC2 and AoE2
  without in-game reconstruction. Deferring the 11 SC2-tracker-bound
  `in_game_snapshot` families front-loads the cross-game-symmetric subset —
  the opposite of silent SC2-drift. Stub invariant I8 correctly cited.

## Non-blocker follow-ups (tracked for Layer-2 execution)

1. **N1 — Registry-artifact path drift.** Layer-2 stub `inputs` must cite the
   registry by its true on-disk name `02_01_01_feature_family_registry.csv/.md`,
   NOT the closed block's stale `..._registry_sc2egset.csv` path. Do NOT fix it
   inside the closed `02_01_01` block (would violate gate (a)); fix only in the
   new stub's own citations. (Folded into plan T01 step 4.)
2. **N2 — Pre-empt the Phase-02 derivation question.** The Layer-2 stub /
   CHANGELOG should note that `02_01 = complete` (sole listed section) is
   consistent with Phase 02 `in_progress` because PIPELINE_SECTION_STATUS lists
   sections incrementally (1-of-8 → phase `in_progress`). Prevents a future
   reviewer from flagging a non-bug. (Folded into plan T03 CHANGELOG `### Notes`.)
3. **N3 — §10 / CROSS-02-01 non-substitution language in stub prose.** Verify at
   Layer-2 execution that the stub's `description` / `continue_predicate` text
   actually restates the distinction (not only the inputs list). The closed block
   already does (lines 2060-2066), so copying conventions should carry it —
   confirm, don't assume. (Tracked for the Layer-2 final gate; the stub
   `continue_predicate` in this plan already carries the non-substitution clause.)

## Honesty audit

Framing accurate; every tested claim traces to an on-disk artifact:
- "vacuous/zero-materialization audit" → leakage_audit_sc2egset.json
  `features_audited:[]`, verdict PASS on §5(a) vacuity. Accurate.
- "status reopen pre-disclosed in PR #230 CHANGELOG + research_log" →
  CHANGELOG.md line 53, research_log.md line 18. Accurate, not invented.
- "OQ4 resolved by PR #231" → PR #231 merged at e96374fe; manifest token present.
  Accurate.
- "5 pre_game families, status=allowed, leakage_modes=none, G-CS-1" → registry
  CSV rows verified one-for-one. Accurate.
- The one drift (registry path `_sc2egset`) is a pre-existing ROADMAP error the
  plan quarantines, not an overstatement by the plan.

## Adversarial-escalation recommendation: DEFER-TO-LAYER-2

A recorded-but-not-executed scope decision in a ROADMAP stub does NOT materially
affect leakage semantics at the draft-planning-PR stage. The trigger for
adversarial review is the *execution* of leakage-affecting code, not its *design
on paper*. Here: (a) no feature column is materialized this turn (stub outputs
explicitly "planned, NOT created"); (b) the actual leakage computation — the
non-vacuous CROSS-02-01 audit over a non-empty `features_audited` — lands in a
separate future PR; (c) that future PR will itself get a Category A
reviewer-adversarial gate, the correct and sufficient checkpoint. The families
the plan would record are the *least* leakage-contested in the registry
(`candidate_leakage_modes=none`, `snapshot_at_match_start`); the contested
rolling-window/rating families are explicitly deferred. No blocker found; nothing
in this stub asserts empirical leakage clearance, flips a status gate, or starts
Phase 03. Per the routing rule (escalate only on a reviewer-deep blocker OR a
material leakage/status/Phase-03 effect), neither trigger fires. Reviewer-adversarial
is correctly deferred to the Layer-2 / scaffold turn, where the full Category A
pre-execution critique of the materialization-scope decision MUST be produced
before any feature value is materialized.

## Draft-PR-first workflow correction — PR #232

PR #232 already exists before Layer-2 execution. The plan now uses literal `PR #232` in all future execution outputs instead of `PR #<this PR>` placeholders. The plan distinguishes the current 2-file planning diff, the 4 future execution files, and the 6-file final tracked PR diff. No scientific scope changed.

## Category-A pre-execution adversarial critique — PR #232 (Layer-2 gate)

> Produced by `@reviewer-adversarial` on 2026-05-22 against branch HEAD `146013e1`
> (base master `e96374fe`). This is the Category-A pre-execution methodology gate
> that the reviewer-deep Layer-1 gate deferred (DEFER-TO-LAYER-2). It must be in the
> record before any Layer-2 ROADMAP execution turn begins.

### Verdict

**APPROVE-WITH-NITS — zero blockers, zero conditions, no `current_plan.md` edit required.**
The ROADMAP-only stub is methodologically defensible as a recorded design decision.
The two methodology-sensitive questions reviewer-deep deferred — the 5-family scope
cut and the `is_mmr_missing_flag` placement — are both adjudicated defensible, the
flag's placement *positively mandated* by the LOCKED CROSS-02-02 spec.

### `is_mmr_missing_flag` decision: KEEP-IN-TRANCHE-1

- **Cannot leak:** registry `snapshot_at_match_start`, `candidate_leakage_modes=none`,
  `G-CS-1`; it is an `MMR=0` sentinel read from the replay's own pre-game header — no
  history window, no outcome dependency, no tracker event. Invariant #3 safe.
- **Not degenerate:** ~84% TRUE / 16% FALSE in the 44,418-row prediction scope
  (37,422 player-rows flagged; MMR = 83.95% missing per the 01_04_01 missingness
  ledger, MAR-primary).
- **Spec-mandated placement:** `reports/specs/02_02_feature_engineering_plan.md`
  line 228 ("use the missingness flag, not the MMR scalar; rating proxies must come
  from `history_enriched_pre_game`") and line 539 (designates `is_mmr_missing` the
  canonical first SC2 validation module). Deferring it with the rating/history
  families would CONTRADICT the locked spec — the spec deliberately separates the
  pre_game *missingness flag* from the deferred *rating proxies* / MMR scalar.
- **Caveat (deferred to materialization PR, nit 1):** the flag is a replay-
  *provenance* proxy (ladder vs. tournament), not a skill measure, and has no AoE2
  analog. The future materialization report must characterize it as provenance, not
  skill — but that is the materialization PR's burden, not a reason to move it.

### Focus-area adjudications (all 10 — all defensible)

1. `02_01_02` ROADMAP-only stub is the correct next atomic unit — YES (TAXONOMY
   sequential steps; data-analysis-lineage sequence step 1; closed-block precedent).
2. 5-family pre_game scope defensible — YES (the only rows with leakage_modes=none +
   G-CS-1 + snapshot_at_match_start; principled cut; not over/under-scoped).
3. `is_mmr_missing_flag` — KEEP-IN-TRANCHE-1 (see above).
4. Avoids materialization / notebooks / artifacts / status flips / research-log writes — YES.
5. PR #229 §10 vs PR #230 CROSS-02-01 evidence kept DISTINCT — YES (continue_predicate
   states §10 does not substitute for the post-materialization audit).
6. No overclaim of empirical leakage clearance — YES (02_01_01 framed catalog-only/vacuous).
7. `02_01_03+` deferral of history (6) + in_game (11) tranches non-abandoning — YES (sequenced).
8. Status-reopen logic honest — YES (no STEP_STATUS row → 02_01 stays complete;
   re-derivation to in_progress fires only on execution; pre-disclosed CHANGELOG L53 +
   research_log L18; the 01_04 net-zero reopen is the established precedent).
9. Future Layer-2 file scope correct (6-file final diff) — YES (all 6 exist; 3.66.0→3.67.0 minor).
10. Any blocker requiring re-planning before Layer-2 — NO.

### Non-blocking nits (fold into the FUTURE Layer-2 materialization PR; no `current_plan.md` edit now)

1. **Provenance-proxy framing + overstated cross-game prose.** Of the 5 tranche-1
   families, only `matchup` and `map` are genuinely cross-game-shared (Invariant #8);
   `patch_version_encoded` and `is_mmr_missing_flag` are SC2-specific (AoE2 uses
   leaderboard/mode provenance). The stub's `scientific_invariants_applied` #8 field
   already narrows this correctly; only the looser "Materialization scope" prose
   overstates it. The future materialization MD must (a) call `is_mmr_missing` a
   provenance indicator, not a skill feature, and (b) not sell the whole tranche as
   cross-game-shared.
2. **Pre-existing CHANGELOG self-inconsistency in the closed PR #230 block** (CHANGELOG
   L46 "Phase 02 not_started → in_progress" vs L78 "Phase 02 remains not_started";
   PHASE_STATUS authoritatively shows in_progress; the closed §10 / leakage_audit
   artifacts still say "Phase 02 not_started", now stale). The stub correctly does NOT
   touch these closed artifacts. A future Category C/E hygiene unit should reconcile
   them — not this plan's concern.
3. **Registry-path drift** (= reviewer-deep N1, re-confirmed): the closed block outputs
   name `..._registry_sc2egset.csv`; the on-disk file is `..._registry.csv`. The stub
   `inputs` already cite the true name; T01 step 4 forbids propagating the stale path.
   Correctly quarantined; no plan action.

### Mandatory for the FUTURE Layer-2 materialization (not this stub PR)

Before the `02_01_02` materialization PR executes, a Claude Chat second-pass review is
REQUIRED (in addition to the executor's own analysis): the focal/opponent projection
SQL is where the first non-vacuous leakage computation lands, and subtle leakage there
must get a second pass even if the executor's output looks correct.
