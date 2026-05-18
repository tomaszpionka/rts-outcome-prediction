---
title: "EsportsBench §2.5.5 version harmonisation (Chapters 1–4 audit must-fix M-1)"
category: F
branch: docs/thesis-esportsbench-version-harmonization
base_ref: c68786273fbdf3c2c8c3e6046ea559acc1e9b570
date: 2026-05-18
planner_model: claude-opus-4-7[1m] (planner-science)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md
  - thesis/pass2_evidence/literature_verification_log.md
  - thesis/chapters/03_related_work.md
critique_required: false
research_log_ref: null
---

# Plan: EsportsBench §2.5.5 version harmonisation (must-fix M-1)

> **User-directed reviewer deviation (binding).** M-1 originates from the PR #220
> Chapters 1–4 citation audit (itself a reviewer-gated Category F deliverable).
> Per the user task brief, **reviewer-deep is the mandatory plan gate (T01) and
> final gate (T03)**; reviewer-adversarial is conditional (escalation trigger
> only). `critique_required: false` reflects "no mandatory pre-execution
> adversarial critique", substituted by a mandatory reviewer-deep plan review.
> The audit itself (`ch1_ch4_citation_literature_support_audit.md` §7 M-1, §11
> PR-1) routes M-1 to reviewer-deep. Recorded for provenance.

## Scope

Single-locus literature-currency harmonisation. Replace exactly one
parenthetical in `thesis/chapters/02_theoretical_background.md` §2.5.5
(line 179) so the EsportsBench version/cutoff matches the already-correct
Chapter 3 (§3.2.4 line 77, §3.5 line 189). This removes a cross-chapter
self-contradiction on a quantitative comparator (the SC2 Aligulac
411 030-match / ~80% Glicko line) and unblocks Chapter 2 from `not_ready`
→ `ready_to_send_with_disclaimer` for supervisor handoff. Plus the
obligatory repo-hygiene tail (version bump, CHANGELOG, planning artifacts,
one dated WRITING_STATUS append). Nothing else.

## Problem Statement

Audit C-01 (`ch1_ch4_citation_literature_support_audit.md:96`, HIGH):
`02_theoretical_background.md:179` still cites EsportsBench as
`v8.0 / cutoff 2025-12-31`, while T14 corrected `03_related_work.md:77`
and `:189` to `v9.0 / cutoff 2026-03-31 / dostęp 2026-04-26`. Per audit §3,
*with M-1 applied* Chapter 2 is `ready_to_send_with_disclaimer`; *without
M-1* it is `not_ready` because the comparator self-contradicts Chapter 3.
M-1 is the only `fix_before_supervisor` item in Chapter 2 and the single
HIGH issue in the audit. It is a currency defect in a comparator already
verified at v9.0 elsewhere — not a methodology defect.

## Assumptions & unknowns

- **Assumption A1:** the string `wersja HuggingFace v8.0, cutoff 2025-12-31`
  occurs exactly once in `02_theoretical_background.md` (line 179).
  *Verified at plan time:* `grep -c` = 1. Falsifier: count ≠ 1 at T02 →
  HALT. The only other EsportsBench mention (line 39) has no version
  parenthetical and is OUT of scope.
- **Assumption A2:** Ch3 §3.2.4 (line 77) and §3.5 (line 189) are already
  correct at HEAD. *Verified at plan time:* both read
  `v9.0 / cutoff 2026-03-31 / dostęp 2026-04-26` verbatim. No live
  inconsistency at HEAD; Ch3 is explicitly NOT touched.
- **Assumption A3:** no `references.bib` change is needed. *Verified:*
  `Thorrez2024` exists (`references.bib:147`); the version label is
  chapter-prose, not a bib field.
- **Unknown (resolved):** whether the §2.5.5 sentence needs prose
  rewriting beyond the parenthetical → ruled "mechanical" (executor;
  writer-thesis NOT needed — see Reviewer routing).
- No web verification required (see Literature context). No open
  methodological unknowns.

## Literature context

