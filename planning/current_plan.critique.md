---
plan_ref: planning/current_plan.md
created: 2026-05-21
reviewer_model: reviewer-adversarial (Opus 4.7, bounded conditions-satisfied check)
category: A
---

# Critique — feat/sc2egset-02-01-01-section10-audit-persistence

reviewer: reviewer-adversarial (Category A bounded conditions-satisfied check)
base_ref: 5c7ef380d181276bc2f7d4c14b4427e336af781e

> Produced by reviewer-adversarial. Audience: Tomasz + viva preparation.
> Not consumed by executors during persistence-only T02..T06 execution.

## Verdict

**APPROVE-WITH-NITS**

Blocking issues: **None**.

The plan correctly applies all 8 required modifications and all 5 non-blocking
nits from the prior critique chain. The 5 remaining nits (recorded below) are
resolved in this materialized plan by inline reproduction of the verbatim
clause-2 sentence (§5 + §9 of the plan), explicit ordering of the
materialization-prerequisite (§13), explicit `audit_pr` lifecycle
clarification (§6), and explicit non-reuse of PR #216's `partial` token
in §9.

## Source-of-truth note

The reviewer reviewed the immediately previous chat-delivered revised plan
(now materialized as `planning/current_plan.md` on
`feat/sc2egset-02-01-01-section10-audit-persistence`). `planning/current_plan.md`
and `planning/current_plan.critique.md` on `master` were read only as
historical context from merged PR #228 and were not treated as the current
target plan.

## Conditions table

