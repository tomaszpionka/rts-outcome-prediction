---
title: "aoestats interface-CSV row-count + [POP:]-scope caveat (Chapters 1–4 audit must-fix M-3 / TQ-05)"
category: F
branch: docs/thesis-aoestats-rowcount-scope-caveat
base_ref: adf933031bb8c9d335d07d1e23d867603c244371
date: 2026-05-18
planner_model: claude-opus-4-7[1m] (planner-science)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md
  - thesis/pass2_evidence/phase01_phase02_writing_readiness_audit.md
  - thesis/pass2_evidence/cross_dataset_comparability_matrix.md
  - thesis/chapters/04_data_and_methodology.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md
  - reports/specs/02_00_feature_input_contract.md
critique_required: false
research_log_ref: null
---

# Plan: aoestats row-count + [POP:]-scope caveat (must-fix M-3 / TQ-05)

> **User-directed reviewer deviation (binding).** Per the task brief,
> reviewer-deep is the mandatory plan gate (T01) and final gate (T03);
> reviewer-adversarial is conditional (escalation trigger only).
> `critique_required: false` reflects "no mandatory pre-execution
> adversarial critique", substituted by a mandatory reviewer-deep plan
> review. Mirrors PR #221 (M-1) / #222 (M-2). The user selected Option A
> verbatim at plan approval, so reviewer-adversarial is NOT mandatorily
> pre-triggered (it remains conditional on a reviewer-deep blocker).

