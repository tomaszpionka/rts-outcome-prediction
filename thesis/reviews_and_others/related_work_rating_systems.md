# Non-ML predictive rating systems for PvP skill assessment

**Purpose.** Supplementary literature review for the thesis's Related Work chapter, covering Bradley-Terry foundations, the canonical rating systems (Elo, Glicko, Glicko-2, TrueSkill) and their modern extensions, their theoretical properties as probabilistic forecasters, and their empirical role as baselines and hybrid features in match outcome prediction. Complements the separate historical RTS prediction review and the 2024–2026 bibliography.
**Scope.** Rating systems: BTL foundation, the canonical four, Whole-History Rating, OpenSkill, intransitivity-aware extensions (mElo, Blade-Chest, disc decomposition), recent Bradley-Terry variants. Use cases: baseline vs. ML, ratings as ML features, hybrid neural-rating models. Application domains: chess, Go, tennis, and specifically StarCraft II and Age of Empires II.
**Date.** 2026-04-13.
**Intended use.** Source material for the `thesis-writer` agent to draft §2 Related Work (Rating Systems) and §3 Methods (Baseline Specification). Reference keys use the project's `[AuthorYear]` convention per `docs/THESIS_WRITING_MANUAL.md`. All claims traceable to the References section below.

## Headline finding for the thesis

Elo-family rating systems are not merely ranking tools — they are probabilistic forecasters rooted in the Bradley-Terry paired comparison model, and they set a remarkably hard-to-beat baseline for match outcome prediction. Across chess, tennis, football, and esports, the typical accuracy uplift of machine learning over a well-tuned Elo baseline is 2–5 percentage points, with most studies clustering around 2–3 pp. This narrow margin makes proper specification of the rating-system baseline a critical methodological decision for any thesis comparing ML predictions against classical approaches. For a comparative SC2-vs-AoE2 study, the choice of baseline is further complicated by intransitivity: AoE2's 45-civilization meta exhibits strong rock-paper-scissors structure that standard Elo assumes away, while SC2's three-race system is more nearly transitive.

## §1 — Bradley-Terry foundations: a shared mathematical ancestor

Every rating system discussed in this review ultimately descends from paired comparison models developed in the mid-twentieth century. The Bradley-Terry (BT) model defines the probability that player *i* defeats player *j* as

> P(i > j) = πᵢ / (πᵢ + πⱼ)

where πᵢ > 0 are strength parameters. Reparameterizing with log-strengths βᵢ = log(πᵢ) yields the logistic form P(i > j) = 1 / (1 + exp(−(βᵢ − βⱼ))), making the log-odds of victory a linear function of the strength difference ([BradleyTerry1952]). The same structure was independently proposed by Zermelo in 1929 for chess tournaments ([Zermelo1929]), predating Bradley and Terry by over two decades, though Zermelo's contribution remained largely unknown in the statistics literature until much later.

Luce generalized this to arbitrary choice sets via the Choice Axiom (Independence from Irrelevant Alternatives): P(i chosen from S) = v(i) / Σⱼ∈S v(j). When restricted to pairwise choices, the Luce model coincides exactly with Bradley-Terry, giving rise to the combined name "Bradley-Terry-Luce" (BTL). Luce's *Individual Choice Behavior* ([Luce1959]) became foundational in mathematical psychology and economics, later underpinning McFadden's multinomial logit and, more recently, reward modelling in RLHF for large language models. [Plackett1975] extended BTL to full rankings by decomposing a permutation into a chain of successive "winner from remaining" choices, producing the Plackett-Luce model widely used in horse racing, Formula 1, and multiplayer game ranking.

A parallel tradition stems from [Thurstone1927], which posits normally distributed latent performance values and uses the standard-normal CDF (probit link) rather than the logistic CDF to compute win probability. Under Thurstone's Case V with equal variances, P(i > j) = Φ((μᵢ − μⱼ) / σ√2). Crucially, the logistic and normal CDFs differ by less than 0.01 across the full range when appropriately scaled, so the BTL (logistic) and Thurstone-Mosteller (probit) models are nearly interchangeable in practice. This distinction becomes operationally significant only in the choice of inference method: TrueSkill uses the probit link because Gaussian priors are conjugate with Gaussian likelihoods, while Elo and Glicko use the logistic link for its closed-form convenience.

The concept of expected score as probability prediction is central. When Elo's logistic formula outputs E_A = 1/(1 + 10^((R_B − R_A)/400)), that number is not merely a summary statistic — it is a falsifiable probabilistic forecast that can be evaluated with proper scoring rules. This makes every Elo-family system a probabilistic forecaster by construction, enabling direct comparison against ML classifiers on calibration, discrimination, and sharpness. The theoretical justification for using proper scoring rules in this context is established by [Gneiting2007], and the specific evaluation triptych from [Dimitriadis2024] applies directly.

The computational standard for fitting generalized BT models is the MM algorithm framework of [Hunter2004].

## §2 — The canonical four systems and their probabilistic signatures

### Elo (1960–1978)

Arpad Elo developed his system for the USCF (adopted 1960) and FIDE (adopted 1970), published definitively in *The Rating of Chessplayers, Past and Present* ([Elo1978]). Elo considered two distribution variants — a normal (Gaussian) model and a logistic model — and the logistic version became standard after the USCF found that weaker players win more often than the normal model predicts. The standard expected-score formula is:

> E_A = 1 / (1 + 10^((R_B − R_A) / 400))

The update rule R'_A = R_A + K(S_A − E_A) adjusts ratings proportionally to the surprise in the outcome, where K is the development coefficient (learning rate). FIDE currently uses K = 40 for new/young players, K = 20 for players rated below 2400, and K = 10 once a player's published rating has reached 2400 ([FIDE2024]). The convention that 400 points = 10:1 odds (i.e., πᵢ = 10^(Rᵢ/400)) makes the system formally equivalent to a BT model with a specific scale factor.

The Elo update can be reinterpreted as stochastic gradient descent on the negative log-likelihood of the BT model, with K serving as the learning rate. This interpretation, formalized by [Tang2025], provides no-regret guarantees even under model misspecification and non-stationarity — explaining why Elo performs surprisingly well in domains that violate its assumptions.

**Strengths:** Simplicity, computational efficiency (O(1) per game), interpretable scale, proven track record spanning decades. **Weaknesses:** No uncertainty quantification (all players treated as equally certain), no mechanism for handling inactive players, single scalar cannot capture intransitive relationships, K-factor requires domain-specific tuning.

### Glicko (Glickman, 1999)

Mark Glickman introduced the Rating Deviation (RD) parameter, representing the standard deviation of the Gaussian belief over a player's true rating ([Glickman1999]). Glicko models each player as a distribution N(r, RD²) rather than a point estimate, with RD growing over time for inactive players and shrinking as more games are played.

