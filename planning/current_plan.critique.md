---
critique_role: reviewer-adversarial
critique_model: claude-opus-4-7[1m]
critique_round: 3
critique_date: 2026-05-28
plan_file: planning/current_plan.md
plan_branch: feat/sc2egset-02-01-03-five-family-materialization
plan_layer: 1
plan_chosen_outcome: A
plan_category: A
plan_base_ref: 3ab48b3025f17ce62843d7300195e8094c893a72
round_cap: "3 rounds total (planning-side) per feedback_adversarial_cap_execution.md."
round_cap_symmetry: "Same 3-round cap applies to execution-side review."
rounds_used: 3
round_1_verdict: HOLD
round_1_blockers_count: 4
round_1_nits_count: 11
round_2_verdict: HOLD
round_2_blockers_count: 4
round_2_nits_count: 2
round_3_verdict: APPROVE-WITH-NITS
round_3_blockers_count: 0
round_3_nits_count: 1
final_verdict: APPROVE-WITH-NITS
final_blockers_count: 0
final_nits_count: 0
final_nits_resolved_in_finalization: [R3-NI-B-test-count-floor-harmonized-to-66]
axes_evaluated_round_1: 25
axes_evaluated_round_2: 17
axes_evaluated_round_3: 10
---

# Reviewer-adversarial critique log — SC2EGSet Step 02_01_03 five-family materialization (Layer-1 planning PR)

