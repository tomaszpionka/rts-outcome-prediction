---
title: "Appendix-only bibliography key canonicalization"
category: F
branch: docs/thesis-appendix-key-canonicalization
base_ref: 637fdb9349d59598f211530ac5a2466d2a83bc69
date: 2026-05-19
version_bump: "3.61.0 → 3.62.0"
planner_model: user-directed (executor-ready plan; reviewer-adversarial gate APPROVE-WITH-CONDITIONS)
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/reviews_and_others/related_work_historical_rts_prediction.md
  - thesis/reviews_and_others/related_work_rating_systems.md
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

Appendix-only bibliography key canonicalization. This plan applies five named-key
actions to the two appendix review files
(`thesis/reviews_and_others/related_work_historical_rts_prediction.md` and
`thesis/reviews_and_others/related_work_rating_systems.md`) and updates
CHANGELOG, pyproject.toml, and planning artifacts.

`thesis/references.bib` and `thesis/chapters/**` are BYTE-UNCHANGED this PR.
No new key is added to `references.bib`. The `BT2025Survey` key is NOT renamed
and NOT imported into `references.bib`.

The five named-key actions and their exact semantics (binding conditions
B1/C1/C2/C3 from the reviewer-adversarial gate):

1. **Baek2022 → BaekKim2022** (B1 + C3): key-token-only swap in the embedded
   `@article{…}` block — no field reorder, no whitespace re-alignment. The
   embedded block differs from references.bib in field order and whitespace; the
   Baek2022 block is NOT byte-equal to canonical. Swap the key token only.
   All inline `[Baek2022]` and references-list `- [Baek2022]` leading token
   updated to `BaekKim2022`.

2. **Porcpine2020 → Porcpine2020EloAoE** (C3): key-token-only swap in the
   embedded `@misc{…}` block. References.bib is the single source of truth and
   is untouched; no note/url/howpublished additions are made to the appendix
   block (reading (b): key-swap only). All inline and references-list leading
   token updated to `Porcpine2020EloAoE`.

3. **Herbrich2007 → Herbrich2006** (key/style only; C2): key-token-only swap in
   the embedded `@inproceedings{…}` block. `year = {2007}` is KEPT DELIBERATELY
   and is NOT asserted to be erroneous. All inline `[Herbrich2007]` and
   references-list `- [Herbrich2007]` leading token updated to `[Herbrich2006]`.
   Herbrich key normalized to the canonical alias Herbrich2006 for cross-document
   key consistency; the embedded year = {2007} is retained deliberately and is
   NOT asserted to be erroneous (NeurIPS 2006 proceedings; 2007 publication is a
   venue-year/publication-year distinction, consistent with the canonical entry).

4. **Glickman2025 appendix 2nd-author typo** (one token, one line): in the
   embedded `@article{Glickman2025,…}` block, the `author` line:
   `Jones, Alexander C.` → `Jones, Albyn C.` (2nd author given name only).
   Nothing else in that block changed. The references-list line uses `A.C.` and
   is left unchanged.

5. **BT2025Survey — repair at all three loci** (C1; key UNCHANGED; NOT imported
   into references.bib):
   - Embedded block: `author` → `Fang, Shuxing and Han, Ruijian and Luo,
     Yuanhang and Xu, Yiming`; `year` → `{2026}`; key/title/journal byte-unchanged.
   - Inline prose: `A 2025 survey ([BT2025Survey])` → `A 2026 survey
     ([BT2025Survey])` (year only; key unchanged; rest of sentence unchanged).
   - References-list line: author `Li, Y. et al.` → `Fang, S., Han, R., Luo,
     Y., & Xu, Y.`; year `(2025)` → `(2026)`; title/arXiv id/URL unchanged.
   Half-repair is unsound (C1): all three loci must be repaired together.

---

## Problem Statement

