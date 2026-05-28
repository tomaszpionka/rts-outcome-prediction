---
plan_role: planner-science (Round 1)
plan_model: claude-opus-4-7[1m]
plan_round: 1
round_1_verdict: APPROVE-WITH-NITS
round_1_blockers_count: 0
round_1_nits_count: 2
round_1_nits_resolved_in_finalization: [NIT-1-halt-counter, NIT-2-verbatim-amendment-inline]
plan_date: 2026-05-28
date: 2026-05-28
plan_layer: 1
chosen_outcome: A
category: A
branch: feat/sc2egset-02-01-03-five-family-scope-amendment
base_ref: 52f9c1082b200019d080cce74e60567452020e18
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_03 (host of materialization-scope amendment note) + 02_01_99 (back-reference)"
non_batching_sequence_position: "ROADMAP scope amendment Layer-1 planning PR following the PR #239 / PR #253 ROADMAP-only stub precedent. Plans the future Layer-2 4-file ROADMAP-only execution PR that records PR #255's omit-closure decision as a materialization-scope amendment against Step 02_01_03 (host) and Step 02_01_99 (back-reference)."
critique_required: true
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate)"
adversarial_round_cap: "3 rounds total (planning-side) per feedback_adversarial_cap_execution.md."
adversarial_cap_symmetry: "Same 3-round cap applies to execution-side review per feedback_adversarial_cap_execution.md."
parent_layer_1_pr: "PR #254 (02_01_99 omit-closure artifact Layer-1; merged at master 0acc0e83)"
parent_layer_2_pr: "PR #255 (02_01_99 omit-closure artifact Layer-2; merged at master 52f9c108)"
planning_pr: "PR #256"
future_execution_pr: "PR #<TBD-future-Layer-2>"
future_execution_file_count: 4
future_execution_files:
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
  - "planning/INDEX.md"
  - "CHANGELOG.md"
  - "pyproject.toml"
future_version_bump: "3.80.0 → 3.81.0"
grep_token: "materialization_scope_amendment_post_pr_255"
five_family_permitted_set:
  - focal_player_history
  - opponent_player_history
  - matchup_history_aggregate
  - cross_region_fragmentation_handling
  - in_game_history_aggregate
excluded_family: reconstructed_rating
excluded_columns:
  - reconstructed_rating_focal_pre
  - reconstructed_rating_opp_pre
  - reconstructed_rating_diff
binding_parent_artifacts:
  - PR #243 Q5 cross-region adjudication (02_01_03_history_cross_region_adjudication.{csv,md})
  - PR #247 Q6F rating-algorithm survey (02_01_03_q6f_rating_algorithm_survey.{csv,md})
  - PR #249 Q6G rating-implementation proof (02_01_03_q6g_rating_implementation_proof.{csv,md})
  - PR #251 Q6H rating-path decision (02_01_03_q6h_rating_path_decision.{csv,md})
  - PR #253 ROADMAP stub for Step 02_01_99
  - PR #255 omit-closure decision artifact (02_01_99_rating_omit_closure.{csv,md})
halt_predicate_count: 9
hard_stops_layer_1:
  - "Only 2 files in this PR's diff: planning/current_plan.md, planning/current_plan.critique.md."
  - "NO ROADMAP edit, NO pyproject.toml bump, NO CHANGELOG.md edit, NO planning/INDEX.md archive flip."
  - "NO STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml byte change."
  - "NO research_log.md byte change (dataset or root)."
  - "NO spec / cleaning-layer YAML / thesis / docs / .claude / data / notebook / AoE2 byte change."
  - "NO source/test/notebook edit. NO Step 02_01_04. NO Phase 03. NO baseline modelling. NO new Q6X PR. NO merging. NO marking ready."
hard_stops_layer_2:
  - "Exactly 4-file diff: ROADMAP.md, planning/INDEX.md, CHANGELOG.md, pyproject.toml."
  - "NO feature value materialization (no .parquet under reports/artifacts/02_feature_engineering/)."
  - "NO CROSS-02-01 post-materialization audit (no reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md})."
  - "NO STEP_STATUS.yaml / PIPELINE_SECTION_STATUS.yaml / PHASE_STATUS.yaml row addition or mutation."
  - "NO research_log.md entry (dataset or root)."
  - "NO Step 02_01_03 closure (closure deferred to a separate later PR with materialization + non-vacuous audit)."
  - "NO Step 02_01_04 / Phase 03 / baseline modelling."
  - "NO Q6X PR / no re-opening of Q5/Q6F/Q6G/Q6H."
  - "NO five-family feature materialization (separate downstream PR)."
---

# Plan: SC2EGSet Step 02_01_03 five-family materialization-scope amendment (Layer-1, ROADMAP-only future execution)

**Outcome chosen:** **A** — ROADMAP scope amendment planning PR. This Layer-1 planning PR authors `planning/current_plan.md` + `planning/current_plan.critique.md` only; the future Layer-2 execution PR it plans is a ROADMAP-only 4-file diff that records the PR #255 omit-closure decision against Step `02_01_03` / `02_01_99`.

**One-paragraph rationale (repo evidence):** PR #255 merged at `52f9c108` records `q6_omission_status = intentionally_omitted_under_branch_iii`, `q6_not_silently_satisfied = TRUE`, `future_roadmap_scope_amendment_required = TRUE`, and `future_materialization_pr_required = TRUE` (all four TRUE in the merged CSV row, verified). Step `02_01_03` ROADMAP block at `ROADMAP.md:2274-2523` still declares all six families including `reconstructed_rating` at line 2284, and Step `02_01_99` at `ROADMAP.md:2527-2740` is the stub that defers omit-closure execution — neither block has yet recorded the materialization-scope amendment. The next atomic unit per the non-batching ladder (`.claude/rules/data-analysis-lineage.md`) and Q-chain precedent (PR #238/#239 ROADMAP-stub, PR #252/#253 ROADMAP-stub, PR #254/#255 artifact) is the ROADMAP scope-amendment Layer-1 planning PR. Outcome B is rejected by `future_roadmap_scope_amendment_required = TRUE`; C is rejected because the ROADMAP amendment IS now allowed (all four PR #255 preconditions TRUE); D/E/F are explicitly REJECT by user prompt; G is rejected because no concrete repo defect blocks A (cosmetic INDEX staleness is not a blocker); H is rejected because the 15 verified predicates are mutually consistent.

---

## Scope

This is a **Layer-1 planning PR (Category A)** that authors exactly two planning files and zero repo edits. It plans a **future Layer-2 execution PR** that will be a ROADMAP-only 4-file diff (no artifact, no materialization, no status YAML, no `research_log`, no spec, no CROSS-02-01 audit).

