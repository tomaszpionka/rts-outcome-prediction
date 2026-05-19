---
title: "Bialecki2023 author positions 3–4 post-merge correction"
category: F
branch: docs/thesis-bialecki2023-author-correction
base_ref: 3238addb8d01b6baa7d642384e0d4f28e249f481
date: 2026-05-19
version_bump: "3.60.0 → 3.61.0"
planner_model: user-directed (executor-ready plan)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/references.bib
  - thesis/pass2_evidence/bibliography_cleanup_report.md
  - CHANGELOG.md
  - pyproject.toml
  - planning/INDEX.md
  - planning/current_plan.md
  - planning/current_plan.critique.md
critique_required: true
critique_file: planning/current_plan.critique.md
research_log_ref: null
---

## Scope

Bib-only post-merge correction. This plan corrects the `Bialecki2023` author
positions 3–4 given-name swap discovered after PR #225 merged. The correction
is applied to `thesis/references.bib` (one-line change) and all five
load-bearing false statements in
`thesis/pass2_evidence/bibliography_cleanup_report.md` are corrected in place
(lineage preserved; none deleted). CHANGELOG, pyproject.toml, and planning
artifacts are updated. No chapter or appendix edit. No .py changes.

---

## Problem Statement

PR #225 (`docs/thesis-bibliography-canonicalization`) audited `Bialecki2023` at
surname + author-count + order granularity. Crossref confirmed 8 authors in the
correct surname order; the audit concluded "matches exactly / keep / NO bib edit".
That conclusion was wrong.

The pre-edit `thesis/references.bib` line 6 read:

```
author  = {Białecki, Andrzej and Jakubowska, Natalia and Dobrowolski, Piotr and Białecki, Paweł and Krupiński, Leszek and Szczap, Andrzej and Białecki, Robert and Gajewski, Jan},
```

Crossref (`10.1038/s41597-023-02510-7`) and arXiv (`2207.03428`) concordantly give:

| Position | Pre-edit bib (WRONG) | Crossref + arXiv (CORRECT) |
|----------|----------------------|---------------------------|
| 3 | Dobrowolski, **Piotr** | Dobrowolski, **Paweł** |
| 4 | Białecki, **Paweł** | Białecki, **Piotr** |

**Root cause:** `Piotr` and `Paweł` both collapse to the initial "P." under
initial-only matching. PR #225 verified surname + count + order — all correct —
but never compared given-name tokens independently. The swap was therefore
invisible to the #225 audit and to the reviewer-adversarial pass that inherited
that blind spot.

**Corrected author line:**

```
author  = {Białecki, Andrzej and Jakubowska, Natalia and Dobrowolski, Paweł and Białecki, Piotr and Krupiński, Leszek and Szczap, Andrzej and Białecki, Robert and Gajewski, Jan},
```

The `@article{Bialecki2023}` key, all other fields, and all citation sites are
unchanged. Zero citation blast radius.

---

## Assumptions & Unknowns

1. Crossref `10.1038/s41597-023-02510-7` is the authoritative primary source for
   `Bialecki2023` author metadata; arXiv `2207.03428` is concordant corroboration.
2. No bib convention or dataset erratum defends the current state.
3. Key `Bialecki2023` must not change — all citation sites remain valid.
4. `thesis/chapters/**` and `thesis/reviews_and_others/**` are READ-ONLY this PR
   (the author names appear only in the bib entry, not in prose).
5. The `bibliography_cleanup_report.md` false statements must be corrected in
   place (not deleted) to preserve the error-lineage record this PR exists to
   document.
6. Unknown: whether any other entry in `references.bib` may have a similar
   initial-only match blind spot — this is out of scope for this PR; a separate
   full given-name token pass is a candidate follow-up.

## Literature Context

This plan does not introduce new literature. It corrects the metadata of an
existing bibliographic entry (`Bialecki2023`) using primary sources already in
the audit record: Crossref DOI `10.1038/s41597-023-02510-7` and arXiv
`2207.03428`, both confirmed concordant by the prior reviewer-adversarial gate.
No new references are added. No chapter prose is edited.

## Open Questions

- None blocking execution. The corrective premise is confirmed by two concordant
  primary sources (Crossref + arXiv); no dataset erratum or alternative bib
  convention is known to defend the pre-edit state.
