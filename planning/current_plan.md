---
title: "Chapters 1–4 citation & literature support audit (audit-only, pre-supervisor handoff)"
category: F
branch: docs/thesis-ch1-ch4-citation-literature-audit
date: 2026-05-17
planner_model: claude-opus-4-7
dataset: null
phase: null
pipeline_section: null
invariants_touched: [I3]
source_artifacts:
  - thesis/chapters/01_introduction.md
  - thesis/chapters/02_theoretical_background.md
  - thesis/chapters/03_related_work.md
  - thesis/chapters/04_data_and_methodology.md
  - thesis/references.bib
  - thesis/pass2_evidence/literature_verification_log.md
  - thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md
  - thesis/pass2_evidence/methodology_risk_register.md
  - thesis/pass2_evidence/phase02_readiness_hardening.md
  - thesis/pass2_evidence/notebook_regeneration_manifest.md
  - thesis/pass2_evidence/cross_dataset_comparability_matrix.md
  - thesis/pass2_evidence/aoe2_ladder_provenance_audit.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/
critique_required: false
research_log_ref: null
---

# Plan: Chapters 1–4 citation & literature-support audit before supervisor handoff

> **User-directed reviewer deviation (binding).** The task brief explicitly sets
> reviewer-deep as the mandatory plan gate (T01) and final gate (T03) for this
> audit-only documentation PR. reviewer-adversarial is **conditional** — invoked
> only on the §"Reviewer routing" escalation trigger. `critique_required: false`
> therefore reflects "no mandatory pre-execution adversarial critique",
> substituted by a mandatory reviewer-deep plan review at T01. This is an
> explicit user override of the default Category F adversarial-critique
> requirement and is recorded here for provenance.

## Scope

A single bounded Category F work unit: produce ONE durable audit document,
`thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`, that
verifies thesis Chapters 1–4 across five dimensions (bibkey existence +
metadata, claim-source support, REVIEW-flag triage, internal artifact-path
support, per-chapter supervisor-readiness) so the user can decide whether
Chapters 1–4 can be sent to the academic supervisor as a working draft. This
PR is an **audit only**: it produces evidence, not fixes. No chapter prose,
no `references.bib`, no citation add/remove, no flag closure, no new thesis
prose, no dataset artifacts, no notebooks, no Phase 03, no AoE2 Phase 02.

## Problem Statement

PR #216–#219 have landed the SC2EGSet provisional feature-family registry,
the Phase 01/02 writing-readiness audit, the Chapter 4 §4.3.x tracker /
repair work, and the §4.5 Phase 02 registry methodology framing (current
version 3.54.0). Chapters 1–4 are drafted but carry a large set of in-prose
`[REVIEW:]` / `[NEEDS CITATION]` / `[UNVERIFIED]` / `[NEEDS JUSTIFICATION]`
flags, several known citation-currency risks (e.g. EsportsBench version
drift), and repo-internal artifact-path claims in Chapter 4 whose support
must be confirmed before the chapters go to the supervisor. The user needs a
defensible, durable record that states — per chapter — whether the draft is
sendable now, what must be fixed first, what is safe to send behind a review
flag, what needs human full-text verification, and what is future-Phase
dependent and must NOT block handoff. No such consolidated Ch1–4 citation /
literature audit currently exists in `thesis/pass2_evidence/`.

## Assumptions & unknowns

- **Assumption:** Prior `thesis/pass2_evidence/` files (notably
  `literature_verification_log.md`, T14 2026-04-26, ~35 recorded URLs;
  `phase01_phase02_writing_readiness_audit.md`, 2026-05-17) are authoritative
  for the loci they already adjudicated; this audit **reuses** them rather
  than re-deriving, and cites the prior file + its recorded URL.
- **Assumption:** Chapter 3 literature loci are largely already verified by
  T14; incremental external web work concentrates on Chapter 1 / Chapter 2
  loci not covered by T14 and on confirming recorded conflicts.