| Condition | Result | Evidence / note |
|---|---:|---|
| Naming / non-closure framing | PASS | Branch `feat/sc2egset-02-01-01-section10-audit-persistence` (no `-closure`). Non-closure disclaimer appears in `current_plan.md` §1 (load-bearing), §Scope, §7 (artifact MD §1 spec), §9 (research_log entry), §12 (CHANGELOG `### Notes` spec), §4 (Forbidden actions: "claiming closure / Phase 02 activation / `02_01_02` authorization anywhere in prose"). Cross-verified against `STEP_STATUS.yaml` (no 02_01_01 entry — Phase 02 absent) and `PHASE_STATUS.yaml` (Phase 02 = `not_started`); the plan correctly leaves both frozen. |
| Artifact CSV schema | PASS | `current_plan.md` §5 enumerates all 23 columns in the stated order. Determinism rules: 26 data rows; row order = frozen registry row order; UTF-8 + `lineterminator="\n"` + `index=False`; reload via `keep_default_na=False`; empty strings (not null/NaN); SHA-256 over raw on-disk bytes; UTC date `YYYY-MM-DD` via `strftime("%Y-%m-%d")`; `git_sha` as a separate column. |
| Safe clause-2 wording | PASS | The verbatim sentence is reproduced TWICE in `current_plan.md`: once in §7 (artifact MD §5 spec) and once in §9 (research_log entry "what this means"). Both occurrences match the required text exactly: "No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121." T05 also requires the same verbatim sentence in `CHANGELOG.md` `### Notes`. (Previous "PASS-WITH-NIT" upgraded to PASS by inline reproduction — nit 1 resolved.) |
| Research-log tokens | PASS | `current_plan.md` §9 requires BOTH `closure_status: still_open` AND `evidence_persistence_state: section10_verdict_audit_persisted_step_open`. The "Decisions taken" subsection explicitly states the non-reuse of PR #216's `closure_status: partial` token with rationale ("PR #216's `partial` denoted 'validators V-1..V-9 are partial coverage toward closure'; this entry denotes 'no closure progress claim at all'"). Target file is the per-dataset `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`; root `reports/research_log.md` is zero-diff (forbidden in §4). |
| Forbidden list completeness | PASS | `current_plan.md` §4 lists: root `reports/research_log.md`; `src/rts_predict/games/aoe2/**`; `data/**` (both top-level and per-dataset); `tests/**`; the validator path; the three status YAMLs; ROADMAP; INVARIANTS; `specs/**`; both registry CSV/MD; `thesis/**`; `notebooks/**`; `.github/workflows/**`; `Makefile`; `scripts/**`. Forbidden actions cover: validator/test mutation; status YAML flips; ROADMAP/INVARIANTS/specs amendment; root research_log write; DuckDB/Parquet/materialized output; new test addition; over-expanded notebook diff; closure/Phase02/02_01_02 claims in prose; `--amend`/`--no-verify`/`--force`/`--no-gpg-sign`. |
| PERSIST falsifier | PASS | `current_plan.md` §10 specifies: (1) reload with `pd.read_csv(..., dtype=str, keep_default_na=False)`; (2) rerun `validate_registry_section10_verdicts(...)` on same frozen inputs; (3) re-encode via same code path; (4) row-by-row + column-by-column comparison; (5) only `audit_executed_at_utc_date`, `audit_pr`, `git_sha` may differ; any other diff HALT (PERSIST fires). Listed as the 10th falsifier in §11 and as a structural halt in §11. Reload assertions enumerated. |
| Artifact MD structure | PASS | `current_plan.md` §7 enumerates §1 disclaimer at top; §2 provenance (all hash + date + spec + PR fields, including `spec_revision_cross_02_03` explicitly listed — nit 5 resolved); §3 aggregate result; §4 falsifier roll-call table (F-1, F-1a, F-1b, F-2..F-7, PERSIST — each "did not fire"); §5 ROADMAP `continue_predicate` verbatim (lines 2060–2066) + three-clause table with inline clause-2 sentence; §6 methodology lineage (spec, validator, notebook, tests); §7 per-row compact 6-column table; §8 cited code/SQL block (Invariant I6). |
| Notebook update scope | PASS | `current_plan.md` §8 limits the diff to EXACTLY ONE new artifact-write cell + EXACTLY ONE banner markdown edit; no `def`/`class`/`lambda` (src frozen); jupytext-paired `.ipynb` synced; no DuckDB connection; no Parquet; no path outside the artifact directory. Structural halt fires if the notebook diff exceeds this scope. |
| Release-tail plan | PASS | `current_plan.md` §12: `pyproject.toml` 3.63.0→3.64.0; `CHANGELOG.md` `[Unreleased]` → `[3.64.0]` with 4 sub-headers re-emitted; `planning/INDEX.md` archive PR #228 (at `5c7ef380`) + set new Active line. Justified by `feat/` prefix → minor bump per `.claude/rules/git-workflow.md`. |
| Reviewer routing / materialization prerequisite | PASS | `current_plan.md` §13 enumerates Steps A/B/C/D in order: **Step A** = THIS planning-only draft PR (parent materializes plan + critique); **Step B** = user/ChatGPT reviews via GitHub connector (materialization prerequisite); **Step C** = `@executor` continues on the same branch (T02..T06); **Step D** = `@reviewer-deep` final gate. Reviewer-adversarial is correctly NOT required again unless reviewer-deep raises a methodology BLOCKER. (Previous FAIL upgraded to PASS by the materialization-prerequisite ordering being made explicit — nit 2 resolved.) |

## Blocking issues

None. The materialization-prerequisite gap from the prior critique was
process-discipline (not methodology). It is resolved at the workflow level
by this draft planning PR being opened BEFORE any execution turn:
`planning/current_plan.md` and `planning/current_plan.critique.md` are
inspectable on GitHub before `@executor` is dispatched, so the future
execution does not rely on stale `master` planning files or on chat memory.

## Materialization prerequisite addendum

**Materialization prerequisite resolved:** the plan is now committed in a
draft planning PR before executor dispatch, so future execution does not
rely on stale master planning files or chat memory.

## Non-blocking nits (record of resolutions)

The five nits from the prior bounded conditions-satisfied check are recorded
here with their resolution status in this materialized plan.

