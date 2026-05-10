# Plan critique — SC2EGSet Step 02_01_01 V-9 per-player construction / focal-opponent symmetry

---
target_plan: planning/current_plan.md
target_branch: phase02/sc2egset-feature-registry-v9-symmetry
target_commit_at_review: master @ 664c869a (workspace HEAD; branch not yet created at critique time)
reviewer: reviewer-deep
reviewer_date: 2026-05-10
critique_round: 1
verdict: PASS
---

## §Summary verdict

This is the cleanest of the four sequential V-N validator plans (PR #212 → #213 → #214 → this PR) and the strongest methodologically. The plan finally lands the actual spec-D10 binding — focal/opponent symmetry / Invariant I5 — at the registry-skeleton layer, and does so with a correct two-clause split: sub-clause 1 (symmetry, all datasets) is enforced for sc2egset; sub-clause 2 (aoestats `canonical_slot` p0/p1 projection) is recorded N/A for sc2egset on a spec-bound rationale (CROSS-02-00-v3.0.1 §5.2 documents `canonical_slot` as "aoestats-ONLY"). The validator design reuses V-7's conjunction predicate verbatim instead of redefining it — a mechanical signal of disciplined plan authoring. The on-disk skeleton's per_player_construction column has a clean two-value partition (23 × `"symmetric"` + 3 × `"blocked"` + 0 of anything else), so V-9 is non-vacuous and structurally guaranteed to pass on the unmodified skeleton. The Step 0 fixture lift is correctly identified as mandatory and is mechanically identical to the PR #214 / PR #213 patterns. No blockers and no required mechanical fixes were found. The single methodological choice that warrants discussion — admitting only `"symmetric"` and rejecting `"asymmetric"` outright at the registry layer — is defensible because Invariant I5 is categorical and asymmetric per-player construction is forbidden at the methodology layer above the registry; this critique walks through that argument explicitly in §Per-question finding 12 and concludes adversarial escalation is not warranted.

The plan is unusually long (1281 lines) but the length is earned: it carries explicit live-verification of every load-bearing claim against master `664c869a`, an explicit D-coverage matrix, and an Open-Questions block resolving the four methodology decisions that could otherwise drift in execution. Verdict: PASS — ready for T01 dispatch.

## §Re-verification of D10 spec claim (sub-clause 1 + sub-clause 2 N/A)

D10 verbatim from `reports/specs/02_03_temporal_feature_audit_protocol.md` line 161 (CROSS-02-03-v1.0.1 §4.1):

> **D10** | Focal/opponent symmetry and p0/p1 projection | Every per-player feature is computed by the same SQL pattern or function for the focal player and the opponent (Invariant I5). For aoestats, the `p0_*` / `p1_*` source asymmetry is resolved via the `canonical_slot` focal/opponent assignment (CROSS-02-00-v3.0.1 §5.2; aoestats-only column) before any feature computation that depends on player role. RISK-24 routes the operationalization to a Phase 02 ROADMAP step.

Two sub-clauses are clearly identifiable:
- **Sub-clause 1 (symmetry, all datasets per Invariant I5):** "Every per-player feature is computed by the same SQL pattern or function for the focal player and the opponent (Invariant I5)." — V-9 binds this for sc2egset.
- **Sub-clause 2 (aoestats p0/p1 projection):** "For aoestats, the `p0_*` / `p1_*` source asymmetry is resolved via the `canonical_slot` focal/opponent assignment (CROSS-02-00-v3.0.1 §5.2; aoestats-only column) before any feature computation that depends on player role." — explicitly aoestats-bound.

Confirming side-evidence on sub-clause 2's aoestats-only nature:
- `reports/specs/02_00_feature_input_contract.md` line 380 (§5.2 aoestats `matches_history_minimal` table): `canonical_slot | VARCHAR | PRE_GAME | aoestats-ONLY; slot_A/slot_B; hash-on-match_id; skill-orthogonal; NOT in MHM UNION ALL`.
- `reports/specs/02_00_feature_input_contract.md` line 369 section header: "§5.2 `matches_history_minimal` — aoestats (10 cols; canonical_slot is aoestats-local)".
- The sc2egset MHM table at §5.1 of the same spec carries no `canonical_slot` column. Live grep against `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/raw/*.yaml` returned no `canonical_slot` hits.

**Verdict: PASS.** D10 has exactly two sub-clauses; sub-clause 1 is what V-9 binds for sc2egset; sub-clause 2 is N/A for sc2egset on a spec-bound rationale and is correctly deferred to a future aoestats-side V-N PR.

## §Re-verification of `per_player_construction` partition

Live extraction against the merged 26-row SKELETON in `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` at master `664c869a`:

| Source block | Row | per_player_construction |
|---|---|---|
| SKELETON_PRE_GAME (lines 293–315) | `focal_race_with_opponent_race_pair` | `"symmetric"` |
| | `map_type_encoded` | `"symmetric"` |
| | `patch_version_encoded` | `"symmetric"` |
| | `matchup_encoded` | `"symmetric"` |
| | `is_mmr_missing_flag` | `"symmetric"` |
| SKELETON_HISTORY (lines 324–356) | `focal_player_history` | `"symmetric"` |
| | `opponent_player_history` | `"symmetric"` |
| | `matchup_history_aggregate` | `"symmetric"` |
| | `reconstructed_rating` | `"symmetric"` |
| | `cross_region_fragmentation_handling` | `"symmetric"` |
| | `in_game_history_aggregate` | `"symmetric"` |
| SKELETON_IN_GAME_NOW (lines 364–382) | `count_units_built_by_cutoff_loop` | `"symmetric"` |
| | `count_units_killed_by_cutoff_loop` | `"symmetric"` |
| | `morph_count_by_cutoff_loop` | `"symmetric"` |
| | `building_construction_count_by_cutoff_loop` | `"symmetric"` |
| SKELETON_IN_GAME_CAVEAT (lines 391–428) | `minerals_collection_rate_history_mean` | `"symmetric"` |
| | `army_value_at_5min_snapshot` | `"symmetric"` |
| | `supply_used_at_cutoff_snapshot` | `"symmetric"` |
| | `food_used_max_history` | `"symmetric"` |
| | `time_to_first_expansion_loop` | `"symmetric"` |
| | `count_units_lost_by_cutoff_loop` | `"symmetric"` |
| | `count_upgrades_by_cutoff_loop` | `"symmetric"` |
| SKELETON_GATE_AND_BLOCKED (lines 437–459) | `slot_identity_consistency` (sanity_gate) | `"symmetric"` |
| | `mind_control_event_count` (carve-out) | `"blocked"` |
| | `army_centroid_at_cutoff_snapshot` (carve-out) | `"blocked"` |
| | `playerstats_cumulative_economy_fields` (carve-out) | `"blocked"` |

Tallies: 23 × `"symmetric"` (5 pre_game + 6 history + 4 in_game_now + 7 in_game_caveat + 1 sanity_gate) + 3 × `"blocked"` (carve-out trio) + 0 × anything else.

**Verdict: PASS.** Partition matches the plan's §Verification §3 verbatim. The sanity_gate row carries `"symmetric"` (not a sentinel), as the plan claims. The 3 carve-out rows carry the `"blocked"` literal exactly. V-9 has 0 violations on the unmodified skeleton.

## §Re-verification of Invariant I5 binding

Invariant I5 verbatim from `.claude/scientific-invariants.md` line 158:

> Both players in every game must be treated identically by the feature pipeline. The same function that computes features for the focal player also computes features for the opponent. No player slot receives privileged treatment. The model input is always structured as `(focal_player_features, opponent_features, context_features)` and this structure is identical regardless of which player is focal.

23/23 model-input-or-sanity-gate rows carry `"symmetric"`. 0/23 carry `"asymmetric"` or any other token. The 3 carve-out rows are not model inputs (they carry `prediction_setting = "blocked_or_deferred"` and `status = "blocked_until_additional_validation"`) and so are exempt from the I5 binding at this layer.

Cross-confirming spec evidence:
- CROSS-02-02-v1.0.1 §5.1 (line 189–193 of `reports/specs/02_02_feature_engineering_plan.md`): "Focal/opponent symmetry (Invariant I5). Every per-player feature must be computed with the same function or SQL pattern for the focal player and the opponent."
- CROSS-02-02-v1.0.1 §6.2 line 239: opponent_player_history is "Symmetric (Invariant I5): same SQL pattern as focal."
- CROSS-02-02-v1.0.1 §4.2 line 167: "symmetric focal/opponent projection is a binding pre-modeling step (Invariant I5 symmetry)".

**Verdict: PASS.** Invariant I5 is upheld at the registry-skeleton layer. V-9 enforces this structurally.

## §Re-verification of V-7 constant reusability

`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` exposes the relevant constants at module scope:

- Line 147: `BLOCKED_SENTINEL: str = "blocked"`
- Line 150: `BLOCKED_PREDICTION_SETTING: str = "blocked_or_deferred"`
- Line 151: `BLOCKED_STATUS: str = "blocked_until_additional_validation"`

The V-7 helper at line 540 uses the exact predicate `is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and st == BLOCKED_STATUS)` and at line 543 asserts `cs == BLOCKED_SENTINEL`. The V-9 helper proposed in the plan (T01 step 2) uses the literally-identical predicate `is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and st == BLOCKED_STATUS)` and asserts `ppc == BLOCKED_SENTINEL` — no redefinition.

**Verdict: PASS.** All three constants exist at module scope, are public-import-safe, and are reusable by V-9 without redefinition. The plan's claim is correct.

## §Re-verification of fixture state

`tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py` line 65 verbatim:

```python
        "per_player_construction": "symmetric",
```

This line is inside the `_row()` helper's returned dict literal (lines 52–66) and is the single source of `per_player_construction` for every fixture row. Live count: the `valid_skeleton` fixture (lines 70–137) emits 7 rows via `_row()`, and indices 4, 5, 6 are the three blocked rows (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`) per the fixture body inspection at lines 107–136. The other 4 rows (indices 0–3: pre_game, history, in_game_snapshot model-input, sanity_gate `slot_identity_consistency`) are non-blocked and correctly inherit `"symmetric"` from the kwarg default the plan adds in T02.

**Verdict: PASS.** Plan's §Assumption 5 is correct: as-is, V-9 would FAIL on the existing fixture's three blocked rows because the V-9 conjunction predicate holds (`prediction_setting = "blocked_or_deferred"` AND `status = "blocked_until_additional_validation"`), so V-9 demands `BLOCKED_SENTINEL` ("blocked"), but the fixture provides `"symmetric"`. T02b Step 0 fixture lift on indices 4, 5, 6 is mandatory and the plan correctly identifies all 3 rows by feature_family_id.

## §Re-verification of notebook narrative line numbers

Verified live against `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` at master `664c869a`:

| Plan claim | File state | Match? |
|---|---|---|
| Line 484 starts the "Checks IN scope" markdown table | Line 484: `# \| Check \| What it asserts \|` | YES |
| Lines 484–491 = the 6-row V-1..V-6 table | Lines 486–491 enumerate V-1 through V-6 (one row per line) | YES |
| Line 493 = "Checks IN scope as of this PR" sentence | Line 493: `# Checks IN scope as of this PR (V-1 base, V-1 strict, V-2..V-7 from PRs` | YES |
| Line 500 = deferred-D-list `D2/D3/D6/D8/D9/D10/D12/D15` | Line 500: `# dimensions D2/D3/D6/D8/D9/D10/D12/D15.` | YES |
| Line 507 = print-banner `(V-1 through V-8)` | Line 507: `print("validate_registry_skeleton: ALL PASS (V-1 through V-8)")` | YES |
| Lines 535–543 = Follow-ups list with D8 misnaming + stale "deferred to a future V-9" | Lines 535–543 contain literally `D8 (per_player_construction\n#   symmetry)` and `D10 ... NOT\n#   source-grain — V-8 of this PR covers source-grain well-formedness;\n#   spec-D10 is symmetry, deferred to a future V-9` | YES |

**Verdict: PASS.** Every line number cited in the plan is correct against master `664c869a`. T03's surgical narrative-only edits at lines 484–491 (table append), 493 (sentence), 500 (D-list), 507 (banner), and 535–543 (Follow-ups) are well-targeted and avoid the SKELETON_* row literals at lines 269–474.

## §Per-question findings

### 1. D10 spec text (sub-clause 1) verification — **PASS**

Re-verified D10 verbatim above. Sub-clause 1 is "Every per-player feature is computed by the same SQL pattern or function for the focal player and the opponent (Invariant I5)" — exactly what V-9 binds. The plan quotes this correctly in §Problem Statement (Verification 1) and in §Literature Context.

### 2. D10 sub-clause 2 N/A determination for sc2egset — **PASS**

CROSS-02-00-v3.0.1 §5.2 documents `canonical_slot` as "aoestats-ONLY" / "NOT in MHM UNION ALL" (§5.2 line 380). The sc2egset `matches_history_minimal` schema at §5.1 of the same spec carries no `canonical_slot` column. SC2EGSet's per-player slot semantics derive from `replay_players_raw` (per-player rows) and tracker `playerId` / `controlPlayerId` / `killerPlayerId` / `owner_via_unitborn_lineage`, all of which are already per-player-keyed. Sub-clause 2 has no operational target on sc2egset, so the N/A determination is methodologically defensible. The plan defers operationalization to a future aoestats-side V-N PR — the correct cross-game routing.

### 3. `per_player_construction` column existence and value partition (live) — **PASS**

Verified above. Column is `_COLS[12]` in the notebook (line 282) and `REQUIRED_COLUMNS[12]` in the validator (line 82). Partition: 23 × `"symmetric"` + 3 × `"blocked"` + 0 × anything else. Sanity-gate row carries `"symmetric"` (not a sentinel). Carve-out rows carry the literal `"blocked"`.

### 4. Invariant I5 binding — **PASS**

Verified above. All 23 model-input-or-sanity-gate rows carry `"symmetric"`. The categorical rejection of `"asymmetric"` at the registry-skeleton layer is the methodologically correct binding for I5; see §Per-question finding 12 below for the longer treatment.

### 5. V-9 helper design — **PASS**

Line-by-line review of the proposed `_check_v9_per_player_construction_vocabulary` helper:

- **Reuses V-7 constants without redefinition.** The plan's T01 §Instructions §1 introduces a single new constant `PER_PLAYER_CONSTRUCTION_VOCAB = frozenset({"symmetric"})` and explicitly NOTES that the conjunction predicate is "literally identical to V-7's" (Verification §8). T01 step 2's helper body uses `BLOCKED_PREDICTION_SETTING`, `BLOCKED_STATUS`, `BLOCKED_SENTINEL` by name — no shadowing, no redefinition.
- **Type-guard for non-empty string.** The proposed helper has both `assert isinstance(ppc, str)` and `assert ppc` (non-empty). This matches V-7's pattern at lines 521–524 and V-8's at lines 586–592.
- **Conjunction predicate is identical.** `is_carve_out = (ps == BLOCKED_PREDICTION_SETTING and st == BLOCKED_STATUS)` — character-for-character match to V-7 line 540.
- **Branches are correctly inverted.** Carve-out → must equal `BLOCKED_SENTINEL` (`"blocked"`); else (every model-input + sanity_gate row) → must be in `PER_PLAYER_CONSTRUCTION_VOCAB` (i.e., `"symmetric"`). Both failure messages cite Invariant I5 / CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1 in the assertion text.
- **No new conjunction logic introduced.** The plan calls this out explicitly as a stop condition in T01 §Task-specific stop condition (item c).

### 6. Step-0 fixture lift completeness — **PASS**

Verified above. Three named fixture rows exist at the expected indices (4, 5, 6) with the named feature_family_ids; the helper currently hard-codes `"symmetric"` on all 7 rows; the four non-blocked fixture rows (indices 0–3) correctly inherit `"symmetric"` from the kwarg default added in T02. T02b Step 0 lifts exactly the 3 blocked rows by passing `per_player_construction="blocked"` explicitly. The Step 0 mandatoriness is correctly identified.

### 7. Notebook narrative line numbers — **PASS**

Verified above. All 5 cited line locations (484–491, 493, 500, 507, 535–543) match the file state at master `664c869a` exactly.

### 8. Changed-files scope (EXACTLY 9) — **PASS**

§File Manifest / Allowed lists 9 committed files. §Gate Condition §1 says "EXACTLY 9 files" matching the manifest count. The lessons-learned-from-PR-#214-F1 file-count discipline is applied correctly. (The two `.github/tmp/*.txt` scratch files are explicitly listed as "not committed".)

### 9. PR #213/#214 follow-up handling — **PASS**

Three PR #213/#214 carry-forward items are deferred to a separate hygiene PR:
- defensive-branch coverage on validator lines 347 / 415 / 421
- test-infra `parents[6]` magic at test file line 25
- V-8 helper bare-`(filename)` permissiveness on tracker rows

None of these affects V-9's correctness or scope. Deferring them keeps the V-9 PR's diff narrow (9 files, validator additions only) and avoids blending hygiene changes with a methodology-binding validator. Defensible.

### 10. D-coverage matrix (post-V-9) — **PASS**

Plan's §Literature Context table is accurate against the merged D-list. After V-9, only D2, D3, D4-in_game, D5-in_game, D6-full, D8 remain unaddressed at the registry-skeleton layer. The conclusion "Step 02_01_01 closure is NOT defensible after this PR" is correct and the plan correctly does not attempt closure.

### 11. Test list completeness — **PASS-WITH-NOTE**

Plan T02b lists 7 V-9 tests covering the carve-out conjunction in both directions, the type-guard, and the asymmetric/unknown-token rejections. Two minor test-shape gaps that the executor may want to fold in opportunistically (NOT BLOCKERS):

**Note 1 — empty-string test missing.** V-9's helper proposes `assert ppc, ...` for empty-string, but no test exercises it. If the executor adds `test_v9_empty_string_fails` (set row 0's `per_player_construction = ""`), V-9's coverage on the new helper is provably 100% on every line.

