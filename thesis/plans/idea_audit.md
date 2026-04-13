# Thesis Writing Flow — Agent Audit & Protocol

Audited 2026-04-13. Revised after adversarial review (same date).
Revised 2026-04-13: bifurcated for literature vs data-fed sections per
idea_audit_review.md findings.

## Agent Capability Matrix

| Agent | Model | WebFetch | WebSearch | Write/Edit | Role |
|---|---|---|---|---|---|
| planner-science | opus | yes | yes | no | Plans phase/thesis work |
| planner | sonnet | no | no | no | Plans code infra |
| writer-thesis | opus | yes | yes | yes (not reports/) | Drafts thesis prose |
| executor | sonnet | no | no | yes | Implements code/notebooks |
| reviewer-adversarial | opus | yes | yes | no | Scientific methodology adversary |
| reviewer-deep | opus | yes | yes | no | Structural/spec compliance |
| reviewer | sonnet | no | no | no | Lightweight post-change check |
| lookup | haiku | no | no | no | Quick answers |

Key facts:
- writer-thesis has WebFetch/WebSearch — it self-researches during drafting.
- reviewer-adversarial has WebFetch/WebSearch — it independently verifies
  cited claims, creating a natural double-check.
- executor lacks web access — wrong agent for thesis writing.
- Subagent dispatch gives clean context separation natively — no DAG
  infrastructure needed for reviewer isolation.

## Section Types

The protocol distinguishes two section types. Every DRAFTABLE section falls
into exactly one.

**Literature sections** have "Feeds from: —" in WRITING_STATUS.md. Their
source material is papers, textbooks, and domain knowledge. No report
artifacts exist. Examples: §1.1–1.4, §2.1, §2.4–2.6, §3.1–3.3, §4.4.4,
§6.5, §7.3.

**Data-fed sections** have a specific Phase listed in WRITING_STATUS.md.
Their source material includes report artifacts produced by Phase work
(notebooks, STEP_STATUS.yaml, research_log entries). Examples: §4.1.1,
§4.2.1–4.2.3, §5.1.1–5.1.4.

Steps below are labeled `[LIT]` or `[DATA]` where they diverge. Unlabeled
steps apply to both.

## Protocol

### Gate 0 — Voice Calibration (once, before any scaling)

**Mandatory.** Per `author-style-brief-pl.md` (lines 70-82), draft **§1.1
only** first. Evaluate against 4 criteria:

1. Does the register sound like Polish academic CS prose, not translated
   from English?
2. Is argumentative structure present, not purely descriptive?
3. Does hedging appear in appropriate places?
4. Are citations present and from primary sources?

**All four must pass.** If any fails, diagnose whether the problem is in
the style brief, the agent calibration, or the source material. Fix before
proceeding.

### Gate 0.5 — Literature Calibration (once, after Gate 0)

**Mandatory for literature sections.** Draft **§2.5 (Player skill rating
systems)** — a bounded, well-defined literature section with known canonical
references. Evaluate against 4 criteria:

1. **Citation density:** >= 2 references per page
2. **Canonical coverage:** Elo (1978), Glickman (1999, 2001), Herbrich et
   al. (2006) all present and correctly characterized
3. **Structural coherence:** Each rating system presented with the same
   depth pattern (formulation, assumptions, strengths, weaknesses)
4. **Critical evaluation:** Section is argumentative, not just descriptive
   — connects rating systems to the thesis prediction task, explains why
   derived ratings serve as ML features

**All four must pass.** Gate 0.5 catches literature-section-specific risks
that Gate 0 (a framing section) cannot test: citation completeness,
textbook-vs-paper balance, and structural coherence across method families.

Only after both gates pass does the protocol scale to parallel drafting.

### Step 1 — Plan (planner-science subagent)

Dispatch planner-science to produce a Category F plan. The plan uses the
standard infrastructure:

    planning/current_plan.md

