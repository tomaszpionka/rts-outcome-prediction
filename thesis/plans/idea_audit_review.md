# Adversarial Review: idea_audit.md -- Dataset-Agnostic Writing Fitness

Reviewed: 2026-04-13. Reviewer: reviewer-adversarial (Opus).

## Verdict

The protocol is **not fit for purpose** for the 16 DRAFTABLE sections in its
current form. It was designed with data-fed chapters in mind: its vocabulary
("feeding artifacts," "report artifacts," "cross-check against artifacts"), its
Pass 1 checklist (steps 1-2 both reference report artifacts), and its
reconciliation rule all assume the writer has empirical artifacts to trace claims
against. For dataset-agnostic literature sections -- which constitute 100% of
the currently draftable work -- the protocol has three categories of failure:

1. It mandates steps that are vacuous (read report artifacts that do not exist)
2. It omits steps that are essential (literature search strategy, source quality
   gates, bibliographic output)
3. It creates ambiguity about what a Category F plan should contain when there
   are no Phase artifacts to reference

An operator following idea_audit.md literally for Chapter 2 would produce a plan
that planner-science cannot populate (because its constraints require
`source_artifacts` for Category F but there are no report artifacts to list) and
a dispatch that writer-thesis cannot execute correctly (because Pass 1 steps 1-2
are empty by construction).

---

## Critical Findings

### Finding 1 -- Pass 1 Steps 1-2 Are Vacuous for Literature Sections

**Evidence:** `thesis-writing.md` lines 7-8 (the mandatory Pass 1 steps)
require:
- Step 1: "Read research_log entries for the section"
- Step 2: "Read report artifacts that feed the section"

`idea_audit.md` line 88-91 faithfully reproduces these as mandatory instructions
for writer-thesis. But WRITING_STATUS.md shows all 16 DRAFTABLE sections have
"Feeds from: --" (literal dash). There are no research_log entries for Chapter
1, 2, or 3 literature sections, and there are no report artifacts.

**Consequence:** writer-thesis receives a mandatory instruction to read artifacts
that do not exist. It will either (a) skip the steps silently, violating the
"complete all 9 mandatory Pass 1 steps" instruction at idea_audit.md line 89, or
(b) halt and report a gap that is not a real gap but a protocol mismatch.

### Finding 2 -- planner-science Cannot Populate "Feeding Artifacts" for Literature Sections

**Evidence:** `idea_audit.md` line 55 requires the plan to include "Feeding
artifacts (paths to report artifacts that supply the data)" per section. But for
14 of the 16 DRAFTABLE sections, there are zero report artifacts. The only
section with any Phase artifact connection is section 2.2 (which has partial
Phase 01 data for game timing), and even that is mostly literature.

**Consequence:** planner-science is forced to either (a) leave `source_artifacts`
empty, violating its own output contract, (b) list THESIS_STRUCTURE.md and
author-style-brief-pl.md as "source artifacts" (technically correct but
semantically meaningless -- these are not data sources, they are
meta-instructions), or (c) list the papers themselves as source artifacts, which
conflates bibliography with pipeline artifacts. The protocol does not distinguish
between "artifacts that contain data findings" and "artifacts that contain
writing instructions."

### Finding 3 -- No Literature Search Protocol

**Evidence:** `idea_audit.md` section "Why DAGs Are Not Needed Here" (line 213)
states "writer-thesis self-researches. WebFetch during drafting replaces
pre-planned literature lookups." This is the entire guidance on how literature
search happens. There is no specification of:

- How many sources per section are expected
- Which databases or indices to search (Google Scholar, Semantic Scholar, DBLP,
  ACM DL)
- Quality gates for sources (the style brief at line 24 says "without Wikipedia
  and random PDFs in final drafts," but the protocol has no enforcement mechanism
  during Pass 1)
- How to handle Polish-language sources vs. English-language sources
- Whether the "must cite" list in the plan is a minimum set or an exhaustive set

**Consequence:** The quality of literature coverage becomes entirely dependent on
writer-thesis's WebSearch behavior, which is model-dependent and
session-dependent. Two runs of the same section could produce wildly different
citation sets. The adversarial review in Step 5 can catch bad citations after the
fact, but cannot catch missing coverage -- you cannot verify the absence of a
paper you did not know should be there.

### Finding 4 -- "Must Justify" List Is Misdirected for Pure Literature Sections

**Evidence:** `idea_audit.md` line 57 requires each plan section to include a
"must justify" list of "methodological choices needing alternatives-considered
paragraphs." For section 2.4 (ML methods for classification), there are no
methodological choices being made -- the section is a textbook survey. The
methodological choices (why logistic regression, why LightGBM, why not SVM)
belong in Chapter 4, not Chapter 2.

