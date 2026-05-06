---
critique_of: planning/current_plan.md
plan_branch: phase02/roadmap-stubs-feature-registry
critique_role: reviewer-deep
critique_model: claude-opus-4-7
critique_date: 2026-05-06
verdict: PASS-WITH-FIXES
---

# Reviewer-deep critique — Phase 02 ROADMAP-stubs PR plan

## Verdict

**PASS-WITH-FIXES.** The plan is structurally sound, scope-disciplined, and faithful to the non-batching rule: it carries only ROADMAP-stub edits, declares (does not create) sandbox/artifact paths, and excludes status YAML / research_log edits in line with `data-analysis-lineage.md` sequence step 1. Five fixes are required before execution: (1) the SC2 stub's `slot_identity_consistency = sanity_gate_not_model_input` claim is a *new* registry vocabulary that does not exist as a `status_in_game_snapshot` value in the upstream tracker CSV (the CSV records that family as `eligible_for_phase02_now` with the `notes_for_phase02` text "feature-engineering sanity gate; not a model input") — the executor must encode this as a registry-level reclassification that *cites* both CSV columns rather than as a verbatim CSV value, otherwise T04 §5 mechanical check is internally consistent but methodologically misleading; (2) the "spec_id literal" framing is sloppy — for CROSS-02-02 and CROSS-02-03 the spec frontmatter has `spec_id: CROSS-02-02-v1` / `CROSS-02-03-v1` while only `version: …-v1.0.1` carries the patch suffix (CROSS-02-00 and CROSS-02-01 are the only two whose `spec_id` field is literally `…-v3.0.1` / `…-v1.0.1`) — the plan should call these "version literals" or accept that "spec_id literal" is used as a project shorthand and document that explicitly; (3) the WP-2 paragraph the plan asks to "preserve verbatim" cites `CROSS-02-01-v1` (no patch suffix) — verbatim preservation conflicts with the plan's own appended sentence that names `CROSS-02-01-v1.0.1`, producing two different version strings for the same spec inside the same section — choose one; (4) the in-plan instruction to dispatch reviewer-adversarial (§§523–524, §564) contradicts `data-analysis-lineage.md` §"Agent and model routing discipline" final paragraph ("for this active Phase 02 readiness PR, do not invoke reviewer-adversarial unless the plan is amended or reviewer-deep raises a BLOCKER"); the plan's "applies only to PR #209" reading is asserted but not supported by the rule text — adopt reviewer-deep as the gate per the parent's dispatch routing, and demote reviewer-adversarial to "if reviewer-deep raises a methodology BLOCKER"; (5) the branch prefix `phase02/` is non-canonical for Category A per `docs/TAXONOMY.md` §Category which says Category A is `feat/`; this PR inherits the `phase02/feature-engineering-readiness` branch precedent from PR #209/#210 but the plan should explicitly cite that precedent rather than implicitly re-using a non-canonical prefix. None of these are structural blockers; they are corrigible by edit before T01 dispatches.

## BLOCKERS (must be resolved before execution)

None.

## REQUIRED FIXES (small but necessary)

1. **`slot_identity_consistency` registry classification source.**
   Plan T01 description (`current_plan.md` lines 113–129) says
   "`slot_identity_consistency is sanity_gate_not_model_input`." The
   tracker CSV at
   `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`
   line 15 (`slot_identity_consistency` row) records
   `status_in_game_snapshot = "eligible_for_phase02_now"`, NOT
   `sanity_gate_not_model_input`. The "sanity gate" semantic is in
   `notes_for_phase02 = "feature-engineering sanity gate; not a model input"`
   and the `eligibility_scope = "structural validity check: per-replay
   assertion …"` columns. The executor must rewrite the SC2 YAML's
   description and halt-predicate so `sanity_gate_not_model_input` is
   declared as a *registry-introduced classification* derived from the
   notes/scope columns, not as a CSV-level status. Otherwise T04 §5's
   "explicitly classifies `slot_identity_consistency` as
   `sanity_gate_not_model_input`" check passes mechanically but the
   stub silently fabricates a CSV-vocabulary that does not exist. Fix:
   add a one-clause hedge — "`sanity_gate_not_model_input` is a
   registry-introduced classification derived from the CSV's
   `notes_for_phase02` field; the CSV's `status_in_game_snapshot` for
   this row reads `eligible_for_phase02_now`."
