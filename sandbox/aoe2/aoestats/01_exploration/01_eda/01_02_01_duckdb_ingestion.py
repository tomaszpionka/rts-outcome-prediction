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
# # Step 01_02_01 -- DuckDB Ingestion: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoestats
# **Question:** Can we ingest all aoestats Parquet and JSON files into DuckDB,
# handling variant column types across weekly files?
# **Invariants applied:** #6 (reproducibility), #9 (step scope)
# **Step scope:** query

# %%
import json
import logging
from pathlib import Path

from rts_predict.common.notebook_utils import get_reports_dir
from rts_predict.games.aoe2.config import AOESTATS_RAW_DIR, AOESTATS_DB_FILE
from rts_predict.games.aoe2.datasets.aoestats.pre_ingestion import (
    run_variant_census,
    run_smoke_test,
    ingest_matches_raw,
    ingest_players_raw,
    ingest_overviews_raw,
    verify_tables,
    check_duration_type,
    find_missing_weeks,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# %% [markdown]
# ## 1. Pre-ingestion variant census (pyarrow)

# %%
census = run_variant_census(AOESTATS_RAW_DIR)
print(f"Matches variant columns: {list(census['matches']['variant_columns'].keys())}")
print(f"Players variant columns: {list(census['players']['variant_columns'].keys())}")

for subdir in ("matches", "players"):
    print(f"\n{subdir}:")
    for col, types in census[subdir]["variant_columns"].items():
        print(f"  {col}: {types}")

# %% [markdown]
# ## 2. Smoke test

# %%
import duckdb

con_smoke = duckdb.connect(":memory:")
smoke = run_smoke_test(con_smoke, AOESTATS_RAW_DIR)
print(f"Smoke matches: {smoke['matches']['row_count']} rows, {smoke['matches']['column_count']} cols")
print(f"Smoke players: {smoke['players']['row_count']} rows, {smoke['players']['column_count']} cols")
con_smoke.close()

# %% [markdown]
# ## 3. Full ingestion

# %%
import duckdb

AOESTATS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
if AOESTATS_DB_FILE.exists():
    AOESTATS_DB_FILE.unlink()

con = duckdb.connect(str(AOESTATS_DB_FILE))
con.execute("SET memory_limit = '24GB'")
con.execute("SET threads = 4")

m_count = ingest_matches_raw(con, AOESTATS_RAW_DIR)
print(f"matches_raw: {m_count:,} rows")

p_count = ingest_players_raw(con, AOESTATS_RAW_DIR)
print(f"players_raw: {p_count:,} rows")

o_count = ingest_overviews_raw(con, AOESTATS_RAW_DIR)
print(f"overviews_raw: {o_count:,} rows")

# %% [markdown]
# ## 4. Post-ingestion verification

# %%
variant_cols = {
    "matches_raw": ["raw_match_type", "started_timestamp"],
    "players_raw": [
        "feudal_age_uptime", "castle_age_uptime",
        "imperial_age_uptime", "profile_id", "opening",
    ],
}
verification = verify_tables(con, variant_columns=variant_cols)
for table, v in verification.items():
    print(f"\n{table}: {v['row_count']:,} rows, {v['column_count']} columns")
    if "variant_null_counts" in v:
        print(f"  Variant NULL counts: {v['variant_null_counts']}")

# %%
dur = check_duration_type(con)
for col, info in dur.items():
    print(f"{col}: typeof={info['typeof']}, note={info.get('note', '')}")
    print(f"  sample: {info.get('sample_seconds', info.get('sample_epoch_seconds', []))}")

# %%
missing = find_missing_weeks(con)
print(f"Matches weeks: {missing['matches_week_count']}")
print(f"Players weeks: {missing['players_week_count']}")
print(f"In matches not players: {missing['in_matches_not_players']}")
print(f"In players not matches: {missing['in_players_not_matches']}")

# %%
con.close()

# %% [markdown]
# ## 5. Write artifacts

# %%
artifacts_dir = (
    get_reports_dir("aoe2", "aoestats")
    / "artifacts" / "01_exploration" / "01_eda"
)
print(f"Artifacts at: {artifacts_dir}")
print("JSON and MD artifacts written by pre_ingestion pipeline.")