EsportsBench [Thorrez2024] current released version is **v9.0**, cutoff
**2026-03-31**, HuggingFace dataset card verified **2026-04-26** — per
`literature_verification_log.md` note 4 (records the v9.0 dataset-card
verification) and the Thorrez2024 verification row (status `corrected`;
recorded URL `https://huggingface.co/datasets/EsportsBench/EsportsBench`,
accessed 2026-04-26), and re-confirmed by audit C-01. This value is
already in Chapter 3 (`03_related_work.md:77`, `:189`). The harmonisation
makes Chapter 2 consistent with Chapter 3 and the verification log. No
`[OPINION]`/`[REVIEW]`/`[UNVERIFIED]` flag is needed or added — the value
is web-verified by T14 and reused (reuse-before-reverify). **No new
EsportsBench version is introduced; no WebFetch/WebSearch in this PR.**

## The single Chapter-2 edit (exact strings — load-bearing)

**File:** `thesis/chapters/02_theoretical_background.md`, line 179.

OLD (unique fragment the executor's Edit must match verbatim):
`EsportsBench [Thorrez2024] — referencyjny zbiór benchmarków obejmujący ponad 20 tytułów esportowych, w tym StarCraft II z 411 030 meczami pochodzącymi z Aligulac (wersja HuggingFace v8.0, cutoff 2025-12-31) — benchmarkuje paired-comparison rating systems`

NEW:
`EsportsBench [Thorrez2024] — referencyjny zbiór benchmarków obejmujący ponad 20 tytułów esportowych, w tym StarCraft II z 411 030 meczami pochodzącymi z Aligulac (wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26) — benchmarkuje paired-comparison rating systems`

Net change: parenthetical `(wersja HuggingFace v8.0, cutoff 2025-12-31)`
→ `(wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26)`.
Everything outside the parentheses is byte-identical. No sentence
restructuring, no flag added/removed, no other line touched. The NEW
parenthetical is character-identical to `03_related_work.md:77`.

## Repo-policy resolutions

1. **Version bump REQUIRED, minor.** `.claude/rules/git-workflow.md`
   step 2: `docs/` ⇒ minor. `3.55.0` → **`3.56.0`** (T04). CHANGELOG
   `[Unreleased]` → `## [3.56.0] — 2026-05-18` with a `### Fixed` entry;
   fresh empty `[Unreleased]` with the four headers preserved.
2. **`WRITING_STATUS.md` update: YES (T02, minimal).** One dated append
   to the §2.5 EsportsBench-history row (append only; do not rewrite
   prior history): records the M-1 correction, the supersession of the
   2026-04-21 local-closure v8.0 value by T14 web-verification, and the
   Chapter-2 readiness transition `not_ready` → `ready_to_send_with_disclaimer`.
3. **`REVIEW_QUEUE.md`: NO (user-confirmed).** It tracks items *awaiting*
   Pass-2, not completed corrections; no open M-1 row exists. Audit doc
   + WRITING_STATUS append are the provenance sinks.
4. **`planning/INDEX.md` (T00):** archive merged PR #220 row; set this
   branch active.
5. **Stale PR #220 critique-file purge: OUT of scope** (residual; the
   planning-drift hook constrains the plan, not stale critique files).
6. **Commit/PR conventions:** commit message via `.github/tmp/commit.txt`
   + `git commit -F`; PR body via `.github/tmp/pr.txt` + `--body-file`;
   delete both after; relative paths from repo root. No `.py` in diff ⇒
   no pytest/coverage gate.

## Execution Steps

### T00 — Branch + full plan + INDEX archive + draft PR

**Objective:** Bootstrap the PR with a planning-drift-complete plan.

**Instructions:**
1. Branch `docs/thesis-esportsbench-version-harmonization` off
   `c6878627` (done).
2. Write this full Category F plan to `planning/current_plan.md`.
3. `planning/INDEX.md`: archive PR #220 row; set this branch active.
4. Commit via `.github/tmp/commit.txt` + `git commit -F` (message
   `chore(pr): bootstrap draft PR for EsportsBench §2.5.5 harmonisation [M-1]`);
   push `-u`.