The expected score formula incorporates opponent uncertainty via a scaling function g(RD) = 1/√(1 + 3q²RD²/π²), where q = ln(10)/400. When the opponent's RD is large, the predicted win probability moves toward 0.5, appropriately reflecting reduced confidence. This is the Bayesian insight: results against players with uncertain ratings carry less informational weight. When RD → 0 for all players, Glicko reduces exactly to the standard Elo system.

The cold-start mechanism — RD growing as RD'(t) = min(√(RD² + c²t), RD_max) — directly addresses the problem of inactive players whose true strength may have drifted. For chess, Glickman suggested c ≈ 63.2 and RD_max = 350. Glicko was originally deployed on the Free Internet Chess Server (FICS) and has been adopted by numerous gaming organizations.

### Glicko-2 (Glickman, 2001)

Glicko-2 adds a third per-player parameter, volatility (σ), representing the expected degree of fluctuation in a player's rating ([Glickman2001]). The three parameters — rating (μ), deviation (φ), and volatility (σ) — enable the system to distinguish between a player who performs consistently and one whose results vary wildly, even when both have the same mean rating and uncertainty. The practical algorithm is described in Glickman's widely cited technical report ([Glickman2013TR]).

The volatility update requires iterative root-finding (Illinois algorithm), making Glicko-2 slightly more computationally expensive than Glicko-1, but the system remains efficient at O(n) per player per rating period plus a small number of Newton-like iterations. Glicko-2 has become the de facto standard for online chess platforms — most notably Lichess, which serves millions of players. The system parameter τ (typically 0.3–1.2) controls how rapidly volatility can change and must be tuned per application.

### TrueSkill (Herbrich, Minka & Graepel, 2006)

TrueSkill was developed at Microsoft Research for Xbox Live matchmaking and represents a qualitative leap in modeling capacity ([Herbrich2007]). Each player has a Gaussian skill belief N(μ, σ²), but inference is performed via Expectation Propagation (EP) on a factor graph rather than closed-form approximations. This architecture natively supports teams, multiplayer games, partial play, and explicit draw modelling.

The 1v1 win probability formula uses the probit link:

> P(i > j) = Φ((μᵢ − μⱼ) / √(2β² + σᵢ² + σⱼ²))

where Φ is the standard normal CDF and β² is the performance noise per game. For leaderboards, TrueSkill displays the conservative estimate μ − 3σ, which starts at zero and rises as confidence grows — a deliberate design to reward both skill and engagement. TrueSkill is patented by Microsoft (US Patent 8,538,910 B2), which has motivated the development of open alternatives.

TrueSkill 2 ([Minka2018TR]) extends the model with player experience curves, squad membership effects, individual performance scores (kills/deaths), and cross-game-mode skill transfer. Validated on ~700K Halo 5 matches, TrueSkill 2 achieved 68% prediction accuracy compared to 52% for TrueSkill 1, primarily by modelling the learning trajectory of new players. Its contextual-factor framework is extensible to asymmetric matchups (race/civilization), making it conceptually relevant to RTS games even though it has not been deployed in that domain.

### Comparative summary

| Feature | Elo | Glicko | Glicko-2 | TrueSkill |
|---|---|---|---|---|
| Parameters per player | 1 (r) | 2 (r, RD) | 3 (μ, φ, σ) | 2 (μ, σ) |
| Link function | Logistic | Logistic | Logistic | Probit |
| Uncertainty tracking | None | RD grows with inactivity | RD + volatility | σ between games |
| Team/multiplayer | No | No | No | Yes (native) |
| Draw model | Score = 0.5 | Score = 0.5 | Score = 0.5 | Explicit draw margin ε |
| Patented | No | No | No | Yes (Microsoft) |
| Canonical venue | [Elo1978] | [Glickman1999] | [Glickman2001] | [Herbrich2007] |

A comprehensive modern survey of all these systems is provided by [Glickman2025], which covers BTL and Thurstone-Mosteller foundations, dynamic extensions, and practical implementations including applications to NBA data. This survey should be cited as a single authoritative reference spanning the entire canonical family.

## §3 — Modern extensions: whole histories, open alternatives, multidimensional skill

### Whole-History Rating

[Coulom2008] rejected incremental updating entirely. Instead, WHR estimates each player's entire rating trajectory simultaneously via maximum a posteriori (MAP) inference under a Wiener-process prior on rating evolution. The Wiener process parameter w controls temporal smoothness: a larger w permits more rapid rating changes. Computation uses Newton's method with tridiagonal Hessians, scaling efficiently even to the KGS Go Server's 10.8 million games (convergence in ~7 minutes on contemporary hardware).

WHR significantly outperforms Elo, Glicko, and TrueSkill in prediction accuracy on KGS data because it retroactively adjusts past ratings as new information arrives — a form of Bayesian smoothing unavailable to online algorithms. It is closely related to Rod Edwards' Edo system for historical chess ratings and to TrueSkill Through Time ([Dangauthier2007]), which applies EP-based smoothing to the TrueSkill factor graph. Coulom himself notes that WHR, Edo, and TTT have nearly identical models but differ primarily in computational approach. WHR has been adopted by goratings.org, the Renju International Federation, and several competitive gaming communities.

### OpenSkill and Weng-Lin

[WengLin2011] derived analytic Bayesian update rules for multi-team, multi-player ranking under both Bradley-Terry and Thurstone-Mosteller models, without the factor-graph machinery of TrueSkill. Their algorithm achieves accuracy competitive with TrueSkill while being 20× faster and requiring under 100 lines of code versus TrueSkill's 500+. Crucially, the Weng-Lin algorithm is not patent-encumbered, making it freely available for academic and commercial use.

The modern OpenSkill Python library ([Joshy2024]) implements five Weng-Lin model variants (Plackett-Luce, Bradley-Terry Full/Part, Thurstone-Mosteller Full/Part) with 150–300% speed improvement over the popular Python TrueSkill package. It supports multiplayer, asymmetric factions, predicted win/draw probabilities, and score margins. For thesis purposes, OpenSkill is the most practical open-source implementation for rating-system baselines in team or 1v1 contexts.

### Addressing intransitivity: mElo, Blade-Chest, disc decomposition

Standard Elo-family systems assume transitivity — if A beats B and B beats C, then A should beat C. This assumption is violated in games with rock-paper-scissors structure, such as AoE2 civilization matchups. Three distinct approaches address this.

Multidimensional Elo (mElo) by [Balduzzi2018] uses the Hodge decomposition to separate a game's payoff matrix into transitive and cyclic components, then augments each player's scalar Elo with k-dimensional "cyclic" vectors. mElo correctly predicts outcomes in intransitive games where standard Elo fails. The paper also proves that standard Elo violates a desirable invariance property: adding redundant copies of an agent can change evaluations.

The Blade-Chest model by [Chen2016BladeChest] assigns each player offensive ("blade") and defensive ("chest") vectors in d dimensions, where victory depends on the blade's effectiveness against the opponent's chest. Applied to StarCraft matchup data, the model empirically outperforms single-scalar methods on datasets with intransitive relationships.

