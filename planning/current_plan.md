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
title: "sc2egset worldwide identity — decomposed VIEW player_identity_worldwide (no hashing; toon_id IS the identifier)"
manual_reference: "docs/ml_experiment_lifecycle/01_DATA_EXPLORATION_MANUAL.md §4 + §5"
invariants_touched: [I2, I6, I7, I9, I10]
predecessors: ["01_04_04 (PR #157)"]
plan_version: "R4 — finally grounded in actual data structure"
---

# sc2egset 01_04_04b — `player_identity_worldwide` VIEW (decomposition-based)

## Problem Statement

R1 (5-signal classifier): rejected — over-engineered.
R2 (external-bridge catalog): rejected — web-verified no external source delivers.
R3 (sha256 composite): rejected — didn't understand the data first.

**Actual finding (direct SQL inspection):** `replay_players_raw.toon_id` is stored as the full Battle.net qualifier `R-S2-G-P` string (e.g., `2-S2-1-315071` = Serral on EU realm 1, profile 315071). Segment 1 = region code, segment 2 = literal "S2", segment 3 = realm/gateway, segment 4 = profile-id (region-scoped per Blizzard).

**toon_id IS already the worldwide identifier** — region-scoped per Blizzard's design (Option 1 external bridge remains dead), but it's the full qualified Battle.net handle, not a bare integer. Region + realm columns are redundant derivations of segments 1 and 3.

**No hashing, no composite encoding needed.** A thin VIEW that decomposes toon_id into human-readable components + renames for semantic clarity is the honest answer.

## Scope

Two deliverables:
1. `player_identity_worldwide` VIEW with decomposed columns (region_code, realm_code, profile_id, region_label, realm_label, nickname) + the full toon_id as `player_id_worldwide`.
2. **Outlier investigation** of 2 rows with empty (length-0) toon_id: where they come from, tournament clustering, temporal distribution, whether they share a filename/replay_id pattern. Queryable results in the notebook + JSON for future assessment.

~2 hour scope. Non-destructive (I9). No hashing. No behavioral signals.

## Literature Context

