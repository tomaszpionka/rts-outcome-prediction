# Plan critique — SC2EGSet Step 02_01_01 V-8 source-grain structural well-formedness

---
target_plan: planning/current_plan.md
target_branch: phase02/sc2egset-feature-registry-v8-source-grain-well-formedness
target_commit_at_review: master @ 7b26b40f (workspace HEAD; branch not yet created)
reviewer: reviewer-deep
reviewer_date: 2026-05-09
critique_round: 1
verdict: PASS-WITH-FIXES
---

## §Summary verdict

The plan's central methodological move — pivoting from the user's framing "V-8 = D10 source-grain well-formedness" to "V-8 = source-grain structural well-formedness + provenance-key consistency, explicitly disjoint from spec-D10 (focal/opponent symmetry)" — is correct and well-supported. Spec text is verified verbatim, the absence of a controlled enum on the `source_grain` column is verified by live extraction, and the proposed helper passes 26/26 rows of the merged skeleton with 0 violations. The notebook narrative renaming is also correct: the deferred-D-list at lines 538–539 inherited from PR #212 misnamed D10, and that local documentation defect is what this PR closes alongside the new validator. This is not a methodology BLOCKER; reviewer-adversarial is NOT required.

The plan does, however, contain several mechanical accuracy defects that would either trip the executor or muddy the diff at gate time. None are scientific; all are fixable in the plan text. The most material defect is an internal arithmetic inconsistency in the file-count gate (§Gate Condition §1 says "EXACTLY 8 files" while the §File Manifest lists 9). Three smaller mechanical fixes round out the required-fix list.

## §Re-verification of D10 spec claim

Spec text at `reports/specs/02_03_temporal_feature_audit_protocol.md` line 161 (CROSS-02-03-v1.0.1 §4.1) reads verbatim:

> **D10** | Focal/opponent symmetry and p0/p1 projection | Every per-player feature is computed by the same SQL pattern or function for the focal player and the opponent (Invariant I5). For aoestats, the `p0_*` / `p1_*` source asymmetry is resolved via the `canonical_slot` focal/opponent assignment (CROSS-02-00-v3.0.1 §5.2; aoestats-only column) before any feature computation that depends on player role. RISK-24 routes the operationalization to a Phase 02 ROADMAP step.

**Verdict: PASS.** D10 is unambiguously focal/opponent symmetry and p0/p1 projection (Invariant I5). It is NOT source-grain. The notebook's inherited paraphrase at line 538–539 (`D10 (source-grain well-formedness)`) disagrees with the locked spec. The plan's pivot is methodologically sound.

A confirming side-observation: spec D3 ("Source grain vs model grain") is the source-grain ↔ model-input-grain reconcilability dimension — which the plan explicitly defers to a future V-N. There is **no spec dimension** for "source-grain structural well-formedness"; V-8 is genuinely a registry-layer well-formedness validator that does not peg to a specific D-ID. The plan is honest about this: §Scope says "V-8 is NOT a controlled-vocabulary enum check ... it is NOT a focal/opponent-symmetry check ... it is NOT a relational source-grain ↔ model-input-grain reconcilability check (that is D3, deferred to a future V-N)."

## §Re-verification of source_grain enumeration

Live extraction by importing the on-disk SKELETON at master `7b26b40f` yields exactly 7 distinct `source_grain` values, with the counts matching the plan's §Verification §2 verbatim:

| count | source_grain |
|-------|--------------|
| 8 | `(filename, player_id_worldwide)` |
| 8 | `(filename, playerId)` |
| 3 | `(filename, controlPlayerId)` |
| 3 | `(filename, owner_via_unitborn_lineage)` |
| 2 | `(filename)` |
| 1 | `(filename, player_id_worldwide, opponent_player_id_worldwide)` |
| 1 | `(filename, killerPlayerId)` |

Total: 26 rows. **Verdict: PASS** on count, distinct-value count, and the per-bucket breakdown.

## §Re-verification of blocked-row sentinel claim

The 3 carve-out rows in the merged SKELETON carry the following literal `source_grain` values:

