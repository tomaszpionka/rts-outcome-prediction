---
category: A
date: 2026-04-18
branch: feat/01-04-04-sc2egset-worldwide-identity
phase: "01"
pipeline_section: "01_04"
step: "01_04_04b"
parent_step: "01_04_04"
dataset: sc2egset
game: sc2
title: "sc2egset worldwide identity — internal primary-key audit + external-linkage catalog"
manual_reference: "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md §4 + §5"
invariants_touched: [I2, I6, I7, I9]
predecessors: ["01_04_04 (PR #157)"]
plan_version: "R2 — reframed after user reject of 5-signal behavioral classifier"
---

# sc2egset 01_04_04b — Cross-region player identity: internal audit + external-linkage catalog

## Problem Statement

PR #157 surfaced the problem; R1 plan over-engineered the solution (5-signal Fellegi-Sunter behavioral classifier). Web research established the actual structural constraint:

**`.SC2Replay` files only carry region-scoped `toon_id = R-S2-G-P`. The profile-id segment `P` is NOT globally unique across regions** — Blizzard deliberately silos region namespaces. Battle.net INTERNALLY links accounts via `battletag` (`Name#1234`), but battletag is NOT exposed in replay data. **No single column in any sc2egset raw table provides a globally-unique player identifier — by design, not by cleaning oversight.**

Therefore cross-region linkage is fundamentally an **external-data problem**, not an internal data-processing problem. Candidate external sources (Liquipedia pro-player pages, Aligulac, sc2pulse, tournament rosters) expose the battletag ↔ (region, profile-id) mappings that Blizzard's replay format omits.

This plan:
1. Empirically confirms no internal column offers cross-region uniqueness (audit).
2. Catalogs external sources that could provide the bridge (web-research-backed).
3. Routes a decision — three options, not a single recommendation: full external integration, accept-as-limitation, or stub composite.

Explicitly **NOT** a behavioral classifier. APM-JSD / race-preference / clanTag fingerprinting is rejected as over-engineering for a structural gap.

## Scope

sc2egset only. ~1 notebook-day of work, not ~1 notebook-week. No VIEW creation, no new Python module, no behavioral fingerprinting. Pure structural audit + external-source documentation.

**Hard constraints (user directives):**
- Case-sensitive `nickname` throughout.
- NO APM / behavioral fingerprint work. If an external source proves unavailable, accept the limitation and document — do not invent an internal workaround.
- Web research must be verifiable — every external-source claim cited with URL; adversarial verifies via WebFetch.

## Literature Context

