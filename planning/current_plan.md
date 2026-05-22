---
plan_ref: planning/current_plan.md
plan_id: docs/thesis-pass2-020101-manifest-closure-reconciliation
category: F
branch: docs/thesis-pass2-020101-manifest-closure-reconciliation
base_ref: 0c45c490e4b306892cf796f2cf3db72201bae826
date: 2026-05-22
outcome: "A — manifest-reconciliation planning PR first"
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
post_execution_reviewer: reviewer-adversarial (Cat F)
invariants_touched: [9]
source_artifacts:
  - thesis/pass2_evidence/notebook_regeneration_manifest.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml
---

# SC2EGSet Step 02_01_01 — OQ4 manifest reconciliation plan (Category F)

This is a **planning-only** materialization. It describes a FUTURE execution PR that
reconciles `thesis/pass2_evidence/notebook_regeneration_manifest.md` with the PR #230
catalog-only closure of SC2EGSet Phase 02 / Step `02_01_01`. Execution requires a
separate, explicitly-approved turn after this plan is inspectable on the draft PR.

## Scope

Reconcile the notebook regeneration manifest (and only the manifest + planning/index +
release tail) with the now-landed PR #230 closure. PR #230 (merged 2026-05-22 at master
`0c45c490`) closed Step `02_01_01` at the catalog-only registry layer via a
zero-materialization CROSS-02-01-v1.0.1 leakage-audit artifact pair, flipped the
STEP/PIPELINE_SECTION/PHASE status triad, and wrote a per-dataset research_log closure
entry. Its final gate recorded **OQ4**: the manifest must be reconciled before any later
`02_01` step (esp. `02_01_02`) cites the closure artifact as manifested/intact.

