"""Pre-ingestion helpers for aoe2companion DuckDB ingestion (step 01_02_01).

Provides:
- Pyarrow binary column inspection
- Smoke test ingestion into temporary DuckDB tables
- Full CTAS ingestion for matches_raw, ratings_raw, leaderboards_raw, profiles_raw
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
    filename = true,
    binary_as_string = true
)
"""

_RATINGS_RAW_CTAS_QUERY = """
CREATE TABLE ratings_raw AS
SELECT * FROM read_csv_auto(
    '{glob}',
    filename = true
)
"""

# Fallback: explicit types when read_csv_auto infers all VARCHAR
_RATINGS_RAW_TYPED_CTAS_QUERY = """
CREATE TABLE ratings_raw AS
SELECT * FROM read_csv(
    '{glob}',
    filename = true,
    header = true,
    types = {{
        'profile_id': 'BIGINT',
        'games': 'BIGINT',
        'rating': 'BIGINT',
        'date': 'TIMESTAMP',
        'leaderboard_id': 'BIGINT',
        'rating_diff': 'BIGINT',
        'season': 'BIGINT'
    }}
)
"""

_LEADERBOARDS_RAW_CTAS_QUERY = """
CREATE TABLE leaderboards_raw AS
SELECT * FROM read_parquet(
    '{path}',
    binary_as_string = true,
    filename = true
)
"""

_PROFILES_RAW_CTAS_QUERY = """
CREATE TABLE profiles_raw AS
SELECT * FROM read_parquet(
    '{path}',
    binary_as_string = true,
    filename = true
)
"""

_ROW_COUNT_QUERY = "SELECT COUNT(*) AS n FROM {table}"

_NULL_COUNT_QUERY = """
SELECT COUNT(*) FILTER (WHERE "{col}" IS NULL) AS null_count
FROM {table}
"""

_DESCRIBE_QUERY = "DESCRIBE {table}"


def inspect_binary_columns(
    raw_dir: Path,
) -> dict[str, Any]:
    """Run pyarrow schema inspection on Parquet files for binary columns.

    For each binary-typed column: records parquet_logical and converted_type
    to determine whether unannotated BYTE_ARRAY (requiring binary_as_string=true)
    or annotated STRING/UTF8.

    Args:
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary with per-subdirectory binary column inspection results.
    """
    result: dict[str, Any] = {}

    subdirs = {
        "matches": raw_dir / "matches",
        "leaderboards": raw_dir / "leaderboards",
        "profiles": raw_dir / "profiles",
    }

    for subdir_name, subdir in subdirs.items():
        files = sorted(subdir.glob("*.parquet"))
        if not files:
            result[subdir_name] = {"error": "no parquet files found"}
            continue

        sample_file = files[0]
        pf = pq.ParquetFile(sample_file)
        schema = pf.schema_arrow
        parquet_schema = pf.schema

        binary_cols: list[dict[str, Any]] = []
        for i, field in enumerate(schema):
            if "binary" in str(field.type).lower() or str(field.type) == "large_binary":
                parquet_col = parquet_schema.column(i)
                binary_cols.append({
                    "name": field.name,
                    "arrow_type": str(field.type),
                    "physical_type": str(parquet_col.physical_type),
                    "logical_type": str(parquet_col.logical_type),
                    "converted_type": str(parquet_col.converted_type),
                })

        result[subdir_name] = {
            "sample_file": sample_file.name,
            "total_columns": len(schema),
            "binary_columns": binary_cols,
            "binary_column_count": len(binary_cols),
        }

    return result


def run_smoke_test(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> dict[str, Any]:
    """Ingest small samples into temporary tables and verify types.

    Picks files from earliest, middle, latest by filename date.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary with smoke test results (DESCRIBE, row counts).
    """
    results: dict[str, Any] = {}

    # Matches (Parquet)
    matches_files = sorted((raw_dir / "matches").glob("*.parquet"))
    if len(matches_files) >= 3:
        match_sample = [matches_files[0], matches_files[len(matches_files) // 2], matches_files[-1]]
    else:
        match_sample = matches_files

    file_list = ", ".join(f"'{f}'" for f in match_sample)
    con.execute(
        f"CREATE TEMP TABLE smoke_matches_raw AS "
        f"SELECT * FROM read_parquet([{file_list}], "
        f"filename=true, binary_as_string=true)"
    )
    describe_df = con.execute("DESCRIBE smoke_matches_raw").df()
    count_df = con.execute("SELECT COUNT(*) AS n FROM smoke_matches_raw").df()
    results["matches"] = {
        "files_sampled": [f.name for f in match_sample],
        "describe": describe_df.to_dict(orient="records"),
        "row_count": int(count_df["n"].iloc[0]),
        "column_count": len(describe_df),
    }
    con.execute("DROP TABLE IF EXISTS smoke_matches_raw")

    # Ratings (CSV)
    ratings_files = sorted((raw_dir / "ratings").glob("*.csv"))
    if len(ratings_files) >= 3:
        mid_idx = len(ratings_files) // 2
        rating_sample = [ratings_files[0], ratings_files[mid_idx], ratings_files[-1]]
    else:
        rating_sample = ratings_files

    file_list = ", ".join(f"'{f}'" for f in rating_sample)
    con.execute(
        f"CREATE TEMP TABLE smoke_ratings_raw AS "
        f"SELECT * FROM read_csv_auto([{file_list}], "
        f"filename=true)"
    )
    describe_df = con.execute("DESCRIBE smoke_ratings_raw").df()
    count_df = con.execute("SELECT COUNT(*) AS n FROM smoke_ratings_raw").df()
    results["ratings"] = {
        "files_sampled": [f.name for f in rating_sample],
        "describe": describe_df.to_dict(orient="records"),
        "row_count": int(count_df["n"].iloc[0]),
        "column_count": len(describe_df),
    }
    con.execute("DROP TABLE IF EXISTS smoke_ratings_raw")

    return results


def ingest_matches_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create matches_raw table from all Parquet files with binary_as_string.

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


def ingest_ratings_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    *,
    use_explicit_types: bool = False,
) -> int:
    """Create ratings_raw table from all CSV files.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.
        use_explicit_types: If True, use explicit column types
            instead of auto-inference. Required when read_csv_auto
            infers all columns as VARCHAR on large file sets.

    Returns:
        Row count of the created table.
    """
    glob = str(raw_dir / "ratings" / "*.csv")
    con.execute("DROP TABLE IF EXISTS ratings_raw")
    if use_explicit_types:
        con.execute(_RATINGS_RAW_TYPED_CTAS_QUERY.format(glob=glob))
    else:
        con.execute(_RATINGS_RAW_CTAS_QUERY.format(glob=glob))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="ratings_raw")).df()
    return int(count_df["n"].iloc[0])


