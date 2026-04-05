# Initialize AoE2 Package Structure & Document Data Acquisition Plan

**Category:** C (Chore)
**Branch:** `chore/init-aoe2-structure` (current branch)
**Invariants in scope:** #9 (reproducibility), #10 (cross-game comparability)

---

## Objective

Two deliverables:

1. Create the AoE2 subdirectory structure mirroring the SC2 layout, per
   ARCHITECTURE.md "Adding a new game" checklist.
2. Write a data acquisition README documenting what to download from each API
   (aoestats, aoe2companion), from where, and into which directories — serving
   as the specification for a future download script.

No sample downloads. No schema profiling. No thesis paragraphs.

---

## Key Facts from Manifests (reference only)

These facts come from the two JSON manifests already on disk. They inform the
acquisition README but are not the deliverable themselves.

- **aoe2companion** (`data/aoe2companion/api/api_dump_list.json`): 2,073 daily
  match parquet files (2020-08-01 to 2026-04-04), 6.94 GB total. Also provides
  leaderboard.parquet (87 MB), profile.parquet (170 MB), rating CSVs (2,072
  files, 2.64 GB total — 1,791 files before 2025-06-27 are sparse at 63-972
  bytes each, 0.20 MB combined; 281 files from 2025-06-27 onward are
  substantive at 2.64 GB combined), and CSV duplicates of match data (43 GB,
  skip). Zero date gaps. URLs are direct CDN links in the `url` field.
- **aoestats** (`data/aoestats/api/db_dump_list.json`): 188 weekly entries
  (2022-08-28 to 2026-04-04), 172 non-zero. 30.7M matches, 108.3M player
  records. 16 zero-count entries across 4 gap ranges. URLs are relative paths
  under `https://aoestats.io`. No file sizes in manifest.
- **Primary source recommendation:** aoe2companion (longer coverage, daily
  granularity, zero gaps, known file sizes, direct URLs).

---

## Step 1 — Create directory tree

Mirror the SC2 layout. The SC2 tree (excluding data contents) is:

```
src/rts_predict/sc2/
├── __init__.py
├── cli.py
├── config.py
├── PHASE_STATUS.yaml
├── data/
│   ├── __init__.py
│   ├── README.md
│   ├── sc2egset/
│   │   ├── raw/         (gitignored contents, README tracked)
│   │   ├── staging/     (gitignored, README tracked)
│   │   │   └── in_game_events/  (.gitkeep)
│   │   ├── db/          (.gitkeep)
│   │   └── tmp/         (.gitkeep)
│   └── tests/
│       ├── __init__.py
│       └── conftest.py  (empty or minimal — no tests yet)
├── reports/
│   └── SC2_THESIS_ROADMAP.md
├── models/              (gitignored contents)
├── logs/                (gitignored)
└── tests/
    ├── __init__.py
    └── test_cli.py
```

For AoE2, create this (items marked [EXISTS] are already on disk):

```
src/rts_predict/aoe2/
├── __init__.py                          [EXISTS]
├── PHASE_STATUS.yaml                    [EXISTS]
├── config.py                            [NEW]
├── data/
│   ├── __init__.py                      [NEW]
│   ├── README.md                        [NEW — acquisition plan goes here]
│   ├── aoe2companion/
│   │   ├── api/
│   │   │   ├── api_dump_list.json       [EXISTS]
│   │   │   └── README.md               [EXISTS]
│   │   ├── raw/
│   │   │   ├── matches/                 [NEW — .gitkeep]
│   │   │   ├── leaderboards/            [NEW — .gitkeep]
│   │   │   ├── profiles/                [NEW — .gitkeep]
│   │   │   ├── ratings/                 [NEW — .gitkeep]
│   │   │   └── README.md               [NEW]
│   │   ├── db/                          [NEW — .gitkeep]
│   │   └── tmp/                         [NEW — .gitkeep]
│   ├── aoestats/
│   │   ├── api/
│   │   │   ├── db_dump_list.json        [EXISTS]
│   │   │   └── api_description_view.json [EXISTS]
│   │   ├── raw/
│   │   │   ├── matches/                 [NEW — .gitkeep]
│   │   │   ├── players/                 [NEW — .gitkeep]
│   │   │   └── README.md               [NEW]
│   │   ├── db/                          [NEW — .gitkeep]
│   │   └── tmp/                         [NEW — .gitkeep]
│   └── tests/
│       └── __init__.py                  [NEW]
├── reports/                             [NEW]
│   └── AOE2_THESIS_ROADMAP.md           [NEW — placeholder]
└── tests/
    └── __init__.py                      [NEW]
```

