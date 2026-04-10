---
# raw_data_readme v2 -- conforms to docs/templates/raw_data_readme_template.yaml

# -- Section A: Identity -------------------------------------------------------

game: sc2
dataset: sc2egset
raw_directory: src/rts_predict/sc2/data/sc2egset/raw/

# -- Section B: Provenance -----------------------------------------------------

source_name: "SC2EGSet -- StarCraft II Esport Replay and Game-state Dataset"
source_url: "https://zenodo.org/records/17829625"
source_type: cdn_download
source_version: "v2.1.0 (Published 2025-12-05)"
source_doi: "10.1038/s41597-023-02510-7"
data_creator: "Bialecki, A. et al."
sampling_mechanism: >
  tournament_only -- replays from publicly released esports tournaments only;
  ladder and amateur games excluded.
citation: Bialecki2023
license: CC-BY-4.0
acquisition_date: "2025-12-05"
# acquisition_date note: manual download from Zenodo; date is publication date of v2.1.0

# acquisition_script omitted -- data was downloaded manually without a script

# -- Section C: Content and Layout ---------------------------------------------

description: >
  SC2EGSet contains StarCraft II tournament replay files exported as JSON.
  Each subdirectory corresponds to one tournament and contains per-replay
  JSON files alongside a map name mapping file. Coverage spans 70 major
  esports tournaments from 2016 to 2024.
file_format: "JSON (SC2Replay export)"