with a lightweight DAG (`planning/dags/DAG.yaml`) containing one task group
per parallel section batch.

#### `[LIT]` Literature section plan contents

The plan must include per section:
- **Seed bibliography** — 5-10 key references (author, year, venue, what
  it contributes to this section). This replaces "feeding artifacts."
- **Structural principle** — how the section is organized and why
  (chronological, by method family, by domain). This replaces "must
  justify" (literature sections make no methodological choices).
- **"Must contrast" list** — claims needing comparison with alternative
  views or competing approaches
- **"Must cite" list** — canonical references that must appear (the seed
  bibliography is the starting point; this list may be shorter or identical)
- Expected length from THESIS_STRUCTURE.md
- Voice note: "argumentative, not descriptive"
- `source_artifacts`: list THESIS_STRUCTURE.md, author-style-brief-pl.md,
  scientific-invariants.md, and any prior chapter drafts that constrain
  the current section. These are meta-documents, not data artifacts.

#### `[DATA]` Data-fed section plan contents

The plan must include per section:
- **Feeding artifacts** — paths to report artifacts that supply the data
  (notebooks, STEP_STATUS.yaml, research_log entries)
- **"Must justify" list** — methodological choices needing alternatives-
  considered paragraphs
- **"Must contrast" list** — claims needing literature comparison
- **"Must cite" list** — key references (author, year, finding)
- Expected length from THESIS_STRUCTURE.md
- Voice note: "argumentative, not descriptive"
- Dependencies between sections (which are parallel-safe, which are
  sequential)

### Step 2 — Adversarial review of plan (reviewer-adversarial subagent)

Dispatch reviewer-adversarial with a pointer to the plan file (Mode A —
Plan Review). It reads the plan fresh, challenges methodology framing,
verifies literature claims via WebSearch, flags weak points.

The dispatch prompt must include:
- Path to the plan file
- `[LIT]` "Verify the seed bibliography: for each entry, WebSearch to
  confirm the paper exists and says what the plan claims. Flag any topic
  where the seed bibliography misses a canonical reference."
- `[DATA]` "Verify the 'must cite' list: for each entry, WebSearch to
  confirm the paper exists and says what the plan claims."

Context separation is automatic — the subagent starts with zero session
context.

### Step 3 — User approves/revises plan

User reads the adversarial review. Revise or proceed.

### Step 4 — Write (writer-thesis subagent, sequential or parallel)

Dispatch writer-thesis with a pointer to the approved plan file and the
target section(s).

#### `[LIT]` Literature section — writer-thesis instructions

The dispatch prompt must instruct writer-thesis to complete these steps:

1. Read section description in `thesis/THESIS_STRUCTURE.md`
2. Read plan's seed bibliography; verify each reference via WebSearch
3. Discover additional references (follow Literature Search Protocol below)
4. Draft in `thesis/chapters/XX_*.md`
5. Run Critical Review Checklist — Literature variant (see
   `.claude/rules/thesis-writing.md`)
6. Plant `[REVIEW:]` and `[NEEDS CITATION]` flags for anything needing
   external validation
7. Append `## References` section at chapter file end with full
   bibliographic entries (see Bibliographic Output Format below)
8. Update `thesis/WRITING_STATUS.md` → DRAFTED
9. Update `thesis/chapters/REVIEW_QUEUE.md` with Pending entry
10. Produce Chat Handoff Summary including: citation count, flag count,
    self-discovered references not in plan's seed list

#### `[DATA]` Data-fed section — writer-thesis instructions

The dispatch prompt must instruct writer-thesis to complete all 9
mandatory Pass 1 steps (from `.claude/rules/thesis-writing.md`):

