---
title: "Chapter-1 footer-only bibliography consolidation into references.bib (Chapters 1–4 audit must-fix M-2)"
category: F
branch: docs/thesis-ch1-footer-bib-consolidation
base_ref: 93f02600df1e5401e5e42cc438fdcd504dc07487
date: 2026-05-18
planner_model: claude-opus-4-7[1m] (planner-science)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md
  - thesis/chapters/01_introduction.md
  - thesis/references.bib
  - thesis/pass2_evidence/literature_verification_log.md
  - thesis/pass2_evidence/methodology_risk_register.md
critique_required: false
research_log_ref: null
---

# Plan: Chapter-1 footer-only bibliography consolidation (must-fix M-2)

> **User-directed reviewer deviation (binding).** M-2 originates from the
> PR #220 Chapters 1–4 citation audit. Per the user task brief, reviewer-deep
> is the mandatory plan gate (T01) and final gate (T03); reviewer-adversarial
> is conditional (escalation trigger only). `critique_required: false`
> reflects "no mandatory pre-execution adversarial critique", substituted by
> a mandatory reviewer-deep plan review. Mirrors PR #221 (M-1).

> **User decisions (2026-05-18, binding):** (1) **Mangat2024 footer
> correction AUTHORISED** — a minimal one-line metadata fix in
> `thesis/chapters/01_introduction.md` footer line 85
> (`40(1), 145-165` → `40(2), 893-914`); NO Chapter-1 prose-body change; the
> transferability `[REVIEW]` hedge (line 11) and the line-85 metadata
> `[REVIEW]` flag are NOT removed unless reviewer-deep explicitly confirms
> resolution. (2) **Recording: WRITING_STATUS append only; no
> REVIEW_QUEUE change.**

## Scope

Bibliography/provenance consolidation. Promote the seven Chapter-1
`## References`-footer-only entries into the central `thesis/references.bib`
with web-verified metadata, and apply one authorised minimal one-line
correction to the Mangat2024 footer entry so footer and bib agree. This
resolves audit must-fix **M-2** (`ch1_ch4_citation_literature_support_audit.md`
§7 M-2, §11 PR-2, §4 C-06, D1-NOTE, §7.1 R-1) so Chapter-1
bibliography/provenance is ready for supervisor handoff. **Bibliography
hygiene, NOT a new theory claim**: zero new prose claims; the transferability
`[REVIEW]` hedge is preserved.

## Problem Statement

Seven keys are cited in Chapter-1 prose and/or listed in the Chapter-1
inline `## References` footer (`01_introduction.md:59`–…) but are absent
from `thesis/references.bib`: `Shin1993`, `Forrest2005`, `Levitt2004`,
`Mangat2024`, `Formosa2022`, `Novak2025`, `Balduzzi2018`. Confirmed absent
at HEAD (`grep -c "{<key>," references.bib` = 0 for all seven;
`grep -c '^@'` = 100). Not a phantom-citation BLOCKER (audit §4 D1) — a
supervisor reading chapter+footer is unaffected — but the central bib is
incomplete for BibTeX typesetting. Additionally, web verification shows the
Chapter-1 footer's `Mangat2024` entry has wrong volume/issue/pages
(`40(1), 145-165`; canonical Springer/PubMed = `40(2), 893-914`,
DOI 10.1007/s10899-023-10256-5); the footer already self-flags this with a
`[REVIEW: … zweryfikować numer tomu/stron]` note. Precedent: PR-TG4
(2026-04-20) already promoted the analogous footer-only `GarciaMendez2025`
into `references.bib`.

## Assumptions & unknowns

- **A1 — all seven absent / no collision.** Verified at plan time (grep,
  all 0). Falsifier: any key present at T02 → drop from add-set, report.
- **A2 — footer carries full starting metadata.** Verified
  (`01_introduction.md:73,75,77,79,81,85,97`). Footer = starting point;
  web confirms/corrects.
- **A3 — none in `literature_verification_log.md`.** Verified (grep, none;
  T14 was Ch3-scoped). Shin1993/Forrest2005 inherit reviewer-deep PR #220
  T03 verified metadata (audit §7.1); the rest are web-verified this PR.