Note: `staging/` directories are omitted intentionally — per ARCHITECTURE.md
they are created "when extraction exists," and no extraction pipeline exists
yet. Similarly, `models/` and `logs/` are omitted until needed.

Note: aoestats provides only `matches.parquet` and `players.parquet` per weekly
dump, so its `raw/` has `matches/` and `players/` subdirs only.
aoe2companion provides matches, leaderboards, profiles, and ratings, so its
`raw/` has four subdirs.

### 1.1 — Directories to create (mkdir -p)

```bash
AOE2=src/rts_predict/aoe2

mkdir -p $AOE2/data/aoe2companion/raw/matches
mkdir -p $AOE2/data/aoe2companion/raw/leaderboards
mkdir -p $AOE2/data/aoe2companion/raw/profiles
mkdir -p $AOE2/data/aoe2companion/raw/ratings
mkdir -p $AOE2/data/aoe2companion/db
mkdir -p $AOE2/data/aoe2companion/tmp
mkdir -p $AOE2/data/aoestats/raw/matches
mkdir -p $AOE2/data/aoestats/raw/players
mkdir -p $AOE2/data/aoestats/db
mkdir -p $AOE2/data/aoestats/tmp
mkdir -p $AOE2/data/tests
mkdir -p $AOE2/reports
mkdir -p $AOE2/tests
```

### 1.2 — .gitkeep files

```bash
touch $AOE2/data/aoe2companion/raw/matches/.gitkeep
touch $AOE2/data/aoe2companion/raw/leaderboards/.gitkeep
touch $AOE2/data/aoe2companion/raw/profiles/.gitkeep
touch $AOE2/data/aoe2companion/raw/ratings/.gitkeep
touch $AOE2/data/aoe2companion/db/.gitkeep
touch $AOE2/data/aoe2companion/tmp/.gitkeep
touch $AOE2/data/aoestats/raw/matches/.gitkeep
touch $AOE2/data/aoestats/raw/players/.gitkeep
touch $AOE2/data/aoestats/db/.gitkeep
touch $AOE2/data/aoestats/tmp/.gitkeep
```

### 1.3 — __init__.py files

```bash
# data package
echo '"""AoE2 data ingestion, processing, and exploration modules."""' \
  > $AOE2/data/__init__.py

# data/tests package
touch $AOE2/data/tests/__init__.py

# tests package
touch $AOE2/tests/__init__.py
```

### 1.4 — config.py

Minimal config mirroring `sc2/config.py` structure. Only path constants and
DuckDB settings — no feature engineering constants until those exist.

```python
"""AoE2 game package configuration — paths and constants."""
from pathlib import Path

# -- Project paths --
GAME_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = GAME_DIR.parent.parent.parent
DATA_DIR: Path = GAME_DIR / "data"
REPORTS_DIR: Path = GAME_DIR / "reports"

# -- Dataset paths (two sources) --
AOE2COMPANION_DIR: Path = DATA_DIR / "aoe2companion"
AOE2COMPANION_RAW_DIR: Path = AOE2COMPANION_DIR / "raw"
AOE2COMPANION_RAW_MATCHES_DIR: Path = AOE2COMPANION_RAW_DIR / "matches"
AOE2COMPANION_RAW_LEADERBOARDS_DIR: Path = AOE2COMPANION_RAW_DIR / "leaderboards"
AOE2COMPANION_RAW_PROFILES_DIR: Path = AOE2COMPANION_RAW_DIR / "profiles"
AOE2COMPANION_RAW_RATINGS_DIR: Path = AOE2COMPANION_RAW_DIR / "ratings"
AOE2COMPANION_DB_FILE: Path = AOE2COMPANION_DIR / "db" / "db.duckdb"
AOE2COMPANION_TEMP_DIR: Path = AOE2COMPANION_DIR / "tmp"
AOE2COMPANION_MANIFEST: Path = AOE2COMPANION_DIR / "api" / "api_dump_list.json"

AOESTATS_DIR: Path = DATA_DIR / "aoestats"
AOESTATS_RAW_DIR: Path = AOESTATS_DIR / "raw"
AOESTATS_RAW_MATCHES_DIR: Path = AOESTATS_RAW_DIR / "matches"
AOESTATS_RAW_PLAYERS_DIR: Path = AOESTATS_RAW_DIR / "players"
AOESTATS_DB_FILE: Path = AOESTATS_DIR / "db" / "db.duckdb"
AOESTATS_TEMP_DIR: Path = AOESTATS_DIR / "tmp"
AOESTATS_MANIFEST: Path = AOESTATS_DIR / "api" / "db_dump_list.json"

# -- Reproducibility --
RANDOM_SEED: int = 42
```

