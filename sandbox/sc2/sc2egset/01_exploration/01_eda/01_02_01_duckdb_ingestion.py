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
# # Step 01_02_01 -- DuckDB Ingestion Investigation: sc2egset
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** sc2egset
# **Question:** How does DuckDB read_json_auto handle SC2EGSet replay JSONs?
# What is the event array storage cost? What table split strategy is optimal?
# **Invariants applied:** #6 (reproducibility), #9 (step scope)
# **Step scope:** query
# **Type:** Investigation only -- no full ingestion of 22,390 files

# %%
import json
import logging
import statistics
from pathlib import Path

import duckdb

from rts_predict.common.notebook_utils import get_reports_dir
from rts_predict.games.sc2.config import REPLAYS_SOURCE_DIR
from rts_predict.games.sc2.datasets.sc2egset.pre_ingestion import (
    select_sample_files,
    probe_read_json_auto_single,
    measure_event_arrays,
    probe_batch_ingestion,
    census_mapping_files,
    probe_mapping_read_json_auto,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# %% [markdown]
# ## 1. Select sample files

# %%
inv_path = Path(
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/"
    "artifacts/01_exploration/01_acquisition/"
    "01_01_01_file_inventory.json"
)
with open(inv_path) as f:
    inventory = json.load(f)

samples = select_sample_files(inventory, REPLAYS_SOURCE_DIR)
print(f"Selected {len(samples)} sample files:")
for s in samples:
    mb = s.stat().st_size / 1024 / 1024
    print(f"  {s.parent.parent.name}/{s.name} ({mb:.1f} MB)")

# %% [markdown]
# ## 2. Test read_json_auto on each sample

# %%
con = duckdb.connect(":memory:")
con.execute("SET memory_limit = '24GB'")
con.execute("SET threads = 4")

rja_results = []
for s in samples:
    r = probe_read_json_auto_single(con, s)
    rja_results.append(r)
    print(f"{r['file']}: success={r['success']}, cols={r.get('column_count')}")
    print(f"  ToonPlayerDescMap: {r.get('ToonPlayerDescMap_type', 'N/A')[:80]}...")

# %% [markdown]
# ## 3. Event array storage assessment

# %%
ea_results = [measure_event_arrays(s) for s in samples]

for key in ("gameEvents", "trackerEvents", "messageEvents"):
    counts = [r[key]["element_count"] for r in ea_results]
    bytes_ = [r[key]["json_bytes"] for r in ea_results]
    total_est_gb = statistics.mean(bytes_) * 22390 / 1024**3
    print(f"{key}:")
    print(f"  elements: mean={statistics.mean(counts):.0f}, "
          f"median={statistics.median(counts):.0f}, "
          f"min={min(counts)}, max={max(counts)}")
    print(f"  est. total (22,390 files): {total_est_gb:.1f} GB")

# %% [markdown]
# ## 4. Batch ingestion test

# %%
batch_dir = (
    REPLAYS_SOURCE_DIR / "2018_Cheeseadelphia_8"
    / "2018_Cheeseadelphia_8_data"
)
batch_result = probe_batch_ingestion(con, batch_dir)
print(f"Directory: {batch_result['directory']}")
print(f"Files: {batch_result['file_count']}")
print(f"Success: {batch_result['success']}")
print(f"Elapsed: {batch_result.get('elapsed_seconds', 'N/A')} seconds")
print(f"Rows: {batch_result.get('row_count', 'N/A')}")

# %% [markdown]
# ## 5. Mapping file census

# %%
census = census_mapping_files(REPLAYS_SOURCE_DIR)
print(f"Files found: {census['total_files_found']}")
print(f"Combined size: {census['total_combined_bytes']:,} bytes")
print(f"Cross-file consistency: {census['cross_file_consistency']}")

# %%
first_mf = (
    REPLAYS_SOURCE_DIR / census["files"][0]["tournament"]
    / "map_foreign_to_english_mapping.json"
)
mapping_test = probe_mapping_read_json_auto(con, first_mf)
print(f"read_json_auto: success={mapping_test['success']}")
print(f"DuckDB type: {mapping_test.get('columns', [{}])[0].get('column_type')}")

# %%
con.close()

# %% [markdown]
# ## 6. Artifacts

# %%
artifacts_dir = (
    get_reports_dir("sc2", "sc2egset")
    / "artifacts" / "01_exploration" / "01_eda"
)
print(f"Artifacts at: {artifacts_dir}")
print("JSON and MD artifacts written by pre_ingestion pipeline.")