**Note 2 — sanity_gate row passes path is not asserted explicitly.** Test 1 (happy path) is the only test that exercises the sanity_gate row's `"symmetric"` value; if the executor wanted a more explicit assertion (e.g., `test_v9_sanity_gate_carries_symmetric_passes`), it would document the design decision that the sanity_gate row is treated identically to model-input rows for V-9 purposes. Not a coverage requirement but a clarity-of-intent one.

Both notes are PASS-WITH-NOTE follow-ups, not BLOCKERS. The 7 listed tests are sufficient for V-9's correctness.

### 12. Methodology defensibility — admitting only `"symmetric"` — **PASS**

This is the load-bearing methodological choice and warrants the longest treatment.

**The choice.** V-9 admits exactly one non-blocked token: `"symmetric"`. Any other value — `"asymmetric"`, `"match_level"`, `"per_player_role"`, etc. — is rejected outright at the registry-skeleton layer.

**The case for the choice (plan's argument).** Invariant I5 is categorical: "Both players in every game must be treated identically by the feature pipeline." Asymmetric per-player feature construction is not just discouraged; it is forbidden by the binding methodology layer. Admitting `"asymmetric"` as a legal token at the registry would create a vocabulary slot that no row may legitimately occupy, which is a methodological smell — controlled vocabularies should describe what is actually allowed, not enumerate forbidden states. The on-disk skeleton has 0 asymmetric rows because the spec authors correctly understood that asymmetric construction is forbidden; V-9 ratifies that empirical fact at the structural layer.

**The case against the choice (steel-man).** A hypothetical future row that legitimately needs asymmetric construction — say, a "focal player did X to opponent" direction-of-action feature where the SQL for the focal-side computation differs from the opponent-side computation by a slot-aware filter — would be rejected at the registry layer before it can even be discussed.

**Adjudication.** The steel-man is weaker than it appears. Three reasons:

1. **The methodological forbidding is upstream of V-9.** Invariant I5 categorically forbids asymmetric per-player computation, with the rationale: `P(A wins | A focal) + P(B wins | A focal) = 1`. Asymmetric construction breaks this consistency. Any direction-of-action feature must be representable as a symmetric pair (e.g., `focal_kills_opponent_units` and `opponent_kills_focal_units`, computed by the same SQL with role-swapped inputs). The "different SQL per slot" scenario is a methodological violation, not an unmet design need.

2. **The skeleton is the right layer to enforce this categorically.** The registry-skeleton layer is precisely the layer at which feature-family declarations get reviewed against Invariant I5. If a future feature family genuinely needs asymmetric construction, the path is to (a) amend the spec with an explicit Invariant I5 carve-out and a worked counterexample, then (b) widen `PER_PLAYER_CONSTRUCTION_VOCAB`. This is the correct sequencing — vocabulary widening downstream of spec amendment, not the other way around.

3. **`"match_level"` for map/patch rows is the only plausible alternative token, and the plan addresses it directly.** Map and patch rows carry an identical constant for both players in a match — which IS the degenerate case of symmetric construction. The on-disk skeleton already encodes it as `"symmetric"`; widening to admit `"match_level"` would require a prior skeleton-row-content change that is explicitly out of scope.

**Verdict: PASS — defensible.** Reviewer-adversarial escalation is NOT warranted.

### 13. Honesty check — **PASS**

The plan is unusually transparent. Five honesty markers worth noting:

1. **Live verification block (§Verification before finalizing this plan, items 1–10).** Every load-bearing claim is explicitly marked "verified live by the planner against master `664c869a`" with file:line citations.
2. **N/A determination for sub-clause 2 is spec-bound, not assertion.** §Verification §5 cites CROSS-02-00-v3.0.1 §5.2 verbatim and the sc2egset MHM column count as evidence.
3. **Step 02_01_01 NOT closed by this PR.** §Out of scope and §Literature Context (D-coverage matrix) explicitly state that 5 dimensions plus D6 partial remain unaddressed. No silent closure attempt.
4. **The "symmetric-only" choice is flagged in §Unknowns as potentially drawing methodological pushback from reviewer-deep**, with the resolution argument prepared in advance. This signals genuine self-skepticism.
5. **Three carry-forward follow-ups from PR #213/#214 are explicitly deferred** (§Verification §10, §Out of scope) rather than silently dropped.

No claim is overstated. **Framing is accurate.**

## §Required fixes (if PASS-WITH-FIXES)

None.

## §Blockers (if BLOCKED)

None. Reviewer-adversarial escalation is NOT warranted.

## §Notes for the executor

These are advisory and non-blocking — none affects T01 dispatch.

1. **Optional: add `test_v9_empty_string_fails`.** Per §Per-question finding 11 Note 1, the empty-string branch in the new V-9 helper (`assert ppc, ...`) is reachable but not exercised by any of the 7 listed tests. A one-line test at the end of the V-9 test block would prove 100% coverage on the helper's added lines.

2. **Optional: add `test_v9_sanity_gate_carries_symmetric_passes`.** Per §Per-question finding 11 Note 2, this would document the explicit design decision that the sanity_gate row is treated identically to model-input rows for V-9 vocabulary purposes.

3. **T03 line-replacement table cell for "Lines 484–491 (markdown table) — append a `V-9` row".** The plan's "After" content is a single very long markdown table row; the executor should preserve the leading `# ` comment marker on every continuation line to keep the markdown cell parseable by jupytext. Verify the resulting `.py` cell still round-trips through `jupytext --sync` cleanly.

4. **T03 should preserve the existing leading `#   ` comment-indentation** on the rewritten Follow-ups paragraph (lines 535–543) so the bulleted hierarchy renders identically in the .ipynb. The plan's "After" content uses `# - D10 sub-clause 2 ...` to introduce a new bullet — confirm this matches the existing bullet style at line 535.

5. **T08 CHANGELOG bullet wording.** The plan's proposed bullet at T08 is long and includes nested escaped quotes (`{\"symmetric\"}`). Consider verifying the CHANGELOG markdown renders cleanly on GitHub before pushing.

6. **T09 reviewer-deep dispatch.** The plan correctly routes T09 to reviewer-deep (per `.claude/rules/data-analysis-lineage.md` line 24 Phase 02 carve-out) and only escalates to reviewer-adversarial on a methodology BLOCKER. No action needed; just preserve the routing.

## §Acceptance for plan-side close

The plan is approved for execution. T01 may fire. The executor is expected to:

1. Land the `docs(planning)` commit carrying this critique + the active-plan row update in `planning/INDEX.md` BEFORE T01 begins.
2. Execute T01 → T02 → T02b (Step 0 fixture lift first, then 7 V-9 tests) → T03 → T04 → T05 → T06 → T07 → T08 → T09 in that order, halting on any §Stop condition.
3. Honor the §File Manifest / Forbidden list — no `STEP_STATUS.yaml`, no `research_log.md`, no `INVARIANTS.md`, no `02_*` spec edits, no SKELETON_* row literal modifications, no aoestats / AoE2 file touches.
4. At T09, expect reviewer-deep to PASS (methodology defensibility for "symmetric-only" was adjudicated in §Per-question finding 12 above; if reviewer-deep at T09 raises a fresh methodology BLOCKER on grounds not enumerated here, route to reviewer-adversarial).
5. After merge, update `planning/INDEX.md` archive row with the merge SHA and PR number.

The non-batching lineage discipline (sequence step 6 — "Next validation module") is preserved: this PR adds exactly one validator, makes no artifact, and does not close Step 02_01_01.