### 1.5 — PHASE_STATUS.yaml

Already exists with `current_phase: null`. Update `roadmap` field only:

```yaml
roadmap: src/rts_predict/aoe2/reports/AOE2_THESIS_ROADMAP.md
```

### 1.6 — AOE2_THESIS_ROADMAP.md (placeholder)

Short file stating the roadmap will be created after the SC2 pipeline reaches
a sufficient phase. Reference ARCHITECTURE.md "Adding a new game" step 3.

### 1.7 — Remove the top-level .gitkeep

`src/rts_predict/aoe2/.gitkeep` was a placeholder for the empty package. Now
that real content exists, delete it.

### 1.8 — pyproject.toml entry point (DO NOT add yet)

Per ARCHITECTURE.md, a CLI entry point is required. However, there is no
`cli.py` to register. Document this as a future action item in the roadmap
placeholder. Do not add a broken entry point.

---

## Step 2 — Data acquisition README

Write `src/rts_predict/aoe2/data/README.md` documenting the acquisition plan.

Content to include:

### 2.1 — Source overview table

| Source | Manifest on disk | Granularity | Date range | Formats | Role |
|--------|-----------------|-------------|------------|---------|------|
| aoe2companion | `aoe2companion/api/api_dump_list.json` | Daily | 2020-08-01 to 2026-04-04 | Parquet, CSV | Primary |
| aoestats | `aoestats/api/db_dump_list.json` | Weekly | 2022-08-28 to 2026-04-04 | Parquet | Validation |

### 2.2 — aoe2companion: what to download

List the file types from the manifest and which ones to download vs. skip:

| File pattern | Count | Total size | Download? | Target directory |
|-------------|-------|-----------|-----------|-----------------|
| `match-{date}.parquet` | 2,073 | 6.94 GB | Yes | `aoe2companion/raw/matches/` |
| `leaderboard.parquet` | 1 | 87 MB | Yes | `aoe2companion/raw/leaderboards/` |
| `profile.parquet` | 1 | 170 MB | Yes | `aoe2companion/raw/profiles/` |
| `rating-{date}.csv` | 2,072 | 2.64 GB | Yes | `aoe2companion/raw/ratings/` |
| `match-{date}.csv` | 2,072 | 43.14 GB | No (parquet preferred) | -- |
| `leaderboard.csv` | 1 | 749 MB | No (parquet preferred) | -- |
| `profile.csv` | 1 | 663 MB | No (parquet preferred) | -- |
| test files | 3 | ~5 MB | No | -- |

URL pattern: each manifest entry has a `url` field with the full CDN URL
(e.g., `https://dump.cdn.aoe2companion.com/match-2020-08-01.parquet`).

Estimated download: ~9.8 GB for the "Yes" items (6.94 GB matches + 0.26 GB
leaderboard+profile + 2.64 GB ratings).

Format rationale: Parquet is preferred over CSV everywhere a parquet version
exists (smaller, typed columns, faster to query). Rating CSVs are acquired
because no parquet equivalent exists for this data.

