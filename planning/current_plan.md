---
title: "SC2EGSet Step 02_01_01 — Provisional registry artifact (validated through V-9)"
category: A
branch: phase02/sc2egset-registry-artifact-provisional-v9
date: 2026-05-10
planner_model: claude-opus-4-7
branch_prefix: phase02/
branch_name: phase02/sc2egset-registry-artifact-provisional-v9
pr_title: "feat(phase02): SC2EGSet 02_01_01 provisional registry artifact (validated through V-9)"
base_ref: "master @ 396f162c"
base_commit: 396f162c
head_at_plan_authoring: f20ccd4f
draft_pr_number: 216
draft_pr_url: "https://github.com/tomaszpionka/rts-outcome-prediction/pull/216"
target_version: "3.52.0"
version_current: "3.51.0"
version_bump_type: "minor (Category A feat — first registry artifact)"
created_date: 2026-05-10
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
step_name: "Feature-family registry skeleton (sc2egset)"
lineage_sequence_step: 7
prior_pr_ref: "#215"
invariants_touched: []
reviewer_gate_plan: "BOTH reviewer-deep AND reviewer-adversarial (mandatory)"
reviewer_gate_post_execution: "BOTH reviewer-deep AND reviewer-adversarial (mandatory)"
reviewer_adversarial_required: true
critique_required: true
spec_bindings:
  - CROSS-02-00-v3.0.1
  - CROSS-02-01-v1.0.1
  - CROSS-02-02-v1.0.1
  - CROSS-02-03-v1.0.1