def ingest_leaderboards_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create leaderboards_raw table from leaderboard.parquet.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Row count of the created table.
    """
    path = str(raw_dir / "leaderboards" / "leaderboard.parquet")
    con.execute("DROP TABLE IF EXISTS leaderboards_raw")
    con.execute(_LEADERBOARDS_RAW_CTAS_QUERY.format(path=path))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="leaderboards_raw")).df()
    return int(count_df["n"].iloc[0])


def ingest_profiles_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
) -> int:
    """Create profiles_raw table from profile.parquet.

    Args:
        con: Open DuckDB connection (read-write).
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Row count of the created table.
    """
    path = str(raw_dir / "profiles" / "profile.parquet")
    con.execute("DROP TABLE IF EXISTS profiles_raw")
    con.execute(_PROFILES_RAW_CTAS_QUERY.format(path=path))
    count_df = con.execute(_ROW_COUNT_QUERY.format(table="profiles_raw")).df()
    return int(count_df["n"].iloc[0])


def verify_tables(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, Any]:
    """Run post-ingestion verification on all aoe2companion tables.

    Args:
        con: Open DuckDB connection.

    Returns:
        Dictionary with verification results per table.
    """
    tables = ["matches_raw", "ratings_raw", "leaderboards_raw", "profiles_raw"]
    results: dict[str, Any] = {}

    for table in tables:
        describe_df = con.execute(_DESCRIBE_QUERY.format(table=table)).df()
        count_df = con.execute(_ROW_COUNT_QUERY.format(table=table)).df()
        row_count = int(count_df["n"].iloc[0])

        results[table] = {
            "describe": describe_df.to_dict(orient="records"),
            "row_count": row_count,
            "column_count": len(describe_df),
        }

    return results


def check_ratings_types(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, str]:
    """Check DuckDB-inferred types for ratings_raw columns.

    Per spec: profile_id -> INTEGER/BIGINT, date -> DATE/TIMESTAMP,
    games/rating/rating_diff -> INTEGER, season -> INTEGER or VARCHAR.

    Args:
        con: Open DuckDB connection.

    Returns:
        Mapping of column_name -> column_type for ratings_raw.
    """
    describe_df = con.execute(_DESCRIBE_QUERY.format(table="ratings_raw")).df()
    return dict(zip(describe_df["column_name"].tolist(), describe_df["column_type"].tolist()))


def count_won_nulls(
    con: duckdb.DuckDBPyConnection,
) -> dict[str, int]:
    """Count NULLs in the won column of matches_raw.

    Args:
        con: Open DuckDB connection.

    Returns:
        Dict with total rows, null count, non-null count.
    """
    df = con.execute(
        "SELECT "
        "COUNT(*) AS total, "
        'COUNT(*) FILTER (WHERE "won" IS NULL) AS null_count, '
        'COUNT(*) FILTER (WHERE "won" IS NOT NULL) AS non_null_count '
        "FROM matches_raw"
    ).df()
    return {
        "total": int(df["total"].iloc[0]),
        "null_count": int(df["null_count"].iloc[0]),
        "non_null_count": int(df["non_null_count"].iloc[0]),
    }


def find_date_gap(
    raw_dir: Path,
) -> dict[str, Any]:
    """Identify which date has matches but no ratings (or vice versa).

    Uses filename patterns: match-{date}.parquet and rating-{date}.csv.

    Args:
        raw_dir: Path to the dataset's raw/ directory.

    Returns:
        Dictionary documenting the file count gap.
    """
    import re

    matches_dates = set()
    for f in (raw_dir / "matches").glob("*.parquet"):
        m = re.search(r"match-(\d{4}-\d{2}-\d{2})\.parquet", f.name)
        if m:
            matches_dates.add(m.group(1))

    ratings_dates = set()
    for f in (raw_dir / "ratings").glob("*.csv"):
        m = re.search(r"rating-(\d{4}-\d{2}-\d{2})\.csv", f.name)
        if m:
            ratings_dates.add(m.group(1))

    return {
        "matches_date_count": len(matches_dates),
        "ratings_date_count": len(ratings_dates),
        "in_matches_not_ratings": sorted(matches_dates - ratings_dates),
        "in_ratings_not_matches": sorted(ratings_dates - matches_dates),
    }
