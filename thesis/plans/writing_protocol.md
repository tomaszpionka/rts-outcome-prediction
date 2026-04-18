# Thesis Writing Protocol

Operator's guide to drafting thesis chapters using the plan/execute
workflow and Claude Code subagents. This document is the operational
"how"; the contract is `.claude/rules/thesis-writing.md`, which takes
precedence in any conflict.

Revised: 2026-04-18. Supersedes `thesis/plans/idea_audit.md`,
`thesis/plans/idea_audit_review.md`, and `thesis/plans/writing_manual.md`.

## 0. Scope and section types

The thesis contains two kinds of draftable section, distinguished by
the `Feeds from:` column in `thesis/WRITING_STATUS.md`.

| Type | `Feeds from:` | Source material | Example sections |
|---|---|---|---|
| **Literature** | `—` (em dash) | Papers, textbooks, domain knowledge. No report artifacts. | §1.1-§1.4, §2.1, §2.4-§2.6, §3.1-§3.5, §4.4.4, §6.5, §7.3 |
| **Data-fed** | A specific Phase + Step range | Report artifacts under `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/...` plus `research_log.md` entries | §4.1.x, §4.2.x, §5.x |

Some sections are mixed (see §2.2, §2.3 in WRITING_STATUS.md) — treat
them as data-fed for the data portion and literature for the rest. The
"must cite / must justify / must contrast" layering below is additive,
not exclusive.

A data-fed section becomes DRAFTABLE when every Step it references in
its `Feeds from:` column is marked `complete` in the active dataset's
`STEP_STATUS.yaml`. A literature section is DRAFTABLE at any time once
Gate 0 and Gate 0.5 have passed.

## 1. Agent capability matrix

Source of truth: `.claude/agents/<agent>.md` frontmatter. Any discrepancy
between this table and the agent files is a bug in this file — fix here,
not there.

| Agent | Model | permissionMode | Write/Edit | WebFetch | WebSearch | Used here for |
|---|---|---|---|---|---|---|
| `planner-science` | opus / max | plan | no | yes | yes | Step 1 (plan) |
| `writer-thesis` | opus / max | — | yes (thesis/, planning/, temp/; plan-authorized: thesis/pass2_evidence/, thesis/references.bib, thesis/WRITING_STATUS.md) | yes | yes | Gate 0, Gate 0.5, Step 4 (draft) |
| `reviewer-adversarial` | opus / max | plan | no | yes | yes | Step 2 (plan critique), Step 5 (draft critique) |
| `reviewer` | sonnet / high | — | no (tools: Read/Grep/Glob/Bash) | no | no | Step 5.5 (optional consistency) |
| `executor` | sonnet / high | — | yes | no | no | Not used for thesis drafting |

Key non-obvious constraints:
- `writer-thesis` MUST HALT and surface to parent on any attempted Write
  under `reports/**` (I9 raw-artifact immutability — see
  `.claude/agents/writer-thesis.md:77-83`).
- `reviewer-adversarial` produces chat output in Mode A/C; for Category F
  plans the critique must also be persisted to
  `planning/current_plan.critique.md` per `planning/README.md:11-13`.
- The `reviewer` agent does not have a dedicated cross-section consistency
  mode; Step 5.5 uses it opportunistically or is performed by the user.

## 2. Plan/execute flow for Category F

Thesis chapters are Category F. They use the same `planning/current_plan.md`
+ `planning/current_plan.critique.md` lifecycle as every other category,
documented in `planning/README.md`. Do NOT invent parallel infrastructure.
DAG files and spec files were decommissioned (CHANGELOG v3.13.0); do not
reintroduce them.

Category F plan fields are mandatory per
`docs/templates/planner_output_contract.md:39`:
Scope, Problem Statement, Assumptions & unknowns, Literature context,
Execution Steps, File Manifest, Gate Condition, Out of scope, Open questions.

Field-to-section mapping for thesis plans:

| Plan field | Literature section uses | Data-fed section uses |
|---|---|---|
| `source_artifacts` | THESIS_STRUCTURE.md, author-style-brief-pl.md, scientific-invariants.md, prior chapter drafts (meta-documents) | Report artifact paths under `reports/<dataset>/artifacts/`, research_log entries, STEP_STATUS.yaml |
| `invariants_touched` | Usually `[]`; populate if a methodological claim touches an invariant | Populate from the feeding Phase's invariants |
| `Literature context` section | Seed bibliography (5-10 key refs per section), structural principle | Feeding artifact paths, prior research log context |
| `Execution Steps T01, T02, …` | One task per section (or one task per parallel batch). Task body includes "must cite", "must contrast" lists. | One task per section. Task body includes "must justify", "must contrast", "must cite" lists. |