The two appendix review files (`related_work_historical_rts_prediction.md` and
`related_work_rating_systems.md`) use stale bib keys (`Baek2022`,
`Porcpine2020`, `Herbrich2007`) that diverge from the canonical aliases in
`thesis/references.bib` (`BaekKim2022`, `Porcpine2020EloAoE`, `Herbrich2006`),
a second-author given-name typo in the embedded `Glickman2025` block
(`Alexander C.` vs canonical `Albyn C.`), and incorrect author/year metadata in
the embedded `BT2025Survey` block (arXiv:2601.14727 is by Fang, Shuxing et al.
(2026), not Li, Yingqi et al. (2025)).

---

## Assumptions & Unknowns

1. `thesis/references.bib` is the single source of truth for canonical key names
   and entry metadata. It is UNTOUCHED this PR.
2. `thesis/chapters/**` are READ-ONLY this PR (zero diff on chapters).
3. Embedded BibTeX blocks in the appendix files are secondary copies; the
   canonicalization goal is to keep keys consistent across documents, NOT to
   make the appendix blocks byte-equal to canonical entries. Field order and
   whitespace inside embedded blocks are NOT modified beyond the named changes.
4. Herbrich2007 → Herbrich2006 is a key/style-only normalization. The embedded
   `year = {2007}` reflects the venue-year/publication-year distinction of NeurIPS
   2006 proceedings; it is retained deliberately and is NOT an error claim.
5. BT2025Survey is a real paper (arXiv:2601.14727, confirmed); key is retained;
   author and year metadata are repaired in the appendix embedded block and
   references list.
6. Unknown: whether any other embedded block in the two files diverges from
   references.bib in ways not listed here — covered by the read-only sweep
   (sweep-and-report, not edit).

## Literature Context

This plan does not introduce new literature. It corrects key aliases and metadata
of existing bibliographic entries using primary sources already in the audit record
and in `thesis/references.bib`. No new references are added. No chapter prose is
edited. The five named keys (`BaekKim2022`, `Porcpine2020EloAoE`, `Herbrich2006`,
`Glickman2025`, `BT2025Survey`) are already present in `thesis/references.bib`;
this plan synchronizes the appendix-file aliases and metadata to match.

---

## Open Questions

None blocking execution. All methodology questions resolved by the
reviewer-adversarial gate (B1/C1/C2/C3).

---

## Execution Steps

### T00 — Branch first

`git checkout -b docs/thesis-appendix-key-canonicalization` from master @
637fdb9349d59598f211530ac5a2466d2a83bc69.

### T01 — related_work_historical_rts_prediction.md

Re-grep for `Baek2022` first. Then:
- All inline `[Baek2022]` → `[BaekKim2022]`.
- References-list leading token `- [Baek2022]` → `- [BaekKim2022]`; rest
  of line byte-unchanged.
- Embedded `@article{Baek2022,` → `@article{BaekKim2022,` — KEY TOKEN ONLY;
  all other fields byte-unchanged (B1 + C3: block is NOT byte-equal to canonical;
  key-only swap, no field reorder, no whitespace re-alignment).

### T02 — related_work_rating_systems.md

Re-grep before editing. Then apply the four actions:

**Porcpine2020 → Porcpine2020EloAoE** (C3):
- All inline `[Porcpine2020]` → `[Porcpine2020EloAoE]`.
- References-list leading token → `[Porcpine2020EloAoE]`; rest byte-unchanged.
- Embedded `@misc{Porcpine2020,` → `@misc{Porcpine2020EloAoE,` — KEY TOKEN ONLY;
  all other fields byte-unchanged (no note/url/howpublished additions).

**Herbrich2007 → Herbrich2006** (C2):
- All inline `[Herbrich2007]` → `[Herbrich2006]` (including comparison-table cell).
- References-list leading token → `[Herbrich2006]`; entry body verbatim
  (including "(2007)" and "Proc. NeurIPS 2006").
- Embedded `@inproceedings{Herbrich2007,` → `@inproceedings{Herbrich2006,` —
  KEY TOKEN ONLY; KEEP `year = {2007}`; all other fields byte-unchanged.
- No prose added claiming 2007 is an error.

**Glickman2025 appendix 2nd-author typo**:
- In embedded `@article{Glickman2025,…}` block, `author` line:
  `Jones, Alexander C.` → `Jones, Albyn C.` (one token). Nothing else changed.
- References-list `A.C.` — left unchanged.

