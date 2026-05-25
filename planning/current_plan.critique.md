---
reviewer_role: reviewer-adversarial
reviewer_model: claude-opus-4-7[1m]
reviewer_date: 2026-05-25
plan_base_ref: 445bae0197fa75b613443f8eafef114ff2bb6939
plan_file: planning/current_plan.md
chosen_outcome: A
branch: feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication
planning_pr_number: 244
planning_pr_url: https://github.com/tomaszpionka/rts-outcome-prediction/pull/244
planning_pr_state: draft
verdict: APPROVE-WITH-NITS
blockers: 0
nits: 10
round: 1
round_cap: 3
future_layer2_pr_number: TBD
---

# Q6 plan adversarial review

## Metadata

- Plan: `planning/current_plan.md`
- Plan author: `@planner-science` (Opus 4.7, 1M context)
- Plan timestamp: 2026-05-25
- Reviewer: `@reviewer-adversarial`
- Review timestamp: 2026-05-25
- Round: 1 of 3 (adversarial cap; per `feedback_adversarial_cap_execution.md`)
- Chosen outcome under review: A — Q6-only rating-reconstruction successor adjudication planning PR
- Branch: `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication`
- Layer: Layer-1 (planning-only; 2-file diff)
- Predecessors verified: PR #242 (Q1-Q4, Q7, Q8 ratified; Q5+Q6 deferred), PR #243 (Q5 resolved at `narrow_with_evidence` with `sensitivity_indicator_co_registration`)
- Remaining deferred blocker after Q6 PR merge target: none on Step 02_01_03 (Q6 is the unique outstanding gate)

## Verdict: APPROVE-WITH-NITS

The plan is materializable as a 2-file Layer-1 planning-only PR. The chosen outcome (A — Q6-only successor adjudication) is correctly motivated and uniquely justified. No findings rise to BLOCKER severity. Several NITs surface real planning gaps that have been inlined into the plan's `## Adversarial-Review Adjustments (Round 1)` section as binding (N-1 through N-4) or soft (N-5 through N-10) Layer-2 executor guidance.

## Blockers (must fix before this planning-only PR can be materialized)

None.

Verification trail:

- The 8 required `##` sections are present (verified at lines 9, 65, 137, 296, 335, 738, 843, 874 of the planner-science raw output in `/tmp/q6_plan_raw.txt`; mirrored in `planning/current_plan.md`).
- Branch name `feat/sc2egset-02-01-03-history-rating-reconstruction-adjudication` mirrors the PR #243 successor pattern (`feat/sc2egset-02-01-03-history-cross-region-adjudication`).
- Version-bump policy (planning PR does not bump; Layer-2 bumps `3.74.0 → 3.75.0`) matches the PR #240 / PR #243 planning-only precedent.
- All 4 parent-PR SHAs match the orchestrator-verified ground state:
  - PR #242 CSV `f2a169ecd9182e1aa4e3a2a73fa33d045c66a7913d11a59982c3122b26faf53b` ✓
  - PR #242 MD  `fdaa7d6dec233cc4f1d0b2bc87aa0ba711e49bea0297d0efd3c7ff96800f237d` ✓
  - PR #243 CSV `29d395229139c7df7b6143e96323983c691c572111b74b68570946f9cafb3424` ✓
  - PR #243 MD  `026deda326b5aa65381bb3bcdf111ae17a0cbde0cf36a73dc7dfa19b0f0f5719` ✓
- OQ1-OQ6 are real ambiguities (not strawmen); each provisional answer is honestly hedged.
- 43 falsifier helpers cover all orchestrator-required minima (parent SHAs × 4, candidate completeness, no NOT_FOUND, no materialized output, no status drift, no research_log drift, no ROADMAP drift, no Q5 re-adjudication, candidate-policy-table completeness, forward-only for non-omit, target-match-outcome rejection, future-match-leakage rejection, global-batch-fit rejection, cold-start represented, tie-handling represented, MMR missingness summary present, materialization-permission blocked unless binding, byte-determinism, no Phase 03 / baseline creep).

