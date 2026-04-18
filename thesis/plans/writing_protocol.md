# Thesis Writing Protocol

Operator's guide to drafting thesis chapters using the plan/execute
workflow and Claude Code subagents. The contract is
`.claude/rules/thesis-writing.md` (auto-loaded on `thesis/**/*` path
touch) — this document is the operational "how." The rule file takes
precedence in any conflict.

Revised: 2026-04-18. Supersedes `thesis/plans/idea_audit.md`,
`thesis/plans/idea_audit_review.md`, and `thesis/plans/writing_manual.md`.

## 0. Scope and section types

The thesis contains three kinds of draftable section, distinguished by
the `Feeds from:` column in `thesis/WRITING_STATUS.md`.

| Type | `Feeds from:` values | Source material | Examples |
|---|---|---|---|
| **Literature** | `—` (em dash) OR a literature tag (e.g. `AoE2 lit review`) | Papers, textbooks, domain knowledge. No report artifacts. | §1.1–§1.4, §2.1, §2.4–§2.6, §3.1–§3.4, §4.4.4, §6.5, §7.3 |
| **Data-fed** | A specific Phase + Step range | Report artifacts under `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/...` plus `research_log.md` entries | §4.1.x, §4.2.x, §5.x |
| **Synthesis** | Other sections (e.g. `§3.1-§3.4`) | The sibling draft content itself, read as source material | §1.5, §3.5, §6.1–§6.4, §7.1–§7.2 |

Mixed sections (see §2.2, §2.3 in WRITING_STATUS.md) combine a Literature
half with a Data-fed half. The "must cite / must justify / must contrast"
layering is additive, not exclusive.

**DRAFTABLE triggers:**
- Literature: any time Gate 0 and Gate 0.5 have passed (both PASSED — see
  §4, §5).
- Data-fed: every referenced Step is `complete` in the active dataset's
  `STEP_STATUS.yaml`.
- Synthesis: every upstream section it references exists as at least
  `DRAFTED`.

## 1. Agent capability matrix

Source of truth: `.claude/agents/<agent>.md` frontmatter. Any discrepancy
between this table and the agent files is a bug here — fix here, not
there.

| Agent | model | effort | permissionMode | tools | disallowedTools | Used for |
|---|---|---|---|---|---|---|
| `planner-science` | opus | max | plan | Read, Grep, Glob, Bash, TodoWrite | — | Step 1 (plan) |
| `writer-thesis` | opus | max | (not declared) | Read, Grep, Glob, Write, Edit, WebFetch, WebSearch | — | Gate 0, Gate 0.5, Step 4 (draft) |
| `reviewer-adversarial` | opus | max | plan | Read, Grep, Glob, Bash, WebFetch, WebSearch | Write, Edit | Step 2 (plan critique), Step 5 (draft critique) |
| `reviewer` | sonnet | high | (not declared) | Read, Grep, Glob, Bash | — | Step 5.5 (cross-section consistency) |
| `executor` | sonnet | high | (not declared) | Read, Write, Edit, Grep, Glob, Bash, TodoWrite | — | Not used for thesis drafting |

Load-bearing non-obvious constraints:
- `writer-thesis` Write/Edit scope is an **allowlist**: `thesis/`,
  `planning/`, `temp/`, plus (when the plan explicitly authorizes)
  `thesis/pass2_evidence/`, `thesis/references.bib`, and
  `thesis/WRITING_STATUS.md`. Any attempted Write under `reports/**`
  MUST HALT and surface to the parent (invariant I9 — raw artifact
  immutability; see `.claude/agents/writer-thesis.md:77-83`).
- `reviewer-adversarial`'s `disallowedTools: Write, Edit` is enforced at
  the platform layer. Dispatch prompts that ask it to "save to …" will
  be rejected; always instruct it to emit chat output and name the
  parent session as the persistence mechanism.