2. **`CROSS-02-02-v1.0.1` and `CROSS-02-03-v1.0.1` are version literals,
   not `spec_id` literals.**
   Plan §"Step YAML content (sc2egset)" (line 107 — "the strings
   `CROSS-02-00-v3.0.1`, `CROSS-02-01-v1.0.1`, `CROSS-02-02-v1.0.1`,
   `CROSS-02-03-v1.0.1` must each appear at least once verbatim") and
   the equivalent passages in T02 / T03 frame all four strings as
   `spec_id` literals. Spec frontmatter check: CROSS-02-00 has
   `spec_id: CROSS-02-00-v3.0.1` (matches), CROSS-02-01 has `spec_id:
   CROSS-02-01-v1.0.1` (matches), CROSS-02-02 has `spec_id:
   CROSS-02-02-v1` and `version: CROSS-02-02-v1.0.1` (mismatch),
   CROSS-02-03 has `spec_id: CROSS-02-03-v1` and `version:
   CROSS-02-03-v1.0.1` (mismatch). Fix: add a short sentence to the
   plan's Assumptions section saying "The strings cited as `spec_id`
   literals throughout this plan correspond to the major-minor-patch
   `version` field for CROSS-02-02 / CROSS-02-03 (whose
   frontmatter `spec_id` field is the bare `-v1` form) and to the
   verbatim `spec_id` field for CROSS-02-00 / CROSS-02-01. The four
   strings are the project-canonical reference form; the
   distinction between `spec_id` and `version` in frontmatter is a
   versioning-convention artifact, not a lineage break." Without this
   fix, a future reviewer-adversarial reading the stubs would
   reasonably ask "where is `CROSS-02-02-v1.0.1` declared as a
   `spec_id`?" and the answer is "nowhere — it is a `version` field
   that the project treats as the canonical citation form."
3. **WP-2 paragraph version-string conflict.**
   Plan T01 step 3 (line 98) and parallel T02 / T03 instructions say
   "the 2026-04-21 WP-2 mandatory-entry-requirement paragraph
   **preserved verbatim** (do not paraphrase)." Verbatim preservation
   includes `CROSS-02-01-v1` and `CROSS-02-00-v1` (the original
   2026-04-21 lock string used in all three ROADMAPs at lines 1910 /
   1753 / 1421 — confirmed against on-disk content). The plan also
   asks the executor to append a new sentence (line 99 / parallel)
   citing `CROSS-02-01-v1.0.1` and `CROSS-02-02-v1.0.1`. Result: the
   same paragraph cites the same spec under two different version
   strings (`CROSS-02-01-v1` and `CROSS-02-01-v1.0.1`). This is
   harmless lineage-wise — `v1.0.1` is the patch successor of `v1` —
   but it is editorially confusing and easy for a future reader to
   read as drift. Fix: either (a) change "preserve verbatim" to
   "preserve content but bump WP-2's spec citations to the
   currently-locked v1.0.1 string", or (b) keep verbatim preservation
   and add a one-line footnote in the appended sentence saying "WP-2
   above cites the 2026-04-21 initial lock string `CROSS-02-01-v1`;
   the currently-locked patch successor is `CROSS-02-01-v1.0.1` (no
   audit-dimension change; convention per the spec's amendment log)."
4. **Reviewer routing — plan instruction contradicts active rule.**
   Plan §"Gate Condition" item 4 (lines 523–524) and §"Critique
   instruction" (line 562) both instruct dispatching
   reviewer-adversarial. `data-analysis-lineage.md` §"Agent and model
   routing discipline" final paragraph reads: "For this active Phase
   02 readiness PR, do not invoke reviewer-adversarial unless the
   plan is amended or reviewer-deep raises a BLOCKER requiring
   adversarial methodology review." The plan's parenthetical
   ("applies only to **PR #209**; this is the next-after-#210 PR
   and Category A standard rules apply") is an interpretation, not a
   citation — the rule says "active Phase 02 readiness PR" without
   pinning to a specific PR number, and the rule was edited in commit
   `0bd9fc2f` (after PR #210 merged) so it post-dates PR #209.
   Furthermore, the parent's dispatch routed this critique to
   reviewer-deep, not reviewer-adversarial — confirming the parent's
   reading. Fix: change Gate Condition item 4 to "Reviewer-deep
   critique exists at `planning/current_plan.critique.md` per
   `data-analysis-lineage.md` §"Agent and model routing discipline".
   reviewer-adversarial is escalated only if reviewer-deep raises a
   methodology BLOCKER." Update §"Critique instruction" (lines 562–
   572) to address reviewer-deep, not reviewer-adversarial.
5. **Branch prefix non-canonical for Category A.**
   Frontmatter `branch: phase02/roadmap-stubs-feature-registry`
   conflicts with `docs/TAXONOMY.md` §Category which assigns
   Category A the `feat/` prefix. The plan's `version_bump` line
   (frontmatter line 12) explicitly cites
   `.claude/rules/git-workflow.md` §"PR Creation Flow" step 2's
   "minor for feat/refactor/docs" rule and routes Category-A→`feat/`
   to a minor bump — but the actual branch is `phase02/`. PR #209
   and PR #210 used `phase02/feature-engineering-readiness` and
   `docs/phase02-contracts-lock-and-planning-cleanup` respectively,
   establishing precedent for Phase 02 readiness work to use a
   `phase02/` prefix or a `docs/` prefix rather than the canonical
   `feat/`. The plan should either (a) cite that precedent
   explicitly in `Assumptions & unknowns` ("Branch prefix `phase02/`
   inherited from PR #209 / PR #210 precedent for Phase 02 readiness
   work; not the canonical `feat/` per `docs/TAXONOMY.md` §Category;
   minor-version-bump rule still applies because the work is
   substantively a `feat`"), or (b) rename the branch to
   `feat/phase02-roadmap-stubs-feature-registry` to comply with
   `docs/TAXONOMY.md` literally. Option (a) is the lower-friction
   path given the existing `phase02/feature-engineering-readiness`
   parent branch convention.

## WARNINGS (cosmetic / discretionary)

1. **`predecessors: "01_06_04"` is a single string, not a list.**
   `docs/templates/step_template.yaml` lines 81–84 shape the field as
   a YAML list (`- "<step number…>"`), and existing step blocks in
   the three ROADMAPs use list form. The plan's three YAML blocks
   write `predecessors: "01_06_04"` (T01 §"Step YAML content" line
   160; T02 step 3 third bullet line 309; T03 step 3 third bullet
   line 368) as a bare string. This will parse as a different YAML
   shape and may break downstream tooling that does
   `for p in step.predecessors: …`. Fix: use list form
   `predecessors: ["01_06_04"]` or block-list form
   `predecessors:\n  - "01_06_04"`.
2. **`predecessors` for the SC2 stub may need to be plural.**
   The SC2 modeling-readiness exit chain produced
   `01_06_01` / `01_06_02` / `01_06_03` / `01_06_04` (data dictionary,
   data quality report, risk register, modeling readiness decision)
   per `STEP_STATUS.yaml` lines for `01_06_*`. The registry "reads
   CROSS-02-02 §6 sc2egset feature-family rows and tracker CSV" and
   declares per-family classifications keyed off RISK-20 / RISK-24 /
   RISK-26 (plan §§T01 step YAML lines 180–230). RISKs live in the
   risk register at `01_06_03`. If the registry plans to cite a RISK
   id by number (it does — see line 156 "RISK-26 — Random race
   semantics"; line 251 — "Amendment 2 of PR #208"), then `01_06_03`
   is also a transitive predecessor of `02_01_01`. Recommend listing
   `["01_06_03", "01_06_04"]`. Same applies to T02 / T03.
3. **`pyproject.toml` version line check.**
   Plan T05 step 1 (line 467) says "Edit `pyproject.toml` line 3 from
   `version = "3.46.0"` to `version = "3.47.0"`. Do not modify any
   other line." Pinning the line number to "line 3" is fragile — if
   the file's leading comment / `[project]` ordering ever shifts,
   "line 3" may not be the version line. Recommend "Edit
   `pyproject.toml`'s `version = "3.46.0"` line under the `[project]`
   table" without a literal line-number reference.
4. **`grep` patterns ignore quoted vs unquoted forms.**
   T01 verification (line 277) uses `grep -F 'CROSS-02-00-v3.0.1'`
   etc. If the executor accidentally writes the spec_id inside YAML
   single-quoted form (`'CROSS-02-00-v3.0.1'`), `grep -F` matches; if
   they write it as a YAML !!str scalar with a backslash-escape, the
   grep still matches because `-F` is fixed-string. Fine in practice;
   noted only because YAML's quoting is more permissive than the
   verification check assumes — a pathological encoding (e.g., the
   Unicode em-dash variant of `-`) would not be caught.
5. **`pipeline_section` field shape.**
   Plan T01 step YAML line 135 writes
   `pipeline_section: "02_01 -- Pre-Game vs In-Game Boundary"`. Other
   committed steps use `pipeline_section: "02_01"` (the bare
   numeric/slug ID per `docs/TAXONOMY.md` §Pipeline Section). The
   plan's form embeds the section name into the field value. This
   may or may not parse against `docs/templates/step_template.yaml`
   which says `value: "<NN_NN — section name, per docs/PHASES.md>"` —
   the template literally suggests embedding the name. Cross-check
   with existing committed Phase 01 step blocks before locking the
   shape; do not silently break with previous Step YAML format.
6. **`phase` field shape.**
   Same observation: plan writes
   `phase: "02 -- Feature Engineering"` (line 134). Template
   suggests this form; existing Phase 01 step blocks should be the
   ground truth — the plan's form must match what
   `02_01_PRACTICAL_VALIDATION` parsers expect. Validate by reading
   one Phase-01 step block from each of the three ROADMAPs before
   T01 dispatch.
7. **`02_FEATURE_ENGINEERING_MANUAL.md, Section 2` reference.**
   `manual_reference: "02_FEATURE_ENGINEERING_MANUAL.md, Section 2"`
   (T01 line 136). Spec text and `docs/PHASES.md` use `§2` notation,
   not "Section 2"; consistency with existing Phase 01 step blocks
   should drive the choice.
8. **OQ3 (CHANGELOG Unreleased preservation) is technically a
   conditional execution branch, not an open question.**
   Plan §"Open questions" OQ3 (lines 557–558) describes a branch in
   T05's behavior depending on whether `[Unreleased]` is empty.
   "Open questions" by convention are blockers-on-user; this is a
   handle-at-execution-time conditional and belongs in T05's
   instructions, not Open Questions. Fold it into T05 step 2.
9. **`gate.artifact_check: "NOT APPLICABLE TO THIS ROADMAP-STUB PR"`**
   T01 step YAML lines 230–235. The Step YAML schema uses
   `gate.artifact_check` as a forward-looking condition for the
   Step's *eventual* gate; "NOT APPLICABLE" reads as if the Step
   itself has no gate, which is incorrect (the future scaffold PR's
   gate is the registry CSV + MD existence check). Recommend
   rewriting as: "Future-PR predicate: the planned CSV and MD
   exist at the declared paths and are non-empty. NOT EVALUATED in
   this ROADMAP-stub PR." Same edit applies to T02 / T03.
10. **`thesis_mapping` Chapter 4 §4.5 reference.**
    Plan T01 line 266 / T02 / T03 cite "Chapter 4 — Data and
    Methodology > §4.5 Feature engineering plan (sc2egset registry)".
    The thesis structure (`thesis/THESIS_STRUCTURE.md` if it exists)
    should be consulted to confirm §4.5 is the canonical landing
    section; the plan does not list it under `source_artifacts`. Not
    blocking, but worth confirming before lock.

## NOTES (informational / future-PR carry)

1. The plan reasonably declares the future scaffold path
   `sandbox/<game>/<dataset>/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py`.
   When the next-PR scaffold lands, the executor should verify the
   directory mirror enforcement in `rts_predict.common`'s notebook
   helpers — the artifacts mirror landing path is
   `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
   (per `docs/TAXONOMY.md` §"Mirroring rule"); the plan's declared
   output path matches.
2. The plan does not propose creating
   `PIPELINE_SECTION_STATUS.yaml` for `02_01` in any of the three
   datasets. This is correct (sequence step 8 territory), but a
   future PR will need to create that file *before* Phase 02 is
   marked `in_progress`. The next-PR plan should explicitly carry
   that creation to keep the derivation chain
   `STEP_STATUS → PIPELINE_SECTION_STATUS → PHASE_STATUS` intact.
3. The plan's reproducibility bullet (T01 step YAML lines 185–190)
   says "no magic constants (Invariant I7); cold-start handling
   expressed as gate categories per CROSS-02-02-v1.0.1 §9 (G-CS-1
   through G-CS-6)." Verify before T01 dispatch that
   `reports/specs/02_02_feature_engineering_plan.md` §9 actually
   contains G-CS-1 through G-CS-6 (the plan asserts this; the
   reviewer-deep evidence from spec frontmatter is consistent but
   not verified at gate-cell granularity here).
4. T04 §6 writes the consistency report to
   `.github/tmp/t04_consistency_report.txt`. Per memory note
   `.github/tmp/pr.txt` cleanup precedent, this file MUST be
   deleted before the final commit. The plan says "deleted before
   commit" (line 449); ensure executor adds an explicit
   `rm -f .github/tmp/t04_consistency_report.txt` step.
5. `predecessors` for the AoE2 stubs cite `01_06_04` as the
   modeling-readiness exit step. Verify by spot-check that
   `01_06_04` for aoestats and aoe2companion is named "Modeling
   Readiness Decision" (or equivalent), not some unrelated step.
   Confirmed for SC2 (`STEP_STATUS.yaml` line 1163: "Modeling
   Readiness Decision"); not verified here for aoestats /
   aoe2companion at gate-cell granularity. Executor should confirm
   during T02 / T03.

## Verification log

| Item | Verdict | Evidence |
|------|---------|----------|
| Frontmatter complete and consistent with Cat A | PASS | `current_plan.md` lines 1–40 — all required fields per `docs/templates/planner_output_contract.md` Layer 1 present, except `branch` is `phase02/` not `feat/` (see REQUIRED FIX 5) |
| `## Execution Steps` parent heading present | PASS | `current_plan.md` line 87 |
| `### T01`, T02, …, under parent | PASS | lines 89, 298, 357, 416, 462 |
| Each task has objective / allowed files / forbidden files / stop / validation / model annotation | PASS-WITH-NOTES | T01–T05 all carry these. Forbidden-files lists are by inclusion in §"Out of scope" + §"Files NOT in this manifest" rather than per-task — acceptable; the executor reads the entire plan before each task |
| Out-of-scope enumerates notebooks / artifacts / raw / status YAML / research_log / thesis / locked specs | PASS | lines 529–549 (13 explicit items) |
| All four `spec_id` literals appear verbatim in plan body | PASS-WITH-CAVEAT | greppable; but two are version literals not `spec_id` literals (REQUIRED FIX 2) |
| No locked spec is paraphrased without version suffix | PASS | the four cited strings carry their suffixes |
| No locked spec proposed for revision/lock-bump | PASS | §"Out of scope" line 544 explicit |
| T05B2 receipt not proposed for regeneration | PASS | §"Out of scope" line 545 explicit |
| ROADMAPs not touched by readiness specs (CROSS-02-02 §12) | PASS | §"Problem Statement" lines 58–59 quote the §12 non-edit rule verbatim |
| "Tracker-derived features are never pre-game" stated verbatim | PASS | T01 step YAML lines 199–200 |
| `history_time < target_time` strict-`<` | PASS | T01 step YAML line 197; T02 step 5 line 329; T03 step 5 line 388 |
| `event.loop <= cutoff_loop` form | PASS | T01 step YAML line 198 |
| tracker_events_feature_eligibility.csv cited by exact path | PASS | T01 step YAML lines 124, 171 |
| Only `eligible_for_phase02_now` and `eligible_with_caveat` admitted | PASS | T01 step YAML line 126; halt-predicate lines 250–253 |
| 3 blocked rows excluded explicitly | PASS | T01 step YAML lines 129, 250–252; T04 §4 line 437 |
| `slot_identity_consistency` classified as `sanity_gate_not_model_input` | FAIL | T01 line 130 — but CSV records `eligible_for_phase02_now` for this row; see REQUIRED FIX 1 |
| AoE2 source-label vocabulary preserved (Tier 4 / ID 6 / ID 18 / mixed-mode) | PASS | T02 step 3 lines 308–310; T03 step 3 line 367 |
| `in_game_snapshot` declared NOT supported for both AoE2 stubs | PASS | T02 step 3 line 308; T03 step 3 line 367 |
| No magic numeric constants for cold-start gates | PASS | T01 step YAML reproducibility line 188 ("G-CS-1 through G-CS-6"); halt-predicate line 254 |
| No batching of ROADMAP + notebook + artifact + next step | PASS | §"Out of scope" lines 533–536 explicit; halt-predicate lines 256–257 |
| No notebook scaffold proposed | PASS | §"Out of scope" line 533 |
| No validation module execution proposed | PASS | §"Out of scope" line 535 |
| Each task has stop condition + validation report | PASS | T01–T05 all enumerate Verification commands |
| Each task has executor-model annotation with rationale | PASS | T01 lines 292–294; T02 lines 351–353; T03 lines 410–412; T04 lines 456–458; T05 lines 486–488 |
| Forbidden-files list explicit | PASS | §"File Manifest > Files NOT in this manifest" lines 505–514 |
| `02_01` is canonical home of feature-family registry per `docs/PHASES.md` | PASS | `docs/PHASES.md` line 114 ("`02_01`  Pre-Game vs In-Game Boundary") |
| Step number `02_01_01` matches taxonomy convention | PASS | `docs/TAXONOMY.md` lines 86–90 |
| Sandbox path matches `docs/TAXONOMY.md` | PASS | `docs/TAXONOMY.md` lines 122–135; plan T01 line 162 |
| Sandbox files NOT created | PASS | §"Out of scope" line 533 |
| Predecessor `01_06_04` exists in all three STEP_STATUS.yamls | PASS | `grep -E '"01_06_04":'` returns hits in all three files (verified) |
| T04 read-only / no file edits | PASS | T04 step 7 line 440 explicit |
| T04 deliverable is textual report, not artifact under `reports/artifacts/` | PASS | T04 line 449 — `.github/tmp/t04_consistency_report.txt`, ephemeral |
| Version bump tier matches `git-workflow.md` for Cat A `feat/` minor | PASS-WITH-CAVEAT | `git-workflow.md` says "minor for feat/refactor/docs"; branch is `phase02/`, not `feat/` (REQUIRED FIX 5) |
| CHANGELOG move pattern matches | PASS | T05 step 2 lines 468–471 |
| PR-number `<TBD>` placeholder pattern acceptable | PASS | T05 lines 462–471 — `(PR #N: phase02/roadmap-stubs-feature-registry)` per PR #209/#210 precedent |
| Plan scope strictly ROADMAP-stubs-only | PASS | §"Scope" lines 44–48 |
| Plan does not modify methodology files | PASS | §"Out of scope" line 514 explicit |
| Plan does not propose `02_05_*` or further specs | PASS | §"Out of scope" line 548 |
| No thesis chapter edits proposed | PASS | §"Out of scope" line 542 |
| Status YAML / research_log edits zero-justified explicitly | PASS | §"Assumptions" A3, A4 (lines 69–70); §"Out of scope" lines 540–541 |
| Reviewer routing aligns with active rule | FAIL | §"Gate Condition" item 4 + §"Critique instruction" §564 dispatch reviewer-adversarial; `data-analysis-lineage.md` final paragraph and the parent's actual dispatch routing both indicate reviewer-deep is the gate (REQUIRED FIX 4) |
| WP-2 paragraph version-string consistency | FAIL | WP-2 verbatim cites `CROSS-02-01-v1`; appended sentence cites `CROSS-02-01-v1.0.1`; same paragraph uses two version strings for one spec (REQUIRED FIX 3) |
| `predecessors` field shape (list vs string) | WARNING | Plan writes bare string; existing Phase 01 step blocks use list form (WARNING 1) |

## Reviewer-deep recommendation for executor dispatch

Dispatch may proceed **only after** the five REQUIRED FIXES are addressed in `planning/current_plan.md`. The fixes are mechanical and small (≤ 50 lines of edit total); none of them requires re-planning. Once fixed, the plan is mergeable as-is — its scope discipline, non-batching compliance, and methodology trace are all defensible. Reviewer-adversarial is *not* required for this PR per the active `data-analysis-lineage.md` exception, unless the executor's edits inadvertently change the methodology surface (e.g., re-introducing a magic constant or relaxing the strict-`<` cutoff). After T01–T05 land, the standard final-review gate is reviewer-deep, not reviewer-adversarial.
