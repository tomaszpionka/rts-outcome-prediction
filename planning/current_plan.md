---
category: F
branch: docs/thesis-4.1-data-chapter
date: 2026-04-17
planner_model: claude-opus-4-7-1m
chapter: "04_data_and_methodology"
sections: ["§4.1.1", "§4.1.2", "§4.1.3"]
section_type: "data-fed"
adversarial_cycle: "iterated up to 3 rounds per user standing directive"
dataset: null
phase: 01
pipeline_section: null
invariants_touched:
  - "I3 (temporal discipline / pre-game vs in-game vs post-game)"
  - "I5 (symmetric player slots; team-1 / side asymmetries)"
  - "I7 (no magic numbers — every threshold cited)"
  - "I8 (cross-game / cross-dataset comparability)"
  - "I9 (raw data immutability and view-only cleaning)"
  - "I10 (filename relative to raw_dir)"
source_artifacts:
  - "thesis/THESIS_STRUCTURE.md"
  - "thesis/WRITING_STATUS.md"
  - "thesis/chapters/02_theoretical_background.md (§2.2 / §2.3 — what NOT to repeat)"
  - "thesis/references.bib"
  - ".claude/author-style-brief-pl.md"
  - ".claude/scientific-invariants.md"
  - ".claude/rules/thesis-writing.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/01_03_04_event_profiling.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
  - "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_long_raw.yaml"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/matches_flat_clean.yaml"
  - "src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_history_all.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/research_log.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/STEP_STATUS.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
  - "src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_long_raw.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/matches_1v1_clean.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoestats/data/db/schemas/views/player_history_all.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/research_log.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/STEP_STATUS.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/PIPELINE_SECTION_STATUS.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility_assessment.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_long_raw.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/matches_1v1_clean.yaml"
  - "src/rts_predict/games/aoe2/datasets/aoe2companion/data/db/schemas/views/player_history_all.yaml"
critique_required: true
research_log_ref: null
---

# Plan: Thesis §4.1.1 (SC2EGSet) and §4.1.2 (AoE2 datasets) — Category F data-fed sections

## Scope

Draft three data-fed thesis subsections in `thesis/chapters/04_data_and_methodology.md`:
**§4.1.1 — SC2EGSet (StarCraft II)** (target ~6–10 stron polskich, ~15–22 tys. znaków),
**§4.1.2 — Korpusy AoE2 (aoestats + aoe2companion)** (target ~6–10 stron, ~18–28 tys.
znaków), and **§4.1.3 — Asymetria danych** (target ~4–7 tys. znaków). All three sections
relocate the corpus statistics that Sprint 7's adversarial review removed from §2.2.5 and
§2.3.4 (commit `1492d90`) into their proper home, ground every numerical claim in Phase 01
artifacts (sections 01_01–01_04 for all three datasets), and acknowledge dataset-level
limitations with forward references to §6.5 (threats to validity). Two CONSORT-style flow
tables (one per game) and the cross-dataset asymmetry split into two tables (Tabela 4.4a
— Skala i akwizycja; Tabela 4.4b — Asymetria analityczna) comprise the load-bearing
tabular content. §4.1.3 is included in this PR's scope as it is a 4–7k Polish-char section
that exists solely to host the asymmetry tables; co-locating it with §4.1.1 / §4.1.2 in a
single PR avoids a half-finished §4.1 chapter.

## Problem Statement

Three datasets have completed Phase 01 sections 01_01 through 01_04 as of 2026-04-17:
sc2egset (PIPELINE_SECTION 01_04 → complete on 2026-04-17), aoestats (01_04 → complete
2026-04-17), aoe2companion (01_04 → complete 2026-04-17 in this PR). Each dataset now has
a frozen analytical schema (`matches_*_clean` + `player_history_all` VIEWs), a per-VIEW
missingness ledger, a CONSORT-style row-flow audit, and a per-dataset research log
populated with the 2026-04-16/17 cleaning entries. This produces enough verifiable
material to draft the `§4.1` corpus description — that is, the methodological description
of *what data the thesis actually uses, with what scope and what known defects* — without
waiting for Phase 01 sections 01_05 (Temporal & Panel EDA) and 01_06 (Decision Gates).

The Sprint 7 retrospective adversarial review (commit `1492d90`, see `WRITING_STATUS.md`
notes for §2.2 and §2.3) caught two BLOCKER-grade scope creeps in Chapter 2: §2.2.5
"Korpus SC2EGSet" subsection had been writing data-driven corpus statistics into a
literature-only section, and §2.3.4 "Źródła danych — aoestats, aoe2companion, mgz parser"
had been doing the same for AoE2. Both subsections were trimmed — `§2.2` lost ~2 tys.
znaków, `§2.3` lost ~4.3 tys. znaków — and the corpus statistics were earmarked for
relocation to §4.1.1 / §4.1.2. This plan closes that loop.

The sections are flagged BLOCKED in `WRITING_STATUS.md` (precondition: Step 01_08 game
settings + completeness audit for §4.1.1; AoE2 roadmap completion for §4.1.2). The user
has explicitly authorized drafting now on the grounds that 01_01–01_04 artifacts are
sufficient for a corpus description that is honest about its limitations and that flags
01_05+ items as `[REVIEW: needs Step 01_NN]` rather than waiting for them. Items the
draft cannot yet ground (e.g., per-tournament temporal stratification, per-Elo-bin
distribution shapes that need 01_05 outputs) are explicitly listed in §"Out of scope"
and re-raised as `[REVIEW]` flags inside the prose.

## Assumptions & unknowns

- **Assumption — corpus snapshots are stable.** All three datasets had their analytical
  VIEWs frozen on 2026-04-17 (sc2egset / aoestats / aoec). The plan assumes no reload
  before drafting completes. If the user reloads any raw data before execution, the
  executor must re-validate row/column counts against the schema YAMLs before commit.
- **Assumption — Phase 01 artifact set is the only source of truth for numbers.** No
  fresh DuckDB queries during drafting. Every number the prose claims must point at a
  specific Phase 01 artifact line (artifact path + section anchor or table caption).
  This is the Critical Review Checklist (Data variant) requirement from
  `.claude/rules/thesis-writing.md`.
- **Assumption — references.bib already covers the three datasets.** `Bialecki2023`,
  `AoEStats`, `AoeCompanion`, `AoE2DE`, `MgzParser` are already in `references.bib`
  per `WRITING_STATUS.md` Sprint 7 notes. New entries are needed only if the executor
  surfaces a Phase 01 finding traceable to a paper not yet cited (e.g., a Schafer &
  Graham 2002 missing-data paper if the missingness narrative requires it — the
  cleaning research log entries already cite this work). Any new entry is added in
  the same commit as the section that introduces it.
- **Assumption — Polish academic register.** Prose follows `.claude/author-style-brief-pl.md`:
  bezosobowy register ("przedstawiono", "stwierdzono", "udokumentowano"), no bullets
  in prose body, anglicisms italicized on first use (e.g., *replay file*, *dryf
  wersji*), `[KeyYear]` citations, hedging idioms in appropriate places.