Disc decomposition by [Bertrand2023] demonstrates that Elo can provably fail to extract even the transitive component of certain transitive games. Their alternative assigns each player two scores — skill and consistency — using the normal (Schur) decomposition of the payoff matrix.

A rigorous theoretical treatment of intransitivity's impact on Elo convergence is provided by [Hamilton2025]. They prove that when transitivity is relaxed, Elo ratings become dependent on the matchmaking schedule (who plays whom), but a unique fixed point still exists for a given matching distribution. They also introduce a statistic to measure the degree of intransitivity present in a game — a diagnostic tool directly applicable to AoE2 civilization data.

### Other notable extensions

Elo-MMR ([Ebtekar2021]) targets massive multiplayer contests (e.g., Codeforces) with provable robustness guarantees and aligned incentives. [Cattelan2012] provides the definitive review of BT model extensions including hierarchical, dynamic, and covariate-assisted variants. A 2025 survey ([BT2025Survey]) covers covariate-assisted BT, Bayesian nonparametric Plackett-Luce, and the connection to RLHF reward modelling.

## §4 — When ratings fail as predictors: transitivity, cold starts, calibration drift

### The transitivity assumption and civilization counter-relationships

The fundamental theoretical limitation of standard Elo/Glicko/TrueSkill is the transitivity assumption: all three systems model player strength as a single scalar on a totally ordered scale. This implicitly assumes that "more likely to win against" is a transitive relation. When two players choose different civilizations in AoE2 or different races in SC2, the matchup may depend not just on skill difference but on the specific pairing — creating a partially intransitive structure that a scalar rating cannot capture.

Lin et al. (2024) demonstrated that AoE2 civilization counter-relationships are strongly intransitive, with certain civilizations systematically beating others regardless of player skill. This finding directly undermines the validity of a naive Elo baseline for AoE2 match prediction when civilization identity is known. For the thesis, this has a critical implication: **reporting ML accuracy against a plain Elo baseline may overstate the ML model's contribution**, because some of the "uplift" comes simply from learning civilization counter-relationships that Elo ignores by construction. A fairer baseline would use per-civilization or counter-adjusted ratings.

SC2's three-race matchup structure is more nearly transitive — the meta periodically shifts which race is strongest, but the cycle is less pronounced than AoE2's 45-civilization combinatorics. Aligulac addresses this by maintaining separate per-matchup ratings (vs. Protoss, vs. Terran, vs. Zerg), effectively a 3×1 conditional Elo rather than a scalar ([Aligulac]).

### Cold-start, uncertainty, and population effects

