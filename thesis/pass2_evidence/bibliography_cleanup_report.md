# Bibliography Canonicalization — Cleanup & Audit Report

This report consolidates the `thesis/references.bib` canonicalization audit.
Base master `e095025a`; v3.59.0 pre-bump; 2026-05-18. Authoritative scope =
the merged audit chain (PR #220–#224) + the planner-science plan
(`planning/current_plan.md`) + the reviewer-deep T01 plan gate
(`planning/current_plan.critique.md`). **This is an audit-only artifact:
`thesis/references.bib` is NOT edited in this report's commit (T02).
Evidence-safe corrections are applied separately at T03** under the
≥80-confidence / identity-safe gate defined by the plan.

All web verification (Crossref / publisher / official) and the
`Dimitriadis2024` identity adjudication referenced below were performed at
plan time (planner-science) and at the reviewer-deep T01 gate; they are
reused here, not re-derived.

---

## Lineage header (per `.claude/rules/data-analysis-lineage.md`)

- **Assumption tested:** the four user-named "duplicate pairs"
  (`Wu2017`+`Wu2017MSC`, `BaekKim2022`+`Baek2022`,
  `Porcpine2020EloAoE`+`Porcpine2020`, `Herbrich2006`+`Herbrich2007`) are
  duplicate records, plus the seven Crossref-verify keys and the schema
  changes carry resolvable canonicalization defects.
- **Measurement:** on-disk `grep`/extraction of every `@`-entry in
  `thesis/references.bib` and every markdown reference-list line / embedded
  ` ```bibtex ``` ` block in the five scoped source files; cross-checked
  against Crossref / publisher / official records collected at plan time +
  reviewer-deep T01.
- **Sanity check:** the 107-entry probe was reproduced on `HEAD`
  (`grep -c '^@' thesis/references.bib` = 107); the `Wu2017` /
  `Wu2017MSC` citation-site grep was re-run on disk.
- **Falsifier:** if a named "pair" were two distinct works, the
  classification flips from dedup/alias-drift to "distinct records, no
  merge". This was the live risk for `Dimitriadis2024`; it was tested at
  the reviewer-deep gate (four concurring sources) and **resolved: same
  triptych work** (see Per-field diffs and the superseded-statements
  section). No other pair triggered the falsifier.
- **Downstream decision:** which `thesis/references.bib` edits T03 applies.
  T02 (this report) makes ZERO bib edits; it freezes the evidence on which
  the T03 edit set is gated.

---

## Master table

**Counted total master-table rows: 119** = 107 `thesis/references.bib`
`@`-entries (one compact row each) + 12 markdown-extracted rows for the
named / alias-candidate / flagged keys (`Wu2017`, `Wu2017MSC`,
`Baek2022`, `Porcpine2020`, `Herbrich2007`, `Glickman2025` appendix copy,
`BT2025Survey`, `Dimitriadis2024` appendix copy, plus the five-file
markdown extraction rows for `Khan2024SCPhi2`/SC-Phi2 label,
`Bahrololloomi2023`, `Glickman1995`, and the prior `literature_verification_log.md`
`Dimitriadis2024` row). Row count was counted from the extraction, not
invented.

Columns are exactly: `key | source_file | entry_type | title | authors | year | venue | doi | url | status | relevance | confidence | note | action`.

### A. `thesis/references.bib` entries (107 rows, compact one-line-per-key)

| key | source_file | entry_type | title | authors | year | venue | doi | url | status | relevance | confidence | note | action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bialecki2023 | references.bib | article | SC2EGSet: StarCraft II Esport Replay and Game-state Dataset | Białecki A.; Jakubowska N.; Dobrowolski P.; Białecki P.; Krupiński L.; Szczap A.; Białecki R.; Gajewski J. | 2023 | Scientific Data 10 art.600 | yes | no | ok | core dataset | 95 | official 8-author list matches bib L5-13 exactly | keep |
| Vinyals2017 | references.bib | article | StarCraft II: A New Challenge for RL | Vinyals O.; Ewalds T.; Bartunov S.; +others | 2017 | arXiv:1708.04782 | no | no | ok | context | 90 | truncated author list (preprint) | keep |
| Wu2017 | references.bib | article | MSC: A Dataset for Macro-Management in SC2 | Wu H.; Zhang J.; Huang K. | 2017 | arXiv preprint (id in Sources) | no | no | intra_bib_dup | dataset | 99 | byte-identical to Wu2017MSC; cited 0x | merge_into:Wu2017MSC |
| BaekKim2022 | references.bib | article | 3D CNNs for predicting SC2 results | Baek I.; Kim S.B. | 2022 | PLOS ONE 17(3):e0264550 | yes | no | ok | core SC2 pred | 95 | canonical key for the appendix `Baek2022` alias | keep |
| Khan2021 | references.bib | inproceedings | Leveraging Transformers for SC2 Macromanagement | Khan M.J.; et al. | 2021 | — | no | no | ok | context | 80 | — | keep |
| Hodge2021 | references.bib | article | Win Prediction in Multi-Player Esports | Hodge V.J.; et al. | 2021 | — | no | no | ok | esports pred | 80 | — | keep |
| CetinTas2023 | references.bib | inproceedings | Regression Analysis of AoE2 DE Match Results | Cetin/Tas | 2023 | — | no | no | ok | AoE2 pred | 80 | — | keep |
| Elbert2025EC | references.bib | inproceedings | What Drives Team Success? | Elbert et al. | 2025 | — | no | no | ok | context | 75 | — | keep |
| Xie2020MediumAoE | references.bib | misc | Predicting Win Rates in AoE2 HD | Xie | 2020 | Medium (grey-lit) | no | yes | ok | grey-lit context | 70 | Tier 3 grey literature | keep |
| Porcpine2020EloAoE | references.bib | misc | Impact of Rating Difference on Win % in AoE2 DE | porcpine1967 | 2020 | GitHub Pages (grey-lit) | no | yes | ok | AoE2 Elo baseline | 80 | canonical key for the appendix `Porcpine2020` alias | keep |
| Glickman2001 | references.bib | article | Dynamic Paired Comparison Models | Glickman M.E. | 2001 | — | no | no | ok | rating systems | 85 | — | keep |
| Herbrich2006 | references.bib | inproceedings | TrueSkill: A Bayesian Skill Rating System | Herbrich R.; Minka T.; Graepel T. | 2006 | NeurIPS | no | no | ok | rating systems | 90 | canonical key for the appendix `Herbrich2007` alias (2007 defensible) | keep |
| Elo1978 | references.bib | article | The Rating of Chessplayers, Past and Present | Elo A.E. | 1978 | (publisher Arco; no journal) | no | no | type_mismatch | rating systems | 90 | `@article` w/ publisher, no journal → should be `@book`; title-form decision (see schema subsection) | schema_change:book |
| Demsar2006 | references.bib | article | Statistical Comparisons of Classifiers | Demšar J. | 2006 | JMLR | no | no | ok | stats methodology | 90 | — | keep |
| Thorrez2024 | references.bib | misc | EsportsBench | Thorrez | 2024 | grey-lit | no | no | ok | rating eval | 70 | — | keep |
| Aligulac | references.bib | misc | Aligulac SC2 player ratings | Aligulac | 2026 | live site (grey-lit) | no | yes | appendix_only | grey-lit data source | 60 | `@misc` year 2026 = live-site date convention; editorial | manual_decision |
| BradleyTerry1952 | references.bib | article | Rank Analysis of Incomplete Block Designs I | Bradley R.A.; Terry M.E. | 1952 | Biometrika | no | no | ok | rating foundations | 95 | — | keep |
| Dimitriadis2024 | references.bib | article | Evaluating probabilistic classifiers: The triptych | Dimitriadis T.; Gneiting T.; Jordan A.I. | 2024 | Int. J. Forecasting 40(1):189–210 | no | no | identity_collision | calibration eval | 92 | identity CLOSED = same triptych work; bib has early/incorrect metadata (40(1):189–210, 3 authors, no DOI); published = 40(3):1101–1122, +Vogel, +DOI | fix_metadata |
| Fujii2023NBTR | references.bib | article | Neural Bradley-Terry Rating | Fujii et al. | 2023 | — | no | no | ok | rating systems | 80 | — | keep |
| Glickman1999 | references.bib | article | Parameter Estimation in Large Dynamic Paired Comparison | Glickman M.E. | 1999 | Applied Statistics | no | no | ok | rating systems | 85 | — | keep |
| Glickman2013TR | references.bib | techreport | Example of the Glicko-2 system | Glickman M.E. | 2013 | tech report | no | no | ok | rating systems | 85 | — | keep |
| Glickman2025 | references.bib | article | Models and Rating Systems for Head-to-Head Competition | Glickman M.E.; Jones Albyn C. | 2025 | Annu. Rev. Stat. 12:259–282 | yes | no | ok | rating systems survey | 98 | central bib correct (Crossref); appendix copy has 2nd-author typo (catalogued) | keep |
| Gneiting2007 | references.bib | article | Strictly Proper Scoring Rules | Gneiting T.; Raftery A.E. | 2007 | JASA | no | no | ok | calibration | 90 | — | keep |
| Hamilton2025 | references.bib | article | Impact of intransitivity on the Elo rating system | Hamilton et al. | 2025 | — | no | no | ok | rating systems | 80 | — | keep |
| Lin2024NCT | references.bib | article | Identifying and Clustering Counter Relationships | Lin et al. | 2024 | — | no | no | ok | AoE2 intransitivity | 80 | — | keep |
| Minka2018TR | references.bib | techreport | TrueSkill 2 | Minka T.; et al. | 2018 | MSR tech report | no | no | ok | rating systems | 85 | — | keep |
| Tang2025 | references.bib | article | Is Elo Rating Reliable? | Tang et al. | 2025 | — | no | no | ok | rating systems | 80 | — | keep |
| Bois2025 | references.bib | article | PandaSkill | Bois et al. | 2025 | — | no | no | ok | esports rating | 75 | — | keep |
| GarciaMendez2025 | references.bib | article | Explainable e-sports win prediction | García-Méndez et al. | 2025 | — | no | no | ok | esports pred | 80 | — | keep |
| Erickson2014 | references.bib | inproceedings | Global State Evaluation in StarCraft | Erickson G.; Buro M. | 2014 | AIIDE | no | no | ok | SC pred | 85 | — | keep |
| Ravari2016 | references.bib | inproceedings | StarCraft Winner Prediction | Ravari Y.N.; et al. | 2016 | — | no | no | ok | SC pred | 80 | — | keep |
| Robertson2014Survey | references.bib | article | A Review of Real-Time Strategy Game AI | Robertson G.; Watson I. | 2014 | AI Magazine | no | no | ok | RTS AI survey | 85 | — | keep |
| Ontanon2013 | references.bib | article | A Survey of RTS Game AI Research | Ontañón S.; et al. | 2013 | IEEE TCIAIG | no | no | ok | RTS AI survey | 85 | — | keep |
| Vinyals2019 | references.bib | article | Grandmaster Level in StarCraft II | Vinyals O.; et al.; +others | 2019 | Nature | no | no | ok | context | 90 | truncated `and others` (Nature long author list — editorial) | manual_decision |
| Bialecki2022 | references.bib | article | Determinants of Victory in Esports — SC2 | Białecki A.; et al. | 2022 | — | no | no | ok | SC2 pred | 80 | — | keep |
| Wu2017MSC | references.bib | article | MSC: A Dataset for Macro-Management in SC2 | Wu H.; Zhang J.; Huang K. | 2017 | arXiv preprint (id in Sources) | no | no | ok | dataset (canonical) | 99 | canonical of the Wu2017/Wu2017MSC intra-bib pair; cited 8 lines | keep |
| Justesen2017 | references.bib | inproceedings | Learning Macromanagement in StarCraft from Replays | Justesen N.; Risi S. | 2017 | IEEE CIG | no | no | ok | SC pred | 85 | — | keep |
| Lin2019NP | references.bib | article | An Uncertainty-Incorporated Approach to Predict the Winner | Lin et al.; +others | 2019 | — | no | no | ok | SC pred | 75 | truncated `and others` author list | manual_decision |
| Volz2019 | references.bib | incollection | Towards Embodied SC2 Winner Prediction | Volz V.; et al. | 2019 | — | no | no | ok | SC pred | 80 | — | keep |
| Avontuur2013 | references.bib | inproceedings | Player Skill Modeling in StarCraft II | Avontuur T.; et al. | 2013 | UMAP | no | no | ok | SC pred | 80 | — | keep |
| Chen2020 | references.bib | inproceedings | Improving SC2 Player League Prediction | Chen et al. | 2020 | LNCS (ambiguous vol.) | no | no | metadata_mismatch | SC pred | 60 | missing pages/DOI, ambiguous LNCS volume | manual_decision |
| Lee2021Combat | references.bib | article | Predicting Combat Outcomes and Optimizing Armies | Lee et al. | 2021 | — | no | no | ok | SC pred | 80 | complete metadata; relevance scoping is a human call | manual_decision |
| Khan2024SCPhi2 | references.bib | article | SC-Phi2: A Fine-Tuned Small LM for SC2 Build Order Prediction | Khan M.J.; Sukthankar G. | 2024 | AI (MDPI) 5(4):2338–2352 | yes | no | ok | SC pred | 98 | Crossref-confirmed; "SC-Phi2" is the user's label, NOT a bibkey | keep |
| Dixon1997 | references.bib | article | Modelling Association Football Scores | Dixon M.J.; Coles S.G. | 1997 | Applied Statistics | no | no | ok | sports modelling | 90 | — | keep |
| Maher1982 | references.bib | article | Modelling Association Football Scores | Maher M.J. | 1982 | Statistica Neerlandica | no | no | ok | sports modelling | 90 | — | keep |
| Constantinou2013 | references.bib | article | pi-football Bayesian network | Constantinou A.C.; et al. | 2013 | — | no | no | ok | sports modelling | 80 | — | keep |
| Bunker2024 | references.bib | article | Comparative evaluation of Elo & ML | Bunker R.; et al. | 2024 | — | no | no | ok | rating/ML | 80 | — | keep |
| Glickman1995 | references.bib | unpublished | A Comprehensive Guide to Chess Ratings | Glickman M.E. | 1995 | American Chess Journal v.3:59–102 | no | no | metadata_mismatch | rating systems foundations | 85 | verified ≥80 via author's official page; no DOI (ACJ not DOI-indexed — correctly absent, NOT a fabrication gap); `@unpublished`→`@article` is an editorial call | manual_decision |
| Yang2017Dota | references.bib | article | Real-time eSports Match Result Prediction | Yang Y.; et al. | 2017 | arXiv:1701.03162 | no | no | ok | esports pred | 80 | — | keep |
| Bahrololloomi2023 | references.bib | article | E-Sports Player Performance Metrics (LoL) | Bahrololloomi F.; Klonowski F.; Sauer S.; Horst R.; Dörner R. | 2023 | SN Computer Science 4(3) art.238 | yes | no | ok | esports pred | 90 | Crossref-confirmed; matches bib | keep |
| Akhmedov2021 | references.bib | article | ML models for DOTA 2 outcomes | Akhmedov; et al. | 2021 | — | no | no | ok | esports pred | 80 | — | keep |
| Silva2018LoL | references.bib | inproceedings | Continuous Outcome Prediction of LoL | Silva et al. | 2018 | — | no | no | ok | esports pred | 80 | — | keep |
| Yangibaev2025 | references.bib | article | DotA 2 Match Outcome Prediction System | Yangibaev | 2025 | — | no | no | ok | esports pred | 75 | — | keep |
| Hastie2009ESL | references.bib | book | The Elements of Statistical Learning | Hastie T.; Tibshirani R.; Friedman J. | 2009 | Springer | no | no | ok | ML textbook | 95 | — | keep |
| Friedman2001GBM | references.bib | article | Greedy Function Approximation: GBM | Friedman J.H. | 2001 | Ann. Statistics | no | no | ok | ML methodology | 95 | — | keep |
| Chen2016XGBoost | references.bib | inproceedings | XGBoost | Chen T.; Guestrin C. | 2016 | KDD | no | no | ok | ML methodology | 95 | — | keep |
| Ke2017LightGBM | references.bib | inproceedings | LightGBM | Ke G.; et al. | 2017 | NeurIPS | no | no | ok | ML methodology | 95 | — | keep |
| Goodfellow2016DL | references.bib | book | Deep Learning | Goodfellow I.; Bengio Y.; Courville A. | 2016 | MIT Press | no | no | ok | ML textbook | 95 | — | keep |
| Breiman2001 | references.bib | article | Random Forests | Breiman L. | 2001 | Machine Learning | no | no | ok | ML methodology | 95 | — | keep |
| CortesVapnik1995 | references.bib | article | Support-Vector Networks | Cortes C.; Vapnik V. | 1995 | Machine Learning | no | no | ok | ML methodology | 95 | — | keep |
| Hochreiter1997LSTM | references.bib | article | Long Short-Term Memory | Hochreiter S.; Schmidhuber J. | 1997 | Neural Computation | no | no | ok | ML methodology | 95 | — | keep |
| KipfWelling2017 | references.bib | inproceedings | Semi-Supervised Classification with GCNs | Kipf T.N.; Welling M. | 2017 | ICLR | no | no | ok | GNN methodology | 95 | — | keep |
| NiculescuMizil2005 | references.bib | inproceedings | Predicting Good Probabilities with Supervised Learning | Niculescu-Mizil A.; Caruana R. | 2005 | ICML | no | no | ok | calibration | 90 | — | keep |
| Brier1950 | references.bib | article | Verification of Forecasts Expressed in Probability | Brier G.W. | 1950 | Monthly Weather Review | no | no | ok | calibration | 95 | — | keep |
| Murphy1973 | references.bib | article | A New Vector Partition of the Probability Score | Murphy A.H. | 1973 | J. Applied Meteorology | no | no | ok | calibration | 95 | — | keep |
| HanleyMcNeil1982 | references.bib | article | The Meaning and Use of the Area under ROC | Hanley J.A.; McNeil B.J. | 1982 | Radiology | no | no | ok | eval metrics | 95 | — | keep |
| Friedman1937 | references.bib | article | The Use of Ranks to Avoid Normality | Friedman M. | 1937 | JASA | no | no | ok | stats methodology | 95 | — | keep |
| Wilcoxon1945 | references.bib | article | Individual Comparisons by Ranking Methods | Wilcoxon F. | 1945 | Biometrics Bulletin | no | no | ok | stats methodology | 95 | — | keep |
| Holm1979 | references.bib | article | A Simple Sequentially Rejective Multiple Test | Holm S. | 1979 | Scand. J. Statistics | no | no | ok | stats methodology | 95 | — | keep |
| GarciaHerrera2008 | references.bib | article | An Extension on Statistical Comparisons of Classifiers | García S.; Herrera F. | 2008 | JMLR | no | no | ok | stats methodology | 90 | — | keep |
| Garcia2010 | references.bib | article | Advanced Nonparametric Tests for Multiple Comparisons | García S.; et al. | 2010 | Information Sciences | no | no | ok | stats methodology | 90 | — | keep |
| Benavoli2016 | references.bib | article | Should We Really Use Post-Hoc Tests Based on Mean-Ranks | Benavoli A.; et al. | 2016 | JMLR | no | no | ok | stats methodology | 90 | — | keep |
| Benavoli2017 | references.bib | article | Time for a Change: Comparing Multiple Classifiers | Benavoli A.; et al. | 2017 | JMLR | no | no | ok | stats methodology | 90 | — | keep |
| Nadeau2003 | references.bib | article | Inference for the Generalization Error | Nadeau C.; Bengio Y. | 2003 | Machine Learning | no | no | ok | stats methodology | 90 | — | keep |
| Dietterich1998 | references.bib | article | Approximate Statistical Tests for Comparing Classifiers | Dietterich T.G. | 1998 | Neural Computation | no | no | ok | stats methodology | 90 | — | keep |
| Bouckaert2003 | references.bib | inproceedings | Choosing Between Two Learning Algorithms | Bouckaert R.R.; Frank E. | 2003 | PAKDD | no | no | ok | stats methodology | 90 | — | keep |
| Buro2003 | references.bib | article | Real-Time Strategy Games: A New AI Research Challenge | Buro M. | 2003 | "Proc. IJCAI" (in journal field) | no | yes | type_mismatch | RTS AI | 92 | journal field holds proceedings → should be `@inproceedings`; pages 1534–1535 + url preserved | schema_change:inproceedings |
| Liquipedia_GameSpeed | references.bib | misc | Game Speed — SC2 Encyclopedia | Liquipedia | 2026 | wiki (grey-lit) | no | yes | ok | game-rule source | 60 | — | keep |
| BlizzardS2Protocol | references.bib | misc | s2protocol replay decoder | Blizzard | 2026 | repo (official) | no | yes | ok | tooling source | 70 | — | keep |
| Wikipedia_SC2Esports | references.bib | misc | SC2 World Championship Series | Wikipedia | 2026 | Wikipedia (discovery only) | no | yes | ok | context | 50 | — | keep |
| Liquipedia_ESLProTour | references.bib | misc | ESL Pro Tour — SC2 Encyclopedia | Liquipedia | 2026 | wiki (grey-lit) | no | yes | ok | context | 55 | — | keep |
| AoE2DE | references.bib | misc | Age of Empires II: Definitive Edition official site | Microsoft/Xbox | 2019 | official site | no | yes | ok | game source | 70 | — | keep |
| MgzParser | references.bib | misc | aoc-mgz AoE2 replay parser | mgz authors | 2026 | repo (official) | no | yes | ok | tooling source | 70 | — | keep |
| AoEStats | references.bib | misc | aoestats AoE2 match statistics | aoestats | 2026 | site (grey-lit) | no | yes | ok | data source | 60 | Tier 4 semantic opacity (do not call unqualified ranked) | keep |
| AoeCompanion | references.bib | misc | AoE II Companion app/API | aoe2companion | 2026 | site/API (grey-lit) | no | yes | ok | data source | 60 | — | keep |
| AoE2MapPool | references.bib | misc | Ranked Map Rotation — AoE2 DE | community | 2026 | wiki (grey-lit) | no | yes | ok | context | 55 | — | keep |
| RedBullWololoLondinium | references.bib | misc | Red Bull Wololo: Londinium tournament | Red Bull | 2026 | site (grey-lit) | no | yes | ok | context | 55 | — | keep |
| Rubin1976 | references.bib | article | Inference and Missing Data | Rubin D.B. | 1976 | Biometrika | no | no | ok | missing-data methodology | 95 | — | keep |
| vanBuuren2018 | references.bib | book | Flexible Imputation of Missing Data | van Buuren S. | 2018 | CRC Press | no | no | ok | missing-data methodology | 95 | — | keep |
| SchaferGraham2002 | references.bib | article | Missing Data: Our View of the State of the Art | Schafer J.L.; Graham J.W. | 2002 | Psychological Methods | no | no | ok | missing-data methodology | 95 | — | keep |
| FellegiSunter1969 | references.bib | article | A Theory for Record Linkage | Fellegi I.P.; Sunter A.B. | 1969 | JASA | no | no | ok | record linkage | 95 | — | keep |
| Christen2012DataMatching | references.bib | book | Data Matching | Christen P. | 2012 | Springer | no | no | ok | record linkage | 95 | — | keep |
| Jakobsen2017 | references.bib | article | When and how should multiple imputation be used | Jakobsen J.C.; et al. | 2017 | BMC Med. Res. Methodol. | no | no | ok | missing-data methodology | 90 | — | keep |
| MadleyDowd2019 | references.bib | article | The proportion of missing data should not be used | Madley-Dowd P.; et al. | 2019 | J. Clin. Epidemiology | no | no | ok | missing-data methodology | 90 | — | keep |
| Nakagawa2017 | references.bib | article | The coefficient of determination R2 and ICC | Nakagawa S.; et al. | 2017 | J. R. Soc. Interface | no | no | ok | stats methodology | 90 | — | keep |
| Chung2013 | references.bib | article | Avoiding zero between-study variance estimates | Chung Y.; et al. | 2013 | Statistics in Medicine | no | no | ok | stats methodology | 90 | — | keep |
| Ukoumunne2003 | references.bib | article | Non-parametric bootstrap CIs for the ICC | Ukoumunne O.C. | 2003 | Statistics in Medicine | no | no | ok | stats methodology | 90 | — | keep |
| WuCrespiWong2012 | references.bib | article | Comparison of methods for estimating the ICC | Wu S.; Crespi C.M.; Wong W.K. | 2012 | Contemp. Clinical Trials | no | no | ok | stats methodology | 90 | — | keep |
| Gelman2007 | references.bib | book | Data Analysis Using Regression and Multilevel Models | Gelman A.; Hill J. | 2007 | Cambridge UP | no | no | ok | stats textbook | 95 | — | keep |
| Minami2024 | references.bib | article | Prediction of esports competition outcomes using EEG | Minami; et al. | 2024 | — | no | no | ok | esports pred | 75 | — | keep |
| Shin1993 | references.bib | article | Measuring the Incidence of Insider Trading | Shin H.S. | 1993 | Economic Journal | no | no | ok | betting-market econ | 85 | — | keep |
| Forrest2005 | references.bib | article | Odds-setters as forecasters | Forrest D.; et al. | 2005 | Int. J. Forecasting | no | no | ok | betting-market econ | 85 | — | keep |
| Levitt2004 | references.bib | article | Why are gambling markets organised so differently | Levitt S.D. | 2004 | Economic Journal | no | no | ok | betting-market econ | 85 | — | keep |
| Mangat2024 | references.bib | article | Understanding Esports-related Betting and Gambling | Mangat H.S.; et al. | 2024 | J. Gambling Studies 40(2):893–914 | yes | no | ok | esports betting | 90 | corrected & web-verified in PR #222; re-confirmed present/correct, no change | keep |
| Formosa2022 | references.bib | article | Definitions of Esports: A Systematic Review | Formosa J.; et al. | 2022 | — | no | no | ok | esports definition | 85 | — | keep |
| Novak2025 | references.bib | article | The legal and economic aspects of the Esports Illusion | Pál et al. | 2025 | Front. Sports Act. Living 7:1636823 | yes | no | ok | esports econ | 90 | corrected & web-verified in PR #222 (first author Pál); re-confirmed, no change | keep |
| Balduzzi2018 | references.bib | inproceedings | Re-evaluating Evaluation | Balduzzi D.; et al. | 2018 | NeurIPS | no | no | ok | eval methodology | 90 | — | keep |

### B. Markdown-extracted rows (named / alias / flagged keys; 12 rows)

| key | source_file | entry_type | title | authors | year | venue | doi | url | status | relevance | confidence | note | action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Wu2017 | references.bib | article | MSC: A Dataset for Macro-Management in SC2 | Wu H.; Zhang J.; Huang K. | 2017 | arXiv preprint (id in Sources) | no | no | intra_bib_dup | dataset | 99 | cited `[Wu2017]` 0 sites under thesis/ (re-grepped on HEAD) | merge_into:Wu2017MSC |
| Wu2017MSC | thesis/chapters + appendix | article | MSC: A Dataset for Macro-Management in SC2 | Wu H.; Zhang J.; Huang K. | 2017 | arXiv preprint (id in Sources) | no | no | ok | dataset (canonical) | 99 | `[Wu2017MSC]` cited on 8 lines (appendix 3 + Ch2 2 + Ch3 1 + Ch4 2) | keep |
| Baek2022 | related_work_historical_rts_prediction.md (embedded bibtex) | article | 3D CNNs for predicting SC2 results | Baek I.; Kim S.B. | 2022 | PLOS ONE 17(3):e0264550 | yes (PLOS ONE DOI; see Sources) | no | bib_md_alias_drift | core SC2 pred | 95 | appendix-only alias of bib `BaekKim2022`; same work; chapters cite `[BaekKim2022]` | flag_bib_vs_md_drift |
| Porcpine2020 | related_work_rating_systems.md (embedded bibtex L577) | misc | Impact of Rating Difference on Win % in AoE2 DE | porcpine1967 | 2020 | GitHub Pages (grey-lit) | no | yes | bib_md_alias_drift | AoE2 Elo baseline | 90 | appendix-only alias of bib `Porcpine2020EloAoE`; same work | flag_bib_vs_md_drift |
| Herbrich2007 | related_work_rating_systems.md (embedded bibtex L482) | inproceedings | TrueSkill: A Bayesian Skill Rating System | Herbrich R.; Minka T.; Graepel T. | 2007 | Proc. NeurIPS 2006, pp.569–576 | no | no | bib_md_alias_drift | rating systems | 90 | appendix-only; same NeurIPS-2006 paper as bib `Herbrich2006`; **2007 is bibliographically defensible** (MSR page: "NeurIPS 20, January 2007") — key/style drift, NOT a year error | flag_bib_vs_md_drift |
| Glickman2025 | related_work_rating_systems.md (embedded bibtex L450) | article | Models and Rating Systems for Head-to-Head Competition | Glickman M.E.; **Jones Alexander C.** | 2025 | Annu. Rev. Stat. 12:259–282 | yes | no | bib_md_alias_drift | rating systems survey | 98 | second-author typo: appendix "Alexander C." vs central bib + Crossref "Albyn C." | flag_bib_vs_md_drift |
| BT2025Survey | related_work_rating_systems.md (embedded bibtex L313) | article | Recent advances in the Bradley-Terry Model | Li Y.; +others | 2025 | arXiv:2601.14727 | no | no | appendix_only | rating systems survey | 50 | appendix-only grey-lit; future-dated arXiv id; no DOI; uncited in chapters | manual_decision |
| Dimitriadis2024 | related_work_rating_systems.md (embedded bibtex L366) | article | Evaluating probabilistic classifiers: The triptych | Dimitriadis T.; Gneiting T.; Jordan A.I. | 2024 | Int. J. Forecasting 40(1):189–210 | no | no | identity_collision | calibration eval | 92 | appendix copy carries the same early/incorrect metadata as the central bib (40(1):189–210, 3 authors, no DOI); appendix read-only this PR | flag_bib_vs_md_drift |
| Dimitriadis2024 | literature_verification_log.md:78 | article | Evaluating probabilistic classifiers: The triptych | Dimitriadis T.; Gneiting T.; Jordan A.I. | 2024 | Int. J. Forecasting 40(1):189–210 | no | no | identity_collision | calibration eval | 92 | prior-audit statement "40(1) 189–210; verified-from-prior-pass" is SUPERSEDED — see "Stale prior-audit statements superseded" | flag_bib_vs_md_drift |
| Khan2024SCPhi2 ("SC-Phi2") | 03_related_work.md, REVIEW_QUEUE.md | article | SC-Phi2 (label) → Khan2024SCPhi2 (bibkey) | Khan M.J.; Sukthankar G. | 2024 | AI (MDPI) 5(4):2338–2352 | yes | no | label_not_bibkey | SC pred | 98 | "SC-Phi2" is the user's documentation label; chapters cite the bibkey `[Khan2024SCPhi2]` correctly | keep |
| Bahrololloomi2023 | references.bib (5-file extraction; no divergent md copy) | article | E-Sports Player Performance Metrics (LoL) | Bahrololloomi F.; Klonowski F.; Sauer S.; Horst R.; Dörner R. | 2023 | SN Computer Science 4(3) art.238 | yes | no | ok | esports pred | 90 | Crossref-confirmed; no markdown drift copy found | keep |
| Glickman1995 | references.bib (5-file extraction; no divergent md copy) | unpublished | A Comprehensive Guide to Chess Ratings | Glickman M.E. | 1995 | American Chess Journal v.3:59–102 | no | no | metadata_mismatch | rating systems foundations | 85 | verified via author's official page; ACJ not DOI-indexed (no DOI is correct, NOT a fabrication gap) | manual_decision |

---

## Four user-named "pairs" — verified true state (transcribed from `planning/current_plan.md`)

| user pair | true on-disk state | operation | canonical | alias | remap (report-only) |
|---|---|---|---|---|---|
| `Wu2017`+`Wu2017MSC` | both in bib, byte-identical; `Wu2017` cited 0x, `Wu2017MSC` 8 lines | **intra-bib dedup** (delete `Wu2017`, gated by zero-citation grep) | `Wu2017MSC` | `Wu2017` (deleted) | `Wu2017 → Wu2017MSC` |
| `BaekKim2022`+`Baek2022` | `Baek2022` NOT in bib (appendix-only, `related_work_historical_rts_prediction.md`); same work; chapters cite `[BaekKim2022]` | bib↔md alias drift (report-only) | `BaekKim2022` | `Baek2022` (appendix) | `Baek2022 → BaekKim2022` |
| `Porcpine2020EloAoE`+`Porcpine2020` | `Porcpine2020` NOT in bib (appendix-only, `related_work_rating_systems.md`); same work | bib↔md alias drift (report-only) | `Porcpine2020EloAoE` | `Porcpine2020` (appendix) | `Porcpine2020 → Porcpine2020EloAoE` |
| `Herbrich2006`+`Herbrich2007` | `Herbrich2007` NOT in bib (appendix-only, year 2007); same TrueSkill NeurIPS-2006 paper; **2007 is defensible — MSR page: "NeurIPS 20, January 2007"** | bib↔md **key/style** drift (report-only; NOT a year-error claim) | `Herbrich2006` (bib) | `Herbrich2007` (appendix) | `Herbrich2007 → Herbrich2006` (key normalization for follow-up PR; NO assertion that 2007 is wrong) |

> Note (reviewer-deep nit 1): the `Wu2017MSC` citation total is the
> **counted** value (8 lines on disk: appendix 3 + Ch2 2 + Ch3 1 + Ch4 2),
> re-grepped on `HEAD`. The safety gate keys only on the exact *zero*
> `[Wu2017]` count, which was re-confirmed as 0.

---

## Alias remap list (report deliverable; report-only this PR)

```
Wu2017       -> Wu2017MSC          (intra-bib true dup; Wu2017 deleted; 0 citation sites)
Baek2022     -> BaekKim2022        (bib<->md drift; appendix-only alias; follow-up PR)
Porcpine2020 -> Porcpine2020EloAoE (bib<->md drift; appendix-only alias; follow-up PR)
Herbrich2007 -> Herbrich2006       (bib<->md key/style drift; year 2007 defensible; follow-up PR — key normalization, not a date correction)
SC-Phi2      -> Khan2024SCPhi2     (user label, not a bibkey; documentation note only; no bib entry to remap)
```

---

## Manual-decision list (`action=manual_decision`, NO auto-change)

(transcribed from `planning/current_plan.md`)

- `BT2025Survey` — appendix-only grey-lit, future-dated arXiv id, no DOI,
  uncited in chapters.
- `Chen2020` — in bib; missing pages/DOI, ambiguous LNCS volume.
- `Lee2021Combat` — in bib, complete metadata; relevance scoping is a
  human call.
- `Lin2019NP` — in bib; truncated `and others` author list.
- `Vinyals2019` — in bib; truncated `and others` (Nature long author
  list — editorial).
- `Aligulac` — in bib `@misc` year 2026; grey-lit live site, editorial
  date convention.
- `Glickman1995` — verified metadata at ≥80 via the author's official
  page, but the `@unpublished`→`@article` type change on an obscure
  non-DOI-indexed venue is an editorial call (user flagged this as
  manual); T03 does NOT auto-apply it.

---

## bib↔markdown drift list (report deliverable; transcribed)

1. `Baek2022` (appendix) ↔ `BaekKim2022` (bib) — same work, divergent key.
2. `Porcpine2020` (appendix) ↔ `Porcpine2020EloAoE` (bib) — same work.
3. `Herbrich2007` (appendix, 2007) ↔ `Herbrich2006` (bib, 2006) — same
   NeurIPS-2006 paper; **key/style + year-style drift, NOT a factual
   error** (2007 defensible per MSR "NeurIPS 20, January 2007").
4. `SC-Phi2` (user label) ↔ `Khan2024SCPhi2` (bib) — label vs bibkey;
   chapters/log use the bibkey correctly.
5. `BT2025Survey` — appendix-only, never in bib/chapters.
6. `Glickman2025` — central bib correct (Crossref); the
   `rating_systems` appendix copy has a **second-author typo**
   ("Alexander C." vs the correct "Albyn C.") — catalogued; appendix
   read-only this PR.
7. The two appendixes carry standalone divergent BibTeX blocks (working
   materials, scope #8) — catalogued, not reconciled.

---

## Schema-change specifics (key-stable; zero citation blast radius)

(transcribed from `planning/current_plan.md`, with reviewer-deep nit 4
title-form decision folded in)

- **`Elo1978`**: `@article` (publisher Arco, no journal) → `@book`,
  `publisher = {Arco Publishing}`, `address = {New York}`, **key
  UNCHANGED**.
  - **Title-form decision (reviewer-deep nit 4):** the current bib
    (`thesis/references.bib:129`) has "The Rating of **Chessplayers**,
    Past and Present" (one word "Chessplayers"). The canonical /
    appendix form is "The Rating of **Chess Players**, Past and
    Present" (two words). **T03 applies the two-word canonical form**;
    this is an explicit, recorded title normalization with
    **confidence ~90**, NOT a silent change.
  - Schema-change confidence: 95; key unchanged → zero citation blast
    radius.
- **`Buro2003`**: `@article` (journal field = IJCAI proceedings) →
  `@inproceedings`, `booktitle = {Proceedings of the 18th International
  Joint Conference on Artificial Intelligence (IJCAI)}`, existing
  `pages = {1534--1535}` + `url` preserved, **key UNCHANGED**.
  Confidence 92.
- **`Glickman1995`**: currently `@unpublished` (American Chess Journal
  v.3, 1995, pp.59–102). Verified ≥80 via the author's official
  research page; **no DOI (American Chess Journal is not DOI-indexed —
  correctly absent, NOT a fabrication gap)**. The `@unpublished`→
  `@article` type change is an editorial call on an obscure venue →
  `action=manual_decision`; the report documents the verified metadata
  and recommended enrichment, but **T03 does NOT auto-apply it**.
  Current-entry confidence 85 on the metadata.

**Key-stability:** none of `Elo1978`/`Buro2003`/`Glickman1995` is
renamed; the only deleted key is `Wu2017` (0 citation sites, re-gated).
All `thesis/chapters/` citation sites stay valid.

---

## Per-field verification diffs (FROZEN — not re-derived)

### `Khan2024SCPhi2` — confidence 98 — action keep

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| venue | AI (MDPI) | AI (MDPI) | Crossref | yes |
| volume/number | 5(4) | 5(4) | Crossref | yes |
| pages | 2338--2352 | 2338–2352 | Crossref | yes |
| year | 2024 | 2024 | Crossref | yes |
| doi | (in `doi` field) | (matches) | Crossref | yes |

Note: "SC-Phi2" is the user's label, NOT a bibkey — documentation note.

### `Bahrololloomi2023` — confidence 90 — action keep

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| venue | SN Computer Science | SN Computer Science | Crossref | yes |
| volume/number | 4 (art.238) | 4(3) art.238 | Crossref | yes |
| year | 2023 | 2023 | Crossref | yes |
| doi | (in `doi` field) | (matches; online-first suffix noted in bib `note`) | Crossref/Springer | yes |

### `Glickman2025` — confidence 98 — action keep (central bib correct)

| field | bib_value (central) | verified_value | source | match? |
|---|---|---|---|---|
| venue | Annual Review of Statistics and Its Application | (same) | Crossref | yes |
| volume/pages | 12:259–282 | 12:259–282 | Crossref | yes |
| author 2 | Jones, Albyn C. | Jones, Albyn C. | Crossref | yes |
| doi | (in `doi` field) | (matches) | Crossref | yes |

The `related_work_rating_systems.md` appendix copy (L451) has a
**second-author typo** ("Jones, Alexander C."); catalogued in the drift
list; the appendix is READ-ONLY this PR.

### `Bialecki2023` (reviewer-deep nit 3) — confidence 95 — action keep — NO bib edit

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| venue | Scientific Data 10:600 | Scientific Data 10 art.600 | Crossref | yes |
| year | 2023 | 2023 | Crossref | yes |
| authors (ordered, 8) | Białecki A.; Jakubowska N.; Dobrowolski P.; Białecki P.; Krupiński L.; Szczap A.; Białecki R.; Gajewski J. | identical 8-author ordered list | Crossref + PMC + arXiv | yes |
| doi | (in `doi` field) | (matches) | Crossref | yes |

The official record returns the **identical 8-author ordered list
already at `thesis/references.bib:5-13`** (Crossref + PMC `PMC10491788`
+ arXiv `2207.03428`). The user's "author mismatch" concern **does NOT
reproduce**. `status=ok`, **action=keep — NO bib edit**; no fix is
manufactured.

### `Dimitriadis2024` (reviewer-deep nit 2 — CLOSED identity) — confidence 92 — action fix_metadata

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| title | Evaluating probabilistic classifiers: The triptych | (identical) | Crossref/RePEc/ScienceDirect/arXiv | yes (same work) |
| volume | 40 | 40 | Crossref | yes |
| number | 1 | **3** | Crossref/ScienceDirect | **no** |
| pages | 189--210 | **1101--1122** | Crossref/ScienceDirect | **no** |
| authors | Dimitriadis T.; Gneiting T.; Jordan A.I. (3) | Dimitriadis T.; Gneiting T.; Jordan A.I.; **Vogel, Peter** (4) | Crossref/RePEc/arXiv | **no (Vogel missing)** |
| doi | (absent) | (the IJF DOI; see Sources) | Crossref | **no (absent in bib)** |

**Identity adjudication (CLOSED):** the Crossref DOI is the **SAME
"triptych" work** as the repo's `Dimitriadis2024` — identical title;
its arXiv preprint (id in Sources) is the same work — published
*International Journal of Forecasting* **40(3):1101–1122**, 4 authors
**Dimitriadis, Gneiting, Jordan, Vogel** (4 concurring sources:
Crossref + RePEc + ScienceDirect + arXiv). The repo bib's
`40(1):189–210, 3 authors, no DOI` is early/incorrect metadata.
`status=identity_collision → RESOLVED (same work)`, confidence 92,
**action=fix_metadata**. Per the user's Q3 step (2) the key stays the
triptych record → T03 corrects it to the published version (volume 40,
number 3, pages 1101--1122, add the IJF DOI, add 4th author
"Vogel, Peter"). No new key; no overwrite of a different work.

### `Elo1978` — confidence ~90 (title-form) — action schema_change:book (reviewer-deep nit 4)

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| entry_type | `@article` (publisher Arco, no journal) | `@book` (publisher Arco Publishing) | bibliographic | no |
| title | The Rating of **Chessplayers**, Past and Present (one word, `thesis/references.bib:129`) | The Rating of **Chess Players**, Past and Present (two words) | canonical / appendix form | no |
| publisher | Arco Publishing (in `publisher` field) | Arco Publishing | bibliographic | yes |
| address | (absent) | New York | bibliographic | no (to add) |
| year | 1978 | 1978 | bibliographic | yes |
| key | Elo1978 | Elo1978 (UNCHANGED) | — | yes |

The current bib has "Chessplayers" (one word, `thesis/references.bib:129`);
the canonical / appendix form is "Chess Players" (two words). T03
applies the **two-word canonical form** at confidence ~90 — an
explicit, recorded title normalization, NOT a silent change. Key
unchanged → zero citation blast radius.

### `Glickman1995` — confidence 85 (metadata) — action manual_decision

| field | bib_value | verified_value | source | match? |
|---|---|---|---|---|
| title | A Comprehensive Guide to Chess Ratings | A Comprehensive Guide to Chess Ratings | author official page | yes |
| venue | American Chess Journal v.3 (1995), pp.59–102 (in `note`) | American Chess Journal, vol. 3, pp. 59–102, 1995 | author official page + corroboration | yes |
| year | 1995 | 1995 | author official page | yes |
| doi | (absent) | (none — ACJ not DOI-indexed) | — | yes (correctly absent) |
| entry_type | `@unpublished` | `@article` (recommended) | editorial | n/a — manual |

Verified ≥80 via the author's OFFICIAL research page (glicko.net
research / `acjpaper.pdf`) plus corroboration: M. E. Glickman,
"A Comprehensive Guide to Chess Ratings", American Chess Journal,
vol. 3, pp. 59–102, 1995. **No DOI is correct (American Chess Journal
is not DOI-indexed) — NOT a fabrication gap.** The `@unpublished`→
`@article` type change is an editorial call on an obscure venue →
`action=manual_decision`; T03 does NOT auto-apply it.

---

## Schema changes to apply at T03

- **`Elo1978` `@article`→`@book`** — `publisher = {Arco Publishing}`,
  `address = {New York}`, **key UNCHANGED**. **Title-form decision
  (reviewer-deep nit 4):** current bib has "The Rating of
  **Chessplayers**, Past and Present" (one word "Chessplayers",
  `thesis/references.bib:129`); the canonical / appendix form is
  "**Chess Players**" (two words). **T03 applies the two-word canonical
  form**, confidence ~90 — explicitly recorded, NOT a silent
  normalization.