| feature_family_id | source_grain |
|---|---|
| `sc2egset.blocked_or_deferred.mind_control_event_count` | `(filename, playerId)` |
| `sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot` | `(filename, owner_via_unitborn_lineage)` |
| `sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields` | `(filename, playerId)` |

**Verdict: PASS.** All 3 carve-out rows carry real source-table key tuples. None carries a `"blocked"` sentinel on `source_grain`. The sentinel is correctly confined to `model_input_grain`, `target_grain`, `temporal_anchor`, `allowed_cutoff_rule`, `candidate_leakage_modes`, and `cold_start_handling` — six columns — exactly as the plan claims. V-8 has no carve-out conjunction and applies the same rule to all 26 rows. This is correct.

## §Per-question findings

### 1. D10 misnaming claim — **PASS**
Verified above. The renaming is the right call.

### 2. Source-grain no-enum claim — **PASS**
Verified above. The 7 distinct values are tuple-of-key-columns expressions, not a closed vocabulary enum.

### 3. Blocked-row sentinel claim — **PASS**
Verified above. 3 carve-out rows × real grain tuples, 0 sentinels on `source_grain`.

### 4. V-8 helper design — **PASS-WITH-NOTE**

Live simulation of `_check_v8_source_grain_well_formedness` against the on-disk SKELETON: **0 violations**, all 26 rows pass.

Edge-case probing on the regex `^\(filename(?:,\s*[A-Za-z_][A-Za-z0-9_]*)*\)$`:

| Input | Match? | Notes |
|-------|--------|-------|
| `()` | NO | rejects empty tuple — good |
| `(filename)` | YES | bare match-level form |
| `(filename,)` | NO | trailing comma rejected — good |
| `( filename)` | NO | leading whitespace rejected — good |
| `(Filename)` | NO | case-sensitive — good |
| `(filename, 123abc)` | NO | numeric prefix rejected — good (this is the implicit I7 check) |
| `(filename,playerId)` | YES | no-space comma accepted (`\s*` allows zero spaces) |
| `(filename, _playerId)` | YES | leading-underscore identifiers accepted (Python convention) |
| `(filename, playerId,)` | NO | trailing comma rejected — good |
| `(filename, player.id)` | NO | dotted identifiers rejected — good |

Tracker partition: live evaluation confirms 15 tracker rows, all using exclusively `{playerId, controlPlayerId, killerPlayerId, owner_via_unitborn_lineage}` (the 4 documented attribution keys). 0 tracker rows use bare `(filename)`. Non-tracker partition: 11 rows; 9 use `player_id_worldwide`, 1 uses both worldwide-identity keys, 2 use bare `(filename)` (`map_type_encoded`, `patch_version_encoded`). All keys are in the declared vocabulary. The bare-`(filename)` form is correctly accepted on the non-tracker side and is not actually used on the tracker side, but the helper as written would also accept it on the tracker side (an empty `extra_keys` list passes the `for k in extra_keys` loop trivially). **Note:** this is intentional and harmless — no tracker row in the merged skeleton uses bare `(filename)`, but if a future row did, V-8 would not fire. If a stricter "tracker rows must carry exactly one attribution key" rule is desirable, that is a future V-N concern, not a V-8 fix.

### 5. Step 0 fixture-update completeness — **PASS**

The 5 fixture rows the plan names are present at the expected positions in `tests/.../test_validate_registry_skeleton.py`:

| `source_table_or_event_family` | feature_family_id (fixture row) | proposed `source_grain` |
|---|---|---|
| `tracker_events_raw.UnitBorn` | `count_units_built_by_cutoff_loop` | `(filename, controlPlayerId)` |
| `tracker_events_raw.PlayerSetup` | `slot_identity_consistency` | `(filename, playerId)` |
| `tracker_events_raw.UnitOwnerChange` | `mind_control_event_count` | `(filename, playerId)` |
| `tracker_events_raw.UnitPositions` | `army_centroid_at_cutoff_snapshot` | `(filename, owner_via_unitborn_lineage)` |
| `tracker_events_raw.PlayerStats` | `playerstats_cumulative_economy_fields` | `(filename, playerId)` |