1. **Inline verbatim clause-2 sentence in the plan body.** RESOLVED.
   `current_plan.md` reproduces the verbatim sentence in §7 (artifact MD
   §5) and §9 (research_log entry); T05 also requires it in CHANGELOG
   `### Notes`. The executor can grep-copy it without consulting any
   prior chat history.
2. **Materialization-prerequisite ordering explicit, not implicit.**
   RESOLVED. `current_plan.md` §13 enumerates ordered Steps A/B/C/D with
   "Step A — Planning-only draft PR (THIS PR)" identified as the
   materialization prerequisite that the executor cannot bypass.
3. **`audit_pr` lifecycle pinned.** RESOLVED. `current_plan.md` §6 states:
   the artifact is written with `PR #<TBD>` and is NOT amended
   post-PR-open; the final PR number lands only in CHANGELOG + per-dataset
   research_log. Rationale included: PERSIST excludes `audit_pr` from
   byte-equality, so a placeholder is safe at write time, but amending
   post-PR-open would produce a self-amending artifact whose hashes
   change post-merge.
4. **R-7 framing anchor citable, not implicit.** RESOLVED at the prose
   level — `current_plan.md` §14 R-7 anchors framing to PR #228's
   approved Round-1 / Round-2 baseline; the merged
   `planning/current_plan.critique.md` on master remains accessible in
   git history. (A precise line-range cite would be optional polish but
   is not load-bearing.)
5. **`spec_revision_cross_02_03` explicit in artifact MD §2.** RESOLVED.
   `current_plan.md` §7 (artifact MD §2 spec) explicitly lists
   `spec_revision_cross_02_03 = CROSS-02-03-v1.0.1` among the provenance
   fields, mirroring the CSV column.

## Invariants check

All 8 scientific invariants assessed (yes / no / n-a + evidence pointer).

- **#1 (per-player split)** — n-a — Persistence increment over a frozen
  registry; no train/test split is constructed.
- **#2 (canonical player identifier)** — n-a — No player rows; this is
  catalog-level metadata.
- **#3 (strict temporal discipline — match_time < T)** — yes — The
  registry's `allowed_cutoff_rule` column is audited declaratively by the
  PR #228 validator; this PR persists the verdict only.
- **#4 (prediction target is next game given prior history)** — n-a —
  Catalog-level audit; no prediction is produced.
- **#5 (symmetric player treatment)** — n-a — Catalog-level audit; not a
  feature.
- **#6 (SQL / code shipped with findings)** — yes — `current_plan.md`
  §7 (artifact MD §8) requires the verbatim validator signature + notebook
  call site in the persisted MD; the CSV captures `validator_module` +
  `validator_module_sha256` + `git_sha` to make the lineage auditable.
- **#7 (no magic numbers)** — yes — All thresholds inherited from the
  frozen validator and the locked spec `CROSS-02-03-v1.0.1`; the artifact
  records the spec revision tag for future drift detection.
- **#8 (cross-game protocol)** — n-a — SC2-only catalog increment; AoE2
  paths are forbidden in §4.

## Temporal discipline assessment

This is a design-time evidence-persistence increment over an in-memory
audit result that was already approved by the PR #228 reviewer-adversarial
chain. No feature computation, no rolling aggregate, no head-to-head
window, no within-tournament feature is introduced. The strict temporal
discipline of the underlying registry rows (`history_time < target_time`
for history rows; `event.loop <= cutoff_loop` for in-game rows) is audited
declaratively by the PR #228 validator (F-3, F-4 falsifiers); this PR
persists the audit verdict and the PERSIST falsifier guarantees
byte-equivalence with a fresh validator run on the same frozen inputs.

## Defensibility check