## Nits (recommended; do not block planning PR; inlined into `planning/current_plan.md` as binding or soft guidance)

### N-1 — Q6 candidate set is incomplete vs the dataset's own research_log

**Severity:** binding for Layer-2 executor.

**Evidence:** Plan Assumption 11 (`Q6_RATING_POLICY_CANDIDATES` lines 219-226 in the raw planner output) closes the candidate set at 6: omit / rolling-baseline / Elo / Glicko-or-Glicko-2 / TrueSkill / deferred-with-survey. But:

- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` line 733-734: "rating-system backtesting (Elo, Glicko, Glicko-2, **TrueSkill, Aligulac-style BTL**)".
- `research_log.md` line 961: "Cross-dataset-harmonized substrate for Phase 02+ rating-system backtesting (Elo, Glicko, Glicko-2, TrueSkill, **Aligulac race-conditioned, Bradley-Terry, Neural BTL**)".

Aligulac-style BTL and Bradley-Terry / Neural BTL are listed as the substrate's *intended* backtesting universe but are silently dropped from the candidate set. That asymmetry is a foreseeable examiner question.

**Fix (inlined as binding executor guidance in plan `## Adversarial-Review Adjustments`):** Either extend `Q6_RATING_POLICY_CANDIDATES` to include `aligulac_race_conditioned_btl` and `bradley_terry_or_neural_btl` (bringing the row count to ≥10) OR author an explicit rejection paragraph in MD §5 and the per-candidate row notes that names these methods and justifies their omission for sc2egset's 1v1-decisive PHA scope.

### N-2 — Missing candidate: "raw MMR-where-present + is_mmr_missing" hybrid

**Severity:** binding for Layer-2 executor.

**Evidence:** The plan rejects MMR-as-feature via the §6.2 row 4 binding ("MMR is structurally absent for 83.95% of rows"), but the *partial-MMR* candidate ("use MMR for the 16.05% rated subset + cold-start the rest") is not the same as the spec rejection of *raw MMR as the sole skill feature*. The orchestrator brief probe 4(a) explicitly named this candidate.

**Fix (inlined):** Add a Q6 row (either a new `Q6G_raw_mmr_where_present_hybrid` candidate row, OR an explicit rejection paragraph) enumerating this candidate. Acceptable rejection rationale: "Violates Invariant I5 symmetric-treatment because rated-vs-unrated rows would be fed asymmetric features; the rated/unrated partition is correlated with skill (tournament players over-represented in the rated 16.05%); the partition-as-feature would leak corpus structure into the model."

### N-3 — Probe 5 reads the wrong player key

**Severity:** binding for Layer-2 executor.

**Evidence:** `PROBE_PHA_PER_PLAYER_HISTORY_DEPTH_SQL` (T02 Probe 5, plan lines 382-398) groups by `toon_id`, but PR #243's adjudication established the canonical player-grouping key as `player_id_worldwide` (the full `R-S2-G-P` toon with cross-region co-registration per Invariant I2 branch iii). Using `toon_id` under-counts per-player history depth for cross-region players because their parallel-region trajectories appear as separate keys. This breaks the cold-start prevalence evidence claim.

**Fix (inlined):** Replace `GROUP BY toon_id` with `GROUP BY player_id_worldwide` (or the canonical PHA column name resolved at Layer-2 plan time) and add an inline comment explicitly noting the choice and citing PR #243's player_id_worldwide binding.

### N-4 — Probes 1 & 2 `LIMIT 1000` without `ORDER BY` is non-deterministic

**Severity:** binding for Layer-2 executor.

**Evidence:** `PROBE_PHA_RESULT_DISTRIBUTION_SQL` (plan lines 348-355) and `PROBE_PHA_DETAILS_TIMEUTC_TRY_CAST_NULL_RATE_SQL` (lines 357-363) use `LIMIT 1000` with no `ORDER BY`. DuckDB's row selection under unordered LIMIT is implementation-defined and may differ across machines / pages / parallelism. This breaks the T06 / Gate Condition byte-determinism guarantee.