Note on rating CSVs: 1,791 files before 2025-06-27 are sparse (63-972 bytes
each, 0.20 MB combined — likely header-only or near-empty). 281 files from
2025-06-27 onward are substantive (2.64 GB combined). All files are acquired
for completeness; the pre-2025 sparse files cost negligible storage and their
presence/absence itself is a useful data point during profiling.

### 2.3 — aoestats: what to download

| File pattern | Count | Total size | Download? | Target directory |
|-------------|-------|-----------|-----------|-----------------|
| `matches.parquet` (weekly) | 172 (non-zero) | Unknown (no sizes in manifest) | Deferred | `aoestats/raw/matches/` |
| `players.parquet` (weekly) | 172 (non-zero) | Unknown | Deferred | `aoestats/raw/players/` |

URL pattern: manifest provides relative paths (e.g.,
`/media/db_dumps/date_range%3D2022-08-28_2022-09-03/matches.parquet`).
Base URL: `https://aoestats.io`.

16 zero-count entries (4 gap ranges) to skip. The manifest `num_matches` field
identifies these.

Deferred because: aoe2companion is the primary source with known sizes and
longer coverage. aoestats download will be planned after aoe2companion data
is profiled in Phase 0.

### 2.4 — Download script requirements (specification, not implementation)

The future download script should:
- Read the manifest JSON to enumerate files
- Route each file to the correct `raw/` subdir based on filename pattern:
  `match-*.parquet` to `raw/matches/`, `leaderboard.parquet` to
  `raw/leaderboards/`, `profile.parquet` to `raw/profiles/`,
  `rating-*.csv` to `raw/ratings/`
- Skip entries with `num_matches == 0` (aoestats) or non-target files
  (aoe2companion CSV duplicates, test files)
- Verify checksums where available (aoestats provides `match_checksum` and
  `player_checksum`; aoe2companion provides `eTag`)
- Be idempotent: skip files already present with matching size/checksum
- Log progress and write a download manifest for reproducibility

### 2.5 — Per-source raw/ README.md

Each `raw/` directory gets a short README stating what files will land there,
the subdir layout, and where they came from:

- `aoe2companion/raw/README.md`: Documents four subdirs (`matches/` for daily
  match parquets, `leaderboards/` for leaderboard.parquet, `profiles/` for
  profile.parquet, `ratings/` for daily rating CSVs). Source: aoe2companion
  CDN. Manifest: `../api/api_dump_list.json`.
- `aoestats/raw/README.md`: Documents two subdirs (`matches/` for weekly
  matches.parquet, `players/` for weekly players.parquet). Source:
  aoestats.io. Manifest: `../api/db_dump_list.json`.

---

## Step 3 — Verification

After execution, verify:

```bash
# Directory structure exists
find src/rts_predict/aoe2 -type d | sort

# .gitkeep files in place
find src/rts_predict/aoe2 -name '.gitkeep' | sort

# __init__.py files
find src/rts_predict/aoe2 -name '__init__.py' | sort

# config.py imports cleanly
poetry run python -c "from rts_predict.aoe2.config import GAME_DIR; print(GAME_DIR)"

# No test regressions
poetry run pytest tests/ src/ -v --tb=short
```

**Executor note:** Exploratory, non-destructive commands during verification
(e.g., `python3 -c '...'` for quick import checks, `find`, `ls`) may be run
without explicit user approval. These are read-only sanity checks, not paid
API calls or data mutations.

---

## Gate Condition

All of the following are true:

1. AoE2 directory tree matches the layout in Step 1 (all [NEW] items exist),
   including object-type subdirs under each `raw/` directory.
2. `config.py` imports without error and path constants resolve correctly,
   including the new `*_RAW_MATCHES_DIR`, `*_RAW_RATINGS_DIR`, etc.
3. `data/README.md` documents what to download, from where, and into which
   subdirectory for both sources, with numbers sourced from the manifest JSONs.
   Rating CSVs are listed as "Yes" (not deferred).
4. Each `raw/` subdirectory has a `.gitkeep`.
5. Each `raw/` directory has a `README.md` describing its subdir layout.
6. `PHASE_STATUS.yaml` references the roadmap path.
7. Existing tests still pass.