Similarly, for section 3.1 (traditional sports prediction), there is nothing to
"justify" -- the section presents prior work, it does not make design decisions.

**Consequence:** planner-science will either (a) produce empty "must justify"
lists for these sections, which wastes a plan constraint that exists for a good
reason, or (b) invent artificial justification requirements that do not match the
section's rhetorical purpose.

The correct analog for literature sections is not "must justify" but something
like **"must structure around"** -- what is the organizing principle for the
section? Chronological? By method family? By game domain? This is a rhetorical
architecture question, not a methodology question.

### Finding 5 -- Reconciliation Rule Assumes Planned Literature Is Exhaustive

**Evidence:** `idea_audit.md` lines 106-109: "writer-thesis must cross-check its
actual citations against the plan's 'must cite' list. Any planned citation not
used must be explained. Any self-discovered citation not in the plan must be
flagged for adversarial verification."

For literature sections, the "must cite" list from the plan will be a seed set of
perhaps 5-10 key references per section. writer-thesis, using WebSearch, will
discover 15-30 additional references during drafting. Under the current rule,
every single one of those self-discovered references must be "flagged for
adversarial verification." This creates a bottleneck: the adversarial reviewer
in Step 5 must WebSearch-verify potentially 60+ citations across a chapter,
within a single subagent invocation.

**Consequence:** Either (a) the adversarial review becomes a citation-
verification marathon that exhausts context budget, or (b) the reviewer triages
and only spot-checks, which undermines the stated purpose of the reconciliation
rule. The protocol needs a tiered citation verification strategy.

### Finding 6 -- Missing Bibliographic Output Specification

**Evidence:** The protocol specifies that drafts go into
`thesis/chapters/XX_*.md` (idea_audit.md line 98, thesis-writing.md line 14).
But there is no mention of `thesis/references.bib` in the protocol. The thesis
structure (THESIS_STRUCTURE.md line 410) says "Maintain a BibTeX file
`references.bib`," but writer-thesis is instructed to use markdown
reference-style links with a References section at the bottom.

**Consequence:** Without explicit guidance, each writer-thesis invocation may
handle citations differently. Chapter 2 might use markdown links; Chapter 3
might use `[AuthorYear]` keys. Reconciling these formats later is manual drudgery
that the protocol was supposed to prevent.

### Finding 7 -- Gate 0 Calibration Does Not Test Literature-Section-Specific Risks

**Evidence:** `idea_audit.md` lines 30-41 specify Gate 0 on section 1.1 with
four criteria: register, argumentative structure, hedging, citation quality.
Section 1.1 is a framing section (~2 pages), not a deep literature survey.

The risks specific to literature-heavy sections (citation density, coverage
completeness, textbook-vs-paper balance, structural coherence across method
families) are not tested by Gate 0. A writer-thesis that passes Gate 0 on
section 1.1 may still produce a section 2.4 that reads like a Wikipedia article
-- descriptive summaries of each method with no connecting thread or critical
evaluation.

**Consequence:** Gate 0 validates voice calibration but not literature-section
competence. The protocol should either add a Gate 0.5 on a substantive literature
section or explicitly acknowledge that Gate 0 tests only voice, not literature
handling.

### Finding 8 -- Protocol-Infrastructure Mismatch on Plan Location

**Evidence:** `idea_audit.md` line 49 specifies plans go to
`thesis/plans/plan_NN_<chapter_slug>.md`. But the standard planning
infrastructure uses `planning/current_plan.md`. The protocol explicitly says
"DAGs are not needed here" (idea_audit.md line 206-216), but planner-science's
own output contract requires a Suggested Execution Graph section.

**Consequence:** Direct contradiction: the protocol says "no DAG," but the agent
it dispatches cannot produce output without one. The protocol must resolve this:
either use the standard planning infrastructure with DAGs, or define an
alternative lightweight plan format and explicitly exempt planner-science from the
DAG requirement for this plan type.

### Finding 9 -- Section 3.5 (Research Gap) Is Mislabeled as DRAFTABLE

**Evidence:** WRITING_STATUS.md line 58 marks section 3.5 as DRAFTABLE. But
`idea_audit.md` lines 193-194 correctly note: "depends on ALL of sections 3.1-
3.4 (synthesizes gaps). Not draftable until section 3.4 is unblocked."

