---
title: "SC2EGSet Step 02_01_01 — V-9 per-player construction / focal-opponent symmetry validation (spec-D10)"
category: A
branch: phase02/sc2egset-feature-registry-v9-symmetry
date: 2026-05-10
planner_model: claude-opus-4-7
branch_prefix: phase02/
branch_name: phase02/sc2egset-feature-registry-v9-symmetry
pr_title: "feat(phase02): SC2EGSet 02_01_01 V-9 per-player construction / focal-opponent symmetry (spec-D10)"
base_ref: "master @ 664c869a"
base_commit: 664c869a7b3f64fcc58c4859e7c0de638f206cde
target_version: "3.51.0"
version_current: "3.50.0"
version_bump_type: "minor (Category A feat)"
created_date: 2026-05-10
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
step_name: "Feature-family registry skeleton (sc2egset)"
lineage_sequence_step: 6
prior_pr_ref: "#214"
invariants_touched: [I5]
reviewer_gate_plan: reviewer-deep
reviewer_gate_post_execution: reviewer-deep
reviewer_adversarial_required: false
critique_required: true
spec_bindings:
  - CROSS-02-00-v3.0.1
  - CROSS-02-02-v1.0.1
  - CROSS-02-03-v1.0.1
non_batching_lineage_position: "Sequence step 6 continuation — additional validation module under data-analysis-lineage.md §'Non-batching rule for empirical work'. PR #212 delivered scaffold + V-1..V-6; PR #213 added V-1 strict + V-7 (cold-start vocabulary/sentinel); PR #214 added V-8 (source-grain structural well-formedness, explicitly disjoint from spec-D10). This PR adds V-9 — the *actual* spec-D10 (Invariant I5 focal/opponent symmetry) registry-layer validator. Artifact generation (sequence step 7), research_log / STEP_STATUS / manifest (step 8) and final reviewer-deep gate (step 9) remain deferred."
source_artifacts:
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - planning/current_plan.md (PR #214 plan, structural template reuse)
  - planning/current_plan.critique.md (PR #214 reviewer-deep critique)
research_log_ref: "(deferred — research_log entry for Step 02_01_01 lands in the future closure PR per data-analysis-lineage.md §'Non-batching rule' step 8; this PR makes no research_log edits)"
---

# Plan: SC2EGSet Step 02_01_01 — V-9 per-player construction / focal-opponent symmetry (spec-D10)

## Scope

This PR delivers ONE additional validation module (V-9) for the SC2EGSet
Step 02_01_01 feature-family registry skeleton, extending
`validate_registry_skeleton()` from V-1..V-8 (delivered by PR #212,
PR #213, PR #214) to V-1..V-9. V-9 implements the *actual* spec-D10
check from CROSS-02-03-v1.0.1 §4.1: **focal/opponent symmetry**
(Invariant I5) — verified at the registry-skeleton layer through
controlled-vocabulary validation of the `per_player_construction`
column with a status-gated conjunction carve-out (analogous in shape
to V-7's cold-start sentinel pattern but distinct in semantics).

The merged 26-row SKELETON from PR #212 (sandbox notebook + paired
ipynb) remains untouched in row content. Only narrative text in
markdown/comment cells is corrected — specifically the residual
"D8 (per_player_construction symmetry)" misnaming on notebook lines
537–538 inherited from PR #214 (D8 is full-replay aggregate exclusion
in the spec, NOT symmetry; symmetry is D10), and an update to lines
540–541 acknowledging that V-9 has landed. No new artifacts are
produced; no STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS /
research_log / manifest edits are performed. Step 02_01_01 itself is
NOT closed by this PR.

This PR continues lineage sequence step 6 ("Next validation module")
per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for
empirical work". V-9 is the next defensible skeleton-layer validator
after the D-coverage analysis in §Problem Statement below — and is
the user's explicitly preferred direction, validated by live
extraction against the on-disk skeleton.

## Problem Statement

After PR #214 (V-8 source-grain structural well-formedness, explicitly
disjoint from spec-D10), six CROSS-02-03-v1.0.1 §4.1 audit dimensions
remain unaddressed by skeleton-layer validators (D2, D3, D4 in_game
side, D5 in_game side, D6 partial, D8, D10), with D9/D15 staying
post-materialization-only and D12/D14 N/A for sc2egset. The user's
preferred next direction is V-9 covering **spec-D10** —
focal/opponent symmetry / Invariant I5 — against the existing
`per_player_construction` column.

Independent verification by the planner against (a) the locked
CROSS-02-03-v1.0.1 spec text and (b) live extraction of all 26 rows
of the merged SKELETON confirms the user's framing is methodologically
sound and the validator is implementable as a narrow, deterministic,
controlled-vocabulary check with a status-gated carve-out:

**Verification 1 — D10 spec text (verbatim).** CROSS-02-03-v1.0.1
§4.1 row D10 reads: *"Focal/opponent symmetry and p0/p1 projection.
Every per-player feature is computed by the same SQL pattern or
function for the focal player and the opponent (Invariant I5). For
aoestats, the `p0_*` / `p1_*` source asymmetry is resolved via the
`canonical_slot` focal/opponent assignment (CROSS-02-00-v3.0.1 §5.2;
aoestats-only column) before any feature computation that depends on
player role. RISK-24 routes the operationalization to a Phase 02
ROADMAP step."* — confirming D10 has two sub-clauses: (i) **symmetry
of construction across focal/opponent** for every per-player feature
(applies to **all** datasets per Invariant I5); and (ii) **p0/p1 →
focal/opponent projection via `canonical_slot`** (explicitly
**aoestats-only** per CROSS-02-00-v3.0.1 §5.2 row, where
`canonical_slot` is documented as "aoestats-ONLY" and "NOT in MHM
UNION ALL"). For SC2EGSet, sub-clause (ii) is **N/A**: sc2egset has
no p0/p1 source asymmetry — its per-player slot semantics derive
from `replay_players_raw` and tracker `playerId` /
`controlPlayerId` / `killerPlayerId` / `owner_via_unitborn_lineage`,
which are already per-player-keyed. V-9 binds sub-clause (i) only;
sub-clause (ii) is recorded as N/A for sc2egset and explicitly
deferred to an aoestats-side V-N PR (out of scope here).

**Verification 2 — `per_player_construction` column existence.** Live
read of `_COLS` in
`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
line 282 and `REQUIRED_COLUMNS` in
`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
line 82 confirms `per_player_construction` is the 13th column of the
13-column audit-object schema. The column exists; V-9 has a
non-vacuous target.

**Verification 3 — column value partition (live, all 26 rows).**
Inline extraction of `per_player_construction` across the entire
merged SKELETON yields **exactly two distinct values**:

| Value | Count | Source rows |
|-------|-------|-------------|
| `symmetric` | 23 | 5 pre_game + 6 history_enriched_pre_game + 4 in_game_now + 7 in_game_caveat + 1 sanity_gate (`slot_identity_consistency`) |
| `blocked` | 3 | the three blocked_or_deferred carve-out rows (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`) |

There are **zero** `asymmetric` rows, **zero** `match_level` rows,
**zero** `per_player_role` rows, and **zero**
`sanity_gate_not_model_input` values on the `per_player_construction`
column. The sanity-gate row (`slot_identity_consistency`) carries
`per_player_construction = "symmetric"` (not a sentinel) — its
sanity-gate semantics live on the `status` column, not on
`per_player_construction`. The `"blocked"` value on the 3 carve-out
rows mirrors the V-7 cold-start sentinel pattern: blocked rows carry
`"blocked"` literally on `per_player_construction`,
`cold_start_handling`, `model_input_grain`, `target_grain`,
`allowed_cutoff_rule`, and `candidate_leakage_modes` — six columns
get the sentinel under the conjunction
`prediction_setting == "blocked_or_deferred"` AND
`status == "blocked_until_additional_validation"`.

**Verification 4 — Invariant I5 holds on all model-input rows (live).**
Every row whose `prediction_setting in {pre_game,
history_enriched_pre_game, in_game_snapshot}` carries
`per_player_construction == "symmetric"` (23 of 23 model-input rows;
this includes the sanity_gate row which is in_game_snapshot but is
not a model input via its `status`). Invariant I5 is upheld at the
registry-skeleton layer. V-9 enforces this structurally.

**V-9 design — controlled vocabulary + conjunction carve-out
(symmetric to V-7).** V-9 asserts:

1. `per_player_construction` is a non-empty string on every row.
2. For rows where the conjunction
   (`prediction_setting == "blocked_or_deferred"` AND
   `status == "blocked_until_additional_validation"`) holds:
   `per_player_construction == "blocked"` (the carve-out sentinel).
3. For all other rows (every model-input row plus the sanity_gate
   row): `per_player_construction == "symmetric"`. This is the
   I5 binding: at the registry-skeleton layer, V-9 admits
   `"symmetric"` as the only legal value for non-blocked rows.
   `"asymmetric"` is rejected categorically — Invariant I5 forbids
   asymmetric per-player feature construction. `"match_level"`,
   `"per_player_role"`, and other speculative tokens are also
   rejected — they do not appear in the merged skeleton and would
   require a separate spec amendment to admit.

**Why "symmetric"-only and not a broader vocabulary?** A broader
vocabulary (e.g., admitting `"match_level"` for map/patch rows that
are technically not per-player) would mis-frame the methodological
question. Match-level features (map, patch) are not "asymmetrically"
constructed; they are *identical* for both players in a match — which
is a degenerate case of symmetric construction (the focal-side and
opponent-side computations both produce the same constant value).
The on-disk skeleton already encodes this correctly: all 5 pre_game
match-level rows carry `"symmetric"`, not a separate `"match_level"`
token. V-9 ratifies that encoding choice.

**Out-of-scope clarifications.** V-9 does NOT verify:
- whether the `per_player_construction == "symmetric"` declaration is
  *operationally* upheld in any future feature-generation SQL — that
  is post-materialization (CROSS-02-01-v1.0.1's leakage audit) and
  cannot be checked at the registry-skeleton layer;
- the aoestats `canonical_slot` p0/p1 projection sub-clause — N/A
  for sc2egset; deferred to a future aoestats-side V-N PR;
- per-row "is `symmetric` the *optimal* construction for this
  family" — that is a methodology/family-design question, not a
  controlled-vocabulary structural one.

**Notebook narrative defects to clean up under V-9.** PR #214's "no
notebook row content change" boundary correctly preserved the 26-row
literals, but two text-only locations now contain residual factual
inaccuracies that V-9 must correct (in addition to landing the
validator):

- **Notebook lines 537–538** (Follow-ups list) call **D8**
  "per_player_construction symmetry". D8 in the locked spec is
  *"Full-replay aggregate exclusion for in-game snapshots"*. D10 is
  the symmetry dimension. This is a leftover paraphrase error that
  V-9 must fix.
- **Notebook lines 540–541** ("spec-D10 is symmetry, deferred to a
  future V-9") will be stale once V-9 lands; it must be updated to
  acknowledge that V-9 of this PR covers spec-D10's first sub-clause
  (symmetry) and to record that the second sub-clause (p0/p1
  projection via `canonical_slot`) remains aoestats-only and
  out-of-scope for sc2egset.

## Assumptions & Unknowns

**Assumptions** (declared explicit so the executor can halt if any
becomes false during T01–T09):

1. The merged 26-row SKELETON in
   `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
   already satisfies V-9 by construction: 23 of 26 rows carry
   `per_player_construction == "symmetric"`, the 3 carve-out rows
   carry `"blocked"`, and no row carries `"asymmetric"` or any other
   value. Verified live by the planner against master `664c869a`
   (PR #214 merge commit). V-9's controlled-vocabulary check
   (`{"symmetric", "blocked"}` partitioned by the V-7 conjunction)
   passes on all 26 rows with 0 violations.
2. The narrative target lines (537–538, 540–541) are stable across
   master `664c869a` and the new branch's HEAD. Verified by the
   planner.
3. `pyproject.toml` line 3 reads `version = "3.50.0"` at branch HEAD;
   T08 mechanically bumps to `"3.51.0"`. (Implicit verification: PR
   #214 release-bumped to 3.50.0; CHANGELOG `[Unreleased]` was rolled
   in T08 of PR #214 and is now empty.)
4. CHANGELOG.md `[Unreleased]` block is empty after PR #214's roll-up
   (verified by inspection of that PR's T08 commit).
5. The fixture in
   `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
   currently hard-codes `"per_player_construction": "symmetric"` for
   all 7 fixture rows (line 65), including the three blocked rows
   that on the on-disk skeleton carry `"blocked"`. **As-is, V-9
   would FAIL on the existing fixture's three blocked rows** because
   the carve-out conjunction (`prediction_setting ==
   "blocked_or_deferred"` AND `status ==
   "blocked_until_additional_validation"`) holds on those rows, so
   V-9 demands `"blocked"` — but the fixture provides `"symmetric"`.
   T02b Step 0 lifts the three fixture blocked rows to
   `per_player_construction="blocked"`, restoring fixture/skeleton
   parity and unblocking V-9 happy-path tests. This is mandatory and
   directly analogous to PR #214 T02b Step 0 fixture lift.
6. `_row()` test helper currently does NOT accept a
   `per_player_construction` kwarg. It hard-codes the value at line
   65. T02 parameterizes the helper to accept the kwarg with
   `"symmetric"` as the default — preserving every existing test's
   behavior since the default matches the previously hard-coded value.
7. The conjunction carve-out predicate in V-9 is *literally identical*
   to V-7's: `is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and st
   == BLOCKED_STATUS)`. This is intentional and the validator can
   reuse the existing module-level constants
   `BLOCKED_PREDICTION_SETTING`, `BLOCKED_STATUS`, and
   `BLOCKED_SENTINEL` without redefinition. V-9 introduces no new
   conjunction-predicate logic; it only introduces a new
   controlled-vocabulary set
   (`PER_PLAYER_CONSTRUCTION_VOCAB = frozenset({"symmetric"})`).

**Unknowns** (must NOT block T01; surfaced for executor awareness):

1. Whether reviewer-deep at T09 (post-execution gate) raises any
   methodology BLOCKER beyond the issues already addressed in this
   plan. If so, T09 routes to reviewer-adversarial per
   `.claude/rules/data-analysis-lineage.md` line 24 carve-out.
2. Whether the planner's chosen "symmetric-only" vocabulary (vs.
   admitting `"match_level"` as a separate token for map/patch rows)
   draws methodological pushback from reviewer-deep. If so, the
   resolution is that the on-disk skeleton already encodes
   match-level rows as `"symmetric"` (their per-player computation
   produces the same constant for both slots, which IS symmetric
   construction); admitting `"match_level"` as a separate token would
   require a skeleton patch first — which is out of scope here per
   §Out of scope.

## Literature Context

- **CROSS-02-03-v1.0.1 §4.1 D10**
  (`reports/specs/02_03_temporal_feature_audit_protocol.md` line
  161): *"Focal/opponent symmetry and p0/p1 projection. Every
  per-player feature is computed by the same SQL pattern or function
  for the focal player and the opponent (Invariant I5). For aoestats,
  the `p0_*` / `p1_*` source asymmetry is resolved via the
  `canonical_slot` focal/opponent assignment (CROSS-02-00-v3.0.1
  §5.2; aoestats-only column) before any feature computation that
  depends on player role. RISK-24 routes the operationalization to a
  Phase 02 ROADMAP step."* — D10 has two sub-clauses; V-9 binds
  sub-clause 1 (symmetry) for sc2egset and records sub-clause 2
  (p0/p1 projection) as N/A for sc2egset.
- **CROSS-02-00-v3.0.1 §5.2**
  (`reports/specs/02_00_feature_input_contract.md` line 380):
  `canonical_slot VARCHAR PRE_GAME` — *"aoestats-ONLY; slot_A/slot_B;
  hash-on-match_id; skill-orthogonal; NOT in MHM UNION ALL"*. The
  aoestats-only nature of `canonical_slot` is the spec-bound reason
  V-9 records sub-clause 2 of D10 as N/A for sc2egset.
- **CROSS-02-02-v1.0.1 §4.2 / §5**
  (`reports/specs/02_02_feature_engineering_plan.md` lines 162–177
  and 189–193):
  - §4.2 distinguishes *"`match_pair / player_match focal row`"*
    from *"`match row with p0/p1 source columns`"* and binds
    *"symmetric focal/opponent projection is a binding pre-modeling
    step (Invariant I5 symmetry). The unprojected p0/p1 row grain is
    a transport grain, not a modeling grain"*.
  - §5.1 commits *"Focal/opponent symmetry (Invariant I5). Every
    per-player feature must be computed with the same function or
    SQL pattern for the focal player and the opponent."*
  V-9 ratifies this commitment at the registry-skeleton layer for
  sc2egset by admitting only `"symmetric"` (or the carve-out
  `"blocked"`) on `per_player_construction`.
- **CROSS-02-02-v1.0.1 §6.2**
  (`reports/specs/02_02_feature_engineering_plan.md` line 239 etc.):
  per-family commitments mark `opponent_player_history` as *"symmetric
  mirror of `focal_player_history` ... Symmetric (Invariant I5): same
  SQL pattern as focal."* — confirming that for sc2egset
  `history_enriched_pre_game` rows, the `per_player_construction =
  "symmetric"` declaration is consistent with the upstream binding
  feature-engineering plan.
- **CROSS-02-01-v1.0.1 §G-L-8**
  (`reports/specs/02_01_leakage_audit_protocol.md`, referenced via
  `reports/specs/02_02_feature_engineering_plan.md` line 459):
  *"No row-order leakage from p0/p1 or focal/opponent slot
  asymmetry"* — the post-materialization gate. CROSS-02-01-v1.0.1
  audits whether the SQL implementation actually upholds
  symmetric construction; V-9 audits only the **declaration** at
  the registry-skeleton layer. The two gates are complementary, not
  redundant (CROSS-02-03-v1 §1.3 non-supersession clause).
- **`.claude/scientific-invariants.md` Invariant I5 (line 158):**
  *"Both players in every game must be treated identically by the
  feature pipeline. The same function that computes features for the
  focal player also computes features for the opponent. No player
  slot receives privileged treatment. The model input is always
  structured as `(focal_player_features, opponent_features,
  context_features)` and this structure is identical regardless of
  which player is focal."* — the Invariant V-9 binds.
- **PR #212** (merged 2026-05-08 at master `18d30a81`): scaffold +
  V-1..V-6.
- **PR #213** (merged 2026-05-08 at master `7b26b40f`): V-1 strict +
  V-7 (cold-start vocabulary/sentinel — established the
  conjunction-carve-out pattern V-9 reuses).
- **PR #214** (merged 2026-05-09 at master `664c869a`): V-8
  (source-grain structural well-formedness; explicitly disjoint from
  spec-D10). Reviewer-deep on PR #214 returned PASS-WITH-FIXES F1–F4
  all applied; carry-forward follow-ups (3 hygiene items) deferred
  to a separate hygiene PR per §Out of scope below.
- **`.claude/rules/data-analysis-lineage.md`** §"Non-batching rule"
  (line 24 Phase 02 carve-out): defines the 9-step empirical
  sequence and authorizes reviewer-deep (not reviewer-adversarial)
  as the plan-phase gate during the active Phase 02 readiness
  iterative-validator-PR sequence. V-9 inherits this routing per
  PR #212 / PR #213 / PR #214.
- **D-coverage matrix after V-9 (corrected from PR #214 §Per-question
  finding 9):**

| Dim | Title | Status after V-9 |
|---|---|---|
| D1 | Prediction setting admissibility | covered (V-1 controlled vocab) |
| D2 | Source classification + temporal availability | NOT covered (deferred) |
| D3 | Source grain vs model grain | NOT covered (deferred) |
| D4 | Temporal anchor correctness | history side covered (V-6); in_game side NOT covered |
| D5 | Cutoff operator correctness | history side covered (V-6); in_game side NOT covered |
| D6 | Target-game exclusion | partially covered (V-6 strict-`<` + post-outcome tokens); in_game / full-replay side deferred |
| D7 | Post-game token exclusion | covered (V-6 token list) |
| D8 | Full-replay aggregate exclusion (in-game) | NOT covered (deferred) |
| D9 | Normalization fit-scope | post-materialization, out of registry layer |
| **D10** | **Focal/opponent symmetry (sub-clause 1)** | **covered (V-9, this PR)** for sc2egset; aoestats p0/p1 sub-clause 2 deferred to aoestats-side V-N |
| D11 | Cold-start vocabulary, no magic numbers | covered (V-7) |
| D12 | Source-mode label discipline | N/A for sc2egset (no source-mode column) |
| D13 | SC2 tracker eligibility | covered (V-2/V-3/V-4/V-5) |
| D14 | AoE2 source-label discipline | N/A for sc2egset |
| D15 | Artifact-lineage readiness | methodological discipline, not row-level; deferred |

After V-9, **five** dimensions remain unaddressed at the
registry-skeleton layer for sc2egset (D2, D3, D4-in_game, D5-in_game,
D8) plus D6 partial. D9 and D15 are post-materialization /
methodology-level. D12, D14 are N/A. **Therefore Step 02_01_01
closure is NOT defensible after this PR** — at least one further
validator PR (covering D8 and/or the in_game-side of D4/D5) must
land before closure is in scope.

## Gate Condition

This PR is mergeable to master when all of the following are
simultaneously true (mirrored in §Acceptance criteria):

1. `git diff master..HEAD --name-only` lists EXACTLY 9 files: the 4
   scaffold/code files (validation module + tests + notebook .py +
   .ipynb) plus `pyproject.toml` + `CHANGELOG.md` plus the planning
   files (`planning/current_plan.md`,
   `planning/current_plan.critique.md`, `planning/INDEX.md`). No
   forbidden file appears.
2. The notebook's `validate_registry_skeleton()` call output cell
   contains the literal string `"validate_registry_skeleton: ALL
   PASS (V-1 through V-9)"`.
3. `pytest tests/ -v --cov` passes with overall coverage ≥ 95% and
   `validate_registry_skeleton.py` per-file coverage ≥ 95%; the new
   helper (`_check_v9_per_player_construction_vocabulary`) shows
   100% line coverage on its added lines.
4. `ruff check`, `mypy`, `jupytext --check` all clean.
5. The 26 SKELETON rows in the notebook .py are byte-identical to
   master `664c869a` (no row literal modified).
6. Reviewer-deep at T09 returns `PASS` or `PASS-WITH-NOTES`. A
   `BLOCKER` methodology verdict halts T09 and routes to
   reviewer-adversarial per `.claude/rules/data-analysis-lineage.md`
   line 24 carve-out.
7. `pyproject.toml` shows `version = "3.51.0"`; `CHANGELOG.md` has a
   `[3.51.0]` block dated 2026-05-10 with the actual PR number `N`
   substituted (no `PR #TBD` remaining).

## File Manifest

### Allowed (this PR may touch only these)

| File | Action | Touch type | Commit |
|------|--------|-----------|--------|
| `planning/current_plan.md` | Rewrite | rewrite (this plan, authored before T01 fires) | docs(planning) — already on branch when execution starts |
| `planning/current_plan.critique.md` | Rewrite | rewrite (reviewer-deep critique authored before execution) | docs(planning) |
| `planning/INDEX.md` | Update | append archive row for PR #214 + update active row to this branch — bulk update lands BEFORE T01 fires; T09 only appends `(PR #N)` to the active-plan row | docs(planning) |
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` | Update | append `PER_PLAYER_CONSTRUCTION_VOCAB` constant (frozenset containing only `"symmetric"`); add `_check_v9_per_player_construction_vocabulary` private helper (reuses existing `BLOCKED_PREDICTION_SETTING` / `BLOCKED_STATUS` / `BLOCKED_SENTINEL` constants); wire call into `validate_registry_skeleton()` after `_check_v8_source_grain_well_formedness`; update module-level docstring to document V-9 | feat (T07 scaffold/code commit) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` | Update | (a) parameterize `_row()` to accept `per_player_construction` kwarg defaulted to `"symmetric"`; (b) **fixture lift Step 0**: pass `per_player_construction="blocked"` explicitly on the three blocked-row fixture entries to restore fixture/skeleton parity; (c) append new tests for V-9 happy path / asymmetric-rejected-on-model-input / unknown-token-rejected / sentinel-required-on-blocked-rows / sentinel-rejected-outside-conjunction / non-string-rejected / status-mismatch-rejects-sentinel | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` | Update | edit markdown / comment text at lines 537–541 (Follow-ups list correction: D8 misnaming; V-9 acknowledgement; aoestats `canonical_slot` deferral); update print-banner line 507 (V-8 → V-9); add a sentence to the V-9 row in the "Checks IN scope" table at lines 493–500 (commentary only — no SKELETON_* literal change) | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` | Update | regenerated by `jupytext --sync` after .py edit; commit alongside paired .py | feat (T07 commit) |
| `pyproject.toml` | Update | bump `version = "3.50.0"` → `version = "3.51.0"` | chore(release) (T08 commit) |
| `CHANGELOG.md` | Update | roll `[Unreleased]` → `[3.51.0] — 2026-05-10 (PR #N: phase02/sc2egset-feature-registry-v9-symmetry)`; insert empty `[Unreleased]` block; populate `[3.51.0]` Added section with V-9 bullet | chore(release) (T08 commit); PR-number substitution post-create |
| `.github/tmp/commit.txt` | Create | scratch (created and removed within session; not committed) | not committed |
| `.github/tmp/pr.txt` | Create | scratch (created, used by `gh pr create --body-file`, removed after PR is created; not committed) | not committed |

### Forbidden (executor must HALT if `git status` lists any of these)

| Forbidden path | Reason |
|----------------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/**` | No artifacts in this PR (lineage step 7 deferred). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Step 02_01_01 not closed by this PR (D2/D3/D4-in_game/D5-in_game/D6-full/D8 still uncovered). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Pipeline-section roll-up deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Phase 02 status roll-up deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Per-dataset research log entry deferred. |
| `reports/research_log.md` | Cross-game research log entry deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | ROADMAP update deferred. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` | Per-dataset invariants file — must NOT be modified by this PR. |
| `reports/specs/02_00_feature_input_contract.md` | Locked spec — read-only. |
| `reports/specs/02_01_leakage_audit_protocol.md` | Locked spec — read-only. |
| `reports/specs/02_02_feature_engineering_plan.md` | Locked spec — read-only. |
| `reports/specs/02_03_temporal_feature_audit_protocol.md` | Locked spec — read-only. |
| `thesis/**` | No thesis prose in this PR. |
| `thesis/pass2_evidence/notebook_regeneration_manifest.md` | Manifest update deferred to closure PR. |
| `src/rts_predict/games/aoe2/**` | No AoE2 work; aoestats `canonical_slot` D10 sub-clause 2 routed to a future aoestats-side V-N PR. |
| `data/**`, `**/data/**` | No raw / staging / db edits. |
| `docs/**` | No taxonomy / spec / methodology edits. |
| `.claude/**` | No agent / rule / invariant edits. |
| Any literal SKELETON_PRE_GAME / SKELETON_HISTORY / SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT / SKELETON_GATE_AND_BLOCKED row tuple in the notebook .py | Skeleton row content is locked from PR #212. |
| `tracker_events_feature_eligibility.csv` | Upstream evidence — must NOT be modified. |
| `pyproject.toml`, `CHANGELOG.md` **during T01–T07** | These are §Allowed only at T08 (release commit). Executor must HALT if either appears in `git status` while T01–T07 are running. |
| `planning/current_plan.md`, `planning/current_plan.critique.md` **during T07–T08** | These already exist on the branch from earlier docs(planning) commits and must NOT appear in the T07 (scaffold) or T08 (release) staged sets. |
| `validate_registry_skeleton.py` lines outside the V-9 additions | T01 must add only the new constant, the new helper, and the single new call site. Existing V-1..V-8 helpers and orchestrator order MUST NOT be modified. |

## Verification before finalizing this plan (executed read-only by the planner)

1. **D-coverage matrix re-check.** Re-read CROSS-02-03-v1.0.1 §4.1
   D1–D15 verbatim. Confirmed: D10 = "Focal/opponent symmetry and
   p0/p1 projection (Invariant I5)". D8 = "Full-replay aggregate
   exclusion for in-game snapshots". The notebook's Follow-ups
   list at lines 537–538 calls D8 "per_player_construction
   symmetry" — that is a leftover narrative inaccuracy from PR #214
   (D8 ≠ symmetry; D10 is symmetry). T03 corrects the misnaming.

2. **`per_player_construction` column existence (live).** Confirmed
   the column is `_COLS[12]` in the notebook (line 282) and
   `REQUIRED_COLUMNS[12]` in
   `validate_registry_skeleton.py` (line 82). The 13-column schema
   binds it; V-1 already enforces presence/absence; V-9 enforces
   value vocabulary.

3. **Column value partition (live, all 26 rows).** Inline-extracted:
   23 × `"symmetric"`, 3 × `"blocked"`, 0 × `"asymmetric"`, 0 ×
   anything else. The 23 `"symmetric"` rows decompose as 5 pre_game
   + 6 history + 4 in_game_now + 7 in_game_caveat + 1 sanity_gate
   (`slot_identity_consistency`). The 3 `"blocked"` rows are the
   carve-out trio (`mind_control_event_count`,
   `army_centroid_at_cutoff_snapshot`,
   `playerstats_cumulative_economy_fields`), each satisfying the
   V-7 conjunction predicate. The sanity-gate row carries
   `"symmetric"` (NOT a sentinel) — its sanity-gate semantics live
   on `status`, not on `per_player_construction`. **0 violations
   under V-9 as designed.**

4. **Invariant I5 binding (live).** All 23 model-input-or-sanity-gate
   rows carry `"symmetric"`. No row carries `"asymmetric"`. Invariant
   I5 (line 158 of scientific-invariants.md: *"Both players in every
   game must be treated identically by the feature pipeline. The
   same function that computes features for the focal player also
   computes features for the opponent."*) is upheld at the
   registry-skeleton layer.

5. **aoestats p0/p1 N/A determination (spec-bound).** CROSS-02-00-v3.0.1
   §5.2 documents `canonical_slot` as "aoestats-ONLY", "NOT in MHM
   UNION ALL". sc2egset has no `canonical_slot` column on
   `matches_history_minimal` (CROSS-02-00-v3.0.1 §5.1: 9 columns,
   no `canonical_slot`). sc2egset's per-player slot semantics are
   already established via `replay_players_raw` (per-player rows)
   and tracker `playerId` / `controlPlayerId` /
   `killerPlayerId` / `owner_via_unitborn_lineage` (per-player or
   per-player-via-lineage). Sub-clause 2 of D10 is therefore N/A
   for sc2egset; V-9 records this as N/A explicitly and does not
   attempt to validate it.

6. **Test fixture state (live).** Test file line 65: every fixture
   row hard-codes `"per_player_construction": "symmetric"`,
   including the three `blocked_or_deferred` rows at fixture
   indices 4, 5, 6. As-is V-9 would fire on these three rows
   (conjunction holds, value is `"symmetric"`, expected `"blocked"`).
   **T02b Step 0 fixture lift is mandatory** to pass
   `per_player_construction="blocked"` on those three rows. Other
   fixture rows inherit `"symmetric"` from the new kwarg default
   without modification.

7. **`_row()` helper signature (live).** Test file lines 40–66:
   `_row()` accepts kwargs for `feature_family_id`,
   `prediction_setting`, `status`, `source_table_or_event_family`,
   `temporal_anchor`, `allowed_cutoff_rule`, `cold_start_handling`,
   `source_grain` (added in PR #214). It does NOT yet accept
   `per_player_construction`. T02 adds it as a new kwarg with
   `"symmetric"` default. This is mechanically identical in shape
   to PR #214's T02 (which added `source_grain`).

8. **V-9 helper signature (planned).** The new helper
   `_check_v9_per_player_construction_vocabulary(skeleton)` takes
   the same `list[dict[str, Any]]` parameter as
   `_check_v7_cold_start_vocabulary` and `_check_v8_*`. It does
   not need the tracker CSV. It reuses the module-level constants
   `BLOCKED_PREDICTION_SETTING`, `BLOCKED_STATUS`,
   `BLOCKED_SENTINEL`, plus the new
   `PER_PLAYER_CONSTRUCTION_VOCAB`. **The conjunction predicate is
   literally the same line of code as in V-7** — V-9 reuses, does
   not redefine.

9. **Notebook narrative target locations (live).** Confirmed via
   read at master `664c869a`:
   - **Line 507** print-banner: `print("validate_registry_skeleton:
     ALL PASS (V-1 through V-8)")` → must update to `(V-1 through V-9)`.
   - **Lines 493–500** (markdown cell, "Checks IN scope" table /
     "Checks NOT YET in scope" prose): the table at lines 484–491
     enumerates V-1 through V-6; line 493 says *"Checks IN scope as
     of this PR (V-1 base, V-1 strict, V-2..V-7 from PRs
     #212/#213, V-8 source-grain structural well-formedness +
     provenance-key consistency from this PR)."* — needs update
     to add V-9. Line 500 says *"audit dimensions
     D2/D3/D6/D8/D9/D10/D12/D15."* — needs to drop D10 (V-9 covers
     it) leaving `D2/D3/D6/D8/D9/D12/D15` (D12/D15 retained because
     D12 is partial-N/A annotation and D15 is methodology).
   - **Lines 537–541** (markdown cell, Follow-ups list): contains
     the `D8 (per_player_construction symmetry)` misnaming and the
     stale `D10 ... deferred to a future V-9` line. Must be
     rewritten to (a) drop the D8 misnaming (D8 is full-replay
     exclusion, not symmetry); (b) acknowledge V-9 covers D10
     sub-clause 1 (symmetry) for sc2egset; (c) record D10 sub-clause
     2 (aoestats `canonical_slot` p0/p1 projection) as aoestats-only
     and out-of-scope for sc2egset.

10. **Three carry-forward follow-ups from PR #213/#214 reviews
    (deferred to a separate hygiene PR — out of scope here).**
    - Defensive-branch coverage on
      `validate_registry_skeleton.py` lines 347 / 415 / 421
      (current line numbers; these were 294 / 362 / 368 in PR #213
      pre-V-7-and-V-8 numbering).
    - Test-infra `parents[6]` magic at
      `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
      line 25.
    - V-8 helper bare-`(filename)` permissiveness on tracker rows
      (currently a no-op since no tracker row uses the bare form;
      tightening would require adding a "tracker rows must carry at
      least one attribution key" rule).

    None of these affects V-9. All three are explicitly out of
    scope for this PR per §Out of scope.

## Execution Steps

Each task lists: ID, allowed files, forbidden files, exact operation,
task-specific stop condition, validation report shape, executor model
assignment.

### T01 — Add V-9 per-player-construction controlled-vocabulary check

**Objective:** Append one new module-level constant
(`PER_PLAYER_CONSTRUCTION_VOCAB`) and the private helper
`_check_v9_per_player_construction_vocabulary` to
`validate_registry_skeleton.py`; wire the call into the public
`validate_registry_skeleton()` orchestrator after the existing
`_check_v8_source_grain_well_formedness` call. Update the module
docstring to reflect the ten-check scope (V-1 base, V-1 strict,
V-2..V-9). The helper reuses the existing
`BLOCKED_PREDICTION_SETTING`, `BLOCKED_STATUS`, and `BLOCKED_SENTINEL`
constants — no new conjunction-predicate logic is introduced.

**Instructions:**
1. Append the new constant after the existing
   `NON_TRACKER_GRAIN_KEYS` / `TRACKER_SOURCE_TABLE_PREFIX` block
   (approximately line 192) and before
   `POST_OUTCOME_FORBIDDEN_TOKENS`:

   ```python
   # CROSS-02-03-v1.0.1 §4.1 D10 (sub-clause 1) controlled vocabulary
   # for the per_player_construction column. V-9 binds Invariant I5
   # (focal/opponent symmetry) at the registry-skeleton layer for
   # sc2egset: every model-input-or-sanity-gate row must carry
   # "symmetric"; only carve-out rows (the V-7 conjunction
   # prediction_setting == "blocked_or_deferred" AND status ==
   # "blocked_until_additional_validation") may carry the literal
   # sentinel "blocked" (BLOCKED_SENTINEL).
   #
   # D10 sub-clause 2 (aoestats p0/p1 projection via canonical_slot,
   # CROSS-02-00-v3.0.1 §5.2) is N/A for sc2egset — sc2egset has no
   # canonical_slot column; per-player slot semantics are already
   # established via replay_players_raw and tracker player-id columns.
   # Sub-clause 2 is deferred to a future aoestats-side V-N PR.
   PER_PLAYER_CONSTRUCTION_VOCAB: frozenset[str] = frozenset(
       {"symmetric"}
   )
   ```

2. Add the private helper after `_check_v8_source_grain_well_formedness`:

   ```python
   def _check_v9_per_player_construction_vocabulary(
       skeleton: list[dict[str, Any]],
   ) -> None:
       """V-9: per_player_construction controlled vocabulary + sentinel under conjunction.

       For each row:
           - If prediction_setting == "blocked_or_deferred" AND
             status == "blocked_until_additional_validation":
                 assert per_player_construction == BLOCKED_SENTINEL.
           - Else (every other row, including all model-input
             pre_game / history_enriched_pre_game / in_game_snapshot
             rows AND the sanity_gate row):
                 assert per_player_construction in PER_PLAYER_CONSTRUCTION_VOCAB
                 (i.e., "symmetric").

       For ALL rows: assert per_player_construction is a non-empty
       string.

       V-9 binds CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1 (Invariant
       I5: focal/opponent symmetry) for sc2egset. D10 sub-clause 2
       (aoestats p0/p1 projection via canonical_slot) is N/A for
       sc2egset and is deferred to a future aoestats-side V-N PR.

       The conjunction predicate is identical in shape to V-7's
       cold-start sentinel pattern; the helper deliberately reuses
       the BLOCKED_PREDICTION_SETTING / BLOCKED_STATUS / BLOCKED_SENTINEL
       constants without redefinition.
       """
       for row in skeleton:
           ppc = row["per_player_construction"]
           ps = row["prediction_setting"]
           st = row["status"]
           ffid = row["feature_family_id"]

           # Type guard: per_player_construction must be a non-empty string.
           assert isinstance(ppc, str), (
               f"V-9: row '{ffid}' per_player_construction is not a string "
               f"(got {type(ppc).__name__!r}); expected str"
           )
           assert ppc, (
               f"V-9: row '{ffid}' per_player_construction is empty"
           )

           # Conjunction predicate (identical to V-7).
           is_carve_out = (
               ps == BLOCKED_PREDICTION_SETTING and st == BLOCKED_STATUS
           )

           if is_carve_out:
               assert ppc == BLOCKED_SENTINEL, (
                   f"V-9: carve-out row '{ffid}' (prediction_setting='{ps}', "
                   f"status='{st}') has per_player_construction='{ppc}'; "
                   f"expected literal '{BLOCKED_SENTINEL}'"
               )
           else:
               assert ppc in PER_PLAYER_CONSTRUCTION_VOCAB, (
                   f"V-9: row '{ffid}' (prediction_setting='{ps}', "
                   f"status='{st}') has per_player_construction='{ppc}'; "
                   f"expected one of {sorted(PER_PLAYER_CONSTRUCTION_VOCAB)} "
                   f"(Invariant I5 / CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1)"
               )
   ```

3. Add a call to
   `_check_v9_per_player_construction_vocabulary(skeleton)` inside
   `validate_registry_skeleton()`, on the line immediately following
   the existing `_check_v8_source_grain_well_formedness(skeleton)`
   call. Order of public checks after this PR will be: V-1 base,
   V-1 strict, V-2, V-3, V-4, V-5, V-6, V-7, V-8, V-9.

4. Update the module docstring "Scope (nine assertions across V-1..V-8
   implemented here):" line to "Scope (ten assertions across V-1..V-9
   implemented here):" and append a `V-9` paragraph:

   ```
       V-9 ``per_player_construction`` controlled vocabulary +
       sentinel under conjunction carve-out:
           model-input and sanity-gate rows must carry the literal
           ``"symmetric"`` (Invariant I5 binding —
           CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1: focal/opponent
           symmetry); rows where ``prediction_setting ==
           "blocked_or_deferred"`` AND ``status ==
           "blocked_until_additional_validation"`` must carry the
           literal sentinel ``"blocked"``. ``"asymmetric"`` is
           categorically rejected. D10 sub-clause 2 (aoestats p0/p1
           projection via ``canonical_slot``) is N/A for sc2egset.
   ```

   Append matching docstring update to the public
   `validate_registry_skeleton` function: change "Run V-1..V-8
   structural assertions" to "Run V-1..V-9 structural assertions",
   and append a `V-9 per_player_construction controlled vocabulary.`
   line in the "Check order:" enumeration.

5. Update the `Deferred to subsequent validation modules (NOT covered
   here):` block in the module docstring to remove the line *"Per-player
   construction symmetry (Invariant I5)."* — V-9 now covers this.

**Verification:**
- `git diff --stat src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
  shows ONLY additions: the new constant, the new helper, the new
  call site, and the docstring amendments.
- `validate_registry_skeleton(SKELETON, TRACKER_CSV)` on the merged
  26-row skeleton (loaded via the notebook) raises no
  `AssertionError` (deferred to T06; not run in T01 itself).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`

**Read scope:**
- `reports/specs/02_03_temporal_feature_audit_protocol.md` (D10
  sub-clause 1 verbatim)
- `reports/specs/02_00_feature_input_contract.md` §5.1 / §5.2
  (canonical_slot aoestats-only)
- `.claude/scientific-invariants.md` Invariant I5

**Task-specific stop condition:** halt if (a) any of the existing
V-1 base / V-1 strict / V-2..V-8 helpers must be modified to land
V-9 (none should), (b)
`_check_v9_per_player_construction_vocabulary` causes a public-API-shape
change to `validate_registry_skeleton()` (it must not — same
`(skeleton, tracker_csv_path)` signature), (c) any redefinition of
`BLOCKED_PREDICTION_SETTING` / `BLOCKED_STATUS` / `BLOCKED_SENTINEL`
appears in the diff (V-9 must reuse, not redefine).

**Validation report shape:** post-edit show diff of
`validate_registry_skeleton.py`; confirm exactly the additions
specified; confirm `_check_v8_source_grain_well_formedness` and
`_check_v7_cold_start_vocabulary` are unchanged in signature/body;
confirm the orchestrator's check order is now V-1 → V-1 strict →
V-2 → V-3 → V-4 → V-5 → V-6 → V-7 → V-8 → V-9.

**Executor model:** Sonnet (mechanical specification; no methodology
inference required beyond the literal vocabulary set and reuse of
the existing carve-out predicate).

---

### T02 — Parameterize `_row()` test helper to accept `per_player_construction`

**Objective:** Update the existing `_row()` helper in the test file
to accept an optional `per_player_construction: str = "symmetric"`
keyword argument. This minimal parameterization unblocks T02b's
fixture lift on the three blocked rows AND V-9-targeted perturbation
tests, without changing the behavior of any pre-existing test (the
default value preserves the current hard-coded value at line 65).
NO existing fixture row is changed in this task.

**Instructions:**
1. Edit
   `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`.
2. At the `_row()` helper (lines 40–66), add `per_player_construction:
   str = "symmetric"` as a keyword-only parameter in the signature,
   AFTER the existing `source_grain` parameter.
3. In the dict literal at line 65, change the hard-coded
   `"per_player_construction": "symmetric",` line to
   `"per_player_construction": per_player_construction,`.
4. Do NOT change any existing fixture row in T02. Do NOT change any
   existing test in T02. The pre-existing tests (post-PR-#214 count;
   ≈ 56 tests including the V-8 block) must continue to pass
   unchanged because the default value matches the hard-coded value
   they previously inherited. Fixture lift on the three blocked rows
   happens in T02b Step 0 below, not here.

**Verification:**
- `git diff tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
  shows ONLY: the new `per_player_construction` kwarg in `_row()`
  signature and the corresponding dict-literal change. No
  fixture-row line is modified in T02.
- `pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py -v`
  passes with all pre-existing tests unchanged (deferred to T05; not
  run in T02 itself).

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`

**Read scope:**
- (none — task is mechanical)

**Task-specific stop condition:** halt if any pre-existing test
fails after this change (it should not — the default preserves
behavior); halt if any existing fixture row is altered in T02 (T02
is purely about the helper signature; fixture lift is T02b Step 0).

**Validation report shape:** show diff of test file; confirm exactly
two hunks (signature + dict-literal); confirm no fixture row changed.

**Executor model:** Sonnet (mechanical signature change).

---

### T02b — Lift fixture parity AND add tests for V-9

**Objective:** Step 0 (mandatory first) lifts the three
`blocked_or_deferred` fixture rows to
`per_player_construction="blocked"` to restore fixture/skeleton
parity. Step 1 onwards appends seven new tests covering V-9 happy
path, asymmetric rejection, unknown-token rejection, sentinel under
conjunction (passes), sentinel outside conjunction (fails), non-string
rejection, and sanity-gate-row symmetric (passes).

**Step 0 (REQUIRED FIRST — fixture lift, analogous to PR #214 Step 0
and PR #213 F1).** Update three fixture rows by passing an explicit
`per_player_construction="blocked"` kwarg:

- Row at fixture index 4 (`feature_family_id =
  "sc2egset.blocked_or_deferred.mind_control_event_count"`): pass
  `per_player_construction="blocked"`.
- Row at fixture index 5 (`feature_family_id =
  "sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot"`):
  pass `per_player_construction="blocked"`.
- Row at fixture index 6 (`feature_family_id =
  "sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields"`):
  pass `per_player_construction="blocked"`.

The other 4 fixture rows (indices 0–3 — pre_game, history,
in_game_snapshot model-input, sanity_gate `slot_identity_consistency`)
inherit the default `per_player_construction="symmetric"` from the
kwarg added in T02. No change is needed on those rows. This Step-0
fixture lift is mandatory: as-is, V-9 would FAIL on the existing
fixture's three blocked rows (conjunction holds, value is
`"symmetric"`, expected `"blocked"`).

**Step 1 onwards.** Append the seven V-9 tests:

1. `test_v9_valid_skeleton_passes(valid_skeleton)` — happy path
   after Step 0 fixture lift.
2. `test_v9_asymmetric_on_model_input_fails(valid_skeleton)` — set
   row 0 (pre_game model-input row) `per_player_construction =
   "asymmetric"`. Expect `AssertionError` matching
   `"V-9.*asymmetric"` (or `"V-9.*expected one of \\['symmetric'\\]"`).
3. `test_v9_unknown_token_fails(valid_skeleton)` — set row 1
   (history model-input row) `per_player_construction =
   "match_level"`. Expect `AssertionError` matching
   `"V-9.*match_level"`.
4. `test_v9_sentinel_under_conjunction_passes(valid_skeleton)` —
   document the sentinel path (the three blocked rows already carry
   `"blocked"` after Step 0; V-9 must pass).
5. `test_v9_sentinel_outside_conjunction_fails(valid_skeleton)` —
   set row 0 (pre_game, `status="allowed"`) `per_player_construction
   = "blocked"`. Conjunction does NOT hold → `"blocked"` not in
   vocabulary `{"symmetric"}` → V-9 fires. Expect `AssertionError`
   matching `"V-9.*blocked"`.
6. `test_v9_non_string_per_player_construction_fails(valid_skeleton)` —
   set row 0 `per_player_construction = 0` (int, type-ignore). Expect
   `AssertionError` matching `"V-9.*not a string"`.
7. `test_v9_status_mismatch_rejects_sentinel(valid_skeleton)` —
   construct a fresh row via `_row()` with
   `prediction_setting="blocked_or_deferred"`,
   `status="allowed"` (NOT
   `"blocked_until_additional_validation"`),
   `per_player_construction="blocked"`,
   `feature_family_id="sc2egset.blocked_or_deferred.custom_deferred_v9"`,
   plus the other defaults that satisfy V-1..V-8. Append it to a
   deepcopy of `valid_skeleton`. Conjunction fails because `status`
   is wrong → `"blocked"` not in V-9 vocabulary → V-9 fires. Expect
   `AssertionError` matching `"V-9"`. (This mirrors V-7's
   `test_v7_carve_out_status_mismatch_fails` pattern; V-3 does NOT
   fire because the family name is not one of the three
   `BLOCKED_TRACKER_FAMILIES`.)

Place the new test block after the existing V-8 test block,
beginning with a section divider comment:

```python
# ---------------------------------------------------------------------------
# V-9 per_player_construction controlled vocabulary + sentinel
# ---------------------------------------------------------------------------
```

**Verification:**
- `pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py -v`
  passes after Step 0 + 7 new tests (deferred to T05).

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` (post-T01, especially the new helper and reused constants)
- The merged notebook .py to confirm the three blocked rows' on-disk `per_player_construction` value is `"blocked"` (live verification).

**Task-specific stop condition:** halt if any test from PR #212 /
PR #213 / PR #214 fails in a way not caused by Step 0; halt if Step
0 is skipped or partially applied; halt if the V-7 sentinel-related
tests (which test cold_start_handling, NOT per_player_construction)
break — they should not, since V-7 and V-9 operate on different
columns.

**Validation report shape:** show diff of test file; confirm 3
fixture row updates + 7 tests added; confirm no test deleted;
confirm the post-T05 coverage report shows the new V-9 helper at
100% on its added lines.

**Executor model:** Sonnet.

---

### T03 — Notebook narrative correction (markdown / comment cells only)

**Objective:** Correct three narrative passages in the merged
notebook .py to (a) acknowledge V-9 has landed; (b) drop "D10" from
the deferred-D-list at line 500 (covered by V-9); (c) fix the D8
misnaming at lines 537–538 (D8 is full-replay aggregate exclusion,
NOT symmetry); (d) update the stale "deferred to a future V-9" line
at lines 540–541 to acknowledge V-9 has landed and to record D10
sub-clause 2 (aoestats `canonical_slot`) as N/A for sc2egset. Update
the print-banner from V-8 to V-9. Add a row to the "Checks IN scope"
table (lines 484–491) documenting V-9. NO SKELETON literal tuple is
changed.

**Instructions:** Replace the text shown in "Before" with "After"
at each of the five locations. Line numbers refer to the .py file
as it exists on master at `664c869a`.

| Location | Before | After |
|----------|--------|-------|
| Lines 484–491 (markdown table "Checks IN scope") — append a `V-9` row | (current 6 rows: V-1, V-2, V-3, V-4, V-5, V-6) | append: `\| V-9 \| Every row's per_player_construction matches the controlled vocabulary {"symmetric"} for model-input and sanity-gate rows, OR equals the sentinel "blocked" under the V-7 conjunction (prediction_setting == "blocked_or_deferred" AND status == "blocked_until_additional_validation"). Invariant I5 / CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1. D10 sub-clause 2 (aoestats canonical_slot p0/p1 projection) is N/A for sc2egset. \|` |
| Line 493 — IN-scope sentence | `Checks IN scope as of this PR (V-1 base, V-1 strict, V-2..V-7 from PRs\n# #212/#213, V-8 source-grain structural well-formedness +\n# provenance-key consistency from this PR).` | `Checks IN scope as of this PR (V-1 base, V-1 strict, V-2..V-7 from PRs\n# #212/#213, V-8 source-grain structural well-formedness from PR #214,\n# V-9 per_player_construction controlled vocabulary + sentinel from this PR).` |
| Line 500 — deferred-D-list | `# dimensions D2/D3/D6/D8/D9/D10/D12/D15.` | `# dimensions D2/D3/D6/D8/D9/D12/D15.` (drop D10; V-9 covers it.) |
| Line 507 print-banner | `print("validate_registry_skeleton: ALL PASS (V-1 through V-8)")` | `print("validate_registry_skeleton: ALL PASS (V-1 through V-9)")` |
| Lines 535–543 (Follow-ups list — D-list paragraph) | `D8 (per_player_construction\n#   symmetry), D9 (allowed_cutoff_rule structural parsing), D10\n#   (focal/opponent symmetry per CROSS-02-03-v1.0.1 §4.1; NOT\n#   source-grain — V-8 of this PR covers source-grain well-formedness;\n#   spec-D10 is symmetry, deferred to a future V-9), D12 (target_grain\n#   consistency with prediction_setting), D15 (cross-row consistency of\n#   tracker-event-family references against the eligibility CSV).` | `D8 (full-replay aggregate exclusion for in_game_snapshot rows per\n#   CROSS-02-03-v1.0.1 §4.1; NOT per_player_construction symmetry\n#   — that is D10 sub-clause 1, covered by V-9 of this PR), D9\n#   (allowed_cutoff_rule structural parsing), D12 (target_grain\n#   consistency with prediction_setting), D15 (cross-row consistency of\n#   tracker-event-family references against the eligibility CSV).\n# - D10 sub-clause 2 (aoestats canonical_slot p0/p1 projection per\n#   CROSS-02-00-v3.0.1 §5.2; aoestats-ONLY column) is N/A for sc2egset\n#   and is deferred to a future aoestats-side V-N PR.` |

After edits, run `jupytext --sync` to regenerate the paired `.ipynb`.

**Stop conditions and validation:** halt on any out-of-scope diff,
any SKELETON_* literal change, or any .ipynb edit not produced by
jupytext --sync. Confirm `git diff --stat
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
shows ONLY narrative hunks (no Python code change beyond the print
banner) and no edits to lines 269–474 (the SKELETON_* row literals
plus the `_COLS` / `SKELETON =` aggregation lines).

**Executor model:** Sonnet.

---

### T04 — Run pre-commit-equivalent checks (ruff/mypy/jupytext)

Same shape as PR #214's T04. Run ruff + mypy + jupytext --check on
the three modified files (validator + tests + notebook .py). Stop
on any error.

**Executor model:** Sonnet.

---

### T05 — Run pytest with coverage; verify ≥ 95%

`source .venv/bin/activate && poetry run pytest tests/ -v --cov
--cov-report=term-missing | tee coverage.txt`. Confirm post-PR-#214
test count + 7 new V-9 tests pass; overall coverage ≥ 95%; new V-9
helper at 100% on its added lines. Delete `coverage.txt`.

**Executor model:** Sonnet.

---

### T06 — Execute the merged notebook and confirm ALL PASS (V-1 through V-9)

`source .venv/bin/activate && poetry run jupyter nbconvert --to
notebook --execute --inplace --ExecutePreprocessor.timeout=300
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`,
then `jupytext --sync`. Confirm output banner reads
`"validate_registry_skeleton: ALL PASS (V-1 through V-9)"`.

**Executor model:** Sonnet.

---

### T07 — Scaffold/code commit (4 files)

Stage exactly:
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`

Commit message subject: `feat(phase02): SC2EGSet 02_01_01 V-9 per-player construction / focal-opponent symmetry (spec-D10)`

(Body per the planner's commit-template content: V-9 description
binding D10 sub-clause 1 / Invariant I5; controlled vocabulary
`{"symmetric"}` + carve-out sentinel `"blocked"` on V-7 conjunction;
fixture lift on three blocked rows analogous to PR #214 T02b Step 0;
narrative correction for D8 misnaming and V-9 acknowledgement;
aoestats sub-clause 2 N/A for sc2egset deferral; spec bindings
CROSS-02-00 §5.2 / CROSS-02-02 §4.2 §5.1 / CROSS-02-03 §4.1 D10;
non-batching lineage step 6.)

**Executor model:** Sonnet.

---

### T08 — Release commit (pyproject.toml + CHANGELOG.md)

- `pyproject.toml`: `version = "3.50.0"` → `version = "3.51.0"`.
- `CHANGELOG.md`: roll `[Unreleased]` → `[3.51.0] — 2026-05-10 (PR
  #N: phase02/sc2egset-feature-registry-v9-symmetry)`; insert fresh
  `[Unreleased]` block; populate `[3.51.0] ### Added` with V-9
  bullet (e.g. *"V-9 per-player construction / focal-opponent
  symmetry validation (spec-D10 sub-clause 1; Invariant I5).
  Controlled vocabulary `{\"symmetric\"}` for model-input and
  sanity-gate rows; carve-out sentinel `\"blocked\"` under the V-7
  conjunction. Fixture lift on three blocked rows. D10 sub-clause 2
  (aoestats `canonical_slot` p0/p1 projection) recorded N/A for
  sc2egset and deferred to a future aoestats-side V-N."*).
- Commit message: `chore(release): bump version to 3.51.0`.

**Executor model:** Sonnet.

---

### T09 — Push, create draft PR, run reviewer-deep, mark ready

1. `git push -u origin phase02/sc2egset-feature-registry-v9-symmetry`.
2. Write PR body to `.github/tmp/pr.txt` per template.
3. `gh pr create --draft --title "feat(phase02): SC2EGSet 02_01_01 V-9 per-player construction / focal-opponent symmetry (spec-D10)" --body-file .github/tmp/pr.txt --base master`.
4. Capture PR number `N`. Substitute `PR #N` into CHANGELOG. Commit
   `chore(release): substitute PR number in CHANGELOG [3.51.0]`. Push.
5. Append `(PR #N)` to active-plan row in `planning/INDEX.md` (bulk
   INDEX update happens BEFORE T01 in the docs(planning) commit
   landing this plan).
6. Dispatch `@reviewer-deep` on the live PR with: `planning/current_plan.md`
   path + `base_ref = master @ 664c869a`.
7. On PASS / PASS-WITH-NOTES → `gh pr ready N` + cleanup `.github/tmp/`.
   On methodology BLOCKER → halt and route to reviewer-adversarial per
   `.claude/rules/data-analysis-lineage.md` line 24 carve-out (do NOT
   merge until adversarial returns PASS).

**Executor model:** Sonnet for mechanics; reviewer-deep for the gate.

## Validation gates

(Same shape as PR #214; see §Gate Condition above. Specifically:
9-file diff; banner shows V-1..V-9; coverage ≥ 95%; ruff/mypy/jupytext
clean; SKELETON literals byte-identical to master `664c869a`;
reviewer-deep PASS or PASS-WITH-NOTES; release artifacts at 3.51.0
with PR-number substituted.)

## Release policy

Version 3.50.0 → 3.51.0. Minor (Cat A feat). Single source:
`pyproject.toml`. CHANGELOG roll under `[3.51.0] — 2026-05-10 (PR
#N: phase02/sc2egset-feature-registry-v9-symmetry)`. Fresh
`[Unreleased]` inserted at top.

## Reviewer routing

- **Plan-phase critique:** `reviewer-deep` (per
  `.claude/rules/data-analysis-lineage.md` line 24 Phase 02
  carve-out — same routing as PR #212 / PR #213 / PR #214).
- **Post-execution gate:** `reviewer-deep` at T09.
- **Reviewer-adversarial:** ONLY on methodology BLOCKER from
  reviewer-deep. The plan-side decision to admit only `"symmetric"`
  (rejecting `"asymmetric"` outright at the registry-skeleton layer
  per Invariant I5) is methodology-load-bearing; reviewer-deep may
  flag this. If a methodology BLOCKER fires, the parent dispatches
  reviewer-adversarial; the 3-round adversarial cap from feedback
  memory applies symmetrically.

## Non-batching rationale

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule":

1. ROADMAP — PR #211 (already merged) ✓
2. Scaffold + first validation module — PR #212 ✓
3. Execute + report — PR #212 ✓
4. User review — PR #212 ✓
5. Commit — PR #212 ✓
6. **Next validation module** —
   PR #213 (V-1 strict + V-7) ✓ → PR #214 (V-8) ✓ → *this PR* (V-9);
   sequence step 6 is iterative, each "next validation module" is
   its own PR.
7. Artifacts — deferred (D2/D3/D4-in_game/D5-in_game/D6-full/D8 still
   uncovered; closure not in scope yet).
8. research_log / STEP_STATUS / manifest — deferred.
9. Closing reviewer-deep — deferred.

V-9 is a single validation module per sequence step 6. This PR does
NOT bundle artifact generation, status updates, or manifest updates.
V-9 is intentionally narrow: it validates ONE column
(`per_player_construction`) against ONE controlled vocabulary
(`{"symmetric"}`) plus the existing V-7 conjunction sentinel. It
does NOT extend to D3 (relational reconcilability), D8 (in_game
full-replay exclusion), D4/D5 in_game side, or aoestats sub-clause 2.
Each future "next validation module" PR lands one validator at a
time.

## Stop conditions

### Pre-implementation stop condition

Working tree must be clean on the freshly-created branch
`phase02/sc2egset-feature-registry-v9-symmetry` (checked out from
`master @ 664c869a`); halt if `git status` lists any modification
beyond `planning/current_plan.md`,
`planning/current_plan.critique.md`, `planning/INDEX.md` (which are
landed by the docs(planning) commit before T01).

### Mid-implementation halt triggers

1. Verification computations in §Verification fail when re-run
   against the on-disk skeleton at master `664c869a`.
2. Pre-commit hook (ruff/mypy) fails; investigate and fix; create
   NEW commit (never `--amend`).
3. Pytest fails or coverage falls below 95%.
4. Notebook execution at T06 raises `AssertionError`.
5. `git status` lists any forbidden file.
6. T01 redefines `BLOCKED_PREDICTION_SETTING` / `BLOCKED_STATUS` /
   `BLOCKED_SENTINEL` instead of reusing them.
7. T01 modifies any V-1..V-8 helper.
8. T03 produces any change to a SKELETON_* row literal in the
   notebook .py.
9. T02b Step 0 is skipped (V-9 fails on existing fixture without it).
10. `gh pr create` fails or `git push` is rejected.
11. Reviewer-deep returns methodology BLOCKER → route to
    reviewer-adversarial.

## Open Questions

None unresolved. Methodology decisions resolved in the plan:

- **Q (chosen direction):** A / B / C / D? **Resolved:** **(A) V-9
  per-player construction / focal-opponent symmetry (spec-D10
  sub-clause 1).** This is the user's preferred direction; it is
  methodologically sound (D10 is the actual symmetry dimension; the
  on-disk column has a clean two-value partition supporting a
  controlled-vocabulary check; Invariant I5 is the load-bearing
  invariant); it is non-vacuous (23 rows = `"symmetric"`; 3 rows =
  `"blocked"`; 0 rows = anything else); and it follows the
  established conjunction-carve-out pattern from V-7 without
  redefining shared logic. (B) was rejected because the user's
  direction is sound and there is no methodological reason to
  defer it. (C) was rejected because at least one further
  skeleton-layer validator is warranted (D10 has been mis-deferred
  twice now — first by PR #212's notebook narrative, then by
  PR #214's documentation cleanup — and finally landing the actual
  validator is overdue). (D) was rejected because D2, D3,
  D4-in_game, D5-in_game, D6-full, D8 remain unaddressed; closure
  is not defensible.

- **Q (controlled vocabulary breadth):** Should V-9 admit
  `"asymmetric"`, `"match_level"`, `"per_player_role"`, or other
  tokens? **Resolved:** No. The on-disk SKELETON uses only
  `{"symmetric", "blocked"}`. Invariant I5 categorically forbids
  asymmetric per-player construction. Match-level features (map,
  patch) on the existing skeleton carry `"symmetric"` (their
  per-player computation produces an identical constant for both
  slots, which IS the degenerate case of symmetric construction);
  admitting `"match_level"` as a separate token would require a
  prior skeleton patch and is out of scope.

- **Q (aoestats canonical_slot sub-clause):** Does V-9 cover D10
  sub-clause 2? **Resolved:** No. CROSS-02-00-v3.0.1 §5.2 documents
  `canonical_slot` as "aoestats-ONLY", "NOT in MHM UNION ALL".
  sc2egset has no `canonical_slot` column on
  `matches_history_minimal`; per-player slot semantics are already
  established via `replay_players_raw` (per-player rows) and
  tracker `playerId` / `controlPlayerId` / `killerPlayerId` /
  `owner_via_unitborn_lineage`. Sub-clause 2 is N/A for sc2egset.
  Deferred to a future aoestats-side V-N PR (out of scope here).

- **Q (sanity-gate row treatment):** Does the
  `slot_identity_consistency` sanity-gate row receive a special
  `per_player_construction` value (e.g.,
  `"sanity_gate_not_model_input"`)? **Resolved:** No. The on-disk
  skeleton has the sanity-gate row at
  `per_player_construction = "symmetric"`. Its
  `sanity_gate_not_model_input` semantics live on the `status`
  column, not on `per_player_construction`. V-9 treats the
  sanity-gate row identically to model-input rows for vocabulary
  purposes — both must carry `"symmetric"`.

- **Q (PR #213/#214 carry-forward follow-ups):** Items (defensive
  branch coverage on lines 347/415/421; `parents[6]` test-infra
  magic; V-8 helper bare-`(filename)` permissiveness) — folded into
  V-9 PR or deferred? **Resolved:** Deferred. None affects V-9 scope.
  All three are listed in §Out of scope as deferred to a separate
  hygiene PR.

- **Q (which validator is V-10 / V-11):** Deferred. V-10 candidates
  in priority order: D8 (in_game full-replay aggregate exclusion —
  binding for the 7+4 in_game rows); D4/D5 in_game side; D3 source
  grain ↔ model grain reconcilability; D2 source classification.
  Chosen in the V-10 plan PR.

## Out of scope

- No row-content edits to the 26-row skeleton. Verification confirms
  all 26 rows already satisfy V-9 by construction.
- No new validation modules beyond V-9.
- No registry CSV / MD artifact under
  `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
- No edits to `STEP_STATUS.yaml`,
  `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, the
  per-dataset `research_log.md`, the cross-game
  `reports/research_log.md`, the ROADMAP, the locked `02_*` specs,
  or the notebook regeneration manifest.
- No DuckDB I/O. No tracker-CSV row-content modification.
- No AoE2 work. **D10 sub-clause 2 (aoestats `canonical_slot` p0/p1
  projection) is N/A for sc2egset and is explicitly deferred to a
  future aoestats-side V-N PR; no aoestats files are touched.**
- Step 02_01_01 itself is NOT closed by this PR. After V-9 lands,
  D2/D3/D4-in_game/D5-in_game/D6-full/D8 remain unaddressed;
  closure requires at least one more validator PR (most likely
  V-10 covering D8).
- Test-infra cleanup (`parents[6]` repo-root magic at
  `tests/.../test_validate_registry_skeleton.py:25`) deferred to a
  hygiene PR.
- Defensive-branch coverage / `# pragma: no cover` for
  `validate_registry_skeleton.py` lines 347 / 415 / 421 (PR #213
  follow-up #4 carry-forward) deferred to a hygiene PR.
- V-8 helper bare-`(filename)` permissiveness on tracker rows
  (PR #214 reviewer-deep §Per-question finding 4 N1) deferred to
  a hygiene PR.
- V-10+ (in_game full-replay D8; in_game side of D4/D5; relational
  D3; source classification D2) deferred to future PRs.

## Acceptance criteria

The PR is mergeable when ALL of the following are simultaneously true:

1. **V-9 passes on the unmodified skeleton.** No SKELETON literal
   tuple changed in `git diff master..HEAD`. Notebook executes ALL
   PASS through V-9. (Verified: 23/23 model-input-or-sanity-gate
   rows carry `"symmetric"`; 3/3 carve-out rows carry `"blocked"`;
   0 violations.)
2. **Narrative correction visible.** `git diff master..HEAD` for the
   notebook .py shows the five hunks at the lines specified in T03
   (table append at 484–491; line 493; line 500; line 507; lines
   535–543), and no other notebook .py edits.
3. **Two implementation commits.** `git log master..HEAD --oneline`
   shows the T07 scaffold/code commit followed by the T08 release
   commit (and optionally a T09 PR-number-substitution commit). No
   `--amend`.
4. **No forbidden files in `git diff master..HEAD`.** Diff lists
   only files from §File Manifest / Allowed; the file count is
   exactly 9.
5. **Coverage ≥ 95%.** `pytest --cov` reports overall ≥ 95%; new
   V-9 helper shows 100% line coverage on its added lines.
6. **Reviewer-deep verdict is PASS or PASS-WITH-NOTES.** No
   unresolved methodology BLOCKER. If a BLOCKER is raised, T09
   halts and the parent dispatches reviewer-adversarial.
7. **Notebook narrative explicitly distinguishes D8, D10, V-8, V-9.**
   The replacement text at lines 535–543 must contain a sentence
   stating that V-9 covers D10 sub-clause 1 (symmetry) for sc2egset,
   that D8 is full-replay aggregate exclusion (NOT symmetry), and
   that D10 sub-clause 2 (aoestats `canonical_slot`) is N/A for
   sc2egset, so future agents do not re-confuse them.
8. **No spec / locked-doc edits.** `git diff master..HEAD --name-only`
   contains no entry under `reports/specs/**`, `docs/**`,
   `.claude/**`, `thesis/**`, or any `INVARIANTS.md`.
