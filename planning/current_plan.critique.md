---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-24
plan_base_ref: 3c6709bfc21baba893d34a3b87c308d7f8ba787e
plan_branch: feat/sc2egset-02-01-03-history-source-anchor-coldstart-adjudication
plan_step: "02_01_03 (Layer-1 source/anchor/cold-start adjudication planning)"
plan_category: A
planning_pr: "PR #242"
round: 3
rounds_cap: 3
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 3
recommended_action: materialize plan to disk
---

## Verdict

**APPROVE-WITH-NITS — 0 blockers, 3 NITs.**

This is round 3 of 3 in the adversarial cap (`feedback_adversarial_cap_execution.md`). The two round-2 blockers (B-X1, B-X2) and four round-2 nits (N-X1–N-X4) are resolved with empirical verification. The 3 net-new round-3 NITs are minor documentation/test-fixture gaps that the Layer-2 executor can resolve without methodology drift.

**Recommended next action:** materialize plan to disk; open the Layer-1 draft PR.

## Round trajectory

| Round | Verdict | Blockers | Nits | Net change |
|------:|---------|---------:|-----:|------------|
| 1 | APPROVE-WITH-NITS | 1 (B1: manifest count `10/8+2` vs correct `11/9+2`) | 5 (N1–N5) | Plan accepted in direction; B1 mechanical; nits substantive but scoped |
| 2 | HOLD | 2 NEW (B-X1: Q6 self-tripping POST_GAME-token falsifier; B-X2: `STRICT_LT_HISTORY_FILTER` divergence across 3 sites) | 4 NEW (N-X1: helper/key mapping implicit; N-X2: Q1 asymmetry over-bound without spec evidence; N-X3: rating-evidence falsifier decorative; N-X4: Q1 EXTEND conflates 2 conditions) | All R1 findings resolved cleanly; revision INTRODUCED new methodology blockers |
| 3 | **APPROVE-WITH-NITS** | **0** | **3** (N-R3-A, N-R3-B, N-R3-C — all documentation-level) | All R2 blockers + nits resolved with empirical verification; net-new nits are executor-resolvable |

## Round 3 per-item results

All checks against `/tmp/02_01_03_plan_round3.md` (materialized to `planning/current_plan.md`).

### B-X1 — scoped POST_GAME-token falsifier

**PASS.** The plan renames `_check_universal_no_post_game_token` → `_check_forbidden_post_game_feature_tokens` (T03 step 8). Scope is limited to source/feature/materialization fields (`POST_GAME_TOKEN_SCOPED_FIELDS` — 9 entries including 2 reserved future fields). Rationale-bearing fields are explicitly exempt (`POST_GAME_TOKEN_EXEMPT_FIELDS` — 7 entries: `notes`, `evidence_paths`, `falsifiers`, `decision_name`, `rationale`, `source_layer_divergence_reason`, `history_source_extension_reason`). T04 priority chain entry 18 uses the new name + key `universal_post_game_token_in_scoped_field`. T06 wires `TestUniversalPostGameToken` (re-scoped), `TestNegativeRationaleAllowedInNotes` (positive companion proving the Q6 rationale text "no target-match outcome; no future results; no global batch fit" passes), `TestForbiddenTokensExemptFieldsList` (asserts the two field-sets are disjoint), and `TestDirectTargetMatchOutcomeRejected` (re-scoped to source/feature/materialization fields, NOT notes).

### B-X2 — single canonical strict-< expression

**PASS.** Canonical expression `TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < target.started_at` (TRY_CAST, NOT bare CAST; `target` alias, NOT `mhm`) is declared as `STRICT_LT_HISTORY_FILTER` constant in T01 step 2. T02 step 5 smoke probe SQL uses the canonical form with `target` alias. T05 Q3 + Q7 bound expressions use the canonical form. New falsifier `_check_strict_lt_filter_divergence` declared in T03 step 12; key `strict_lt_filter_divergence` added to T04 priority chain.

Empirical verification:
- `matches_history_minimal.yaml` line 24 uses `TRY_CAST(matches_flat_clean.details_timeUTC AS TIMESTAMP)` — TRY_CAST (NOT bare CAST). Verified directly by file read. The canonical choice in the plan matches the canonical schema metadata.
- Grep of `details_timeUTC` across the plan returned 26 occurrences. Every executable site uses canonical TRY_CAST. The 5 bare-form occurrences are explicitly labeled as ROADMAP-raw-form provenance constants (`STRICT_LT_FILTER_ROADMAP_RAW`), rejection-case bullets in the new divergence falsifier description, or "rejected form" test-fixture documentation. No bare uncast `ph.details_timeUTC <` is left in any executable/code-bearing position.

T06 wires `TestStrictLtFilterCanonicalAcrossSites` (asserts the constant + smoke SQL + Q3/Q7 bound expressions all use canonical form) and `TestRoadmapRawFormNotPropagated` (asserts bare form only appears in named constant + falsifier message-format string).