1. Read relevant entry in the active dataset's `research_log.md`
2. Read report artifacts that feed the section
3. Read section description in `thesis/THESIS_STRUCTURE.md`
4. Draft in `thesis/chapters/XX_*.md`
5. Run Critical Review Checklist (below)
6. Plant `[REVIEW: ...]` flags for anything needing external validation
7. Update `thesis/WRITING_STATUS.md` → DRAFTED
8. Update `thesis/chapters/REVIEW_QUEUE.md` with Pending entry
9. Produce Chat Handoff Summary (format below)

#### Citation reconciliation

**`[LIT]` Literature sections — tiered reconciliation:**
writer-thesis must cross-check its actual citations against the plan's
seed bibliography. Planned citations not used must be explained. Self-
discovered citations are handled by the tiered verification in Step 5 —
they do not need individual flagging during drafting.

**`[DATA]` Data-fed sections — strict reconciliation:**
writer-thesis must cross-check its actual citations against the plan's
"must cite" list. Any planned citation not used must be explained. Any
self-discovered citation not in the plan must be flagged for adversarial
verification.

**Parallel dispatch rules (both types):**
- Only dispatch parallel writer-thesis instances on sections the plan
  marks as parallel-safe (no content dependency).
- Limit to 2 parallel instances per chapter to control voice drift.
- Each instance writes to a different section file or clearly delineated
  section within a chapter file.
- If one instance fails, the other's output is still valid — review
  proceeds on completed sections only.

### Step 5 — Adversarial review of draft (reviewer-adversarial subagent)

Dispatch reviewer-adversarial (Mode C — Thesis Chapter Review).

#### `[LIT]` Literature sections — tiered citation verification

The dispatch prompt must include:
- Path to the drafted chapter file
- Path to the plan file (for seed bibliography cross-check)
- Instruction: "Use tiered citation verification:
  **Tier 1 (must verify):** Every reference from the plan's seed
  bibliography — confirm the paper exists and the draft's characterization
  is accurate.
  **Tier 2 (spot check):** 30-50% of self-discovered references in
  peer-reviewed venues — verify by WebSearch.
  **Tier 3 (defer):** Supplementary references, recent preprints,
  documentation links — flag for Pass 2 verification only."

#### `[DATA]` Data-fed sections — artifact-based verification

The dispatch prompt must include:
- Path to the drafted chapter file
- Path to the plan file (for "must cite" and "must justify" cross-check)
- Paths to feeding artifacts (for claim-evidence alignment)
- Instruction: "For each cited paper, verify via WebSearch that the
  citation says what the draft claims."

**Context budget note:** The reviewer reads 6+ documents cold (draft,
plan, style brief, invariants, thesis structure, feeding artifacts). For
chapters with many feeding artifacts, the dispatch prompt should
prioritize: (1) draft, (2) plan, (3) feeding artifacts. The reviewer's
own "required reading" list handles the rest.

### Step 5.5 — Chapter consistency pass

**After all sections in a chapter have passed adversarial review** (Step
5), perform a consistency pass before Chat handoff. This is the user's
responsibility (manually or by dispatching a reviewer):

1. **Terminology consistency:** Same concepts use same terms across all
   sections (e.g., "gradient boosted trees" vs "GBDT" — pick one)
2. **No redundant coverage:** If both §2.4 and §2.6 describe ROC-AUC,
   consolidate into one section and cross-reference from the other
3. **Structural balance:** No section more than 2x the length of its
   siblings unless justified by content density
4. **Cross-references:** Internal references between sections are accurate
5. **Voice consistency:** Register does not drift between sections drafted
   by different parallel instances

### Step 6 — Chat handoff (Pass 2)

User takes to Claude Chat:
- The drafted chapter
- The Chat Handoff Summary (from Step 4 output)
- The adversarial review (from Step 5 output)
- `[LIT]` Tier 3 citations flagged for verification

Chat does: literature validation, citation checking, methodology
alignment, [REVIEW:] flag resolution.

## Literature Search Protocol

Applies to writer-thesis when drafting literature sections (Step 4 `[LIT]`).