The "seed bibliography / structural principle / must cite / must contrast /
must justify" vocabulary lives INSIDE `Literature context` and each task's
`Instructions:` block. It does NOT require a schema change to the plan
template.

## 3. The six-step flow

The steps map 1:1 onto the standard plan/execute workflow. Gate 0 and
Gate 0.5 are one-time calibration gates that precede the first production
run; they are not re-run per chapter.

| Step | Agent | Artifact produced |
|---|---|---|
| Gate 0 | writer-thesis | thesis/chapters/01_introduction.md (§1.1) |
| Gate 0.5 | writer-thesis | thesis/chapters/02_theoretical_background.md (§2.5) |
| 1. Plan | planner-science | planning/current_plan.md (category: F) |
| 2. Critique plan | reviewer-adversarial | planning/current_plan.critique.md |
| 3. Approve | user | (decision recorded in chat; revise plan if needed) |
| 4. Draft | writer-thesis | thesis/chapters/NN_*.md, updated WRITING_STATUS.md, REVIEW_QUEUE.md entry |
| 5. Critique draft | reviewer-adversarial | chat output (Mode C) |
| 5.5. Consistency (per-chapter) | reviewer OR user | chat output or direct edits |
| 6. Pass 2 handoff | user → Claude Chat | Resolution of [REVIEW:]/[NEEDS CITATION] flags; REVIEW_QUEUE.md moves to Completed |

## 4. Gate 0 — voice calibration

Mandatory, one-time, before any parallel scaling.

Dispatch writer-thesis to draft §1.1 (Background and motivation). This
IS a real draft — if it passes, §1.1 is DRAFTED.

Copy-pasteable dispatch:

```
@writer-thesis draft §1.1 (Background and motivation) as a Gate 0 voice
calibration.

This is a literature section. Follow the literature variant from
.claude/rules/thesis-writing.md (Pass 1 steps 1-10).

Section scope: see thesis/THESIS_STRUCTURE.md §1.1.

Target: ~2 pages of Polish academic prose. Primary voice calibration
per .claude/author-style-brief-pl.md lines 70-82.

After drafting:
- Append ## References at end of chapter file
- Update thesis/WRITING_STATUS.md → DRAFTED
- Update thesis/chapters/REVIEW_QUEUE.md (Pending row)
- Produce Chat Handoff Summary (format in .claude/rules/thesis-writing.md)
```

Evaluation (ALL four must pass — see author-style-brief-pl.md:72-82):
1. Register: Polish academic CS prose, not translated from English.
2. Argumentative structure present, not purely descriptive.
3. Hedging in appropriate places; uses Polish hedging idioms.
4. Citations present; no Wikipedia; primary sources.

Failure → diagnose per style brief lines 74-82. Do not scale.

## 5. Gate 0.5 — literature calibration

Mandatory, one-time, after Gate 0. Gate 0 tests voice on a framing
section. Gate 0.5 tests depth on a substantive literature section.

Dispatch writer-thesis to draft §2.5 (Player skill rating systems).
This is the literature calibration target because rating systems have
well-known canonical references that make coverage easy to verify.

Copy-pasteable dispatch:

```
@writer-thesis draft §2.5 (Player skill rating systems) as a Gate 0.5
literature calibration.

This is a literature section. Follow the literature variant from
.claude/rules/thesis-writing.md.

Section scope: Elo (Elo 1978), Glicko/Glicko-2 (Glickman 1999, 2001),
TrueSkill (Herbrich et al. 2006), Aligulac SC2 variant. Explain how
derived ratings serve as features in downstream ML models.

Canonical references that MUST appear:
- Elo, A. E. (1978). The Rating of Chessplayers.
- Glickman, M. E. (1999). Applied Statistics, 48(3).
- Glickman, M. E. (2001). J. Applied Statistics, 28(6).
- Herbrich, R., Minka, T., Graepel, T. (2006). TrueSkill. NeurIPS.

Structural requirement: each rating system presented with the same
depth pattern (formulation, assumptions, strengths, weaknesses).

Target: ~3 pages of Polish academic prose.

After drafting: same post-draft steps as Gate 0.
```

