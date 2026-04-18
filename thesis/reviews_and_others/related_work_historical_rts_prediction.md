# Historical treatment of match outcome prediction in real-time strategy games

**Purpose.** Supplementary literature review for the thesis's Related Work chapter, establishing how the academic community has treated RTS match outcome prediction from the 1990s through 2023. Complements the separate 2024–2026 bibliography and the non-ML rating systems review.
**Scope.** Games covered: StarCraft: Brood War, StarCraft II, Age of Empires II, and contextual mentions of Warcraft III, Command & Conquer, Total War, Wargus/Stratagus, and microRTS. Time window: 1990s through end of 2023. Post-2023 work is out of scope for this document.
**Date.** 2026-04-13.
**Intended use.** Source material for the `thesis-writer` agent to draft §2 Related Work (Historical). All factual claims are attributed to specific sources in the References section. Reference keys use the project's `[AuthorYear]` convention per `docs/THESIS_WRITING_MANUAL.md`.

## Summary of the historical arc

RTS match outcome prediction has been an evolving academic pursuit for over two decades, yet it remains dramatically uneven in its coverage across game titles. StarCraft — first Brood War, then StarCraft II — absorbed nearly the entire field's attention, progressing from rule-based bots through Bayesian models to deep learning, while Age of Empires II accumulated precisely two relevant papers before 2024 and every other commercial RTS title received none. This asymmetry is not accidental: it was driven by the availability of programmatic APIs, competition infrastructure, professional replay data, and a self-reinforcing academic ecosystem. The narrative below traces this three-decade arc as historical context for a comparative SC2–AoE2 prediction thesis, identifying the methodological lineage, the enabling infrastructure, and the gaps that such a thesis can address.

> **Affiliation note.** The group most directly relevant to the thesis — Andrzej Białecki's research line — is affiliated with Warsaw University of Technology (Politechnika Warszawska), not PJAIT. His verified institutional email is at pw.edu.pl. This matters when situating the thesis within the Polish academic landscape: Białecki's SC2EGSet line [Bialecki2023] is the most important local research lineage but not an in-house PJAIT line.

## §1 — Before academia noticed (1990s–2005)

The RTS genre crystallized rapidly in the 1990s. Dune II (Westwood Studios, 1992) established the template: resource harvesting, base construction, and real-time combat. Warcraft: Orcs & Humans (1994) and Command & Conquer (1995) popularized the formula. Age of Empires (1997) introduced historical settings and asymmetric civilizations. Then, in March 1998, Blizzard released StarCraft, followed by the Brood War expansion in November — and the competitive landscape shifted permanently.

South Korea transformed StarCraft: Brood War into the world's first mass-audience esport. By 2000, dedicated television channels OnGameNet (OGN) and MBCGame were broadcasting professional StarCraft leagues to millions. The Korea e-Sports Association (KeSPA) formalized player licensing, team management, and broadcasting rights. Corporate-sponsored teams — SK Telecom T1, KT Rolster, Samsung Khan — employed salaried professional players. The OnGameNet Starleague (OSL) and MBCGame StarCraft League (MSL) ran continuously, and KeSPA's Proleague (from 2003) became the premier team competition, operating until 2016. This professional infrastructure generated thousands of expert-level replays — a data resource no other RTS could match.

Community platforms emerged to serve this ecosystem. TeamLiquid.net, founded in 2001, became the preeminent English-language hub for StarCraft discussion, news translation from Korean, and replay sharing. It later spawned the Team Liquid Progaming Database (TLPD), cataloguing every professional match, and Liquipedia, a comprehensive esports wiki. GosuGamers, founded in 2002, maintained a replay archive of approximately 7,930 Brood War replays before ceasing additions in April 2013. ICCup (International Cyber Cup), launched in November 2007, operated a private Battle.net server with a competitive ladder and became a critical replay source for both the foreign and Korean communities through approximately 2010.

BWChart, created by JCA, was the first widely used replay analysis tool — calculating APM (actions per minute), plotting resource charts, and even detecting hacks from replay data. It represented the earliest systematic extraction of quantitative data from RTS replays at a community level, anticipating the academic replay-mining work that would follow by several years.

Age of Empires II (1999) developed its own competitive scene, though on a far smaller scale. AoE2 appeared at the World Cyber Games in 2000, 2001, and 2002. Microsoft's MSN Gaming Zone provided early online play until Microsoft terminated support in 2006. Voobly, launched in 2009, became the primary competitive platform, paired with community mods like UserPatch and WololoKingdoms. The scene remained grassroots and community-driven, with no equivalent to Korea's broadcast infrastructure or corporate team system, until the Definitive Edition (November 2019) triggered a resurgence with tournaments like Red Bull Wololo and Hidden Cup.

Meanwhile, a handful of AI researchers began recognizing RTS games as fertile ground. [Laird2001] published "Human-Level AI's Killer Application: Interactive Computer Games" in *AI Magazine*, one of the first AAAI publications identifying real-time games as excellent AI research environments. The decisive intervention came from Michael Buro at the University of Alberta, who published two foundational papers: [Buro2002] introducing ORTS (Open Real-Time Strategy), an open-source RTS engine with server-side simulation preventing client-side hacking; and [Buro2003], the seminal position paper arguing that RTS games posed novel AI challenges combining resource management, adversarial planning, spatial reasoning, decision-making under uncertainty, and opponent modeling. The 2003 IJCAI paper is widely cited as the founding document of RTS AI research.

ORTS competitions ran annually from 2006 to 2009 at AIIDE conferences. Meanwhile, the Stratagus engine (2004) and its Warcraft II-based game definition Wargus provided another open-source testbed. [Ponsen2004] used Wargus for evolutionary learning of game AI tactics; [Ponsen2005] extended this with adaptive game AI; [McCoy2008] demonstrated an integrated ABL (A Behavior Language) agent in Wargus. However, Wargus lacked replays, an active player base, and networking infrastructure for bot-vs-bot testing. It would be superseded entirely once BWAPI opened StarCraft itself.

[Hsieh2008] applied case-based reasoning to learn player strategies from StarCraft: BW build orders — one of the earliest papers using actual StarCraft replays for AI research, predating BWAPI.

Throughout this pre-academic period, no paper attempted to predict match outcomes in any RTS game. The intellectual groundwork was being laid — data was accumulating in community archives, APIs were being prototyped, and AI researchers were framing the challenge — but direct prediction work would require the infrastructure that emerged next.

## §2 — BWAPI ignites a research ecosystem (2006–2015)

The release of BWAPI (Brood War Application Programming Interface) around 2009, created by Michal "Kovarex" Kovarik and later maintained by Adam Heinermann, was the single most consequential event in RTS AI research history. BWAPI provided programmatic access to StarCraft: BW — reading game state, controlling individual units, and parsing replays frame-by-frame, all while respecting fog-of-war constraints. An ecosystem of companion tools followed: BWTA/BWTA2 for terrain analysis, SparCraft (David Churchill) for combat simulation, and Java wrappers (JNIBWAPI, BWMirror) enabling broader participation. Later, [Synnaeve2016TorchCraft] bridged StarCraft to machine learning frameworks.

### The competition infrastructure

Three annual competitions created standardized benchmarks and attracted a global research community. The **AIIDE StarCraft AI Competition** (from 2010) was organized initially by Ben Weber at UC Santa Cruz, later by David Churchill and Michael Buro at the University of Alberta (2011–2016). The first event drew 26 entrants; Overmind (UC Berkeley) won the inaugural competition. Full 1v1 games with fog-of-war were run 24/7 at superhuman speed for approximately two weeks per round-robin, with required source code submission and public release afterward. The **CIG StarCraft Competition** (from 2011) was co-located with the IEEE Conference on Computational Intelligence and Games, organized by Mike Preuss and collaborators (2011–2013), then by Kyung-Joong Kim's team at Sejong University. **SSCAIT (Student StarCraft AI Tournament)** (from 2011), created by Michal Čertický at Comenius University, Bratislava, began as a local course event for ~50 students and expanded internationally, distinctively operating a continuous live ladder with streaming.