- **Bialecki et al. (2023)** — SC2EGSet paper. Did NOT propose cross-region linkage; treated toon_id as the entity key. Our Phase 01.04 acceptance-as-limitation option inherits this precedent.
- **Liquipedia StarCraft II Pro Players database** — community-maintained per-player pages typically listing all known accounts across regions. Primary external-linkage candidate.
- **Aligulac** ([aligulac.com](https://aligulac.com/)) — SC2 tournament rating database with unified player records across tournaments. Secondary candidate.
- **sc2pulse** ([sc2pulse.nephest.com](https://sc2pulse.nephest.com/)) — ladder-focused cross-region aggregator. Tertiary (tournament coverage less complete).
- **Blizzard Community APIs** — Battle.net profile endpoints; require OAuth, per-region profile-id retrieval; useful for battletag → profile-id if we have battletags.

## Assumptions & Unknowns

**Assumptions:**
- Raw `replay_players_raw.toon_id` is stored as the full `R-S2-G-P` string (needs confirmation in Task A1 — could be just profile-id segment).
- SC2EGSet coverage = competitive tournament replays 2016–2022 per Bialecki 2023. Pro-player population is the ~100-300 active tournament competitors; Liquipedia covers most of them.
- External sources have stable URLs + parseable content (WebFetch-accessible).

**Unknowns resolved by execution:**
- **U1:** Does sc2egset's stored `toon_id` include the region-prefix (`R-S2-G-P`) or just the profile-id segment (`P`)? Determines whether decomposition is even possible.
- **U2:** What does the `userID` BIGINT column actually contain? 01_04_04 dismissed it with "cardinality=16, slot index" — but 16 is not a typical slot range for 1v1. Could be something else (Battle.net internal ID, replay-level slot, etc.).
- **U3:** Does sc2egset raw data carry any nested metadata (JSON in replay.details, replay.initData) that exposes cross-region info we haven't surfaced to columns?
- **U4:** Of the 2,495 distinct sc2egset toon_ids, how many are pro players covered by Liquipedia?
- **U5:** Is there a Liquipedia Pro-player list that can be WebFetch-scraped in bulk, or is it per-page?

## Execution Steps

### T01 — Internal primary-key audit (SQL-only, ≤ 1 hour)

Notebook: `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.py` (jupytext-paired). Read-only DuckDB.

**Cell A** — imports + connection + sanity (row counts 44,817 / 44,418 / 44,817).

**Cell B** — `toon_id` decomposition probe: SQL to parse the `R-S2-G-P` format. Split on `-` separator. Report distinct region-codes observed, distinct realm-codes, distinct profile-ids. Confirm (or falsify) that profile-id alone repeats across regions (= same P on different R for distinct observed rows). If toon_id is just the profile-id segment (not the full R-S2-G-P string), report and stop the decomposition logic. Verbatim SQL in JSON.

**Cell C** — `userID` forensics. Actual cardinality + distribution + per-value row count. Does `userID` correlate with nickname? With toon_id? With replay_id? Is it a stable-per-player number or a per-replay slot? Answer U2 empirically.

**Cell D** — Nested metadata probe. Inspect `replays_meta_raw` + any raw JSON/STRUCT columns in `replay_players_raw` for hidden identity fields (`bnet_url`, `battletag`, `clan_name`, any account hash). If found, check cross-region uniqueness.

**Cell E** — Conclusion: enumerate every identity-capable column; per column, report (cardinality, cross-region stability verdict, primary-key candidacy). Expected outcome: all columns region-scoped or per-replay. One-table summary for the MD report.

### T02 — External-source catalog (web-research, ≤ 2 hours)

**Cell F** — For each of 4 external candidates (Liquipedia, Aligulac, sc2pulse, Blizzard OAuth API), WebFetch 1–2 sample pages to confirm:
- URL patterns (e.g., Liquipedia `https://liquipedia.net/starcraft2/<PlayerName>` — per-player pages)
- Available identity fields (battletag, all-regions account list, handle aliases)
- Coverage estimate (do sample sc2egset nicknames resolve to pages?) — test with 5 known pro nicknames from the 01_04_04 top-overlap list (Serral, Reynor, Maru, etc.)
- Licensing (Creative Commons? API TOS? scraping allowed?)
- Bulk-access feasibility (category list, dump, API endpoint?)
- Integration effort: High (requires scraping + OAuth + rate limiting), Medium (scraping + HTML parsing), Low (single CSV dump)

Output: **4-row comparison table** in MD + JSON — columns `source, url, fields_available, coverage_on_sc2egset, license, bulk_access, integration_effort, verdict`.

**Cell G** — Nickname overlap probe: take the 246 cross-region nicknames from `01_04_04_cross_region_nicknames.csv`, sample 10, WebFetch Liquipedia pages for each, report hit rate (page exists vs 404). Quantifies U4.

### T03 — Decision routing

**Cell H** — Three routing options written explicitly with criteria:

- **Option 1 — External integration (Liquipedia or Aligulac scrape).** If Task B shows ≥ 50% Liquipedia hit-rate on sc2egset nicknames AND license permits scraping → route to follow-up PR `feat/01-04-05-external-identity-bridge` with scraping + battletag-keyed composite identity.
- **Option 2 — Accept-as-limitation.** If external sources are inadequate OR effort exceeds thesis budget → accept `(region, realm, toon_id)` as entity, document multi-region-split bias in Chapter 4 §4.2.2 as a dataset limitation. Precedent: Bialecki 2023 did the same.
- **Option 3 — Stub composite now + upgrade path.** `player_id_worldwide = sha256("sc2egset|"+region+"|"+realm+"|"+toon_id)[:16]` as a stable placeholder. Phase 02 uses it as primary key with documented caveat. If external bridge later proves feasible, `player_id_worldwide` gets a supplemental mapping table without breaking downstream code.

**Cell I** — Planner recommendation + user decision point. Planner defaults to **Option 3** (stub composite) because:
- It's the minimum-scope deliverable that doesn't lose information.
- Downstream Phase 02 code has a stable key to join on (no regression from current state).
- External-bridge upgrade in Option 1 is a deterministic future PR, not a dependency on this PR.
- Thesis defensibility: we CAN acknowledge the limitation AND ship a working key.

User can override to Option 1 (external scrape now) or Option 2 (pure limitation) before T04.

### T04 — Deliverables + status

**Cell J** — JSON artifact `01_04_04b_worldwide_identity.json` with:
- T01 SQL queries verbatim (≥ 4: toon_id_decomposition, userid_forensics, nested_metadata_probe, column_summary)
- T01 findings: per-column cross-region verdict
- T02 external-source comparison (4-row table) + WebFetch sample snippets (with URLs)
- T03 decision rubric + chosen option + rationale
- `identity_key_temporal_scope` declaration (identity is offline cleaning artifact; Phase 02 filters per-time-T features independently)
- `literature` citations (Bialecki 2023, Blizzard s2protocol, Liquipedia, Aligulac, sc2pulse — at least 5 URLs)

**Cell K** — MD report `01_04_04b_worldwide_identity.md`:
- 1-paragraph problem restatement
- T01 audit findings (table: column × cross-region-stability × primary-key-candidacy)
- T02 external-source catalog (4-row table with web-verified data)
- T03 decision + rationale
- Follow-up PR sketch if Option 1 or 3 chosen

**Cell L** — Sub-case-dependent artifacts:
- **If Option 3 chosen (default):** create a tiny canonical VIEW `player_identity_worldwide` over `(region, realm, toon_id) → sha256-composite-id`. 1 column added vs existing 4. Schema YAML `player_identity_worldwide.yaml` with I2/I6/I7/I9/I10 invariants; provenance note that this is a stub pending Option 1 upgrade.
- **If Option 1 chosen:** emit `pending_external_integration.md` artifact; no VIEW; follow-up PR scope listed.
- **If Option 2 chosen:** no VIEW; `accepted_limitation.md` artifact with thesis-chapter text.

**Cell M** — Status + research_log:
- STEP_STATUS add `01_04_04b: complete`
- PIPELINE_SECTION_STATUS 01_04 roundtrip complete → in_progress → complete (Option 3 only)
- research_log prepend dated entry with findings + chosen option
- ROADMAP.md append sub-step block under Step 01_04_04

## File Manifest

**NEW:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.{py,ipynb}`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_04b_worldwide_identity.{json,md}`
- **(Option 3 only)** `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_identity_worldwide.yaml`
- **(Option 1 only)** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/pending_external_integration.md`
- **(Option 2 only)** `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/accepted_limitation.md`

**MODIFIED:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` (append 01_04_04b sub-step)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml` (add 01_04_04b)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml` (Option 3: flip-then-flip-back; Option 1/2: no change)
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md` (prepend)

**NOT touched (I9):**
- All sc2egset raw + view YAMLs (except new one in Option 3)
- aoestats + aoec files
- PHASE_STATUS.yaml

**Explicitly NOT created (rejected from R1 plan):**
- NO 5-signal classifier
- NO Union-Find module (`src/rts_predict/common/union_find.py` DELETED from scope)
- NO 7 CSVs + 5 PNGs behavioral artifacts
- NO APM-JSD / race-overlap / MMR-Jaccard / clanTag-Bayesian tables
- NO pytest test file for Union-Find (module not created)

## Gate Condition

- T01 SQL ≥ 4 queries verbatim in JSON (I6)
- T01 column-summary table in MD has row per identity-capable column with verdict
- T02 external-source table has 4 rows with non-null URL + verdict per source
- T02 nickname-Liquipedia probe: ≥ 8 of 10 sample nicknames resolved to pages (hit-rate reported)
- T03 decision explicit (Option 1 / 2 / 3 chosen + rationale)
- JSON has ≥ 5 literature citations (Bialecki + 4 external sources)
- I9 empty diff on upstream raw + view YAMLs (Option 3: new VIEW YAML exempt)
- STEP_STATUS 01_04_04b = complete; PIPELINE_SECTION 01_04 ending state = complete

## Open Questions

- **Q1:** If Option 1 selected, is Liquipedia scraping ToS-compliant for thesis use? Needs license check in T02.
- **Q2:** Is there a better external source not in our 4-candidate list? Adversarial review may surface it.
- **Q3:** Should `userID` cardinality=16 be fully explained before moving on? Yes — Cell C non-negotiable.

## Adversarial instruction

**Category A — single pre-execution adversarial round.** Reviewer-adversarial dispatched **with WebFetch** to:
1. Independently verify each external-source claim in T02 (Liquipedia URL pattern, Aligulac API, sc2pulse coverage, Blizzard OAuth feasibility).
2. Probe for unlisted candidate sources (e.g., ESL gaming DB, GosuGamers, team official sites).
3. Challenge whether the 3-option decision framework is complete or missing an obvious 4th option.
4. Verify the `toon_id` format claim (`R-S2-G-P` and `P` NOT globally unique) against authoritative docs (s2protocol repo, sc2reader source).