**This Layer-1 PR diff (exactly 2 files):**

- `planning/current_plan.md` — this plan body
- `planning/current_plan.critique.md` — reviewer-adversarial critique log (Round 1)

**The future Layer-2 execution PR diff (exactly 4 files; planned, NOT created in this PR):**

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` — insert one materialization-scope amendment note block (grep token `materialization_scope_amendment_post_pr_255`) adjacent to the existing Step `02_01_03` block, plus a back-reference inside Step `02_01_99`. Original six-family declaration at line 2284 must remain byte-unchanged.
- `planning/INDEX.md` — archive Layer-1 (this PR) row + Layer-2 (next PR) Active line.
- `CHANGELOG.md` — new `[3.81.0]` section + reset `[Unreleased]`.
- `pyproject.toml` — `version = "3.80.0"` → `"3.81.0"`.

**Branch (this Layer-1 PR):** `feat/sc2egset-02-01-03-five-family-scope-amendment`. Justification: branch slug uses the canonical taxonomy `02-01-03` because the amendment is methodologically scoped to Step `02_01_03`'s materialization permission (the ROADMAP amendment block lives in or adjacent to Step `02_01_03`; the Step `02_01_99` back-reference is secondary). The slug does NOT use `02-01-99` because Step `02_01_99` is the omit-closure follow-up stub (already executed by PR #253/#255), not the host of the scope-amendment note. Both Layer-1 and Layer-2 PRs share this branch name (mirroring PR #252 → PR #253 single-branch precedent for the omit-closure stub pair).

**Branch (future Layer-2 PR):** same — `feat/sc2egset-02-01-03-five-family-scope-amendment`.

**Phase/Step ref:** Phase 02 — Feature Engineering / Pipeline Section 02_01 — Pre-Game vs In-Game Boundary / Step `02_01_03` (host of the scope-amendment note) and Step `02_01_99` (back-reference). No new Step number is created. No Step is closed. No status YAML row is added.

**Category:** A — Phase 02 ROADMAP/materialization-scope amendment.

**Expected future version bump:** `3.80.0 → 3.81.0` (minor; feat-family per `.claude/rules/git-workflow.md` because the amendment changes the methodological scope of a future feat-PR's materialization). Justification for not patch-bumping: per Q-chain precedent (PR #239 ROADMAP stub minor-bumped `3.70.1 → 3.71.0`; PR #253 omit-closure stub minor-bumped `3.78.0 → 3.79.0`), ROADMAP scope changes use minor bumps. Justification for not major-bumping: no backward-incompatible spec/contract change.

**Hard stops this Layer-1 PR respects:**

- Only 2 files in this PR's diff: `planning/current_plan.md`, `planning/current_plan.critique.md`.
- NO ROADMAP edit, NO `pyproject.toml` bump, NO `CHANGELOG.md` edit, NO `planning/INDEX.md` archive flip, NO status YAML flip, NO `research_log` edit (dataset or root), NO spec edit, NO cleaning-layer YAML edit, NO source / test / notebook / artifact / sandbox / `data/` touch, NO Step `02_01_04` start, NO Phase 03 start, NO baseline modelling, NO Q6X PR, NO merging, NO marking ready, NO AoE2 edits, NO docs / `.claude` / thesis edits.

**Hard stops the future Layer-2 PR respects:**

- Exactly 4-file diff above; no fifth file.
- NO feature value materialization (no `.parquet` under `reports/artifacts/02_feature_engineering/`).
- NO CROSS-02-01 post-materialization audit (no `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`).
- NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` row flip or addition.
- NO `research_log.md` entry (dataset or root) — the ROADMAP-only amendment follows the precedent of PR #239 / PR #253 ROADMAP-stub PRs that emitted no `research_log` entry.
- NO Step `02_01_03` closure; closure remains deferred until actual five-family materialization + non-vacuous CROSS-02-01 audit lands in a separate later PR.
- NO Step `02_01_04` / Phase 03 / baseline modelling.
- NO Q6X PR / no re-opening of Q5/Q6F/Q6G/Q6H.
- NO five-family feature materialization (a separate downstream PR after this scope-amendment PR merges).

---

## Execution Steps

These are the planned Layer-2 execution tasks (T01 … T06) that the future ROADMAP-only execution PR will run. This Layer-1 planning PR itself does not execute any of them.

### T01 — Pre-execution verification (READ-ONLY; pinned SHA assertions)

