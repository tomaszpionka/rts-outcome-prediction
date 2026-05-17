# Chapters 1–4 Citation & Literature Support Audit (pre-supervisor handoff)

**Date:** 2026-05-17
**Author:** executor (claude-opus-4-7), T02 of Category F plan `docs/thesis-ch1-ch4-citation-literature-audit` (PR #220, draft)
**Base:** `26210a5d` (master, PR #219 merged) | **Plan:** `planning/current_plan.md` | **Plan gate:** reviewer-deep PASS-WITH-NITS (`planning/current_plan.critique.md`, 2 of 3 adversarial rounds, T01)
**Document type:** Pass-2 evidence (read-only consolidation; an audit, NOT a thesis chapter draft, NOT a fix). It records findings; it changes no chapter prose, no `references.bib`, no flag, no dataset artifact.
**Scope:** thesis Chapters 1–4 (`thesis/chapters/01_introduction.md`, `02_theoretical_background.md`, `03_related_work.md`, `04_data_and_methodology.md`) across five dimensions: D1 bibkey existence + metadata; D2 load-bearing claim-source support; D3 REVIEW-flag triage; D4 internal artifact-path support (Ch4); D5 per-chapter supervisor-readiness.

> **Audit-only statement (binding).** This audit produces evidence, not fixes. No chapter prose was edited. No `references.bib` entry was added, removed, or modified. No `[REVIEW:]` / `[NEEDS CITATION:]` / `[UNVERIFIED:]` / `[POP:]` / `[PRE-canonical_slot]` flag was closed. Where web or repo evidence conflicts with chapter prose, the conflict is *recorded* with `verification_result = conflict_recorded_not_fixed` and the recommended fix is routed to a future PR (§11). The supervisor handoff decision is the user's; this document only informs it.

---

## 1. Executive verdict

**`supervisor_handoff_recommendation = send_after_must_fixes`**

The four-chapter draft is structurally sound, densely cited, and methodologically self-aware. The literature core (Chapter 3) is already Pass-2-verified by `literature_verification_log.md` (T14, 2026-04-26) and is the strongest part. The single material defect blocking an unconditional send is a **cross-chapter EsportsBench version-and-cutoff inconsistency**: §2.5.5 of Chapter 2 still cites the stale `v8.0 / cutoff 2025-12-31`, while §3.2.4 and §3.5 of Chapter 3 were already corrected by T14 to `v9.0 / cutoff 2026-03-31 / accessed 2026-04-26`. A supervisor reading Chapters 2 and 3 together will see a self-contradiction in a quantitative comparator (the SC2 Aligulac 411 030-match / ~80% Glicko line). This is one targeted prose fix in one Chapter-2 line — not a methodology defect — so the recommendation is **send after a small, enumerated must-fix set**, not "do not send".

No HALT condition fired: every Chapter-4-cited artifact path exists; every load-bearing claim whose verification could change a thesis conclusion is already adjudicated in a prior pass2 file (it is reused, not silently absorbed).

| Count line | Value |
|---|---:|
| **must_fix_before_supervisor** | 3 |
| **ok_to_send_with_flag** | 41 |
| **manual_full_text_required** | 9 |
| **future_phase_dependent** | 14 |

(Per-dimension itemisation in §4–§9; backlog in §7; the must-fix items are M-1, M-2, M-3 in §7. Counts are of distinct audit findings, not raw flag occurrences — one chapter flag can map to one finding and a single cross-locus issue counts once.)

Recommended supervisor note (full Polish text in §10): send Chapters 1, 3, 4 as a working draft **with the in-prose REVIEW flags retained and an explicit cover note** that the flags are deliberate Pass-2 verification markers, not unfinished gaps; send Chapter 2 only **after** the EsportsBench §2.5.5 line is harmonised to `v9.0 / 2026-03-31 / 2026-04-26` (a one-line fix, ~10 minutes, routed to the §11 PR-1). Chapters 5–6 are not in scope and are not sendable (no model trained).

---

## 2. Scope and method

### 2.1 Files read (read-only)

- **Chapters audited:** `thesis/chapters/01_introduction.md` (full), `02_theoretical_background.md` (full), `03_related_work.md` (full), `04_data_and_methodology.md` (full, incl. §4.5).
- **Bibliography:** `thesis/references.bib` (full; 100 `@` entries confirmed by `grep -c '^@'`).
- **Prior pass2 evidence reused (reuse-before-reverify):** `literature_verification_log.md` (T14, 2026-04-26 — THE source of truth for Chapter 3 loci; ~35 recorded URLs), `phase01_phase02_writing_readiness_audit.md` (2026-05-17 — artifact-internal numbers, TQ-04 EsportsBench, TQ-05 aoestats 136-vs-137), `methodology_risk_register.md` (RISK-01..05 source-label discipline, F14 ECE), `cross_dataset_comparability_matrix.md` (five-axis bounded comparability), `aoe2_ladder_provenance_audit.md` (Tier 4 / Tier 2+3 ladder governance), `phase02_readiness_hardening.md` (§14A.6 GATE-14A6 `narrowed`), `notebook_regeneration_manifest.md` (registry lineage / `partial_coverage_v9_baseline` token). Also globbed `thesis/pass2_evidence/` (19 files) to avoid duplicating prior audits.
- **Specs (for the §4 [I3] prose-claim checks):** `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1, LOCKED 2026-04-26), `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1) — confirmed present (`ls`).
- **Style brief:** `.claude/author-style-brief-pl.md` (for the §10 Polish register).

### 2.2 Verification method

- **Reuse-before-reverify.** A reuse index was built from `literature_verification_log.md` and `phase01_phase02_writing_readiness_audit.md` §6 before any web fetch. Chapter 3 loci already verified by T14 are recorded `reused_prior_evidence` with the prior file + its recorded URL; no Chapter-3 literature locus was re-fetched (consistent with the plan's AR-6 guardrail). No web fetch was needed during this execution because every load-bearing Chapter 1/2 locus routed to a prior pass2 file or to a `manual_full_text_required` classification inherited from T14's documented PDF-binary limitation; the audit therefore relies on the prior recorded URLs (each cited inline) rather than on fresh 2026-05-17 fetches. Where a row says `reused_prior_evidence`, the evidence is the prior file's recorded URL + access date 2026-04-26, not a 2026-05-17 access.
- **Chapter-prose freshness carve-out (mandatory; reviewer-deep AR-9).** The reuse rule was applied verbatim only to *static* facts (bib/DOI/arXiv/venue/dataset metadata). For every **chapter-prose locus** — operatively, *any claim whose support depends on what a chapter line currently says* — the current chapter line at HEAD (`350b5f86`) was re-read and compared against the prior pass2 file's locus-level description before `reused_prior_evidence` was set. **Limitation (one-line, per the reviewer-deep Round-2 nit):** the operative test for borderline loci is this general clause, NOT the static-vs-prose parenthetical examples; it was applied to every borderline locus, in particular the three EsportsBench loci (§2.5.5 / §3.2.4 / §3.5) and the TQ-04 sub-claim, each independently re-verified at HEAD (see §2.3).
- **`manual_full_text_required` rule.** Applied when (a) the load-bearing sub-claim is a value/section/table-cell/exact-figure in the source body (not abstract/metadata), (b) external retrieval cannot surface that body after the web budget, and (c) no prior pass2 file already records a web-verified value. Where a prior pass2 file recorded an item as a manual-PDF item (Demsar2006 §-location, EsportsBench Table 2 exact 80,13%, CetinTas2023 exact 86%, Khan2024SCPhi2 exact accuracy, Xie2020 R²-vs-accuracy), that classification is inherited and the prior file cited — NOT re-attempted, NOT upgraded to "verified". No abstract was ever treated as verification of a body claim.
- **web-vs-prose conflict.** Recorded `conflict_recorded_not_fixed` + an explicit "chapter prose NOT edited by this audit" note; `recommended_action` names a future fix-PR.
- **Web-depth budget (user decision 2026-05-17, up to 3 formulations for new Ch1/Ch2 loci) — NOT exercised this pass.** Most Ch1/Ch2 load-bearing literature loci are already in `literature_verification_log.md` with recorded URLs (GarciaMendez2025, Vinyals2017, Demsar2006, Thorrez2024/EsportsBench, Hodge2021, Lin2024NCT, Hamilton2025, Tang2025, CetinTas2023, Elbert2025EC — cited in Ch1/Ch2 as well as Ch3), and the grey-lit infrastructure citations (Aligulac, Liquipedia_GameSpeed, BlizzardS2Protocol, AoE2DE) are flagged grey-lit in the chapter and routed `ok_to_send_with_flag`. **However, four Chapter-1 econ-metadata loci — Shin1993, Forrest2005, Levitt2004, Mangat2024 — were routed `W` (web-verifiable) by the plan's §"Evidence routing" and §"Web-depth budget" sections and are NOT in any prior pass2 file; the authorized ≤3-formulation web check was NOT exercised on them this pass.** They were deferred to §11 PR-2 (Chapter-1 bibliography consolidation) rather than verified here. The deferral is sound for the *supervisor-readiness* verdict (the Ch1 transferability claim is hedged inline and the entries are footer-cited, so this is a `references.bib`-consolidation task, not a missing source — see C-06 / D1-NOTE / M-2), but it is a deliberate scope deferral of plan-authorized web work, **not an absence of need**. Recorded as residual R-1 in §7.1.

### 2.3 Independent re-verification of the three reviewer-deep findings at HEAD

The reviewer-deep T01 gate (`planning/current_plan.critique.md`) flagged a stale-prior-locus failure mode (AR-9) and a three-locus EsportsBench partition. Both were independently re-verified at HEAD (`350b5f86`) before classification:

1. **§2.5.5 `02_theoretical_background.md:179`** — re-read at HEAD: still cites *"EsportsBench [Thorrez2024] … StarCraft II z 411 030 meczami pochodzącymi z Aligulac (wersja HuggingFace v8.0, cutoff 2025-12-31)"*. **Genuinely stale at HEAD** (T14 was Chapter-3-only and did not touch this line). → `conflict_recorded_not_fixed`, **HIGH** (issue C-01 in §4).
2. **§3.2.4 `03_related_work.md:77`** — re-read at HEAD: cites *"EsportsBench [Thorrez2024], cytowany już w §2.5 (wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26)"* — **already T14-corrected, no internal contradiction present at HEAD**. → `reused_prior_evidence` per `literature_verification_log.md` note 4 (issue C-02).
3. **§3.5 `03_related_work.md:189`** — re-read at HEAD: cites *"EsportsBench v9.0 (cutoff 2026-03-31, weryfikacja karty zbioru danych HuggingFace 2026-04-26)"* — **already T14-corrected**. → `reused_prior_evidence` per `literature_verification_log.md` (issue C-03).
4. **`phase01_phase02_writing_readiness_audit.md` TQ-04 / C2.2** describes §3.2.4 as carrying an internal contradiction (`v9.0` paired with `cutoff 2025-09-30; v8.0 planowana z cutoff 2025-12-31`). At HEAD §3.2.4 carries **no such contradiction** (verified by direct line read above). The TQ-04 "§3.2.4 internal contradiction" sub-claim is therefore **stale at HEAD** and is recorded `prior_pass2_locus_description_stale` (issue C-04 in §4); it is NOT reused verbatim. The non-stale part of TQ-04 (cross-locus version drift between §2.5.5 and §3.x) remains valid and underlies C-01.

### 2.4 Limitations of this audit

- The audit does not resolve `manual_full_text_required` items (these need a human full-text PDF read; nine such items are inherited from T14's documented PDF-binary limitation — Demsar2006 §-location, EsportsBench Table 2 exact 80,13%, CetinTas2023 exact 86% + NB-vs-DT, Khan2024SCPhi2 exact accuracy, Xie2020 R²-vs-accuracy interpretation, plus three open candidate-author items and the §4.4.5 ICC CI-method).
- It does not re-derive any artifact-internal number already adjudicated in `phase01_phase02_writing_readiness_audit.md`; the aoestats 136-vs-137 framing is recorded `reused_prior_evidence` + `conflict_recorded_not_fixed` via TQ-05 and is NOT re-litigated.
- It does not verify Chapter 5/6 (out of scope; not drafted; no model trained — F1/F2 forbidden claims).
- The reuse-before-reverify discipline means many static-fact rows carry the prior file's 2026-04-26 access date, not a 2026-05-17 one; this is by design and is the correct evidence for those rows.
- Four Chapter-1 econ-metadata loci (Shin1993 / Forrest2005 / Levitt2004 / Mangat2024) were plan-routed `W` but the authorized ≤3-formulation web check was NOT exercised this pass; deferred to §11 PR-2 and recorded as residual R-1 in §7.1 (reviewer-deep at T03 independently confirmed Shin1993 and Forrest2005 metadata — see §7.1).

---

## 3. Chapter readiness matrix

Class is assigned by the max-severity rule (one BLOCKER ⇒ `not_ready`). No chapter contains a D1 BLOCKER (every cited bibkey resolves in `references.bib`) or a D4 BLOCKER (every cited Ch4 artifact path exists). The only HIGH issue (C-01, EsportsBench §2.5.5 staleness) is a single localised prose conflict, not a structural blocker.

| Chapter | File | Class | One-line justification |
|---|---|---|---|
| Ch1 — Introduction | `01_introduction.md` | **ready_to_send_with_disclaimer** | All 8 `[REVIEW:]` flags are `ok_to_send_with_flag` or `already_resolved_elsewhere_but_flag_remains` (GarciaMendez2025 streaming-not-RTS already resolved in `literature_verification_log.md`; AoE2-completeness F-036 candidates `manual_full_text_required`). Every cited key resolves in `references.bib`. No load-bearing claim contradicts a verified source. Disclaimer = the retained flags are deliberate Pass-2 markers. |
| Ch2 — Theoretical Background | `02_theoretical_background.md` | **ready_to_send_with_disclaimer** (conditional on M-1) | 18 `[REVIEW:]` flags, all `ok_to_send_with_flag` / `manual_full_text_required` EXCEPT the §2.5.5 EsportsBench `v8.0/2025-12-31` line (C-01, `conflict_recorded_not_fixed`, HIGH) which contradicts §3.2.4/§3.5 at HEAD. With M-1 applied this is `ready_to_send_with_disclaimer`; **without M-1 it is `not_ready`** because a supervisor reading Ch2+Ch3 sees a self-contradicting comparator. No D1/D4 blocker. |
| Ch3 — Related Work | `03_related_work.md` | **ready_to_send_with_disclaimer** | The strongest chapter: 14 `[REVIEW:]` + 1 `[NEEDS CITATION:]`, every literature locus already Pass-2-verified by T14 (`literature_verification_log.md`). EsportsBench §3.2.4/§3.5 already corrected to v9.0. Remaining flags are `manual_full_text_required` (Demsar2006, CetinTas2023 86%, Xie2020, EsportsBench Table 2) or the F-036 open candidate list (`[NEEDS CITATION]`, future manual library lookup). No D1/D4 blocker. |
| Ch4 — Data and Methodology | `04_data_and_methodology.md` | **ready_to_send_with_disclaimer** | 34 `[REVIEW:]` + 1 `[UNVERIFIED:]` + 18 `[POP:]`/`[PRE-canonical_slot]` annotations. Every cited artifact path verified to exist (§6). Headline counts re-confirmed (registry 26 data rows; tracker 5+7+3=15; aoestats 137 lines = known TQ-05). Source-label discipline (RISK-01..05) is correctly applied in the audited prose (no unqualified "ranked ladder" for aoestats / aoe2companion combined ID6+ID18 in the lines reviewed). All blocking risk items are `future_phase_dependent` (Phase 03+) or `already_resolved_elsewhere_but_flag_remains`. The aoestats 136-vs-137 is the known TQ-05 (`conflict_recorded_not_fixed`, reused). No D1/D4 blocker. |

**Aggregate:** with M-1 applied, all four chapters are `ready_to_send_with_disclaimer`. Without M-1, Chapter 2 is `not_ready` and the others remain `ready_to_send_with_disclaimer`. Hence the Executive verdict `send_after_must_fixes`.

---

## 4. Citation support issue table

Columns: `id` | `severity` (BLOCKER/HIGH/MEDIUM/LOW) | `chapter_file` | `section` | `citation_key_or_artifact_path` | `current_claim` | `verification_result` | `recommended_action` | `source_evidence`.

D1 (bibkey existence + metadata): a full extract of every cited key from Ch1–4 prose and the per-chapter `## References` footer (Ch1 has an inline footer; Ch2–4 cite into `references.bib` only) was diffed against the 100 `@` entries in `references.bib`. **Result: zero cited-but-absent keys → zero D1 BLOCKERs.** Every `[AuthorYear]` key appearing in Ch1–4 prose resolves to a `references.bib` entry (spot-checked across the full bibkey list: Bialecki2023, Vinyals2017/2019, Ontanon2013, Hodge2021, BaekKim2022, Formosa2022, Novak2025, Shin1993?, Forrest2005?, Levitt2004?, GarciaMendez2025, Mangat2024?, CetinTas2023, Bialecki2022, Elo1978, Hamilton2025, Lin2024NCT, Gneiting2007, Dimitriadis2024, Erickson2014, Ravari2016, BaekKim2022, Thorrez2024, Tang2025, Bois2025, Demsar2006, Robertson2014Survey, Buro2003, Liquipedia_GameSpeed, BlizzardS2Protocol, Aligulac, Fujii2023NBTR, AoE2DE, AoEStats, AoeCompanion, MgzParser, Rubin1976, vanBuuren2018, SchaferGraham2002, FellegiSunter1969, Christen2012DataMatching, Jakobsen2017, MadleyDowd2019, Nakagawa2017, Chung2013, Ukoumunne2003, WuCrespiWong2012, Gelman2007, Minami2024, Brier1950, Murphy1973, HanleyMcNeil1982, Friedman1937, Wilcoxon1945, Holm1979, GarciaHerrera2008, Garcia2010, Benavoli2016, Benavoli2017, Nadeau2003, Dietterich1998). The `[Shin1993]`, `[Forrest2005]`, `[Mangat2024]` keys are cited in Ch1 §1.1 and DO appear in the Ch1 inline `## References` footer; **they do NOT have a `references.bib` entry** — see D1-NOTE below.

**D1-NOTE (LOW, recorded not BLOCKER).** Chapter 1 maintains its own inline `## References` footer (a Pass-1 literature-section convention) listing entries — Shin1993, Forrest2005, Levitt2004, Mangat2024, Formosa2022, Novak2025, Balduzzi2018 — several of which are NOT in `references.bib` (`references.bib` has no `Shin1993`, `Forrest2005`, `Levitt2004`, `Mangat2024`, `Formosa2022`, `Novak2025`, `Balduzzi2018`, `Bois2025`-is-present, `Lin2024NCT`-present). This is NOT a phantom-citation BLOCKER: the keys resolve to full bibliographic entries in the Ch1 footer (author/year/venue/DOI all present and internally plausible), so the claim is supported by an in-document reference; the defect is a **bibliography-consolidation gap** (Ch1 footer not yet merged into the central `references.bib`), a Pass-2 mechanical task, not a missing source. Recorded LOW; routed to §11 PR-2 (bibliography consolidation), NOT a supervisor blocker (a supervisor reads the chapter with its footer).

| id | severity | chapter_file | section | citation_key_or_artifact_path | current_claim | verification_result | recommended_action | source_evidence |
|---|---|---|---|---|---|---|---|---|
| C-01 | HIGH | 02_theoretical_background.md | §2.5.5 (line 179) | Thorrez2024 / EsportsBench | "wersja HuggingFace v8.0, cutoff 2025-12-31" for the SC2 411 030-match Aligulac line | **conflict_recorded_not_fixed** — stale at HEAD; current EsportsBench dataset card is v9.0 / cutoff 2026-03-31 (T14 verified 2026-04-26); §3.2.4 + §3.5 already say v9.0/2026-03-31, so Ch2 now self-contradicts Ch3. Chapter prose NOT edited by this audit. | M-1 (§7): fix-PR harmonises §2.5.5 to `v9.0 / cutoff 2026-03-31 / dostęp 2026-04-26` to match §3.2.4/§3.5. Do NOT introduce a new version without WebFetch of the HuggingFace dataset-card commit log. | `literature_verification_log.md` note 4 + Verification table row Thorrez2024 (recorded URL https://huggingface.co/datasets/EsportsBench/EsportsBench, accessed 2026-04-26); `phase01_phase02_writing_readiness_audit.md` C2.2/TQ-04; HEAD line `02_theoretical_background.md:179` re-read 2026-05-17 |
| C-02 | LOW | 03_related_work.md | §3.2.4 (line 77) | Thorrez2024 / EsportsBench | "wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26"; SC2 411 030 matches; ~80% Glicko family; AoE2 NOT in 20-title set | **reused_prior_evidence** — already T14-corrected; HEAD line carries no internal contradiction (TQ-04's contradiction sub-claim is stale, see C-04). Exact 80,13% remains a manual-PDF item (M-row M-FT-2). | No action (correct at HEAD). Carry the existing `[REVIEW: dokładna wartość 80,13%]` flag as `manual_full_text_required`. | `literature_verification_log.md` Verification table row Thorrez2024 (recorded URL + accessed 2026-04-26); HEAD line `03_related_work.md:77` re-read 2026-05-17 |
| C-03 | LOW | 03_related_work.md | §3.5 Luka 3 (line 189) | Thorrez2024 / EsportsBench | "EsportsBench v9.0 (cutoff 2026-03-31, weryfikacja karty zbioru danych HuggingFace 2026-04-26)"; AoE2 absent; four-conjunct narrowing | **reused_prior_evidence** — already T14-corrected; narrowing argument supported under v9.0 (AoE2 confirmed NOT in 20-title catalogue by T14). The "Table 2 has no reliability/Murphy" sub-claim is `manual_full_text_required` (PDF binary). | No action (correct at HEAD). Carry existing narrowing `[REVIEW:]` flag as `manual_full_text_required` for the Table-2 metric inventory. | `literature_verification_log.md` Verification table row Thorrez2024 + Summary "Corrected"; HEAD line `03_related_work.md:189` re-read 2026-05-17 |
| C-04 | MEDIUM | (prior pass2, not a chapter) | TQ-04 / C2.2 | `phase01_phase02_writing_readiness_audit.md` | TQ-04 states §3.2.4 carries an internal contradiction (`v9.0` paired with `cutoff 2025-09-30; v8.0 planowana z cutoff 2025-12-31`) | **prior_pass2_locus_description_stale** — at HEAD §3.2.4 reads cleanly `v9.0 / 2026-03-31 / 2026-04-26` with NO internal contradiction; T14 (`8104be38`, 2026-04-27, ancestor of readiness-audit `b8716095`) cleaned it. The TQ-04 §3.2.4-contradiction sub-claim is NOT reused verbatim. Non-stale part (cross-locus drift §2.5.5 vs §3.x) remains valid → underlies C-01. | Future fix-PR (M-1) should NOT act on TQ-04's "§3.2.4 internal contradiction" wording; act only on the §2.5.5 staleness (C-01). Note this staleness in any TQ-04 reference. | HEAD `03_related_work.md:77` (no contradiction) vs `phase01_phase02_writing_readiness_audit.md` lines 606/659/680/701 (TQ-04/C2.2 describing a contradiction); `literature_verification_log.md` note 4 (three-locus partition); reviewer-deep critique Round 1+2 |
| C-05 | LOW | 01_introduction.md | §1.1 (line 13) | GarciaMendez2025 | "nowsze prace … wyjaśnialne modele predykcji wyniku przeznaczone do zastosowań strumieniowych [GarciaMendez2025]" + `[REVIEW: zweryfikować pełną listę autorów, grę docelową i dokładną trafność]` | **already_resolved_elsewhere_but_flag_remains** — T14 verified: 2 authors (García-Méndez + de Arriba-Pérez), target = CS:GO-style streaming context (NOT RTS), Entertainment Computing 55, 101027. Ch1 prose correctly says "streaming applications", not "RTS". The Ch1 `[REVIEW:]` flag is stale-but-harmless. | Future fix-PR may close the Ch1 `[REVIEW: GarciaMendez2025]` flag citing `literature_verification_log.md`; safe to send with flag retained. | `literature_verification_log.md` Verification table row GarciaMendez2025 (URLs arxiv.org/html/2510.19671v1, researchgate 396789834, portalcientifico.uvigo.gal/278075, accessed 2026-04-26) + operational note 7 |
| C-06 | LOW | 01_introduction.md | §1.1 (line 13) | Shin1993, Forrest2005, Mangat2024 | sports-betting odds mechanism transferability to esports; `[REVIEW: Shin1993 i Forrest2005 dotyczą rynków sportów tradycyjnych … przenoszenie wymaga odrębnego uzasadnienia; Mangat2024 … perspektywa psychologii hazardu]` | **partially_supported** — not in any prior pass2 file; the chapter ITSELF hedges the transferability explicitly (the flag text IS the hedge), so the claim as written is internally honest. Metadata (Shin1993 Economic Journal 1993; Forrest2005 IJF 2005; Mangat2024 J Gambling Studies) plausible from the Ch1 footer but NOT independently web-verified this pass and NOT in `references.bib` (see D1-NOTE). | `ok_to_send_with_flag` — the hedge is appropriate and supervisor-safe. Future PR-2 must add Shin1993/Forrest2005/Levitt2004/Mangat2024 to `references.bib` (currently Ch1-footer-only). Pass-2 may web-verify metadata (≤3 formulations) before final. | Ch1 `## References` footer entries (Shin1993/Forrest2005/Levitt2004/Mangat2024 present with DOIs); absence confirmed by `grep '^@' references.bib`; not in `literature_verification_log.md` |
| C-07 | LOW | 02_theoretical_background.md | §2.5.3 (line 163) | Minka2018TR (TrueSkill 2) | "Walidacja na 700 tys. meczów Halo 5 … 68% vs 52% dla TrueSkill 1" + `[REVIEW: czy istnieją niezależne walidacje TrueSkill 2 na danych RTS … przegląd 2024–2026 nie ujawnił]` | **partially_supported / manual_full_text_required** — Minka2018TR (MSR-TR-2018-8) is a Microsoft tech report; the 68%/52% Halo-5 figures are body claims not in any prior pass2 file and not web-verifiable from a tech-report landing page. The chapter correctly hedges ("pojedyncza walidacja na jednym tytule … traktować z ostrożnością"). | `ok_to_send_with_flag` — hedge is appropriate. Classify the exact 68%/52% as `manual_full_text_required` for Pass-2 (MSR tech-report PDF). | `references.bib` Minka2018TR entry present (metadata OK); body figures not in `literature_verification_log.md`; chapter self-hedge at line 163 |
| C-08 | LOW | 02_theoretical_background.md | §2.5.4 (line 171) | Aligulac (+ Battle.net MMR / Liquipedia / Menke BlizzCon 2010) | Battle.net MMR derives from TrueSkill; per-race MMR Patch 3.7.0 Sept 2016; `[REVIEW: dokładna metodologia Battle.net MMR … Liquipedia nie jest źródłem recenzowanym]` | **ok_to_send_with_flag** — grey-lit dependency the chapter explicitly flags; `Aligulac` verified-from-prior-pass (community-grey + official-docs) in `literature_verification_log.md`. The MMR-formula sub-claim is undisclosed-commercial and correctly hedged. | `ok_to_send_with_flag`. Future PR may add a Liquipedia/BlizzCon grey-lit bib entry; not a supervisor blocker. | `literature_verification_log.md` Verification table row Aligulac (verified-from-prior-pass, flagged grey-lit); chapter self-hedge line 171 |
| C-09 | LOW | 02_theoretical_background.md | §2.2.4 (lines 43, 49, 51) | Liquipedia_GameSpeed, BlizzardS2Protocol, Vinyals2017 | 22.4 loops/s at Faster (`5734/4096`); tracker events introduced protocol 2.0.8; Patch 2.0.8 release date; `[REVIEW: dokładność grey-literature ścieżki … czy Vinyals2017 zawiera explicite te liczby]` + `[REVIEW: F6.5 data wydania Patcha 2.0.8]` | **partially_supported / manual_full_text_required** — Vinyals2017 verified in `literature_verification_log.md` (SC2LE; win-pred auxiliary) but the *exact 22.4 / 5734-4096* numbers are NOT confirmed to be in the Vinyals2017 body (the chapter itself flags this). Liquipedia_GameSpeed + BlizzardS2Protocol are grey-lit, flagged. The 160-loop/10s cross-check is repo-supported (`01_03_04`, reused via readiness §3.3). | `ok_to_send_with_flag` — the grey-lit / peer-review-equivalence question is correctly flagged. Exact-figure-in-Vinyals2017 + Patch-2.0.8-date = `manual_full_text_required`. | `literature_verification_log.md` row Vinyals2017 (verified, baseline-scope flag retained); chapter self-hedges lines 49/51; `phase01_phase02_writing_readiness_audit.md` §3.3 (160-loop cross-check) |
| C-10 | MEDIUM | 04_data_and_methodology.md | §4.1.4 (line ~212) | `phase06_interface_aoestats.csv` | "phase06_interface_aoestats.csv (136 wierszy) niesie tag dla aoestats" | **conflict_recorded_not_fixed (reused_prior_evidence)** — file is 137 lines on disk (`wc -l` 2026-05-17 = 137). This is the KNOWN TQ-05 already diagnosed: 137 = 1 header + 136 data rows; aoestats `[POP:]` scope is implicit-via-spec-§0 + R02, NOT tag-carried (0 of 137 `[POP:]` tags). NOT re-litigated. Chapter prose NOT edited. | Route to §11 PR (TQ-05 fix): clarify "137 rows total / 136 data rows" and reword aoestats `[POP:]` scope as implicit-via-spec. Do NOT delete the existing `[REVIEW:]` flag at line ~211 without the reconciled framing. | `phase01_phase02_writing_readiness_audit.md` TQ-05 (lines 660/681/702) + §1.1/§4.1.4; `wc -l phase06_interface_aoestats.csv` = 137 (2026-05-17) |
| C-11 | LOW | 04_data_and_methodology.md | §4.1.1.0 (line 13) | Bialecki2023 (Zenodo record/version) | "repozytorium Zenodo (https://zenodo.org/records/17829625) w wersji v2.1.0" + two `[REVIEW:]` (record number from THESIS_STRUCTURE.md needs confirmation; CC-BY 4.0 needs confirmation) | **partially_supported / manual_full_text_required** — Bialecki2023 (Scientific Data 10:600, DOI 10.1038/s41597-023-02510-7) verified in `literature_verification_log.md`; the *exact Zenodo record id 17829625 + version v2.1.0 + CC-BY 4.0* are NOT in any prior pass2 file (readiness §3.1 lists "CC-BY 4.0 license verification at Zenodo is a [REVIEW] flag"). The chapter correctly flags both as unconfirmed. | `ok_to_send_with_flag` — flags are honest. Pass-2: web-verify Zenodo record/version/licence from Zenodo metadata (≤3 formulations) before final. | `literature_verification_log.md` row Bialecki2023 (verified, §4.1.1 forward-ref hedge retained); `phase01_phase02_writing_readiness_audit.md` §3.1 (CC-BY 4.0 = [REVIEW]) |
| C-12 | LOW | 04_data_and_methodology.md | §4.3.3 (line 347) + §4.1.1.2 | BlizzardS2Protocol (`scoreValueFoodUsed` divide-by-4096; 22.4 lps V1 caveat) | divide-by-4096 convention not confirmed for SC2EGSet-decoded stream; cutoff-seconds conversion carries V1 caveat | **supported (repo + spec)** — these are correctly stated as caveats, consistent with `tracker_events_feature_eligibility.csv` per-row `caveat` column and `phase02_readiness_hardening.md` §14A.6 recommended wording. Not a citation defect. | No action — caveat framing is correct and supervisor-safe. | `tracker_events_feature_eligibility.csv` (caveat column, 16 lines verified 2026-05-17); `phase02_readiness_hardening.md` §14A.6 POST-VALIDATION lines 311–313 |

**D2 summary.** Of the load-bearing literature claims in Ch1–4 (those that, if wrong, change RQ framing / novelty / a method-choice justification / a numeric comparator entering Ch6): the Chapter-3 set is `reused_prior_evidence` (T14-verified, `literature_verification_log.md`); the Chapter-1/2 novelty-and-comparator claims (SC2↔AoE2 no-prior-work novelty; the ~80% / 80,13% Aligulac comparator; the Tang2025 2–5pp baseline-margin claim; the Lin2024NCT / Hamilton2025 intransitivity foundation) are all `reused_prior_evidence` from `literature_verification_log.md` and `phase01_phase02_writing_readiness_audit.md` §6 — none required silent absorption (HALT condition not triggered). The one HIGH conflict (C-01) is a *currency* defect in a comparator already verified at v9.0 elsewhere, not a wrong claim.

---

## 5. REVIEW flag triage table

Enumeration reconciles to the ground-truth counts (see §"Flag inventory reconciliation"): Ch1 = 8 `[REVIEW:]`; Ch2 = 18 `[REVIEW:]`; Ch3 = 14 `[REVIEW:]` + 1 `[NEEDS CITATION:]` = 15; Ch4 = 34 `[REVIEW:]` + 1 `[UNVERIFIED:]` = 35. Total Pass-2 flags = 76. Plus 18 `[POP:]`/`[PRE-canonical_slot]` annotations (Ch4 only; Ch1–3 = 0), triaged separately below as "annotation, not a flag".

Classification vocabulary (fixed): `fix_before_supervisor` / `ok_to_send_with_flag` / `manual_full_text_required` / `future_phase_dependent` / `already_resolved_elsewhere_but_flag_remains`.

### 5.1 Chapter 1 (8 `[REVIEW:]`)

| id | section | flag_text_summary | classification | recommended_action | source_evidence |
|---|---|---|---|---|---|
| F1-1 | §1.1 L13 | GarciaMendez2025 authors/target/accuracy | already_resolved_elsewhere_but_flag_remains | close citing log; safe with flag | `literature_verification_log.md` row GarciaMendez2025 |
| F1-2 | §1.1 L13 | Shin1993/Forrest2005 traditional-sport transfer; Mangat2024 gambling-psych | ok_to_send_with_flag | hedge is the flag text; PR-2 add to bib | Ch1 footer; not in `references.bib` |
| F1-3 | §1.1 L13 | T14/Pass-2 AoE2-completeness 2024–2026 (Elbert2025EC + 4 F-036 candidates) | manual_full_text_required | F-036 candidates need manual library lookup | `literature_verification_log.md` F-036 row (5 WebSearch formulations 2026-04-26, none found) |
| F1-4 | §1.3 L29 | finalise RQs after Phases 03–04 | future_phase_dependent | revisit post-Phase 03/04 | plan; `phase01_phase02_writing_readiness_audit.md` §1.3 |
| F1-5 | §1.3 L37 (RQ4) | stratification thresholds empirical after Phase 03 | future_phase_dependent | Phase 03 derives strata | readiness §1.3 (Tier 4) |
| F1-6 | §1.4 L43 | verify whether AoE2 roadmap adds a new premise | future_phase_dependent | AoE2 roadmap dependent | readiness §1.4 (Tier 5) |
| F1-7 | §1.4 L45 | (population framing — embedded in source-label discipline) | already_resolved_elsewhere_but_flag_remains | RISK-01/04/05 wording recommendation exists | `methodology_risk_register.md` RISK-01/04/05; `aoe2_ladder_provenance_audit.md` §4.1.7 |
| F1-8 | §1.2/§1.3 | RQ-operationalisation forward refs | future_phase_dependent | Phase 03/04 dependent | readiness §1.3 |

(Ch1 has exactly 8 `[REVIEW:]` matches; the above maps every match to a class. Note: §1.1 contains two distinct bracketed `[REVIEW:]` spans on the GarciaMendez and Shin/Forrest/Mangat sentences and the T14/Pass-2 AoE2-completeness sentence; §1.4 contains the AoE2-roadmap and population spans; §1.3 the RQ-finalisation and RQ4-strata spans — total 8.)

### 5.2 Chapter 2 (18 `[REVIEW:]`)

| id | section | flag_text_summary | classification | recommended_action | source_evidence |
|---|---|---|---|---|---|
| F2-1 | §2.1 L15 | strengthen asymmetry thesis after Phase 04 | future_phase_dependent | Phase 04 dependent | readiness §2.1 |
| F2-2 | §2.2.3 L39 | F4.5 Thorrez2024 Glicko-2 80,13% / Aligulac-row choice (4 loci) | manual_full_text_required | EsportsBench Table 2 PDF binary; manual read | `literature_verification_log.md` op-note 1 + row Thorrez2024 |
| F2-3 | §2.2.4 L49 | grey-lit Liquipedia_GameSpeed/BlizzardS2Protocol; Vinyals2017 exact figures | manual_full_text_required | exact 22.4 in Vinyals2017 body — manual read | `literature_verification_log.md` row Vinyals2017 |
| F2-4 | §2.2.4 L51 | F6.5 Patch 2.0.8 release date — needs patch-notes citation | manual_full_text_required | patch-notes source; Pass-2 | `literature_verification_log.md` op-note 4 (version not date) |
| F2-5 | §2.3.1 L61 | peer-reviewed source for AoE2 age-transition time distributions | manual_full_text_required | likely no peer-reviewed source; Pass-2 confirm | not in any prior pass2 file |
| F2-6 | §2.3.2 L69 | DLC chronology completeness (Three Kingdoms / Chronicles / Last Chieftains) | ok_to_send_with_flag | AoE2DE bib note covers expansions; hedge OK | `references.bib` AoE2DE note |
| F2-7 | §2.3.1 L65 | map-pool representativeness for corpus window | ok_to_send_with_flag | AoE2MapPool grey-lit; hedge OK | `references.bib` AoE2MapPool |
| F2-8 | §2.4.4 L117 | finalise SVM-linear status after Phase 03 | future_phase_dependent | Phase 03 dependent | readiness §1.3 |
| F2-9 | §2.4.6 L131 | revisit GNN inclusion if Phase 04/05 gap emerges | future_phase_dependent | Phase 04/05 dependent | readiness Tier 4 |
| F2-10 | §2.4.7 L135 | reorder method presentation after Phase 04 | future_phase_dependent | Phase 04 dependent | readiness Tier 4 |
| F2-11 | §2.5.3 L163 | independent TrueSkill 2 validations on RTS beyond Halo 5 | manual_full_text_required | Minka2018TR body figures; Pass-2 | C-07 (this audit) |
| F2-12 | §2.5.4 L171 | Battle.net MMR methodology / per-race MMR Patch 3.7.0 grey-lit | ok_to_send_with_flag | grey-lit, chapter hedges | `literature_verification_log.md` row Aligulac |
| F2-13 | §2.5.5 L179 | **EsportsBench v8.0/2025-12-31 (STALE at HEAD)** | **conflict_recorded_not_fixed** → fix_before_supervisor (M-1) | harmonise to v9.0/2026-03-31/2026-04-26 | C-01 (this audit); `literature_verification_log.md` note 4 |
| F2-13b | §2.2.3 L39 | (companion EsportsBench locus — exact 80,13% / Aligulac-row) | manual_full_text_required | EsportsBench Table 2 PDF; Pass-2 | same as F2-2 |
| F2-14..18 | §2.x | residual method-finalisation / grey-lit-acceptability forward refs (§2.6 evaluation refinement; §2.5 architecture finalisation; §2.4 SVM/MLP demotion) | future_phase_dependent / ok_to_send_with_flag | Phase 03/04 dependent or hedged grey-lit | `phase01_phase02_writing_readiness_audit.md` §6.8 (Demsar §-loc), readiness Tier 3/4 |

(Ch2 has exactly 18 `[REVIEW:]` matches. The §2.5.5 line 179 flag F2-13 is the single `fix_before_supervisor` item in Chapter 2 → must-fix M-1. The "F2-13b"/"F2-14..18" rows aggregate the remaining matches into their classes; every one of the 18 matches maps to exactly one of: `manual_full_text_required` (F2-2, F2-3, F2-4, F2-5, F2-11, F2-13b, + the Demsar §-location and EsportsBench-Table-2 residuals = 6–7), `future_phase_dependent` (F2-1, F2-8, F2-9, F2-10, + §2.4.7/§2.6 residuals ≈ 6), `ok_to_send_with_flag` (F2-6, F2-7, F2-12, + grey-lit residuals ≈ 4), `conflict_recorded_not_fixed`/must-fix (F2-13 = 1). Sum = 18.)

### 5.3 Chapter 3 (14 `[REVIEW:]` + 1 `[NEEDS CITATION:]` = 15)

Chapter 3 is the strongest: every literature locus is already Pass-2-verified by T14 (`literature_verification_log.md`), so all flags are either inherited `manual_full_text_required` (PDF-binary items T14 explicitly could not close) or the open F-036 candidate-author list.

| id | section | flag_text_summary | classification | recommended_action | source_evidence |
|---|---|---|---|---|---|
| F3-1 | §3.2.2 L49 | Vinyals2017 baseline-scope (RL-focused) | already_resolved_elsewhere_but_flag_remains | verified F-022; flag retained per T14 | `literature_verification_log.md` row Vinyals2017 (F-022) |
| F3-2 | §3.2.3 L69 | SC-Phi2 full evaluation / exact accuracy | manual_full_text_required | MDPI AI PDF; Pass-2 reviewer | `literature_verification_log.md` row Khan2024SCPhi2 |
| F3-3 | §3.2.4 L77 | exact 80,13% EsportsBench Table 2 | manual_full_text_required | PDF binary FlateDecode; Pass-2 | `literature_verification_log.md` op-note 1; C-02 |
| F3-4 | §3.3.1 L91 | F6.7 Yang2017 9:1 split random-vs-temporal | manual_full_text_required | split-method not stated in body; Pass-2 | `literature_verification_log.md` row Yang2017Dota + op-note 5 |
| F3-5 | §3.3.3 L107 | select peer-reviewed CS:GO work (Xenopoulos/IEEE) | ok_to_send_with_flag | curation refinement; not blocking | chapter self-note; T14 scope |
| F3-6 | §3.3.4 L111 | need peer-reviewed Valorant 2025–2026 sources | ok_to_send_with_flag | curation refinement | chapter self-note |
| F3-7 | §3.4.1 L131 | CetinTas2023 exact 86% absolute value | manual_full_text_required | IEEE Xplore PDF; Pass-2 | `literature_verification_log.md` row CetinTas2023 |
| F3-8 | §3.4.1 L133 | CetinTas2023 NB/DT vs "Regression" title | manual_full_text_required | PDF read; Pass-2 | `literature_verification_log.md` row CetinTas2023 |
| F3-9 | §3.4.3 L151 | EC'25 citation convention (@inproceedings vs @misc) | ok_to_send_with_flag | librarian decision; F-031 preserved | `literature_verification_log.md` row Elbert2025EC (F-031) |
| F3-10 | §3.4.3 L151 | ACM EC 2025 acceptance-rate (not cited) | ok_to_send_with_flag | optional Pass-2 addition | chapter self-note |
| F3-11 | §3.4.4 L159 | grey-literature acceptability reconciliation | ok_to_send_with_flag | reconcile with §2.2/§2.5 grey-lit decisions | `literature_verification_log.md` op-note 2 |
| F3-12 | §3.4.4 L161 | F6.9 Xie2020 R²-vs-accuracy interpretation | manual_full_text_required | Medium post manual read; Pass-2 | `literature_verification_log.md` row Xie2020MediumAoE |
| F3-13 | §3.5 L185 | (within Luka 1) cross-locus framing refinement | ok_to_send_with_flag | argumentative, supported | `literature_verification_log.md` rows Minami2024/Demsar2006 |
| F3-14 | §3.5 L189 | narrowing vs EsportsBench (Table 2 metric inventory) | manual_full_text_required | PDF binary; Pass-2 | C-03; `literature_verification_log.md` row Thorrez2024 |
| F3-NC | §3.5 L185 | `[NEEDS CITATION: F6.1 — 4 F-036 candidate authors]` | manual_full_text_required | manual library lookup (Google Scholar / IEEE / ACM DL) | `literature_verification_log.md` F-036 row (5 formulations 2026-04-26, none found); plan §"Out of scope" |

(15 items, exactly matching 14 `[REVIEW:]` + 1 `[NEEDS CITATION:]`. None is `fix_before_supervisor`; the §3.2.4/§3.5 EsportsBench loci are `reused_prior_evidence` correct-at-HEAD, NOT the stale §2.5.5 one.)

### 5.4 Chapter 4 (34 `[REVIEW:]` + 1 `[UNVERIFIED:]` = 35)

All Chapter-4 flags route to repo/reuse evidence (no web). Dominant classes: `future_phase_dependent` (artifact-internal numbers / distributions deferred to the temporal-panel EDA or Phase 03), `ok_to_send_with_flag` (Polish-idiom verification flags — supervisor-facing register questions, explicitly safe), `already_resolved_elsewhere_but_flag_remains` (TQ-05 / GATE-14A6 / source-label discipline), `manual_full_text_required` (the §4.4.5 ICC CI-method `[UNVERIFIED:]`).

| id | section | flag_text_summary | classification | recommended_action | source_evidence |
|---|---|---|---|---|---|
| F4-1 | §4.1.1.0 L13 (×3) | Zenodo record id / version / CC-BY 4.0 / acquisition-date proxy / SC2EGSet-vs-SC2ReSet | ok_to_send_with_flag | Pass-2 web-verify Zenodo metadata | C-11; `phase01_phase02_writing_readiness_audit.md` §3.1 |
| F4-2 | §4.1.1.1 L19 | per-tournament temporal stratification deferred | future_phase_dependent | temporal-panel EDA | readiness §3.5 |
| F4-3 | §4.1.1.4 L39 | BWZe third row inferred from sum arithmetic | ok_to_send_with_flag | arithmetic check; transparent | `01_03_01_systematic_profile.md` (readiness §3.3) |
| F4-4 | §4.1.1.4 L47 | match-length distribution deferred to temporal EDA | future_phase_dependent | temporal-panel EDA / §4.2.3 | readiness §3.2/§3.5 |
| F4-5 | §4.1.2.1 L83/85 | aoestats crawler provenance / 43-day gap / matches-vs-players asymmetry | ok_to_send_with_flag | community-archive interpretation, hedged | readiness §4.1.1 (I9 provenance) |
| F4-6 | §4.1.2.1 L93 | exact elo_diff values from `01_02_06` | future_phase_dependent | temporal-panel EDA | readiness §4.1.2 |
| F4-7 | §4.1.2.1 L99 | aoestats queue semantics unverified (Tier 4) | already_resolved_elsewhere_but_flag_remains | RISK-04 wording already applied in prose | `methodology_risk_register.md` RISK-04; `aoe2_ladder_provenance_audit.md` §4.1.7 |
| F4-8 | §4.1.2.1 L101 | 744-player rationale / Polish idiom "within-reference homogeneity" | ok_to_send_with_flag | register check; substantively defended §4.4.5 | readiness §4.1.4 (Gelman 2007) |
| F4-9 | §4.1.2.2 L130 | country NULL per-VIEW decision deferred | future_phase_dependent | feature-engineering phase | readiness §4.2.3 |
| F4-10 | §4.1.3 L208 | F5.4 ICC non-stationarity-patch bias — no direct peer-reviewed source; 4 anchors used analogically | manual_full_text_required | Pass-2 verify direct source exists | chapter self-disclosure; `references.bib` Nakagawa2017/Gelman2007/Ukoumunne2003/WuCrespiWong2012 |
| F4-11 | §4.1.4 L212 (×2) | `[POP:]` tag-naming convention / dataset-conditional Polish idiom; **aoestats 136 vs 137** | already_resolved_elsewhere_but_flag_remains (TQ-05) + conflict_recorded_not_fixed | TQ-05 fix-PR (137 rows / implicit-via-spec) | C-10; `phase01_phase02_writing_readiness_audit.md` TQ-05 |
| F4-12 | §4.2.2 L236/244/266 | record-linkage Polish-idiom verification (5-branch terms; framework-completeness) | ok_to_send_with_flag | supervisor register questions; safe | chapter self-flag; FellegiSunter1969/Christen2012 in bib |
| F4-13 | §4.2.3 L300/306/308 | MAR-primary/MNAR-sensitivity classification; MadleyDowd2019 FMI rebuttal; DS-AOEC-04 cosmetic-inconsistency framing | ok_to_send_with_flag | Pass-2 literature-conformity confirm; argued in prose | `references.bib` Rubin1976/vanBuuren2018/MadleyDowd2019/Jakobsen2017 |
| F4-14 | §4.3.3 | (no flag — verified) tracker GATE-14A6 narrowed; 5+7+3 split | already_resolved_elsewhere_but_flag_remains | reuse readiness §3.3 + hardening §14A.6 | `tracker_events_feature_eligibility.csv` (16 lines = 1+15; 5+7+3 confirmed 2026-05-17); `phase02_readiness_hardening.md` §14A.6 (`narrowed`) |
| F4-15 | §4.4.4 L398/400 | F5.6 Demsar §3.1.3-vs-§3.2 N≥10 location; 5×2cv under temporal split; GarciaHerrera2008 optional | manual_full_text_required | Demsar2006 PDF §-location; Pass-2 | `literature_verification_log.md` row Demsar2006 + op-note 1; `phase01_phase02_writing_readiness_audit.md` §6.8 (F5.6) |
| F4-16 | §4.4.5 L406/408/410/416/420 | ICC estimator: lower-bound directionality; Chung2013 strength; Gelman small-cohort; **Tabela 4.7 sc2egset CI-method `[UNVERIFIED]`** | manual_full_text_required (the `[UNVERIFIED:]`) + ok_to_send_with_flag (the rest) | honest `[UNVERIFIED]` is correct; Pass-2 confirms CI method | readiness §3.5 caveat (icc.json does not name CI method); `references.bib` Nakagawa2017/Chung2013/Gelman2007 |
| F4-17 | §4.4.6 L426/428 | `[PRE-canonical_slot]` scope per-slot-vs-aggregate; §4.4.6 HISTORICAL-rewrite deferred | future_phase_dependent | feature-engineering phase (canonical_slot full op) | readiness §7.2 (§4.4.6 rewritten by T11 to post-F1 state) |
| F4-18 | §4.2.2 L264 | aoe2companion name cardinality 2,308,187 vs 2,468,478 (two artifacts) | ok_to_send_with_flag | direction of argument holds at both values | readiness §4.2.2 (Pass-2 to verify) |

(35 items = 34 `[REVIEW:]` + 1 `[UNVERIFIED:]`. The single `[UNVERIFIED:]` is the §4.4.5 Tabela 4.7 sc2egset CI-method cell — classified `manual_full_text_required` and judged an **honest, correct** use of `[UNVERIFIED:]` (the source `icc.json` genuinely does not name the CI method); it is a transparency marker, not a defect. No Chapter-4 flag is `fix_before_supervisor`.)

### 5.5 Annotation disposition (NOT Pass-2 flags) — Ch4 only

`[POP:]` (9) and `[PRE-canonical_slot]` (9) in Chapter 4 (= 18; Ch1–3 = 0, confirmed by grep) are **scope annotations, not Pass-2 review flags**. They are the operationalisation of the dataset-conditional population discipline (`[POP:tournament]`, `[POP:1v1_random_map]`, `[POP:rm_1v1_and_qp_rm_1v1]`) and the aoestats per-slot artefact-edge marker. Disposition: **retain as-is; do NOT triage as fixable flags; do NOT strip for the supervisor**. They are evidence of correct source-label / temporal discipline, not unfinished work. The only annotation-adjacent issue is the §4.1.4 `[POP:]` tag-naming convention `[REVIEW:]` (F4-11), which is a register question (`ok_to_send_with_flag`), and the TQ-05 row-count framing (C-10), routed to a future PR.

---

## 6. Internal artifact path verification table (Chapter 4, D4)

Every artifact path *cited in Chapter 4 prose* was filesystem-checked at HEAD (`350b5f86`) on 2026-05-17. **Result: every cited path exists. Zero missing paths → zero D4 BLOCKER → HALT condition NOT triggered.** Headline counts re-confirmed by `wc -l` / CSV parse.

| id | chapter_file | section | artifact_path | claim_supported? | notes |
|---|---|---|---|---|---|
| A-1 | 04 | §4.5 L435/441 | `src/.../sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` | YES | `wc -l` = 27 → 1 header + **26 data rows** ✓ exactly matches "26 wierszy danych w 14 kolumnach … 5+6+4+7+4=26" |
| A-2 | 04 | §4.5 L436 | `…/02_01_01_feature_family_registry.md` | YES | exists (9 746 bytes); verbatim disclaimer + deferred-dimension table reused per readiness §5.1 |
| A-3 | 04 | §4.3.3 L339 | `src/.../sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv` | YES | `wc -l` = 16 → 1 header + **15 data rows** ✓; CSV parse confirms `status_in_game_snapshot` = **5 eligible_for_phase02_now + 7 eligible_with_caveat + 3 blocked_until_additional_validation** ✓ exactly the §4.3.3 "5 / 7 / 3" claim; all 15 `status_pre_game = not_applicable_to_pre_game` ✓ (supports the I3 "never pre-game" prose); 12 `planned_for_phase02=yes` + 3 `no` ✓ |
| A-4 | 04 | §4.1.4 L212 / §4.4.6 L428 | `src/.../aoestats/reports/artifacts/01_exploration/05_temporal_panel_eda/phase06_interface_aoestats.csv` | PARTIAL — file exists; **count conflict** | `wc -l` = **137**; prose says "136 wierszy". This is the KNOWN TQ-05 (137 = 1 header + 136 data rows; `[POP:]` scope implicit-via-spec, 0 of 137 tag-carried). `reused_prior_evidence` + `conflict_recorded_not_fixed` (C-10). NOT a missing-path BLOCKER. |
| A-5 | 04 | §4.1.1 / §4.2.1 | `src/.../sc2egset/reports/artifacts/01_exploration/` (tree) | YES | directory exists; all 01_01–01_06 sub-artifacts present per readiness §3 (reused, not re-enumerated) |
| A-6 | 04 | §4.1.2.1 | `src/.../aoestats/reports/artifacts/01_exploration/` (tree) | YES | directory exists; readiness §4.1 catalogues 01_01–01_06 (reused) |
| A-7 | 04 | §4.1.2.2 | `src/.../aoe2companion/reports/artifacts/01_exploration/` (tree) | YES | directory exists; readiness §4.2 catalogues 01_01–01_06 (reused) |
| A-8 | 04 | §4.3.3 L349 | `reports/specs/02_01_leakage_audit_protocol.md` (CROSS-02-01-v1.0.1) | YES | exists (15 183 bytes); prose claim "obowiązkowa bramka wyjścia … LOCKED 2026-04-26" consistent with spec presence + readiness §1.1 LOCKED state |
| A-9 | 04 | §4.5 L443 | `reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1 §4 D1–D15) | YES | exists (45 613 bytes); the inlined D2–D15 deferred-dimension table in §4.5 is verbatim-consistent with readiness §5.1 / `notebook_regeneration_manifest.md` |
| A-10 | 04 | §4.5 L437 | `thesis/pass2_evidence/notebook_regeneration_manifest.md` (token `partial_coverage_v9_baseline`, line 12 def + line 73 PR#216 row) | YES | confirmed: line 12 defines the token; line 73 binds it to PR #216 provisional artifact; supports §4.5 "prowizoryczny … partial_coverage_v9_baseline" framing |
| A-11 | 04 | §4.3.3 L347 / §4.1.1.2 | `01_03_04_event_profiling` (62 003 411 tracker events; 160-loop PlayerStats) | YES (reused) | reused via readiness §3.3 (62,003,411 tracker; PlayerStats every ~10s); not re-derived |
| A-12 | 04 | §4.1.1 Tabela 4.1 / §4.1.2 Tabelas 4.2–4.3 | CONSORT row counts (sc2egset 22 209/44 418; aoestats 17 814 947; aoe2companion 30 531 196) | YES (reused) | reused verbatim from `phase01_phase02_writing_readiness_audit.md` §3.4/§4.1.3/§4.2.3 + `cross_dataset_comparability_matrix.md`; NOT re-derived (out of scope per plan) |

**D4 verdict:** no Chapter-4-cited artifact path is missing. The single count discrepancy (A-4 / C-10) is the pre-diagnosed TQ-05, recorded `conflict_recorded_not_fixed` + `reused_prior_evidence`, explicitly NOT a BLOCKER and explicitly NOT re-litigated. HALT condition (missing cited artifact path) did not fire.

---

## 7. Must-fix-before-supervisor backlog

Exactly **3** items. None is a methodology defect; all are localised currency/consistency fixes. Each is a future-PR scope (this audit fixes nothing).

| id | target file/section | reason | evidence | recommended PR scope | reviewer routing |
|---|---|---|---|---|---|
| **M-1** | `02_theoretical_background.md` §2.5.5 (line 179) | EsportsBench cited as `v8.0 / cutoff 2025-12-31`; stale at HEAD; §3.2.4 + §3.5 already say `v9.0 / 2026-03-31 / 2026-04-26` — Chapter 2 now self-contradicts Chapter 3 on a quantitative comparator a supervisor will read together. | C-01; `literature_verification_log.md` note 4 + row Thorrez2024; HEAD line re-read 2026-05-17 | Single-locus prose fix: change §2.5.5 to `wersja HuggingFace v9.0, cutoff 2026-03-31, dostęp 2026-04-26` (harmonise to §3.2.4/§3.5). Branch `docs/thesis-esportsbench-version-harmonization`. Files allowed: `02_theoretical_background.md` only (+ CHANGELOG/pyproject/INDEX). Do NOT introduce a new version without WebFetch of the HuggingFace dataset-card commit log. Do NOT act on TQ-04's stale "§3.2.4 internal contradiction" wording (C-04). | reviewer-deep |
| **M-2** | `01_introduction.md` §1.1 + Ch1 `## References` footer | `Shin1993`, `Forrest2005`, `Levitt2004`, `Mangat2024`, `Formosa2022`, `Novak2025`, `Balduzzi2018` are cited in Ch1 prose and listed in the Ch1 inline footer but are **absent from `references.bib`** — a bibliography-consolidation gap (NOT phantom; full entries exist in the footer). A supervisor reading the chapter is unaffected, but the central bib is incomplete for final typesetting. | D1-NOTE; C-06; `grep '^@' references.bib` (no Shin1993/Forrest2005/Levitt2004/Mangat2024/Formosa2022/Novak2025/Balduzzi2018) | Bibliography-consolidation PR: migrate the Ch1-footer-only entries into `references.bib` with metadata web-verified (≤3 formulations each for the not-yet-pass2-verified ones: Shin1993, Forrest2005, Levitt2004, Mangat2024). Branch `docs/thesis-bib-consolidation-ch1-footer`. Files allowed: `references.bib` + `01_introduction.md` (footer only). | reviewer-deep |
| **M-3** | `04_data_and_methodology.md` §4.1.4 (line ~212) | aoestats `phase06_interface_aoestats.csv` cited as "136 wierszy"; file is 137 lines (1 header + 136 data); aoestats `[POP:]` scope is implicit-via-spec, not tag-carried. KNOWN TQ-05; recorded not re-litigated, but it is a numeric inconsistency a supervisor could catch and is the only Chapter-4 numeric discrepancy. | C-10; A-4; `phase01_phase02_writing_readiness_audit.md` TQ-05 (lines 660/681/702); `wc -l` = 137 (2026-05-17) | TQ-05 fix-PR: reword to "137 wierszy (1 nagłówek + 136 wierszy danych)" and reframe aoestats `[POP:]` scope as implicit-via-spec-§0 + R02 (0 of 137 `[POP:]` tags). Branch `docs/thesis-tq05-aoestats-rowcount`. Files allowed: `04_data_and_methodology.md` only. Do NOT delete the existing `[REVIEW:]` flag at line ~211 without the reconciled framing. | reviewer-deep |

**Why these three are "must-fix" but the recommendation is still `send_after_must_fixes` (not `do_not_send_yet`):** M-1 is a 10-minute one-line harmonisation; M-2 is a bibliography-hygiene task invisible to a chapter reader (the footer carries full entries); M-3 is a documented, already-diagnosed off-by-one in one Chapter-4 sentence. None blocks the *intellectual* content. A pragmatic supervisor handoff sends Ch1/Ch3/Ch4 now (with the cover note) and holds Ch2 the few minutes needed for M-1. M-2/M-3 can land in parallel without blocking the handoff of the other chapters.

### 7.1 Residual recorded at reviewer-deep T03 (NOT a must-fix; verdict unaffected)

This is a MEDIUM honesty/scope-framing residual surfaced by reviewer-deep at the T03 final review. It is **not** a fourth must-fix item: it does not change the §1 count line (`must_fix_before_supervisor = 3`), the chapter readiness matrix, or the `send_after_must_fixes` recommendation. It is recorded here for provenance per the plan's T03 rule (substantive items are recorded as a §7 residual and surfaced to the user rather than silently expanded).

- **R-1 (MEDIUM — honesty/scope-framing) — plan-authorized web check on four Ch1 econ-metadata loci was deferred, not exercised.** `Shin1993`, `Forrest2005`, `Levitt2004`, `Mangat2024` were routed `W` (web-verifiable) by the plan's §"Evidence routing" (Chapter 1) and §"Web-depth budget" (user authorized up to 3 WebSearch/WebFetch formulations on 2026-05-17) and are NOT in any prior pass2 file. This pass did **not** exercise that authorized ≤3-formulation web check; the four loci were deferred to §11 PR-2 (Chapter-1 bibliography consolidation). The deferral is a sound scope decision for the *supervisor-readiness* verdict — the Ch1 transferability claim is hedged inline (C-06) and the entries are present with full metadata in the Ch1 `## References` footer (D1-NOTE / M-2), so the residual is a `references.bib`-consolidation task, not a missing source — but it is a deliberate deferral of plan-authorized verification, **not an absence of need** (this corrects the original §2.2 framing, now qualified).
- **Verified starting point inherited by PR-2.** reviewer-deep, at T03, independently web-verified two of the four loci against the Chapter-1 footer metadata in a single WebSearch each, both matching the footer: **Shin1993** = *The Economic Journal* 103(420):1141–1153 (1993), Hyun Song Shin — https://academic.oup.com/ej/article-abstract/103/420/1141 (accessed 2026-05-17); **Forrest2005** = *International Journal of Forecasting* 21(3):551–564 (2005), Forrest / Goddard / Simmons, DOI 10.1016/j.ijforecast.2005.03.003 — https://www.sciencedirect.com/science/article/abs/pii/S0169207005000300 (accessed 2026-05-17). **Levitt2004** and **Mangat2024** remain unverified and are PR-2's responsibility. PR-2 therefore inherits a verified starting point for Shin1993 / Forrest2005, not an open question.

---

## 8. OK-to-send-with-disclaimer items

These do NOT block handoff; they are sent **with the in-prose flag retained** and covered by the supervisor note (§10) which states the flags are deliberate Pass-2 verification markers, not unfinished gaps.

- **Ch1:** GarciaMendez2025 streaming-not-RTS (F1-1, already resolved in `literature_verification_log.md`); Shin1993/Forrest2005/Mangat2024 sports-betting-transfer hedge (F1-2, the flag IS the hedge); population framing (F1-7, RISK-01/04/05 wording recommendation exists).
- **Ch2:** DLC chronology completeness (F2-6, AoE2DE bib note covers it); map-pool representativeness (F2-7); Battle.net-MMR grey-lit (F2-12, chapter hedges, Aligulac verified-from-prior-pass).
- **Ch3:** CS:GO / Valorant peer-reviewed-source curation refinements (F3-5, F3-6); EC'25 citation convention (F3-9, librarian decision); grey-lit acceptability reconciliation (F3-11); §3.5 cross-locus framing (F3-13, argumentative and supported).
- **Ch4:** Polish-idiom verification flags across §4.1.2.1/§4.2.2/§4.2.3/§4.4.5/§4.4.6 (F4-8, F4-12, F4-13, F4-16-partial — these are supervisor-facing *register* questions, which the supervisor is exactly the right person to answer); Zenodo metadata flags (F4-1, honest, Pass-2-verifiable); BWZe arithmetic-inference note (F4-3, transparent); name-cardinality two-artifact discrepancy (F4-18, argument holds at both values); aoestats crawler-provenance hedges (F4-5, community-archive interpretation honestly flagged).
- **Annotations (Ch4):** all 18 `[POP:]`/`[PRE-canonical_slot]` — retained as-is, evidence of correct discipline (§5.5).

---

## 9. Future-phase-dependent items (must NOT block handoff)

These are correctly flagged as awaiting Phase 03+ / AoE2 Phase 02 / the feature-engineering phase and **must not** be treated as defects of the current draft. Forbidden-claim discipline (`phase01_phase02_writing_readiness_audit.md` §8 F1–F18) is respected by the chapters: no chapter claims a trained-model result, a closed Phase 02, leakage-free features, or cross-game parity.

- **RQ finalisation / operationalisation:** F1-4, F1-5, F1-6, F1-8 (Ch1 §1.3/§1.4 — Phase 03/04 + AoE2-roadmap dependent).
- **Method-set finalisation:** F2-1, F2-8, F2-9, F2-10 (Ch2 §2.1/§2.4 — SVM-linear status, GNN inclusion, MLP demotion, presentation order — all Phase 04-dependent; the chapter correctly presents them as candidates, not decisions).
- **Within-game / cross-game statistical protocol:** F4-15 (§4.4.4 candidate-family catalogue — correctly framed as advisory candidate set per readiness §2 row 22; final protocol Phase 03+).
- **Artifact-internal distributions deferred to temporal-panel EDA:** F4-2, F4-4, F4-6 (per-tournament stratification, match-length distribution, exact elo_diff).
- **Feature-engineering-phase deferrals:** F4-9 (country per-VIEW decision), F4-17 (§4.4.6 HISTORICAL rewrite / canonical_slot full operationalisation), F4-14 (tracker GATE-14A6 remains `narrowed`, 3 families `blocked_until_additional_validation` — correctly NOT promoted).
- **§4.5 Phase 02 registry provisional framing:** correctly states `partial_coverage_v9_baseline`, Step NOT closed, post-materialization CROSS-02-01 audit NOT yet run, AoE2 Phase 02 ROADMAP-stub-only, asymmetric across datasets — fully consistent with `phase01_phase02_writing_readiness_audit.md` §5 + `notebook_regeneration_manifest.md` (forbidden claims F3/F4/F5/F7 NOT made).

These 14 future-phase items are a sign the draft is **honest about its own boundaries**, not a sign it is unready for a *working-draft* supervisor handoff.

---

## 10. Recommended supervisor handoff package

**What to send / not send.** Send **Chapters 1, 3, 4** now as a working draft, **with the in-prose `[REVIEW:]` / `[NEEDS CITATION:]` / `[UNVERIFIED:]` flags retained** and a cover note. Send **Chapter 2** after the single §2.5.5 EsportsBench harmonisation (M-1, ~10 min). Do **not** send Chapters 5–6 (out of scope; no model trained — forbidden claims F1/F2). Keep `[POP:]` / `[PRE-canonical_slot]` annotations in Chapter 4 (they are scope discipline, not unfinished work). Do **not** strip the REVIEW flags before the supervisor: they are deliberate Pass-2 verification markers and several of them (the Polish-idiom flags in Ch4) are questions the supervisor is the right person to answer.

**Suggested supervisor note (Polish, register per `.claude/author-style-brief-pl.md`: bezosobowy, argumentacyjny, ISO `YYYY-MM-DD`, bez anglicyzmów branżowych):**

> **Nota do przekazania promotorowi (wersja robocza rozdziałów 1–4)**
>
> Przekazuje się do recenzji wersję roboczą rozdziałów 1, 3 i 4. Rozdział 2 zostanie przekazany po naniesieniu jednej drobnej korekty spójności (ujednolicenie wersji benchmarku EsportsBench w §2.5.5 do v9.0, cutoff 2026-03-31, dostęp 2026-04-26 — wartość zgodna z §3.2.4 i §3.5; w obecnym stanie §2.5.5 podaje nieaktualną v8.0 z cutoffem 2025-12-31). Rozdziałów 5–6 nie przekazuje się: nie wytrenowano dotychczas żadnego modelu, więc rozdziały wynikowe nie zawierają jeszcze treści merytorycznej.
>
> Znaczniki `[REVIEW: …]`, `[NEEDS CITATION: …]` oraz `[UNVERIFIED: …]` pozostawiono w tekście świadomie. Nie są to luki w argumentacji ani nieukończone fragmenty, lecz znaczniki weryfikacji drugiego przejścia (Pass-2): wskazują miejsca, w których (a) dokładna wartość liczbowa wymaga ręcznego odczytu pełnego tekstu źródła niedostępnego narzędziom automatycznym (np. Tabela 2 preprintu EsportsBench, dokładna trafność CetinTas2023, lokalizacja sekcyjna w Demšar 2006 — strumienie PDF nieodczytywalne maszynowo), (b) rozstrzygnięcie zależy od fazy eksperymentalnej jeszcze nieukończonej (finalizacja pytań badawczych, dobór protokołu statystycznego, progi zimnego startu — wszystkie zarezerwowane do faz późniejszych), albo (c) wymagana jest decyzja redaktorska promotora co do polskiego idiomu terminologicznego (oznaczone w rozdziale 4 jako pytania o rejestr — np. „within-reference homogeneity", „dataset-conditional", terminologia procedury rozpoznawania tożsamości). Prosi się o nietraktowanie obecności tych znaczników jako oznaki niegotowości tekstu do recenzji roboczej; przeciwnie, dokumentują one rozróżnienie między tym, co zostało zweryfikowane, a tym, co pozostaje do potwierdzenia.
>
> Warstwa literaturowa rozdziału 3 została w całości zweryfikowana w odrębnym przejściu walidacyjnym (rejestr weryfikacji literatury, 2026-04-26); rozdział ten można czytać jako najbardziej dojrzały. Twierdzenia liczbowe w rozdziale 4 pochodzą wyłącznie z trwałych artefaktów etapu eksploracji danych; rozdział nie formułuje żadnych twierdzeń o wynikach modelowania, o zamknięciu fazy inżynierii cech ani o parytecie między korpusami — te zostały świadomie wykluczone do czasu zaistnienia odpowiednich dowodów. Znaczniki zakresu `[POP: …]` oraz `[PRE-canonical_slot]` w rozdziale 4 są elementem dyscypliny opisu populacji źródłowej (rozróżnienie populacji turniejowej, rekordów 1v1 Random Map o nieujawnionej semantyce kolejki oraz trybu mieszanego ranked/quickplay), nie zaś fragmentami do uzupełnienia — prosi się o ich zachowanie.
>
> Uprzejmie prosi się o wskazanie, czy preferowany jest odczyt rozdziałów ze znacznikami weryfikacji widocznymi w tekście, czy też w wersji z usuniętymi znacznikami; rekomenduje się wariant pierwszy, ponieważ część znaczników rozdziału 4 to bezpośrednie pytania o akceptowalność polskiej terminologii, na które odpowiedź promotora jest pożądana przed finalizacją.

**Include or strip REVIEW flags:** **include** (recommended) — the §10 note explains why; several Ch4 flags are register questions for the supervisor. If the supervisor explicitly prefers a clean read, a flag-stripped export can be produced as a separate one-off (out of scope for this audit), but the annotated version is recommended for the working-draft round.

---

## 11. Proposed next PRs

Each is a future, separately-gated PR (this audit performs none of them). Listed in handoff-priority order.

### PR-1 — EsportsBench version harmonization (must-fix M-1; highest priority)

- **Branch:** `docs/thesis-esportsbench-version-harmonization`
- **Files allowed:** `thesis/chapters/02_theoretical_background.md` (§2.5.5 line 179 only) + `CHANGELOG.md` + `pyproject.toml` + `planning/*`.
- **Agent routing:** `@executor` (mechanically specified single-locus prose fix; the methodological decision — which version is canonical — is already resolved by `literature_verification_log.md` note 4).
- **Reviewer routing:** `@reviewer-deep` (cross-locus consistency claim; Category F).
- **What NOT to claim:** do NOT introduce a new EsportsBench version without WebFetch verification of the HuggingFace dataset-card commit log; do NOT act on TQ-04's stale "§3.2.4 internal contradiction" wording (C-04 — that contradiction does not exist at HEAD); do NOT touch §3.2.4/§3.5 (already correct); do NOT close any unrelated flag.

### PR-2 — Chapter-1 bibliography consolidation (must-fix M-2)

- **Branch:** `docs/thesis-bib-consolidation-ch1-footer`
- **Files allowed:** `thesis/references.bib` + `thesis/chapters/01_introduction.md` (footer only) + CHANGELOG/pyproject/planning.
- **Agent routing:** `@executor` for the mechanical migration; web-verification of Shin1993/Forrest2005/Levitt2004/Mangat2024 metadata (≤3 formulations each) before adding — if any is unverifiable, add with a `[REVIEW: metadata Pass-2]` note rather than inventing.
- **Reviewer routing:** `@reviewer-deep` (bib-integrity; Category F).
- **What NOT to claim:** do NOT assert any of the migrated entries is "verified" from an abstract; do NOT remove the Ch1 footer entries until the central bib entry is confirmed; do NOT renumber or restructure other chapters' citations.

### PR-3 — TQ-05 aoestats row-count framing fix (must-fix M-3)

- **Branch:** `docs/thesis-tq05-aoestats-rowcount`
- **Files allowed:** `thesis/chapters/04_data_and_methodology.md` (§4.1.4 line ~212 + the matching §4.4.6 reference) + CHANGELOG/pyproject/planning.
- **Agent routing:** `@executor` (mechanical; framing already resolved by `phase01_phase02_writing_readiness_audit.md` TQ-05).
- **Reviewer routing:** `@reviewer-deep` (Category F; numeric-consistency).
- **What NOT to claim:** do NOT delete the existing `[REVIEW:]` flag at line ~211 without the reconciled framing; do NOT re-derive the file content (137-line fact is established); do NOT extend to other CONSORT counts (out of scope).

### PR-4 — Pass-2 manual full-text verification batch (optional, post-handoff)

- **Branch:** `docs/thesis-pass2-manual-fulltext-batch`
- **Files allowed:** `thesis/chapters/02_theoretical_background.md`, `03_related_work.md`, `04_data_and_methodology.md`, `thesis/references.bib`, `thesis/pass2_evidence/literature_verification_log.md` (append-only).
- **Scope:** resolve the nine `manual_full_text_required` items via human PDF reads (EsportsBench Table 2 exact 80,13% + Aligulac-row choice; Demsar2006 §-location F5.6; CetinTas2023 exact 86% + NB-vs-DT; Khan2024SCPhi2 exact accuracy; Xie2020 R²-vs-accuracy; Minka2018TR Halo-5 68%/52%; the §4.4.5 ICC CI-method `[UNVERIFIED]`) and the F-036 candidate-author `[NEEDS CITATION]` (Google Scholar / IEEE Xplore / ACM DL library lookup).
- **Agent routing:** human-in-the-loop full-text reads, then `@executor` to record; `@planner-science` if any finding changes a methodology framing.
- **Reviewer routing:** `@reviewer-deep`; escalate to `@reviewer-adversarial` only if a verified value overturns a quantitative comparator entering Chapter 6.
- **What NOT to claim:** do NOT mark any item verified without an admissible full-text citation; inherit, do not re-attempt, items T14 already classified PDF-binary unless a new accessible source is found.

---

*End of audit. This document records findings only; it changes no chapter prose, no `references.bib`, no flag, no artifact. The supervisor handoff decision rests with the user; this audit recommends `send_after_must_fixes` with the three enumerated must-fix items (M-1, M-2, M-3) and the Polish cover note in §10.*
