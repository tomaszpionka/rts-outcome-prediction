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
nits: 5
gate_status: passed-with-nits
date: 2026-05-31
v1_predecessor_pr: 276
v1_predecessor_sha: 37c3a8855af038bd1bd4eefbdbd03497da323d47
---

# Reviewer-Adversarial Critique — Round 1 (V3 Scaffold Layer-1 Plan)

## Round 1 verdict

**Verdict: APPROVE-WITH-NITS.** Zero blockers. **5 NITs surfaced** (N-A through N-E). The plan's methodological structure is sound. V3 as the immediately-next scaffold rung is correctly motivated and the commitment lineage (V1 docstring + CHANGELOG [3.88.0] Notes + PR #275 NIT-2) is solid. The DESIGN-TIME ONLY scope is well-declared and the V3/CROSS-02-01 complementarity is conceptually correct but requires explicit docstring framing (NIT-E). The separation from V1 (separate module, no V1 import) is enforced by H1. Five NITs require inline application before Layer-2 may proceed.

**Round 1 of 3** (cap per `.claude/agent-memory/reviewer-adversarial/feedback_adversarial_cap_execution.md`). Round 2 triggers if: (a) the executor materially amends the plan after applying N-A through N-E; (b) a new BLOCKER surfaces; or (c) H6/H7 grep falsifiers fail on the materialized plan text.

## What was verified