### N-X1 — helper-to-falsifier-key mapping

**PASS.** T03b declares an explicit `HELPER_TO_FALSIFIER_KEY` literal table with 20 entries — covering every helper/falsifier pair including the new `_check_forbidden_post_game_feature_tokens` → `universal_post_game_token_in_scoped_field` and `_check_strict_lt_filter_divergence` → `strict_lt_filter_divergence`. T04 priority chain references the mapping. T06 wires `TestHelperToFalsifierKeyMappingIsComplete` and `TestPriorityChainReferencesMapping`.

### N-X2 — Q1 asymmetry evidence (Option A chosen, with verbatim spec quotes)

**PASS.** Option A (RECOMMENDED, BINDING) is chosen and substantiated with **5 verbatim spec/schema quotes** in T05 Q1 — each with source-path + row-identification + empirical line-number match:
1. `02_02_feature_engineering_plan.md` line 238 row 1 (focal_player_history → `player_history_all`)
2. `02_02_feature_engineering_plan.md` line 241 row 4 (reconstructed_rating → `player_history_all.result` filtered by I3 anchor)
3. `02_02_feature_engineering_plan.md` line 243 row 6 (in_game_history_aggregate → `player_history_all.APM/SQ/supplyCappedPercent/header_elapsedGameLoops`)
4. `02_00_feature_input_contract.md` line 87 (row grain "1 row per player per match (all game types; no 1v1 filter)")
5. `player_history_all.yaml` line 236 (view scope: "All replays (no 1v1/decisive filter). Includes non-1v1 and indecisive replays excluded from matches_flat_clean.")

Alternative B (symmetric 1v1-only history) is REJECTED with cited rationale: cold-start support-set sparsity under the 83.95% MMR-missing density regime would contradict §6.2 rows 1, 4, 6 verbatim. Option B fallback (demote `binding_level` to `recommendation_only`/`deferred_blocker`) NOT triggered.

### N-X3 — strengthened rating-evidence falsifier

**PASS.** T03 step 4 strengthens `_check_q6_rating_default_deferred`:
- `deferred_blocker` branch: PASSES iff `evidence_paths != ""` AND notes contain `"deferred_blocker because:"`
- Model-family branch: HALTS unless ALL of: `evidence_paths` contains ≥1 repo path (regex `^(src/|reports/|sandbox/|thesis/|tests/|docs/|\.claude/)`) AND ≥1 primary-source citation (regex `^@\w+|\\cite\{|^[A-Z][a-z]+\d{4}`); notes contain forward-only phrases; notes contain cold-start + missingness handling wording

T05 Q6 recommended `evidence_paths` (3 repo paths + 4 citations) and recommended `notes` (containing `"deferred_blocker because:"`, `"no target-match outcome"`, `"no future results"`, `"no global batch fit"`, `"cold-start handled by"`, `"missingness handled by"`) verbatim. T06 `TestQ6RatingEvidenceSufficiency` declares all 4 branches: deferred-pass, deferred-fail-no-rationale, bind-pass-with-full-evidence, bind-fail-with-only-1-repo-path.

### N-X4 — Q1 EXTEND disambiguation via subfields

**PASS.** T01 step 3 dataclass adds 2 NEW subfields (Q1 only): `source_layer_divergence_reason` and `history_source_extension_reason`. T05 Q1 populates both verbatim. Q1 stays a single row (N5 preserved); subfield count grows from 3 → 5. Future Layer-2 CSV schema = 26 dataclass fields + `notes` = 27 columns. §Gate Condition condition 3 explicitly states "27 columns (26 dataclass fields + `notes`)". Column-count propagation is consistent across T01 step 3, T04 step 1, T06 `TestDeterministicCsvSchema`, T08 step 6 verification, §File Manifest, §Gate Condition condition 3, and §Self-check.

### Preserved fixes from rounds 1–2

- **B1** (manifest count): PASS — `11 final tracked files (9 deliverable + 2 inherited planning)` everywhere; notebook pair `.py` + `.ipynb` counts as 2 deliverables; no stale `10 files` / `8 deliverable` / `notebook pair counts as one file` anywhere.
- **N1** (`in_game_historical_columns_in_scope`): PASS — Q7 binds exact `APM|SQ|supplyCappedPercent|header_elapsedGameLoops`.
- **N2** (Q7-specific `_check_in_game_historical_strict_lt`): PASS — distinct from any generic strict-< check.
- **N3** (Q6 default `deferred_blocker`): PASS — preserved AND strengthened by N-X3.
- **N4** (`pr241_scaffold_validator_module_sha256`): PASS — constant `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904` empirically verified bit-for-bit via `shasum -a 256` on the PR #241 validator module.
- **N5** (Q1 single row): PASS — subfield count grows 3 → 5 (with N-X4 additions) but Q1 stays a single decision row; no Q1a/Q1b split.