**Fix (inlined):** Either (a) add a deterministic `ORDER BY` (e.g., `ORDER BY replay_id`) before LIMIT, or (b) drop the LIMIT and probe the full 44,817-row table. (b) is preferred unless the executor finds a probe whose semantics genuinely require sampling.

### N-5 — Surface that Q6 probes are single-table by design

**Severity:** soft.

**Rationale:** PR #243 surfaced a LEFT-JOIN-NULL trap (Dispatch 3 OPTION (a) fix). The Q6 probes do not use LEFT JOIN (single-table COUNT FILTER on PHA + MFC), so the trap is structurally inapplicable, but the plan should record one sentence in T02 explicitly noting this — this preempts the round-2 question.

### N-6 — Schema delta vs PR #243's 30-column template is not justified

**Severity:** soft.

**Evidence:** Plan declares 36 columns (line 818); PR #243's template CSV is 30 columns (verified via header inspection of `02_01_03_history_cross_region_adjudication.csv`). The 6+ new columns are Q6-specific (rating-discipline-specific fields PR #243's cross-region adjudication did not need) and reasonable, but the plan should briefly justify each delta vs the PR #243 template.

### N-7 — Plan section ordering departs from PR #243's template

**Severity:** soft.

**Evidence:** PR #243's `current_plan.md` orders sections (verified): Scope → Problem Statement → Assumptions → Literature Context → Execution Steps → File Manifest → Gate Condition → Open Questions → **Out of scope** → **Critique instruction** → **Self-check against R4 B4-only mechanical fix**. The Q6 planner-science raw output omitted the trailing 3 sections. The pre-commit hook only requires the first 8, so this is not a blocker.

**Fix (inlined):** `## Out of scope` section added to `planning/current_plan.md` per this nit. `## Critique instruction` and `## Self-check` are PR #243-specific and not added.

### N-8 — N-X3 strengthened-gate wording is referenced but not fully reproduced

**Severity:** soft.

**Evidence:** Plan references "the N-X3 strengthened gate from PR #242" (line 174) and enumerates its 4 requirements ("≥1 repo path + ≥1 citation + forward-only wording + cold-start/missingness wording"). Confirmed verbatim consistent with the PR #242 §13 / Q6 row rationale at `02_01_03_history_source_anchor_coldstart_adjudication.md:125`.

**Fix (inlined):** Pin the exact N-X3 quote from PR #242 into Assumption 18 so the Q6 executor cannot drift the gate language.

### N-9 — Helper 17 POST-GAME token list is unstated

**Severity:** soft.

**Evidence:** `_check_no_post_game_token_in_scoped_fields` (line 454) is declared but the actual forbidden token list is not enumerated. PR #242 used a specific universal scanner; the Q6 executor must reuse the *exact same* token set (no new tokens added; no tokens silently dropped).

**Fix (inlined):** Explicit instruction: helper 17 imports the existing `POST_GAME_TOKEN_SET` from `adjudicate_history_enriched_pre_game_source_layer.py` rather than redefining it.

### N-10 — Algorithm-survey-vs-Q6-collapse adequately handled but worth strengthening

**Severity:** soft.

**Evidence:** I checked this carefully (orchestrator probe 3). The plan handles it via candidate Q6F (`deferred_with_algorithm_survey_required`) which is itself a legitimate verdict. The plan does NOT pre-commit a winner (Assumption 12 line 226, OQ2 line 881), so the Q6 executor's substantive T05 can honestly conclude "the comparative evidence does not exist; punt to algorithm survey." This is the correct planning posture.

**Fix (inlined):** Add explicit wording to MD §5 (Per-Candidate Decision Table) that selecting `Q6F_deferred_with_algorithm_survey` is a legitimate Q6 verdict, not a planning failure. This prevents the Layer-2 executor from feeling pressured to bind a winner under thin evidence.

## Non-issues considered and dismissed