- **A4 — no betting-transfer/source-label risk contradicted.** Verified:
  `methodology_risk_register.md` RISK-01/04/05 concern AoE2
  source-label/population only; a bib-only consolidation + a numeric footer
  fix add no prose claim and cannot strengthen transferability.
- **Unknown (resolved by user):** Chapter-1 footer Mangat2024 one-line
  numeric correction AUTHORISED; Chapter-1 prose body unchanged.

## Literature context

Authoritative scope: audit §11 PR-2 binding constraints — web-verify
metadata (≤3 formulations each); if unverifiable, add with a
`[REVIEW: metadata Pass-2]` note rather than inventing; do NOT assert any
entry "verified" from an abstract; do NOT renumber/restructure other
chapters' citations; preserve existing bibkeys (no renames). Inherited
verified starting points (audit §7.1, reviewer-deep PR #220 T03):
Shin1993 = *The Economic Journal* 103(420):1141–1153 (1993), Hyun Song Shin
(https://academic.oup.com/ej/article-abstract/103/420/1141); Forrest2005 =
*International Journal of Forecasting* 21(3):551–564 (2005),
Forrest/Goddard/Simmons, DOI 10.1016/j.ijforecast.2005.03.003. Planner-stage
web verification (re-confirmed at T02): **Levitt2004** = Steven D. Levitt,
"Why are gambling markets organised so differently from financial markets?",
*The Economic Journal* 114(495):223–246 (2004),
DOI 10.1111/j.1468-0297.2004.00207.x (matches footer); **Mangat2024** =
*Journal of Gambling Studies* **40(2):893–914** (2024; online 2023),
DOI 10.1007/s10899-023-10256-5 (footer's `40(1),145-165` is wrong — gambling
psychology systematic review, NOT odds-pricing, confirms audit C-06);
**Formosa2022** = *Proc. ACM Human-Computer Interaction* 6(CHI PLAY)
Art. 399, 1–45, DOI 10.1145/3549490 (matches footer); **Novak2025**
(*Frontiers in Sports and Active Living* 7:1636823,
DOI 10.3389/fspor.2025.1636823) and **Balduzzi2018** (NeurIPS 2018,
arXiv:1806.02643) confirmed at T02. No `[OPINION]` claim added.

## Definitive footer-only key table

| key | cited in Ch1 prose? | references.bib? | verification routing |
|---|---|---|---|
| Shin1993 | YES (`:11`) | NO | reuse PR#220 T03 + re-confirm (OUP) |
| Forrest2005 | YES (`:11`) | NO | reuse PR#220 T03 + re-confirm (DOI 10.1016/j.ijforecast.2005.03.003) |
| Levitt2004 | YES (`:11`,`:43`) | NO | web-verified (DOI 10.1111/j.1468-0297.2004.00207.x; matches footer) |
| Mangat2024 | YES (inside `:11` `[REVIEW]` hedge) | NO | web-verified — footer DISCREPANT: `40(1),145-165` → canonical `40(2),893-914` |
| Formosa2022 | YES (`:5`) | NO | web-verified (DOI 10.1145/3549490; matches footer) |
| Novak2025 | YES (`:5`) | NO | web-confirm at T02 (Frontiers DOI 10.3389/fspor.2025.1636823) |
| Balduzzi2018 | NO — footer-only (`:97`) | NO | web-confirm at T02 (NeurIPS 2018; arXiv:1806.02643) — in scope (audit M-2/D1-NOTE name it) |

Final add-set = exactly these seven (none present; none dropped). No other
footer-only key found (full footer enumerated; all others resolve in
`references.bib`).

## Chapter-1 change ruling (explicit)

- **Prose body: NO change.** Byte-unchanged.
- **`## References` footer: ONE authorised minimal change** — line 85,
  Mangat2024 only: replace `40(1), 145-165` with `40(2), 893-914`. Nothing
  else on line 85 changes (DOI, author list, title, the
  `[REVIEW: … zweryfikować numer tomu/stron]` flag all kept verbatim). No
  other footer line touched.
- **`[REVIEW]` flags: none removed.** The line-11 transferability hedge and
  the line-85 metadata flag are preserved; reviewer-deep T03 may advise on
  the line-85 flag but execution removes nothing.

## Intended BibTeX entries (house style; appended as dated block)

Appended at end of `references.bib` under
`% === Additions for §1.1 Ch1 footer consolidation (2026-05-18, Pass-2 PR M-2) ===`.
Every field re-confirmed at T02 against the recorded primary source before
writing (no invention; no "verified from abstract"; bare DOI, no
`https://doi.org/` wrapper; author Unicode kept; `--` page ranges).

```bibtex
@article{Shin1993,
  author  = {Shin, Hyun Song},
  title   = {Measuring the Incidence of Insider Trading in a Market for State-Contingent Claims},
  journal = {The Economic Journal},
  volume  = {103}, number = {420}, pages = {1141--1153}, year = {1993},
  doi     = {10.2307/2234240}
}
@article{Forrest2005,
  author  = {Forrest, David and Goddard, John and Simmons, Robert},
  title   = {Odds-setters as forecasters: The case of {English} football},
  journal = {International Journal of Forecasting},
  volume  = {21}, number = {3}, pages = {551--564}, year = {2005},
  doi     = {10.1016/j.ijforecast.2005.03.003}
}
@article{Levitt2004,
  author  = {Levitt, Steven D.},
  title   = {Why are gambling markets organised so differently from financial markets?},
  journal = {The Economic Journal},
  volume  = {114}, number = {495}, pages = {223--246}, year = {2004},
  doi     = {10.1111/j.1468-0297.2004.00207.x}
}
@article{Mangat2024,
  author  = {Mangat, Harshdeep Singh and Griffiths, Mark D. and Yu, Sarah M. and Felvinczi, Katalin and Ngetich, Ronald K. and Demetrovics, Zsolt and Czakó, Andrea},
  title   = {Understanding Esports-related Betting and Gambling: A Systematic Review of the Literature},
  journal = {Journal of Gambling Studies},
  volume  = {40}, number = {2}, pages = {893--914}, year = {2024},
  doi     = {10.1007/s10899-023-10256-5}
}
@article{Formosa2022,
  author  = {Formosa, Jane and O'Donnell, Nicholas and Horton, Ella M. and Türkay, Selen and Mandryk, Regan L. and Hawks, Marcus and Johnson, Daniel},
  title   = {Definitions of Esports: A Systematic Review and Thematic Analysis},
  journal = {Proceedings of the {ACM} on Human-Computer Interaction},
  volume  = {6}, number = {CHI PLAY}, pages = {1--45}, year = {2022},
  doi     = {10.1145/3549490}, note = {Article 399}
}
@article{Novak2025,
  author  = {Novák, Patrik and Hohmann, Balázs and Sipos, Dávid and Szőke, Gergely},
  title   = {The legal and economic aspects of the ``Esports Illusion'': why competitive gaming fails to become an independent industry},
  journal = {Frontiers in Sports and Active Living},
  volume  = {7}, pages = {1636823}, year = {2025},
  doi     = {10.3389/fspor.2025.1636823}
}
@inproceedings{Balduzzi2018,
  author    = {Balduzzi, David and Tuyls, Karl and Pérolat, Julien and Graepel, Thore},
  title     = {Re-evaluating Evaluation},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2018},
  note      = {NeurIPS 2018; preprint arXiv:1806.02643},
  url       = {https://arxiv.org/abs/1806.02643}
}
```

Each `verify@exec`: re-confirm at T02. If a field resists 3 web
formulations → keep footer value + a `% [REVIEW: metadata Pass-2 — <field>;
queries: …]` comment line above the entry (parser-safe). Mangat2024 carries
a `% Mangat2024: Ch1 footer (01_introduction.md:85) gave 40(1),145-165;
Springer/PubMed canonical 40(2),893-914 verified 2026-05-18` comment above
the entry.

## @executor web-tools constraint (resolved)

`@executor` (Sonnet) lacks WebFetch/WebSearch. **T02 web verification is
performed by the PARENT/Opus session**, producing a frozen byte-final
verified-metadata block (the 7 entries + the exact footer old→new string).
The parent hands that frozen block to `@executor` on **Sonnet** for the
purely mechanical append + footer one-liner + WRITING_STATUS append. All
scientific/metadata-correctness judgement (incl. Mangat2024 adjudication and
any `metadata Pass-2` classification) is resolved before delegation
(satisfies the data-analysis-lineage routing rule). Parent-only execution of
T02 is an acceptable alternative.

## Execution Steps

### T00 — Branch + full plan + INDEX archive #221 + draft PR

**Objective:** Bootstrap a planning-drift-complete Cat-F plan.
**Instructions:** branch off `93f02600` (done); write this full plan to
`planning/current_plan.md`; `planning/INDEX.md` — archive merged PR #221,
set this branch active; commit via `.github/tmp/commit.txt` + `git commit -F`
(`chore(pr): bootstrap draft PR for Chapter-1 footer bibliography consolidation [M-2]`);
push `-u`; `gh pr create --draft --title "docs(thesis): consolidate Chapter 1 footer sources into references.bib" --body-file .github/tmp/pr.txt`; delete `.github/tmp/*.txt`.
**Verification:** `gh pr view --json isDraft` → true; planning-drift hook
passes; `git show --stat HEAD` = only `planning/current_plan.md` +
`planning/INDEX.md`.
**File scope:** `planning/current_plan.md`, `planning/INDEX.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** parent (mechanical).

### T01 — reviewer-deep plan review (HALT on blocker)

**Objective:** Validate the plan before any edit.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `93f02600`. Checks: (a) 7 absent / no collision; (b) BibTeX
shapes match house style; (c) Mangat2024 footer+bib both → `40(2),893-914`,
discrepancy comment sound; (d) Chapter-1 prose body unchanged, footer change
limited to the line-85 Mangat2024 numeric tokens, `[REVIEW]` flags
preserved, no betting-transfer claim (RISK-01/04/05 non-contradiction);
(e) @executor-lacks-web-tools resolution sound; (f) WRITING_STATUS-only /
REVIEW_QUEUE-none decisions sound; (g) version 3.56.0→3.57.0; (h)
Balduzzi2018 in scope despite prose-uncited. BLOCKER → HALT, surface to
user, amend only on user direction, re-review. If reviewer output committed
→ `planning/current_plan.critique.md`, commit, push.
**Verification:** reviewer-deep verdict; 0 unresolved BLOCKERs.
**File scope:** `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** `planning/current_plan.md`. **Push:** yes if critique committed.

### T02 — Web-verify + append 7 bib entries + Mangat2024 footer fix + WRITING_STATUS append

**Objective:** Freeze verified metadata (parent/Opus web step), then
mechanically apply the three edits.
**Instructions:**
1. **Web verification (PARENT/Opus — NOT Sonnet executor):** re-confirm
   every field of all 7 entries vs recorded primary source, ≤3 formulations
   each (Shin1993/Forrest2005 via audit §7.1 URLs; Levitt2004/Mangat2024/
   Formosa2022 via plan-recorded DOIs; Novak2025 via Frontiers DOI;
   Balduzzi2018 NeurIPS 2018 + arXiv:1806.02643). Mangat2024 MUST be
   `40(2),893-914`. Unconfirmable field → footer value + `% [REVIEW:
   metadata Pass-2 …]` comment; never invent; never "verified from
   abstract". Freeze the byte-final 7-entry block.
2. **Mechanical (@executor Sonnet, given the frozen block):** append the
   dated block + 7 entries to end of `thesis/references.bib` (append-only;
   no existing entry touched).
3. **Mangat2024 footer one-liner** (`thesis/chapters/01_introduction.md`
   line 85): replace exactly `Journal of Gambling Studies, 40(1), 145-165.`
   with `Journal of Gambling Studies, 40(2), 893-914.` — change ONLY those
   volume/issue/pages tokens; the DOI, author list, title, and the
   `[REVIEW: … zweryfikować numer tomu/stron]` flag stay verbatim; no other
   line/character in `01_introduction.md` changes (prose body byte-unchanged).
4. Append ONE dated line (2026-05-18) to the §1.1 row of
   `thesis/WRITING_STATUS.md` (append only): seven footer-only keys promoted
   to references.bib (M-2/C-06/D1-NOTE resolved for supervisor handoff);
   Mangat2024 footer metadata corrected `40(1),145-165` → `40(2),893-914` to
   match verified canonical (Springer/PubMed, DOI 10.1007/s10899-023-10256-5)
   and the new bib entry; Shin1993/Forrest2005 inherited reviewer-deep
   PR #220 audit §7.1 verified starting points; Chapter-1 prose body
   unchanged; broader betting-market transferability remains an open
   review/caveat (line-11 `[REVIEW]` hedge NOT closed by this metadata
   consolidation).
5. Do NOT touch `REVIEW_QUEUE.md`, Chapter-1 prose body, any other chapter,
   any existing bib entry.
6. Commit via `.github/tmp/commit.txt` + `git commit -F`
   (`docs(thesis): consolidate 7 Chapter-1 footer-only refs into references.bib + fix Mangat2024 footer metadata [M-2]`);
   push.
**Verification (grep battery):**
- For each `k` in the seven: `grep -c "{$k," thesis/references.bib` == 1.
- `grep -c '^@' thesis/references.bib` == 107.
- Mangat2024 bib entry contains `number = {2}` and `893--914`, not `145`.
- `01_introduction.md:85` now reads `… 40(2), 893-914.`; `grep -c "40(1), 145-165" thesis/chapters/01_introduction.md` == 0.
- Chapter-1 prose body byte-unchanged: `git diff 93f02600..HEAD -- thesis/chapters/01_introduction.md` shows ONLY the line-85 Mangat2024 vol/issue/pages tokens changed (one hunk, ≤1 line).
- `grep -c 'REVIEW: Shin1993 i Forrest2005' thesis/chapters/01_introduction.md` unchanged vs base (≥1); `grep -c 'zweryfikować numer tomu/stron' thesis/chapters/01_introduction.md` unchanged vs base (line-85 flag intact).
- **Ch1 bibkey-coverage:** every `[Key]` cited in Ch1 prose resolves in `references.bib` (0 unresolved; was 6).
- `git diff --name-only 93f02600..HEAD` ⊆ {planning/current_plan.md, planning/INDEX.md, planning/current_plan.critique.md, thesis/references.bib, thesis/chapters/01_introduction.md, thesis/WRITING_STATUS.md}.
- `git diff 93f02600..HEAD -- thesis/chapters/REVIEW_QUEUE.md` empty; references.bib diff purely additive.
**File scope:** `thesis/references.bib`, `thesis/chapters/01_introduction.md`
(line 85 only), `thesis/WRITING_STATUS.md`, `.github/tmp/*`. **Read scope:**
those files. **Push:** yes. **Executor:** parent/Opus step 1 (web + freeze);
`@executor` Sonnet steps 2–6 (mechanical). Parent-only acceptable.

### T03 — reviewer-deep final check

**Objective:** Validate the applied diff.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `93f02600`. Verify: (a) exactly 7 new entries, keys exact, no
collision, `^@`==107; (b) each entry's metadata matches its recorded
source; Mangat2024 bib AND footer both `40(2),893-914`; any `metadata
Pass-2` comment justified (no invented values; no "verified from abstract");
(c) house-style conformant; (d) references.bib purely additive; (e)
Chapter-1 prose body byte-unchanged; footer change limited to the line-85
Mangat2024 vol/issue/pages; `[REVIEW]` flags (line 11 transferability hedge;
line 85 metadata flag) NOT removed; no betting-transfer claim
(RISK-01/04/05); (f) Ch1 bibkey-coverage passes (0 unresolved); (g)
WRITING_STATUS §1.1 append additive & accurate; REVIEW_QUEUE untouched and
its §1.1 `Pending` row not moved to Completed; (h) grep battery passes; (i)
scope-diff containment. Escalate to `@reviewer-adversarial` ONLY on an
unresolved overclaim/methodology BLOCKER (trigger list in Reviewer routing);
3-round symmetric cap. Mechanical in-scope fixes only; substantive residual
→ record + surface to user. Commit + push if changed.
**Verification:** reviewer-deep APPROVE; 0 unresolved BLOCKERs.
**File scope:** `thesis/references.bib`, `thesis/chapters/01_introduction.md`,
`thesis/WRITING_STATUS.md`, `planning/current_plan.critique.md`,
`.github/tmp/*`. **Read scope:** diff. **Push:** yes if changed.

### T04 — Version bump 3.56.0 → 3.57.0 + CHANGELOG

**Objective:** Release hygiene.
**Instructions:** `pyproject.toml` `3.56.0` → `3.57.0`; CHANGELOG
`[Unreleased]` → `## [3.57.0] — 2026-05-18 (PR #<n>: docs/thesis-ch1-footer-bib-consolidation)`
with `### Added` (seven Ch1 footer-only refs promoted) + `### Fixed`
(resolves audit must-fix M-2 / C-06 / D1-NOTE central-bib gap; Mangat2024
footer+bib corrected `40(1),145-165` → `40(2),893-914` vs verified canonical;
Chapter-1 prose body unchanged; transferability `[REVIEW]` hedge retained,
not resolved; no new theory claim); fresh empty `[Unreleased]` with 4
headers; `[3.56.0]` (PR #221) untouched. `<n>` from `gh pr view --json number`.
Commit `chore(release): bump version to 3.57.0`; push.
**Verification:** `pyproject.toml`=3.57.0; CHANGELOG `[Unreleased]` empty
4 headers; one Added + one Fixed under `[3.57.0]`; `[3.56.0]` untouched.
**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** @executor Sonnet (mechanical).

### T05 — PR body refresh + mark ready (NO merge)

**Objective:** Finalize without merging.
**Instructions:** reconcile PR-number placeholder in `planning/INDEX.md`
active line + CHANGELOG `[3.57.0]` header; refresh `.github/tmp/pr.txt` per
`.github/pull_request_template.md` (Summary: M-2 — 7 footer-only refs
consolidated; web-verified metadata; Mangat2024 footer+bib corrected; no
prose-body change; transferability hedge retained; scope guards; Test plan:
grep battery + `^@` 100→107 + Ch1 bibkey-coverage + prose-body unchanged +
reviewer-deep PASS + v3.57.0); `gh pr edit --body-file`; `gh pr ready` only
after T03 APPROVE; **No merge.** Delete `.github/tmp/*.txt`; final report.
**Verification:** `gh pr view --json isDraft` → false; PR NOT merged.
**File scope:** `planning/INDEX.md`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** parent (mechanical).

## Reviewer routing

- **T01 / T03:** `@reviewer-deep` — mandatory.
- **`@reviewer-adversarial` escalation trigger (precise):** ONLY IF
  reviewer-deep raises an unresolved overclaim/methodology BLOCKER —
  (i) a claim the consolidation resolves/weakens the C-06/F1-2
  transferability hedge; (ii) a betting-market-transfer assertion
  introduced into prose or a bib `note`; (iii) a metadata value asserted
  "verified" without admissible source / invented; (iv) a Chapter-1
  prose-body change, or a footer change beyond the authorised Mangat2024
  vol/issue/pages tokens, made without user approval; (v) scope creep
  beyond the File Manifest. Else NOT invoked.
- **3-round symmetric cap** (execution-side too); unresolved after round 3
  → recorded residual + surfaced to user, not silently expanded.

## Repo-policy resolutions

1. **Version bump REQUIRED, minor:** `docs/` ⇒ minor; 3.56.0 → 3.57.0 (T04).
2. **WRITING_STATUS.md YES** — one additive dated line, §1.1 row (T02; user
   decision). **REVIEW_QUEUE.md NO** — no open M-2 row; §1.1 Pending row
   stays Pending (substantive Pass-2 transferability flag NOT resolved by
   this bib-only PR) (user decision).
3. **planning/INDEX.md (T00):** archive merged PR #221, set this branch
   active.
4. **Stale prior critique-file purge OUT of scope** (residual; planning-drift
   hook constrains the plan, not stale critique files).
5. Commit/PR conventions: `.github/tmp/commit.txt` + `git commit -F`;
   `.github/tmp/pr.txt` + `--body-file`; delete after; relative paths. No
   `.py` ⇒ no pytest gate.

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00, T05 |
| `planning/current_plan.critique.md` | Create (conditional) | T01 / T03 |
| `thesis/references.bib` | Update (append-only: dated block + 7 entries) | T02 |
| `thesis/chapters/01_introduction.md` | Update (footer line 85 Mangat2024 vol/issue/pages ONLY) | T02 |
| `thesis/WRITING_STATUS.md` | Update (one §1.1 dated append) | T02 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T02/T04/T05 |

Explicitly NOT modified: Chapter-1 prose BODY; any other footer line; any
existing `references.bib` entry; `thesis/chapters/REVIEW_QUEUE.md`;
chapters 02–07; `thesis/pass2_evidence/**`; the audit doc; specs; status
YAMLs; ROADMAPs; code; notebooks; `docs/TAXONOMY.md`; `.claude/**`.

## Gate Condition

1. Exactly 7 new `references.bib` entries; keys exact; no collision;
   `grep -c '^@'` == 107; references.bib purely additive.
2. Each entry's metadata web-verified vs recorded source; Mangat2024 bib AND
   footer both `40(2), 893-914`; any unconfirmable field carries a justified
   `% [REVIEW: metadata Pass-2 …]` comment (no invented values).
3. Chapter-1 **prose body byte-unchanged**; footer diff limited to line-85
   Mangat2024 vol/issue/pages tokens; `40(1), 145-165` count == 0.
4. No `[REVIEW]` flag removed (line-11 transferability hedge + line-85
   metadata flag intact); no betting-transfer claim introduced
   (RISK-01/04/05 non-contradiction).
5. Ch1 bibkey-coverage: every `[Key]` in Ch1 prose resolves in
   `references.bib` (0 unresolved; was 6).
6. Scope-diff containment: `git diff --name-only 93f02600..HEAD` ⊆ File
   Manifest; Chapters 02–07 + REVIEW_QUEUE + audit doc untouched.
7. WRITING_STATUS §1.1 append additive & accurate; REVIEW_QUEUE untouched,
   §1.1 Pending row not moved to Completed.
8. Version 3.57.0; CHANGELOG `[3.57.0]` Added+Fixed; fresh empty
   `[Unreleased]`; `[3.56.0]` untouched.
9. reviewer-deep APPROVE at T01 and T03; reviewer-adversarial only if its
   trigger fired then resolved; 3-round cap respected.
10. `planning/INDEX.md`: PR #221 archived, this branch active, PR-number
    reconciled. PR ready (`isDraft` false), NOT merged; temp files deleted.

## Out of scope

- Any Chapter-1 prose-body change; any footer change beyond the authorised
  Mangat2024 vol/issue/pages tokens.
- Resolving/weakening the C-06/F1-2 transferability `[REVIEW]` hedge, or
  F1-1 / F1-3 Ch1 flags; removing the line-85 metadata flag.
- M-1 (PR #221, merged) and M-3 (future PR-3 — TQ-05 aoestats row-count);
  the manual-full-text batch (audit §11 PR-4).
- Touching/restructuring Chapters 2–7 citations or any existing
  `references.bib` entry.
- Stale prior `planning/current_plan.critique*.md` purge (residual).
- pytest/coverage (no `.py`); BibTeX LaTeX build validation.

## Open questions

- **OQ-1 — RESOLVED (user 2026-05-18):** Mangat2024 footer one-line
  numeric correction AUTHORISED (`40(1),145-165` → `40(2),893-914`);
  Chapter-1 prose body unchanged; `[REVIEW]` flags not removed.
- **OQ-2 — RESOLVED (user 2026-05-18):** WRITING_STATUS §1.1 dated append;
  no REVIEW_QUEUE change.
- **OQ-3 — RESOLVED:** branch `docs/thesis-ch1-footer-bib-consolidation`
  (user brief governs over the audit §11 PR-2 name variant).
- **R-1 (residual, no decision):** stale prior critique-file purge deferred
  to a future planning-hygiene sweep.
