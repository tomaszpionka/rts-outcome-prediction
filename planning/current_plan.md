---
title: "SC2EGSet Step 02_01_01 — V-8 source-grain structural well-formedness validation"
category: A
branch: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness
date: 2026-05-09
planner_model: claude-opus-4-7
branch_prefix: phase02/
branch_name: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness
pr_title: "feat(phase02): SC2EGSet 02_01_01 V-8 source-grain structural well-formedness"
base_ref: "master @ 7b26b40f"
base_commit: 7b26b40ffdb016bf643a8cd1a74a8388da6cb7ea
target_version: "3.50.0"
version_current: "3.49.0"
version_bump_type: "minor (Category A feat)"
created_date: 2026-05-09
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
step_name: "Feature-family registry skeleton (sc2egset)"
lineage_sequence_step: 6
prior_pr_ref: "#213"
invariants_touched: [I3, I6, I7]
reviewer_gate_plan: reviewer-deep
reviewer_gate_post_execution: reviewer-deep
reviewer_adversarial_required: false
critique_required: true
spec_bindings:
  - CROSS-02-00-v3.0.1
  - CROSS-02-02-v1.0.1
  - CROSS-02-03-v1.0.1
non_batching_lineage_position: "Sequence step 6 continuation — additional validation module under data-analysis-lineage.md §'Non-batching rule'. PR #212 delivered scaffold + V-1..V-6; PR #213 added V-1 strict + V-7. This PR adds V-8. Artifact generation (sequence step 7), research_log / STEP_STATUS / manifest (steps 8) and final reviewer-deep gate (step 9) remain deferred."
source_artifacts:
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - planning/current_plan.md (PR #213 plan, structural template reuse)
  - planning/current_plan.critique.md (PR #213 reviewer-deep critique)
research_log_ref: "(deferred — research_log entry for Step 02_01_01 lands in the future closure PR per data-analysis-lineage.md §'Non-batching rule' step 8; this PR makes no research_log edits)"
---

# Plan: SC2EGSet Step 02_01_01 — V-8 source-grain structural well-formedness validation

## Scope

This PR delivers ONE additional validation module (V-8) for the SC2EGSet
Step 02_01_01 feature-family registry skeleton, extending
`validate_registry_skeleton()` from V-1..V-7 (delivered by PR #212 and
PR #213) to V-1..V-8. V-8 asserts column-level **structural
well-formedness** of the `source_grain` field for every skeleton row,
plus **provenance-key consistency** between `source_grain` and
`source_table_or_event_family`. V-8 is NOT a controlled-vocabulary
enum check (the `source_grain` column does not carry an enum); it is
NOT a focal/opponent-symmetry check (that is CROSS-02-03-v1.0.1 §4.1
D10, deferred to a future V-9); and it is NOT a relational
source-grain ↔ model-input-grain reconcilability check (that is D3,
deferred to a future V-N).

The merged 26-row skeleton from PR #212 (sandbox notebook + paired
ipynb) remains untouched in row content. Only narrative text in
markdown cells / code-comment cells is corrected to align with V-8's
resolved scope. No new artifacts are produced; no STEP_STATUS /
PIPELINE_SECTION_STATUS / PHASE_STATUS / research_log / manifest edits
are performed. Step 02_01_01 itself is NOT closed by this PR.

This PR continues lineage sequence step 6 ("Next validation module")
per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for
empirical work". V-8 is the next defensible skeleton-layer validator
after the D-coverage analysis in §Problem Statement below.

## Problem Statement

PR #212 delivered the SC2EGSet Step 02_01_01 feature-family registry
scaffold — a 26-row in-memory skeleton plus the V-1..V-6 validation
module. PR #213 added V-1 strict (`feature_family_id` second-segment
alignment with `prediction_setting`) and V-7 (`cold_start_handling`
controlled vocabulary `{G-CS-1..G-CS-6}` plus the `"blocked"` sentinel
under the `prediction_setting == "blocked_or_deferred"` AND
`status == "blocked_until_additional_validation"` carve-out
conjunction).

After PR #213, eight CROSS-02-03-v1.0.1 §4.1 audit dimensions remain
unaddressed by skeleton-layer validators (D2, D3, D4 in_game side,
D5 in_game side, D8, D10, plus D6 partial and D9/D15 which are
post-materialization and out-of-scope at this layer). The user's
preferred next direction is "V-8 / D10 source-grain well-formedness".
Independent verification of that framing against the locked
CROSS-02-03-v1.0.1 spec finds **two methodological defects** in the
user's framing that must be resolved before authoring V-8:

**Defect 1 — D10 in the spec is NOT source-grain well-formedness.**
CROSS-02-03-v1.0.1 §4.1 row D10 reads: *"Focal/opponent symmetry and
p0/p1 projection. Every per-player feature is computed by the same
SQL pattern or function for the focal player and the opponent
(Invariant I5). For aoestats, the `p0_*` / `p1_*` source asymmetry
is resolved via the `canonical_slot` focal/opponent assignment
(CROSS-02-00-v3.0.1 §5.2; aoestats-only column) before any feature
computation that depends on player role. RISK-24 routes the
operationalization to a Phase 02 ROADMAP step."*. The notebook's own
deferred-D-list at lines 535–540 of
`02_01_01_feature_family_registry_skeleton.py` calls D10
"source-grain well-formedness" — that is a notebook narrative
inaccuracy inherited from PR #212 that disagrees with the locked
spec. The spec is authoritative; this PR's V-8 must therefore
**rename** the work to "source-grain structural well-formedness" and
explicitly state it is **not** spec-D10 (which is symmetry, deferred
to a future V-9).

**Defect 2 — the on-disk `source_grain` column has no controlled
enum.** Live extraction of all 26 rows of the merged SKELETON yields
7 distinct values, all of shape `(filename[, key1[, key2]])`:

- `(filename, player_id_worldwide)` ×8 — non-tracker
- `(filename, playerId)` ×8 — tracker (PlayerStats / Upgrade /
  PlayerSetup, plus 2 of the 3 carve-out blocked rows)
- `(filename, controlPlayerId)` ×3 — tracker (UnitBorn / UnitInit)
- `(filename, owner_via_unitborn_lineage)` ×3 — tracker (UnitTypeChange
  / UnitDied lineage-attributed / UnitPositions carve-out)
- `(filename)` ×2 — non-tracker match-level (map_type / patch)
- `(filename, player_id_worldwide, opponent_player_id_worldwide)` ×1
  — non-tracker matchup history (head-to-head)
- `(filename, killerPlayerId)` ×1 — tracker (UnitDied direct
  attribution)

These are tuple-of-key-columns grain expressions describing the
identity-key composition each source feeds into the model row, not
a closed enum vocabulary. Crucially, **the 3 carve-out (blocked)
rows DO carry real source_grain key tuples**, NOT a `"blocked"`
sentinel — sentinels are present on `model_input_grain`,
`target_grain`, `temporal_anchor`, `allowed_cutoff_rule`,
`candidate_leakage_modes`, and `cold_start_handling`, but the
`source_grain` column carries the actual source table's natural key
even for blocked rows, because the source table provenance is known
(only the downstream model usage is blocked).

The user's framing is therefore methodologically incorrect on two
counts: (1) D10 is not source-grain, and (2) source_grain has no
enum to lock. **The defensible reframing is to deliver V-8 as a
column-shape structural validator** that asserts (a) every row's
`source_grain` parses as a non-empty parenthesised tuple expression
beginning with `filename`; (b) every key in the tuple is a
syntactically valid identifier; (c) tracker-event rows carry one of
the four documented tracker attribution keys (`playerId`,
`controlPlayerId`, `killerPlayerId`, or `owner_via_unitborn_lineage`)
in their grain tuple; (d) non-tracker rows carry either no extra key
(bare `(filename)`) or one or two of the worldwide-identity keys
(`player_id_worldwide`, `opponent_player_id_worldwide`). This is
narrow, deterministic, and can be validated entirely in a regex /
parse + set-membership check.

V-8 in this PR closes a skeleton-layer well-formedness gap on the
`source_grain` column without committing to spec-D10 semantics. The
spec-D10 (focal/opponent symmetry) is left for a future V-9 against
the existing `per_player_construction` column.

## Assumptions & Unknowns

**Assumptions** (declared explicit so the executor can halt if any
becomes false during T01–T08):

1. The merged 26-row SKELETON in
   `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
   already satisfies V-8 by construction (all 26 rows match the
   `^\(filename(?:,\s*[A-Za-z_][A-Za-z0-9_]*)*\)$` regex; tracker
   rows use only the four documented attribution keys; non-tracker
   rows use only the bare-match form or `player_id_worldwide` +
   optional `opponent_player_id_worldwide`). Verified live by the
   planner during plan authoring (0 violations; planner-mode read-only
   extraction reproduced in §Verification below).
2. The narrative target lines in the notebook .py (lines 144, 500,
   539) are stable across master `7b26b40f` (PR #213 merge commit)
   and the new branch's HEAD. Verified by the planner against the
   on-disk file at master `7b26b40f`.
3. The existing `valid_skeleton` test fixture (7 rows after PR #213's
   updates) carries `source_grain == "(filename, player_id_worldwide)"`
   on every row by `_row()` default. After the carve-out
   `cold_start_handling` patch from PR #213 Step 0 of T02b, the
   fixture's three `blocked_or_deferred` rows have
   `cold_start_handling == "blocked"` but `source_grain` remains the
   default tuple — that satisfies V-8 (carve-out rows carry real
   grain tuples, not a `"blocked"` sentinel on this column).
4. `pyproject.toml` line 3 reads `version = "3.49.0"` at branch HEAD;
   T08 mechanically bumps to `"3.50.0"`. Confirmed by the planner.
5. CHANGELOG.md `[Unreleased]` block is empty after PR #213's
   roll-up. Confirmed by the planner.
6. The four tracker attribution keys (`playerId`, `controlPlayerId`,
   `killerPlayerId`, `owner_via_unitborn_lineage`) cover every
   tracker_events_raw player-attribution semantics declared in
   `tracker_events_feature_eligibility.csv` `notes_for_phase02` /
   `eligibility_scope` / `evidence_source` columns. Verified by the
   planner: PlayerStats / PlayerSetup / Upgrade rows attribute via
   `playerId`; UnitBorn / UnitInit rows attribute via `controlPlayerId`;
   UnitDied direct attribution uses `killerPlayerId` (V2 high-confidence
   per CSV), UnitDied lineage-attributed victim ownership uses
   `owner_via_unitborn_lineage` (V5 lineage); UnitTypeChange uses
   `owner_via_unitborn_lineage` (V5 lineage); UnitPositions uses
   `owner_via_unitborn_lineage` (V5 deferred). No fifth key is needed
   for the merged 26-row skeleton.
7. The two non-tracker worldwide-identity keys (`player_id_worldwide`,
   `opponent_player_id_worldwide`) cover every non-tracker
   player-keyed row in the merged skeleton; the bare `(filename)`
   form covers map / patch / version match-level rows. No third
   non-tracker key is needed.

**Unknowns** (must NOT block T01; surfaced for executor awareness):

1. Whether the existing `_row()` test helper accepts a
   `source_grain` parameter or hard-codes it. Inspection of the test
   file confirms `_row()` hard-codes
   `"source_grain": "(filename, player_id_worldwide)"` at line 56.
   Mitigation: T02b Step 0 parameterizes `_row()` to accept
   `source_grain` as an optional kwarg defaulted to the existing
   value; no fixture row needs to change unless a perturbation test
   needs a different value.
2. Whether reviewer-deep at T09 (post-execution gate) raises any
   methodology BLOCKER beyond the issues already addressed in this
   plan. If so, T09 routes to reviewer-adversarial per
   `.claude/rules/data-analysis-lineage.md` line 24 carve-out.

## Literature Context

- **CROSS-02-00-v3.0.1** (`reports/specs/02_00_feature_input_contract.md`):
  binding input contract for Phase 02 feature engineering. §3.2
  defines the per-dataset native player-identity column on
  `player_history_all` for sc2egset (`toon_id`, with §3.2 noting
  identity-resolution work in 01_04_04b yielded
  `player_id_worldwide` as the worldwide-identity column).
  V-8's non-tracker grain-key vocabulary
  (`player_id_worldwide`, `opponent_player_id_worldwide`) binds the
  worldwide-identity column documented in INVARIANTS.md §2 / Branch
  (iii).
- **CROSS-02-02-v1.0.1 §4.1 / §6.1 / §6.2 / §6.3**
  (`reports/specs/02_02_feature_engineering_plan.md`): defines
  source grains and per-family source-table assignments. §4.1
  specifies prose-style source grain descriptions (`2 rows per
  match (one per player)`, `1 row per player per match`, `1 event
  per row`); the on-disk skeleton encodes these as tuple-of-key-columns
  expressions, which is a richer (but spec-consistent) representation
  of the underlying grain contract.
- **CROSS-02-03-v1.0.1 §3 audit-object schema**
  (`reports/specs/02_03_temporal_feature_audit_protocol.md`):
  defines the `source_grain` field of the audit object as
  *"`2 rows per match (one per player)` (sc2egset / aoe2companion /
  aoestats post-projection); `1 row per player per match` for
  `player_history_all`; `1 event per row` for tracker event
  families"*. V-8 of THIS PR validates a richer encoding of the same
  underlying contract — the tuple-of-key-columns shape — and asserts
  the column is well-formed and provenance-consistent with
  `source_table_or_event_family`.
- **CROSS-02-03-v1.0.1 §4.1 D10**: explicitly defines D10 as
  *"Focal/opponent symmetry and p0/p1 projection"* (Invariant I5),
  NOT source-grain well-formedness. V-8 of THIS PR is a renamed
  source-grain validator and is explicitly disjoint from spec-D10.
  The notebook's deferred-D-list narrative (line 539) using "D10
  (source-grain well-formedness)" is corrected to "source-grain
  well-formedness (NOT spec-D10)" in T03.
- **`tracker_events_feature_eligibility.csv`** (15 rows): documents
  per-tracker-event family attribution semantics in the
  `notes_for_phase02`, `eligibility_scope`, and `evidence_source`
  columns. The four documented attribution keys
  (`playerId`, `controlPlayerId`, `killerPlayerId`,
  `owner_via_unitborn_lineage`) correspond verbatim to the attribution
  patterns recorded in those CSV columns:
  - `playerId` for PlayerStats / PlayerSetup / Upgrade ("V2
    high-confidence playerId mapping");
  - `controlPlayerId` for UnitBorn / UnitInit ("V2 high-confidence
    controlPlayerId");
  - `killerPlayerId` for UnitDied direct kill attribution
    ("killer attribution direct via killerPlayerId");
  - `owner_via_unitborn_lineage` for UnitTypeChange / UnitDied
    lineage-attributed victim / UnitPositions ("owner via UnitBorn
    / UnitInit lineage join"; "lineage-attributed cutoff-count").
- **PR #212** (merged 2026-05-08 at master `18d30a81`): scaffold +
  V-1..V-6.
- **PR #213** (merged 2026-05-08 at master `7b26b40f`): V-1 strict
  + V-7. Reviewer-deep on PR #213 filed follow-ups #3 (`_row()`
  conjunction-discipline reminder), #4 (defensive-branch coverage
  on `validate_registry_skeleton.py` lines 294/362/368), #5
  (`parents[6]` test-infra magic), #6 (plan-frontmatter date
  semantics). Per §Out of scope, items #4 and #5 are deferred to a
  hygiene PR; item #3 is folded into T02b only if a new test added
  by this PR happens to touch the relevant lines; item #6 is
  resolved in this plan's frontmatter (see §Open Questions
  resolution: this plan uses `date: 2026-05-09` as the **plan
  authoring date** convention, which matches the PR #213 plan's
  established convention).
- **`.claude/scientific-invariants.md`**: I3 (no future leakage),
  I6 (analytical results reported alongside producing code), I7 (no
  magic numbers). V-8 binds I6 indirectly (the SQL query patterns
  for tracker-event attribution must match the CSV-documented
  attribution keys) and I7 indirectly (the closed sets of allowed
  grain keys are derived from the on-disk evidence, not from
  arbitrary numeric thresholds).
- **`.claude/rules/data-analysis-lineage.md`** §"Non-batching rule":
  defines the 9-step empirical sequence. This PR is sequence step 6
  ("Next validation module") — see §Non-batching rationale at the
  end of this plan.

## Gate Condition

This PR is mergeable to master when all of the following are
simultaneously true (mirrored in §Acceptance criteria):

1. `git diff master..HEAD --name-only` lists EXACTLY 9 files: the 4
   scaffold/code files (validation module + tests + notebook .py +
   .ipynb) plus `pyproject.toml` + `CHANGELOG.md` plus the planning
   files (`planning/current_plan.md`, `planning/current_plan.critique.md`,
   `planning/INDEX.md`). No forbidden file appears.
2. The notebook's `validate_registry_skeleton()` call output cell
   contains the literal string `"validate_registry_skeleton: ALL
   PASS (V-1 through V-8)"`.
3. `pytest tests/ -v --cov` passes with overall coverage ≥ 95% and
   `validate_registry_skeleton.py` per-file coverage ≥ 95%; the new
   helper (`_check_v8_source_grain_well_formedness`) shows 100%
   line coverage on its added lines.
4. `ruff check`, `mypy`, `jupytext --check` all clean.
5. The 26 SKELETON rows in the notebook .py are byte-identical to
   master `7b26b40f` (no row literal modified).
6. Reviewer-deep at T09 returns `PASS` or `PASS-WITH-NOTES`. A
   `BLOCKER` methodology verdict halts T09 and routes to
   reviewer-adversarial per `.claude/rules/data-analysis-lineage.md`
   line 24 carve-out.
7. `pyproject.toml` shows `version = "3.50.0"`; `CHANGELOG.md` has a
   `[3.50.0]` block dated 2026-05-09 with the actual PR number `N`
   substituted (no `PR #TBD` remaining).

## File Manifest

### Allowed (this PR may touch only these)

| File | Action | Touch type | Commit |
|------|--------|-----------|--------|
| `planning/current_plan.md` | Rewrite | rewrite (this plan, authored before T01 fires) | docs(planning) — already on branch when execution starts |
| `planning/current_plan.critique.md` | Rewrite | rewrite (reviewer-deep critique authored before execution) | docs(planning) |
| `planning/INDEX.md` | Update | append archive row for PR #213 + update active row to this branch — bulk update lands BEFORE T01 fires; T09 only appends `(PR #N)` to the active-plan row | docs(planning) |
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` | Update | append constants (`SOURCE_GRAIN_TUPLE_REGEX`, `TRACKER_ATTRIBUTION_KEYS`, `NON_TRACKER_GRAIN_KEYS`); add `_check_v8_source_grain_well_formedness` private helper; wire call into `validate_registry_skeleton()` after `_check_v7_cold_start_vocabulary` | feat (T07 scaffold/code commit) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` | Update | (a) parameterize `_row()` to accept `source_grain` kwarg defaulted to existing value; (b) append new tests for V-8 happy path / regex-malformed / unknown-tracker-key / unknown-non-tracker-key / mixed-key / blocked-row-still-validates / sentinel-rejected | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` | Update | edit markdown / comment text at lines 144, 500, 539 (commentary only — no SKELETON_* literal change); update print-banner line at line 507 (V-7 → V-8) | feat (T07 commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` | Update | regenerated by `jupytext --sync` after .py edit; commit alongside paired .py | feat (T07 commit) |
| `pyproject.toml` | Update | bump `version = "3.49.0"` → `version = "3.50.0"` | chore(release) (T08 commit) |
| `CHANGELOG.md` | Update | roll `[Unreleased]` → `[3.50.0] — 2026-05-09 (PR #N: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness)`; insert empty `[Unreleased]` block; populate `[3.50.0]` Added section with V-8 bullet | chore(release) (T08 commit); PR-number substitution post-create |
| `.github/tmp/commit.txt` | Create | scratch (created and removed within session; not committed) | not committed |
| `.github/tmp/pr.txt` | Create | scratch (created, used by `gh pr create --body-file`, removed after PR is created; not committed) | not committed |

### Forbidden (executor must HALT if `git status` lists any of these)

| Forbidden path | Reason |
|----------------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/**` | No artifacts in this PR (lineage step 7 deferred). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Step 02_01_01 not closed by this PR. |
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
| `src/rts_predict/games/aoe2/**` | No AoE2 work. |
| `data/**`, `**/data/**` | No raw / staging / db edits. |
| `docs/**` | No taxonomy / spec / methodology edits. |
| `.claude/**` | No agent / rule / invariant edits. |
| Any literal SKELETON_PRE_GAME / SKELETON_HISTORY / SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT / SKELETON_GATE_AND_BLOCKED row tuple in the notebook .py | Skeleton row content is locked from PR #212. |
| `tracker_events_feature_eligibility.csv` | Upstream evidence — must NOT be modified. |
| `pyproject.toml`, `CHANGELOG.md` **during T01–T07** | These are §Allowed only at T08 (release commit). Executor must HALT if either appears in `git status` while T01–T07 are running. |
| `planning/current_plan.md`, `planning/current_plan.critique.md` **during T07–T08** | These already exist on the branch from earlier docs(planning) commits and must NOT appear in the T07 (scaffold) or T08 (release) staged sets. |
| `validate_registry_skeleton.py` lines outside the V-8 additions | T01 must add only the new constants, the new helper, and the single new call site. Existing V-1..V-7 helpers and orchestrator order MUST NOT be modified. |

## Verification before finalizing this plan (executed read-only by the planner)

1. **D-coverage matrix re-check.** Re-read CROSS-02-03-v1.0.1 §4.1
   D1–D15. Result: D10 is "Focal/opponent symmetry and p0/p1
   projection (Invariant I5)" — NOT source-grain. The notebook's
   deferred-D-list at line 539 calling D10 "source-grain
   well-formedness" is a notebook narrative inaccuracy. This plan's
   V-8 is therefore re-scoped and renamed.

2. **Source-grain enum check (live).** Inline-evaluated all 26 rows
   of the merged SKELETON. The `source_grain` column has 7 distinct
   values:
   - `(filename, player_id_worldwide)` ×8 (5 pre_game + 5 history,
     minus matchup/h2h which uses the 3-key form, minus 2 pre_game
     match-level rows that use `(filename)`)
   - `(filename, playerId)` ×8 (PlayerStats / Upgrade / PlayerSetup
     / 2 carve-outs)
   - `(filename, controlPlayerId)` ×3 (UnitBorn / UnitInit)
   - `(filename, owner_via_unitborn_lineage)` ×3 (UnitTypeChange /
     UnitDied lineage / UnitPositions carve-out)
   - `(filename)` ×2 (map_type / patch — pre_game match-level)
   - `(filename, player_id_worldwide, opponent_player_id_worldwide)` ×1
     (matchup_history_aggregate)
   - `(filename, killerPlayerId)` ×1 (UnitDied direct kill
     attribution)

   No row carries a `"blocked"` sentinel on `source_grain`. The 3
   blocked carve-out rows DO carry real grain tuples (per the
   per-row table extraction in §Verification §3 below):
   - `mind_control_event_count` — `(filename, playerId)`
   - `army_centroid_at_cutoff_snapshot` — `(filename, owner_via_unitborn_lineage)`
   - `playerstats_cumulative_economy_fields` — `(filename, playerId)`

3. **V-8 regex / key-set check (live).** All 26 rows match the
   regex `^\(filename(?:,\s*[A-Za-z_][A-Za-z0-9_]*)*\)$`. All
   tracker-row keys are drawn from `{playerId, controlPlayerId,
   killerPlayerId, owner_via_unitborn_lineage}` (4 keys; the
   tracker partition has exactly these 4 keys with the counts above
   summing to 8 + 3 + 3 + 1 = 15 tracker rows). All non-tracker-row
   keys (excluding the bare `(filename)`) are drawn from
   `{player_id_worldwide, opponent_player_id_worldwide}` (2 keys; 8
   non-tracker rows use `player_id_worldwide`, 1 row uses both keys).
   The bare `(filename)` form is permitted and used by 2 non-tracker
   match-level rows. **0 violations under V-8 as designed.**

4. **Narrative target locations (live).** The merged notebook .py
   contains three locations that paraphrase the deferred-D-list
   incorrectly (calling D10 source-grain well-formedness):
   - **line 144** (markdown cell, "Downstream decision" sub-list):
     `"add validation modules D2, D3, D6, D8, D9, D10,"` — must be
     updated to acknowledge V-8 has landed and rename "D10
     (source-grain well-formedness)" out of the deferred list (or
     correct the spec mapping inline).
   - **line 500** (markdown cell, "Checks NOT YET in scope (deferred
     to subsequent validation modules)" list): `"audit dimensions
     D2/D3/D6/D8/D9/D10/D11/D12/D15."` — must drop D11 (already
     covered by V-7) AND rename "source-grain well-formedness" out
     of D10 (D10 is symmetry, deferred separately).
   - **line 539** (markdown cell, "Follow-ups" sub-list): `"D10
     (source-grain well-formedness)"` — must be changed to either
     (a) "V-8 covers source-grain structural well-formedness; D10
     in spec is symmetry + p0/p1 projection, deferred to a future
     V-9" or equivalent; (b) remove "D10 (source-grain
     well-formedness)" since V-8 has landed.

   T03 below specifies the exact replacement text for each location.

5. **Print-banner location (live).** Line 507 reads
   `print("validate_registry_skeleton: ALL PASS (V-1 through V-7)")`.
   T03 updates this to `(V-1 through V-8)`.

## Execution Steps

Each task lists: ID, allowed files, forbidden files, exact operation,
task-specific stop condition, validation report shape, executor model
assignment.

### T01 — Add V-8 source-grain structural well-formedness check

**Objective:** Append three new module-level constants
(`SOURCE_GRAIN_TUPLE_REGEX`, `TRACKER_ATTRIBUTION_KEYS`,
`NON_TRACKER_GRAIN_KEYS`) and the private helper
`_check_v8_source_grain_well_formedness` to
`validate_registry_skeleton.py`; wire the call into the public
`validate_registry_skeleton()` orchestrator after the existing
`_check_v7_cold_start_vocabulary` call. Update the module docstring
to reflect the eight-check scope (V-1 base, V-1 strict, V-2..V-8).

**Instructions:**
1. Append after the existing `BLOCKED_STATUS` constant (around
   line 139) and before the `POST_OUTCOME_FORBIDDEN_TOKENS` constant:

   ```python
   # CROSS-02-03-v1.0.1 §3 audit-object schema for source_grain — the
   # column carries tuple-of-key-columns expressions describing the
   # identity-key composition each source feeds into the model row.
   # The on-disk skeleton uses a richer encoding than the spec's
   # prose-style description; V-8 validates the encoding's structural
   # well-formedness and provenance-key consistency with the source
   # table. V-8 is NOT spec-D10 (which is focal/opponent symmetry
   # and p0/p1 projection — Invariant I5 — deferred to a future V-9).
   import re
   SOURCE_GRAIN_TUPLE_REGEX: re.Pattern[str] = re.compile(
       r"^\(filename(?:,\s*[A-Za-z_][A-Za-z0-9_]*)*\)$"
   )

   # Tracker-event-row attribution keys documented in
   # tracker_events_feature_eligibility.csv `notes_for_phase02` /
   # `eligibility_scope` / `evidence_source` columns:
   #   - playerId: PlayerStats / PlayerSetup / Upgrade
   #   - controlPlayerId: UnitBorn / UnitInit
   #   - killerPlayerId: UnitDied direct attribution
   #   - owner_via_unitborn_lineage: UnitTypeChange / UnitDied
   #     lineage-attributed / UnitPositions
   TRACKER_ATTRIBUTION_KEYS: frozenset[str] = frozenset(
       {
           "playerId",
           "controlPlayerId",
           "killerPlayerId",
           "owner_via_unitborn_lineage",
       }
   )

   # Non-tracker (history / pre_game) row grain keys: the
   # worldwide-identity columns documented in INVARIANTS.md §2 /
   # Branch (iii) and CROSS-02-00-v3.0.1 §3.2 (sc2egset native
   # toon_id / player_id_worldwide). Bare-match rows (map / patch /
   # version) carry no extra key — represented as the empty tuple.
   NON_TRACKER_GRAIN_KEYS: frozenset[str] = frozenset(
       {"player_id_worldwide", "opponent_player_id_worldwide"}
   )

   # Tracker source-table prefix used for V-8 partitioning.
   TRACKER_SOURCE_TABLE_PREFIX: str = "tracker_events_raw"
   ```

   Place the `import re` statement at the top of the module with the
   other imports (move it to the existing import block at lines
   51–55) rather than inline; keep the constant definitions where
   shown.

2. Add the private helper function after
   `_check_v7_cold_start_vocabulary` (around line 502):

   ```python
   def _check_v8_source_grain_well_formedness(
       skeleton: list[dict[str, Any]],
   ) -> None:
       """V-8: source_grain structural well-formedness + provenance-key consistency.

       For every row, asserts:
           1. ``source_grain`` is a non-empty string.
           2. ``source_grain`` matches the regex
              ``^\\(filename(?:,\\s*[A-Za-z_][A-Za-z0-9_]*)*\\)$``
              (parenthesised tuple beginning with ``filename``,
              optionally followed by comma-separated identifier keys).
           3. If the row's ``source_table_or_event_family`` starts
              with ``"tracker_events_raw"``: every key after
              ``filename`` is in :data:`TRACKER_ATTRIBUTION_KEYS`.
           4. Otherwise (non-tracker row): every key after
              ``filename`` is in :data:`NON_TRACKER_GRAIN_KEYS`.
              The bare ``(filename)`` form (no extra keys) is
              accepted only on non-tracker rows.

       V-8 is NOT a check of CROSS-02-03-v1.0.1 §4.1 D10 (focal/opponent
       symmetry and p0/p1 projection); D10 is deferred to a future V-9
       against the ``per_player_construction`` column.
       """
       for row in skeleton:
           ffid = row["feature_family_id"]
           sg = row["source_grain"]
           src = row.get("source_table_or_event_family", "") or ""

           # 1. Non-empty string.
           assert isinstance(sg, str), (
               f"V-8: row '{ffid}' source_grain is not a string "
               f"(got {type(sg).__name__!r}); expected str"
           )
           assert sg, (
               f"V-8: row '{ffid}' source_grain is empty"
           )

           # 2. Structural regex.
           assert SOURCE_GRAIN_TUPLE_REGEX.match(sg), (
               f"V-8: row '{ffid}' source_grain='{sg}' does not match "
               f"the well-formed tuple pattern "
               f"'(filename[, key1[, key2]])'"
           )

           # Extract keys after 'filename' (strip parens, split, drop 'filename').
           inner = sg.strip("()")
           parts = [p.strip() for p in inner.split(",")]
           # parts[0] is 'filename' by regex; remaining parts are extra keys.
           extra_keys = parts[1:]

           # 3 + 4. Provenance-key consistency.
           is_tracker = src.startswith(TRACKER_SOURCE_TABLE_PREFIX)
           if is_tracker:
               for k in extra_keys:
                   assert k in TRACKER_ATTRIBUTION_KEYS, (
                       f"V-8: tracker row '{ffid}' (source_table_or_event_family="
                       f"'{src}') has source_grain='{sg}' containing key "
                       f"'{k}' not in tracker attribution vocabulary "
                       f"{sorted(TRACKER_ATTRIBUTION_KEYS)}"
                   )
           else:
               for k in extra_keys:
                   assert k in NON_TRACKER_GRAIN_KEYS, (
                       f"V-8: non-tracker row '{ffid}' (source_table_or_event_family="
                       f"'{src}') has source_grain='{sg}' containing key "
                       f"'{k}' not in non-tracker grain-key vocabulary "
                       f"{sorted(NON_TRACKER_GRAIN_KEYS)}"
                   )
   ```

3. Add a call to `_check_v8_source_grain_well_formedness(skeleton)`
   inside `validate_registry_skeleton()`, on the line immediately
   following the existing `_check_v7_cold_start_vocabulary(skeleton)`
   call. Order of public checks after this PR will be: V-1 base,
   V-1 strict, V-2, V-3, V-4, V-5, V-6, V-7, V-8.

4. Update the module docstring "Scope (eight assertions across V-1..V-7
   implemented here):" line to "Scope (nine assertions across V-1..V-8
   implemented here):" and append a `V-8` paragraph:

   ```
       V-8 ``source_grain`` structural well-formedness:
           every row's ``source_grain`` matches the parenthesised
           tuple form ``(filename[, key1[, key2]])``; tracker-event
           rows draw the extra keys from
           ``{playerId, controlPlayerId, killerPlayerId,
              owner_via_unitborn_lineage}``; non-tracker rows draw
           the extra keys from
           ``{player_id_worldwide, opponent_player_id_worldwide}``,
           or use the bare ``(filename)`` form for match-level rows.
           V-8 is NOT spec-D10 (focal/opponent symmetry); D10 is
           deferred.
   ```

   Append matching docstring update to the public
   `validate_registry_skeleton` function: change "Run V-1..V-7
   structural assertions" to "Run V-1..V-8 structural assertions",
   and append a `V-8 source_grain well-formedness.` line in the
   "Check order:" enumeration.

**Verification:**
- `git diff --stat src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
  shows ONLY additions: the three new constants, the new helper, the
  new call site, the import-line `re` addition, and the docstring
  amendments.
- `validate_registry_skeleton(SKELETON, TRACKER_CSV)` on the merged
  26-row skeleton (loaded via the notebook) raises no
  `AssertionError` (deferred to T06; not run in T01 itself).

**File scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`

**Read scope:**
- `reports/specs/02_03_temporal_feature_audit_protocol.md` (D10
  semantics)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`
  (tracker attribution keys)

**Task-specific stop condition:** halt if (a) any of the existing
V-1 base / V-1 strict / V-2..V-7 helpers must be modified to land
V-8 (none should), (b) `_check_v8_source_grain_well_formedness`
causes a public-API-shape change to `validate_registry_skeleton()`
(it must not — same `(skeleton, tracker_csv_path)` signature).

**Validation report shape:** post-edit show diff of
`validate_registry_skeleton.py`; confirm exactly the additions
specified; confirm `_check_v7_cold_start_vocabulary` is unchanged in
signature/body.

**Executor model:** Sonnet (mechanical specification; no methodology
inference required beyond the literal regex + set-membership
checks).

---

### T02 — Parameterize `_row()` test helper to accept `source_grain`

**Objective:** Update the existing `_row()` helper in the test file
to accept an optional `source_grain: str = "(filename, player_id_worldwide)"`
keyword argument. This minimal parameterization unblocks T02b's
V-8-targeted perturbation tests without changing the behavior of
any pre-existing test (the default value preserves the current
hard-coded value at line 56). NO existing fixture row is changed in
this task.

**Instructions:**
1. Edit
   `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`.
2. At the `_row()` helper (lines 40–65), add `source_grain: str =
   "(filename, player_id_worldwide)"` as a keyword-only parameter
   in the signature, AFTER the existing `cold_start_handling`
   parameter.
3. In the dict literal at line 56, change the hard-coded
   `"source_grain": "(filename, player_id_worldwide)",` line to
   `"source_grain": source_grain,`.
4. Do NOT change any existing fixture row. Do NOT change any
   existing test. The pre-existing 30 tests must continue to pass
   unchanged because the default value matches the hard-coded value
   they previously inherited.

**Verification:**
- `git diff tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
  shows ONLY: the new `source_grain` kwarg in `_row()` signature
  and the corresponding dict-literal change.
- `pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py -v`
  passes with all 48 pre-existing tests unchanged (deferred to
  T05; not run in T02 itself).

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`

**Read scope:**
- (none — task is mechanical)

**Task-specific stop condition:** halt if any pre-existing test
fails after this change (it should not — the default preserves
behavior); halt if any existing fixture row is altered (T02 is
purely about the helper signature).

**Validation report shape:** show diff of test file; confirm
exactly two hunks (signature + dict-literal); confirm no fixture
row changed.

**Executor model:** Sonnet (mechanical signature change).

---

### T02b — Add tests for V-8 (with mandatory Step 0 fixture update)

**Objective:** Append eight new tests covering V-8 happy path,
regex-malformed `source_grain` (3 patterns), unknown-tracker-key,
unknown-non-tracker-key, blocked-row-source-grain-still-validates,
non-string-source-grain. Use `copy.deepcopy(valid_skeleton)` for
mutation tests; use `_row()` directly for fresh-row insertion tests.

**Step 0 (REQUIRED FIRST — fixture update analogous to PR #213
F1).** Update the following fixture rows by passing an explicit
`source_grain` kwarg matching the row's `source_table_or_event_family`:

- Row whose `source_table_or_event_family` is
  `"tracker_events_raw.UnitBorn"` (the
  `count_units_built_by_cutoff_loop` row): pass
  `source_grain="(filename, controlPlayerId)"`.
- Row whose `source_table_or_event_family` is
  `"tracker_events_raw.PlayerSetup"` (the
  `slot_identity_consistency` row): pass
  `source_grain="(filename, playerId)"`.
- Row whose `source_table_or_event_family` is
  `"tracker_events_raw.UnitOwnerChange"` (the
  `mind_control_event_count` blocked row): pass
  `source_grain="(filename, playerId)"`.
- Row whose `source_table_or_event_family` is
  `"tracker_events_raw.UnitPositions"` (the
  `army_centroid_at_cutoff_snapshot` blocked row): pass
  `source_grain="(filename, owner_via_unitborn_lineage)"`.
- Row whose `source_table_or_event_family` is
  `"tracker_events_raw.PlayerStats"` (the
  `playerstats_cumulative_economy_fields` blocked row): pass
  `source_grain="(filename, playerId)"`.

The non-tracker rows inherit the default
`(filename, player_id_worldwide)` from the kwarg default — no change
needed.

This Step-0 fixture update is mandatory: as-is, every existing test
that uses `valid_skeleton` (37 of the 39 tests after PR #213) would
fail at the new V-8 step because the fixture's tracker rows
currently inherit a non-tracker grain key (`player_id_worldwide`) by
`_row()` default. Step 0 lifts the tracker rows to
tracker-vocabulary keys.

**Step 1 onwards.** Append the seven V-8 tests:

1. `test_v8_valid_skeleton_passes(valid_skeleton)` — happy path.
2. `test_v8_unparenthesised_source_grain_fails(valid_skeleton)` —
   set one row's `source_grain` to `"filename, playerId"` (no
   parentheses). Expect `AssertionError` matching
   `"V-8.*does not match"`.
3. `test_v8_missing_filename_prefix_fails(valid_skeleton)` —
   set one row's `source_grain` to `"(player_id_worldwide)"`
   (does not start with `filename`). Expect `AssertionError`
   matching `"V-8.*does not match"`.
4. `test_v8_invalid_identifier_key_fails(valid_skeleton)` —
   set one row's `source_grain` to `"(filename, 123player)"`
   (key starts with a digit). Expect `AssertionError` matching
   `"V-8.*does not match"`.
5. `test_v8_unknown_tracker_attribution_key_fails(valid_skeleton)` —
   on the row whose `source_table_or_event_family` is
   `"tracker_events_raw.UnitBorn"`, set
   `source_grain="(filename, ownerPlayerId)"`. Expect
   `AssertionError` matching
   `"V-8.*tracker.*ownerPlayerId.*not in tracker attribution"`.
6. `test_v8_unknown_non_tracker_grain_key_fails(valid_skeleton)` —
   on a non-tracker row, set
   `source_grain="(filename, profile_id)"`. Expect
   `AssertionError` matching
   `"V-8.*non-tracker.*profile_id.*not in non-tracker grain-key"`.
7. `test_v8_non_string_source_grain_fails(valid_skeleton)` —
   set one row's `source_grain` to `12345` (an int). Expect
   `AssertionError` matching `"V-8.*not a string"`.
8. `test_v8_blocked_row_source_grain_still_validates()` — construct
   a fresh skeleton via `_row()` with one row having
   `prediction_setting="blocked_or_deferred"`,
   `status="blocked_until_additional_validation"`,
   `source_table_or_event_family="tracker_events_raw.UnitOwnerChange"`,
   `cold_start_handling="blocked"`, AND
   `source_grain="(filename, playerId)"`. Confirm V-8 passes — i.e.,
   blocked rows do NOT receive a `"blocked"` sentinel on
   `source_grain`; they carry real grain tuples.

Place the new test block after the existing V-7 test block,
beginning with a section divider comment:

```python
# ---------------------------------------------------------------------------
# V-8 source_grain structural well-formedness
# ---------------------------------------------------------------------------
```

**Verification:**
- `pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py -v`
  passes with 48 + 8 = 56 tests (deferred to T05).

**File scope:**
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`

**Read scope:**
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` (post-T01)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`

**Task-specific stop condition:** halt if any test from PR #212 /
PR #213 fails in a way not caused by Step 0 or by V-8; halt if Step
0 is skipped or partially applied.

**Validation report shape:** show diff of test file; confirm 7
tests added + 5 fixture row updates; confirm no test deleted;
confirm the post-T05 coverage report shows the new helper at 100%.

**Executor model:** Sonnet.

---

### T03 — Notebook narrative correction (markdown / comment cells only)

**Objective:** Correct three narrative passages in the merged
notebook .py to (a) acknowledge V-8 has landed; (b) drop "D11" from
the deferred-D-list (already covered by V-7 in PR #213); (c) rename
"D10 (source-grain well-formedness)" out of the deferred list.
Update the print-banner from V-7 to V-8. NO SKELETON literal tuple
is changed.

**Instructions:** Replace the text shown in "Before" with "After"
at each of the four locations. Line numbers refer to the .py file
as it exists on master at `7b26b40f`.

| Location | Before | After |
|----------|--------|-------|
| Lines 143–144 (markdown cell, "Downstream decision" sub-list — multi-line spillover; the D-list begins at line 143 and continues at line 144) | `subsequent PRs may add validation modules D2, D3, D6, D8, D9, D10,\n# D11, D12, D15 and ultimately materialize the registry artifact.` | `subsequent PRs may add validation modules for D2, D3, D6 (full),\n# D8, D9, D10 (focal/opponent symmetry per CROSS-02-03-v1.0.1\n# §4.1), D12, D15 and ultimately materialize the registry\n# artifact.` |
| Line 500 (markdown cell, "Checks NOT YET in scope" — final line of the deferred-D-list block at lines 496–500) | `# dimensions D2/D3/D6/D8/D9/D10/D11/D12/D15.` | `# dimensions D2/D3/D6/D8/D9/D10/D12/D15.` (drop `D11` only; D11 is now covered by V-7. The D10 rename happens at lines 538–539, NOT here — line 500 is just a D-ID list with no parenthetical names.) |
| Lines 538–539 (markdown cell, "Follow-ups" sub-list — multi-line spillover; the `D10 (source-grain` phrase straddles lines 538 and 539) | (existing list calling D10 "source-grain well-formedness") | (V-8 has landed; D10 in spec is focal/opponent symmetry, deferred to V-9 against `per_player_construction`) |
| Line 507 print-banner | `print("validate_registry_skeleton: ALL PASS (V-1 through V-7)")` | `print("validate_registry_skeleton: ALL PASS (V-1 through V-8)")` |

After edits, run `jupytext --sync` to regenerate the paired `.ipynb`.

**Stop conditions and validation** as in PR #213's analogous T03:
halt on any out-of-scope diff, any SKELETON literal change, or any
.ipynb edit not produced by jupytext --sync.

**Executor model:** Sonnet.

---

### T04 — Run pre-commit-equivalent checks (ruff/mypy/jupytext)

Same shape as PR #213's T04. Run ruff + mypy + jupytext --check on
the three modified files (validator + tests + notebook .py). Stop
on any error.

**Executor model:** Sonnet.

---

### T05 — Run pytest with coverage; verify ≥ 95%

`source .venv/bin/activate && poetry run pytest tests/ -v --cov
--cov-report=term-missing | tee coverage.txt`. Confirm 55+ tests
pass; overall coverage ≥ 95%; new helper at 100% on added lines.
Delete `coverage.txt`.

**Executor model:** Sonnet.

---

### T06 — Execute the merged notebook and confirm ALL PASS (V-1 through V-8)

`source .venv/bin/activate && poetry run jupyter nbconvert --to
notebook --execute --inplace --ExecutePreprocessor.timeout=300
sandbox/.../02_01_01_feature_family_registry_skeleton.ipynb`, then
`jupytext --sync`. Confirm output banner reads
`"validate_registry_skeleton: ALL PASS (V-1 through V-8)"`.

**Executor model:** Sonnet.

---

### T07 — Scaffold/code commit (4 files)

Stage exactly:
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
- `sandbox/.../02_01_01_feature_family_registry_skeleton.py`
- `sandbox/.../02_01_01_feature_family_registry_skeleton.ipynb`

Commit message subject: `feat(phase02): SC2EGSet 02_01_01 V-8 source-grain structural well-formedness`

(Body per the planner's commit-template content: V-8 description,
NOT D10 disambiguation, narrative locations, fixture update analogous
to PR #213 F1, spec bindings, deferral framing.)

**Executor model:** Sonnet.

---

### T08 — Release commit (pyproject.toml + CHANGELOG.md)

- `pyproject.toml`: `version = "3.49.0"` → `version = "3.50.0"`.
- `CHANGELOG.md`: roll `[Unreleased]` → `[3.50.0] — 2026-05-09 (PR #N: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness)`; insert fresh `[Unreleased]` block; populate `[3.50.0] ### Added` with V-8 bullet (G-CS-style framing per the planner's template).
- Commit message: `chore(release): bump version to 3.50.0`.

**Executor model:** Sonnet.

---

### T09 — Push, create draft PR, run reviewer-deep, mark ready

1. `git push -u origin phase02/sc2egset-feature-registry-v8-source-grain-well-formedness`.
2. Write PR body to `.github/tmp/pr.txt` per template.
3. `gh pr create --draft --title "feat(phase02): SC2EGSet 02_01_01 V-8 source-grain structural well-formedness" --body-file .github/tmp/pr.txt --base master`.
4. Capture PR number `N`. Substitute `PR #N` into CHANGELOG. Commit `chore(release): substitute PR number in CHANGELOG [3.50.0]`. Push.
5. Append `(PR #N)` to active-plan row in `planning/INDEX.md` (bulk INDEX update happens BEFORE T01 in the docs(planning) commit landing this plan).
6. Dispatch `@reviewer-deep` on the live PR.
7. On PASS / PASS-WITH-NOTES → `gh pr ready N` + cleanup `.github/tmp/`. On BLOCKER → halt and route to reviewer-adversarial only if methodology BLOCKER.

**Executor model:** Sonnet for mechanics; reviewer-deep for the gate.

## Validation gates

(Same shape as PR #213; see Gate Condition above.)

## Release policy

Version 3.49.0 → 3.50.0. Minor (Cat A feat). Single source: `pyproject.toml`. CHANGELOG roll under `[3.50.0] — 2026-05-09 (PR #N: ...)`. Fresh `[Unreleased]` inserted at top.

## Reviewer routing

- **Plan-phase critique:** `reviewer-deep` (per `.claude/rules/data-analysis-lineage.md` line 24 carve-out — same routing as PR #212 / PR #213).
- **Post-execution gate:** `reviewer-deep` at T09.
- **Reviewer-adversarial:** ONLY on methodology BLOCKER from reviewer-deep.

## Non-batching rationale

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule":

1. ROADMAP — PR #211 ✓
2. Scaffold + first validation module — PR #212 ✓
3. Execute + report — PR #212 ✓
4. User review — PR #212 ✓
5. Commit — PR #212 ✓
6. **Next validation module** — PR #213 (V-1 strict + V-7) ✓; *this PR* (V-8) — sequence step 6 is iterative, each "next validation module" is its own PR.
7. Artifacts — deferred (multiple D-dimensions still uncovered).
8. research_log / STEP_STATUS / manifest — deferred.
9. Closing reviewer-deep — deferred.

V-8 is a single validation module per sequence step 6. This PR does NOT bundle artifact generation, status updates, or manifest updates. V-8 is intentionally narrow: it does NOT extend to spec-D10 (symmetry), D3 (relational reconcilability), or D8 (in_game cutoff structural). Each future "next validation module" PR lands one validator at a time.

## Stop conditions

### Pre-implementation stop condition

Working tree must be clean on the freshly-created branch
`phase02/sc2egset-feature-registry-v8-source-grain-well-formedness`
(checked out from `master @ 7b26b40f`); halt if `git status` lists
any modification beyond `planning/current_plan.md`,
`planning/current_plan.critique.md`, `planning/INDEX.md` (which are
landed by the docs(planning) commit before T01).

### Mid-implementation halt triggers

1. Verification computations in §Verification fail when re-run against the on-disk skeleton.
2. Pre-commit hook (ruff/mypy) fails; investigate and fix; create NEW commit (never `--amend`).
3. Pytest fails or coverage falls below 95%.
4. Notebook execution at T06 raises `AssertionError`.
5. `git status` lists any forbidden file.
6. `gh pr create` fails or `git push` is rejected.
7. Reviewer-deep returns methodology BLOCKER → route to reviewer-adversarial.

## Open Questions

None unresolved. Methodology decisions resolved in the plan:

- **Q (user-claim accuracy):** "V-8 = D10 source-grain well-formedness". **Resolved:** D10 in CROSS-02-03-v1.0.1 §4.1 is focal/opponent symmetry, NOT source-grain. V-8 is renamed to "source-grain structural well-formedness" and is explicitly disjoint from spec-D10. Notebook narrative corrected in T03 to fix the D10 misnaming inherited from PR #212.

- **Q (source-grain enum):** "Should V-8 lock a controlled vocabulary on `source_grain`?" **Resolved:** No closed enum exists; `source_grain` carries tuple-of-key-columns expressions. V-8 validates the **shape** (regex match) plus **provenance-key consistency** (tracker keys ⊂ documented attribution-keys vocabulary; non-tracker keys ⊂ documented worldwide-identity-keys vocabulary).

- **Q (blocked-row sentinel):** "Do the 3 carve-out rows carry a `"blocked"` sentinel on `source_grain`?" **Resolved:** No. Live extraction confirms all 3 carry real grain tuples. Sentinels exist on `cold_start_handling`, `model_input_grain`, `target_grain`, `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`, but NOT on `source_grain`. V-8 has no carve-out conjunction and applies the same rule to all 26 rows.

- **Q (PR #213 follow-ups):** Items #4 (defensive-branch coverage on lines 294/362/368) and #5 (`parents[6]` test-infra magic) are out of V-8 scope (see §Out of scope below); item #3 (`_row()` conjunction-discipline reminder docstring) is folded into T02 if convenient; item #6 (plan-frontmatter date semantics) resolved as: `date:` is the plan-authoring date (matches PR #213 convention).

- **Q (which validator is V-9):** Deferred — V-9 candidates: D10 symmetry (`per_player_construction == "symmetric"`), D3 source/model grain reconcilability, D8 in_game cutoff structural. Chosen in the V-9 plan PR.

## Out of scope

- No row-content edits to the 26-row skeleton. Verification confirms all 26 rows already satisfy V-8 by construction.
- No new validation modules beyond V-8.
- No registry CSV / MD artifact under `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
- No edits to `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, the per-dataset `research_log.md`, the cross-game `reports/research_log.md`, the ROADMAP, the locked `02_*` specs, or the notebook regeneration manifest.
- No DuckDB I/O. No tracker-CSV row-content modification.
- No AoE2 work; no thesis chapter prose.
- Step 02_01_01 itself is NOT closed by this PR.
- Test-infra cleanup (`parents[6]` repo-root magic at `tests/.../test_validate_registry_skeleton.py:25`) deferred to a hygiene PR.
- Defensive-branch coverage / `# pragma: no cover` for `validate_registry_skeleton.py` lines 294/362/368 (PR #213 follow-up #4) deferred to a hygiene PR.
- The `_row()` conjunction-discipline reminder docstring (PR #213 follow-up #3) folded into T02 as an optional one-line addition if convenient.
- V-9 (focal/opponent symmetry — actual spec-D10) deferred to a future PR.

## Acceptance criteria

The PR is mergeable when ALL of the following are simultaneously true:

1. **V-8 passes on the unmodified skeleton.** No SKELETON literal tuple changed in `git diff master..HEAD`. Notebook executes ALL PASS through V-8. (Verified: 26/26 regex match; 15/15 tracker keys in-vocab; 9/9 non-tracker keys in-vocab or bare-form; 0 violations.)
2. **Narrative correction visible.** `git diff master..HEAD` for the notebook .py shows the four hunks at lines 144, 500, 507, 539.
3. **Two implementation commits.** `git log master..HEAD --oneline` shows the T07 scaffold/code commit followed by the T08 release commit (and optionally a T09 PR-number-substitution commit). No `--amend`.
4. **No forbidden files in `git diff master..HEAD`.** Diff lists only files from §File Manifest / Allowed.
5. **Coverage ≥ 95%.** `pytest --cov` reports overall ≥ 95%; new V-8 helper shows 100% line coverage on its added lines.
6. **Reviewer-deep verdict is PASS or PASS-WITH-NOTES.** No unresolved methodology BLOCKER. If a BLOCKER is raised, T09 halts and the parent dispatches reviewer-adversarial.
7. **Notebook narrative explicitly distinguishes V-8 from spec-D10.** The replacement text at line 539 must contain a sentence stating that V-8 covers source-grain well-formedness and that spec-D10 is focal/opponent symmetry (deferred to V-9), so future agents do not re-confuse them.