Each proposed `source_grain` matches the merged-skeleton tracker partition for the same source. The history fixture row uses `source_table_or_event_family="matches_flat"` (non-tracker) and inherits the default `(filename, player_id_worldwide)` — clean. The pre_game fixture row uses `source_table_or_event_family="replay_players_raw"` (non-tracker) and inherits the same default — clean.

No additional fixture rows need updating. **Verdict: PASS.**

### 6. Narrative line numbers — **PASS-WITH-NOTE**

Lines as they exist at master `7b26b40f`:

- Line 144 is the *second* line of the multi-line spillover that begins at line 143. The plan's "Before" quote spans lines 143–144. Calling it "line 144" is mildly imprecise.
- Line 500 is the *last* line of the deferred-D-list block spanning lines 496–500. The plan promises to "rename source-grain well-formedness out of D10" at line 500, but at line 500 the D-list is just D-IDs without parenthetical names. The phrase "source-grain well-formedness" only appears at lines 538–539. The plan should specify the replacement at line 500 simply drops `D11` from the list.
- Line 507 print-banner — exact match.
- Line 539 — second line of the spillover starting at line 538 (`D10 (source-grain` straddles 538–539).

**Verdict: PASS-WITH-NOTE.** All four target locations are correct in intent. The line-number labels are slightly imprecise on the multi-line spillovers. Minor fix; non-blocker.

### 7. Changed-files scope — **FIX**

The §File Manifest / Allowed table enumerates 9 committed files: 4 code + 2 release + 3 planning = 9.

The §Gate Condition §1 reads "EXACTLY 8 files". This is wrong — total committed files = 9. The gate-condition arithmetic is off-by-one. This will cause the executor (or reviewer-deep at T09) to flag a false-positive "extra file" failure if read literally. **Fix: change "EXACTLY 8 files" to "EXACTLY 9 files"** (see §Required fixes §F1).

### 8. PR #213 follow-up handling — **PASS**

- Item #3 (`_row()` conjunction-discipline reminder docstring): folded into T02 as optional addition. Reasonable.
- Items #4 (defensive-branch coverage on lines 294/362/368) and #5 (`parents[6]` test-infra magic): deferred to a hygiene PR. Defensible per the same rationale as PR #213.
- Item #6 (plan-frontmatter date semantics): resolved as "plan-authoring date convention" with `date: 2026-05-09`. Internally consistent with PR #213's convention.

### 9. D-coverage matrix — **PASS-WITH-NOTE**

Plan §Problem Statement claims "After PR #213, eight CROSS-02-03-v1.0.1 §4.1 audit dimensions remain unaddressed by skeleton-layer validators (D2, D3, D4 in_game side, D5 in_game side, D8, D10, plus D6 partial and D9/D15 which are post-materialization and out-of-scope at this layer)". Cross-checking against §4.1 D1–D15:

| Dim | Title | Coverage status after PR #213 |
|---|---|---|
| D1 | Prediction setting admissibility | covered (V-1 controlled vocab) |
| D2 | Source classification + temporal availability | NOT covered |
| D3 | Source grain vs model grain | NOT covered (V-8 ≠ D3) |
| D4 | Temporal anchor correctness | history side covered (V-6); in_game side NOT |
| D5 | Cutoff operator correctness | history side covered (V-6); in_game side NOT |
| D6 | Target-game exclusion | partially covered (V-6 strict-`<` + post-outcome tokens) |
| D7 | Post-game token exclusion | covered (V-6 token list) |
| D8 | Full-replay aggregate exclusion | NOT covered |
| D9 | Normalization fit-scope | post-materialization, out of registry layer |
| D10 | Focal/opponent symmetry | NOT covered (intentional; future V-9 candidate) |
| D11 | Cold-start vocabulary, no magic numbers | covered (V-7) |
| D12 | Source-mode label discipline | partially relevant; sc2egset has no source-mode column |
| D13 | SC2 tracker eligibility | covered (V-2/V-3/V-4/V-5) |
| D14 | AoE2 source-label discipline | N/A for sc2egset |
| D15 | Artifact-lineage readiness | methodological discipline, not row-level |