**BT2025Survey — repair at all three loci** (C1):
- Embedded block: `author = {Li, Yingqi and others},` →
  `author = {Fang, Shuxing and Han, Ruijian and Luo, Yuanhang and Xu, Yiming},`;
  `year = {2025}` → `year = {2026}`; key/title/journal byte-unchanged.
- Inline prose: `A 2025 survey ([BT2025Survey])` → `A 2026 survey ([BT2025Survey])`.
- References-list: `Li, Y. et al. (2025)` → `Fang, S., Han, R., Luo, Y., & Xu, Y. (2026)`;
  title/arXiv id/URL unchanged; URL stays inside `<…>`.

**Read-only sweep**: scan all OTHER embedded BibTeX blocks in BOTH files vs
`thesis/references.bib`; list any divergence in the PR body as deferred
follow-up candidates. DO NOT edit non-named blocks.

### T03 — Planning / release tail

- Write `planning/current_plan.md` (this file).
- Write `planning/current_plan.critique.md` with Round-1 reviewer-adversarial
  critique verbatim.
- Update `planning/INDEX.md`: archive the prior active line; set new active line.
- Update `CHANGELOG.md`: insert `[3.62.0]` above `[3.61.0]`; `[3.61.0]`
  byte-unchanged; leave `[Unreleased]` with empty headers.
- Update `pyproject.toml`: `version = "3.61.0"` → `"3.62.0"`.

### Commit / push / PR

Stage only the 7 manifest files. Commit via `.github/tmp/commit.txt`. Push.
Open non-draft PR. After PR number known: replace `#NNN` → `#<N>` in CHANGELOG
`[3.62.0]` header only; commit + push. Delete `.github/tmp/pr.txt` and
`.github/tmp/commit.txt`.

---

## File Manifest

| File | Change |
|------|--------|
| `thesis/reviews_and_others/related_work_historical_rts_prediction.md` | Baek2022→BaekKim2022: 2 inline + 1 ref-list + 1 embedded key token |
| `thesis/reviews_and_others/related_work_rating_systems.md` | Porcpine/Herbrich/Glickman/BT2025Survey: inline + ref-list + embedded |
| `CHANGELOG.md` | `[3.62.0]` section added; `[3.61.0]` unchanged |
| `pyproject.toml` | version `3.61.0` → `3.62.0` |
| `planning/INDEX.md` | Archive row added; Active plan replaced |
| `planning/current_plan.md` | This file (plan artifact) |
| `planning/current_plan.critique.md` | Round-1 reviewer-adversarial critique |

---

## Gate Condition

Reviewer-adversarial Round-1 gate: APPROVE-WITH-CONDITIONS (B1/C1/C2/C3 bound).
Round-2 FINAL gate will be APPENDED to `planning/current_plan.critique.md`
under a distinct heading after PR creation.

No `.py` files changed — no pytest/ruff/mypy gate required.
PR left NOT merged pending FINAL gate and explicit user approval.

---

## Out of Scope / Forbidden Paths

- `thesis/references.bib` — READ-ONLY (zero diff)
- `thesis/chapters/**` — READ-ONLY (zero diff)
- Any other `thesis/` file except the two named `thesis/reviews_and_others/` files
- `src/**`, `tests/**`, `notebooks/**`, `data/**` — zero diff
- No new key added to `references.bib`
- `BT2025Survey` key NOT renamed and NOT imported into `references.bib`

---

## Deliverables

1. `thesis/reviews_and_others/related_work_historical_rts_prediction.md` with
   Baek2022→BaekKim2022 applied at all loci (key-token-only in embedded block).
2. `thesis/reviews_and_others/related_work_rating_systems.md` with all four
   named actions applied.
3. `CHANGELOG.md` with `[3.62.0]` added (historical entries byte-unchanged).
4. `pyproject.toml` at version `3.62.0`.
5. `planning/INDEX.md` with archive row + updated active plan line.
6. `planning/current_plan.md` (this file).
7. `planning/current_plan.critique.md` (Round-1 critique).
8. One atomic commit on branch `docs/thesis-appendix-key-canonicalization`.
