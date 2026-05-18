# Chapters 1–4 supervisor handoff package

Consolidates merged audit chain #220 audit / #221 M-1 / #222 M-2 / #223 M-3, all on master `855bdbb6`, version pre-bump 3.58.0, 2026-05-18. No new methodology, no chapter prose edit. Authoritative source: `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md`.

## 1. Executive decision

- Chapters 1–4 may be sent **as a working draft**; use the exact phrase `ready_to_send_with_disclaimer`.
- All three must-fixes CLOSED on master: M-1 (#221), M-2 (#222), M-3 (#223). The audit §10 "send 1/3/4 now, hold Chapter 2 for M-1" framing is **superseded** — with M-1 merged, Chapters 1, 2, 3, 4 are all sendable together.
- The "disclaimer": retained `[REVIEW:]`/`[NEEDS CITATION:]`/`[UNVERIFIED:]` flags are deliberate Pass-2 / transparent draft markers, not unfinished core methodology; several Ch4 flags are register questions for the supervisor.
- Chapters 5–7 NOT sent as substantive content: no Phase 03+ model results; Ch5 all BLOCKED, Ch6 §6.1–§6.4 BLOCKED + §6.5 skeleton, Ch7 §7.1/§7.2 BLOCKED + §7.3 idea list. Sending them creates a false expectation of completed experiments.

## 2. What to send

Default handoff = exactly these four files (flags retained, see §5):
`thesis/chapters/01_introduction.md`,
`thesis/chapters/02_theoretical_background.md`,
`thesis/chapters/03_related_work.md`,
`thesis/chapters/04_data_and_methodology.md`.
**Optional traceability attachments — only if the supervisor asks (or the user wants evidence/bibliography support):** `thesis/references.bib` (consolidated after #222) and `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md` (readiness reasoning + flag triage). Default handoff is the four chapter files alone.

## 3. What not to send yet

`thesis/chapters/05_experiments_and_results.md` (all subsections BLOCKED — Phase 03/04/05 / AoE2 phases / both-games-complete); `thesis/chapters/06_discussion.md` (§6.1–§6.4 BLOCKED — Chapter 5; §6.5 skeleton stub); `thesis/chapters/07_conclusions.md` (§7.1/§7.2 BLOCKED; §7.3 idea-comment). Rationale: blocked on Phase 03+ / AoE2 phases; no model trained; sending misrepresents status and creates a false expectation of completed results.

## 4. Must-fix closure summary

| Must-fix | Issue | Fix | PR | Readiness impact |
|---|---|---|---|---|
| **M-1** | `02_theoretical_background.md` §2.5.5 cited EsportsBench `v8.0 / cutoff 2025-12-31` — stale; §3.2.4 + §3.5 already `v9.0 / 2026-03-31 / dostęp 2026-04-26`, so Ch2 self-contradicted Ch3 on a quantitative comparator (SC2 Aligulac 411 030-match / ~80% Glicko). | Single-locus prose harmonisation §2.5.5 → `v9.0, cutoff 2026-03-31, dostęp 2026-04-26`. No flag added/removed; no `references.bib` change. | **#221** | Ch2 `not_ready` → `ready_to_send_with_disclaimer`; removed the only cross-chapter self-contradiction (sole `fix_before_supervisor` flag). |
| **M-2** | Ch1 §1.1 + footer: Shin1993/Forrest2005/Levitt2004/Mangat2024/Formosa2022/Novak2025/Balduzzi2018 cited but absent from `references.bib` (consolidation gap, NOT phantom); Mangat2024 footer `40(1),145-165`. | Append-only migration of 7 footer entries → `references.bib` (100→107), web-verified; Mangat2024 → `40(2),893-914` (PMID 37740076); Novak2025 first author → Pál. Prose body unchanged; no flag removed. | **#222** | Closes the central-bib consolidation gap; bib complete for typesetting. Line-11 transferability `[REVIEW]` hedge intentionally NOT closed. |
| **M-3** | `04_data_and_methodology.md` §4.1.4 cited aoestats CSV as "136 wierszy"; file 137 lines; artifact carries `[POP:ranked_ladder]` in all 136 data rows but prose discipline is `[POP:1v1_random_map]`/Tier-4 (R02 + input contract 02_00). | Reword to `137 wierszy łącznie: 1 nagłówek + 136 wierszy danych` + on-disk-true caveat (artifact `[POP:ranked_ladder]` operationally superseded in prose by `[POP:1v1_random_map]`/Tier-4); the audit's own stale "0 tags" prescription corrected. Line-212 `[REVIEW]` retained; no `references.bib`/REVIEW_QUEUE change; no prose-body rewrite. | **#223** | M-3/TQ-05 resolved. With M-1+M-2, Chapters 1–4 `ready_to_send_with_disclaimer`; closes the only Ch4 numeric discrepancy; source-label discipline preserved. |

## 5. Retained review flags

Totals: Ch1 = 8 `[REVIEW:]`; Ch2 = 18 `[REVIEW:]`; Ch3 = 14 `[REVIEW:]` + 1 `[NEEDS CITATION:]`; Ch4 = 34 `[REVIEW:]` + 1 `[UNVERIFIED:]`; total Pass-2 = 76; + 18 Ch4 `[POP:]`/`[PRE-canonical_slot]` annotations (scope discipline, not flags). Aggregate: 41 ok_to_send_with_flag / 9 manual_full_text_required / 14 future_phase_dependent (the 3 must-fixes are now closed).
- **Literature/source-verification (`ok_to_send_with_flag`, ~41):** the flag text is itself the honest hedge (Ch1 §1.1 Shin1993/Forrest2005 transferability; Mangat2024 gambling-psych); grey-lit acceptability (Ch2 §2.2.4/§2.5.4, Ch3 §3.4.4); DLC chronology (Ch2 §2.3.2); Zenodo metadata (Ch4 §4.1.1.0). Safe with the flag visible.
- **`manual_full_text_required` (9):** human PDF reads — EsportsBench Table 2 80,13% + Aligulac-row; Demsar2006 §-location; CetinTas2023 86% + NB-vs-DT; Khan2024SCPhi2 accuracy; Xie2020 R²-vs-accuracy; Minka2018TR Halo-5 68%/52%; §4.4.5 ICC CI-method `[UNVERIFIED]` (honest — `icc.json` does not name the CI method); + F-036 `[NEEDS CITATION]` library lookup. Precision items on already-cited sources.
- **`future_phase_dependent` (14):** RQ finalisation (Ch1 §1.3/§1.4); method-set finalisation (Ch2 §2.1/§2.4 — candidates not decisions); within/cross-game protocol (§4.4.4); artifact-internal distributions (§4.1.x); feature-engineering deferrals (§4.4.6; tracker GATE-14A6 `narrowed`, 3 families correctly NOT promoted); §4.5 provisional registry (`partial_coverage_v9_baseline`, Step NOT closed). Evidence of boundary honesty.
- **Intentionally-retained methodology caveats / annotations:** 18 Ch4 `[POP:]`/`[PRE-canonical_slot]` = correct source-label/population discipline (tournament vs 1v1 Random Map undisclosed-queue vs mixed ranked/quickplay), NOT fragments to fill. Ch4 Polish-idiom register flags retained because the supervisor is the right person to answer them.

State clearly: stripping the flags before the supervisor is NOT recommended — they document verified-vs-to-be-confirmed; several Ch4 flags are direct register questions; they are transparent draft markers, not unfinished core methodology.

## 6. Recommended Polish note to supervisor

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

## 7. Suggested attachment/export options

- Default: send the four chapter Markdown files directly (lowest friction; preserves the visible `[REVIEW]` flags).
- Optional traceability — only if the supervisor asks: include `thesis/references.bib` (bibliography traceability after #222) and/or `thesis/pass2_evidence/ch1_ch4_citation_literature_support_audit.md` (readiness reasoning + flag triage).
- PDF/DOCX export and any flag-stripped clean copy are deliberately a separate later step (out of scope here; annotated version recommended — Ch4 flags are register questions). This PR exports nothing and creates no clean copy.

## 8. Remaining after supervisor handoff

Phase 03 Splitting & Baselines (SC2) → unblocks Ch5 §5.1.1; optional retained-flag cleanup (the `manual_full_text_required` batch + F-036 lookup — audit §11 PR-4, post-handoff); Phase 04/05 Model Training & Evaluation (SC2) → unblocks Ch5 §5.1.2–§5.1.4 + Ch6; AoE2 Phase 02 onward (later) → unblocks Ch5 §5.2/§5.3; Chapters 5–7 drafted only after the corresponding model results exist; §1.5 thesis outline finalised last.
