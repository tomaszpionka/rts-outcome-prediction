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
# # Step 01_02_02 -- DuckDB Ingestion: aoe2companion
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoe2companion
# **Question:** Materialise raw data into persistent DuckDB tables using the
# strategies determined by 01_02_01 (binary_as_string, explicit CSV types).
# **Invariants applied:** #6 (reproducibility), #7 (provenance), #9 (step scope)
# **Step scope:** ingest
# **Prerequisites:** 01_02_01 artifacts on disk, notebook re-executed with outputs

# %%
import json
import logging

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir
from rts_predict.games.aoe2.config import AOE2COMPANION_RAW_DIR
from rts_predict.games.aoe2.datasets.aoe2companion.ingestion import (
    load_all_raw_tables,
)
from rts_predict.games.aoe2.datasets.aoe2companion.types import DtypeDecision

logging.basicConfig(level=logging.INFO)

# %% [markdown]
# ## 1. Configure dtype decision
#
# The DtypeDecision for rating CSVs was determined in Step 01_02_01.
# Using auto_detect as the default strategy; switch to explicit if
# 01_02_01 findings require it.

# %%
# Default: auto_detect. Update if 01_02_01 prescribes explicit types.
decision = DtypeDecision(
    strategy="auto_detect",
    rationale="01_02_01 did not identify type inference failures requiring explicit types",
)
print(f"Dtype strategy: {decision.strategy}")
print(f"Rationale: {decision.rationale}")

# %% [markdown]
# ## 2. Ingest all DuckDB tables
#
# Calls `load_all_raw_tables` which creates:
# - `raw_matches` -- from 2,073 daily match Parquet files
# - `raw_ratings` -- from 2,072 daily rating CSV files
# - `raw_leaderboard` -- singleton leaderboard Parquet
# - `raw_profiles` -- singleton profile Parquet

# %%
db = get_notebook_db("aoe2", "aoe2companion", read_only=False)
counts = load_all_raw_tables(db.con, AOE2COMPANION_RAW_DIR, decision=decision)
print("Ingestion counts:")
for table, n in counts.items():
    print(f"  {table}: {n:,} rows")

# %% [markdown]
# ## 3. Post-ingestion validation: DESCRIBE tables

# %%
for table in counts:
    print(f"\n=== DESCRIBE {table} ===")
    desc_df = db.fetch_df(f'DESCRIBE "{table}"')
    print(desc_df.to_string(index=False))

# %% [markdown]
# ## 4. NULL rates on key fields

# %%
# raw_matches NULL rates
match_null_query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(match_id) AS match_id_null,
    COUNT(*) - COUNT(started) AS started_null,
    COUNT(*) - COUNT(map_name) AS map_name_null,
    COUNT(*) - COUNT(filename) AS filename_null
FROM raw_matches
"""
print("=== raw_matches NULL rates ===")
print(db.fetch_df(match_null_query).to_string(index=False))

# %%
# raw_ratings NULL rates
rating_null_query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(profile_id) AS profile_id_null,
    COUNT(*) - COUNT(rating) AS rating_null,
    COUNT(*) - COUNT(filename) AS filename_null
FROM raw_ratings
"""
print("=== raw_ratings NULL rates ===")
print(db.fetch_df(rating_null_query).to_string(index=False))

# %%
# raw_leaderboard row count
print(f"raw_leaderboard: {counts.get('raw_leaderboard', 'N/A'):,} rows")
print(f"raw_profiles: {counts.get('raw_profiles', 'N/A'):,} rows")

# %%
db.close()

# %% [markdown]
# ## 5. Write artifacts

# %%
reports_dir = get_reports_dir("aoe2", "aoe2companion")
artifacts_dir = reports_dir / "artifacts" / "01_exploration" / "02_eda"
artifacts_dir.mkdir(parents=True, exist_ok=True)

artifact_data = {
    "step": "01_02_02",
    "dataset": "aoe2companion",
    "dtype_decision": {
        "strategy": decision.strategy,
        "rationale": decision.rationale,
    },
    "tables_created": {
        table: {"row_count": n} for table, n in counts.items()
    },
}

artifact_path = artifacts_dir / "01_02_02_duckdb_ingestion.json"
artifact_path.write_text(json.dumps(artifact_data, indent=2))
print(f"Artifact written: {artifact_path}")

# %%
md_lines = [
    "# Step 01_02_02 -- DuckDB Ingestion: aoe2companion\n",
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
    f"## Dtype strategy: {decision.strategy}\n",
    "",
    f"Rationale: {decision.rationale}",
    "",
    "## SQL used\n",
    "",
    "See `src/rts_predict/games/aoe2/datasets/aoe2companion/ingestion.py` for all",
    "SQL constants.",
])

md_path = artifacts_dir / "01_02_02_duckdb_ingestion.md"
md_path.write_text("\n".join(md_lines))
print(f"Report written: {md_path}")