1. **Start from the plan's seed bibliography.** Verify each reference
   exists via WebSearch before using it.
2. **Discover additional references.** Minimum 3 WebSearch queries per
   section with different query formulations (e.g., for §2.4: "gradient
   boosted trees binary classification survey", "XGBoost LightGBM
   comparison", "random forest vs logistic regression esports").
3. **Prefer peer-reviewed sources.** In order of preference:
   - Conference proceedings: NeurIPS, ICML, AAAI, IJCAI, IEEE CIG/CoG,
     KDD, WWW
   - Journals: JMLR, IEEE Trans. Games, Machine Learning, PLOS ONE
   - Canonical textbooks: Bishop (2006), Hastie et al. (2009), Murphy
     (2012/2022), Goodfellow et al. (2016)
   - Dataset papers: Scientific Data, data descriptor venues
   - Official documentation: game engine docs, API docs
4. **Flag non-peer-reviewed sources.** Any source not in a peer-reviewed
   venue gets `[REVIEW: non-peer-reviewed source — <url>]`.
5. **Target citation density.** Approximately 2-4 references per page,
   consistent with CS thesis norms. Literature survey sections (Ch 2, 3)
   should be at the higher end; framing sections (Ch 1) at the lower end.
6. **No Wikipedia in final prose.** Wikipedia may be used to discover
   primary sources but must not appear as a citation. If a Wikipedia
   claim is useful, find and cite the primary source it references.

## Bibliographic Output Format

writer-thesis writes inline citation keys in `[AuthorYear]` format within
the chapter markdown (e.g., `[Glickman2001]`, `[DemSar2006]`). This is
consistent with `.claude/rules/thesis-writing.md` line 46.

At the end of each chapter file, writer-thesis appends a `## References`
section with full bibliographic entries in a consistent format:

```
## References

- [Elo1978] Elo, A. E. (1978). The Rating of Chessplayers, Past and
  Present. Arco.
- [Glickman2001] Glickman, M. E. (2001). Dynamic paired comparison models
  with stochastic variances. Journal of Applied Statistics, 28(6), 673-689.
```

A separate consolidation step (manual or scripted) merges chapter-level
references into `thesis/references.bib` for final typesetting. writer-thesis
does not maintain BibTeX during drafting — it breaks flow and introduces a
format that markdown review cannot validate.

## Session Architecture

```
Session 1 (ML experiments)          Session 2 (thesis writing)
------------------------------      --------------------------------
                                    Gate 0: draft §1.1, calibrate voice
                                      (one-time, before scaling)
                                    Gate 0.5: draft §2.5, calibrate
                                      literature handling (one-time)
                                        |
Phase 01 notebooks                  Step 1: plan (planner-science)
  |                                 Step 2: adversarial review of plan
  |                                 Step 3: user approves
  |                                 Step 4: write (writer-thesis x N)
  |                                 Step 5: adversarial review of draft
  |                                 Step 5.5: chapter consistency pass
  |                                 Step 6: Chat handoff (Pass 2)
  v                                   |
Phase 01 findings feed into   <---    v
  thesis §4.1.1, §4.2.x              next chapter plan
```

The two sessions are independent. ML experiments produce artifacts in
`reports/`; thesis writing reads those artifacts. No shared state beyond
the filesystem.

## Plan Infrastructure

Category F thesis plans use the standard planning infrastructure:

- Plan file: `planning/current_plan.md`
- DAG: `planning/dags/DAG.yaml`
- Specs: `planning/specs/spec_*.md` (one per section or parallel batch)

The DAG is lightweight — typically one task group per parallel section
batch. This avoids contradicting planner-science's output contract (which
requires a Suggested Execution Graph) while keeping the overhead minimal.

For literature sections, `source_artifacts` in the plan lists meta-
documents (THESIS_STRUCTURE.md, author-style-brief-pl.md, scientific-
invariants.md, prior chapter drafts), not report artifacts. This is a
semantic distinction, not a schema change.