The authoritative reference documenting all three competitions is [Certicky2019], "StarCraft AI Competitions, Bots, and Tournament Manager Software," published in *IEEE Transactions on Games*.

Competition results were themselves a form of outcome prediction data: comparing bot architectures across thousands of automated matches provided empirical evidence about which strategic approaches dominated. However, the competitions evaluated agent design, not predictive modeling per se.

### From strategy prediction to outcome prediction

The academic literature of this period followed a clear progression from opponent modeling through plan recognition to direct outcome prediction.

[Weber2009Data] is the foundational opponent modeling paper. It encoded SC:BW replays as feature vectors using first production time of each unit/building type, built a dataset of 5,493 replays from GosuGamers, TeamLiquid, and ICCup, and demonstrated that data mining can predict opponent strategies even under imperfect information. This paper established the replay-mining methodology that all subsequent prediction work would build upon. [Weber2009CBR] applied case-based reasoning to build order selection, showing domain-specific case retrieval outperforms nearest-neighbor under imperfect information.

[Synnaeve2011Opening] presented a Bayesian model for predicting opponent opening strategies, with parameters learned from replays via semi-supervised EM. General enough for any RTS with tech trees. One of the most cited SC:BW plan recognition papers. [Synnaeve2011Plan] extended their Bayesian approach to full build-tree (tech tree) prediction from noisy observations using unsupervised learning.

[Dereszynski2011] used Hidden Markov Models to learn probabilistic models of high-level strategic behavior from game logs. Crucially, their approach was not biased by preconceived strategic categories — strategic states were discovered automatically. This paper demonstrated that latent strategy states could be inferred and used for prediction.

[Churchill2011BuildOrder] formulated build order planning as a constraint resource allocation problem with makespan minimization. They developed a depth-first branch-and-bound search producing near-optimal build orders that matched professional player timings. This became the foundation of the UAlbertaBot system.

[Hostetler2012] extended the HMM work to handle partial observability (limited scouting), using dynamic Bayesian networks combining strategy generation with scouting evidence.

The field's first major consolidation came with the survey that remains the most-cited paper in the domain: [Ontanon2013]. It decomposed RTS AI into hierarchical levels (strategy, tactics, reactive control, terrain analysis, intelligence gathering), surveyed all existing SC:BW approaches, reviewed the AIIDE and CIG competitions, analyzed seven bot architectures from source code, and identified open problems. It established the taxonomy used by virtually all subsequent work.

### Direct outcome prediction emerges

The transition from strategy classification to explicit match winner prediction happened between 2013 and 2016.

[Stanescu2013] presented a Bayesian model for predicting outcomes of isolated battles and determining what units would be needed to defeat a given army, with parameters learned from simulated battles. This was battle-level, not match-level, prediction — but it established the principle that game states contain enough information for probabilistic outcome estimation.

[Erickson2014] was the first rigorous attempt at predicting which player will win a SC:BW match from game state. They used logistic regression on features extracted via BWAPI from replays: resources, buildings, units, map control, and novel player skill metrics derived from battle simulation baselines. Limited to Protoss vs. Protoss matches (~400 replays). Prediction accuracy improved with game progression. This paper is cited by virtually every subsequent SC2 outcome prediction study.

[Ravari2016] produced the most comprehensive SC:BW winner prediction study, extending Erickson and Buro (2014) to all six race matchups (PvT, PvZ, TvZ, PvP, ZvZ, TvT). They used random forest and gradient boosting models, achieving >63% average accuracy across all time slices. They found that economic features are the strongest predictors, followed by micro-command metrics. This finding — that economic variables dominate — would be replicated across nearly every subsequent RTS prediction paper.

An earlier phase-dependent evaluation study, [Bakkes2007], had explored outcome evaluation in the Spring RTS engine (a Total Annihilation clone), achieving ~97% prediction accuracy in perfect-information settings — but this used an artificial RTS environment rather than a commercial game.

### Key datasets from this era

The evolution of data infrastructure followed a clear scaling curve: [Weber2009Data] assembled 5,493 BW replays from GosuGamers, TeamLiquid, and ICCup; [Synnaeve2012Dataset] extended to 7,649 replays with full state data every 25/100 frames, becoming the community standard; [Robertson2014Dataset] improved the extraction process using BWAPI; and [Lin2017STARDATA] released STARDATA at 365 GB and 65,646 games, the largest SC:BW dataset to that point, processed using TorchCraft.

### Notable PhD theses from this era

Five doctoral theses defined the intellectual core of SC:BW research. [Synnaeve2012Thesis] developed a full Bayesian framework for multi-level RTS AI, integrated into the BroodwarBotQ competition bot. [Weber2012Thesis] built EISBot, integrating reactive planning, machine learning for opponent modeling, and case-based reasoning; it achieved D ranking on ICCup. [Hagelback2012Thesis] pioneered potential fields for RTS bot control. [Churchill2016Thesis] covered build-order search, SparCraft combat simulation, Portfolio Greedy Search, UAlbertaBot (winner of 2013 AIIDE), and the Tournament Manager software used by all three competitions. [Uriarte2017Thesis] covered game-tree search with high-level state abstractions, terrain analysis (BWTA2), and combat model learning.

The most directly relevant thesis for prediction work specifically is [Stanescu2018Thesis], which developed abstract combat outcome prediction models that were both accurate and computationally efficient, serving as evaluation functions for search algorithms. It was tested on StarCraft and µRTS.

## §3 — StarCraft II and the deep learning inflection (2015–2019)

### AlphaGo triggers the RTS grand challenge narrative

