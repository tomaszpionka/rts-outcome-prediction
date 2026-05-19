---
title: "Canonicalize references.bib + bibliography cleanup report"
category: F
branch: docs/thesis-bibliography-canonicalization
base_ref: e095025a76660873c3bbff2c83377044ed095283
date: 2026-05-18
planner_model: claude-opus-4-7[1m] (planner-science) + user-directed amendments 2026-05-18
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/references.bib
  - thesis/chapters/01_introduction.md
  - thesis/reviews_and_others/related_work_historical_rts_prediction.md
  - thesis/reviews_and_others/related_work_rating_systems.md
  - thesis/pass2_evidence/literature_verification_log.md
  - thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md
critique_required: false
research_log_ref: null
---

# Plan: Bibliography canonicalization — references.bib single-source + cleanup report

> **User-directed reviewer deviation (binding, mirrors PR #221–#224).**
> Category-F bibliography-hygiene PR on the highest-sensitivity thesis
> file. reviewer-deep is the mandatory gate (T01 plan + T03 final);
> reviewer-adversarial is conditional (escalation triggers in §"Reviewer
> routing"). `critique_required: false` reflects "no mandatory
> pre-execution adversarial critique", substituted by a mandatory
> reviewer-deep plan review (user Q5 = reviewer-deep + adversarial
> conditional).

> **User decisions (2026-05-18, binding) — resolved Open Questions:**
> - **Q1 = C (bib-only).** Corrections only in `thesis/references.bib`
>   + the new report. `thesis/chapters/**` AND the
>   `thesis/reviews_and_others/**` markdown appendixes are **read-only**
>   this PR. The full `oldkey → canonical` alias-remap list is
>   documented in the report as material for a SEPARATE, separately
>   approved follow-up PR. ZERO chapter/appendix edits.
> - **Mandatory-fix list amended to ADD `Bialecki2023`** — user states
>   its author metadata does not match the official *Scientific Data*
>   record; T02 web-verifies the author list; T03 fixes
>   `references.bib` ONLY if confirmed at ≥80, else `action=verify`
>   (no bib edit).
> - **Q3 = `Dimitriadis2024` verify-first / identity-first (NOT the
>   planner's earlier fields/full).** There is a record-identity
>   collision: in this repo `Dimitriadis2024` denotes *"Evaluating
>   probabilistic classifiers: The triptych"* (IJF 40(1):189–210),
>   used consistently by `references.bib`, Chapter 3, the
>   `rating_systems` appendix, and the prior verification log — NOT a
>   paper about "calibration-loss dominance in comparative backtests".
>   The Crossref DOI `10.1016/j.ijforecast.2023.09.007` →
>   IJF 40(3):1101–1122 the planner found **may be a different
>   Dimitriadis paper**. Procedure (binding): (1) resolve whether
>   `Dimitriadis2024` stays the "triptych" record; (2) if yes, correct
>   it to the published version of *that* (triptych) paper; (3) if the
>   calibration-loss-dominance paper should also enter the bibliography,
>   add it as a **NEW key**, never overwrite `Dimitriadis2024`;
>   (4) **until the identity collision is closed at ≥80, set
>   `action=verify` and make NO `references.bib` edit for this key.**
> - **Q4 = report + separate PR (appendixes read-only this PR).** The
>   report explicitly lists concrete appendix follow-up fixes for a
>   separate approved PR. **`Herbrich2007` is NOT framed as a definite
>   factual date correction** — it is canonical-key / normalization
>   drift (appendix `Herbrich2007` vs central bib `Herbrich2006`); the
>   year 2007 is bibliographically defensible (official Microsoft
>   Research page lists the paper as "Advances in Neural Information
>   Processing Systems 20 | January 2007"). The follow-up PR may
>   normalize the appendix key/style, not assert a year error.
> - **Q5 = reviewer-deep gate + adversarial conditional** (above).

## Scope

Make `thesis/references.bib` the single canonical bibliographic source,
within a strictly **bib-only** PR. Produce one new audit artifact
`thesis/pass2_evidence/bibliography_cleanup_report.md` (full per-key
table, live Crossref/publisher verification, the four user-named-pair
true-state analysis, the alias-remap list, the manual-decision list,
the bib↔markdown drift list, the schema-change specifics, a section
marking stale prior-audit statements as superseded, and a candidate
appendix-follow-up-PR list). Apply ONLY ≥80-confidence,
identity-safe corrections to `references.bib`. ZERO edits to
`thesis/chapters/**` and ZERO edits to `thesis/reviews_and_others/**`
(read-only working materials, user scope #8 + Q1=C + Q4). No key
rename except deleting the byte-identical uncited `Wu2017` duplicate
(verified zero citation sites; re-gated by grep at execution). No
merge until explicit user approval.

## Problem Statement

`references.bib` (107 `@` entries, 1078 lines, master `e095025a`,
v3.59.0) carries metadata errors, type mismatches, and one true
intra-bib duplicate; the markdown appendixes carry a parallel,
divergent bibliography that has drifted from the canonical bib. The
user's brief named four "duplicate pairs", seven Crossref-verify keys,
six manual-decision keys, and three schema changes — but on-disk
verification (planner-science, this plan's evidence) shows several of
those keys do not exist in `references.bib` (they are appendix-only
aliases) and one named correction (`Dimitriadis2024`) carries a
record-identity collision. The PR must canonicalize the bib
**without** propagating any unverified or mis-identified record into
the thesis's single source of truth, and **without** touching chapter
prose or the working-material appendixes (consistent with the entire
#220–#224 no-chapter-edit discipline).

## Assumptions & unknowns

Verified at plan time (planner-science + parent probe):
- Master `e095025a` clean; `references.bib` = 107 `@` / 1078 lines;
  v3.59.0.
- **One real intra-bib duplicate:** `Wu2017` ≡ `Wu2017MSC`
  byte-identical; `Wu2017` cited **0×** under `thesis/`,
  `Wu2017MSC` cited 7×. Falsifier: if execution grep finds any
  `[Wu2017]` site, the deletion is blocked (gate).
- **Three "pairs" are NOT bib merges:** `Baek2022`, `Porcpine2020`,
  `Herbrich2007` are absent from `references.bib`; appendix-only
  aliases of canonical bib keys (`BaekKim2022`, `Porcpine2020EloAoE`,
  `Herbrich2006`); zero `thesis/chapters/` sites.
- **`SC-Phi2`, `BT2025Survey` are not bibkeys.** `SC-Phi2` = user
  label for `Khan2024SCPhi2` (present; Crossref-confirmed).
  `BT2025Survey` = appendix-only grey-literature → manual decision.
- **Unknown — `Dimitriadis2024` record identity:** the bib/Chapter-3
  usage = "triptych" (IJF 40(1):189–210); whether the Crossref DOI
  `10.1016/j.ijforecast.2023.09.007` (40(3):1101–1122, +Vogel) is the
  SAME work or a DIFFERENT Dimitriadis paper is UNRESOLVED → T02
  resolves identity-first; until closed at ≥80, NO bib edit
  (`action=verify`).
- **Unknown — `Bialecki2023` author list:** user asserts it does not
  match the official *Scientific Data* record (DOI
  `10.1038/s41597-023-02510-7`); planner's Crossref pass confirmed
  venue/year only. T02 web-verifies the author list; fix only if ≥80.
- **Unknown — `Glickman1995` primary source:** *American Chess
  Journal* not DOI-indexed; T02 attempts ≤3 web formulations; if no
  ≥80 source, leave `@unpublished` + `verify` (NO fabrication).
- **Unknown — `Glickman2025` appendix second-author typo:** user
  flags a typo in the `rating_systems` appendix's `Glickman2025`
  entry; the central bib `Glickman2025` is Crossref-confirmed correct;
  the appendix typo is catalogued (appendix read-only this PR).

## Literature context

Not primary-source research; bibliographic-metadata canonicalization.
Quality rules (user-stated, binding): prefer Crossref → publisher page
→ PubMed/PMC → official site; **if confidence < 80, do NOT auto-overwrite
the record — `action=verify`**; in the report's prose, NO raw URLs
outside fenced code blocks. Crossref/publisher verification performed
at plan time (planner-science) — reused, not re-derived, except the
two newly-flagged items (`Bialecki2023` author list; `Dimitriadis2024`
identity) which T02 web-verifies fresh:

```
https://api.crossref.org/works/10.3390/ai5040115                          -> Khan2024SCPhi2: AI 5(4):2338-2352, 2024 (matches bib; "SC-Phi2" = user label, NOT a bibkey)
https://api.crossref.org/works/10.1007/s42979-022-01660-6                 -> Bahrololloomi2023: SN Comp Sci 4(3) art.238, 2023 (bib correct)
https://api.crossref.org/works/10.1146/annurev-statistics-040722-061813   -> Glickman2025: Annu Rev Stat 12:259-282, 2025 (central bib correct; appendix copy has a 2nd-author typo — catalogued)
https://api.crossref.org/works/10.1038/s41597-023-02510-7                 -> Bialecki2023: Scientific Data 10 art.600, 2023 (venue/year OK; AUTHOR list NOT yet confirmed -> T02 verifies vs official record)
https://api.crossref.org/works/10.1016/j.ijforecast.2023.09.007           -> Dimitriadis2024 IDENTITY UNRESOLVED: this DOI's record vs the repo's "triptych" usage (IJF 40(1):189-210) -> T02 identity-first
```

`Mangat2024` (J. Gambling Studies 40(2):893–914, DOI
`10.1007/s10899-023-10256-5`) and `Novak2025` (Frontiers Sports Act.
Living 7:1636823, DOI `10.3389/fspor.2025.1636823`, first author Pál)
were corrected & web-verified in PR #222 — reuse that evidence
(`literature_verification_log.md` / the citation audit); re-confirm
present-and-correct on master, expect NO change. `[OPINION]`: the
highest-value safety property here is identity-before-overwrite — a
mis-identified canonical-bib record is worse than a known-incomplete
one; hence the verify-first defaults.

## Report table design

`thesis/pass2_evidence/bibliography_cleanup_report.md` carries one
master table, columns EXACTLY:

```
| key | source_file | entry_type | title | authors | year | venue | doi | url | status | relevance | confidence | note | action |
```

- `confidence` ∈ 0–100. `action` ∈ `{keep, fix_metadata,
  merge_into:<key>, schema_change:<type>, verify, manual_decision,
  flag_bib_vs_md_drift}`. `status` ∈ `{ok, metadata_mismatch,
  type_mismatch, intra_bib_dup, bib_md_alias_drift, appendix_only,
  label_not_bibkey, identity_collision}`.
- One row per `(key, source_file)`; 107 `references.bib` rows + the
  markdown-extracted rows for every named/alias/flagged key. Executor
  records the exact total in the report header (counted from the
  extraction — NOT invented).

The report additionally contains, transcribed/derived from this plan:
the four-pair true-state table; the alias-remap list; the
manual-decision list; the bib↔markdown drift list; the schema-change
specifics; per-field Crossref diffs with confidence; a **"Stale
prior-audit statements superseded"** section; a **"Candidate
appendix follow-up PR"** section; a `data-analysis-lineage` Lineage
header (assumption / measurement / sanity check / falsifier /
downstream decision).

### Four user-named "pairs" — verified true state

| user pair | true on-disk state | operation | canonical | alias | remap (report-only) |
|---|---|---|---|---|---|
| `Wu2017`+`Wu2017MSC` | both in bib, byte-identical; `Wu2017` cited 0×, `Wu2017MSC` 7× | **intra-bib dedup** (delete `Wu2017`, gated by zero-citation grep) | `Wu2017MSC` | `Wu2017` (deleted) | `Wu2017 → Wu2017MSC` |
| `BaekKim2022`+`Baek2022` | `Baek2022` NOT in bib (appendix-only, `related_work_historical_rts_prediction.md`); same work; chapters cite `[BaekKim2022]` | bib↔md alias drift (report-only) | `BaekKim2022` | `Baek2022` (appendix) | `Baek2022 → BaekKim2022` |
| `Porcpine2020EloAoE`+`Porcpine2020` | `Porcpine2020` NOT in bib (appendix-only, `related_work_rating_systems.md`); same work | bib↔md alias drift (report-only) | `Porcpine2020EloAoE` | `Porcpine2020` (appendix) | `Porcpine2020 → Porcpine2020EloAoE` |
| `Herbrich2006`+`Herbrich2007` | `Herbrich2007` NOT in bib (appendix-only, year 2007); same TrueSkill NeurIPS-2006 paper; **2007 is defensible — MSR page: "NeurIPS 20, January 2007"** | bib↔md **key/style** drift (report-only; NOT a year-error claim) | `Herbrich2006` (bib) | `Herbrich2007` (appendix) | `Herbrich2007 → Herbrich2006` (key normalization for follow-up PR; NO assertion that 2007 is wrong) |

### Alias remap list (report deliverable; report-only this PR)

```
Wu2017       -> Wu2017MSC          (intra-bib true dup; Wu2017 deleted; 0 citation sites)
Baek2022     -> BaekKim2022        (bib<->md drift; appendix-only alias; follow-up PR)
Porcpine2020 -> Porcpine2020EloAoE (bib<->md drift; appendix-only alias; follow-up PR)
Herbrich2007 -> Herbrich2006       (bib<->md key/style drift; year 2007 defensible; follow-up PR — key normalization, not a date correction)
SC-Phi2      -> Khan2024SCPhi2     (user label, not a bibkey; documentation note only; no bib entry to remap)
```

### Manual-decision list (`action=manual_decision`, NO auto-change)

`BT2025Survey` (appendix-only grey-lit, future-dated arXiv id, no DOI,
uncited in chapters); `Chen2020` (in bib; missing pages/DOI, ambiguous
LNCS volume); `Lee2021Combat` (in bib, complete metadata; relevance
scoping is a human call); `Lin2019NP` (in bib; truncated `and others`
author list); `Vinyals2019` (in bib; truncated `and others` — Nature
long author list, editorial); `Aligulac` (in bib `@misc` year 2026;
grey-lit live site, editorial date convention); `Glickman1995`
(possibly manual if no ≥80 primary source at T02).

### bib↔markdown drift list (report deliverable)

1. `Baek2022` (appendix) ↔ `BaekKim2022` (bib) — same work, divergent key.
2. `Porcpine2020` (appendix) ↔ `Porcpine2020EloAoE` (bib) — same work.
3. `Herbrich2007` (appendix, 2007) ↔ `Herbrich2006` (bib, 2006) —
   same NeurIPS-2006 paper; **key/style + year-style drift, NOT a
   factual error** (2007 defensible per MSR "NeurIPS 20, January 2007").
4. `SC-Phi2` (user label) ↔ `Khan2024SCPhi2` (bib) — label vs bibkey;
   chapters/log use the bibkey correctly.
5. `BT2025Survey` — appendix-only, never in bib/chapters.
6. `Glickman2025` — central bib correct (Crossref); the
   `rating_systems` appendix copy has a **second-author typo**
   (catalogued; appendix read-only this PR).
7. The two appendixes carry standalone divergent BibTeX blocks
   (working materials, scope #8) — catalogued, not reconciled.

### Schema-change specifics (key-stable; zero citation blast radius)

- **`Elo1978`**: `@article` (publisher Arco, no journal) → `@book`,
  `publisher = {Arco Publishing}`, `address = {New York}`, canonical
  two-word title "The Rating of Chess Players, Past and Present".
  Confidence 95; key unchanged.
- **`Buro2003`**: `@article` (journal=IJCAI) → `@inproceedings`,
  `booktitle = {Proceedings of the 18th International Joint Conference
  on Artificial Intelligence (IJCAI)}`, existing `pages = {1534--1535}`
  + `url` preserved. Confidence 92 (WebSearch-confirmed IJCAI-03);
  key unchanged.
- **`Glickman1995`**: `@unpublished` (American Chess Journal v.3,
  1995, pp.59–102). T02 ≤3 web formulations for a ≥80 primary source;
  if found → `@article` enrich; if NOT → leave `@unpublished` +
  `action=verify` (NO fabrication). Current-entry confidence 60.

**Key-stability:** none of `Elo1978`/`Buro2003`/`Glickman1995` is
renamed; the only deleted key is `Wu2017` (0 citation sites,
re-gated). All `thesis/chapters/` citation sites stay valid.

## Execution Steps

All repo-changing tasks commit AND push. Branch off `e095025a`.
Draft PR at T00; kept draft until reviewer-deep PASS at T03; **NO
merge until explicit user approval**. `.github/tmp/commit.txt` +
`git commit -F`; `.github/tmp/pr.txt` + `--body-file`; delete after;
relative paths; no `.py` in diff ⇒ no pytest gate.

### T00 — Branch + full plan + INDEX archive #224 + draft PR
**Objective:** PR-first scaffold; planning-drift-complete plan.
**Instructions:** branch off `e095025a` (done); write this plan to
`planning/current_plan.md` (EXACT planning-drift headings; `##
Literature context` has NO parenthetical — the PR #223 defect);
`planning/INDEX.md` — archive merged PR #224, set this branch active;
commit via `.github/tmp/commit.txt` + `git commit -F`
(`chore(pr): bootstrap draft PR for bibliography canonicalization`);
push `-u`; `gh pr create --draft --title "docs(thesis): canonicalize references.bib + bibliography cleanup report" --body-file .github/tmp/pr.txt`; delete `.github/tmp/*.txt`.
**Verification:** `gh pr view --json isDraft` → true; planning-drift
hook passes; `git show --stat HEAD` = only `planning/current_plan.md`
+ `planning/INDEX.md`.
**File scope:** `planning/current_plan.md`, `planning/INDEX.md`,
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent.

### T01 — reviewer-deep plan gate (HALT on blocker)
**Objective:** validate the amended plan before any extraction/edit.
**Instructions:** Dispatch `@reviewer-deep` with
`planning/current_plan.md` + base_ref `e095025a`. Checks:
(a) Q1=C bib-only scope structurally bound — File Manifest/per-task
File scope/Gate cannot produce a `thesis/chapters/**` or
`thesis/reviews_and_others/**` edit; (b) `Dimitriadis2024` is
identity-first — the plan does NOT bake the planner's earlier Crossref
40(3) values into a bib edit; default is `action=verify`, no bib edit
until the identity collision is closed at ≥80 in T02; (c)
`Bialecki2023` is verify-then-fix-only-if-≥80 (no blind overwrite);
(d) `Wu2017` deletion is gated on an execution `grep -rno "\[Wu2017\]"
thesis/` == 0; (e) `Elo1978`/`Buro2003` schema changes preserve keys
(zero blast radius); (f) `Glickman1995` no-fabrication verify;
(g) `Herbrich2007` is framed as key/style drift, NOT a year-error
correction (2007 defensible, MSR "NeurIPS 20, January 2007");
(h) report content complete incl. stale-prior-audit-superseded section
+ Glickman2025 appendix typo + appendix-follow-up-PR list;
(i) planning-drift exact headings; (j) URL-discipline rule present.
HALT on methodology/source-scope/overclaim BLOCKER → surface to user,
amend only on user direction, re-review. If reviewer output committed
→ `planning/current_plan.critique.md`, commit, push.
**Verification:** reviewer-deep verdict; 0 unresolved BLOCKERs.
**File scope:** `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** `planning/current_plan.md`. **Push:** yes if committed.

### T02 — Generate bibliography_cleanup_report.md (audit-only; web-verify the two new items)
**Objective:** the full audit artifact + fresh web verification of the
two newly-flagged items; **NO `references.bib` edit** (audit-only;
non-batching rule — canonical bib not mutated in the same step as the
audit).
**Instructions:**
1. Extract every `@`-entry from `references.bib` (107) + every
   markdown reference-list line / embedded BibTeX block from the 5
   scoped files for every named/alias/flagged key.
2. Build the 14-column master table; record the actual row count in
   the report header (counted, not invented).
3. **Web-verify (parent/Opus — read-only) the two new items:**
   - `Bialecki2023`: fetch the official *Scientific Data* record (DOI
     `10.1038/s41597-023-02510-7`) + Crossref; produce the full
     verified author list; per-field diff vs the current bib `author`;
     confidence. (≥80 → T03 fixes; <80 → `action=verify`, no edit.)
   - `Dimitriadis2024` **identity-first**: determine whether the
     repo's `Dimitriadis2024` ("triptych", IJF 40(1):189–210) and the
     Crossref DOI `10.1016/j.ijforecast.2023.09.007`
     (40(3):1101–1122, +Vogel) are the SAME work or two distinct
     Dimitriadis papers. Record the resolution + evidence + a per-field
     diff. If SAME and the published "triptych" metadata is confirmed
     at ≥80 → record the exact corrective values for T03. If DISTINCT
     → `Dimitriadis2024` stays the triptych record; the
     calibration-loss-dominance paper is a separate-key candidate
     (manual decision, NOT auto-added); `action=verify` for the bib
     key. If unresolved at ≥80 → `action=verify`, NO bib edit.
   - `Glickman1995`: ≤3 web formulations for a ≥80 primary source;
     record found/not-found (no fabrication).
   - `Glickman2025`: confirm the central bib is correct (Crossref) and
     catalogue the `rating_systems` appendix second-author typo
     (appendix read-only — catalogue only).
4. Transcribe: the four-pair true-state table, the alias-remap list,
   the manual-decision list, the bib↔markdown drift list, the
   schema-change specifics, per-field Crossref diffs+confidence.
5. Add a **"Stale prior-audit statements superseded"** section: e.g.
   the prior `literature_verification_log.md` / citation audit
   carried `Dimitriadis2024` = IJF 40(1):189–210 with no DOI — mark
   it `under-verification / superseded-pending-identity-resolution`
   (do NOT assert the new values are correct until identity closed);
   any other stale statement found.
6. Add a **"Candidate appendix follow-up PR"** section listing the
   concrete (separate-PR) appendix normalizations: `Baek2022 →
   BaekKim2022`, `Porcpine2020 → Porcpine2020EloAoE`, `Herbrich2007`
   → align to canonical key/style (NOT a year correction — 2007
   defensible), `Glickman2025` appendix second-author typo, optional
   dedup of the embedded BibTeX blocks.
7. URL discipline: every URL/DOI ONLY inside fenced code blocks;
   verify `grep -nE 'https?://|doi:' the_report` — every hit inside a
   fence.
8. Lineage header (assumption / measurement / sanity check /
   falsifier / downstream decision).
9. Commit (`docs(thesis): add bibliography_cleanup_report.md
   (audit-only)`); push. **Audit-only — assert in the report that
   `references.bib` was NOT edited in this step.**
**Verification:** report exists; 14 named columns; header row count =
extraction; URL-discipline grep clean (all fenced); contains the
four-pair table, remap list, manual-decision (≥6), drift list (≥6),
schema specifics (3), per-field Crossref diffs, the
stale-prior-audit-superseded section, the appendix-follow-up section;
`git diff 855... ` ⊄ — `git diff --name-only e095025a..HEAD` shows NO
`references.bib`, NO `thesis/chapters/**`, NO `thesis/reviews_and_others/**`.
**File scope:** `thesis/pass2_evidence/bibliography_cleanup_report.md`,
`.github/tmp/*`. **Read scope:** the 6 source files + WebFetch/WebSearch
for the 2 new items. **Push:** yes. **Executor:** **parent/Opus** for
the web-verification + identity adjudication (subtle source-semantics
judgement per data-analysis-lineage); report transcription is
mechanical.

### T03 — Apply evidence-safe references.bib corrections + reviewer-deep final
**Objective:** apply ONLY ≥80-confidence, identity-safe corrections;
then reviewer-deep final gate on the full diff.
**Instructions:**
1. **Wu2017 dedup:** `grep -rno "\[Wu2017\]" thesis/` MUST be 0
   (re-verify NOW — gate). If 0: delete the entire `@article{Wu2017,
   …}` block (do not touch `Wu2017MSC`). If >0: HALT, report (do not
   delete).
2. **Elo1978 → @book**, **Buro2003 → @inproceedings**: replace per
   §"Schema-change specifics" (keys unchanged).
3. **Bialecki2023:** if T02 confirmed the official author list at
   ≥80, correct the `author` field to the verified list; else leave
   unchanged + ensure the report row is `action=verify` (NO edit).
4. **Dimitriadis2024:** apply a bib edit **ONLY** if T02 closed the
   identity collision at ≥80 AND resolved it to "triptych" with a
   confirmed published correction for *that* paper. Default (identity
   unresolved or distinct) = **NO `references.bib` edit**;
   `action=verify` stands in the report; the calibration-loss paper,
   if relevant, is recorded as a NEW-key manual-decision candidate
   (not added here).
5. **Glickman1995:** enrich to `@article` ONLY if T02 found a ≥80
   primary source; else leave `@unpublished` + `verify`.
6. Update the report "Applied" section (lineage closure): exactly
   which rows were applied vs deferred-to-manual vs verify-unresolved
   — report final state must mirror bib final state.
7. Re-run key probe + `grep -c '^@'`: expected `@` = **106** (107 − 1
   `Wu2017`) IF Wu2017 deleted (else 107); every other named key
   count unchanged; `Wu2017` 0 / `Wu2017MSC` 1. BibTeX
   well-formedness: `source .venv/bin/activate && poetry run python -c`
   brace/parse check (read-only validation; no committed test).
8. Commit (`docs(thesis): apply evidence-safe references.bib
   corrections [bib-only]`); push.
9. Dispatch **@reviewer-deep** final with `planning/current_plan.md`
   + base_ref `e095025a` + full branch diff. Verifies: only manifest
   files changed; ZERO `thesis/chapters/**` / `thesis/reviews_and_others/**`
   edits; `references.bib` well-formed, expected `@` count, no
   orphaned citation (`[Wu2017]` resolves to 0 sites and Wu2017MSC
   intact); `Dimitriadis2024` NOT silently overwritten if identity
   open; `Bialecki2023` only changed if ≥80-confirmed; report
   "Applied" section matches bib final state; URL discipline; no
   overclaim. Escalate to `@reviewer-adversarial` ONLY on an
   unresolved overclaim/methodology BLOCKER (triggers in §"Reviewer
   routing"); 3-round symmetric cap. Apply only mechanical in-scope
   fixes; substantive residual → record + surface to user. Commit +
   push if changed.
**Verification:** `grep -c '^@' thesis/references.bib` = 106 (or 107
if Wu2017 retained by gate); `grep -c '{Wu2017,'` = 0 & `{Wu2017MSC,'`
= 1 (if deleted); `grep -rno "\[Wu2017\]" thesis/` = 0;
`@book{Elo1978,` = 1; `@inproceedings{Buro2003,` = 1;
`Dimitriadis2024` unchanged unless identity-closed; `git diff
--name-only e095025a..HEAD` ⊆ manifest, zero chapters/appendix;
reviewer-deep final PASS, 0 unresolved BLOCKERs.
**File scope:** `thesis/references.bib`,
`thesis/pass2_evidence/bibliography_cleanup_report.md` (Applied
section), `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** report, plan, full diff. **Push:** yes. **Executor:**
**@executor on Opus** for the bib edits (canonical-bib edit +
identity/≥80 judgement = data-analysis-lineage "subtle source
semantics" branch); reviewer-deep is the gate.

### T04 — Version bump 3.59.0 → 3.60.0 + CHANGELOG
**Objective:** repo-policy bookkeeping (`docs/` ⇒ minor).
**Instructions:** `pyproject.toml` `3.59.0` → `3.60.0`; CHANGELOG
`[Unreleased]` → `## [3.60.0] — 2026-05-18 (PR #<n>:
docs/thesis-bibliography-canonicalization)` with `### Added` (the
report) + `### Fixed`/`### Changed` describing the ACTUAL applied
corrections (Wu2017 dedup if grep-clean; Elo1978/Buro2003 schema;
Bialecki2023 author only if ≥80-confirmed; Dimitriadis2024
identity-first → verify-only if collision open, no bib edit) + a note
that bib↔markdown alias drift (Baek2022/Porcpine2020/Herbrich2007 —
key/style, 2007 defensible) is catalogued for a separate approved PR;
no chapter/appendix edit; fresh empty `[Unreleased]` 4 headers;
`[3.59.0]` untouched. `<n>` from `gh pr view --json number`. Commit
`chore(release): bump version to 3.60.0`; push.
**Verification:** `pyproject.toml`=3.60.0; CHANGELOG `[Unreleased]`
empty 4 headers; `[3.60.0]` entry; `[3.59.0]` untouched.
**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** @executor Sonnet.

### T05 — PR body refresh + mark ready (NO merge until user approval)
**Objective:** finalize for review without merging; conditional
stale-critique purge.
**Instructions:** reconcile PR-number placeholder in
`planning/INDEX.md` active line + CHANGELOG `[3.60.0]` header.
**Conditional stale-critique purge:** delete
`planning/current_plan.critique_resolution.md` (a long-merged-plan
residual) ONLY with reviewer-deep concurrence at T03 — if concurred,
add to the File Manifest and delete here; else leave. Refresh
`.github/tmp/pr.txt` per `.github/pull_request_template.md` (Summary:
Q1=C bib-only; what was actually corrected vs verify-deferred — esp.
`Dimitriadis2024` identity-first verify-only and `Bialecki2023`
conditional; report added; alias-drift catalogued for separate PR;
chapters/appendixes read-only; Test plan: report 14-col + URL
discipline + `@` count + zero-chapter/appendix diff + reviewer-deep
PASS T01+T03 + v3.60.0). `gh pr edit --body-file`; `gh pr ready` only
after T03 reviewer-deep PASS. **Do NOT `gh pr merge` — merge awaits
explicit user approval.** Delete `.github/tmp/*.txt`; produce final
report.
**Verification:** `gh pr view --json isDraft` → false; `state` OPEN,
NOT merged. **File scope:** `planning/INDEX.md`, `CHANGELOG.md`,
`planning/current_plan.critique_resolution.md` (conditional delete),
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent.

## Reviewer routing

- **T01 (plan) + T03 (final): reviewer-deep — mandatory.** Mirrors
  PR #222 (references.bib, reviewer-deep gated) + the #220–#224 chain.
  `critique_required: false` with the user-directed-deviation note.
- **reviewer-adversarial escalation trigger (any one → adversarial for
  that gate):** (1) reviewer-deep raises a methodology/overclaim
  BLOCKER unresolved in ≤3 rounds; (2) a `references.bib` edit is
  proposed for `Dimitriadis2024` while the identity collision is NOT
  closed at ≥80 (identity-overwrite = overclaim); (3) a `Bialecki2023`
  author overwrite is proposed below ≥80 confidence; (4) any
  `thesis/chapters/**` or `thesis/reviews_and_others/**` edit appears
  in the diff (scope breach — Q1=C forbids it); (5) the report frames
  `Herbrich2007` as a definite factual year error rather than
  key/style drift. Otherwise NOT invoked.
- **3-round symmetric cap** (execution-side too); unresolved after
  round 3 → halt + surface to user; do not loop.

## Repo-policy resolutions

1. **Version bump:** `docs/` ⇒ minor; 3.59.0 → 3.60.0 (T04).
2. **Markdown appendixes + chapters read-only (Q1=C, Q4, scope #8):**
   `thesis/reviews_and_others/**` and `thesis/chapters/**` are NEVER
   edited this PR; drift catalogued + follow-up-PR candidates listed
   in the report only.
3. **planning/INDEX.md (T00):** archive merged PR #224, set this
   branch active.
4. **Stale-critique residual:** `planning/current_plan.critique.md`
   is overwritten in T01 by this PR's reviewer-deep output.
   `planning/current_plan.critique_resolution.md` (long-merged-plan
   residual) → T05 conditional delete ONLY with reviewer-deep
   concurrence.
5. Commit/PR conventions: `.github/tmp/commit.txt` + `git commit -F`;
   `.github/tmp/pr.txt` + `--body-file`; delete after; relative paths;
   no `.py` ⇒ no pytest gate; the T03 bibtex brace check is a
   read-only `poetry run python -c` validation (no committed test).

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00, T05 |
| `planning/current_plan.critique.md` | Create/overwrite (reviewer-deep provenance) | T01, T03 |
| `thesis/pass2_evidence/bibliography_cleanup_report.md` | Create + Applied-section update | T02, T03 |
| `thesis/references.bib` | Update (Wu2017 delete gated; Elo1978→@book; Buro2003→@inproceedings; Bialecki2023 author IF ≥80; Dimitriadis2024 ONLY IF identity-closed ≥80; Glickman1995 enrich IF ≥80) | T03 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `planning/current_plan.critique_resolution.md` | Delete (CONDITIONAL on reviewer-deep concurrence) | T05 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T02/T03/T04/T05 |

Explicitly NOT modified: `thesis/chapters/**` (all chapter prose +
`REVIEW_QUEUE.md`); `thesis/reviews_and_others/**` (working-material
appendixes); `thesis/WRITING_STATUS.md`; other `thesis/pass2_evidence/**`;
datasets; notebooks; specs; ROADMAPs; status YAMLs; code; raw data;
`docs/TAXONOMY.md`; `.claude/**`.

## Gate Condition

1. `bibliography_cleanup_report.md` exists with the 14 named columns,
   header row count from extraction, four-pair table, alias-remap
   list, manual-decision list (≥6), bib↔md drift list (≥6), schema
   specifics (3), per-field Crossref diffs, stale-prior-audit-superseded
   section, appendix-follow-up-PR section, Lineage header; URL
   discipline (every link fenced).
2. `references.bib`: `Wu2017` deleted IFF `grep -rno "\[Wu2017\]"
   thesis/` == 0 (else retained, reported); `@book{Elo1978,`=1;
   `@inproceedings{Buro2003,`=1; `Dimitriadis2024` byte-unchanged
   unless T02 closed identity at ≥80; `Bialecki2023` author changed
   ONLY if ≥80-confirmed; `Glickman1995` enriched ONLY if ≥80;
   well-formed (brace-balanced; parses); `@` count = 106 (or 107 if
   Wu2017 gate-retained).
3. ZERO `thesis/chapters/**` and ZERO `thesis/reviews_and_others/**`
   in `git diff --name-only e095025a..HEAD`; diff ⊆ File Manifest.
4. Report "Applied" section mirrors the bib's final state exactly
   (lineage closure); every `verify`/`manual_decision` row carries a
   reason; no record asserted "verified" below confidence 80.
5. `Herbrich2007` framed as key/style drift; the report does NOT
   assert 2007 is a factual error (2007 defensible — MSR
   "NeurIPS 20, January 2007").
6. Version 3.60.0; CHANGELOG `[3.60.0]` accurate to the corrections
   actually applied; `[3.59.0]` untouched.
7. reviewer-deep PASS at T01 and T03; reviewer-adversarial only if a
   §"Reviewer routing" trigger fired then resolved (3-round cap).
8. `planning/INDEX.md`: PR #224 archived, this branch active,
   PR-number reconciled. PR ready (`isDraft` false), **NOT merged**
   (merge awaits explicit user approval); temp files deleted.

## Out of scope

- Any `thesis/chapters/**` edit; any `thesis/reviews_and_others/**`
  edit (Q1=C, Q4, scope #8 — appendixes are working materials).
- Any chapter-citation `[oldkey]→[canonical]` rewrite (Q1≠B; deferred
  to a separate approved follow-up PR documented in the report).
- Adding the calibration-loss-dominance paper as a new bibkey (manual
  decision; recorded as a candidate, not added).
- Overwriting `Dimitriadis2024` while its record-identity collision is
  open; overwriting `Bialecki2023` author below ≥80; fabricating
  `Glickman1995` metadata.
- Asserting `Herbrich2007`→2006 as a factual year correction.
- Re-opening PR #222 (Ch1-footer econ keys already in bib); Phase 03 /
  AoE2 Phase 02 / dataset artifacts / notebooks / specs / ROADMAPs /
  status YAMLs / code / `docs/TAXONOMY.md` / `.claude/**`.
- Merging the PR (awaits explicit user approval).

## Open questions

- **Q1 — RESOLVED (user 2026-05-18): C, bib-only.** Chapters +
  appendixes read-only; alias remap documented for a separate PR.
- **Q2 — RESOLVED:** branch `docs/thesis-bibliography-canonicalization`
  (plan approval = branch authorization).
- **Q3 — RESOLVED (user 2026-05-18): `Dimitriadis2024`
  verify-first / identity-first.** No bib edit until the
  triptych-vs-calibration-loss identity collision is closed at ≥80;
  the other paper, if relevant, is a NEW-key candidate, never an
  overwrite.
- **Amendment — RESOLVED (user 2026-05-18):** `Bialecki2023` added to
  the fix-or-verify list (author vs official *Scientific Data*; fix
  only if ≥80, else verify).
- **Q4 — RESOLVED (user 2026-05-18): report + separate PR.**
  Appendixes read-only this PR; `Herbrich2007` is key/style drift
  (2007 defensible), NOT a year-error correction; concrete appendix
  follow-up fixes listed in the report for a separate approved PR.
- **Q5 — RESOLVED (user 2026-05-18): reviewer-deep gate + adversarial
  conditional** (T01 + T03 sufficient unless scope expands beyond the
  canonical bib).
- **R-1 (residual, no decision):** the conditional
  `planning/current_plan.critique_resolution.md` purge is
  reviewer-deep-concurrence-gated at T03/T05.
