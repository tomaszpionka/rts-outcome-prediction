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
# # Step 01_02_01 -- DuckDB Pre-Ingestion: aoestats
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoestats
# **Question:** What does the raw data look like before we commit to an
# ingestion strategy? Are there variant column types across weekly files,
# type promotions, or NULL patterns we need to handle?
# **Invariants applied:** #6 (reproducibility), #9 (step scope)
# **Step scope:** query

# %%
import logging

import duckdb

from rts_predict.games.aoe2.config import AOESTATS_RAW_DIR
from rts_predict.games.aoe2.datasets.aoestats.pre_ingestion import (
    run_variant_census,
    run_smoke_test,
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
con = duckdb.connect(":memory:")
smoke = run_smoke_test(con, AOESTATS_RAW_DIR)
print(f"Smoke matches: {smoke['matches']['row_count']} rows, {smoke['matches']['column_count']} cols")
print(f"Smoke players: {smoke['players']['row_count']} rows, {smoke['players']['column_count']} cols")

# %% [markdown]
# ## 3. DESCRIBE -- column names, types, nullability

# %%
for table_name in smoke:
    print(f"\n{'='*60}")
    print(f"  DESCRIBE {table_name}")
    print(f"{'='*60}")
    files = smoke[table_name]["files_sampled"]
    full_paths = [str(AOESTATS_RAW_DIR / table_name / f) for f in files]
    file_list = ", ".join(f"'{p}'" for p in full_paths)
    con.sql(
        f"DESCRIBE SELECT * FROM read_parquet([{file_list}], "
        f"union_by_name=true, filename=true)"
    ).show()

# %% [markdown]
# ## 4. Row preview -- SELECT * LIMIT 10

# %%
for table_name in smoke:
    print(f"\n{'='*60}")
    print(f"  {table_name}: {smoke[table_name]['row_count']} rows, {smoke[table_name]['column_count']} cols")
    print(f"{'='*60}")
    files = smoke[table_name]["files_sampled"]
    full_paths = [str(AOESTATS_RAW_DIR / table_name / f) for f in files]
    file_list = ", ".join(f"'{p}'" for p in full_paths)
    con.sql(
        f"SELECT * FROM read_parquet([{file_list}], "
        f"union_by_name=true, filename=true) LIMIT 10"
    ).show()

# %% [markdown]
# ## 5. Variant columns -- types and NULL counts per week (matches)

# %%
con.sql("""
    SELECT
        filename.split('matches/')[2][:10] AS file_week,
        COUNT(*) AS rows,
        COUNT(raw_match_type) AS raw_match_type_nn,
        COUNT(started_timestamp) AS started_timestamp_nn,
        COUNT(duration) AS duration_nn,
        COUNT(irl_duration) AS irl_duration_nn,
        typeof(duration) AS duration_type,
        typeof(irl_duration) AS irl_duration_type
    FROM read_parquet(
        '{glob}',
        union_by_name=true, filename=true
    )
    GROUP BY file_week
    ORDER BY file_week
""".format(glob=str(AOESTATS_RAW_DIR / "matches" / "*.parquet"))).show()

# %% [markdown]
# ## 6. Variant columns -- types and NULL counts per week (players)

# %%
con.sql("""
    SELECT
        filename.split('players/')[2][:10] AS file_week,
        COUNT(*) AS rows,
        COUNT(profile_id) AS profile_id_nn,
        COUNT(feudal_age_uptime) AS feudal_nn,
        COUNT(castle_age_uptime) AS castle_nn,
        COUNT(imperial_age_uptime) AS imperial_nn,
        COUNT(opening) AS opening_nn,
        typeof(profile_id) AS profile_id_type,
        typeof(feudal_age_uptime) AS feudal_type
    FROM read_parquet(
        '{glob}',
        union_by_name=true, filename=true
    )
    GROUP BY file_week
    ORDER BY file_week
""".format(glob=str(AOESTATS_RAW_DIR / "players" / "*.parquet"))).show()

# %%
con.close()