- **Assumption — voice argumentative, not descriptive.** Per the brief, every
  methodological choice (e.g., "why true-1v1-decisive scope, not all 1v1?", "why two
  AoE2 corpora, not one?") gets at least one sentence of "dlaczego to, a nie oczywista
  alternatywa?" reasoning in the same paragraph as the choice.
- **Unknown — exact date range coverage of SC2EGSet replays inside the corpus.**
  Acquisition file inventory lists 70 tournament directories named with year prefixes
  spanning 2016–2024 (smallest year = 2016 IEM 10 Taipei, largest = 2024 EWC /
  HomeStory Cup XXVI / Stara Zagora Bellum Gens Elite). The actual `details.timeUTC`
  range needs the executor to point at a 01_02_04 univariate census line. Resolves by:
  reading `01_02_04_univariate_census.md` row for `details.timeUTC` (or equivalent).
  If unambiguous → fact; otherwise `[REVIEW: timeUTC range not in 01_02_04 — needs
  01_05 temporal EDA]`.
- **Unknown — exact aoestats and aoec date range.** File inventories give 2022-08-28
  to 2026-02-07 (aoestats matches/players, with 4 multi-day gaps) and 2020-08-01 to
  2026-04-04 (aoec matches, no gaps). The executor must verify against
  `01_02_04_univariate_census.md` `started_timestamp` / `started` ranges that the
  filename-date range matches the intra-file date range; if mismatched, flag and use
  the intra-file range as authoritative.
- **Unknown — exact tournament count post-true-1v1 filter.** The 70 acquisition
  directories include some that may lose all replays under the 22,209-replay
  `matches_flat_clean` scope. The executor reads `01_03_02_true_1v1_profile.md` (or
  equivalent) for the true-1v1 filter narrative; if it does not break down by
  tournament, the prose says "70 tournament directories at acquisition; the
  cleaning steps did not surface any tournament losing all replays — `[REVIEW: needs
  01_05 per-tournament breakdown]`".
- **Unknown — exact distinct civ count in aoestats vs aoec post-cleaning.** Schemas
  state "50 distinct civilizations" (aoestats matches_1v1_clean per `notes:`) and
  reference 45 in §2.3 prose. Executor reconciles via `01_03_01_systematic_profile.md`
  for both AoE2 datasets and reports the actual count from each, flagging the
  discrepancy with §2.3 if any.

## Literature context

Both subsections are **data-fed**, not literature-fed; the literature work for AoE2 /
SC2 background already lives in §2.2 and §2.3 (drafted in Sprint 7). §4.1 cites only:

- **The dataset papers themselves** (must cite, in their proper home):
  - `Bialecki2023` (SC2EGSet, Scientific Data) — must cite with corpus claim,
    Zenodo DOI, version 2.1.0, license.
  - `AoEStats` (aoestats.io aggregator) — must cite with API claim and Parquet dump
    description.
  - `AoeCompanion` (aoe2companion REST API project) — must cite with API claim and
    schema description.
  - `AoE2DE` (Definitive Edition release notes / patch documentation) — must cite for
    the patch-period framing.
  - `MgzParser` (aoc-mgz parser library) — cited in §2.3 for replay-parsing
    feasibility; appears in §4.1.2 only as a forward reference to §7.3 (future work),
    not as a primary tool of this thesis.
- **Methodological background for missing-data treatment** (must cite where the
  cleaning narrative invokes them — these are already in the per-dataset research
  log entries dated 2026-04-17):
  - `Rubin1976` — MCAR/MAR/MNAR taxonomy. Cite when explaining the missingness
    audit framework. `[REVIEW: confirm this entry exists in references.bib; if
    not, add it as `Rubin1976` with Biometrika 63(3):581–592, 1976]`.
  - `vanBuuren2018` — warning against rigid global thresholds for missingness, S4
    rule (>80%) for drop. Cite when justifying the >80% MMR drop in sc2egset and
    the antiquityMode/server/scenario drop in aoec. `[REVIEW: confirm bib key]`.
  - `SchaferGraham2002` — the <5% MCAR boundary used uniformly across the three
    cleaning audits. Cite when justifying RETAIN_AS_IS for low-NULL game settings.
    `[REVIEW: confirm bib key]`.
- **Forward references to thesis sections** (no literature, just chapter pointers):
  - §1.4 (scope and limitations) — for the framing of "professional-only data"
    asymmetry.
  - §2.2 (StarCraft II mechanics) — for the asymmetric-races and event-stream
    background that §4.1.1 does not re-explain.
  - §2.3 (Age of Empires II mechanics) — for the four-resource economy and
    civilisation roster background that §4.1.2 does not re-explain.
  - §2.5 (rating systems) — for the Elo / Glicko-2 background relevant to the
    `rating` / `old_rating` columns and the MMR sentinel discussion.
  - §2.6 (evaluation metrics) — for the cross-game comparison framing.
  - §3.2 (SC2 prediction literature) — for the SC2EGSet's place among public corpora.
  - §4.2 (data preprocessing) — forward reference for cleaning-rule details that
    §4.1 only summarises.
  - §4.3 (feature engineering) — forward reference for what the per-VIEW columns
    are eventually consumed by.
  - §4.4 (experimental protocol) — forward reference for the per-player temporal
    split that operationalises the cross-dataset asymmetries documented here.
  - §6.5 (threats to validity) — forward reference for downstream consequences of
    each limitation acknowledged in §4.1.

[OPINION] The cross-dataset asymmetry table is inherently methodologically novel —
no published RTS comparison work I know of presents three corpora at once with this
column-set / row-grain / event-stream / rating-availability matrix. The plan does
not need a literature anchor for the *table format*; the comparator is the implicit
"informacja o danych" demand that any defensible empirical thesis owes the reader.

## Execution Steps

### T01 — Read all Phase 01 artifacts and catalog every numerical claim

**Objective:** Build a complete artifact-to-claim crosswalk before writing prose, so
that every number in §4.1.1 / §4.1.2 traces to a specific artifact line. This is a
*read-only* preparatory step — its sole output is the crosswalk that T02–T07 consume.

**Instructions:**
1. Read `thesis/THESIS_STRUCTURE.md` lines covering §4.1.1 / §4.1.2 / §4.1.3 (lines
   ~178–200); read `thesis/WRITING_STATUS.md` lines for these two sections; read
   `.claude/author-style-brief-pl.md` end-to-end; read `.claude/rules/thesis-writing.md`
   end-to-end.
2. Read `thesis/chapters/02_theoretical_background.md` — ALL of §2.2.x
   subsections AND ALL of §2.3.x subsections (not only §2.2.5 / §2.3.4).
   For each subsection, classify every numerical claim or corpus statistic
   appearing in the prose as:
   (a) **instrumental** — legitimately belongs in §2 as background/literature
       context (e.g., a citation to an external benchmark); keep as-is.
   (b) **§4.1 migration candidate** — a corpus statistic that should live in
       §4.1 rather than in §2 (e.g., row counts, schema column counts, rating
       null rates that describe THIS thesis's datasets).
   Catalog the exact sentences for each (b) finding so the §4.1 draft
   satisfies these promises and avoids verbatim repetition.
   **Halt condition:** If more than 3 (b) findings are surfaced across all
   §2.2.x + §2.3.x subsections, STOP and report to parent session before
   proceeding to step 3. The parent session will decide whether those
   statistics should be removed from §2 in a separate chore commit before
   this plan's execution continues.
3. For SC2EGSet, read in sequence:
   - `reports/research_log.md` entries dated 2026-04-09 through 2026-04-17 (Phase 01
     sections 01_01–01_04, all 16 step entries)
   - `reports/STEP_STATUS.yaml` (verify all 01_01–01_04 steps `complete`)
   - `reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
     (70 tournament directories, 22,390 replay files, 214 GB raw size)
   - `reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md`
     (per-column null/sentinel/cardinality table; specifically pull `details.timeUTC`
     range, `metadata.gameVersion` distinct count, `metadata.mapName` cardinality,
     `MMR` zero rate)
   - `reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md`
   - `reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md`
     (MMR distribution mean/std/skewness, race distribution, result distribution,
     APM distribution, MMR_rated_only IQR fence)
   - `reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md`
     (players-per-replay distribution, max_players distribution, Undecided/Tie count,
     empty selectedRace count = 1110 rows / 555 replays = "Random" race, BW race
     variant rows = 3, replay classification breakdown leading to 22,209 true 1v1
     decisive)
   - `reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.md`
     (which raw tables made it into the analytical pipeline and which were declared
     out of scope)
   - `reports/artifacts/01_exploration/03_profiling/01_03_04_event_profiling.md`
     (event stream sizes: tracker_events_raw 62,003,411 rows / 10 event types,
     game_events_raw 608,618,823 rows / 23 event types, message_events_raw 52,167
     rows / 3 event types; PlayerStats 160-loop period = ~7.14s at Faster speed;
     UnitBorn dominates tracker stream at 36.08%; CameraUpdate dominates game stream
     at 63.67%; per-replay event density mean/median)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md`
     (matches_long_raw 44,817 rows / 22,390 replays; side asymmetry side=0 wins
     51.96% vs side=1 wins 47.97% — 3.99pp deviation, alert threshold 10pp not
     breached; leaderboard_raw NULL for 100% of rows = "tournament dataset, no
     matchmaking ladder")
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` (R01
     true-1v1-decisive: -24 replays / -85 rows; R03 MMR<0 replay-level exclusion:
     -157 replays / -314 rows; final matches_flat_clean = 22,209 replays / 44,418
     rows; 50.0/50.0 result balance; 2,495 distinct toon_ids in player_history_all;
     1,110 selectedRace='' → 'Random' normalisation; 273 map_size=0 anomaly flagged
     not excluded; isBlizzardMap duplication audit; gameSpeed cardinality=1 W02 fix;
     gd_isBlizzardMap == details_isBlizzardMap W03 fix; NULLIF guard W04 fix)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
     (load and pull MMR rates 83.95% in matches_flat_clean / 83.65% in
     player_history_all; highestLeague ~72%; clanTag ~73.93% in player_history_all;
     APM=0 sentinel 1,132 rows = 2.53% in player_history_all; handicap=0 anomalous
     2 rows = 0.0045%)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md`
     (final column counts: matches_flat_clean 28 cols (49→28, dropped 21);
     player_history_all 37 cols (51→37, dropped 16, added 2 — is_decisive_result
     and is_apm_unparseable, modified 1 — APM via NULLIF); 18 validation assertions
     PASS; 1132 APM NULLs as expected; 26 non-decisive Undecided/Tie rows in
     player_history_all)
   - Schema YAMLs: `data/db/schemas/views/matches_long_raw.yaml`,
     `matches_flat_clean.yaml`, `player_history_all.yaml`
4. For aoestats, read in sequence (same pattern):
   - `reports/research_log.md` 2026-04-15 through 2026-04-17 entries
   - `reports/STEP_STATUS.yaml`
   - `reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
     (matches: 172 weekly Parquet files, 610.55 MB, 2022-08-28 to 2026-02-07 with
     3 gaps; players: 171 weekly Parquet files, 3162.86 MB, 2022-08-28 to 2026-02-07
     with 4 gaps; matches/players directories must match — they don't exactly
     (171 vs 172) — flag this asymmetry)
   - `reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md` (avg
     elo_diff between team-0 and team-1 winners — pulls the team-1 wins ~52.27%
     asymmetry from the source)
   - `reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md`
   - `reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md`
   - `reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md`
     (total matches 30,690,651; matches with player data 30,477,761 = 99.31%;
     true 1v1 18,438,769 = 60.08%; ranked 1v1 random_map 17,815,944 = 58.52%;
     Jaccard true 1v1 ∩ ranked 1v1 = 0.958755; co_random_map 622,817 = 3.38% of
     true 1v1)
   - `reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility.md`
     (which raw tables are usable; overviews_raw out of analytical scope)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md`
     (matches_long_raw 107,626,399 rows; side asymmetry side=1 wins ~52.27% in
     1v1 ranked scope; leaderboard_raw distribution: random_map 35.6M,
     team_random_map 67.9M, co_team_random_map 2.8M, co_random_map 1.2M)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md`
     (R01–R08; profile_id precision check max=24,853,897 < 2^53 SAFE for BIGINT;
     scope funnel: 30,690,651 → 18,438,769 structural 1v1 → 17,815,944 ranked
     random_map → 17,814,947 after R08 inconsistent-winner exclusion (997 rows,
     0.0056%); ratings_raw absence W03 finding; opening/age_uptime in-game
     populated until 2024-03-10 then drops to 0% — patch event)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
     (per-column rates for matches_1v1_clean and player_history_all; key:
     leaderboard + num_players + raw_match_type constants; p0_old_rating
     n_sentinel=4,730 = 0.0266%; p1_old_rating 188 = 0.0011%; avg_elo 118 =
     0.0007%; team_0/1_elo sentinel=-1 absent in 1v1 ranked scope; player_history_all
     old_rating sentinel=0 5,937 rows = 0.0055%)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md`
     (matches_1v1_clean 21→20 cols; player_history_all 13→14 cols; 33 validation
     assertions PASS)
   - Schema YAMLs: same three.
5. For aoe2companion, read in sequence:
   - `reports/research_log.md` 2026-04-15 through 2026-04-17 entries
   - `reports/STEP_STATUS.yaml`
   - `reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.md`
     (matches: 2073 daily Parquet files, 6621.52 MB, 2020-08-01 to 2026-04-04, no
     gaps; ratings: 2072 daily CSV files, 2519.59 MB, 1 small gap; leaderboards:
     1 snapshot file 83.32 MB; profiles: 1 snapshot file 161.84 MB)
   - `reports/artifacts/01_exploration/01_acquisition/01_01_02_schema_discovery.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_04_univariate_census.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_06_bivariate_eda.md`
   - `reports/artifacts/01_exploration/02_eda/01_02_07_multivariate_analysis.md`
   - `reports/artifacts/01_exploration/03_profiling/01_03_01_systematic_profile.md`
   - `reports/artifacts/01_exploration/03_profiling/01_03_02_true_1v1_profile.md`
     (74,788,989 distinct matchIds; 40,062,975 = 53.57% have 2 rows/match — true
     1v1 candidates; profileId=-1 ai status 12,947,078 rows / 4,150,733 matches
     excluded as AI; profileId=-1 player status 19,232 rows / 8,993 matches
     excluded as parse-failed-player)
   - `reports/artifacts/01_exploration/03_profiling/01_03_03_table_utility_assessment.md`
     (leaderboards_raw and profiles_raw declared out-of-analytical-scope; matches_raw
     primary)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_00_source_normalization.md`
     (matches_long_raw 277,099,059 rows; team encoding artifact: aoec uses team=1/2
     not team=0/1 for 1v1 — side encoding fix in CASE WHEN; side=0 only 449 rows
     vs side=1 130,369,073 rows in this 0/1 mapping — explained as encoding artifact)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` (R00
     status='player' filter: removed 12.95M ai rows + 19,232 parse-failed-player rows;
     R02 profileId != -1; R03 1v1 complementarity HAVING COUNT(*)=2 with TRUE+FALSE
     won; R04 NULL-cluster era boundary; final matches_1v1_clean 30,531,196 matches
     × 2 rows = 61,062,392 player-rows; player_history_all 264,132,745 rows)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
     (matches_1v1_clean: rating 26.20%, server 97.39%, scenario 100%, modDataset
     100%, password 77.57%, antiquityMode 60.06%, hideCivs 37.18%, country 2.25%,
     mod/status n_distinct=1 constants, won 0% by R03 complementarity;
     player_history_all: won 0.0073% NULL = 19,251 rows, country 8.30%)
   - `reports/artifacts/01_exploration/04_cleaning/01_04_02_post_cleaning_validation.md`
     (matches_1v1_clean 54→48 cols; player_history_all 20→19 cols)
   - Schema YAMLs.
6. Build a crosswalk of all numbers the plan's prose plan (T03–T07) cites.
   Each row of the crosswalk: `{claim_text, artifact_path,
   artifact_anchor_or_table_name, prose_form, artifact_form, normalized_value,
   datatype, hedging_needed}`. For every numerical claim that resolves cleanly
   to one artifact line, mark `hedging_needed=False`. For every claim that
   requires aggregation across artifacts (e.g., "across all three datasets, the
   cleaning audits used the <5% Schafer & Graham 2002 MCAR boundary uniformly")
   or where the artifact is ambiguous, mark `hedging_needed=True` and add a
   `[REVIEW]` flag.

   **Number-format normalization (per round-1 critique fix B-1):** Prose uses
   Polish typography (non-breaking space `\u00A0` between thousand groups, e.g.,
   `22 390`). Artifacts use comma thousands (e.g., `22,390`) or no separator
   (e.g., `22390`). Numerical match verification is computed after normalizing
   BOTH forms to plain integer: `int(value.replace(',', '').replace(' ',
   '').replace('\u00A0', ''))`. The crosswalk `prose_form` column records the
   Polish-typography form; the `artifact_form` column preserves the source form
   verbatim; the `normalized_value` column holds the integer used for equality
   testing. Decimals follow Polish convention (`260,5`, NOT `260.5`); for
   decimal verification, normalize to `float(value.replace(',', '.'))`.

   Persist crosswalk to `temp/plan_4.1_crosswalk.md` as a structured Markdown
   table (format specified in step 7 below).

7. **Persist crosswalk artifact.** Write `temp/plan_4.1_crosswalk.md` with the
   following structure:

   ```markdown
   # §4.1 Numerical Crosswalk
   Generated: 2026-04-17 by T01 executor.

   | claim_text | artifact_path | anchor | prose_form | artifact_form | normalized_value | datatype | hedging_needed |
   |---|---|---|---|---|---|---|---|
   | ... | ... | ... | ... | ... | ... | int/float/str | True/False |
   ```

   Rules: one row per distinct number cited in T03–T07 prose plan. If a number
   appears in multiple datasets, create one row per dataset. Append a summary
   line at the bottom: `Total: N rows, M with hedging_needed=True.`

**Verification:**
- The executor produces a durable crosswalk persisted to disk at `temp/plan_4.1_crosswalk.md`
  (per Fix 9 / step 7) listing every number used in T03–T07 with its artifact pointer.
  No prose-writing task may begin without this crosswalk being written to disk; T07
  re-reads it explicitly (not from working memory, which may have been compressed).
- For each of the 3 datasets, the artifact set actually read in T01 contains:
  acquisition file inventory, univariate census, systematic profile, true-1v1 profile,
  source normalisation MD, data cleaning MD + missingness ledger CSV, post-cleaning
  validation MD, and the three schema YAMLs (matches_long_raw, matches_*_clean,
  player_history_all). Total artifact files read: at least 3 datasets × 11 files =
  33 files.
- The executor confirms the §2.2.5 / §2.3.4 sentence catalog is complete: every
  data-claim sentence flagged for relocation in commit `1492d90` notes is accounted
  for and assigned to a §4.1.1 / §4.1.2 subsection.

**File scope:** `temp/plan_4.1_crosswalk.md` (write — produced in step 7).

**Read scope:**
- All artifacts listed under `source_artifacts` in the frontmatter.

---

### T02 — Draft §4.1 framing paragraph and §4.1.1.0 SC2EGSet citation block

**Objective:** Open §4.1 with a 2-paragraph framing that (a) sets up the section's
purpose (corpus description as methodological commitment, not narrative colour) and
(b) explicitly states the cross-dataset commitment ("trzy korpusy: jeden SC2,
dwa AoE2; szczegółowy opis każdego — niżej; podsumowanie porównawcze — w §4.1.3
oraz tablicy asymetrii na końcu §4.1.2"). Then open §4.1.1 with the canonical
citation block for SC2EGSet (Bialecki2023, Zenodo DOI, version 2.1.0, license,
distributor, date of acquisition).

**Instructions:**
1. Write the §4.1 opening framing in Polish (~1.5–2.5 tys. znaków) covering:
   - The purpose of §4.1 as methodological commitment, not corpus marketing.
   - Forward-reference to §4.2 (preprocessing) for cleaning details and §4.3–§4.4
     for feature/protocol details.
   - Backward-reference to §1.4 (scope and limitations) for the "professional vs.
     ladder" population-asymmetry framing established there.
   - The cross-dataset roadmap: "§4.1.1 omawia korpus SC2EGSet [Bialecki2023] dla
     StarCraft II; §4.1.2 omawia dwa komplementarne korpusy AoE2 (aoestats
     [AoEStats] i aoe2companion [AoeCompanion]); §4.1.3 syntezuje wnioski
     porównawcze i prezentuje tablicę asymetrii."
2. Write §4.1.1.0 (no number — opens §4.1.1) covering the citation block (~1.5
   tys. znaków):
   - "SC2EGSet: StarCraft II Esport Replay and Game-state Dataset" jako exact
     dataset title (per scientific-invariants.md I9 wymóg).
   - Authors and journal (Bialecki et al., 2023, Scientific Data) — must cite
     `[Bialecki2023]`.
   - Zenodo distribution: https://zenodo.org/records/17829625 with version
     identifier (v2.1.0 per `THESIS_STRUCTURE.md`).
   - License (CC-BY 4.0 — `[REVIEW: confirm license from Zenodo metadata]`).
   - Acquisition date for this thesis: refer to `01_01_01_file_inventory.md`
     (mtime / last-modified evidence) — `[REVIEW: 01_01_01 doesn't record an
     acquisition date; cite the research log 2026-04-09 entry as proxy "data
     pozyskania to data wykonania kroku 01_01_01, czyli 2026-04-09"]`.
   - One sentence positioning SC2EGSet in the SC2 public-corpora landscape
     (UAlbertaBot Replay → MSC [Wu2017] → SC2EGSet [Bialecki2023]) — short, no
     duplication of §3.2; see THESIS_STRUCTURE.md §3.2 for full SC2 lit
     coverage.

**Voice constraints (Pass 1 Data variant):**
- Opening framing must avoid generic dataset-marketing language. No "obszerny
  korpus", no "bogata dokumentacja". Specific facts only.
- The argumentative sentence Tomasz expects: "Decyzja o oparciu predykcji SC2 na
  korpusie [Bialecki2023], a nie na MSC [Wu2017], wynika z trzech jednoczesnych
  okoliczności: pełnej dystrybucji plików `.SC2Replay`, większej liczby zdarzeń
  trakerowych na replay, oraz dłuższego okresu temporalnego — szczegóły w
  podsekcjach 4.1.1.1–4.1.1.4."

**Verification:**
- The §4.1 opening is 1.5–2.5 tys. znaków; cites at least 3 thesis sections by
  number; uses bezosobowy register throughout.
- §4.1.1.0 contains the exact dataset title verbatim, the Zenodo DOI, the
  version, and at least one cited reference for the SC2 corpora landscape.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (in-place edit of the §4.1 opening
  and §4.1.1 opening — the existing skeleton lines `## 4.1 Datasets`,
  `### 4.1.1 SC2EGSet (StarCraft II)`, and the HTML comment under §4.1.1 are
  replaced with prose)

**Read scope:**
- Crosswalk built in T01.

---

### T03 — Draft §4.1.1 SC2EGSet remaining subsections (§4.1.1.1 through §4.1.1.5)

**Objective:** Cover the THESIS_STRUCTURE-mandated content for §4.1.1 — corpus
size, tournament count, date range, replay structure; data quality (parse
coverage, missing events, duration distribution); APM availability and MMR
unusability; limitations explicitly acknowledged.

**Subsection breakdown** (each with an artifact-anchor → claim mapping):

#### §4.1.1.1 — Skala i pokrycie czasowe korpusu (~3–4 tys. znaków)
- Liczba turniejów: 70 katalogów turniejowych (zgodnie z findingiem
  `01_01_01_file_inventory.md`, sekcja "Top-level directories: 70"), z czego
  najmniejszy zawiera 30 powtórek (2016 IEM 10 Taipei), największy — 1296
  (2022_03_DH_SC2_Masters_Atlanta), mediana 260,5 powtórek na turniej.
- Liczba surowych powtórek: 22 390 plików `.SC2Replay.json` o łącznym
  rozmiarze ~214 GB (`01_01_01_file_inventory.md`).
- Pokrycie czasowe: ~2016–2024 zgodnie z prefiksami katalogów turniejowych.
  `[REVIEW: dokładny zakres details.timeUTC pochodzący z 01_02_04 univariate
  census należy zweryfikować w wykonaniu T01; jeśli niedostępny, prosić o
  Step 01_05 temporal EDA]`.
  [REVIEW: temporal concentration of tournaments deferred to Phase 01 Step
  01_05].
- Hedging idiomatyczny: "Na podstawie inwentarza plików można stwierdzić,
  że..."
- Closing sentence (forward reference): "Skala SC2EGSet w kontekście
  porównawczym wszystkich trzech korpusów — w Tabeli 4.4a w §4.1.3."

**Must justify:** wybór SC2EGSet [Bialecki2023] over MSC [Wu2017] (forward
reference to §3.2); wybór 1v1 jako jedynego scope (forward reference do §1.4 i
§4.4.1).

**Must contrast:** Skala SC2EGSet vs MSC vs UAlbertaBot Replay Dataset (jedno
zdanie przewidziane w §4.1.1.0, nie powielane).

#### §4.1.1.2 — Struktura plików powtórek i strumieni zdarzeń (~3–4 tys. znaków)
- Trzy strumienie zdarzeń per replay: `tracker_events_raw` (62 003 411
  zdarzeń łącznie / 10 typów; UnitBorn 36,08% dominuje), `game_events_raw`
  (608 618 823 zdarzeń łącznie / 23 typów; CameraUpdate 63,67% dominuje),
  `message_events_raw` (52 167 zdarzeń łącznie / 3 typy). Wszystko z
  `01_03_04_event_profiling.md`.
- Periodyczność PlayerStats: 160 game loops dla ~98% obserwacji, czyli
  ~7,14 s przy prędkości *Faster* (160/22,4) — naturalny rytm próbkowania
  cech śródmeczowych. Forward-reference to §4.3.2 (SC2-specific in-game
  features) — w §4.1.1 odnotowujemy tylko dostępność, nie konsumpcję.
- Pokrycie zdarzeń per replay: UnitBorn / PlayerStats / PlayerSetup w 100%
  replays; UnitOwnerChange tylko w 25,39% (Neural Parasite / mind control
  rzadkie zjawisko).
- Backward-reference to §2.2.4 (silnik gry i format powtórek) — bez
  powtarzania mechaniki. Argumentacja: "Trzy odrębne strumienie zdarzeń
  generują strukturalną przewagę SC2EGSet nad agregowanymi korpusami AoE2
  omawianą w §4.1.2 — przewagę wykorzystywaną w §4.3.2 oraz omawianą jako
  oś asymetrii eksperymentalnej w §1.4."

**Must justify:** dlaczego oddzielne strumienie tracker / game / message są
istotne dla zadania predykcji — bo umożliwiają rekonstrukcję ścieżki
ekonomicznej i militarnej z dokładnością do pojedynczego zdarzenia, a nie
tylko z dostępu do agregowanych statystyk meczu.

#### §4.1.1.3 — Schemat analityczny po wstępnym czyszczeniu (~3–5 tys. znaków)
- Trzy widoki DuckDB powstałe w trakcie Phase 01 / Pipeline Section 01_04:
  `matches_long_raw` (warstwa kanoniczna long-skeleton, 44 817 wierszy =
  ~2 wiersze na replay), `matches_flat_clean` (widok celu predykcji, 28
  kolumn × 44 418 wierszy = 22 209 powtórek prawdziwe-1v1-rozstrzygnięte),
  `player_history_all` (widok historii cech, 37 kolumn × 44 817 wierszy
  obejmujący wszystkie powtórki dla feature engineering w §4.3).
- Schemat post-cleaning (`matches_flat_clean`): 28 kolumn obejmujących 5
  kategorii prowenancji (IDENTITY, TARGET, PRE_GAME, IN_GAME_HISTORICAL,
  CONTEXT) per niezmiennik I3 — dostępny w
  `data/db/schemas/views/matches_flat_clean.yaml`.
- Krótka tabela "Kategorie kolumn po czyszczeniu" (1 tabela formatowa, ~6
  wierszy) z liczbą kolumn per kategoria w obu widokach. Forward-reference
  do §4.2.3 dla pełnej listy reguł czyszczenia.
- Argumentacja: "Decyzja o utrzymaniu dwóch oddzielnych widoków —
  `matches_flat_clean` jako celu predykcji i `player_history_all` jako
  źródła historii cech — wynika bezpośrednio z niezmiennika temporalnego
  (I3 / niezmiennik 3 sekcji 'Temporal discipline') i jest omawiana
  szczegółowo w §4.2.3 i §4.3."

**Must justify:** dlaczego model post-cleaning rozdziela target VIEW od
history VIEW (jednogłośność z aoestats / aoec); dlaczego utrzymanie 2 wierszy
na replay (w przeciwieństwie do aoestats 1-row-per-match).

#### §4.1.1.4 — Jakość danych: kompletność cech, parse coverage, MMR, APM (~3–5 tys. znaków)
- **Result distribution:** 22 382 Win / 22 409 Loss + 24 Undecided + 2 Tie
  w surowym korpusie; po filtracji true-1v1-decisive — 50,0% Win / 50,0%
  Loss perfect (`01_03_01_systematic_profile.md` "Categorical Top-5
  Profiles" + `01_04_01_data_cleaning.md` post-cleaning balance).
- **Race distribution:** Protoss 36,21% / Zerg 35,02% / Terran 28,76% +
  3 BW-prefixed wiersze (BWTe/BWZe/BWPr — odgrywki Brood War w jednej
  6-osobowej powtórce, klasyfikowane jako szum strukturalny i wykluczane
  filtrem true-1v1).
- **MMR unusability** (kluczowy *finding*): MMR=0 sentinel pokrywa 83,95%
  wierszy w `matches_flat_clean` i 83,65% wierszy w `player_history_all`
  (`01_04_01_missingness_ledger.csv`). Mechanism: MNAR (missing not at
  random) — sentinel odpowiada statusowi "unrated professional" w korpusie
  zawodowym. Decyzja DS-SC2-01: DROP_COLUMN per Rule S4 ([vanBuuren2018]),
  z zachowaniem flagi `is_mmr_missing` jako indykatora missingness-as-signal.
  Argumentacja: "Dropping MMR z 83,95% sentinelem nie jest standardową
  procedurą — alternatywą byłaby imputacja medianą-w-rasie albo retencja z
  flagą is_unrated. Wybór DROP_COLUMN z flagą wynika z (a) zerowej
  predykcyjnej wartości MMR=0 jako sygnału stałego dla 84% korpusu, (b)
  obecności pełnej historii cech w `player_history_all` umożliwiającej
  retrospektywne obliczenie rankingów Glicko-2 (omówione w §4.3) niezależnie
  od MMR z replay, (c) jednorodności decyzji z analogicznymi
  DS-AOESTATS-02 i DS-AOEC-04 dla AoE2."
- **APM availability:** APM dostępne dla 97,47% wierszy
  `player_history_all` (1 132 wierszy z APM=0 sentinel = 2,53% — parse
  failures lub puste replays; per DS-SC2-10 NULLIF zastosowane,
  is_apm_unparseable flag dodany). Klasyfikacja prowenancji:
  IN_GAME_HISTORICAL — APM nie jest cechą *pre-game*; może wystąpić w
  feature engineeringu wyłącznie jako agregat historyczny przefiltrowany
  przez `match_time < T` (per niezmiennik 3).
- **Highest league + clanTag:** dropped (DS-SC2-02 / 03) ze względu na
  72%+ sentinel coverage; istnienie tych pól w surowym schemacie odnotowane
  jako udokumentowany koszt parsera s2protocol.
- **SQ (spending quotient):** sentinel INT32_MIN dla 2 wierszy (parse
  artifact); NULLIF zastosowany w `player_history_all` (R05).
- **Pokrycie parsera:** 99,9509% replays ma rozsądny `players_per_replay=2`
  (22 379 z 22 390); pozostałe 11 to powtórki obserwacyjne, mecze 4/6/8/9
  graczy (`01_03_02_true_1v1_profile.md`). 26 wierszy Undecided/Tie w 13
  replays (typically disconnect / leaver) wykluczane filtrem decisive.
- **Distribution of game length (gd_mapSize, header_elapsedGameLoops):**
  pokrótce — `[REVIEW: rozkład długości meczu (header_elapsedGameLoops)
  nie jest jeszcze sprofilowany w 01_03; pełna analiza w 01_05 temporal
  EDA, do uzupełnienia w rewizji §4.1.1 po Step 01_05]`.

**Must contrast:** APM dostępność (97,47%) vs MMR niedostępność (16% rated)
— jako bezpośrednie świadectwo specyfiki populacji zawodowej; APM zawsze
parsowalne z replay, MMR opcjonalnie raportowane przez Battle.net tylko dla
ranked-ladder players (a większość zawodowych meczów na turniejach jest
na koncie unrated).

#### §4.1.1.5 — Asymetrie strony i ograniczenia (~2–3 tys. znaków)
- **Asymetria stron** (side-of-board): w `matches_long_raw` strona 0 wygrywa
  51,96%, strona 1 — 47,97% (różnica 3,99pp poniżej alert threshold 10pp;
  `01_04_00_source_normalization.md`). Decyzja w 01_04: udokumentować, nie
  korygować na poziomie surowego widoku; randomizacja focal/opponent
  obowiązkowa w Phase 02 per niezmiennik I5 — forward reference to §4.3.1.
- **Wąska reprezentacja populacji:** korpus zawodowy turniejowy; brak
  meczów ladderowych (`leaderboard_raw` NULL dla 100% wierszy
  matches_long_raw, `01_04_00_source_normalization.md`). Konsekwencje dla
  generalizacji omawiane w §4.4 i §6.5.
- **Kompletność map:** 188 unikalnych nazw map zgodnie z
  `01_03_03_table_utility.md` (cite); 273 powtórki z
  `gd_mapSizeX/Y=0` (parse artifact, `01_04_01_data_cleaning.md` finding);
  decyzja: NULLIF + retain in player_history_all, drop from
  matches_flat_clean (DS-SC2-06).
- **Dryf wersji (dryf między patchami):** 22 390 replays obejmują wiele
  patchy SC2; `metadata.gameVersion` ma dużą kardynalność. `[REVIEW:
  dokładną liczbę patchy zweryfikować w 01_02_04 univariate census; jeśli
  niedostępna, Step 01_05 temporal EDA]`. Konsekwencje dryfu wersji omawiane
  w §4.4 (split protocol) i §6.5 (threats to validity).
- Zamykające zdanie: "Pełna lista konsekwencji wymienionych ograniczeń
  dla protokołu eksperymentalnego — w §4.4; konsekwencje dla trafności
  wniosków — w §6.5."

**Must justify:** decyzja niekorygowania asymetrii strony na poziomie
01_04 (alternatywa — przepróbkowanie wierszy aż do 50/50; wybór:
udokumentowanie + randomizacja w Phase 02, ponieważ przepróbkowanie zmieniłoby
liczbę wierszy i zakłóciło CONSORT chain).

**CONSORT Tabela 4.1 — Przepływ danych SC2EGSet** (wstawiana po §4.1.1.5,
przed §4.1.1.6 jeśli istnieje, lub jako finalna sekcja §4.1.1):

| Etap | Mecze (powtórki .SC2Replay) | Wiersze gracz×mecz |
|---|---|---|
| Surowe pliki `.SC2Replay.json` (acquisition) | 22 390 | n/a |
| `replays_meta_raw` po dekompresji | 22 390 | n/a |
| `replay_players_raw` po dekompresji | n/a | 44 817 |
| `matches_long_raw` (lossless JOIN) | 22 390 | 44 817 |
| `matches_flat` (structural JOIN) | 22 390 | 44 817 |
| Po R01 (true_1v1_decisive: -24 mecze) | 22 366 | 44 732 |
| Po R03 (MMR<0 replay-level exclusion: -157 mecze) | 22 209 | 44 418 |
| **`matches_flat_clean` (cel predykcji)** | **22 209** | **44 418** |
| `player_history_all` (źródło historii cech, all replays) | 22 390 | 44 817 |

Caption: "Tabela 4.1. CONSORT-style przepływ danych SC2EGSet od surowych
plików powtórek do widoków post-cleaning. R01 = filtr true-1v1-decisive
(R01 z `01_04_01_data_cleaning.md`); R03 = wykluczenie wszystkich powtórek
zawierających choć jednego gracza z MMR<0 (BLOCKER F01 fix per critique).
Wiersze gracz×mecz w `matches_flat_clean` to 2× powtórki z założenia
2-wierszowej struktury per replay (niezmiennik I5)."

Hedging required: any claim that has more than one possible source artifact
(e.g., "MMR sentinel coverage" appears in both 01_04_01 missingness ledger
and the schema YAML notes) gets a single canonical citation pointing at the
ledger as the audit source; the schema YAML is a derived view of the ledger.

**Voice constraint — terminology consistency with §2.2.2:** When referring to
version-related instability in the SC2EGSet replay corpus, use "dryf wersji"
or "dryf między patchami" (per §2.2.2 production prose authority). Do NOT
write "patch drift" (anglicism). "Patch" may appear only when naming a
specific patch event (e.g., "po patchu 2024-03-10").

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (replaces and expands the existing
  §4.1.1 skeleton lines 5–13 with full prose for §4.1.1.0 through §4.1.1.5 + Tabela 4.1)

**Read scope:**
- Crosswalk built in T01 (`temp/plan_4.1_crosswalk.md`).

**Halt condition (mid-execution):** If any subsection (§4.1.1.1 through
§4.1.1.5) exceeds its per-subsection character cap (§4.1.1.1: 4k; §4.1.1.2:
4k; §4.1.1.3: 5k; §4.1.1.4: 5k; §4.1.1.5: 3k), STOP and report to parent
session before continuing. If any numerical claim cannot be grounded in the
T01 crosswalk, insert `[REVIEW: ungrounded number — X]` and continue, but
flag count in T08 handoff.

---

### T04 — Draft §4.1.2 framing and §4.1.2.1 aoestats subsection

**Objective:** Open §4.1.2 with a framing paragraph explaining the dual-corpus
strategy (why two AoE2 sources rather than one), then describe the aoestats
corpus with the same depth pattern as §4.1.1.

**Subsection breakdown:**

#### §4.1.2.0 — Framing: dlaczego dwa korpusy AoE2 (~2–3 tys. znaków)
- Forward reference do §2.3.4 (literackie umiejscowienie aoestats /
  aoe2companion / mgz parser) bez powtarzania.
- Triple validation argument: (a) wybrane statystyki opisowe można
  porównać między korpusami — kontrola próbkowania; (b) predykcje wytrenowane
  na cechach z aoestats walidowane na cechach analogicznych z aoec —
  rozdzielenie efektu metody od efektu źródła; (c) cechy wymagające
  długich okien historycznych (rolling win rate, retrospektywne Glicko-2)
  korzystają z aoec jako nadrzędnego, aoestats jako kontroli.
- Argumentacja decyzyjna: "Niezbędność strategii dwukorpusowej — w
  odróżnieniu od jednokorpusowej dla SC2EGSet — wynika bezpośrednio z faktu,
  że żadne z dwóch źródeł danych AoE2 nie udostępnia plików surowego
  zapisu meczu na skalę porównywalną do korpusu SC2EGSet [Bialecki2023].
  Komplementarność między aoestats (szeroki agregat) a aoe2companion
  (głębokie historie) jest substytutem strukturalnej bogactwa replays."
- Backward reference do §1.4 (asymetria eksperymentalna SC2 ↔ AoE2).

**Must justify:** dlaczego nie aoestats sam (zbyt agregowane); dlaczego nie
aoec sam (struktura player-row-oriented bardziej kosztowna w przetwarzaniu;
prostsze 1-row-per-match z aoestats jako kontrolne); dlaczego nie mgz parser
samodzielnie (rezygnacja z ścieżki replay-parsing dla AoE2 — forward
reference do §7.3 future work).

#### §4.1.2.1 — Korpus aoestats (~5–6 tys. znaków, łącznie z mini-CONSORT)

**§4.1.2.1.a — Cytowanie i pozyskanie:**
- "aoestats — agregator publicznie dostępny serwujący tygodniowe zrzuty
  bazy meczów rankingowych w formacie Parquet, generowane przez crawlowanie
  API aoe2.net [AoEStats]."
- Pliki: 172 weekly Parquet files w `matches/` (610,55 MB) + 171 weekly
  Parquet files w `players/` (3162,86 MB) + 1 plik `overview.json` z
  metadanymi singleton (`01_01_01_file_inventory.md`).
- **Asymetria wsadu**: matches/ ma 172 plików, players/ ma 171 plików — różnica
  1 pliku. `[REVIEW: zweryfikować pochodzenie różnicy w ostatnim tygodniu
  pobrania; jeśli niezamierzona, wymaga uzupełnienia w wykonaniu T01]`.
- Pokrycie czasowe: 2022-08-28 do 2026-02-07, 172 tygodni. Trzy luki w
  matches/ (2024-07-20 → 2024-09-01 = 43 dni, 2024-09-28 → 2024-10-06 = 8 dni,
  2025-03-22 → 2025-03-30 = 8 dni); cztery luki w players/ (te trzy plus
  2025-11-15 → 2025-11-23 = 8 dni). Argumentacja: "Luka 43-dniowa w lipcu/
  sierpniu 2024 odpowiada okresowi po wielkim patchu, w którym aoestats.io
  zatrzymał crawl — okoliczność udokumentowana w archiwach społeczności;
  w protokole walidacji w §4.4 ten przedział może wymagać dodatkowego
  okna purge."

**§4.1.2.1.b — Schemat analityczny po wstępnym czyszczeniu:**
- `matches_long_raw` (107 626 399 wierszy = lossless JOIN players_raw ×
  matches_raw przefiltrowany do profile_id IS NOT NULL i started_timestamp
  IS NOT NULL).
- `matches_1v1_clean` (20 kolumn × 17 814 947 meczów = 1 wiersz na mecz —
  WAŻNE: aoestats jest 1-row-per-match, nie 2-rows-per-match jak sc2egset
  i aoec; player slots zakodowane w kolumnach `p0_*` i `p1_*`).
- `player_history_all` (14 kolumn × 107 626 399 wierszy = wszystkie typy
  rozgrywki bez filtra leaderboard, dla pełnej historii feature
  computation).
- Argumentacja: "Decyzja o 1-row-per-match w aoestats nie jest naszym
  wyborem schematu — jest cechą formatu źródłowego aoestats. Rzetelne
  porównanie symetryczności gracz×mecz między korpusami wymaga jawnej
  konwersji w Phase 02; szczegóły w §4.3.1 i §4.4.1."

**§4.1.2.1.c — Jakość danych: rozkład Elo, kompletność rankingów, asymetria
slotów:**
- **Elo distribution:** średnie Elo meczu (`avg_elo`) — `[REVIEW: rozkład
  pełny, średnia, IQR, percentyle pochodzą z 01_03_01 systematic profile;
  zweryfikować w T01 dokładne wartości]`.
- **Rankingi (`p0_old_rating`, `p1_old_rating`):** sentinel=0 dla 4 730
  wierszy w `p0_old_rating` (0,0266%) i 188 wierszy w `p1_old_rating`
  (0,0011%). NULLIF + flagi `p0_is_unrated` / `p1_is_unrated` per
  DS-AOESTATS-02 (`01_04_01_missingness_ledger.csv`). Asymetria slotów
  (4 730 vs 188 sentinel) jest sama w sobie diagnostyką slot asymmetry —
  forward reference to §4.4.1.
- **avg_elo sentinel=0:** 118 wierszy (0,0007%) — NULLIF (DS-AOESTATS-03).
- **`team_0_elo`, `team_1_elo` sentinel=-1:** absent in 1v1 ranked scope
  (DS-AOESTATS-01 F1 override) — kolumny pozostają jako diagnostyczne dla
  scenariuszy non-1v1.
- **Asymetria stron (KLUCZOWY FINDING):** team=1 wygrywa ~52,27% meczów
  1v1 rankingowych, ze średnim `elo_diff = team_0_elo - team_1_elo`
  wynoszącym -18,48 gdy team=1 wygrywa vs -0,37 gdy team=0 wygrywa
  (`01_04_01_data_cleaning.md` TEAM-ASSIGNMENT ASYMMETRY block,
  `01_02_06_bivariate_eda.md`). Argumentacja: "Asymetria 52,27% nie jest
  losowa — jest funkcją mechaniki przypisywania graczy do slotów team=0/1
  przez aoestats, prawdopodobnie skorelowanej z Elo. Konsekwencja: każdy
  model trenowany bez randomizacji focal/opponent w Phase 02 nauczy się
  sygnału przypisywania, nie umiejętności gry. Niezmiennik I5 wymaga
  randomizacji; szczegóły w §4.3.1."
- **Inconsistent winners:** 997 wierszy (0,0056%) z `p0_winner = p1_winner`
  (811 oba False, 186 oba True) — wykluczone w `01_04_01_data_cleaning.md`
  R08. Niska skala (~5,6 na 100 000) — udokumentowane jako artefakt
  jakości upstream danych aoestats, nie jako artefakt naszego JOIN.
- **Schema-evolution:** kolumny in-game (`opening`,
  `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime`)
  wypełnione do ~2024-03-10 (~92%–86% NULL przed); od 2024-03-17 — 0%
  pokrycia (`01_04_01_data_cleaning.md` T05). Powód: zmiana
  konfiguracji crawlera lub formatu źródłowego. Argumentacja: "Dla
  zachowania spójności pre-game / in-game w niezmienniku I3 wykluczyliśmy
  te kolumny z `matches_1v1_clean` (DS-AOESTATS-04 i prior I3 cleanup);
  feature-inclusion (np. uśredniony historyczny age uptime jako proxy
  efektywności otwarcia) zdefiniowano jako Phase 02 decision (I9)."

**§4.1.2.1.d — Asymetrie i ograniczenia:**
- Brak in-game state (jak we wszystkich źródłach AoE2 — odnotować jednorazowo,
  nie powtarzać dla aoec).
- Brak granularnych identyfikatorów graczy (profile_id z aoestats jest
  wystarczająco unikalny — max=24 853 897 < 2^53 SAFE for BIGINT — ale
  wąskogłowny względem aoec).
- Pokrycie tylko 1v1 ranked random_map (96,62% true 1v1 zgodnie z
  `01_03_02_true_1v1_profile.md`); pozostałe 3,38% to co_random_map (1v1
  na koop. mapach) i ślad team_random_map / co_team_random_map.

**CONSORT Tabela 4.2 — Przepływ danych aoestats**:

| Etap | Mecze | Wiersze gracz×mecz |
|---|---|---|
| Surowe pliki Parquet (acquisition) | n/a | n/a |
| `matches_raw` po ingestion | 30 690 651 | n/a |
| `players_raw` po ingestion | n/a | 107 627 584 |
| Po ingestion-level filter (profile_id, started_timestamp non-null) | n/a | 107 626 399 |
| Po 1v1 structural filter (= 2 wierszy na mecz) | 18 438 769 | 36 877 538 |
| Po leaderboard='random_map' filter | 17 815 944 | 35 631 888 |
| Po R08 inconsistent-winner exclusion (-997 meczów) | 17 814 947 | 35 629 894 |
| **`matches_1v1_clean` (cel predykcji, 1-row-per-match)** | **17 814 947** | **17 814 947** |
| `player_history_all` (źródło historii, wszystkie leaderboardy) | n/a | 107 626 399 |

Caption: "Tabela 4.2. CONSORT-style przepływ danych aoestats. Uwaga: wiersze
gracz×mecz w `matches_1v1_clean` równe liczbie meczów z powodu
1-row-per-match struktury aoestats (kolumny `p0_*` / `p1_*` zawierają oba
gracze w jednym wierszu); wartość 35 629 894 = 2× 17 814 947 jest podana
dla porównywalności z `player_history_all`."

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (replaces and expands §4.1.2
  skeleton lines 15–20 with prose for §4.1.2.0 + §4.1.2.1)

**Read scope:**
- Crosswalk from T01 (`temp/plan_4.1_crosswalk.md`).

**Halt condition (mid-execution):** If §4.1.2.0 exceeds 3k znaków or §4.1.2.1
exceeds 6k znaków (excluding table rows), STOP and report to parent session. If
any numerical claim cannot be grounded in the T01 crosswalk, insert `[REVIEW:
ungrounded number — X]` and continue, but flag count in T08 handoff.

---

### T05 — Draft §4.1.2.2 aoe2companion subsection

**Objective:** Describe the aoe2companion corpus with the same depth pattern,
explicitly highlighting the differences from aoestats (player-row-oriented
schema, larger raw scale, different rating column semantics).

**Subsection breakdown:**

#### §4.1.2.2.a — Cytowanie i pozyskanie:
- "aoe2companion — projekt mobilnej aplikacji towarzyszącej z dedykowanym
  REST API udostępniającym pełne historie meczowe per-gracza [AoeCompanion]."
- Pliki: 2073 daily Parquet files w `matches/` (6621,52 MB) + 2072 daily
  CSV files w `ratings/` (2519,59 MB) + 1 snapshot `leaderboards/leaderboard.parquet`
  (83,32 MB) + 1 snapshot `profiles/profile.parquet` (161,84 MB)
  (`01_01_01_file_inventory.md`).
- Pokrycie czasowe: matches 2020-08-01 do 2026-04-04 (2073 dni, brak luk);
  ratings 2020-08-01 do 2026-04-04 (1 mała luka 2025-07-10 → 2025-07-12).
  Argumentacja: "Codzienne migawki dziennej granulacji w aoec stoją w
  kontraście z tygodniowymi migawkami w aoestats — głębsze pokrycie
  temporalne kosztem zwiększonej redundancji; szczegóły deduplikacji w
  cleaning rules w §4.2."

**§4.1.2.2.b — Schemat analityczny:**
- `matches_long_raw`: lossless projection (277 099 059 wierszy =
  matches_raw row count, 74 788 989 distinct matchIds).
- `matches_1v1_clean`: 48 kolumn × 61 062 392 wierszy = 30 531 196 meczów
  (POKAZAĆ: 2 wiersze na mecz — player-row-oriented, w przeciwieństwie do
  aoestats 1-row-per-match). Kolumny obejmują 5 kategorii prowenancji
  per niezmiennik I3.
- `player_history_all`: 19 kolumn × 264 132 745 wierszy (wszystkie game
  types, dla feature scope).
- **WAŻNE — kontrast z aoestats:** "Decyzja o player-row-oriented schemacie
  w `matches_1v1_clean` aoec — w przeciwieństwie do 1-row-per-match w
  aoestats — wynika z formatu źródłowego (REST API per-player). Zaletą
  jest brak konieczności rozplatania `p0_*`/`p1_*` dla cech indywidualnych;
  wadą — podwojona objętość i konieczność JOIN w obliczaniu cech meczu
  (w aoestats — naturalne SELECT na jednym wierszu, w aoec — JOIN na
  matchId)."

**§4.1.2.2.c — Jakość danych:**
- **Rating distribution:** rating ELO entering match, 26,20% NULL w scope
  matches_1v1_clean = 15 999 234 wierszy (`01_04_01_missingness_ledger.csv`
  row 'rating'). DS-AOEC-04: RETAIN + `rating_was_null` BOOLEAN flag (sklearn
  MissingIndicator pattern). Argumentacja: "Wysoki rate (26,20%) jest cechą
  populacji aoec — obejmuje wszystkie ranked-1v1 leaderboardy
  (internalLeaderboardId IN (6, 18)), w tym mecze sejmowe, w których
  wartość rating jest jeszcze nieprzyznana albo nieznana. Decyzja FLAG_FOR_
  IMPUTATION zamiast DROP_COLUMN wynika z primary-feature exception per
  Rule S4 ([vanBuuren2018]); rating jest cechą predykcyjną pierwszego
  rzędu i jego usunięcie skutkowałoby utratą ~74% zachowanego sygnału na
  rzecz uniknięcia 26% missingness."
- **Country:** 2,25% NULL w scope matches_1v1_clean (DS-AOEC-05); 8,30%
  NULL w player_history_all (przekracza próg <5% MCAR); decyzja
  per-VIEW odroczona do Phase 02.
- **Game settings missingness:** server 97,39% NULL (MNAR — DROP per Rule
  S4); scenario, modDataset 100% NULL (DROP); password 77,57% NULL (DROP
  via 40–80% MAR-non-primary path); antiquityMode 60,06% NULL (DROP via
  schema-evolution interpretation); hideCivs 37,18% NULL (FLAG_FOR_
  IMPUTATION); pełen ledger w `01_04_01_missingness_ledger.csv`.
- **NULL-cluster era boundary:** 10 game-settings columns (allowCheats,
  lockSpeed, lockTeams, recordGame, sharedExploration, teamPositions,
  teamTogether, turboMode, fullTechTree, population) NULL jednocześnie w
  <0,02% wierszy (`is_null_cluster=TRUE` flag). Spans entire date range,
  informational only.
- **Won target:** 0 NULLs w `matches_1v1_clean` przez R03 complementarity
  (każdy mecz ma dokładnie jeden TRUE i jeden FALSE won wiersz); 19 251
  NULLs (0,0073%) w `player_history_all` z unranked/unknown leaderboards
  (DS-AOEC-07 EXCLUDE_TARGET_NULL_ROWS, fizyczne wykluczenie odroczone do
  Phase 02 per Rule S2).
- **profileId precision:** all profileId=-1 rows excluded upstream (R02 /
  R00); zero NULLs after.
- **Team encoding artifact:** aoec używa team=1 i team=2 jako 1v1 stron, nie
  team=0 i team=1 (`01_04_00_source_normalization.md`). 449 wierszy w side=0
  vs 130 369 073 w side=1 w mapowaniu team IN (0,1) → side; pozostałe
  wiersze mają team_id 2-12 lub NULL. Argumentacja: "Konwersja team→side
  w warstwie `matches_long_raw` traktuje team=1 i team=2 jako 1v1 strony
  za pomocą CASE WHEN; szczegóły w schema YAML."

**§4.1.2.2.d — Asymetrie i ograniczenia:**
- AI players excluded: 12 947 078 wierszy z status='ai' i profileId=-1
  (4 150 733 mecze z udziałem AI) wykluczone w R00 — zgodnie z
  `01_03_02_true_1v1_profile.md`. To samo zjawisko w aoestats — AI
  partycypanci mają NULL profile_id i są filtrowani naturalnie.
- Większy raw scale (264M wierszy player_history vs 107M dla aoestats)
  oznacza wyższe wymagania pamięciowe; wszystkie zapytania za pośrednictwem
  DuckDB z spill-to-disk.
- Brak in-game state (już omówione w §4.1.2.0).

**CONSORT Tabela 4.3 — Przepływ danych aoe2companion**:

| Etap | Mecze | Wiersze gracz×mecz |
|---|---|---|
| Surowe pliki Parquet (acquisition) | n/a | n/a |
| `matches_raw` po ingestion | 74 788 989 distinct matchIds | 277 099 059 |
| Po R00 status='player' filter (-12 947 078 ai rows) | 70 638 256 | 264 151 981 |
| Po R02 profileId != -1 filter (-19 232 parse-failed-player rows) | 70 629 263 | 264 132 745 |
| `matches_long_raw` (canonical projection) | 70 629 263 | 264 132 745 |
| Po internalLeaderboardId IN (6, 18) (rm_1v1 + analog) filter | ~30,5M | ~61M |
| Po deduplikacji (matchId, profileId) ORDER BY started | ~30,5M | ~61M |
| Po R03 1v1 complementarity HAVING COUNT(*)=2 z TRUE+FALSE won | 30 531 196 | 61 062 392 |
| **`matches_1v1_clean` (cel predykcji, 2 wiersze na mecz)** | **30 531 196** | **61 062 392** |
| `player_history_all` (źródło historii, all leaderboardy) | n/a | 264 132 745 |

Caption: "Tabela 4.3. CONSORT-style przepływ danych aoe2companion. Uwaga
strukturalna: aoe2companion utrzymuje player-row-oriented schemat (2
wiersze na mecz w `matches_1v1_clean`), w przeciwieństwie do aoestats
(1-row-per-match z `p0_*`/`p1_*` kolumnami)."

**Voice constraint:** Drugi corpus pisany jako kontrast dla pierwszego —
unikać powtarzania ogólnych stwierdzeń o AoE2 (te w §4.1.2.0). Każda
podsekcja w aoec wskazuje konkretną różnicę vs aoestats jako
strukturalną cechę motywującą strategię dwukorpusową.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (adds §4.1.2.2 prose for
  aoe2companion)

**Read scope:**
- Crosswalk from T01 (`temp/plan_4.1_crosswalk.md`).

**Halt condition (mid-execution):** If §4.1.2.2 prose (excluding table rows)
exceeds 6k znaków, STOP and report to parent session. If any numerical claim
cannot be grounded in the T01 crosswalk, insert `[REVIEW: ungrounded number
— X]` and continue, but flag count in T08 handoff.

---

### T06 — Draft §4.1.2 closing forward-reference paragraph (1k–2k znaków)

**Objective:** Draft the §4.1.2 closing forward-reference paragraph (1k–2k
znaków) that bridges to §4.1.3 (cross-dataset asymmetry section). Do NOT
include any asymmetry tables here — those live in §4.1.3.

**Prose content (single paragraph):**
Closing paragraph of §4.1.2 that reads approximately: "Pełna macierz
asymetrii informacyjnej między korpusem SC2EGSet a oboma korpusami AoE2 —
wraz z tablicami 4.4a (skala i akwizycja) oraz 4.4b (asymetria analityczna)
— przedstawiona jest w §4.1.3."

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (adds §4.1.2 closing paragraph
  of 1k–2k znaków)

**Read scope:**
- Crosswalk from T01 (`temp/plan_4.1_crosswalk.md`).

**Halt condition (mid-execution):** If the closing paragraph exceeds 2k
znaków or introduces any asymmetry table content (rows or cells from Tabela
4.4a / 4.4b), STOP and report to parent session. Do not continue to T06b.

---

### T06b — Draft §4.1.3 cross-dataset asymmetry section (4k–7k znaków)

**Objective:** Draft §4.1.3 (Data asymmetry acknowledgement) as a new section
after §4.1.2, hosting the canonical cross-dataset asymmetry tables (Tabela
4.4a + Tabela 4.4b) + argumentative prose.

**Content plan:**

**Framing paragraph (~0.8k znaków):** Why the asymmetry is split across two
tables; forward-ref to §4.1.2.0 dual-corpus motivation; backward-ref to
§4.1.1 / §4.1.2 for per-corpus details.

**Tabela 4.4a — Skala i akwizycja trzech korpusów:**

| Wymiar | SC2EGSet | aoestats | aoe2companion |
|---|---|---|---|
| Gra | StarCraft II | Age of Empires II DE | Age of Empires II DE |
| Źródło danych | Pliki `.SC2Replay` (Bialecki2023) | API agregator aoestats.io | REST API aoe2companion |
| Surowy rozmiar | 214 GB | 3,77 GB | 9,39 GB |
| Liczba plików (acquisition) | 22 390 plików `.SC2Replay.json` | 172 + 171 Parquet (matches/players) | 2073 + 2072 Parquet/CSV (matches/ratings) + 2 snapshoty |
| Pokrycie czasowe (zakres) | ~2016–2024 (turniejowy, nieciągły) | 2022-08-28 — 2026-02-07 (3 luki) | 2020-08-01 — 2026-04-04 (brak luk) |
| Granulacja archiwum | 70 katalogów turniejowych | tygodniowa | dzienna |
| Populacja | Zawodowa turniejowa | Ladder rankingowy | Ladder rankingowy |

Caption: "Tabela 4.4a. Skala i akwizycja trzech korpusów. Liczby pochodzą z
`01_01_01_file_inventory.md` w odpowiednich katalogach
reports/artifacts/01_exploration/01_acquisition/."

**Argumentative prose between tables (~1.5k znaków):** Commentary on the
structural asymmetry between SC2EGSet (event streams) and AoE2 corpora
(aggregated statistics only); the consequence for the common pre-game feature
set strategy (§4.3.1); note on AoE2 intra-corpus asymmetry (1-row vs 2-row,
3-column vs 1-column rating schema, sentinel vs 26,20% NULL missingness).

**Tabela 4.4b — Asymetria analityczna trzech korpusów po wstępnym czyszczeniu:**

| Wymiar | SC2EGSet | aoestats | aoe2companion |
|---|---|---|---|
| Liczba meczów (post-cleaning) | 22 209 (true 1v1 decisive) | 17 814 947 (1v1 ranked) | 30 531 196 (1v1 ranked) |
| Wiersze per mecz w `*_clean` | 2 (player-row) | 1 (p0_/p1_ kolumny) | 2 (player-row) |
| Liczba kolumn `matches_*_clean` | 28 | 20 | 48 |
| Liczba kolumn `player_history_all` | 37 | 14 | 19 |
| Wiersze `player_history_all` | 44 817 | 107 626 399 | 264 132 745 |
| Strumienie zdarzeń in-game | 3 (tracker 62M, game 608M, message 52K) | brak | brak |
| Cechy in-game w `*_clean` | brak (I3 wykluczone do Phase 02) | brak (I3 wykluczone) | brak (I3 wykluczone) |
| Asymetria stron (winning slot pct) | side=0: 51,96% | team=1: 52,27% | n/a (player-row) |
| Kolumna(y) ratingu | MMR (DROPPED, 83,95% sentinel) → flaga is_mmr_missing | p0/p1_old_rating + avg_elo (3 kolumny) | rating (1 kolumna) |
| Rating availability | 16,05% rated | ~99,97% rated (avg_elo) | ~73,80% rated (rating non-NULL) |
| Mechanizm dominującej missingness | MNAR (MMR=0 unrated prof.) | MAR / MCAR (low rates) | MAR (game settings drift) |
| Schema-evolution kolumny wykluczone | gd_mapSize=0 (273 wierszy) | opening + 3× age_uptime (po 2024-03-10) | 10-kolumnowy NULL-cluster (era boundary) |
| Kanoniczny identyfikator gracza | toon_id (Battle.net) | profile_id (BIGINT) | profileId (INTEGER) |

Caption: "Tabela 4.4b. Asymetria analityczna trzech korpusów po wstępnym
czyszczeniu Phase 01 / Pipeline Section 01_04. Liczby pochodzą z
`01_04_01_data_cleaning.md`, `01_04_01_missingness_ledger.csv`,
`01_04_02_post_cleaning_validation.md` oraz schemas/views/*.yaml."

**Closing paragraph with forward references (~0.8k znaków):** Forward
references to §4.2 / §4.3.1 / §4.3.2 / §4.3.3 / §4.4.1 / §4.4.4 / §6.5.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (adds §4.1.3 prose 4k–7k
  znaków + Tabela 4.4a + Tabela 4.4b)

**Read scope:**
- Crosswalk from T01 (`temp/plan_4.1_crosswalk.md`).

**Halt condition (mid-execution):** If §4.1.3 prose (excluding table rows)
exceeds 7k znaków before the closing paragraph, STOP and report to parent
session. If Tabela 4.4a or 4.4b cannot be fully grounded in `temp/plan_4.1_crosswalk.md`
(i.e., any cell value has no artifact pointer), insert `[REVIEW: ungrounded
cell — verify in T01 crosswalk]` and continue, but flag in T08 handoff.

---

### T07 — Run Critical Review Checklist (Data variant), update WRITING_STATUS.md, update REVIEW_QUEUE.md

**Objective:** Apply the 6-point Critical Review Checklist (Data variant) per
`.claude/rules/thesis-writing.md`, update `WRITING_STATUS.md` to reflect
DRAFTED status for §4.1.1, §4.1.2, and §4.1.3, and append Pending entries
to `thesis/chapters/REVIEW_QUEUE.md`.

**Instructions:**
1. **Numerical consistency check.** Re-walk every number in the §4.1.1 /
   §4.1.2 / §4.1.3 prose against the persisted T01 crosswalk
   (`temp/plan_4.1_crosswalk.md` per Fix 9). For each number:
   - Apply the **number-format normalization rule** (per T01 step 6): strip
     `,` `' '` and `\u00A0` from both prose and artifact forms; convert Polish
     decimal `,` → `.` for decimals; compare on the resulting integer/float.
   - Verify the normalized prose value equals the normalized artifact value
     exactly for absolute counts.
   - Verify it matches within ±1 row tolerance for ledger-derived counts (per
     the I7 convention used in 01_04_02 plans).
   - Insert `[REVIEW: numerical mismatch — claimed X, artifact Y]` for any
     mismatch and continue (do not silently fix; the adversarial cycle will
     resolve).
2. **Claim-evidence alignment check.** For each substantive claim:
   - Hedge with "na podstawie X stwierdzono", "zaobserwowano", "zgodnie z
     findingiem 01_NN_NN" when the artifact is suggestive but not
     conclusive
   - Use direct attribution ("MMR jest niedostępne dla 83,95% wierszy")
     only when the artifact unambiguously establishes the claim
3. **Derivation traceability check.** Every threshold cited in prose
   (>80% for DROP, <5% for MCAR retain, 40–80% MAR, 10pp side asymmetry
   alert) must include a citation to the source paper or to the
   `temp/null_handling_recommendations.md` document that codifies them.
4. **Statistical interpretation check.** No effect-size claims yet (no
   experiments). Where Phase 01 reports correlations (e.g., elo_diff
   skewness vs winning team in `01_02_06`), report the magnitude alongside
   the direction; do NOT call it "significant" without a test.
5. **Scope honesty check.** The professional-only nature of SC2EGSet is
   restated in §4.1.1.5 with a forward reference to §6.5. The
   ranked-only-1v1 nature of both AoE2 corpora is restated in §4.1.2.1.d
   and §4.1.2.2.d with the same forward reference.
6. **Missing context flags check.** Insert `[REVIEW: ...]` flags for:
   - Field-norm divergences (e.g., "Aligulac reportuje ~80% accuracy"
     dziedziczone z §2.5.4)
   - Numbers that need 01_05 / 01_06 artifacts (per-tournament breakdown,
     full duration distribution, exact patch count)
   - Bibtex-key existence checks (Rubin1976, vanBuuren2018, SchaferGraham2002
     — confirm these are in `references.bib`; if not, T07 adds the entries
     in the same edit pass)

7. **Update `thesis/WRITING_STATUS.md`:**
   - §4.1.1 SC2EGSet description: BLOCKED → DRAFTED with note: "Drafted
     2026-04-17. ~Y tys. znaków polskich. N [REVIEW] flags. Phase 01
     sections 01_01–01_04 fully cited; sections 01_05 (Temporal & Panel
     EDA), 01_06 (Decision Gates) deferred — flagged where claims await
     them."
   - §4.1.2 AoE2 datasets: BLOCKED → DRAFTED with same template.
   - §4.1.3 (Data asymmetry acknowledgement): BLOCKED → DRAFTED with note:
     "Drafted 2026-04-17. ~Z tys. znaków polskich. M [REVIEW] flags. Hosts
     canonical Tabela 4.4a (Skala i akwizycja) + Tabela 4.4b (Asymetria
     analityczna)."

8. **Append to `thesis/chapters/REVIEW_QUEUE.md`:**
   - One Pending entry per section (§4.1.1, §4.1.2, and §4.1.3) with:
     - Section path
     - Drafted date (2026-04-17)
     - Pass 1 status (DRAFTED)
     - Total flag count (N [REVIEW], 0 [NEEDS CITATION] expected for data
       sections, 0 [UNVERIFIED], 0 [NEEDS JUSTIFICATION])
     - Required Pass 2 actions (numerical re-check against any new 01_05/
       01_06 artifacts produced after this draft; bibtex-key reconciliation
       for Rubin1976 / vanBuuren2018 / SchaferGraham2002 if added in this
       draft)

**Verification:**
- WRITING_STATUS.md shows `§4.1.1 SC2EGSet description: DRAFTED`,
  `§4.1.2 AoE2 datasets: DRAFTED`, and `§4.1.3 Data asymmetry: DRAFTED`
  with notes matching the format used in Sprint 7 entries.
- REVIEW_QUEUE.md has three new Pending entries dated 2026-04-17.
- All numbers in the section prose appear in the T01 crosswalk
  (`temp/plan_4.1_crosswalk.md`).
- All `[REVIEW]` flags have a specific concern, not a generic "verify".
- Total characters for §4.1.1 are within the 15–22k Polish range;
  §4.1.2 within 18–28k; §4.1.3 within 4–7k; total §4.1 within 40–55k.

**File scope:**
- `thesis/chapters/04_data_and_methodology.md` (final integration pass; no
  new prose, only flag insertion + cross-reference verification)
- `thesis/WRITING_STATUS.md` (update §4.1.1 and §4.1.2 status rows)
- `thesis/chapters/REVIEW_QUEUE.md` (append three Pending entries — §4.1.1, §4.1.2, §4.1.3)
- `thesis/references.bib` (append Rubin1976, vanBuuren2018, SchaferGraham2002
  IF AND ONLY IF these are not already present after the executor's existence
  check; the existence check is part of T07 step 6)

**Read scope:**
- All files written in T02–T06b.

---

### T08 — Produce Chat Handoff Summary

**Objective:** Produce the Chat Handoff Summary per `.claude/rules/thesis-writing.md`
Data-fed sections format. This is a chat-only output — no file writes.

**Instructions:**
1. Compose the summary covering:
   - Section paths (§4.1.1, §4.1.2, and §4.1.3 in
     `thesis/chapters/04_data_and_methodology.md`)
   - Status (DRAFTED for all three)
   - Flag counts: N [REVIEW] for §4.1.1, M [REVIEW] for §4.1.2, P [REVIEW]
     for §4.1.3; 0 [NEEDS CITATION] (data-fed sections do not need lit
     citations beyond what §2.2/§2.3/§3.2 already provide); 0 [UNVERIFIED]
   - Artifacts list (the 33+ Phase 01 artifacts read in T01)
   - Numbers verified per section, with the format
     `<number> ← <artifact_path>:<line_or_table_anchor> ✓` — at least 15
     numbers per section
   - Questions for Chat:
     - (Q1, Q2, Q5 LOCKED by round-1 adversarial — no Pass 2 action)
     - (Q3) Confirm SC2EGSet acquisition date proxy via research_log 2026-04-09
       or add alternative timestamp source.
     - (Q4) Confirm license (CC BY 4.0 for SC2EGSet, ToS aoe2.net for
       aoestats, ToS aoe2companion) — add to §4.1.x attribution footer?
     - (Q6) §4.1.2 prose envelope — is 21k–28k tight enough, or should the
       per-corpus caps be lowered?
   - List of `[REVIEW]` flags requiring Pass 2 attention with a short
     justification per flag

**Verification:**
- The summary is < 600 words (as per the user's plan-summary cap; not
  applicable to the in-thesis prose).
- The summary points at all `[REVIEW]` flags and at all forward references
  the draft makes (so Chat can verify the receiving sections exist and the
  forward refs are accurate).

**File scope:** None.

**Read scope:**
- `thesis/chapters/04_data_and_methodology.md` (final state after T07)

---

## File Manifest

| File | Action |
|------|--------|
| `thesis/chapters/04_data_and_methodology.md` | Update — replace §4.1.1 and §4.1.2 skeleton lines with full prose (T02–T06); add §4.1.2 closing bridge paragraph (T06); add §4.1.3 with Tabela 4.4a (Skala i akwizycja) + Tabela 4.4b (Asymetria analityczna) (T06b) |
| `temp/plan_4.1_crosswalk.md` | Write — structured Markdown crosswalk table produced in T01 step 6/7 |
| `thesis/WRITING_STATUS.md` | Update — flip §4.1.1, §4.1.2, and §4.1.3 rows to DRAFTED with the standard note format used in Sprint 7 entries |
| `thesis/chapters/REVIEW_QUEUE.md` | Update — append three Pending entries (§4.1.1, §4.1.2, and §4.1.3) dated 2026-04-17 |
| `thesis/references.bib` | Update — append Rubin1976, vanBuuren2018, SchaferGraham2002 entries IF AND ONLY IF they are not already present (T07 existence check); no other bib changes |

## Gate Condition

The plan executes successfully when ALL of the following hold:

- [ ] §4.1.1 prose (excluding HTML comments) is 15 000 – 22 000 znaków polskich,
  with per-subsection caps: §4.1.1 total 15k–22k; §4.1.1.1 3k–4k; §4.1.1.2 3k–4k;
  §4.1.1.3 3k–5k; §4.1.1.4 3k–5k; §4.1.1.5 2k–3k
- [ ] §4.1.2 prose (excluding HTML comments) is 21 000 – 28 000 znaków polskich,
  with per-subsection caps: §4.1.2.0 2k–3k; §4.1.2.1 8k–12k; §4.1.2.2 8k–12k;
  §4.1.2 closing paragraph 1k–2k (caps widened to reconcile arithmetic with §4.1
  total floor per round-2 adversarial fix)
- [ ] §4.1.3 prose is 4 000 – 7 000 znaków polskich (new section hosting
  Tabela 4.4a + Tabela 4.4b)
- [ ] Total §4.1 (§4.1.1 + §4.1.2 + §4.1.3) is 40 000 – 57 000 znaków polskich
  (15 + 21 + 4 = 40 floor; 22 + 28 + 7 = 57 ceiling)
- [ ] Tabela 4.1 (CONSORT przepływ SC2EGSet) is present in §4.1.1 with caption
  pointing at `01_04_01_data_cleaning.md`
- [ ] Tabela 4.2 (CONSORT przepływ aoestats) is present in §4.1.2.1 with caption
  pointing at the same artifact
- [ ] Tabela 4.3 (CONSORT przepływ aoe2companion) is present in §4.1.2.2 with
  caption pointing at the same artifact
- [ ] Tabela 4.4a (Skala i akwizycja) is present in §4.1.3, spanning all three
  corpora, with rows-as-dimensions format
- [ ] Tabela 4.4b (Asymetria analityczna) is present in §4.1.3 after Tabela 4.4a,
  spanning all three corpora, with rows-as-dimensions format
- [ ] Each subsection ends with at least one forward reference to a chapter / section
  it is preparing the reader for, or backward reference to a chapter / section it is
  not duplicating (per §2.2/§2.3 deferral commitments and per §4.2/§4.3/§4.4/§6.5
  forward-feed responsibilities)
- [ ] Every numerical claim is traceable: each number has a `<number> ← <artifact>`
  line in the T08 chat handoff summary
- [ ] Every methodological choice (e.g., DROP MMR, retain rating with flag, exclude
  997 inconsistent winners) has a "dlaczego to, a nie oczywista alternatywa?"
  sentence in the same paragraph (per author-style-brief-pl.md)
- [ ] Polish academic register: no bullet lists in body prose (tables and forward-
  reference paragraphs OK); bezosobowy ("przedstawiono", "stwierdzono"); anglicisms
  italicized on first use; `[KeyYear]` citation format throughout
- [ ] No verbatim duplication of sentences from §2.2.5 or §2.3.4 (post-Sprint 7
  trimmed versions); §4.1 IS the home for the corpus statistics, not §2.2/§2.3
- [ ] All 9 scientific invariants (and especially I3 / I5 / I8 / I9 / I10) are
  consistent with the prose claims; e.g., the I3 prose statement matches the
  schema YAML provenance_categories block exactly
- [ ] WRITING_STATUS.md updated with the standard Sprint 7 note format (date,
  draft type, char count, flag count, distinct keys count not applicable for
  data-fed sections)
- [ ] REVIEW_QUEUE.md appended with three Pending entries (§4.1.1, §4.1.2, §4.1.3)
- [ ] All `[REVIEW]` flags name a specific concern with an actor/method to resolve
  (not generic "verify")
- [ ] If references.bib is modified, only Rubin1976 / vanBuuren2018 / SchaferGraham2002
  are added (or no changes if all three are present)
- [ ] Branch `docs/thesis-4.1-data-chapter` exists and the commit message references
  Phase 01 sections 01_01–01_04 closure across all three datasets, plus the
  WRITING_STATUS / REVIEW_QUEUE updates

## Out of scope

- **Per-tournament SC2EGSet breakdown** beyond the inventory-level 70 directories
  + min/max/median replays-per-tournament. A per-tournament temporal stratification
  is the substance of Step 01_05 (Temporal & Panel EDA) and is flagged for
  inclusion in §4.1.1 revision after 01_05 completes.
- **Full duration distribution analysis for SC2EGSet replays.**
  `header_elapsedGameLoops` is in `player_history_all` (37 cols) but its rozkład
  empirical (mean / median / IQR / fences) is not yet profiled in 01_03; the
  decision-driven duration threshold derivation needed for §4.2.3 (cleaning
  rules) belongs to Step 01_05 + 01_06.
- **Per-civilization win rate analysis for AoE2 corpora.** This is feature-
  engineering territory (§4.3.1) and Phase 02 / 01_05 work, not §4.1
  description. §4.1.2 references existence of the data (50 distinct civs in
  aoestats per `matches_1v1_clean.yaml` notes; 45+ in DE per §2.3) without
  computing rankings.
- **Rating distribution histograms / Elo curves.** Same as above — the rozkład
  Elo wymaga 01_05 plot artifacts and §4.3.1 feature engineering work.
- **Per-leaderboard breakdown for aoec.** internalLeaderboardId IN (6, 18) is
  the post-cleaning scope; what proportion of original matches each
  leaderboardId contributes is a 01_05 question.
- **Replay-parsing completeness for aoec / aoestats.** mgz parser feasibility
  is forward-referenced to §7.3 future work, not analysed in §4.1.
- **Cross-domain statistical comparison.** §4.4.4 (already DRAFTABLE) and §5.3
  own this. §4.1 only documents the data substrate.
- **Dataset versioning / Zenodo metadata for AoE2 corpora.** aoestats and aoec
  do not have versioned datasets — they are continuously crawled. The
  implications for reproducibility are flagged in §4.1.2.0 with a forward
  reference to §6.5; full reproducibility prose belongs to Appendix A or §6.5.
- **CC-BY 4.0 license verification for SC2EGSet.** The plan flags `[REVIEW: confirm
  license from Zenodo metadata]` rather than asserting a license without
  verification.
- **Modification of any data, schemas, queries, or notebooks.** This is a
  Category F thesis-only plan; no `src/` changes.

## Open questions

- **Q1 — §4.1.3 standalone vs merged.** LOCKED. §4.1.3 is now in-scope as a
  standalone subsection (4k–7k znaków) hosting Tabela 4.4a + Tabela 4.4b + 
  argumentative prose. T06b drafts it. The §4.1.2 closing paragraph (T06) 
  contains only a forward-reference bridge to §4.1.3, not the tables themselves.

- **Q2 — Bibtex keys for the missing-data papers.** LOCKED. T07 performs the
  `Grep` existence check on `references.bib`. If `Rubin1976`, `vanBuuren2018`,
  or `SchaferGraham2002` are absent, T07 adds them with the entries below:
  - `@article{Rubin1976, author={Rubin, D.B.}, title={Inference and missing data}, journal={Biometrika}, volume={63}, number={3}, pages={581-592}, year={1976}}`
  - `@book{vanBuuren2018, author={van Buuren, S.}, title={Flexible Imputation of Missing Data}, edition={2nd}, publisher={Chapman \& Hall/CRC}, year={2018}}`
  - `@article{SchaferGraham2002, author={Schafer, J.L. and Graham, J.W.}, title={Missing data: Our view of the state of the art}, journal={Psychological Methods}, volume={7}, number={2}, pages={147-177}, year={2002}}`

- **Q3 — Acquisition date for SC2EGSet.** Open. `01_01_01_file_inventory.md`
  does not record an acquisition date; the research log entry dated 2026-04-09
  is the proxy. Should §4.1.1.0 cite this as "data pozyskania danych w trybie
  produkcyjnym to 2026-04-09 zgodnie z research_log Phase 01 step 01_01_01"?
  Resolves by: planner default = yes, with a `[REVIEW]` flag for Pass 2
  user verification.

- **Q4 — License verification for the three corpora.** Open. SC2EGSet is on
  Zenodo with metadata-supplied license; aoestats and aoec are project websites
  with varying license clarity. Should §4.1 quote the licenses verbatim, or
  just cite the source URL with the implication that the user follows the
  source's license terms?
  Resolves by: planner default = cite source URL + flag licenses with `[REVIEW]`
  for Pass 2 verification by the user with the institutional supervisor (PJAIT
  thesis-defense considerations).

- **Q5 — Tabela 4.4a/4.4b column ordering.** LOCKED. Both tables use
  rows-as-dimensions × columns-as-corpora format (as specified in Fix 2).
  Tabela 4.4a covers scale/acquisition dimensions; Tabela 4.4b covers
  analytical asymmetry dimensions.

- **Q6 — Length envelope tolerance.** Open. §4.1.2 may exceed 25k znaków
  because it covers two corpora plus the closing bridge paragraph to §4.1.3.
  With §4.1.3 now a standalone section (4k–7k), the §4.1.2 prose envelope
  can be tighter (~20–28k); the total §4.1 envelope is 40–55k.
  Resolves by: adversarial review after drafting.

---

## Critique-required note (to parent session)

This is a **Category F plan** per `docs/templates/planner_output_contract.md`.
**Adversarial critique is required before execution begins.** The parent session
must dispatch reviewer-adversarial (Mode A — Plan Review) on this plan to produce
`temp/plan_thesis_4_1_data_chapter.critique.md` (or the analogous
`planning/current_plan.critique.md` if the user wishes to migrate the plan to the
canonical location).

Per the user's standing directive in this conversation:
- Round 1: adversarial critique → if findings, dispatch planner-science to apply
  fixes → round 2 critique → if findings, planner-science fixes → round 3 critique
  → if findings, escalate to user; otherwise execute.
- Up to 3 critique rounds before execution.
