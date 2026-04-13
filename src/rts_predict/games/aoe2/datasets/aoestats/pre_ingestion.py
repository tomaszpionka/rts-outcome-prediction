"""Pre-ingestion helpers for aoestats DuckDB ingestion (step 01_02_01).

Provides:
- Variant column census via pyarrow (pre-ingestion type inspection)
- Smoke test ingestion into temporary DuckDB tables
- Full CTAS ingestion for matches_raw, players_raw, overviews_raw
- Post-ingestion verification queries

Uses ``_raw`` suffix table naming convention for all raw-layer tables.
Does NOT depend on the obsolete ``ingestion.py`` module.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import duckdb
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)

# ── SQL constants ─────────────────────────────────────────────────────────────

_MATCHES_RAW_CTAS_QUERY = """
CREATE TABLE matches_raw AS
SELECT * FROM read_parquet(
    '{glob}',
    union_by_name = true,
    filename = true
)
"""

_PLAYERS_RAW_CTAS_QUERY = """
CREATE TABLE players_raw AS
SELECT * FROM read_parquet(
    '{glob}',
    union_by_name = true,
    filename = true
)
"""

_OVERVIEWS_RAW_CTAS_QUERY = """
CREATE TABLE overviews_raw AS
SELECT * FROM read_json_auto(
    '{path}',
    filename = true
)
"""

_ROW_COUNT_QUERY = "SELECT COUNT(*) AS n FROM {table}"

_NULL_COUNT_QUERY = """
SELECT COUNT(*) FILTER (WHERE "{col}" IS NULL) AS null_count
FROM {table}
"""

_DESCRIBE_QUERY = "DESCRIBE {table}"


def run_variant_census(
    raw_dir: Path,
) -> dict[str, Any]:
    """Run pyarrow schema census on all matches + players Parquet files.

    Reads only metadata (no row data) to build a per-column type
    distribution across all files.

    Args:
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary with per-subdirectory variant column census.
    """
    result: dict[str, Any] = {}

    for subdir_name in ("matches", "players"):
        subdir = raw_dir / subdir_name
        files = sorted(subdir.glob("*.parquet"))
        logger.info("Scanning %d %s files for variant census", len(files), subdir_name)

        col_types: dict[str, dict[str, list[str]]] = {}
        for f in files:
            schema = pq.read_schema(f)
            for field in schema:
                if field.name not in col_types:
                    col_types[field.name] = {}
                type_str = str(field.type)
                if type_str not in col_types[field.name]:
                    col_types[field.name][type_str] = []
                col_types[field.name][type_str].append(f.name)

        variant_cols = {
            col: types
            for col, types in col_types.items()
            if len(types) > 1
        }

        result[subdir_name] = {
            "total_files": len(files),
            "all_columns": {
                col: {t: len(fnames) for t, fnames in types.items()}
                for col, types in col_types.items()
            },
            "variant_columns": {
                col: {t: len(fnames) for t, fnames in types.items()}
                for col, types in variant_cols.items()
            },
        }

    return result


def run_smoke_test(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> dict[str, Any]:
    """Ingest a small sample into temporary tables and verify types.

    Picks 3 files per subdirectory (earliest, middle, latest by filename).

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary with smoke test results (DESCRIBE, row counts).
    """
    results: dict[str, Any] = {}

    smoke_pairs = [("matches", "smoke_matches_raw"), ("players", "smoke_players_raw")]
    for subdir_name, table_name in smoke_pairs:
        subdir = raw_dir / subdir_name
        files = sorted(subdir.glob("*.parquet"))
        if len(files) < 3:
            sample_files = files
        else:
            sample_files = [files[0], files[len(files) // 2], files[-1]]

        file_list = ", ".join(f"'{f}'" for f in sample_files)
        sql = (
            f"CREATE TEMP TABLE {table_name} AS "
            f"SELECT * FROM read_parquet([{file_list}], "
            f"union_by_name=true, filename=true)"
        )
        con.execute(sql)

        describe_df = con.execute(f"DESCRIBE {table_name}").df()
        count_df = con.execute(f"SELECT COUNT(*) AS n FROM {table_name}").df()

        results[subdir_name] = {
            "files_sampled": [f.name for f in sample_files],
            "describe": describe_df.to_dict(orient="records"),
            "row_count": int(count_df["n"].iloc[0]),
            "column_count": len(describe_df),
        }

        con.execute(f"DROP TABLE IF EXISTS {table_name}")

    return results


def ingest_matches_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create matches_raw table from all Parquet files.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Row count of the created table.
    """
    glob = str(raw_dir / "matches" / "*.parquet")
    con.execute("DROP TABLE IF EXISTS matches_raw")
    con.execute(_MATCHES_RAW_CTAS_QUERY.format(glob=glob))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="matches_raw")).df()
    return int(count_df["n"].iloc[0])


