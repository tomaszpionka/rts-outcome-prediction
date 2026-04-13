"""Pre-ingestion investigation helpers for sc2egset (step 01_02_01).

SC2EGSet is investigation-only at this step: test read_json_auto behavior,
estimate event array storage, census mapping files.

Does NOT create persistent DuckDB tables.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import duckdb

logger = logging.getLogger(__name__)


def select_sample_files(
    inventory: dict[str, Any],
    raw_dir: Path,
    *,
    n_middle: int = 3,
) -> list[Path]:
    """Select 5-10 sample .SC2Replay.json files spanning the file-size distribution.

    Strategy: compute avg MB/file per directory from inventory data, pick
    1 from smallest-avg dir, 1 from largest-avg dir, the literal largest
    individual file, plus n_middle from middle of distribution.

    Args:
        inventory: Parsed 01_01_01 file inventory JSON.
        raw_dir: Path to the dataset's raw/ directory.
        n_middle: Number of files to pick from middle directories.

    Returns:
        List of Path objects to sample files.
    """
    dirs = inventory["top_level_dirs"]
    dir_avgs: list[tuple[str, float]] = []
    for d in dirs:
        count = d["replay_file_count"]
        total = d["total_bytes"]
        if count > 0:
            dir_avgs.append((d["name"], total / count))

    dir_avgs.sort(key=lambda x: x[1])

    samples: list[Path] = []

    # 1 from smallest-avg dir
    smallest_dir_name = dir_avgs[0][0]
    smallest_dir = raw_dir / smallest_dir_name / f"{smallest_dir_name}_data"
    smallest_files = sorted(smallest_dir.glob("*.SC2Replay.json"))
    if smallest_files:
        samples.append(smallest_files[0])

    # 1 from largest-avg dir
    largest_dir_name = dir_avgs[-1][0]
    largest_dir = raw_dir / largest_dir_name / f"{largest_dir_name}_data"
    largest_files = sorted(largest_dir.glob("*.SC2Replay.json"))
    if largest_files:
        samples.append(largest_files[0])

    # Literal largest individual file across all dirs
    all_files_with_size: list[tuple[Path, int]] = []
    for d_name, _ in dir_avgs:
        data_dir = raw_dir / d_name / f"{d_name}_data"
        for f in data_dir.glob("*.SC2Replay.json"):
            all_files_with_size.append((f, f.stat().st_size))

    if all_files_with_size:
        all_files_with_size.sort(key=lambda x: x[1], reverse=True)
        largest_file = all_files_with_size[0][0]
        if largest_file not in samples:
            samples.append(largest_file)

    # n_middle from middle dirs
    mid_start = len(dir_avgs) // 4
    mid_end = 3 * len(dir_avgs) // 4
    mid_dirs = dir_avgs[mid_start:mid_end]
    step = max(1, len(mid_dirs) // n_middle)
    for i in range(0, len(mid_dirs), step):
        if len(samples) >= 5 + n_middle:
            break
        d_name = mid_dirs[i][0]
        data_dir = raw_dir / d_name / f"{d_name}_data"
        mid_files = sorted(data_dir.glob("*.SC2Replay.json"))
        if mid_files:
            mid_file = mid_files[len(mid_files) // 2]
            if mid_file not in samples:
                samples.append(mid_file)

    return samples


def probe_read_json_auto_single(
    con: duckdb.DuckDBPyConnection,
    file_path: Path,
) -> dict[str, Any]:
    """Test read_json_auto on a single SC2Replay.json file.

    Records which root keys become columns, DuckDB types, and any errors.

    Args:
        con: Open in-memory DuckDB connection.
        file_path: Path to a .SC2Replay.json file.

    Returns:
        Dictionary with column names, types, success/failure status.
    """
    result: dict[str, Any] = {
        "file": file_path.name,
        "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
    }

    try:
        con.execute(
            f"CREATE TEMP TABLE test_json AS "
            f"SELECT * FROM read_json_auto('{file_path}', "
            f"maximum_object_size=536870912)"
        )
        describe_df = con.execute("DESCRIBE test_json").df()
        result["success"] = True
        result["columns"] = describe_df.to_dict(orient="records")
        result["column_count"] = len(describe_df)

        # Check ToonPlayerDescMap type
        tpdm_rows = describe_df[describe_df["column_name"] == "ToonPlayerDescMap"]
        if len(tpdm_rows) > 0:
            result["ToonPlayerDescMap_type"] = tpdm_rows.iloc[0]["column_type"]
        else:
            result["ToonPlayerDescMap_type"] = "NOT_FOUND"

        con.execute("DROP TABLE IF EXISTS test_json")
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        con.execute("DROP TABLE IF EXISTS test_json")

    return result


def measure_event_arrays(
    file_path: Path,
) -> dict[str, Any]:
    """Measure JSON byte size and element count of event arrays in a file.

    Args:
        file_path: Path to a .SC2Replay.json file.

    Returns:
        Dictionary with event array metrics.
    """
    with open(file_path) as f:
        data = json.load(f)

    result: dict[str, Any] = {
        "file": file_path.name,
        "file_size_bytes": file_path.stat().st_size,
    }

    for key in ("gameEvents", "trackerEvents", "messageEvents"):
        if key in data:
            arr = data[key]
            arr_json = json.dumps(arr)
            result[key] = {
                "element_count": len(arr),
                "json_bytes": len(arr_json.encode("utf-8")),
            }
        else:
            result[key] = {"element_count": 0, "json_bytes": 0}

    return result


def probe_batch_ingestion(
    con: duckdb.DuckDBPyConnection,
    directory: Path,
) -> dict[str, Any]:
    """Test read_json_auto on an entire tournament directory glob.

    Args:
        con: Open in-memory DuckDB connection.
        directory: Path to a tournament's _data directory.

    Returns:
        Dictionary with batch test results.
    """
    import time

    glob = str(directory / "*.SC2Replay.json")
    file_count = len(list(directory.glob("*.SC2Replay.json")))
    result: dict[str, Any] = {
        "directory": directory.name,
        "file_count": file_count,
    }

    try:
        start = time.perf_counter()
        con.execute(
            f"CREATE TEMP TABLE batch_test AS "
            f"SELECT * FROM read_json_auto('{glob}', "
            f"union_by_name=true, filename=true, "
            f"maximum_object_size=536870912)"
        )
        elapsed = time.perf_counter() - start

        count_df = con.execute("SELECT COUNT(*) AS n FROM batch_test").df()
        describe_df = con.execute("DESCRIBE batch_test").df()

        result["success"] = True
        result["elapsed_seconds"] = round(elapsed, 2)
        result["row_count"] = int(count_df["n"].iloc[0])
        result["column_count"] = len(describe_df)
        result["columns"] = describe_df.to_dict(orient="records")

        con.execute("DROP TABLE IF EXISTS batch_test")
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        con.execute("DROP TABLE IF EXISTS batch_test")

    return result


def census_mapping_files(
    raw_dir: Path,
) -> dict[str, Any]:
    """Full census of all map_foreign_to_english_mapping.json files.

    Reads ALL 70 files, records structure, checks cross-file consistency.

    Args:
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary with census results.
    """
    mapping_files: list[Path] = []
    for d in sorted(raw_dir.iterdir()):
        if d.is_dir():
            mf = d / "map_foreign_to_english_mapping.json"
            if mf.exists():
                mapping_files.append(mf)

    result: dict[str, Any] = {
        "total_files_found": len(mapping_files),
        "total_combined_bytes": sum(f.stat().st_size for f in mapping_files),
        "files": [],
    }

    all_root_types: list[str] = []
    all_key_counts: list[int] = []
    all_key_sets: list[set[str]] = []

    for mf in mapping_files:
        with open(mf) as f:
            data = json.load(f)

        file_info: dict[str, Any] = {
            "tournament": mf.parent.name,
            "size_bytes": mf.stat().st_size,
        }

        if isinstance(data, dict):
            file_info["root_type"] = "dict"
            file_info["key_count"] = len(data)
            file_info["value_types"] = list({type(v).__name__ for v in data.values()})
            if data:
                sample_key = next(iter(data))
                file_info["sample_key"] = sample_key
                file_info["sample_value"] = str(data[sample_key])[:100]
            all_root_types.append("dict")
            all_key_counts.append(len(data))
            all_key_sets.append(set(data.keys()))
        elif isinstance(data, list):
            file_info["root_type"] = "list"
            file_info["element_count"] = len(data)
            all_root_types.append("list")
            all_key_counts.append(len(data))
            all_key_sets.append(set())
        else:
            file_info["root_type"] = type(data).__name__
            all_root_types.append(type(data).__name__)

        result["files"].append(file_info)

    # Cross-file consistency
    unique_root_types = set(all_root_types)
    result["cross_file_consistency"] = {
        "all_same_root_type": len(unique_root_types) == 1,
        "root_types": list(unique_root_types),
        "key_count_range": [min(all_key_counts), max(all_key_counts)] if all_key_counts else [],
    }

    if all_key_sets and all(all_key_sets):
        intersection = set.intersection(*all_key_sets)
        union = set.union(*all_key_sets)
        result["cross_file_consistency"]["shared_keys_count"] = len(intersection)
        result["cross_file_consistency"]["total_unique_keys"] = len(union)
        result["cross_file_consistency"]["all_same_key_set"] = intersection == union

    return result


def probe_mapping_read_json_auto(
    con: duckdb.DuckDBPyConnection,
    mapping_file: Path,
) -> dict[str, Any]:
    """Test read_json_auto on one mapping file.

    Args:
        con: Open in-memory DuckDB connection.
        mapping_file: Path to a map_foreign_to_english_mapping.json file.

    Returns:
        Dictionary with parse results.
    """
    result: dict[str, Any] = {"file": mapping_file.name}

    try:
        con.execute(
            f"CREATE TEMP TABLE mapping_test AS "
            f"SELECT * FROM read_json_auto('{mapping_file}')"
        )
        describe_df = con.execute("DESCRIBE mapping_test").df()
        count_df = con.execute("SELECT COUNT(*) AS n FROM mapping_test").df()

        result["success"] = True
        result["columns"] = describe_df.to_dict(orient="records")
        result["row_count"] = int(count_df["n"].iloc[0])
        con.execute("DROP TABLE IF EXISTS mapping_test")
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        con.execute("DROP TABLE IF EXISTS mapping_test")

    return result
