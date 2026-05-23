---
plan_ref: planning/current_plan.md
created: 2026-05-22
category: A
base_ref: 3cda752813659490e4992df78ecb10a72b8f010c
reviewer_model: reviewer-adversarial (Opus, Category A pre-execution methodology gate)
verdict: APPROVE-WITH-NITS
blockers: 0
authorizes_layer1_materialization: true
chat_second_pass_required_before_materialization: true
---

# Critique — SC2EGSet Step 02_01_02 scaffold + one validation module (Category A pre-execution gate)

> Produced by `@reviewer-adversarial` as the Category A pre-execution methodology
> gate (Phase 02, methodology-sensitive, designs the first non-vacuous
> leakage-sensitive path). Every load-bearing claim was independently verified
> against the on-disk repo; no claim was taken on trust.

## Verdict

**APPROVE-WITH-NITS — zero blockers; no required `current_plan.md` edit.**
Authorizes materializing the draft planning PR this turn. The two nits are
Layer-2 / future-PR instructions (folded into plan §4.1/§4.3/§7), not NOW edits.

## Non-blocking nits (Layer-2 / future-PR instructions)

1. **Risk-register path.** The `RISK-NN` identifiers (RISK-24 focal/opponent
   slot asymmetry; RISK-26 SC2 Random race must not be conflated with eventual
   race; RISK-20 cross-region fragmentation) live in
   `thesis/pass2_evidence/methodology_risk_register.md`, NOT the dataset-level
   `risk_register_sc2egset.csv` (which uses the `SC-R01..` scheme). The future
   scaffold notebook must cite the methodology-register path so a reader does
   not grep the dataset register, find `SC-R`, and conclude the falsifier is
   undefined. Verified: RISK-24 @ methodology_risk_register.md:445; RISK-26
   @ line 479; RISK-20 @ line 375. No NOW edit required.
2. **Anchor-column divergence is the SAME view-vs-raw decision.** The registry
   CSV records `temporal_anchor=details_timeUTC` (raw column); CROSS-02-02 §6.1
   / CROSS-02-00 §5.1 name the harmonized-view anchor `started_at`. This is the
   same view-vs-raw divergence as the source-table divergence (§4.1). The
   future second-pass must treat anchor-column-name and source-table-layer as
   ONE coupled decision, not two. (Plan §4.1 now records this.) No NOW edit.

## 13-check results (all PASS)