> **CRITICAL FINDING (verified on disk 2026-05-18; drives the wording).**
> The framing prescribed by the task brief AND the PR #220 audit
> (M-3 / TQ-05 / C-10) — "aoestats `[POP:]` is *not tag-carried* /
> *0 of 137 tags* / implicit-via-spec" — is **STALE and factually FALSE**
> against the post-F6 artifact. Independently confirmed:
> `phase06_interface_aoestats.csv` = **137 lines = 1 header + 136 data
> rows**, and **all 136 data rows carry `[POP:ranked_ladder]`** (+30 also
> carry `[PRE-canonical_slot]`). The audit/readiness text captured a
> pre-F6 snapshot; a BACKLOG-F6 backfill (2026-04-19) added the tokens;
> chapter line 428 and §4.4.6 were already reconciled to the post-F6
> state, but §4.1.4 line 212 (and the audit's TQ-05 text itself) were
> not. Per the anti-GIGO discipline and the user's instruction
> ("flag rather than bake in an unverifiable claim"), the false
> "0 tags / not tag-carried" claim is NOT entered into the thesis.
> **User decision (2026-05-18): Option A** — on-disk-true wording that
> names the provisional `[POP:ranked_ladder]` artifact token and states
> it is operationally superseded in the prose by the disciplined
> `[POP:1v1_random_map]` / Tier-4 framing. The stale `pass2_evidence/**`
> text is left as historical audit evidence (NOT corrected here).

## Scope

One-locus Category F prose clarification resolving audit must-fix
**M-3 / TQ-05**. In scope: (1) ONE Edit to
`thesis/chapters/04_data_and_methodology.md` line 212 (§4.1.4
"Twierdzenia dataset-conditional") — correct the aoestats row-count to
explicit header/data form and reword the aoestats `[POP:]`-carriage
clause to be true against the post-F6 artifact (Option A); (2) one dated
one-line append to the §4.1.4 row of `thesis/WRITING_STATUS.md`;
(3) version bump 3.57.0 → 3.58.0 + `CHANGELOG.md`; (4) `planning/INDEX.md`
archive of merged PR #222 + active-plan line + `planning/current_plan.md`
overwrite; (5) branch / draft-PR / commit-push lifecycle (no merge).
After merge: M-1 ✅ #221, M-2 ✅ #222, M-3 = this PR → Chapters 1–4
`ready_to_send_with_disclaimer`.

## Problem Statement

`04_data_and_methodology.md:212` (§4.1.4) — cited by audit C-10, M-3,
§11 PR-3, F4-11 and readiness TQ-05 — has two defects in the
operationalisation sentence: (i) row-count ambiguity — bare
"`phase06_interface_aoestats.csv` (136 wierszy)" is inconsistent with
the "X/X wierszy" framing used for the other two corpora and does not
disambiguate the 137-line file (1 header + 136 data rows); (ii) the
"niesie tag dla aoestats" clause papers over the fact that the artifact
carries the stale/provisional `[POP:ranked_ladder]` token (the Tier-4
mis-label) in all 136 data rows, while the surrounding prose correctly
uses the disciplined `[POP:1v1_random_map]` "bez kwalifikacji 'ranked
ladder'". The audit's prescribed corrected framing ("not tag-carried /
0 tags / implicit-via-spec") is stale/false post-F6 (see CRITICAL
FINDING). The fix must be on-disk-true, must distinguish the on-disk
artifact token from the thesis methodology label, must not contradict
CX-17/Tier-4 discipline, must not remove/alter any `[REVIEW]` flag, and
must not imply the previous "136" was conceptually wrong.

## Assumptions & unknowns

Verified on disk 2026-05-18 (do not re-discover): master @ `adf93303`
clean, v3.57.0; `phase06_interface_aoestats.csv` 137 lines = 1 header +
136 data rows; **136 `[POP:ranked_ladder]`** + 30 `[PRE-canonical_slot]`;
sc2egset interface 35 data rows × `[POP:tournament]`; aoe2companion
interface 74 data rows × tag; R02 defined at
`src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md:11`
(`leaderboard='random_map'` cleaning rule); "spec §0" = established
shorthand for `reports/specs/02_00_feature_input_contract.md` (aoestats
input contract; no literal "§0" heading); line 428 already says
"136 wierszy danych" (post-F6-correct, OUT of scope); line-212 trailing
`[REVIEW]` + line-214 two `[REVIEW]` flags present; Chapter 4 has 34
`[REVIEW:]` + 1 `[UNVERIFIED:]`; WRITING_STATUS §4.1.4 row records the
stale pre-F6 "0 tags" lineage; OLD line-212 fragment is unique (line 428
uses a different string). Unknowns resolved: OQ-1 → Option A (user);
OQ-2 → WRITING_STATUS-only (user); OQ-3 → informational (stale
pass2_evidence text left as historical, out of scope).

## Literature context

Internal pass-2 evidence chain (numeric-consistency + scope-honesty):

- `ch1_ch4_citation_literature_support_audit.md` — C-10 establishes the
  137-line fact and routes "clarify 137 total / 136 data rows + reword
  aoestats `[POP:]` scope; do NOT delete the line-~211 `[REVIEW]` flag
  without the reconciled framing; do NOT re-derive file content; do NOT
  extend to other CONSORT counts". M-3 (§7), §11 PR-3.
- `phase01_phase02_writing_readiness_audit.md` — TQ-05 prescribes the
  137/136 disambiguation; its "not tag-carried / 0 tags" sub-claim is
  the pre-F6 stale snapshot (self-contradictory: also references the
  post-F6 backfill on 30 of 136 data rows). This PR supersedes that
  framing IN THE CHAPTER + WRITING_STATUS ONLY; the pass2_evidence file
  is NOT corrected (left as historical audit evidence).
- `cross_dataset_comparability_matrix.md` — CX-17 / Tier-4: aoestats is
  Tier 4; must NOT be called "ranked ladder" without qualification;
  `[POP:ranked_ladder]` is the known artifact mis-label that the prose
  deliberately supersedes with `[POP:1v1_random_map]`. Option A is
  consistent with this discipline (it does not re-assert
  `[POP:ranked_ladder]` as correct — it names it as the provisional
  artifact token superseded in prose).

## The exact edit (single line-212 locus)

**File:** `thesis/chapters/04_data_and_methodology.md`, line 212.
`old_string` is unique (line 428 uses "136 wierszy danych", a different
string → line 428 untouched).

### OLD (exact — Edit `old_string`):
```
Operacjonalizacja tagu `[POP:]` w artefaktach interfejsu temporalnego: `phase06_interface_sc2egset.csv` (35/35 wierszy) niesie `[POP:tournament]` w kolumnie `notes`, `01_05_phase06_interface_aoe2companion.csv` (74/74 wierszy) niesie tag dla aoe2companion, a `phase06_interface_aoestats.csv` (136 wierszy) niesie tag dla aoestats — całość zachowuje claim **dataset-conditional** we wszystkich trzech korpusach.
```

### NEW (exact — Edit `new_string`; Option A, user-approved verbatim):
```
Operacjonalizacja tagu `[POP:]` w artefaktach interfejsu temporalnego: `phase06_interface_sc2egset.csv` (35/35 wierszy) niesie `[POP:tournament]` w kolumnie `notes`, `01_05_phase06_interface_aoe2companion.csv` (74/74 wierszy) niesie tag w kolumnie `notes` dla aoe2companion, a `phase06_interface_aoestats.csv` (137 wierszy łącznie: 1 nagłówek + 136 wierszy danych) niesie tag w kolumnie `notes` we wszystkich 136 wierszach danych — przy czym w artefakcie aoestats jest to literalny, prowizoryczny token `[POP:ranked_ladder]` operacyjnie zastąpiony w niniejszej prozie zdyscyplinowanym `[POP:1v1_random_map]` (Tier-4 opacja kolejki; por. regułę czyszczenia R02 `leaderboard='random_map'` w `01_04_01_data_cleaning.md` oraz kontrakt wejściowy `02_00`), nie zaś tagiem identycznym z prozą; rozdźwięk artefakt–proza nie narusza claimu **dataset-conditional**, który jest zachowany we wszystkich trzech korpusach.
```

**Edit invariants:** `old_string` unique; the trailing line-212
`[REVIEW]` flag and the line-214 `[REVIEW]` flags are OUTSIDE
`old_string` (untouched); sc2egset `(35/35 wierszy) niesie
[POP:tournament] w kolumnie notes` byte-identical OLD→NEW; aoe2companion
`(74/74 wierszy)` count byte-identical (only "w kolumnie `notes`"
parallelism added inside that clause); dataset-conditional claim
preserved; no other line in the file changes. The NEW string contains
NO false "0 tags / not tag-carried / NO [POP:] tag" claim; it states a
token IS present in all 136 data rows and distinguishes the on-disk
artifact token (`[POP:ranked_ladder]`) from the thesis methodology label
(`[POP:1v1_random_map]` / Tier-4).

## writer-thesis vs executor ruling

**@executor (Sonnet); writer-thesis NOT invoked.** Single-sentence
numeric/scope correction with the exact replacement string fully
resolved here (Option A, verbatim, zero executor discretion). The one
methodology decision (OQ-1) is resolved by the user at plan approval.
No literature search, no new citation, no `references.bib` change, no
paragraph rewrite, non-propagating. This is the data-analysis-lineage
"mechanically specified, plan resolves the decisions → Sonnet executor"
case.

## Execution Steps

### T00 — Branch + full plan + INDEX archive #222 + draft PR
**Objective:** bootstrap a planning-drift-complete Cat-F plan.
**Instructions:** branch off `adf93303` (done); write this full plan to
`planning/current_plan.md`; `planning/INDEX.md` — archive merged PR #222,
set this branch active; commit via `.github/tmp/commit.txt` +
`git commit -F` (`chore(pr): bootstrap draft PR for aoestats row-count/scope caveat [M-3]`);
push `-u`; `gh pr create --draft --title "docs(thesis): clarify aoestats row-count and POP scope in Chapter 4" --body-file .github/tmp/pr.txt`; delete `.github/tmp/*.txt`.
**Verification:** `gh pr view --json isDraft` → true; planning-drift hook
passes; `git show --stat HEAD` = only `planning/current_plan.md` +
`planning/INDEX.md`.
**File scope:** `planning/current_plan.md`, `planning/INDEX.md`,
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent.

### T01 — reviewer-deep plan review (HALT on blocker)
**Objective:** validate the plan (esp. that Option A is on-disk-true and
does NOT re-introduce the false audit framing) before any edit.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `adf93303`. Checks: (a) NEW string numeric consistency vs the
on-disk artifact (137 = 1 header + 136 data rows; 136
`[POP:ranked_ladder]`); (b) NEW string contains NO false "0 tags /
not tag-carried / NO [POP:] tag" claim and does not assert
`[POP:ranked_ladder]` is the correct discipline tag; (c) CX-17/Tier-4
discipline + the line-212 `[REVIEW]` flag preserved; (d) line 428 and
the `[PRE-canonical_slot]`/`canonical_slot` narrative untouched;
(e) sc2egset 35/35 + aoe2companion 74/74 + dataset-conditional preserved;
(f) `pass2_evidence/**` / specs / `references.bib` / other chapters not
in scope; (g) WRITING_STATUS-only / REVIEW_QUEUE-none decision sound;
(h) version 3.57.0→3.58.0; (i) OQ-1/OQ-3 reasoning sound. BLOCKER → HALT,
surface to user, amend only on user direction, re-review. If reviewer
output committed → `planning/current_plan.critique.md`, commit, push.
**Verification:** reviewer-deep verdict; 0 unresolved BLOCKERs.
**File scope:** `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** `planning/current_plan.md`. **Push:** yes if critique committed.

### T02 — Line-212 edit (Option A) + WRITING_STATUS append
**Objective:** apply the single verbatim Option-A Edit + the §4.1.4
WRITING_STATUS append.
**Instructions:**
1. Edit `04_data_and_methodology.md` line 212: replace the exact OLD
   string with the exact NEW (Option A) string above. Single Edit; no
   other line/character changes.
2. Append ONE dated line (2026-05-18) to the §4.1.4 row of
   `thesis/WRITING_STATUS.md` (append only; same style as PR #221/#222):
   records M-3/TQ-05 resolved; row-count corrected to
   `137 wierszy łącznie: 1 nagłówek + 136 wierszy danych`; on-disk
   artifact carries `[POP:ranked_ladder]` in all 136 data rows but the
   prose supersedes that stale/provisional token with the disciplined
   `[POP:1v1_random_map]` / Tier-4 queue-opacity framing (R02 + 02_00);
   this supersedes the row's stale pre-F6 "0 tags" lineage; line-212
   `[REVIEW]` flag remains open; Chapter 4 →
   `ready_to_send_with_disclaimer` (subject to retained review flags);
   line 428 / sibling clauses / `references.bib` / `REVIEW_QUEUE.md`
   unchanged; pass2_evidence untouched.
3. Do NOT touch line 428, any `[REVIEW]`/`[PRE-canonical_slot]`/
   `canonical_slot` content, sc2egset/aoe2companion clauses,
   `references.bib`, `REVIEW_QUEUE.md`, other chapters, `pass2_evidence/**`,
   specs, dataset artifacts.
4. Commit via `.github/tmp/commit.txt` + `git commit -F`
   (`docs(thesis): clarify aoestats §4.1.4 row-count + [POP:] scope (137=1+136; ranked_ladder superseded by 1v1_random_map) [M-3]`);
   push.
**Verification (grep battery):**
- `grep -c '137 wierszy łącznie: 1 nagłówek + 136 wierszy danych' thesis/chapters/04_data_and_methodology.md` == 1 (line 212).
- `grep -c '(136 wierszy) niesie tag dla aoestats' thesis/chapters/04_data_and_methodology.md` == 0.
- `grep -c '136 wierszy danych' thesis/chapters/04_data_and_methodology.md` unchanged vs base (line 428 still present).
- `grep -c '\[REVIEW:' thesis/chapters/04_data_and_methodology.md` == 34 (= base); `grep -c '\[UNVERIFIED:' …` == 1 (= base).
- sc2egset `(35/35 wierszy) niesie \`[POP:tournament]\` w kolumnie \`notes\`` present; aoe2companion `(74/74 wierszy)` present.
- `git diff base..HEAD -- thesis/chapters/04_data_and_methodology.md` = exactly ONE hunk at line 212; no hunk at/near line 428.
- `git diff --name-only adf93303..HEAD` ⊆ {planning/current_plan.md, planning/INDEX.md, planning/current_plan.critique.md, thesis/chapters/04_data_and_methodology.md, thesis/WRITING_STATUS.md}.
- `git diff adf93303..HEAD -- thesis/references.bib thesis/chapters/REVIEW_QUEUE.md` empty; no `pass2_evidence/**` / specs / artifacts in diff.
**File scope:** `thesis/chapters/04_data_and_methodology.md`,
`thesis/WRITING_STATUS.md`, `.github/tmp/*`. **Read scope:** the OLD/NEW
strings, `WRITING_STATUS.md` §4.1.4 row. **Push:** yes. **Executor:**
@executor on **Sonnet** (verbatim Edit + verbatim append; the methodology
decision OQ-1 resolved at plan approval).

### T03 — reviewer-deep final check
**Objective:** validate the applied diff.
**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `adf93303`. Verify: NEW == Option A spec; on-disk-true (no
false "0 tags"; does not assert `[POP:ranked_ladder]` correct); 137=1+136
present; `(136 wierszy) niesie tag dla aoestats` gone; line 428
byte-unchanged; all `[REVIEW]`/`[UNVERIFIED]` flags unchanged (34/1);
sc2egset 35/35 + aoe2companion 74/74 + dataset-conditional intact; exactly
one Ch4 hunk (line 212); `references.bib`/`REVIEW_QUEUE.md`/
`pass2_evidence/**`/specs/other chapters untouched; WRITING_STATUS §4.1.4
append additive & accurate; no Phase 02/06 closure claim. Escalate to
`@reviewer-adversarial` ONLY on an unresolved overclaim/methodology
BLOCKER (trigger list in Reviewer routing); 3-round symmetric cap.
Mechanical in-scope fixes only; substantive residual → record + surface
to user. Commit + push if changed.
**Verification:** reviewer-deep APPROVE; 0 unresolved BLOCKERs.
**File scope:** `thesis/chapters/04_data_and_methodology.md`,
`thesis/WRITING_STATUS.md`, `planning/current_plan.critique.md`,
`.github/tmp/*`. **Read scope:** diff. **Push:** yes if changed.

### T04 — Version bump 3.57.0 → 3.58.0 + CHANGELOG
**Objective:** release hygiene.
**Instructions:** `pyproject.toml` `3.57.0` → `3.58.0`; CHANGELOG
`[Unreleased]` → `## [3.58.0] — 2026-05-18 (PR #<n>: docs/thesis-aoestats-rowcount-scope-caveat)`
with `### Fixed` (resolves audit must-fix M-3 / C-10 / TQ-05; §4.1.4
row-count corrected to 137 total = 1 header + 136 data rows; aoestats
artifact carries provisional `[POP:ranked_ladder]` in 136 data rows,
operationally superseded in prose by disciplined `[POP:1v1_random_map]` /
Tier-4 via R02 + `02_00`; supersedes the stale pre-F6 "0 tags" framing —
on-disk-true correction, no Phase 02/06 closure claim; line 428 /
`[REVIEW]` flags / sibling clauses / `references.bib` / `REVIEW_QUEUE.md`
unchanged; M-1 + M-2 + M-3 all closed → Chapters 1–4
`ready_to_send_with_disclaimer`); fresh empty `[Unreleased]` with 4
headers; `[3.57.0]` (PR #222) untouched. `<n>` from
`gh pr view --json number`. Commit `chore(release): bump version to 3.58.0`;
push.
**Verification:** `pyproject.toml`=3.58.0; CHANGELOG `[Unreleased]` empty
4 headers; one `### Fixed` under `[3.58.0]`; `[3.57.0]` untouched.
**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** @executor Sonnet.

### T05 — PR body refresh + mark ready (NO merge)
**Objective:** finalize without merging.
**Instructions:** reconcile PR-number placeholder in `planning/INDEX.md`
active line + CHANGELOG `[3.58.0]` header; refresh `.github/tmp/pr.txt`
per `.github/pull_request_template.md` (Summary: M-3; OLD→NEW Option-A
excerpt; the OQ-1 note — audit/brief "0 tags / not tag-carried"
prescription was stale/false post-F6, on-disk-true Option A used
instead; scope guards; Test plan: grep battery + line-428-unchanged +
flags-unchanged + reviewer-deep PASS + v3.58.0); `gh pr edit --body-file`;
`gh pr ready` only after T03 APPROVE; **No merge.** Delete
`.github/tmp/*.txt`; produce final report.
**Verification:** `gh pr view --json isDraft` → false; PR NOT merged.
**File scope:** `planning/INDEX.md`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** parent.

## Reviewer routing

- **T01 / T03:** `@reviewer-deep` — mandatory.
- **`@reviewer-adversarial` escalation trigger (precise):** ONLY IF
  reviewer-deep raises an unresolved overclaim/methodology BLOCKER —
  (a) the applied wording still misstates the on-disk artifact
  (re-introduces "0 tags / not tag-carried", or asserts
  `[POP:ranked_ladder]` is the correct discipline tag); (b) contradicts
  CX-17/Tier-4 discipline or the line-212 `[REVIEW]` flag; (c) a Phase
  02/06 closure claim is introduced; (d) the diff exceeds the
  single-locus scope (line 428, other §§, forbidden files). User
  selected Option A verbatim, so adversarial is NOT mandatorily
  pre-triggered. Else NOT invoked.
- **3-round symmetric cap** (execution-side too); unresolved after
  round 3 → recorded residual + surfaced to user, not silently expanded.

## Repo-policy resolutions

1. **Version bump REQUIRED, minor:** `docs/` ⇒ minor; 3.57.0 → 3.58.0 (T04).
2. **WRITING_STATUS.md YES (user decision)** — one additive dated line on
   the §4.1.4 row (supersedes that row's stale pre-F6 "0 tags" lineage).
   **REVIEW_QUEUE.md NO (user decision)** — no exact open TQ-05/M-3
   work-row; line-212 `[REVIEW]` flag deliberately retained.
3. **planning/INDEX.md (T00):** archive merged PR #222, set this branch active.
4. **pass2_evidence stale text OUT of scope (OQ-3, informational):** the
   readiness-audit / citation-audit pre-F6 "0 tags" text + WRITING_STATUS
   row are superseded in the CHAPTER + WRITING_STATUS row only;
   `pass2_evidence/**` is forbidden this PR and left as historical audit
   evidence. A future Cat-E/F chore may reconcile it; NOT required for
   M-3 closure.
5. **Stale prior critique-file purge OUT of scope** (residual).
6. Commit/PR conventions: `.github/tmp/commit.txt` + `git commit -F`;
   `.github/tmp/pr.txt` + `--body-file`; delete after; relative paths.
   No `.py` in diff ⇒ no pytest gate.

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00, T05 |
| `planning/current_plan.critique.md` | Create (conditional) | T01 / T03 |
| `thesis/chapters/04_data_and_methodology.md` | Update (line 212 only) | T02 |
| `thesis/WRITING_STATUS.md` | Update (one §4.1.4 dated append) | T02 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T02/T04/T05 |

Explicitly NOT modified: line 428 + every `[REVIEW]`/`[UNVERIFIED]`/
`[POP:]`/`[PRE-canonical_slot]` annotation + sc2egset/aoe2companion
clauses + all other §§ of Ch4; `thesis/references.bib`;
`thesis/chapters/REVIEW_QUEUE.md`; chapters 01/02/03/05/06/07;
`thesis/pass2_evidence/**`; `reports/specs/**`; dataset artifacts;
ROADMAPs; status YAMLs; code; notebooks; `docs/TAXONOMY.md`; `.claude/**`.

## Gate Condition

1. `04_data_and_methodology.md:212` == Option A NEW string; rest of file
   byte-identical to base (exactly one hunk at line 212).
2. Grep battery: `137 wierszy łącznie: 1 nagłówek + 136 wierszy danych`
   present (1, line 212); `(136 wierszy) niesie tag dla aoestats` == 0;
   `136 wierszy danych` count unchanged (line 428 intact);
   `[REVIEW:]`==34, `[UNVERIFIED:]`==1 (= base); sc2egset 35/35 +
   aoe2companion 74/74 present.
3. NEW string is on-disk-true: contains NO "0 tags / not tag-carried /
   NO [POP:] tag" claim; names `[POP:ranked_ladder]` as the provisional
   artifact token superseded in prose by `[POP:1v1_random_map]`; does
   NOT assert `[POP:ranked_ladder]` is correct discipline.
4. Scope containment: `git diff --name-only adf93303..HEAD` ⊆ File
   Manifest; `references.bib`/`REVIEW_QUEUE.md`/`pass2_evidence/**`/
   specs/other chapters/artifacts untouched.
5. WRITING_STATUS §4.1.4 append additive & accurate; REVIEW_QUEUE
   untouched.
6. Version 3.58.0; CHANGELOG `[3.58.0]` `### Fixed`; fresh empty
   `[Unreleased]`; `[3.57.0]` untouched.
7. reviewer-deep APPROVE at T01 and T03; reviewer-adversarial only if
   its trigger fired then resolved; 3-round cap respected.
8. `planning/INDEX.md`: PR #222 archived, this branch active, PR-number
   reconciled. PR ready (`isDraft` false), NOT merged; temp files deleted.

## Out of scope

- Line 428 / `[PRE-canonical_slot]` / `canonical_slot` narrative.
- Altering sc2egset 35/35 or aoe2companion 74/74 (beyond the
  count-preserving "w kolumnie `notes`" parallelism); removing/rewording
  any `[REVIEW]`/`[UNVERIFIED]` flag.
- Asserting `[POP:ranked_ladder]` is the correct discipline tag; any
  Phase 02/06 closure claim; broader cross-game methodology.
- Correcting the stale pre-F6 text in `thesis/pass2_evidence/**` or the
  WRITING_STATUS §4.1.4 row's historical entries (only an additive new
  line is added) — OQ-3, future chore.
- `references.bib`, `REVIEW_QUEUE.md`, any other chapter, specs,
  ROADMAPs, status YAMLs, code, notebooks, `docs/TAXONOMY.md`,
  `.claude/**`; re-deriving the 137-line fact; merging the PR.

## Open questions

- **OQ-1 — RESOLVED (user 2026-05-18): Option A.** On-disk-true wording
  naming the provisional `[POP:ranked_ladder]` token superseded in prose
  by `[POP:1v1_random_map]` / Tier-4 (R02 + `02_00`). The audit/brief
  "0 tags / not tag-carried / implicit-via-spec" prescription is NOT
  used (stale/false post-F6).
- **OQ-2 — RESOLVED (user 2026-05-18):** WRITING_STATUS §4.1.4 dated
  append; no REVIEW_QUEUE change.
- **OQ-3 — RESOLVED (informational):** stale pre-F6 `pass2_evidence/**`
  + WRITING_STATUS-row text left as historical audit evidence; superseded
  in chapter + WRITING_STATUS row only; future Cat-E/F chore may
  reconcile pass2_evidence (out of scope here).
- **R-1 (residual):** stale prior critique-file purge — future
  planning-hygiene sweep.
