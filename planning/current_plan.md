---
category: F
branch: docs/thesis-pass2-tg1-methodological-drift
date: 2026-04-20
planner_model: claude-opus-4-7
dataset: null
phase: null
pipeline_section: null
invariants_touched: []
source_artifacts:
  - thesis/chapters/01_introduction.md
  - thesis/chapters/02_theoretical_background.md
  - thesis/chapters/04_data_and_methodology.md
  - thesis/THESIS_STRUCTURE.md
  - thesis/WRITING_STATUS.md
  - thesis/chapters/REVIEW_QUEUE.md
  - thesis/references.bib
  - .claude/author-style-brief-pl.md
  - .claude/scientific-invariants.md
  - .claude/rules/thesis-writing.md
  - thesis/plans/writing_protocol.md
critique_required: true
research_log_ref: null
---

# Plan: Pass-2 TG1 — Un-commit Dimitriadis triptych + deferred within-game statistical protocol across §1.2, §2.6, §4.4.4

## Scope

This plan executes Task Group 1 of the Pass-2 dispatch. It corrects a three-way methodological commitment drift across three chapters that (i) treats the Dimitriadis, Gneiting, Jordan and Vogel (2024) triptych inconsistently — cautiously hedged in §1.2 paragraph 1, but fully adopted ("pełny tryptyk diagnostyczny") in §2.6.2 / §2.6.5 and forward-referenced as planned practice — and (ii) hard-commits §4.4.4 to Friedman omnibus + Wilcoxon-Holm + Bayesian signed-rank as the within-game statistical comparison protocol, in violation of the explicit user instruction that the statistical comparison method is deferred until after experiment design is finalized. The plan produces one PR (PR-1) and defers TG2–TG6 to sequential follow-up plans per the dispatch's halt-and-review protocol. No empirical artifacts are touched; the work is prose-only across three chapter files plus two tracker files (WRITING_STATUS.md, REVIEW_QUEUE.md).

## Problem Statement

The three subsections currently carry inconsistent commitment strength for two load-bearing methodological choices.

**Current state — Dimitriadis triptych.** §1.2 paragraph 1 (`01_introduction.md` line 19) closes with the hedge: *"Tryptyk ten stanowi potencjalną ramę ewaluacyjną dla porównania metod predykcyjnych; jego zastosowanie w niniejszej pracy zostanie rozważone w rozdziale poświęconym metodyce ewaluacji."* — correctly positioning the triptych as a candidate framework whose adoption is deferred. In contrast, §2.6.2 (`02_theoretical_background.md` line 203) states: *"Dimitriadis, Gneiting, Jordan i Vogel [Dimitriadis2024], cytowani w §1.2 niniejszej pracy, proponują systematyczny tryptyk diagnostyczny obejmujący diagram rzetelności, krzywą ROC i diagram Murphy'ego — łącznie dostarczający pełnej charakterystyki probabilistycznej klasyfikatora. Jego zastosowanie w niniejszej pracy jest planowane jako rama ewaluacji jakościowej najlepszych modeli z każdej rodziny"* — a planned adoption, not a candidate. §2.6.5 (line 231) makes the adoption categorical: *"Poziom pojedynczego modelu — pełny tryptyk diagnostyczny [Dimitriadis2024]…"*. §4.4.4 (`04_data_and_methodology.md` line 367) drops the triptych entirely and replaces it with ECE + reliability diagrams + AUC + accuracy as the operational protocol, without any cross-reference to §2.6.5's adoption claim. The three sections point at three mutually inconsistent commitments.

**Current state — within-game statistical protocol.** §2.6.3 (line 215) presents Wilcoxon-Holm as *"Aktualnie rekomendowanym protokołem"* and §2.6.5 (line 231) catalogues it alongside Friedman and Bayesian signed-rank with ROPE=±0,01 as the committed within-game protocol. §4.4.4 (line 371) concretises this as a hard commitment: *"W ramach jednej gry — przy N_folds ≥ 5 — porównanie modeli prowadzone jest w trybie omnibusa Friedmana [Friedman1937] z testami post-hoc Wilcoxon-Holm [Holm1979, Wilcoxon1945] oraz bayesowskim signed-rank via baycomp [Benavoli2017]."* This language — *"prowadzone jest"* — has no hedge and no deferral; it commits. The user's Pass-2 dispatch explicitly flags this as a violation: the statistical comparison choice is deferred to post-experiment methodology finalization. Invariant #8 in `.claude/scientific-invariants.md` lines 197–213 names the same protocol but as a guidance reference, not as a locked contract; the user has confirmed (Open Q 4 resolution) that the invariants file remains aspirational-advisory while Chapter 4 is being drafted.

**Criterion for invariant #7 binding vs. invariant #8 advisory.** These two invariants have different binding status because they operate at different epistemic levels. Invariant #7 governs a concrete data-analysis action already present in the prose: citing a magic number (ROPE=±0,01) as though it were an established constant. The existing §2.6.3 line 217 text offers "w literaturze klasyfikacji typowy zakres dla trafności wynosi ±0,01" as grounding — this is an uncited qualitative assertion with no named paper or equation reference, which fails invariant #7's requirement for a specific cited precedent. Invariant #8, by contrast, names a prospective experimental protocol the thesis has not yet run; its advisory status reflects this forward-looking, pre-experiment nature. The two invariants are not symmetrically downgrade-able: #7 applies to a currently-written number; #8 applies to a future protocol. Removing the fixed ROPE value restores #7 compliance; keeping invariant #8 as advisory is correct at this phase.