**Chosen outcome: A** (manifest-reconciliation planning PR first). Rejected alternatives:
B (proceed to `02_01_02` planning) — the manifest row is load-bearing for future `02_01`
planning and currently asserts "no Step closure", contradicting on-disk STEP_STATUS
(Invariant #9 risk); C (HOLD as a non-hand-editable generated artifact) — the manifest has
NO generator pipeline (grep across `src/`, `sandbox/`, `scripts/`, `Makefile` = 0 hits;
git history shows only hand edits), so the `.claude/rules/data-analysis-lineage.md`
"Artifact discipline" hand-edit prohibition (which governs notebook/script-emitted
artifacts) does not apply; D (combine with `02_01_02` design) — forbidden by the
non-batching rule in `.claude/rules/data-analysis-lineage.md`.

This plan touches (in the eventual execution PR) ONLY:
`thesis/pass2_evidence/notebook_regeneration_manifest.md`, `planning/INDEX.md`,
`planning/current_plan.md`, `planning/current_plan.critique.md`, `CHANGELOG.md`,
`pyproject.toml`. No status YAML, no artifact, no notebook, no source, no test, no chapter
prose, no `02_01_02` work, no Phase 03 work.

## Problem statement

The manifest (`Generated: 2026-04-26 by T03 executor`) predates PR #230. Its single
Phase-02 sc2egset row (the `02_01_01_feature_family_registry_skeleton.py` row) still reads
status `partial_coverage_v9_baseline` with artifact-status text "no Step closure". That
assertion is now false on three counts that the token's own definition enumerates:
(1) the per-family CROSS-02-03 §10 verdict is satisfied on disk (PR #229); (2) Step closure
is no longer deferred (PR #230 closed it at the catalog-only layer); only (3) the
post-materialization CROSS-02-01 audit re-run remains genuinely unsatisfied (nothing is
materialized yet — that is the future `02_01_02`). The manifest also has no row at all for
the PR #229 §10 verdict-audit notebook nor for the PR #230 CROSS-02-01 artifact pair. A
future `02_01` planner consulting the manifest would inherit a stale "not closed" upstream
assertion. OQ4 (PR #230 research_log) names this reconciliation as the explicit next
planner-science task and instructs cross-referencing the new closure token combination
(`closure_status: closed` + `leakage_audit_state: zero_materialization_pass`).

## Assumptions & Unknowns

- **A1.** The manifest is a hand-maintained audit tracker, not a pipeline-generated
  artifact. Evidence: no generator script anywhere; git history is hand edits only
  (T03 created it; T06/T07/T09/T12 edited rows by hand). Hand-editing via a
  planner -> reviewer-adversarial -> executor PR is the canonical, repo-precedented path.
- **A2.** PR #230's closure stands and is byte-stable on master; this plan does NOT
  re-touch any status YAML, artifact, or research_log. STEP_STATUS `02_01_01: complete`
  landed in PR #230 (commit `a47d0809`), NOT PR #229 (`a14dc547`).
- **A3.** The single ROADMAP step `02_01_01` covers BOTH the registry-skeleton notebook
  and the §10-audit notebook; neither is its own step. `confirmed_intact` is defined at
  Step granularity ("promote a Step"), so it must not be applied per-artifact in a way
  that implies an earlier PR closed the step. (This is why N1 below moves the §10-audit
  row to the catalog-only-closure token rather than `confirmed_intact`.)
- **U1 (OQ-M1, resolved here per reviewer N2):** Summary accounting uses a footnote, NOT a
  new table column, to avoid widening the Summary table with mostly-empty cells for a
  3-row concept and to preserve the existing `confirmed_intact` total invariant.

## Literature Context

Not applicable in the empirical sense — this is a thesis-lineage bookkeeping
reconciliation, not a new experiment. Governing repo conventions: the manifest's own
status-vocabulary definitions and `confirmed_intact` promotion rule (lines 8-14);
`.claude/rules/data-analysis-lineage.md` "Artifact discipline" (governs pipeline-generated
artifacts only) and "Non-batching rule"; `.claude/scientific-invariants.md` Invariant #9
(research-pipeline discipline — a downstream document must not assert facts contradicting
on-disk artifacts); `.claude/rules/git-workflow.md` version policy ("minor for
feat/refactor/docs"); CLAUDE.md category table (F = `docs/thesis-`, loads thesis-writing
rule on `thesis/` touch).

## Execution steps

> All steps below are for the FUTURE execution PR, on this branch, after this plan is
> approved on the draft PR and an explicit execution turn begins. Locate manifest edits by
> anchor content (quoted strings), not solely by line number — line numbers drift as edits
> land. Approximate line numbers are from master `0c45c490`.

### E1 — Add the new status token to the manifest vocabulary

In `thesis/pass2_evidence/notebook_regeneration_manifest.md`, immediately AFTER the
`partial_coverage_v9_baseline` bullet (≈ line 12), insert one new vocabulary bullet:

> `catalog_only_closed_zero_materialization` — Step closed at the catalog-only registry
> layer via the CROSS-02-01-v1.0.1 zero-materialization leakage-audit artifact pair
> (`reports/artifacts/02_01_01/leakage_audit_<dataset>.{json,md}`); the STEP_STATUS /
> PIPELINE_SECTION_STATUS / PHASE_STATUS flips have landed (per-dataset research_log
> `closure_status: closed` + `leakage_audit_state: zero_materialization_pass`). Asserts
> CATALOG-LAYER closure ONLY: no feature column is materialized, `verdict=PASS` is vacuous
> per CROSS-02-01-v1.0.1 §5(a), and a future post-materialization CROSS-02-01 audit re-run
> remains REQUIRED before any empirical leakage-clearance claim. Distinct from
> `confirmed_intact` (which requires a full ROADMAP -> notebook -> artifact -> research_log
> -> STEP_STATUS lineage and implies no further lineage work) and from
> `partial_coverage_v9_baseline` (which asserts Step closure is still deferred).

Do NOT alter the `confirmed_intact` promotion-rule text (≈ line 9). Retain
`partial_coverage_v9_baseline` in the vocabulary (other/future rows may still need it).

### E2 — Re-tokenize the existing `02_01_01` registry-skeleton row

Replace the current row (≈ line 73) for
`02_01_01_feature_family_registry_skeleton.py`. From the stale
`... | no Step closure | ... | partial_coverage_v9_baseline | PR #216 ... non-closure lineage |`
to:

> `| sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py | 02_01_01 | registry CSV+MD present (PR #216, validated_through=V-9); Step 02_01_01 CLOSED at catalog-only layer via CROSS-02-01-v1.0.1 zero-materialization audit pair (PR #230); no feature column materialized | Chapter 4 §4.5 feature-engineering registry / Phase 02 catalog-only registry closure | catalog_only_closed_zero_materialization | PR #216 provisional baseline -> PR #230 catalog-only closure (zero-materialization CROSS-02-01 audit) |`

### E3 — Add two new Phase-02 rows

After the E2 row (before the closing `---` of the Phase-02 sc2egset table), add:

**Row A — PR #229 §10 verdict-audit notebook** (N1: uses the catalog-only-closure token,
NOT `confirmed_intact`, because the step's STEP_STATUS flip landed at PR #230, not PR #229;
all three rows share the single step's closure provenance):

> `| sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py | 02_01_01 (§10 audit) | §10 verdict-audit CSV+MD present (PR #229); 26 rows audited; materialized_column_count=0; step closed at catalog-only layer by PR #230 (PR #229 itself was closure_status: still_open) | Chapter 4 §4.5 — secondary lineage row (CROSS-02-03 §10 design-time per-family verdicts) | catalog_only_closed_zero_materialization | PR #229 §10 evidence persistence; step closed by PR #230 |`

**Row B — PR #230 CROSS-02-01 hand-written artifact pair** (N3: explicitly annotate that it
is a hand-written stub, not a notebook, so a blank notebook path is not read as a
missing-notebook defect):

> `| — (hand-written CROSS-02-01 artifact pair; not a notebook; no regeneration lineage applies): reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md} | 02_01_01 (closure audit) | zero-materialization CROSS-02-01-v1.0.1 leakage-audit JSON+MD present (PR #230); verdict=PASS vacuous per §5(a); NOT a substitute for the §10 audit nor for a future post-materialization CROSS-02-01 audit | Chapter 4 §4.5 — closure-row lineage; does NOT enable an empirical leakage-clearance claim | catalog_only_closed_zero_materialization | PR #230 catalog-only closure |`

### E4 — Update the manifest Summary block (footnote accounting, per N2)

- Update the **Last updated** line to: `**Last updated:** 2026-05-22 by
  planner-science-directed executor (PR #231, OQ4 manifest closure reconciliation for
  SC2EGSet Step 02_01_01).`
- Add a one-line **Change** note recording: SC2EGSet Step 02_01_01 row moved
  `partial_coverage_v9_baseline` -> `catalog_only_closed_zero_materialization` (PR #230
  catalog-only closure); 2 new Phase-02 rows added (§10 verdict-audit notebook;
  CROSS-02-01 closure artifact pair), both `catalog_only_closed_zero_materialization`.
- Add a **footnote** beneath the Summary table (do NOT add a new column): `† 3 sc2egset
  Phase 02 rows carry catalog_only_closed_zero_materialization (registry skeleton, §10
  verdict-audit, CROSS-02-01 closure pair); these are NOT counted in confirmed_intact.`
- Confirm the existing cross-dataset assertion lines (`0 flagged_stale`,
  `0 regenerated_pending_log`) remain TRUE and are not contradicted (they are not — the new
  token is neither). Leave the `confirmed_intact` total unchanged.

### E5 — Archive PR #230 in `planning/INDEX.md`

- Move the current Active line (the `feat/sc2egset-02-01-01-formal-closure-...` line, which
  still carries the now-stale "(PR #230, draft)" qualifier) into the Archive table as a new
  TOP row, replacing the qualifier with: `... | current_plan.md | #230 (merged 2026-05-22 at
  master 0c45c490) |`, Category A.
- Set the new Active line to this branch:
  `docs/thesis-pass2-020101-manifest-closure-reconciliation (2026-05-22) — Category F:
  reconcile thesis/pass2_evidence/notebook_regeneration_manifest.md with the PR #230
  catalog-only closure of SC2EGSet Step 02_01_01 (move the 02_01_01 row to a new
  catalog_only_closed_zero_materialization token, add §10-audit + CROSS-02-01 rows,
  cross-reference PR #230 sibling tokens); archive PR #230; version bump; NO 02_01_02, NO
  Phase 03, NO chapter prose (PR #231, draft).`

### E6 — Release tail

- `pyproject.toml`: bump `version = "3.65.0"` -> `version = "3.66.0"` (minor; docs/thesis
  family per git-workflow policy).
- `CHANGELOG.md`: move `[Unreleased]` content under a new
  `## [3.66.0] — 2026-05-22 (PR #231: docs/thesis-pass2-020101-manifest-closure-reconciliation)`
  block with a `### Changed` entry describing the manifest reconciliation + INDEX archival;
  re-empty `[Unreleased]` with the four standard sub-headers; preserve `[3.65.0]` and
  older blocks.

### E7 — Validation (future execution PR; HALT on any failure)

1. `grep -c "catalog_only_closed_zero_materialization" thesis/pass2_evidence/notebook_regeneration_manifest.md` -> exactly 4 (1 vocab bullet + 3 rows).
2. The `02_01_01` registry-skeleton row no longer contains "no Step closure"; it contains "CLOSED at catalog-only layer" and "PR #230".
3. `partial_coverage_v9_baseline` still matches exactly once (the retained vocabulary definition), not the data row.
4. STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS are byte-unchanged (`git diff --name-only master..HEAD` does NOT list them).
5. No file under `…/reports/artifacts/**`, no `…/research_log.md` (per-dataset OR root), no `thesis/chapters/**`, no notebook, no validator/test is in the diff.
6. `pyproject.toml` = `3.66.0`; `CHANGELOG.md` has `## [3.66.0]` and an empty `[Unreleased]`; `[3.65.0]` preserved.
7. `planning/INDEX.md`: PR #230 appears once in Archive with merge SHA `0c45c490`, no "draft" qualifier on it; the new branch is the sole Active line.
8. **Final tracked diff = exactly 6 files** (`git diff --name-only master..HEAD | sort`) — the 2 planning files (already on the branch from THIS materialization commit) + the 4 execution files:
   ```
   CHANGELOG.md
   planning/INDEX.md
   planning/current_plan.critique.md
   planning/current_plan.md
   pyproject.toml
   thesis/pass2_evidence/notebook_regeneration_manifest.md
   ```
9. **Execution-file subset = exactly 4**: `git diff --name-only master..HEAD | grep -vE '^planning/current_plan(\.critique)?\.md$' | sort` returns exactly `CHANGELOG.md`, `planning/INDEX.md`, `pyproject.toml`, `thesis/pass2_evidence/notebook_regeneration_manifest.md` (count = 4).
10. **Transient files absent**: `test ! -e .github/tmp/commit.txt && test ! -e .github/tmp/pr.txt` exits 0 — both created/deleted during wrap-up if used and MUST NOT appear in the final diff.
11. **No live PR-number placeholders in execution files or the PR #231 body**: scoped to the 4 execution files AND the PR body, a grep for `PR #<n>` / `PR #<this PR>` / `PR #<TBD>` / `PR #{n}` returns 0 — every reference to this PR is the literal `PR #231`. Any placeholder-like strings remaining anywhere in the diff are ONLY regex-documentation text inside the planning files (`planning/current_plan.md` / `.critique.md`), which are exempt from the execution-placeholder check; the planning files MUST NOT be edited to mask the check.

## File Manifest

Future execution-PR file set (justified per file):

| File | Why | Edit type |
|---|---|---|
| `thesis/pass2_evidence/notebook_regeneration_manifest.md` | The reconciliation target. | Edit: vocab bullet, row re-token, +2 rows, Summary footnote. |
| `planning/INDEX.md` | Archive PR #230; set new Active line; drop stale "draft". | Edit. |
| `planning/current_plan.md` | This plan (handoff artifact). | Already materialized in THIS planning PR. |
| `planning/current_plan.critique.md` | Cat F mandatory critique. | Already materialized in THIS planning PR. |
| `CHANGELOG.md` | `[Unreleased]` -> `[3.66.0]` move. | Edit. |
| `pyproject.toml` | Single version source; minor bump. | Edit (version line only). |

**Manifest-count (draft-PR-first; PR #231 already exists before execution):**
- Current planning-only draft diff before execution = **2 tracked planning files** (`planning/current_plan.md`, `planning/current_plan.critique.md`).
- Future execution adds **4 tracked execution files** (`thesis/pass2_evidence/notebook_regeneration_manifest.md`, `planning/INDEX.md`, `CHANGELOG.md`, `pyproject.toml`).
- **Final tracked PR diff after execution = 6 files** (2 planning + 4 execution).
- Transient `.github/tmp/commit.txt` and `.github/tmp/pr.txt` are created/deleted during wrap-up if needed and MUST NOT appear in the final diff.

Because PR #231 already exists before execution, the future execution writes literal `PR #231` everywhere it references this manifest-reconciliation PR (manifest "Last updated" line, CHANGELOG `[3.66.0]` header, `planning/INDEX.md` Active line, the PR body, and validation). No `PR #<n>` / `PR #<this PR>` placeholder is used in any execution file. Do NOT call `gh pr create`; the future execution updates the EXISTING draft PR #231 body via `gh pr edit 231`.

## Gate Condition

The future execution PR is mergeable iff: (a) the manifest `02_01_01` row asserts
catalog-only closure with the new token and no longer says "no Step closure"; (b) the two
new rows exist with `catalog_only_closed_zero_materialization`; (c) the vocabulary defines
the new token and cross-references the PR #230 sibling tokens; (d) PR #230 is archived in
INDEX with merge SHA `0c45c490` and the stale "draft" qualifier removed; (e) all 11 E7
validation checks pass (final tracked diff = 6 files = 2 planning + 4 execution; execution
subset = 4; transient `.github/tmp/*` absent; no `PR #<n>` / `PR #<this PR>` placeholder in
any execution file or the PR #231 body — all references are literal `PR #231`); (f) version
is `3.66.0` with a matching CHANGELOG block; (g) the
`@reviewer-adversarial` post-execution Cat F final gate returns APPROVE with zero blockers.
PR #230's closure is preserved untouched throughout.

## Open Questions

- **OQ-M1 (RESOLVED here per reviewer N2):** Summary accounting uses a footnote, not a new
  column. No open decision remains.
- **OQ-A (deferred, NOT in scope):** When does `02_01_02` planning begin? Deferred to a
  separate planner-science cycle AFTER this reconciliation lands. The non-batching rule
  forbids combining it here.
- **OQ-B (deferred, NOT in scope):** The post-materialization CROSS-02-01 audit re-run
  remains REQUIRED for any future materializing step; it is preserved verbatim in the new
  token's definition and is not performed by this plan.

### What this plan preserves (invariant)

PR #230 closure stands: Step `02_01_01` CLOSED at catalog-only layer; Phase 02
`in_progress`; Step `02_01_02` NOT started; Phase 03 NOT started. The CROSS-02-01 artifact
does NOT claim empirical leakage clearance. A future post-materialization CROSS-02-01 audit
remains required. PR #229 §10 artifacts remain distinct from PR #230 CROSS-02-01 artifacts.
No feature column is materialized. No models/splits/baselines/Phase-03. No thesis chapter
prose is changed.

### Forbidden paths (future execution PR MUST NOT touch)

`thesis/chapters/**`; the three status YAMLs (`STEP_STATUS`, `PIPELINE_SECTION_STATUS`,
`PHASE_STATUS`); `ROADMAP.md`; `INVARIANTS.md`; any registry CSV/MD; the §10 verdict-audit
CSV/MD; the CROSS-02-01 JSON/MD (cited, never modified); any validator or its tests; the
per-dataset `research_log.md` AND the root `reports/research_log.md` (PR #230 already wrote
the closure entry; OQ4 asks only for the manifest update); any `sandbox/**` notebook; any
`reports/specs/**`; `.claude/**`; any `src/rts_predict/**` source.

### Reviewer routing

Category F. Pre-execution critique gate: `@reviewer-adversarial` (this critique is
materialized as `planning/current_plan.critique.md` in this PR; verdict APPROVE-WITH-NITS,
zero blockers; nits N1/N2/N3 folded into this plan above). Post-execution final gate:
`@reviewer-adversarial` (Cat F) on the execution diff. 3-round adversarial cap applies
(`feedback_adversarial_cap_execution.md`).
