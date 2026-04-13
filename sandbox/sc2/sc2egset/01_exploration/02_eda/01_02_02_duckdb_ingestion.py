# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 01_02_02 -- DuckDB Ingestion: sc2egset
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** sc2egset
# **Question:** Materialise raw data into persistent DuckDB tables using the
# three-stream strategy determined by 01_02_01.
# **Invariants applied:** #6 (reproducibility), #7 (provenance), #9 (step scope)
# **Step scope:** ingest
# **Prerequisites:** 01_02_01 artifacts on disk, notebook re-executed with outputs

# %%
import json
import logging
from pathlib import Path

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir
from rts_predict.games.sc2.config import IN_GAME_PARQUET_DIR, REPLAYS_SOURCE_DIR
from rts_predict.games.sc2.datasets.sc2egset.ingestion import (
    extract_events_to_parquet,
    load_all_raw_tables,
)

logging.basicConfig(level=logging.INFO)

# %% [markdown]
# ## 1. Ingest all DuckDB tables
#
# Calls `load_all_raw_tables` which creates:
# - `replays_meta` -- one row per replay, STRUCT columns, ToonPlayerDescMap as VARCHAR
# - `replay_players` -- normalised one row per (replay, player)
# - `map_aliases` -- foreign-to-english map names with tournament provenance

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=False)
counts = load_all_raw_tables(db.con, REPLAYS_SOURCE_DIR)
print("Ingestion counts:")
for table, n in counts.items():
    print(f"  {table}: {n:,} rows")

# %% [markdown]
# ## 2. Post-ingestion validation: DESCRIBE tables

# %%
for table in counts:
    print(f"\n=== DESCRIBE {table} ===")
    desc_df = db.fetch_df(f'DESCRIBE "{table}"')
    print(desc_df.to_string(index=False))

# %% [markdown]
# ## 3. NULL rates on key fields

# %%
# replays_meta: check NULL rates for metadata STRUCT columns
null_check_query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(details) AS details_null,
    COUNT(*) - COUNT(header) AS header_null,
    COUNT(*) - COUNT(initData) AS initData_null,
    COUNT(*) - COUNT(metadata) AS metadata_null,
    COUNT(*) - COUNT(ToonPlayerDescMap) AS tpdm_null,
    COUNT(*) - COUNT(filename) AS filename_null
FROM replays_meta
"""
print("=== replays_meta NULL rates ===")
null_df = db.fetch_df(null_check_query)
print(null_df.to_string(index=False))

# %%
# replay_players: check NULL rates for key player fields
player_null_query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(toon_id) AS toon_id_null,
    COUNT(*) - COUNT(nickname) AS nickname_null,
    COUNT(*) - COUNT(MMR) AS MMR_null,
    COUNT(*) - COUNT(race) AS race_null,
    COUNT(*) - COUNT(result) AS result_null,
    COUNT(*) - COUNT(APM) AS APM_null,
    COUNT(*) - COUNT(filename) AS filename_null
FROM replay_players
"""
print("=== replay_players NULL rates ===")
player_null_df = db.fetch_df(player_null_query)
print(player_null_df.to_string(index=False))

# %%
# map_aliases: check NULL rates
alias_null_query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(tournament) AS tournament_null,
    COUNT(*) - COUNT(foreign_name) AS foreign_name_null,
    COUNT(*) - COUNT(english_name) AS english_name_null,
    COUNT(DISTINCT tournament) AS distinct_tournaments
FROM map_aliases
"""
print("=== map_aliases NULL rates ===")
alias_null_df = db.fetch_df(alias_null_query)
print(alias_null_df.to_string(index=False))

# %% [markdown]
# ## 4. ToonPlayerDescMap VARCHAR verification

# %%
# Verify ToonPlayerDescMap is stored as VARCHAR (JSON text blob)
tpdm_type_query = """
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'replays_meta' AND column_name = 'ToonPlayerDescMap'
"""
print("=== ToonPlayerDescMap type ===")
tpdm_type_df = db.fetch_df(tpdm_type_query)
print(tpdm_type_df.to_string(index=False))

# %%
db.close()

# %% [markdown]
# ## 5. Extract events to Parquet (optional -- SSD-dependent)
#
# This step extracts gameEvents, trackerEvents, messageEvents to
# zstd-compressed Parquet. If SSD space is insufficient, skip this step.

# %%
# Uncomment to run event extraction:
# event_counts = extract_events_to_parquet(
#     REPLAYS_SOURCE_DIR,
#     IN_GAME_PARQUET_DIR,
#     batch_size=100,
# )
# print("Event extraction counts:")
# for et, n in event_counts.items():
#     print(f"  {et}: {n:,} rows")

# %% [markdown]
# ## 6. Write artifacts

# %%
reports_dir = get_reports_dir("sc2", "sc2egset")
artifacts_dir = reports_dir / "artifacts" / "01_exploration" / "02_eda"
artifacts_dir.mkdir(parents=True, exist_ok=True)

artifact_data = {
    "step": "01_02_02",
    "dataset": "sc2egset",
    "tables_created": {
        table: {"row_count": n} for table, n in counts.items()
    },
}

artifact_path = artifacts_dir / "01_02_02_duckdb_ingestion.json"
artifact_path.write_text(json.dumps(artifact_data, indent=2))
print(f"Artifact written: {artifact_path}")

# %%
md_lines = [
    "# Step 01_02_02 -- DuckDB Ingestion: sc2egset\n",
    "",
    "## Tables created\n",
    "",
    "| Table | Rows |",
    "|-------|------|",
]
for table, n in counts.items():
    md_lines.append(f"| {table} | {n:,} |")
md_lines.extend([
    "",
    "## Ingestion strategy\n",
    "",
    "Three-stream extraction:",
    "- **replays_meta**: DuckDB table, one row per replay. Metadata as STRUCT columns,",
    "  ToonPlayerDescMap as VARCHAR (JSON text blob). Event arrays excluded.",
    "- **replay_players**: DuckDB table, normalised from ToonPlayerDescMap.",
    "  One row per (replay, player) with all player fields extracted.",
    "- **map_aliases**: DuckDB table, all tournament mapping files with",
    "  tournament provenance column.",
    "- **Events**: Parquet extraction (optional, SSD-dependent).",
    "",
    "## SQL used\n",
    "",
    "See `src/rts_predict/games/sc2/datasets/sc2egset/ingestion.py` for all",
    "SQL constants and extraction logic.",
])

md_path = artifacts_dir / "01_02_02_duckdb_ingestion.md"
md_path.write_text("\n".join(md_lines))
print(f"Report written: {md_path}")
