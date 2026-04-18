# Planning Backlog

Deferred follow-ups from merged PRs. A session picks ONE item, then fleshes it
out into `current_plan.md` (see `planning/README.md` §Lifecycle) and works
through the standard plan/execute/review loop.

This file is the queue — not an active plan. It holds no executable detail
beyond scoping; the full plan is produced at the moment a session claims the
item.

---

## Origin: PR #160 (feat/pre-01-05-cleanup) + PR #159 (chore/post-pr-158-hygiene)

Opened 2026-04-18.

### F1 — aoestats `canonical_slot` column (Phase 02 unblocker)

- **Category:** A (phase work, aoestats)
- **Branch:** `feat/aoestats-canonical-slot`
- **Invariants touched:** I3, I5, I7, I9
- **Predecessors:** PR #160 W3 verdict `ARTEFACT_EDGE` (commit `ab23ab1d`;
  `reports/specs/01_05_preregistration.md` §14 amendment v1.0.1)
- **Spec amendment trigger:** bumps spec to v1.1.0.

**Scope.** Add a `canonical_slot VARCHAR` derived column to aoestats
`matches_history_minimal` (and upstream `matches_1v1_clean` if needed) to
neutralise the upstream API skill-correlated slot assignment identified by W3.
Phase 02 features then consume `canonical_slot` instead of raw `team`.

**Decision to make during planning.** Whether `canonical_slot` derives from
`old_rating` (skill-ordered) or `profile_id` (identity-ordered,
skill-orthogonal). Artifact JSON §Phase 02 interface at
`src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_05_i5_diagnosis.json`
names both.

**Acceptance.** Schema YAML updated; derivation SQL documented; aoestats
`INVARIANTS.md` §5 `I5` row transitions PARTIAL → HOLDS (or equivalent);
spec §14 amended + `spec_version` bumped; no row-count regression on existing
views.

**Why priority 1.** Unblocks aoestats 01_05 from emitting
`[PRE-canonical_slot]`-tagged outputs and unblocks aoestats Phase 02 entirely.

---

### F2 — Per-dataset 01_05 Temporal & Panel EDA (three parallel PRs)

- **Category:** A × 3 (one PR per dataset)
- **Branches:** `feat/01-05-sc2egset`, `feat/01-05-aoe2companion`,
  `feat/01-05-aoestats`
- **Spec binding:** `reports/specs/01_05_preregistration.md@<SHA>` in every
  `sandbox/<game>/<dataset>/01_exploration/05_temporal_panel_eda/*.py`
  docstring (enforced by `scripts/check_01_05_binding.py` pre-commit hook).
- **Predecessors:** PR #160 W4 spec v1.0.1. aoestats additionally depends on F1
  if the session wants final (not `[PRE-canonical_slot]`) numbers.

**Scope.** Execute Pipeline Section 01_05 per the spec's 9 parameter groups:
quarterly grain (10-quarter overlap window 2022-Q3 → 2024-Q4), equal-frequency
PSI N=10 with frozen reference edges, `regime_id ≡ calendar quarter`, triple
survivorship analysis, reference periods 2022-08-29..2022-12-31 (sc2egset/aoec)
and 2022-08-29..2022-10-27 (aoestats single-patch), between/within variance
decomposition, `temporal_leakage_audit_v1`, POST_GAME DGP diagnostics in
dedicated subsection, Phase 06 interface schema.

**Parallelization.** sc2egset + aoec can start immediately. aoestats either
waits for F1 or accepts `[PRE-canonical_slot]` outputs and amends post hoc.

**Acceptance per PR.** Notebook + JSON + MD artifacts + `research_log.md`
entry + `STEP_STATUS.yaml` + `ROADMAP.md` + `INVARIANTS.md` §4 empirical
findings populated. `PHASE_STATUS.yaml` ticks when all three 01_05 step sets
are `complete`.

**Why priority 2.** 01_05 is the next gate on the critical thesis path. All
downstream phases depend on it.

---

### F3 — Thesis §4.2.2 prose revision + Tabela 4.5 row 247 correction