**Consequence:** If an operator trusts WRITING_STATUS.md, they will attempt to
draft section 3.5 in full. If they trust the parallelism map, they will skip it.
The status tracker should be reconciled -- either BLOCKED or a new status like
PARTIAL_DRAFTABLE.

### Finding 10 -- No Cross-Section Consistency Pass Is Defined

**Evidence:** `idea_audit.md` line 227 mentions "User does a consistency pass
after all sections in a chapter are drafted -- this is explicitly part of the
workflow, not an afterthought." But there is no step in the 6-step protocol for
this.

For Chapter 2, where sections 2.1, 2.4, 2.5, and 2.6 can be drafted in parallel
by up to 2 instances, there is a real risk of: terminology inconsistency, 
redundant coverage (both 2.4 and 2.6 describe ROC-AUC), or structural imbalance.

**Consequence:** The consistency pass is mentioned as a principle but not
operationalized. There is no guidance on what it checks, who does it, or when it
happens relative to Pass 2.

---

## Recommendations

### R1 -- Bifurcate the Protocol

Create explicit variant sections for "data-fed sections" and "literature
sections." The 6-step sequence is fine as a skeleton, but steps 1 and 4 need
variant instructions.

For literature sections, Pass 1 steps 1-2 should be replaced with:
- Step 1: Read `THESIS_STRUCTURE.md` section description; identify the section's
  rhetorical purpose (survey, framing, methodology background)
- Step 2: Read the plan's seed bibliography; use WebSearch to verify each seed
  reference and discover related work

### R2 -- Define a Literature Plan Schema

For Category F plans covering literature sections, replace "feeding artifacts"
with **"seed bibliography"** -- a curated list of 5-10 key references per section
with (author, year, venue, what it contributes to this section). Replace "must
justify" with **"structural principle"** -- how the section is organized and why
(chronological, by method family, by domain). Keep "must cite" and "must
contrast" as-is; they work for literature sections.

### R3 -- Add a Literature Search Protocol

Specify for writer-thesis:
1. For each section, begin with the plan's seed bibliography
2. Use WebSearch to find additional peer-reviewed sources (minimum 3 searches
   per section with different query formulations)
3. Prefer: conference proceedings (NeurIPS, ICML, AAAI, IEEE CIG), journals
   (JMLR, IEEE Trans. Games), canonical textbooks (Bishop, Hastie et al.,
   Murphy)
4. Flag any non-peer-reviewed source with `[REVIEW: non-peer-reviewed source]`
5. Target citation density: approximately 2-4 references per page (consistent
   with CS thesis norms)

### R4 -- Resolve the DAG Contradiction

Choose one of:
- **(a)** Use the standard `planning/current_plan.md` + DAG infrastructure for
  Category F plans. The DAG is lightweight (one task group per parallel section
  batch). Consistent with all existing infrastructure.
- **(b)** Formally exempt Category F literature plans from the DAG requirement.
  This requires modifying planner-science's output contract.

Option (a) is simpler and does not require modifying existing agent definitions.

### R5 -- Define Bibliographic Output Format

State explicitly: writer-thesis writes inline citation keys in `[AuthorYear]`
format within the chapter markdown. At the end of each chapter file, it appends a
`## References` section with full bibliographic entries. A separate consolidation
step (manual or scripted) merges these into `thesis/references.bib`. Do not ask
writer-thesis to maintain BibTeX during drafting -- it breaks flow and introduces
a format that markdown review cannot validate.

### R6 -- Add a Tiered Citation Verification Strategy

Replace the blanket "flag all self-discovered citations for adversarial
verification" with:
- **Tier 1 (must verify):** Canonical references from the plan's "must cite"
  list. Adversarial reviewer verifies these exist and say what the draft claims.
- **Tier 2 (spot check):** Self-discovered references in peer-reviewed venues.
  Adversarial reviewer spot-checks 30-50% by WebSearch.
- **Tier 3 (defer to Pass 2):** Supplementary references, recent preprints,
  documentation links. Verified in Chat Pass 2.

### R7 -- Add Gate 0.5 for Literature Sections

After Gate 0 passes on section 1.1, draft one substantive literature section
(recommendation: section 2.5 on rating systems -- bounded scope, well-known
canonical references, directly thesis-relevant). Evaluate on: citation density,
coverage completeness, structural coherence, critical evaluation (not just
description). Only after Gate 0.5 passes should parallel literature drafting
proceed.

### R8 -- Reconcile Section 3.5 Status

Change WRITING_STATUS.md section 3.5 status from DRAFTABLE to BLOCKED, with
note: "Skeleton draftable from sections 3.1-3.3; full draft blocked on section
3.4 (AoE2)." The parallelism map already says this; the status tracker should
agree.