- `reviewer` in cross-section consistency mode (Step 5.5) supplements
  the standard thesis checklist with 5 additional checks — see
  `.claude/agents/reviewer.md` ("For thesis chapters — cross-section
  consistency mode").

## 2. Plan/execute flow for Category F

Thesis chapters are Category F. They use the same `planning/current_plan.md`
+ `planning/current_plan.critique.md` lifecycle as every other category
(see `planning/README.md`). Do NOT invent parallel infrastructure. DAG
files and spec files were decommissioned in CHANGELOG v3.13.0; do not
reintroduce them.

Category F plans require the sections named in
`docs/templates/planner_output_contract.md:39`: Scope, Problem Statement,
Assumptions & unknowns, Literature context, Execution Steps, File
Manifest, Gate Condition, Out of scope, Open questions.

Field-to-content mapping for thesis plans:

| Plan section | Literature / Synthesis sections use | Data-fed sections use |
|---|---|---|
| `source_artifacts` frontmatter | THESIS_STRUCTURE.md, author-style-brief-pl.md, scientific-invariants.md, prior chapter drafts that constrain content | Report artifact paths under `reports/<dataset>/artifacts/`, research_log entries, STEP_STATUS.yaml |
| `invariants_touched` frontmatter | Usually `[]`; populate only if a methodological claim touches an invariant | Populate from the feeding Phase's invariants |
| `Literature context` prose | Seed bibliography + structural principle, grouped per section (see placement rule below) | Feeding artifact paths + prior research log context |
| `Execution Steps` (T01, T02, …) | One task per section (or one per parallel batch); `Instructions:` block lists "must cite" and "must contrast" per task | One task per section; `Instructions:` block lists "must justify", "must contrast", "must cite" |

**Seed-bibliography placement rule (resolves a common planner ambiguity):**
when a single plan covers multiple sections (e.g. Chapter 3 §3.1–§3.3),
put seed bibliography under `Literature context` as one consolidated
sub-block per section (`### Seed bibliography — §3.1`,
`### Seed bibliography — §3.2`, …). The per-task "must cite / must
contrast / must justify" lists stay inside each task's `Instructions:`
block, because those are task-scoped execution constraints that vary
per section.

## 3. Full flow overview

The per-chapter work is six steps (1 → 6). Gate 0 and Gate 0.5 are
one-time calibration events that precede the first production run; they
are not re-run per chapter. Both have already PASSED — see §4 and §5.

| Stage | Agent | Artifact |
|---|---|---|
| Gate 0 (one-time; PASSED 2026-04-13) | writer-thesis | `thesis/chapters/01_introduction.md` §1.1 |
| Gate 0.5 (one-time; PASSED 2026-04-17) | writer-thesis | `thesis/chapters/02_theoretical_background.md` §2.5 |
| 1. Plan | planner-science | `planning/current_plan.md` (category: F) |
| 2. Critique plan | reviewer-adversarial | `planning/current_plan.critique.md` (parent-persisted; see §6.2) |
| 3. Approve | user | (decision; revise plan if needed) |
| 4. Draft | writer-thesis | `thesis/chapters/NN_*.md`, updated WRITING_STATUS.md, REVIEW_QUEUE.md Pending row |
| 5. Critique draft | reviewer-adversarial | chat output (Mode C; not auto-persisted — see note) |
| 5.5. Consistency (per-chapter) | reviewer OR user | chat output or direct edits |
| 6. Pass 2 handoff | user → Claude Chat | Flag resolution; REVIEW_QUEUE.md moves to Completed |

Why Step 2 is persisted and Step 5 is chat-only: Category F plans
require `current_plan.critique.md` as on-branch provenance per
`planning/README.md:11-13`. Draft critiques are consumed immediately by
the user or fed back to writer-thesis for revision; they live in chat
and only need a file if cited in Pass 2.

## 4. Gate 0 — voice calibration

**Status: PASSED on 2026-04-13.** Draft §1.1 (Background and motivation)
accepted against the four evaluation criteria below. `WRITING_STATUS.md`
records §1.1 as `DRAFTED`. Do NOT re-dispatch — a new run would overwrite
the accepted draft.

Re-run triggers (all three would motivate a fresh Gate 0):
1. `.claude/author-style-brief-pl.md` is updated in a way that changes
   voice expectations.
2. `.claude/agents/writer-thesis.md` frontmatter changes materially
   (different tools, different model).
3. An adversarial review rejects a production draft on voice grounds.

Runbook (archived for re-run scenarios):

```
@writer-thesis draft §1.1 (Background and motivation) as a Gate 0 voice
calibration re-run.

This is a literature section. Follow the literature variant from
.claude/rules/thesis-writing.md (Pass 1 steps 1–10).

Section scope: see thesis/THESIS_STRUCTURE.md §1.1.

Target: ~2 pages of Polish academic prose. Primary voice calibration
per .claude/author-style-brief-pl.md lines 70–82.

After drafting:
- Append ## References at end of chapter file
- Update thesis/WRITING_STATUS.md → DRAFTED
- Update thesis/chapters/REVIEW_QUEUE.md with a Pending row
- Produce the Chat Handoff Summary from .claude/rules/thesis-writing.md
```

Evaluation (ALL four must pass — see author-style-brief-pl.md:72–82):
1. Register: Polish academic CS prose, not translated from English.
2. Argumentative structure, not purely descriptive.
3. Hedging in appropriate places; uses Polish hedging idioms.
4. Citations present; no Wikipedia; primary sources.

Failure → diagnose per style-brief lines 74–82. Do not scale.

## 5. Gate 0.5 — literature calibration

**Status: PASSED_FOR_PRODUCTION_SCALING on 2026-04-17.** Draft §2.5
(Player skill rating systems) accepted against the four criteria below.
`WRITING_STATUS.md` records §2.5 as `DRAFTED`. Do NOT re-dispatch under
ordinary circumstances.

Re-run triggers: same three conditions as Gate 0, plus (4) a shift in
the canonical rating-system reference set that would motivate a new
depth calibration target.

Runbook (archived):

```
@writer-thesis draft §2.5 (Player skill rating systems) as a Gate 0.5
literature calibration re-run.

This is a literature section. Follow the literature variant from
.claude/rules/thesis-writing.md. Apply the Literature Search Protocol
(in the rule file).

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
2. Canonical coverage: all four canonical refs, correctly characterized.
3. Structural coherence: consistent depth pattern across systems.
4. Critical evaluation: connects rating systems to the thesis
   prediction task; explains why derived ratings serve as ML features.

Failure → diagnose (citation coverage / structural coherence / critical
depth). Fix the seed bibliography or dispatch prompt. Re-draft §2.5
before scaling.

## 6. Standard dispatch sequence per chapter

With Gates 0/0.5 PASSED, every new chapter runs through Steps 1–6.

### 6.1 Step 1 — plan

Copy-pasteable dispatch (Chapter 3 example; substitute as needed):

```
@planner-science produce a Category F plan for Chapter 3 remaining
draftable literature sections (§3.1 Traditional sports prediction,
§3.2 StarCraft prediction literature, §3.3 MOBA and other esports).

Plan goes to planning/current_plan.md and MUST conform to
docs/templates/plan_template.md + docs/templates/planner_output_contract.md.

Per-section content:
- Inside Literature context: one `### Seed bibliography — §X.Y` block
  per section (5–10 refs each with author/year/venue and one-line
  contribution); one `### Structural principle — §X.Y` note
  (chronological / by method family / by game / by data richness).
- Inside each task's Instructions block: "must cite", "must contrast",
  expected length (from thesis/THESIS_STRUCTURE.md), voice note
  ("argumentative, not descriptive").

source_artifacts: THESIS_STRUCTURE.md, author-style-brief-pl.md,
scientific-invariants.md, plus any prior chapter drafts constraining
these sections (e.g. 02_theoretical_background.md §2.5 for Ch 3).

invariants_touched: [] unless a methodological claim in the plan
touches one (justify if so).

Parallel-safety: these sections are literature-only and topically
disjoint, so all three are parallel-safe. State this explicitly in
the plan so a parallel execute pass is legal.

critique_required: true. Parent will dispatch reviewer-adversarial
to produce planning/current_plan.critique.md before execution.
```

For data-fed sections, replace "seed bibliography / structural principle"
with:
- Feeding artifact paths (absolute repo-relative paths under
  `src/rts_predict/games/<game>/datasets/<dataset>/reports/artifacts/`).
- "Must justify" list — every methodological decision needs an
  alternatives-considered paragraph.
- Prior research_log entries that feed the narrative.

For synthesis sections (e.g. §3.5, §6.1), replace with:
- Upstream section list (`§3.1`, `§3.2`, …) with the specific claim
  each contributes to the synthesis.
- "Must integrate" list — which sibling claims must appear tied
  together.

### 6.2 Step 2 — adversarial critique of plan

reviewer-adversarial has `disallowedTools: Write, Edit`; it cannot
write files. It produces chat output. The parent session copies that
output to `planning/current_plan.critique.md` using the Write tool (or
via an executor dispatch) so the artifact exists on-branch as
provenance per `planning/README.md:11-13`.

Copy-pasteable dispatch:

```
@reviewer-adversarial Mode A — Plan Review of planning/current_plan.md.

Produce critique as chat output using docs/templates/plan_critique_template.md
as the structural schema. The parent session will persist your output
to planning/current_plan.critique.md (you cannot write it yourself due
to disallowedTools: Write, Edit).

In addition to the standard 5-lens review:
- Literature sections: verify the seed bibliography via WebSearch. For
  each entry confirm the paper exists and says what the plan claims.
  Flag any topic with a missing canonical reference.
- Data-fed sections: verify each feeding artifact path exists in the
  repo and supports the claim the plan intends to make.
- Synthesis sections: verify every upstream section reference is
  DRAFTED and the claim each contributes is actually present in that
  draft.
- Check structural principles match each section's rhetorical purpose.
```

### 6.3 Step 3 — approval

User reads the critique, decides. REVISE or REDESIGN verdict → adjust
plan, re-run Step 2. Proceed only on PROCEED. No dispatch — this is a
human decision.

### 6.4 Step 4 — draft (fresh session recommended)

Copy-pasteable dispatch (Ch 3 parallel example):

```
@writer-thesis draft §3.1 per planning/current_plan.md task T01.

This is a literature section. Follow the 10-step Pass 1 sequence in
.claude/rules/thesis-writing.md (Literature variant), including the
Literature Search Protocol in that file.

Reconcile actual citations against the plan's seed bibliography per §7
of thesis/plans/writing_protocol.md.

After drafting:
- Append ## References at end of 03_related_work.md
- Update thesis/WRITING_STATUS.md → DRAFTED
- Update thesis/chapters/REVIEW_QUEUE.md with a Pending row
- Produce the Chat Handoff Summary from .claude/rules/thesis-writing.md
  (literature variant), including:
    - Citation count (total / from seed / self-discovered)
    - Self-discovered references not in the plan's seed list
    - Tier 3 citations flagged for Pass 2 verification
```

Parallel dispatch rules (literature, synthesis, and data-fed alike):
- Only dispatch parallel instances on sections the plan marks as
  parallel-safe.
- Observed maximum without voice drift: 4 instances (NIGHT_SUMMARY
  2026-04-17 Sprint 5-extended: §2.4 / §2.6 / §3.1 / §3.3). Default
  cap is **4**; do not exceed without re-validating Gate 0.
- Each instance writes to a distinct chapter file or clearly delineated
  section within one file.
- If one instance fails, sibling outputs are still valid.

### 6.5 Step 5 — adversarial critique of draft

```
@reviewer-adversarial Mode C review of thesis/chapters/03_related_work.md.

Cross-check against planning/current_plan.md seed bibliography and
"must cite" lists. Cross-check against author-style-brief-pl.md for
voice quality (Lens 4 in the agent's 5-lens protocol).

Literature sections — tiered citation verification:
- Tier 1 (must verify): every reference from the plan's seed
  bibliography. WebSearch to confirm paper exists and draft's
  characterization is accurate.
- Tier 2 (spot check): WebSearch 30–50% of self-discovered references
  in peer-reviewed venues.
- Tier 3 (defer): supplementary references, recent preprints,
  documentation links — flag for Pass 2 verification.

Data-fed sections — artifact-based verification:
- For each numerical claim, trace to the cited artifact and confirm.
- For each cited paper, WebSearch to verify the citation matches
  what the draft claims.

Output: chat (Mode C). The draft is not re-written — writer-thesis or
user applies the critique.
```

### 6.6 Step 5.5 — chapter consistency pass

Runs only after every section in a chapter has passed Step 5. Dispatch
`reviewer` in cross-section consistency mode (now a first-class mode on
`.claude/agents/reviewer.md`):

```
@reviewer thesis/chapters/03_related_work.md — cross-section consistency
mode. Run both the standard thesis checklist AND the 5 cross-section
checks under "For thesis chapters — cross-section consistency mode"
in .claude/agents/reviewer.md.
```

For short chapters or ≤2 drafted sections, manual inspection is more
efficient than a dispatch.

### 6.7 Step 6 — Pass 2 handoff to Claude Chat

User takes to claude.ai:
- The drafted chapter file.
- The Chat Handoff Summary from Step 4.
- The Step 5 (and 5.5 if used) critique(s).
- The Tier 3 citations list flagged for verification.
- For data-fed sections: the feeding artifacts in REVIEW_QUEUE.md's
  "Key artifacts" column.

Chat resolves `[REVIEW:]`, `[NEEDS CITATION]`, `[UNVERIFIED:]`, and
`[NEEDS JUSTIFICATION]` flags; verifies Tier 3 citations; cross-checks
statistical interpretation. Move the section from Pending to Completed
in REVIEW_QUEUE.md when Pass 2 is resolved.

## 7. Citation reconciliation at draft time

Literature / synthesis sections — tiered reconciliation:
- Every seed-bibliography reference in the plan should appear in the
  draft OR the Chat Handoff Summary must explain why it was dropped.
- Self-discovered references are grouped in the Chat Handoff Summary's
  "Self-discovered references not in plan" list for Step 5 tiered
  verification.

Data-fed sections — strict reconciliation:
- Every planned "must cite" entry must appear or be explained.
- Every self-discovered citation must be listed in the Chat Handoff
  Summary so the Step 5 adversarial critique can verify it.

## 8. Parallelism map for current work

As of 2026-04-18 most DRAFTABLE sections are already `DRAFTED` (see
`thesis/WRITING_STATUS.md`). Remaining drafts: synthesis sections
depending on their upstream siblings, §1.5, §4.4.4, §6.5, §7.3,
§4.2.4+. Dependency rules:

- Before moving any section from `BLOCKED` to `DRAFTABLE`, confirm its
  `Feeds from:` entry is satisfied (Phase STEP_STATUS `complete` for
  data-fed; all upstream sections ≥ `DRAFTED` for synthesis).
- Chapter-internal parallelism is permitted when the plan marks sections
  as parallel-safe. Sections that survey topically disjoint material
  (e.g. Ch 2 §2.1 / §2.4 / §2.6, Ch 3 §3.1 / §3.2 / §3.3) are
  parallel-safe; synthesis sections are not (their upstream must exist).

## 9. Critical Review Checklists and Literature Search Protocol

See `.claude/rules/thesis-writing.md`. The rule file is auto-loaded on
any `thesis/**/*` path touch; it owns both Critical Review Checklist
variants (Data and Literature) and the Literature Search Protocol
(including WebSearch-failure handling). Do not duplicate that content
here — if it drifts, fix the rule file.

## 10. Bibliographic output format

writer-thesis uses `[AuthorYear]` inline keys (e.g. `[Glickman2001]`,
`[DemsarHerrera2006]`) per `.claude/rules/thesis-writing.md`
("Writing Quality" section). Keys are added to `thesis/references.bib`
(plan-authorized Write scope) at draft time. At the end of each chapter
file, writer-thesis appends a `## References` section mirroring the
chapter's cited entries as human-readable text for review convenience.

BibTeX syntax is NOT hand-maintained during drafting — consolidation of
chapter-level `## References` into `thesis/references.bib` is a
separate mechanical chore.

Advisory reference: `docs/thesis/THESIS_WRITING_MANUAL.md` (cited from
`.claude/author-style-brief-pl.md:24`) is a general thesis-writing
advisory, not a citation-format specification. The `[AuthorYear]`
convention above remains authoritative.

## 11. Flag lifecycle

Flag types are defined in `.claude/rules/thesis-writing.md` ("Inline
Flag Types"). Lifecycle:

| Flag | Planted by | Cleared by |
|---|---|---|
| `[REVIEW: <concern>]` | writer-thesis | Pass 2 (Claude Chat) |
| `[UNVERIFIED: source?]` | writer-thesis | Pass 2 (Claude Chat) |
| `[NEEDS JUSTIFICATION]` | writer-thesis | Pass 2 or a re-dispatched writer-thesis |
| `[NEEDS CITATION]` | writer-thesis | Pass 2 (Chat finds the citation) |

writer-thesis logs flag counts in the Chat Handoff Summary. The
REVIEW_QUEUE.md Pending row mirrors these counts; its `Pass 2 status`
column tracks resolution. Move to Completed once Pass 2 questions have
explicit answers applied to the draft.

## 12. Error and recovery cases

- **writer-thesis fails mid-draft:** Chapter file may have partial
  content. User inspects, decides whether to re-dispatch or revert.
  Completed sibling sections (from parallel dispatch) are unaffected.
- **Adversarial critique returns BLOCKER:** Revise the draft (manually
  or via a re-dispatched writer-thesis) before Pass 2. If the blocker
  lives in the plan, revise and re-run Step 2.
- **Gate 0 / Gate 0.5 fails on a re-run:** diagnose per their §4 / §5
  runbooks; do not scale further writing until the failing gate passes
  again.
- **Citation reconciliation gap:** writer-thesis noted a planned
  citation it could not use, or used one not in the plan. Step 5
  adversarial critique verifies the substitution or the omission.
- **Step 5.5 finds drift:** minor terminology drift — user edits
  directly. Structural drift — re-dispatch writer-thesis on the
  offending section with explicit sibling-section references.
- **WRITING_STATUS.md disagrees with the plan:** the plan's
  `File Manifest` is authoritative for the PR. Update WRITING_STATUS.md
  in the same PR; do not leave the status row stale.
- **Phase dependency changes mid-draft:** if a data-fed section's
  feeding artifacts are invalidated (a Phase step re-runs, a cleaning
  rule changes), mark the section `REVISED` in WRITING_STATUS.md and
  re-plan. Do not silently update the draft without a plan revision.

## 13. Session architecture

Category A sessions (Phase work) produce report artifacts under
`src/rts_predict/games/<game>/datasets/<dataset>/reports/`. Category F
sessions (thesis writing) read those artifacts as inputs for data-fed
thesis sections. Sessions are independent; the only shared state is
the filesystem and git.

## 14. References to authoritative files

Do not duplicate content from these files — reference them:

- `.claude/rules/thesis-writing.md` — Pass 1 step sequences, Critical
  Review Checklists (Data and Literature variants), Literature Search
  Protocol, inline flag types, Chat Handoff Summary format, Writing
  Quality. Auto-loaded on `thesis/**/*` path touch.
- `.claude/author-style-brief-pl.md` — voice model; Gate 0 evaluation
  criteria.
- `.claude/scientific-invariants.md` — the 9 invariants; constrains
  writer-thesis.
- `docs/templates/plan_template.md` — Category F plan frontmatter and
  skeleton.
- `docs/templates/planner_output_contract.md` — required plan sections
  and self-check.
- `docs/templates/plan_critique_template.md` — Step 2 critique schema.
- `planning/README.md` — plan/execute lifecycle; critique persistence
  contract.
- `thesis/THESIS_STRUCTURE.md` — per-section scope and feeds-from
  mapping.
- `thesis/WRITING_STATUS.md` — live status of every section.
- `thesis/chapters/REVIEW_QUEUE.md` — Pass 1 → Pass 2 register.
- `docs/PHASES.md` — canonical 7-phase list.
- `docs/agents/AGENT_MANUAL.md` — agent routing cheat sheet.