- **Category:** F (thesis writing)
- **Branch:** `docs/thesis-4.2.2-identity-meta-rule`
- **Predecessors:** PR #160 W5 meta-rule. **Blocked on F2 landing for all
  three datasets** (per W5 critique A5: §4.2.2 must reflect 01_05
  within-profile stability findings).

**Scope.**
1. Revise `thesis/chapters/04_data_and_methodology.md` §4.2.2 to describe the
   5-branch decision procedure (I2 extended form) with three worked examples
   + one stress-test rejection (chess.com hypothetical).
2. Correct Tabela 4.5 row 247:
   - sc2egset: `LOWER(nickname)` → `player_id_worldwide` (branch (iii); 12%
     documented bias)
   - aoec: `LOWER(name)` → `profileId` (branch (i))
   - aoestats: keep `profile_id`, annotate as branch (v) structurally-forced
3. `thesis/WRITING_STATUS.md` §4.2.2 DRAFTED → REVISED.
4. `thesis/chapters/REVIEW_QUEUE.md` updated.

**Acceptance.** Prose follows argumentative Polish style; Tabela 4.5 row 247
matches each dataset's `INVARIANTS.md` §2; `thesis/references.bib` unchanged
(Christen 2012 not used as identity threshold in the revised meta-rule).

**Why priority 3.** High information value but cannot be authored before
01_05 provides the within-profile stability findings that justify the "trust
the ID" stance.

---

### F4 — Narrative-drift checker (chore)

- **Category:** C (chore)
- **Branch:** `chore/narrative-drift-checker`
- **Predecessors:** PR #160 W2 critique A3 (deferred as scope creep).

**Scope.** Implement `scripts/verify_narrative_numbers.py`:
- Parse numeric tokens (≥ 4 significant digits) from every `research_log.md`.
- For tokens under a section header matching `[Phase NN / Step XX_YY_ZZ]`,
  grep the corresponding artifact JSON for the same value.
- Fail on research-log numbers absent from the step's artifact; allow
  documented exceptions via `# drift-allow: <justification>` inline marker.

Install as opt-in pre-commit hook (`git config hooks.checknarrativedrift true`)
and CI lint job on PRs touching `research_log.md`.

**Scope boundary.** Regex extraction must skip dates (`2026-04-18`), seed IDs
(`20260418`), row counts (`683,790`), percentages.

**Acceptance.** Script < 200 LOC; ruff + mypy clean; unit tests cover clean
case, drift detection, exception handling; CI job + pre-commit hook
documented in `.claude/rules/git-workflow.md`.

**Why priority 4.** Defence-in-depth against the class of defect W2
reconciled, but not blocking current work. Can interleave as a low-friction
chore.

---

### F5 — Purge decommissioned `planning/dags/` + `planning/specs/`

- **Category:** C (chore)
- **Branch:** `chore/planning-purge-dags-specs`
- **Predecessors:** user directive "Decommission DAG/specs" (see memory
  `feedback_decommission_dag.md`); flagged out-of-scope during W1.

**Scope.** `rm -rf planning/dags/ planning/specs/`; `grep -r` verifies no
outside reference; update `planning/README.md` if it still mentions either;
CHANGELOG `[Unreleased]` → `Removed` entry.

**Acceptance.** Directories gone; no broken references; PR title
`chore(planning): remove decommissioned dags/ and specs/`.

**Why priority 5.** Zero-risk hygiene; unblocks no downstream work.

---

## Claiming an item

1. Delete the item's entry from this backlog in the same PR that authors
   its `current_plan.md`, so the two artifacts are transactionally
   consistent.
2. Write the full plan into `current_plan.md` (must conform to
   `docs/templates/plan_template.md` — the `planning-drift` pre-commit
   hook enforces the template).
3. For Category A/F: dispatch `reviewer-adversarial` to produce
   `current_plan.critique.md` before execution.
4. For Category C: skip the adversarial gate; `planner` + executor is
   sufficient.
5. Execute, merge, purge per `planning/README.md` §Purge protocol.