## Parallelism Map for DRAFTABLE Sections

Based on THESIS_STRUCTURE.md and WRITING_STATUS.md content dependencies.
`||` = parallel-safe, `->` = sequential dependency.

**Chapter 1** (plan_01):
  - §1.1 is the calibration section (Gate 0) — draft first, alone
  - After Gate 0: §1.2 || §1.3 -> §1.4

**Chapter 2** (plan_02):
  - §2.5 is the calibration section (Gate 0.5) — draft after Gate 0
  - After Gate 0.5: §2.1 || §2.4 || §2.6 (all independent: RTS games,
    ML methods, evaluation metrics — disjoint topics)
  - §2.2 depends on Phase 01 artifacts (game timing, replay structure),
    not on sibling sections. Draft when Phase 01 data is available,
    independent of §2.1/2.4/2.5/2.6 completion.
  - §2.3 BLOCKED (AoE2 roadmap)

**Chapter 3** (plan_03):
  - §3.1 || §3.2 || §3.3 (independent literature surveys)
  - §3.4 BLOCKED (AoE2 lit review)
  - §3.5 BLOCKED — depends on ALL of §3.1-§3.4 (synthesizes gaps).
    Cannot draft until §3.4 is unblocked. A skeleton noting the gap
    from §3.1-§3.3 is acceptable but does not constitute DRAFTABLE.

**Chapter 4** (plan_04):
  - §4.4.4 only (evaluation metrics — literature, draftable now)
  - All other sections BLOCKED on Phase 01-04

**Chapter 6** (plan_06):
  - §6.5 only (threats to validity — start listing known threats)

**Chapter 7** (plan_07):
  - §7.3 only (future work — accumulate ideas)

## Voice Drift Mitigation

1. writer-thesis reads `.claude/author-style-brief-pl.md` first (already
   in agent definition's "Read first" list).
2. Limit to 2 parallel instances per chapter.
3. Gate 0 calibration test catches systemic voice problems before scaling.
4. Gate 0.5 catches literature-section-specific problems before scaling.
5. Adversarial review (Step 5) flags register inconsistencies across
   sections (Lens 4 includes voice checks against the style brief).
6. Step 5.5 consistency pass catches terminology and structural drift
   across sections drafted in parallel.
7. User does a final consistency pass after all sections in a chapter are
   drafted — this is explicitly part of the workflow, not an afterthought.

## Failure Recovery

- **Writer-thesis subagent fails mid-draft:** The chapter file may have
  partial content. User inspects, decides whether to re-dispatch on the
  same section or revert the file. Completed sibling sections (from
  parallel dispatch) are unaffected.
- **Adversarial review finds blockers:** User revises the draft (manually
  or by re-dispatching writer-thesis with the review findings) before
  proceeding to Pass 2.
- **Calibration test (Gate 0) fails:** Diagnose per the style brief's
  instructions (lines 74-82). Do not scale until fixed.
- **Literature calibration (Gate 0.5) fails:** Diagnose whether the issue
  is citation coverage, structural coherence, or critical depth. Adjust
  the Literature Search Protocol or seed bibliography guidance. Re-draft
  §2.5 before scaling to other literature sections.
- **Citation reconciliation gap (data-fed):** If writer-thesis used
  citations not in the plan's "must cite" list, adversarial review in
  Step 5 independently verifies them. If writer-thesis missed a planned
  citation, the adversarial review flags the omission.
- **Citation coverage gap (literature):** If adversarial review (Step 5)
  finds missing canonical references, user decides whether to re-dispatch
  writer-thesis for the section or handle in Pass 2.
- **Consistency pass finds drift (Step 5.5):** User resolves terminology,
  coverage, or balance issues before Chat handoff. For minor issues, edit
  directly. For structural issues, re-dispatch writer-thesis on the
  affected section with explicit instructions referencing the sibling
  sections.