Evaluation (ALL four must pass):
1. Citation density ≥ 2 references per page.
2. Canonical coverage: all four canonical refs above, correctly
   characterized.
3. Structural coherence: consistent depth pattern across systems.
4. Critical evaluation: connects rating systems to the thesis
   prediction task, explains why derived ratings serve as ML features.

Failure → diagnose (citation coverage / structural coherence / critical
depth). Fix the seed bibliography or dispatch prompt. Re-draft §2.5
before scaling.

## 6. Standard dispatch sequence per chapter

Once Gate 0 and Gate 0.5 have passed, chapters run through steps 1-6.

### 6.1 Step 1 — plan

Copy-pasteable dispatch (Chapter 3 example; substitute as needed):

```
@planner-science produce a Category F plan for Chapter 3 remaining
draftable literature sections (§3.1 Traditional sports prediction,
§3.2 StarCraft prediction literature, §3.3 MOBA and other esports).

Plan goes to planning/current_plan.md and MUST conform to
docs/templates/plan_template.md and docs/templates/planner_output_contract.md.

Per-section content inside Literature context and Execution Steps:
- Seed bibliography (5-10 refs with author, year, venue, one-line
  contribution)
- Structural principle (chronological / by method family / by game /
  by data richness)
- "Must cite" list
- "Must contrast" list
- Expected length from thesis/THESIS_STRUCTURE.md
- Voice note: "argumentative, not descriptive"

source_artifacts: THESIS_STRUCTURE.md, author-style-brief-pl.md,
scientific-invariants.md, plus any prior chapter drafts constraining
these sections (e.g. 02_theoretical_background.md for Ch 3 references
§2.5 rating systems).

invariants_touched: [] unless a methodological claim in the plan
touches one (justify if so).

Parallel-safety: sections in this chapter are literature-only and
topically disjoint, so all three are parallel-safe. State this
explicitly in the plan so a parallel execute pass is legal.

critique_required: true. Parent will dispatch reviewer-adversarial
to produce planning/current_plan.critique.md before execution.
```

For data-fed sections, replace "seed bibliography / structural principle"
with:
- Feeding artifact paths (absolute repo-relative paths under
  `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/`)
- "Must justify" list — every methodological decision needs an
  alternatives-considered paragraph
- Prior research_log entries that feed the narrative

### 6.2 Step 2 — adversarial critique of plan

```
@reviewer-adversarial produce planning/current_plan.critique.md for the
Category F plan at planning/current_plan.md (Mode A — Plan Review).

In addition to the standard 5-lens review:
- Literature sections: verify the seed bibliography via WebSearch. For
  each entry confirm the paper exists and says what the plan claims.
  Flag any topic with a missing canonical reference.
- Data-fed sections: verify each feeding artifact path exists in the
  repo and supports the claim the plan intends to make.
- Check structural principles match each section's rhetorical purpose.

Output: save to planning/current_plan.critique.md using
docs/templates/plan_critique_template.md. (If producing chat-only Mode A
output, note that persistent critique artifact is still required for
Category F per planning/README.md.)
```

Per `planning/README.md:11-13`, `current_plan.critique.md` is the
authoritative artifact. reviewer-adversarial in Mode A emits chat
output; the orchestrator must persist it to that path.

### 6.3 Step 3 — approval

User reads the critique, decides. If REVISE or REDESIGN verdict:
adjust the plan and re-run Step 2. Proceed only on PROCEED. This is
the only step without a dispatch — it is a human decision.

### 6.4 Step 4 — draft (fresh session recommended)

Copy-pasteable dispatch (Ch 3 parallel example):

```
@writer-thesis draft §3.1 per planning/current_plan.md task T01.

This is a literature section. Follow the 10-step Pass 1 sequence in
.claude/rules/thesis-writing.md (the literature variant). Follow the
Literature Search Protocol in this file (thesis/plans/writing_protocol.md
§9 below). Reconcile actual citations against the plan's seed
bibliography per §10 below.

After drafting:
- Append ## References at end of 03_related_work.md
- Update thesis/WRITING_STATUS.md → DRAFTED
- Update thesis/chapters/REVIEW_QUEUE.md with a Pending row
- Produce the Chat Handoff Summary from .claude/rules/thesis-writing.md
  (literature variant), including:
    - Citation count (total / from seed / self-discovered)
    - Self-discovered references not in plan's seed list
    - Tier 3 citations flagged for Pass 2 verification
```