- Verify `HEAD = master` and `master HEAD` matches the merge commit of this Layer-1 PR (this PR must merge BEFORE Layer-2 begins).
- Verify `pyproject.toml` version is `3.80.0` (Layer-2 will bump to `3.81.0`).
- Verify PR #255 merge commit `52f9c1082b200019d080cce74e60567452020e18` is on master (the PR #255 omit-closure artifact is the binding evidence anchor for this amendment).
- Verify the existing Step `02_01_03` ROADMAP block at `ROADMAP.md:2274-2523` is byte-unchanged from PR #239 merge (canonical six-family declaration including `reconstructed_rating` at line 2284 still present).
- Verify the existing Step `02_01_99` ROADMAP block at `ROADMAP.md:2527-2740` is byte-unchanged from PR #253 merge (Q6H §17 verbatim authority basis at line 2543-2545 still present).
- Verify the PR #255 omit-closure artifact pair exists at:
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.csv`
  - `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_99_rating_omit_closure.md`
- Read the PR #255 CSV row and confirm `decision_verdict = omit_reconstructed_rating_and_unblock_other_five`, `q6_omission_status = intentionally_omitted_under_branch_iii`, `q6_not_silently_satisfied = TRUE`, `future_roadmap_scope_amendment_required = TRUE`, `future_materialization_pr_required = TRUE`.
- Compute and pin SHA-256 over each of the 14 binding parent artifacts (12 Q-chain parent artifact files from PR #243/#247/#249/#251 + 2 PR #255 omit-closure artifact files) and assert no drift before any write occurs.

### T02 — Author the ROADMAP scope-amendment note (in-memory only; no write yet)

Draft the materialization-scope amendment note block (verbatim content shown in §Future ROADMAP amendment content below). The note must:

- Be inserted **immediately after** the closing ` ``` ` fence of the existing Step `02_01_03` YAML block (at `ROADMAP.md:2523`) AND **before** the `---` separator (at `ROADMAP.md:2525`). This placement is "adjacent to" the Step `02_01_03` block, not "in-place rewrite" — Step `02_01_03`'s YAML body bytes (lines 2276-2523) MUST remain byte-unchanged.
- Use a markdown `##### ` heading (one level deeper than the existing `### Step 02_01_03 ...` heading at line 2274) titled `##### Materialization-scope amendment (post-PR #255)` so the amendment is grep-discoverable AND visually subordinate to its host Step.
- Carry the grep token `materialization_scope_amendment_post_pr_255` (exact string) inside the heading subtitle text AND inside an inline `<!-- amendment_id: materialization_scope_amendment_post_pr_255 -->` HTML comment to guarantee grep visibility.
- Draft a parallel back-reference block inside Step `02_01_99` (insertion point: immediately after `ROADMAP.md:2740`'s closing ` ``` ` fence and before the `---` at `ROADMAP.md:2742`). The Step `02_01_99` back-reference's grep token is also `materialization_scope_amendment_post_pr_255` so a single grep yields both anchors.

### T03 — Bump `pyproject.toml` version

Replace exactly the line `version = "3.80.0"` with `version = "3.81.0"`. No other byte of `pyproject.toml` changes.

### T04 — Update `CHANGELOG.md`

- Replace `[Unreleased]` content (currently empty per the post-PR255 state) with a new `[3.81.0] — YYYY-MM-DD (PR #N: feat/sc2egset-02-01-03-five-family-scope-amendment)` section (date and PR number back-filled at squash-merge time).
- Reset `[Unreleased]` to the empty 4-header skeleton (Added / Changed / Fixed / Removed).
- The `[3.81.0]` section text MUST include:
  - "ROADMAP-only materialization-scope amendment recording PR #255's omit-closure decision against Step 02_01_03 / Step 02_01_99."
  - The exact grep token `materialization_scope_amendment_post_pr_255`.
  - Verbatim recital of the five permitted families: `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`.
  - Verbatim excluded family: `reconstructed_rating`.
  - Verbatim excluded columns: `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`.
  - PR lineage citation: "Parents: PR #243 Q5; PR #247 Q6F; PR #249 Q6G; PR #251 Q6H; PR #253 ROADMAP stub; PR #255 omit-closure artifact."
  - NO-list: "No feature materialization. No CROSS-02-01 audit. No status YAML flip. No research_log entry. No Step 02_01_03 closure. No Step 02_01_04. No Phase 03. No new Q6X PR."

### T05 — Update `planning/INDEX.md`

- Archive **this Layer-1 PR row** (date, category A, description summary, plan path, merged PR number — back-filled at squash merge).
- Replace the Active line with the future Layer-2 row pointing at `feat/sc2egset-02-01-03-five-family-scope-amendment` Layer-2 execution PR.

### T06 — Final write + Layer-2 reviewer-adversarial Round 1

- Write ROADMAP.md, pyproject.toml, CHANGELOG.md, planning/INDEX.md atomically (single commit).
- Dispatch reviewer-adversarial Round 1 over the 4-file diff.
- Round 1 verdict must be APPROVE-WITH-NITS or APPROVE with 0 blockers. Any HOLD with a blocker triggers Round 2.
- If three planning-side rounds exhaust without APPROVE, halt to user per `feedback_adversarial_cap_execution.md`.
- After APPROVE, mark Layer-2 PR ready (Layer-2's PR draft was created at T01-T06 start), wait for user to merge.

### Stop conditions during Layer-2 execution (halt before write) — **nine** explicit clauses

S1. Halt if any byte of Step `02_01_03`'s YAML body at `ROADMAP.md:2276-2523` would change (in-place rewrite is forbidden).
S2. Halt if the exact five family names drift in any position (insertion order, spelling, underscore vs hyphen).
S3. Halt if PR #255 omit-closure artifact SHA-256 differs from the SHA pinned in T01.
S4. Halt if any Q5/Q6F/Q6G/Q6H parent artifact's bytes drift from their PR-merge SHAs.
S5. Halt if `reconstructed_rating` is silently removed from the existing Step `02_01_03` block at line 2284.
S6. Halt if any of the three excluded column names changes spelling.
S7. Halt if the amendment block touches `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, `research_log.md` (dataset or root), spec files, cleaning-layer YAMLs, or any artifact path.
S8. Halt if any `.parquet`, audit JSON, or audit MD appears in the Layer-2 diff.
S9. Halt if Phase 03 or Step `02_01_04` work is introduced.

(NIT-1 resolution: prior plan-text summary mis-stated the halt-clause count as "eight"; the canonical enumeration is **nine** as listed above.)

---

## File Manifest

### This Layer-1 PR (2 files)

| Path | Action | Rationale |
|------|--------|-----------|
| `planning/current_plan.md` | CREATE (overwrite previous PR #255 plan archive) | Authored by parent session after planner-science output approved and reviewer-adversarial APPROVES this plan. |
| `planning/current_plan.critique.md` | CREATE (overwrite previous PR #255 critique archive) | Authored by reviewer-adversarial (Round 1). |

No other repo file touched in this Layer-1 PR.

### Future Layer-2 execution PR (4 files; planned, NOT created in this Layer-1 PR)

| Path | Action | Bytes-affected (estimate) |
|------|--------|---------------------------|
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` | EDIT — insert two amendment note blocks (one after Step 02_01_03's YAML fence at line 2524, one after Step 02_01_99's YAML fence at line 2741). Step 02_01_03's YAML body (lines 2276-2523) and Step 02_01_99's YAML body (lines 2529-2740) BYTE-UNCHANGED. | +60-90 lines of new prose; zero existing bytes mutated. |
| `planning/INDEX.md` | EDIT — archive this Layer-1 row + flip Active to Layer-2. | +2 lines / -1 line. |
| `CHANGELOG.md` | EDIT — new `[3.81.0]` section + `[Unreleased]` reset. | +30-40 lines. |
| `pyproject.toml` | EDIT — version `3.80.0` → `3.81.0`. | 1 line touched. |

No other repo path touched in the future Layer-2 PR.

### Forbidden files (both PRs)

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `reports/research_log.md`
- Any file under `reports/artifacts/02_feature_engineering/` (no new artifact, no PR #255 artifact mutation)
- Any file under `reports/artifacts/02_01_03/` (no CROSS-02-01 audit)
- Any `reports/specs/02_*.md`
- Any `src/rts_predict/**/cleaning/**` YAML
- Any `src/rts_predict/games/sc2/datasets/sc2egset/*.py` source file
- Any `tests/**` file
- Any `sandbox/**` notebook
- Any `data/**` file
- Any AoE2 path (`src/rts_predict/games/aoe2/**`)
- `docs/INDEX.md`, `docs/PHASES.md`, `docs/TAXONOMY.md`, any `docs/**` file
- Any `.claude/**` file
- Any `thesis/**` file

---

## Problem Statement

After PR #255 (merged 2026-05-28 at master `52f9c108`), the SC2EGSet ROADMAP is in an interim methodological state: the PR #255 omit-closure decision artifact records a binding verdict (`omit_reconstructed_rating_and_unblock_other_five`) that authorises five-family materialization, but the ROADMAP itself still describes Step `02_01_03` as a six-family materialization step including `reconstructed_rating`. PR #255's CSV row explicitly records `future_roadmap_scope_amendment_required = TRUE` and `future_materialization_pr_required = TRUE`, encoding the requirement that a ROADMAP amendment PR must merge between PR #255 and any future five-family materialization PR.

This Layer-1 planning PR exists because the non-batching rule (`.claude/rules/data-analysis-lineage.md`) and the Q-chain precedent ladder (PR #252 Layer-1 → PR #253 Layer-2 ROADMAP-stub; PR #254 Layer-1 → PR #255 Layer-2 artifact) require that each substantive ROADMAP edit be preceded by its own Layer-1 planning PR with adversarial review. A direct ROADMAP edit without prior planning would batch Layer-1 + Layer-2 in a single execution and violate the non-batching invariant.

**Methodological tension this plan must resolve:** the original Step `02_01_03` YAML block is the binding declaration of the six families AND the parent record of all Q-chain adjudications (Q1-Q8, Q5, Q6, Q6F, Q6G, Q6H). Mutating it in-place would erase the historical declaration that Q6H Branch (iii)'s "intentionally omitted, not silently satisfied" semantics requires (PR #255 row field `q6_not_silently_satisfied = TRUE`). The amendment must therefore be **additive (insertion-only)**, NOT a rewrite of the original block — the original six-family list remains visible alongside the amendment note recording the narrowing to five families.

**Why this is methodologically defensible:** PR #255's `omit_reconstructed_rating_and_unblock_other_five` is itself a Branch (iii) elevation (thesis_pragmatism = TRUE) — it is not a re-adjudication of Q6H. The ROADMAP amendment records that elevation's downstream consequence (which families are now materializable) without re-opening Q6H. The "intentionally omitted" formula preserves Invariant I9 (a step's conclusions derive from its own artifacts and lower-numbered predecessors): the amendment cites PR #255 verbatim and adds no new evidence claims.

**Why Outcome B (direct five-family materialization PR) is rejected:** PR #255's row explicitly records `future_roadmap_scope_amendment_required = TRUE`. A materialization PR that fired without first amending ROADMAP would violate PR #255's own continue-predicate semantics AND would land Parquet content describing a "five-family table" while the ROADMAP at the same SHA still declares "six families including `reconstructed_rating`" — that contradiction is precisely the GIGO failure mode that `data-analysis-lineage.md` forbids.

**Why Outcome C (blocked-state note) is rejected:** the four PR #255 preconditions are all TRUE in the merged record (`q6_omission_status`, `q6_not_silently_satisfied`, `future_roadmap_scope_amendment_required`, `future_materialization_pr_required`). The ROADMAP amendment is *allowed* now; a blocked-state note would falsely signal that it is not.

**Why Outcome G (hygiene-only) is rejected:** no concrete repo defect blocks A. The `planning/INDEX.md` cosmetic staleness mentioned in the user prompt is not load-bearing on the ROADMAP amendment.

---

## Assumptions & Unknowns

Assumptions are tagged **BINDING** (re-asserted at Layer-2 execution time via SHA-pin or grep token) vs **WORKING** (defensible at plan-time, may be refined at Layer-2 execution time without re-planning).

### Binding assumptions

- **A1 (BINDING)** PR #255 merge commit on master is `52f9c1082b200019d080cce74e60567452020e18`. Layer-2 T01 must verify via `git rev-parse HEAD` and `gh pr view 255`.
- **A2 (BINDING)** The PR #255 CSV row's `decision_verdict` is exactly `omit_reconstructed_rating_and_unblock_other_five`. Layer-2 T01 must verify by reading the CSV.
- **A3 (BINDING)** The PR #255 CSV row records `q6_omission_status = intentionally_omitted_under_branch_iii` AND `q6_not_silently_satisfied = TRUE` AND `future_roadmap_scope_amendment_required = TRUE` AND `future_materialization_pr_required = TRUE`. All four must be TRUE in the verified CSV.
- **A4 (BINDING)** The five permitted family names from Q6H constant `Q6H_FIVE_FAMILY_POST_OMIT_SET` are EXACTLY (canonical order): `focal_player_history`, `opponent_player_history`, `matchup_history_aggregate`, `cross_region_fragmentation_handling`, `in_game_history_aggregate`. No reordering, no rename, no addition.
- **A5 (BINDING)** The excluded family is exactly `reconstructed_rating` (one family, singular).
- **A6 (BINDING)** The excluded column names are exactly `reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff` (three columns).
- **A7 (BINDING)** The grep token recorded in the ROADMAP amendment (both anchor in Step `02_01_03` host block and back-reference in Step `02_01_99`) is exactly `materialization_scope_amendment_post_pr_255`. Layer-2 T01 must `grep -c materialization_scope_amendment_post_pr_255 ROADMAP.md` and expect `0` before write and `>=2` after write.
- **A8 (BINDING)** Step `02_01_03`'s existing YAML body bytes at `ROADMAP.md:2276-2523` are NOT mutated; the amendment is additive (insertion-only). Layer-2 T01 must SHA-256 lines 2276-2523, write the amendment, re-SHA the same line range, and abort if the SHAs differ.
- **A9 (BINDING)** Step `02_01_99`'s existing YAML body bytes at `ROADMAP.md:2529-2740` are NOT mutated; the back-reference is additive. Same SHA-fence procedure as A8.
- **A10 (BINDING)** PR #255 omit-closure CSV path (`02_01_99_rating_omit_closure.csv`) and MD path (`02_01_99_rating_omit_closure.md`) are byte-unchanged across this Layer-2 PR's diff (their SHAs are pinned at Layer-2 T01).
- **A11 (BINDING)** Each of the 12 parent artifact files (6 file SHAs from Step 02_01_03's Q-chain CSVs + 6 MDs at the canonical paths listed in §Future ROADMAP amendment content) is byte-unchanged across this Layer-2 PR's diff. Layer-2 T01 pins each SHA.
- **A12 (BINDING)** Version bump is `3.80.0 → 3.81.0` (minor). Justified by Q-chain precedent (PR #239 ROADMAP stub minor-bumped; PR #253 omit-closure stub minor-bumped). The bump must be exactly one digit in the minor position.
- **A13 (BINDING)** No `research_log.md` entry is created (per ROADMAP-stub precedent PR #239, PR #253). The Layer-2 PR's CHANGELOG row substitutes for a research-log entry at this Layer.
- **A14 (BINDING)** No STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS YAML row addition, mutation, or flip. Step `02_01_03` remains absent from `STEP_STATUS.yaml` (since it is still open); Step `02_01_99` also remains absent (added by a future closure PR, not by this scope-amendment PR).
- **A15 (BINDING)** Step `02_01_03` remains OPEN after this PR merges (no closure). Closure requires (a) actual five-family materialization in a future PR, (b) non-vacuous CROSS-02-01 audit, (c) a separate closure PR (U2.B-style, analogous to PR #237 closing Step 02_01_02).

### Working assumptions

- **W1 (WORKING)** Both PRs (Layer-1 + Layer-2) share branch `feat/sc2egset-02-01-03-five-family-scope-amendment`. Branch slug uses canonical taxonomy `02-01-03` (host of the amendment). If the user prefers a different slug at Layer-2 time, no methodology re-work needed.
- **W2 (WORKING)** The 14 binding parent artifact SHAs (12 Q-chain + 2 PR #255 artifact files) are pinned at Layer-2 T01 via the canonical PR-merge commit identifiers. Working refinement at Layer-2 T01: the exact set of SHAs may be extended by 1-2 additional contextual SHAs (e.g., `head_master_at_layer_1_plan_time = 52f9c108`) without re-planning.
- **W3 (WORKING)** The exact prose of the ROADMAP amendment note (drafted in §Future ROADMAP amendment content as a near-final template) may receive minor stylistic refinements at Layer-2 T02 in response to reviewer-adversarial nits, provided every BINDING clause (A1-A15) is preserved.
- **W4 (WORKING)** The Layer-2 PR's commit count is exactly 1 squash-merge commit. If a Round 2 reviewer-adversarial pass requires a fix-up commit before squash-merge, that is acceptable.
- **W5 (WORKING)** PR-numbering: this Layer-1 PR is expected to be PR #256; the future Layer-2 PR is expected to be PR #257. Final PR numbers are back-filled in `planning/INDEX.md` at squash-merge time.

### Unknowns (resolved at Layer-2 T01)

- **U1** Whether reviewer-adversarial Round 1 verdict will be APPROVE / APPROVE-WITH-NITS / HOLD. Plan accommodates up to 3 planning-side rounds per `feedback_adversarial_cap_execution.md`.
- **U2** Whether any Q-chain parent artifact SHA has drifted since this Layer-1 plan was authored. If T01 verification surfaces drift, halt to user.
- **U3** Whether the user wishes to consolidate Layer-1 + Layer-2 into a single PR (the precedent is two PRs; the user may elect one if hygiene cost outweighs the audit benefit). Default: two PRs.

---

## Literature Context

Three categories of context inform this amendment's methodology:

**1. Project-internal precedent (the dominant authority basis).**

- **PR #239** (`feat/sc2egset-02-01-03-roadmap-stub`, merged 2026-05-24 at `f378f6f4`) established the precedent that a ROADMAP stub PR uses a minor version bump (`3.70.1 → 3.71.0`) and contains no `research_log` entry. This amendment PR mirrors that precedent (minor bump, no research_log entry).
- **PR #253** (`feat/sc2egset-02-01-03b-omit-closure-roadmap-stub`, merged 2026-05-27 at `a9cf552f`) established the precedent for ROADMAP-only stub PRs that defer closure to a downstream artifact PR (PR #255). This amendment PR mirrors PR #253's "ROADMAP-only, no artifact, no audit, no status flip" structure with minor bump.
- **PR #255** (`feat/sc2egset-02-01-99-rating-omit-closure-artifact`, merged 2026-05-28 at `52f9c108`) is the direct evidence anchor: its CSV row records the verdict that this amendment encodes into ROADMAP. The amendment is the downstream "scope amendment" PR that PR #255's `future_roadmap_scope_amendment_required = TRUE` predicts.
- **PR #237** (Step 02_01_02 formal closure, merged 2026-05-24 at `a16d78c2`) established the precedent that a step's closure is a separate PR from its evidence-emission PR (PR #229 → PR #230, PR #236 → PR #237). The current plan respects this: closure of Step `02_01_03` does NOT happen in this scope-amendment PR; it requires future five-family materialization + audit + a U2.B-style closure PR.

**2. Methodology rules (binding governance).**

- **`.claude/rules/data-analysis-lineage.md`** — "Non-batching rule for empirical work" requires sequence step 1 (ROADMAP stub) be its own PR, step 2 (notebook scaffold + one validation module) be a separate PR, etc. This Layer-1 + Layer-2 pairing is sequence step 1 for the "five-family materialization PR" that follows.
- **`.claude/scientific-invariants.md`** — Invariant I9 (a step's conclusions derive only from its own artifacts and all prior steps' artifacts) governs the amendment's evidence base: the amendment cites PR #243, PR #247, PR #249, PR #251, PR #253, PR #255 (all merged and on disk at lower-numbered or sibling positions) and introduces no new evidence claims.
- **`.claude/rules/git-workflow.md`** — minor bump for feat-family PRs; PR body via Write tool to `.github/tmp/pr.txt` then `--body-file`; HEREDOC-free commit messages via `.github/tmp/commit.txt`.

**3. External authority (light citation; the amendment makes no new empirical claim).**

- **Glickman, M.E. (2012).** *Example of the Glicko-2 system.* — cited only via Q-chain parents (PR #247, PR #249, PR #251); this amendment makes no new Glicko-2 claim.
- **Demsar, J. (2006).** *Statistical Comparisons of Classifiers over Multiple Data Sets.* — cited only via `.claude/scientific-invariants.md` Invariant 8 (cross-game comparison protocol); this amendment makes no new statistical claim.

The amendment is therefore a **methodological housekeeping PR**, not a substantive scientific contribution. It records a Branch (iii) elevation's downstream ROADMAP consequence; it does not produce new evidence.

---

## Gate Condition

This Layer-1 PR is approved-to-merge when **all** of the following are TRUE:

1. **2-file diff exactly.** `git diff --name-only master...HEAD` outputs exactly two lines: `planning/current_plan.md` and `planning/current_plan.critique.md`.
2. **planner-science plan present.** `planning/current_plan.md` contains all eight required `##` sections (Scope, Execution Steps, File Manifest, Problem Statement, Assumptions & Unknowns, Literature Context, Gate Condition, Open Questions) per `feedback_plan_required_sections.md`.
3. **Reviewer-adversarial APPROVE recorded.** `planning/current_plan.critique.md` records a Round 1 (or Round 2 / Round 3) verdict of `APPROVE` or `APPROVE-WITH-NITS` with `0` blockers; cap is 3 rounds per `feedback_adversarial_cap_execution.md`.
4. **No edits outside the 2-file diff.** Verified by `git diff --stat master...HEAD` listing only the two planning files.
5. **No PR-state mutation.** Layer-1 PR remains in `draft` state; it is NOT marked `ready` and NOT merged by Layer-1. The user merges manually after reviewer-adversarial APPROVE.

The future Layer-2 PR is approved-to-merge when **all** of the following are TRUE (re-recorded here for completeness; Layer-2 has its own plan and own critique):

- **L1.** 4-file diff exactly (ROADMAP, INDEX, CHANGELOG, pyproject).
- **L2.** ROADMAP grep token count: `grep -c materialization_scope_amendment_post_pr_255 ROADMAP.md` returns `>=2` (one in Step `02_01_03` host, one in Step `02_01_99` back-reference; may be more if implementation chooses additional anchors).
- **L3.** Step `02_01_03` YAML body (lines 2276-2523 at the pre-edit baseline) is byte-unchanged after the amendment (insertion-only).
- **L4.** Step `02_01_99` YAML body (lines 2529-2740 at the pre-edit baseline) is byte-unchanged after the amendment (insertion-only).
- **L5.** Original six-family declaration including `reconstructed_rating` at `ROADMAP.md:2284` is byte-unchanged.
- **L6.** The five permitted family names appear verbatim and in canonical order in the amendment note.
- **L7.** The three excluded column names (`reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`) appear verbatim in the amendment note.
- **L8.** The amendment note explicitly states `reconstructed_rating` is `intentionally_omitted_under_branch_iii` (NOT silently satisfied).
- **L9.** Parent PR citations PR #243, PR #247, PR #249, PR #251, PR #253, PR #255 all present.
- **L10.** Version bumped exactly `3.80.0 → 3.81.0`.
- **L11.** CHANGELOG `[3.81.0]` section exists with required content per T04.
- **L12.** `planning/INDEX.md` archive flip recorded.
- **L13.** NO file under `reports/artifacts/02_feature_engineering/` mutated or created.
- **L14.** NO file under `reports/artifacts/02_01_03/` created (no CROSS-02-01 audit JSON or MD).
- **L15.** NO `STEP_STATUS.yaml` / `PIPELINE_SECTION_STATUS.yaml` / `PHASE_STATUS.yaml` byte changed.
- **L16.** NO `research_log.md` byte changed (dataset or root).
- **L17.** NO `tests/`, `src/rts_predict/games/`, `sandbox/`, `reports/specs/`, `docs/`, `.claude/`, `thesis/`, `data/`, AoE2 path byte changed.
- **L18.** Reviewer-adversarial verdict for Layer-2 PR is APPROVE or APPROVE-WITH-NITS with 0 blockers.

---

## Future ROADMAP amendment content (planned; NOT written in this Layer-1 PR)

(NIT-2 resolution: the verbatim insertion text is inlined below. Layer-2 T02 may make minor stylistic refinements provided every BINDING clause from §Assumptions & Unknowns A1-A15 is preserved.)

**Insertion point 1: after `ROADMAP.md:2523` (Step 02_01_03 closing ` ``` ` fence) and before `---` at `ROADMAP.md:2525`.**

````markdown
##### Materialization-scope amendment (post-PR #255)

<!-- amendment_id: materialization_scope_amendment_post_pr_255 -->

**Status:** materialization_scope_amendment_post_pr_255 — recorded by PR #<TBD-future-Layer-2> (the Layer-2 execution PR materialising this amendment).

**Effect on Step 02_01_03:** the original six-family declaration above (including
`reconstructed_rating`) remains BINDING as the historical record of the closed
Q-chain. The MATERIALIZATION PATH that Step 02_01_03 will execute under is
NARROWED to exactly five families:

1. `focal_player_history`
2. `opponent_player_history`
3. `matchup_history_aggregate`
4. `cross_region_fragmentation_handling`
5. `in_game_history_aggregate`

The 6th family `reconstructed_rating` is EXCLUDED from the materialization path.

**Excluded columns (verbatim):**

- `reconstructed_rating_focal_pre`
- `reconstructed_rating_opp_pre`
- `reconstructed_rating_diff`

**Q6 omission status:** `intentionally_omitted_under_branch_iii`. The exclusion of
`reconstructed_rating` is NOT silent satisfaction of Q6 — it is the explicit
recording of Q6H Branch (iii) elevation per PR #255 row field
`q6_not_silently_satisfied = TRUE`.

**Authority basis (parent artifacts):**

- PR #243 Q5 cross-region adjudication (`02_01_03_history_cross_region_adjudication.{csv,md}`).
- PR #247 Q6F rating-algorithm survey (`02_01_03_q6f_rating_algorithm_survey.{csv,md}`).
- PR #249 Q6G rating-implementation proof (`02_01_03_q6g_rating_implementation_proof.{csv,md}`).
- PR #251 Q6H rating-path decision (`02_01_03_q6h_rating_path_decision.{csv,md}`).
- PR #253 ROADMAP stub for Step 02_01_99.
- PR #255 omit-closure decision artifact (`02_01_99_rating_omit_closure.{csv,md}`)
  with `decision_verdict = omit_reconstructed_rating_and_unblock_other_five`.

**Scope of this amendment:**

- NO feature value materialization. No `.parquet` is produced by this amendment PR.
- NO CROSS-02-01 post-materialization audit. No
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}` is created.
- NO `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, or `PHASE_STATUS.yaml`
  row addition or mutation.
- NO `research_log.md` entry (dataset or root).
- NO Step 02_01_04 start.
- NO Phase 03 start.
- NO new Q6X PR (Q6H is terminal per PR #251).

**Continue-predicate (updated):** Feature materialization for Step 02_01_03 may
proceed in a future PR only when ALL of the following hold:

1. The materialized columns cover exactly the five permitted families listed
   above (no more, no fewer).
2. No column with name matching `reconstructed_rating_focal_pre`,
   `reconstructed_rating_opp_pre`, or `reconstructed_rating_diff` (or any other
   `reconstructed_rating_*` token) is materialized.
3. The CROSS-02-01 post-materialization audit is NON-vacuous (`features_audited`
   covers exactly the five families' materialized columns) and returns
   `verdict = PASS`.
4. All Q5/Q6F/Q6G/Q6H parent artifact bytes are unchanged (no Q-chain
   re-adjudication).
5. PR #255 omit-closure artifact bytes are unchanged.

**Halt-predicate (updated):** Halt before any future PR proceeds if:

- any `reconstructed_rating_*` column is generated;
- the exact five-family set drifts (renamed, reordered, added to, dropped from);
- the PR #255 omit-closure artifact bytes drift from the SHA pinned at this PR's
  merge time;
- any Q5 (PR #243), Q6F (PR #247), Q6G (PR #249), or Q6H (PR #251) parent
  artifact's bytes drift;
- any target-match outcome, future-match outcome, or Phase 03 split leakage is
  introduced into any feature column;
- any `STEP_STATUS.yaml`, `PIPELINE_SECTION_STATUS.yaml`, `PHASE_STATUS.yaml`, or
  `research_log.md` is edited in this scope-amendment PR;
- any feature `.parquet`, CROSS-02-01 audit JSON/MD, or
  `reports/artifacts/02_01_03/` file is produced in this scope-amendment PR.

**Step 02_01_03 closure status:** OPEN. This amendment does NOT close Step
02_01_03. Closure requires (a) actual five-family materialization (a separate
future PR), (b) a non-vacuous CROSS-02-01 post-materialization audit on the five
families' columns, and (c) a separate closure PR analogous to PR #237 for Step
02_01_02. Until all three conditions are met, Step 02_01_03 remains absent from
`STEP_STATUS.yaml` (status row is added by the closure PR, not by this
amendment).

**Forward path (informational, not a commitment):** the next planned PR after
this amendment merges is the five-family materialization PR (planned branch
`feat/sc2egset-02-01-03-five-family-materialization`), followed by the formal
Step 02_01_03 closure PR.
````

**Insertion point 2: after `ROADMAP.md:2740` (Step 02_01_99 closing ` ``` ` fence) and before `---` at `ROADMAP.md:2742`.**

````markdown
##### Materialization-scope amendment back-reference (post-PR #255)

<!-- amendment_id: materialization_scope_amendment_post_pr_255 (back-reference) -->

PR #255 (omit-closure decision artifact, merged 2026-05-28 at
`52f9c1082b200019d080cce74e60567452020e18`) satisfied the four preconditions
declared in this Step 02_01_99's `question` field. The downstream
`materialization_scope_amendment_post_pr_255` note is recorded against Step
02_01_03 above; see the host amendment block for the five permitted families,
the excluded family `reconstructed_rating`, the three excluded columns, and the
updated continue-predicate / halt-predicate. Step 02_01_99 itself remains a
ROADMAP-only stub; no new artifact, no new YAML row, no status flip is
introduced by the amendment.
````

This verbatim text satisfies all 12 required content sub-clauses from the user prompt (verbatim mapping):

1. **Preserves Step 02_01_03 history; no silent deletion.** Insertion-only at `ROADMAP.md:2524` placement; Step 02_01_03 YAML body (lines 2276-2523) byte-unchanged.
2. **Grep-visible amendment with exact token `materialization_scope_amendment_post_pr_255`.** Token appears in the `##### Materialization-scope amendment (post-PR #255)` heading subtitle, in the `<!-- amendment_id: ... -->` HTML comment, and in the prose. Lives inside Step 02_01_03 (host) AND inside Step 02_01_99 (back-reference).
3. **Five-family materialization path stated.** Five families listed verbatim in canonical Q6H order.
4. **`reconstructed_rating` excluded due to PR #255 verdict.** Cited.
5. **Intentionally omitted, NOT silently satisfied.** Phrasing `intentionally_omitted_under_branch_iii` AND the explicit "is NOT silent satisfaction of Q6" clause.
6. **Three excluded column names verbatim.** Listed as a bullet list.
7. **Parent PRs cited.** PR #243 Q5, PR #247 Q6F, PR #249 Q6G, PR #251 Q6H, PR #253 stub, PR #255 omit-closure.
8. **No feature values materialized in the ROADMAP-only amendment.** Explicit clause in `Scope of this amendment`.
9. **No feature artifact, CROSS-02-01 audit, status YAML, research_log, Step 02_01_04, or Phase 03 work.** Explicit `Scope of this amendment` clause covers all six.
10. **Updated `continue_predicate`.** New continue-predicate states materialization may proceed only for the five families; no `reconstructed_rating` columns; CROSS-02-01 audit must be non-vacuous for the five.
11. **Halt predicates / falsifiers.** Seven halt clauses cover all six required halt predicates from the user prompt: (i) halt if any `reconstructed_rating_*` column generated; (ii) halt if exact five-family set drifts; (iii) halt if PR #255 artifact drifts; (iv) halt if Q5/Q6F/Q6G/Q6H parent decisions drift; (v) halt if target-match outcome / future-match / Phase 03 split leakage introduced; (vi) halt if status YAML or research_log edited; (vii) halt if materialization artifact or CROSS-02-01 audit appears in the ROADMAP-only PR.
12. **Step 02_01_03 remains open until materialization + non-vacuous audit + closure occur.** Explicit `Step 02_01_03 closure status: OPEN` clause.

---

## Open Questions

These are unresolved at Layer-1 planning time. Layer-2 execution may resolve them or defer.

- **OQ1** Should the amendment block be inserted INSIDE the existing Step 02_01_03 YAML block (as additional YAML fields, e.g., `materialization_scope_amendment:` mapping) or OUTSIDE the YAML block (as adjacent markdown prose)? **Recommendation:** OUTSIDE as prose (current plan). Rationale: (a) preserves the byte-unchanged invariant on the YAML body, (b) avoids mutating the `step_template.yaml`-conformant schema of the YAML block, (c) matches the `### Step XX_YY_ZZ` heading-then-fenced-YAML pattern used by all other ROADMAP entries, (d) keeps the amendment grep-discoverable via `##### ` markdown headings rather than embedded inside a YAML body. **Resolution:** prose insertion (already adopted in the §Future ROADMAP amendment content draft). Layer-2 may not change this without re-plan.

- **OQ2** Should the back-reference block in Step 02_01_99 be omitted (single-anchor amendment in Step 02_01_03 only) or kept (dual-anchor)? **Recommendation:** dual-anchor (current plan). Rationale: (a) PR #255 lives in the 02_01_99 lineage, so a reader landing at Step 02_01_99 needs forward visibility to the scope amendment, (b) grep `materialization_scope_amendment_post_pr_255` then yields both anchors, (c) the back-reference is a single 8-10 line prose block, low marginal byte cost. **Resolution:** dual-anchor (adopted).

- **OQ3** Should the future five-family materialization PR's branch slug be predicted in the amendment text? The §Future ROADMAP amendment content draft mentions `feat/sc2egset-02-01-03-five-family-materialization` informationally. **Recommendation:** keep the slug prediction as informational only (not binding). Rationale: branch slugs may shift; the amendment's binding content is the five-family permitted set, not the future PR slug. **Resolution:** keep informational.

- **OQ4** Whether to also reference the methodology of Q6H Branch (iii) precondition verification (PR #255 §6 thesis-pragmatism elevation, Jaccard 0.1708 vs Q6H §15) in the amendment. **Recommendation:** do NOT — the amendment defers to PR #255 by citation, not by re-reciting PR #255's precondition evidence. Re-citing would risk drift between the amendment text and PR #255's own MD §6. **Resolution:** cite PR #255 by name only; do not paraphrase its content.

- **OQ5** Whether the future Layer-2 reviewer-adversarial pass should be invoked at Round 1 with a "compressed Layer-2 scope" instruction (because the 4-file diff is mechanically narrow) or with a "full critique" instruction. **Recommendation:** full critique — the ROADMAP amendment is methodologically load-bearing despite being mechanically small; adversarial defensibility matters more than diff size. **Resolution:** full critique at Round 1.

- **OQ6** Whether `pyproject.toml` should bump to `3.81.0` (minor; planned) or `3.80.1` (patch). **Recommendation:** minor `3.81.0` per Q-chain precedent (PR #239 minor; PR #253 minor for ROADMAP-only stubs). Rationale: the amendment changes the methodological scope of a future feat-PR's materialization — this is a feat-family change, not a chore/fix-family change. **Resolution:** minor bump.

- **OQ7** Whether the Layer-2 PR is created as `--draft` (default) or `--ready`. **Recommendation:** `--draft`, mirroring the PR #254 / PR #255 pair pattern (Layer-1 draft, Layer-2 draft until reviewer-adversarial APPROVES). The user marks ready manually post-APPROVE. **Resolution:** `--draft`.

---

## Reviewer-adversarial dispatch instructions for THIS Layer-1 PR

(These are the instructions the parent session uses to dispatch reviewer-adversarial after this plan is approved by the user. They are part of the plan because reviewer-adversarial reads the plan, not the dispatch prompt.)

**Agent:** reviewer-adversarial (Opus).
**Inputs to review (READ-ONLY):**

- `planning/current_plan.md` (this file).
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` at master `52f9c108` (the pre-edit baseline).
- The 14 binding parent artifacts (12 from PR #243/#247/#249/#251 + 2 from PR #255).
- `.claude/scientific-invariants.md`, `.claude/rules/data-analysis-lineage.md`, `.claude/rules/git-workflow.md`.

**Adversarial questions reviewer-adversarial must ask (the 22 axes):**

Planner-charter axes (1-15):

1. Is Outcome A the correct next atomic unit after PR #255?
2. Is the 2-file Layer-1 / 4-file Layer-2 split justified vs. a single PR?
3. Is the branch slug `feat/sc2egset-02-01-03-five-family-scope-amendment` canonical?
4. Are all five families enumerated correctly and in canonical order?
5. Does the amendment preserve `q6_not_silently_satisfied = TRUE` semantics?
6. Are all parent PR citations (#243, #247, #249, #251, #253, #255) present and accurate?
7. Does the amendment prevent silent five-family materialization authorisation?
8. Are Q5/Q6F/Q6G/Q6H BINDING verdicts preserved (no re-adjudication risk)?
9. Is materialization barred in BOTH this Layer-1 PR and the future Layer-2 PR?
10. Is the no-Q6X-re-opening invariant preserved?
11. Are Phase 03 / Step 02_01_04 explicitly barred?
12. Is version bump 3.80.0 → 3.81.0 SemVer-correct and Q-chain-consistent?
13. Is the grep token `materialization_scope_amendment_post_pr_255` unique and grep-discoverable?
14. Is the insertion-only invariant (no Step 02_01_03 / 02_01_99 byte mutation) testable?
15. Is the non-batching rule satisfied (Layer-1 separate from Layer-2; this PR does not author Layer-2's diff)?

User-prompt axes (A1-A7):

- **A1.** Is the future ROADMAP amendment content complete on all 12 required sub-clauses?
- **A2.** Is the grep token exact (`materialization_scope_amendment_post_pr_255`) — no typo, no abbreviation, no plural?
- **A3.** Are the three excluded column names verbatim (`reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`, `reconstructed_rating_diff`)?
- **A4.** Is the five-family permitted set verbatim and in Q6H canonical order?
- **A5.** Are all five halt predicates (i)-(vi) and additional (vii) present in the future amendment text?
- **A6.** Is the future continue-predicate updated to require five families + no `reconstructed_rating` + non-vacuous audit?
- **A7.** Does Step 02_01_03 remain open with closure deferred to a future PR after materialization + audit?

If any axis fails, reviewer-adversarial returns HOLD with a blocker. Up to 3 planning-side rounds permitted per `feedback_adversarial_cap_execution.md`. After 3 rounds without APPROVE, escalate to user.

---

## Critique gate (Category A)

Per `.claude/agents/planner-science.md` charter: **for Category A plans, adversarial critique is required before execution begins. Do NOT produce the critique yourself — reviewer-adversarial handles it.** The parent session dispatched reviewer-adversarial against this plan after the user approved it and BEFORE materializing this Layer-1 PR. The reviewer-adversarial critique log lives at `planning/current_plan.critique.md` and is part of this Layer-1 PR's 2-file diff.

---

**End of plan.** All eight required `##` sections present (Scope, Execution Steps, File Manifest, Problem Statement, Assumptions & Unknowns, Literature Context, Gate Condition, Open Questions). All 12 required future-ROADMAP-amendment content sub-clauses present in §Future ROADMAP amendment content (verbatim inlined per NIT-2 resolution). All 4 future-execution files listed (ROADMAP, INDEX, CHANGELOG, pyproject). All nine halt clauses listed explicitly (per NIT-1 resolution). Future version bump `3.80.0 → 3.81.0` justified. Branch `feat/sc2egset-02-01-03-five-family-scope-amendment` justified. Exact grep token `materialization_scope_amendment_post_pr_255` declared. Five family names verbatim in canonical order. Three excluded column names verbatim. PR #255 omit-closure decision encoded without re-adjudicating Q6H.