- The PR number placeholder (`#NNN`) in CHANGELOG `[3.61.0]` will be filled at
  PR creation time; this is intentional.

---

## Execution Steps

### T01 — Branch first (master guard hook blocks writes on master)

1. Verify `git rev-parse HEAD` == `3238addb8d01b6baa7d642384e0d4f28e249f481` and
   `git branch --show-current` == `master`.
2. `git checkout -b docs/thesis-bialecki2023-author-correction`.
3. Confirm `git branch --show-current` == `docs/thesis-bialecki2023-author-correction`.

### T02 — thesis/references.bib (+1/−1)

In `thesis/references.bib` line 6, replace the exact substring:

```
Dobrowolski, Piotr and Białecki, Paweł
```

with:

```
Dobrowolski, Paweł and Białecki, Piotr
```

Change NOTHING else. `git diff thesis/references.bib` must be exactly one line,
+1/−1. Key, title, journal, volume, number, pages, year, doi, author count,
author order, and the other 6 author names must be byte-identical.

### T03 — thesis/pass2_evidence/bibliography_cleanup_report.md (correct-in-place)

Five load-bearing false sites, all corrected in place. Do NOT delete any
row/heading/line. Do NOT touch L564–565 (fenced Sources block).

**L64 master-table row:** Change the `confidence`/`note`/`action` cells to
reflect: authors 3–4 given-name swap found post-merge; bib edit applied this PR;
prior "matches exactly / keep" was a surname+initial-granularity artifact.

**The `### Bialecki2023` per-field subsection (≈L332–L345):**
- Heading: `### Bialecki2023 (reviewer-deep nit 3) — confidence 95 — action keep — NO bib edit`
  → change to `action bib_edit_applied (POST-MERGE CORRECTION)`.
- `authors (ordered, 8)` table row (≈L338): show pre-edit bib had positions 3–4
  as `Dobrowolski, Piotr` / `Białecki, Paweł` while Crossref+arXiv give
  `Dobrowolski, Paweł` / `Białecki, Piotr`; `match? → no (pre-edit); corrected
  this PR`.
- Prose (≈L341–345): rewrite to state the bib edit was applied and explain the
  **root cause at this site**: #225 verified surname + count + order but never
  compared given-name tokens; `Piotr`/`Paweł` both collapse to "P." under
  initial-only matching, so the swap and the reviewer-adversarial pass that
  trusted it were blind to it. Keep the venue/year/doi rows (correctly "yes").

**L508–513 "Audit-only assertion" block:** Correct ONLY the `Bialecki2023`
clause to state an edit WAS applied this PR (authors 3–4). Leave
`Glickman2025`/`Glickman1995`/`Wu2017`/`Dimitriadis2024`/`Elo1978`/`Buro2003`
statements byte-unchanged.

**C5 item (≈L546–552):** Rewrite from "Deferred / no edit" to an
applied-correction statement (authors 3–4 given-name swap fixed), explicitly
noting the prior C5 "no edit / matches exactly" was a surname+initial-
verification artifact. Do NOT touch C1/C2/C3/C4/C6.

**Writer-thesis marker:** In the existing "Stale prior-audit statements
superseded" section (search for that heading; it discusses Dimitriadis2024),
insert on its own line at the END of that section:

```
<!-- WRITER-THESIS: INSERT Bialecki2023 post-merge corrective/superseded note HERE -->
```

Do not write the prose note. No DOI/URL in prose anywhere (DOIs stay only in
the L564–565 fenced block). L564–565 kept VERBATIM.

### T04 — CHANGELOG.md ([3.61.0] supersedes, does NOT retro-edit [3.60.0])

Add a new `## [3.61.0] — 2026-05-19 (PR #NNN: docs/thesis-bialecki2023-author-correction)`
section immediately above `## [3.60.0]`. Leave `[Unreleased]` empty with the
4 headers (Added/Changed/Fixed/Removed). Under **Fixed**:
- State the `Bialecki2023` authors 3–4 correction (`Dobrowolski, Piotr` /
  `Białecki, Paweł` → `Dobrowolski, Paweł` / `Białecki, Piotr`) per concordant
  Crossref `10.1038/s41597-023-02510-7` + arXiv `2207.03428`.