1. **Outcome A correctly chosen — PASS.** data-analysis-lineage.md:43-53 mandates
   the 9-step non-batching sequence; step 1 = ROADMAP stub (PR #232), step 2 =
   "notebook scaffold + one validation module," steps 7-8 = artifacts/status only
   after all validation modules pass. Outcome B forbidden by the ROADMAP halt
   predicate (ROADMAP.md:2250-2263, incl. "halt if the future notebook scaffold
   attempts to batch ROADMAP + notebook + artifact + next step"). CROSS-02-02
   §12.1 line 539 verbatim: "a single `is_mmr_missing` flag for sc2egset … No
   feature table is produced." Confirmed exactly.
2. **Non-batching obeyed — PASS.** Layer-2 manifest = scaffold .py + .ipynb +
   validator + test + planning/INDEX + 2 planning files + CHANGELOG + pyproject.
   No Parquet/artifact/status/research_log/ROADMAP. Exactly sequence step 2.
3. **No feature value materialized — PASS.** `materialized_output_paths` hard-coded
   to `()`; validator writes nothing; notebook persists nothing (FORBIDDEN
   CREATE/INSERT/COPY/to_parquet). Gate asserts the json still has
   `features_audited==[]` (verified on disk).
4. **No artifact/status/research_log mutation — PASS.** Manifest excludes all;
   F-mutation falsifier + gate require diff == 9-file manifest exactly. ROADMAP
   itself confirms research_log NOT required for this lineage step.
5. **Phase 03 / 02_01_03 / 02_02+ untouched — PASS.** Out-of-scope §10 + F-phase03;
   ROADMAP.md:2240-2249 gates 02_01_03 behind a non-vacuous post-materialization
   audit this scaffold does not run.
6. **is_mmr_missing_flag framing safe — PASS.** CROSS-02-02 §6.1 line 228 verbatim:
   "Use the missingness flag, not the MMR scalar. MMR is structurally absent for
   83.95% of rows … the raw scalar is not a defensible naive skill feature."
   Validator `_check_is_mmr_missing_is_flag_not_skill` + `FORBIDDEN_SKILL_TOKENS`
   enforces flag-not-scalar. CROSS-02-03 §6.1 line 240 independently lists it as
   an allowed pre-game flag. Registry CSV row 6 confirms classification.
7. **5-family tranche correct, free of history/in-game — PASS.** Registry CSV rows
   2-6 are exactly the 5 named families (pre_game/allowed/none/G-CS-1/
   snapshot_at_match_start); rows 7-12 (6 history_enriched, history_time<target,
   G-CS-2..5, rolling/h2h/rating modes) and rows 13-23 (11 in_game_snapshot,
   tracker_events_raw, event.loop≤cutoff_loop) correctly deferred. §10 verdict
   audit: all 5 carry derived_section10_verdict=allowed, empty halting_falsifier.
8. **SQL/projection design sufficient + §4.2 cutoff semantics correct — PASS.**
   CROSS-02-03 §6.1 line 235 ("a pre_game family reads only static pre-match
   attributes of game T", cutoff "none (game-T attribute)") + CROSS-02-02 §6.1
   lines 224-228 confirm the planner is CORRECT that these 5 static families take
   NO history_time<target_time strict-< filter (that operator is for the deferred
   history tranche per CROSS-02-03 D5/§6.2). Leak-freedom triad (game-T pre-game
   columns only + POST-GAME token absence + non-tracker source) is correct.
   CROSS-02-00 §3.2 line 187 confirms started_at exists only in
   matches_history_minimal; sc2egset raw anchor is VARCHAR details_timeUTC.
   Design is specific enough for the downstream Chat second-pass (which §7
   mandates and the scaffold gate does NOT discharge).
9. **Focal/opponent symmetry (I5) addressed — PASS.** §4.3 self-join on
   (filename, player_id_worldwide); SAME expression both slots; no privileged
   slot; RISK-24 enumerated; designed names contain no POST_GAME token.
   `EXPECTED_PER_PLAYER_CONSTRUCTION="symmetric"` + `_check_symmetry`; registry
   per_player_construction=symmetric for all 5.
10. **PR #229 §10 vs PR #230 CROSS-02-01 evidence DISTINCT — PASS.** The
    leakage_audit json's own `notes` field states it is NOT a substitute for the
    PR #229 §10 verdict pair NOR for a future post-materialization audit. §10
    verdict CSV has 26 data rows (verified). Ledger §11 accurate; scaffold adds
    none, claims no clearance.
11. **Files minimal + repo-consistent — PASS.** Validator/test naming matches the
    two on-disk pairs (validate_registry_skeleton, validate_registry_section10_verdicts);
    jupytext config at sandbox/jupytext.toml = `formats = "ipynb,py:percent"`;
    9-file manifest minimal; notebook path matches the ROADMAP-declared notebook_path.
12. **Version bump correct — PASS.** Current pyproject 3.67.0 (verified); future
    scaffold-execution PR → 3.68.0 (MINOR, Category A feat); Layer-1 planning PR
    does not bump. Consistent with git-workflow "minor for feat".
13. **Blockers — none.** Every load-bearing assertion confirmed against disk.

## SQL / leakage-surface assessment (§4.1 / §4.2 / §4.3)

The leakage surface is the point of this unit and the plan handles it correctly
for a scaffold. **§4.2** is the load-bearing claim and survives scrutiny: the 5
families are game-T static pre-match attributes; the spec corpus (CROSS-02-03
§6.1 line 235; CROSS-02-02 §6.1 "none (game-T attribute)") confirms NO
`history_time < target_time` strict-`<` filter applies to them (that operator is
reserved for the deferred history tranche, CROSS-02-03 D5/§6.2). Leak-freedom
correctly rests on the triad (game-T-pre-game-columns-only + POST-GAME-token-
absence + non-tracker-source); the future substantive CROSS-02-01 §2.2 check
(must report 0) is correctly deferred to materialization, not claimed now. The
Random-race-is-post-decision trap (RISK-26) is correctly captured in §4.4
("eventually-played race is post-decision, NOT used"). **§4.1** is the most
material divergence: the registry CSV binds to `replay_players_raw`/`matches_flat`
(raw/flat) while CROSS-02-02 §6.1 names `matches_history_minimal.faction` /
`player_history_all.*` (view layer). The plan does NOT silently pick a layer — it
binds to the closed registry CSV (the authoritative catalog per the lineage
rule), records the divergence, and explicitly DEFERS the view-vs-raw layer
decision to the mandatory future second-pass (§4.1/§7/§10). This is the correct
disposition for a design-only scaffold. **§4.3** specifies a symmetric self-join
on (filename, player_id_worldwide) with the same expression in both slots and
RISK-24 enumerated — adequate for the downstream Chat leakage review §7 mandates.
The anchor-column-name divergence (details_timeUTC vs started_at) is the same
coupled view-vs-raw issue (nit 2). None of this makes the SCAFFOLD plan wrong or
indefensible; the genuinely leakage-sensitive resolution is correctly deferred to
the materialization PR plus its non-discharged Chat second-pass.

## Files inspected

.claude/scientific-invariants.md; .claude/rules/data-analysis-lineage.md;
sc2egset PHASE_STATUS.yaml / STEP_STATUS.yaml / ROADMAP.md (Step 02_01_02,
lines 2099-2272); 02_01_01_feature_family_registry.{csv,md};
02_01_01_section10_verdict_audit.csv; 02_01_01/leakage_audit_sc2egset.json;
reports/specs/02_00_feature_input_contract.md (§3.1/§3.2);
reports/specs/02_02_feature_engineering_plan.md (§6.1, §9, §12.1);
reports/specs/02_03_temporal_feature_audit_protocol.md (§6.1, D5/D7);
sandbox/jupytext.toml; validate_registry_skeleton.py (naming reference);
thesis/pass2_evidence/methodology_risk_register.md (RISK-20/24/26).

## ChatGPT second-pass leakage review addendum — PR #233

The second-pass identified that the planned `FORBIDDEN_SKILL_TOKENS` check would falsely reject the approved `is_mmr_missing_flag` / `focal_is_mmr_missing` / `opponent_is_mmr_missing` names because they contain the substring `mmr`. The plan now distinguishes approved MMR-missingness/provenance tokens from scalar/rating/skill MMR tokens using an explicit allowlist plus boundary-aware forbidden-token checks. No scope or scientific decision changed: `is_mmr_missing_flag` remains tranche 1, but scalar MMR/rating proxies remain forbidden/deferred.

## ChatGPT repo-first implementation review addendum — PR #233 exact-membership fix

ChatGPT identified that the first execution of the validator enforced "no extra pre_game family" but did not mechanically fail when a non-MMR expected tranche family was missing. The validator now exposes `missing_families_in_tranche`, checks exact set equality against `TRANCHE1_PRE_GAME_FAMILY_IDS`, and halts on `missing_families_in_tranche` before other falsifiers. This is an implementation correction against the approved exact-5-family plan; no scope changed.