- **`Buro2003` `@article`→`@inproceedings`** — `booktitle =
  {Proceedings of the 18th International Joint Conference on Artificial
  Intelligence (IJCAI)}`, existing `pages = {1534--1535}` + `url`
  preserved, **key UNCHANGED**, confidence 92.

Both keys are preserved → **zero citation blast radius** across
`thesis/chapters/`.

`Glickman1995` is NOT in this auto-apply set — it is
`action=manual_decision` (see Manual-decision list); the verified
metadata and recommended `@article` enrichment are documented for a
human editorial decision, not auto-applied at T03.

---

## Stale prior-audit statements superseded (reviewer-deep nit 2)

The prior `thesis/pass2_evidence/literature_verification_log.md`
(line 78) carries `Dimitriadis2024` as *Int. J. Forecasting*
**40(1):189–210**, "triptych framework", "verified-from-prior-pass",
with **no DOI**. **This statement is SUPERSEDED.** The identity is now
**CLOSED**: the Crossref DOI record is the **same triptych paper**,
published *International Journal of Forecasting* **40(3):1101–1122**
with **Peter Vogel as the 4th author** (arXiv preprint
arXiv preprint, id in Sources), confirmed by four concurring sources (Crossref +
RePEc + ScienceDirect + arXiv).

This is stated as **CLOSED**, not as an open "may be a different
paper". This report supersedes that prior statement **in the
chapter/bib lineage only**; the prior `literature_verification_log.md`
file itself is READ-ONLY this PR and is not edited here. The
corresponding `references.bib` correction is applied at T03 (per the
`Dimitriadis2024` per-field diff), not in this T02 commit.