Plan's enumeration is approximately right but reads slightly off. The in_game side of D4 / D5 is genuinely uncovered (V-6 only checks the history side); the plan doesn't currently flag this. **Non-blocker.** A future V-9 plan should restate the matrix accurately.

### 10. Test list completeness — **PASS-WITH-NOTE**

Plan T02b §Heading says "seven new tests" but the body lists **eight** tests numbered 1–8. The eighth is `test_v8_blocked_row_source_grain_still_validates` which is the most methodologically interesting one. Discrepancy in three places: heading, §Verification ("48+7=55"), and implicit reference in §Acceptance §3. **Fix: harmonize to "eight new tests" and "48+8=56 tests".** See §Required fixes §F2.

Edge cases not covered by the proposed test list:
- Empty `source_grain` (string `""`): would fail the explicit `assert sg, ...` in the helper. Currently uncovered by the proposed 8 tests.
- Whitespace-only `source_grain` (`"   "`): would pass the empty check and fail the regex. Uncovered.

**Non-blocker:** the plan can add one more test or fold this assertion's coverage into one of the existing tests.

### 11. Numeric-token concern carry-over — **PASS**

The regex `^\(filename(?:,\s*[A-Za-z_][A-Za-z0-9_]*)*\)$` requires `[A-Za-z_]` as the first character of every key. This is a syntactically tight implicit I7 numeric-token rejection: a key beginning with a digit (`123player`) cannot match. Test 4 (`test_v8_invalid_identifier_key_fails`) exercises exactly this with `(filename, 123player)`. The test failure mode is "regex does not match" rather than "numeric token rejected" — the diagnostic message is `"V-8.*does not match"`, which is fine. No separate I7 numeric helper is needed. **Plan is sound; no fix needed.**

### 12. Honesty check — **PASS-WITH-NOTE**

The plan's framing is largely accurate and transparent. Notable wins: honest about D10 misnaming (Defect 1), honest about no-enum (Defect 2), honest about scope ("V-8 in this PR closes a skeleton-layer well-formedness gap on the `source_grain` column without committing to spec-D10 semantics"), honest about V-9 candidate selection.

Mild overstatements / minor inaccuracies:
1. §Verification §3 says "9/9 non-tracker keys in-vocab or bare-form". The non-tracker partition has 11 rows: 9 use `player_id_worldwide`, 1 also uses `opponent_player_id_worldwide` (so row contributes 2 keys), 2 are bare. Counted per-row-with-keys: 9. Counted per-key: 10. The "9/9" is defensible as "9 rows-with-extra-keys, all of which carry only in-vocab keys" but slightly muddles the denominator. **Non-blocker.**
2. §Problem Statement says "After PR #213, eight ... dimensions ... plus D6 partial" totals 6 fully + 1 partial + 2 out-of-scope = 9 items, not 8. Arithmetic mild slip. **Non-blocker.**

## §Required fixes (PASS-WITH-FIXES)

### F1 (most material) — Gate Condition §1 file count off-by-one

**Where:** `planning/current_plan.md` §Gate Condition item 1 (and §Acceptance criteria item 4 if it contradicts).

**Problem:** "EXACTLY 8 files" should be "EXACTLY 9 files": 4 code + 2 release + 3 planning = 9.

**Fix:** Change `EXACTLY 8 files` to `EXACTLY 9 files` in §Gate Condition §1.

**Severity:** PASS-WITH-FIX. If left unfixed, T09 / reviewer-deep will misread the diff as "extra file" violation.

### F2 — T02b heading vs body test count mismatch

**Where:** `planning/current_plan.md` §T02b §Objective heading and §Verification.

**Problem:** Heading says "seven new tests"; body lists eight tests (numbered 1–8); §Verification says "48 + 7 = 55 tests".

**Fix:** Replace "seven" with "eight" in §Objective heading. Replace "48 + 7 = 55" with "48 + 8 = 56" in §Verification.