subdirectory_layout:
  - directory: "2016_IEM_10_Taipei/"
    contents: "Per-replay JSON files for the IEM Season 10 Taipei tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 30
    size_mb: 188.4
  - directory: "2016_IEM_11_Shanghai/"
    contents: "Per-replay JSON files for the IEM Season 11 Shanghai tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 60
    size_mb: 337.81
  - directory: "2016_WCS_Winter/"
    contents: "Per-replay JSON files for the 2016 WCS Winter tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 465
    size_mb: 2450.07
  - directory: "2017_HomeStory_Cup_XV/"
    contents: "Per-replay JSON files for the HomeStory Cup XV tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 107
    size_mb: 922.84
  - directory: "2017_HomeStory_Cup_XVI/"
    contents: "Per-replay JSON files for the HomeStory Cup XVI tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 249
    size_mb: 2267.4
  - directory: "2017_IEM_Shanghai/"
    contents: "Per-replay JSON files for the IEM Shanghai 2017 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 81
    size_mb: 704.23
  - directory: "2017_IEM_XI_World_Championship_Katowice/"
    contents: "Per-replay JSON files for the IEM XI World Championship Katowice"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 409
    size_mb: 2238.77
  - directory: "2017_WCS_Austin/"
    contents: "Per-replay JSON files for the 2017 WCS Austin tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 399
    size_mb: 1992.3
  - directory: "2017_WCS_Global_Finals/"
    contents: "Per-replay JSON files for the 2017 WCS Global Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 45
    size_mb: 450.1
  - directory: "2017_WCS_Jonkoping/"
    contents: "Per-replay JSON files for the 2017 WCS Jonkoping tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 332
    size_mb: 2399.31
  - directory: "2017_WCS_Montreal/"
    contents: "Per-replay JSON files for the 2017 WCS Montreal tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 242
    size_mb: 1437.9
  - directory: "2017_WESG_Barcelona/"
    contents: "Per-replay JSON files for the 2017 WESG Barcelona tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 135
    size_mb: 1284.54
  - directory: "2017_WESG_Haikou/"
    contents: "Per-replay JSON files for the 2017 WESG Haikou tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 165
    size_mb: 1336.14
  - directory: "2018_Cheeseadelphia_8/"
    contents: "Per-replay JSON files for the Cheeseadelphia 8 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 64
    size_mb: 374.73
  - directory: "2018_HomeStory_Cup_XVII/"
    contents: "Per-replay JSON files for the HomeStory Cup XVII tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 343
    size_mb: 3219.66
  - directory: "2018_HomeStory_Cup_XVIII/"
    contents: "Per-replay JSON files for the HomeStory Cup XVIII tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 352
    size_mb: 2989.17
  - directory: "2018_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice 2018 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 444
    size_mb: 3995.82
  - directory: "2018_IEM_PyeongChang/"
    contents: "Per-replay JSON files for the IEM PyeongChang 2018 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 62
    size_mb: 417.73
  - directory: "2018_WCS_Austin/"
    contents: "Per-replay JSON files for the 2018 WCS Austin tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 406
    size_mb: 2491.81
  - directory: "2018_WCS_Global_Finals/"
    contents: "Per-replay JSON files for the 2018 WCS Global Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 72
    size_mb: 669.02
  - directory: "2018_WCS_Leipzig/"
    contents: "Per-replay JSON files for the 2018 WCS Leipzig tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 420
    size_mb: 2785.89
  - directory: "2018_WCS_Montreal/"
    contents: "Per-replay JSON files for the 2018 WCS Montreal tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 442
    size_mb: 2984.34
  - directory: "2018_WCS_Valencia/"
    contents: "Per-replay JSON files for the 2018 WCS Valencia tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 410
    size_mb: 3081.9
  - directory: "2018_WESG_Grand_Finals/"
    contents: "Per-replay JSON files for the 2018 WESG Grand Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 313
    size_mb: 1594.42
  - directory: "2019_Assembly_Summer/"
    contents: "Per-replay JSON files for the 2019 Assembly Summer tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 169
    size_mb: 1764.74
  - directory: "2019_HomeStory_Cup_XIX/"
    contents: "Per-replay JSON files for the HomeStory Cup XIX tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 330
    size_mb: 2705.63
  - directory: "2019_HomeStory_Cup_XX/"
    contents: "Per-replay JSON files for the HomeStory Cup XX tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 317
    size_mb: 3017.46
  - directory: "2019_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice 2019 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 440
    size_mb: 4244.61
  - directory: "2019_WCS_Fall/"
    contents: "Per-replay JSON files for the 2019 WCS Fall tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 601
    size_mb: 4330.3
  - directory: "2019_WCS_Grand_Finals/"
    contents: "Per-replay JSON files for the 2019 WCS Grand Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 111
    size_mb: 973.58
  - directory: "2019_WCS_Spring/"
    contents: "Per-replay JSON files for the 2019 WCS Spring tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 540
    size_mb: 3643.61
  - directory: "2019_WCS_Summer/"
    contents: "Per-replay JSON files for the 2019 WCS Summer tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 596
    size_mb: 4747.79
  - directory: "2019_WCS_Winter/"
    contents: "Per-replay JSON files for the 2019 WCS Winter tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 469
    size_mb: 4947.48
  - directory: "2020_05_Dreamhack_Last_Chance/"
    contents: "Per-replay JSON files for the 2020 Dreamhack Last Chance tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 84
    size_mb: 1272.49
  - directory: "2020_ASUS_ROG_Online/"
    contents: "Per-replay JSON files for the 2020 ASUS ROG Online tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 107
    size_mb: 1193.32
  - directory: "2020_Dreamhack_SC2_Masters_Fall/"
    contents: "Per-replay JSON files for the 2020 Dreamhack SC2 Masters Fall"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 799
    size_mb: 10477.05
  - directory: "2020_Dreamhack_SC2_Masters_Summer/"
    contents: "Per-replay JSON files for the 2020 Dreamhack SC2 Masters Summer"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 783
    size_mb: 10006.92
  - directory: "2020_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice 2020 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 438
    size_mb: 4062.9
  - directory: "2020_StayAtHome_Story_Cup_1/"
    contents: "Per-replay JSON files for the StayAtHome Story Cup 1 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 172
    size_mb: 2179.03
  - directory: "2020_StayAtHome_Story_Cup_2/"
    contents: "Per-replay JSON files for the StayAtHome Story Cup 2 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 237
    size_mb: 2521.89
  - directory: "2020_TSL5/"
    contents: "Per-replay JSON files for the 2020 TSL5 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 185
    size_mb: 2769.79
  - directory: "2020_TSL6/"
    contents: "Per-replay JSON files for the 2020 TSL6 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 121
    size_mb: 1272.12
  - directory: "2021_ASUS_ROG_Fall/"
    contents: "Per-replay JSON files for the 2021 ASUS ROG Fall tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 78
    size_mb: 1063.69
  - directory: "2021_Cheeseadelphia_Winter_Championship/"
    contents: "Per-replay JSON files for the Cheeseadelphia Winter Championship"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 73
    size_mb: 521.59
  - directory: "2021_Dreamhack_SC2_Masters_Fall/"
    contents: "Per-replay JSON files for the 2021 Dreamhack SC2 Masters Fall"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 786
    size_mb: 8767.36
  - directory: "2021_Dreamhack_SC2_Masters_Summer/"
    contents: "Per-replay JSON files for the 2021 Dreamhack SC2 Masters Summer"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 791
    size_mb: 8835.46
  - directory: "2021_Dreamhack_SC2_Masters_Winter/"
    contents: "Per-replay JSON files for the 2021 Dreamhack SC2 Masters Winter"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 802
    size_mb: 9062.53
  - directory: "2021_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice 2021 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 261
    size_mb: 3176.94
  - directory: "2021_StayAtHome_Story_Cup_3/"
    contents: "Per-replay JSON files for the StayAtHome Story Cup 3 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 183
    size_mb: 1810.33
  - directory: "2021_StayAtHome_Story_Cup_4/"
    contents: "Per-replay JSON files for the StayAtHome Story Cup 4 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 210
    size_mb: 2601.73
  - directory: "2021_TSL7/"
    contents: "Per-replay JSON files for the 2021 TSL7 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 132
    size_mb: 1708.3
  - directory: "2021_TSL8/"
    contents: "Per-replay JSON files for the 2021 TSL8 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 165
    size_mb: 1598.09
  - directory: "2022_03_DH_SC2_Masters_Atlanta/"
    contents: "Per-replay JSON files for the 2022 DH SC2 Masters Atlanta"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 1296
    size_mb: 11846.84
  - directory: "2022_Dreamhack_SC2_Masters_Last_Chance2021/"
    contents: "Per-replay JSON files for the 2022 Dreamhack SC2 Masters Last Chance 2021"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 355
    size_mb: 3218.55
  - directory: "2022_Dreamhack_SC2_Masters_Valencia/"
    contents: "Per-replay JSON files for the 2022 Dreamhack SC2 Masters Valencia"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 1094
    size_mb: 11714.03
  - directory: "2022_HomeStory_Cup_XXI/"
    contents: "Per-replay JSON files for the HomeStory Cup XXI tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 91
    size_mb: 1200.75
  - directory: "2022_HomeStory_Cup_XXII/"
    contents: "Per-replay JSON files for the HomeStory Cup XXII tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 285
    size_mb: 2532.57
  - directory: "2022_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice 2022 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 263
    size_mb: 3221.25
  - directory: "2022_TSL9/"
    contents: "Per-replay JSON files for the 2022 TSL9 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 181
    size_mb: 2177.43
  - directory: "2023_01_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice January 2023 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 260
    size_mb: 2742.97
  - directory: "2023_04_ESL_SC2_Masters_Summer_Finals/"
    contents: "Per-replay JSON files for the 2023 ESL SC2 Masters Summer Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 698
    size_mb: 8764.88
  - directory: "2023_05_Gamers8/"
    contents: "Per-replay JSON files for the 2023 Gamers8 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 122
    size_mb: 1530.96
  - directory: "2023_07_ESL_SC2_Masters_Winter_Finals/"
    contents: "Per-replay JSON files for the 2023 ESL SC2 Masters Winter Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 270
    size_mb: 2911.21
  - directory: "2023_HomeStory_Cup_XXIV/"
    contents: "Per-replay JSON files for the HomeStory Cup XXIV tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 167
    size_mb: 1849.28
  - directory: "2024_01_IEM_Katowice/"
    contents: "Per-replay JSON files for the IEM Katowice January 2024 tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 422
    size_mb: 4346.6
  - directory: "2024_03_ESL_SC2_Masters_Spring_Finals/"
    contents: "Per-replay JSON files for the 2024 ESL SC2 Masters Spring Finals"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 264
    size_mb: 2329.11
  - directory: "2024_05_EWC/"
    contents: "Per-replay JSON files for the 2024 EWC tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 154
    size_mb: 1781.3
  - directory: "2024_HomeStory_Cup_XXV/"
    contents: "Per-replay JSON files for the HomeStory Cup XXV tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 175
    size_mb: 1554.85
  - directory: "2024_HomeStory_Cup_XXVI/"
    contents: "Per-replay JSON files for the HomeStory Cup XXVI tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 171
    size_mb: 1676.13
  - directory: "2024_StaraZagora_BellumGensElite/"
    contents: "Per-replay JSON files for the 2024 StaraZagora BellumGensElite tournament"
    file_pattern: "<sha256_hash>.SC2Replay.json"
    file_count: 95
    size_mb: 770.87