**Target end-state.** Per Open Q 2 resolution (option **b**), ECE + reliability diagrams + Murphy decomposition are the operational aggregate-level diagnostic in both §2.6.2 and §4.4.4; the Dimitriadis triptych is named as a candidate alternative to that operational set in both sections (pending Phase 04 methodology finalization). §2.6.2 must explicitly designate ECE + reliability diagrams + Murphy decomposition as the operational aggregate-level diagnostic, so that §4.4.4's "operational" framing is consistent, not contradictory, with §2.6.2's framing. All three sections present the within-game statistical comparison protocol as a candidate space — enumerating alternative candidate protocols (e.g., Friedman + Wilcoxon-Holm + Bayesian signed-rank as one candidate per `[Demsar2006]`, `[Benavoli2016]`, `[Benavoli2017]`, `[GarciaHerrera2008]`; pure Bayesian via baycomp per `[Benavoli2017]` as another; 5×2 cv F-test / Nadeau-Bengio per `[Dietterich1998]`, `[Nadeau2003]` as another) — explicitly uncommitted. ROPE width is not fixed (currently §2.6.3 fixes it at ±0,01 without justification, which additionally violates invariant #7; see Problem Statement for the #7-binds/#8-advises criterion). The three sections must be mutually consistent per a final post-rewrite grep sweep. Forward references from §4.4.4 to §2.6 must point at the hedged framing, not a commitment.

## Assumptions & unknowns

- **Assumption:** §1.2 paragraph 1 still contains the *"zostanie rozważone"* hedge verbatim. Verified 2026-04-20 via Read of `thesis/chapters/01_introduction.md:19`.
- **Assumption:** §2.6.2 and §2.6.5 still use *"tryptyk diagnostyczny"* with adoption language. Verified — §2.6.2 line 203, §2.6.5 line 231.
- **Assumption:** §2.6.3 still presents Wilcoxon-Holm as *"aktualnie rekomendowany protokół"* and fixes ROPE=±0,01. Verified — line 215, line 217.
- **Assumption:** §4.4.4 currently hard-commits to Friedman + Wilcoxon-Holm + Bayesian signed-rank. Verified — line 371.
- **Assumption:** No TG1 finding touches §4.2. Verified via grep of `Dimitriadis|tryptyk|Nemenyi|Wilcoxon|Friedman|signed-rank|Bayesian|ROPE` on `04_data_and_methodology.md` — only hits are at line 213 (§4.1.4 Zakres populacji — mentions Friedman + Wilcoxon-Holm as inapplicable at N=2; negative-framing is consistent with target deferred-candidate end-state; no rewrite required, but T03 executor must confirm §4.1.4 line 213 remains coherent after §4.4.4 rewrite) and line 371 (§4.4.4).
- **Assumption:** No material edit to §4.4.5 or §4.4.6 is needed. Scope boundary: only §4.4.4 in Chapter 4 is touched.
- **Unknown — resolved by writer-thesis during T02 execution:** is the N ≥ 5 recommendation in Demšar 2006 at §3.1.3 as F5.6 claims? If confirmed via WebFetch, apply the citation fix; if the PDF places the guidance elsewhere, plant `[REVIEW: Demsar section verification]` instead of speculating.
- **Unknown — resolved by reviewer-adversarial Mode A (Step 2):** does the proposed target end-state ("triptych as one candidate among several alongside ECE + reliability diagrams + Murphy decomposition") genuinely un-commit, or does it introduce a new commitment at a lower abstraction (the competing alternatives being named)?

## Literature context

This plan's rewrites do not introduce new bibkeys — all cited references already exist in `thesis/references.bib` and are in active use in the current §2.6 / §4.4.4 drafts. The following keys are load-bearing for the TG1 target framing:

- **[Demsar2006]** — Statistical comparisons of classifiers (JMLR). §3.1.3 establishes the Friedman N ≥ 5 block requirement (F5.6 fix). §3.2 establishes the Friedman omnibus procedure. Must cite as canonical reference for the within-game protocol candidate, not as adopted authority. Note: §3.1 and §3.2 provide two distinct thresholds operating on different dimensions (N_folds blocks vs. N_datasets); T02 and T03 should not conflate them — the produced prose should distinguish "≥5 folds for within-game Friedman" (§3.1.3) from "≥10 datasets for cross-game Friedman" (§3.2).
- **[Benavoli2016]** — Should we really use post-hoc tests based on mean-ranks? Must cite to motivate *why* Wilcoxon-Holm is a candidate alternative to Nemenyi, not to commit to Wilcoxon-Holm itself.
- **[Benavoli2017]** — Time for a change (Bayesian classifier comparison tutorial). Must cite as candidate protocol; ROPE width must not be fixed.
- **[GarciaHerrera2008]** / **[Garcia2010]** — sequential Wilcoxon-Holm analyses. Must cite to frame Wilcoxon-Holm as one candidate.
- **[Dimitriadis2024]** — the triptych. Must cite as candidate diagnostic framework. Must not use "pełny tryptyk" / "adopted" language.
- **[Gneiting2007]** — Strictly Proper Scoring Rules. Must cite to ground the Brier + log-loss primary-metric decision — defensible *without* committing to the full triptych or to any specific statistical comparison protocol.
- **[Dietterich1998]** / **[Bouckaert2003]** / **[Nadeau2003]** — 5×2 cv F-test and corrected t-test. Must cite as candidates for cross-game protocol, complementing the within-game candidate set.
- **[Friedman1937]** / **[Wilcoxon1945]** / **[Holm1979]** — primary references for the named tests. Must cite when naming the tests but not as the committed protocol.

Invariant #8 in `.claude/scientific-invariants.md` lines 197–213 names the within-game protocol (Friedman + Wilcoxon-Holm + Bayesian signed-rank via baycomp) and the cross-game protocol (per-game rankings + 5×2 cv F-test or Nadeau-Bengio + qualitative concordance). Per Open Q 4 resolution, this invariant remains ADVISORY at the current phase; the thesis prose's job is to reflect the actual commitment state, which at this phase is deferred. `[OPINION]` — the invariants file remains the correct place for the aspirational protocol definition; the thesis prose reflects the actual deferred commitment state.

## Execution Steps

Each task uses the `writer-thesis` agent as executor (per `thesis/plans/writing_protocol.md` §6.4). Tasks are NOT parallel-safe — §4.4.4 forward-refs §2.6 and §1.2, so the three must be drafted in order to preserve cross-reference consistency.

### T01 — §1.2 paragraph 1 revision (introduction chapter)

**Objective:** Tighten §1.2 paragraph 1 so that the Dimitriadis triptych is framed explicitly as one candidate diagnostic framework among several, not as the sole or leading candidate. The current *"zostanie rozważone"* hedge is directionally correct but too generic — it must explicitly name that aggregate-level diagnostics (ECE, reliability diagrams, Murphy decomposition) are competing candidates, to prevent the reader from treating the Dimitriadis triptych as the default.

**Instructions:**
1. Read `thesis/chapters/01_introduction.md` §1.2 paragraph 1 (line 19 in current state) in full.
2. Read `.claude/author-style-brief-pl.md` for voice constraints (argumentacja decyzyjna, hedging idiomatycznie polski, no first-person plural, no bullets).
3. Read `thesis/chapters/02_theoretical_background.md` §2.6.2 (line 195–205) and §2.6.3 (line 207–219) for cross-reference consistency — the §1.2 rewrite must be compatible with the T02 target language.
4. Rewrite the closing sentence of §1.2 paragraph 1 to achieve target end-state:
   - Must name ECE + reliability diagrams + Murphy decomposition as the **current operational aggregate-level diagnostic** (consistent with §2.6.2 Option B designation and §4.4.4 operational framing)
   - Must name the Dimitriadis triptych as **one candidate extension/alternative under consideration** relative to that operational diagnostic — NOT as a co-equal competing candidate or as the leading framework
   - Must defer the adoption decision to Chapter 4 methodology finalization
   - Must NOT fix a committed framework
   - **Must cite:** `[Dimitriadis2024]` (once), `[Gneiting2007]` (retain as proper-scoring-rules grounding)
   - **Must hedge:** no "zostanie wykorzystany / zastosowany / przyjęty" — use "zostanie rozważone", "stanowi jedną z rozpatrywanych ram", or equivalent
   - **Must cross-reference:** to §4.4.4 (methodology chapter, evaluation metrics); do NOT cross-reference to §2.6.2 at the §1.2 level
5. Preserve all other prose in §1.2 paragraphs 2–4 verbatim.
6. Do NOT introduce new bibkeys. Do NOT modify `thesis/references.bib`.
7. Update §1.2 status row in `thesis/WRITING_STATUS.md` with a dated Notes entry: *"2026-04-20 (PR-TG1): §1.2 ¶1 closing sentence revised to un-commit Dimitriadis triptych per Pass-2 TG1 dispatch; full §1.2 still DRAFTABLE (other paragraphs unchanged)."*
8. Add a Pending row in `thesis/chapters/REVIEW_QUEUE.md` for §1.2 ¶1 revision.
9. Produce writer-thesis Chat Handoff Summary per `.claude/rules/thesis-writing.md` literature-variant schema.

**Verification:**
- `grep -n "zostanie rozważone\|stanowi jedną z rozpatrywanych\|kandydack" thesis/chapters/01_introduction.md` returns at least one match in §1.2 ¶1 line range.
- `grep -cn "pełny tryptyk\|zostanie wykorzystan\|zostanie zastosowan\|zostanie przyjęt" thesis/chapters/01_introduction.md` returns 0 matches in §1.2 ¶1 line range.
- `grep -n "ECE\|reliability\|diagram rzetelnoś\|diagram Murphy" thesis/chapters/01_introduction.md` returns at least one match in §1.2 ¶1 line range.
- [sanity-check, not blocking] §1.2 ¶1 character count unchanged ± 500 characters.
- No net-additive substance: the T01 rewrite of §1.2 ¶1 substitutes commitment-strength framing only; does not introduce new diagnostics or protocols. Verified via writer-thesis Chat Handoff Summary enumeration.
- `thesis/WRITING_STATUS.md` Chapter 1 §1.2 row contains a 2026-04-20 PR-TG1 note.
- `thesis/chapters/REVIEW_QUEUE.md` contains a new Pending row for §1.2 ¶1 revision.

**File scope:**
- `thesis/chapters/01_introduction.md` (Update §1.2 ¶1 closing sentence)
- `thesis/WRITING_STATUS.md` (Update §1.2 row note)
- `thesis/chapters/REVIEW_QUEUE.md` (Add Pending row)

**Read scope:**
- `thesis/chapters/02_theoretical_background.md` §2.6.2, §2.6.3
- `.claude/author-style-brief-pl.md`
- `.claude/rules/thesis-writing.md`

---

### T02 — §2.6 revision (theoretical background chapter)

**Objective:** Rewrite §2.6.2, §2.6.3, and §2.6.5 so that the triptych is one candidate framework among several and the within-game statistical protocol (Friedman + Wilcoxon-Holm + Bayesian signed-rank + ROPE) is a candidate protocol, with adoption deferred to §4.4.4. Additionally correct F5.6 (Demsar §3.1.3 citation) while the subsection is being rewritten.

**Instructions:**
1. Read `thesis/chapters/02_theoretical_background.md` §2.6 in full (lines 185–232).
2. Read T01's output (the revised §1.2 ¶1 closing sentence) to ensure §2.6.2's cross-reference to §1.2 remains accurate.
3. Read `.claude/author-style-brief-pl.md`, `.claude/rules/thesis-writing.md` (literature variant).
4. Rewrite §2.6.2 final paragraph (line 203). Rewrite only the paragraph beginning at line 203 (the "Dimitriadis...jest planowane" paragraph). Preserve the paragraph at line 205 ("Należy podkreślić rzadkość...") verbatim — it does not name a commitment and requires no change. Target (per Open Q 2 option **b**): designate ECE + reliability diagrams + Murphy decomposition as the operational aggregate-level diagnostic, and frame the Dimitriadis triptych as a candidate alternative to that operational set — not as a co-equal candidate alongside it. Defer the triptych adoption decision to §4.4.4.
   - **Must cite:** `[Dimitriadis2024]` (retain, once)
   - **Must hedge on triptych:** no "pełny tryptyk", no "jest planowane", no "stanowi ramę ewaluacji". Use "stanowi jedną z rozpatrywanych ram diagnostycznych", "rozważane jest w niniejszej pracy jako kandydat obok…", or equivalent Polish idiomatic hedge.
   - **Must designate operational diagnostic:** ECE + reliability diagrams + Murphy decomposition must be explicitly named as the operational aggregate-level diagnostic, consistent with §4.4.4. Do not frame them as a mere candidate alongside the triptych.
5. Rewrite §2.6.3 paragraph starting at line 215 (*"Testy post-hoc — protokół Wilcoxon–Holm"*). Target: present Wilcoxon-Holm as one candidate post-hoc protocol motivated by the Nemenyi critique `[Benavoli2016]`, NOT as the protocol in use.
   - Replace *"Aktualnie rekomendowanym protokołem"* with deferred framing (e.g., *"Kandydatem post-hoc motywowanym krytyką Nemenyiego jest…"* or equivalent).
   - In the same §2.6.3 block at line 217 (Bayesian signed-rank): replace the hard commitment *"Niniejsza praca raportuje oba testy — Wilcoxon–Holm jako podstawową procedurę frequentystyczną oraz bayesowski test rang znaków z ROPE = ±0,01…"* with candidate framing. Do NOT fix ROPE width. Hedge ROPE width by saying it will be justified at methodology finalization, not fixed here.
   - **Must defer α:** The α value for Holm sequential rejection must NOT be fixed in §2.6.3 prose (analogous to ROPE deferral, invariant #7). The Holm schedule mechanics (*progami α/(k − i + 1)*) may be stated, but α must be left as a symbol with an explicit in-prose note that the value is uzasadniony na etapie finalizacji metodyki (post-Phase 04), consistent with the ROPE deferral in the same block. Do NOT cite Demsar 2006 §3.1 as a normative source for α = 0,05 — Demsar uses α = 0,05 as a convention in worked examples, not as an endorsed threshold. Candidate phrasing: *"…przy rodzinnym poziomie istotności α ustalonym w toku finalizacji metodyki (§4.4.2) — wartość α nie jest fiksowana w niniejszej sekcji z tych samych względów co szerokość ROPE"*.
   - **Must cite:** `[Benavoli2016]`, `[Benavoli2017]`, `[GarciaHerrera2008]`, `[Garcia2010]`, `[Wilcoxon1945]`, `[Holm1979]` (all retained)
   - **Must hedge:** no "Niniejsza praca raportuje", no fixed ROPE width, no "aktualnie rekomendowany"
   - **Must cross-reference:** forward-ref to §4.4.4 as the location where the within-game protocol will be finalized.
6. Fix F5.6 citation error: §2.6.3 line 211 currently says *"Demšar [Demsar2006] rekomenduje test Friedmana jako standardowe narzędzie omnibusowe, lecz wskazuje warunek dotyczący liczby bloków: dla $N < 5$ moc testu jest na tyle niska…"*. Verify via WebFetch that the N ≥ 5 recommendation lives at §3.1.3 of Demšar 2006; if confirmed, add explicit section reference (e.g., *"[Demsar2006, §3.1.3]"*). If unverifiable via WebFetch, plant `[REVIEW: Demšar §3.1.3 citation section]`.
7. Rewrite §2.6.5 Podsumowanie (line 231). Target: present the three-level protocol as a catalogue of candidate procedures informed by the cited literature, with a closing sentence making explicit that the adoption decision for within-game comparison is deferred to §4.4.4.
   - **Must cite:** all existing bibkeys retained
   - **Must hedge:** every "jest" / "raportuje" / "stosuje" at the protocol-naming level must be softened to "zostanie rozpatrzon", "stanowi kandydata", or equivalent
   - **Must cross-reference:** forward-ref to §4.4.4
   - **Must contrast:** preserve the existing contrast against Nemenyi (line 213) as an example of methodological revision.
8. Update §2.6.4 (cross-game protocol, lines 221–227) minimally — only to ensure consistency. Current wording at line 225 (*"Niniejsza praca raportuje oba"* for Nadeau-Bengio + 5×2 cv F-test); soften to candidate framing (*"rozpatrywane są dwa kandydaty"* or equivalent). Do NOT expand §2.6.4 otherwise.
9. Update §2.6 row in `thesis/WRITING_STATUS.md`: status from `DRAFTED` → `REVISED`, add dated Notes entry: *"2026-04-20 (PR-TG1): §2.6.2 final ¶, §2.6.3 Wilcoxon-Holm + Bayesian-ROPE blocks, §2.6.4 cross-game candidate framing, §2.6.5 summary — all rewritten to un-commit within-game protocol and triptych per Pass-2 TG1 dispatch. F5.6 Demsar §3.1.3 citation fix applied in §2.6.3."*
10. Update the existing §2.6 Pending row in `thesis/chapters/REVIEW_QUEUE.md` (line 25): append a 2026-04-20 PR-TG1 revision note to the Pass 2 status column (do NOT add a new row — the existing one is still open).
11. Do NOT introduce new bibkeys. No `thesis/references.bib` modification.
12. Produce writer-thesis Chat Handoff Summary.

**Verification:**
- `grep -cn "pełny tryptyk\|Aktualnie rekomendowan\|ROPE = ±0,01\|Niniejsza praca raportuje" thesis/chapters/02_theoretical_background.md` returns 0 matches.
- `grep -n "kandydat\|rozpatrywan\|zostanie rozpatrzon" thesis/chapters/02_theoretical_background.md` returns multiple matches in §2.6.2, §2.6.3, §2.6.5 line ranges.
- `grep -n "Demsar2006.*§3\|§3\.1\.3" thesis/chapters/02_theoretical_background.md` returns at least one match in §2.6.3 (F5.6 fix landed, or [REVIEW] flag planted).
- `grep -n "α = 0,05\|α=0,05\|alpha = 0.05\|α = 0.05" thesis/chapters/02_theoretical_background.md` returns 0 matches in §2.6.3 line range.
- [sanity-check, not blocking] §2.6 total character count unchanged ± 1,500 characters.
- No net-additive substance: the T02 rewrites of §2.6.2/§2.6.3/§2.6.4/§2.6.5 substitute pre-TG1 prose with candidate-set framing plus the F5.6 citation fix and α-deferral. No new methodological claims beyond what the pre-TG1 prose named. Verified via writer-thesis Chat Handoff Summary enumeration.
- `thesis/WRITING_STATUS.md` §2.6 row status is `REVISED` with 2026-04-20 note.
- `thesis/chapters/REVIEW_QUEUE.md` existing §2.6 row has PR-TG1 revision note appended.

**File scope:**
- `thesis/chapters/02_theoretical_background.md` (Update §2.6.2 final ¶, §2.6.3 Wilcoxon-Holm + Bayesian-ROPE blocks, §2.6.4 minimal cross-game candidate-framing update, §2.6.5 summary, F5.6 citation fix)
- `thesis/WRITING_STATUS.md` (Update §2.6 row)
- `thesis/chapters/REVIEW_QUEUE.md` (Append to existing §2.6 row)

**Read scope:**
- `thesis/chapters/01_introduction.md` §1.2 ¶1 (T01's output)
- `.claude/author-style-brief-pl.md`
- `.claude/rules/thesis-writing.md`
- `.claude/scientific-invariants.md`

---

### T03 — §4.4.4 revision (methodology chapter)

**Objective:** Rewrite §4.4.4 to (i) drop the hard commitment to Friedman + Wilcoxon-Holm + Bayesian signed-rank as *the* within-game protocol in favour of the candidate-list framing established in §2.6, (ii) preserve ECE + reliability diagrams + Murphy decomposition as the operational aggregate-level diagnostic (per Open Q 2 option **b**), noting the triptych as a candidate alternative pending methodology finalization, and (iii) plant forward-refs to §2.6 and §1.2 that now point at consistently-hedged language.

**Instructions:**
1. Read `thesis/chapters/04_data_and_methodology.md` §4.4.4 in full (lines 361–371).
2. Read T01 and T02 outputs (revised §1.2 ¶1 + revised §2.6) to ensure forward-refs remain accurate.
3. Read `.claude/author-style-brief-pl.md`, `.claude/rules/thesis-writing.md`.
4. Rewrite §4.4.4 Metryki podstawowe (line 365): retain Brier + log-loss as primary + Murphy decomposition per `[Gneiting2007]` + `[Murphy1973]` + `[Brier1950]`. Explicit but non-committing mention: Dimitriadis triptych is a candidate diagnostic framework whose adoption is deferred.
5. Rewrite §4.4.4 Metryki dyskryminacyjne (line 367): retain ROC-AUC + ECE + reliability diagrams as the operational aggregate-level diagnostic (Open Q 2 option **b**). Note the Dimitriadis triptych explicitly as a candidate alternative to that operational set, pending post-experiment methodology finalization. The commitment-level assigned here to ECE + reliability diagrams + Murphy decomposition (operational) must match the designation in §2.6.2 (per T02 step 4) — this is the cross-section consistency required by the Option B target end-state.
5.5. Cross-chapter framing consistency checklist (blocking). Before finalising the §4.4.4 rewrite, explicitly verify the commitment-level in each of the following sections and confirm all are consistent:
   - §1.2 ¶1: ECE + reliability + Murphy = operational aggregate-level diagnostic; triptych = candidate alternative under consideration relative to that operational diagnostic (per T01 output, consistent with Option B)
   - §2.6.2: ECE + reliability + Murphy = operational aggregate-level diagnostic; triptych = candidate alternative to that set (per T02 step 4 output, Option B)
   - §2.6.3: within-game statistical comparison = candidate protocol, not committed; ROPE width not fixed
   - §2.6.4: cross-game N=2 protocol framed as candidate set (5×2 cv F-test / Nadeau-Bengio); confirm the within-game vs. cross-game distinction remains clean after §4.4.4 rewrite — no within-game test should appear in §2.6.4 and no cross-game test should appear in the §4.4.4 within-game candidate list
   - §2.6.5: three-level protocol = candidate set; adoption deferred to §4.4.4
   - §4.1.4 (lines 209–213): Friedman + Wilcoxon-Holm named as "inapplicable at N=2" — confirm this negative-framing remains coherent with the deferred-candidate framing now in §4.4.4 (no rewrite of §4.1.4 required, but flag any incoherence)
   - §4.4.4 (this task): ECE + reliability + Murphy = operational (consistent with §2.6.2); triptych = candidate alternative; within-game comparison protocol = deferred candidate space (multiple alternatives named)
   If any section's commitment-level is inconsistent with the target, flag a `[REVIEW: cross-section framing inconsistency after TG1 rewrite]` and do NOT silently resolve it.
6. Rewrite §4.4.4 Porównanie within-game i cross-game (line 371). Current: *"W ramach jednej gry — przy $N_{folds} \geq 5$ — porównanie modeli prowadzone jest w trybie omnibusa Friedmana [Friedman1937] z testami post-hoc Wilcoxon-Holm [Holm1979, Wilcoxon1945] oraz bayesowskim signed-rank via baycomp [Benavoli2017]."* Target: present the within-game statistical comparison as a deferred *candidate space* — enumerating at least two named alternative protocols — with the adoption decision explicitly deferred to methodology finalization after Phase 04 completes.
   - **Candidate-space enumeration (required):** The rewritten paragraph must enumerate at least two genuinely distinct inferential families for within-game comparison, making the deferral substantive rather than a mere verb-swap. The candidate families, all drawing on the comparative-testing survey by Demšar `[Demsar2006]`, are:
     1. **Rangowa frequentystyczna rodzina** — Friedman omnibus + post-hoc Wilcoxon-Holm (`[Friedman1937]`, `[Wilcoxon1945]`, `[Holm1979]`), motywowana krytyką Nemenyi w `[Benavoli2016]` oraz zanalizowana przez `[GarciaHerrera2008]`. Warianty bramkowania (ang. *gating*): (a) z testem omnibusowym jako warunkiem wstępnym dla post-hoc, (b) bez omnibusa z kontrolą błędu rodzinnego wyłącznie przez korekcję Holma zgodnie z `[GarciaHerrera2008]`.
     2. **Bayesowska rodzina** — bayesowski test rang znaków via `baycomp` (`[Benavoli2016]`, `[Benavoli2017]`), niezależny od założenia omnibusa frequentystycznego, raportujący trzy prawdopodobieństwa $P(A > B)$, $P(A \approx B)$, $P(B > A)$ przy odroczonej szerokości ROPE (§2.6.3).
     3. **Rodzina resamplingowa (permutacyjna / bootstrap par)** — paired-bootstrap średniej różnicy metryki między fałdami CV lub test permutacyjny studentyzowany, jako alternatywa resamplingowa nie oparta o rangi ani posterior — empirycznie rekonstruująca rozkład zerowy różnicy metryki poprzez resampling fałdów. Rodzina ta jest spójna metodologicznie z bootstrapem stosowanym cross-game w §2.6.4 i nie wymaga nowych bibkeyów.
   - **Rationale for the "two families plus gating variants" framing:** The Friedman-omnibus-then-post-hoc-Wilcoxon pipeline (family 1, gating variant a) and the Holm-only-sequential-Wilcoxon pipeline (family 1, gating variant b) share the rank-based frequentist framework and differ only in the omnibus-gating decision; presenting them as **one family with two gating variants** is methodologically more honest than presenting them as two independent candidates. Family 2 (Bayesian) and family 3 (resampling) are genuinely distinct inferential frameworks.
   - Note: 5×2 cv F-test `[Dietterich1998]` and Nadeau-Bengio corrected t-test `[Nadeau2003]` are **cross-game** protocols catalogued in §2.6.4; they must **not** appear in the within-game candidate list at §4.4.4.
   - The rewrite must NOT single-select one candidate with the definite article "kandydatem jest X" while preserving the full bibkey ensemble of the original — that pattern is semantically isomorphic to the original commitment (only the verb changes). The §4.4.4 rewritten paragraph must enumerate at least two named within-game alternative protocols directly — no forward-reference to §2.6 is an acceptable substitute for this enumeration.
   - **N_folds ≥ 5 threshold:** The ≥5 threshold is a property of the Friedman test specifically (per `[Demsar2006, §3.1.3]`). Either (a) scope it explicitly inside the conditional — "if Friedman omnibus is selected as the within-game protocol, N_folds ≥ 5 is required per [Demsar2006, §3.1.3]" — or (b) note that the fold-count threshold itself is a Demsar-derived condition that will be operationalized at protocol finalization. Do NOT carry the unqualified ≥5 threshold into the candidate framing as if Friedman is already selected.
   - Forward-ref to §2.6 for the fuller candidate-set discussion (not to §2.6 as a completed protocol).
   - Acknowledge invariant #8 as ADVISORY guidance informing the candidate set (not as a fixed contract).
   - **Must cite:** retain all existing bibkeys; no new bibkeys.
   - **Must hedge:** replace every "prowadzone jest", "raportuje się dodatkowo", "Operacjonalizuje się" (when attached to protocol commitments) with candidate-language equivalents.
   - **Must cross-reference:** forward-ref to §2.6 (candidate-set discussion), forward-ref to §4.4.2 (Phase 04 methodology finalization — currently BLOCKED, which supports the deferral framing).
6.5. **§4.1.4 line 213 within-game/cross-game qualifier.** Insert a within-game/cross-game scoping qualifier into the sentence at `04_data_and_methodology.md:213` *"…dla N = 2 gier Friedman oraz Wilcoxon-Holm są inaplikowalne per [Demsar2006]."*. Target replacement: *"…w porównaniu **cross-game** przy N = 2 gier Friedman oraz Wilcoxon-Holm są inaplikowalne per [Demsar2006, §3.2]; analogiczne porównania **w ramach jednej gry** (z N = fałdów CV) są przedmiotem §4.4.4."* or equivalent Polish idiomatic phrasing. Must NOT upgrade the candidate-vs-committed framing of §4.1.4; this is a clarification-only edit to prevent the post-TG1 reader from inferring that §4.1.4 carries firmer methodology than §4.4.4. The section reference `[Demsar2006, §3.2]` (cross-game N ≥ 10 corollary) is distinct from `[Demsar2006, §3.1.3]` used in T02 step 6 (within-game N ≥ 5 blocks) — do not conflate.
7. Preserve the existing N=2 Friedman corollary argument (Demsar 2006 §3.2 N ≥ 10 issue) — this is a correct methodological point that does not require un-committing.
8. Preserve both existing [REVIEW:] flags at line 371 and add a new flag at the rewritten within-game protocol commitment point: *"[REVIEW: Pass-2 TG1 — within-game statistical protocol is candidate; adoption decision deferred to methodology finalization after Phase 04 (cf. invariant #8 advisory role)]"*.
9. Update §4.4.4 row in `thesis/WRITING_STATUS.md`: status from `DRAFTED` → `REVISED`, add dated Notes entry: *"2026-04-20 (PR-TG1): §4.4.4 within-game protocol rewritten from hard commitment to candidate-list framing per Pass-2 TG1 dispatch. Forward-refs to §2.6 (candidate set) and §1.2 (triptych as candidate diagnostic) confirmed consistent."*
10. Update the existing §4.4.4 Pending row in `thesis/chapters/REVIEW_QUEUE.md` (line 40): append a 2026-04-20 PR-TG1 revision note. Flag count becomes 3 [REVIEW] (2 existing + 1 new TG1 flag). **Executor warning:** `thesis/chapters/REVIEW_QUEUE.md` lines 43–44 carry a malformed row anomaly — the *"§4.4.6 | Post-F1 revision | DRAFTED | …"* row at line 43–44 is preceded by a blank line and uses a 4-column schema while the main table (line 38+) uses a 7-column schema. This anomaly is not a TG1 concern but may break naive `grep`/`sed` scripting when locating the *existing* §4.4.4 Pending row (line 40) for the T03 append. Target the §4.4.4 row explicitly by matching on *"§4.4.4 Evaluation metrics"* in the second column, not by line number offset from the §4.4.6 row. Do NOT resolve the line 43–44 anomaly in TG1 — it is separate scope (§4.4.6 coordination, Open Q 3).
11. Do NOT modify §4.4.5 or §4.4.6. Do NOT introduce new bibkeys.
12. Produce writer-thesis Chat Handoff Summary.

**Verification:**
- `grep -cn "porównanie modeli prowadzone jest\|Niniejsza praca raportuje" thesis/chapters/04_data_and_methodology.md` returns 0 matches (within §4.4.4 line range).
- `grep -n "kandydat\|kandydatem statystycznego\|zostanie rozpatrzon\|odroczon\|finalizacj" thesis/chapters/04_data_and_methodology.md` returns at least one match in §4.4.4 line range.
- `grep -n "§2\.6\|§1\.2\|§4\.4\.2" thesis/chapters/04_data_and_methodology.md` confirms forward/cross-refs in §4.4.4.
- `grep -cn "Pass-2 TG1" thesis/chapters/04_data_and_methodology.md` returns at least 1 match (the new [REVIEW:] flag).
- [sanity-check, not blocking] §4.4.4 character count unchanged ± 1,000 characters.
- `thesis/WRITING_STATUS.md` §4.4.4 row status is `REVISED` with 2026-04-20 note.
- `thesis/chapters/REVIEW_QUEUE.md` existing §4.4.4 row has PR-TG1 revision note appended, flag count 3.
- `grep -n "cross-game\|w ramach jednej gry\|w porównaniu cross-game" thesis/chapters/04_data_and_methodology.md` returns at least one match in §4.1.4 line 213 range.
- No net-additive substance: the T03 rewrite of §4.4.4 either substitutes pre-TG1 prose with candidate-set framing, or adds clarification (N_folds ≥ 5 conditional scoping, within-game/cross-game qualifier). It does NOT introduce new protocols or diagnostics beyond the three-family candidate enumeration and ECE + reliability + Murphy operational designation. Verified via writer-thesis Chat Handoff Summary enumeration.
- Post-rewrite cross-section consistency sweep: `grep -n "pełny tryptyk\|Aktualnie rekomendowan\|ROPE = ±0,01\|prowadzone jest w trybie omnibusa" thesis/chapters/{01,02,04}*.md` returns 0 matches across all three files.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (Update §4.4.4 only)
- `thesis/WRITING_STATUS.md` (Update §4.4.4 row)
- `thesis/chapters/REVIEW_QUEUE.md` (Append to existing §4.4.4 row)

**Read scope:**
- `thesis/chapters/01_introduction.md` §1.2 ¶1 (T01's output)
- `thesis/chapters/02_theoretical_background.md` §2.6 (T02's output)
- `thesis/chapters/04_data_and_methodology.md` §4.1.4 (lines 209–213 — Friedman + Wilcoxon-Holm "inapplicable at N=2" framing; confirm it remains coherent after §4.4.4 rewrite)
- `.claude/author-style-brief-pl.md`
- `.claude/rules/thesis-writing.md`
- `.claude/scientific-invariants.md`

---

## File Manifest

| File | Action |
|------|--------|
| `thesis/chapters/01_introduction.md` | Update (§1.2 ¶1 closing sentence only) |
| `thesis/chapters/02_theoretical_background.md` | Update (§2.6.2 final ¶, §2.6.3 Wilcoxon-Holm + Bayesian-ROPE blocks, §2.6.4 minor cross-game tweak, §2.6.5 summary, F5.6 Demsar §3.1.3 citation fix) |
| `thesis/chapters/04_data_and_methodology.md` | Update (§4.4.4 primary rewrite; §4.1.4 line 213 one-sentence within-game/cross-game qualifier; §4.4.5 and §4.4.6 untouched) |
| `thesis/WRITING_STATUS.md` | Update (§1.2 note, §2.6 status → REVISED, §4.4.4 status → REVISED) |
| `thesis/chapters/REVIEW_QUEUE.md` | Update (new §1.2 ¶1 Pending row; append 2026-04-20 PR-TG1 note to existing §2.6 and §4.4.4 Pending rows) |

## Gate Condition

All conditions must hold after execution for PR-1 to merge.

- §1.2 ¶1 closing sentence frames the Dimitriadis triptych as a candidate alternative to the current operational aggregate-level diagnostic (ECE + reliability diagrams + Murphy decomposition), matching the §2.6.2 and §4.4.4 Option B designation, with adoption deferred to Chapter 4 methodology finalization. `grep` confirms target phrases present and forbidden phrases absent.
- §2.6.2 no longer uses *"pełny tryptyk"* or *"jest planowane"*; explicitly designates ECE + reliability diagrams + Murphy decomposition as the operational aggregate-level diagnostic and names the triptych as a candidate alternative to that operational set.
- §1.2, §2.6.2, and §4.4.4 assign the same commitment-level to ECE + reliability diagrams + Murphy decomposition: all three designate it as the operational aggregate-level diagnostic (Option B consistency check).
- §2.6.3 no longer uses *"Aktualnie rekomendowanym protokołem"* for Wilcoxon-Holm; frames it as a candidate motivated by `[Benavoli2016]` critique of Nemenyi.
- §2.6.3 ROPE width is NOT fixed at ±0,01 (invariant #7 compliance restored); framing hedges to "dobór uzasadniony na etapie finalizacji metodyki".
- §2.6.3 does NOT fix α at 0,05 (or any other numeric value); Holm schedule mechanics cite α symbolically, consistent with the ROPE deferral (invariant #7 full compliance, not half).
- §2.6.4 cross-game N=2 discussion frames 5×2 cv F-test + Nadeau-Bengio as candidate protocols, not as committed.
- §2.6.5 summary presents three-level protocol as candidate set, with explicit deferral to §4.4.4 and invariant #8 cited as advisory.
- §2.6.3 F5.6 Demsar §3.1.3 citation fix applied (or, if unverifiable in this pass, tagged with `[REVIEW: Demsar §3.1.3 section verification]`).
- §4.4.4 no longer uses *"porównanie modeli prowadzone jest w trybie omnibusa Friedmana"* or equivalent hard commitment; §4.4.4 enumerates at least two genuinely distinct inferential families (rank-based frequentist, Bayesian, resampling) as candidate protocols directly, with any sub-variants (e.g., omnibus-gated vs. Holm-only sequential) labelled as gating variants of their parent family, not as independent candidates. A forward-reference to §2.6 is not an acceptable substitute for this enumeration.
- §4.4.4 N_folds ≥ 5 threshold is scoped inside a conditional on Friedman selection, or flagged as a Demsar-derived condition deferred to protocol finalization — not carried as an unqualified threshold into the candidate framing.
- §4.1.4 line 213 carries an explicit within-game/cross-game scoping qualifier; sentence no longer reads as unqualified Friedman+Wilcoxon inapplicability and no longer risks being read as firmer methodology than §4.4.4.
- §4.4.4 forward-refs to §2.6 and §1.2 point at consistently-hedged language; no cross-reference cycles.
- Across all three chapter files, a unified post-rewrite grep sweep shows zero remaining hard-commitment phrases from the pre-TG1 state.
- `thesis/WRITING_STATUS.md` updated (§1.2 note, §2.6 → REVISED, §4.4.4 → REVISED).
- `thesis/chapters/REVIEW_QUEUE.md` updated with new §1.2 ¶1 row + appended notes on existing §2.6, §4.4.4 rows.
- No new bibkeys introduced (`git diff thesis/references.bib` returns no changes).
- No edits outside the File Manifest.
- **No net-additive substance.** Each TG1 rewrite is a commitment-strength adjustment (hard-commit → candidate-set) paired with minor clarifications (F5.6 citation fix, §4.1.4 qualifier, α-deferral, operational-diagnostic designation). No rewrite introduces a new methodological claim, protocol, diagnostic, or threshold not already present in the pre-TG1 prose or explicitly warranted by a cited reference already in `references.bib`. Character budget overshoots beyond ±10% require a paragraph-by-paragraph justification in the writer-thesis Chat Handoff Summary demonstrating that the overshoot corresponds to the candidate-set enumeration expansion and not to new substance.
- reviewer-adversarial Mode C draft review (Step 5 per `thesis/plans/writing_protocol.md`) returns PASS or REQUIRE_MINOR_REVISION.
- Cross-section consistency pass (T03 step 5.5) confirms consistent un-commitment framing across §1.2, §2.6.2, §2.6.3, §2.6.5, §4.1.4, and §4.4.4; any incoherence is flagged with `[REVIEW: cross-section framing inconsistency after TG1 rewrite]` rather than silently resolved.
- Post-merge halt: TG2 planning does not begin until the user reviews the merged PR-1 diff and explicitly requests re-planning (per Open Q 1 Option β and the halt-and-review protocol).

## Rollback plan

If PR-1 is rejected at review, all three chapter rewrites can be individually reverted via `git revert` of the PR merge commit. The `thesis/WRITING_STATUS.md` DRAFTED → REVISED transitions are single-row inversions. The `thesis/chapters/REVIEW_QUEUE.md` appended notes are removed in the same revert. No empirical artifacts or bibkeys are touched, so rollback carries no data-layer risk.

## Out of scope

- **TG2** — Factual contradictions (§4.1.1.1 date range 2016–2024 vs §4.1.1.2 2016–2022; Mountain Royals date; 45 AoE2 civs window-dependent). Separate PR.
- **TG3** — Luka 3 narrowing (§3.5 amendment against Thorrez 2024 EsportsBench; 3-part edit). Separate PR.
- **TG4** — 11 bibliography findings (García-Méndez, Hodge, Bunker, SC-Phi2, Aligulac, Elbert, EsportsBench, Baek, Glickman, Lin, Çetin Taş). Separate PR.
- **TG5** — 6 internal-consistency fixes (except F5.6 Demsar §3.1.3, which lands in T02 as a single-line citation correction because it is natural to pair with §2.6.3 rewrite). Separate PR.
- **TG6** — 12 prophylactic/hygiene fixes. Separate PR.
- **§4.4.5** — Wybór estymatora ICC. Untouched by TG1.
- **§4.4.6** — `[PRE-canonical_slot]` flag. Untouched by TG1; coordinates with existing `REVIEW_QUEUE.md:44` Pending *"Post-F1 revision"* entry, which lands in a separate Cat F session (Open Q 3 resolution).
- **`.claude/scientific-invariants.md`** — not modified; invariant #8 remains aspirational-advisory text (Open Q 4 resolution). Any future hard-commitment of the within-game protocol would motivate a companion edit, out of TG1 scope.
- **Chapter 5 / 6 / 7 forward-refs** — BLOCKED in WRITING_STATUS.md; no prose touches them.
- **New empirical claims** — none. Prose-only rewriting.
- **Phase 01 artifact modification** — invariant #9 forbids; nothing in TG1 requires it.
- **Bibkey additions** — none. All citations exist in `thesis/references.bib`.
- **Çetin Taş 2023 verification** (F4.11) — persistent `[REVIEW:]` flag stays in place; out-of-scope.
- **Master-roadmap archiving of the user's Pass-2 dispatch** — recommended as a separate Category C chore (file the dispatch as `thesis/plans/pass2_dispatch_master.md`) but NOT part of this plan (Open Q 1 resolution: Option β).

## Open questions

All four load-bearing Open Questions have been resolved by the user (2026-04-20):

- **Open Q 1 (plan-scope dispatch model) — RESOLVED: Option β.** Author this one plan for PR-1 / TG1 only; re-plan sequentially for PR-2..PR-9. The user's original Pass-2 dispatch stays outside `planning/` as a reference (archival as `thesis/plans/pass2_dispatch_master.md` is a separate Category C chore, not part of this plan).
- **Open Q 2 (§4.4.4 target framing) — RESOLVED: option (b).** ECE + reliability diagrams + Murphy decomposition remain the operational aggregate-level diagnostic; the triptych is noted as candidate alternative pending Phase 04 methodology finalization. Resolution source: in-session user directive, 2026-04-20 (no external artifact). reviewer-adversarial Mode A should independently confirm option (b) alignment before T03 executes — see Open Q 7.
- **Open Q 3 (§4.4.6 coordination) — RESOLVED: stay off.** TG1 does not touch §4.4.6; the existing `REVIEW_QUEUE.md:44` Post-F1 revision entry is handled in a separate Cat F session.
- **Open Q 4 (invariant #8 textual framing) — RESOLVED: advisory only.** `.claude/scientific-invariants.md` remains unchanged; TG1 prose rewrites treat invariant #8 as ADVISORY guidance and not as a hard commitment.

Remaining deferred questions:

- **Open Q 5 (Ambiguity B — §4.2 scope verification) — RESOLVED: §4.2 untouched.** Reviewer-adversarial Mode A (2026-04-20) independently ran `grep -n 'Dimitriadis|tryptyk|Nemenyi|Wilcoxon|Friedman|signed-rank|Bayesian|ROPE' thesis/chapters/04_data_and_methodology.md` and confirmed exactly 2 hits: line 213 (§4.1.4) and line 371 (§4.4.4). §4.2 carries zero hits. Dispatch §1.1's *"other §4.x subsections remain BLOCKED"* remains factually wrong as a blanket claim (§4.2.1–§4.2.3 are DRAFTED/REVISED), but the scope-by-omission is correct: no TG1 finding touches §4.2. No plan edit required. Resolution source: `planning/current_plan.critique.md` MINOR A4 / Probe 8.
- **Open Q 6 (F5.6 Demsar §3.1.3 citation — verification).** writer-thesis during T02 execution verifies via WebFetch whether Demšar 2006 §3.1.3 houses the N ≥ 5 recommendation. If yes, apply citation fix; if unverifiable, plant `[REVIEW:]` flag. **Resolves by:** writer-thesis during T02.
- **Open Q 7 (target end-state validation).** reviewer-adversarial Mode A validates whether *"triptych as one candidate among several alongside ECE + reliability diagrams + Murphy decomposition"* genuinely un-commits the prose rather than re-committing at a lower abstraction. **Resolves by:** reviewer-adversarial Mode A.

---

**Adversarial critique triggers for Step 2** (reviewer-adversarial Mode A targeting recommendations — NOT the critique itself):

- **Hardest-to-catch risk.** Whether the proposed target end-state introduces a NEW commitment (the competing alternatives being named) rather than removing a commitment. Reviewer should verify genuine un-commitment.
- **Cross-reference consistency.** Verify that §1.2 ¶1 → §4.4.4; §2.6.2/.3/.5 → §4.4.4; §4.4.4 → §2.6 + §1.2 form a connected, non-circular graph after rewrite. Any cycle is a structural bug.
- **Invariant #8 timing.** Verify the plan does not accidentally commit the thesis to a protocol that invariant #8 names advisorily. Probe whether T03's *"invariant #8 (advisory)"* framing is load-bearing or window-dressing.
- **ROPE width invariant #7 compliance.** Current §2.6.3 line 217 fixes ROPE = ±0,01 without citation or empirical justification — a straightforward invariant #7 violation. Reviewer should verify T02's rewrite removes the fixed value without smuggling in a different unjustified constant.
- **F5.6 Demsar §3.1.3 citation fix.** Reviewer should WebSearch the Demsar 2006 JMLR paper to confirm the N ≥ 5 recommendation lives at §3.1.3.
- **Voice consistency.** Check §1.2 revision output against §1.2 paragraphs 2–4 (unchanged), and §2.6.2–§2.6.5 post-rewrite flow against §2.6.1 (unchanged). Drift between rewritten and preserved paragraphs is a voice-calibration failure.
- **Scope creep guardrails.** Verify File Manifest is strictly limited to the five listed files and that no task prescribes edits to §4.4.5, §4.4.6, `references.bib`, or any Chapter 5/6/7 file.
- **Ambiguity B verification.** Grep `Dimitriadis|tryptyk|Nemenyi|Wilcoxon|Friedman|signed-rank|Bayesian|ROPE` independently across the full `04_data_and_methodology.md` to confirm §4.2 is untouched by TG1.
- **Option (b) decision re-verification.** Although Open Q 2 is resolved as (b), reviewer should independently consider whether option (a) would be a more defensible target end-state. If reviewer argues for (a), this is a plan-revision trigger, not a draft-time decision.
- **Pass-2 flag lifecycle.** The new [REVIEW:] flag planted in T03 must be correctly counted in the REVIEW_QUEUE flag count increment (2 → 3) and not conflict with existing Pass-2 flags.
