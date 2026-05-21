---
plan_id: feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit
plan_revision: v3
supersedes_plan_revision: v2 (Outcome A'(i), returned BLOCKING-CONDITIONS by reviewer-adversarial; v1 was Outcome A, returned HOLD-REPLAN)
date: 2026-05-21
category: A
branch: feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit
phase: "02"
pipeline_section: "02_01"
step: "02_01_01"
dataset: sc2egset
game: sc2
base_ref: a14dc547bf19245ddc205048dbaf9cb6b11d9400
master_head_at_plan_time: a14dc547bf19245ddc205048dbaf9cb6b11d9400
version_bump: 3.64.0 -> 3.65.0
outcome_verdict: A'(i)-APPROVE
gate_action: close Step 02_01_01 with zero-materialization CROSS-02-01 leakage-audit artifact pair
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
post_execution_reviewer: reviewer-adversarial (Cat A) as T11; reviewer-deep as final-gate fallback per §9; ordering = Route A (final gate while DRAFT → `gh pr ready 230` on APPROVE → NO merge)
---

<!-- v3 EDIT LEDGER (vs v2):
  BLOCKING condition C1 (OQ1 normalization_fit_scope new string):
    - JSON value flipped from 'N/A_no_features_materialized' to 'training_fold_only' (alternative beta).
    - JSON notes prose: OQ1 invitation replaced with v3 resolution rationale.
    - MD sec 1, sec 7: updated to reflect resolved beta.
    - T05 Decisions taken: records resolved beta.
    - Sec 5 disclaimer 7: rewritten as RESOLVED-statement.
    - Sec 10 R1: downgraded HIGH to LOW.
    - Sec 11 OQ1: RESOLVED pre-execution.
    - Unknown U1: RESOLVED block.
    - Sec 1 outcome adjudication: rationale + bullets updated.
  BLOCKING condition C2 (root research_log CROSS entry violates ml-protocol):
    - T05.b removed in entirety; replaced by REMOVED-justification block.
    - Scope clause: CROSS entry mention removed.
    - CHANGELOG Added: root research_log line removed.
    - Sec 6 manifest: dropped from 11 to 10 entries (9 diff-touching); root research_log removed.
    - Q8 manifest: same drop; tail prose updated.
    - T08 pre-merge validation: '11-file manifest' -> '9 diff-touching files'.
    - Sec 11 OQ2: cites this PR's per-dataset entry as the precedent path.
  Nit 3 (T02a.2 write technique): heredoc option dropped from executor menu.
  Nit 4 (T02a.3 MD sec 8): explicit 'Audit queries: none - vacuously satisfied' section added.
  Nit 5 (T07 visual-verify): replaced with explicit grep -c / grep -n checks.
  Branch name: long form preserved per user explicit specification:
    feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit
  v3 supersedes v2 (Outcome A'(i), returned BLOCKING-CONDITIONS by reviewer-adversarial).
  v2 superseded v1 (Outcome A, returned HOLD-REPLAN by reviewer-adversarial).
-->

# SC2EGSet Phase 02 / Step 02_01_01 — Closure plan v3 (Outcome A'(i): zero-materialization CROSS-02-01 leakage-audit artifact pair; BLOCKING conditions C1 + C2 resolved)

## Scope

Close SC2EGSet Phase 02 / Step `02_01_01` (Feature-family registry skeleton) by:

1. Emitting a CROSS-02-01-v1.0.1-compliant zero-materialization leakage-audit artifact pair at the spec-named path `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}`. This satisfies §3 (artifact-at-named-path) and §5(c) (both files present) unconditionally, and satisfies §5(a) (every materialized column appears in `features_audited`) vacuously because the materialized set is empty at the catalog layer.
2. Flipping STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS to record that the step and its enclosing 02_01 pipeline section are now `complete`, and Phase 02 is now `in_progress`.
3. Recording a closure entry in the per-dataset `research_log.md` (sc2egset). NO CROSS entry in root `reports/research_log.md` is added by THIS PR (per `.claude/ml-protocol.md` lines 51-54: per-dataset closure is a single-dataset status flip, not a cross-dataset decision).
4. Doing the standard release tail (CHANGELOG entry, version bump 3.64.0 -> 3.65.0, planning/INDEX.md archive shuffle).

This is a single-PR closure of Step 02_01_01. The closure neither opens Step 02_01_02 nor begins any 02_01 materialization work. No notebook, no source code, no validator, no spec, no ROADMAP body, no registry CSV/MD, no Phase 01 artifact, no INVARIANTS.md, no thesis chapter is touched.

The zero-materialization artifact pair is the specific Outcome-A'(i) resolution prescribed by `reviewer-adversarial` in the v1 HOLD-REPLAN verdict. It is NOT a substitute for the PR #229 §10 verdict-audit artifact pair, and it is NOT a substitute for a future post-materialization CROSS-02-01 audit that any later Step 02_01_02 will require.

## Problem statement

The previous closure plan (v1, Outcome A) was returned HOLD-REPLAN. The load-bearing reviewer-adversarial blocker was a conflation of two distinct clauses of CROSS-02-01-v1.0.1:

- **§5(a)** ("Every feature column materialized in 02_01 appears in `features_audited`") IS vacuously satisfied on the empty materialized set at the catalog layer.
- **§3** (line 90) UNCONDITIONALLY requires a JSON artifact at `reports/artifacts/02_<step>/leakage_audit_<dataset>.json`.
- **§5(c)** (line 145) UNCONDITIONALLY requires "Both the JSON artifact and the sibling Markdown report are present at the prescribed path".

§5(a) vacuity does not waive §3 or §5(c). The persisted `02_01_01_section10_verdict_audit.{csv,md}` (PR #229) is a CROSS-02-03 §10 design-time verdict artifact per its own §6 lineage statement, NOT the CROSS-02-01 leakage-audit JSON that §3 names. With those two artifacts absent at the spec-named path, the v1 plan would have closed the step against a gate condition that the spec textually fails.

The reviewer's preferred resolution is **A'(i)**: emit a zero-materialization CROSS-02-01 leakage-audit JSON+MD pair at the spec-named path that

- is honest about the catalog-only nature of Step 02_01_01 (empty `features_audited`, no real cutoff filter applied, no normalizer fit, no target encoding),
- passes the §3 schema by populating every required field with a defensible value,
- justifies its `verdict = "PASS"` only on the §5(a) vacuity, not on any empirical leakage clearance,
- documents that this artifact pair is a layered closure device for a catalog-only step, not a substitute for a future post-materialization audit,
- raises any spec-strict-reading ambiguities as open questions for `reviewer-adversarial` to overrule, with explicit overrule-invitation prose in the JSON `notes` field.

The v1 reviewer-adversarial gate also flagged 5 non-blocker fixes (toggle disclosure on status reopen, PR #228 vs PR #229 SHA disambiguation, manifest in forbidden list, INVARIANTS.md hedge, T05 "authorise" softening); the v2 plan folded all five. The v2 reviewer-adversarial gate then returned 2 BLOCKING conditions (C1: `normalization_fit_scope` new string; C2: T05.b CROSS entry violates ml-protocol) and 3 non-blocker nits (Nit 3: drop heredoc from T02a.2 write technique; Nit 4: add MD sec 8 "Audit queries: none - vacuously satisfied"; Nit 5: replace T07 "visually verify" with explicit grep checks). This v3 plan resolves BOTH BLOCKING conditions pre-execution and folds all 3 nits into the appropriate sections (T02a.2 write technique, T02a.3 MD sec 8, T07 explicit-grep verification).

## Assumptions & Unknowns

### Assumption A1 (replacement for the v1 blocker assumption)

A zero-materialization CROSS-02-01 leakage-audit JSON+MD pair at the spec-named path `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` satisfies §3 (artifact-at-named-path), §5(c) (both files present at prescribed path), and §5(a) (every materialized column appears in `features_audited` — vacuously satisfied because the materialized set is empty at the catalog-only registry layer). The `verdict = "PASS"` is justified on §5(a) vacuity, not on any empirical leakage clearance.

### Assumption A2 (catalog-only step semantics)

Step 02_01_01 as scoped through PR #216 and PR #229 is a catalog-only step: no feature column is materialized to DuckDB or Parquet at the registry layer; PR #216 emitted the registry CSV+MD; PR #228 implemented the §10 verdict-audit validator in-memory; PR #229 persisted §10 evidence on disk. The on-disk state at master `a14dc547` is consistent with this scoping: no DuckDB VIEW or materialized table introduces a Phase 02 feature column, no Parquet feature table exists. Therefore `features_audited = []` is empirically correct, not an editorial choice.

### Assumption A3 (closure status semantics)

`STEP_STATUS.yaml`'s `02_01_01: complete` plus `PIPELINE_SECTION_STATUS.yaml`'s `02_01: complete` plus `PHASE_STATUS.yaml`'s `Phase 02: in_progress` are the closure tokens for "the catalog-only registry skeleton step is done and the Phase 02 work has officially begun, even though no feature column has been materialized." This is the same semantics the v1 plan used. It is consistent with `docs/PHASES.md`'s 8-section canonical structure (02_01..02_08) — closure of one section does not require all sections.

### Assumption A4 (PIPELINE_SECTION_STATUS reopen behaviour is documented, not silent revisionism)

Per the YAML-derivation rule documented in `STEP_STATUS.yaml` header lines and `PIPELINE_SECTION_STATUS.yaml` header lines: "Pipeline section is complete when ALL its steps are complete." Adding a future Step `02_01_02` to STEP_STATUS as `in_progress` will mechanically flip the derived `02_01: complete` back to `02_01: in_progress`. This is intended derivation behaviour, NOT silent revisionism. T05 (per-dataset research_log entry) and T06 (CHANGELOG entry) MUST surface this reopen behaviour as an explicit bullet so that any future reviewer sees the closure-then-reopen sequence as designed-in, not a status-tracking bug.

### Assumption A5 (continue_predicate three-clause read)

ROADMAP `continue_predicate` (lines 2060-2066, verbatim from the read above) decomposes into three clauses:
- **C1** "Step 02_01_01 has reached its CSV + MD artifact-check at a future PR" — SATISFIED by PR #216 (registry CSV+MD on disk).
- **C2** "the CROSS-02-01-v1.0.1 post-materialization audit gate has been re-run for any feature column the registry triggers materialization of" — SATISFIED by the new zero-materialization JSON+MD pair this plan adds at T02a, because the registry triggers materialization of zero feature columns at the catalog layer. The audit re-run scope is therefore "zero feature columns", and the artifact pair at the spec-named path makes that re-run on-disk and citable.
- **C3** "a per-family CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row" — SATISFIED by PR #229 (§10 verdict-audit CSV+MD on disk for all 26 rows).

Three clauses ALL satisfied at master `a14dc547` after this PR lands. The continue_predicate is therefore met and the closure is well-formed.

### Unknown U1 (RESOLVED in v3: spec-strict reading of `normalization_fit_scope` for catalog-only step)

The §3 schema requires `normalization_fit_scope = "training_fold_only"` for PASS. The catalog-only step fits no normalizer. The v2 plan recommended option (alpha): use `"N/A_no_features_materialized"` (a NEW string not in the spec's enumerated pass values) with OQ1 invitation for reviewer-adversarial overrule. The v2 reviewer-adversarial gate ruled this BLOCKING (the artifact would assert `verdict = "PASS"` while carrying a schema-violating field). v3 RESOLVES this by adopting option (beta): `"training_fold_only"` — the spec-permitted value — with vacuous-satisfaction rationale: no normalizer fit took place at the catalog-only registry layer; the pass condition is vacuously met on empty `features_audited`. This treatment is symmetric to the field values used for `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously). The schema-strict reading is preserved; no new strings are introduced. OQ1 is closed pre-execution (see §11).

### Unknown U2 (spec-strict reading of structural-check fields for catalog-only step)

The §3 schema requires `cutoff_time_filter_structural_check = "pass"` and `reference_window_assertion = "pass"` for PASS. The registry rows DO declare cutoff rules (history rows use `history_time < target_time`; in_game rows use `event.loop <= cutoff_loop`). But these are catalog declarations, not actual SQL filters applied to feature data. Reasonable resolution: use `"pass"` (vacuously — no columns materialized so no actual cutoff filter is structurally applied), and document in the JSON `notes` field and in the MD that the catalog declarations are CROSS-02-03 §10 territory and are audited by PR #229's §10 evidence artifact, not by this CROSS-02-01 leakage audit. The reasonable value is `"pass"` rather than a new string because no fact-of-the-matter is misrepresented (no filter was applied; no filter was wrong).

### Unknown U3 (spec_version field exact string)

The §3 schema requires `spec_version = "CROSS-02-01-v1"`. The spec file frontmatter is `spec_id: CROSS-02-01-v1.0.1` and `version: CROSS-02-01-v1.0.1`. The §3 schema text reads `"CROSS-02-01-v1"`, which is the major-version prefix. This plan uses `"CROSS-02-01-v1"` (spec-text literal) and records the actual frozen point-release (`CROSS-02-01-v1.0.1`) in the `notes` field. No OQ — this matches the spec's required value verbatim.

### Unknown U4 (no Phase 02 entries in STEP_STATUS or PIPELINE_SECTION_STATUS today)

STEP_STATUS.yaml currently has 38 entries, all Phase 01; PIPELINE_SECTION_STATUS.yaml currently has 6 Phase 01 sections; PHASE_STATUS.yaml has Phase 02 = `not_started`. Inserting `02_01_01` and `02_01` is the first Phase 02 mutation across these three files. The plan must add `02_01_01` to STEP_STATUS with `pipeline_section: "02_01"`, add `02_01` to PIPELINE_SECTION_STATUS with `phase: "02"` and `name: "Pre-Game vs In-Game Boundary"` per `docs/PHASES.md`, and flip PHASE_STATUS Phase 02 from `not_started` to `in_progress`.

## Literature Context

- `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1, LOCKED 2026-04-26) — the spec whose §3, §4, and §5 govern this closure. The catalog-only zero-materialization closure is the methodologically defensible reading of the spec at the registry-skeleton step: §5(a) vacuity is real on the empty set, and §3+§5(c) artifact-presence is satisfied by emitting the spec-named JSON+MD pair with empty `features_audited`. The spec's enforcement mechanism (§5 line 149) is convention-based and gated by `reviewer-adversarial` review; this plan therefore explicitly invokes `reviewer-adversarial` pre-execution AND post-execution to honor the enforcement convention.
- `.claude/scientific-invariants.md` Invariant I3 (no data from game T or later for predicting T) — satisfied vacuously by this closure because no feature column is materialized; I3 is in scope only for post-materialization audits.
- `.claude/rules/data-analysis-lineage.md` (Artifact discipline + Stop conditions + Non-batching rule) — satisfied: the zero-materialization artifact emission is the canonical lineage for a catalog-only step's leakage-audit gate, and the closure batches only what a single closure PR may batch (status flips, lineage artifact, release tail). No notebook is created, no validator is re-run, no surprising empirical result is encoded.
- `docs/PHASES.md` — the canonical 8-section Phase 02 structure (02_01..02_08) supports closing 02_01 while leaving 02_02..02_08 not started.
- `thesis/pass2_evidence/notebook_regeneration_manifest.md` — this manifest records on-disk stale/intact status for every Phase 02 audit artifact per CROSS-02-01-v1.0.1 §4 lines 123-133. This plan does NOT update the manifest in this PR (manifest is in the forbidden list per §7 and Q9), but flags Open Question OQ4 to instruct the next planner-science session to update the manifest's status vocabulary with the new closure token.

## Execution steps

Branch creation is T01. The new zero-materialization audit artifact pair is T02a. STEP_STATUS, PIPELINE_SECTION_STATUS, and PHASE_STATUS edits are T02..T04. Per-dataset research_log entry only (NO root / CROSS entry, per `.claude/ml-protocol.md` lines 51-54) is T05; T05.b was REMOVED in v3 per BLOCKING condition C2. CHANGELOG, version bump, and planning/INDEX.md shuffle are T06..T07. The validation-and-PR steps are T08..T11.

### T01 Branch creation

- Create branch `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit` from `master` at HEAD `a14dc547bf19245ddc205048dbaf9cb6b11d9400`.
- Single bash command, `&&`-chained.
- Allowed files: none (branch-only).
- Forbidden files: any.
- Stop condition: `git status` reports clean tree on the new branch with no diff.

### T02a Emit zero-materialization CROSS-02-01 leakage-audit artifact pair (NEW — replaces v1 vacuity claim)

This is the load-bearing new task added by this revision. It creates the two artifacts whose absence triggered the v1 HOLD-REPLAN.

#### T02a.1 Create parent directory

- Bash command (single-line): `mkdir -p src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01`.
- Stop condition: directory exists per `ls -la`.

#### T02a.2 Write `leakage_audit_sc2egset.json`

Target path: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json`.

The JSON MUST contain every §3 field. Exact field values:

```
{
  "spec_version": "CROSS-02-01-v1",
  "dataset": "sc2egset",
  "phase_02_step": "02_01_01",
  "audit_date": "2026-05-21",
  "future_leak_count": 0,
  "post_game_token_violations": 0,
  "normalization_fit_scope": "training_fold_only",
  "target_encoding_fold_awareness": "N/A_no_target_encoding",
  "cutoff_time_filter_structural_check": "pass",
  "reference_window_assertion": "pass",
  "features_audited": [],
  "verdict": "PASS",
  "notes": "Zero-materialization closure of Step 02_01_01 (catalog-only registry skeleton). features_audited is empty because no feature column is materialized to DuckDB (no VIEW or table introducing a Phase 02 feature column) or to Parquet at the registry-skeleton layer; PR #216 emitted the registry CSV+MD only, PR #228 added the in-memory PM-1 §10 verdict-audit validator, and PR #229 persisted the §10 verdict-audit CSV+MD on disk. verdict='PASS' is justified on CROSS-02-01-v1.0.1 §5(a) vacuity (every materialized column appears in features_audited — vacuously true on the empty set) plus CROSS-02-01-v1.0.1 §3 / §5(c) artifact-presence at the spec-named path. This artifact is NOT a substitute for the PR #229 CROSS-02-03 §10 verdict-audit pair (which records per-family design-time verdicts for all 26 catalog rows) and is NOT a substitute for a future post-materialization CROSS-02-01 audit that any later Step 02_01_02 (or other 02_01 materialization step) will require, at which point features_audited will be non-empty. The actual frozen spec point-release is CROSS-02-01-v1.0.1 (LOCKED 2026-04-26); the spec_version field uses the §3-prescribed major-version prefix 'CROSS-02-01-v1'. RESOLVED pre-execution (v3, alternative beta chosen): no normalizer was fit at the catalog-only registry layer; the §3 pass condition `training_fold_only` is vacuously satisfied on empty features_audited; this treatment is symmetric to the field values used for `target_encoding_fold_awareness` (`N/A_no_target_encoding` - spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously). The structural-check fields (cutoff_time_filter_structural_check, reference_window_assertion) use 'pass' vacuously because no real SQL filter was applied to feature data; the catalog's declared cutoff rules (history rows: history_time < target_time; in_game rows: event.loop <= cutoff_loop) are CROSS-02-03 §10 design-time declarations audited by PR #229's §10 evidence artifact, not by this CROSS-02-01 leakage audit."
}
```

Constraints on the JSON write:
- Use either `python -c "import json; json.dump({...}, open('path','w'), indent=2)"` (canonical single-line method) or the Write tool. Do NOT use a `cat > … << 'EOF' … EOF` heredoc (zsh breaks heredoc-in-quoted-argument forms per memory `feedback_git_commit_format.md`). The executor MUST preserve the field order and JSON-validity (lint with `python -m json.tool` after write).
- The JSON MUST be UTF-8, LF-line-ended, terminated with a trailing newline.
- The `notes` field is the single load-bearing prose field; it documents the catalog-only step status, the §5(a) vacuity argument, the §3+§5(c) artifact-presence argument, the non-substitution disclaimer (this artifact does NOT replace PR #229's §10 evidence, does NOT replace a future post-materialization audit), and the v3 RESOLVED-pre-execution rationale for the `normalization_fit_scope = training_fold_only` (alternative beta) choice.

#### T02a.3 Write `leakage_audit_sc2egset.md`

Target path: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md`.

The MD MUST contain the following sections in order. Section bodies are summarised here; the executor writes the full prose per the spec:

1. **Top non-overclaim disclaimer** (one paragraph) — this artifact is the CROSS-02-01-v1.0.1 leakage-audit artifact for the catalog-only Step 02_01_01; it does NOT claim empirical leakage clearance for any materialized feature column (there are none); it does NOT substitute for the PR #229 CROSS-02-03 §10 verdict-audit pair; it does NOT substitute for a future post-materialization CROSS-02-01 audit; `verdict = "PASS"` is justified solely on §5(a) vacuity plus §3 / §5(c) artifact-presence at the spec-named path. (v3 note: the `normalization_fit_scope = "training_fold_only"` choice is the alternative beta resolution, applied pre-execution per the v2 reviewer-adversarial BLOCKING condition C1; the spec-permitted value is vacuously satisfied on empty `features_audited`.)

2. **§3 spec citation (verbatim)** — quote the §3 required JSON fields table (lines 92-107) and lines 109, 111 (sibling MD required, both committed before 02_01 exit). Cite the spec file path: `reports/specs/02_01_leakage_audit_protocol.md`.

3. **§5(a) vacuity argument** — explain that "Every feature column materialized in 02_01 appears in `features_audited`" is vacuously satisfied on the empty materialized set at the catalog layer (zero materialized columns implies the universal quantifier is vacuously true). Cite §5 line 141.

4. **§3 / §5(c) artifact-presence argument** — explain that this JSON file and this MD file at `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` satisfy §3 line 90 (JSON at spec-named path) and §5(c) line 145 (both JSON and sibling MD at prescribed path). The spec-named path is `reports/artifacts/02_01_*/leakage_audit_<dataset>.{json,md}` per the wildcard in §5(c); this artifact pair uses `02_01_01` as the concrete step value per §3 line 90 example.

5. **Explicit non-substitution statement** — paragraph stating:
   - this artifact is NOT a substitute for the PR #229 §10 verdict-audit CSV+MD pair at `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.{csv,md}` (which audits CROSS-02-03 §10 design-time per-family verdicts for all 26 catalog rows);
   - this artifact is NOT a substitute for a future post-materialization CROSS-02-01 audit that any later 02_01 step (e.g., 02_01_02) will require once it materializes the first feature column;
   - this artifact does NOT make Step 02_01_01 a materialization step. Step 02_01_01 remains catalog-only.

6. **Verdict justification** — `verdict = "PASS"`. Justified per §5(a) vacuity (empty set, universal quantifier vacuously satisfied) plus §3 / §5(c) artifact-presence at the spec-named path. NOT justified on any empirical leakage clearance (none was performed because no feature column was audited; `future_leak_count = 0` and `post_game_token_violations = 0` are vacuously true on empty `features_audited = []`).

7. **OQ1 RESOLVED pre-execution (v3 cross-reference)** — the JSON `notes` field documents the v3 RESOLVED-pre-execution rationale for the `normalization_fit_scope = "training_fold_only"` choice (alternative beta, the spec-permitted PASS value, vacuously satisfied on empty `features_audited`). No `reviewer-adversarial` overrule is invited. This treatment is symmetric to the field values used for `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously). The CROSS-02-01-v1.0.1 §3 line 109 "SQL verbatim per Invariant I6" requirement is vacuously satisfied because no queries were executed (no feature materialization, so no SQL was produced).

8. **Audit queries: none - vacuously satisfied** - the CROSS-02-01-v1.0.1 §3 line 109 "SQL verbatim per Invariant I6" requirement is vacuously satisfied because no queries were executed (no feature materialization, so no SQL was produced). This sentence MUST appear as a standalone section per Nit 4 of the v2 reviewer-adversarial gate.

Constraints on the MD write:
- The MD MUST be UTF-8, LF-line-ended, with a trailing newline.
- The MD MUST NOT contain SQL (this is an audit-artifact stub for a catalog-only step; no SQL queries were executed). The spec's §3 requirement that the MD carry SQL verbatim per Invariant I6 is vacuously satisfied (no queries were run; no queries to record).
- The MD MUST cite the spec path verbatim: `reports/specs/02_01_leakage_audit_protocol.md`.

#### T02a.4 Falsifier: validate the JSON against §3 schema

- After writing, run a single-line `python -m json.tool src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json` to confirm the file is valid JSON.
- Run a single-line `python -c "import json,sys; d=json.load(open('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json')); req=['spec_version','dataset','phase_02_step','audit_date','future_leak_count','post_game_token_violations','normalization_fit_scope','target_encoding_fold_awareness','cutoff_time_filter_structural_check','reference_window_assertion','features_audited','verdict']; missing=[k for k in req if k not in d]; sys.exit(0 if not missing else 1)"` to confirm every §3 required field is present. Stop condition: exit code 0.
- If either falsifier fails: HALT before T02..T07; do not proceed; report to the parent session; do not commit anything.

Allowed files: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json` and `.md` (both NEW).
Forbidden files: any other.
Stop condition: both files exist on disk; JSON validates against §3 required-fields list; MD contains all 7 prescribed sections.

### T02 Insert `02_01_01: complete` into STEP_STATUS.yaml

- Target file: `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`.
- Insertion point: at the end of the existing 38-entry `steps:` map (preserving file order; do not re-sort earlier Phase 01 entries).
- New entry:
  ```yaml
    "02_01_01":
      name: "Feature-family registry skeleton"
      pipeline_section: "02_01"
      status: complete
  ```
- Edit technique: single-line `python` or single-line `Edit`-tool call; preserve file's exact indentation (2 spaces), trailing newline, comment header.
- Allowed files: STEP_STATUS.yaml only.
- Forbidden files: any other.
- Stop condition: `grep -c '"02_01_01"' src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` returns >= 1; total entry count is 39; YAML parses (`python -c "import yaml; yaml.safe_load(open('...'))"` exits 0).

### T03 Insert `02_01: complete` into PIPELINE_SECTION_STATUS.yaml

- Target file: `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`.
- Insertion point: at the end of the existing 6-entry `pipeline_sections:` map.
- New entry:
  ```yaml
    "02_01":
      name: "Pre-Game vs In-Game Boundary"
      phase: "02"
      status: complete
  ```
- The `name` value matches `docs/PHASES.md` Phase 02 §02_01 exactly.
- Allowed files: PIPELINE_SECTION_STATUS.yaml only.
- Forbidden files: any other.
- Stop condition: YAML parses; the new section is present with status `complete` and phase `02`; the YAML-derivation chain documented in the file header is consistent (every step under section 02_01 in STEP_STATUS is `complete`).

### T04 Flip Phase 02 from `not_started` to `in_progress` in PHASE_STATUS.yaml

- Target file: `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`.
- Surgical edit: change the single `status: not_started` line on the Phase `"02"` block to `status: in_progress`. Do NOT touch Phase 01 or Phases 03..07.
- Allowed files: PHASE_STATUS.yaml only.
- Forbidden files: any other.
- Stop condition: YAML parses; Phase 02 status is `in_progress`; all other phase statuses are unchanged from master.

### T05 Per-dataset research_log closure entry

- Target file: `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`.
- Insertion point: at the very top of the file, immediately after the existing `# Research Log — SC2 / sc2egset` header and its trailing `---` separator. The new entry becomes the topmost dated entry; the existing 2026-05-21 PR #229 entry becomes the second entry (do not modify it).
- Required entry fields (using the existing per-dataset research_log format):
  - **date_iso:** `2026-05-21` (ISO YYYY-MM-DD per memory).
  - **title:** `Close Step 02_01_01 with zero-materialization CROSS-02-01 leakage-audit artifact pair`.
  - **Category:** A (science / Phase 02 / step closure).
  - **Dataset:** sc2egset.
  - **Branch:** `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`.
  - **PR:** `PR #230` (literal). PR #230 is the EXISTING draft PR for this closure; it was created before plan execution. No placeholder is used and no T10 amendment is required.
  - **Step scope:** Step 02_01_01 — closure of the catalog-only registry-skeleton step with a zero-materialization CROSS-02-01-v1.0.1 leakage-audit artifact pair.
  - **closure_status:** `closed` — NEW single-word token for THIS PR, symmetric with the repo's existing single-word `closure_status` convention (PR #216 used `partial`, PR #229 used `still_open`; per the per-dataset research_log entry written by PR #229, each PR picks its own short single-word token rather than reusing a prior PR's token). PR #229 did NOT use `closed_after_section10_verdict_audit_persisted` (PR #229 used `still_open`); no reuse is occurring or available. The semantic increment of THIS PR over PR #229 — emission of the CROSS-02-01 audit JSON+MD pair on disk at the spec-named path — is captured in the orthogonal long-form sibling field below: `leakage_audit_state: zero_materialization_pass`. This mirrors PR #229's orthogonal long-form pattern (`closure_status: still_open` + `evidence_persistence_state: section10_verdict_audit_persisted_step_open`). (See Q3 below for the rationale for the short-token + orthogonal-field approach over a single compound token.)
  - **leakage_audit_state:** `zero_materialization_pass` — NEW field that distinguishes "we now have a CROSS-02-01 audit artifact on disk at the spec-named path with verdict=PASS justified on §5(a) vacuity" from PR #229's "we have §10 evidence on disk but no CROSS-02-01 audit artifact".
  - **What:** The catalog-only Step 02_01_01 is closed. The closure produces a zero-materialization CROSS-02-01-v1.0.1 leakage-audit artifact pair at `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` (NEW per T02a), and flips STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS to record closure of the step, closure of the 02_01 pipeline section, and Phase 02 transition to `in_progress`.
  - **Why:** the ROADMAP `continue_predicate` three-clause read is now satisfied on disk (C1 by PR #216, C2 by THIS PR's new zero-materialization audit pair, C3 by PR #229); the §5(a) vacuity argument is real on the empty materialized set; the §3 + §5(c) artifact-presence is satisfied by THIS PR's new artifact pair. The closure honours the convention-based enforcement mechanism (§5 line 149) by routing through `reviewer-adversarial` both pre-execution (critique gate) and post-execution (final-gate review).
  - **How (reproducibility):** the artifact pair is a hand-written stub (no notebook); the JSON conforms to the §3 schema; the MD contains the 7 prescribed sections. No script generated either file; the executor wrote them per the T02a spec. Catalog inputs unchanged from PR #216 (registry CSV/MD SHA-256 unchanged) and PR #229 (§10 evidence CSV/MD SHA-256 unchanged).
  - **Findings:** Step 02_01_01 is closed; the 02_01 pipeline section is closed; Phase 02 is now `in_progress`. The closure does NOT materialize any feature column (catalog-only by design); does NOT replace the §10 evidence; does NOT replace a future post-materialization audit.
  - **What this means (status reopen disclosure — REQUIRED by reviewer feedback fix 1):** PIPELINE_SECTION_STATUS `02_01 = complete` is derived from STEP_STATUS per the YAML header rule "Pipeline section is complete when ALL its steps are complete." If a future PR adds a successor step (e.g., `02_01_02`) to STEP_STATUS with status `in_progress`, the derivation chain will mechanically re-derive `02_01 = in_progress`. This is INTENDED YAML-derivation behaviour, not silent revisionism. The closure-then-reopen sequence is designed-in to the YAML-derivation rule. No reviewer should treat a future `02_01 = in_progress` value as a regression of this closure.
  - **What this means (catalog-only authorisation softening — REQUIRED by reviewer feedback fix 5):** the closure does NOT authorise the start of `02_01_02`; instead, the gate for a future planner-science session to design `02_01_02` is now open (no implication of when such a session occurs, who runs it, or what its scope is). The closure also does NOT authorise any Phase 03 work; Phase 02 has only 1 of 8 canonical sections closed (02_01); Phase 02's remaining 7 sections (02_02..02_08 per docs/PHASES.md) are not started.
  - **Decisions taken:** emit the zero-materialization CROSS-02-01 artifact pair at the spec-named path; use the field value `"training_fold_only"` for `normalization_fit_scope` (alternative beta, v3 RESOLVED pre-execution per the v2 reviewer-adversarial BLOCKING condition C1; spec-permitted value vacuously satisfied on empty `features_audited`); use `"N/A_no_target_encoding"` (spec-permitted) for `target_encoding_fold_awareness`; use `"pass"` (vacuously) for the structural-check fields with explicit documentation in the JSON `notes` and MD that the catalog's declared cutoff rules are CROSS-02-03 §10 territory audited by PR #229. Use the NEW single-word closure_status token `closed` for THIS PR (PR #229 used `still_open`, not `closed_after_section10_verdict_audit_persisted`; no reuse is available or occurring; the short-token + orthogonal-field pattern matches PR #229's own structure), and add the NEW orthogonal long-form sibling field `leakage_audit_state: zero_materialization_pass` to capture this PR's semantic increment (CROSS-02-01 audit JSON+MD pair on disk at the spec-named path).
  - **Decisions deferred:** Step `02_01_02` design (a future planner-science session may begin); the post-materialization CROSS-02-01 audit for any future 02_01 materialization step (a future audit run per CROSS-02-01-v1.0.1 §4 line 117); the manifest update to `thesis/pass2_evidence/notebook_regeneration_manifest.md` (see OQ4 below); Phase 03+ work.
  - **Thesis mapping:** Chapter 4 §4.5 — citable as the closure-row lineage entry for Step 02_01_01 at the catalog-only registry layer. Does NOT enable any empirical leakage-clearance thesis claim.
  - **Open questions / follow-ups:** OQ1 (normalization_fit_scope spec-strict reading); OQ2 (this is the first 02_01_01 closure for any dataset; aoestats and aoe2companion will need parallel closures when their Phase 02 work begins, with the same zero-materialization template if their first steps are also catalog-only); OQ3 (reviewer-adversarial mandatory final gate is the v1 enforcement mechanism per §5 line 149); OQ4 (the next planner-science session must update `thesis/pass2_evidence/notebook_regeneration_manifest.md` status vocabulary with the new closure token combination `closure_status: closed` + `leakage_audit_state: zero_materialization_pass`).
  - **Acknowledged trade-offs:** the zero-materialization artifact pair is a hand-written stub, not a notebook-generated artifact. This is intentional for a catalog-only step where no notebook would have anything to compute; emitting a notebook would falsify the lineage. The artifact pair encodes the §5(a) vacuity argument as documentation, not as an empirical run.

- Allowed files: the per-dataset research_log only.
- Forbidden files: any other research_log, any other status file.
- Stop condition: the new entry is the topmost dated entry; the existing PR #229 entry is preserved verbatim; the file has the same line-ending convention and trailing-newline behaviour as master.

#### T05.b REMOVED in v3 (per BLOCKING condition C2)

The v2 plan added T05.b writing a CROSS entry to root `reports/research_log.md`. The v2 reviewer-adversarial gate ruled this violates `.claude/ml-protocol.md` lines 51-54: per-dataset closure is a single-dataset status flip, NOT a cross-dataset decision. T05.b is therefore REMOVED in v3. The methodological precedent that future aoestats / aoe2companion sessions may cite is captured by the per-dataset `research_log.md` entry produced by T05 (sc2egset) - any future cross-dataset planner-science session opening a parallel Phase 02 catalog-only closure may cite THIS PR's per-dataset research_log entry as the precedent. No CROSS entry is added by THIS PR.

### T06 CHANGELOG entry + version bump

- Target file: `CHANGELOG.md` and `pyproject.toml`.
- CHANGELOG.md edits:
  - Move the contents of `## [Unreleased]` (currently empty Added/Changed/Fixed/Removed buckets per the read above) under a new `## [3.65.0] — 2026-05-21 (PR #230: feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit)` block.
  - The new `[3.65.0]` block MUST contain:
    - **Added:**
      - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json` (NEW; CROSS-02-01-v1.0.1 zero-materialization closure stub for the catalog-only registry layer; verdict=PASS justified on §5(a) vacuity + §3/§5(c) artifact-presence at the spec-named path; features_audited=[]).
      - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md` (NEW; companion MD with 7 prescribed sections including top non-overclaim disclaimer, §3 spec citation, §5(a) vacuity argument, §3/§5(c) artifact-presence argument, explicit non-substitution statement, verdict justification, and OQ1 cross-reference).
      - New `research_log.md` entry in `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (Step 02_01_01 closure; `closure_status: closed`; `leakage_audit_state: zero_materialization_pass`; PR #230).
    - **Changed:**
      - `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` — added `"02_01_01": complete`.
      - `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` — added `"02_01": complete` (phase: "02", name: "Pre-Game vs In-Game Boundary").
      - `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml` — Phase 02 `not_started` -> `in_progress`.
      - `planning/INDEX.md` — PR #229 archived (merged 2026-05-21 at master `a14dc547`); new Active plan line for `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`.
      - `pyproject.toml` — version 3.64.0 -> 3.65.0.
    - **Notes:**
      - **This PR closes Step 02_01_01 at the catalog-only registry layer.** Closure is justified on the zero-materialization CROSS-02-01 leakage-audit artifact pair (verdict=PASS) at the spec-named path plus the §5(a) vacuity argument on the empty materialized set. No feature column is materialized by this PR.
      - **Status-reopen disclosure (per reviewer feedback fix 1).** PIPELINE_SECTION_STATUS `02_01 = complete` is YAML-derived from STEP_STATUS per the file header rule "Pipeline section is complete when ALL its steps are complete." If a future PR adds a successor step (e.g., `02_01_02`) to STEP_STATUS with status `in_progress`, the derivation chain will re-derive `02_01 = in_progress`. This is intended YAML-derivation behaviour, not silent revisionism. No regression is implied by a future `02_01 = in_progress` value.
      - **Non-substitution disclaimers.** The new artifact pair does NOT substitute for the PR #229 §10 verdict-audit CSV+MD pair (which audits CROSS-02-03 §10 design-time per-family verdicts for all 26 catalog rows). The new artifact pair does NOT substitute for a future post-materialization CROSS-02-01 audit that any later 02_01 materialization step will require. The new artifact pair does NOT make Step 02_01_01 a materialization step; Step 02_01_01 remains catalog-only.
      - **OQ1 RESOLVED pre-execution (v3).** The JSON field `normalization_fit_scope = "training_fold_only"` is the spec-permitted PASS value (alternative beta), vacuously satisfied on empty `features_audited` at the catalog-only layer (no normalizer was fit). The v2 plan proposed the new string `"N/A_no_features_materialized"` with OQ1 invitation for `reviewer-adversarial` overrule; v3 RESOLVES this pre-execution per the v2 reviewer-adversarial BLOCKING condition C1, removing the new-string risk. Treatment is symmetric to `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously).
      - **No notebook is created.** Step 02_01_01 closure at the catalog-only layer requires no notebook; emitting one would falsify the lineage.
      - **No source code, no validator, no spec, no ROADMAP body, no registry CSV/MD, no Phase 01 artifact, no INVARIANTS.md, no thesis chapter is touched.** This is a closure PR, not a feature PR.
- pyproject.toml edit: change `version = "3.64.0"` to `version = "3.65.0"`. Surgical single-line change.
- Allowed files: CHANGELOG.md, pyproject.toml.
- Forbidden files: any other.
- Stop condition: CHANGELOG has the new `[3.65.0]` block with the four prescribed Notes bullets; `[Unreleased]` block exists with the four empty sub-headers; pyproject.toml version is 3.65.0.

### T07 Update planning/INDEX.md

- Target file: `planning/INDEX.md`.
- Two surgical edits:
  1. **Archive PR #229.** Move the current Active line (`feat/sc2egset-02-01-01-section10-audit-persistence (2026-05-21) — Category A: SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict-audit evidence persistence; ...; Step 02_01_01 NOT closed (PR #229, draft)`) into the Archive table as a new row with: `feat/sc2egset-02-01-01-section10-audit-persistence | 2026-05-21 | A | SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict-audit evidence persistence; persist CSV+MD artifacts + per-dataset research_log entry; STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / ROADMAP / INVARIANTS / registry CSV/MD / validator / validator tests / root research_log frozen; Step 02_01_01 NOT closed | current_plan.md | #229 (merged 2026-05-21 at master a14dc547)`.
  2. **New Active line.** Replace the Active block with: `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit (2026-05-21) — Category A: SC2EGSet Phase-02 Step 02_01_01 closure via zero-materialization CROSS-02-01-v1.0.1 leakage-audit artifact pair at the spec-named path; STEP_STATUS adds 02_01_01: complete; PIPELINE_SECTION_STATUS adds 02_01: complete; PHASE_STATUS Phase 02 -> in_progress; per-dataset research_log entry only (no CROSS entry, per `.claude/ml-protocol.md` lines 51-54); CHANGELOG + version bump 3.64.0 -> 3.65.0; no notebook, no source, no validator, no spec, no ROADMAP body, no registry CSV/MD, no INVARIANTS.md edits (PR #230, draft)`.

- **Per reviewer feedback fix 2 (PR #228 vs PR #229 SHA disambiguation):** the Archive table already contains the correct PR #228 row (`feat/sc2egset-02-01-01-section10-verdict-audit ... #228 (merged 2026-05-21 at master 5c7ef380)`). The new PR #229 archive row added by this T07 step MUST cite `5c7ef380` for PR #228 (already in place) and `a14dc547` for PR #229 (new). Per v3 Nit 5, replace the v2 "visually verify" instruction with explicit bash checks: `grep -c "5c7ef380" planning/INDEX.md` and `grep -c "a14dc547" planning/INDEX.md` — each MUST return ≥ 1 AND the two SHAs MUST be on distinct rows (one row per PR). Concretely: run `grep -n "5c7ef380" planning/INDEX.md` and `grep -n "a14dc547" planning/INDEX.md` and confirm the line numbers differ.

- Allowed files: planning/INDEX.md only.
- Forbidden files: any other.
- Stop condition: planning/INDEX.md has exactly one Active row referencing the new branch; PR #229's archive row references SHA `a14dc547`; PR #228's archive row continues to reference SHA `5c7ef380`; no other Archive row is modified.

### T08 Pre-merge validation (single pass)

- Sequence of single-line bash commands:
  1. `git status` — confirm only the allowed files are modified.
  2. `git diff --name-only master..HEAD` — confirm the 9 diff-touching files in the §6 manifest exactly (items 1–9; item 10 transient pair MUST NOT appear).
  3. `python -m json.tool src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json > /dev/null` — JSON valid.
  4. `python -c "import yaml; yaml.safe_load(open('src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml'))"` — STEP_STATUS parses.
  5. `python -c "import yaml; yaml.safe_load(open('src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml'))"` — PIPELINE_SECTION_STATUS parses.
  6. `python -c "import yaml; yaml.safe_load(open('src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml'))"` — PHASE_STATUS parses.
  7. `source .venv/bin/activate && poetry run pytest tests/ -q` — full test suite passes (no notebooks, no validators, no source changed, so test suite must be green by construction).
  8. `source .venv/bin/activate && poetry run ruff check src/ tests/` — lint clean.
  9. `source .venv/bin/activate && poetry run mypy src/rts_predict/` — type check clean.

- Stop condition: all 9 commands succeed.
- If ANY command fails: HALT; investigate root cause before re-attempting; do NOT push, do NOT update PR #230 body, do NOT mark PR #230 ready.

### T09 Commit + push + update existing draft PR #230

- Commit message (HEREDOC-free, in `.github/tmp/commit.txt`, then `git commit -F .github/tmp/commit.txt` per memory):
  ```
  feat(sc2egset): close 02_01_01 with zero-materialization CROSS-02-01 leakage audit (3.65.0)

  Emit the CROSS-02-01-v1.0.1 leakage-audit artifact pair at
  reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md} with
  verdict=PASS justified on §5(a) vacuity (empty materialized set) plus
  §3 / §5(c) artifact-presence at the spec-named path. The closure does
  not materialize any feature column; Step 02_01_01 remains catalog-only.

  STEP_STATUS adds 02_01_01: complete; PIPELINE_SECTION_STATUS adds
  02_01: complete; PHASE_STATUS Phase 02 not_started -> in_progress.

  PIPELINE_SECTION_STATUS 02_01 may reopen as in_progress when a future
  PR adds a successor step to STEP_STATUS (intended YAML-derivation
  behaviour, not silent revisionism).

  The new pair does NOT substitute for PR #229's §10 verdict-audit CSV+MD,
  and does NOT substitute for a future post-materialization CROSS-02-01
  audit that any later 02_01 materialization step will require.

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```
- Push: `git push -u origin feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`.
- PR body update on the EXISTING draft PR #230: `gh pr edit 230 --body-file .github/tmp/pr.txt`. PR #230 was created from this branch before execution and remains the persistent draft PR for this closure. Do NOT call `gh pr create`. The body file mirrors the CHANGELOG `[3.65.0]` block plus a Test plan checklist plus a Validation report section.
- After PR body update: `rm .github/tmp/pr.txt` per memory.

- Allowed files: `.github/tmp/commit.txt` (created and deleted in this step), `.github/tmp/pr.txt` (created, used as input to `gh pr edit 230 --body-file`, and deleted in this step).
- Stop condition: `gh pr view 230 --json state,isDraft,number` returns `state=OPEN`, `isDraft=true`, `number=230`; the updated body is visible via `gh pr view 230 --json body`; commit SHA recorded; PR #230 remains DRAFT throughout T09 (do NOT call `gh pr ready 230` in T09).

### T10 No-placeholder verification

- PR #230 is the EXISTING draft PR; the literal `PR #230` is already used in T05 (per-dataset research_log entry), T06 (CHANGELOG `[3.65.0]` block header and Added bullet), and T07 (planning/INDEX.md Active line and Archive row, the latter for PR #229). T10 verifies — via `grep` — that NO `PR #<n>` / `PR #<TBD>` / `PR #{n}` placeholder survives anywhere in the diff: `git diff master..HEAD | grep -E 'PR #<(n|TBD)>|PR #\{n\}'` MUST return zero lines.
- Allowed files: none (read-only verification step).
- Stop condition: the grep returns zero lines; the placeholder-free state is confirmed.

### T11 Post-execution reviewer-adversarial final gate, then `gh pr ready 230`

- PR #230 remains DRAFT throughout T01..T10. T11 is run only after T08 validation passes, T09 has updated PR #230's body via `gh pr edit 230 --body-file`, and T10 has resolved any PR-number placeholders.
- **Step 1:** invoke `@reviewer-adversarial` post-execution final gate (per §9). Reviewer reads this plan + the `master..HEAD` diff on branch `feat/sc2egset-02-01-01-formal-closure-with-zero-materialization-audit`. Required scope per §9 (file-manifest match, JSON schema, MD section count, §5 disclaimer presence, OQ1 notes, YAML cascade).
- **Step 2:** if and only if the final gate returns APPROVE, run `gh pr ready 230` to mark PR #230 ready for review.
- **Step 3:** STOP. Do NOT merge PR #230. Merge remains the user's decision.
- Allowed files: none (final-gate review is read-only; `gh pr ready 230` mutates only the PR ready-state, not any tracked file).
- Stop condition: `@reviewer-adversarial` final-gate verdict is APPROVE AND `gh pr view 230 --json isDraft` returns `isDraft=false`. PR #230 remains OPEN and NOT merged.

## File Manifest

The full file manifest is enumerated in **§6 Allowed files (10-entry manifest: 9 diff-touching + 1 transient)** below. Summary: 9 diff-touching files (`reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` (NEW); `STEP_STATUS.yaml`; `PIPELINE_SECTION_STATUS.yaml`; `PHASE_STATUS.yaml`; per-dataset `research_log.md`; `pyproject.toml`; `CHANGELOG.md`; `planning/INDEX.md`; `planning/current_plan.md` + `planning/current_plan.critique.md` as a single planning-pair entry) + 1 transient working file (`.github/tmp/{commit.txt,pr.txt}` deleted post-create). See §6 for verbatim paths and per-file action (Update / Create) and §7 for the forbidden-paths list.

## Gate Condition

The closure gate condition is enumerated across §11 (Open questions / blockers) and across the T08 validation step. Summary: the future execution PR passes its closure gate if and only if (a) all 9 diff-touching files in §6 are present in the diff with the prescribed content, (b) zero forbidden-list paths from §7 are touched, (c) the new `leakage_audit_sc2egset.json` validates against CROSS-02-01-v1.0.1 §3 schema with `verdict = "PASS"` and `features_audited = []`, (d) the new `.md` sibling contains all 8 prescribed sections including the v3-added "Audit queries: none — vacuously satisfied" section, (e) STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS derivations are honest under the YAML-header derivation rules (Q4 walkthrough), (f) the per-dataset `research_log.md` entry uses the NEW single-word `closure_status: closed` token plus the NEW orthogonal long-form sibling field `leakage_audit_state: zero_materialization_pass` with explicit non-reuse of PR #216's `partial` and PR #229's `still_open` tokens, (g) `PR #230` is referenced literally everywhere (no `PR #<n>` / `PR #<TBD>` placeholder survives — verified by T10), and (h) the `@reviewer-adversarial` post-execution final-gate review per T11 returns APPROVE, after which `gh pr ready 230` is run; PR #230 is NOT merged. See §9 for reviewer routing, T11 for the final-gate-then-ready sequence, and §11 for the open-questions / blockers gate.

## Open Questions

Open questions are enumerated in **§11 Open questions / blockers** below. Summary: 4 open questions (OQ1 RESOLVED pre-execution; OQ2 future cross-dataset citation precedent; OQ3 user adjudication of branch name long-form acceptance; OQ4 next planner-science session to update `notebook_regeneration_manifest.md` vocabulary). §11 ends with the standard "No blockers remain that prevent execution after `@reviewer-adversarial` pre-execution critique gate clearance." line per `docs/templates/planner_output_contract.md`.

## §1 Outcome adjudication

**Verdict: A'(i)-APPROVE.**

Rationale: the v2 plan was returned BLOCKING-CONDITIONS by `reviewer-adversarial` because (C1) the JSON used a new string `"N/A_no_features_materialized"` for `normalization_fit_scope` that is NOT in §3's enumerated PASS values, while still asserting `verdict = "PASS"`, and (C2) the plan added a CROSS entry to root `reports/research_log.md` violating `.claude/ml-protocol.md` lines 51-54 (per-dataset closure is not a cross-dataset decision). v3 resolves BOTH BLOCKING conditions pre-execution. (The v1 plan was earlier returned HOLD-REPLAN; the v2 plan implemented A'(i) faithfully via T02a; v3 corrects the residual two BLOCKING conditions in v2.) v3 retains the A'(i) resolution mechanism:

- The JSON populates every §3 required field with a spec-permitted PASS value. `normalization_fit_scope = "training_fold_only"` is the v3-resolved alternative beta (vacuously satisfied on empty `features_audited`); `target_encoding_fold_awareness = "N/A_no_target_encoding"` is spec-permitted; the structural-check fields use `"pass"` vacuously. No new strings; no OQ-flagged choices remain open in v3.
- The MD contains 8 sections (top disclaimer, §3 citation, §5(a) vacuity argument, §3/§5(c) artifact-presence argument, non-substitution statement, verdict justification, OQ1-RESOLVED cross-reference, and the v3-added "Audit queries: none — vacuously satisfied" sec 8 per Nit 4).
- The closure honours the convention-based enforcement mechanism (§5 line 149) by routing through `reviewer-adversarial` both pre-execution (critique gate per §9) and post-execution (final-gate review per §9).
- v3 drops the T05.b root-research_log CROSS entry per BLOCKING condition C2; the precedent for future aoestats / aoe2companion closures lives in this PR's per-dataset research_log entry.
- All v2 non-blocker reviewer fixes (originally 5) remain folded in; v3 adds 3 v2-gate-recommended nits (3, 4, 5).

The verdict is APPROVE-v3, not HOLD-SCHEMA or HOLD-SPEC or HOLD-REPLAN, because:
- The plan does not propose any spec amendment (HOLD-SPEC would apply if it did).
- The plan does not propose a different artifact schema than §3 (HOLD-SCHEMA would apply if it did).
- The plan does not propose a fundamentally different closure mechanism (HOLD-REPLAN would apply if it did).
- The v2 BLOCKING conditions C1 and C2 are RESOLVED pre-execution in v3 by (C1) adopting the spec-permitted `"training_fold_only"` for `normalization_fit_scope` with vacuous-satisfaction rationale, and (C2) dropping the T05.b root research_log CROSS entry per `.claude/ml-protocol.md` lines 51-54.

## §2 Repo evidence

Master HEAD: `a14dc547bf19245ddc205048dbaf9cb6b11d9400`.
Version at master: `3.64.0` (planned bump to `3.65.0` per Cat A `feat/` rule).

Status files at master (verified via Bash reads):
- STEP_STATUS.yaml: 38 entries, all Phase 01; no Phase 02 entries.
- PIPELINE_SECTION_STATUS.yaml: 6 Phase 01 sections, no Phase 02 sections.
- PHASE_STATUS.yaml: Phase 02 = `not_started`; Phase 01 = `complete`; Phases 03..07 = `not_started`.

Artifact state at master (verified via Bash reads):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/`: **DIRECTORY DOES NOT EXIST.**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`: contains 4 files — the PR #216 registry CSV+MD (`02_01_01_feature_family_registry.{csv,md}`) and the PR #229 §10 verdict-audit CSV+MD (`02_01_01_section10_verdict_audit.{csv,md}`). All four are unchanged by this PR.

Spec file at master:
- `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1, LOCKED 2026-04-26). §3, §4, §5 as quoted verbatim in the task instructions to this planner.

ROADMAP `continue_predicate` at master:
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` lines 2060-2066, verbatim as in the task instructions. Three clauses C1, C2, C3 (see Assumption A5).

INVARIANTS.md at master:
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` EXISTS (verified via `find` and via the file structure listing). The hedge "(if it exists; not touched)" used in the v1 plan was wrong; this v2 plan uses the precise wording "(exists; not touched)" per reviewer feedback fix 4.

Notebook regeneration manifest at master:
- `thesis/pass2_evidence/notebook_regeneration_manifest.md` EXISTS. Its status vocabulary documents `confirmed_intact`, `not_yet_assessed`, `flagged_stale`, `partial_coverage_v9_baseline`, `regenerated_pending_log`, `phase_blocked`. None of these is the right token for the post-closure state introduced by this PR. The manifest is in the forbidden list (per §7 and Q9) and is updated in a separate future planner-science session (per OQ4).

Planning/INDEX.md at master:
- Active line: `feat/sc2egset-02-01-01-section10-audit-persistence (2026-05-21) — ... (PR #229, draft)`. T07 archives this line citing PR #229 merged at SHA `a14dc547`.
- Archive table: PR #228 row already present, citing SHA `5c7ef380`. T07 does not modify this row.

Notebook regeneration manifest cross-reference (CROSS-02-01-v1.0.1 §4 lines 123-133): the manifest is the authoritative stale/current registry for Phase 02 audit artifacts. This PR creates a new audit artifact pair; the manifest does NOT yet record its status. OQ4 instructs the next planner-science session to add this entry. The closure of THIS PR is valid because:
- the §5(a) vacuity does not depend on a manifest entry;
- the §3 artifact-presence does not depend on a manifest entry;
- the v1 enforcement mechanism (§5 line 149) is convention-based via `reviewer-adversarial` review, which substitutes for the not-yet-extant manifest entry at the time of closure.

CHANGELOG at master:
- `[Unreleased]` block exists with empty Added/Changed/Fixed/Removed sub-headers (verified). `[3.64.0]` block records PR #229. The T06 edit moves the empty `[Unreleased]` content under a new `[3.65.0]` block and refills `[Unreleased]` with empty sub-headers.

pyproject.toml at master:
- `version = "3.64.0"` (verified).

## §3 Answers to 10 questions (Q1–Q10)

### Q1: Is the ROADMAP `continue_predicate` satisfied?

YES. Three-clause decomposition (Assumption A5):
- C1 (CSV+MD artifact-check) — SATISFIED by PR #216.
- C2 (CROSS-02-01-v1.0.1 post-materialization audit gate re-run for any feature column the registry triggers materialization of) — SATISFIED by THIS PR's new zero-materialization audit pair at T02a, because the registry triggers materialization of zero feature columns at the catalog layer, and the audit re-run scope is therefore "zero feature columns", and the artifact pair at the spec-named path makes that re-run on-disk and citable. NOTE: the v1 plan failed Q1 because it claimed C2 was vacuously satisfied without emitting any CROSS-02-01 artifact at the spec-named path; this v2 plan satisfies C2 with the actual artifact pair.
- C3 (per-family CROSS-02-03-v1.0.1 §10 verdict for every registry row) — SATISFIED by PR #229.

### Q2: Is the CROSS-02-01-v1.0.1 §5 gate condition satisfied?

YES, on all three clauses.
- §5(a) "Every feature column materialized in 02_01 appears in `features_audited`" — vacuously satisfied because the materialized set is empty at the catalog layer (`features_audited = []` and zero columns are materialized; universal quantifier vacuously true).
- §5(b) `verdict = "PASS"` — satisfied by the new JSON artifact's verdict field.
- §5(c) "Both the JSON artifact and the sibling Markdown report are present at the prescribed path" — satisfied by T02a writing both files at `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}`.

### Q3: Why use a short `closure_status` token plus an orthogonal long-form sibling field, instead of a single long compound token? (v3 RESOLVED per user directive: PR #229 did NOT use `closed_after_section10_verdict_audit_persisted` — that long-form was a planner-side invention; PR #229 used the short `still_open` token plus the orthogonal long-form `evidence_persistence_state` field. The short + orthogonal pattern is the established repo convention; v3 plan adopts it for THIS PR.)

Concrete repo evidence for the short `closure_status` convention:
- PR #216: per-dataset research_log L35 = `closure_status: partial`; registry MD L101 = `closure_status: partial` (single short word).
- PR #229: per-dataset research_log L12 = `closure_status: still_open`; sibling field L13 = `evidence_persistence_state: section10_verdict_audit_persisted_step_open` (short closure_status + orthogonal long-form field).
- PR #229 per-dataset research_log L19 explicitly forbade reusing PR #216's token ("Explicitly do NOT reuse PR #216's `closure_status: partial` token"), establishing the convention that each PR picks its own short single-word `closure_status`.

v3 plan adopts this pattern for THIS PR:
- `closure_status: closed` — short single-word token, NEW for THIS PR (not a reuse — PR #229's token was `still_open`, not `closed_after_...`).
- `leakage_audit_state: zero_materialization_pass` — orthogonal long-form sibling field, NEW for THIS PR, factoring out the dimension "is there a CROSS-02-01 leakage-audit artifact on disk at the spec-named path?" with values `not_yet_emitted` (the state at PR #229) and `zero_materialization_pass` (the state at THIS PR).

Rationale for the short + orthogonal pattern over a single long compound token:
- A single long compound token would collapse the orthogonal closure dimension (open/partial/still_open/closed) with the orthogonal evidence/audit dimension, making the progression hard to read.
- The pattern matches PR #229's own structure exactly.
- The token `closed` is the canonical terminal value for `closure_status`, symmetric to `partial` and `still_open` (the prior PRs' terminal values for their epistemic state).

The closure-progression history for Step 02_01_01 reads cleanly under this pattern: PR #216 (`closure_status: partial`), PR #229 (`closure_status: still_open` + `evidence_persistence_state: section10_verdict_audit_persisted_step_open`), THIS PR (`closure_status: closed` + `leakage_audit_state: zero_materialization_pass`, recorded against `PR #230`).

### Q4: Does this PR cascade Phase 02 to `in_progress`? (UPDATED per task instructions)

YES, the cascade is explicit and intentional, and the cascade behaviour with respect to YAML derivation is fully documented.

Cascade chain (per the file header documentation in STEP_STATUS, PIPELINE_SECTION_STATUS, and PHASE_STATUS):
- STEP_STATUS adds `02_01_01: complete`.
- PIPELINE_SECTION_STATUS adds `02_01: complete` (derived from the STEP_STATUS rule "Pipeline section is complete when ALL its steps are complete"; since `02_01_01` is the only step under section `02_01` and it is `complete`, the derived value is `complete`).
- PHASE_STATUS Phase 02 = `in_progress` (derived from the PIPELINE_SECTION_STATUS rule "Phase is in_progress when ANY pipeline section is in_progress or complete"; since `02_01` is `complete`, Phase 02 is `in_progress`).

Reopen behaviour (REQUIRED by reviewer feedback fix 1 — see Assumption A4):
- If a future PR adds a successor step `02_01_02` (or any other step under section `02_01`) to STEP_STATUS with status `in_progress`, the YAML derivation rule mechanically re-derives `PIPELINE_SECTION_STATUS 02_01 = in_progress` (not `complete`, because not ALL steps are complete).
- This is intended YAML-derivation behaviour, not silent revisionism.
- T05 (per-dataset research_log) and T06 (CHANGELOG) both surface this reopen behaviour as explicit bullets so that any future reviewer encountering `02_01 = in_progress` after THIS PR's closure sees the closure-then-reopen sequence as designed-in.

### Q5: Does the PR number in research_log / CHANGELOG need to be the exact assigned number?

YES, and it is known. PR #230 is the EXISTING draft PR for this closure; it was created before plan execution. The CHANGELOG block header and the per-dataset research_log entry both use the literal `PR #230`. No placeholder appears in any prose entry. T10 is retained only to formalise the "no placeholder remains" verification after T09's `gh pr edit 230 --body-file` publishes the body.

### Q6: Is `INVARIANTS.md` touched?

NO. INVARIANTS.md (located at `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`) EXISTS at master and is NOT touched by any task in this plan. INVARIANTS.md is in the forbidden list (§7). Per reviewer feedback fix 4, the precise wording in the plan is "(exists; not touched)" rather than the hedge "(if it exists; not touched)".

### Q7: Are the registry CSV/MD touched?

NO. The PR #216 registry CSV/MD at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.{csv,md}` are unchanged. They are in the forbidden list (§7). The new T02a artifact pair is at a DIFFERENT path (`reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}`) per the §3 spec-named-path requirement.

### Q8: What is the exact file manifest? (UPDATED in v3 per BLOCKING condition C2 — was 11 entries in v2, now 10 entries: 9 diff-touching + 1 transient pair entry; root `reports/research_log.md` dropped)

10 entries (9 diff-touching files + 1 transient working-file entry):
1. **NEW** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json`
2. **NEW** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md`
3. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
4. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
5. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
6. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (new top entry)
7. **MODIFIED** `CHANGELOG.md` (new `[3.65.0]` block; `[Unreleased]` re-emptied)
8. **MODIFIED** `pyproject.toml` (3.64.0 -> 3.65.0)
9. **MODIFIED** `planning/INDEX.md` (PR #229 archived, new Active line for this PR)
10. **CREATED-AND-DELETED-IN-T09** `.github/tmp/commit.txt` and `.github/tmp/pr.txt` (transient working files; per memory, deleted after commit / PR creation; do NOT appear in the final commit diff)

**v3 note:** the v2 plan listed root `reports/research_log.md` as item 7; this is REMOVED in v3 per BLOCKING condition C2 (per-dataset closure is not a cross-dataset decision per `.claude/ml-protocol.md` lines 51-54). The diff-touching count is therefore **9 files** (items 1-9 above); item 10 is the transient pair (commit.txt + pr.txt) created and deleted within T09 and does NOT appear in the final commit diff.

Item 10 (the transient pair) does not count as a modified file in the PR diff (created and deleted within T09). Items 1–9 are the 9 diff-touching file-manifest entries; item 10 is the transient tooling. The literal count of new+modified files in the final commit diff is **9** (1 new pair = 2 files + 7 modified = 9). The §6 Allowed files list enumerates all 10 entries.

### Q9: What's in the forbidden list? (UPDATED per reviewer feedback fix 3)

The forbidden list is enumerated in §7. It includes (load-bearing entries):
- All Phase 01 artifacts.
- The PR #216 registry CSV+MD.
- The PR #229 §10 verdict-audit CSV+MD.
- The PM-1 validator (`validate_registry_section10_verdicts.py`) and validator tests.
- The notebook (`02_01_01_registry_section10_verdict_audit.{py,ipynb}`).
- INVARIANTS.md (exists; not touched).
- ROADMAP.md body (continue_predicate text is referenced as-is, not amended).
- All specs (CROSS-02-01, CROSS-02-03, etc.).
- All source code under `src/rts_predict/`.
- All tests.
- All thesis chapters.
- **`thesis/pass2_evidence/notebook_regeneration_manifest.md`** — NEW per reviewer feedback fix 3; updates to this manifest's status vocabulary for the new closure token combination are deferred to a future planner-science session per OQ4.

### Q10: What's the reviewer routing?

Per §9 (mandatory `reviewer-adversarial` pre-execution critique gate; mandatory `reviewer-adversarial` post-execution final gate; `reviewer-deep` available as final-gate alternative if `reviewer-adversarial` recommends offloading the structural-correctness pass).

## §4 Status-chain cascade analysis (with explicit toggle reopen behaviour)

Cascade chain at master `a14dc547`:
- STEP_STATUS: 38 entries (all Phase 01).
- PIPELINE_SECTION_STATUS: 6 Phase 01 sections.
- PHASE_STATUS: Phase 02 = `not_started`.

Cascade chain after this PR lands:
- STEP_STATUS: 39 entries (38 Phase 01 + 1 new Phase 02 entry: `02_01_01: complete`).
- PIPELINE_SECTION_STATUS: 7 sections (6 Phase 01 + 1 new Phase 02 section: `02_01: complete`).
- PHASE_STATUS: Phase 02 = `in_progress` (flipped from `not_started`).

Cascade chain after a hypothetical future PR adds Step `02_01_02`:
- STEP_STATUS: 40 entries (38 Phase 01 + 2 Phase 02 entries: `02_01_01: complete`, `02_01_02: in_progress`).
- PIPELINE_SECTION_STATUS: 7 sections, but `02_01` re-derives from `complete` to `in_progress` per the YAML rule "Pipeline section is complete when ALL its steps are complete; in_progress when ANY step is in_progress or complete." Since `02_01_02 = in_progress`, NOT ALL steps are complete, so `02_01` is `in_progress`.
- PHASE_STATUS: Phase 02 = `in_progress` (unchanged).

**Reopen behaviour disclosure (REQUIRED by reviewer feedback fix 1):**
The `02_01 = complete -> 02_01 = in_progress` transition under a future Step 02_01_02 PR is INTENDED YAML-derivation behaviour, not silent revisionism. This is the same convention that lets Phase 01 sections (which closed step-by-step over Phase 01 work) stay `complete` because all their steps are `complete`. T05 (per-dataset research_log) and T06 (CHANGELOG) MUST surface this reopen behaviour as explicit bullets so that any future reviewer encountering `02_01 = in_progress` after this PR's closure sees the closure-then-reopen sequence as designed-in.

## §5 Boundary / non-overclaim disclaimers

The closure of Step 02_01_01 by this PR carries the following boundary disclaimers, which MUST appear in (a) the per-dataset research_log entry (T05), (b) the CHANGELOG entry (T06), (c) the new MD artifact (T02a), and (d) the new JSON `notes` field (T02a):

1. **The new artifact pair does NOT substitute for the PR #229 §10 verdict-audit CSV+MD pair.** PR #229 audits CROSS-02-03 §10 design-time per-family verdicts for all 26 catalog rows. THIS PR's pair audits CROSS-02-01 pre-training leakage. The two specs are sibling-but-distinct.
2. **The new artifact pair does NOT substitute for a future post-materialization CROSS-02-01 audit.** Any later 02_01 materialization step (e.g., 02_01_02 if it materializes the first feature column) will require a fresh CROSS-02-01 audit with non-empty `features_audited`. The closure of Step 02_01_01 by this PR does not pre-approve any future materialization.
3. **The new artifact pair does NOT make Step 02_01_01 a materialization step.** Step 02_01_01 remains catalog-only. The new artifact pair is a layered closure device for a catalog-only step, encoding the §5(a) vacuity argument as documentation rather than as an empirical run. This disclaimer is NEW per the reviewer-adversarial preferred resolution (was not in the v1 plan in this explicit form).
4. **The new closure does NOT authorise the start of 02_01_02.** The gate for a future planner-science session to design 02_01_02 is now open (no implication of when such a session occurs, who runs it, or what its scope is). Per reviewer feedback fix 5: the v1 plan's "(a) a separate later planner-science session to design 02_01_02" wording is softened to "the gate for a future planner-science session to design 02_01_02 is now open".
5. **The new closure does NOT authorise any Phase 03 work.** Phase 02 has only 1 of 8 canonical sections closed (02_01); Phase 02's remaining 7 sections (02_02..02_08 per docs/PHASES.md) are not started. Phase 03 starts only after Phase 02 is `complete`, not merely `in_progress`.
6. **PIPELINE_SECTION_STATUS `02_01 = complete` may reopen as `in_progress` if a future PR adds a successor step to STEP_STATUS.** Per Assumption A4 and §4 above, this is intended YAML-derivation behaviour, not silent revisionism. The closure-then-reopen sequence is designed-in.
7. **The `normalization_fit_scope` field value `"training_fold_only"` is the spec-permitted PASS value (v3 RESOLVED pre-execution per BLOCKING condition C1 of the v2 reviewer-adversarial gate).** No new string is introduced. The value is vacuously satisfied on empty `features_audited` at the catalog-only layer (no normalizer was fit; the pass condition is vacuously met). This treatment is symmetric to the field values used for `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously). OQ1 is RESOLVED pre-execution (alternative beta); no `reviewer-adversarial` overrule is invited.

## §6 Allowed files (10-entry manifest: 9 diff-touching + 1 transient)

Allowed for modification or creation in this PR (per the file manifest in Q8):

1. **NEW** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json`
2. **NEW** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.md`
3. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
4. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
5. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
6. **MODIFIED** `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
7. **MODIFIED** `CHANGELOG.md`
8. **MODIFIED** `pyproject.toml`
9. **MODIFIED** `planning/INDEX.md`
10. **TRANSIENT** `.github/tmp/commit.txt` and `.github/tmp/pr.txt` (created and deleted within T09; do NOT appear in the final commit diff per memory)

**v3 note:** the v2 plan listed root `reports/research_log.md` as item 7; this is REMOVED in v3 per BLOCKING condition C2. The diff-touching file count is 9 (items 1-9); item 10 is the transient pair.

Edits at any other path are FORBIDDEN.

## §7 Forbidden files

Forbidden from modification or creation in this PR:

- All Phase 01 artifacts in `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/`.
- The PR #216 registry CSV+MD at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.{csv,md}`.
- The PR #229 §10 verdict-audit CSV+MD at `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.{csv,md}`.
- The PM-1 validator at `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`.
- The validator tests at `tests/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py` (or its equivalent path).
- The PM-1 notebook at `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.{py,ipynb}`.
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md` (exists; not touched — per reviewer feedback fix 4 the precise wording is "exists; not touched" rather than the v1 hedge "if it exists; not touched").
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (body not amended; the `continue_predicate` text is referenced verbatim by Assumption A5, not edited).
- All locked specs under `reports/specs/`, including:
  - `02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1).
  - `02_00_feature_input_contract.md` (CROSS-02-00-v3.0.1).
  - The CROSS-02-03 spec (whose §10 is audited by PR #229).
- All source code under `src/rts_predict/` (no code change in this closure PR).
- All tests under `tests/` (no test change in this closure PR).
- All thesis chapters under `thesis/chapters/`.
- **`thesis/pass2_evidence/notebook_regeneration_manifest.md`** — NEW in this forbidden list per reviewer feedback fix 3. Updates to this manifest's status vocabulary for the new closure token combination (`closure_status: closed` + `leakage_audit_state: zero_materialization_pass`) are deferred to a future planner-science session per OQ4.
- All `thesis/pass2_evidence/` sibling files (claim_evidence_matrix, dependency_lineage_audit, methodology_risk_register, reviewer_gate_report, sec_4_1_crosswalk, sec_4_2_crosswalk, etc.).
- Any path under `.claude/` (no rule or invariant change).
- Any path under `docs/` (no doc change; `docs/PHASES.md` is read for its 8-section canonical structure but not edited).
- Any path under `data/` or `staging/`.
- Any other path not enumerated in §6.

## §8 Release-tail plan (3.64.0 → 3.65.0)

Per the `feat/` branch-prefix rule: minor-version bump. 3.64.0 → 3.65.0.

Release-tail tasks (sequence preserved):
1. T06 (CHANGELOG edit + pyproject.toml version bump) — done in the main execution sequence.
2. T07 (planning/INDEX.md archive + new Active line) — done in the main execution sequence.
3. T09 (commit + push + update existing draft PR #230 via `gh pr edit 230 --body-file`) — done in the main execution sequence.
4. T10 (no-placeholder verification) — done after T09's `gh pr edit 230 --body-file`.
5. T11 (`@reviewer-adversarial` post-execution final gate, then `gh pr ready 230` on APPROVE; do NOT merge) — done after T10.

No tag is created in this PR; tags are created at master merge per the user's standard release flow.

## §9 Reviewer routing

**Pre-execution critique gate (MANDATORY for Cat A per `.claude/rules/data-analysis-lineage.md` and per the v1 enforcement mechanism in CROSS-02-01-v1.0.1 §5 line 149):**
- `@reviewer-adversarial` reads this plan + the v1 plan + the v1 critique + the master HEAD state. Output is `planning/current_plan.critique.md` (separate file from this plan).
- Required scope of the critique: re-test Assumption A1 (replacement for the v1 blocker assumption); re-test Assumption A4 (reopen behaviour); re-test the OQ1 spec-strict reading; re-test the §3 schema-completeness of the JSON; re-test the non-substitution disclaimers in §5.
- If the critique returns APPROVE: proceed to execution.
- If the critique returns HOLD-SCHEMA / HOLD-SPEC / HOLD-REPLAN: do not execute; revise this plan; resubmit.
- 3-round adversarial cap per memory `feedback_adversarial_cap_execution.md` (symmetric: applies to plan-side and execution-side review).

**Execution:** `@executor` on Sonnet (mechanical multi-file editing per the file manifest in §6; no scientific reasoning required; all decisions resolved by this plan).

**Post-execution final gate (MANDATORY for Cat A; executed as T11):**
- Primary: `@reviewer-adversarial` reads this plan + the post-execution diff (`master..HEAD`). Required scope: assert the §6 file manifest matches the diff exactly; assert the §3 schema is satisfied by the new JSON; assert all 8 MD sections are present (including the v3-added "Audit queries: none — vacuously satisfied" sec 8 per Nit 4); assert the §5 disclaimers appear in per-dataset research_log + CHANGELOG + MD; assert OQ1 is documented in the JSON `notes`; assert the YAML cascade chain is correct; assert the per-dataset research_log entry uses `closure_status: closed` + `leakage_audit_state: zero_materialization_pass`; assert literal `PR #230` appears everywhere (no placeholder survives); assert NO root `reports/research_log.md` edit appears in the diff.
- Fallback (per `.claude/rules/data-analysis-lineage.md` "Use reviewer-deep for structural correctness, spec compliance, and invariant tracing"): if `@reviewer-adversarial` recommends offloading the structural-correctness pass, `@reviewer-deep` may run as the final-gate alternative. This is a fallback, not a default. Default is `@reviewer-adversarial`.
- **Ordering (Route A; the plan adopts Route A).** PR #230 remains DRAFT throughout T01..T10. T11 runs the post-execution final gate while PR #230 is DRAFT. Only on APPROVE does T11 run `gh pr ready 230`. The plan does NOT instruct any executor to merge PR #230; merge remains the user's decision.

## §10 Risks

**R1 (LOW — downgraded from HIGH in v3 per BLOCKING condition C1 resolution) — `normalization_fit_scope` spec-strict reading.** RESOLVED pre-execution by adopting alternative beta (`"training_fold_only"`, the spec-permitted value, vacuously satisfied on empty `features_audited`). No reviewer-adversarial overrule path is required; the JSON value is schema-conformant on a strict reading. Residual LOW-severity risk: if the v3 reviewer-adversarial gate identifies a fact-of-the-matter objection to claiming a `training_fold_only` fit-scope where no fit occurred, the JSON `notes` field documents the vacuous-satisfaction rationale, and the symmetry with the other field values (`N/A_no_target_encoding`, `pass` vacuously) provides additional cover. Mitigation: the resolution is symmetric and documented; no further action expected.

**R2 (MEDIUM) — manifest entry deferred.** `thesis/pass2_evidence/notebook_regeneration_manifest.md` does not have an entry for the new artifact pair after this PR lands. The closure is valid (per §5 line 149 the v1 enforcement mechanism is `reviewer-adversarial` review, not the manifest), but the manifest stale-status tracking will be out of sync until OQ4 is resolved by a future planner-science session. Mitigation: OQ4 is explicit (§11) and the missing manifest entry does NOT block any Phase 02 work because Phase 02 work after this PR is gated by the future post-materialization CROSS-02-01 audit, which has its own manifest-entry requirement at that audit's PR time.

**R3 (MEDIUM) — PR #229 ordering coupling.** THIS PR (PR #230) ASSUMES PR #229 is merged to master at SHA `a14dc547` (which the master HEAD verification confirms). If PR #229 is reverted between this plan's submission and PR #230's eventual merge (which is a separate user decision; this plan does NOT instruct any executor to merge PR #230), the §10 verdict-audit CSV+MD would be absent from master, the C3 clause of the ROADMAP `continue_predicate` would no longer be satisfied, and PR #230's closure justification would fail. Mitigation: the `base_ref` is pinned to `a14dc547` in the frontmatter; if master HEAD advances during execution, the executor MUST verify PR #229's artifacts are still on disk before committing.

**R4 (LOW) — version bump collision.** If another PR lands between this plan's submission and this PR's merge that also bumps pyproject.toml version, the version bump in T06 will conflict. Mitigation: planning/INDEX.md verification at execution time will reveal any new merged PRs; in that case T06 is amended to bump from the new master version (e.g., 3.65.0 -> 3.66.0).

**R5 (LOW) — empty `[Unreleased]` block reformat.** The current `[Unreleased]` block at master is empty (Added/Changed/Fixed/Removed sub-headers exist with no content). The T06 edit moves these empty sub-headers under the new `[3.65.0]` block (where they will be filled with the prescribed content) and re-creates empty sub-headers under a new `[Unreleased]` block. Mitigation: the edit pattern is the same as PR #229 (and earlier PRs); no novelty.

**R6 (LOW) — pre-commit hook fails on the JSON or MD.** If ruff or mypy or any pre-commit hook rejects the new files (unlikely — JSON is not linted by ruff/mypy; MD is not linted), the commit fails and T09 must be retried after fix. Mitigation: T08 runs ruff and mypy as part of the pre-merge validation, so any hook failure surfaces before commit.

## §11 Open questions / blockers

**OQ1 (RESOLVED pre-execution; alternative beta chosen for schema-strict reading):** The field value `normalization_fit_scope = "training_fold_only"` is the spec-permitted PASS value, vacuously satisfied on empty `features_audited` at the catalog-only layer (no normalizer was fit; the pass condition is vacuously met). This treatment is symmetric to the field values used for `target_encoding_fold_awareness` (`N/A_no_target_encoding` — spec-permitted) and `cutoff_time_filter_structural_check` / `reference_window_assertion` (`pass` vacuously). No reviewer-adversarial overrule is invited; the resolution is closed.

**OQ2:** When aoestats and aoe2companion reach their Phase 02 catalog-only registry-skeleton steps, do they close via the same zero-materialization CROSS-02-01 audit template established by this PR? Planner-science default answer: YES, the template applies symmetrically for cross-game comparability. Resolution path: deferred to the future aoestats / aoe2companion planner-science sessions. Future aoestats / aoe2companion sessions opening their own Phase 02 catalog-only closure entries may cite THIS PR's per-dataset research_log entry as the methodological precedent; no CROSS entry is added by THIS PR because the closure is a single-dataset status flip, not a cross-dataset decision per `.claude/ml-protocol.md` lines 51-54.

**OQ3:** Is the convention-based v1 enforcement mechanism (CROSS-02-01-v1.0.1 §5 line 149: "(i) the reviewer-adversarial mandatory review gate before any 02_01 exit PR is merged, and (ii) this spec's convention") satisfied by routing this PR through `@reviewer-adversarial` both pre-execution AND post-execution? Planner-science default answer: YES, the double routing operationalises the convention. Resolution path: `@reviewer-adversarial` rules during the pre-execution critique gate.

**OQ4:** The next planner-science session must update `thesis/pass2_evidence/notebook_regeneration_manifest.md` to add the new closure token combination (`closure_status: closed` + `leakage_audit_state: zero_materialization_pass`) to the status vocabulary, and to record an entry for the new audit artifact pair at `reports/artifacts/02_01_01/leakage_audit_sc2egset.{json,md}` as `confirmed_intact` (the closure has landed and the artifact pair is on disk, recorded against `PR #230`). This OQ does NOT block this PR (the manifest is in the forbidden list per §7; closure is valid per §5 line 149 without the manifest entry), but it is a follow-up scheduled item.

**OQ5:** Does the closure of Step 02_01_01 trigger any thesis-side editorial pass on Chapter 4 §4.5? Planner-science default answer: NO, the §4.5 framing (PR #219) is at the registry-methodology level and does not depend on the closure status; a future Chapter 4 update may add a closure-row sentence but is not blocked by this PR. Resolution path: deferred to a future thesis-side planner-science session.

**No blockers remain that prevent execution after `@reviewer-adversarial` pre-execution critique gate clearance.**