No other stale prior-audit statement was found in the five scoped
files for the named/flagged keys (the `ch1_ch4_citation_literature_support_audit.md`
`Dimitriadis2024` mention is a bibkey-existence spot-check, not a
metadata claim, so it is not superseded by metadata change).

---

## Candidate appendix follow-up PR (separate, separately-approved — NOT done here)

`thesis/reviews_and_others/**` and `thesis/chapters/**` are **READ-ONLY
this PR**. The following concrete normalizations are listed for a
SEPARATE, separately-approved follow-up PR — none is performed here:

- `Baek2022 → BaekKim2022` (appendix key/style normalization to the
  canonical bib key).
- `Porcpine2020 → Porcpine2020EloAoE` (appendix key/style
  normalization).
- `Herbrich2007 → Herbrich2006` — **key/style normalization, NOT a
  year correction.** The year 2007 is bibliographically defensible: the
  official Microsoft Research page lists the paper as "Advances in
  Neural Information Processing Systems 20 | January 2007". The
  follow-up PR may normalize the appendix key/style; it MUST NOT assert
  that 2007 is a factual error.
- `Glickman2025` appendix second-author typo: appendix
  "Jones, Alexander C." → correct "Jones, Albyn C." (matches central
  bib + Crossref).
- Optional: dedup of the two appendixes' divergent embedded BibTeX
  blocks against the canonical `thesis/references.bib`.

