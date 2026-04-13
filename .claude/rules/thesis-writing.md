---
paths:
  - "thesis/**/*"
---

# Thesis Writing Workflow

## Two-Pass Process (MANDATORY)

### Pass 1 — Claude Code (Category F session)

**Data-fed sections** (WRITING_STATUS.md lists a specific Phase):
1. Read relevant entry in the active dataset's `research_log.md`
2. Read report artifacts that feed the section
3. Read section description in `thesis/THESIS_STRUCTURE.md`
4. Draft in `thesis/chapters/XX_*.md`
5. Run Critical Review Checklist — Data variant (below)
6. Plant `[REVIEW: ...]` flags for anything needing external validation
7. Update `thesis/WRITING_STATUS.md` → DRAFTED
8. Update `thesis/chapters/REVIEW_QUEUE.md` with Pending entry
9. Produce Chat Handoff Summary (format below)

**Literature sections** (WRITING_STATUS.md shows "Feeds from: —"):
1. Read section description in `thesis/THESIS_STRUCTURE.md`
2. Read plan's seed bibliography; verify each reference via WebSearch
3. Discover additional references (see Literature Search Protocol in
   `thesis/plans/idea_audit.md`)
4. Draft in `thesis/chapters/XX_*.md`
5. Run Critical Review Checklist — Literature variant (below)
6. Plant `[REVIEW:]` and `[NEEDS CITATION]` flags
7. Append `## References` section at chapter file end with full entries
8. Update `thesis/WRITING_STATUS.md` → DRAFTED
9. Update `thesis/chapters/REVIEW_QUEUE.md` with Pending entry
10. Produce Chat Handoff Summary including: citation count, flag count,
    self-discovered references not in plan's seed list

### Pass 2 — Claude Chat (external validation)
User brings draft + artifacts to Claude Chat for literature validation,
citation checking, methodology alignment, and flag resolution.

## Critical Review Checklist (MUST complete before DRAFTED status)

### Data variant (sections fed by Phase artifacts)

1. **Numerical consistency:** Every number traces to a report artifact exactly
2. **Claim-evidence alignment:** Evidence supports the specific claim;
   hedge when suggestive ("consistent with..." not "demonstrates")
3. **Derivation traceability:** Every threshold has empirical or cited justification
4. **Statistical interpretation:** Effect sizes alongside p-values; non-significant
   ≠ "no effect"; note multiple comparison corrections
5. **Scope honesty:** Don't generalise beyond dataset; don't minimise limitations
6. **Missing context flags:** Insert `[REVIEW: ...]` for field-norm divergence

### Literature variant (sections fed by papers/textbooks)

1. **Citation accuracy:** Every claim attributed to a source accurately reflects
   that source's finding; do not mischaracterize or overstate
2. **Claim-citation alignment:** Every substantive claim is backed by a citation
   or explicit reasoning; flag gaps with `[NEEDS CITATION]`
3. **Coverage completeness:** Canonical references for the section's topic are
   present; flag known gaps with `[REVIEW: missing coverage — <topic>]`
4. **Critical evaluation:** Section is argumentative, not purely descriptive;
   connects surveyed work to the thesis problem
5. **Scope honesty:** Don't generalise findings beyond what the cited work claims;
   note limitations of cited studies where relevant
6. **Missing context flags:** Insert `[REVIEW: ...]` for field-norm divergence
   or claims needing primary-source verification

## Inline Flag Types
- `[REVIEW: <concern>]` — needs literature validation (Pass 2)
- `[UNVERIFIED: source?]` — number not traceable to artifact
- `[NEEDS JUSTIFICATION]` — threshold without derivation
- `[NEEDS CITATION]` — claim requires literature reference

## Writing Quality
- Third person or first person plural; academic register
- Present tense for established facts, past tense for actions taken
- Every figure/table has caption and number
- Citations: `[AuthorYear]` keys in `thesis/references.bib`
- Do NOT copy-paste from research_log.md — rewrite for thesis audience

## WRITING_STATUS.md Semantics
| Status | Meaning |
|--------|---------|
| SKELETON | Header exists, no prose |
| BLOCKED | Feeding phase incomplete |
| DRAFTABLE | Feeding phase complete, ready to write |
| DRAFTED | First draft exists, may need revision |
| REVISED | Updated after later-phase context |
| FINAL | Content-complete, reviewed, ready for typesetting |

## Chat Handoff Summary Format

### Data-fed sections
```
## Chat Handoff Summary
### Section: §X.Y — [title] in thesis/chapters/XX_*.md
### Status: DRAFTED (first draft / revision)
### Flags: N [REVIEW], N [NEEDS CITATION], etc.
### Artifacts: [list with what each contains]
### Questions for Chat: [concrete questions]
### Numbers verified: [number] ← [artifact, line] ✓
```

### Literature sections
```
## Chat Handoff Summary
### Section: §X.Y — [title] in thesis/chapters/XX_*.md
### Status: DRAFTED (first draft / revision)
### Flags: N [REVIEW], N [NEEDS CITATION], etc.
### Citations: N total (N from seed bibliography, N self-discovered)
### Self-discovered references not in plan: [list]
### Tier 3 citations for Pass 2 verification: [list]
### Questions for Chat: [concrete questions]
```

## Phase-to-section mapping

The canonical Phase list, numbering, and definitions live in docs/PHASES.md.
docs/INDEX.md provides a convenience lookup from active Phase to methodology
manual — it does not define Phases. Each ROADMAP.md's per-step 'Thesis mapping'
field is the source of truth for which thesis section a given phase output
feeds. Do not duplicate that mapping here.

## Formatting Reference

For content validation thresholds (minimum character count, abstract bounds, keyword count,
required sections) applicable during Markdown authoring, see
`.claude/thesis-formatting-rules.yaml` → `content_thresholds`.

The `word_formatting_spec` section of the same file (font, margins, binding) is deferred
and only relevant when producing the final Word/PDF submission.