# total_files = total_replay_files (22390) + metadata_files_total (432) + files_at_root (4)
total_files: 22826
# total_size_mb is PENDING: total_replay_bytes (224458832476) present in artifact
# but metadata file sizes were not measured in 01_01_01
total_size_mb: "PENDING: 01_01_01 fix pending"

# -- Section D: Temporal Coverage ----------------------------------------------

temporal_grain: per_game
# date_range uses year-only from tournament directory name prefixes;
# exact per-replay dates require 01_01_02 JSON parsing
date_range_start: "2016"
date_range_end: "2024"
known_gaps: []
gap_analysis_status: partial
coverage_notes: >
  Date range is year-only, derived from tournament directory name prefixes.
  Exact per-replay timestamps require 01_01_02 JSON parsing (not yet complete).
  No temporal gap analysis has been performed at the file level.
  The 2020 calendar year is present (IEM Katowice, ASUS ROG Online, etc.) despite
  COVID-19 -- the dataset includes online tournaments that ran during that period.

# -- Section E: Acquisition Filtering ------------------------------------------

# acquisition_filters: no filtering was performed; all files from Zenodo v2.1.0 downloaded.

excluded_formats:
  - format: ".SC2Replay (binary)"
    reason: >
      Binary replay files require a running StarCraft II client to parse.
      The JSON export format was chosen because it is human-readable and
      parseable without game client dependencies. SC2EGSet distributes
      JSON exports, not binary replays.