Glicko and TrueSkill address the cold-start problem through their uncertainty parameters (RD and σ respectively), which start high for new players and decrease with more games. Elo has no such mechanism — a new player's first games have the same update magnitude as a veteran's (modulo K-factor adjustments like FIDE's K=40 for new players). TrueSkill 2 goes further by modelling the learning curve of new players, recognizing that a player's 10th game reflects systematically different skill than their 1000th.

Rating inflation and deflation are persistent concerns. In FIDE chess, K=10 for top players produces sluggish adjustment, and Jeff Sonas has argued K=24 would be more accurate. FIDE's 2024 reforms attempted to address deflationary pressure by compressing ratings below 2000 upward and adding hypothetical draws against 1800-rated opponents for new players. In AoE2 DE, the community has noted that actual win rates between players 200 points apart sometimes exceed the Elo-predicted ~64%, suggesting mild miscalibration in the specific K=32 implementation.

### Empirical calibration: the logistic curve under scrutiny

[Glickman2024TR]'s early analysis of USCF data found that the Elo logistic curve required a correction factor of 0.713 to match observed outcomes across the full rating pool. For top players the factor was ~0.95 (near-perfect calibration), while for middle-rated players it was ~0.59 (substantial miscalibration). Sonas's analysis for ChessBase found an 83% scaling factor necessary to compress effective rating differences. The primary explanation is that imprecise ratings (high RD for players with uncertain ratings) attenuate the effective skill difference — exactly the phenomenon Glicko was designed to address.

The porcpine1967 analysis of 913,201 AoE2 DE matches ([Porcpine2020]) established r = 0.96 linear correlation between Elo difference and observed win probability, with a slope of approximately 1.1 percentage points per 10 rating points. This strong linearity — essentially confirming that the Elo logistic curve is well-calibrated within the matchmaker's operating range — means Elo difference is a powerful baseline feature for AoE2 prediction. However, confidence intervals widen at large rating differences because the matchmaker concentrates games near similar ratings, leaving calibration at the tails poorly tested.

## §5 — Elo as ML baseline: a remarkably hard ceiling to surpass

The most consequential empirical finding across the rating-system literature is that ML models struggle to substantially outperform well-tuned Elo baselines for pre-match outcome prediction. [Tang2025] tested Elo, Glicko, TrueSkill, mElo, and pairwise models across chess, Go, tennis, Scrabble, StarCraft, Renju, and Hearthstone. Their headline result: despite significant violations of BT model assumptions and stationarity in every dataset, Elo frequently outperformed more complex rating systems in win-rate prediction. The mechanism is a bias-variance tradeoff: complex models have lower misspecification error but higher regret in the sparse-data regime typical of competitive games.

Domain-specific empirical comparisons confirm this pattern consistently. In **tennis**, [Kovalchik2016] compared 11 published forecasting models and found FiveThirtyEight's Elo among the most accurate, matching or exceeding regression, point-based, and other paired comparison approaches. [Bunker2024] measured an average ML uplift of just 2.3 pp (ADTree: ~72.7% vs. Elo: ~70.4%) across 14 train-test splits of ATP data, and found that ANN, SVM, and Random Forest did not outperform Elo at all. [Angelini2022] proposed Weighted Elo (WElo) incorporating scoreline information, outperforming standard Elo on both Brier score and log loss across >60,000 ATP/WTA matches.

In **football**, the 2017 Soccer Prediction Challenge benchmark showed Elo-based methods achieving ~51.5% three-way accuracy, with the best ML approach (CatBoost + pi-ratings) reaching ~55.8% — an uplift of ~4.3 pp. [Hvattum2010] established that adapted Elo provides predictions comparable to those from more complex models.

For **esports**, [EsportsBench] curates datasets spanning 20+ esports titles including StarCraft II (411,030 matches), Dota 2, LoL, and CS:GO, benchmarking Elo, Glicko, and TrueSkill across all titles. It notes that these rating systems are routinely used as baselines or as features in more sophisticated machine learning pipelines. In SC2 specifically, Aligulac's Glicko-based system achieves excellent calibration up to ~80% predicted win probability. **No published AoE2 study reports a formal Elo-vs-ML accuracy comparison**, which represents a gap the thesis can fill.

[Sipko2015] explored logistic regression and neural networks achieving 65–70% accuracy on ATP matches, with the neural network generating positive ROI against betting markets — demonstrating that even small margins over Elo translate to exploitable edges.

## §6 — Hybrid approaches: rating features inside ML pipelines

### Elo difference as a dominant feature

When Elo-derived features are included as inputs to ML classifiers, they consistently rank among the top 2–3 most important features regardless of the ML architecture used. The 2017 Soccer Prediction Challenge analysis concluded that "in the absence of match-related features on in-game events, ratings seem to be an effective means of condensing a large amount of historical match information into a concise set of model features." The winning CatBoost model used pi-ratings (a soccer-specific paired comparison system) as its core feature set. In tennis, statistical-enhanced learning studies combining Elo with age and rank in spline models achieved a Brier score of 0.151 and classification rate of 79.5% for Grand Slam prediction, with Elo consistently the most important variable.

The mechanism is straightforward: an Elo rating compresses a player's entire match history into a single informative scalar via Bayesian updating. Adding raw match statistics (APM, resources gathered, win streaks) on top of Elo provides incremental signal, but the marginal improvement is typically 1–3 pp because much of that statistical information is already captured in the rating trajectory. For the thesis, this implies that any feature engineering effort should include Elo difference (or its Glicko/TrueSkill equivalent) as a mandatory baseline feature, and the relevant question is how much additional signal civilization/race identity, map, and in-game statistics provide beyond what ratings already capture.

### Neural rating systems

[Fujii2023NBTR] integrates the BT model directly into a neural network via weight-sharing architecture, learning the rating estimator R_i = log(πᵢ) end-to-end. The key insight is that feature importance on the NBTR estimator reveals what determines "overall strength" (the transitive component), while a standard classifier conflates this with intransitive matchup effects. This decomposition is directly relevant to AoE2, where separating player skill from civilization advantage is a core analytical challenge.

Lin et al.'s Neural Rating Table (NRT) and Neural Counter Table (NCT) ([Lin2024NCT]) represent the most directly relevant hybrid work for the thesis. NRT learns individual strength ratings via neural networks, while NCT learns an M×M counter table (M = number of civilizations) that captures pairwise civilization advantages while maintaining interpretability. Applied to 1,261,288 AoE2 matches from aoestats.io, the NCT achieves superior prediction accuracy over standard Elo by explicitly modelling the intransitive civilization meta. A follow-up ([Lin2025EloRCC]) proposes Elo-RCC (Elo with Residual Counter Category learning), an online update algorithm that extends Elo to incorporate counter categories in real time — bridging the gap between static neural models and live rating systems.

For SC2, the Aligulac system already implements a simple version of hybrid rating by maintaining per-matchup ratings (vP, vT, vZ), effectively a 3×1 conditional Elo. Any ML model using Aligulac data should use these matchup-specific ratings rather than the aggregate rating as features.

## §7 — Rating systems in the thesis domain: StarCraft II and Age of Empires II

### StarCraft II: TrueSkill-derived MMR and Aligulac's Glicko variant

Battle.net's SC2 MMR system is TrueSkill-inspired with uncertainty tracking (confirmed by Liquipedia, with former Blizzard designer Josh Menke presenting on the system at BlizzCon 2010). MMR was made visible in Patch 3.4 (July 2016), and per-race MMR was introduced in Patch 3.7.0 (September 2016) — acknowledging that a player's skill varies across races. The ladder distributes players across seven leagues (Bronze through Grandmaster, top 200 per region), with MMR thresholds recalculated each season based on the prior distribution.

Aligulac ([Aligulac]) provides the most analytically transparent SC2 rating system. It uses a modified Glicko algorithm with three key features: per-matchup ratings (vP, vT, vZ) whose mean equals the overall rating, numerical optimization rather than Glicko's approximations, and a logistic distribution (switched from normal). Ratings update on discrete 2-week periods. Aligulac's calibration analysis over 100K+ games shows predicted win rates closely matching actuals up to ~80%, with slight overestimation beyond. The system tracks ~900 professional and semi-professional players. [Vinyals2019] validated that SC2's MMR-based win probability models closely match empirical results for both human players and AlphaStar, confirming the Elo/logistic framework's applicability to RTS games.

### Age of Empires II: standard Elo with strong linear calibration

AoE2 Definitive Edition uses a standard Elo system with the logistic function and K = 32 for all players. Players start at approximately 1000 Elo after 10 placement matches, with separate ratings per mode (1v1 Random Map, Team Random Map, Empire Wars). The system is simpler than SC2's — no uncertainty tracking, no per-civilization adjustment.

The [Porcpine2020] analysis (913,201 matches, May 2020) established the headline calibration result: r = 0.96 linear correlation between Elo difference and win probability, with a slope of approximately 1.1 percentage points per 10 rating points. Players with the superior rating won 54% of matches overall (reflecting the matchmaker's tendency to pair similarly-rated players). This strong linearity means Elo difference is a powerful baseline feature for AoE2 prediction.

Community data sources include aoe2.net (API for match, rating, and player data — the primary source), aoestats.io (civilization win rates by Elo bracket, map, and patch), aoe-elo.com (tournament-only ratings, analogous to Aligulac), and aoe2insights.com (player profiles). Before the Definitive Edition (2019), the competitive community used Voobly's Elo system for 14+ years, though it had known issues with rating inflation from "noob bashing" and a problematic 1600 starting Elo.

Mike Xie's community analysis found that XGBoost/Random Forest using Elo difference and civilization features achieved 77% accuracy for AoE2 HD win prediction — substantially above the ~54% baseline of Elo-only prediction when the matchmaker pairs similar players. This suggests that civilization identity provides substantial predictive signal beyond Elo difference in AoE2, consistent with Lin et al.'s intransitivity findings.

## §8 — Concrete implications for a comparative SC2-AoE2 thesis

### Recommended baselines differ by game

For **SC2**, the recommended baseline is Aligulac's per-matchup Glicko ratings if using professional data, or Battle.net MMR if using ladder data. Aligulac's three matchup-specific ratings (vP, vT, vZ) already condition on race asymmetry, providing a strong baseline that accounts for the primary source of intransitivity in SC2. The relevant expected-score formula uses the logistic CDF with the matchup-specific rating difference. For ladder data where Aligulac ratings are unavailable, the raw MMR difference should serve as the Elo-equivalent baseline, with the caveat that Battle.net's exact formula is not publicly disclosed.

For **AoE2**, a standard Elo baseline (logistic function with the ladder's K=32 ratings) provides the minimal baseline, supported by [Porcpine2020]'s r=0.96 calibration validation. However, this baseline is arguably unfair because it ignores civilization identity — information that is known pre-match and that Lin et al. (2024) showed to be strongly predictive due to intransitivity. The thesis should therefore report two baselines: plain Elo difference (the minimal baseline), and a conditional Elo or counter-adjusted baseline such as Lin et al.'s NCT or a per-civilization Elo variant. The gap between these two baselines quantifies how much predictive signal comes from civilization matchup structure alone, independent of ML.

### A unified baseline is possible but requires care

Both games' rating systems produce probabilities via the logistic function of rating difference, so in principle a single unified Elo-based baseline methodology can be reported across both. The procedure is: compute Elo (or MMR) difference, apply the standard logistic function, and evaluate via Brier score and log loss. However, the games differ enough that the calibration constants may differ — AoE2's K=32 and 400-divisor scale may not match SC2's TrueSkill-derived scale. The thesis should verify calibration separately for each game and report game-specific scaling corrections if needed, following the approach of Sonas's 83% squeeze factor for FIDE chess.

### Framing the hybrid ML+rating contribution

The thesis's core contribution can be framed as follows: rating systems provide a strong but assumption-limited baseline (transitivity, single scalar, no context); ML models can capture additional signal from civilization/race identity, map, player history features, and potentially in-game statistics. The relevant question is not whether ML beats Elo (it almost certainly will, given the literature's consistent 2–5 pp uplift), but how much of the uplift comes from each information source — skill difference vs. matchup asymmetry vs. contextual factors vs. temporal dynamics. Decomposing the uplift into these components would be a genuine thesis contribution, following the spirit of [Balduzzi2018]'s Hodge decomposition and [Fujii2023NBTR]'s NBTR distinction between transitive strength and intransitive matchup effects.

### Evaluating ratings as probabilistic forecasters

The [Dimitriadis2024] evaluation triptych — comprising calibration, discrimination (ROC/AUC), and a proper scoring rule (Brier or log loss) — applies directly to rating-system predictions. For each system, the logistic (or probit) expected-score formula produces a probability forecast for every match, which can be evaluated on all three dimensions. The thesis should report reliability diagrams for each baseline to visually assess calibration, complemented by the Brier score decomposition into reliability, resolution, and uncertainty. This evaluation framework makes the rating-system baseline and the ML model directly comparable as probabilistic forecasters — not merely as binary classifiers.

A specific prediction for AoE2: the plain Elo baseline will show good calibration on average (consistent with [Porcpine2020]'s findings) but poor conditional calibration when stratified by civilization matchup — particularly for matchups with strong counter-relationships identified by Lin et al. The ML model should show improved conditional calibration in these matchup-stratified subgroups, providing evidence that the uplift comes from modelling intransitivity rather than merely from having more parameters.

### The intransitivity question: is a standard Elo baseline even fair?

Given Lin et al.'s findings, using plain Elo as the sole AoE2 baseline risks a strawman comparison — the ML model may appear impressive simply because it learns civilization counters that Elo ignores by design. For a methodologically rigorous thesis, the fair comparison requires at least one intermediate baseline that accounts for civilization identity without ML (e.g., per-civilization-pair historical win rates, or a conditional Elo that adjusts for the known civilization matchup). The truly informative comparison is then: plain Elo → conditional Elo → ML model, with each step quantifying additional predictive value. This three-tier baseline structure would strengthen the thesis's contribution significantly.

For SC2, this concern is less acute because (a) the race matchup space is much smaller (3×3 vs. 45×45), (b) Aligulac already provides per-matchup ratings, and (c) SC2's race asymmetries are more nearly transitive. The contrast between the two games' baseline requirements is itself an interesting comparative finding.

## Conclusion: what the rating-system landscape means for the thesis

Three insights emerge from this review that should shape the thesis's methodology.

First, **Elo-family ratings are not naive baselines** — they are grounded in Bradley-Terry theory, produce proper probability forecasts, and are empirically robust even under model misspecification, as [Tang2025] demonstrates with no-regret guarantees. Any ML model that fails to meaningfully beat this baseline has not demonstrated genuine predictive value.

Second, **the asymmetry between SC2 and AoE2** in terms of matchup intransitivity creates a natural experiment: the same ML architecture should show larger uplift over Elo in AoE2 (where intransitivity is strong and Elo ignores it) than in SC2 (where Aligulac's per-matchup ratings already capture most of the asymmetry). Documenting this differential uplift would be a novel comparative finding.

Third, **the hybrid approach** of using rating-derived features within gradient-boosted or neural classifiers is well-established and consistently produces the strongest results across sports and esports domains — the thesis should adopt this as the primary modeling strategy while using the pure rating-system prediction as the properly specified baseline against which all improvements are measured.

No Polish-language academic sources on rating systems were identified beyond encyclopedia-level materials on the FIDE Elo system. The field's literature is overwhelmingly English-language.

## References

- [Aligulac] Kim, E. et al. Aligulac: StarCraft II professional player ratings. <https://aligulac.com/about/faq/>; source code <https://github.com/TheBB/aligulac>. [grey literature / live system]
- [Angelini2022] Angelini, G., Candila, V., & De Angelis, L. (2022). Weighted Elo rating for tennis match predictions. *European Journal of Operational Research* 297(1): 120–132. DOI: 10.1016/j.ejor.2021.04.011. [peer-reviewed journal]
- [Balduzzi2018] Balduzzi, D., Tuyls, K., Pérolat, J., & Graepel, T. (2018). Re-evaluating Evaluation. *Advances in Neural Information Processing Systems 31 (NeurIPS 2018)*. arXiv:1806.02643. <http://papers.neurips.cc/paper/7588-re-evaluating-evaluation.pdf> [peer-reviewed conference]
- [Bertrand2023] Bertrand, Q., Czarnecki, W.M., & Gidel, G. (2023). On the Limitations of the Elo, Real-World Games are Transitive, not Additive. *Proc. AISTATS 2023*, PMLR 206: 2905–2921. arXiv:2206.12301. <https://proceedings.mlr.press/v206/bertrand23a.html> [peer-reviewed conference]
- [BradleyTerry1952] Bradley, R.A. & Terry, M.E. (1952). Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons. *Biometrika* 39(3/4): 324–345. DOI: 10.1093/biomet/39.3-4.324. [peer-reviewed journal]
- [BT2025Survey] Li, Y. et al. (2025). Recent advances in the Bradley-Terry Model: theory, algorithms, and applications. *arXiv:2601.14727*. <https://arxiv.org/abs/2601.14727> [arXiv preprint]
- [Bunker2024] Bunker, R., Yeung, C., Susnjak, T., Espie, C., & Fujii, K. (2024). A comparative evaluation of Elo ratings- and machine learning-based methods for tennis match result prediction. *Proceedings of the Institution of Mechanical Engineers, Part P: Journal of Sports Engineering and Technology*. DOI: 10.1177/17543371231212235. [peer-reviewed journal]
- [Cattelan2012] Cattelan, M. (2012). Models for Paired Comparison Data: A Review with Emphasis on Dependent Data. *Statistical Science* 27(3): 412–433. DOI: 10.1214/12-STS396. [peer-reviewed journal]
- [Chen2016BladeChest] Chen, S. & Joachims, T. (2016). Modeling Intransitivity in Matchup and Comparison Data. *Proc. WSDM 2016*, pp. 227–236. <https://www.cs.cornell.edu/people/tj/publications/chen_joachims_16b.pdf> [peer-reviewed conference]
- [Coulom2008] Coulom, R. (2008). Whole-History Rating: A Bayesian Rating System for Players of Time-Varying Strength. *Computers and Games (CG 2008)*, LNCS 5131, pp. 113–124. DOI: 10.1007/978-3-540-87608-3_11. <https://www.remi-coulom.fr/WHR/WHR.pdf> [peer-reviewed conference]
- [Dangauthier2007] Dangauthier, P., Herbrich, R., Minka, T., & Graepel, T. (2007). TrueSkill Through Time: Revisiting the History of Chess. *Proc. NeurIPS 2007*, pp. 337–344. [peer-reviewed conference]
- [Dimitriadis2024] Dimitriadis, T., Gneiting, T., & Jordan, A.I. (2024). Evaluating probabilistic classifiers: The triptych. *International Journal of Forecasting* 40(1): 189–210. [peer-reviewed journal]
- [Ebtekar2021] Ebtekar, A. & Liu, P. (2021). Elo-MMR: A Rating System for Massive Multiplayer Competitions. *Proc. The Web Conference (WWW) 2021*. arXiv:2101.00400. <https://arxiv.org/abs/2101.00400> [peer-reviewed conference]
- [Elo1978] Elo, A.E. (1978). *The Rating of Chessplayers, Past and Present.* Arco Publishing, New York. ISBN 978-0-668-04721-0. [book]
- [EsportsBench] Thorrez, C. (2024). EsportsBench: A Benchmark of 20+ Esports Datasets for Paired Comparison Rating Systems. *Preprint*. <https://cthorrez.github.io/papers/esportsbench/EsportsBench_preprint.pdf> [grey literature / preprint]
- [FIDE2024] FIDE (2024). FIDE Rating Regulations. FIDE Handbook, B.02. <https://handbook.fide.com/chapter/B02RBRegulations202210> [official regulation]
- [Fujii2023NBTR] Fujii, K. (2023). Neural Bradley-Terry Rating: Quantifying Properties from Comparisons. *arXiv:2307.13709*. <https://arxiv.org/abs/2307.13709> [arXiv preprint]
- [Glickman1999] Glickman, M.E. (1999). Parameter Estimation in Large Dynamic Paired Comparison Experiments. *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 48(3): 377–394. DOI: 10.1111/1467-9876.00159. [peer-reviewed journal]
- [Glickman2001] Glickman, M.E. (2001). Dynamic Paired Comparison Models with Stochastic Variances. *Journal of Applied Statistics* 28(6): 673–689. DOI: 10.1080/02664760120059219. [peer-reviewed journal]
- [Glickman2013TR] Glickman, M.E. (2013). Example of the Glicko-2 system. Technical report. <https://www.glicko.net/glicko/glicko2.pdf> [technical report]
- [Glickman2024TR] Glickman, M.E. Rating the Chess Rating System. Technical report, Boston University. <https://glicko.net/research/chance.pdf> [technical report]
- [Glickman2025] Glickman, M.E. & Jones, A.C. (2025). Models and Rating Systems for Head-to-Head Competition. *Annual Review of Statistics and Its Application* 12: 259–282. DOI: 10.1146/annurev-statistics-040722-061813. [peer-reviewed journal]
- [Gneiting2007] Gneiting, T. & Raftery, A.E. (2007). Strictly Proper Scoring Rules, Prediction, and Estimation. *Journal of the American Statistical Association* 102(477): 359–378. DOI: 10.1198/016214506000001437. [peer-reviewed journal]
- [Hamilton2025] Hamilton, N., Kalenkova, A., & Roughan, M. (2025). The impact of intransitivity on the Elo rating system. *PLOS ONE* 20(12): e0338261. DOI: 10.1371/journal.pone.0338261. [peer-reviewed journal]
- [Herbrich2007] Herbrich, R., Minka, T., & Graepel, T. (2007). TrueSkill™: A Bayesian Skill Rating System. *Proc. NeurIPS 2006*, pp. 569–576. <https://www.microsoft.com/en-us/research/publication/trueskilltm-a-bayesian-skill-rating-system/> [peer-reviewed conference]
- [Hunter2004] Hunter, D.R. (2004). MM algorithms for generalized Bradley-Terry models. *Annals of Statistics* 32(1): 384–406. DOI: 10.1214/aos/1079120141. [peer-reviewed journal]
- [Hvattum2010] Hvattum, L.M. & Arntzen, H. (2010). Using ELO ratings for match result prediction in association football. *International Journal of Forecasting* 26(3): 460–470. DOI: 10.1016/j.ijforecast.2009.10.002. [peer-reviewed journal]
- [Joshy2024] Joshy, V. (2024). OpenSkill: A faster asymmetric multi-team, multiplayer rating system. *Journal of Open Source Software* 9(93): 5901. arXiv:2401.05451. <https://arxiv.org/abs/2401.05451> [peer-reviewed journal]
- [Kovalchik2016] Kovalchik, S.A. (2016). Searching for the GOAT of tennis win prediction. *Journal of Quantitative Analysis in Sports* 12(3): 127–138. DOI: 10.1515/jqas-2015-0059. [peer-reviewed journal]
- [Lin2024NCT] Lin, C.-C., Shih, Y.-W., Kuo, K.-T., Chen, Y.-C., Chen, C.-H., Chiu, W.-C., & Wu, I.-C. (2024). Identifying and Clustering Counter Relationships of Team Compositions in PvP Games for Efficient Balance Analysis. *Transactions on Machine Learning Research (TMLR)*. ISSN 2835-8856. arXiv:2408.17180. <https://arxiv.org/abs/2408.17180> [peer-reviewed journal]
- [Lin2025EloRCC] Lin, C.-C. & Wu, I.-C. (2025). Online Learning of Counter Categories and Ratings in PvP Games. *arXiv:2502.03998*. <https://arxiv.org/abs/2502.03998> [arXiv preprint]
- [Luce1959] Luce, R.D. (1959). *Individual Choice Behavior: A Theoretical Analysis.* Wiley, New York; Dover reprint 2005. ISBN 978-0-486-44136-8. [book]
- [Minka2018TR] Minka, T., Cleven, R., & Zaykov, Y. (2018). TrueSkill 2: An improved Bayesian skill rating system. Microsoft Technical Report MSR-TR-2018-8. <https://www.microsoft.com/en-us/research/publication/trueskill-2-improved-bayesian-skill-rating-system/> [technical report]
- [Plackett1975] Plackett, R.L. (1975). The Analysis of Permutations. *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 24(2): 193–202. DOI: 10.2307/2346567. [peer-reviewed journal]
- [Porcpine2020] porcpine1967 (2020). Impact of Rating Difference on Win Percentage in Age of Empires II Definitive Edition. Community analysis. <https://porcpine1967.github.io/aoe2_comparisons/elo/> [grey literature]
- [Sipko2015] Sipko, M. (2015). *Machine Learning for the Prediction of Professional Tennis Matches.* MEng thesis, Imperial College London. <https://www.doc.ic.ac.uk/teaching/distinguished-projects/2015/m.sipko.pdf> [master's thesis]
- [Tang2025] Tang, S., Wang, Y., & Jin, C. (2025). Is Elo Rating Reliable? A Study Under Model Misspecification. *arXiv:2502.10985*. <https://arxiv.org/abs/2502.10985> [arXiv preprint]
- [Thurstone1927] Thurstone, L.L. (1927). A law of comparative judgment. *Psychological Review* 34(4): 273–286. [peer-reviewed journal]
- [Vinyals2019] Vinyals, O., Babuschkin, I., Czarnecki, W.M., et al. (2019). Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning. *Nature* 575: 350–354. DOI: 10.1038/s41586-019-1724-z. [peer-reviewed journal]
- [WengLin2011] Weng, R.C. & Lin, C.-J. (2011). A Bayesian Approximation Method for Online Ranking. *Journal of Machine Learning Research* 12: 267–300. [peer-reviewed journal]
- [Zermelo1929] Zermelo, E. (1929). Die Berechnung der Turnier-Ergebnisse als ein Maximumproblem der Wahrscheinlichkeitsrechnung. *Mathematische Zeitschrift* 29: 436–460. [peer-reviewed journal]

## BibTeX appendix

```bibtex
@misc{Aligulac,
  author = {Kim, Espen and others},
  title = {Aligulac: {StarCraft II} professional player ratings},
  howpublished = {\url{https://aligulac.com/about/faq/}},
  note = {Source code: \url{https://github.com/TheBB/aligulac}}
}

@article{Angelini2022,
  author = {Angelini, Giovanni and Candila, Vincenzo and De Angelis, Luca},
  title = {Weighted {Elo} rating for tennis match predictions},
  journal = {European Journal of Operational Research},
  year = {2022},
  volume = {297},
  number = {1},
  pages = {120--132},
  doi = {10.1016/j.ejor.2021.04.011}
}

@inproceedings{Balduzzi2018,
  author = {Balduzzi, David and Tuyls, Karl and Pérolat, Julien and Graepel, Thore},
  title = {Re-evaluating Evaluation},
  booktitle = {Advances in Neural Information Processing Systems 31 (NeurIPS 2018)},
  year = {2018}
}

@inproceedings{Bertrand2023,
  author = {Bertrand, Quentin and Czarnecki, Wojciech M. and Gidel, Gauthier},
  title = {On the Limitations of the {Elo}, Real-World Games are Transitive, not Additive},
  booktitle = {Proc. AISTATS 2023},
  series = {PMLR},
  volume = {206},
  year = {2023},
  pages = {2905--2921}
}

@article{BradleyTerry1952,
  author = {Bradley, Ralph Allan and Terry, Milton E.},
  title = {Rank Analysis of Incomplete Block Designs: {I}. The Method of Paired Comparisons},
  journal = {Biometrika},
  year = {1952},
  volume = {39},
  number = {3/4},
  pages = {324--345},
  doi = {10.1093/biomet/39.3-4.324}
}

@article{BT2025Survey,
  author = {Li, Yingqi and others},
  title = {Recent advances in the {Bradley--Terry} Model: theory, algorithms, and applications},
  journal = {arXiv preprint arXiv:2601.14727},
  year = {2025}
}

@article{Bunker2024,
  author = {Bunker, Rory and Yeung, Calvin and Susnjak, Teo and Espie, Chester and Fujii, Keisuke},
  title = {A comparative evaluation of {Elo} ratings- and machine learning-based methods for tennis match result prediction},
  journal = {Proceedings of the Institution of Mechanical Engineers, Part P: Journal of Sports Engineering and Technology},
  year = {2024},
  doi = {10.1177/17543371231212235}
}

@article{Cattelan2012,
  author = {Cattelan, Manuela},
  title = {Models for Paired Comparison Data: A Review with Emphasis on Dependent Data},
  journal = {Statistical Science},
  year = {2012},
  volume = {27},
  number = {3},
  pages = {412--433},
  doi = {10.1214/12-STS396}
}

@inproceedings{Chen2016BladeChest,
  author = {Chen, Shuo and Joachims, Thorsten},
  title = {Modeling Intransitivity in Matchup and Comparison Data},
  booktitle = {Proc. WSDM 2016},
  year = {2016},
  pages = {227--236}
}

@inproceedings{Coulom2008,
  author = {Coulom, Rémi},
  title = {Whole-History Rating: A Bayesian Rating System for Players of Time-Varying Strength},
  booktitle = {Computers and Games (CG 2008)},
  series = {LNCS},
  volume = {5131},
  year = {2008},
  pages = {113--124},
  doi = {10.1007/978-3-540-87608-3_11}
}

@inproceedings{Dangauthier2007,
  author = {Dangauthier, Pierre and Herbrich, Ralf and Minka, Tom and Graepel, Thore},
  title = {{TrueSkill} Through Time: Revisiting the History of Chess},
  booktitle = {Proc. NeurIPS 2007},
  year = {2007},
  pages = {337--344}
}

@article{Dimitriadis2024,
  author = {Dimitriadis, Timo and Gneiting, Tilmann and Jordan, Alexander I.},
  title = {Evaluating probabilistic classifiers: The triptych},
  journal = {International Journal of Forecasting},
  year = {2024},
  volume = {40},
  number = {1},
  pages = {189--210}
}

@inproceedings{Ebtekar2021,
  author = {Ebtekar, Aram and Liu, Paul},
  title = {{Elo-MMR}: A Rating System for Massive Multiplayer Competitions},
  booktitle = {Proc. The Web Conference (WWW) 2021},
  year = {2021}
}

@book{Elo1978,
  author = {Elo, Arpad E.},
  title = {The Rating of Chessplayers, Past and Present},
  publisher = {Arco Publishing},
  address = {New York},
  year = {1978},
  isbn = {978-0-668-04721-0}
}

@misc{EsportsBench,
  author = {Thorrez, Calvin},
  title = {{EsportsBench}: A Benchmark of 20+ Esports Datasets for Paired Comparison Rating Systems},
  howpublished = {Preprint, \url{https://cthorrez.github.io/papers/esportsbench/EsportsBench_preprint.pdf}},
  year = {2024}
}

@misc{FIDE2024,
  author = {{FIDE}},
  title = {{FIDE} Rating Regulations},
  howpublished = {FIDE Handbook, B.02},
  year = {2024},
  url = {https://handbook.fide.com/chapter/B02RBRegulations202210}
}

@article{Fujii2023NBTR,
  author = {Fujii, Keisuke},
  title = {Neural {Bradley-Terry} Rating: Quantifying Properties from Comparisons},
  journal = {arXiv preprint arXiv:2307.13709},
  year = {2023}
}

@article{Glickman1999,
  author = {Glickman, Mark E.},
  title = {Parameter Estimation in Large Dynamic Paired Comparison Experiments},
  journal = {Journal of the Royal Statistical Society: Series C (Applied Statistics)},
  year = {1999},
  volume = {48},
  number = {3},
  pages = {377--394},
  doi = {10.1111/1467-9876.00159}
}

@article{Glickman2001,
  author = {Glickman, Mark E.},
  title = {Dynamic Paired Comparison Models with Stochastic Variances},
  journal = {Journal of Applied Statistics},
  year = {2001},
  volume = {28},
  number = {6},
  pages = {673--689},
  doi = {10.1080/02664760120059219}
}

@techreport{Glickman2013TR,
  author = {Glickman, Mark E.},
  title = {Example of the {Glicko-2} system},
  year = {2013},
  url = {https://www.glicko.net/glicko/glicko2.pdf}
}

@techreport{Glickman2024TR,
  author = {Glickman, Mark E.},
  title = {Rating the Chess Rating System},
  institution = {Boston University},
  url = {https://glicko.net/research/chance.pdf}
}

@article{Glickman2025,
  author = {Glickman, Mark E. and Jones, Alexander C.},
  title = {Models and Rating Systems for Head-to-Head Competition},
  journal = {Annual Review of Statistics and Its Application},
  year = {2025},
  volume = {12},
  pages = {259--282},
  doi = {10.1146/annurev-statistics-040722-061813}
}

@article{Gneiting2007,
  author = {Gneiting, Tilmann and Raftery, Adrian E.},
  title = {Strictly Proper Scoring Rules, Prediction, and Estimation},
  journal = {Journal of the American Statistical Association},
  year = {2007},
  volume = {102},
  number = {477},
  pages = {359--378},
  doi = {10.1198/016214506000001437}
}

@article{Hamilton2025,
  author = {Hamilton, Nicholas and Kalenkova, Anna and Roughan, Matthew},
  title = {The impact of intransitivity on the {Elo} rating system},
  journal = {PLOS ONE},
  year = {2025},
  volume = {20},
  number = {12},
  pages = {e0338261},
  doi = {10.1371/journal.pone.0338261}
}

@inproceedings{Herbrich2007,
  author = {Herbrich, Ralf and Minka, Tom and Graepel, Thore},
  title = {{TrueSkill}: A Bayesian Skill Rating System},
  booktitle = {Proc. NeurIPS 2006},
  year = {2007},
  pages = {569--576}
}

@article{Hunter2004,
  author = {Hunter, David R.},
  title = {{MM} algorithms for generalized {Bradley-Terry} models},
  journal = {Annals of Statistics},
  year = {2004},
  volume = {32},
  number = {1},
  pages = {384--406},
  doi = {10.1214/aos/1079120141}
}

@article{Hvattum2010,
  author = {Hvattum, Lars Magnus and Arntzen, Halvard},
  title = {Using {ELO} ratings for match result prediction in association football},
  journal = {International Journal of Forecasting},
  year = {2010},
  volume = {26},
  number = {3},
  pages = {460--470},
  doi = {10.1016/j.ijforecast.2009.10.002}
}

@article{Joshy2024,
  author = {Joshy, Vivek},
  title = {{OpenSkill}: A faster asymmetric multi-team, multiplayer rating system},
  journal = {Journal of Open Source Software},
  year = {2024},
  volume = {9},
  number = {93},
  pages = {5901}
}

@article{Kovalchik2016,
  author = {Kovalchik, Stephanie A.},
  title = {Searching for the {GOAT} of tennis win prediction},
  journal = {Journal of Quantitative Analysis in Sports},
  year = {2016},
  volume = {12},
  number = {3},
  pages = {127--138},
  doi = {10.1515/jqas-2015-0059}
}

@article{Lin2024NCT,
  author = {Lin, Chiu-Chou and Shih, Yi-Wei and Kuo, Kuei-Ting and Chen, Yu-Cheng and Chen, Chien-Hua and Chiu, Wei-Chen and Wu, I-Chen},
  title = {Identifying and Clustering Counter Relationships of Team Compositions in {PvP} Games for Efficient Balance Analysis},
  journal = {Transactions on Machine Learning Research},
  year = {2024},
  issn = {2835-8856}
}

@article{Lin2025EloRCC,
  author = {Lin, Chiu-Chou and Wu, I-Chen},
  title = {Online Learning of Counter Categories and Ratings in {PvP} Games},
  journal = {arXiv preprint arXiv:2502.03998},
  year = {2025}
}

@book{Luce1959,
  author = {Luce, R. Duncan},
  title = {Individual Choice Behavior: A Theoretical Analysis},
  publisher = {Wiley},
  address = {New York},
  year = {1959},
  note = {Dover reprint 2005},
  isbn = {978-0-486-44136-8}
}

@techreport{Minka2018TR,
  author = {Minka, Tom and Cleven, Ryan and Zaykov, Yordan},
  title = {{TrueSkill 2}: An improved Bayesian skill rating system},
  institution = {Microsoft Research},
  number = {MSR-TR-2018-8},
  year = {2018}
}

@article{Plackett1975,
  author = {Plackett, Robin L.},
  title = {The Analysis of Permutations},
  journal = {Journal of the Royal Statistical Society: Series C (Applied Statistics)},
  year = {1975},
  volume = {24},
  number = {2},
  pages = {193--202},
  doi = {10.2307/2346567}
}

@misc{Porcpine2020,
  author = {{porcpine1967}},
  title = {Impact of Rating Difference on Win Percentage in {Age of Empires II Definitive Edition}},
  howpublished = {\url{https://porcpine1967.github.io/aoe2_comparisons/elo/}},
  year = {2020}
}

@mastersthesis{Sipko2015,
  author = {Sipko, Michal},
  title = {Machine Learning for the Prediction of Professional Tennis Matches},
  school = {Imperial College London},
  year = {2015}
}

@article{Tang2025,
  author = {Tang, Shange and Wang, Yuanhao and Jin, Chi},
  title = {Is {Elo} Rating Reliable? A Study Under Model Misspecification},
  journal = {arXiv preprint arXiv:2502.10985},
  year = {2025}
}

@article{Thurstone1927,
  author = {Thurstone, Louis L.},
  title = {A law of comparative judgment},
  journal = {Psychological Review},
  year = {1927},
  volume = {34},
  number = {4},
  pages = {273--286}
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

@article{WengLin2011,
  author = {Weng, Ruby C. and Lin, Chih-Jen},
  title = {A Bayesian Approximation Method for Online Ranking},
  journal = {Journal of Machine Learning Research},
  year = {2011},
  volume = {12},
  pages = {267--300}
}

@article{Zermelo1929,
  author = {Zermelo, Ernst},
  title = {Die {Berechnung} der {Turnier-Ergebnisse} als ein {Maximumproblem} der {Wahrscheinlichkeitsrechnung}},
  journal = {Mathematische Zeitschrift},
  year = {1929},
  volume = {29},
  pages = {436--460}
}
```