- **Choice:** Drop `STEP_STATUS.yaml` update from this PR; persist only
  artifacts + research_log entry; defer the status-chain triad to a
  separate closure PR.
  - **Strongest objection:** The persisted artifact looks like "Step 02_01_01
    is closing" — a future reader scanning `02_01_01_section10_verdict_audit.{csv,md}`
    might mistake the artifact for closure evidence.
  - **Rebuttal evidence needed:** The non-closure disclaimer appears in 4
    loci (artifact MD §1 at the TOP, research_log entry, CHANGELOG `### Notes`,
    PR body); the artifact filename does not contain "closure"; the branch
    name does not contain "closure"; the PR title example does not claim
    closure; the `closure_status: still_open` token in the research_log
    entry is machine-parseable.

- **Choice:** Use deterministic `audit_executed_at_utc_date` (date only,
  not timestamp), and a separate `git_sha` column.
  - **Strongest objection:** Date-only loses sub-day reproducibility
    information; if the audit is re-run twice on the same day with
    different commits, only `git_sha` distinguishes them.
  - **Rebuttal evidence needed:** That is the intended behaviour — Invariant
    I6 demands byte-identical artifacts on re-run, and `git_sha` IS the
    sub-day distinguishing field. A future audit comparing two runs would
    look at `git_sha` first (commit equality), then `audit_executed_at_utc_date`
    (audit recency), then the three SHA-256 hashes (input/code drift).

- **Choice:** Add a new falsifier (PERSIST) for this PR even though no new
  scientific claim is introduced.
  - **Strongest objection:** A persistence increment shouldn't need its own
    falsifier; it's a clerical step.
  - **Rebuttal evidence needed:** Persistence carries a real assertion (the
    on-disk encoding must be byte-equivalent to a fresh validator run).
    Without PERSIST, a notebook-side drift between in-memory and on-disk
    encoding could ship undetected. PERSIST converts the clerical step
    into a self-falsifying step.

- **Choice:** Use distinct research_log tokens
  (`closure_status: still_open` + `evidence_persistence_state: section10_verdict_audit_persisted_step_open`)
  instead of reusing PR #216's `closure_status: partial`.
  - **Strongest objection:** Two tokens are more complex than one; the
    `closure_status: partial` token already exists and could be reused.
  - **Rebuttal evidence needed:** The two epistemic states differ. PR #216's
    `partial` denoted "validators V-1..V-9 are partial coverage toward
    closure" (i.e., closure is partially-progressed). This PR denotes
    "no closure progress claim at all" (i.e., the §10 audit increment did
    not advance overall closure state). Reusing `partial` would conflate
    those two states and produce an unreadable closure-progression
    history for Step 02_01_01.

## Likely supervisor / committee questions

- On methodology:
  - "Why didn't you just flip `STEP_STATUS.yaml` if all 26 rows passed?"
    → Because the ROADMAP `continue_predicate` has THREE clauses, and only
    clause-3 is satisfied by this audit. Clause-1 was satisfied by PR #216;
    clause-2 is vacuously satisfied at the catalog layer but becomes
    non-vacuous at first materialization. The closure decision is a separate
    methodology gate, not a mechanical consequence of clause-3.
  - "Why is `materialized_column_count = 0` not a contradiction with the
    registry having 26 feature families?"
    → A feature family in the registry is a *catalog declaration* of an
    intended feature; "materialized" per `02_01_leakage_audit_protocol.md`
    §4 lines 117–121 means a feature column persisted to DuckDB or Parquet
    for the training pipeline. None of the 26 families have been
    materialized yet; the catalog is the design-time blueprint.

- On data:
  - "What happens if the registry CSV is regenerated and the row order
    changes?"
    → `registry_csv_sha256` would change; a future audit comparing the
    persisted artifact against a regenerated registry would detect the
    drift via hash mismatch, and the persisted artifact would be flagged
    as stale (not silently reused).