# -- Section F: Verification ---------------------------------------------------

checksum_status: none
# No file-level checksums were verified for replay JSON files.
# The map_foreign_to_english_mapping.json files were checked for
# cross-tournament consistency during Phase 01 profiling (01_01_01 notebook),
# but this is a content-consistency check, not a file-integrity checksum.

# checksum_source and checksum_verified omitted -- checksum_status is none.

# -- Section G: Immutability and Artifact Link ---------------------------------

immutability:
  status: true
  enforcement_mechanism: none_documented

inventory_artifact: "src/rts_predict/sc2/reports/sc2egset/artifacts/01_01/01_01_01_file_inventory.json"

notes: >
  Acquired by manual download from Zenodo record 17829625 (v2.1.0, published
  2025-12-05). total_size_mb is PENDING because the 01_01_01 notebook records
  per-tournament sizes for replay files only; metadata file sizes were not summed.
  total_replay_bytes (224458832476) is available in the inventory artifact and
  covers replay JSON files only.

# -- Section H: Known Limitations ----------------------------------------------

known_biases: >
  Tournament-only coverage introduces survivorship bias: only games from
  professional players who competed in events with publicly released replays
  are represented. Ladder games and amateur play are absent entirely.

representativeness_notes: >
  Top-tier professional players are over-represented relative to the broader
  StarCraft II player population. Korean players dominate pre-2022 coverage due
  to tournament geography. Coverage broadens geographically from 2022 onward
  following globalization of the esports scene.
---

# SC2EGSet -- Raw Replays

SC2EGSet v2.1.0 contains StarCraft II tournament replay files exported as JSON.
This directory holds the raw data layer and must never be modified.

**Source:** [https://zenodo.org/records/17829625](https://zenodo.org/records/17829625)
**DOI:** 10.1038/s41597-023-02510-7 (Bialecki et al., 2023)
**License:** CC-BY-4.0
**Acquisition date:** 2025-12-05 (manual download; date is Zenodo v2.1.0 publication date)

## Layout

Two-level structure: 

Each of the 70 tournament subdirectories contains:
- Per-replay JSON files named 
- A  metadata file

| Metric | Value |
|--------|-------|
| Tournament directories | 70 |
| Total replay files | 22,390 |
| Total metadata files | 432 |
| Files at root level | 4 |
| **Total files** | **22,826** |
| Total size | PENDING (01_01_01 fix pending) |

## Temporal Coverage

- **Grain:** per-game (one file per replay)
- **Date range:** 2016 to 2024 (year-only from directory names; exact dates require 01_01_02)
- **Gap analysis status:** partial -- no file-level temporal analysis completed

## Verification

No file-level checksums were verified. The 
files were checked for cross-tournament consistency during Phase 01 profiling,
but this is a content-consistency check, not a file-integrity checksum.

## Known Limitations

- Tournament-only survivorship bias; ladder and amateur games absent
- Professional players over-represented relative to the general player population
- Korean players dominate pre-2022 coverage due to tournament geography

## Inventory Artifact