### R9 -- Operationalize the Consistency Pass

Add Step 5.5 between adversarial review and Chat handoff:
- After all sections in a chapter have passed adversarial review, the user (or a
  reviewer dispatch) reads all sections sequentially and checks: terminology
  consistency, no redundant coverage, structural balance (no section more than 2x
  the length of its siblings unless justified), cross-references between sections.

### R10 -- Specify `source_artifacts` for Category F Literature Plans

For Category F literature plans, `source_artifacts` should list the documents
that inform the plan (THESIS_STRUCTURE.md, author-style-brief-pl.md,
scientific-invariants.md, any prior chapter drafts that constrain the current
one), NOT the report artifacts that feed data into the section.

---

## Revised Protocol Sketch for Dataset-Agnostic Chapters

This is a condensed variant of the full protocol, applicable when all sections
in the batch have "Feeds from: --" in WRITING_STATUS.md.

### Gate 0 -- Voice Calibration (unchanged)

Draft section 1.1. Evaluate 4 criteria: register, argumentative structure,
hedging, citation quality. All four must pass.

### Gate 0.5 -- Literature Calibration (new)

Draft section 2.5 (rating systems). Evaluate:
- Citation density >= 2/page
- All canonical references present (Elo 1978, Glickman 1999/2001, Herbrich et
  al. 2006)
- Structural coherence (each system presented with same depth pattern)
- Critical evaluation present (not just "Elo works as follows")

Only after both gates pass does parallel drafting proceed.

### Step 1 -- Plan (planner-science)

Produce a Category F plan at `planning/current_plan.md` with:
- Per section: **seed bibliography** (5-10 key references), **structural
  principle** (chronological/by-family/etc.), "must contrast" list, expected
  length
- Instead of "feeding artifacts": list THESIS_STRUCTURE.md and any prior chapter
  drafts as source_artifacts
- DAG with one task group per parallel batch (matching the parallelism map)

### Step 2 -- Adversarial review of plan (unchanged)

Add: "Verify seed bibliography covers the canonical references for each
section's topic."

### Step 3 -- User approval (unchanged)

### Step 4 -- Write (writer-thesis)

Modified Pass 1 for literature sections:
1. Read section description in THESIS_STRUCTURE.md
2. Read plan's seed bibliography; verify each reference via WebSearch
3. Discover additional references (minimum 3 WebSearch queries per section,
   varying query formulation)
4. Draft in `thesis/chapters/XX_*.md` -- prose, not bullets; argumentative, not
   descriptive
5. Run Critical Review Checklist (adapted: "numerical consistency" becomes
   "citation accuracy"; "derivation traceability" becomes "every claim backed by
   citation or explicit reasoning")
6. Plant `[REVIEW:]` and `[NEEDS CITATION]` flags
7. Append `## References` section at chapter file end with full entries
8. Update WRITING_STATUS.md to DRAFTED
9. Update REVIEW_QUEUE.md
10. Produce Chat Handoff Summary including: citation count, flag count,
    self-discovered references not in plan's seed list

### Step 5 -- Adversarial review of draft

Use tiered citation verification:
- Tier 1: verify all seed bibliography references (must match what draft claims)
- Tier 2: spot-check 30-50% of self-discovered references
- Tier 3: flag for Pass 2

### Step 5.5 -- Chapter consistency pass (new)

After all sections in a chapter have passed adversarial review:
- Terminology consistency across sections
- No redundant coverage
- Structural balance
- Cross-reference accuracy

### Step 6 -- Chat handoff (unchanged)

Explicitly include Tier 3 citations for verification.

---

## Draftable Sections Summary (post-reconciliation)

After applying R8 (reconcile section 3.5), the truly draftable sections are:

**15 sections** (not 16):

| Chapter | Sections | Parallel batches |
|---------|----------|-----------------|
| Ch 1 | 1.1 (Gate 0), then 1.2 &#124;&#124; 1.3 -> 1.4 | 2 batches |
| Ch 2 | 2.1 &#124;&#124; 2.4 &#124;&#124; 2.5 (Gate 0.5) &#124;&#124; 2.6 | 1 batch (max 2 parallel) |
| Ch 3 | 3.1 &#124;&#124; 3.2 &#124;&#124; 3.3 | 1 batch (max 2 parallel) |
| Ch 4 | 4.4.4 | standalone |
| Ch 6 | 6.5 | standalone |
| Ch 7 | 7.3 | standalone |

Section 3.5 is BLOCKED until 3.4 (AoE2) is unblocked.