Parallel dispatch rules (literature and data-fed both):
- Only dispatch parallel instances on sections the plan marks as
  parallel-safe.
- Hard cap: see `thesis/WRITING_STATUS.md` historical evidence — Chapter
  2 was drafted with up to 2 parallel instances without observed voice
  drift; beyond 2 is untested. Treat 2 as the default cap and deviate
  only if Gate 0 calibration has been re-validated since.
- Each instance writes to a distinct chapter file or clearly delineated
  section within one file.
- If one instance fails, sibling outputs are still valid.

### 6.5 Step 5 — adversarial critique of draft

```
@reviewer-adversarial Mode C review of thesis/chapters/03_related_work.md.

Cross-check against planning/current_plan.md seed bibliography and
"must cite" lists. Cross-check against author-style-brief-pl.md for
voice quality (Lens 4 in the agent's 5-lens protocol).

Literature sections — use tiered citation verification:
- Tier 1 (must verify): every reference from the plan's seed
  bibliography. WebSearch to confirm paper exists and draft's
  characterization is accurate.
- Tier 2 (spot check): WebSearch 30-50% of self-discovered references
  in peer-reviewed venues.
- Tier 3 (defer): supplementary references, recent preprints,
  documentation links — flag for Pass 2 verification only.

Data-fed sections — artifact-based verification:
- For each numerical claim, trace to the cited artifact and confirm.
- For each cited paper, WebSearch to verify the citation matches
  what the draft claims.

Output: chat (Mode C). The draft is not re-written — writer-thesis or
user applies the critique.
```

### 6.6 Step 5.5 — chapter consistency pass

Only after all sections in a chapter have passed Step 5. The `reviewer`
agent does not have a bespoke "cross-section consistency" mode — it has
a general thesis-review checklist. Either the user performs this pass
manually OR dispatches reviewer with an explicit cross-section prompt:

```
@reviewer thesis/chapters/03_related_work.md — cross-section consistency
review. This is BEYOND the standard .claude/agents/reviewer.md thesis
checklist; please also explicitly check:

1. Terminology consistency across §3.1–§3.5 (same concepts use same
   terms, e.g. "gradient boosted trees" vs "GBDT" — pick one).
2. No redundant coverage between sections.
3. Structural balance (no section > 2× the length of its siblings
   unless content density justifies it).
4. Cross-references between sections are accurate.
5. Voice consistency across sections drafted in parallel (Polish
   hedging register, argumentative cadence, citation density).
```

For short chapters or ≤2 drafted sections, manual inspection is more
efficient than the dispatch.

### 6.7 Step 6 — Pass 2 handoff to Claude Chat

User takes to claude.ai:
- The drafted chapter file.
- The Chat Handoff Summary from Step 4 output.
- The adversarial critique from Step 5 (and 5.5 if used).
- The list of Tier 3 citations flagged for verification.
- For data-fed sections: the feeding artifacts in the "Key artifacts"
  column of REVIEW_QUEUE.md.

Chat does:
- Verify Tier 3 citations (papers writer-thesis could not verify
  alone).
- Resolve `[REVIEW:]` flags (literature validation, methodology
  alignment).
- Resolve `[NEEDS CITATION]` flags (Chat searches the literature).
- Resolve `[UNVERIFIED:]` flags (trace to authoritative source).
- Cross-check statistical interpretation.

Move the section from Pending to Completed in REVIEW_QUEUE.md when
Pass 2 is resolved.

## 7. Parallelism map for current DRAFTABLE work

As of 2026-04-18 most sections are DRAFTED (see WRITING_STATUS.md).
The remaining work is primarily post-Phase revision and §1.5, §4.4.4,
§6.5, §7.3, §4.2.4+. When drafting new sections or revising existing
ones, apply these dependency rules:

- Any section not yet drafted: check its `Feeds from:` column in
  WRITING_STATUS.md. If a specific Phase is listed, confirm the
  referenced STEP_STATUS is `complete` before moving from BLOCKED
  to DRAFTABLE.
- Synthesis sections (§1.5, §3.5, §6.x, §7.x) depend on all their
  upstream sections existing as at least DRAFTED.