- On evaluation:
  - "Why no new pytest test for the persistence step?"
    → `tests/**` is forbidden in this PR (validator + tests frozen by
    PR #228). The PERSIST byte-equivalence check is enforced inside the
    notebook cell, not as a pytest test, because the assertion is on the
    on-disk encoding of an artifact produced by this PR specifically, not
    on the validator's behaviour.

## Known weaknesses

- The artifact relies on the executor running the notebook fresh at PR
  time. If the executor reuses a stale `.ipynb` output from local
  experimentation, the PERSIST check would fire (or worse, if the executor
  bypasses re-run, the artifact could diverge from the validator's
  current output). Mitigation: the executor MUST run the artifact-write
  cell as part of the PR commit, not paste in a stale file.
- The artifact uses `PR #<TBD>` as the `audit_pr` placeholder and does not
  amend post-PR-open. A future reader scanning the artifact in isolation
  would see `PR #<TBD>` and have to cross-reference the CHANGELOG entry
  to find the actual PR number. This is a defensibility trade-off chosen
  over a self-amending artifact (rejected because amending would change
  hashes post-merge).

## Alternatives considered and rejected

- **Alternative:** Include a `STEP_STATUS.yaml` row flip in the same PR
  to close Step 02_01_01.
  - **Rejected because:** The repo schema exposes only `not_started`,
    `in_progress`, `complete` — no non-deriving `evidence_recorded` token.
    Any flip would mechanically cascade up `PIPELINE_SECTION_STATUS.yaml`
    and `PHASE_STATUS.yaml`, which this PR is explicitly forbidden from
    touching. Furthermore, closure requires a fresh reviewer-adversarial
    methodology gate, which this persistence-only PR is not the right
    container for.
  - **Reconsider if:** The status-schema is extended with a non-deriving
    `evidence_recorded` token, OR a separate closure PR is planned with
    its own reviewer-adversarial gate.

- **Alternative:** Reuse PR #216's `closure_status: partial` token in the
  new research_log entry.
  - **Rejected because:** Token collision with two distinct epistemic
    states (PR #216 = "validators provide partial coverage toward closure";
    this PR = "no closure progress claim at all"). Reuse would produce
    an unreadable closure-progression history.
  - **Reconsider if:** A future research-log overhaul introduces a
    higher-resolution status vocabulary that can encode both meanings
    without ambiguity.

- **Alternative:** Write the PM-1 entry to the root `reports/research_log.md`.
  - **Rejected because:** `.claude/ml-protocol.md` lines 51–54 require
    per-dataset entries in per-dataset logs; the root CROSS log is for
    cross-cutting work only.
  - **Reconsider if:** The work is reclassified as cross-cutting (it is
    not).

- **Alternative:** Use a runtime `audit_run_at_utc` timestamp
  (`YYYY-MM-DD HH:MM:SS`) instead of a date-only column.
  - **Rejected because:** A runtime timestamp would produce a different
    artifact byte-by-byte on every re-run, breaking Invariant I6
    (byte-identical reproducibility). The PERSIST falsifier could not
    represent this without trivially excluding timestamps from comparison.
  - **Reconsider if:** A future workflow needs sub-day audit timing (none
    currently).

## Citations

- `[OPINION]` The validator-vs-registry-staleness defense relies on the
  three SHA-256 hash columns being computed deterministically from
  on-disk bytes. No external citation needed — the discipline is internal
  to `.claude/scientific-invariants.md` Invariant I6.
- `[OPINION]` The non-closure framing's defensibility relies on the
  ROADMAP `continue_predicate`'s three-clause structure being a load-bearing
  closure gate, not a heuristic. Internal source: SC2EGSet `ROADMAP.md`
  lines 2060–2066 (verbatim quoted in `current_plan.md` §7 spec).
- Workflow discipline references: `.claude/rules/data-analysis-lineage.md`
  (Artifact discipline, Non-batching rule, Agent and model routing
  discipline); `.claude/rules/git-workflow.md` (minor bump for feat/refactor/docs);
  `.claude/ml-protocol.md` (per-dataset vs. root research_log discipline).