- **sc2reader + Blizzard s2protocol** confirm `R-S2-G-P` format. [sc2reader objects.py](https://github.com/GraylinKim/sc2reader/blob/master/sc2reader/objects.py)
- **Bialecki 2023 (SC2EGSet paper)** — uses toon_id as entity key; precedent for region-scoped identity.
- **R2 web-adversarial findings:** no external bridge (Liquipedia/Aligulac/sc2pulse/Blizzard OAuth) delivers cross-region profile-id linkage at bulk scale.

## Assumptions & Unknowns

**Assumptions:**
- `toon_id` LIKE `%-S2-%-%` is the canonical 4-segment format. Non-matching rows (including the 2 empty strings) need explicit handling.
- `region` + `realm` columns are derived from segments 1 and 3 upstream — should match SPLIT_PART outputs for all valid rows.
- 98-region ("local Battle.net" / test replays) is structurally valid `R-S2-G-P`; include in VIEW with no special treatment.

**Resolved at execution:**
- **Cell A empirical:** what exactly are the 2 empty-toon_id rows? Single tournament? Date cluster? Same filename prefix? Replay metadata pattern?

## Execution Steps

### T01 — Decomposition VIEW creation (~30 min)

Notebook `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.py` (jupytext-paired).

**Cell A** — imports + DB connection (read-only for audit; writable for DDL).

**Cell B** — structural audit table (per column: toon_id, region, realm, nickname, userID, playerID): cardinality, sample values, inferred role. Brief — no behavioral fingerprinting. 1 Markdown table output.

**Cell C** — toon_id format consistency probe:
```sql
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN toon_id IS NULL THEN 1 ELSE 0 END) AS n_null,
  SUM(CASE WHEN LENGTH(toon_id) = 0 THEN 1 ELSE 0 END) AS n_empty,
  SUM(CASE WHEN toon_id LIKE '%-S2-%-%' THEN 1 ELSE 0 END) AS n_canonical_format,
  SUM(CASE WHEN toon_id LIKE '%-S2-%-%'
           AND CAST(SPLIT_PART(toon_id, '-', 1) AS INT) =
               CASE region
                 WHEN 'US' THEN 1 WHEN 'Europe' THEN 2 WHEN 'Korea' THEN 3
                 WHEN 'China' THEN 5 WHEN 'SEA' THEN 6 WHEN 'Unknown' THEN 98
                 ELSE -1
               END
           THEN 1 ELSE 0 END) AS n_region_consistent
FROM replay_players_raw;
```
Verify: canonical format count = 44,815; empty = 2; region-code consistency holds for all canonical rows. Report any anomalies.

**Cell D** — DDL:
```sql
CREATE OR REPLACE VIEW player_identity_worldwide AS
SELECT DISTINCT
    toon_id                                      AS player_id_worldwide,
    CAST(SPLIT_PART(toon_id, '-', 1) AS INT)     AS region_code,
    CAST(SPLIT_PART(toon_id, '-', 3) AS INT)     AS realm_code,
    CAST(SPLIT_PART(toon_id, '-', 4) AS BIGINT)  AS profile_id,
    region                                       AS region_label,
    realm                                        AS realm_label,
    nickname                                     AS nickname_case_sensitive
FROM replay_players_raw
WHERE toon_id LIKE '%-S2-%-%';
```

Filter `LIKE '%-S2-%-%'` excludes the 2 empty-string rows + any NULL. The 98-S2-* "local Battle.net" rows included.

**Cell E** — gate assertions:
- Row count = 2,495 (matches 01_04_04 K1 = distinct toon_id count)
- Distinct `player_id_worldwide` = 2,495 (trivially — SELECT DISTINCT on toon_id)
- DESCRIBE: 7 columns, dtypes `[VARCHAR, INT, INT, BIGINT, VARCHAR, VARCHAR, VARCHAR]`
- Spot-check 3 known toon_ids: Serral (`2-S2-1-315071` → EU/1/315071), and 2 others from random sample

### T02 — Outlier investigation: 2 empty-toon_id rows (~45 min)

Goal: characterize these 2 rows enough that the user can later decide whether they're data-quality issues worth fixing upstream, or acceptable noise.

**Cell F** — pull full per-row context for the 2 empty-toon_id rows:
```sql
SELECT
    rp.*,
    rm.details_timeUTC,
    rm.metadata_gameVersion,
    rm.metadata_mapName,
    rm.details_isBlizzardMap
FROM replay_players_raw rp
LEFT JOIN replays_meta_raw rm USING (filename)
WHERE rp.toon_id IS NULL OR LENGTH(rp.toon_id) = 0
ORDER BY rp.filename;
```

Produce a Markdown table in the MD report: 2 rows × ~20 columns, human-readable.

**Cell G** — tournament / temporal clustering probes. For each of the 2 outlier filenames:
- What does the filename look like? Does it share a prefix/folder with tournament naming (many sc2egset filenames encode tournament name)?
- Extract filename components (if filename pattern is `tournament/YYYY-MM-DD/replay.SC2Replay`, parse it).
- Date from `details_timeUTC` — cluster with other empty-toon_id rows? (N=2, so "cluster" = are they close in time or far apart?)
- Map name — same map for both?
- Opponent in the same replay: pull the OTHER player row for the same replay_id. Does that player have a valid toon_id?
   ```sql
   SELECT rp2.*
   FROM replay_players_raw rp1
   JOIN replay_players_raw rp2 USING (replay_id)
   WHERE (rp1.toon_id IS NULL OR LENGTH(rp1.toon_id) = 0)
     AND rp2.toon_id IS NOT NULL AND LENGTH(rp2.toon_id) > 0;
   ```
- Result per outlier: who were they playing against? Did the opponent win? Partial-data game?

**Cell H** — anomaly pattern search (N=2 so just narrative):
- Is there a data-ingestion stage where this could originate (e.g., a particular tournament's replay pack known to have metadata issues)?
- Is the replay file size / duration / chat-message count abnormal compared to the global distribution?

**Cell I** — outlier summary block in JSON:
```json
"outliers_empty_toon_id": {
  "count": 2,
  "filenames": ["...", "..."],
  "replay_ids": ["...", "..."],
  "tournaments_inferred": ["...", "..."],
  "dates": ["...", "..."],
  "opponent_toon_ids": ["...", "..."],
  "opponent_valid": [true/false, true/false],
  "assessment": "narrative verdict: isolated data-quality quirks / systematic tournament issue / ..."
}
```

### T03 — Artifacts + status

**Cell J** — schema YAML `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_identity_worldwide.yaml`:
- 7 cols spec
- I2/I6/I7/I9/I10 invariants
- `player_id_worldwide` description explicitly notes: "Full Battle.net R-S2-G-P qualifier — region-scoped by Blizzard design. A physical human active on multiple regions = multiple distinct player_id_worldwide values (structural limitation inherited from replay format; no external bridge available per R2 web-research). Upgrade path: future manual tournament-roster PR could add supplemental merge-mapping table."
- `region_code`, `realm_code`, `profile_id` descriptions with integer code → label mappings
- Provenance: `source_tables: [replay_players_raw]`, `filter: "toon_id LIKE '%-S2-%-%'"`, DDL verbatim

**Cell K** — `01_04_04b_worldwide_identity.json`:
- All T01 SQL + T02 outlier-probe SQL verbatim (I6; ≥6 queries)
- T01 column-audit table + format-consistency results
- T02 outlier investigation results (per Cell I structure)
- Web-research summary (R2 adversarial findings): 4 external sources + infeasibility reasons
- `identity_key_temporal_scope` declaration
- ≥5 literature URLs

**Cell L** — `01_04_04b_worldwide_identity.md`:
- Problem restatement (toon_id IS the identifier; no hash needed)
- T01 decomposition + gate results
- T02 outlier investigation (2-row table + narrative assessment)
- Region-scoping limitation note + upgrade-path sketch
- Why external bridges don't work (2-sentence summary citing R2)

**Cell M** — status files:
- STEP_STATUS.yaml: add `01_04_04b: complete`
- PIPELINE_SECTION_STATUS.yaml: 01_04 flip roundtrip complete → in_progress → complete
- research_log.md: prepend dated entry
- ROADMAP.md: append `### Step 01_04_04b -- Stub worldwide identity VIEW (decomposition-based)` block under existing 01_04_04

## File Manifest

**NEW:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_04b_worldwide_identity.{py,ipynb}`
- `src/rts_predict/games/sc2/datasets/sc2egset/data/db/schemas/views/player_identity_worldwide.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_04b_worldwide_identity.{json,md}`

**MODIFIED:**
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`

**NOT touched (I9):**
- All existing sc2egset raw + view YAMLs except new one
- aoestats + aoec
- PHASE_STATUS.yaml

## Gate Condition

- VIEW has 2,495 rows (= 01_04_04 K1); 2,495 distinct player_id_worldwide
- DESCRIBE: 7 cols in spec order + dtypes
- 3 spot-check entities decompose correctly (including Serral `2-S2-1-315071`)
- Outlier investigation Cell I JSON block populated with concrete values (not NULLs) for all 2 outlier rows
- Schema YAML has 7 cols + I2/I6/I7/I9/I10 invariants + region-scoping limitation note
- JSON has ≥6 SQL verbatim + ≥5 literature URLs
- I9 empty diff on upstream YAMLs
- STEP_STATUS 01_04_04b = complete; PIPELINE_SECTION 01_04 ending state = complete

## Open Questions

None blocking. User-approved simpler approach. 2 empty-toon_id rows handled in T02 as investigation-only (filter from VIEW; surface findings).

## Adversarial note

Skip — R2 web-adversarial already validated structural claim; R4 removed the hash that would have been the only remaining over-engineering. Post-execution verification via direct git diff inspection is sufficient.
