---
title: "Chapters 1–4 supervisor handoff package (capstone of merged audit chain #220→#221→#222→#223)"
category: F
branch: docs/thesis-ch1-ch4-supervisor-handoff-package
base_ref: 855bdbb684862d50859d39e5742fac78b6cfad89
date: 2026-05-18
planner_model: claude-opus-4-7[1m] (planner-science)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md
  - thesis/WRITING_STATUS.md
  - thesis/chapters/REVIEW_QUEUE.md
  - thesis/chapters/01_introduction.md
  - thesis/chapters/02_theoretical_background.md
  - thesis/chapters/03_related_work.md
  - thesis/chapters/04_data_and_methodology.md
  - thesis/chapters/05_experiments_and_results.md
  - thesis/chapters/06_discussion.md
  - thesis/chapters/07_conclusions.md
  - CHANGELOG.md
  - .claude/author-style-brief-pl.md
critique_required: false
research_log_ref: null
---

# Plan: Chapters 1–4 supervisor handoff package

> **User-directed reviewer deviation (binding).** Category-F
> documentation-relay PR; no new methodology, no chapter prose edit;
> consolidates the merged audit chain (#220 audit → #221 M-1 → #222 M-2
> → #223 M-3, all on master). reviewer-deep is the mandatory gate (T01
> plan + T03 final); reviewer-adversarial is conditional (escalation
> trigger only). `critique_required: false` reflects "no mandatory
> pre-execution adversarial critique", substituted by a mandatory
> reviewer-deep plan review. Mirrors PR #221/#222/#223.

> **User decisions (2026-05-18, binding):** (1) the §6 Polish supervisor
> note is the user's **verbatim amended text** reproduced in
> §"Deliverable content" §6 — transcribe exactly, no edits. (2)
> Attachments policy: default handoff = the four chapter Markdown files
> only; `thesis/references.bib` + the PR #220 audit doc named as
> OPTIONAL traceability attachments only; no clean copies, no flag
> stripping, no PDF/DOCX export this PR.

## Scope

Create ONE new file, `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md`,
plus planning/CHANGELOG/pyproject bookkeeping. It is a durable relay over
the merged audit chain: what to send the supervisor, what NOT to send,
how to describe the retained `[REVIEW]` flags honestly, and a
ready-to-paste Polish cover note (user-approved verbatim). NO new
methodology, NO chapter prose edit, NO `references.bib` edit, NO
`[REVIEW]` flag removed, NO stripped/clean chapter copy, NO export. NOT
writer-thesis. T02 is verbatim transcription of §"Deliverable content".

## Problem Statement

The send / do-not-send decision is scattered across the audit doc
(§3/§5/§7/§8/§9/§10/§11), `WRITING_STATUS.md` (PR #221/#222/#223
appends), and CHANGELOG. No single artifact (a) states the decision,
(b) lists exact files, (c) explains retained flags to the supervisor,
(d) carries a post-#223 Polish note (the audit §10 draft is **pre-#221**
and wrongly says "hold Chapter 2 for M-1"), (e) guards against
representing the Chapters 5–7 skeletons as completed results. The handoff
package controls the risk that the user, under time pressure, sends
Ch5–7, strips the flags, or reuses the stale §10 note.

## Assumptions & unknowns

Verified at plan time: master `855bdbb6` clean, v3.58.0; M-1 #221 / M-2
#222 / M-3 #223 all merged (WRITING_STATUS appends confirm; CHANGELOG
`[3.56.0]`/`[3.57.0]`/`[3.58.0]`); audit §3 = all four chapters
`ready_to_send_with_disclaimer`; flag ground-truth Ch1=8 / Ch2=18 /
Ch3=14+1 / Ch4=34+1 (=76) + 18 Ch4 `[POP:]`/`[PRE-canonical_slot]`
annotations; aggregate 41 ok_to_send_with_flag / 9
manual_full_text_required / 14 future_phase_dependent; Ch5
(05_experiments_and_results.md, 77 lines) / Ch6 (39) / Ch7 (29) are
BLOCKED/skeleton (no model results). `thesis/WRITING_STATUS.md` and
`thesis/chapters/REVIEW_QUEUE.md` are NOT in this PR's allowed files —
read-only here. Unknowns resolved by user: OQ-1 (Polish note = user's
verbatim amended text); OQ-2 (optional-only attachments). No `.py` in
diff ⇒ no pytest gate.