5. `gh pr create --draft --title "docs(thesis): harmonize EsportsBench version citation in Chapter 2" --body-file .github/tmp/pr.txt`; delete `.github/tmp/*.txt`.

**Verification:** `gh pr view --json isDraft` → true; planning-drift hook
passes; `git show --stat HEAD` = only `planning/current_plan.md` +
`planning/INDEX.md`.

**File scope:** `planning/current_plan.md`, `planning/INDEX.md`,
`.github/tmp/*`. **Read scope:** —. **Push:** yes. **Executor:** parent
(Sonnet-equivalent mechanical bootstrap).

### T01 — reviewer-deep plan review (HALT on blocker)

**Objective:** Validate the plan before any chapter edit.

**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `c6878627`. Checks: (a) NEW string == `03_related_work.md:77`
canonical form; (b) Ch3 confirmed not touched / no live HEAD inconsistency;
(c) no new version introduced, no web needed; (d) TQ-04 stale "§3.2.4
internal contradiction" sub-claim NOT actioned; (e) line 39 / §3.2.4 /
§3.5 out of scope; (f) version-bump + WRITING_STATUS-yes / REVIEW_QUEUE-no
decisions sound; (g) no `references.bib` change possible. If reviewer-deep
raises a methodology/source-scope BLOCKER: HALT, surface to user, amend
only on user direction, re-review. If reviewer output committed → write to
`planning/current_plan.critique.md`, commit, push.

**Verification:** reviewer-deep verdict, 0 unresolved BLOCKERs.
**File scope:** `planning/current_plan.critique.md`, `.github/tmp/*`.
**Read scope:** `planning/current_plan.md`. **Push:** yes if critique
committed.

### T02 — The single mechanical edit + WRITING_STATUS append

**Objective:** Apply the one parenthetical substitution + minimal
WRITING_STATUS append.

**Instructions:**
1. Pre-edit uniqueness check (A1 falsifier):
   `grep -c "wersja HuggingFace v8.0, cutoff 2025-12-31" thesis/chapters/02_theoretical_background.md`
   MUST be exactly 1. If not → HALT, report, do not edit.
2. Edit `02_theoretical_background.md:179`: replace the OLD fragment with
   the NEW fragment (exact strings above; match the full quoted fragment
   for uniqueness).
3. Append the dated M-1 line to the §2.5 row of `thesis/WRITING_STATUS.md`
   (append only; date 2026-05-18; records M-1 done, v8.0→v9.0 correction,
   2026-04-21 local-closure superseded by T14, Chapter-2 `not_ready` →
   `ready_to_send_with_disclaimer`).
4. Do NOT touch `02_theoretical_background.md:39`, the `[REVIEW: F4.5 ...]`
   flag, §3.2.4, §3.5, `references.bib`, or `REVIEW_QUEUE.md`.
5. Commit via `.github/tmp/commit.txt` + `git commit -F` (message
   `docs(thesis): harmonise EsportsBench §2.5.5 version v8.0→v9.0 to match Ch3 [M-1]`);
   push.

**Verification (grep validation battery):**
- `grep -c "wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26" thesis/chapters/02_theoretical_background.md` ≥ 1
- `grep -c "v8.0" thesis/chapters/02_theoretical_background.md` = 0
- `grep -c "2025-12-31" thesis/chapters/02_theoretical_background.md` = 0
- `grep -c "80,13%" thesis/chapters/02_theoretical_background.md` unchanged vs HEAD (≥1; line 39 intact)
- `grep -c "REVIEW: F4.5" thesis/chapters/02_theoretical_background.md` unchanged vs HEAD
- `git diff --name-only c6878627..HEAD` ⊆ {planning/current_plan.md, planning/INDEX.md, thesis/chapters/02_theoretical_background.md, thesis/WRITING_STATUS.md}
- `git diff c6878627..HEAD -- thesis/chapters/03_related_work.md` empty
- `git diff c6878627..HEAD -- thesis/references.bib` empty

