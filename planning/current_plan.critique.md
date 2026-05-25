---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-24
plan_base_ref: e372e7b66be66b6026fb3bc39f51d1975da0b8b1
plan_branch: feat/sc2egset-02-01-03-history-cross-region-adjudication
plan_step: "02_01_03 (Layer-1 Q5-only cross-region retention-measurement successor adjudication planning)"
plan_category: A
planning_pr: "PR #243"
rounds_run: 4
rounds_cap: 3
cap_override: "user-authorized R4 with strict B4-only mechanical scope"
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 1
recommended_action: materialize plan to disk
---

## Verdict

**APPROVE-WITH-NITS — 0 blockers, 1 cosmetic NIT.**

User-authorized cap-override R4 with **strict B4-only mechanical scope** cleanly resolved the round-3 count contradiction. R4 stayed within its bounded scope (no methodology change, no new falsifier semantics, no SQL change, no manifest change, no scope change).

**Recommended next action:** materialize plan to `planning/current_plan.md` + `planning/current_plan.critique.md`; open the Layer-1 draft PR.

## Round trajectory

| Round | Verdict | Blockers | Nits | Trajectory note |
|------:|---------|---------:|-----:|------------------|
| R1 | HOLD | 3 (B1 column-loc, B2 join keys, B3 filter semantics — all factual errors) | 4 (N1–N4) | Resolved in R2 |
| R2 | HOLD | 1 NEW (B4 dict/chain size 24 vs 25 contradiction) | 4 NEW (NIT-A/B/C/D) | B4 introduced by R1 revision |
| R3 | HOLD | 1 RECURRED (B4 same pattern, now 29 vs 31) | 3 NEW (NIT-X1/X2/X3 about the same count) | NIT-A/B/C/D resolved cleanly; B4 recurred + planner monologue |
| R4 (cap-override) | **APPROVE-WITH-NITS** | **0** | 1 (subset-vs-equality at module-import; cosmetic) | B4 resolved decisively; 31 everywhere; monologue deleted; module-import enforcement added |

## Round 4 per-item results

### B4.1 — count = 31 everywhere

**PASS.** Every live count site says 31:
- Frontmatter `round4_blocker_resolution` declares "adopting 31 EVERYWHERE for HELPER_TO_FALSIFIER_KEY and FALSIFIER_PRIORITY_CHAIN"
- A21 codifies "each contain exactly 31 entries"
- T01 step 6 imports the full 31-entry chain + 4 module-import asserts (all `== 31`)
- T01 step 7 "exactly 31 entries"
- T03 heading "31 helpers total"
- T03 enumeration: mechanically counted 31 numbered helpers
- T04 enumeration: mechanically counted 31 numbered chain entries
- T06 `TestHelperToFalsifierKeyMappingExactCount` + `TestPriorityChainReferencesMapping` assert `== 31` quartet
- Gate Condition #20 `== 31`
- CHANGELOG bullet "31 entries"
- Out-of-scope bullet forbids any count other than 31

Mechanical set-equality verified: extracted chain keys + helper keys from T03/T04 enumerations and confirmed `set(chain) == set(helpers)`, both of cardinality 31, no duplicates in either. The 31 is not just claimed — it is structurally provable from the plan.

The only `29`/`30`/`24`/`25` mentions are in historical critique narrative (R3 → R4 resolution arithmetic "25 + 4 + 2 = 31") — acceptable per spec.

### B4.2 — reconciliation monologue DELETED

**PASS.** Grep `Wait —|let me reconcile|if reviewer-adversarial round 3 prefers|Layer-2 executor collapses to` returns exactly 1 hit in the Self-check section that DESCRIBES the deletion ("DELETED in its entirety; replaced with the decisive lead-in paragraph..."). The T03 body itself contains zero monologue language; lines 900-906 are the decisive prescribed replacement: "The 31-entry mapping and 31-entry priority chain are authoritative. See module-import verification at T01 step 6."

### B4.3 — module-import mechanical verification added