## Literature context

Not primary-source research; no new literature claim, citation, or
methodology. The package SUMMARISES (does not re-derive) the audit's
classification of the 9 `manual_full_text_required` items (EsportsBench
Table 2 80,13% + Aligulac-row; Demsar2006 §-location; CetinTas2023 86% +
NB-vs-DT; Khan2024SCPhi2 accuracy; Xie2020 R²-vs-accuracy; Minka2018TR
Halo-5 68%/52%; §4.4.5 ICC CI-method `[UNVERIFIED]`; +3 candidate-author
`[NEEDS CITATION]` items) and the 14 `future_phase_dependent` items, from
audit §5/§8/§9. The §6 Polish note follows `.claude/author-style-brief-pl.md`
(courteous first-person email register per its formal-email carve-out;
ISO `YYYY-MM-DD`; no anglicyzmy branżowe) and is the user's verbatim
amended text. The audit §10 bezosobowy draft is NOT reused verbatim
(pre-#221 + wrong register for an email).

## Deliverable content (verbatim source for T02 — transcribe, do not author)

File `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md`:
H1 `# Chapters 1–4 supervisor handoff package`, a 3–5 line provenance
preamble (consolidates merged audit chain #220 audit / #221 M-1 / #222
M-2 / #223 M-3, all on master `855bdbb6`, version pre-bump 3.58.0,
2026-05-18; no new methodology, no chapter prose edit; authoritative
source = `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`),
then EXACTLY these 8 sections in order:

### §1 — Executive decision
- Chapters 1–4 may be sent **as a working draft**; use the exact phrase
  `ready_to_send_with_disclaimer`.
- All three must-fixes CLOSED on master: M-1 (#221), M-2 (#222), M-3
  (#223). The audit §10 "send 1/3/4 now, hold Chapter 2 for M-1" framing
  is **superseded** — with M-1 merged, Chapters 1, 2, 3, 4 are all
  sendable together.
- The "disclaimer": retained `[REVIEW:]`/`[NEEDS CITATION:]`/`[UNVERIFIED:]`
  flags are deliberate Pass-2 / transparent draft markers, not unfinished
  core methodology; several Ch4 flags are register questions for the
  supervisor.
- Chapters 5–7 NOT sent as substantive content: no Phase 03+ model
  results; Ch5 all BLOCKED, Ch6 §6.1–§6.4 BLOCKED + §6.5 skeleton, Ch7
  §7.1/§7.2 BLOCKED + §7.3 idea list. Sending them creates a false
  expectation of completed experiments.

### §2 — What to send
Default handoff = exactly these four files (flags retained, see §5):
`thesis/chapters/01_introduction.md`,
`thesis/chapters/02_theoretical_background.md`,
`thesis/chapters/03_related_work.md`,
`thesis/chapters/04_data_and_methodology.md`.
**Optional traceability attachments — only if the supervisor asks (or the
user wants evidence/bibliography support):** `thesis/references.bib`
(consolidated after #222) and
`thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`
(readiness reasoning + flag triage). Default handoff is the four chapter
files alone.

### §3 — What not to send yet
`thesis/chapters/05_experiments_and_results.md` (all subsections BLOCKED —
Phase 03/04/05 / AoE2 phases / both-games-complete);
`thesis/chapters/06_discussion.md` (§6.1–§6.4 BLOCKED — Chapter 5; §6.5
skeleton stub); `thesis/chapters/07_conclusions.md` (§7.1/§7.2 BLOCKED;
§7.3 idea-comment). Rationale: blocked on Phase 03+ / AoE2 phases; no
model trained; sending misrepresents status and creates a false
expectation of completed results.

### §4 — Must-fix closure summary (verbatim table)

| Must-fix | Issue | Fix | PR | Readiness impact |
|---|---|---|---|---|
| **M-1** | `02_theoretical_background.md` §2.5.5 cited EsportsBench `v8.0 / cutoff 2025-12-31` — stale; §3.2.4 + §3.5 already `v9.0 / 2026-03-31 / dostęp 2026-04-26`, so Ch2 self-contradicted Ch3 on a quantitative comparator (SC2 Aligulac 411 030-match / ~80% Glicko). | Single-locus prose harmonisation §2.5.5 → `v9.0, cutoff 2026-03-31, dostęp 2026-04-26`. No flag added/removed; no `references.bib` change. | **#221** | Ch2 `not_ready` → `ready_to_send_with_disclaimer`; removed the only cross-chapter self-contradiction (sole `fix_before_supervisor` flag). |
| **M-2** | Ch1 §1.1 + footer: Shin1993/Forrest2005/Levitt2004/Mangat2024/Formosa2022/Novak2025/Balduzzi2018 cited but absent from `references.bib` (consolidation gap, NOT phantom); Mangat2024 footer `40(1),145-165`. | Append-only migration of 7 footer entries → `references.bib` (100→107), web-verified; Mangat2024 → `40(2),893-914` (PMID 37740076); Novak2025 first author → Pál. Prose body unchanged; no flag removed. | **#222** | Closes the central-bib consolidation gap; bib complete for typesetting. Line-11 transferability `[REVIEW]` hedge intentionally NOT closed. |
| **M-3** | `04_data_and_methodology.md` §4.1.4 cited aoestats CSV as "136 wierszy"; file 137 lines; artifact carries `[POP:ranked_ladder]` in all 136 data rows but prose discipline is `[POP:1v1_random_map]`/Tier-4 (R02 + input contract 02_00). | Reword to `137 wierszy łącznie: 1 nagłówek + 136 wierszy danych` + on-disk-true caveat (artifact `[POP:ranked_ladder]` operationally superseded in prose by `[POP:1v1_random_map]`/Tier-4); the audit's own stale "0 tags" prescription corrected. Line-212 `[REVIEW]` retained; no `references.bib`/REVIEW_QUEUE change; no prose-body rewrite. | **#223** | M-3/TQ-05 resolved. With M-1+M-2, Chapters 1–4 `ready_to_send_with_disclaimer`; closes the only Ch4 numeric discrepancy; source-label discipline preserved. |

### §5 — Retained review flags (by category, NOT line-by-line)
Totals: Ch1 = 8 `[REVIEW:]`; Ch2 = 18 `[REVIEW:]`; Ch3 = 14 `[REVIEW:]`
+ 1 `[NEEDS CITATION:]`; Ch4 = 34 `[REVIEW:]` + 1 `[UNVERIFIED:]`; total
Pass-2 = 76; + 18 Ch4 `[POP:]`/`[PRE-canonical_slot]` annotations (scope
discipline, not flags). Aggregate: 41 ok_to_send_with_flag / 9
manual_full_text_required / 14 future_phase_dependent (the 3 must-fixes
are now closed).
- **Literature/source-verification (`ok_to_send_with_flag`, ~41):** the
  flag text is itself the honest hedge (Ch1 §1.1 Shin1993/Forrest2005
  transferability; Mangat2024 gambling-psych); grey-lit acceptability
  (Ch2 §2.2.4/§2.5.4, Ch3 §3.4.4); DLC chronology (Ch2 §2.3.2); Zenodo
  metadata (Ch4 §4.1.1.0). Safe with the flag visible.
- **`manual_full_text_required` (9):** human PDF reads — EsportsBench
  Table 2 80,13% + Aligulac-row; Demsar2006 §-location; CetinTas2023 86%
  + NB-vs-DT; Khan2024SCPhi2 accuracy; Xie2020 R²-vs-accuracy;
  Minka2018TR Halo-5 68%/52%; §4.4.5 ICC CI-method `[UNVERIFIED]`
  (honest — `icc.json` does not name the CI method); + F-036
  `[NEEDS CITATION]` library lookup. Precision items on already-cited
  sources.
- **`future_phase_dependent` (14):** RQ finalisation (Ch1 §1.3/§1.4);
  method-set finalisation (Ch2 §2.1/§2.4 — candidates not decisions);
  within/cross-game protocol (§4.4.4); artifact-internal distributions
  (§4.1.x); feature-engineering deferrals (§4.4.6; tracker GATE-14A6
  `narrowed`, 3 families correctly NOT promoted); §4.5 provisional
  registry (`partial_coverage_v9_baseline`, Step NOT closed). Evidence
  of boundary honesty.
- **Intentionally-retained methodology caveats / annotations:** 18 Ch4
  `[POP:]`/`[PRE-canonical_slot]` = correct source-label/population
  discipline (tournament vs 1v1 Random Map undisclosed-queue vs mixed
  ranked/quickplay), NOT fragments to fill. Ch4 Polish-idiom register
  flags retained because the supervisor is the right person to answer
  them.
State clearly: stripping the flags before the supervisor is NOT
recommended — they document verified-vs-to-be-confirmed; several Ch4
flags are direct register questions; they are transparent draft markers,
not unfinished core methodology.

### §6 — Recommended Polish note to supervisor (USER-APPROVED VERBATIM — transcribe exactly)

> Temat: Praca magisterska — robocza wersja rozdziałów 1–4 do recenzji
>
> Szanowny Panie Profesorze,
>
> przesyłam do recenzji roboczą wersję czterech pierwszych rozdziałów pracy magisterskiej. Rozdziały te obejmują kolejno: wprowadzenie i sformułowanie problemu badawczego (rozdział 1), tło teoretyczne — gry strategiczne czasu rzeczywistego, metody klasyfikacji uczenia maszynowego i systemy oceny siły gracza (rozdział 2), przegląd prac pokrewnych — predykcję w sportach tradycyjnych, w StarCraft II, w innych grach esportowych oraz w Age of Empires II, wraz z identyfikacją luki badawczej (rozdział 3), a także opis danych i metodyki — pozyskanie i czyszczenie korpusów, rozpoznawanie tożsamości gracza, dyscyplinę temporalną, plan inżynierii cech oraz protokół ewaluacji (rozdział 4).
>
> Rozdziały eksperymentalne stanowią kolejny etap pracy. Żaden model nie został jeszcze wytrenowany, dlatego rozdziały wynikowe pozostają na razie szkieletami i ich przekazanie mogłoby sugerować ukończone wyniki, których jeszcze nie ma. Praca na obecnym etapie nie formułuje żadnych twierdzeń o wynikach modelowania ani o porównaniu skuteczności metod.
>
> W tekście pozostawiłem widoczne znaczniki [REVIEW: …], [NEEDS CITATION: …] oraz [UNVERIFIED: …]. Są to celowe znaczniki dalszej weryfikacji, a nie ukryte założenia: wskazują miejsca, w których dokładną wartość liczbową trzeba potwierdzić ręcznym odczytem pełnego tekstu źródła niedostępnego narzędziom automatycznym, rozstrzygnięcie zależy od etapu eksperymentalnego jeszcze nieukończonego albo potrzebna jest decyzja redakcyjna co do polskiej terminologii. Te ostatnie, szczególnie w rozdziale 4, traktuję jako pytania, przy których opinia Pana Profesora będzie dla mnie szczególnie cenna. Wszystkie krytyczne poprawki wskazane w wewnętrznym audycie przedwysyłkowym zostały już naniesione i domknięte.
>
> Będę wdzięczny za uwagi przede wszystkim co do struktury pracy, doboru poziomu szczegółowości, zrozumiałości opisu metodyki oraz zakresu przyjętego tła teoretycznego i przeglądu literatury. Pozostaję do dyspozycji w sprawie dogodnego terminu omówienia uwag.
>
> Z wyrazami szacunku,
> Tomasz Pionka

### §7 — Suggested attachment/export options
- Default: send the four chapter Markdown files directly (lowest
  friction; preserves the visible `[REVIEW]` flags).
- Optional traceability — only if the supervisor asks: include
  `thesis/references.bib` (bibliography traceability after #222) and/or
  `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`
  (readiness reasoning + flag triage).
- PDF/DOCX export and any flag-stripped clean copy are deliberately a
  separate later step (out of scope here; annotated version recommended
  — Ch4 flags are register questions). This PR exports nothing and
  creates no clean copy.

### §8 — Remaining after supervisor handoff
Phase 03 Splitting & Baselines (SC2) → unblocks Ch5 §5.1.1; optional
retained-flag cleanup (the `manual_full_text_required` batch + F-036
lookup — audit §11 PR-4, post-handoff); Phase 04/05 Model Training &
Evaluation (SC2) → unblocks Ch5 §5.1.2–§5.1.4 + Ch6; AoE2 Phase 02 onward
(later) → unblocks Ch5 §5.2/§5.3; Chapters 5–7 drafted only after the
corresponding model results exist; §1.5 thesis outline finalised last.

## Execution Steps

All repo-changing tasks commit AND push. Branch off `855bdbb6`. Draft PR
at T00; kept draft until reviewer-deep passes at T03; **NO merge until
explicit user approval**. `.github/tmp/commit.txt` + `git commit -F`;
`.github/tmp/pr.txt` + `--body-file`; delete after; relative paths; no
`.py` ⇒ no pytest gate.

### T00 — Branch + full plan + INDEX archive #223 + draft PR
**Objective:** bootstrap a planning-drift-complete Cat-F plan.
**Instructions:** branch off `855bdbb6` (done); write this full plan to
`planning/current_plan.md` (EXACT planning-drift section headings — no
parenthetical on `## Literature context`); `planning/INDEX.md` — archive
merged PR #223, set this branch active; commit via
`.github/tmp/commit.txt` + `git commit -F`
(`chore(pr): bootstrap draft PR for Chapters 1–4 supervisor handoff package`);
push `-u`; `gh pr create --draft --title "docs(thesis): prepare Chapters 1–4 supervisor handoff package" --body-file .github/tmp/pr.txt`; delete `.github/tmp/*.txt`.
**Verification:** `gh pr view --json isDraft` → true; planning-drift hook
passes; `git show --stat HEAD` = only `planning/current_plan.md` +
`planning/INDEX.md`.
**File scope:** `planning/current_plan.md`, `planning/INDEX.md`,
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent.

### T01 — reviewer-deep plan review (HALT on blocker)
**Objective:** validate the plan before writing the deliverable.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `855bdbb6`. Checks: 8 sections faithful to audit; §4 maps
M-1→#221 / M-2→#222 / M-3→#223 with correct impacts; §6 == the user's
verbatim amended Polish note AND contains no completed-experiment claim
AND does not represent Ch5–7 as ready; §1 supersedes the pre-#221 audit
§10 "hold Chapter 2" framing and uses `ready_to_send_with_disclaimer`;
§5 totals reconcile (76 + 18); §2/§7 optional-only attachments; scope
containment (no `thesis/chapters/**`, no `references.bib`, no
`WRITING_STATUS.md`, no `REVIEW_QUEUE.md` in the plan's File Manifest).
BLOCKER → HALT, surface to user, amend only on user direction,
re-review. If reviewer output committed → `planning/current_plan.critique.md`,
commit, push.
**Verification:** reviewer-deep verdict; 0 unresolved BLOCKERs.
**File scope:** `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** `planning/current_plan.md`. **Push:** yes if critique committed.

### T02 — Write the handoff package deliverable
**Objective:** create the deliverable as a verbatim transcription of
§"Deliverable content".
**Instructions:** create
`thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md` with H1 +
preamble + the 8 sections from §"Deliverable content" (the §4 table
verbatim; the §6 Polish note verbatim — every word/diacritic exactly as
in §"Deliverable content" §6, which is the user-approved text). No new
prose, no 9th section, no chapter/bib/WRITING_STATUS/REVIEW_QUEUE edit,
no `[REVIEW]` flag removed, no stripped/clean copy, no export. Commit via
`.github/tmp/commit.txt` + `git commit -F`
(`docs(thesis): add Chapters 1–4 supervisor handoff package`); push.
**Verification (battery):**
- File exists; `grep -c '^## ' thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md` == 8; the 8 titles in order (1 Executive decision … 8 Remaining after supervisor handoff).
- `grep -c 'Szanowny Panie Profesorze' …` ≥ 1 and `grep -c 'Z wyrazami szacunku' …` ≥ 1 and `grep -c 'przy których opinia Pana Profesora będzie dla mnie szczególnie cenna' …` ≥ 1 (user-verbatim markers present).
- `grep -c 'ready_to_send_with_disclaimer' …` ≥ 1; §4 contains `#221`, `#222`, `#223`.
- No completed-experiment claim: `grep -niE 'wytrenowano model|uzyskano wyniki|model osiąga|results show|trained model achiev' …` == 0 (the note's only model sentence is the negation "Żaden model nie został jeszcze wytrenowany").
- `git diff --name-only 855bdbb6..HEAD` ⊆ {planning/current_plan.md, planning/INDEX.md, planning/current_plan.critique.md, thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md}; ZERO `thesis/chapters/`, ZERO `thesis/references.bib`, ZERO `thesis/WRITING_STATUS.md`, ZERO `thesis/chapters/REVIEW_QUEUE.md`.
**File scope:** `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md`,
`.github/tmp/*`. **Read scope:** §"Deliverable content" of this plan.
**Push:** yes. **Executor:** @executor on **Sonnet** (verbatim
transcription + mechanical structure check; all content resolved in this
plan; user-approved Polish note; data-analysis-lineage
"mechanically-specified, decisions resolved" → Sonnet).

### T03 — reviewer-deep final check
**Objective:** validate the committed deliverable.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `855bdbb6`. Verify: 8 sections present + faithful to audit;
§4 PR mapping correct; §6 is the user's verbatim amended Polish note (no
drift), no completed-experiment claim, Ch5–7 not represented ready;
§1 uses `ready_to_send_with_disclaimer` and supersedes the pre-#221
framing; §5 totals reconcile; §2/§7 optional-only attachments; scope
⊆ allowed set (zero `thesis/chapters/**`, zero `references.bib`, zero
`WRITING_STATUS.md`, zero `REVIEW_QUEUE.md`); no flag removed, no
stripped copy. Escalate to `@reviewer-adversarial` ONLY on an unresolved
overclaim/methodology BLOCKER (trigger list in Reviewer routing);
3-round symmetric cap. Mechanical in-scope fixes only; substantive
residual → record + surface to user. Commit + push if changed.
**Verification:** reviewer-deep APPROVE; 0 unresolved BLOCKERs.
**File scope:** `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md`,
`planning/current_plan.critique.md`, `.github/tmp/*`. **Read scope:**
diff. **Push:** yes if changed.

### T04 — Version bump 3.58.0 → 3.59.0 + CHANGELOG
**Objective:** release hygiene.
**Instructions:** `pyproject.toml` `3.58.0` → `3.59.0`; CHANGELOG
`[Unreleased]` → `## [3.59.0] — 2026-05-18 (PR #<n>: docs/thesis-ch1-ch4-supervisor-handoff-package)`
with `### Added` (Chapters 1–4 supervisor handoff package consolidating
the merged audit chain #220→#221→#222→#223; relay/assembly only — no
chapter prose / no `references.bib` edit; default handoff = four chapter
files, optional-only traceability attachments; user-approved Polish
cover note; M-1/M-2/M-3 all closed → Chapters 1–4
`ready_to_send_with_disclaimer`); fresh empty `[Unreleased]` with 4
headers; `[3.58.0]` (PR #223) untouched. `<n>` from
`gh pr view --json number`. Commit `chore(release): bump version to 3.59.0`;
push.
**Verification:** `pyproject.toml`=3.59.0; CHANGELOG `[Unreleased]` empty
4 headers; one `### Added` under `[3.59.0]`; `[3.58.0]` untouched.
**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** @executor Sonnet.

### T05 — PR body refresh + mark ready (NO merge until user approval)
**Objective:** finalize the PR for review WITHOUT merging.
**Instructions:** reconcile PR-number placeholder in `planning/INDEX.md`
active line + CHANGELOG `[3.59.0]` header; refresh `.github/tmp/pr.txt`
per `.github/pull_request_template.md` (Summary: handoff package; what
to send / not send; M-1/M-2/M-3 closed; Polish note user-approved;
optional-only attachments; Test plan: 8-section + Polish-marker grep
battery + scope-containment + reviewer-deep PASS + v3.59.0);
`gh pr edit --body-file`; `gh pr ready` only after T03 APPROVE.
**Do NOT `gh pr merge` — merge awaits explicit user approval.** Delete
`.github/tmp/*.txt`; produce final report.
**Verification:** `gh pr view --json isDraft` → false; `state` OPEN, NOT
merged. **File scope:** `planning/INDEX.md`, `CHANGELOG.md`,
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent.

## Reviewer routing

- **T01 / T03:** `@reviewer-deep` — mandatory.
- **`@reviewer-adversarial` escalation trigger (precise):** ONLY IF
  reviewer-deep raises an unresolved overclaim/methodology BLOCKER —
  (a) §1 or §6 claims completed experiments/results; (b) Ch5–7
  represented as ready/substantive; (c) the §4 table misattributes a PR
  (M-1/M-2/M-3 ↔ #221/#222/#223); (d) a scope breach (any
  `thesis/chapters/**` or `thesis/references.bib` edit in the diff);
  (e) §6 deviates from the user's verbatim approved text. Else NOT
  invoked (documentation-relay PR, no new methodology).
- **3-round symmetric cap** (execution-side too); unresolved after
  round 3 → recorded residual + surfaced to user, not silently expanded.

## Repo-policy resolutions

1. **Version bump REQUIRED, minor:** `docs/` ⇒ minor; 3.58.0 → 3.59.0 (T04).
2. **No `WRITING_STATUS.md` change** — NOT in allowed files; the
   #221/#222/#223 appends already record readiness. **No
   `REVIEW_QUEUE.md` change** — `thesis/chapters/**` forbidden; flag
   inventory summarised from the audit, not edited.
3. **planning/INDEX.md (T00):** archive merged PR #223, set this branch
   active.
4. **Stale prior critique-file purge OUT of scope** (residual); no
   pre-existing `planning/*.critique.md` deleted/rewritten;
   `planning/current_plan.critique.md` touched only if a reviewer output
   is committed.
5. Commit/PR conventions: `.github/tmp/commit.txt` + `git commit -F`;
   `.github/tmp/pr.txt` + `--body-file`; delete after; relative paths.

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00, T05 |
| `planning/current_plan.critique.md` | Create (conditional) | T01 / T03 |
| `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md` | Create | T02 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T02/T04/T05 |

Explicitly NOT modified: any `thesis/chapters/**` (all 7 chapter files +
`REVIEW_QUEUE.md`); `thesis/references.bib`; `thesis/WRITING_STATUS.md`;
any other `thesis/pass2_evidence/**` file; dataset artifacts; notebooks;
specs; ROADMAPs; status YAMLs; research logs; code; raw data;
`docs/TAXONOMY.md`; `.claude/**`.

## Gate Condition

1. `thesis/pass2_evidence/ch1_ch4_supervisor_handoff_package.md` exists;
   H1 + exactly the 8 specified sections in order.
2. §6 == the user's verbatim amended Polish note (markers present:
   `Szanowny Panie Profesorze`, `przy których opinia Pana Profesora
   będzie dla mnie szczególnie cenna`, `Z wyrazami szacunku`,
   `Tomasz Pionka`); no completed-experiment claim; Ch5–7 not
   represented as ready.
3. §4 maps M-1→#221, M-2→#222, M-3→#223 with the specified impacts; §1
   uses `ready_to_send_with_disclaimer` and supersedes the pre-#221
   "hold Chapter 2" framing.
4. §5 totals reconcile (Ch1=8 / Ch2=18 / Ch3=14+1 / Ch4=34+1 = 76; + 18
   Ch4 annotations), by category not line-by-line; §2/§7 = optional-only
   attachments policy.
5. Scope containment: `git diff --name-only 855bdbb6..HEAD` ⊆ File
   Manifest; ZERO `thesis/chapters/**`, ZERO `thesis/references.bib`,
   ZERO `thesis/WRITING_STATUS.md`, ZERO `thesis/chapters/REVIEW_QUEUE.md`,
   ZERO other `pass2_evidence/**`; no flag removed; no stripped copy; no
   export.
6. Version 3.59.0; CHANGELOG `[3.59.0]` `### Added`; fresh empty
   `[Unreleased]`; `[3.58.0]` untouched.
7. reviewer-deep APPROVE at T01 and T03; reviewer-adversarial only if its
   trigger fired then resolved; 3-round cap respected.
8. `planning/INDEX.md`: PR #223 archived, this branch active, PR-number
   reconciled. PR ready (`isDraft` false), **NOT merged** (merge awaits
   explicit user approval); temp files deleted.

## Out of scope

- Any `thesis/chapters/**` edit (all 7 chapter files + `REVIEW_QUEUE.md`);
  any `thesis/references.bib` edit; any `thesis/WRITING_STATUS.md` edit;
  any other `thesis/pass2_evidence/**` edit.
- Removing/adding any `[REVIEW]`/`[UNVERIFIED]`/`[NEEDS CITATION]` flag;
  any stripped/clean chapter copy; any PDF/DOCX export.
- Any new methodology/citation/literature claim or audit re-derivation;
  the `manual_full_text_required` PDF reads + F-036 lookup (audit §11
  PR-4).
- Phase 03 / AoE2 Phase 02 / dataset artifacts / notebooks / specs /
  ROADMAPs / status YAMLs / code / raw data / `docs/TAXONOMY.md` /
  `.claude/**`.
- Merging the PR (awaits explicit user approval); deleting/rewriting any
  pre-existing `planning/*.critique.md`.

## Open questions

- **OQ-1 — RESOLVED (user 2026-05-18):** the §6 Polish note is the
  user's verbatim amended text (reproduced in §"Deliverable content" §6);
  transcribe exactly, no edits.
- **OQ-2 — RESOLVED (user 2026-05-18):** §2/§7 = optional-only
  attachments (default = four chapter files; `references.bib` + audit
  doc optional-only; no clean copy / no flag stripping / no export).
- **R-1 (residual, no decision):** stale prior critique-file purge
  deferred to a future planning-hygiene sweep.