**File scope:** `thesis/chapters/02_theoretical_background.md`,
`thesis/WRITING_STATUS.md`, `.github/tmp/*`. **Read scope:** those two
files. **Push:** yes. **Executor:** @executor on **Sonnet** (mechanically
specified; canonical value + byte-level strings + falsifier all resolved
in this plan; no thesis-facing methodological judgement at execution time
per the data-analysis-lineage routing rule).

### T03 — reviewer-deep final check

**Objective:** Validate the applied diff.

**Instructions:** Dispatch `@reviewer-deep` with `planning/current_plan.md`
+ base_ref `c6878627`. Verify: edit == spec; grep battery passes; Ch3
byte-unchanged; line 39 + F4.5 flag untouched; no `references.bib` change;
WRITING_STATUS append additive & accurate; no scope creep. Escalate to
`@reviewer-adversarial` ONLY on an unresolved overclaim/methodology
BLOCKER (trigger list in Reviewer routing); 3-round symmetric cap. Apply
only mechanical in-scope fixes; substantive residual → audit-style record
+ surface to user. Commit + push if changed.

**Verification:** reviewer-deep APPROVE, 0 unresolved BLOCKERs.
**File scope:** `thesis/chapters/02_theoretical_background.md`,
`planning/current_plan.critique.md`, `.github/tmp/*`. **Read scope:** diff.
**Push:** yes if changed.

### T04 — Version bump + CHANGELOG

**Objective:** Standard release hygiene.

**Instructions:**
1. `pyproject.toml` `version = "3.55.0"` → `"3.56.0"`.
2. CHANGELOG `[Unreleased]` → `## [3.56.0] — 2026-05-18 (PR #<n>: docs/thesis-esportsbench-version-harmonization)`; `### Fixed` entry for the M-1 harmonisation; fresh empty `[Unreleased]` with the four headers. `<n>` from `gh pr view --json number`.
3. Commit `chore(release): bump version to 3.56.0`; push.

**Verification:** `pyproject.toml` = 3.56.0; CHANGELOG `[Unreleased]`
empty with 4 headers; one `### Fixed` bullet under `[3.56.0]`.
**File scope:** `pyproject.toml`, `CHANGELOG.md`, `.github/tmp/*`.
**Read scope:** —. **Push:** yes. **Executor:** @executor on **Sonnet**
(mechanical).

### T05 — PR body refresh + mark ready (NO merge)

**Objective:** Finalize the PR for review without merging.

**Instructions:**
1. Reconcile the PR-number placeholder in `planning/INDEX.md` active line
   (single edit; fold into a small commit or the T04 commit).
2. Refresh `.github/tmp/pr.txt` per `.github/pull_request_template.md`
   (Summary: M-1/C-01, exact old→new parenthetical, scope guards Ch3/line
   39/F4.5/bib untouched; Test plan: grep battery + reviewer-deep PASS +
   v3.56.0; footer). `gh pr edit --body-file`.
3. `gh pr ready` only after T03 APPROVE on record. **No merge.** Delete
   `.github/tmp/*.txt`. Produce final report.

**Verification:** `gh pr view --json isDraft` → false; PR NOT merged.
**File scope:** `planning/INDEX.md`, `.github/tmp/*`. **Read scope:** —.
**Push:** yes (INDEX reconciliation).

## Reviewer routing

- **T01 (plan)** and **T03 (final):** `@reviewer-deep` — mandatory
  (substituted gate per the critique provenance note).
- **`@reviewer-adversarial` escalation trigger (precise):** invoke ONLY
  IF reviewer-deep (T01 or T03) raises an unresolved overclaim/methodology
  BLOCKER — specifically: (a) disputes that
  `v9.0 / 2026-03-31 / dostęp 2026-04-26` is the canonical value;
  (b) asserts a live Ch3 inconsistency at HEAD; (c) argues web
  re-verification is methodologically required before the edit;
  (d) argues the WRITING_STATUS append overclaims the readiness
  transition. A formatting nit / wording suggestion / scope-confirmation
  request is NOT a trigger.