- **Assumption:** Repo policy requires a per-PR semver bump (every recent
  thesis/docs PR carries a `chore(release)` commit; resolved in §"Repo-policy
  resolutions"). `docs/` ⇒ minor ⇒ 3.54.0 → 3.55.0.
- **Unknown:** PR number — not known until `gh pr create` at T00; the
  CHANGELOG/commit references are filled at T04 from `gh pr view --json
  number` (resolved by execution, not a blocker).
- **Unknown:** Exact in-body values for several sources (Demsar2006
  section-location, EsportsBench Table 2 cells, SC-Phi2 exact accuracy,
  Xie2020 metric type) — resolved by classification as
  `manual_full_text_required`, not by this audit.

## Literature context

This is an audit *of* the thesis's literature use, not new research. The
evidence base it reuses and the high-priority loci it must route are
enumerated in §"Evidence routing". The binding scientific-invariant context
is `[I3]` (temporal-leakage): Chapter 4 prose asserts the
tracker-never-pre-game and post-materialization-audit invariants; this audit
verifies those prose claims against `reports/specs/02_01_leakage_audit_protocol.md`,
`reports/specs/02_03_temporal_feature_audit_protocol.md`, and the SC2 tracker
eligibility artifact, but changes no code/spec/artifact. `[OPINION]`: the
highest-value triage output is the
`already_resolved_elsewhere_but_flag_remains` class — it separates stale
in-prose flag noise from live issues for the supervisor; this is an
audit-design judgement, not a cited claim.

## Audit methodology

Cross-cutting decision rules (apply to every dimension):

- **`manual_full_text_required` rule.** Classify a citation/claim
  `manual_full_text_required` when ALL of: (a) the load-bearing sub-claim is
  a value/section/table-cell/exact-figure inside the source body (not the
  abstract/metadata), AND (b) external retrieval cannot surface that body
  (PDF binary stream, paywall, content not surfaced) after the web-depth
  budget below is exhausted, AND (c) no prior pass2 file already records a
  web-verified value for that exact sub-claim. If a prior pass2 file recorded
  it as a manual-PDF item, inherit that classification and cite the prior
  file — do NOT re-attempt and do NOT upgrade to "verified".
- **Web-depth budget (user decision 2026-05-17).** For Chapter 1 / Chapter 2
  loci NOT already verified in `literature_verification_log.md`: up to **3
  distinct WebSearch/WebFetch formulations** to the preferred primary source
  before declaring `manual_full_text_required`. (User explicitly chose the
  deeper "up to 3 search formulations" option over single-fetch, given this
  is a supervisor handoff.)
- **"web conflicts with prose" rule.** If web evidence contradicts a chapter
  claim, record it in §4 of the deliverable with `verification_result =
  conflict_recorded_not_fixed` plus an explicit "chapter prose NOT edited by
  this audit" note; recommended_action names a future fix-PR, never an edit
  performed here.
- **Reuse-before-reverify rule.** Before any web fetch, check
  `literature_verification_log.md` and
  `phase01_phase02_writing_readiness_audit.md` §6. If the exact
  bibkey+sub-claim is already verified, set `verification_result =
  reused_prior_evidence` and cite the prior file + its recorded URL.
  Re-verify online ONLY for: loci not covered by any prior pass2 file;
  Chapter 1/2/4 loci (T14 covered Chapter 3); or a prior file that
  explicitly left the item open for Pass-2.
- **Chapter-prose freshness carve-out (mandatory).** The reuse rule above
  applies verbatim ONLY to *static* facts (bib/DOI/arXiv/venue/dataset
  metadata). For any **chapter-prose locus** (a claim whose support depends
  on what a chapter line currently says), before setting
  `reused_prior_evidence` the executor MUST re-read the current chapter line
  at HEAD and confirm the prior pass2 file's locus-level description still
  matches. If the chapter prose changed since the prior pass2 file froze its
  description, classify the current state freshly and record the prior
  file's now-stale description as `prior_pass2_locus_description_stale`,
  citing both. **Known instance:**
  `phase01_phase02_writing_readiness_audit.md` TQ-04 describes §3.2.4 as
  carrying an EsportsBench internal contradiction
  (`v9.0/2025-09-30` vs `v8.0 planowana`), but T14 (commit `8104be38`,
  2026-04-27 — an ancestor of the readiness audit `b8716095`) already
  cleaned §3.2.4 to `v9.0, cutoff 2026-03-31`; that TQ-04 sub-claim is
  stale at HEAD and MUST NOT be reused verbatim.

**Dimension 1 — Bibkey existence + metadata.** Extract every citation key
cited in Ch1–4 prose + per-chapter `## References` footers; confirm each
exists in `thesis/references.bib` (read-only); a key cited but absent =
BLOCKER (recorded, not fixed). Per key, check author/year/venue/identifier
plausibility against prior log (reuse) then ≤3-formulation web to
publisher/DOI/arXiv. Phantom scan: unresolved by all routes + not in any
prior pass2 → `manual_full_text_required` + candidate-phantom (use the
Tarassoli2024 closure precedent in `literature_verification_log.md` as the
evidentiary template; do NOT assert "phantom" without exhausting reuse + the
web budget).

**Dimension 2 — Claim-source support.** Scope = load-bearing literature
claims (a claim that, if wrong, changes a thesis conclusion: RQ framing,
novelty, method-choice justification, a numeric comparator entering Ch6).
Per claim, record verdict: `supported` / `partially_supported` /
`conflict_recorded_not_fixed` / `reused_prior_evidence` /
`manual_full_text_required`, checking the seven facets: game/dataset/task
identity, method family, metric name, numeric value, year/version/cutoff,
stated limitation, primary-vs-reimplementation provenance. Non-load-bearing
background citations get Dimension-1 metadata check only.

**Dimension 3 — REVIEW-flag triage.** Enumerate every flag in Ch1–4
(expected ≈ Ch1:8, Ch2:18, Ch3:14+1, Ch4:34+1; plus ≈18 `[POP:]` /
`[PRE-canonical_slot]` annotations — Ch4 only, Ch1–3 = 0 — triaged under a separate
"annotation, not a flag" disposition with its own count line). Classify
each flag into exactly one fixed value: `fix_before_supervisor`,
`ok_to_send_with_flag`, `manual_full_text_required`,
`future_phase_dependent`, `already_resolved_elsewhere_but_flag_remains`
(cross-check `literature_verification_log.md` remaining-flag column,
`methodology_risk_register.md` RISK-01..05 mitigation status, and
WRITING_STATUS PR-TG history to populate the
`already_resolved_elsewhere_but_flag_remains` pointers).

**Dimension 4 — Internal artifact-path support (Ch4).** Filesystem-confirm
every cited artifact path exists; re-confirm the load-bearing headline
counts (registry 26 data rows; tracker eligibility 15 rows / 5+7+3;
aoestats interface 137 lines vs prose-136 — the latter is the known TQ-05
issue already diagnosed in `phase01_phase02_writing_readiness_audit.md`,
recorded `reused_prior_evidence` + `conflict_recorded_not_fixed`, not
re-litigated). All other artifact-internal numbers: reuse the prior
readiness audit. Missing cited path = BLOCKER.

**Dimension 5 — Per-chapter readiness.** Each chapter gets exactly one
class via the max-severity rule (one BLOCKER ⇒ `not_ready`):
`ready_to_send` / `ready_to_send_with_disclaimer` /
`send_only_as_structure` / `not_ready`, with a one-paragraph justification
grounded in the deliverable's §4/§5/§6 tables.

## Evidence routing

Legend: **R** = reuse prior pass2 evidence (cite file; no re-fetch);
**W** = web-verifiable (≤3 formulations to preferred primary);
**M** = likely `manual_full_text_required`; **Repo** = filesystem/artifact check.

**Operative-verdict precedence (NIT-1 resolution, binding).** Where a route
letter is followed by a parenthetical, the **parenthetical verdict is
operative and binding**; the leading letter denotes only the verification
*channel*, never the conclusion. The executor must read the parenthetical —
not the letter — to determine the recorded `verification_result`, and must
apply the Chapter-prose freshness carve-out before any `reused_prior_evidence`.

**Chapter 1.** GarciaMendez2025 authors/target/accuracy → **R** then W-confirm
(EntComp DOI 10.1016/j.entcom.2025.101027 / arXiv 2510.19671; prior log: 2
authors, target = streaming not RTS → Ch1 flag =
`already_resolved_elsewhere_but_flag_remains`).
Shin1993/Forrest2005/Mangat2024 sports-betting transferability → **W** (not in
prior pass2; verify metadata + hedge fidelity → likely
`ok_to_send_with_flag`). AoE2 completeness 2024–2026 (CetinTas2023,
Elbert2025EC, +4 candidates) → **R** (`literature_verification_log.md` F-036
+ readiness §6.5: CetinTas2023 & Elbert2025EC verified; 4 candidates
unresolved by 2× WebSearch → `manual_full_text_required`). SC2↔AoE2 novelty
claim → **R** (readiness §1.5/§3.5 + Thorrez2024 row).

**Chapter 2.** Vinyals2017 SC2LE "800K" + baseline phrasing → **R** then W
(arXiv 1708.04782; prior log: win-pred is auxiliary; "800K" exact count
W-verify, else M). BlizzardS2Protocol 2.0.8 → **W/M** (s2protocol README =
protocol version not patch date; likely `ok_to_send_with_flag`).
Liquipedia_GameSpeed + Vinyals2017 22.4 loops/s → **W** (+ repo 160-loop/10s
cross-check reuse readiness §3.3). Aligulac/Glicko-2/TrueSkill/Bnet-MMR
grey-lit → **R** (prior log, flagged grey-lit, `ok_to_send_with_flag`).
EsportsBench version/cutoff — **three distinct loci, do NOT collapse to a
binary**: (i) §2.5.5 `02_theoretical_background.md:179` still carries stale
`v8.0/2025-12-31` (T14 was Chapter-3-only and did not touch it) →
`conflict_recorded_not_fixed`, **HIGH**, channel Repo+R (read the live line;
cite `literature_verification_log.md` note 4); (ii) §3.2.4
`03_related_work.md:77` and §3.5 `03_related_work.md:189` were already
corrected to `v9.0/2026-03-31` by T14 → `reused_prior_evidence` per
`literature_verification_log.md` (apply the Chapter-prose freshness carve-out
to confirm HEAD still matches); (iii)
`phase01_phase02_writing_readiness_audit.md` TQ-04's "§3.2.4 internal
contradiction" sub-claim is **stale at HEAD** → record
`prior_pass2_locus_description_stale`, do NOT reuse verbatim.
Demsar2006/Friedman/Wilcoxon N → **M** (PDF binary,
`manual_full_text_required`; do not re-attempt). Gneiting2007 + ECE → **R/Repo**
prose check (§2.6.2 states ECE is NOT a proper scoring rule → `supported`;
consistent with `methodology_risk_register.md` F14).

**Chapter 3 (mostly R — T14 already did this on 2026-04-26).**
Thorrez2024/EsportsBench: §3.2.4/§3.5 version/cutoff already T14-corrected →
`reused_prior_evidence` (NOT the stale TQ-04 §3.2.4 sub-claim — see the Ch2
EsportsBench three-locus note + Chapter-prose freshness carve-out); Table 2
80.13% / Glicko-2-vs-Aligulac row → **M** (PDF binary);
Khan2024SCPhi2 attribution → **R** (MDPI AI 5(4) 2338–2352; Tarassoli2024
phantom already deleted PR-TG4); exact accuracy → M. Yang2017Dota 9:1 +
58.69%/Kinkade → **R** (60.07% closed; split semantics M).
Silva2018LoL → **R** (ISSN 2179-2259 verified, flag closed PR-TG6b).
Xie2020 "below 2%" → **R+M** (Tier-3; metric-type M). Porcpine2020 r=0.96 →
**R** (caveat in prose → `ok_to_send_with_flag`). Elbert2025EC placement →
**R** (arXiv 2506.04475; residualization-not-SHAP). §3.5 gap currency → **R**
(readiness §2/§6.5 + F-036; 4 candidates M).

**Chapter 4 (all Repo / reuse — no web).** All artifact-path existence +
headline numbers → **Repo**; §4.3.3 tracker 15/5+7+3 + GATE-14A6 narrowed →
**R/Repo** (readiness §3.3 + `phase02_readiness_hardening.md` §14A.6);
§4.5 registry 26/14/V-9/`partial_coverage_v9_baseline` → **R/Repo**
(readiness §5.1 + `notebook_regeneration_manifest.md`); §4.4.5 ICC CI-method
`[UNVERIFIED]` → **R** (readiness §3.5 caveat — honest [UNVERIFIED] is
correct → `already_resolved_elsewhere_but_flag_remains`/`manual_full_text_required`);
§4.4.6 `[PRE-canonical_slot]` → **R** (annotation disposition); aoestats
136-vs-137 → **R** (readiness TQ-05; `conflict_recorded_not_fixed`);
SC2EGSet 2016–2024 / inventory / 22.4 loops/s / cleaning ledgers / identity
/ CROSS-02-01 non-supersession / AoE2 source-label discipline (aoestats
Tier 4; aoe2companion ID6 rm_1v1 / ID18 qp_rm_1v1 / 6+18 mixed-mode) → **R**
(readiness §3–§5 + `methodology_risk_register.md` RISK-01..05 +
`aoe2_ladder_provenance_audit.md`).

Pre-confirmed during planning (executor re-verifies, does not re-derive):
registry CSV = 27 lines = 1 header + 26 data rows ✓; tracker eligibility
CSV = 16 lines = 1 header + 15 data rows ✓; `phase06_interface_aoestats.csv`
= 137 lines (prose-136 = known TQ-05); SC2EGSet `01_exploration/` tree and
both AoE2 `01_exploration/` trees present ✓; `references.bib` = 100 `@`
entries; no pre-existing ch1–ch4 citation audit in `pass2_evidence/`.

## Execution Steps

### T00 — Branch + full plan + INDEX + bootstrap commit + draft PR

**Objective:** Establish the PR-first scaffold (branch, committed plan,
archived INDEX pointer, draft PR) so all subsequent work is pushed and never
local-only. The `planning-drift` pre-commit hook requires a complete
Category F plan, so the bootstrap commit carries this full plan (collapsing
the user-skeleton's separate stub/author steps — "bootstrap stub if repo
convention requires"; convention requires a full plan).

**Instructions:**
1. From clean master @ `26210a5d`: create branch
   `docs/thesis-ch1-ch4-citation-literature-audit` (done).
2. Write this full plan to `planning/current_plan.md`; update
   `planning/INDEX.md` (set this branch active; archive merged PR #219).
3. Commit via `.github/tmp/commit.txt` + `git commit -F` (message
   `chore(pr): bootstrap draft PR for Ch1–Ch4 citation/literature audit`);
   push `-u`.
4. Open **draft** PR via
   `gh pr create --draft --title "docs(thesis): audit Chapters 1–4 citations before supervisor handoff" --body-file .github/tmp/pr.txt`;
   delete `.github/tmp/*.txt`.

**Verification:** `gh pr view --json isDraft` → true; branch tracks remote;
`planning/INDEX.md` no longer shows PR #219 active; `git show --stat HEAD`
lists only `planning/current_plan.md` + `planning/INDEX.md`.

**File scope:** `planning/current_plan.md`, `planning/INDEX.md`,
`.github/tmp/commit.txt`, `.github/tmp/pr.txt`

**Read scope:** —

### T01 — reviewer-deep plan review (HALT on blocker)

**Objective:** Gate the committed plan through reviewer-deep before any audit
execution.

**Instructions:**
1. Dispatch **@reviewer-deep** with `planning/current_plan.md` + base_ref
   `26210a5d`. Checks: scope-boundedness (no chapter/bib edits possible),
   source-reuse discipline (reuses `literature_verification_log.md` /
   `phase01_phase02_writing_readiness_audit.md` rather than duplicating),
   `manual_full_text_required` decision rule soundness, structural
   overclaim-impossibility, frontmatter validity incl. the user-directed
   `critique_required:false` deviation.
2. If reviewer-deep raises a **methodology/source-scope BLOCKER**: HALT;
   surface to user; amend only on user direction; re-review. Do NOT proceed.
3. If reviewer output is committed: write to
   `planning/current_plan.critique.md`, commit, push.

**Verification:** reviewer-deep verdict recorded; 0 unresolved BLOCKERs.

**File scope:** `planning/current_plan.critique.md`,
`.github/tmp/commit.txt`

**Read scope:** `planning/current_plan.md`

### T02 — Execute the audit; write the deliverable

**Objective:** Produce
`thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md` covering
all 5 dimensions, reusing prior pass2 evidence, classifying unverifiable
sources `manual_full_text_required`, recording (not fixing) prose conflicts.

**Instructions:**
1. Reuse pass first (no web): read all prior `pass2_evidence/` files +
   both specs; build a reuse index of every (bibkey/sub-claim) already
   verified with its prior file + recorded URL.
2. Dimension 1: extract all cited keys from Ch1–4; diff vs `references.bib`
   (read-only); ≤3-formulation web only for keys not in reuse index and in
   Ch1/2/4.
3. Dimension 2: per load-bearing claim, apply the §"Audit methodology"
   verdict rules with the §"Evidence routing" table.
4. Dimension 3: enumerate + classify all flags into the fixed vocabulary;
   populate `already_resolved_elsewhere_but_flag_remains` pointers from the
   reuse index + RISK-01..05 status + WRITING_STATUS PR-TG history.
5. Dimension 4: filesystem-confirm every cited Ch4 path; re-confirm the
   three headline counts; reuse readiness audit for artifact-internal
   numbers; record aoestats 136-vs-137 as `conflict_recorded_not_fixed`
   citing TQ-05.
6. Dimension 5: assign each chapter exactly one class (max-severity rule).
7. Write the deliverable with the fixed §1–§11 structure (see
   §"Deliverable structure"), including the Polish supervisor note per
   `.claude/author-style-brief-pl.md` register (bezosobowy, argumentacyjny,
   ISO dates, no anglicyzmy branżowe). Every web row carries URL + access
   date; every repo row carries repo-relative path (+ line range if
   load-bearing); every reused row cites the prior pass2 file + its URL.
8. Commit via `.github/tmp/commit.txt` + `git commit -F` (message
   `docs(thesis): add Ch1–Ch4 citation & literature support audit`); push.

**HALT before finalizing the readiness verdict if:** any cited Chapter-4
artifact path does not exist (record BLOCKER, surface to user); OR a
load-bearing claim's verification would change a thesis conclusion AND is
not already adjudicated in a prior pass2 file (surface, do not silently
absorb).

**Verification:** deliverable exists with all §1–§11 sections incl.
Executive verdict `supervisor_handoff_recommendation` and the Polish note;
`git diff 26210a5d..HEAD --name-only` shows ZERO `thesis/chapters/**` and
ZERO `thesis/references.bib`; every `verified`/`supported` row has URL or
repo path or prior-file citation; ≥1 row demonstrates
`conflict_recorded_not_fixed`.

**File scope:**
`thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`,
`.github/tmp/commit.txt`

**Read scope:** all four chapter files (read-only), `references.bib`
(read-only), all prior `pass2_evidence/` files, both specs, Ch4 internal
artifact paths.

### T03 — reviewer-deep final audit review + mechanical fixes

**Objective:** Independent verification that the audit does not itself
overclaim and obeys all hard constraints.

**Instructions:**
1. Dispatch **@reviewer-deep** with `planning/current_plan.md` + base_ref
   `26210a5d`. Verifies: zero chapter/bib edits; every `verified`/`supported`
   row has admissible evidence (no "verified from abstract");
   `manual_full_text_required` correctly applied (no upgraded items);
   conflicts recorded-not-fixed; §1–§11 complete; Polish note register.
2. Escalate to **@reviewer-adversarial** ONLY IF reviewer-deep raises an
   unresolved methodology/overclaim BLOCKER OR the Executive verdict /
   `ready_to_send` classification constitutes a methodology-defensibility
   claim that may not survive examination (3-round symmetric cap; HALT +
   surface after round 3).
3. Apply ONLY mechanical, in-scope fixes to the audit doc (typos, missing
   URL/path on a row, structure completeness, classification-vocabulary
   consistency). NO new verification claims, NO scope expansion; record any
   substantive residual in the audit's own §7 and surface to user instead.
4. If changed: commit (`docs(thesis): apply reviewer-deep mechanical fixes
   to Ch1–Ch4 audit`); push.

**Verification:** reviewer-deep verdict, 0 unresolved BLOCKERs (or
reviewer-adversarial APPROVE if escalated); post-fix `git diff` touches only
the audit doc (and `planning/current_plan.critique.md` if reviewer output
committed).

**File scope:**
`thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`,
`planning/current_plan.critique.md`, `.github/tmp/commit.txt`

**Read scope:** the audit doc + base diff.

### T04 — Version bump + CHANGELOG

**Objective:** Apply the repo's mandatory per-PR semver bump.

**Instructions:**
1. Bump `pyproject.toml` `version` `3.54.0` → `3.55.0` (minor; docs PR per
   `.claude/rules/git-workflow.md` step 2).
2. Move CHANGELOG `[Unreleased]` → `## [3.55.0] — 2026-05-17 (PR #<n>:
   docs/thesis-ch1-ch4-citation-literature-audit)` with one `### Added`
   bullet for the audit doc; leave a fresh empty `[Unreleased]` with the
   four headers. `<n>` filled from `gh pr view --json number`.
3. Commit `chore(release): bump version to 3.55.0`; push.

**Verification:** `pyproject.toml` = 3.55.0; CHANGELOG `[Unreleased]` empty
with 4 headers; one bullet under `[3.55.0]`.

**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/commit.txt`

**Read scope:** —

### T05 — Refresh PR body; mark ready (NO merge)

**Objective:** Finalize the PR for review without merging.

**Instructions:**
1. Refresh `.github/tmp/pr.txt` per `.github/pull_request_template.md`
   (`## Summary` 1–5 bullets: audit-only, no chapter/bib edits, 5
   dimensions, reuse-not-duplicate; `## Test plan`: `git diff --name-only`
   shows only allowed files, reviewer-deep PASS, version bump present;
   footer line). `gh pr edit --body-file .github/tmp/pr.txt`.
2. `gh pr ready` (drops draft). **Do NOT merge.** Delete `.github/tmp/*.txt`.
3. Produce final report (PR URL, branch, commits, files changed, supervisor
   recommendation, must-fix count, reviewer verdicts, constraint
   confirmations, next user decision).

**Verification:** `gh pr view --json isDraft` → false; PR NOT merged; body
matches template.

**File scope:** `.github/tmp/pr.txt`

**Read scope:** —

## Deliverable structure

The audit doc has the fixed sections: **1** Executive verdict
(`supervisor_handoff_recommendation` ∈ {send_now, send_after_must_fixes,
do_not_send_yet}; recommended supervisor note; must-fix /
ok-to-send-with-flag / manual-full-text / future-phase counts); **2** Scope
and method (files read; web verification method; limitations; explicit
"no chapter prose edited" statement); **3** Chapter readiness matrix;
**4** Citation support issue table (id; severity BLOCKER/HIGH/MEDIUM/LOW;
chapter_file; section; citation_key_or_artifact_path; current_claim;
verification_result; recommended_action; source_evidence); **5** REVIEW flag
triage table (id; chapter_file; section; flag_text_summary; classification;
recommended_action; source_evidence); **6** Internal artifact path
verification table (id; chapter_file; section; artifact_path;
claim_supported?; notes); **7** Must-fix-before-supervisor backlog (target
file/section; reason; evidence; recommended PR scope; reviewer routing);
**8** OK-to-send-with-disclaimer items; **9** Future-phase-dependent items;
**10** Recommended supervisor handoff package (which chapters to send / not
send; suggested supervisor note **in Polish**; whether to include or strip
REVIEW flags); **11** Proposed next PRs (1–4, each: branch name; files
allowed; agent routing; reviewer routing; what not to claim).

## Reviewer routing

- **T01 (plan):** @reviewer-deep — scope-boundedness + source-reuse
  discipline + overclaim-impossibility. HALT on methodology/source-scope
  BLOCKER.
- **T03 (final):** @reviewer-deep — mandatory; verifies the audit does not
  itself overclaim.
- **@reviewer-adversarial escalation trigger (precise):** invoke ONLY IF
  (a) reviewer-deep at T01 or T03 raises an unresolved methodology/overclaim
  BLOCKER, OR (b) the audit's Executive verdict or any `ready_to_send`
  classification constitutes a methodology-defensibility claim that may not
  survive examination. Audit-doc-only nature ⇒ adversarial NOT auto-required.
- **3-round adversarial cap (symmetric):** if triggered, ≤3
  critique↔resolution rounds (symmetric to execution side per standing user
  feedback); after round 3 unresolved → HALT + surface to user.

## Risk register (audit overclaim guardrails)

| # | Where the audit could overclaim | Guardrail |
|---|---|---|
| AR-1 | "verified" from abstract/metadata only | `manual_full_text_required` rule; reviewer-deep T03 check |
| AR-2 | silently "correcting" a number prior pass2 adjudicated | reuse-before-reverify; cite prior file; never overwrite — record divergence |
| AR-3 | fixing prose on web conflict (scope breach) | "web conflicts" rule + forbidden-files + `git diff` gate |
| AR-4 | `ready_to_send` while a BLOCKER row exists | Dimension-5 max-severity rule; adversarial trigger (b) |
| AR-5 | "phantom" without exhausting reuse + web budget | D1 phantom rule; Tarassoli2024 closure template |
| AR-6 | duplicating / contradicting `literature_verification_log.md` | Ch3 routed **R**; new web only Ch1/2; reviewer-deep T01 check |
| AR-7 | treating `[POP:]`/`[PRE-canonical_slot]` as Pass-2 flags | D3 separate "annotation, not a flag" disposition |
| AR-8 | Polish note drifting into anglicyzmy / descriptive register | `.claude/author-style-brief-pl.md`; reviewer-deep T03 check |
| AR-9 | inheriting a prior-pass2 locus-conclusion the chapter has since outgrown (stale TQ-04 §3.2.4) | Chapter-prose freshness carve-out (mandatory re-read of HEAD before `reused_prior_evidence`; `prior_pass2_locus_description_stale` tag); reviewer-deep T03 check |

## Repo-policy resolutions

- **Version bump REQUIRED.** Every recent thesis/docs PR carries a dedicated
  `chore(release): bump version` commit (PR #219 → 3.54.0 `d96f56c6`; #218 →
  3.53.0). `.claude/rules/git-workflow.md` step 2: `docs/` ⇒ minor. 3.54.0
  → **3.55.0**. T04 is required, not optional.
- **No test gate.** git-workflow step 1 skips pytest/coverage when no `.py`
  in diff; this PR touches zero `.py` files.
- **Commit/PR conventions.** Commit message via `.github/tmp/commit.txt` +
  `git commit -F`; PR body via `.github/tmp/pr.txt` + `--body-file`; delete
  both after. Relative paths from repo root.
- **planning/INDEX.md update is in-scope** (active pointer still showed
  merged PR #219; T00 archives it).
- **Stale #219 critique-file purge is OUT of scope** for this audit PR
  (`planning/current_plan.critique_resolution.md` not in the user
  allowed-files list); flagged as residual repo-hygiene in the final report.

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00 |
| `planning/current_plan.critique.md` | Create (conditional) | T01 / T03 |
| `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md` | Create | T02 → T03 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T01/T02/T03/T04/T05 |

## Gate Condition

- Draft PR opened at T00; PR marked ready (NOT merged) at T05.
- `git diff 26210a5d..HEAD --name-only` lists ONLY: the audit doc,
  `planning/current_plan.md`, `planning/INDEX.md`, optionally
  `planning/current_plan.critique.md`, `CHANGELOG.md`, `pyproject.toml`.
  ZERO entries under `thesis/chapters/`, `thesis/references.bib`, datasets,
  notebooks, specs, status YAMLs, `.claude/`, `docs/TAXONOMY.md`.
- Audit doc contains all 11 fixed sections incl. Executive verdict with a
  `supervisor_handoff_recommendation` value and the Polish supervisor note.
- Every `verified`/`supported` row carries a URL, repo path, or prior-pass2
  citation; ≥1 row demonstrates `conflict_recorded_not_fixed`; every
  `manual_full_text_required` row names why the body was unretrievable.
- reviewer-deep PASS with 0 unresolved BLOCKERs at T01 and T03
  (reviewer-adversarial APPROVE iff escalated).
- `pyproject.toml` = 3.55.0; CHANGELOG `[Unreleased]` empty with 4 headers.

## Out of scope

- Any chapter prose edit, flag closure, renumbering, or `references.bib`
  change (deferred to the "Proposed next PRs" the audit enumerates in its
  §11).
- Re-verifying Chapter 3 loci already verified in
  `literature_verification_log.md` (reuse only).
- Re-deriving artifact-internal numbers already mapped in
  `phase01_phase02_writing_readiness_audit.md` (reuse only).
- Resolving `manual_full_text_required` items (needs human full-text read).
- Fixing the aoestats 136-vs-137 framing or the EsportsBench version drift
  in chapter prose (record-not-fix; route to future PRs).
- Phase 03 / AoE2 Phase 02 / notebook execution / dataset artifact
  generation.
- Stale PR #219 planning critique-file purge (residual repo-hygiene; not in
  the user allowed-files list for this PR).

## Open questions

- **Web-verification depth — RESOLVED (user decision 2026-05-17):** up to
  **3 distinct search formulations** per new Ch1/Ch2 locus before
  `manual_full_text_required` (user chose the deeper option over
  single-fetch given supervisor handoff). Resolved by: user decision.
- **EsportsBench version-drift handling — RESOLVED (user task brief):**
  record as `conflict_recorded_not_fixed` (HIGH); route prose fix to a
  future PR; do NOT touch §2.5.5/§3.2.4/§3.5. Resolved by: user instruction
  ("if web evidence conflicts with chapter prose, mark issue; do not fix
  prose").
- **reviewer-adversarial — RESOLVED (user task brief):** conditional only,
  per §"Reviewer routing" trigger. Resolved by: user instruction.
- **Dimension-2 scope — RESOLVED (user task brief):** load-bearing claims
  only ("for every load-bearing literature claim"). Resolved by: user
  instruction.
- **PR number in CHANGELOG/commit — RESOLVED:** filled at T04 from
  `gh pr view --json number`. Resolved by: execution.