def ingest_players_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create players_raw table from all Parquet files.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Row count of the created table.
    """
    glob = str(raw_dir / "players" / "*.parquet")
    con.execute("DROP TABLE IF EXISTS players_raw")
    con.execute(_PLAYERS_RAW_CTAS_QUERY.format(glob=glob))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="players_raw")).df()
    return int(count_df["n"].iloc[0])


def ingest_overviews_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create overviews_raw table from overview.json.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Row count of the created table.
    """
    path = str(raw_dir / "overview" / "overview.json")
    con.execute("DROP TABLE IF EXISTS overviews_raw")
    con.execute(_OVERVIEWS_RAW_CTAS_QUERY.format(path=path))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="overviews_raw")).df()
    return int(count_df["n"].iloc[0])


def verify_tables(
    con: duckdb.DuckDBPyConnection,
    variant_columns: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Run post-ingestion verification on all aoestats tables.

    Args:
        con: Open DuckDB connection.
        variant_columns: Optional mapping of table -> list of variant
            column names to check NULL counts for.

    Returns:
        Dictionary with verification results.
    """
    tables = ["matches_raw", "players_raw", "overviews_raw"]
    results: dict[str, Any] = {}

    for table in tables:
        describe_df = con.execute(_DESCRIBE_QUERY.format(table=table)).df()
        count_df = con.execute(_ROW_COUNT_QUERY.format(table=table)).df()
        row_count = int(count_df["n"].iloc[0])

        table_result: dict[str, Any] = {
            "describe": describe_df.to_dict(orient="records"),
            "row_count": row_count,
            "column_count": len(describe_df),
        }

        if variant_columns and table in variant_columns:
            null_counts: dict[str, int] = {}
            for col in variant_columns[table]:
                null_df = con.execute(
                    _NULL_COUNT_QUERY.format(col=col, table=table)
                ).df()
                null_counts[col] = int(null_df["null_count"].iloc[0])
            table_result["variant_null_counts"] = null_counts

        results[table] = table_result

    return results


def check_duration_type(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, Any]:
    """Verify duration column types and produce sample values.

    DuckDB 1.5.1 maps Arrow duration[ns] to BIGINT (nanoseconds),
    not INTERVAL. This function documents the actual mapped type and
    converts sample values to seconds for reasonableness check.

    Args:
        con: Open DuckDB connection.

    Returns:
        Dictionary with typeof results and sample values.
    """
    result: dict[str, Any] = {}
    for col in ("duration", "irl_duration"):
        typeof_df = con.execute(
            f'SELECT typeof("{col}") AS t FROM matches_raw LIMIT 1'
        ).df()
        actual_type = typeof_df["t"].iloc[0]

        # If BIGINT (duration[ns] -> nanoseconds), convert to seconds
        if actual_type == "BIGINT":
            sample_df = con.execute(
                f'SELECT "{col}" / 1000000000.0 AS seconds '
                f'FROM matches_raw WHERE "{col}" IS NOT NULL LIMIT 5'
            ).df()
            result[col] = {
                "typeof": actual_type,
                "note": "Arrow duration[ns] mapped to BIGINT nanoseconds",
                "sample_seconds": sample_df["seconds"].tolist(),
            }
        elif actual_type == "INTERVAL":
            epoch_df = con.execute(
                f'SELECT EXTRACT(EPOCH FROM "{col}") AS epoch_seconds '
                f'FROM matches_raw WHERE "{col}" IS NOT NULL LIMIT 5'
            ).df()
            result[col] = {
                "typeof": actual_type,
                "sample_epoch_seconds": epoch_df["epoch_seconds"].tolist(),
            }
        else:
            result[col] = {"typeof": actual_type, "note": "unexpected type"}
    return result


def find_missing_weeks(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, Any]:
    """Identify weeks present in matches but not players (or vice versa).

    Extracts date ranges from filenames using the pattern
    {start}_{end}_{type}.parquet and compares by date range.

    Args:
        con: Open DuckDB connection.

    Returns:
        Dictionary documenting the missing-week asymmetry.
    """
    import re

    matches_files_df = con.execute(
        "SELECT DISTINCT filename FROM matches_raw ORDER BY filename"
    ).df()
    players_files_df = con.execute(
        "SELECT DISTINCT filename FROM players_raw ORDER BY filename"
    ).df()

    def extract_date_range(filepath: str) -> str | None:
        """Extract date range from filename like .../{start}_{end}_{type}.parquet."""
        basename = filepath.rsplit("/", 1)[-1]
        m = re.match(
            r"(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_\w+\.parquet",
            basename,
        )
        return f"{m.group(1)}_{m.group(2)}" if m else None

    matches_weeks = {
        extract_date_range(f)
        for f in matches_files_df["filename"].tolist()
        if extract_date_range(f)
    }
    players_weeks = {
        extract_date_range(f)
        for f in players_files_df["filename"].tolist()
        if extract_date_range(f)
    }

    return {
        "matches_week_count": len(matches_weeks),
        "players_week_count": len(players_weeks),
        "in_matches_not_players": sorted(matches_weeks - players_weeks),
        "in_players_not_matches": sorted(players_weeks - matches_weeks),
    }