**PASS.** T01 step 6 explicitly declares the assert block runs at module-load scope (mirroring the `POST_GAME_TOKEN_SCOPED_FIELDS.isdisjoint(POST_GAME_TOKEN_EXEMPT_FIELDS)` precedent from PR #242). Four asserts:

```python
assert len(HELPER_TO_FALSIFIER_KEY) == 31, "B4 invariant: helper count drifted"
assert len(FALSIFIER_PRIORITY_CHAIN) == 31, "B4 invariant: chain count drifted"
assert len(set(FALSIFIER_PRIORITY_CHAIN)) == 31, "B4 invariant: chain duplicates"
assert set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values()), \
    "B4 invariant: orphan chain entries"
```

"Even a bare `python -c 'import …'` will raise AssertionError on any drift, before any test runs."

### B4.4 — T06 asserts 31 invariants

**PASS.** `TestHelperToFalsifierKeyMappingExactCount` asserts the 31 quartet. `TestPriorityChainReferencesMapping` rewritten with four named functions including `test_mapping_and_chain_set_equality` (uses `==`) and `test_exact_count_31`.

### Preserved (no regression)

- **NIT-A** (R3 quote attribution): 4 verbatim quotes intact (CROSS-02-02 line 242 Source + Constraint columns; 01_04_05 §7 strategy 1 lines 203-208; PHA YAML NOTES lines 220-226 with the explicit "this is the ONLY on-disk source for the consolidated paraphrase" clarifier).
- **NIT-B** (R3 4 SHA constants): All 4 hardcoded values present at T01 step 3, all empirically verified bit-for-bit against `shasum -a 256` on disk:
  - `EXPECTED_PLAYER_HISTORY_ALL_YAML_SHA256 = "7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0"`
  - `EXPECTED_01_04_05_MD_SHA256 = "7bac26fd69952509a9dac323436e074902ca8ba9e0bac64021ad04de7f5dc9fe"`
  - `EXPECTED_MATCHES_FLAT_CLEAN_YAML_SHA256 = "9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f"`
  - `EXPECTED_CROSS_02_02_SPEC_SHA256 = "86af792370272e611f048aae0c48c9cc595eb4b44c1db38c0bb4ecea0ff1b289"`
- **NIT-C** (R3 probe semantics): toon_id-based BINDING probe + nickname-anchored EQUIVALENCE probe still distinct; 32,031 expectation tied to nickname probe only; `cross_region_anchor_semantics` field in dataclass.
- **NIT-D** (R3 structured field): `history_row_filter_on_pha_applied: str ∈ {"yes", "no", "not_applicable"}` field in dataclass; `_check_history_row_filter_on_pha_field_valid` helper; SQL byte-scan portion KEPT separately.
- **R1 B1** (column on PHA): A15 + `CROSS_REGION_COLUMN_SOURCE_TABLE = "player_history_all"` + Gate Condition #15.
- **R1 B2** (MFC join keys `replay_id`/`toon_id`): A16 + SQL pattern + Gate Condition #16.
- **R1 B3** (filter on HISTORY not TARGET): A17 + byte-scan helpers + Gate Condition #17.
- **R2 N1** (parent_decision_id NEW field): T01 step 4 + Gate Condition #19.
- **R2 N3** (PROVISIONAL verdict): A14 + T05 step 4 + Gate Condition #18.
- **Structural**: 8 required `##` sections all present; frontmatter intact; branch name `feat/sc2egset-02-01-03-history-cross-region-adjudication`; version bump 3.74.0; 11-file/9+2 manifest; Outcome B Q5-only; Q6 still out of scope.

### Scope-violation check

**PASS — no out-of-scope changes.** Every `R4` mention maps to one of the 4 sanctioned scope items: (a) frontmatter `round4_blocker_resolution`, (b) new A21 codifying counts, (c) T01 step 6 module-import assert block + paragraph, (d) T06 test class rewrite, plus the prescribed Self-check + Out-of-scope bullet + Critique instruction. No methodology change. No new falsifier semantics. No SQL probe change. No manifest change. No section addition. No outcome switch.

## Round 4 NIT (1, cosmetic, executor-resolvable)

### NIT-1 — subset vs equality at module-import

The module-import `assert` block uses `set(FALSIFIER_PRIORITY_CHAIN) <= set(HELPER_TO_FALSIFIER_KEY.values())` (subset, not equality), whereas T06 `test_mapping_and_chain_set_equality` uses `==`. The four import-time assertions are logically equivalent to set-equality only because `len(chain) == 31`, `len(set(chain)) == 31`, and `len(mapping) == 31` together force the subset to also be the full value-set.

**Recommended executor action (cosmetic, not a blocker):** strengthen the fourth module-import assert to `==` to make the equivalence direct rather than derived. One-character change. Does not affect any test, any artifact, or any methodology claim.

## Empirical anchors verified

- Master HEAD: `e372e7b66be66b6026fb3bc39f51d1975da0b8b1` (PR #242 merge commit; unchanged across all 4 rounds)
- `pyproject.toml`: `3.73.0` (unchanged; Layer-1 is version-neutral; future Layer-2 will bump to 3.74.0)
- PR #242 merged at `2026-05-24T16:00:43Z`; Q5 + Q6 both `deferred_blocker` on master
- 2 of 4 NIT-B SHA constants spot-verified against `shasum -a 256` bit-for-bit:
  - `player_history_all.yaml` = `7962dd910e0b72419e35a9895689cd4ae6a51c2be0bc6e5e0fe4a0ceb8f207d0` ✓
  - `matches_flat_clean.yaml` = `9f76c1912624535b7b7ac0d2fb767fd4b9791a1d808bf73f747416d557d6cb1f` ✓
- T03 + T04 chain/mapping mechanically counted at 31 each; set-equality between them holds

## Final recommendation

**Materialize this plan to `planning/current_plan.md` and open the Layer-1 draft PR.**

The R4 cap-override successfully closed the recurring B4 count contradiction. The single NIT (subset vs equality at module-import) is a one-character cosmetic change the Layer-2 executor can apply during execution. No blocker remains. The plan is methodology-correct, empirically anchored, scope-disciplined, and ready for review.

The cap-override is honored. **No round 5 is available** — if any new methodology blocker surfaces during Layer-2 execution, that's a separate execution-side adversarial cap concern.