- PR #276 (V1 scaffold execution) merged at master `37c3a8855af038bd1bd4eefbdbd03497da323d47` — confirmed via `gh pr view 276 --json mergeCommit`.
- `validate_temporal_feature_grid.py` docstring lines 3-4: V3-separation clause confirmed present ("Future temporal-discipline checks (V3) must land in a separate validator module under a separate scaffold rung.").
- CHANGELOG `[3.88.0]` Notes: V3 deferred to IMMEDIATELY-NEXT scaffold rung per NIT-2 of PR #275 plan — confirmed.
- pyproject.toml currently `3.88.0` (post-PR #276); planned V3 bump `3.88.0 → 3.89.0` is feat-class minor per `.claude/rules/git-workflow.md` — matches PR #276 precedent.
- CROSS-02-03-v1.0.1 (LOCKED 2026-05-06) confirmed at `reports/specs/02_03_temporal_feature_audit_protocol.md`.
- CROSS-02-00-v3.0.1 (LOCKED 2026-04-26) and CROSS-02-02-v1.0.1 (LOCKED 2026-05-06) confirmed LOCKED.
- tracker_events_feature_eligibility.csv present at canonical path.
- `validate_temporal_discipline.py` does NOT yet exist — confirmed.
- PHASE_STATUS Phase 02 `in_progress` / Phase 03 `not_started` — confirmed.
- Q8 cross-game portability correctly scoped to syntactic-only (no empirical AoE2 transferability claim in plan draft).
- V3 DESIGN-TIME ONLY scope (schema footer reads, no data-value reads, no DuckDB queries) — confirmed in plan draft §Problem Statement and §Execution Steps T02.

## NITs to apply before materialization

- **N-A (explicit out-of-scope list in §Scope):** §Scope lacks an explicit "Out of scope" bullet list declaring the V3 design surface boundary. Without it, a Layer-2 executor has no negative-space contract beyond what is implied by the positive scope. Add to §Scope a bulleted "Out of scope (V3 design surface — declared here, enforced by Layer-2 falsifiers):" list explicitly excluding: concrete temporal window sizes; decay half-lives; cold-start k-thresholds; tracker_events family inclusion decision; in-game temporal scope decision; any feature materialization; any artifact emission to `reports/artifacts/02_feature_engineering/03_temporal_features/**`; any ROADMAP / STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS / dataset research_log / root research_log edits; Phase 03 activation or baseline modeling; any empirical AoE2 transferability claim.

- **N-B (Layer-2 "Files that MUST remain byte-unchanged" list):** §File Manifest shows the 7-file create/update table but lacks an explicit binding negative-space contract for files that must NOT be touched. In the PR #276 precedent plan, a "Files that MUST remain byte-unchanged" subsection followed the manifest table. Add to §File Manifest, after the 7-file table, an explicit subsection: "Files that MUST remain byte-unchanged in Layer-2 (binding negative-space contract):" listing at minimum: ROADMAP.md; STEP_STATUS.yaml; PIPELINE_SECTION_STATUS.yaml; PHASE_STATUS.yaml; dataset research_log.md; root research_log.md; `validate_temporal_feature_grid.py` (V1; annotated: "H1 falsifier's no-V1-import rule implies V1 cannot be edited as a side effect"); all `reports/artifacts/**` subdirectories; tracker_events_feature_eligibility.csv; all locked CROSS specs; docs/**; .claude/**; data/**; aoe2/**; thesis/**.

- **N-C (A-15 cross-game-portable vocabulary: explicit binding needed):** The plan mentions cross-game-portable vocabulary in §Problem Statement and §Execution Steps T02 but does not declare it as a named Assumption in §Assumptions & Unknowns. This means the Layer-2 executor lacks a named anchor to halt against. Add to §Assumptions & Unknowns the verbatim assumption: "**A-15. Cross-game-portable vocabulary.** The V3 validator module, mirrored test, and notebook scaffold use cross-game-portable vocabulary only (focal/opponent, history window, started_at, prior, target-game exclusion) and do NOT name SC2-specific terms (race, mineral, vespene, PlayerStats, tracker_events, toon_id, apm, sq) or AoE2-specific terms (civilization, civ, profile_id, leaderboard) where avoidable. No empirical AoE2 transferability claim is made; that determination is deferred to a future AoE2-specific Phase 02 step. This is verifiable by grep falsifiers H6 (cross-game-portable vocabulary) and H7 (Q8 syntactic-only guard) at Layer-2 execution."

- **N-D (A-9 PHASE_STATUS assumption: scope expansion needed):** §Assumptions & Unknowns A-9 in the plan draft states only "PHASE_STATUS.yaml NOT touched." This is correct but thin — it does not explain the sequencing rationale. A Layer-2 executor who misreads Phase 02 completeness might attempt a premature flip. Expand A-9 to read: "**A-9. PHASE_STATUS.yaml NOT touched.** Phase 02 stays `in_progress`; Phase 03 stays `not_started`. No PHASE_STATUS row added or modified by the Layer-2 V3 scaffold execution PR. Phase 02 closure (and Phase 03 readiness) require future U2.B-style closure PR(s) downstream of adjudication + materialization rungs." This makes the sequencing dependency explicit and guards against executor scope creep.

- **N-E (V3 module docstring framing: schema-level complement to CROSS-02-01 value-level):** §Execution Steps T02 requires the V3 module docstring to be present but does not specify its framing relative to CROSS-02-01. A reviewer examining V3 in isolation may question whether V3 and CROSS-02-01 duplicate each other or whether V3 supersedes CROSS-02-01. The relationship must be explicitly framed in the V3 module docstring itself (not just in the plan). Add to T02 the requirement that the V3 module docstring includes VERBATIM: "V3 is a schema-level design-time gate enforcing strict-`<` temporal discipline via history-naming convention, temporal-anchor presence, and cite-string provenance. Value-level leakage (sophisticated semantic leaks not detectable from schema metadata alone) is gated separately by post-materialization audits per CROSS-02-01-v1.0.1. V3 and CROSS-02-01 are complementary, not redundant. V3 catches the common contributor failure modes (forbidden column naming, missing temporal anchor, missing cite-strings); CROSS-02-01 catches sophisticated semantic leaks at the value layer." This framing must also appear in §Literature Context for plan-level verifiability (G4 gate predicate).

## Blockers

None.

## Methodological findings

**V3 as DESIGN-TIME gate is correctly positioned.** The V3 scope (schema-level, no data-value reads, no DuckDB queries) is appropriately narrow for a scaffold rung. It enforces the naming convention and structural discipline that makes later value-level audits (CROSS-02-01) interpretable. Without V3, a contributor could commit a feature grid with ambiguous column names or a missing temporal anchor, and CROSS-02-01 would catch it only post-materialization (expensive) rather than at design time (cheap). V3 as a pre-materialization gate is the correct layering.

**H1 falsifier (V3 re-pins V1 SHA; no V1 import) is the correct anchor.** Re-pinning the V1 SHA in H1 of the V3 falsifier chain creates a SHA-chain provenance: V1 SHA is recorded at V1 merge; V3 verifies V1 SHA is still byte-stable at V3 execution. This is the correct approach for multi-rung scaffold lineage.

**V3 falsifier chain H1-H7 is correctly scoped.** H1 (predecessor + V1 byte-stability), H2 (temporal anchor), H3 (naming convention), H4 (cite-string provenance), H5 (forbidden emission), H6 (cross-game vocabulary), H7 (Q8 syntactic-only) cover the seven observable design-time failure modes for a temporal-discipline validator. No falsifier is missing or duplicated.

**OQ-1/OQ-2/OQ-3 deferral is correct.** Concrete window sizes (OQ-1), tracker family eligibility (OQ-2), and in-game temporal scope (OQ-3) are appropriately deferred to the adjudication PR. V3 does not resolve these — it validates that the schema discipline required to receive those values is in place.

**OQ-4 boundary preserved.** CROSS-02-02 (feature engineering plan) and CROSS-02-03 (design-time audit protocol) are cited with distinct roles. V3 cites CROSS-02-03 cite-strings (D1-D6 schema-level audit dimensions). No conflation of the two CROSS specs.

**Q8 syntactic-only is correctly enforced.** No empirical AoE2 transferability claim appears in the draft plan. The vocabulary scope (focal/opponent, history window, started_at) is cross-game-portable without asserting AoE2 compliance.

**Adjudication-direct rejected.** The plan correctly bars adjudication before V3 lands. Q1 commits V3 as the immediately-next rung.

## Gate decision

Layer-1 plan may materialize to disk after N-A through N-E are applied inline. Layer-2 V3 scaffold PR may proceed once Layer-1 merges, provided:

- The out-of-scope list (N-A) is present in §Scope.
- The byte-unchanged list (N-B) is present in §File Manifest.
- A-15 cross-game-portable vocabulary assumption (N-C) is in §Assumptions & Unknowns.
- A-9 PHASE_STATUS assumption (N-D) includes sequencing rationale.
- V3 module docstring framing (N-E) is in §Execution Steps T02 AND §Literature Context.
- All Layer-2 halt conditions H1–H7 remain green.
- Round 2 re-gate trigger is explicit in §Gate Condition.

## Sources / verification trail

- `gh pr view 276 --json mergeCommit --jq .mergeCommit.oid` → `37c3a8855af038bd1bd4eefbdbd03497da323d47`
- `grep -n 'Future temporal-discipline' validate_temporal_feature_grid.py` → lines 3-4 confirmed
- `grep -F 'V3 (strict-' CHANGELOG.md` → CHANGELOG [3.88.0] Notes entry confirmed
- `grep -E '^version = ' pyproject.toml` → `version = "3.88.0"` confirmed
- `ls reports/specs/02_03_temporal_feature_audit_protocol.md` → CROSS-02-03-v1.0.1 LOCKED 2026-05-06 confirmed
- `ls src/rts_predict/games/sc2/datasets/sc2egset/validate_temporal_discipline.py` → does not exist (correct)
