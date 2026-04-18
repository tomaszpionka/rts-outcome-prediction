# Thesis Review Queue — Pass 1 → Pass 2 Handoff

This file tracks thesis sections that Claude Code has drafted (Pass 1) and
that need external validation in Claude Chat (Pass 2).

## Workflow

1. Claude Code drafts a section and runs the Critical Review Checklist
   (see `.claude/thesis-writing.md`)
2. Claude Code plants `[REVIEW: ...]` and other inline flags
3. Claude Code appends an entry to the Pending table below
4. User brings the section + referenced artifacts to Claude Chat for Pass 2
5. After Pass 2 corrections are applied, move the entry to Completed

## Pending Pass 2 reviews

| Section | Chapter file | Drafted date | Flag count | Key artifacts | Pass 2 status |
|---------|-------------|-------------|------------|---------------|---------------|
| §1.1 Background and motivation | thesis/chapters/01_introduction.md | 2026-04-13 | 0 | — (literature section, no data artifacts) | Pending — Pass 2 blocking items resolved |
| §2.5 Player skill rating systems | thesis/chapters/02_theoretical_background.md | 2026-04-17 | 4 [REVIEW] | thesis/reviews_and_others/related_work_rating_systems.md (seed bibliography); thesis/references.bib (12 new entries appended) | Pending — Gate 0.5 calibration draft. 17 keys cited. Polish ~13.4k chars. Key Pass 2 questions: (1) TrueSkill 2 independent RTS validation? (2) Liquipedia/Battle.net MMR grey-literature acceptability? (3) historical Aligulac snapshots for SC2EGSet retrospective ratings? (4) EsportsBench cross-system validation reference? |
| §1.3 Research questions | thesis/chapters/01_introduction.md | 2026-04-17 | 2 [REVIEW] | thesis/references.bib (Bois2025 added) | Pending — Pass 2 questions: (1) RQ4 cold-start strata thresholds — empirical match-count distribution to be confirmed after Phase 03; (2) RQ1 hypothesis on GBDT dominance in two-game cross comparison — verify Thorrez2024 EsportsBench reports cross-system comparability beyond per-system fit. |
| §1.4 Scope and limitations | thesis/chapters/01_introduction.md | 2026-04-17 | 1 [REVIEW] | — (literature/framing section) | Pending — Pass 2 questions: (1) AoE2 roadmap status — verify whether mgz parser inclusion remains out of scope after AoE2 phase planning; (2) AoE2 civilization count over corpus window — confirm 45 figure against actual data window vs. current Definitive Edition value. |
| §3.2 StarCraft prediction literature | thesis/chapters/03_related_work.md | 2026-04-17 | 6 [REVIEW] | thesis/reviews_and_others/related_work_historical_rts_prediction.md (seed bibliography); thesis/references.bib (15 new entries appended) | Pending — Pass 1 calibration draft. 28 distinct keys cited. Polish ~14.8k chars. Key Pass 2 questions: (1) confirm Tarassoli2024 bib deletion as SC-Phi2 misattribution; (2) verify SC-Phi2 quantified accuracy from MDPI AI version; (3) verify EsportsBench 80.13% exact figure for SC2 from Thorrez preprint; (4) verify Khan2024SCPhi2 venue (arXiv vs MDPI AI); (5) verify Vinyals2017 prediction baseline phrasing; (6) verify Bialecki2022 vs Bialecki2023 corpus relationship language |

## Completed Pass 2 reviews

| Section | Reviewed date | Reviewer notes |
|---------|--------------|----------------|
| *(none yet)* | | |

## How to use this in Claude Chat

When bringing a section for Pass 2 review, provide Claude Chat with:
1. The section text from `thesis/chapters/XX_*.md`
2. The report artifacts listed in the "Key artifacts" column
3. The specific `[REVIEW: ...]` flags from the draft
4. Any `[NEEDS CITATION]` flags (Claude Chat will search the literature)

Claude Chat will return: resolved flags, suggested citations, methodology
alignment checks, and any corrections to statistical interpretation.
