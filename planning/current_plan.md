---
# Layer 1 — fixed frontmatter (mechanically validated)
category: F
branch: docs/thesis-ch4-corpus-framing-residuals
date: 2026-04-19
planner_model: claude-opus-4-7
dataset: null
phase: null
pipeline_section: null
invariants_touched: [I5, I8]
source_artifacts:
  - planning/CHAPTER_4_DEFEND_IN_THESIS.md
  - thesis/chapters/04_data_and_methodology.md
  - thesis/chapters/REVIEW_QUEUE.md
  - thesis/WRITING_STATUS.md
  - reports/specs/01_05_preregistration.md
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.json
  - src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.csv
  - src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_phase06_interface_aoe2companion.csv
  - .claude/scientific-invariants.md
  - .claude/rules/thesis-writing.md
  - docs/templates/plan_template.md
critique_required: true
research_log_ref: null
---

# Plan: Chapter 4 DEFEND-IN-THESIS residuals — corpus framing (PR-1 of 3)

## Scope

First of three Cat F PRs addressing the six DEFEND-IN-THESIS residuals from
`planning/CHAPTER_4_DEFEND_IN_THESIS.md`. This PR covers **three
corpus-framing residuals (#1, #2, #4)** — all of which describe properties of
the corpora themselves (reference-window construction, population scope,
aoestats cohort ceiling). PR-2 covers methodology-level residuals (#3, #6);
PR-3 covers the `canonical_slot` flag (#5). All edits land in
`thesis/chapters/04_data_and_methodology.md` §4.1 subsections. No
cross-cutting methodology discussions (those live in PR-2 §4.4.5); no
cross-references to Tabela 4.7 (which does not yet exist on master).

## Problem Statement

Post-v1.0.5 spec + master `63257289`, three facts about the three corpora
have no resting place in Chapter 4:

1. **Reference-window asymmetry (#1).** sc2egset and aoe2companion use a
   4-month reference period (2022-08-29 → 2022-12-31, spec §7); aoestats
   uses a 9-week patch-anchored single-patch window (2022-08-29 → 2022-10-27,
   patch 66692, spec §7 + §11 W3 ARTEFACT_EDGE binding). The examiner
   question "why not comparable length?" is anticipated in the DEFEND doc
   and must be answered in prose, with the construction rationale (patch
   homogeneity > comparable length) explicit in §4.1.3 before the
   cross-corpus asymmetry framing concludes.

2. **Population-scope differences (#2).** sc2egset is `[POP:tournament]`,
   aoe2companion is `[POP:ranked_ladder]` (broad skill range), aoestats is
   `[POP:ranked_ladder]` but with a different upstream crawler. The examiner
   question "what does it mean to compare ICC between 'AoE2 players' and
   'SC2 players' when samples are differently scoped?" is anticipated in
   the DEFEND doc. The thesis must state once (at the end of §4.1) that all
   cross-dataset claims are **dataset-conditional**, with `[POP:]` as a
   controlled experimental variable per invariant #8 — not a confound.

3. **aoestats 744-player cohort ceiling (#4).** Spec §11 W3 ARTEFACT_EDGE
   binding forces aoestats to restrict the reference to patch 66692 (9
   weeks); at the §6.3 default cohort threshold N=10, the sensitivity
   table in `01_05_05_icc_results.json` gives 4 325 / 744 / 3 eligible
   players at N=5 / N=10 / N=20 respectively. The examiner question "why
   so small?" needs a construction-rationale answer in §4.1.2.1 (the
   aoestats corpus subsection). Identification-side ICC defense (Gelman &
   Hill 2007 §11-12 reasoning that ICC point estimates are well-identified
   with 20–50 clusters) is deferred to PR-2 §4.4.5, where ICC is actually
   reported.

The three residuals are mechanically entangled: #1 extends §4.1.3's
asymmetry framing; #2 closes §4.1 as a new §4.1.4; #4 adds a new
subsection paragraph inside §4.1.2.1 between the "Schemat analityczny"
and "Jakość danych" subsections. Bundling them into one PR minimizes
§4.1 diff churn across subsequent PRs and gives reviewer-adversarial a
coherent block to audit.

## Assumptions & unknowns

- **Assumption:** The sensitivity-table player counts (4 325 / 744 / 3) and
  ICC values (0.0251 / 0.0268 / 0.0176) in `01_05_05_icc_results.json`
  lines 13–71 are the **authoritative** post-v1.0.5 numbers. Verified
  2026-04-19 (session transcript) via direct JSON read + cross-check
  against `phase06_interface_aoestats.csv` rows 122/124/126. These are
  the exact numbers writer-thesis will cite.
- **Assumption:** Spec §11 W3 ARTEFACT_EDGE binding is the canonical
  citation for the single-patch constraint. Spec §7 is the canonical
  citation for the 4-month reference period for sc2egset + aoe2companion.
  Both bindings live in `reports/specs/01_05_preregistration.md` at master
  `63257289`; the plan cites file-only, with line numbers resolved at
  draft time.
- **Assumption:** Invariant #8 in `.claude/scientific-invariants.md` is the
  canonical citation for the cross-game comparative-methodology claim.
  Demsar 2006 (already in `references.bib` via §2.6) is a **supporting**
  citation for residual #2 but is NOT the primary anchor — the
  comparative framing is a project-internal invariant, not a
  literature-derived rule.
- **Unknown:** Exact line numbers inside §4.1.2.1 where the 744-player
  paragraph should slot. Writer-thesis resolves by choosing between
  "after `Jakość danych` (line 89) / before `Dryf schematu` (line 97)"
  or a dedicated new paragraph. Resolved at draft time with the
  constraint "before Tabela 4.2 (line 101)" — the paragraph should
  precede the CONSORT flow so the reader has the 744 number in hand
  when reading the table.
- **Unknown:** Whether §4.1.4 gets a numbered header (`#### 4.1.4
  Zakres populacji — ramy porównawcze`) or an unnumbered `##### Zakres
  populacji` subsection. Resolved by writer-thesis per consistency
  with §4.1.3's numbering (which IS numbered, so §4.1.4 should also be
  numbered).

## Literature context

Primary citations (all already in `references.bib` at master
`63257289`; **no new bibtex entries in this PR**):

- **Spec §7 + §11** (`reports/specs/01_05_preregistration.md`) — project
  preregistration document; reference-period construction and W3
  ARTEFACT_EDGE binding live here. Cite as file path (not bibkey).
- **Invariant #8** (`.claude/scientific-invariants.md`) —
  cross-game/cross-dataset comparability methodology. Project-internal
  document; cite as file path.
- **[Demsar2006]** — *Statistical Comparisons of Classifiers over Multiple
  Data Sets*, JMLR 7:1–30. Already cited in §2.6. Residual #2 may
  reference it as supporting the N≥5 convention (which residual #6
  addresses explicitly in PR-2); avoid re-introducing the bibkey, cite
  once in §4.1.4 only if the comparative-methodology paragraph naturally
  calls for it. [OPINION] writer-thesis decides at draft time.
- **[Gelman2007]** — *Data Analysis Using Regression and
  Multilevel/Hierarchical Models*, §11-12. Cited by residual #4's defense
  framing for the claim "ICC point estimates are reasonable with as few
  as 20-50 clusters". NOTE: this is an **identification-side** claim
  which belongs in PR-2 §4.4.5, NOT in PR-1's §4.1.2.1 construction
  paragraph. Do NOT cite Gelman2007 in this PR; the §4.1.2.1 paragraph
  states the cohort-size fact and references §4.4.5 forward for
  identification discussion.

`[OPINION]` tag: The decision to split #4 into construction-rationale
(§4.1.2.1, this PR) + identification-discussion (§4.4.5, PR-2) is a
planner-science judgment call not derivable from the DEFEND doc's
"mention once when reporting the 0.0268 ANOVA ICC" language alone.
Rationale: §4.1.2.1 currently stops at 01_04 content (cleaning,
asymmetry, schema drift); jumping to 01_05 ICC identification there
would disrupt the 01_04 → 01_05 → 01_06 narrative arc of Chapter 4.
Better to leave construction in §4.1 and identification in §4.4.

## Execution Steps

### T01 — §4.1.3 tail paragraph: reference-window asymmetry defense

**Objective:** Add a single defense paragraph at the end of §4.1.3
(after the current line 201 closing paragraph, before §4.2 at line 205)
that explicitly anticipates the examiner question "why doesn't aoestats
use a comparable-length reference?" and answers with the
patch-homogeneity > comparable-length argument. The paragraph must name
spec §7 and §11 explicitly.

**Instructions:**
1. Read current §4.1.3 lines 161–203 (Asymetria korpusów — ramy
   porównawcze). Verify understanding: the section already hosts Tables
   4.4a (scale/acquisition) and 4.4b (analytic asymmetry) + 3
   discussion paragraphs. The NEW paragraph extends the section by
   addressing the fourth asymmetry axis — **reference-window
   construction** — not covered by the existing Tables.
2. Draft a Polish paragraph (300–500 chars with spaces) that makes
   three moves:
   - (a) State the asymmetry plainly: sc2egset and aoe2companion use a
     4-month reference period (2022-08-29 → 2022-12-31, cytując
     `reports/specs/01_05_preregistration.md` §7); aoestats uses a
     9-week patch-anchored reference (2022-08-29 → 2022-10-27, patch
     66692) — cytując §7 aoestats-rationale paragraph and §11 W3
     ARTEFACT_EDGE binding.
   - (b) Name the design priority: within-reference distributional
     homogeneity (not comparable length). Extending the aoestats
     window across a patch boundary would confound the reference
     distribution with patch-regime shift; spec §7 is explicit that
     homogeneity is the priority.
   - (c) Pre-empt the examiner: the asymmetry is a known, locked,
     justified design choice — not post-hoc rescue. PSI / ICC findings
     depend on reference **distribution**, not reference **length**;
     homogeneity protects distribution.
3. Plant `[REVIEW: Pass-2 — patch-anchored vs. comparable-length
   framing; verify Polish idiom for "patch-regime shift"]` flag at
   the end of the paragraph.
4. Update `thesis/chapters/REVIEW_QUEUE.md` with a new Pending entry
   for §4.1.3 (updated paragraph). Format per existing entries in the
   file: one table row, columns {Section, Chapter file, Drafted date,
   Flag count, Key artifacts, Pass 2 status}. Key artifacts:
   `planning/CHAPTER_4_DEFEND_IN_THESIS.md` Residual #1,
   `reports/specs/01_05_preregistration.md` §7 + §11, the DEFEND doc's
   framing sketch.
5. Update `thesis/WRITING_STATUS.md` §4.1.3 row: keep status `DRAFTED`,
   extend the Notes cell with a `**2026-04-19:** defense paragraph
   added for reference-window asymmetry (Residual #1 of
   CHAPTER_4_DEFEND_IN_THESIS)` note.

**Verification:**
- The new paragraph is the LAST paragraph of §4.1.3 (between current
  line 201 closing paragraph and the §4.2 header at line 205).
- Paragraph cites `reports/specs/01_05_preregistration.md` §7 and §11
  explicitly (at least two spec-section references).
- Paragraph length 300–500 Polish chars with spaces (verify by
  `wc -m` on the draft).
- REVIEW_QUEUE has one new Pending row for §4.1.3.
- WRITING_STATUS §4.1.3 Notes cell extended with 2026-04-19 date line.
- Flag count for §4.1.3 row increments by 1 (existing 1 [REVIEW] → 2).

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (§4.1.3 tail only)
- `thesis/chapters/REVIEW_QUEUE.md`
- `thesis/WRITING_STATUS.md`

**Read scope:**
- `planning/CHAPTER_4_DEFEND_IN_THESIS.md` Residual #1
- `reports/specs/01_05_preregistration.md` §7 + §11

---

### T02 — §4.1.2.1 paragraph: aoestats 744-player cohort construction rationale

**Objective:** Add a paragraph to §4.1.2.1 (aoestats corpus subsection,
current lines 81–116) that names the 744-eligible-player ceiling, cites
the sensitivity table (4 325 / 744 / 3 at N=5 / N=10 / N=20), and
attributes the ceiling to the spec §11 W3 ARTEFACT_EDGE single-patch
constraint — **without** discussing ICC identification (that is
deferred to PR-2 §4.4.5). The paragraph slots **before Tabela 4.2**
(current line 101) so the reader has the 744 number in hand when
reading the CONSORT flow.

**Instructions:**
1. Read current §4.1.2.1 lines 81–116. Identify the insertion point:
   after the current "Dryf schematu (kolumny *in-game*)" paragraph
   (ends ~line 97) and before the "Asymetrie i ograniczenia" paragraph
   (starts ~line 99), OR after "Asymetrie i ograniczenia" and before
   Tabela 4.2 (line 101). Writer-thesis picks based on prose flow;
   recommendation: after "Asymetrie i ograniczenia" — that paragraph
   ends with a sentence about aoestats scope (1v1 ranked random_map
   96.62% coverage); the new paragraph extends "ograniczenia" with
   the cohort-ceiling dimension.
2. Draft a Polish paragraph (500–700 chars with spaces; widened from
   400–600 per M1 resolution) that makes **four** moves:
   - (a) State the fact: przy progu kohorty N=10 (spec §6.3 default),
     w referencyjnym oknie patch 66692 (spec §7, §11 W3
     ARTEFACT_EDGE) kwalifikowalnych jest **744 graczy** z 7 909
     obserwacji. Cite via JSONPath:
     `01_05_05_icc_results.json → icc_by_cohort_threshold.n_min10.n_players`
     (per m2 — avoid fragile line-number anchors).
   - (b) Cite the sensitivity table: N=5 daje 4 325 graczy (30 975
     obs.), N=20 daje 3 graczy (77 obs.) — PR #171 cohort-axis
     sensitivity (post-v1.0.4 spec amendment) potwierdza hard
     ceiling. Cite via JSONPath:
     `01_05_05_icc_results.json → icc_by_cohort_threshold.{n_min5,n_min10,n_min20}`.
   - (c) Attribute the ceiling to the single-patch constraint, NOT to
     dataset size per se: relaxing patch 66692 would re-introduce
     patch heterogeneity (forbidden by spec §11) — the ceiling is
     the cost of within-reference homogeneity (forward-ref to §4.1.3
     tail paragraph added in T01).
   - (d) **(M1 fix — pre-empt isolated-reading examiner attack)** Add
     one defensive sentence: `Przy tej wielkości kohorty estymata
     punktowa ICC typu ANOVA pozostaje identyfikowalna (szerzej
     omawiane w §4.4.5 w kolejnej aktualizacji rozdziału);
     ograniczenie 744 graczy rozszerza przedział ufności, nie obciąża
     punktu estymaty.` Do NOT cite [Gelman2007] here (reserved for
     §4.4.5); hedge via the forward-ref. This closes the §4.1.2.1
     isolated-reading vulnerability documented in
     `planning/current_plan.critique.md` M1.
3. Plant TWO flags at specified positions (per M2 resolution —
   forward-ref flag is **mandatory**, not optional):
   - `[REVIEW: Pass-2 — 744-player construction rationale;
     verify Polish idiom for "within-reference homogeneity"]`
     at the end of the (c) sentence.
   - `[REVIEW: forward-ref — §4.4.5 tworzone w PR-2 sekwencji
     DEFEND-IN-THESIS]` at the end of the (d) sentence.
4. Update `thesis/chapters/REVIEW_QUEUE.md` §4.1.2 row: extend the
   Notes cell with a `**2026-04-19:** defense paragraph added for
   aoestats 744-player cohort ceiling (Residual #4 of
   CHAPTER_4_DEFEND_IN_THESIS); mandatory forward-ref flag to §4.4.5
   planted per M2 resolution` note; increment flag count by 2
   (existing 4 [REVIEW] → 6).
5. Update `thesis/WRITING_STATUS.md` §4.1.2 row: keep status
   `DRAFTED`, extend the Notes cell with a `**2026-04-19:** cohort
   ceiling paragraph added (Residual #4)` note.

**Verification:**
- The new paragraph precedes Tabela 4.2 (current line 101 on master;
  line number will shift after insertion).
- Paragraph cites `01_05_05_icc_results.json` via JSONPath
  (`icc_by_cohort_threshold.n_min10.n_players` etc.) — NOT line
  numbers (per m2 fragility concern).
- Paragraph cites spec §11 W3 ARTEFACT_EDGE explicitly.
- Paragraph contains an explicit hedged forward-ref to §4.4.5
  using `w kolejnej aktualizacji rozdziału` wording (not bare
  `patrz §4.4.5`) — plant the MANDATORY
  `[REVIEW: forward-ref — §4.4.5 tworzone w PR-2]` flag.
- Paragraph contains the M1-fix defensive sentence ("estymata
  punktowa ICC … pozostaje identyfikowalna … rozszerza przedział
  ufności, nie obciąża punktu estymaty").
- Paragraph length 500–700 Polish chars with spaces (widened per
  M1 defensive-sentence addition).
- Flag count in paragraph = 2 (primary [REVIEW] + forward-ref
  [REVIEW]).
- REVIEW_QUEUE §4.1.2 Notes cell extended; flag count incremented
  by 2 (existing 4 [REVIEW] → 6).
- WRITING_STATUS §4.1.2 Notes cell extended.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (§4.1.2.1 only)
- `thesis/chapters/REVIEW_QUEUE.md`
- `thesis/WRITING_STATUS.md`

**Read scope:**
- `planning/CHAPTER_4_DEFEND_IN_THESIS.md` Residual #4
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_05_icc_results.json`
- `reports/specs/01_05_preregistration.md` §11 W3 ARTEFACT_EDGE

---

### T03 — NEW §4.1.4: `[POP:]` population-scope framing

**Objective:** Create a new subsection `#### 4.1.4 Zakres populacji —
ramy porównawcze dataset-conditional` at the end of §4.1 (between
current §4.1.3 end at line 203 and §4.2 header at line 205). The
subsection states once that ALL cross-dataset claims in Chapter 4 are
dataset-conditional, `[POP:]` scopes every finding, and cross-dataset
comparisons are framed as "do the same analytic patterns appear across
differently-sampled populations?" per invariant #8. Every subsequent
per-dataset interpretation paragraph in §4.4 (PR-2) will
cross-reference back to this subsection.

**Instructions:**
1. Read the current §4.1.3 closing paragraph (ends at line 203) and
   the §4.2 header (line 205). Verify the insertion point is clean
   (one blank line between §4.1.3 end and §4.2 start).
2. Draft a new subsection `### 4.1.4 Zakres populacji — ramy
   porównawcze dataset-conditional` as a sibling of §4.1.3 (both
   use `###` per verified chapter convention; `####` is reserved
   for `4.1.X.Y` subsubsections only). B2 resolution per
   reviewer-adversarial round 1: the `####` language that appeared
   in an earlier revision of this plan has been struck. **Do NOT
   replicate** the pre-existing line-157 bug (`#### 4.1.2
   Podsumowanie`) — that mis-use of `####` for a §4.1.2.3 element
   is a known defect flagged for a separate chore, not a template.
3. The subsection contains 2–3 Polish paragraphs (~1 000–1 500 chars
   with spaces total) making four moves:
   - (a) State what the thesis does NOT claim: uniwersalnych twierdzeń
     o "graczach AoE2" lub "graczach SC2". Population-scope of each
     corpus is distinct: sc2egset = `[POP:tournament]` (kuratorowany
     korpus turniejowy), aoe2companion = `[POP:ranked_ladder]`
     (szeroki zakres umiejętności na ladderze), aoestats =
     `[POP:ranked_ladder]` (również ladder, lecz z innym crawlerem
     upstream z inną asymetrią próbkowania).
   - (b) **(B1 fix — align claim to artifact state)** State what the
     thesis DOES claim, **honestly matched to the artifact**:
     sc2egset Phase 06 CSV (`phase06_interface_sc2egset.csv`,
     35/35 wierszy) i aoe2companion Phase 06 CSV
     (`01_05_phase06_interface_aoe2companion.csv`, 74/74 wierszy)
     niosą jawny prefix `[POP:]` w kolumnie `notes` każdego wiersza
     (odpowiednio `[POP:tournament]` i `[POP:ranked_ladder]`).
     aoestats Phase 06 CSV (`phase06_interface_aoestats.csv`,
     137 wierszy) **NIE niesie** jawnego tagu `[POP:]` —
     population-scope aoestats (`[POP:ranked_ladder]`) wynika
     **implicit** z preregistration spec §0 scope
     (`leaderboard = 'random_map'` → `is_1v1_ranked` per spec §1).
     Rozdźwięk artefakt-spec jest udokumentowaną znaną niespójnością
     (dodawaną do `planning/BACKLOG.md` jako Category-D chore
     `[POP:] tag backfill into aoestats Phase 06 CSV` w Out-of-scope
     tego planu) — thesis zapisuje **rzeczywisty** stan artefaktów,
     nie deklaratywny. Claims pozostają **dataset-conditional** we
     wszystkich trzech korpusach (dwa przez jawny tag, jeden przez
     scope spec'owy).
   - (c) Framing cross-dataset: porównania między korpusami są
     operacjonalizowane jako pytanie "czy te same analityczne wzorce
     pojawiają się w różnie próbkowanych populacjach?" (*do the same
     patterns appear across differently-sampled populations?*) — nie
     jako "czy populacje zgadzają się co do swojego agregatu?"
     Population-scope is a **controlled experimental variable**, nie
     confound — zgodnie z niezmiennikiem #8 w
     `.claude/scientific-invariants.md` (comparative methodology).
   - (d) Forward-ref: pełna methodologia porównań cross-dataset —
     w szczególności ograniczenie N=2 dla statystycznych testów
     Friedman / Wilcoxon-Holm — omawiana jest w §4.4.4 (Evaluation
     metrics) i §4.4.6 (`[PRE-canonical_slot]` flag), tworzonych
     odpowiednio w PR-2 i PR-3 sekwencji DEFEND-IN-THESIS. Methodology
     defense tej sekcji jest zatem forward-referenced — §4.1.4
     *scopes* claims, §4.4 *defends* methodology.
4. Plant `[REVIEW: Pass-2 — [POP:] framing dataset-conditional
   honestly-matched to artifact state; verify Polish idiom dla
   "dataset-conditional", "controlled experimental variable",
   oraz "implicit scope z spec §0"]` flag at the end of the
   subsection (per B1 fix — flag must reference artifact-vs-spec
   divergence for aoestats so Pass-2 reviewer audits the
   honest-matching argument).
5. Plant **mandatory** `[REVIEW: forward-ref — §4.4.4 DRAFTABLE
   na master; §4.4.5 i §4.4.6 tworzone odpowiednio w PR-2 i PR-3
   sekwencji DEFEND-IN-THESIS; forward-reference intended to
   resolve w kolejnej aktualizacji rozdziału]` flag at the
   forward-ref paragraph (per M2 fix — hedged Polish wording
   "w kolejnej aktualizacji rozdziału" rather than bare
   `patrz §4.4.X`).
6. Update `thesis/chapters/REVIEW_QUEUE.md` with a new Pending entry
   for §4.1.4. Format per existing entries. Key artifacts:
   `planning/CHAPTER_4_DEFEND_IN_THESIS.md` Residual #2,
   `.claude/scientific-invariants.md` #8, sample Phase 06 CSV
   (cite notes column).
7. Update `thesis/WRITING_STATUS.md`: add a new row for §4.1.4
   between the §4.1.3 row and the §4.2.1 row. Status `DRAFTED`,
   Feeds from: Phase 01 (cross-corpus synthesis), Notes: `Drafted
   2026-04-19 via Residual #2 of CHAPTER_4_DEFEND_IN_THESIS. ~1.2k
   znaków polskich. 2 [REVIEW] flags. Scopes all cross-dataset
   claims in §4.4 as dataset-conditional per invariant #8.`
8. **(B1 provenance — add Category-D BACKLOG entry)** Append to
   `planning/BACKLOG.md` a new `F6` entry (assigned at execution time;
   F4 and F5 were already taken — writer-thesis verified and used F6)
   titled `aoestats Phase 06 CSV — [POP:] and [PRE-canonical_slot]
   tag backfill` with: Category D, Predecessors `PR-1 of
   DEFEND-IN-THESIS sequence (documents the artifact-vs-spec
   divergence in §4.1.4)`, Scope `Populate notes column of
   phase06_interface_aoestats.csv with [POP:ranked_ladder] on all
   137 rows and [PRE-canonical_slot] on rows conditioned on team
   per spec §1 line 71`, Why priority `Unblocks a future spec-level
   closure of the artifact-vs-spec divergence that §4.1.4 and §4.4.6
   (PR-3) currently describe as "implicit scope". Also pre-empts
   PR-3 hitting the same BLOCKER for [PRE-canonical_slot] per
   reviewer-adversarial round 1 critique B1 secondary finding`.
   This provenance serves as the audit trail for §4.1.4's honest
   description of the artifact state and prevents the PR-3
   blocker from arriving unannounced.

**Verification:**
- New subsection `### 4.1.4 ...` inserted between current §4.1.3 end
  and §4.2 start.
- Subsection cites `.claude/scientific-invariants.md` #8 explicitly.
- Subsection references three Phase 06 CSV files (one per dataset).
- Subsection contains 2 flags (`[REVIEW]` + `[REVIEW: forward-ref]`).
- Total length 1 000–1 500 Polish chars with spaces.
- REVIEW_QUEUE has new Pending row for §4.1.4.
- WRITING_STATUS has new §4.1.4 row, status `DRAFTED`.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (new §4.1.4)
- `thesis/chapters/REVIEW_QUEUE.md`
- `thesis/WRITING_STATUS.md`
- `planning/BACKLOG.md` (append Category-D entry per step 8)

**Read scope:**
- `planning/CHAPTER_4_DEFEND_IN_THESIS.md` Residual #2
- `.claude/scientific-invariants.md` invariant #8
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_sc2egset.csv` (header + one sample notes cell)
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/05_temporal_panel_eda/01_05_phase06_interface_aoe2companion.csv` (header + one sample notes cell)
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv` (header + one sample notes cell)
- `reports/specs/01_05_preregistration.md` §0 (aoestats scope) and §1 (`[PRE-canonical_slot]` tag definition, line 71)

---

### T04 — Wrap-up commit 1 of 2: CHANGELOG TBD backfill (chore, m1 resolution)

**Objective:** Backfill two pre-existing `PR #TBD` cosmetic references
in CHANGELOG (PR #172 for `[3.23.0]`, PR #174 for `[3.23.1]`) as a
**separate atomic commit** before the version bump. Per m1 reviewer
finding, cosmetic backfills are orthogonal to the Cat F thesis changes
and get their own commit per `.claude/rules/git-workflow.md` atomic-unit
convention.

**Instructions:**
1. Edit `CHANGELOG.md`:
   - Backfill `[3.23.0] — 2026-04-19 (PR #TBD: fix/01-05-phase06-schema-harmonization)`
     → `(PR #172: fix/01-05-phase06-schema-harmonization)`.
   - Backfill `[3.23.1] — 2026-04-19 (PR #TBD: chore/purge-planning-pr-173)`
     → `(PR #174: chore/purge-planning-pr-173)`.
2. Commit with message
   `chore(changelog): backfill PR #172 and PR #174 numbers`
   (writing to `.github/tmp/commit.txt` per memory
   `feedback_git_commit_format.md`).

**Verification:**
- `[3.23.0]` header reads `(PR #172: fix/01-05-phase06-schema-harmonization)`.
- `[3.23.1]` header reads `(PR #174: chore/purge-planning-pr-173)`.
- Commit is atomic (only CHANGELOG.md changed).

**File scope:**
- `CHANGELOG.md`

**Read scope:**
- (none — self-contained admin step)

---

### T05 — Wrap-up commit 2 of 2: version bump + CHANGELOG [3.24.0] entry

**Objective:** Bump `pyproject.toml` to 3.24.0 (minor per docs-category
convention) and add the `[3.24.0]` CHANGELOG entry describing this PR's
three residuals. Separate commit from T04 per m1.

**Instructions:**
1. Edit `pyproject.toml` line 3: `version = "3.23.1"` → `version = "3.24.0"`.
2. Edit `CHANGELOG.md`:
   - Insert `[3.24.0] — 2026-04-19 (PR #TBD: docs/thesis-ch4-corpus-framing-residuals)`
     block between `[Unreleased]` and `[3.23.1]`.
   - Under `[3.24.0]` `### Changed`, add bullet summarizing: "Chapter 4
     §4.1.3 tail paragraph added (Residual #1 of CHAPTER_4_DEFEND_IN_THESIS
     — reference-window asymmetry defense); §4.1.2.1 paragraph added
     (Residual #4 — aoestats 744-player cohort ceiling); new §4.1.4
     subsection added (Residual #2 — `[POP:]` population-scope framing,
     dataset-conditional claim scoping per invariant #8)."
3. The `[3.24.0]` `PR #TBD` stays as TBD in this commit — it will be
   backfilled to `PR #175` (or whatever number GitHub assigns this PR)
   in the next chore commit after merge, matching the
   `[3.23.1]` pattern.
4. Commit with message `chore(release): bump version to 3.24.0`.

**Verification:**
- `pyproject.toml` line 3 shows `version = "3.24.0"`.
- CHANGELOG has four sections in order: `[Unreleased]`, `[3.24.0]`,
  `[3.23.1]`, `[3.23.0]`.
- `[3.24.0]` header reads `(PR #TBD: docs/thesis-ch4-corpus-framing-residuals)`.
- Commit is atomic (only CHANGELOG.md + pyproject.toml changed).

**File scope:**
- `pyproject.toml`
- `CHANGELOG.md`

**Read scope:**
- (none — self-contained admin step)

---

## File Manifest

| File | Action |
|------|--------|
| `thesis/chapters/04_data_and_methodology.md` | Update (§4.1.2.1 + §4.1.3 + new §4.1.4) |
| `thesis/chapters/REVIEW_QUEUE.md` | Update (2 new Pending rows + 1 extended Notes) |
| `thesis/WRITING_STATUS.md` | Update (extend §4.1.2 and §4.1.3 Notes; add new §4.1.4 row) |
| `planning/BACKLOG.md` | Update (append Category-D entry `F4` per T03 step 8) |
| `pyproject.toml` | Update (version bump 3.23.1 → 3.24.0 via T05) |
| `CHANGELOG.md` | Update — T04 commit 1: PR #172/#174 TBD backfills (chore); T05 commit 2: new `[3.24.0]` entry |
| `planning/current_plan.md` | Update (this file — commit as provenance) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial round 1 output — already written before execution) |

## Gate Condition

- All three residuals' paragraphs are present in
  `thesis/chapters/04_data_and_methodology.md` at the specified slots.
- Polish character count total across the three insertions: ~2 100 –
  2 800 (T01 ~400 + T02 ~600 (widened per M1) + T03 ~1 200).
- `[REVIEW: ...]` flag count across PR-1 insertions: 3–7 (widened from
  3–5 per m3 to accommodate the mandatory T02 forward-ref flag from M2
  fix: T01 = 1, T02 = 2, T03 = 2 → total 5 expected; ceiling of 7
  allows writer-thesis headroom for Polish-idiom flags).
- `thesis/chapters/REVIEW_QUEUE.md` has 2 new Pending rows (for §4.1.3
  defense paragraph and §4.1.4 new subsection) + 1 extended Notes cell
  (for §4.1.2).
- `thesis/WRITING_STATUS.md` has 1 new row (§4.1.4 `DRAFTED`) + 2
  extended Notes cells (§4.1.2 and §4.1.3).
- `pyproject.toml` shows `version = "3.24.0"`.
- `CHANGELOG.md` has a `[3.24.0]` entry with three bullets covering the
  three residuals; `[3.23.0]` and `[3.23.1]` headers show `PR #172`
  and `PR #174` instead of `PR #TBD`.
- `planning/current_plan.critique.md` exists and has been read by the
  user before execution begins (Cat F requirement).
- Pre-commit hooks (ruff, mypy, planning artifact validation,
  jupytext) all pass. No notebook or code changes in this PR — only
  thesis/ and meta files — so most hooks skip.
- New PR opened on branch `docs/thesis-ch4-corpus-framing-residuals`.

## Out of scope

- **Residual #3 (observed- vs latent-scale ICC).** Deferred to PR-2.
  Reason: lives in §4.4.5 (methodology), not in §4.1.
- **Residual #5 (`[PRE-canonical_slot]` flag).** Deferred to PR-3.
  Reason: flag definition lives in new §4.4.6 (methodology) + footnote
  at §4.1.2.1 (which PR-3 adds). PR-1 does NOT add any
  `[PRE-canonical_slot]` footnote — that is PR-3's job.
- **Residual #6 (N=2 cross-game test limit).** Deferred to PR-2.
  Reason: lives in §4.4.4 (evaluation metrics methodology), not in §4.1.
- **Tabela 4.7 (ICC headline reconciliation across three datasets).**
  Created in PR-2 §4.4.5. PR-1's T02 paragraph may forward-ref
  §4.4.5 but does NOT create the table.
- **Chapter 5 (Experiments and Results) pre-staging.** The 0.0268
  ANOVA ICC point estimate is a Chapter-4 methodology preview in
  PR-2's Tabela 4.7, not a Chapter-5 result. PR-1 does not touch
  Chapter 5.
- **Gelman2007 §11-12 citation for ICC identification.** Belongs in
  §4.4.5 (PR-2), not in §4.1.2.1. PR-1 forward-refs §4.4.5 but does
  NOT cite Gelman2007 directly.
- **Bibtex additions.** PR-1 adds zero new bibtex entries. All
  citations use existing bibkeys (Demsar2006, Rubin1976, vanBuuren2018,
  SchaferGraham2002, Bialecki2023, AoEStats, AoeCompanion) or file-path
  references (spec, invariants).
- **Polish Pass-2 corrections.** Pass-2 (Claude Chat external
  validation) runs after merge, separately. PR-1 produces Pass-1
  draft + `[REVIEW]` flags; Pass-2 resolves flags in a later session.
- **(B1 resolution — deferred)** aoestats Phase 06 CSV `[POP:]` and
  `[PRE-canonical_slot]` tag backfill. This is a Category-D fix to
  align the artifact with spec §0 scope and spec §1 line 71 tag
  definition (see T03 step 8 BACKLOG entry). PR-1 describes the
  **honest current state** of the artifact (spec implicit, not
  tagged); the Category-D chore that closes the artifact-vs-spec
  divergence is scheduled separately via `planning/BACKLOG.md F4`.
  Once F4 lands, §4.1.4's prose will be trivially revisable to
  drop the "implicit" language.
- **(B2 resolution — deferred)** Pre-existing line-157 heading bug
  (`#### 4.1.2 Podsumowanie i forward-reference do §4.1.3`) — a
  misuse of `####` for a §4.1.2.3 element. Fix belongs in a
  separate Category-E chore, not this PR. Flagged here so a future
  session can claim it.
- **Skeleton §4.4.4/§4.4.5/§4.4.6 headers (M2 fix option 3).** The
  reviewer suggested stubbing these headers in PR-1 so interim-state
  forward-refs resolve to stubs. Declined: adding §4.4 touches to
  a §4.1-focused PR violates the file-scope discipline that motivates
  the 3-PR split in the first place. Hedged Polish language + mandatory
  `[REVIEW]` flag (M2 options 1 + 2) is the adopted mitigation.

## Open questions

- **Q1:** Should §4.1.4 use header level `###` (sibling to §4.1.3) or
  `####` (child of §4.1.3)? Resolves by: writer-thesis reading
  existing §4.1.1, §4.1.2, §4.1.3 headers at master. The current
  chapter uses `###` for §4.1.X — so §4.1.4 uses `###`. (Resolved at
  plan time by reading the existing chapter.)
- **Q2:** Does residual #2's `[POP:]` framing paragraph belong in §4.1
  (corpus description) or §4.4 (methodology)? Resolves by: R2
  (planner-science decision 2026-04-19). Placed in §4.1.4 because
  (a) it *scopes* claims — naturally belongs at the end of the
  corpus-description section before methodology begins; (b) §4.4
  methodology sections can forward-reference §4.1.4 as the scoping
  anchor. Resolved in this plan.
- **Q3:** Should T02's §4.1.2.1 paragraph include the specific
  interpretation "ICC point estimate is well-identified at n=744 per
  Gelman & Hill 2007"? Resolves by: planner-science
  split-of-concerns (R4). Identification belongs in §4.4.5 (PR-2);
  construction belongs in §4.1.2.1 (this PR). Resolved in this plan.
- **Q4:** Should PR-1 run reviewer-adversarial on each T-task
  individually or on the full diff at end? Resolves by: user
  directive 2026-04-19 — "run adversarial reviews after each step".
  Interpretation: reviewer-adversarial runs once on the plan
  (before T01 execution begins, producing
  `planning/current_plan.critique.md` — **round 1 already completed
  2026-04-19, verdict REVISE, fixes applied inline via this plan
  revision**) AND once on the execution diff (after T05 completes,
  before PR creation). This is the symmetric 3-round adversarial
  cap per memory `feedback_adversarial_cap_execution.md`. Running
  adversarial
  review between each T-task within one PR would over-burn the
  reviewer cap and conflict with CLAUDE.md Cat F workflow.
  Resolved: two adversarial passes per PR (plan-side + execution-side).
- **Q5:** Do T01/T02/T03 need to be executed sequentially (with
  writer-thesis re-reading the chapter between tasks) or can one
  writer-thesis invocation handle all three? Resolves by:
  writer-thesis agent contract. One invocation can handle multiple
  residuals in the same chapter; writer-thesis reads the chapter
  once, drafts three insertions, and updates trackers. Resolved:
  one writer-thesis invocation executes T01+T02+T03 together; T04
  (CHANGELOG TBD backfill) and T05 (version bump) are admin-only
  and inlined by the parent session (no writer-thesis invocation
  needed).
- **Q6 (added post-round-1-critique):** Does the BACKLOG F4 entry
  added in T03 step 8 overlap with the Residual #5 BACKLOG F1
  entry scheduled for PR-3? Resolves by: inspection of
  `planning/BACKLOG.md` F1 scope at current master. F1 is
  scoped to `canonical_slot` COLUMN derivation (Phase 02
  unblocker); F4 would be scoped to `notes`-column TAG backfill
  (Phase 01 artifact alignment). Distinct chores. Resolved:
  F4 is a new entry, not a merge with F1.
