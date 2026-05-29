---
title: "SC2EGSet Step 02_02_01 source-anchor / column-naming / direction-policy adjudication (Layer-1 planning PR; Round 2)"
category: A
branch: feat/sc2egset-02-02-01-symmetry-difference-adjudication
base_ref: master
base_sha: 9abcd6bc62e1de21172970baf84aa863c4423a1b
predecessor_pr: 266
predecessor_pr_merge_sha: 9abcd6bc62e1de21172970baf84aa863c4423a1b
dataset: sc2egset
phase: "02"
pipeline_section: "02_02 — Symmetry & Difference Features"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
revision_round: 2
revision_basis: "Round 1 reviewer-adversarial HOLD verdict (B1: vacuous F4 pair-operation framing; B2: A14 algebra error on product redundancy; B3: abs_diff exclusion incompatible with LogReg under I8); user-bound resolution: drop F4 as pair operation; fix A14 algebra and per-transform decisions; include abs_diff as default symmetric magnitude."
draft_pr_files:
  - planning/current_plan.md
  - planning/current_plan.critique.md
future_execution_files:
  - src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_feature_scope.py
  - tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_symmetry_difference_feature_scope.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.py
  - sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.ipynb
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.md
  - planning/INDEX.md
  - CHANGELOG.md
  - pyproject.toml
future_execution_file_count: 9
target_version_bump: "3.84.0 -> 3.85.0"
critique_required: true
research_log_ref: null
date: 2026-05-29
---

## Scope

Execute `.claude/rules/data-analysis-lineage.md` "Non-batching rule for empirical
work" sequence step 6 ("Next validation module") in its per-precedent adjudication
specialisation: PR #233 → PR #234 for Step 02_01_02 (source-anchor / race-column
adjudication producing one CSV+MD artifact pair) and PR #241 → PR #242 for Step
02_01_03 (source/anchor/cold-start adjudication producing one CSV+MD artifact
pair). PR #266 (merged 2026-05-29 at master `9abcd6bc`) delivered the scaffold-
stage validator. The next atomic unit is the binding source-anchor / column-naming
/ direction-policy adjudication, recorded as one CSV+MD artifact pair under the
canonical reports path, gated by the PR #266 validator over the now-pinned
candidate spec list. This adjudication does not materialise any feature value.

**Two-PR sequence on branch `feat/sc2egset-02-02-01-symmetry-difference-adjudication`.**

1. **THIS Layer-1 planning PR** writes only two files:
   - `planning/current_plan.md` (this document);
   - `planning/current_plan.critique.md` (Round 2 reviewer-adversarial output).
2. **FUTURE Layer-2 execution PR on the same branch** performs the 9-file manifest
   below (adjudicator module + mirrored test + jupytext notebook pair + 1-row CSV
   + per-§ MD + `pyproject.toml` + `planning/INDEX.md` + `CHANGELOG.md`).

**Explicitly out of scope** for both PRs:

- feature value materialization (NO Parquet under
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/`
  matching `*_features.parquet`; NO CROSS-02-01 audit JSON+MD pair under
  `reports/artifacts/02_02_01/`);
- a second validator module (the PR #266 validator covers every structural
  property; this PR pins the candidate list and direction policy as data, not
  as code);
- STEP_STATUS.yaml additions for `02_02_01` (closure deferred to a future
  U2.B-style PR analogous to PR #237 / PR #262 post-materialisation);
- PIPELINE_SECTION_STATUS.yaml `02_02` row addition (deferred per PR #230
  precedent — section row first lands at step closure, not at adjudication);
- PHASE_STATUS.yaml mutation (Phase 02 stays `in_progress`; Phase 03 stays
  `not_started`);
- ROADMAP.md body edits (the `02_02_01` block at lines 2853–3131 remains
  byte-identical);
- root `reports/research_log.md` and per-dataset `research_log.md` edits
  (per non-batching sequence — research_log appended only at step closure,
  sequence step 8; not at adjudication);
- thesis chapters, bib, appendix, `docs/**`, `.claude/**`, `data/**`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- Step `02_02_02+`; Step `02_01_04`; Phase 03; any baseline modeling;
- reopen of Q5 / Q6 / Q6F / Q6G / Q6H / `reconstructed_rating` closure;
- new MMR scalar feature (PR #234 `is_mmr_missing` flag precedent stands);
- new tracker-derived target-match feature (Invariant I3);
- AoE2 `civilization` vocabulary (SC2EGSet uses `race` exclusively per
  Invariant I8 cross-game hygiene);
- any matchup-history pair operation (B1: dropped — see A20);
- the `sum`, `product`, and ratio transforms over numeric focal/opponent pairs
  (B2: per-transform decisions in A14; see §"Candidate feature families").

## Problem Statement

PR #266 produced a name- and direction-aware validator that gates proposed
candidate specs but does not itself pin them. The validator's three parameters —
`designed_difference_specs`, `designed_symmetric_pair_specs`,
`designed_race_pair_candidate_specs` (validator public function lines 682–688) —
are tuples of `CandidateFeatureSpec` produced by the notebook caller. PR #265
plan §"Open Questions" OQ8 (race-pair `02_02` vs `02_05`), OQ9 (cross-region
BOOLEAN-pair `02_02` vs `02_03+`), OQ10 (symmetric pair mean/sum/product
tabular vs GNN) explicitly defer the binding scope decision to a future PR.

The Round 1 plan additionally introduced three methodological errors that
Round 1 reviewer-adversarial (HOLD) identified:

- **B1 (vacuous F4 pair operation).** Round 1 framed F4 "Matchup history pair
  operations" as a focal/opponent pair, but `matchup_h2h_focal_win_rate` is a
  SINGLE audited column in the 24-tuple at line 130; there is no
  `matchup_h2h_opponent_win_rate` audited counterpart. Treating it as a paired
  focal/opponent operation with "implicit complement `1 − matchup_h2h_focal_win_rate`"
  produces the affine `2·focal − 1`, which is zero information gain for linear
  models and zero splitting effect for trees.
- **B2 (A14 algebra error).** Round 1 said "drop `product` because mean × 2 =
  sum." Correct algebra: `sum = focal + opponent = 2·mean`, so `sum` (not
  `product`) is the redundant transform with respect to `mean`. `product = focal ×
  opponent` is a genuine multiplicative interaction. Each transform requires
  its own independent methodological decision.
- **B3 (abs_diff exclusion incompatible with LogReg under I8).** Invariant I8
  (lines 197–214 of `.claude/scientific-invariants.md`) binds the SC2/AoE2
  cross-game protocol to include logistic regression. For LogReg,
  `|focal − opponent|` is NOT a linear function of `(focal − opponent)` and
  CANNOT be recovered. Round 1's "tree models can route the sign" rationale
  leaves LogReg without a way to express symmetric magnitude.

Without a written adjudication that:

1. enumerates the binding list of candidate symmetric/difference features that
   the future materialisation PR may emit,
2. annotates each candidate with its `direction` ∈ {`focal_minus_opponent`,
   `symmetric`},
3. ties each candidate to the audited 7-tuple / 24-tuple source columns,
4. records the row-identity join policy (`focal_match_id`, `focal_player`,
   `opponent_player`, `started_at`),
5. provides a per-transform independent decision (mean / abs_diff / sum /
   product / ratio) so that LogReg has a symmetric-magnitude expressive
   surface (B3),
6. resolves the matchup-history transform scope without false-pair framing
   (B1; see A20),
7. binds the cross-region BOOLEAN-pair transform set (`either`, `both`, `xor`)
   with each transform's independence rationale,
8. resolves the three open methodology boundaries (race-pair → 02_05;
   cross-region BOOLEAN-pair → 02_02; symmetric-pair-aggregate → tabular with
   `(mean, abs_diff)` only),

the future materialisation PR has no machine-checkable contract to bind against.

`.claude/rules/data-analysis-lineage.md` lines 109–119 ("Feature-engineering
discipline") require every feature family to declare dataset, source
table/event family, prediction setting, feature table grain, temporal anchor,
allowed cutoff rule, leakage falsifier, cold-start behavior, and lineage
artifact. PR #266 declares three of these structurally (source family,
temporal anchor inheritance, leakage falsifier); this adjudication PR declares
the remaining six per candidate and records them as a CSV+MD artifact pair.

Step 02_01_02 followed exactly this ladder (PR #233 scaffold → PR #234
source/anchor/race adjudication CSV+MD pair → PR #235 materialisation
planning → PR #236 materialisation execution + CROSS-02-01 audit) verified at
`planning/INDEX.md` archive rows for PRs #233–#237. Step 02_01_03 followed
the same ladder with a larger Q-chain (PR #241 scaffold → PR #242 adjudication
→ … → PR #259 materialisation). This PR is the analogous next rung for Step
02_02_01.

## Literature Context

**Manual binding (must justify each cited).** Per `.claude/rules/data-analysis-
lineage.md` §"Feature-engineering discipline," each candidate family in the
adjudication must declare temporal anchor + cutoff rule + leakage falsifier +
cold-start behavior + lineage artifact.

`02_FEATURE_ENGINEERING_MANUAL.md` §3 lines 43–59 ("Symmetry in Pairwise
Prediction Demands Difference Features") establishes the Bradley-Terry
connection (Bradley & Terry 1952): for latent strengths β_i,
`P(i > j) = 1 / (1 + e^(β_j − β_i))`, so the logit of win probability equals
the **difference** of latent strengths. Line 51: "difference features ...
preferred for most models." Line 53: "Ratio features: for strictly positive
features, use $x_A / x_B$ or equivalently $\log(x_A) - \log(x_B)$." Lines
55–57: canonical ordering with concatenation introduces slot bias; symmetric
kernels (Hue & Vert ICML 2010; Zaheer et al. 2017 "Deep Sets") are
permutation-invariant. **Difference as default** for this adjudication; the
canonical-ordering family is rejected outright (slot bias incompatible with
Invariant I5).

**Invariant I8 binds LogReg into the cross-game protocol (B3 anchor).**
`.claude/scientific-invariants.md` Invariant I8 (lines 197–214) requires
that "Both games use the same ML methods (logistic regression, random forest,
gradient boosted trees), the same evaluation metrics, and a common statistical
comparison methodology." For LogReg the model is
`logit P(focal wins) = w₀ + Σ w_k · φ_k(x_focal, x_opponent)`. If `φ_k` is the
signed difference `focal − opponent`, then magnitude information
`|focal − opponent|` cannot be linearly recovered from the signed term —
the LogReg basis must include `abs_diff` explicitly to express a
"how-far-apart-are-the-players" feature symmetrically. For tree models the
absolute term is a piecewise-linear function of the signed term and is
recoverable; for LogReg it is not. **Therefore `abs_diff` is the canonical
symmetric magnitude transform for every eligible numeric focal/opponent pair
in this adjudication's binding set.** This is the B3 anchor.

`.claude/scientific-invariants.md` Invariant I5 (lines 156–170) binds: "The
model input is always structured as `(focal_player_features, opponent_features,
context_features)` and this structure is identical regardless of which player
is focal." The adjudication binds I5 at the candidate-spec layer (every
`direction == "focal_minus_opponent"` candidate trace to a `focal_*` /
`opponent_*` source pair; every `direction == "symmetric"` candidate is
permutation-invariant under focal/opponent swap).

`.claude/scientific-invariants.md` Invariant I3 (lines 130–148) binds the
temporal cutoff inherited from `02_01_03`: `history_time < target_time`
strict, enforced at `02_01_03` materialisation via
`TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at` (verified at
`02_01_03/leakage_audit_sc2egset.json:86`). The adjudication declares that
every candidate inherits this cutoff via the audited 7-tuple / 24-tuple
columns; no candidate may introduce a new time-aware operation.

**Three precedent adjudications cited as shape sources:**

- PR #234 (`02_01_02_source_anchor_race_adjudication.{csv,md}`): 3-decision
  adjudication, 8-section MD, 24-column CSV with per-decision provenance
  SHAs.
- PR #242 (`02_01_03_history_source_anchor_coldstart_adjudication.{csv,md}`):
  8-decision adjudication (Q1–Q8), 33-column CSV, §1–§14 MD.
- PR #245 (`02_01_03_history_rating_reconstruction_adjudication.{csv,md}`):
  Q6 6-candidate adjudication with 31-column CSV, 18-section MD.

This adjudication follows the PR #234 shape (smaller decision tree;
single-row CSV recording the unified adjudication; MD per-§ rationale) rather
than the larger PR #242/#245 multi-row decision-table shape, because the
`02_02_01` adjudication has **one** binding scope question with multiple
candidate families inside it, rather than multiple coupled Q-questions.

**[OPINION on B2 `product` transform.]** Pair product `focal × opponent` is
not algebraically expressible from `(mean, abs_diff)` alone — it is a genuine
multiplicative interaction. Under the Hue & Vert (2010) symmetric kernel
formulation, the `product` transform is the canonical 2-degree symmetric
polynomial counterpart to the canonical 1-degree symmetric polynomial
(`mean`). However, `02_FEATURE_ENGINEERING_MANUAL.md` §6 lines 131–135
positions categorical and numeric interactions as a Pipeline Section 02_05
concern. The 02_02 layer is structurally tighter (sym/diff TRANSFORMS over
identity-paired numeric columns) than the 02_05 layer (encoded interactions
across heterogeneous columns). Deferring `product` to 02_05 keeps 02_02's
contract narrow without losing the multiplicative-interaction surface for
Phase 04. Re-open trigger: if a future Phase 04 ablation study finds a
methodological need for `product` at the 02_02 layer (e.g., a non-monotone
interaction that 02_05's matchup-conditioned encoding cannot capture),
re-bind in a follow-up PR.

**[OPINION on `sum` exclusion.]** Pair sum `focal + opponent = 2·mean` is an
affine duplicate of `pair_mean`. Including both is a feature-set redundancy
that wastes column budget without information gain for any model class
(LogReg, RF, GBT). Per `.claude/rules/python-code.md` "No magic numbers" the
exclusion rationale is recorded as a binding methodological decision, not a
size-fits-all rule.

**[OPINION on ratio family.]** Ratio features (`focal_X / opponent_X`)
excluded for tabular Phase 04 scope: zero-bounded denominators in
`opponent_prior_win_rate_*` columns (cold start) and in
`opponent_prior_match_count` (cold start → 0). The log-ratio degenerates to
a difference for already-log-transformed columns (not currently in 02_01_03
24-tuple), so excluding ratios costs no expressivity beyond what differences
+ abs_diff already capture. The future materialisation PR may revisit if a
non-zero-bounded log-transformed denominator family emerges in `02_03+`.

**[OPINION on F4 / matchup history transform.]** B1 evidence: the 24-tuple
contains exactly ONE matchup-history column (`matchup_h2h_focal_win_rate`,
line 130) and ONE non-rate count column (`matchup_h2h_count`, line 129).
There is no audited `matchup_h2h_opponent_win_rate` because the H2H rate is
conditioned on focal's perspective by construction; the opponent rate against
focal would be `1 − matchup_h2h_focal_win_rate` only if the prior matches
were strictly decisive AND symmetric, neither of which is structurally
guaranteed by the 02_01_03 spec. Even if it were, the resulting candidate
`2·focal − 1` is an affine transform of the same column — zero new
information for any linear model basis, zero new split for any tree model.
**Decision: drop F4 entirely from the binding adjudication.** The
`matchup_h2h_focal_win_rate` column remains available as a base unary feature
to Phase 04 directly via 02_01_03 history-enriched Parquet (it does not need a
02_02 transform to be modeled). See A20.

## Assumptions & Unknowns

- **A1 (Outcome A justified).** Outcomes B–G rejected (cited in chat-side
  planning output and in §"Adjudication outcomes" of `current_plan.critique.md`).
  Outcome A is the only sequence-step-6-compliant outcome under
  `.claude/rules/data-analysis-lineage.md` given that PR #234 / PR #242 are
  the canonical precedents for "after scaffold + 1 validator, before
  materialisation" on a per-Step basis.
- **A2 (Branch name).** `feat/sc2egset-02-02-01-symmetry-difference-
  adjudication` mirrors PR #234 idiom `feat/sc2egset-02-01-02-source-anchor-
  race-adjudication` (step → subject-suffix → `-adjudication`). Verified
  against `planning/INDEX.md` archive row for PR #234. Deviates from the
  PR #266 scaffold branch by replacing the `-scaffold` suffix with
  `-adjudication`.
- **A3 (Version bump 3.84.0 → 3.85.0).** Minor; per `.claude/rules/git-
  workflow.md` "minor for feat/refactor/docs." Matches PR #234 version step
  3.68.0 → 3.69.0 (minor), PR #242 3.72.0 → 3.73.0 (minor), PR #245 3.74.0 →
  3.75.0 (minor). The bump lands in the Layer-2 execution PR, not in this
  Layer-1 planning PR.
- **A4 (Adjudicator module name).**
  `adjudicate_symmetry_difference_feature_scope.py` per the existing repo
  precedent that adjudicator modules carry the family-scope name with the
  `adjudicate_` prefix. Verified: `adjudicate_pre_game_source_layer.py`
  (PR #234), `adjudicate_history_enriched_pre_game_source_layer.py`
  (PR #242), `adjudicate_history_cross_region_retention.py` (PR #243),
  `adjudicate_history_rating_reconstruction.py` (PR #245). All carry the
  family suffix; none use a stage marker in the filename.
- **A5 (Notebook filename and overwrite contract).**
  `02_02_01_symmetry_difference_feature_adjudication.{py,ipynb}` per
  `sandbox/README.md` single-notebook-per-Step contract OVERWRITTEN in
  place by the future materialisation PR. The scaffold notebook
  `02_02_01_symmetry_difference_feature_materialization.{py,ipynb}` created
  by PR #266 is NOT overwritten by this PR — adjudication has its own
  notebook because the artifact emitted differs (CSV+MD adjudication pair vs
  scaffold no-emit). The materialisation PR (analogue of PR #259) will
  overwrite the scaffold notebook in place; this PR creates a sibling
  notebook with `_adjudication` suffix. Verified precedent: PR #234's
  notebook is `02_01_02_source_anchor_race_adjudication.{py,ipynb}` (separate
  from PR #233's scaffold notebook), and PR #259 overwrote PR #241's
  scaffold notebook, not PR #242's adjudication notebook.
- **A6 (Sandbox subdir = `02_symmetry_and_difference_features/`).** Same
  `_and_`-form subdir already created by PR #266; this PR adds a sibling
  notebook pair, does not create a new subdir.
- **A7 (Upstream artifacts byte-stable at named SHAs).** Verified
  2026-05-29 SHA256: 02_01_02 Parquet `24db73fb…`; 02_01_03 Parquet
  `053900e7…`. The two audit JSONs (`02_01_02/leakage_audit_sc2egset.json`
  and `02_01_03/leakage_audit_sc2egset.json`) are present and byte-stable.
  The PR #266 validator at `validate_symmetry_difference_feature_
  materialization.py` is byte-stable at its merge SHA.
- **A8 (Validator module is a dependency, not a target).** The adjudicator
  imports the validator and runs it against the pinned candidate spec list.
  The adjudicator MUST NOT modify or reimplement the validator. SHA of the
  validator module is pinned as a parent artifact in the CSV+MD.
- **A9 (Row-identity join policy is BINDING).** Join keys for any future
  materialisation that consumes both 02_01_02 and 02_01_03 Parquets:
  `(focal_match_id, focal_player, opponent_player, started_at)`. Verified
  from `02_01_03/leakage_audit_sc2egset.json:38–46`: `projected_identity_
  columns = ["focal_match_id", "focal_player", "opponent_player"]`;
  `projected_context_columns = ["started_at"]`. Both Parquets are joined
  one-to-one on these keys per `02_01_03` row_count = 44,418 and
  distinct_focal_match_count = 22,209 (one row per ordered focal/opponent
  pair, two rows per match — verified at `02_01_03/leakage_audit_
  sc2egset.json:56–57`).
- **A10 (Source-anchor traceability is BINDING).** Every candidate's
  `source_columns` MUST consist of column names appearing in
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_02` (7-tuple) or
  `UPSTREAM_AUDITED_FEATURE_COLUMNS_02_01_03` (24-tuple), copied verbatim
  from the validator's lines 105–141. No transform may introduce a new
  source semantic at this layer.
- **A11 (Direction policy is BINDING).** `focal_minus_opponent` denotes the
  signed difference `focal_value − opponent_value` (slot-orthogonal per
  Invariant I5; satisfies `P(A wins | A focal) = 1 − P(B wins | B focal)` at
  the model input layer). `symmetric` denotes a transform invariant under
  focal/opponent swap, e.g., `mean(focal, opponent) = (focal + opponent)/2`,
  `|focal − opponent|`, OR `focal AND opponent`. Slot-dependent encodings
  (`player_1 − player_2`, `slot_1 − slot_2`, `home − away`, `host − guest`,
  `a − b`) are rejected by `BLOCKED_SLOT_TOKEN_REGEX`. The validator's
  `direction_name_consistency_ok` check (validator lines 485–525)
  treats `_abs_diff` as symmetric (line 519: "symmetric wins"), `_pair_mean`
  as symmetric (line 504), `_minus_` as `focal_minus_opponent` (line 502).
  All Round 2 candidate name templates align with these existing recognised
  patterns; no validator change is required.
- **A12 (Race-pair scope decision is BINDING — defer to 02_05).** Decision
  rationale: `race_pair` is already a 9-class categorical in 02_01_02
  (3 SC2 races × 3 SC2 races, Random folded into Prot/Terr/Zerg per PR #234
  Q3.RATIFY at `02_01_02_source_anchor_race_adjudication.md:§4`). Per
  `02_FEATURE_ENGINEERING_MANUAL.md` §6 lines 131–135 ("Categorical
  interactions"), creating a matchup categorical is the standard pre-game
  pair feature and belongs to Pipeline Section 02_05 (Categorical Encoding &
  Interactions). The 02_02 candidate list excludes race-pair encoded
  interactions; the `race_pair__defer_to_02_05` placeholder in the scaffold
  is consumed by this decision and is NOT carried forward as a candidate.
- **A13 (Cross-region BOOLEAN-pair scope decision is BINDING — bind in
  02_02 with three transforms).** Decision rationale:
  `is_cross_region_fragmented_focal_history_any` and
  `is_cross_region_fragmented_opponent_history_any` are already a symmetric
  BOOLEAN pair on disk in 02_01_03 (PR #243 Q5 BINDING + PR #259
  cross_region_policy = `sensitivity_indicator_co_registration`, verified at
  `02_01_03/leakage_audit_sc2egset.json:79`). They are not time-aware in the
  02_03 sense (they are point indicators, not rolling windows). Binding them
  at 02_02 as a `symmetric` BOOLEAN-pair family with three independent
  transforms inherits the I5 promise upstream-symmetric:
  - **`either = focal OR opponent`** — true iff at least one player has any
    cross-region fragmentation in history; captures "any-fragmentation
    matchup" signal.
  - **`both = focal AND opponent`** — true iff both players have
    cross-region fragmentation in history; distinct from `either` (proper
    subset of `either`); captures "both-fragmented matchup" signal.
  - **`xor = focal XOR opponent`** — true iff exactly one player has
    cross-region fragmentation; distinct from `either` and `both` (e.g.,
    `xor` = `either` − `both`); captures the "asymmetric fragmentation"
    signal that pure `either`/`both` miss. None of the three is
    algebraically recoverable from the others as a single feature
    (specifically, `either` is recoverable as `both OR xor` but with two
    distinct binary inputs needed, so removing any one drops a unique
    expressive surface for tree splits on a single column).
- **A14 (Per-transform binding decisions for symmetric pair aggregates over
  numeric pairs — Round 2 corrected algebra).** **Round 1 had an algebra
  error reading "drop product because mean × 2 = sum"; the correct relation
  is `sum = 2·mean` (sum is the affine duplicate of mean). Round 2 records
  each transform's decision independently:**
  - **`mean = (focal + opponent) / 2`** — BIND for tabular Phase 04 per
    `02_FEATURE_ENGINEERING_MANUAL.md` §3 line 57 (Hue & Vert 2010
    symmetric kernels). Captures permutation-invariant "average level" of
    the focal/opponent pair, which a signed difference cannot express.
    Name template: `<base>_pair_mean`. Direction: `symmetric`. The
    validator recognises `_pair_mean` as symmetric at line 504.
  - **`abs_diff = |focal − opponent|`** — BIND for tabular Phase 04 per
    Invariant I8 (B3 anchor in Literature Context). For LogReg, `|x|` is
    NOT a linear function of `x` and cannot be recovered from the signed
    `focal_minus_opponent` term; LogReg has no way to express
    "symmetric magnitude of the gap between players" unless `abs_diff` is
    explicitly in the basis. For tree models it is recoverable but
    inexpensive; including it harmonises the basis across LogReg, RF, GBT.
    Name template: `<base>_pair_abs_diff`. Direction: `symmetric`. The
    validator recognises `_abs_diff` as symmetric at line 519 ("symmetric
    wins" against the `_diff` suffix rule). **Per-pair override:** for
    BOOLEAN inputs (none in the current numeric pair set), `abs_diff`
    degenerates to `xor`; this override is mooted by the binding decision
    that BOOLEAN pairs go through F5 with `xor` transform directly.
  - **`sum = focal + opponent`** — EXCLUDE on redundancy grounds.
    Algebraically `sum = 2·mean`, so `sum` carries no information beyond
    `mean` × 2 (a constant factor invisible to any model with a bias term;
    invisible to tree splits on a single column). Including both `sum`
    AND `mean` is a strict feature-set redundancy.
  - **`product = focal × opponent`** — DEFER to 02_05. Per
    Literature Context [OPINION on B2 `product` transform], `product`
    captures a genuine 2-degree symmetric polynomial interaction that
    `(mean, abs_diff)` alone cannot express; however, the
    `02_FEATURE_ENGINEERING_MANUAL.md` §6 placement of "interactions" in
    Pipeline Section 02_05 means 02_02 should not pre-empt 02_05's
    interaction surface. Recorded as `product_transform_decision =
    defer_to_02_05` in the binding CSV; re-open trigger documented.
  - **`ratio = focal / opponent`** — EXCLUDE per A15 (zero-bounded
    denominators in cold-start cases; no log-transform present).
  - **Binding constant:** `BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS:
    tuple[str, str] = ("mean", "abs_diff")`. Tests assert this tuple
    exactly; tests assert `sum`, `product`, `ratio` are NOT in the tuple.
- **A15 (Ratio family decision is BINDING — exclude).** Per Literature
  Context [OPINION on ratio family], excluded. The binding adjudication
  records this as ratio_family_decision = `excluded_zero_bounded_
  denominators_unless_log_transform_introduced_in_02_03`.
- **A16 (No new MMR scalar).** PR #234 `is_mmr_missing` BOOLEAN flag remains
  the only MMR-related signal; no `mmr_diff`, no `rating_diff`, no
  `reconstructed_rating_diff` candidate. Enforced by validator's
  `BLOCKED_FAMILY_FRAGMENTS` (lines 172–177) at scaffold execution time;
  reiterated as adjudication binding. Additionally enforces:
  `reconstructed_rating_decision = excluded_per_pr_255_omit_closure`.
- **A17 (No tracker re-introduction at this layer).** PR #259 already
  promoted four tracker-derived columns (APM, SQ, supplyCappedPercent,
  header_elapsedGameLoops) into history-aggregated `*_prior_mean` form in
  the 24-tuple. The adjudication permits difference / symmetric-pair
  operations on those aggregated columns; it does NOT permit reading
  `tracker_events_raw` directly. Enforced by validator's tracker prefix
  check; reiterated as adjudication binding.
- **A18 (CHANGELOG `### Notes` style consistent with PR #266).** Layer-2
  CHANGELOG `## [3.85.0]` block uses `### Added` + `### Changed` + `### Notes`
  with bolded `**No X**` bullets per the PR #234 / PR #266 precedent.
- **A19 (CHANGELOG PR-number placeholder).** Layer-2 CHANGELOG header uses
  `PR #<TBD>` at PR-open time, swept to the real number by a follow-up
  housekeeping commit pre-merge (mirrors PR #266 `5633f319 chore: normalize
  PR #<TBD> placeholders to PR #266`).
- **A20 (NEW — Matchup history transform scope decision is BINDING — drop
  F4 entirely per B1).** Decision rationale: `matchup_h2h_focal_win_rate`
  (validator line 130, 24-tuple) is the only matchup rate column in the
  audited tuple; there is no `matchup_h2h_opponent_win_rate` counterpart.
  Treating it as a paired focal/opponent operation requires either:
  (a) inventing `matchup_h2h_opponent_win_rate = 1 − matchup_h2h_focal_
  win_rate` as an implicit complement, which then makes any pair operation
  an affine transform of the single source column (`2·focal − 1` for
  `focal_minus_opponent`; `0.5` constant for `mean`; `|2·focal − 1|` for
  `abs_diff`), OR
  (b) deriving the opponent rate from raw H2H events at adjudication time,
  which would require reading `02_01_03` source events, violating the
  validator's "source columns must be in audited tuple" check.
  Path (a) provides zero new information for linear models (affine
  transforms of one column have the same column space as the original)
  and minimal split value for trees (a tree can recover `2·focal − 1`
  from `focal` directly). Path (b) violates A10. **Round 2 decision:
  drop F4 entirely from the binding candidate set.** The
  `matchup_h2h_focal_win_rate` column remains available to Phase 04 as a
  base unary feature directly from the 02_01_03 Parquet; no 02_02
  transform is bound. Consequence: the Round 1
  `BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS` constant is REMOVED from the
  adjudicator module. Tests assert the constant is absent.
- **A21 (NEW — Unary `2x−1` rescaling of matchup_h2h_focal_win_rate is
  excluded from the Round 2 binding set per N1).** The reviewer-adversarial
  Round 1 N1 nit noted that if a unary `matchup_h2h_focal_advantage =
  2·focal − 1` transform is offered, it must NOT be tagged as a
  pair-direction candidate. Round 2 chooses the cleaner option: exclude
  the unary entirely from the 02_02 binding set, since (i) the
  validator's `direction_name_consistency_ok` line 522 would force any
  name containing `_minus_` to declare `focal_minus_opponent` direction
  (which is meaningless for a unary transform), and (ii) the unary rescaling
  is a trivial Phase 04 preprocessing step that does not require a 02_02
  artifact. If a future Phase 04 ablation finds value, a name like
  `matchup_h2h_focal_advantage_centered` (no `_minus_` token; declared
  `direction = symmetric` since there's only one player in the
  computation, which makes it vacuously invariant under any pair swap)
  would be the cleanest naming. Recorded as informational, not binding,
  in §"Open Questions".
- **U1 (Validator's three-tuple signature consumed structurally).** The
  adjudicator's notebook calls
  `validate_symmetry_difference_feature_materialization` with the
  adjudication-pinned three tuples. The adjudicator's CSV records the
  validator result columns (passed, halting_falsifier, etc.) as evidence
  rather than re-implementing the validation. Resolves at execution time.
- **U2 (Exact final candidate count per family).** Difference family will
  enumerate the subset of the 24-tuple that has a `focal_*` / `opponent_*`
  numeric pair (estimated 11 pairs); symmetric BOOLEAN-pair family will
  enumerate 3 candidates (cross_region_either, cross_region_both,
  cross_region_xor); symmetric pair mean+abs_diff family will enumerate
  the same numeric pairs as the difference family × 2 transforms = 22
  candidates. **Total estimated 11 + 22 + 3 = 36 candidates.** F4 dropped
  (B1). F6 deferred to 02_05 (A12). Exact count resolved by the notebook
  enumeration step, validated by the PR #266 validator at adjudication
  execution time.
- **U3 (Exact test count target).** Target ≥ 35 effective test cases on the
  adjudicator module with coverage ≥ 95%. PR #234 test file has ~28 tests;
  PR #242 test file has 159 tests; the difference reflects question
  complexity. The Round 2 adjudication has additional tests for the B1/B2/B3
  resolutions (per-transform binding assertions, absence-of-F4 assertion,
  abs_diff inclusion assertions), so ~35–60 tests is the expected range.

## Execution Steps

**Layer-1 (THIS PR — planning-only):**

L1.1 Read (all read-only): `.claude/scientific-invariants.md`,
`.claude/ml-protocol.md`, `.claude/rules/data-analysis-lineage.md`,
`.claude/rules/git-workflow.md`, `.claude/rules/python-code.md`,
`.claude/rules/sql-data.md`, `docs/PHASES.md`, `docs/TAXONOMY.md`,
`docs/ml_experiment_lifecycle/02_FEATURE_ENGINEERING_MANUAL.md`,
the four `reports/specs/02_0X_*.md` specs, the dataset's STEP_STATUS /
PIPELINE_SECTION_STATUS / PHASE_STATUS / ROADMAP / research_log, the merged
PR #266 validator + test file + scaffold notebook, the precedent adjudicator
sources `adjudicate_pre_game_source_layer.py` (PR #234) and
`adjudicate_history_enriched_pre_game_source_layer.py` (PR #242) plus their
test files and CSV+MD outputs, the `02_01_02` and `02_01_03` audit JSONs
(no Parquet value reads), and the Round 1 critique pinned in
`.github/tmp/planner_output.md` for context.

L1.2 Confirm verified state matches the lookup-PASS section of the parent
prompt: master HEAD `9abcd6bc`; pyproject `3.84.0`; STEP_STATUS
`02_01_03: complete`, no `02_02_01` row; ROADMAP `02_02_01` block at lines
2853–3131 byte-unchanged; PIPELINE_SECTION_STATUS has no `02_02` row;
PHASE_STATUS Phase 02 `in_progress`, Phase 03 `not_started`.

L1.3 Author `planning/current_plan.md` (this Round 2 document). The pre-commit
hook (`feedback_plan_required_sections.md`) requires `## Scope`,
`## Problem Statement`, `## Literature Context`, `## Assumptions & Unknowns`,
`## Execution Steps`, `## File Manifest`, `## Gate Condition`,
`## Open Questions`. Verified inline.

L1.4 Author `planning/current_plan.critique.md` recording the Round 2
reviewer-adversarial verdict (target APPROVE-WITH-NITS, 0 blockers).

L1.5 Open draft PR with exactly those two files. Branch
`feat/sc2egset-02-02-01-symmetry-difference-adjudication` off master
`9abcd6bc`. PR body in `.github/tmp/pr.txt` per
`feedback_pr_body_file.md`; delete after PR opens (`feedback_pr_body_cleanup.md`).

**Layer-2 (FUTURE execution PR — same branch — DO NOT execute now):**

### T01 — Author the adjudicator module

**Objective:** Create
`src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_
feature_scope.py` — a pure-function adjudicator that (a) opens the PR #266
validator's pinned tuples as the source-anchor universe; (b) constructs the
Round 2 binding candidate spec list per A12–A17 + A20; (c) re-checks every
constructed spec against the validator (imported, not reimplemented); (d)
computes parent artifact SHA pins; (e) renders the 23-column CSV and §1–§13
MD; (f) writes both artifact files. The module writes ONLY the two
adjudication artifacts; it does NOT materialise any feature, does NOT write
any Parquet, does NOT emit a CROSS-02-01 audit, does NOT touch STEP_STATUS /
research_log / ROADMAP. The function returns a frozen
`SymmetryDifferenceAdjudicationResult` dataclass with all decision fields.

**Instructions:**

1. Module docstring opens with: `"""Adjudication module for SC2EGSet Step
   02_02_01 — symmetry & difference feature scope adjudication.` Mirrors
   PR #234's `adjudicate_pre_game_source_layer.py` line 1 wording.
2. Declare module-level UPPER_SNAKE constants (Invariant I7):
   - `AUDIT_PR: str = "PR #<TBD>"` (swept to real number pre-merge).
   - `EXECUTED_AT_UTC_DATE: str = "2026-05-29"`.
   - `LINEAGE_POSITION: str` — descriptive string analogous to PR #234's
     line 106–111.
   - `_VALIDATOR_MODULE_RELPATH: str` and `_VALIDATOR_MODULE_SHA256_PIN`
     (computed at module import via `_sha256_of_file`; pinned at first
     adjudication run; halt if validator file mutated post-pin).
   - `_PARENT_02_01_02_PARQUET_RELPATH: str` and
     `_PARENT_02_01_02_PARQUET_SHA256_PIN: str =
     "24db73fbb897f883f73891745bc5e98d3e6c9a33d961c9606f6e2c5dc224ff39"`.
   - `_PARENT_02_01_03_PARQUET_RELPATH: str` and
     `_PARENT_02_01_03_PARQUET_SHA256_PIN: str =
     "053900e7712e992e2de12c1595935aa652f05e07d586998db2de0425505aa071"`.
   - `_PARENT_02_01_02_AUDIT_RELPATH: str` +
     `_PARENT_02_01_03_AUDIT_RELPATH: str` — pinned via canonical-JSON SHA
     computed at adjudication time and embedded in the CSV.
   - `ROW_IDENTITY_JOIN_KEYS: tuple[str, str, str, str] = ("focal_match_id",
     "focal_player", "opponent_player", "started_at")` — per A9.
   - `RACE_PAIR_DECISION: str = "defer_to_02_05"` — per A12.
   - `CROSS_REGION_BOOLEAN_PAIR_DECISION: str = "bind_in_02_02_with_three_
     transforms_either_both_xor"` — per A13.
   - `SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION: str = "bind_mean_and_abs_diff_
     only_for_tabular_phase_04_sum_excluded_redundant_product_deferred_to_
     02_05"` — per A14.
   - `RATIO_FAMILY_DECISION: str = "excluded_zero_bounded_denominators_
     unless_log_transform_introduced_in_02_03"` — per A15.
   - `RECONSTRUCTED_RATING_DECISION: str = "excluded_per_pr_255_omit_closure"`
     — per A16.
   - `RAW_SKILL_SCALAR_DECISION: str = "excluded_per_pr_234_is_mmr_missing_
     binding_no_new_mmr_scalar"` — per A16.
   - `TRACKER_SOURCING_DECISION: str = "permitted_via_02_01_03_prior_mean_
     aggregates_only_never_via_tracker_events_raw_direct"` — per A17.
   - `MATCHUP_HISTORY_TRANSFORM_DECISION: str = "dropped_no_audited_
     opponent_counterpart_per_b1_round2"` — per A20.
3. Define the candidate enumeration as data, not code:
   - `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS: tuple[tuple[str, str], ...]` —
     enumerate the `(focal_base, opponent_base)` pairs from the 24-tuple
     that admit numeric subtraction. Estimated 11 pairs from columns
     `focal_prior_match_count` ↔ `opponent_prior_match_count`,
     `focal_prior_win_rate_decisive` ↔ `opponent_prior_win_rate_decisive`,
     `focal_days_since_prior_match` ↔ `opponent_days_since_prior_match`,
     `focal_prior_win_rate_race_conditional` ↔ `opponent_prior_win_rate_
     race_conditional`, `focal_prior_win_rate_map_conditional` ↔
     `opponent_prior_win_rate_map_conditional`,
     `focal_prior_win_rate_matchup_conditional` ↔
     `opponent_prior_win_rate_matchup_conditional`, `focal_apm_prior_mean`
     ↔ `opponent_apm_prior_mean`, `focal_sq_prior_mean` ↔
     `opponent_sq_prior_mean`, `focal_supply_capped_pct_prior_mean` ↔
     `opponent_supply_capped_pct_prior_mean`,
     `focal_elapsed_game_loops_prior_mean` ↔
     `opponent_elapsed_game_loops_prior_mean`. Note: `matchup_h2h_count` is
     a single column (no opponent counterpart), so it does NOT enter the
     pair set; it is available to Phase 04 directly as a unary feature.
   - **`BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS: tuple[str, str] =
     ("mean", "abs_diff")` — per A14 Round 2 corrected.** Note the
     replacement of `"sum"` (Round 1) with `"abs_diff"` (Round 2).
   - `BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES: tuple[str, str] =
     ("is_cross_region_fragmented_focal_history_any",
     "is_cross_region_fragmented_opponent_history_any")` — per A13.
   - `BINDING_CROSS_REGION_BOOLEAN_PAIR_TRANSFORMS: tuple[str, str, str] =
     ("either", "both", "xor")` — per A13.
   - **`BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS` constant is REMOVED.**
     The Round 1 entry is deleted from the adjudicator module per A20.
     Tests assert the symbol is absent from the module's namespace.
4. Public function:
   ```python
   def adjudicate_symmetry_difference_feature_scope(
       *,
       repo_root: Path | str | None = None,
       output_csv_path: Path | str,
       output_md_path: Path | str,
   ) -> SymmetryDifferenceAdjudicationResult:
   ```
   Function performs ONLY: (a) constructs the candidate spec list from the
   module-level binding constants; (b) calls
   `validate_symmetry_difference_feature_materialization(...)` from the
   PR #266 validator; (c) computes parent artifact SHA pins; (d) renders
   the CSV and MD; (e) writes both files. Halts (raises
   `ProvenanceShaNotFoundError`) on any SHA mismatch, on validator failure,
   or on any non-determinism check failure.
5. Frozen dataclass `SymmetryDifferenceAdjudicationResult` carries the
   complete adjudication state including the validator pass-through result,
   the rendered CSV row tuple, and the rendered MD section count.
6. Candidate spec construction (for the validator call):
   - **Difference family (F1):** For each `(focal_base, opponent_base)` in
     `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS`, build
     `CandidateFeatureSpec(column_name=f"focal_minus_opponent_{stem}_diff",
     direction="focal_minus_opponent",
     source_columns=(focal_base, opponent_base))` where `stem` strips the
     `focal_` prefix from `focal_base`.
   - **Symmetric pair mean family (F2):** For each pair, build
     `CandidateFeatureSpec(column_name=f"{stem}_pair_mean",
     direction="symmetric", source_columns=(focal_base, opponent_base))`.
   - **Symmetric pair abs_diff family (F3 — RENAMED FROM ROUND 1
     "sum" PER A14 ROUND 2):** For each pair, build
     `CandidateFeatureSpec(column_name=f"{stem}_pair_abs_diff",
     direction="symmetric", source_columns=(focal_base, opponent_base))`.
     The validator's `direction_name_consistency_ok` check (validator
     line 519: "`_abs_diff` ends with `_diff` but is symmetric — symmetric
     wins") accepts this naming.
   - **Cross-region BOOLEAN-pair family (F5):** For each `op` in
     `("either", "both", "xor")`, build `CandidateFeatureSpec(
     column_name=f"cross_region_{op}",
     direction="symmetric",
     source_columns=BINDING_CROSS_REGION_BOOLEAN_PAIR_SOURCES)`. Note:
     none of `cross_region_either`, `cross_region_both`, `cross_region_xor`
     contains the `_minus_` token (so the validator's name-direction check
     does not force `focal_minus_opponent`); none contains the explicit
     `_pair_*` tokens either (the validator's symmetric-token list at
     lines 504–514 includes `_pair_xor`, `_pair_and`, `_pair_or` —
     consider renaming to `cross_region_pair_xor`, `cross_region_pair_and`,
     `cross_region_pair_or` for explicit validator name-token alignment;
     **decision:** rename to the `_pair_*` form for explicit validator
     alignment, since the validator's symmetric-token list explicitly
     recognises those suffixes). Final names:
     `cross_region_pair_or` (for `either`), `cross_region_pair_and`
     (for `both`), `cross_region_pair_xor` (for `xor`).
   - **Matchup history family (F4):** EMPTY (per A20; no specs constructed).
   - **Race-pair family (F6):** Passed to the validator as the third
     parameter `designed_race_pair_candidate_specs = ()` (empty tuple) per
     A12.
7. Halting falsifier priority chain (first failure wins; halt before write):
   `validator_module_sha_pin_mismatch` →
   `parent_parquet_02_01_02_sha_mismatch` →
   `parent_parquet_02_01_03_sha_mismatch` →
   `parent_audit_02_01_02_sha_mismatch` →
   `parent_audit_02_01_03_sha_mismatch` →
   `validator_failed_passed_false` →
   `validator_halting_falsifier_fired` →
   `binding_symmetric_pair_aggregate_transforms_not_mean_abs_diff` →
   `binding_matchup_history_pair_operations_symbol_present` →
   `provenance_sha_not_found_in_rendered_row` →
   `non_deterministic_render_csv` →
   `non_deterministic_render_md` →
   `materialized_output_paths_non_empty` →
   `target_directory_outside_canonical_02_02_subtree` →
   `byte_drift_on_re_render`.
8. SQL-in-Python (Invariant I6): no SQL is executed by this module —
   adjudication is a pure decision-recording module. If a future enhancement
   needs SQL counts (e.g., to re-verify 44,418 rows), use named module-level
   `_QUERY` constants per `.claude/rules/python-code.md`.
9. Use `logging.getLogger(__name__)`; no `print`; 100% type-hinted; Google-
   style docstrings; functions ≤ 50 lines, decomposed into helpers per
   `.claude/rules/python-code.md`.

**Verification:**

- `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import adjudicate_symmetry_difference_feature_scope, SymmetryDifferenceAdjudicationResult, BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS; assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ('mean', 'abs_diff'); print('import OK')"`
  returns `import OK`.
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_feature_scope.py`
  exits 0.
- `source .venv/bin/activate && poetry run mypy src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_feature_scope.py`
  exits 0.

**File scope:** `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_
symmetry_difference_feature_scope.py`

**Read scope:** PR #266 validator, the 02_01_02 + 02_01_03 audit JSONs, the
PR #234 + PR #242 adjudicator modules, the four `reports/specs/02_0X_*.md`
specs.

---

### T02 — Mirror the test module (≥ 35 tests, ≥ 95% coverage)

**Objective:** Create
`tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_symmetry_
difference_feature_scope.py` covering every helper pass/fail branch, every
halting falsifier, byte-determinism of the rendered CSV + MD across two
re-renders, AND the Round 2 specific assertions for B1/B2/B3 resolutions.

**Instructions:**

1. Resolve repo-relative paths via `Path(__file__).resolve().parents[6]`
   per predecessor pattern.
2. Build fixtures: (a) clean execution returning a valid result; (b) mutated
   parent Parquet SHA fixture; (c) mutated parent audit JSON fixture; (d)
   mutated validator module SHA fixture; (e) deliberately-non-deterministic
   rendering fixture (mocked time/uuid).
3. Named test functions (≥ 35 effective cases targeted):

   **Round 1 carry-over tests (passing checks 8/11):**
   - `test_module_imports_and_constants_exist`
   - `test_row_identity_join_keys_match_audited_tuples`
   - `test_binding_difference_family_numeric_pairs_subset_of_24_tuple`
   - `test_binding_cross_region_boolean_pair_sources_match_audit_json`
   - `test_race_pair_decision_defer_to_02_05`
   - `test_cross_region_boolean_pair_decision_bind_in_02_02_three_
     transforms`
   - `test_ratio_family_decision_excluded`
   - `test_reconstructed_rating_decision_excluded`
   - `test_raw_skill_scalar_decision_excluded`
   - `test_tracker_sourcing_decision_aggregated_only`
   - `test_validator_invoked_with_pinned_spec_list_passed_true`
   - `test_validator_invoked_with_pinned_spec_list_halting_falsifier_none`
   - `test_validator_invoked_with_pinned_spec_list_materialized_output_
     paths_empty`
   - `test_parent_02_01_02_parquet_sha_pin_matches_disk`
   - `test_parent_02_01_03_parquet_sha_pin_matches_disk`
   - `test_parent_02_01_02_audit_json_sha_pin_matches_disk`
   - `test_parent_02_01_03_audit_json_sha_pin_matches_disk`
   - `test_validator_module_sha_pin_matches_disk`
   - `test_csv_row_has_no_not_found_sha`
   - `test_csv_render_byte_deterministic_across_two_calls`
   - `test_md_render_byte_deterministic_across_two_calls`
   - `test_artifact_directory_target_under_canonical_02_02_subtree`
   - `test_no_parquet_emitted_anywhere`
   - `test_no_audit_json_or_md_emitted_under_02_02_01_subtree`
   - `test_no_status_yaml_modified_during_run`
   - `test_no_research_log_modified_during_run`
   - `test_no_roadmap_modified_during_run`
   - `test_post_game_token_regex_boundary_aware_focal_prior_win_rate_
     decisive_passes`
   - `test_post_game_token_regex_boundary_aware_matchup_h2h_focal_win_
     rate_passes`
   - `test_post_game_token_regex_boundary_aware_final_outcome_fails`
   - `test_slot_dependent_token_player_1_minus_player_2_rejected`
   - `test_slot_dependent_token_slot_1_minus_slot_2_rejected`
   - `test_slot_dependent_token_home_minus_away_rejected`
   - `test_slot_dependent_token_a_minus_b_rejected`
   - `test_reconstructed_rating_diff_candidate_rejected`
   - `test_civilization_aoe2_vocabulary_rejected`
   - `test_tracker_events_raw_source_column_rejected`
   - `test_halting_falsifier_priority_validator_module_sha_pin_mismatch_
     before_parent_parquet_mismatch`

   **Round 2 NEW tests (B1/B2/B3/N1/N2 resolution assertions):**
   - **B1 anchors:**
     - `test_binding_matchup_history_pair_operations_symbol_absent`:
       `assert not hasattr(adjudicator_module,
       "BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS")`.
     - `test_no_matchup_h2h_pair_candidate_in_difference_family`: assert
       none of the constructed difference specs has
       `source_columns == ("matchup_h2h_focal_win_rate", ...)`.
     - `test_no_matchup_h2h_pair_candidate_in_symmetric_family`: assert
       none of the constructed symmetric specs has `matchup_h2h` in
       `source_columns`.
     - `test_matchup_history_transform_decision_dropped`:
       `assert MATCHUP_HISTORY_TRANSFORM_DECISION == "dropped_no_audited_
       opponent_counterpart_per_b1_round2"`.
   - **B2 anchors:**
     - `test_binding_symmetric_pair_aggregate_transforms_exactly_mean_
       abs_diff`: `assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS ==
       ("mean", "abs_diff")`.
     - `test_sum_not_in_bound_transforms`: `assert "sum" not in
       BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS`.
     - `test_product_not_in_bound_transforms`: `assert "product" not in
       BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS`.
     - `test_symmetric_pair_aggregate_scope_decision_round2_text`:
       `assert SYMMETRIC_PAIR_AGGREGATE_SCOPE_DECISION ==
       "bind_mean_and_abs_diff_only_for_tabular_phase_04_sum_excluded_
       redundant_product_deferred_to_02_05"`.
     - `test_no_pair_sum_candidate_constructed`: assert no constructed
       spec has column_name ending in `_pair_sum`.
     - `test_no_pair_product_candidate_constructed`: assert no constructed
       spec has column_name ending in `_pair_product`.
   - **B3 anchors:**
     - `test_pair_abs_diff_candidate_per_numeric_pair`: for each pair in
       `BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS`, assert a spec with
       column_name `{stem}_pair_abs_diff`, direction=`symmetric`, and
       source_columns matching the pair is in the constructed list.
     - `test_pair_abs_diff_count_equals_numeric_pair_count`: assert
       count of `_pair_abs_diff` specs equals
       `len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS)`.
     - `test_pair_abs_diff_direction_is_symmetric_in_validator_naming`:
       assert validator's `direction_name_consistency_ok` returns True
       for a synthetic spec with name `<base>_pair_abs_diff` and
       `direction="symmetric"`.
     - `test_abs_diff_inclusion_motivated_by_logreg_i8`: docstring-only
       test asserting the test module's module docstring references
       Invariant I8 + B3 for traceability.
   - **N1 anchors:**
     - `test_no_unary_matchup_h2h_focal_advantage_in_bound_set`:
       assert no constructed spec has column_name containing
       `matchup_h2h_focal_advantage`.
     - `test_unary_naming_does_not_contain_minus_token`: synthetic
       check that a hypothetical name `matchup_h2h_focal_advantage_
       centered` does NOT match `_minus_` in
       validator's diff_tokens list (informational; not a constructed
       candidate).
   - **N2 anchors:**
     - `test_row_count_44418_is_documentary_not_runtime_promise`:
       inspect the rendered MD §3 section text for the explicit
       "documentary future-materialisation gate, not a runtime promise
       for the adjudication PR" sentence; assert presence.
   - **Other Round 2 specific:**
     - `test_csv_column_count_equals_23` (incremented from 22 to add
       `matchup_history_transform_decision` column per A20).
     - `test_md_section_count_equals_13` (incremented from 12 to add
       §13 "Round 2 revision provenance" subsection citing PR #266
       merge SHA and the B1/B2/B3 resolutions).

4. Use `pytest.mark.parametrize` for slot-token regex sweeps; `tmp_path` for
   output paths; mock `time.time` and `uuid.uuid4` only for the determinism
   tests, never for the validator invocations.

**Verification:**

- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_symmetry_difference_feature_scope.py -v`
  — all tests pass.
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_symmetry_difference_feature_scope.py -v --cov=rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope --cov-report=term-missing`
  — coverage ≥ 95% on the new module.

**File scope:** `tests/rts_predict/games/sc2/datasets/sc2egset/test_
adjudicate_symmetry_difference_feature_scope.py`

---

### T03 — Author the jupytext-paired adjudication notebook

**Objective:** Create
`sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_
features/02_02_01_symmetry_difference_feature_adjudication.{py,ipynb}` per
A5. The notebook declares hypothesis + falsifiers + sanity check up front,
imports the T01 adjudicator and the PR #266 validator, runs the
adjudicator end-to-end, prints the validator result and the CSV+MD
emission paths, and asserts the gate conditions.

**Instructions:**

1. The notebook is a sibling of the scaffold notebook from PR #266 (which
   carries the `_materialization` suffix and will be overwritten by the
   future materialisation PR). This adjudication notebook with the
   `_adjudication` suffix lives alongside it.
2. First markdown cell: step heading
   `# Step 02_02_01 — Symmetry & difference feature scope adjudication: sc2egset (Round 2)`,
   citing PR #266 (scaffold), PR #264 (ROADMAP stub), the manual §3
   Bradley-Terry argument, and the Round 1 reviewer-adversarial verdict
   (HOLD with B1/B2/B3 blockers) as the basis for the Round 2 revision.
3. Second markdown cell — assumption / falsifier / sanity check declaration,
   per `.claude/rules/data-analysis-lineage.md` "Required structure for
   every empirical analysis." Each of A12–A18, A20, A21 enumerated as a
   binding decision with rationale. Each B1/B2/B3 resolution explicitly
   called out.
4. Third markdown cell — context: byte-stable parent SHA pins; PR #266
   validator module path + SHA; lineage position.
5. Fourth markdown cell — the binding candidate enumeration as a markdown
   table mirroring T01's BINDING_* constants. Columns:
   `(family, name_template, direction, source_columns, rationale,
   per_transform_decision_anchor)`. Round 2 changes flagged inline:
   - F1 unchanged from Round 1.
   - F2 (pair_mean) unchanged.
   - F3 RENAMED to `_pair_abs_diff` (was `_pair_sum` in Round 1; B2/B3).
   - F4 DROPPED ENTIRELY (B1; A20).
   - F5 unchanged (three transforms — either, both, xor).
   - F6 deferred to 02_05 (unchanged from Round 1).
6. Fifth code cell — import T01 adjudicator and PR #266 validator; pass
   the canonical paths for the two output artifacts; invoke
   `adjudicate_symmetry_difference_feature_scope(...)`; print the
   result.
7. Sixth code cell — assertions: `result.validator_passed is True`;
   `result.validator_halting_falsifier is None`; `result.csv_path.exists()`;
   `result.md_path.exists()`; `result.materialized_output_paths == ()`;
   no path under `reports/artifacts/02_02_01/` exists; the binding
   transform set equals `("mean", "abs_diff")`.
8. Seventh markdown cell — closing summary itemising what this PR produced
   (one CSV+MD adjudication artifact pair, Round 2 revision) and what it
   did NOT produce (per the §"Scope" hard-stops list; the matchup-history
   pair operations dropped per B1; the `sum` and `product` transforms
   dropped/deferred per B2; `abs_diff` included per B3).
9. Round-trip via
   `source .venv/bin/activate && poetry run jupytext --to ipynb ...` and
   execute via `nbconvert --to notebook --execute --inplace`. No executed
   outputs in the `.py` source — outputs live in the `.ipynb`.

**Verification:**

- The notebook executes end-to-end without error.
- `[ ! -f src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_02_01/leakage_audit_sc2egset.json ]`
  exits 0.
- The CSV+MD artifacts exist at their canonical paths.

**File scope:** the two notebook files at the canonical sandbox path.

---

### T04 — Render the 23-column CSV + 13-section MD adjudication artifact pair

**Objective:** Persist the adjudication as one CSV (1 row × 23 columns) +
one MD (13 sections) at canonical paths under
`reports/artifacts/02_feature_engineering/02_symmetry_and_difference_
features/`.

**Instructions:**

1. The CSV is rendered by T01's `_render_csv` private helper called from
   the adjudicator's public function. Header row + 1 data row. UTF-8,
   `\n` line endings, no trailing whitespace. **23 columns** (incremented
   from Round 1 22 to add `matchup_history_transform_decision` per A20).
2. The MD is rendered by T01's `_render_md` private helper. **13 §
   sections** (incremented from Round 1 12 to add §13 "Round 2 revision
   provenance" per A14 + A20 documentation).
3. The CSV+MD pair is the ONLY artifact emitted; no Parquet, no audit JSON,
   no audit MD under `02_02_01/`.
4. Both files are byte-deterministic across two re-renders (verified by
   T02 tests).

**Verification:**

- `wc -l reports/artifacts/02_feature_engineering/02_symmetry_and_
  difference_features/02_02_01_symmetry_difference_feature_
  adjudication.csv` returns 2 (header + 1 data row).
- `grep -c '^## §' reports/artifacts/02_feature_engineering/02_symmetry_
  and_difference_features/02_02_01_symmetry_difference_feature_
  adjudication.md` returns 13.

**File scope:** the two artifact files at the canonical reports path.

---

### T05 — Update planning index, CHANGELOG, and version

**Objective:** Mechanical bookkeeping; archive PR #266; register the active
plan; bump minor; add `## [3.85.0]` block with literal `### Notes`
subsection.

**Instructions:**

1. Bump `pyproject.toml` `version = "3.84.0"` → `version = "3.85.0"` per A3.
2. Move PR #266 archive row in `planning/INDEX.md` from "Active plan" to
   Archive table (merge SHA `9abcd6bc`). Add the new "Active plan" line
   for this PR with the Round 2 revision marker.
3. Add `## [3.85.0] — 2026-05-29 (PR #<TBD>: feat/sc2egset-02-02-01-
   symmetry-difference-adjudication)` to CHANGELOG.md under `[Unreleased]`,
   above `## [3.84.0]`. Required subsections: `### Added`, `### Changed`,
   `### Notes` with bolded `**No X**` bullets (per A18). At minimum:
   - `**No feature value materialised.**` (no Parquet under
     `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_
     features/` matching `*_features.parquet`);
   - `**No CROSS-02-01 audit artifact.**` (no `leakage_audit_sc2egset.{json,
     md}` under `reports/artifacts/02_02_01/`);
   - `**No STEP_STATUS row added for 02_02_01.**`;
   - `**No PIPELINE_SECTION_STATUS row added for 02_02.**`;
   - `**No PHASE_STATUS mutation.**`;
   - `**No ROADMAP edit.**`;
   - `**No research_log append.**`;
   - `**No upstream artifact mutation.**` (both Parquets and both audit
     JSONs byte-stable);
   - `**No reconstructed_rating re-introduction.**`;
   - `**No new MMR scalar.**`;
   - `**No AoE2 civilization vocabulary.**`;
   - `**No Phase 03 / Step 02_01_04 / Step 02_02_02+ / baseline modelling.**`;
   - `**No matchup-history pair operations (Round 2 / B1).**`;
   - `**No `sum` or `product` transforms (Round 2 / B2; `sum`
     excluded redundant, `product` deferred to 02_05).**`;
   - `**`abs_diff` included as symmetric magnitude transform per Invariant I8
     LogReg requirement (Round 2 / B3).**`

**Verification:** `git diff pyproject.toml` shows exactly one line change;
`grep -c '^## \[3.85.0\]' CHANGELOG.md` returns 1; `grep -A 200 '^## \[3.85.0\]'
CHANGELOG.md | grep -c '^### Notes$'` returns 1.

**File scope:** `pyproject.toml`, `planning/INDEX.md`, `CHANGELOG.md`.

---

For each Layer-2 step, the executor must: grep-discover anchor strings
before each edit; run pre-commit hooks once before commit (ruff / mypy run
automatically on `.py` touch); verify the 9-file diff at commit time; reject
any 10th tracked entity.

## File Manifest

### THIS Layer-1 planning PR (exactly 2 files; ONLY after Round 2 reviewer approval):

| Path | Action |
|---|---|
| `planning/current_plan.md` | create/overwrite |
| `planning/current_plan.critique.md` | create/overwrite |

### Future Layer-2 execution PR (exactly 9 files):

| Path | Action | Scope notes | Forbidden content |
|---|---|---|---|
| `src/rts_predict/games/sc2/datasets/sc2egset/adjudicate_symmetry_difference_feature_scope.py` | Create | T01 — adjudicator module; imports PR #266 validator; writes CSV+MD only; Round 2 binding constants per A12–A17, A20, A21 | No Parquet write; no audit JSON write; no status YAML mutation; no SQL execution; no `BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS` symbol; no `_pair_sum` or `_pair_product` candidate names; transforms must be `("mean", "abs_diff")` exactly |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_adjudicate_symmetry_difference_feature_scope.py` | Create | T02 — ≥ 35 effective test cases; ≥ 95% coverage; includes B1/B2/B3/N1/N2 assertion tests | No real Parquet read in tests; no real DuckDB connection (mocked or skipped) |
| `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.py` | Create | T03 — jupytext source with hypothesis/falsifier/sanity-check declaration; Round 2 revision marker | No executed cell outputs in `.py` |
| `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.ipynb` | Create | T03 — paired notebook with executed outputs | n/a (outputs are the point) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.csv` | Create | T04 — 23-column 1-row CSV; UTF-8; `\n` line endings | No `NOT_FOUND` SHA; no absolute paths; no trailing whitespace; column count exactly 23 (Round 2 adds `matchup_history_transform_decision`) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_adjudication.md` | Create | T04 — 13-section MD; non-materialization disclaimer at top; Round 2 revision provenance §13 | No CROSS-02-01 §3 audit claims; no feature value materialisation claims; §3 row-count language must be tagged "documentary, not runtime" per N2 |
| `pyproject.toml` | Update | T05 — version 3.84.0 → 3.85.0 (minor; A3) | n/a |
| `planning/INDEX.md` | Update | T05 — archive PR #266 + add new Active line | n/a |
| `CHANGELOG.md` | Update | T05 — `## [3.85.0]` with literal `### Notes` per A18, including Round 2 B1/B2/B3 notes | n/a |

### Forbidden in future Layer-2 (must NOT appear in diff):

- `src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
  (PR #266 validator byte-unchanged);
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_symmetry_difference_feature_materialization.py`
  (PR #266 test file byte-unchanged);
- `sandbox/sc2/sc2egset/02_feature_engineering/02_symmetry_and_difference_features/02_02_01_symmetry_difference_feature_materialization.{py,ipynb}`
  (PR #266 scaffold notebook byte-unchanged; overwritten only by future
  materialisation PR);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
  (no `02_02_01` row);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
  (no `02_02` row);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
  (Phase 02 stays `in_progress`);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
  (`02_02_01` block at lines 2853–3131 byte-unchanged);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`;
- `reports/research_log.md` (root);
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`;
- any path matching `reports/artifacts/02_02_01/**` (no CROSS-02-01 audit
  yet);
- any path matching
  `reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/*.parquet`
  (no feature materialisation yet);
- any byte change to `02_01_02_pre_game_features.parquet`,
  `02_01_03_history_enriched_pre_game_features.parquet`,
  `reports/artifacts/02_01_02/leakage_audit_sc2egset.{json,md}`,
  `reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`;
- any spec under `reports/specs/` or schema YAML under
  `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/`;
- any AoE2 path under `src/rts_predict/games/aoe2/**`;
- any thesis chapter, bib, appendix under `thesis/**`;
- any `docs/**`, `.claude/**`, or `data/**` path.

### Future CSV schema (23 columns; deterministic 64-char lowercase hex SHAs; no `NOT_FOUND`)

```
decision_id                                  # "02_02_01_symmetry_difference_feature_scope"
candidate_family_set                         # JSON-encoded list of bound family identifiers: ["F1","F2","F3","F5"]
direction_policy                             # "focal_minus_opponent_xor_symmetric_literal"
binding_difference_family_numeric_pair_count # int — count of pairs in 24-tuple admitting subtraction (expected 11)
binding_symmetric_pair_aggregate_transforms  # "mean,abs_diff"  (Round 2: replaces "mean,sum")
binding_cross_region_boolean_pair_transforms # "either,both,xor"
race_pair_decision                           # "defer_to_02_05"
cross_region_boolean_pair_decision           # "bind_in_02_02_with_three_transforms_either_both_xor"
symmetric_pair_aggregate_scope_decision      # "bind_mean_and_abs_diff_only_for_tabular_phase_04_sum_excluded_redundant_product_deferred_to_02_05"
matchup_history_transform_decision           # "dropped_no_audited_opponent_counterpart_per_b1_round2"  (Round 2 NEW per A20)
ratio_family_decision                        # "excluded_zero_bounded_denominators_unless_log_transform_introduced_in_02_03"
reconstructed_rating_decision                # "excluded_per_pr_255_omit_closure"
raw_skill_scalar_decision                    # "excluded_per_pr_234_is_mmr_missing_binding_no_new_mmr_scalar"
tracker_sourcing_decision                    # "permitted_via_02_01_03_prior_mean_aggregates_only_never_via_tracker_events_raw_direct"
row_identity_join_keys                       # "focal_match_id,focal_player,opponent_player,started_at"
row_alignment_policy                         # "one_to_one_on_join_keys_inner_join_row_count_44418_documentary_future_gate_not_runtime_promise"  (Round 2 wording per N2)
validator_passed                             # "True" (literal string from boolean)
validator_halting_falsifier                  # "None" (literal string)
parent_02_01_02_parquet_sha256               # hex64
parent_02_01_03_parquet_sha256               # hex64
parent_02_01_02_audit_json_sha256            # hex64 (canonical JSON)
parent_02_01_03_audit_json_sha256            # hex64 (canonical JSON)
validator_module_sha256                      # hex64 (source bytes)
```

SHA computation: `hashlib.sha256(Path(p).read_bytes()).hexdigest()` for
Parquet and source bytes; for audit JSON use canonical form via
`json.dumps(json.load(open(p)), sort_keys=True, separators=(",",":")).encode()`
to defeat whitespace drift. All 23 columns deterministic across two re-renders
(T02 tests).

### Future MD section list (13 sections)

- §1 — Non-materialization disclaimer (top of file): "This adjudication
  records the binding `02_02_01` symmetry & difference feature scope
  decision. It does NOT materialise any feature value, does NOT emit any
  CROSS-02-01 audit, and does NOT close Step `02_02_01`. The future
  materialisation PR (analogue of PR #259) emits the Parquet + CROSS-02-01
  audit pair under `reports/artifacts/02_02_01/`."
- §2 — Input artifact lineage (paths + SHA-256 for both Parquets, both
  audit JSONs, the validator module).
- §3 — Row identity / alignment policy (per A9; one-to-one inner-join on
  `(focal_match_id, focal_player, opponent_player, started_at)`; expected
  row count 44,418). **Round 2 wording per N2:** The §3 head sentence MUST
  read: "The row count `44,418` and one-to-one alignment are a documentary
  future-materialisation gate, not a runtime promise for the adjudication
  PR. This adjudication does not consume Parquet rows — it pins the binding
  candidate spec list. The future materialisation PR is responsible for
  runtime row-count assertions and join-policy enforcement; if the row
  count drifts at materialisation, the materialisation PR halts before
  artifact generation. The adjudication artifact pair (CSV+MD) is purely
  decision-recording."
- §4 — Candidate feature table mirroring CSV; per-family rows with
  `direction`, `source_columns`, `transform_formula_inline`, and
  Round 2 revision markers (F3 renamed; F4 dropped; F6 deferred).
- §5 — Direction policy (per A11; the two-Literal binding; explicit
  reference to validator's `direction_name_consistency_ok` line 519
  for `_abs_diff` symmetric tagging).
- §6 — Source-column traceability proof (per candidate, the 7-tuple /
  24-tuple row indices its source columns map to).
- §7 — Validator result summary (passed / halting_falsifier / per-check
  result fields; SHA-pinned to the validator module).
- §8 — Race-pair deferral to 02_05 (per A12 with manual §6 citation).
- §9 — Excluded features / families (Round 2 corrected per B2 + B3 + B1):
  - Subsection §9.1 — `sum` transform: **excluded** — algebraic argument
    `sum = 2·mean` makes `sum` an affine duplicate of `pair_mean`;
    feature-set redundancy without information gain.
  - Subsection §9.2 — `product` transform: **deferred to 02_05** —
    `focal × opponent` is a genuine multiplicative interaction (not
    expressible from `(mean, abs_diff)` alone), but per
    `02_FEATURE_ENGINEERING_MANUAL.md` §6 lines 131–135 numeric
    interactions belong to Pipeline Section 02_05 (Categorical Encoding &
    Interactions). Re-open trigger: Phase 04 ablation finding non-monotone
    interaction unrecoverable from 02_05 matchup-conditioned encoding.
  - Subsection §9.3 — `abs_diff` transform: **INCLUDED** (per B3 / A14
    Round 2). Invariant I8 binds LogReg into the cross-game protocol;
    LogReg cannot recover `|x|` linearly from `x`; `abs_diff` is therefore
    the canonical symmetric magnitude transform. Cross-reference to §9.1
    (mean) and §9.2 (product).
  - Subsection §9.4 — `ratio` family: **excluded** per A15 (zero-bounded
    denominators; no log-transform present).
  - Subsection §9.5 — `reconstructed_rating` family: **excluded** per
    PR #255 omit-closure (binding via validator's
    `BLOCKED_FAMILY_FRAGMENTS`).
  - Subsection §9.6 — raw MMR/rating/Elo/Glicko/mu/sigma scalars:
    **excluded** per A16; PR #234 `is_mmr_missing` BOOLEAN flag is the
    only MMR-related signal.
  - Subsection §9.7 — matchup-history pair operations (F4): **excluded**
    entirely per B1 / A20 — `matchup_h2h_focal_win_rate` has no audited
    opponent counterpart in the 24-tuple; reframing as a paired focal/
    opponent operation requires an affine transform of one column with
    zero information gain. The unary `2x−1` rescaling
    (`matchup_h2h_focal_advantage`) is informational only (A21) and is
    NOT in the binding set.
  - Subsection §9.8 — `tracker_events_raw` direct sourcing: **excluded**
    per A17; only `*_prior_mean` aggregated forms permitted.
- §10 — Leakage controls (Invariant I3 inheritance from 02_01_03; Invariant
  I5 enforced via direction + source-columns traceability; boundary-aware
  POST_GAME_TOKEN_REGEX inheritance; Invariant I8 LogReg binding for
  `abs_diff` per B3 / A14).
- §11 — Future materialisation contract (what a downstream materialisation
  PR must satisfy: row count 44,418; CROSS-02-01 audit; SHA pins on all
  parent artifacts; byte-determinism; emits `_pair_abs_diff` columns for
  every eligible numeric pair).
- §12 — Out-of-scope disclaimers (no status / research_log / Phase-03
  claim; race-pair deferral is binding for 02_02 not for 02_05; `product`
  deferral is binding for 02_02 not for 02_05).
- §13 — **Round 2 revision provenance (NEW).** Cites the Round 1
  reviewer-adversarial HOLD verdict (B1: vacuous F4 pair-operation framing;
  B2: A14 algebra error; B3: abs_diff exclusion incompatible with LogReg
  under I8) and the Round 2 resolutions: F4 dropped (A20); A14 algebra
  corrected, per-transform decisions independent (A14 corrected); `abs_diff`
  included as `_pair_abs_diff` (A14 + B3); validator naming alignment via
  `direction_name_consistency_ok` line 519 ("symmetric wins"). PR #266
  merge SHA `9abcd6bc` recorded. Round number = 2.

### Future test plan summary

- Target ≥ 35 effective test cases on the adjudicator module
- Target ≥ 95% line coverage on the adjudicator module
- Tests enumerated in T02 cover: every constant, every binding decision
  rationale (including A20 new), every halting falsifier (including the
  Round 2 new `binding_symmetric_pair_aggregate_transforms_not_mean_abs_diff`
  and `binding_matchup_history_pair_operations_symbol_present` falsifiers),
  byte-determinism, validator invocation pass-through, parent SHA pins,
  slot-token boundary-aware regex sweep (positive and negative),
  POST_GAME_TOKEN_REGEX positive controls (`focal_prior_win_rate_decisive`,
  `matchup_h2h_focal_win_rate` do NOT fire), reconstructed_rating exclusion,
  AoE2 vocabulary exclusion, tracker source exclusion, artifact directory
  target validation, no status / research_log / ROADMAP mutation, AND the
  Round 2 specific B1/B2/B3/N1/N2 assertions.

### Row-identity join policy (binding; per N2 — documentary, not runtime)

- **Join keys:** `(focal_match_id, focal_player, opponent_player,
  started_at)` per A9. All four columns present in both Parquets
  identically (verified at `02_01_02/leakage_audit_sc2egset.json:21–28`
  and `02_01_03/leakage_audit_sc2egset.json:39–46`).
- **Expected row alignment:** Inner join row count = 44,418; distinct
  focal_match_id = 22,209; two rows per match (one per focal-player
  perspective).
- **Failure mode (DOCUMENTARY GATE, NOT RUNTIME PROMISE for THIS PR per
  N2):** If row count drifts at FUTURE materialisation time, the future
  materialisation PR halts before any artifact generation. The
  adjudication does not consume the actual Parquet rows (pure-function
  decision recording); this PR's adjudicator emits a CSV+MD pair recording
  the decisions only. The future materialisation PR is solely responsible
  for runtime row-count assertions.

### Candidate feature families (binding for 02_02; bound per A12–A17 + A20 — Round 2)

| Family | Direction | Source columns (audited tuple) | Name template | Round 2 change |
|---|---|---|---|---|
| F1 — Numeric difference | `focal_minus_opponent` | 11 pairs from 24-tuple where `(focal_X, opponent_X)` are numeric | `focal_minus_opponent_<stem>_diff` | unchanged |
| F2 — Symmetric pair mean | `symmetric` | Same 11 numeric pairs | `<stem>_pair_mean` | unchanged |
| F3 — Symmetric pair absolute difference | `symmetric` | Same 11 numeric pairs | `<stem>_pair_abs_diff` | **RENAMED from "Symmetric pair sum" / `_pair_sum`** per B2 (sum redundant with mean) + B3 (abs_diff required for LogReg per I8). Validator recognises `_abs_diff` as symmetric at line 519. |
| F4 — Matchup history pair operations | n/a | n/a | n/a | **DROPPED ENTIRELY** per B1 / A20 — `matchup_h2h_focal_win_rate` has no audited opponent counterpart; pair framing is vacuous. |
| F5 — Cross-region BOOLEAN-pair | `symmetric` | `is_cross_region_fragmented_focal_history_any`, `is_cross_region_fragmented_opponent_history_any` | `cross_region_pair_<op>` for op ∈ {or, and, xor} | unchanged scope; explicit `_pair_<op>` naming aligns with validator's symmetric-token list at lines 504–514 |
| F6 — Race-pair encoded interaction | **DEFERRED TO 02_05** | n/a | n/a (no candidate in 02_02) | unchanged |

**Excluded by binding adjudication (Round 2):**

- Ratio family (A15);
- `reconstructed_rating` family (A16);
- raw MMR/rating/Elo/Glicko/mu/sigma scalars (A16);
- `_pair_sum` transform per A14 Round 2 (sum = 2·mean is an affine
  duplicate of pair_mean);
- `_pair_product` transform deferred to 02_05 per A14 Round 2 (genuine
  multiplicative interaction, not redundant — belongs in
  `02_FEATURE_ENGINEERING_MANUAL.md` §6 Pipeline Section 02_05);
- Matchup-history pair operations entirely (per B1 / A20 — no audited
  opponent counterpart for `matchup_h2h_focal_win_rate`);
- Unary `matchup_h2h_focal_advantage = 2·focal − 1` (A21 — informational
  only; not in the binding 02_02 set);
- `tracker_events_raw` direct sourcing (A17 — only `*_prior_mean`
  aggregated forms permitted).

**Total binding candidate count (estimated):** F1 (11) + F2 (11) + F3 (11)
+ F5 (3) = **36 candidates**. F4 and F6 contribute 0. Exact count
validated by the PR #266 validator at adjudication execution time.

## Gate Condition

**Layer-1 gate (THIS PR):** satisfied iff ALL of:

1. PR diff = exactly two files (`planning/current_plan.md` +
   `planning/current_plan.critique.md`).
2. PR is open as draft.
3. `planning/current_plan.md` contains all eight required `##` sections
   verbatim.
4. Round 2 reviewer-adversarial returns APPROVE or APPROVE-WITH-NITS with
   zero blockers; verdict recorded in `current_plan.critique.md`.

**Layer-2 gate (FUTURE execution PR):** satisfied iff ALL of:

1. **Adjudicator imports cleanly and binding transform tuple is correct** —
   `source .venv/bin/activate && poetry run python -c "from rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope import adjudicate_symmetry_difference_feature_scope, BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS; assert BINDING_SYMMETRIC_PAIR_AGGREGATE_TRANSFORMS == ('mean', 'abs_diff'); print('OK')"`
   returns `OK`.
2. **`BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS` symbol absent (Round 2 B1
   anchor)** —
   `source .venv/bin/activate && poetry run python -c "import rts_predict.games.sc2.datasets.sc2egset.adjudicate_symmetry_difference_feature_scope as m; assert not hasattr(m, 'BINDING_MATCHUP_HISTORY_PAIR_OPERATIONS'); print('OK')"`
   returns `OK`.
3. **All ≥ 35 tests pass** with coverage ≥ 95% on the adjudicator module.
4. **PR #266 validator is byte-unchanged** —
   `git diff master..HEAD -- src/rts_predict/games/sc2/datasets/sc2egset/validate_symmetry_difference_feature_materialization.py`
   returns empty.
5. **Notebook executes end-to-end** with the CSV+MD artifact pair persisted.
6. **CSV has 23 columns, 1 data row, no `NOT_FOUND` SHA** —
   `awk -F, 'NR==1{print NF}END{print NR}' .../adjudication.csv` returns
   `23\n2`; `grep -c 'NOT_FOUND' .../adjudication.csv` returns 0.
7. **MD has 13 §-sections** —
   `grep -c '^## §' .../adjudication.md` returns 13.
8. **MD §3 row-count language tagged "documentary, not runtime promise"
   per N2** — `grep -c 'documentary future-materialisation gate, not a
   runtime promise' .../adjudication.md` returns ≥ 1.
9. **Byte-deterministic re-render** — running the adjudicator twice produces
   byte-identical CSV+MD pairs (T02 enforces; gate spot-checks via
   `sha256sum`).
10. **Artifact-free promise (no Parquet, no CROSS-02-01 audit)** —
    `[ ! -f reports/artifacts/02_02_01/leakage_audit_sc2egset.json ]`,
    `[ ! -f reports/artifacts/02_02_01/leakage_audit_sc2egset.md ]`,
    `! ls reports/artifacts/02_feature_engineering/02_symmetry_and_difference_features/*.parquet 2>/dev/null`
    all exit 0.
11. **Status / ROADMAP / research_log byte-unchanged** —
    `git diff origin/master..HEAD -- ...STEP_STATUS.yaml ...PIPELINE_SECTION_STATUS.yaml ...PHASE_STATUS.yaml ...ROADMAP.md ...research_log.md reports/research_log.md`
    returns empty.
12. **Version bumped to 3.85.0** —
    `grep '^version = ' pyproject.toml` returns `version = "3.85.0"`.
13. **CHANGELOG `## [3.85.0]` entry with `### Notes` subsection** —
    grep counts match A18 + Round 2 specific notes.
14. **Diff is exactly the 9-file manifest** —
    `git diff --name-only origin/master..HEAD | sort` returns exactly the
    9 files listed in the File Manifest table.
15. **Validator invocation reports `passed=True`** — the adjudicator's
    persisted result contains `validator_passed=True`,
    `validator_halting_falsifier=None`.
16. **Parent SHA pins match disk** — `parent_02_01_02_parquet_sha256` ==
    `24db73fb…`; `parent_02_01_03_parquet_sha256` == `053900e7…`; both
    audit JSON SHAs match `_sha256_of_canonical_json` of the on-disk
    audit JSONs at execution time.
17. **Race-pair candidate count is 0 in 02_02** — the CSV's
    `race_pair_decision` field equals `defer_to_02_05` and the bound
    candidate family set in §4 excludes race-pair.
18. **Matchup-history pair candidate count is 0 (Round 2 B1 anchor)** —
    the CSV's `matchup_history_transform_decision` field equals
    `dropped_no_audited_opponent_counterpart_per_b1_round2` and no
    constructed candidate spec has `matchup_h2h` in its `source_columns`.
19. **`abs_diff` candidate count equals `BINDING_DIFFERENCE_FAMILY_
    NUMERIC_PAIRS` count (Round 2 B3 anchor)** — count of constructed
    specs with column_name ending in `_pair_abs_diff` equals 11 (or
    whatever the exact pair count is at execution time).
20. **`_pair_sum` candidate count is 0 (Round 2 B2 anchor)** — no
    constructed spec has column_name ending in `_pair_sum`.
21. **`_pair_product` candidate count is 0 (Round 2 B2 anchor)** — no
    constructed spec has column_name ending in `_pair_product`.

## Open Questions

- **OQ1 — Outcome adjudication.** A (adjudication PR) chosen. B–G rejected
  on repo evidence (chat output §2; cross-referenced in
  `current_plan.critique.md` §"Adjudication outcomes").
- **OQ2 — Single-row vs multi-row CSV.** Single-row chosen because
  `02_02_01` records ONE binding family-scope decision (with eight sub-
  rationales A12–A18 + A20). PR #234 used single-row CSV for its 3-decision
  Q1/Q2/Q3 adjudication; PR #242 used multi-row for 8 coupled Q-decisions.
  The current PR is closer in shape to PR #234.
- **OQ3 — Race-pair scope (02_02 vs 02_05).** Bound to 02_05 per A12 +
  manual §6 citation. Future 02_05 PR re-opens this question with its own
  candidate enumeration; this PR's binding is `02_02-side` only.
- **OQ4 — Cross-region BOOLEAN-pair scope (02_02 vs 02_03+).** Bound to
  02_02 per A13 with three independent transforms (either / both / xor).
  The point-indicator nature distinguishes from rolling-window temporal
  features.
- **OQ5 — Symmetric pair aggregate scope (tabular vs GNN).** Bound to
  tabular Phase 04 with **Round 2 corrected** transform set
  `(mean, abs_diff)` per A14. GNN comparison in Phase 04 will use a
  separate feature surface (planned as Phase 06 scope per
  `docs/PHASES.md`).
- **OQ6 — Ratio family inclusion.** Excluded per A15 with explicit re-open
  condition (log-transform in 02_03).
- **OQ7 — `product` transform placement (02_02 vs 02_05).** **Round 2
  resolution:** Deferred to 02_05 per A14 + Literature Context [OPINION on
  B2]; `product = focal × opponent` is a genuine multiplicative
  interaction not expressible from `(mean, abs_diff)`, but
  `02_FEATURE_ENGINEERING_MANUAL.md` §6 places interactions in Pipeline
  Section 02_05. Re-open trigger: Phase 04 ablation finding non-monotone
  interaction unrecoverable from 02_05 matchup-conditioned encoding.
- **OQ8 — Matchup history transform scope.** **Round 2 resolution:**
  Dropped entirely per B1 / A20 — `matchup_h2h_focal_win_rate` has no
  audited opponent counterpart in the 24-tuple. The unary `2x−1` rescaling
  (`matchup_h2h_focal_advantage`) is excluded per A21; Phase 04 may consume
  `matchup_h2h_focal_win_rate` directly as a unary feature from 02_01_03
  Parquet without a 02_02 transform.
- **OQ9 — Notebook overwrite contract.** Scaffold notebook
  `_materialization.{py,ipynb}` (PR #266) is preserved by this PR; the
  adjudication notebook is a separate `_adjudication.{py,ipynb}` sibling
  per A5. The future materialisation PR will overwrite the scaffold
  notebook, not the adjudication notebook.
- **OQ10 — Test count exact target.** Target ≥ 35 as a tight lower bound
  (Round 2 incremented from Round 1's 30 to accommodate the B1/B2/B3/N1/N2
  new assertion tests); PR #234 has ~28 tests; PR #242 has 159. The
  adjudication scope here is closer to PR #234. Resolved by reviewer-deep
  at execution time.
- **OQ11 — `sum` transform re-open potential.** **Round 2 resolution:**
  Excluded per A14 (sum = 2·mean is affine duplicate). Re-open trigger:
  none expected (the algebraic identity is invariant). Recorded for
  completeness only.
- **OQ12 — Validator's `direction_name_consistency_ok` line 519
  "symmetric wins" rule alignment.** **Round 2 resolution:** The Round 2
  binding name `_pair_abs_diff` deliberately leverages this rule: the
  suffix `_diff` would naively force `focal_minus_opponent`, but the
  presence of the symmetric token `_abs_diff` triggers the line 519
  override "symmetric wins". The adjudicator's constructed specs declare
  `direction="symmetric"` for every `_pair_abs_diff` candidate;
  Round 2 tests assert this via the validator's `direction_name_
  consistency_ok` check returning True.
- **OQ13 — `abs_diff` per-pair exclusion reservation.** Per Round 2
  B3 anchor "If any specific `abs_diff` candidate is excluded, require a
  per-feature reason." Round 2 default: ALL 11 numeric pairs admit
  `abs_diff`. If a future re-binding excludes a specific pair (e.g.,
  `focal_apm_prior_mean ↔ opponent_apm_prior_mean` could be excluded if
  cold-start sparsity makes `abs_diff` unreliable), the per-feature
  rationale MUST be recorded in §9.3 of the MD with explicit reference to
  the specific pair. Round 2 records: no per-pair exclusion.

---

## Reviewer-adversarial Round 2 nits applied (Layer-1 materialisation)

Round 2 reviewer-adversarial verdict: **APPROVE-WITH-NITS** (0 blockers; 6 nits).
Full verdict at `planning/current_plan.critique.md`. Nit-to-assumption mapping:

| Nit | Maps to | Summary | Apply at |
|---|---|---|---|
| N1 | A14 / OQ7 / Literature Context [OPINION on B2] | "`product` is not expressible from `(mean, abs_diff)` alone" should read "not LINEARLY expressible" — identity `focal × opponent = mean^2 - (abs_diff/2)^2` makes product a quadratic polynomial in `(mean, abs_diff)`. Decision unchanged. | Layer-2 execution — wording fix in `[OPINION on B2]` and MD §9.2. |
| N2 | A14 / D2 / manual §6 lines 133-135 | Manual §6 line 135 notes trees capture interactions naturally; the `product -> 02_05` deferral rationale should acknowledge that the Pipeline-Section placement is a convention choice, not a methodological necessity. | Layer-2 execution — tighten last sentence of `[OPINION on B2]`. |
| N3 | A13 / D3 / OQ4 | F5 independence argument holds for trees; under LogReg with regularization the design matrix is rank-2 over the 2-dim Boolean source (`either = both OR xor`). Decision to retain all three transforms stands; rationale must not claim non-redundancy for all model classes. | Layer-2 execution — add LogReg-redundancy footnote to A13 / MD §4 caption. |
| N4 | A21 / N1 (R1) resolution / OQ8 | A21's prescriptive "tag unary as `symmetric` by convention" pre-empts a future design choice; reframe as open design question (a unary feature is, strictly, neither `focal_minus_opponent` nor `symmetric` under the binary Literal). | Layer-2 execution — soften A21 last paragraph. |
| N5 | U2 / Gate clause #19 / OQ13 | Gate clause #19 wording "(or whatever the exact pair count is at execution time)" softens a deterministic gate. Replace with internal-consistency assertion: `count(_pair_abs_diff specs) == len(BINDING_DIFFERENCE_FAMILY_NUMERIC_PAIRS) == binding_difference_family_numeric_pair_count CSV column`. | Layer-2 execution — gate condition #19 and corresponding test. |
| N6 | A14 / B3 anchor / D1 | LogReg / abs_diff argument is complete on the signed-vs-magnitude axis but does not cross-link to the `mean`-inclusion rationale. Recommend MD §9.3 explicitly note: the joint basis `(focal_minus_opponent, pair_mean, pair_abs_diff)` spans linear-in-signed-difference, linear-in-mean-level, and linear-in-symmetric-magnitude; quadratic effects (`focal^2`, `opponent^2`, `product`) remain unrecoverable without polynomial terms — these are the 02_05 deferral surface. | Layer-2 execution — add §9.3 cross-link paragraph. |

All six nits are wording/cross-link refinements applied at Layer-2 execution time. No Round 2 binding decision changes. The Round 2 plan as authored above is the binding contract for the future Layer-2 adjudication execution PR.
