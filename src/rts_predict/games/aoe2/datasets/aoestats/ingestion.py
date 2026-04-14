"""Raw CTAS ingestion for aoestats into DuckDB.

Materialises three append-only raw tables from the weekly dump files:
- matches_raw   — one row per match per week, from weekly match parquets
- players_raw   — one row per player per match per week, from weekly player parquets
- overviews_raw — singleton snapshot from overview/overview.json

All tables carry a ``filename`` provenance column populated by
``filename = true`` on the source read. Removing this column in any
downstream view is forbidden (INVARIANT I7, I10).

Files follow the naming pattern: {start_date}_{end_date}_{type}.parquet
"""

import logging
from pathlib import Path

import duckdb

logger = logging.getLogger(__name__)

# ── SQL constants ─────────────────────────────────────────────────────────────

_DROP_IF_EXISTS_QUERY = "DROP TABLE IF EXISTS {table}"

_MATCHES_RAW_QUERY = """
CREATE TABLE matches_raw AS
SELECT * FROM read_parquet(
    '{glob}',
    union_by_name = true,
    filename = true
)
"""

_PLAYERS_RAW_QUERY = """
CREATE TABLE players_raw AS
SELECT * FROM read_parquet(
    '{glob}',
    union_by_name = true,
    filename = true
)
"""

_OVERVIEWS_RAW_QUERY = """
CREATE TABLE overviews_raw AS
SELECT * FROM read_json_auto('{path}', filename = true)
"""

_COUNT_QUERY = "SELECT count(*) FROM {table}"

# Strips the raw_dir prefix from DuckDB's absolute filename column (I10).
# prefix_len = len(str(raw_dir)) + 2  (+1 for 1-based substr, +1 for trailing /)
_RELATIVIZE_FILENAME_QUERY = (
    "UPDATE {table} SET filename = substr(filename, {prefix_len})"
)


def _relativize_filenames(
    con: duckdb.DuckDBPyConnection, table: str, raw_dir: Path
) -> None:
    """Strip raw_dir prefix from the filename column to make paths relative (I10).

    Args:
        con: Active DuckDB connection.
        table: Table whose filename column to update.
        raw_dir: The raw data directory whose path to strip.
    """
    prefix_len = len(str(raw_dir)) + 2
    con.execute(_RELATIVIZE_FILENAME_QUERY.format(table=table, prefix_len=prefix_len))


def _count_rows(con: duckdb.DuckDBPyConnection, table: str) -> int:
    """Return the row count for a table.

    Args:
        con: Active DuckDB connection.
        table: Table name to count.

    Returns:
        Integer row count.
    """
    row = con.execute(_COUNT_QUERY.format(table=table)).fetchone()
    assert row is not None
    return int(row[0])


def load_matches_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    *,
    should_drop: bool = True,
) -> int:
    """Materialise matches_raw from all weekly match parquet files.

    Args:
        con: Active DuckDB connection.
        raw_dir: Path to the raw data directory (contains matches/ subdir).
        should_drop: If True, drop existing matches_raw before creating.

    Returns:
        Row count in matches_raw after ingestion.
    """
    if should_drop:
        con.execute(_DROP_IF_EXISTS_QUERY.format(table="matches_raw"))
        logger.info("Dropped existing matches_raw table.")

    glob = str(raw_dir / "matches" / "*_matches.parquet")
    con.execute(_MATCHES_RAW_QUERY.format(glob=glob))
    _relativize_filenames(con, "matches_raw", raw_dir)
    n = _count_rows(con, "matches_raw")
    logger.info("matches_raw: %d rows from %s", n, glob)
    return n


def load_players_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    *,
    should_drop: bool = True,
) -> int:
    """Materialise players_raw from all weekly player parquet files.

    Args:
        con: Active DuckDB connection.
        raw_dir: Path to the raw data directory (contains players/ subdir).
        should_drop: If True, drop existing players_raw before creating.

    Returns:
        Row count in players_raw after ingestion.
    """
    if should_drop:
        con.execute(_DROP_IF_EXISTS_QUERY.format(table="players_raw"))
        logger.info("Dropped existing players_raw table.")

    glob = str(raw_dir / "players" / "*_players.parquet")
    con.execute(_PLAYERS_RAW_QUERY.format(glob=glob))
    _relativize_filenames(con, "players_raw", raw_dir)
    n = _count_rows(con, "players_raw")
    logger.info("players_raw: %d rows from %s", n, glob)
    return n


def load_overviews_raw(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    *,
    should_drop: bool = True,
) -> int:
    """Materialise overviews_raw from the singleton overview JSON.

    Args:
        con: Active DuckDB connection.
        raw_dir: Path to the raw data directory (contains overview/ subdir).
        should_drop: If True, drop existing overviews_raw before creating.

    Returns:
        Row count in overviews_raw after ingestion.
    """
    if should_drop:
        con.execute(_DROP_IF_EXISTS_QUERY.format(table="overviews_raw"))
        logger.info("Dropped existing overviews_raw table.")

    path = str(raw_dir / "overview" / "overview.json")
    con.execute(_OVERVIEWS_RAW_QUERY.format(path=path))
    _relativize_filenames(con, "overviews_raw", raw_dir)
    n = _count_rows(con, "overviews_raw")
    logger.info("overviews_raw: %d rows from %s", n, path)
    return n


def load_all_raw_tables(
    con: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    *,
    should_drop: bool = True,
) -> dict[str, int]:
    """Materialise all three raw tables in the aoestats DuckDB.

    Args:
        con: Active DuckDB connection.
        raw_dir: Path to the raw data directory.
        should_drop: Passed through to each individual loader.

    Returns:
        Dict mapping table name to row count.
    """
    counts: dict[str, int] = {}
    counts["matches_raw"] = load_matches_raw(con, raw_dir, should_drop=should_drop)
    counts["players_raw"] = load_players_raw(con, raw_dir, should_drop=should_drop)
    counts["overviews_raw"] = load_overviews_raw(con, raw_dir, should_drop=should_drop)
    logger.info("load_all_raw_tables complete: %s", counts)
    return counts
