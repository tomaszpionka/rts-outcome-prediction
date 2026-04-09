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
# # Step 01_01_01 — File Inventory: sc2egset
#
# **Phase:** 01 — Data Exploration
# **Pipeline Section:** 01_01 — Data Acquisition & Source Inventory
# **Dataset:** sc2egset
# **Question:** What files exist on disk, how many are there, and how are they organized?
#
# This notebook walks the sc2egset raw directory and counts everything.
# It does NOT compare against any expected counts — it produces the counts
# for the first time.

# %%
import json
import logging
from pathlib import Path

from rts_predict.common.inventory import inventory_directory
from rts_predict.common.notebook_utils import get_reports_dir

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# %%
# Paths — derived from project config, not hardcoded
from rts_predict.sc2.config import REPLAYS_SOURCE_DIR

RAW_DIR: Path = REPLAYS_SOURCE_DIR
ARTIFACTS_DIR: Path = get_reports_dir("sc2", "sc2egset") / "artifacts" / "01_01"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

logger.info("Raw directory: %s", RAW_DIR)
logger.info("Artifacts directory: %s", ARTIFACTS_DIR)

# %%
result = inventory_directory(RAW_DIR)

logger.info("Total files: %d", result.total_files)
logger.info("Total size: %.2f MB", result.total_bytes / (1024 * 1024))
logger.info("Subdirectories: %d", len(result.subdirs))
logger.info("Files at root: %d", len(result.files_at_root))

# %%
# Compute per-subdirectory stats
subdir_data = []
for sd in result.subdirs:
    subdir_data.append({
        "name": sd.name,
        "file_count": sd.file_count,
        "total_bytes": sd.total_bytes,
        "total_mb": round(sd.total_bytes / (1024 * 1024), 2),
        "extensions": sd.extensions,
    })

# Summary statistics
file_counts = [sd.file_count for sd in result.subdirs]
if file_counts:
    import statistics
    logger.info("Files per subdir — min: %d, max: %d, median: %.1f",
                min(file_counts), max(file_counts), statistics.median(file_counts))

# Subdirectories with 0 replay files (if filtering was applied)
# Since we use file_glob="*", all files are counted, so flag subdirs
# with 0 .SC2Replay.json files specifically
for sd in result.subdirs:
    json_count = sd.extensions.get(".json", 0)
    if json_count == 0:
        logger.warning("Subdirectory with 0 .json files: %s", sd.name)

# %%
artifact = {
    "step": "01_01_01",
    "dataset": "sc2egset",
    "raw_dir": str(RAW_DIR),
    "total_files": result.total_files,
    "total_bytes": result.total_bytes,
    "num_subdirs": len(result.subdirs),
    "files_at_root": len(result.files_at_root),
    "subdirs": subdir_data,
}

json_path = ARTIFACTS_DIR / "01_01_01_file_inventory.json"
json_path.write_text(json.dumps(artifact, indent=2, default=str))
logger.info("JSON artifact written: %s", json_path)

# %%
lines = [
    "# Step 01_01_01 — File Inventory: sc2egset\n",
    f"**Raw directory:** `{RAW_DIR}`\n",
    f"**Total files:** {result.total_files}\n",
    f"**Total size:** {result.total_bytes / (1024**2):.2f} MB\n",
    f"**Subdirectories:** {len(result.subdirs)}\n",
    f"**Files at root level:** {len(result.files_at_root)}\n",
    "\n## Per-subdirectory breakdown\n",
    "| Subdirectory | Files | Size (MB) | Extensions |",
    "|---|---|---|---|",
]
for sd in subdir_data:
    ext_str = ", ".join(f"{k}: {v}" for k, v in sorted(sd["extensions"].items()))
    lines.append(f"| {sd['name']} | {sd['file_count']} | {sd['total_mb']} | {ext_str} |")

if file_counts:
    lines.extend([
        "\n## Summary statistics\n",
        f"- Min files per subdir: {min(file_counts)}",
        f"- Max files per subdir: {max(file_counts)}",
        f"- Median files per subdir: {statistics.median(file_counts):.1f}",
    ])

md_path = ARTIFACTS_DIR / "01_01_01_file_inventory.md"
md_path.write_text("\n".join(lines) + "\n")
logger.info("Markdown artifact written: %s", md_path)

# %% [markdown]
# ## Verification
#
# The artifacts have been written. The counts above ARE the authoritative
# inventory — they are not compared against any prior documentation.