- Chapter-internal parallelism is permitted when the plan marks
  specific sections as parallel-safe. As-is, sections that survey
  disjoint topics (e.g. Ch 2 §2.1 / §2.4 / §2.6 / Ch 3 §3.1 / §3.2 /
  §3.3) are parallel-safe.

## 8. Critical Review Checklists

See `.claude/rules/thesis-writing.md` — the Data variant and Literature
variant checklists are the authoritative versions. writer-thesis runs
the appropriate variant at Pass 1 step 5 (data) / step 5 (literature)
before DRAFTED. Do not duplicate those checklists here; if they drift
from this file, fix thesis-writing.md.

## 9. Literature Search Protocol

Applies to writer-thesis when drafting any section that cites papers
(literature sections always, data-fed sections for their literature
portions).

1. Start from the plan's seed bibliography. WebSearch each reference
   before using it — do not cite a paper you could not retrieve or
   verify.
2. Discover additional references via minimum 3 WebSearch queries per
   section, each with a distinct formulation (e.g. for §2.6:
   "classifier comparison binary classification statistical test",
   "Friedman test Holm correction multiple classifiers", "Brier score
   decomposition Murphy probabilistic forecasting").
3. Preferred sources, in order:
   - Conference proceedings: NeurIPS, ICML, AAAI, IJCAI, IEEE CIG/CoG,
     KDD, WWW, AIIDE.
   - Journals: JMLR, IEEE Trans. Games, Machine Learning (Springer),
     PLOS ONE, Entropy.
   - Canonical textbooks: Bishop (2006), Hastie et al. (2009), Murphy
     (2012/2022), Goodfellow et al. (2016).
   - Dataset papers: Scientific Data, data descriptor venues.
   - Official documentation: game engine, API, protocol specs.
4. Non-peer-reviewed sources are permitted only when no peer-reviewed
   alternative exists. Tag with `[REVIEW: grey-literature — <url>]`.
   Wikipedia is never cited in final prose; use it only to discover
   primary sources.
5. Citation density target: 2-4 references per page. Literature
   surveys (Ch 2-3) at the higher end; framing sections (Ch 1) at the
   lower end.
6. WebSearch failure handling:
   - If a search returns nothing relevant, widen the query (remove
     specific terms) and try again.
   - If two widened queries both return nothing, plant
     `[NEEDS CITATION]` in the draft with a parenthetical note of the
     queries attempted. Do NOT invent a citation.
   - If WebSearch fails for infrastructure reasons (rate limit, error),
     plant `[UNVERIFIED: WebSearch unavailable]` and continue.
   - Pass 2 in Claude Chat resolves all NEEDS CITATION / UNVERIFIED
     flags.

## 10. Citation reconciliation at draft time

Literature sections — tiered reconciliation:
- Every seed-bibliography reference in the plan should appear in the
  draft OR the draft's Chat Handoff Summary must explain why it was
  dropped.
- Self-discovered references are not individually flagged at draft
  time; they are grouped in the Chat Handoff Summary's "Self-discovered
  references not in plan" list for Step 5 tiered verification.

Data-fed sections — strict reconciliation:
- Every planned "must cite" entry must appear or be explained.
- Every self-discovered citation must be listed in the Chat Handoff
  Summary so the Step 5 adversarial critique can verify it.

## 11. Bibliographic output format

writer-thesis uses `[AuthorYear]` inline keys (e.g. `[Glickman2001]`,
`[DemsarHerrera2006]`). Keys are added to `thesis/references.bib`
(plan-authorized Write scope per writer-thesis agent) at draft time.
At the end of each chapter file, writer-thesis appends a `## References`
section mirroring the chapter's cited entries in human-readable form
for review convenience:

```
## References

- [Elo1978] Elo, A. E. (1978). The Rating of Chessplayers, Past and
  Present. Arco.
- [Glickman2001] Glickman, M. E. (2001). Dynamic paired comparison
  models with stochastic variances. J. Applied Statistics, 28(6),
  673-689.
```

Do NOT ask writer-thesis to hand-maintain BibTeX syntax during
drafting — it breaks flow and the markdown review pass cannot
validate it. Mechanical consolidation of chapter-level `## References`
into `thesis/references.bib` happens as a separate chore.

## 12. Flag lifecycle

Four flag types, defined in `.claude/rules/thesis-writing.md`
(section "Inline Flag Types"):

| Flag | Planted by | Cleared by |
|---|---|---|
| `[REVIEW: <concern>]` | writer-thesis | Pass 2 (Claude Chat) |
| `[UNVERIFIED: source?]` | writer-thesis | Pass 2 (Claude Chat) |
| `[NEEDS JUSTIFICATION]` | writer-thesis | Pass 2 or re-dispatched writer-thesis |
| `[NEEDS CITATION]` | writer-thesis | Pass 2 (Claude Chat finds the citation) |

writer-thesis logs flag counts in the Chat Handoff Summary. The
REVIEW_QUEUE.md Pending row mirrors these counts and the `Pass 2
status` column tracks resolution. Move to Completed once the Pass 2
questions have explicit answers applied to the draft.

## 13. Error and recovery cases

- **writer-thesis fails mid-draft:** The chapter file may have partial
  content. User inspects, decides whether to re-dispatch or revert.
  Completed sibling sections (from parallel dispatch) are unaffected.
- **Adversarial critique returns BLOCKER:** Revise the draft (manually
  or by re-dispatching writer-thesis with the critique findings) before
  Pass 2. If the blocker is in the plan itself, revise the plan and
  re-run Step 2.
- **Gate 0 fails:** Diagnose per author-style-brief-pl.md:74-82. Do not
  scale.
- **Gate 0.5 fails:** Diagnose whether the issue is citation coverage,
  structural coherence, or critical depth. Adjust the Literature Search
  Protocol or seed bibliography guidance. Re-draft §2.5 before scaling.
- **Citation reconciliation gap:** writer-thesis noted a planned
  citation it could not use, or used a citation not in the plan.
  Adversarial critique in Step 5 verifies the substitution or the
  omission.
- **Step 5.5 finds drift:** Minor terminology drift — user edits
  directly. Structural drift — re-dispatch writer-thesis on the
  offending section with explicit sibling-section references.
- **WRITING_STATUS.md disagrees with parallelism intent:** The plan's
  `File Manifest` is authoritative for what this PR writes. Update
  WRITING_STATUS.md in the same PR. Do not leave the status row stale.
- **Phase dependency changes mid-draft:** If a data-fed section's
  feeding artifacts are invalidated (a Phase step is re-run, a cleaning
  rule changes), mark the section `REVISED` in WRITING_STATUS.md and
  re-plan. Do not silently update the draft without a plan revision.

## 14. Session architecture

```
Session A (Phase work — category A)     Session B (Thesis — category F)
---------------------------------       --------------------------------
                                         Gate 0: draft §1.1
                                         Gate 0.5: draft §2.5
Phase 01 Step 01_04_03, ...                    │
  artifacts to reports/<dataset>/              ↓
  research_log.md entry                   Step 1: @planner-science plan
         │                                Step 2: @reviewer-adversarial
         │                                Step 3: user approves
         │                                Step 4: @writer-thesis draft
         ↓                                Step 5: @reviewer-adversarial
  Report artifacts available <─────────   Step 5.5: @reviewer (optional)
  as inputs for data-fed thesis           Step 6: user → Claude Chat
  sections (§4.1.x, §4.2.x, §5.x)               │
                                                ↓
                                         Next section / chapter plan
```

Sessions are independent. ML experiments produce artifacts in
`reports/`; thesis writing reads those artifacts. No shared state
beyond the filesystem and git.

## 15. References to authoritative files

Do not duplicate content from these files — reference them:

- `.claude/rules/thesis-writing.md` — the contract. Pass 1 step
  sequences, Critical Review Checklists, flag types, Chat Handoff
  Summary format.
- `.claude/author-style-brief-pl.md` — the voice model. Gate 0
  evaluation criteria.
- `.claude/scientific-invariants.md` — the 9 invariants. Referenced
  by writer-thesis constraints.
- `docs/templates/plan_template.md` — the Category F plan frontmatter
  and section skeleton.
- `docs/templates/planner_output_contract.md` — required plan sections
  and self-check.
- `planning/README.md` — plan/execute lifecycle and purge protocol.
- `thesis/THESIS_STRUCTURE.md` — per-section scope and feeds-from
  mapping.
- `thesis/WRITING_STATUS.md` — live state of every section.
- `thesis/chapters/REVIEW_QUEUE.md` — Pass 1 → Pass 2 handoff register.
- `docs/PHASES.md` — canonical 7-phase list; Phase 07 semantics for
  thesis-gate.
- `docs/agents/AGENT_MANUAL.md` — agent routing cheat sheet.