non_batching_lineage_position: "Sequence step 7 — 'Only after all validation modules pass, generate artifacts' under data-analysis-lineage.md §'Non-batching rule for empirical work'. PR #212 delivered scaffold + V-1..V-6; PR #213 added V-1 strict + V-7; PR #214 added V-8; PR #215 added V-9. V-9 is the user-declared stopping point for registry-layer validators in this cycle. THIS PR delivers the FIRST on-disk artifact emitted under the V-9 baseline: ONE versionless CSV + ONE companion MD with a per-row 'block' column. The artifact's claim shape is `validated_through = V-9` only — explicitly NOT a closure of Step 02_01_01, NOT a closure of Pipeline Section 02_01, NOT a closure of Phase 02. Sequence step 8 (research_log / manifest) is included in this PR with non-final status tokens; sequence step 9 (final reviewer-deep + reviewer-adversarial gate) is dispatched at T10."
source_artifacts:
  - sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py
  - src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
  - planning/current_plan.md (PR #215 plan, structural template reuse)
  - planning/current_plan.critique.md (PR #215 reviewer-deep critique)
research_log_ref: "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md (Cat A entry appended in T09 — partial-coverage status; explicitly NOT closure)"
manifest_ref: "thesis/pass2_evidence/notebook_regeneration_manifest.md (row appended in T09 with non-final status token `provisional_through_v9_pending_post_materialization_audit`)"
---

# Plan: SC2EGSet Step 02_01_01 — Provisional registry artifact (validated through V-9)

## Scope

This PR delivers the FIRST on-disk artifact for SC2EGSet Step 02_01_01:
ONE versionless CSV (`02_01_01_feature_family_registry.csv`) and ONE
companion MD (`02_01_01_feature_family_registry.md`) under
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.

The artifact is emitted at `validated_through = V-9` per the V-9 stopping
point declared by the user. It is **provisional**: no further V-N validators
land in this PR; no model-ready feature matrix is claimed; no model training,
splitting, scaler-fit, target encoding, or feature selection is performed.
No feature *value* is computed.

The artifact's load-bearing methodology surface is the verbatim disclaimer
recovered by reviewer-adversarial in the prior cycle (reproduced verbatim in
§Disclaimer text — verbatim below). The disclaimer encodes the per-dimension
deferred-coverage table for D2 / D3 / D4-in_game / D5-in_game / D6-full / D8 /
D9 / D10-sub-2 / D12 / D14 / D15, the explicit non-supersession of
CROSS-02-01-v1.0.1's post-materialization audit, and the explicit
"Step 02_01_01 closure status — partial" claim.

This PR ALSO appends:
- ONE `research_log.md` Category A entry (per CLAUDE.md and
  `.claude/rules/data-analysis-lineage.md` §"Notebook discipline" /
  §"Artifact discipline" — the artifact's lineage must be recorded);
- ONE `notebook_regeneration_manifest.md` row using a non-final status
  token (`provisional_through_v9_pending_post_materialization_audit`),
  added to the manifest's status vocabulary docstring as a NEW token.

This PR DOES NOT touch:
- `STEP_STATUS.yaml` (Step 02_01_01 is NOT closed by this PR — see §5
  adjudication below);
- `PIPELINE_SECTION_STATUS.yaml` (derived from STEP_STATUS — no change);
- `PHASE_STATUS.yaml` (derived from PIPELINE_SECTION_STATUS — no change);
- ROADMAP.md (the existing `continue_predicate` for Step 02_01_01 already
  enumerates a 3-clause conjunction — artifact-check + post-materialization
  audit re-run + per-family §10 verdict — this artifact satisfies clause 1
  only; no ROADMAP edit required);
- `validate_registry_skeleton.py` (validator frozen at V-9; no V-10+);
- `test_validate_registry_skeleton.py` (no new V-N tests);
- any SKELETON_* row literal in the notebook source.

This PR continues lineage sequence step 7 ("artifact generation") per
`.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical
work". Sequence steps 1–6 are complete (PR #212 → #213 → #214 → #215);
this PR adds step 7 (artifact generation) plus partial step 8
(research_log + manifest, with non-final status tokens that explicitly do
not imply closure); step 9 (post-execution gate by BOTH reviewer-deep AND
reviewer-adversarial in parallel) is dispatched at T10.

## Problem Statement

After PR #215 (V-9, merged 2026-05-10 at master `396f162c`),
`validate_registry_skeleton()` enforces V-1 base, V-1 strict, V-2..V-9
across all 26 rows of the merged SKELETON. The 26-row skeleton is in-memory
in the notebook but has never been emitted as a file artifact. Per
`.claude/rules/data-analysis-lineage.md` §"Artifact discipline" and the
non-batching sequence step 7, generating an artifact is the next defensible
move once all validators have passed.

The methodological subtleties this PR must navigate:

**(a) Honest claim shape.** The on-disk artifact must declare
`validated_through = V-9`. It must NOT imply that:
- all 15 CROSS-02-03-v1.0.1 §4.1 audit dimensions D1–D15 are mechanically
  enforced — six dimensions plus partial D6 remain unaddressed at the
  registry-skeleton layer (D2, D3, D4-in_game, D5-in_game, D6-full, D8);
  D9, D15 remain post-materialization / methodology-discipline; D12, D14,
  D10 sub-clause 2 remain N/A for sc2egset;
- Step 02_01_01 is closed — the ROADMAP `continue_predicate` is a
  conjunctive 3-clause gate (artifact-check + CROSS-02-01-v1.0.1
  post-materialization audit re-run + per-family CROSS-02-03-v1.0.1 §10
  verdict). This artifact satisfies clause 1 only; clauses 2 and 3 require
  at least one materialization step;
- Pipeline Section 02_01 or Phase 02 is closed — both derive from
  STEP_STATUS, which this PR does not touch.

**(b) Non-supersession of CROSS-02-01-v1.0.1.** Per
CROSS-02-03-v1.0.1 §1.3, the design-time and post-materialization audits
are complementary, not redundant. The artifact's `validated_through = V-9`
status does NOT excuse a future materialized column from
CROSS-02-01-v1.0.1's post-materialization audit gate. The disclaimer
states this explicitly.

**(c) Status-YAML touch decision (THE LOAD-BEARING METHODOLOGY DECISION).**
Schema inspection of STEP_STATUS.yaml (file lines 1–11 + lines 17–195)
shows:
- the file has only one declared status vocabulary (`complete` with
  `completed_at` timestamps; no `started_at` is documented as required for
  steps to register, although several Phase 01 steps DO carry an
  `started_at` field — see lines 110–121);
- there is no documented "in_progress" or "partial" token in the file's
  comment block. The comment block (lines 1–12) defines the file's
  derivation chain but not its allowed statuses for individual steps;
- the file's authority is "if this file disagrees with the ROADMAP,
  this file is wrong" — i.e., status flips here must reflect ROADMAP
  reality.

PIPELINE_SECTION_STATUS.yaml header (lines 1–22) explicitly enumerates
three statuses for pipeline sections: `complete | in_progress | not_started`,
with `in_progress` defined as "ANY step is in_progress or complete".
PHASE_STATUS.yaml header (lines 1–11) defines the same three statuses for
phases.

**Decision:** No-touch on STEP_STATUS / PIPELINE_SECTION_STATUS /
PHASE_STATUS in this PR. Justification:
1. The ROADMAP `continue_predicate` for Step 02_01_01 is conjunctive
   (3-clause); this artifact satisfies clause 1 only; flipping STEP_STATUS
   to `complete` would lie about closure.
2. `in_progress` is a pipeline-section / phase status (not documented as a
   per-step status in STEP_STATUS.yaml comments); inferring its meaning at
   the per-step layer would require a methodology-justifying comment edit
   that exceeds the scope of an artifact PR.
3. Pipeline Section 02_01's status is *derived from* STEP_STATUS per the
   PIPELINE_SECTION_STATUS comment chain (lines 6–13). The derivation rule
   "ANY step is in_progress or complete" → `in_progress` would only fire
   if a step were marked `in_progress`. Currently no Phase 02 step has
   ever been marked anything in STEP_STATUS (not even an empty entry —
   STEP_STATUS.yaml ends at row `01_06_04` line 195). Adding a new
   per-step status here is a methodology-load-bearing change that should
   land with the closure PR, not this artifact PR.
4. Lineage of "artifact landed" is recorded in (i) the artifact MD itself
   ("Step 02_01_01 closure status — partial"), (ii) the research_log
   entry, and (iii) the manifest row — all of which are honest about
   partial coverage. STEP_STATUS no-touch is the safer default.

**(d) Vocabulary extension for the manifest.** The manifest's status
vocabulary docstring (lines 8–13 of
`thesis/pass2_evidence/notebook_regeneration_manifest.md`) currently lists:
`confirmed_intact | not_yet_assessed | flagged_stale |
regenerated_pending_log | phase_blocked`. None of these correctly
characterizes a freshly emitted Phase 02 partial-coverage artifact:
- `confirmed_intact` is forbidden by the docstring's own rule
  (line 9): "Reaching this status from `flagged_stale` requires the FULL
  repair lineage to have landed; do NOT promote a Step to
  `confirmed_intact` immediately after artifact regeneration." The
  spirit of that rule applies to first-emission as well.
- `phase_blocked` was for Phase 02+ notebooks not yet executed; this
  notebook IS executed.
- `not_yet_assessed` understates that the artifact has a defined V-1..V-9
  coverage scope.

T09 extends the manifest's status vocabulary docstring (lines 8–13) by
adding a NEW token: `provisional_through_v9_pending_post_materialization_audit`.
The token's docstring sentence is:
*"`provisional_through_v9_pending_post_materialization_audit` — artifact
emitted at validated_through=V-9 baseline per the registry-skeleton layer
of CROSS-02-03-v1.0.1; BOTH the CROSS-02-01-v1.0.1 post-materialization
audit re-run AND the per-family CROSS-02-03-v1.0.1 §10 verdict for every
registry row remain unsatisfied; Step closure remains deferred."* The new token is added in alphabetical position immediately
before `regenerated_pending_log`. The manifest row uses this new token.

## Assumptions & Unknowns

**Assumptions** (declared explicit so the executor can halt if any becomes
false during T01–T11):

1. The merged 26-row SKELETON in the notebook has not been modified since
   PR #215 (master `396f162c`); `validate_registry_skeleton()` returns
   None (no AssertionError) when called on `(SKELETON, TRACKER_CSV)`.
   Verified live by the planner against current branch HEAD (`f20ccd4f` =
   master + empty bootstrap commit; no .py edits yet).
2. Pyproject.toml line 3 reads `version = "3.51.0"` at branch HEAD; T08
   mechanically bumps to `"3.52.0"`. CHANGELOG `[Unreleased]` block is
   empty after PR #215's roll-up (verified by inspection of CHANGELOG.md
   lines 12–20).
3. The artifact CSV has one row per SKELETON row (26 rows total) plus a
   `block` column identifying source partition (one of:
   `pre_game | history_enriched_pre_game | in_game_now | in_game_caveat |
   gate_and_blocked`). The CSV's data columns are exactly the 13
   `REQUIRED_COLUMNS` from `validate_registry_skeleton.REQUIRED_COLUMNS`
   plus the `block` column appended at position 14 (last column). Total:
   14 columns, 26 rows.
4. Bidirectional notebook ↔ ipynb sync remains via `jupytext.toml` at
   `sandbox/jupytext.toml` (per memory `project_jupytext_location`).
   `jupytext --sync` round-trips cleanly after the new artifact-export
   cell is added.
5. The artifact MD is authored from a single in-notebook string template
   (no separate write step); the notebook writes both CSV and MD from
   the same lineage. Re-running the notebook produces byte-identical
   CSV + MD (idempotency).
6. The disclaimer text (supplied by parent, recovered from JSONL line
   1111, 912 words) is single-source-of-truth for the per-dimension
   deferred-coverage table. The artifact MD body contains the table
   verbatim; no paraphrase.
7. Encoding choice for the disclaimer: plain `<` / `>` (option B from
   parent's note) for cleaner GitHub markdown rendering. The disclaimer
   text below in §"Disclaimer text — verbatim" uses plain `<` / `>`;
   T02 uses this exact text. Both encodings are semantically equivalent
   on GitHub; option B is chosen for cleaner side-by-side rendering and
   easier code-review diff inspection.
8. The post-execution gate dispatches BOTH reviewer-deep AND
   reviewer-adversarial in parallel (per §9) — neither is a "primary"
   reviewer; both must return PASS or PASS-WITH-NOTES (or
   APPROVE-WITH-CONDITIONS for adversarial) for merge eligibility.
9. The 3-round adversarial cap (per memory `feedback_adversarial_cap_execution`)
   applies symmetrically across plan-side and execution-side review for
   this artifact PR.
10. The empty bootstrap commit `f20ccd4f` on the current branch already
    seeded draft PR #216; the planning commit (T00) is the FIRST real
    commit on this branch.

**Unknowns** (must NOT block T01; surfaced for executor awareness):

1. Whether reviewer-adversarial at T10 raises an unanticipated
   methodology BLOCKER on the artifact's claim shape. If so, the
   resolution path is documented in §Stop conditions and §Reviewer
   routing.
2. Whether the manifest vocabulary extension
   (`provisional_through_v9_pending_post_materialization_audit`) draws
   reviewer pushback that the token is too verbose. The fallback name
   (NOT used in T01–T09 unless reviewer mandates) is `partial_coverage_v9_baseline`,
   which is the parent's first-suggested alternative. The verbose name
   is preferred because it encodes the unmet predicate explicitly.
3. Whether the artifact MD's ordering of sections matches reviewer
   expectations. The chosen order (T02): YAML frontmatter → H1 → top-of-document
   coverage status disclaimer (verbatim) → provenance / run-metadata
   block → V-1..V-9 mapping table (also in disclaimer) → CSV preview /
   row-count summary → "How to regenerate" notebook command → §References
   to upstream specs.

## Literature Context

- **`.claude/rules/data-analysis-lineage.md`** §"Non-batching rule for
  empirical work" sequence step 7: *"Only after all validation modules
  pass, generate artifacts."* — V-9 is the user-declared stopping point
  for registry-layer validators; sequence step 7 is now defensible.
- **`.claude/rules/data-analysis-lineage.md`** §"Artifact discipline":
  *"A generated artifact may be cited as evidence only after: (1) the
  upstream notebook/script assumptions were reviewed; (2) the sanity
  checks passed; (3) the falsifier did not fail; (4) the artifact was
  generated from the reviewed notebook/script; (5) the lineage was
  recorded in the appropriate research_log / STEP_STATUS / manifest path."*
  — this PR satisfies (1)–(4) via PR #212/#213/#214/#215 reviewed
  history; satisfies (5) partially via research_log + manifest (NOT
  STEP_STATUS, per §Problem Statement adjudication).
- **CROSS-02-03-v1.0.1 §1.3 non-supersession clause**
  (`reports/specs/02_03_temporal_feature_audit_protocol.md` lines 61–78):
  *"CROSS-02-03 does not replace CROSS-02-01-v1.0.1. The two specs are
  complementary, not redundant... CROSS-02-03 audits definitions;
  CROSS-02-01-v1.0.1 audits materialized columns. Both gates are
  mandatory."* — verbatim binding for the artifact disclaimer's
  non-supersession section.
- **CROSS-02-03-v1.0.1 §4.1 D1–D15** — the audit dimension list whose
  per-dimension coverage status the disclaimer table reports.
- **CROSS-02-01-v1.0.1 §2** (`reports/specs/02_01_leakage_audit_protocol.md`
  lines 44–106): cutoff structural check, POST-GAME token absence,
  normalization fit-scope, reference-window assertion — the four checks
  that the post-materialization audit will run on materialized columns
  (the gate the artifact disclaimer commits to NOT superseding).
- **ROADMAP Step 02_01_01 `continue_predicate`** (lines 2060–2066 of
  `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`):
  *"A future PR may begin Step 02_01_02 (or the next 02_01 step in the
  ROADMAP) only after this Step 02_01_01 has reached its CSV + MD
  artifact-check at a future PR, the CROSS-02-01-v1.0.1
  post-materialization audit gate has been re-run for any feature column
  the registry triggers materialization of, and a per-family
  CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row."*
  — this artifact satisfies clause 1 ("CSV + MD artifact-check") but
  NOT clauses 2 or 3.
- **PR #212** (merged 2026-05-08 at master `18d30a81`): scaffold +
  V-1..V-6.
- **PR #213** (merged 2026-05-09 at master `7b26b40f`): V-1 strict + V-7.
- **PR #214** (merged 2026-05-10 at master `664c869a`): V-8.
- **PR #215** (merged 2026-05-10 at master `396f162c`): V-9 — the
  validator stopping point for this cycle; reviewer-deep PASS (no
  reviewer-adversarial escalation triggered).
- **`thesis/pass2_evidence/notebook_regeneration_manifest.md`** — the
  manifest whose status vocabulary the artifact PR extends with
  `provisional_through_v9_pending_post_materialization_audit`.

**Coverage matrix at artifact emission (from V-9 baseline, mirrored
from PR #215 plan §Literature Context):**

| Dim | Title | Status at emission | Where artifact reports |
|---|---|---|---|
| D1 | Prediction setting admissibility | covered (V-1) | disclaimer V-1 row |
| D2 | Source classification + temporal availability | NOT covered (deferred) | disclaimer table D2 row |
| D3 | Source grain vs model grain | NOT covered (deferred) | disclaimer table D3 row |
| D4 | Temporal anchor correctness | history side covered (V-6); in_game side deferred | disclaimer table D4-in_game row |
| D5 | Cutoff operator correctness | history side covered (V-6); in_game side deferred | disclaimer table D5-in_game row |
| D6 | Target-game exclusion | partially covered (V-6 strict-`<` + post-outcome tokens, history side); in_game / full-replay side deferred | disclaimer table D6-full row |
| D7 | Post-game token exclusion | covered (V-6 token list) | disclaimer V-6 row |
| D8 | Full-replay aggregate exclusion (in-game) | NOT covered (deferred) | disclaimer table D8 row |
| D9 | Normalization fit-scope | post-materialization-only | disclaimer table D9 row |
| D10 | Focal/opponent symmetry sub-clause 1 | covered (V-9) | disclaimer V-9 row + table |
| D10 sub-clause 2 | aoestats canonical_slot p0/p1 | N/A for sc2egset | disclaimer table D10-sub-2 row |
| D11 | Cold-start vocabulary, no magic numbers | covered (V-7) | disclaimer V-7 row |
| D12 | Source-mode label discipline | N/A for sc2egset | disclaimer table D12 row |
| D13 | SC2 tracker eligibility | covered (V-2/V-3/V-4/V-5) | disclaimer V-2..V-5 rows |
| D14 | AoE2 source-label discipline | N/A for sc2egset | disclaimer table D14 row |
| D15 | Artifact-lineage readiness | methodological discipline | disclaimer V-1 row + table D15 row |

After this PR: the artifact is on disk; D2 / D3 / D4-in_game / D5-in_game /
D6-full / D8 remain unaddressed at the registry-skeleton layer; D9 / D15
remain post-materialization-only; D10 sub-clause 2 / D12 / D14 remain N/A
for sc2egset. **Step 02_01_01 closure remains NOT in scope** — at least
one materialization step (02_01_02 or successor) plus CROSS-02-01-v1.0.1
post-materialization audit and per-family CROSS-02-03-v1.0.1 §10 verdicts
must land before closure is defensible.

## Gate Condition

This PR is mergeable to master when ALL the following are simultaneously
true (mirrored in §Acceptance criteria):

1. `git diff master..HEAD --name-only` lists EXACTLY the files in the
   §File Manifest / Allowed table; no forbidden file appears.
2. Both new artifact files exist:
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
   - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md`
3. The artifact CSV has exactly 26 data rows + 1 header row = 27 lines
   total; 14 columns (13 REQUIRED_COLUMNS + 1 `block` column appended
   last).
4. The artifact MD contains the verbatim disclaimer text from §"Disclaimer
   text — verbatim" (modulo encoding option B: plain `<` / `>`); diff
   tool comparison MUST show no semantic difference. Per-dimension table
   contains all rows from the disclaimer.
5. The artifact MD contains a provenance / run-metadata block with:
   notebook execution timestamp (ISO YYYY-MM-DD per memory
   `feedback_iso_date_format`), git SHA at execution, validator version
   string `V-1..V-9` (from validator module docstring), Python version,
   poetry version, notebook path, regeneration command.
6. The notebook's print banner reads
   `"validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emitted"`
   in the executed cell output.
7. Notebook regenerates the artifact deterministically: re-running
   `jupyter nbconvert --to notebook --execute --inplace` produces
   byte-identical CSV and MD (no timestamp drift in the file content;
   provenance block uses a stable rule — execution timestamp lives in a
   `manifest.json`-style field that is NOT in the file or is itself
   captured at PR-merge time, NOT each notebook run; resolved in T01
   by writing the `git_sha`, `python_version`, and `executed_at`
   fields to the MD only on the FIRST emission and treating subsequent
   re-runs as idempotent — see T01 §Instructions).
8. `pytest tests/ -v --cov` passes with overall coverage ≥ 95%; the
   validator module's per-file coverage stays ≥ 95% (no validator code
   changed).
9. `ruff check`, `mypy`, `jupytext --check` all clean.
10. The 26 SKELETON rows in the notebook .py are byte-identical to
    master `396f162c` (no row literal modified).
11. STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml,
    ROADMAP.md, INVARIANTS.md, all `02_*` specs, and
    `validate_registry_skeleton.py` + its tests are all unchanged.
12. `pyproject.toml` shows `version = "3.52.0"`; `CHANGELOG.md` has a
    `[3.52.0] — 2026-05-10` block with the actual PR number `N`
    substituted (no `PR #TBD` remaining).
13. `research_log.md` has a new Cat A entry dated 2026-05-10 with no
    closure language.
14. `notebook_regeneration_manifest.md` has the new
    `provisional_through_v9_pending_post_materialization_audit` token in
    the status vocabulary docstring AND a manifest row for the notebook
    using that token.
15. **BOTH** reviewer-deep AND reviewer-adversarial at T10 return
    `PASS` / `PASS-WITH-NOTES` (or `APPROVE-WITH-CONDITIONS` for
    adversarial). Either reviewer returning a `BLOCKER` halts the PR;
    the resolution path is in §Stop conditions.

## File Manifest

### Allowed (this PR may touch only these)

| File | Action | Touch type | Commit |
|------|--------|-----------|--------|
| `planning/current_plan.md` | Rewrite | rewrite (this plan, authored before T01 fires) | docs(planning) — already on branch when execution starts (T00) |
| `planning/current_plan.critique.md` | Rewrite | rewrite (TWO critiques: reviewer-deep AND reviewer-adversarial, each in its own H1 section) | docs(planning) (T00) |
| `planning/INDEX.md` | Update | (a) at T00: append archive row for PR #215 with merge commit `396f162c` and merge date 2026-05-10; update active row to `phase02/sc2egset-registry-artifact-provisional-v9` (2026-05-10) — first artifact for Step 02_01_01; (b) at T11: append `(PR #N)` to the active row | docs(planning) (T00 + T11) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` | Create | CSV emitted by notebook from `SKELETON` lineage; 26 rows × 14 cols (13 REQUIRED_COLUMNS + `block`); UTF-8 + LF newlines + Unix line endings | feat (T07 artifact commit) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md` | Create | MD authored by notebook from in-notebook string template; contains verbatim disclaimer (option B encoding), per-dimension table, provenance block, V-1..V-9 mapping, regeneration command, references | feat (T07 artifact commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` | Update | (a) add new "## Artifact emission" markdown cell with anchor "validated_through=V-9 baseline"; (b) add new code cell that creates `ARTIFACTS_DIR` (idempotent `Path.mkdir(parents=True, exist_ok=True)`), writes the CSV via `csv.DictWriter` from `SKELETON` + `block` column, writes the MD via in-notebook string template (verbatim disclaimer + provenance + tables); (c) update print banner from `"ALL PASS (V-1 through V-9)"` to `"ALL PASS (V-1 through V-9); artifact emitted"`; (d) update Conclusion §Artifacts produced from "**None.**" to a paragraph that honestly states the partial-coverage emission and points to the artifact paths (no claim of closure, no claim of model-readiness); (e) update Conclusion §Status / log / manifest updates to honestly state the research_log + manifest updates and the explicit STEP_STATUS no-touch decision; (f) update Conclusion §Follow-ups to remove the obsolete "After all validation modules pass on review, materialize the registry CSV / MD artifact" bullet (now done) and add new bullets enumerating the still-open work (D2/D3/D4-in_game/D5-in_game/D6-full/D8 and the 3-clause continue_predicate) | feat (T07 artifact commit) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` | Update | regenerated by `jupytext --sync` after .py edit; commit alongside paired .py | feat (T07 artifact commit) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` | Update | append ONE Cat A entry dated 2026-05-10 titled "[Phase 02 / Step 02_01_01] Provisional registry artifact (validated through V-9)"; entry uses the standard schema (What / Why / How / Findings / What this means / Decisions taken / Decisions deferred / Acknowledged trade-offs / Thesis mapping); explicitly states `closure_status = partial`; cites artifact paths; cites the 3-clause `continue_predicate`; explicitly states STEP_STATUS no-touch and rationale | feat (T09 lineage commit) |
| `thesis/pass2_evidence/notebook_regeneration_manifest.md` | Update | (a) extend status vocabulary docstring (lines 8–13) with the new token `provisional_through_v9_pending_post_materialization_audit` in alphabetical position immediately before `regenerated_pending_log`; (b) add ONE manifest row for `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` under "## sc2egset — Phase 02 notebooks" (a NEW section header may need to be added — verify; if section absent, insert it after the existing "## sc2egset — Phase 01 notebooks" section); manifest row uses the new token | feat (T09 lineage commit) |
| `pyproject.toml` | Update | bump `version = "3.51.0"` → `version = "3.52.0"` | chore(release) (T08 commit) |
| `CHANGELOG.md` | Update | roll `[Unreleased]` → `[3.52.0] — 2026-05-10 (PR #N: phase02/sc2egset-registry-artifact-provisional-v9)`; insert empty `[Unreleased]` block; populate `[3.52.0]` Added with provisional-artifact bullet that explicitly says "validated_through=V-9; closure NOT claimed; STEP_STATUS untouched; CROSS-02-01-v1.0.1 post-materialization audit still mandatory" | chore(release) (T08 commit); PR-number substitution post-create |
| `.github/tmp/commit.txt` | Create | scratch (created and removed within session per memory `feedback_git_commit_format`; not committed) | not committed |
| `.github/tmp/pr.txt` | Create | scratch (created, used by `gh pr create --body-file`, removed after PR is created per memory `feedback_pr_body_cleanup`; not committed) | not committed |

### Forbidden (executor must HALT if `git status` lists any of these)

| Forbidden path | Reason |
|----------------|--------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` | Step 02_01_01 NOT closed; ROADMAP `continue_predicate` 3-clause unmet (clauses 2 + 3 deferred). Adjudication in §Problem Statement (c). |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` | Derived from STEP_STATUS; no change there → no change here. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` | Derived from PIPELINE_SECTION_STATUS; no change there → no change here. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | The ROADMAP `continue_predicate` already enumerates the 3-clause conjunction; no edit required for honest partial-coverage framing. The artifact MD does that framing instead. |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` | No invariant change. |
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` | Validator FROZEN at V-9; no V-10+ work in this cycle. |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` | No new V-N tests; validator frozen. |
| Any literal SKELETON_PRE_GAME / SKELETON_HISTORY / SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT / SKELETON_GATE_AND_BLOCKED row tuple in the notebook .py | Skeleton row content is locked from PR #212 and validated through V-9. |
| `tracker_events_feature_eligibility.csv` | Upstream evidence; must NOT be modified. |
| `reports/specs/02_00_feature_input_contract.md` | Locked spec — read-only. |
| `reports/specs/02_01_leakage_audit_protocol.md` | Locked spec — read-only. |
| `reports/specs/02_02_feature_engineering_plan.md` | Locked spec — read-only. |
| `reports/specs/02_03_temporal_feature_audit_protocol.md` | Locked spec — read-only. |
| `reports/specs/02_*.md` (all) | Locked specs — read-only. |
| `reports/research_log.md` | Cross-game (CROSS) research log entry deferred; this is dataset-scoped artifact — entry goes in dataset-scoped `research_log.md` only. |
| `thesis/chapters/**` | No thesis prose in this PR. |
| `thesis/WRITING_STATUS.md` | No section status flips. |
| `thesis/chapters/REVIEW_QUEUE.md` | No Pass-2 entries from this PR. |
| `src/rts_predict/games/aoe2/**` | No AoE2 work in this PR. |
| `data/**`, `**/data/**` | No raw / staging / db edits. |
| `docs/**` | No taxonomy / spec / methodology / agent-doc edits. |
| `.claude/**` | No agent / rule / invariant edits. |
| `pyproject.toml`, `CHANGELOG.md` **during T01–T07** | These are §Allowed only at T08 (release commit). Executor must HALT if either appears in `git status` while T01–T07 are running. |
| `planning/current_plan.md`, `planning/current_plan.critique.md` **during T07–T11** | These already exist on the branch from earlier docs(planning) commits and must NOT appear in the T07 (artifact) / T08 (release) / T09 (lineage) staged sets. |

## Verification before finalizing this plan (executed read-only by the planner)

1. **Master HEAD and PR #215 merge confirmation.** `git log --oneline
   master -5` confirms `396f162c feat(phase02): SC2EGSet 02_01_01 V-9
   per-player construction / focal-opponent symmetry (spec-D10) (#215)`.
   Master HEAD = `396f162c` as of 2026-05-10.
2. **Current branch and bootstrap commit.** `git branch --show-current` =
   `phase02/sc2egset-registry-artifact-provisional-v9`. Branch HEAD =
   `f20ccd4f chore(pr): bootstrap draft PR for provisional SC2EGSet
   registry artifact`. `git diff master..HEAD --name-only` = empty (the
   bootstrap commit is empty).
3. **Pyproject.toml version.** Line 3 reads `version = "3.51.0"`.
4. **CHANGELOG `[Unreleased]` empty.** Lines 12–20 confirm empty Added /
   Changed / Fixed / Removed.
5. **STEP_STATUS.yaml schema check.** File comments lines 1–11 establish
   the derivation chain (this file → PIPELINE_SECTION_STATUS →
   PHASE_STATUS) and the authority rule "if this file disagrees with
   the ROADMAP, this file is wrong." The file does not enumerate
   per-step status vocabulary in its own comments; per-step entries
   carry only `status: complete` + `completed_at` (lines 17–195). No
   Phase 02 step entry exists yet. **Decision in §Problem Statement (c)
   is no-touch.**
6. **PIPELINE_SECTION_STATUS.yaml schema check.** Lines 1–22 enumerate
   `complete | in_progress | not_started` for pipeline sections,
   derived from steps.
7. **PHASE_STATUS.yaml schema check.** Lines 1–11 enumerate
   `complete | in_progress | not_started` for phases, derived from
   pipeline sections.
8. **ROADMAP `continue_predicate` reads.** Lines 2060–2066: the
   conjunctive 3-clause predicate (artifact-check + post-materialization
   audit re-run + per-family §10 verdict). This artifact satisfies
   clause 1 only.
9. **CROSS-02-03-v1.0.1 §1.3 non-supersession clause text.** Lines
   61–78 read verbatim per §Literature Context above. The disclaimer's
   non-supersession section uses identical phrasing.
10. **Manifest status vocabulary.** Lines 8–13 list five tokens: none
    correctly characterizes a freshly emitted partial-coverage Phase 02
    artifact. New token addition justified in §Problem Statement (d).
11. **Notebook artifact-export feasibility.** Notebook lines 56–73
    already establish `TRACKER_CSV` via `get_reports_dir(...)`;
    `ARTIFACTS_DIR` follows the same pattern with mkdir-on-create.
    Notebook conventions (per memory `feedback_notebook_print_vs_logger`)
    use `print()` for data exploration; the artifact-emission cell will
    `print()` row counts and file paths after writing for cell-output
    reproducibility.
12. **Disclaimer text completeness check.** The verbatim disclaimer
    (912 words, supplied by parent) covers all five required elements:
    (i) §"What V-1..V-9 mechanically enforce on this artifact" + V-N
    table; (ii) §"What V-1..V-9 do NOT enforce — deferred dimensions"
    + per-dimension table for D2 / D3 / D4-in_game / D5-in_game /
    D6-full / D8 / D9 / D10-sub-2 / D12 / D14 / D15; (iii)
    §"Non-supersession of the post-materialization audit"; (iv)
    §"Step 02_01_01 closure status — partial"; (v) §"Commitment path
    for resolving deferred dimensions before thesis defense". Text
    spot-checked against the parent's supplied verbatim block —
    identical modulo HTML entity decoding.
13. **JSONL encoding choice.** Plain `<` / `>` (option B) chosen for
    cleaner GitHub markdown rendering and easier code-review diff
    inspection. Both options are functionally identical on GitHub.
14. **Branch hygiene check.** Memory `feedback_no_branches_without_approval`
    — the branch was already created by parent and pushed; no new
    branch creation in this PR.
15. **Reviewer-routing precedent check.** PR #215 ran reviewer-deep
    only (per `.claude/rules/data-analysis-lineage.md` line 24 Phase
    02 carve-out). This artifact PR is methodology-load-bearing
    (the disclaimer is the load-bearing artifact); BOTH reviewer-deep
    AND reviewer-adversarial are mandatory at both plan and execution
    gates per the user's instruction.

## Disclaimer text — verbatim (for inclusion in artifact MD at T02)

The artifact MD at
`src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md`
MUST contain the following text VERBATIM as its top-of-document section
(immediately under the H1 title, before the provenance block). Encoding
choice: plain `<` / `>` (option B) for cleaner GitHub markdown render.
T02 is forbidden to paraphrase; any deviation must be approved by
reviewer-adversarial at T10.

```
## Coverage status — provisional registry artifact

This registry artifact is emitted at `validated_through = V-9` per
`reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1).
It is **provisional**: not all 15 design-time audit dimensions (D1–D15) of
CROSS-02-03-v1.0.1 §4 are mechanically enforced at the registry-skeleton
layer. Coverage is as follows.

### What V-1..V-9 mechanically enforce on this artifact

The validation module `validate_registry_skeleton()` in
`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
runs ten checks (V-1 base, V-1 strict, V-2..V-9) on every row of the registry.
Each check is a structural gate; failure on any row halts artifact regeneration.

| V-N | What it asserts | Maps to CROSS-02-03 dimension |
|-----|-----------------|-------------------------------|
| V-1 | Required-column presence (13-column schema) | D1 (admissibility), D15 (lineage readiness) |
| V-1 strict | Controlled vocabulary on `prediction_setting` | D1 |
| V-2..V-5 | SC2 tracker eligibility CSV cross-reference | D13 |
| V-6 | History cutoff is `history_time < target_time` strict; post-game-token list excluded | D5 (history side), D6 (target-game exclusion, history side), D7 |
| V-7 | Cold-start vocabulary + status-gated sentinel; no magic numbers | D11 |
| V-8 | Source-grain structural well-formedness + provenance-key consistency | (orthogonal to D8 — see below) |
| V-9 | `per_player_construction` controlled vocabulary; status-gated `"blocked"` sentinel; admits `"symmetric"` only on model-input rows | D10 sub-clause 1 (Invariant I5 symmetry) |

V-9 admits exactly one non-blocked token (`"symmetric"`). It is a
**structural guard against future drift**, not a violation detector against
the current 26-row skeleton — the spec authors already encoded `"symmetric"`
on every model-input row before V-9 was implemented. V-9's load-bearing
guarantee is that any future PR adding a row with
`per_player_construction != "symmetric"` (on a model-input row) is
mechanically blocked at the registry layer.

### What V-1..V-9 do NOT enforce — deferred dimensions

The following CROSS-02-03 dimensions are NOT mechanically enforced on this
artifact at the registry-skeleton layer. Each carries an explicit
commitment path for resolution before the thesis defense.

| Dim | Title | Status here | Commitment path |
|-----|-------|-------------|-----------------|
| D2 | Source classification + temporal availability | NOT mechanically enforced; declared per-row via `source_table_or_event_family` literal + manual cross-check against CROSS-02-00-v3.0.1 §5 column classification | Resolved at materialization step 02_01_02 via manual lineage review + post-materialization audit (CROSS-02-01-v1.0.1 §2.2 POST-GAME token absence check, AST-walk or docstring trace) |
| D3 | Source grain vs model grain | NOT mechanically enforced; declared per-row via `source_grain` + `model_input_grain` literals | Resolved at materialization step 02_01_02 via projection SQL review |
| D4 (in-game side) | Temporal anchor correctness for in-game features | NOT mechanically enforced beyond V-6's history-side check; in-game side relies on row-literal `temporal_anchor = "event.loop"` | Resolved at materialization via CROSS-02-01-v1.0.1 §2.1 cutoff structural check |
| D5 (in-game side) | Cutoff operator correctness for in-game features | NOT mechanically enforced beyond V-6's history-side check; in-game side relies on row-literal `allowed_cutoff_rule = "event.loop <= cutoff_loop"` | Resolved at materialization via CROSS-02-01-v1.0.1 §2.1 |
| D6 (full) | Target-game exclusion | partially enforced (V-6 strict-`<` for history; in-game / full-replay side relies on row-literal allowed_cutoff_rule) | Resolved at materialization via CROSS-02-01-v1.0.1 §2.2 + tracker eligibility CSV `full_replay_min_loop_blocked` per-row |
| D8 | Full-replay aggregate exclusion (in-game snapshots) | NOT mechanically enforced at registry layer; relies on row-literal `allowed_cutoff_rule` + tracker eligibility CSV per-row caveats | Resolved at materialization via post-materialization audit; for SC2, additional gate is the tracker eligibility CSV row's `upstream_verdicts` cell, which records the `full_replay_min_loop_blocked=True` verdict for V-7 time-to-first-event families |
| D9 | Normalization fit-scope | post-materialization-only per CROSS-02-03-v1.0.1 §4.1 | CROSS-02-01-v1.0.1 §2.3 post-materialization audit |
| D10 sub-clause 2 | aoestats `canonical_slot` p0/p1 projection | N/A for sc2egset (no `canonical_slot` column on sc2egset MHM per CROSS-02-00-v3.0.1 §5.1) | aoestats-side V-N PR (separate dataset) |
| D12 | Source-mode label discipline | N/A for sc2egset (no source-mode column) | N/A |
| D14 | AoE2 source-label discipline | N/A for sc2egset | N/A |
| D15 | Artifact-lineage readiness | methodology-discipline, asserted by lineage chain not by row check | Lineage rule `.claude/rules/data-analysis-lineage.md` |

### Non-supersession of the post-materialization audit

This registry artifact does NOT replace, weaken, or amend
CROSS-02-01-v1.0.1's post-materialization leakage audit gate. Per
CROSS-02-03-v1.0.1 §1.3, the design-time and post-materialization audits
are complementary, not redundant. Every feature column that this registry
triggers materialization of must additionally pass CROSS-02-01-v1.0.1's
audit before any consuming Pipeline Section may exit. The registry's
`validated_through = V-9` status does NOT excuse a materialized column
from CROSS-02-01-v1.0.1.

### Step 02_01_01 closure status — partial

This artifact satisfies clause 1 of the ROADMAP `continue_predicate` for
Step 02_01_01 ("CSV + MD artifact-check"). It does NOT satisfy clauses 2
or 3 ("CROSS-02-01-v1.0.1 post-materialization audit re-run for any
feature column the registry triggers materialization of"; "per-family
CROSS-02-03-v1.0.1 §10 verdict recorded for every registry row"). Step
02_01_01 therefore remains open. STEP_STATUS.yaml is unchanged by the PR
that emits this artifact. Closure of Step 02_01_01 is deferred to a
future PR after at least one materialization step (02_01_02 or successor)
runs CROSS-02-01-v1.0.1's post-materialization audit and records per-family
§10 verdicts for every registry row.

### Commitment path for resolving deferred dimensions before thesis defense

Per the methodology-debt commitment, the deferred dimensions D2 / D3 /
D4-in_game / D5-in_game / D6-full / D8 are resolved through path (a):
each is operationalized at its appropriate later layer (materialization
step + CROSS-02-01-v1.0.1 post-materialization audit), not through
additional V-N registry-layer validators. No CROSS-02-03 spec amendment
is required. This artifact is cited in the thesis (Chapter 4 §4.5) only
alongside the post-materialization audit artifact that closes the
deferred dimensions; the registry artifact alone does not constitute a
full Phase 02 leakage-clearance claim.
```

## Execution Steps

### T00 — Bundled docs(planning) commit (BEFORE T01 fires)

- **Operation:** Parent writes `planning/current_plan.md` (this plan) +
  `planning/current_plan.critique.md` (TWO critiques: reviewer-deep
  AND reviewer-adversarial, each in its own H1 section in the file) +
  updates `planning/INDEX.md` (archive PR #215 row with merge commit
  `396f162c` + merge date 2026-05-10; update active-plan row to this
  branch). Single commit.
- **Allowed files:** `planning/current_plan.md`,
  `planning/current_plan.critique.md`, `planning/INDEX.md`.
- **Forbidden files:** anything else.
- **Stop condition:** the three planning files are staged and committed
  as ONE `docs(planning)` commit; both critiques return PASS or
  PASS-WITH-NOTES (or APPROVE-WITH-CONDITIONS for adversarial); no
  BLOCKER outstanding.
- **Validation report shape:** parent reports the commit SHA and links
  to both critiques in chat.
- **Executor model assignment:** N/A — parent session executes T00.
- **Reviewer-routing:** plan-side critiques BY reviewer-deep AND
  reviewer-adversarial (BOTH mandatory per §Reviewer routing). 3-round
  cap applies.

### T01 — Notebook artifact-emission cell (CSV + MD lineage)

- **Operation:** Add a new code cell to
  `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
  positioned IMMEDIATELY AFTER the existing
  `validate_registry_skeleton(SKELETON, tracker_csv_path=TRACKER_CSV)`
  call cell (currently lines 503–508). Cell contents:
  1. Define `ARTIFACTS_DIR = get_reports_dir("sc2", "sc2egset") /
     "artifacts" / "02_feature_engineering" / "01_pre_game_vs_in_game_boundary"`
     and call `ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)`.
  2. Define `_BLOCK_BY_FAMILY: dict[str, str]` mapping each
     `feature_family_id` to its source block (one of `pre_game`,
     `history_enriched_pre_game`, `in_game_now`, `in_game_caveat`,
     `gate_and_blocked`). Build this dict from the in-memory
     `SKELETON_PRE_GAME` / `SKELETON_HISTORY` / `SKELETON_IN_GAME_NOW` /
     `SKELETON_IN_GAME_CAVEAT` / `SKELETON_GATE_AND_BLOCKED` lists by
     iterating each list and emitting `{row["feature_family_id"]: block_label}`.
  3. Build `csv_rows = [dict(row, block=_BLOCK_BY_FAMILY[row["feature_family_id"]])
     for row in SKELETON]`. The fieldnames for the writer are
     `list(REQUIRED_COLUMNS) + ["block"]` (14 columns). Use
     `csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")` for
     deterministic LF newlines (no platform-default CRLF on macOS / Linux
     differences). Write CSV to
     `ARTIFACTS_DIR / "02_01_01_feature_family_registry.csv"`.
  4. Build the MD body via a single `MD_BODY = f"""..."""` triple-quoted
     string containing:
     - H1 title: `# SC2EGSet Step 02_01_01 — Feature-family registry
       (provisional, validated through V-9)`
     - The verbatim disclaimer (option B encoding) from §"Disclaimer
       text — verbatim" above. NO PARAPHRASE.
     - Provenance / run-metadata block (under H2 `## Provenance`):
       notebook_path (relative to repo root), `validated_through = "V-9"`
       constant, validator_module relative path, `regenerated_via`
       command (the exact `jupyter nbconvert ... --execute --inplace`
       command), `python_version` from `sys.version_info`,
       `executed_at` ISO YYYY-MM-DD computed via
       `datetime.now(timezone.utc).date().isoformat()` (timezone-explicit
       UTC; NOT local-tz `date.today()` which would drift across
       local-midnight when not running in UTC). The provenance block
       MUST include the disclosure sentence: *"Re-running the notebook
       on the same UTC day produces a byte-identical artifact.
       Cross-UTC-day re-runs differ only in the `executed_at` field;
       semantic content (CSV rows, MD body, disclaimer) is identical."*
       This makes the reproducibility claim honest about its
       day-granularity limit (the artifact is reproducible WITHIN a
       UTC day, not ACROSS UTC days).
     - H2 `## Row counts by block` table summarizing 26-row partition:
       5 + 6 + 4 + 7 + 4 = 26 (computed from `_BLOCK_BY_FAMILY`).
     - H2 `## How to regenerate` with the exact `jupyter nbconvert`
       command (per `.claude/rules/data-analysis-lineage.md`
       reproducibility).
     - H2 `## References` listing the four upstream specs (CROSS-02-00,
       CROSS-02-01, CROSS-02-02, CROSS-02-03) with version + LOCKED date.
  5. Write `MD_BODY` to `ARTIFACTS_DIR / "02_01_01_feature_family_registry.md"`.
  6. `print()` the row count, the CSV path, the MD path, and an
     "artifact emission complete" line (use `print()` per memory
     `feedback_notebook_print_vs_logger` — this is data exploration,
     not diagnostic logging).
- **Allowed files:**
  `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`,
  `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`
  (regenerated by jupytext sync at T06).
- **Forbidden files:** every file in §File Manifest / Forbidden,
  PLUS `validate_registry_skeleton.py` (no validator change), PLUS
  `test_validate_registry_skeleton.py` (no test change here), PLUS
  `pyproject.toml` and `CHANGELOG.md` (T08 only).
- **Stop condition:** the new code cell exists at the correct position;
  a minimal smoke-run executes it without errors (deferred to T06 for
  full execution); the cell is jupytext-paired-friendly (single `# %%`
  marker; no in-cell newlines that would break the percent-format
  round-trip); no SKELETON_* row literal modified (verify by `git
  diff` of the .py file showing only additions in the artifact-emission
  region).
- **Validation report shape:** executor reports the cell's location
  (line range), the new code's line count, and the diff line count.
- **Executor model assignment:** Opus execution required. Reasoning:
  the artifact-emission cell is a methodology-load-bearing piece of
  code — its design choices (CSV column ordering, MD section ordering,
  provenance field choice, idempotency rule) are reviewed against the
  disclaimer. A Sonnet executor risks paraphrasing the disclaimer or
  silently using ISO-non-conformant date format, both of which would
  bounce at T10 reviewer-adversarial. (Per
  `.claude/rules/data-analysis-lineage.md` §"Agent and model routing
  discipline" line 20 — "use Opus when the implementation step itself
  requires subtle reasoning about ... thesis-facing methodological
  claims".)

### T02 — Notebook narrative correction (no SKELETON literal change)

- **Operation:** Edit narrative-only locations in the same .py file:
  1. Update the H2 `## Validation module (V-1 through V-8)` heading at
     line 477 to `## Validation module (V-1 through V-9)`. Live check
     during plan authoring confirmed line 477 still reads `(V-1 through
     V-8)` on master `396f162c` — PR #215's narrative-correction commit
     missed this heading. **This is a real edit, NOT a verify-only.**
  2. Update the markdown table at lines 484–492 — already includes V-9
     row from PR #215. Verify.
  3. Update line 494 narrative `Checks IN scope as of this PR (V-1
     base, V-1 strict, V-2..V-7 from PRs #212/#213, V-8 source-grain
     structural well-formedness from PR #214, V-9 per_player_construction
     controlled vocabulary + sentinel from this PR).` — change "from
     this PR" to "from PR #215; this PR adds artifact emission, no new
     validators." — exact wording at executor's discretion within the
     non-paraphrase zone.
  4. Update line 508 print banner from
     `print("validate_registry_skeleton: ALL PASS (V-1 through V-9)")`
     to
     `print("validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emission begins below")`.
  5. Update Conclusion §Artifacts produced (lines 513–521) from
     "**None.**" + deferral note to a paragraph that:
     - confirms the CSV + MD are now emitted under `ARTIFACTS_DIR`;
     - states `validated_through = V-9`;
     - explicitly states "this is provisional — closure of Step
       02_01_01 is NOT claimed";
     - cites the 3-clause `continue_predicate`;
     - cites the disclaimer's per-dimension table for unaddressed
       coverage.
  6. Update Conclusion §Status / log / manifest updates (lines 523–528)
     from "**None in this PR.**" to a paragraph that states:
     - STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / ROADMAP /
       INVARIANTS are deliberately untouched in this PR (cite §Problem
       Statement (c) rationale);
     - `research_log.md` IS updated with a partial-coverage entry;
     - `notebook_regeneration_manifest.md` IS updated with the new
       `provisional_through_v9_pending_post_materialization_audit`
       token + manifest row.
  7. Update Conclusion §Follow-ups (lines 535–554):
     - REMOVE the obsolete bullet "After all validation modules pass on
       review, materialize the registry CSV / MD artifact" (now done);
     - REMOVE bullet "Step 02_01_01 is NOT complete after this scaffold
       PR; completion requires the subsequent artifacts/log/status/
       manifest PR" (replace with the more honest "Step 02_01_01
       remains open after this artifact PR; closure requires the
       3-clause `continue_predicate`'s clauses 2 and 3 — see ROADMAP");
     - PRESERVE bullets enumerating still-open D2 / D3 / D6 / D8 / D9 /
       D10 / D12 / D15 deferrals (now reframed against the new D-coverage
       baseline).
  8. **DO NOT MODIFY** the SKELETON_PRE_GAME / SKELETON_HISTORY /
     SKELETON_IN_GAME_NOW / SKELETON_IN_GAME_CAVEAT /
     SKELETON_GATE_AND_BLOCKED row literals at lines 293–459.
- **Allowed files:** notebook .py + paired .ipynb (regenerated at T06).
- **Forbidden files:** as T01 plus all SKELETON_* literal lines.
- **Stop condition:** all 8 narrative edits land; no SKELETON_* line
  modified; jupytext round-trip remains clean.
- **Validation report shape:** executor reports the line numbers of all
  edits and verifies the SKELETON_* literal byte count is unchanged.
- **Executor model assignment:** Opus execution required (same rationale
  as T01 — narrative claims are methodology-load-bearing).

### T03 — Pre-commit-equivalent checks (lint / type / jupytext)

- **Operation:** Run (in this order):
  1. `source .venv/bin/activate && poetry run ruff check
     sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
  2. `source .venv/bin/activate && poetry run mypy
     sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
     (note: jupytext-paired .py files in `sandbox/` may be excluded
     from mypy by config — if so, this is a no-op which is acceptable).
  3. `source .venv/bin/activate && poetry run jupytext --check
     ipynb,py:percent
     sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`.
- **Allowed files:** none modified during T03 (read-only checks).
- **Forbidden files:** all (this is a check task).
- **Stop condition:** all three commands return exit 0.
- **Validation report shape:** executor reports each command's exit
  code and any warnings.
- **Executor model assignment:** Sonnet sufficient (mechanical check
  task).

### T04 — pytest with coverage (no validator changes; validator coverage stays ≥95%)

- **Operation:** Run
  `source .venv/bin/activate && poetry run pytest tests/ -v --cov
  --cov-report=term-missing | tee coverage.txt`. Per
  `.claude/rules/git-workflow.md` step 1.b — `--cov` without a path uses
  `[tool.coverage.run] source` from `pyproject.toml`
  (= `src/rts_predict`). Read `coverage.txt` and verify:
  - overall coverage ≥ 95% (the `fail_under = 95` threshold in
    `pyproject.toml`);
  - `validate_registry_skeleton.py` per-file coverage ≥ 95% (no
    validator code changed; coverage should be unchanged from PR #215
    baseline).
  Then `rm coverage.txt`.
- **Allowed files:** `coverage.txt` (created and removed within session;
  not committed).
- **Forbidden files:** all (this is a check task).
- **Stop condition:** pytest passes; coverage thresholds met; coverage.txt
  removed before T07 commit.
- **Validation report shape:** executor reports total test count,
  overall coverage %, and validator-file coverage %.
- **Executor model assignment:** Sonnet sufficient (mechanical check
  task).

### T05 — DELIBERATE GAP (renumbered upstream)

(This step number was reserved in the parent's task scaffold but the
underlying work is collapsed into T03 + T04. T05 is a no-op slot to
preserve the parent-supplied numbering. T06 follows.)

### T06 — Notebook execution end-to-end + idempotency check

- **Operation:**
  1. Run
     `source .venv/bin/activate && poetry run jupytext --sync
     sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
     to regenerate the .ipynb from the modified .py.
  2. Run
     `source .venv/bin/activate && poetry run jupyter nbconvert --to
     notebook --execute --inplace --ExecutePreprocessor.timeout=300
     sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`.
  3. Verify both artifact files now exist on disk (`ls -la` on both).
  4. **Idempotency check:** capture
     `sha256sum 02_01_01_feature_family_registry.csv 02_01_01_feature_family_registry.md`
     into `artifact_hash_a.txt`. Re-run the notebook execute command
     (step 2). Capture sha256sum again into `artifact_hash_b.txt`. The
     two hash files MUST be identical (`diff artifact_hash_a.txt
     artifact_hash_b.txt` returns no output and exit 0). If `executed_at`
     differs across the two runs (cross-midnight UTC race), HALT and
     escalate to user — the assumption (8.5) is violated.
  5. Remove `artifact_hash_a.txt` + `artifact_hash_b.txt`.
- **Allowed files:** notebook .ipynb (regenerated by jupytext + jupyter
  nbconvert), the two artifact files (created), the two scratch hash
  files (created and removed within session, not committed).
- **Forbidden files:** all others.
- **Stop condition:** notebook executes cleanly; both artifact files
  exist with the expected row counts (CSV: 27 lines total = 26 data + 1
  header); MD contains all five disclaimer H3 subsections, verified via
  `grep -c "^### " 02_01_01_feature_family_registry.md` returning exactly
  `5`; idempotency check passes (sha256 match across two same-UTC-day
  runs).
- **Validation report shape:** executor reports the .ipynb cell count,
  artifact row counts, file sizes, and sha256s.
- **Executor model assignment:** Sonnet sufficient (mechanical check
  task; the methodology-load-bearing edits already happened in T01–T02).

### T07 — Bundled feat commit for the artifact (CSV + MD + notebook .py + .ipynb)

- **Operation:** Stage and commit:
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md`
  - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
  - `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb`
  - Commit message via `.github/tmp/commit.txt` per memory
    `feedback_git_commit_format`:
    `feat(phase02): emit SC2EGSet 02_01_01 provisional registry artifact (validated through V-9)`
    + 1-paragraph body explaining: artifact paths; validated_through=V-9
    only; closure NOT claimed; STEP_STATUS untouched; CROSS-02-01-v1.0.1
    post-materialization audit still mandatory; full disclaimer in the
    artifact MD.
- **Allowed files:** the 4 paths above; `.github/tmp/commit.txt`
  (created, used, removed within this step).
- **Forbidden files:** all others; specifically `pyproject.toml` and
  `CHANGELOG.md` (T08 only); `research_log.md` and manifest (T09 only).
- **Stop condition:** commit lands; pre-commit hooks (ruff + mypy) pass;
  `git status` clean; `.github/tmp/commit.txt` removed.
- **Validation report shape:** executor reports the commit SHA and the
  4-file-only diff confirmation.
- **Executor model assignment:** Sonnet sufficient (mechanical commit
  with a pre-authored message).

### T08 — Bundled chore(release) commit (pyproject.toml + CHANGELOG)

- **Operation:**
  1. Edit `pyproject.toml` line 3: `version = "3.51.0"` → `version =
     "3.52.0"`.
  2. Edit `CHANGELOG.md`:
     - Move `[Unreleased]` block to a new `[3.52.0] — 2026-05-10
       (PR #TBD: phase02/sc2egset-registry-artifact-provisional-v9)`
       block (PR-number substitution post-create, mirroring PR #215
       precedent at lines 22 of CHANGELOG.md).
     - Insert empty `[Unreleased]` block (Added / Changed / Fixed /
       Removed headers).
     - Populate `[3.52.0]` Added with one bullet:
       `Provisional registry artifact for SC2EGSet Step 02_01_01:
       CSV + MD emitted at validated_through=V-9 baseline. Closure of
       Step 02_01_01 is NOT claimed; STEP_STATUS.yaml is untouched;
       CROSS-02-01-v1.0.1 post-materialization audit gate remains
       mandatory for any future feature column the registry triggers
       materialization of. Disclaimer in artifact MD enumerates
       per-dimension deferred coverage (D2 / D3 / D4-in_game /
       D5-in_game / D6-full / D8 / D9 / D10-sub-2 / D12 / D14 / D15).
       Manifest extended with new status token
       provisional_through_v9_pending_post_materialization_audit.`
  3. Stage both files and commit via `.github/tmp/commit.txt`:
     `chore(release): bump version to 3.52.0`.
  4. Remove `.github/tmp/commit.txt`.
- **Allowed files:** `pyproject.toml`, `CHANGELOG.md`,
  `.github/tmp/commit.txt`.
- **Forbidden files:** all others.
- **Stop condition:** commit lands; pre-commit hooks pass; `git status`
  clean.
- **Validation report shape:** executor reports the commit SHA and the
  2-file diff confirmation.
- **Executor model assignment:** Sonnet sufficient (mechanical edit + commit).

### T09 — Lineage commit: research_log + manifest

- **Operation:**
  1. Edit `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`:
     append a new Cat A entry at the top of the file (immediately under
     the last `---` separator preceding the most recent existing entry,
     OR at the canonical position dictated by the file's existing
     ordering convention — verify by reading the existing structure).
     Entry uses the standard schema (per the existing 2026-05-05
     entry's structure):
     - **Date / Phase / Step / Branch / Step scope** header
     - **Artifacts produced:** the 2 artifact paths
     - **What:** "Emitted the first on-disk artifact for Step 02_01_01:
       CSV + MD at `validated_through = V-9`. The artifact is provisional
       and does not constitute closure of Step 02_01_01."
     - **Why:** lineage sequence step 7; non-batching rule satisfied
       through PR #212/#213/#214/#215; user-declared validator stopping
       point at V-9.
     - **How (reproducibility):** notebook path; jupyter nbconvert
       command; idempotency confirmed via sha256 cross-run match.
     - **Findings:** 26-row registry CSV partition (5+6+4+7+4); D-coverage
       matrix (10 covered / partial; 6 deferred at registry layer; 5 N/A
       or post-materialization-only).
     - **What this means:** registry artifact is on disk and citable in
       Chapter 4 §4.5 ONLY alongside the future post-materialization
       audit artifact; alone it does NOT constitute a Phase 02
       leakage-clearance claim.
     - **Decisions taken:**
       - Status YAMLs untouched (cite §Problem Statement (c) rationale);
       - Manifest vocabulary extended with
         `provisional_through_v9_pending_post_materialization_audit`;
       - ROADMAP `continue_predicate` clauses 2 + 3 explicitly deferred.
     - **Decisions deferred:** materialization step (02_01_02 or
       successor); CROSS-02-01-v1.0.1 post-materialization audit
       re-run; per-family CROSS-02-03-v1.0.1 §10 verdicts.
     - **Acknowledged trade-offs:** none; the partial-coverage framing
       is honest by design.
     - **Thesis mapping:** Chapter 4 §4.5 (cited only with future
       post-materialization audit artifact).
  2. Edit `thesis/pass2_evidence/notebook_regeneration_manifest.md`:
     - Insert NEW token in the status vocabulary docstring
       (lines 8–13). Position: alphabetical, immediately BEFORE
       `regenerated_pending_log`. Token name and docstring text per
       §Problem Statement (d).
     - Add a new section header `## sc2egset — Phase 02 notebooks` if
       absent (likely is — the file currently has only Phase 01
       sections per the read at lines 23–65). Position: immediately
       after the existing "## sc2egset — Phase 01 notebooks" section
       block; before "## aoestats — Phase 01 notebooks". If the
       executor finds the file already has a Phase 02 section header,
       append the row to it instead.
     - Add ONE row to the new (or existing) Phase 02 section with:
       - Notebook path: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`
       - Step: `02_01_01`
       - Artifact status: `intact (newly created in this PR; provisional
         at validated_through=V-9)`
       - Thesis claim(s): `Chapter 4 §4.5 (cited only alongside future
         post-materialization audit artifact)`
       - Regen status: `provisional_through_v9_pending_post_materialization_audit`
       - Cause: `—`
  3. Stage both files and commit via `.github/tmp/commit.txt`:
     `feat(phase02): record SC2EGSet 02_01_01 provisional artifact
     lineage (research_log + manifest)`.
  4. Remove `.github/tmp/commit.txt`.
- **Allowed files:** `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`,
  `thesis/pass2_evidence/notebook_regeneration_manifest.md`,
  `.github/tmp/commit.txt`.
- **Forbidden files:** all others; specifically NO STEP_STATUS edit;
  NO ROADMAP edit; NO PIPELINE_SECTION_STATUS edit; NO PHASE_STATUS
  edit; NO `reports/research_log.md` (cross-game) edit.
- **Stop condition:** commit lands; pre-commit hooks pass; `git status`
  clean; the manifest's NEW status token appears exactly once in the
  vocabulary docstring AND exactly once in a manifest row.
- **Validation report shape:** executor reports the commit SHA and the
  2-file diff confirmation, plus a `grep -c "provisional_through_v9_pending_post_materialization_audit"`
  count of 2 (one in vocab + one in row).
- **Executor model assignment:** Opus execution required. Reasoning:
  the research_log entry is the lineage record that future thesis prose
  will cite; the manifest token name extension is methodology-load-bearing
  (it enters the vocabulary that downstream lineage audits use). Both
  must be authored carefully against the disclaimer's wording.

### T10 — Post-execution gate: BOTH reviewer-deep AND reviewer-adversarial in parallel

- **Operation:** Parent dispatches BOTH reviewer agents in parallel:
  1. `@reviewer-deep` with arguments: plan path = `planning/current_plan.md`;
     base_ref = `master @ 396f162c`; full diff for review.
  2. `@reviewer-adversarial` with same arguments.
  Each reviewer reads the plan + the diff + the artifact MD + the
  research_log entry + the manifest changes, and returns a verdict.
- **Allowed files:** none modified during T10 (review only). Reviewers
  may write to a `planning/current_plan.critique.md` follow-up section
  (e.g., "Round 2 — post-execution") via the parent.
- **Forbidden files:** all (this is a review task).
- **Stop condition:** BOTH reviewers return PASS, PASS-WITH-NOTES, or
  APPROVE-WITH-CONDITIONS (or PASS-WITH-FIXES for reviewer-deep, where
  fixes are mechanical and addressed in a follow-up commit before T11).
  Either reviewer returning a `BLOCKER` (reviewer-deep) or `BLOCKED`
  (reviewer-adversarial) halts T11; the resolution path is in §Stop
  conditions (3-round adversarial cap).
- **Validation report shape:** parent reports both verdicts in chat,
  with file:line citations for any FIX or BLOCKER.
- **Executor model assignment:** Opus (reviewer-deep) and Opus
  (reviewer-adversarial); both reviewers are Opus by §Reviewer routing.

### T11 — Ready: PR body, push, mark ready, cleanup

- **Operation:**
  1. Mark draft PR #216 ready for review:
     `gh pr ready 216` (no body change yet).
  2. Author PR body via `.github/tmp/pr.txt` per memory
     `feedback_pr_body_file`. Format per
     `.claude/rules/git-workflow.md` PR body format. Body summary
     bullets:
     - First on-disk registry artifact for Step 02_01_01 (CSV + MD).
     - Validated through V-9 (V-9 is the user-declared stopping point
       for registry-layer validators in this cycle).
     - Closure of Step 02_01_01 is NOT claimed; STEP_STATUS untouched;
       3-clause continue_predicate's clauses 2 and 3 deferred.
     - CROSS-02-01-v1.0.1 post-materialization audit gate remains
       mandatory.
     - Manifest vocabulary extended with new partial-coverage token.
     Test plan bullets: artifact regeneration command; idempotency
     check; pytest pass; ruff/mypy/jupytext clean.
  3. Update PR body:
     `gh pr edit 216 --body-file .github/tmp/pr.txt`.
  4. Substitute the PR number `216` in CHANGELOG `[3.52.0]` block's
     header (replace `PR #TBD` → `PR #216`). Stage CHANGELOG.md and
     commit via `.github/tmp/commit.txt`:
     `chore(release): substitute PR number in CHANGELOG [3.52.0]`.
  5. Update `planning/INDEX.md` active row: append `(PR #216)`. Stage
     and commit via `.github/tmp/commit.txt`:
     `docs(planning): record PR number for SC2EGSet 02_01_01 provisional
     artifact plan`.
  6. Push branch (parent decides timing per CLAUDE.md "ASK FIRST" for
     `git push`).
  7. Remove `.github/tmp/pr.txt` and `.github/tmp/commit.txt` per
     memories `feedback_pr_body_cleanup` and `feedback_git_commit_format`.
- **Allowed files:** `CHANGELOG.md`, `planning/INDEX.md`,
  `.github/tmp/pr.txt`, `.github/tmp/commit.txt`.
- **Forbidden files:** all others.
- **Stop condition:** PR is ready (not draft); body matches template;
  CHANGELOG PR number substituted; INDEX active row carries `(PR #216)`;
  scratch files removed.
- **Validation report shape:** parent reports the PR URL,
  ready/draft state, and final commit SHAs.
- **Executor model assignment:** Sonnet sufficient (mechanical CLI +
  commit ops).

## Validation gates

(All gates must hold simultaneously for merge eligibility — mirrored from
§Gate Condition.)

1. File-diff scope matches §File Manifest exactly (no forbidden file).
2. CSV file has 26 data rows + 1 header row = 27 lines total; 14 columns
   (13 REQUIRED_COLUMNS + `block`).
3. MD file contains the verbatim disclaimer (option B encoding) — no
   paraphrase.
4. MD file contains the per-dimension deferred-coverage table.
5. MD file contains the provenance / run-metadata block.
6. Notebook print banner reads
   `"validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emission begins below"`
   in executed cell output.
7. Notebook regeneration is idempotent (sha256 match across two runs;
   intra-day execution).
8. pytest passes; coverage ≥ 95% overall AND validator file ≥ 95%.
9. ruff / mypy / jupytext clean.
10. Status YAMLs and ROADMAP unchanged; validator and tests unchanged;
    skeleton row literals unchanged.
11. Manifest vocabulary docstring extended with new token; row uses new
    token.
12. research_log entry uses partial-coverage language; cites 3-clause
    continue_predicate; explicitly states STEP_STATUS no-touch
    rationale.
13. Pyproject.toml `version = "3.52.0"`; CHANGELOG `[3.52.0]` block dated
    2026-05-10 with PR #216 substituted.
14. BOTH reviewer-deep AND reviewer-adversarial at T10 return PASS,
    PASS-WITH-NOTES, or APPROVE-WITH-CONDITIONS.

## Release policy

- Version bump: minor (`3.51.0` → `3.52.0`) per
  `.claude/rules/git-workflow.md` step 2 ("minor for feat/refactor/docs,
  patch for fix/test/chore"). This is a Cat A feat (artifact emission).
- CHANGELOG bullet under `[3.52.0]` Added — single bullet documenting
  the artifact, the validated_through=V-9 claim, the explicit closure
  non-claim, the STEP_STATUS no-touch, and the manifest token extension.
- Empty `[Unreleased]` block re-inserted with Added / Changed / Fixed /
  Removed headers.

## Reviewer routing

- **Plan-side critique (T00):** BOTH reviewer-deep AND reviewer-adversarial.
  This is methodology-load-bearing — the artifact disclaimer is the
  load-bearing surface. Both critiques live in one
  `planning/current_plan.critique.md` file (one H1 section per reviewer).
  3-round adversarial cap applies.
- **Execution-side critique (T10):** BOTH reviewer-deep AND
  reviewer-adversarial in parallel. Same file may be amended with
  Round 2 sections (or a sibling `.critique.round2.md` file at parent's
  discretion). 3-round cap applies symmetrically per memory
  `feedback_adversarial_cap_execution`.
- **Why both gates:** Per `.claude/rules/data-analysis-lineage.md`
  line 24, the active Phase 02 readiness PR cycle was authorized to
  use reviewer-deep alone for the V-N validator-PR sequence (PR #212
  through PR #215). This artifact PR is methodologically distinct —
  it produces the FIRST on-disk artifact, encodes the load-bearing
  disclaimer, and extends the manifest vocabulary. The user has
  explicitly required BOTH reviewers for this PR. The carve-out at
  line 24 does NOT apply to artifact-emission PRs.

## Non-batching rationale (sequence step 7 — artifact)

Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule for
empirical work", the 9-step sequence is:
1. ROADMAP stub only — done at PR #208 (Step 02_01_01 entry).
2. Notebook scaffold + one validation module — done at PR #212.
3. Execute and report — done at PR #212.
4. User review — done before PR #212 merge.
5. Commit — done at PR #212.
6. Next validation module — done at PR #213 (V-1 strict + V-7),
   PR #214 (V-8), PR #215 (V-9). User declared V-9 as the stopping
   point for this cycle.
7. **Only after all validation modules pass, generate artifacts —
   THIS PR.**
8. Then research_log / STEP_STATUS / manifest — research_log + manifest
   in T09 of THIS PR; STEP_STATUS deferred per §Problem Statement (c).
9. Then reviewer-deep — T10 of THIS PR (with reviewer-adversarial
   added per the methodology-load-bearing nature of this PR).

The non-batching rule is satisfied: this PR does NOT batch a new
validator with the artifact emission, and does NOT touch the next Step
(02_01_02). The closure of Step 02_01_01 is explicitly deferred (it
requires the 3-clause continue_predicate's clauses 2 and 3, which depend
on a future materialization step).

## Stop conditions

Halt T01 → T11 if any of the following:

1. **Disclaimer overclaim risk.** If T01–T02 implementation produces an
   artifact that implies closure of Step 02_01_01 (e.g., wording like
   "Step closed", "fully validated", "complete coverage", "registry
   final"), HALT and escalate to user. The artifact may HONESTLY claim
   only `validated_through = V-9`.
2. **Status YAML touch attempt.** If T01–T11 produce any diff against
   STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml,
   HALT and escalate. Default no-touch is the load-bearing methodology
   decision per §Problem Statement (c).
3. **Idempotency check fails.** If T06 sha256 cross-run check fails for
   any reason except cross-midnight UTC race, HALT and escalate to
   user; the assumption (8.5) is violated and the artifact would be
   non-reproducible.
4. **Validator drift.** If `git status` shows any change to
   `validate_registry_skeleton.py` or its test file, HALT immediately —
   validator is FROZEN at V-9 in this cycle.
5. **Skeleton row literal modification.** If `git diff master..HEAD --
   sandbox/.../02_01_01_feature_family_registry_skeleton.py` shows any
   change to lines 293–459 (SKELETON_* literals), HALT immediately.
6. **AoE2 file touch.** If `git status` lists any file under
   `src/rts_predict/games/aoe2/`, HALT immediately.
7. **Spec edit attempt.** If `git status` lists any file under
   `reports/specs/02_*.md`, HALT immediately.
8. **Reviewer BLOCKER at T00.** If reviewer-deep OR reviewer-adversarial
   returns a BLOCKER on the plan-side critique, address the BLOCKER and
   re-run that reviewer. 3-round adversarial cap applies. After 3
   rounds without convergence, HALT and escalate to user.
9. **Reviewer BLOCKER at T10.** Same as (8) for the post-execution
   gate. 3-round cap symmetric.
10. **Encoding ambiguity surfaces.** If GitHub markdown rendering of
    plain `<` / `>` produces visible escape artifacts in the PR diff
    preview, switch to option A (HTML entities `&lt;` / `&gt;`) at
    parent's direction. Both options are valid per parent's note.
11. **CROSS-02-01-v1.0.1 supersession risk.** If any reviewer at T00 or
    T10 raises that the artifact MD wording weakens or supersedes
    CROSS-02-01-v1.0.1's post-materialization audit gate, HALT and
    rewrite the §"Non-supersession of the post-materialization audit"
    block to make the non-supersession claim more explicit.

Halt before delegating any task if:
- the task lacks exact allowed files;
- the task lacks exact forbidden files;
- the task lacks a stop condition;
- the task does not specify whether Sonnet executor is sufficient or
  Opus execution is required;
- the task would allow an executor to batch artifact + research_log +
  manifest + STEP_STATUS in one execution.

## Open Questions

**Resolved (decisions documented in this plan):**

1. STEP_STATUS touch? — No-touch. §Problem Statement (c) +
   §Verification 5/6/7. ROADMAP `continue_predicate` is conjunctive
   3-clause; clause 1 satisfied here; clauses 2+3 require materialization
   step. STEP_STATUS no-touch is the safer methodology default.
2. PIPELINE_SECTION_STATUS touch? — No-touch (derived from
   STEP_STATUS).
3. PHASE_STATUS touch? — No-touch (derived from
   PIPELINE_SECTION_STATUS).
4. ROADMAP touch? — No-touch. The existing `continue_predicate`
   already enumerates the 3-clause conjunction; partial-coverage framing
   lives in the artifact MD disclaimer, not the ROADMAP.
5. research_log entry? — Yes — per CLAUDE.md "After Category A
   step: Update the active dataset's research_log.md". Entry uses
   partial-coverage language; explicitly states STEP_STATUS no-touch.
6. Manifest entry? — Yes — using a NEW status token
   `provisional_through_v9_pending_post_materialization_audit` added
   to the vocabulary docstring (§Problem Statement (d)).
7. Disclaimer encoding? — Option B (plain `<` / `>`) — cleaner
   GitHub rendering and easier code-review diff inspection. Option A
   fallback documented in Stop condition (10).
8. Single CSV + single MD vs. per-block split? — Single CSV +
   single MD, with `block` column on the CSV identifying source partition.
   Justification: 26 rows is well below the threshold where splitting
   improves readability; a single artifact aligns with the
   `02_01_01_feature_family_registry.csv` versionless naming convention
   and matches the manifest's per-notebook (single-row) pattern.
9. Versionless filename? — Yes — `02_01_01_feature_family_registry.csv`
   (no `_v9` or `_provisional` suffix in the filename). The
   `validated_through` field lives INSIDE the artifact (CSV provenance
   row in the MD; not a CSV column at this stage). This matches the
   Phase 01 artifact-naming convention (e.g.,
   `tracker_events_feature_eligibility.csv` — no version suffix).
10. Reviewer routing? — BOTH reviewer-deep AND reviewer-adversarial
    at BOTH plan-side (T00) and execution-side (T10) gates. 3-round
    adversarial cap symmetric.
11. CROSS-02-03 §1.3 non-supersession encoded in MD? — Yes —
    verbatim block "Non-supersession of the post-materialization
    audit" reproduces CROSS-02-03-v1.0.1 §1.3 phrasing.
12. AoE2 sub-clause 2 reference? — Recorded as N/A in the
    per-dimension table; deferred to a future aoestats-side V-N PR.

**Unresolved (surfaced for executor + reviewer awareness):**

- (none material to T01 dispatch)

**Methodology-load-bearing items the user's 12-question framing
covered well — surfacing for reviewer-adversarial visibility:**

- The closure-status framing is the load-bearing claim. The disclaimer
  has it; the research_log entry has it; the CHANGELOG has it; the
  PR body has it. A reviewer probing for inconsistency across these
  surfaces should find none.
- The non-supersession claim is the second load-bearing claim. Same
  multi-surface coverage.
- The STEP_STATUS no-touch decision rests on (a) ROADMAP `continue_predicate`
  conjunctivity and (b) the per-step status vocabulary not documenting
  `in_progress`. A reviewer who challenges this can be redirected to
  §Problem Statement (c) + §Verification 5–7.

## Out of scope

- V-10+ validator design or implementation.
- Any AoE2 work (aoestats canonical_slot D10 sub-clause 2; aoe2companion
  any).
- Phase 03 implementation.
- Materialization step 02_01_02 implementation.
- CROSS-02-01-v1.0.1 post-materialization audit re-run.
- Per-family CROSS-02-03-v1.0.1 §10 verdict recording.
- Step 02_01_01 closure (and downstream Pipeline Section 02_01 / Phase
  02 closure).
- Thesis prose edits (Chapter 4 §4.5 will cite this artifact only after
  the post-materialization audit artifact lands; that drafting is a
  separate Cat F PR).
- ROADMAP `continue_predicate` rewording.
- INVARIANTS.md (per-dataset) edits.
- `.claude/**` rule / agent / scientific-invariants edits.
- `docs/**` taxonomy / methodology edits.
- Cross-game research_log entry (`reports/research_log.md`) — this is a
  dataset-scoped artifact; entry goes in dataset-scoped log only.
- Hygiene follow-ups deferred from PR #213/#214 (defensive-branch coverage
  on validator lines 347 / 415 / 421; test-infra `parents[6]` magic
  refactor; V-8 helper bare-`(filename)` permissiveness on tracker rows).
- Manifest extension for any other status vocabulary token (only
  `provisional_through_v9_pending_post_materialization_audit` is added).
- Adding a `validated_through` column to the CSV (it lives in the MD
  provenance block; CSV stays at 14 columns).

## Acceptance criteria

This PR is mergeable to master when ALL of the following hold:

1. `git diff master..HEAD --name-only` matches §File Manifest / Allowed
   exactly. Forbidden file count = 0.
2. CSV exists at the declared path; 26 data rows + 1 header row = 27
   lines total; 14 columns (13 REQUIRED_COLUMNS + `block`).
3. MD exists at the declared path; contains verbatim disclaimer (option
   B encoding) + provenance block + per-dimension table + V-1..V-9
   mapping + regeneration command + references.
4. Notebook regenerates artifact deterministically (sha256 match across
   two intra-day runs).
5. Notebook print banner reads
   `"validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emission begins below"`.
6. pytest passes; coverage ≥ 95% overall AND validator file ≥ 95%
   (validator unchanged).
7. ruff / mypy / jupytext clean.
8. Status YAMLs (STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS),
   ROADMAP, INVARIANTS, all `02_*` specs,
   `validate_registry_skeleton.py`, its test file, and all SKELETON_*
   row literals are byte-identical to master `396f162c`.
9. `research_log.md` has a new Cat A entry dated 2026-05-10 with
   partial-coverage language.
10. `notebook_regeneration_manifest.md` has the new status token
    `provisional_through_v9_pending_post_materialization_audit` in the
    vocabulary docstring AND a manifest row using that token.
11. `pyproject.toml` shows `version = "3.52.0"`.
12. `CHANGELOG.md` has a `[3.52.0] — 2026-05-10` block with PR #216
    substituted.
13. `planning/INDEX.md` archive shows PR #215 with merge SHA `396f162c`;
    active row = this branch with `(PR #216)`.
14. **BOTH** reviewer-deep AND reviewer-adversarial at T10 return PASS,
    PASS-WITH-NOTES, or APPROVE-WITH-CONDITIONS. Either reviewer
    returning a BLOCKER halts the PR.
15. PR #216 is ready (not draft); body follows
    `.github/pull_request_template.md` per
    `.claude/rules/git-workflow.md`.
16. No closure overclaim anywhere across CSV, MD, commit messages,
    research_log entry, manifest entry, CHANGELOG, PR body, or notebook
    narrative.
