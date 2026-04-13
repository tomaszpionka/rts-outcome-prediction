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
# # Step 01_02_01 -- DuckDB Ingestion: aoe2companion
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoe2companion
# **Question:** Can we ingest all aoe2companion Parquet and CSV files into
# DuckDB, handling binary column annotations and CSV type inference?
# **Invariants applied:** #6 (reproducibility), #9 (step scope)
# **Step scope:** query

# %%
import json
import logging
from pathlib import Path

from rts_predict.common.notebook_utils import get_reports_dir
from rts_predict.games.aoe2.config import (
    AOE2COMPANION_RAW_DIR,
    AOE2COMPANION_DB_FILE,
)
from rts_predict.games.aoe2.datasets.aoe2companion.pre_ingestion import (
    inspect_binary_columns,
    run_smoke_test,
    ingest_matches_raw,
    ingest_ratings_raw,
    ingest_leaderboards_raw,
    ingest_profiles_raw,
    verify_tables,
    check_ratings_types,
    count_won_nulls,
    find_date_gap,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# %% [markdown]
# ## 1. Pyarrow binary column inspection

# %%
binary_info = inspect_binary_columns(AOE2COMPANION_RAW_DIR)
for subdir, info in binary_info.items():
    print(f"{subdir}: {info['binary_column_count']} binary columns")
    for col in info["binary_columns"]:
        print(f"  {col['name']}: {col['converted_type']}")

# %% [markdown]
# ## 2. Smoke test

# %%
import duckdb

con_smoke = duckdb.connect(":memory:")
smoke = run_smoke_test(con_smoke, AOE2COMPANION_RAW_DIR)
print(f"Smoke matches: {smoke['matches']['row_count']} rows, {smoke['matches']['column_count']} cols")
print(f"Smoke ratings: {smoke['ratings']['row_count']} rows, {smoke['ratings']['column_count']} cols")
con_smoke.close()

# %% [markdown]
# ## 3. Full ingestion

# %%
import duckdb

AOE2COMPANION_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
if AOE2COMPANION_DB_FILE.exists():
    AOE2COMPANION_DB_FILE.unlink()

con = duckdb.connect(str(AOE2COMPANION_DB_FILE))
con.execute("SET memory_limit = '24GB'")
con.execute("SET threads = 4")

m = ingest_matches_raw(con, AOE2COMPANION_RAW_DIR)
print(f"matches_raw: {m:,} rows")

# %%
# ratings_raw: use explicit types (read_csv_auto fails on full 2072 files)
r = ingest_ratings_raw(con, AOE2COMPANION_RAW_DIR, use_explicit_types=True)
print(f"ratings_raw: {r:,} rows")

# %%
l = ingest_leaderboards_raw(con, AOE2COMPANION_RAW_DIR)
print(f"leaderboards_raw: {l:,} rows")

p = ingest_profiles_raw(con, AOE2COMPANION_RAW_DIR)
print(f"profiles_raw: {p:,} rows")

# %% [markdown]
# ## 4. Post-ingestion verification

# %%
v = verify_tables(con)
for table, info in v.items():
    print(f"\n{table}: {info['row_count']:,} rows, {info['column_count']} columns")

# %%
rt = check_ratings_types(con)
print("Ratings types:")
for col, typ in rt.items():
    print(f"  {col}: {typ}")

# %%
wn = count_won_nulls(con)
print(f"won column: {wn['null_count']:,} NULL / {wn['total']:,} total")

# %%
dg = find_date_gap(AOE2COMPANION_RAW_DIR)
print(f"Matches: {dg['matches_date_count']} dates")
print(f"Ratings: {dg['ratings_date_count']} dates")
print(f"In matches not ratings: {dg['in_matches_not_ratings']}")

# %%
con.close()

# %% [markdown]
# ## 5. Artifacts

# %%
artifacts_dir = (
    get_reports_dir("aoe2", "aoe2companion")
    / "artifacts" / "01_exploration" / "01_eda"
)
print(f"Artifacts at: {artifacts_dir}")
print("JSON and MD artifacts written by pre_ingestion pipeline.")