---

## Wu2017 dedup (reviewer-deep nit 1)

`Wu2017` ≡ `Wu2017MSC` are byte-identical apart from the key.
On-disk citation grep, re-run on `HEAD`:

- `grep -rEno '\[Wu2017\]' thesis/ | wc -l` → **0** (`[Wu2017]` cited
  0 times).
- `grep -rEno '\[Wu2017MSC\]' thesis/ | wc -l` → **8** (counted value:
  `related_work_historical_rts_prediction.md` 3 + `02_theoretical_background.md`
  2 + `03_related_work.md` 1 + `04_data_and_methodology.md` 2 = 8
  lines; appendix 3 + Ch2 2 + Ch3 1 + Ch4 2).

**Action:** T03 deletes the `@article{Wu2017, …}` block ONLY after
re-confirming `grep -rEno '\[Wu2017\]' thesis/` == 0 at execution time
(safety gate). `Wu2017MSC` is not touched. This report records the
**counted on-disk** `Wu2017MSC` value (8 cited lines), superseding the
plan's earlier narrative figure of seven occurrences (reviewer-deep
nit 1: use the counted value, not the narrative one).

---

## Audit-only assertion

`thesis/references.bib` was **NOT edited** in this (T02) commit. This
report is the frozen evidence base; the evidence-safe corrections it
specifies (`Wu2017` dedup gated; `Dimitriadis2024` fix_metadata to the
published triptych version; `Elo1978`→`@book` with two-word title;
`Buro2003`→`@inproceedings`) are applied separately at T03 under the
≥80-confidence / identity-safe / zero-chapter-blast-radius gate.
`Bialecki2023` and `Glickman2025` central bib = no edit (verified
match). `Glickman1995` = manual decision, not auto-applied.

## Sources (URLs / DOIs — fenced; never in prose)

```
Crossref Baek2022/BaekKim2022    : 10.1371/journal.pone.0264550
Crossref Khan2024SCPhi2          : 10.3390/ai5040115
Crossref Bahrololloomi2023       : 10.1007/s42979-022-01660-6
Crossref Glickman2025            : 10.1146/annurev-statistics-040722-061813
Crossref Bialecki2023            : 10.1038/s41597-023-02510-7
Bialecki2023 corroboration       : PMC PMC10491788 ; arXiv 2207.03428
Crossref Dimitriadis2024 (triptych, published) : 10.1016/j.ijforecast.2023.09.007
Dimitriadis2024 preprint         : arXiv:2301.10803
Dimitriadis2024 corroboration    : RePEc + ScienceDirect + arXiv (4 concurring sources w/ Crossref)
Glickman1995 official source     : glicko.net research / acjpaper.pdf (American Chess Journal vol. 3, pp. 59-102, 1995)
PR #222 reuse                    : Mangat2024 10.1007/s10899-023-10256-5 ; Novak2025 10.3389/fspor.2025.1636823
Herbrich2007 defensibility       : Microsoft Research page "Advances in Neural Information Processing Systems 20 | January 2007"
```