- Explicitly state this supersedes the now-falsified `[3.60.0]` statement
  "Bialecki2023 official author list already matches the bib" — name the version
  (`[3.60.0]`) — which was wrong because the #225 audit and the inheriting
  reviewer-adversarial pass verified only at surname+initial granularity (Piotr &
  Paweł both → "P.").
- State that five load-bearing false statements in the cleanup report were
  corrected in place (lineage preserved; none deleted).
- Use literal `#NNN` placeholder for the PR number.

DO NOT modify the historical `[3.60.0]` block — it stays byte-unchanged and is
superseded, not rewritten.

### T05 — pyproject.toml

Change `version = "3.60.0"` to `version = "3.61.0"`. Nothing else.

### T06 — planning/INDEX.md

1. Add a new Archive-table row (replicate existing column format):
   `| docs/thesis-bibliography-canonicalization | 2026-05-18 | F | bib-only canonicalization — Wu2017 dedup, Elo1978→@book, Buro2003→@inproceedings, Dimitriadis2024 metadata + cleanup report | current_plan.md | #225 (merged 2026-05-19 at master 3238addb) |`
2. Replace the `## Active plan` content with:
   `- docs/thesis-bialecki2023-author-correction (2026-05-19) — Category F bib-only: Bialecki2023 authors 3–4 post-merge correction overturning #225's surname+initial-blind "no edit" conclusion; concordant Crossref + arXiv; 5 load-bearing report statements corrected in place (lineage preserved); CHANGELOG [3.61.0] supersedes [3.60.0]`

Leave the Agent-routing table and all other archive rows unchanged.

### T07 — Write planning artifacts

Write `planning/current_plan.md` (this file) with the full Category F plan.
Write `planning/current_plan.critique.md` with the Round-1 reviewer-adversarial
critique verbatim. Round 2 (FINAL gate) will be APPENDED later under a distinct
heading — do not add a Round-2 placeholder.

### Commit

Write commit message to `.github/tmp/commit.txt`, then
`git commit -F .github/tmp/commit.txt`. Stage only the 7 intended files.
Do NOT push. Do NOT create a PR.

---

## File Manifest

| File | Change |
|------|--------|
| `thesis/references.bib` | +1/−1: authors 3–4 given-name swap corrected |
| `thesis/pass2_evidence/bibliography_cleanup_report.md` | 5 false sites corrected in place + writer-thesis marker inserted |
| `CHANGELOG.md` | `[3.61.0]` section added; `[3.60.0]` unchanged |
| `pyproject.toml` | version `3.60.0` → `3.61.0` |
| `planning/INDEX.md` | Archive row added; Active plan replaced |
| `planning/current_plan.md` | This file (plan artifact) |
| `planning/current_plan.critique.md` | Round-1 reviewer-adversarial critique |

---

## Gate Condition

**Reviewer-adversarial FINAL gate is mandatory** — this PR overturns a prior
adversarial-confirmed conclusion. A separate Round-2 pass appends to
`planning/current_plan.critique.md` under a distinct heading.

No `.py` files changed → no pytest/ruff/mypy gate required.

PR left NOT merged pending the FINAL gate and explicit user approval.

---

## Out of Scope / Forbidden Paths

- `thesis/chapters/**` — READ-ONLY
- `thesis/reviews_and_others/**` — READ-ONLY
- `src/**`, `tests/**`, `notebooks/**`, `data/**` — zero diff
- No key rename in `thesis/references.bib`
- No citation-site edits anywhere
- No edits to other `references.bib` entries
- No retro-edit of CHANGELOG `[3.60.0]`

---

## Deliverables

1. `thesis/references.bib` with corrected `Bialecki2023` author line (+1/−1).
2. `thesis/pass2_evidence/bibliography_cleanup_report.md` with 5 false sites
   corrected in place and the writer-thesis marker inserted.
3. `CHANGELOG.md` with `[3.61.0]` superseding `[3.60.0]` (historical entry
   preserved byte-unchanged).
4. `pyproject.toml` at version `3.61.0`.
5. `planning/INDEX.md` with archive row + updated active plan line.
6. `planning/current_plan.md` (this file).
7. `planning/current_plan.critique.md` (Round-1 critique).
8. One atomic commit on branch `docs/thesis-bialecki2023-author-correction`.