- **3-round symmetric cap:** plan-side and execution-side adversarial
  review (if triggered) each capped at 3 rounds; symmetric. BLOCKER
  surviving 3 rounds → HALT + surface to user.

## writer-thesis vs executor ruling

**Mechanical → @executor (Sonnet). writer-thesis NOT needed.** The change
is a single parenthetical substitution inside a sentence whose surrounding
clause is byte-identical before/after; no prose authoring, argument
construction, register/idiom judgement, citation insertion, or flag
authoring. The target string equals the already-approved §3.2.4 wording
character-for-character. Per the data-analysis-lineage routing rule, a
mechanically-specified step whose methodological decision is fully
resolved in the plan routes to a Sonnet executor.

## File Manifest

| File | Action | Task |
|------|--------|------|
| `planning/current_plan.md` | Rewrite | T00 |
| `planning/INDEX.md` | Update | T00, T05 |
| `planning/current_plan.critique.md` | Create (conditional) | T01 / T03 |
| `thesis/chapters/02_theoretical_background.md` | Update (line 179 only) | T02 |
| `thesis/WRITING_STATUS.md` | Update (one §2.5 append) | T02 |
| `CHANGELOG.md` | Update | T04 |
| `pyproject.toml` | Update | T04 |
| `.github/tmp/commit.txt`, `.github/tmp/pr.txt` | Create then Delete (ephemeral) | T00/T02/T04/T05 |

## Gate Condition

1. `02_theoretical_background.md:179` reads
   `(wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26)`; rest
   of the sentence byte-identical to HEAD.
2. Grep battery (all pass): new string ≥1; `v8.0` = 0; `2025-12-31` = 0;
   `80,13%` unchanged; `REVIEW: F4.5` unchanged.
3. `git diff --name-only c6878627..HEAD` ⊆ {`planning/current_plan.md`,
   `planning/INDEX.md`, `planning/current_plan.critique.md` (conditional),
   `thesis/chapters/02_theoretical_background.md`,
   `thesis/WRITING_STATUS.md`, `CHANGELOG.md`, `pyproject.toml`}.
4. `git diff c6878627..HEAD -- thesis/chapters/03_related_work.md` empty.
5. `git diff c6878627..HEAD -- thesis/references.bib` empty.
6. `pyproject.toml` = 3.56.0; CHANGELOG has the `[3.56.0]` `### Fixed`
   entry; `[Unreleased]` empty with 4 headers.
7. reviewer-deep APPROVE at T01 and T03; planning-drift + pre-commit
   hooks green.
8. Draft PR opened at T00; marked ready only after T03 APPROVE; NOT
   merged; temp files deleted.
9. Resolution matches audit M-1 / PR-1 exactly; TQ-04 stale sub-claim NOT
   actioned; line 39 / §3.2.4 / §3.5 NOT modified.

## Out of scope

- `02_theoretical_background.md:39`, the `[REVIEW: F4.5 ...]` flag, §2.2.3.
- §3.2.4 / §3.5 (already correct at HEAD).
- TQ-04's stale "§3.2.4 internal contradiction" sub-claim (C-04).
- M-2 (Ch1 bib consolidation — PR-2) and M-3 (TQ-05 aoestats — PR-3).
- Any web verification / new EsportsBench version.
- `references.bib`, any other chapter, any non-prose artifact, any
  unrelated flag.
- Stale PR #220 planning critique-file purge (residual repo-hygiene).

## Open questions

- **Q1 — RESOLVED (user decision 2026-05-18):** WRITING_STATUS.md §2.5
  dated append YES; REVIEW_QUEUE.md NO change. Resolved by user.
- **R-1 (residual, no decision needed):** stale PR #220
  `planning/current_plan.critique*.md` purge is OUT of scope; flagged for
  a future planning-hygiene sweep.