**Severity:** PASS-WITH-FIX. Defensive accuracy.

### F3 — T03 line-number precision (multi-line spillovers)

**Where:** `planning/current_plan.md` §T03 instructions table.

**Problem:** Lines 144 and 539 are the *second* lines of multi-line comment spillovers. The actual D-list and the `D10 (source-grain ...)` phrase span lines 143–144 and 538–539 respectively.

**Fix:** Update line numbers to "lines 143–144" and "lines 538–539".

**Severity:** PASS-WITH-FIX. Minor; executor would still find the right text.

### F4 — Line 500 narrative correction wording

**Where:** `planning/current_plan.md` §T03 instructions table for "Line 500".

**Problem:** Plan says "(rewritten block dropping D11, renaming D10 to focal/opponent symmetry)". At line 500 the only correction needed is to drop D11 from the list (since V-7 covers it). The "rename D10 to symmetry" phrasing is more accurate at lines 538–539, not at line 500.

**Fix:** Clarify §T03 row "Line 500" to "drop `D11` from the deferred-D-list (V-7 covers it)" only. The "rename D10 to symmetry" instruction stays unique to the lines-538–539 row.

**Severity:** PASS-WITH-FIX. Mechanical clarity.

## §Notes for the executor

- **N1** — The bare `(filename)` form is *currently* used only by non-tracker rows (`map_type_encoded`, `patch_version_encoded`). The V-8 helper as written would also accept it on the tracker side. No tracker row uses this form, so the helper is correct as designed.

- **N2** — The regex `[A-Za-z_]` first-character requirement implicitly enforces I7 (no numeric tokens in keys). Test 4 exercises this with `(filename, 123player)`. The diagnostic is "does not match" rather than "I7 numeric"; this is acceptable.

- **N3** — When updating the fixture (§T02b Step 0), confirm that the default-passing rows (history row at fixture index 1, pre_game row at fixture index 0) remain untouched.

- **N4** — Order of orchestrator checks after this PR will be: V-1 base → V-1 strict → V-2 → V-3 → V-4 → V-5 → V-6 → V-7 → V-8.

- **N5** — `(filename, 0x10)` would be rejected by the regex (`0` is not in `[A-Za-z_]`).

- **N6** — `source_table_or_event_family == ""` would route to the non-tracker branch. No SKELETON row has empty `source_table_or_event_family` (V-1 catches this case earlier).

- **N7** — The new constant `TRACKER_SOURCE_TABLE_PREFIX = "tracker_events_raw"` is a candidate for cross-helper reuse, but DO NOT refactor V-5 in this PR.

- **N8** — When jupytext-syncing the .ipynb after T03, confirm the diff against master shows ONLY the four narrative locations.

- **N9** — Test count at master `7b26b40f` is 48. After T02b lands 8 new V-8 tests + 5 fixture-row updates, total = 56. F2 fixes the count.

- **N10** — `pyproject.toml` line 3 currently reads `version = "3.49.0"`. T08 mechanical bump to `3.50.0` is clean. CHANGELOG `[Unreleased]` section is empty.

## §Acceptance for plan-side close

This plan is approved for execution after the following are applied to `planning/current_plan.md`:

1. **F1** — Gate Condition §1 file count: change "EXACTLY 8 files" to "EXACTLY 9 files".
2. **F2** — T02b heading and verification: change "seven new tests" to "eight new tests" and "48 + 7 = 55 tests" to "48 + 8 = 56 tests".
3. **F3** — T03 line-number precision: update "line 144" → "lines 143–144" and "line 539" → "lines 538–539".
4. **F4** — T03 line-500 narrative correction: clarify that the line-500 correction is "drop D11 from the deferred-D-list" only, not the D10 rename (the D10 rename is at lines 538–539).

After applying F1–F4, the plan reads accurately and the executor can proceed without ambiguity. No methodology BLOCKER was raised; the D10 misnaming pivot is sound; the V-8 helper design is correct on all 26 rows by live verification; the fixture update scope is correct. **Reviewer-adversarial is NOT needed.**