In March 2016, DeepMind's AlphaGo defeated Go world champion Lee Sedol 4–1 in Seoul. The victory was a watershed: Go's branching factor (~250 vs. chess's ~35) had been considered intractable for AI. Almost immediately, the research community converged on a consensus that real-time strategy games — particularly StarCraft — represented "the next frontier." DeepMind founder Demis Hassabis had called StarCraft "the next step up" as early as 2011. At BlizzCon 2016, DeepMind and Blizzard formally announced their collaboration. The narrative arc — Chess (Deep Blue, 1997) → Go (AlphaGo, 2016) → StarCraft — became a standard framing in grant applications, conference keynotes, and media coverage.

### SC2LE opens the floodgates

[Vinyals2017] introduced the SC2LE (StarCraft II Learning Environment) and PySC2, a Python RL wrapper. It released ~800,000 anonymized ladder replays, a suite of mini-game benchmarks, and baseline results. The paper included initial experiments on predicting game outcomes from replay observations — establishing outcome prediction as one of the natural tasks enabled by the platform. Its significance for the historical narrative is as the enabling moment that opened SC2 to the broader ML community.

### Pre-AlphaStar deep learning on SC2

A burst of deep learning research on StarCraft followed in 2016–2018, mostly focused on agent construction rather than prediction. [Usunier2016] was one of the earliest deep RL works on StarCraft combat scenarios, proposing heuristic RL using episodic exploration in policy space. [Justesen2017] showed macro-management decisions can be learned from replays using neural networks, achieving 54.6% top-1 accuracy on next-build-action prediction from 789,571 state-action pairs; when integrated into UAlbertaBot, the learned network outperformed the built-in bot. [Wu2017MSC] released the MSC dataset built on SC2LE, with baselines for global state evaluation (winner prediction from game state) using GRU-based networks — one of the first SC2-specific datasets designed for ML macro-management research, with winner prediction as a defined task. [Sun2018TStarBots] was the first public work to defeat cheating-level built-in SC2 AI in full 1v1 games using deep RL. [Pang2019] applied hierarchical RL for full-length SC2 games, achieving >93% win rate against level-7 built-in AI.

### Outcome prediction matures in SC2

The critical thread for this thesis — direct outcome prediction — developed in parallel with agent research. [Avontuur2013] predicted the league (skill tier) of SC2 players using behavioral features from 1,297 replays, achieving 47.3% weighted accuracy across 7 leagues (vs. 25.5% baseline). While focused on skill prediction rather than match outcome, this established SC2 replay-based player modeling. [Leblanc2013] was one of the earliest attempts at SC2 game outcome prediction. [SanchezRuiz2015] compared LDA, QDA, SVM, and kNN for outcome prediction using influence maps, with LDA achieving 71% accuracy; notable for introducing spatial features to match prediction. [AlvarezCaballero2017] compared six ML algorithms for early prediction using Spark/MLlib. [Lin2019NP] used the MSC dataset and proposed Neural Processes for SC2 winner prediction, incorporating probabilistic inference to handle uncertainty; achieved >80% accuracy with only 200 training samples, notable for explicit uncertainty quantification. [Volz2019] applied winner prediction using partial information available to only one player (the "embodied" perspective), showing that accuracies near full-information results are achievable — practically significant, since a deployed prediction system must operate from one player's view, not an omniscient replay perspective.

### AlphaStar closes the grand challenge arc

[Vinyals2019] — AlphaStar reaching Grandmaster level using multi-agent RL with league training — is the closing milestone. After AlphaStar, SC2 transitioned from "unsolved grand challenge" to a domain for refinement, applied analysis, and match outcome prediction as a distinct research question separable from agent construction.

## §4 — Refinement and expansion (2020–2023)

### Sophisticated SC2 prediction methods

With the grand-challenge narrative resolved by AlphaStar, the 2020–2023 period saw outcome prediction pursued as an independent research objective with increasingly refined methods. [Chen2020] improved league prediction to 61.7% accuracy (up from Avontuur's 47.3%) using the Spending Quotient — an economic efficiency metric — demonstrating that macro-level economic features outperform raw mechanical metrics for player evaluation. [Lee2021Combat] used deep learning for combat outcome prediction incorporating terrain information alongside squad composition, then proposed constrained optimization for unit-combination selection based on the predictor, bridging the gap between prediction and strategic decision-making. [Lee2021League] collected 46,398 replays from Spawning Tool and achieved 75.3% accuracy on league prediction using a novel feature extraction method comparing features across six replay sections.

[Bialecki2022] analyzed 6,509 games from five Master/GrandMaster-level players using logistic regression with 9 performance indicators. They identified economic aspects as the strongest victory determinants, replicating the finding from SC:BW research. This is the first publication from Białecki's group that preceded their landmark dataset release.

[Baek2022] proposed a 3D-ResNet architecture treating SC2 replay data as spatiotemporal video-like sequences. It outperformed ML baselines (logistic regression, random forest, XGBoost, LightGBM) and 2D-CNN approaches, and used Grad-CAM to identify key turning-point situations — the first paper to visualize *why* a match outcome was predicted, not just *what* the prediction was. Represents the state-of-the-art in deep learning for SC2 outcome prediction through 2023.

[Baek2023] proposed contrastive self-supervised learning to predict invisible enemy information under fog of war — directly relevant to outcome prediction, since knowledge of enemy state is a critical but hidden input.

### Dataset infrastructure matures

[Bialecki2023] released SC2EGSet — the largest publicly available SC2 esports dataset — containing 55 tournament replaypacks and 17,930 replay files from Premiere and Major tournaments (2016–2022). It includes open-source extraction tools (SC2InfoExtractorGo) and PyTorch/Lightning APIs. Published in Nature's data descriptor journal *Scientific Data*, establishing a high-quality standard for esports research data.

Community data infrastructure also matured during this period. SC2ReplayStats (sc2replaystats.com) provided automated replay upload and analysis. Spawning Tool (spawningtool.com) focused on build order extraction and became a data source for several studies. Aligulac (aligulac.com) maintained an Elo-based rating system for professional SC2, used as a skill reference in academic work.

### AoE2 receives its first — and nearly only — academic attention

The literature search reveals an extreme paucity of academic prediction work on Age of Empires II. [CetinTas2023] created a prediction model using Naïve Bayes and Decision Trees on AoE2: Definitive Edition data, predicting win probability based on civilization and map selection. **This is the only paper specifically dedicated to AoE2 match outcome prediction in the entire pre-2024 literature.**

The Lin et al. (2024) work on counter relationships in PvP games — which uses AoE2 data (1,261,288 matches from aoestats.io) as one of four validation games — lies outside this document's 2023 cutoff but is the natural continuation of the AoE2 thread and is covered in the 2024–2026 supplement.

Community analytics platforms — aoestats.io, aoe2.net, and aoe2insights.com — have accumulated substantial data on civilization win rates, Elo distributions, and map performance. A GitHub project, PyAge2 (Kachaiev, 2021), created an OpenAI Gym-compatible RL environment for AoE2: The Conquerors, but was never published academically. These resources demonstrate that AoE2 data exists in sufficient quantity for academic work — what was missing was the research community to use it.

### Other RTS games: a comprehensive absence

The literature search produced the following explicit gap findings. For **Warcraft III**, only one tangential paper was found — [Tong2011] — which used genetic algorithms to evolve unit-spawning controllers on a custom WC3 map. This is unit composition optimization, not match prediction. No Warcraft III match outcome prediction work exists in the academic literature. For the **Command & Conquer series**, no academic prediction, AI, or analytical work was found for any C&C title; the games are mentioned in genre overviews but never used as research testbeds. For **Total War, Dawn of War, Supreme Commander, Company of Heroes, Homeworld, Rise of Nations, Age of Mythology, and Empire Earth**, no academic prediction or AI research papers were found for any of these titles. Total War's neural-network-based unit AI and genetic-algorithm campaign AI are documented in industry blog posts but received no academic treatment. For **0 A.D.**, despite being open-source — theoretically the most accessible RTS for researchers — no published academic work was found using it as a testbed. **Dune II** is universally cited as the "first modern RTS" in historical sections of surveys but never used as a research testbed.

The simplified academic testbed microRTS, created by Santiago Ontañón, has generated 20+ papers and annual competitions since 2017 ([Ontanon2018microRTS]). However, microRTS is an artificial environment designed for research, not a commercial game, and its prediction dynamics differ fundamentally from commercial RTS titles with large player bases and professional scenes.

## §5 — Three decades of uneven attention: cross-cutting themes

### How data access shaped the research landscape

The evolution of data sources for RTS research follows four distinct phases, each enabling new categories of work. Phase 1 — professional replay archives (pre-2009) — comprised Korean pro-game replays shared on fan sites, GosuGamers (~7,930 BW replays), ICCup ladder replays, TeamLiquid repositories, and RepDepot (>56,600 replays, mixed skill). Data was raw replay files requiring custom parsers. Research was limited to strategy classification from build orders. Phase 2 — BWAPI-enabled extraction (2009–2016) — brought frame-by-frame game-state extraction, enabling micromanagement research, spatial reasoning, and quantitative feature extraction for prediction models. [Synnaeve2012Dataset] became the community standard. Phase 3 — official platforms and large-scale dumps (2017–2019) — saw SC2LE release ~800K anonymized ladder replays, [Lin2017STARDATA] provide 65,646 BW replays (365 GB), and [Synnaeve2016TorchCraft] bridge StarCraft to ML frameworks. This was the first time researchers could work with hundreds of thousands of games rather than thousands. Phase 4 — curated academic datasets (2020–2023) — saw [Bialecki2023] provide 17,930 tournament replays as a shift toward quality over quantity: curated professional-level data with standardized extraction tools and ML-ready APIs.

For AoE2, data infrastructure remained at Phase 1 throughout this entire period: community platforms collected statistics, but no BWAPI-equivalent API, no official research dataset, and no standardized extraction pipeline existed before 2024.

### The methodological arc from rules to deep learning

The methods used for RTS outcome prediction evolved through clearly demarcated eras. Rule-based and scripted approaches dominated commercial game AI and early academic bots (pre-2008). Case-based reasoning was the first machine learning paradigm applied to RTS ([Hsieh2008]; [Weber2009CBR]). Bayesian networks and HMMs followed in 2011 ([Synnaeve2011Opening]; [Dereszynski2011]), introducing principled uncertainty handling. Classical ML — logistic regression, SVMs, random forests, gradient boosting — produced the first direct outcome prediction results ([Erickson2014]; [Ravari2016]). The deep learning era began around 2016–2017, with CNNs and RNNs applied to both agent construction and prediction ([Wu2017MSC]; [Lin2019NP]). By 2022, spatiotemporal deep learning ([Baek2022]) represented the state of the art.

A striking finding across this entire arc: **economic features consistently emerge as the strongest predictors of match outcome**, regardless of era, method, or specific game (SC:BW or SC2). This was first established by [Erickson2014], confirmed by [Ravari2016], and replicated by [Bialecki2022]. Whether the same holds for AoE2 — where civilizations have structurally different economies — is an open question that the thesis can directly address.

### Why StarCraft monopolized academic attention

The surveys by [Robertson2014Survey] and [Ontanon2013] collectively identify a clear set of enabling factors, and the research record confirms their assessment. StarCraft's academic dominance rests on five reinforcing pillars. **First**, API availability: BWAPI (2009) and SC2LE (2017) provided programmatic access that no other commercial RTS offered. AoE2's game engine remained closed; WC3 had a map editor but no research API; C&C and Total War had no external interfaces at all. **Second**, competition infrastructure: three annual competitions (AIIDE, CIG, SSCAIT) created incentive structures, standardized evaluation, and a global community. No other RTS game had even one academic competition. **Third**, professional replay data: Korea's decade-long professional SC:BW scene produced thousands of expert-level replays. AoE2's competitive scene, while active, was smaller and less systematically archived. **Fourth**, game properties: StarCraft's three-race asymmetry, well-defined tech trees, deterministic simulation, and imperfect information created a rich but tractable research space. AoE2's 30+ civilizations, randomized maps, and diverse win conditions create higher variance — potentially more interesting for prediction research, but harder for controlled experiments. **Fifth**, academic network effects: once Buro, Weber, Synnaeve, Churchill, and Ontañón established StarCraft as the standard RTS testbed, subsequent researchers chose StarCraft for comparability, access to existing tools, and community support. This self-reinforcing dynamic meant that even as AoE2's player base grew substantially after the Definitive Edition (2019), academic attention did not follow.

**The absence of AoE2 literature is the single most important gap finding for the thesis.** A game with millions of active players, 45 asymmetric civilizations, a professional esports scene (Red Bull Wololo, Hidden Cup), and publicly available match data produced one dedicated prediction paper ([CetinTas2023]) in three decades.

### Polish academic contributions

Poland's contribution to RTS prediction research is concentrated in a single research group. Andrzej Białecki, a PhD candidate at Warsaw University of Technology (Faculty of Electrical Engineering), began publishing in 2021–2022. His earliest outputs were software tools (SC2MapLocaleExtractor, SC2_Datasets) released on Zenodo, followed by [Bialecki2022] and the landmark [Bialecki2023] dataset. His work is esports data science rather than traditional bot-AI — analyzing determinants of victory using statistical methods and building datasets for the research community, rather than constructing playing agents. Białecki's primary collaborator is Jan Gajewski at Józef Piłsudski University of Physical Education in Warsaw. Beyond the Białecki group, Gdańsk University of Technology participated in SSCAIT (from 2012) as a student project, but produced no standalone publications. No RTS prediction or AI research was identified from PJAIT, AGH, Jagiellonian University, or any other Polish institution.

## What the historical record reveals — implications for the thesis

Three decades of RTS prediction research yield a clear set of findings that frame the thesis's contribution.

First, **the methodological toolkit is mature but narrowly applied.** From Bayesian models through gradient boosting to 3D-CNNs, the progression of methods is well-documented — but applied almost exclusively to StarCraft. Whether these methods transfer to AoE2's different strategic structure (more civilizations, randomized maps, multiple viable win conditions) is genuinely unknown.

Second, **economic features dominate prediction across all prior work.** Every SC:BW and SC2 prediction study that performed feature importance analysis found resource/economic variables to be the strongest predictors. AoE2's civilization-specific economic bonuses create a structurally different economic landscape that may alter this pattern.

Third, **AoE2's absence from the literature is not a data problem — it is an infrastructure and community problem.** Community platforms have collected millions of matches. What was lacking was the academic entry point: an API, a competition, a foundational paper establishing AoE2 as a research target.

Fourth, **the comparative dimension is entirely novel.** No paper in the pre-2024 literature compares prediction performance across two different commercial RTS games. A head-to-head comparison of prediction models trained on SC2 (with its deep existing literature) and AoE2 (with its near-total absence of prior work) would be a genuinely original contribution — not merely filling a gap but creating a new category of comparative RTS prediction research.

## References

- [AlvarezCaballero2017] Álvarez-Caballero, A., Merelo, J.J., & García, P. (2017). Early Prediction of the Winner in StarCraft Matches. *Proc. International Joint Conference on Computational Intelligence (IJCCI 2017)*, pp. 401–406. [peer-reviewed conference]
- [Avontuur2013] Avontuur, T., Spronck, P., & van Zaanen, M. (2013). Player Skill Modeling in StarCraft II. *Proc. AIIDE 2013*. [peer-reviewed conference]
- [Baek2022] Baek, I. & Kim, S.B. (2022). 3-Dimensional convolutional neural networks for predicting StarCraft II results and extracting key game situations. *PLOS ONE* 17(3): e0264550. DOI: 10.1371/journal.pone.0264550. <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0264550> [peer-reviewed journal]
- [Baek2023] Baek, I. et al. (2023). Self-supervised Learning for Predicting Invisible Enemy Information in StarCraft II. In *IntelliSys 2022*, LNNS vol. 542, Springer. [peer-reviewed conference]
- [Bakkes2007] Bakkes, S., Spronck, P., & van den Herik, J. (2007). Phase-dependent Evaluation in RTS Games. *BNAIC 2007*, pp. 3–10. <https://spronck.net/pubs/BakkesBNAIC2007.pdf> [peer-reviewed conference]
- [Bialecki2022] Białecki, A., Gajewski, J., Białecki, P., Phatak, A., & Memmert, D. (2022). Determinants of Victory in Esports — StarCraft II. *Multimedia Tools and Applications* 82(7): 11099–11115. DOI: 10.1007/s11042-022-13373-2. <https://link.springer.com/article/10.1007/s11042-022-13373-2> [peer-reviewed journal]
- [Bialecki2023] Białecki, A., Jakubowska, N., Dobrowolski, P., Białecki, P., Krupiński, L., Szczap, A., Białecki, R., & Gajewski, J. (2023). SC2EGSet: StarCraft II Esport Replay and Game-state Dataset. *Scientific Data* 10: 600. DOI: 10.1038/s41597-023-02510-7. <https://www.nature.com/articles/s41597-023-02510-7> [peer-reviewed journal]
- [Buro2002] Buro, M. (2002). ORTS: A Hack-Free RTS Game Environment. *International Computers and Games Conference (CG 2002)*, Springer, LNCS 2883, pp. 280–291. [peer-reviewed conference]
- [Buro2003] Buro, M. (2003). Real-Time Strategy Games: A New AI Research Challenge. *Proc. IJCAI-03*, pp. 1534–1535. <https://www.researchgate.net/publication/228698194_Call_for_AI_research_in_RTS_games> [peer-reviewed conference]
- [Certicky2019] Čertický, M., Churchill, D., Kim, K.-J., Čertický, M., & Kelly, R. (2019). StarCraft AI Competitions, Bots, and Tournament Manager Software. *IEEE Transactions on Games* 11(3): 227–237. DOI: 10.1109/TG.2018.2883499. [peer-reviewed journal]
- [CetinTas2023] Çetin Taş, İ. & Müngen, A.A. (2023). Regression Analysis of Age of Empires II DE Match Results with Machine Learning. *2023 8th International Conference on Computer Science and Engineering (UBMK)*, IEEE. DOI: 10.1109/UBMK59864.2023.10391048. <https://ieeexplore.ieee.org/document/10391048/> [peer-reviewed conference]
- [Chen2020] Chen, Y., Aitchison, M., & Sweetser, P. (2020). Improving StarCraft II Player League Prediction with Macro-Level Features. *AI 2020: Advances in Artificial Intelligence (Australasian AI Conference)*, Springer LNCS. [peer-reviewed conference]
- [Churchill2011BuildOrder] Churchill, D. & Buro, M. (2011). Build Order Optimization in StarCraft. *Proc. AIIDE 2011* 7(1): 14–19. DOI: 10.1609/aiide.v7i1.12435. [peer-reviewed conference]
- [Churchill2016Thesis] Churchill, D. (2016). *Heuristic Search Techniques for Real-Time Strategy Games.* PhD Thesis, University of Alberta. Supervisor: Michael Buro. <https://ualberta.scholaris.ca/items/afe784f4-012b-4f5a-9fdb-ed956b98406f> [doctoral thesis]
- [Dereszynski2011] Dereszynski, E.W., Hostetler, J., Fern, A., Dietterich, T.G., Hoang, T.-T., & Udarbe, M. (2011). Learning Probabilistic Behavior Models in Real-Time Strategy Games. *Proc. AIIDE 2011* 7(1): 20–25. DOI: 10.1609/aiide.v7i1.12433. [peer-reviewed conference]
- [Erickson2014] Erickson, G. & Buro, M. (2014). Global State Evaluation in StarCraft. *Proc. AIIDE 2014* 10(1): 112–118. DOI: 10.1609/aiide.v10i1.12725. <https://ojs.aaai.org/index.php/AIIDE/article/view/12725> [peer-reviewed conference]
- [Hagelback2012Thesis] Hagelbäck, J. (2012). *Multi-Agent Potential Field Based Architectures for Real-Time Strategy Game Bots.* PhD Thesis, Blekinge Institute of Technology, Sweden. [doctoral thesis]
- [Hostetler2012] Hostetler, J., Dereszynski, E., Dietterich, T., & Fern, A. (2012). Inferring Strategies from Limited Reconnaissance in Real-Time Strategy Games. *Proc. UAI 2012*. [peer-reviewed conference]
- [Hsieh2008] Hsieh, J.-L. & Sun, C.-T. (2008). Building a Player Strategy Model by Analyzing Replays of Real-Time Strategy Games. *Proc. IEEE IJCNN 2008*, pp. 3106–3111. [peer-reviewed conference]
- [Justesen2017] Justesen, N. & Risi, S. (2017). Learning Macromanagement in StarCraft from Replays using Deep Learning. *Proc. IEEE CIG 2017*, pp. 162–169. DOI: 10.1109/CIG.2017.8080430. <https://sebastianrisi.com/wp-content/uploads/justesen_cig17.pdf> [peer-reviewed conference]
- [Laird2001] Laird, J.E. & van Lent, M. (2001). Human-Level AI's Killer Application: Interactive Computer Games. *AI Magazine* 22(2): 15–26. [peer-reviewed journal]
- [Leblanc2013] Leblanc, D. & Louis, S. (2013). Early Prediction of a Game Outcome in StarCraft 2. *28th International Conference on Computers and Their Applications (CATA 2013)*, pp. 319–326. [peer-reviewed conference]
- [Lee2021Combat] Lee, D., Kim, M., & Ahn, C.W. (2021). Predicting Combat Outcomes and Optimizing Armies in StarCraft II by Deep Learning. *Expert Systems with Applications* 185: 115592. DOI: 10.1016/j.eswa.2021.115592. [peer-reviewed journal]
- [Lee2021League] Lee, C.M. & Ahn, C.W. (2021). Feature Extraction for StarCraft II League Prediction. *Electronics* 10(8): 909. DOI: 10.3390/electronics10080909. [peer-reviewed journal]
- [Lin2017STARDATA] Lin, Z., Gehring, J., Khalidov, V., & Synnaeve, G. (2017). STARDATA: A StarCraft AI Research Dataset. *Proc. AIIDE 2017* 13(1): 50–56. DOI: 10.1609/aiide.v13i1.12929. <https://arxiv.org/abs/1708.02139> [peer-reviewed conference]
- [Lin2019NP] Lin, M., Wang, T., Li, X.B., Liu, J., Wang, Y., Zhu, Y., et al. (2019). An Uncertainty-Incorporated Approach to Predict the Winner in StarCraft II Using Neural Processes. *IEEE Access* 7: 101609–101619. DOI: 10.1109/ACCESS.2019.2930581. <https://ieeexplore.ieee.org/document/8776593> [peer-reviewed journal]
- [McCoy2008] McCoy, J. & Mateas, M. (2008). An Integrated Agent for Playing Real-Time Strategy Games. *Proc. AAAI-08*, pp. 1313–1318. [peer-reviewed conference]
- [Ontanon2013] Ontañón, S., Synnaeve, G., Uriarte, A., Richoux, F., Churchill, D., & Preuss, M. (2013). A Survey of Real-Time Strategy Game AI Research and Competition in StarCraft. *IEEE Transactions on Computational Intelligence and AI in Games* 5(4): 293–311. DOI: 10.1109/TCIAIG.2013.2286295. <https://ieeexplore.ieee.org/document/6637024/> [peer-reviewed journal]
- [Ontanon2018microRTS] Ontañón, S., Barriga, N.A., Silva, C.R., Moraes, R.O., & Lelis, L.H.S. (2018). The First microRTS Artificial Intelligence Competition. *AI Magazine* 39(1): 75–83. DOI: 10.1609/aimag.v39i1.2777. [peer-reviewed journal]
- [Pang2019] Pang, Z.-J., Liu, R.-Z., Meng, Z.-Y., Zhang, Y., Yu, Y., & Lu, T. (2019). On Reinforcement Learning for Full-Length Game of StarCraft. *Proc. AAAI 2019* 33(01): 4691–4698. DOI: 10.1609/aaai.v33i01.33014691. [peer-reviewed conference]
- [Ponsen2004] Ponsen, M. & Spronck, P. (2004). Improving Adaptive Game AI with Evolutionary Learning. *CGAIDE 2004*, pp. 389–396. [peer-reviewed conference]
- [Ponsen2005] Ponsen, M., Muñoz-Avila, H., Spronck, P., & Aha, D.W. (2005). Automatically Acquiring Domain Knowledge for Adaptive Game AI Using Evolutionary Learning. *Proc. IAAI-05*, pp. 1535–1540. [peer-reviewed conference]
- [Ravari2016] Ravari, Y.N., Bakkes, S., & Spronck, P. (2016). StarCraft Winner Prediction. *Proc. AIIDE 2016 Workshop* 12(2): 2–8. DOI: 10.1609/aiide.v12i2.12887. <https://www.spronck.net/pubs/AIIDE2016Yaser.pdf> [peer-reviewed workshop]
- [Robertson2014Dataset] Robertson, G. & Watson, I. (2014). An Improved Dataset and Extraction Process for Starcraft AI. *Proc. FLAIRS-27*. <https://cdn.aaai.org/ocs/7867/7867-36776-1-PB.pdf> [peer-reviewed conference]
- [Robertson2014Survey] Robertson, G. & Watson, I. (2014). A Review of Real-Time Strategy Game AI. *AI Magazine* 35(4): 75–104. DOI: 10.1609/aimag.v35i4.2478. <https://www.cs.auckland.ac.nz/research/gameai/publications/Robertson_Watson_AIMag14.pdf> [peer-reviewed journal]
- [SanchezRuiz2015] Sánchez-Ruiz, A.A. (2015). Predicting the Winner in Two Player StarCraft Games. *Proc. CoSECivi*, pp. 24–35. [peer-reviewed conference]
- [Stanescu2013] Stanescu, M., Hernandez, S.P., Erickson, G., Greiner, R., & Buro, M. (2013). Predicting Army Combat Outcomes in StarCraft. *Proc. AIIDE 2013*. [peer-reviewed conference]
- [Stanescu2018Thesis] Stanescu, A.M. (2018). *Outcome Prediction and Hierarchical Models in Real-Time Strategy Games.* PhD Thesis, University of Alberta. Supervisor: Michael Buro. [doctoral thesis]
- [Sun2018TStarBots] Sun, P., Sun, X., Han, L., et al. (2018). TStarBots: Defeating the Cheating Level Builtin AI in StarCraft II in the Full Game. *arXiv:1809.07193*. <https://arxiv.org/abs/1809.07193> [arXiv preprint]
- [Synnaeve2011Opening] Synnaeve, G. & Bessière, P. (2011). A Bayesian Model for Opening Prediction in RTS Games with Application to StarCraft. *Proc. IEEE CIG 2011*, pp. 281–288. <https://hal.science/hal-00607277> [peer-reviewed conference]
- [Synnaeve2011Plan] Synnaeve, G. & Bessière, P. (2011). A Bayesian Model for Plan Recognition in RTS Games Applied to StarCraft. *Proc. AIIDE 2011*. [peer-reviewed conference]
- [Synnaeve2012Dataset] Synnaeve, G. & Bessière, P. (2012). A Dataset for StarCraft AI & an Example of Armies Clustering. *Proc. AIIDE Workshop on AI in Adversarial Real-Time Games*. <https://www.researchgate.net/publication/233532265_A_Dataset_for_StarCraft_AI_an_Example_of_Armies_Clustering> [peer-reviewed workshop]
- [Synnaeve2012Thesis] Synnaeve, G. (2012). *Bayesian Programming and Learning for Multi-Player Video Games: Application to RTS AI.* PhD Thesis, Institut National Polytechnique de Grenoble (INPG), France. [doctoral thesis]
- [Synnaeve2016TorchCraft] Synnaeve, G., Nardelli, N., Auvolat, A., Chintala, S., Lacroix, T., Lin, Z., Richoux, F., & Usunier, N. (2016). TorchCraft: a Library for Machine Learning Research on Real-Time Strategy Games. *arXiv:1611.00625*. <https://arxiv.org/abs/1611.00625> [arXiv preprint]
- [Tong2011] Tong, C.K., On, C.K., Teo, J., & Kiring, A.M.K. (2011). Evolving Neural Controllers Using GA for Warcraft 3 — Real Time Strategy Game. *Proc. BIC-TA 2011*, IEEE, pp. 15–20. [peer-reviewed conference]
- [Uriarte2017Thesis] Uriarte, A. (2017). *Adversarial Search and Spatial Reasoning in Real Time Strategy Games.* PhD Dissertation, Drexel University. Supervisor: Santiago Ontañón. [doctoral thesis]
- [Usunier2016] Usunier, N., Synnaeve, G., Lin, Z., & Chintala, S. (2016). Episodic Exploration for Deep Deterministic Policies: An Application to StarCraft Micromanagement Tasks. *arXiv:1609.02993* (submitted to ICLR 2017). <https://arxiv.org/abs/1609.02993> [arXiv preprint]
- [Vinyals2017] Vinyals, O., Ewalds, T., Bartunov, S., et al. (2017). StarCraft II: A New Challenge for Reinforcement Learning. *arXiv:1708.04782*. <https://arxiv.org/abs/1708.04782> [arXiv preprint]
- [Vinyals2019] Vinyals, O., Babuschkin, I., Czarnecki, W.M., et al. (2019). Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning. *Nature* 575: 350–354. DOI: 10.1038/s41586-019-1724-z. <https://www.nature.com/articles/s41586-019-1724-z> [peer-reviewed journal]
- [Volz2019] Volz, V., Preuss, M., & Bonde, M.K. (2019). Towards Embodied StarCraft II Winner Prediction. In: Cazenave, T., Saffidine, A., Sturtevant, N. (eds) *Computer Games*, CCIS vol. 1017, Springer, pp. 3–22. DOI: 10.1007/978-3-030-24337-1_1. [peer-reviewed book chapter]
- [Weber2009Data] Weber, B.G. & Mateas, M. (2009). A Data Mining Approach to Strategy Prediction. *Proc. IEEE CIG 2009*, pp. 140–147. [peer-reviewed conference]
- [Weber2009CBR] Weber, B.G. & Mateas, M. (2009). Case-Based Reasoning for Build Order in Real-Time Strategy Games. *Proc. AIIDE 2009*. [peer-reviewed conference]
- [Weber2012Thesis] Weber, B.G. (2012). *Integrating Learning in a Multi-Scale Agent.* PhD Dissertation, UC Santa Cruz. <https://eis-blog.soe.ucsc.edu/2012/06/dissertation-weber/> [doctoral thesis]
- [Wu2017MSC] Wu, H., Zhang, J., & Huang, K. (2017). MSC: A Dataset for Macro-Management in StarCraft II. *arXiv:1710.03131*. <https://arxiv.org/abs/1710.03131> [arXiv preprint]

## BibTeX appendix

```bibtex
@article{AlvarezCaballero2017,
  author = {Álvarez-Caballero, A. and Merelo, J.J. and García, P.},
  title = {Early Prediction of the Winner in StarCraft Matches},
  booktitle = {Proc. International Joint Conference on Computational Intelligence (IJCCI 2017)},
  year = {2017},
  pages = {401--406}
}

@inproceedings{Avontuur2013,
  author = {Avontuur, Tetske and Spronck, Pieter and van Zaanen, Menno},
  title = {Player Skill Modeling in {StarCraft II}},
  booktitle = {Proc. AIIDE 2013},
  year = {2013}
}

@article{Baek2022,
  author = {Baek, Insung and Kim, Seoung Bum},
  title = {3-Dimensional convolutional neural networks for predicting {StarCraft II} results and extracting key game situations},
  journal = {PLOS ONE},
  year = {2022},
  volume = {17},
  number = {3},
  pages = {e0264550},
  doi = {10.1371/journal.pone.0264550}
}

@incollection{Baek2023,
  author = {Baek, Insung and others},
  title = {Self-supervised Learning for Predicting Invisible Enemy Information in {StarCraft II}},
  booktitle = {IntelliSys 2022},
  series = {LNNS},
  volume = {542},
  publisher = {Springer},
  year = {2023}
}

@inproceedings{Bakkes2007,
  author = {Bakkes, Sander and Spronck, Pieter and van den Herik, Jaap},
  title = {Phase-dependent Evaluation in {RTS} Games},
  booktitle = {BNAIC 2007},
  year = {2007},
  pages = {3--10}
}

@article{Bialecki2022,
  author = {Białecki, Andrzej and Gajewski, Jan and Białecki, Przemysław and Phatak, Aditya and Memmert, Daniel},
  title = {Determinants of Victory in Esports --- {StarCraft II}},
  journal = {Multimedia Tools and Applications},
  year = {2022},
  volume = {82},
  number = {7},
  pages = {11099--11115},
  doi = {10.1007/s11042-022-13373-2}
}

@article{Bialecki2023,
  author = {Białecki, Andrzej and Jakubowska, Natalia and Dobrowolski, Paweł and Białecki, Przemysław and Krupiński, Leszek and Szczap, Andrzej and Białecki, Robert and Gajewski, Jan},
  title = {{SC2EGSet}: {StarCraft II} Esport Replay and Game-state Dataset},
  journal = {Scientific Data},
  year = {2023},
  volume = {10},
  pages = {600},
  doi = {10.1038/s41597-023-02510-7}
}

@inproceedings{Buro2002,
  author = {Buro, Michael},
  title = {{ORTS}: A Hack-Free {RTS} Game Environment},
  booktitle = {International Computers and Games Conference (CG 2002)},
  publisher = {Springer},
  series = {LNCS},
  volume = {2883},
  year = {2002},
  pages = {280--291}
}

@inproceedings{Buro2003,
  author = {Buro, Michael},
  title = {Real-Time Strategy Games: A New {AI} Research Challenge},
  booktitle = {Proc. IJCAI-03},
  year = {2003},
  pages = {1534--1535}
}

@article{Certicky2019,
  author = {Čertický, Michal and Churchill, David and Kim, Kyung-Joong and Čertický, Matej and Kelly, Richard},
  title = {{StarCraft AI} Competitions, Bots, and Tournament Manager Software},
  journal = {IEEE Transactions on Games},
  year = {2019},
  volume = {11},
  number = {3},
  pages = {227--237},
  doi = {10.1109/TG.2018.2883499}
}

@inproceedings{CetinTas2023,
  author = {Çetin Taş, İclal and Müngen, Ahmet Anıl},
  title = {Regression Analysis of {Age of Empires II DE} Match Results with Machine Learning},
  booktitle = {2023 8th International Conference on Computer Science and Engineering (UBMK)},
  publisher = {IEEE},
  year = {2023},
  doi = {10.1109/UBMK59864.2023.10391048}
}

@inproceedings{Chen2020,
  author = {Chen, Ying and Aitchison, Matthew and Sweetser, Penny},
  title = {Improving {StarCraft II} Player League Prediction with Macro-Level Features},
  booktitle = {AI 2020: Advances in Artificial Intelligence},
  publisher = {Springer},
  series = {LNCS},
  year = {2020}
}

@inproceedings{Churchill2011BuildOrder,
  author = {Churchill, David and Buro, Michael},
  title = {Build Order Optimization in {StarCraft}},
  booktitle = {Proc. AIIDE 2011},
  year = {2011},
  volume = {7},
  number = {1},
  pages = {14--19},
  doi = {10.1609/aiide.v7i1.12435}
}

@phdthesis{Churchill2016Thesis,
  author = {Churchill, David},
  title = {Heuristic Search Techniques for Real-Time Strategy Games},
  school = {University of Alberta},
  year = {2016}
}

@inproceedings{Dereszynski2011,
  author = {Dereszynski, Ethan W. and Hostetler, Jesse and Fern, Alan and Dietterich, Thomas G. and Hoang, Thao-Trang and Udarbe, Mark},
  title = {Learning Probabilistic Behavior Models in Real-Time Strategy Games},
  booktitle = {Proc. AIIDE 2011},
  year = {2011},
  volume = {7},
  number = {1},
  pages = {20--25},
  doi = {10.1609/aiide.v7i1.12433}
}

@inproceedings{Erickson2014,
  author = {Erickson, Graham and Buro, Michael},
  title = {Global State Evaluation in {StarCraft}},
  booktitle = {Proc. AIIDE 2014},
  year = {2014},
  volume = {10},
  number = {1},
  pages = {112--118},
  doi = {10.1609/aiide.v10i1.12725}
}

@phdthesis{Hagelback2012Thesis,
  author = {Hagelbäck, Johan},
  title = {Multi-Agent Potential Field Based Architectures for Real-Time Strategy Game Bots},
  school = {Blekinge Institute of Technology},
  year = {2012}
}

@inproceedings{Hostetler2012,
  author = {Hostetler, Jesse and Dereszynski, Ethan and Dietterich, Thomas and Fern, Alan},
  title = {Inferring Strategies from Limited Reconnaissance in Real-Time Strategy Games},
  booktitle = {Proc. UAI 2012},
  year = {2012}
}

@inproceedings{Hsieh2008,
  author = {Hsieh, Ji-Lung and Sun, Chuen-Tsai},
  title = {Building a Player Strategy Model by Analyzing Replays of Real-Time Strategy Games},
  booktitle = {Proc. IEEE IJCNN 2008},
  year = {2008},
  pages = {3106--3111}
}

@inproceedings{Justesen2017,
  author = {Justesen, Niels and Risi, Sebastian},
  title = {Learning Macromanagement in {StarCraft} from Replays using Deep Learning},
  booktitle = {Proc. IEEE CIG 2017},
  year = {2017},
  pages = {162--169},
  doi = {10.1109/CIG.2017.8080430}
}

@article{Laird2001,
  author = {Laird, John E. and van Lent, Michael},
  title = {Human-Level {AI}'s Killer Application: Interactive Computer Games},
  journal = {AI Magazine},
  year = {2001},
  volume = {22},
  number = {2},
  pages = {15--26}
}

@inproceedings{Leblanc2013,
  author = {Leblanc, Daniel and Louis, Sushil},
  title = {Early Prediction of a Game Outcome in {StarCraft 2}},
  booktitle = {28th International Conference on Computers and Their Applications (CATA 2013)},
  year = {2013},
  pages = {319--326}
}

@article{Lee2021Combat,
  author = {Lee, Donggyu and Kim, Minwoo and Ahn, Chang Wook},
  title = {Predicting Combat Outcomes and Optimizing Armies in {StarCraft II} by Deep Learning},
  journal = {Expert Systems with Applications},
  year = {2021},
  volume = {185},
  pages = {115592},
  doi = {10.1016/j.eswa.2021.115592}
}

@article{Lee2021League,
  author = {Lee, Chang Min and Ahn, Chang Wook},
  title = {Feature Extraction for {StarCraft II} League Prediction},
  journal = {Electronics},
  year = {2021},
  volume = {10},
  number = {8},
  pages = {909},
  doi = {10.3390/electronics10080909}
}

@inproceedings{Lin2017STARDATA,
  author = {Lin, Zeming and Gehring, Jonas and Khalidov, Vasil and Synnaeve, Gabriel},
  title = {{STARDATA}: A {StarCraft AI} Research Dataset},
  booktitle = {Proc. AIIDE 2017},
  year = {2017},
  volume = {13},
  number = {1},
  pages = {50--56},
  doi = {10.1609/aiide.v13i1.12929}
}

@article{Lin2019NP,
  author = {Lin, Minghan and Wang, Tao and Li, Xiao Bai and Liu, Jia and Wang, Yongjie and Zhu, Yuhang and others},
  title = {An Uncertainty-Incorporated Approach to Predict the Winner in {StarCraft II} Using Neural Processes},
  journal = {IEEE Access},
  year = {2019},
  volume = {7},
  pages = {101609--101619},
  doi = {10.1109/ACCESS.2019.2930581}
}

@inproceedings{McCoy2008,
  author = {McCoy, Josh and Mateas, Michael},
  title = {An Integrated Agent for Playing Real-Time Strategy Games},
  booktitle = {Proc. AAAI-08},
  year = {2008},
  pages = {1313--1318}
}

@article{Ontanon2013,
  author = {Ontañón, Santiago and Synnaeve, Gabriel and Uriarte, Alberto and Richoux, Florian and Churchill, David and Preuss, Mike},
  title = {A Survey of Real-Time Strategy Game {AI} Research and Competition in {StarCraft}},
  journal = {IEEE Transactions on Computational Intelligence and AI in Games},
  year = {2013},
  volume = {5},
  number = {4},
  pages = {293--311},
  doi = {10.1109/TCIAIG.2013.2286295}
}

@article{Ontanon2018microRTS,
  author = {Ontañón, Santiago and Barriga, Nicolas A. and Silva, Cleyton R. and Moraes, Rubens O. and Lelis, Levi H. S.},
  title = {The First {microRTS} Artificial Intelligence Competition},
  journal = {AI Magazine},
  year = {2018},
  volume = {39},
  number = {1},
  pages = {75--83},
  doi = {10.1609/aimag.v39i1.2777}
}

@inproceedings{Pang2019,
  author = {Pang, Zhen-Jia and Liu, Ruo-Ze and Meng, Zhou-Yu and Zhang, Yi and Yu, Yang and Lu, Tong},
  title = {On Reinforcement Learning for Full-Length Game of {StarCraft}},
  booktitle = {Proc. AAAI 2019},
  year = {2019},
  volume = {33},
  number = {01},
  pages = {4691--4698},
  doi = {10.1609/aaai.v33i01.33014691}
}

@inproceedings{Ponsen2004,
  author = {Ponsen, Marc and Spronck, Pieter},
  title = {Improving Adaptive Game {AI} with Evolutionary Learning},
  booktitle = {CGAIDE 2004},
  year = {2004},
  pages = {389--396}
}

@inproceedings{Ponsen2005,
  author = {Ponsen, Marc and Muñoz-Avila, Héctor and Spronck, Pieter and Aha, David W.},
  title = {Automatically Acquiring Domain Knowledge for Adaptive Game {AI} Using Evolutionary Learning},
  booktitle = {Proc. IAAI-05},
  year = {2005},
  pages = {1535--1540}
}

@inproceedings{Ravari2016,
  author = {Ravari, Yaser Norouzzadeh and Bakkes, Sander and Spronck, Pieter},
  title = {{StarCraft} Winner Prediction},
  booktitle = {Proc. AIIDE 2016 Workshop},
  year = {2016},
  volume = {12},
  number = {2},
  pages = {2--8},
  doi = {10.1609/aiide.v12i2.12887}
}

@inproceedings{Robertson2014Dataset,
  author = {Robertson, Glen and Watson, Ian},
  title = {An Improved Dataset and Extraction Process for {Starcraft AI}},
  booktitle = {Proc. FLAIRS-27},
  year = {2014}
}

@article{Robertson2014Survey,
  author = {Robertson, Glen and Watson, Ian},
  title = {A Review of Real-Time Strategy Game {AI}},
  journal = {AI Magazine},
  year = {2014},
  volume = {35},
  number = {4},
  pages = {75--104},
  doi = {10.1609/aimag.v35i4.2478}
}

@inproceedings{SanchezRuiz2015,
  author = {Sánchez-Ruiz, Antonio A.},
  title = {Predicting the Winner in Two Player {StarCraft} Games},
  booktitle = {Proc. CoSECivi},
  year = {2015},
  pages = {24--35}
}

@inproceedings{Stanescu2013,
  author = {Stanescu, Marius and Hernandez, Sergio Poo and Erickson, Graham and Greiner, Russell and Buro, Michael},
  title = {Predicting Army Combat Outcomes in {StarCraft}},
  booktitle = {Proc. AIIDE 2013},
  year = {2013}
}

@phdthesis{Stanescu2018Thesis,
  author = {Stanescu, Adrian Marius},
  title = {Outcome Prediction and Hierarchical Models in Real-Time Strategy Games},
  school = {University of Alberta},
  year = {2018}
}

@article{Sun2018TStarBots,
  author = {Sun, Peng and Sun, Xinghai and Han, Lei and others},
  title = {{TStarBots}: Defeating the Cheating Level Builtin {AI} in {StarCraft II} in the Full Game},
  journal = {arXiv preprint arXiv:1809.07193},
  year = {2018}
}

@inproceedings{Synnaeve2011Opening,
  author = {Synnaeve, Gabriel and Bessière, Pierre},
  title = {A Bayesian Model for Opening Prediction in {RTS} Games with Application to {StarCraft}},
  booktitle = {Proc. IEEE CIG 2011},
  year = {2011},
  pages = {281--288}
}

@inproceedings{Synnaeve2011Plan,
  author = {Synnaeve, Gabriel and Bessière, Pierre},
  title = {A Bayesian Model for Plan Recognition in {RTS} Games Applied to {StarCraft}},
  booktitle = {Proc. AIIDE 2011},
  year = {2011}
}

@inproceedings{Synnaeve2012Dataset,
  author = {Synnaeve, Gabriel and Bessière, Pierre},
  title = {A Dataset for {StarCraft AI} and an Example of Armies Clustering},
  booktitle = {Proc. AIIDE Workshop on AI in Adversarial Real-Time Games},
  year = {2012}
}

@phdthesis{Synnaeve2012Thesis,
  author = {Synnaeve, Gabriel},
  title = {Bayesian Programming and Learning for Multi-Player Video Games: Application to {RTS AI}},
  school = {Institut National Polytechnique de Grenoble},
  year = {2012}
}

@article{Synnaeve2016TorchCraft,
  author = {Synnaeve, Gabriel and Nardelli, Nantas and Auvolat, Alex and Chintala, Soumith and Lacroix, Timothée and Lin, Zeming and Richoux, Florian and Usunier, Nicolas},
  title = {{TorchCraft}: a Library for Machine Learning Research on Real-Time Strategy Games},
  journal = {arXiv preprint arXiv:1611.00625},
  year = {2016}
}

@inproceedings{Tong2011,
  author = {Tong, C.K. and On, C.K. and Teo, J. and Kiring, A.M.K.},
  title = {Evolving Neural Controllers Using {GA} for {Warcraft 3} --- Real Time Strategy Game},
  booktitle = {Proc. BIC-TA 2011},
  publisher = {IEEE},
  year = {2011},
  pages = {15--20}
}

@phdthesis{Uriarte2017Thesis,
  author = {Uriarte, Alberto},
  title = {Adversarial Search and Spatial Reasoning in Real Time Strategy Games},
  school = {Drexel University},
  year = {2017}
}

@article{Usunier2016,
  author = {Usunier, Nicolas and Synnaeve, Gabriel and Lin, Zeming and Chintala, Soumith},
  title = {Episodic Exploration for Deep Deterministic Policies: An Application to {StarCraft} Micromanagement Tasks},
  journal = {arXiv preprint arXiv:1609.02993},
  year = {2016}
}

@article{Vinyals2017,
  author = {Vinyals, Oriol and Ewalds, Timo and Bartunov, Sergey and others},
  title = {{StarCraft II}: A New Challenge for Reinforcement Learning},
  journal = {arXiv preprint arXiv:1708.04782},
  year = {2017}
}

@article{Vinyals2019,
  author = {Vinyals, Oriol and Babuschkin, Igor and Czarnecki, Wojciech M. and others},
  title = {Grandmaster Level in {StarCraft II} Using Multi-Agent Reinforcement Learning},
  journal = {Nature},
  year = {2019},
  volume = {575},
  pages = {350--354},
  doi = {10.1038/s41586-019-1724-z}
}

@incollection{Volz2019,
  author = {Volz, Vanessa and Preuss, Mike and Bonde, Martin Kristian},
  title = {Towards Embodied {StarCraft II} Winner Prediction},
  booktitle = {Computer Games},
  editor = {Cazenave, T. and Saffidine, A. and Sturtevant, N.},
  series = {CCIS},
  volume = {1017},
  publisher = {Springer},
  year = {2019},
  pages = {3--22},
  doi = {10.1007/978-3-030-24337-1_1}
}

@inproceedings{Weber2009Data,
  author = {Weber, Ben G. and Mateas, Michael},
  title = {A Data Mining Approach to Strategy Prediction},
  booktitle = {Proc. IEEE CIG 2009},
  year = {2009},
  pages = {140--147}
}

@inproceedings{Weber2009CBR,
  author = {Weber, Ben G. and Mateas, Michael},
  title = {Case-Based Reasoning for Build Order in Real-Time Strategy Games},
  booktitle = {Proc. AIIDE 2009},
  year = {2009}
}

@phdthesis{Weber2012Thesis,
  author = {Weber, Ben G.},
  title = {Integrating Learning in a Multi-Scale Agent},
  school = {UC Santa Cruz},
  year = {2012}
}

@article{Wu2017MSC,
  author = {Wu, Huikai and Zhang, Junge and Huang, Kaiqi},
  title = {{MSC}: A Dataset for Macro-Management in {StarCraft II}},
  journal = {arXiv preprint arXiv:1710.03131},
  year = {2017}
}
```