Plan: SC2EGSet Step 02_01_03 five-family materialization (Layer-1; future Layer-2 materialization execution)
Phase: 02 — Feature Engineering / Pipeline Section 02_01 / Step 02_01_03 (host)
Branch: `feat/sc2egset-02-01-03-five-family-materialization`
Base ref: `3ab48b3025f17ce62843d7300195e8094c893a72` (PR #257 merge commit)
Date: 2026-05-28

**Final verdict (Round 3): APPROVE-WITH-NITS with 0 blockers and 1 non-blocking nit (R3-NI-B test-count floor inconsistency 60/63/66), harmonized by the parent at materialization time (all `≥60 tests` / `≥60 named test cases` / `≥63 named test cases` references swept to `≥66 named test cases` to match T05's actual enumeration of 66 tests).**

Cap protocol: 3 planning-side rounds (`feedback_adversarial_cap_execution.md`); this log reaches Round 3 without escalation.

---

## Round 1 — verdict: HOLD (4 blockers + 11 non-blocking nits)

### Round 1 blockers

- **R1-B1 — Layer-2 file count 10 vs 11.** Plan claimed PR #236 was 10 files; `git show 51288130 --stat` proves PR #236 was 11 files including a 30-line `research_log.md` entry. Plan's "10-file diff exactly" claim was a factual misreading of precedent. **Required remediation:** include `research_log.md` in the canonical Layer-2 diff (matching PR #236) OR justify the deviation explicitly. **Resolved in Round 2.**

- **R1-B2 — History-source layer asymmetry causes false-positive heads-up.** `player_history_all` is all-game-types (per Q1 BINDING, justified for cold-start support), but the `matchup_history_aggregate` CTE joined on shared `replay_id` without restricting to 1v1 replays. Two players who shared a non-1v1 historical match (as teammates in 4v4, as opponents in 2v2, etc.) would generate spurious head-to-head counts. `focal_prior_win_rate_decisive` and `opponent_prior_win_rate_decisive` similarly aggregated win rates across game types, not 1v1 only. **Required remediation:** (a) restrict matchup CTE to 1v1 history via `JOIN matches_flat_clean mfc_h ON mfc_h.replay_id = ph_focal.replay_id`; (b) document the cross-game-type win-rate aggregation in audit MD §1 as a deliberate Q1-binding consequence. **Resolved in Round 2** (option (a) for matchup + partial (b) for per-player win-rates).

- **R1-B3 — A22 / OQ4 default "no `research_log.md` entry per PR #236 precedent" is factually wrong.** PR #236 DID add a 30-line `research_log.md` entry with `closure_status: still_open`. **Required remediation:** elevate A22 default to "MUST add a single dataset `research_log.md` entry with `closure_status: still_open`, `materialization_state: materialized`, `leakage_audit_state: post_materialization_pass`, `features_audited_count`, `row_count`, `artifact`, `leakage_audit`". **Resolved in Round 2.**

- **R1-B4 — A13 SHA-pin count math wrong + PR #245 omitted.** A13 arithmetic "6 CSVs + 6 MDs = 12" contradicted "5 PRs × 2 = 10"; PR #245 CSV+MD (referenced as parents by PR #255 row) were NOT in the pin list. **Required remediation:** recompute the actual binding-parent count and include PR #245 artifacts in T01. **Resolved in Round 2 (partial)** — PR #245 added, count recomputed to 16, but a new SHA cross-contamination surfaced (Round 2 NI-6 → Round 3 R3-B3).

### Round 1 non-blocking nits

- **R1-N1** `FIVE_FAMILY_PERMITTED_SET` (frozenset, unordered) — add a `FIVE_FAMILY_CANONICAL_ORDER: tuple[str, ...]` for ordered display/audit. **Resolved in Round 2.**
- **R1-N2** A7 binding-chain logic should cite PR #255's `q5_policy` field as the explicit BINDING elevation, not just the byte-unchanged transitive argument. **Resolved in Round 2.**
- **R1-N3** Subsumed by R1-B4.
- **R1-N4** Sub-feature count per history-side family (3 of 6 listed in CROSS-02-02 §6.2 row 1) silently narrowed; justify or expand. **Resolved in Round 2** by widening to 6 sub-features per side (24 audited columns total).
- **R1-N5** Audit JSON schema extended §3 with 5+ custom fields; flag as "fields beyond §3" in audit MD. **Resolved in Round 2** via `custom_extensions` section.
- **R1-N6** Add a test pinning the JOIN-then-FILTER invariant (target row admitted, excluded by FILTER). **Resolved in Round 2** as `test_join_then_filter_invariant_target_row_admitted_but_excluded`.
- **R1-N7** W4 self-contradictory about `audit_date`; pin one convention. **Resolved in Round 2** as "materialization-execution date, mirroring PR #236 = 2026-05-23".
- **R1-N8** Notebook filename divergence (`_feature_materialization` scaffold vs `_materialization` new) undocumented. **Resolved in Round 2** by overwriting the scaffold in place per `sandbox/README.md` notebook contract.
- **R1-N9** Cross-region indicator symmetrization went beyond PR #243's text authority; cite Invariant I5 explicitly. **Resolved in Round 2** as audit MD §1 citation.
- **R1-N10** Tied to R1-N4; resolved.
- **R1-N11** Use `ph.is_decisive_result = TRUE` instead of inline `ph.result IN ('Win', 'Loss')`. **Resolved in Round 2.**

---

## Round 2 — verdict: HOLD (4 blockers + 2 non-blocking nits)

Round 2 confirmed all 4 Round 1 blockers were resolved in intent and 9 of 11 nits resolved cleanly. The revision surfaced **4 new internal-consistency blockers** (mechanical, not methodological) and **2 non-blocking nits**.

### Round 2 blockers (all surfaced by the revision)

- **R2-NI-1** T02 constants code block declared `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 30` and `EXPECTED_PARQUET_COLUMN_COUNT: int = 34`, then the prose immediately after said "Final pinned: = 24 / = 28". Self-acknowledged contradiction inside one section; an executor would copy the wrong constants and fail the falsifier. **Required remediation:** rewrite the code block to declare `= 24` / `= 28` directly. **Resolved in Round 3 (R3-B1).**

- **R2-NI-5** Constant comment `# 6+6+2+2+8+6+matchup-conditional rate already counted` listed six terms when there are only 5 families; trailing "+6" had no semantic referent. **Required remediation:** rewrite to `# 6+6+2+2+8 = 24 (5 families per FIVE_FAMILY_CANONICAL_ORDER)`. **Resolved in Round 3 (R3-B2).**

- **R2-NI-6** Plan attributed merge SHA `ee15d362` to BOTH PR #243 and PR #245. Verified via `gh pr view 243 --json mergeCommit`: PR #243's actual SHA is `445bae0197fa75b613443f8eafef114ff2bb6939`; `ee15d3625eee60688776219f533d4a5ceefb4b76` belongs exclusively to PR #245. The plan's test `test_q5_binding_sha_pin_matches_pr243_merge_sha` would fail at executor time. **Required remediation:** correct all PR #243 attributions. **Resolved in Round 3 (R3-B3).**

- **R2-B4-residual** Round 2 revision summary at line 11 said "raising audited column count from 18 to **30**"; File Manifest item 5 said "44,418 rows × 34 cols = 3 identity + 1 context + 30 audited"; File Manifest item 8 said `features_audited_count: 30`. All three contradicted the rest of the plan (which used 24). **Required remediation:** sweep-replace `30 audited → 24 audited`, `34 cols → 28 cols`, `from 18 to 30 → from 18 to 24`, `features_audited_count: 30 → features_audited_count: 24`. **Resolved in Round 3 (R3-B4).**

### Round 2 non-blocking nits

- **R2-NI-7** A13 claimed 16 BINDING parent artifact SHAs but audit JSON T07 enumerated 17 distinct SHA pins (12 Q-chain + 2 omit-closure + 1 registry + 1 tranche-1 Parquet + 1 tranche-1 audit JSON + 1 tranche-1 audit MD = 17, not 16). **Required remediation:** reconcile to 17 everywhere. **Resolved in Round 3 (R3-N1).**

- **R2-NI-N2** `matches_long_raw_yaml_sha256` pinned defensively but the view is not joined by the SQL. Add a clarifying note. **Resolved in Round 3 (R3-N2)** via audit MD §2 note.

---

## Round 3 — verdict: APPROVE-WITH-NITS (0 blockers + 1 non-blocking nit)

### Round 2 blocker resolution verification

- **R3-B1 — PASS.** `planning/current_plan.md` T02 constants block declares `EXPECTED_AUDITED_FEATURE_COLUMN_COUNT: int = 24` and `EXPECTED_PARQUET_COLUMN_COUNT: int = 28` directly. The Round 2 `= 30 / = 34` then-correction pattern is gone; constants block is self-consistent.

- **R3-B2 — PASS.** Comment reads `# 6 + 6 + 2 + 2 + 8 = 24 (Family 1 + Family 2 + Family 3 + Family 4 + Family 5 per FIVE_FAMILY_CANONICAL_ORDER)`. Single-source-of-truth phrasing. No trailing `+6`, no "matchup-conditional rate already counted" residue.

- **R3-B3 — PASS.** Verified via `gh pr view`: PR #243's merge SHA is `445bae0197fa75b613443f8eafef114ff2bb6939`; PR #245's is `ee15d3625eee60688776219f533d4a5ceefb4b76`. Both T01 and Literature Context attribute PR #243 to `445bae01` and PR #245 to `ee15d362` correctly. Cross-contamination resolved. A disambiguation test `test_pr245_binding_sha_pin_matches_pr245_merge_sha_ee15d362` exists.

- **R3-B4 — PASS.** `grep -n "= 30\|= 34\|30 audited\|34 cols\|features_audited_count: 30\|from 18 to 30"` returns matches ONLY in Round 3 meta-text (revision summary describing the fix). Zero matches in substantive plan body. `24 audited` / `28 cols` / `features_audited_count: 24` consistent across Scope, T03, T04 falsifier label, T05 test names, T07 audit JSON, T08 research_log labels, A15, A22, L4, gate summary.

### Round 2 nit resolution verification

- **R3-N1 — PASS.** A13, S2, L7, T01, dispatch instructions, and gate summary all say `17 BINDING parent artifact SHAs` consistently. Enumeration `12 Q-chain + 2 omit-closure + 1 registry + 3 tranche-1 = 17` appears at T01 and gate summary. Three new test cases enforce: `test_pr236_tranche1_three_sha_pins_distinct`, `test_total_binding_parent_sha_count_is_seventeen`, `test_matches_long_raw_yaml_pinned_defensively_not_joined`.

- **R3-N2 — PASS.** Audit MD §2 defensive-pin note added: "`matches_long_raw_yaml_sha256` is a defensive lineage-completeness pin (not a read-source pin) to detect future drift if a later revision joins this view; the current materialisation does NOT read `matches_long_raw`." Codified as A31, S26, L23, OQ13, and a named test.

### New-issue scans (Round 3)

- **R3-NI-A — PASS.** All 10 PR merge SHAs in the Round 3 revision summary enumeration (PR #236, #237, #241, #242, #243, #245, #247, #249, #251, #255, #257) verified via `gh pr view N --json mergeCommit,title`. Every prefix matches GitHub. PR titles also confirm each PR is what the plan claims it is.

- **R3-NI-B — NIT.** Test-count floors inconsistent across the plan: File Manifest said `≥60`; W7 and gate summary said `≥63`; T05 enumerated 66 test cases. All three floors technically satisfied by the actual count, but the inconsistency invites drift. **Handled by parent at materialization time** — all `≥60 tests` / `≥60 named test cases` / `≥63 named test cases` references swept to `≥66 named test cases` in `planning/current_plan.md`. The only remaining `≥60` / `≥63` reference is in the Round 3 revision-summary meta-text describing the fix.

- **R3-NI-C — PASS.** PR #236's actual research_log heading is `## 2026-05-23 — Materialize Step 02_01_02 pre_game tranche-1 Parquet + first non-vacuous CROSS-02-01 audit`. Round 3 plan's specified heading follows this pattern with the Step 02_01_03 / scope-noun substitution. Required sub-headings (Category, Dataset, Branch, PR, Step scope, What, Why, How (reproducibility), Findings, What this means, Decisions taken, Decisions deferred, Thesis mapping, Open questions / follow-ups, Acknowledged trade-offs, Scope notes) match PR #236's actual diff exactly.

- **R3-NI-D — PASS.** `sandbox/README.md` does not prohibit overwriting a notebook for phase transition within the same Step number. Hard rules (cell-size cap, read-only DuckDB, both files committed) are silent on overwrite semantics. The PR #233 → PR #236 lineage precedent (notebook updated, not replaced) supports this. Round 3's overwrite-in-place fix is permissible.

### Round 3 final blockers

None.

### Round 3 final non-blocking nits

- **R3-NI-B** Test-count floor inconsistency 60/63/66 — handled by parent at materialization time (all swept to ≥66 in `planning/current_plan.md`). Plan's T05 enumeration of 66 tests is the authoritative deliverable; gate floor and W7 / File Manifest / Scope all aligned to ≥66.

### Recommendation

**APPROVE-WITH-NITS.** All 4 Round 2 blockers resolved with line-level evidence; all 2 Round 2 nits resolved; all 10 PR SHAs in the Round 3 self-verification block independently verified against GitHub; PR #236's actual research_log heading and sub-headings mirrored faithfully; sandbox README permits the planned notebook overwrite. The only Round 3 non-blocking nit (R3-NI-B) was harmonized by the parent at materialization time.

Per the 3-round cap protocol, with 0 blockers and 0 outstanding nits, the parent materializes the plan + this critique log to:
- `planning/current_plan.md`
- `planning/current_plan.critique.md`

on branch `feat/sc2egset-02-01-03-five-family-materialization` and opens a DRAFT planning PR.

---

## Repo verifications performed (Rounds 1–3)

GitHub `gh pr view N --json mergeCommit,title,mergedAt`:
- PR #236 → `39298c0afd3a23bfbd4603415314af784a672952` (Materialize Step 02_01_02 pre_game tranche-1)
- PR #237 → `a16d78c2…` (Closure for Step 02_01_02)
- PR #241 → `3c6709bfc21baba893d34a3b87c308d7f8ba787e` (Step 02_01_03 history scaffold)
- PR #242 → `e372e7b6…` (Q1/Q2/Q3/Q4/Q7/Q8 adjudication)
- PR #243 → `445bae0197fa75b613443f8eafef114ff2bb6939` (Q5 cross-region adjudication) — Round 2 plan had this wrong as `ee15d362`; corrected in Round 3.
- PR #245 → `ee15d3625eee60688776219f533d4a5ceefb4b76` (Q6 rating-reconstruction successor adjudication)
- PR #247 → `779dc40a…` (Q6F rating-algorithm survey)
- PR #249 → `d9276194…` (Q6G implementation proof)
- PR #251 → `28bfc89f…` (Q6H path decision)
- PR #255 → `52f9c108…` (Step 02_01_99 omit-closure)
- PR #257 → `3ab48b30…` (ROADMAP materialization-scope amendment)

Repo files inspected (Rounds 1–3):
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (PR #257 amendment lines 2525–2618 + back-reference 2837–2849)
- `src/rts_predict/games/sc2/datasets/sc2egset/materialize_pre_game_features.py` (PR #236 template; confirms module-level constants, falsifier-priority chain, `_QUERY` suffix convention)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (PR #236 30-line precedent entry; field labels + sub-headings)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_02/leakage_audit_sc2egset.json` (PR #236 audit-schema template; `audit_date = 2026-05-23` convention)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml` (confirms `is_decisive_result` BOOLEAN; confirms all-game-types scope)
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml` (Q1 target source; used for matchup CTE 1v1 restriction)
- `reports/specs/02_00_feature_input_contract.md` (LOCKED CROSS-02-00-v3.0.1)
- `reports/specs/02_01_leakage_audit_protocol.md` (LOCKED CROSS-02-01-v1.0.1; §3 audit schema; §5 gate condition)
- `reports/specs/02_02_feature_engineering_plan.md` (LOCKED CROSS-02-02-v1.0.1; §6.2 row 1 verbatim 6-sub-feature enumeration)
- `reports/specs/02_03_temporal_feature_audit_protocol.md` (LOCKED CROSS-02-03-v1.0.1)
- `sandbox/README.md` (notebook contract; confirms overwrite-in-place is permissible)
- `.claude/scientific-invariants.md` (I3 strict-<; I5 symmetric; I6 verbatim SQL; I7 no magic numbers; I9 lineage; I10 relative paths)
- `.claude/ml-protocol.md` (three leakage failure modes)
- `.claude/rules/data-analysis-lineage.md` (non-batching sequence; sequence step 7 = artifact generation)
- `.claude/rules/python-code.md` (module-level UPPER_SNAKE; `_QUERY` suffix; mirrored tests; ≥95% branch coverage)
- `.claude/rules/git-workflow.md` (semver bump rules; PR body via `.github/tmp/pr.txt`; commit via `.github/tmp/commit.txt`)
