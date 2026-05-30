---
plan: planning/current_plan.md
phase: 02
pipeline_section: 02_03
step: 02_03_01
category: A (feat/)
layer: 1
reviewer: reviewer-adversarial
round: 1
cap: 3
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 6
gate_status: passed-with-nits
date: 2026-05-30
supersedes: held-adjudication-direct-attempt
prior_round_verdict: HOLD (2 BLOCKERs accepted by user; adjudication-direct REJECTED)
---

# Adversarial Pre-Materialization Critique — Step 02_03_01 SCAFFOLD + One Validation Module (Layer-1; New Branch)

## Round 1 verdict

APPROVE-WITH-NITS. Zero blockers. Six NITs (N1–N6). The plan's core methodological structure is faithful to the PR #265 → PR #266 scaffold precedent. The scaffold-first mandate is respected. The two BLOCKERs from the prior held adjudication-direct attempt (BLOCKER 1: scaffold-first mandatory per ROADMAP continue_predicate; BLOCKER 2: Q8 syntactic-only) are resolved. The V1-first choice is methodologically defensible given the SHA-pin provenance need. Open questions Q2–Q5 are appropriately deferred. Non-batching discipline is preserved.

## What was verified

- PR #274 (ROADMAP-only stub for 02_03_01) merged at master `6716aa1745b29cae50ed1323e3c2853987a47ca7` — confirmed via `gh pr view 274 --json mergeCommit`.
- ROADMAP.md lines 3372-3384: `continue_predicate` confirmed present, mandating scaffold PR before adjudication PR.
- PR #265 = 2-file Layer-1 (planning/current_plan.md + planning/current_plan.critique.md), scaffolded 02_02_01 scaffold plan.
- PR #266 = 7-file Layer-2 (validator + mirrored test + jupytext pair + pyproject 3.83.0→3.84.0 minor + CHANGELOG + planning/INDEX.md), confirmed scaffold precedent.
- pyproject.toml currently `3.87.0` (post-PR #274); planned bump `3.87.0 → 3.88.0` is feat-class minor per .claude/rules/git-workflow.md — matches PR #266 precedent.
- tracker_events_feature_eligibility.csv present at canonical path.
- Four parent artifact merge SHAs verified: PR #236 `39298c0a`, PR #259 `5a62fc76`, PR #255 `52f9c108`, PR #270 `eddd0489`.
- Q8 cross-game portability reduced to syntactic-only per BLOCKER 2 acceptance. No empirical AoE2 transferability claim in plan.
- docs/PHASES.md line 116 confirms 02_03 is row 3 of Phase 02.
- CROSS-02-00-v3.0.1 (LOCKED 2026-04-26), CROSS-02-02-v1.0.1 (LOCKED 2026-05-06), CROSS-02-03-v1.0.1 (LOCKED 2026-05-06) all confirmed LOCKED.

## NITs to apply before materialization

- **N1 (continue_predicate verbatim citation):** §Literature Context must quote the merged ROADMAP `continue_predicate` text VERBATIM (lines 3372-3384) and frame it as the binding obligation, not a policy preference. The citation block must name the file and line range explicitly.
- **N2 (V3-next commitment):** §Open Questions Q1 AND §Literature Context must explicitly commit: "V1 is shipped first as foundational provenance anchor. V3 (strict-`<` temporal-discipline predicate) is committed as the IMMEDIATELY-NEXT scaffold rung (separate Layer-1 + Layer-2 PR pair), to land BEFORE any adjudication PR. Without this commitment, V1-first degrades to 'V1 only forever' and the temporal-discipline invariant is never directly exercised at design time before concrete grid values are pinned."
- **N3 (validator filename precision — Option B):** Keep `validate_temporal_feature_grid.py` AND require future Layer-2 to add module docstring declaring verbatim: "This validator audits predecessor artifact provenance only (V1). It does NOT validate any temporal feature grid. Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung." Document the choice explicitly in §File Manifest under the validator module entry. Option B (extensible + docstring constraint) is preferred over Option A (rename to `validate_predecessor_artifact_provenance.py`) because it allows V3 to land as a separate module under a clearly-scoped pattern.
- **N4 (Q8 grep falsifiers in §Gate Condition):** Add to §Gate Condition (Layer-1 gate predicates): Falsifier F-Q8-syntactic: `grep -niE 'aoe2|civilization|aoestats|aoe2companion' planning/current_plan.md` — every match MUST be bounded as a forbidden-term constraint or as "deferred to future AoE2-specific Phase 02 step"; no unbounded transferability claim. Falsifier F-candidate-agnostic: `grep -niE '\b(7|14|30|90|180)d\b|\b(7|10|14|30)_games?\b|half_life|k_threshold|tracker_events|PlayerStats|race|mineral|vespene' planning/current_plan.md` — zero matches in validator-design or test-scaffolding sections (candidate-agnostic discipline + Invariant I8 cross-game vocabulary).
- **N5 (PR #266 version bump verification):** §Assumptions & Unknowns or §Literature Context must cite the actual PR #266 version bump verified via `gh pr view 266` ("PR #266 bumped `3.83.0 → 3.84.0` confirmed via `gh pr view 266`"). Lock the Layer-2 plan to `3.87.0 → 3.88.0` minor. If the version query returns something other than `3.83.0 → 3.84.0`, adjust accordingly and re-derive the Layer-2 target.
- **N6 (Round 2 re-gate trigger):** §Gate Condition must add an explicit clause: "If the materialized `planning/current_plan.md` fails any of the F-Q8-syntactic / F-candidate-agnostic grep falsifiers (NIT-4) or the 8-section literal-match check (`grep -cE '^## (Scope|Execution Steps|File Manifest|Problem Statement|Assumptions & Unknowns|Literature Context|Gate Condition|Open Questions)$' planning/current_plan.md` must = 8), the Layer-1 PR must escalate to reviewer-adversarial Round 2 on the materialized text. 3-round cap per `feedback_adversarial_cap_execution.md`."

## Blockers

None.

## V1 vs V3 finding

V1-first (SHA-pin predecessor artifact provenance) is methodologically defensible as the foundational anchor that gates any future feature work against verified predecessor inputs. However, V3 (strict-`<` temporal-discipline predicate) must not be deferred indefinitely. The temporal-discipline invariant (Invariant I7: no feature uses data with `history_time >= T` for target game T) is the core leakage guard for the entire Phase 02 feature engineering ladder. If V3 does not land as the immediately-next scaffold rung, the adjudication PR will pin concrete window/decay/k-threshold values without any tested temporal leakage gate in the codebase — creating a structural gap.

NIT-2 mandates the V3-next commitment. Without it, Round 2 will be required after materialization.

## Round budget

Round 1 of 3 (cap per `.claude/agent-memory/reviewer-adversarial/feedback_adversarial_cap_execution.md`). Round 2 triggers if: (a) the executor materially amends the plan after applying N1–N6; (b) a new BLOCKER surfaces; or (c) F-Q8-syntactic or F-candidate-agnostic grep falsifiers fail on the materialized text.

## Gate decision

Layer-1 plan may materialize to disk after N1–N6 are applied inline. Layer-2 scaffold PR may proceed once Layer-1 merges, provided:

- The ROADMAP `continue_predicate` citation (N1) is verbatim and line-referenced.
- The V3-next commitment (N2) appears in both §Literature Context and §Open Questions Q1.
- The validator module docstring constraint (N3 Option B) is documented in §File Manifest.
- Both grep falsifiers F-Q8-syntactic and F-candidate-agnostic (N4) are present in §Gate Condition.
- PR #266 version bump is cited and Layer-2 target locked to `3.87.0 → 3.88.0` (N5).
- Round 2 re-gate trigger (N6) is explicit in §Gate Condition.
- All Layer-2 halt conditions H1–H8 remain green.