### Outcome A (Layer-1 planning-only PR)

**PASS.** Plan describes Layer-1 PR = exactly 2 files (`planning/current_plan.md` + `planning/current_plan.critique.md`). Future Layer-2 PR = 11 files (9 deliverable + 2 inherited planning). §Files explicitly NOT touched enumerates all frozen artifacts; §Out of scope enumerates all deferred work.

### Plan-structure compliance (pre-commit hook gate)

All 8 required `##` sections present: `## Scope`, `## Problem Statement`, `## Assumptions & Unknowns`, `## Literature Context`, `## Execution Steps`, `## File Manifest`, `## Gate Condition`, `## Open Questions`. Bonus sections `## Out of scope` and `## Self-check against B-X1, B-X2, N-X1, N-X2, N-X3, N-X4 + preserved B1+N1-N5` are informational and permitted.

## Round 3 NITs (3, all NIT-level; executor-resolvable)

### N-R3-A — orphan-helper documentation gap

The `HELPER_TO_FALSIFIER_KEY` mapping table declares 20 helpers, but T02/T03 explicitly say "Implement <helper>" for only 18 of them. The remaining 2 — `_check_materialization_creep` and `_check_decision_count` — are referenced in the priority chain and the mapping table but have no T-step instruction telling the executor to implement them. The executor must infer them from the priority-chain descriptions ("exactly 8 decisions, no more no fewer" / "no decision row has `materialized_output_paths != \"\"`") and from the test classes `TestExactEightDecisionsPresent` + `TestMaterializationCreepRejected`. This will likely succeed but the asymmetry is a documentation gap.

**Recommended executor action:** add explicit "Implement `_check_materialization_creep`" and "Implement `_check_decision_count`" bullets to T03 (or T04) before module implementation begins. Both are trivial.

### N-R3-B — test-fixture cross-dependency on Q6 deferred-pass branch

T06 `TestQ6RatingEvidenceSufficiency` deferred-pass branch only specifies `evidence_paths` non-empty + `"deferred_blocker because:"` in notes. But the COMPANION falsifier `_check_q6_rating_forward_only` (distinct from `_check_q6_rating_default_deferred`) ALWAYS requires the three forward-only phrases in Q6 notes regardless of verdict. The deferred-pass fixture should also include the forward-only phrases (otherwise it will halt on `q6_rating_forward_only_missing` even though `q6_rating_default_deferred_violated` passed). The recommended Q6 notes binding at T05 Q6 contains those phrases, so the executor can resolve this — but the test specification should make the dependency explicit.

**Recommended executor action:** in the test fixture for `TestQ6RatingEvidenceSufficiency` deferred-pass, include the recommended Q6 notes text from T05 Q6 (which already contains the forward-only phrases). Trivial.

### N-R3-C — priority-chain constant vs in-function list

T04 step 4 describes the falsifier priority chain as an inline bulleted list with no explicit "declare `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` constant" instruction. But T06 `TestPriorityChainReferencesMapping` needs to "parse the constant or list-of-names in the module". The executor must choose between (a) a module-level constant or (b) a discoverable in-function list. The plan permits both ("the constant or list-of-names") but doesn't pin one.

**Recommended executor action:** declare `FALSIFIER_PRIORITY_CHAIN: tuple[str, ...]` as a module-level constant for testability and provenance. Trivial.

## Empirical anchors verified

- Master HEAD: `3c6709bfc21baba893d34a3b87c308d7f8ba787e` (unchanged across all 3 rounds)
- `pyproject.toml` version: `3.72.0` (unchanged; Layer-1 planning PR is version-neutral)
- PR #241 validator SHA-256: `b9df4ccfd6bee46d8c6e3ef55d3b9498dcd5b10615064eb2618e93ad9f208904` (empirically matches the plan's hardcoded constant)
- `matches_history_minimal.yaml` line 24: `TRY_CAST(matches_flat_clean.details_timeUTC AS TIMESTAMP)` (validates the canonical TRY_CAST choice)
- 5 verbatim spec/schema passages cited in T05 Q1 (Option A for N-X2) all match the source files at the stated line numbers

## Final recommendation

**Materialize this plan to `planning/current_plan.md` and open the Layer-1 draft PR.**

The 3 NITs are documentation-level gaps that the Layer-2 executor can resolve during execution. No blocker remains. The plan is methodology-correct, empirically anchored, and respects every hard-stop (Layer-1 = 2 files; no execution, no materialization, no status YAMLs, no research_log, no ROADMAP, no CHANGELOG/pyproject/INDEX in this PR, no Phase 03, no Step 02_01_04, no merge, no ready-for-review).

The cap (3 rounds) is honored. No round 4 is available without explicit user override.