- **Materialization gate framing.** The plan's framing ("MATERIALIZATION REMAINS BLOCKED" lines 122, 159) is verbatim-consistent with `02_01_03_history_source_anchor_coldstart_adjudication.md:235` §13 and PR #243's §10/§13.
- **Selecting `omit` constitutes an upgrade (OQ1).** The PR #242 §13 wording does not enumerate `recommendation_only` for the omit case, but the plan's OQ1 surfaces this ambiguity for user/reviewer decision. Correctly flagged, not unilaterally resolved.
- **External-citation policy.** OQ3 honestly hedges; the PR #242 Q6 row already lists the 4 citations as `evidence_paths` (verified at `02_01_03_history_source_anchor_coldstart_adjudication.md:133-136`). In-repo-sufficient is defensible.
- **Q6 vs Phase 03 boundary.** Assumption 17 + Open Question discipline + the explicit Phase 03 forbidden-file list at line 773 are sufficient. G-CS-4 (rating cold-start) is correctly distinguished from G-CS-6 (training-fold-fit, deferred).
- **Forbidden-file list completeness.** Lines 764-775 cover Parquet, leakage audits, all 3 status YAMLs, both research_logs, ROADMAP, specs, cleaning-layer YAMLs, thesis/docs/.claude/data, aoe2, sandbox/jupytext.toml. Comprehensive.
- **Decision-routing (Sonnet vs Opus).** T05 → Opus REQUIRED (line 548); T04 → Opus (entrypoint orchestration, line 505); T01-T03, T06-T08 → Sonnet. Consistent with data-analysis-lineage agent-routing discipline.
- **MMR-missingness over-fitting.** The plan correctly uses the 83.95% figure as motivating evidence for the family choice, not as a winner-selector (lines 158, 302-303, Assumption 9). T05 honest reasoning treats each candidate on its merits, not on missingness density alone.
- **No invented numbers.** All quantitative claims (44,418 MFC, 44,817 PHA, 22,209 distinct replay_id, 83.95% / 83.65% MMR-missing, 7128 rated rows, 37,290 MMR-zero rows) trace to research_log line citations (lines 106, 1135) or PR #242 §10.
- **Critique placeholder format.** Lines 904-932 of the raw planner output follow the PR #243 stub pattern (this file replaces it with the full reviewer transcript).

## Summary

| Dimension | Verdict |
|---|---|
| Outcome A defensibility | yes — uniquely motivated; B/C/D/E/F rejections cite verifiable evidence |
| Candidate-set completeness | conditional — 6 candidates are well-formed but N-1 + N-2 surface real omissions vs the dataset's research_log methods list |
| Schema sufficiency | conditional — 36 columns are sufficient but N-6 asks for explicit delta-justification vs PR #243's 30-column template |
| Falsifier-set completeness | yes — 43 helpers cover all orchestrator-required minima |
| Materialization-gate framing | correct — verbatim consistent with PR #242 §13 + PR #243 §10/§13 |
| Total blockers | 0 |
| Total nits | 10 (N-1 through N-4 binding; N-5 through N-10 soft; all 10 inlined into plan) |
| Recommended next step | materialize draft PR; do NOT begin Layer-2 execution until user has reviewed |

Round 1 of 3 adversarial cap consumed.

## Layer-2 dispatch reminder for the parent session

After this planning-only PR is reviewed and merged, the next session's executor:

- Reads `planning/current_plan.md` (this Q6 plan) directly.
- Honours the 4 binding nits N-1 through N-4 as Layer-2 execution gates (the Layer-2 PR cannot pass its own final adversarial gate without them addressed).
- Treats N-5 through N-10 as soft guidance to incorporate if the schema/probe/MD draft would otherwise mismatch.
- Routes T05 (substantive Q6 content) to Opus; T01-T03 / T06-T08 may use Sonnet; T04 / T09 require Opus oversight.
- Dispatches `@reviewer-adversarial` (NOT `@reviewer-deep`) as the Layer-2 final gate; the adversarial 3-round cap resets for Layer-2 (per `feedback_adversarial_cap_execution.md` symmetric application).
- Does NOT begin Step 02_01_04 or Phase 03 work.
