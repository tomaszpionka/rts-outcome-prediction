"""Shared EDA column-profiling utilities for DuckDB tables.

Game-agnostic. Produces a per-column profile dict containing null counts,
zero counts, cardinality, top-N / bottom-N most/least frequent values,
and temporal range. All SQL is captured for Invariant #6 artifact emission.

Usage in notebooks::

    from rts_predict.common.eda_census import profile_table
    specs = [{"name": r["column_name"], "dtype": r["column_type"]}
             for _, r in con.execute("DESCRIBE my_table").df().iterrows()]
    result = profile_table(con, "my_table", specs)
    findings["my_table_census"] = result["profiles"]
    for col, sqls in result["sql_registry"].items():
        sql_queries[f"census.my_table.{col}.null"] = sqls["sql_null"]
        sql_queries[f"census.my_table.{col}.top_n"] = sqls["sql_top_n"]
        sql_queries[f"census.my_table.{col}.bottom_n"] = sqls["sql_bottom_n"]

See also: .claude/scientific-invariants.md (Invariant #6, #7).
"""

from __future__ import annotations

import logging
import time
from typing import Any

import duckdb

logger = logging.getLogger(__name__)

# ── DuckDB type classification ────────────────────────────────────────────────

_COMPLEX_TYPE_PREFIXES: tuple[str, ...] = ("STRUCT", "MAP")
_COMPLEX_TYPE_SUFFIXES: tuple[str, ...] = ("[]",)


def _is_complex_type(dtype: str) -> bool:
    """Return True if dtype is a STRUCT, MAP, or array type."""
    dtype_upper = dtype.upper().strip()
    if any(dtype_upper.startswith(p) for p in _COMPLEX_TYPE_PREFIXES):
        return True
    if any(dtype_upper.endswith(s) for s in _COMPLEX_TYPE_SUFFIXES):
        return True
    return False


def _is_numeric_type(dtype: str) -> bool:
    """Return True if dtype is a numeric scalar (integer, float, decimal)."""
    dtype_upper = dtype.upper().strip()
    numeric_keywords = (
        "TINYINT", "SMALLINT", "INTEGER", "BIGINT", "HUGEINT",
        "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC", "REAL",
        "INT", "INT1", "INT2", "INT4", "INT8",
        "UTINYINT", "USMALLINT", "UINTEGER", "UBIGINT",
    )
    base_type = dtype_upper.split("(")[0].strip()
    return base_type in numeric_keywords


def _is_boolean_type(dtype: str) -> bool:
    """Return True if dtype is BOOLEAN."""
    return dtype.upper().strip() in ("BOOLEAN", "BOOL")


def _is_timestamp_type(dtype: str) -> bool:
    """Return True if dtype is a timestamp or date type."""
    dtype_upper = dtype.upper().strip()
    return dtype_upper in (
        "TIMESTAMP", "TIMESTAMP WITH TIME ZONE", "TIMESTAMPTZ",
        "TIMESTAMP_S", "TIMESTAMP_MS", "TIMESTAMP_NS",
        "DATE", "TIME", "INTERVAL",
    )


# ── Core profiling ────────────────────────────────────────────────────────────

def _serialize_value(val: Any) -> Any:
    """Convert a DuckDB value to a JSON-serializable type."""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float, str)):
        return val
    if hasattr(val, "isoformat"):
        return val.isoformat()
    return str(val)


def profile_column(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    col_name: str,
    col_dtype: str,
    n_top: int = 5,
    skip_topn: bool = False,
) -> dict[str, Any]:
    """Profile a single column: nulls, zeros, cardinality, top/bottom-N, temporal range.

    Type dispatch:
    - STRUCT/LIST/array: null count only; array_length via LEN() for [] types;
      no top/bottom.
    - Numeric: null_count, cardinality, zero_count, top_n, bottom_n.
    - Boolean: null_count, cardinality, top_n (TRUE/FALSE split), bottom_n.
    - Timestamp/Date: adds temporal_range (min, max).
    - VARCHAR (any cardinality): null_count, cardinality, top_n, bottom_n.

    All SQL strings captured in return dict for Invariant #6.

    Args:
        con: Open DuckDB connection.
        table_name: DuckDB table or view name.
        col_name: Column name (double-quoted in SQL).
        col_dtype: DuckDB type string from DESCRIBE output.
        n_top: Number of top/bottom frequent values to return (default 5,
            per Tukey 1977 exploratory convention).
        skip_topn: If True, skip top_n/bottom_n profiling (null/cardinality
            still computed). Use for high-cardinality or semantically opaque
            columns where GROUP BY is prohibitively expensive or meaningless.

    Returns:
        Dict with null_count, null_pct, cardinality, zero_count, zero_pct,
        top_n, bottom_n, temporal_range, analytical_note, sql_null,
        sql_top_n, sql_bottom_n, elapsed_seconds.

        ``top_n`` pct is relative to total rows (including NULL rows);
        ``bottom_n`` pct is relative to non-NULL rows only. Intentional:
        top_n surfaces NULL dominance; bottom_n percentages reflect
        distribution of valid data.
    """
    result: dict[str, Any] = {
        "column": col_name,
        "dtype": col_dtype,
        "null_count": None,
        "null_pct": None,
        "cardinality": None,
        "zero_count": None,
        "zero_pct": None,
        "top_n": None,
        "bottom_n": None,
        "temporal_range": None,
        "analytical_note": None,
        "sql_null": None,
        "sql_top_n": None,
        "sql_bottom_n": None,
        "elapsed_seconds": None,
    }

    t_start = time.monotonic()
    is_complex = _is_complex_type(col_dtype)
    is_numeric = _is_numeric_type(col_dtype)
    is_timestamp = _is_timestamp_type(col_dtype)

    if is_complex:
        sql_null = (
            f'SELECT\n'
            f'    COUNT(*) AS total_rows,\n'
            f'    COUNT(*) - COUNT("{col_name}") AS null_count,\n'
            f'    ROUND(100.0 * (COUNT(*) - COUNT("{col_name}")) / '
            f'NULLIF(COUNT(*), 0), 4) AS null_pct\n'
            f'FROM {table_name}'
        )
        result["sql_null"] = sql_null
        row = con.execute(sql_null).fetchone()
        assert row is not None
        result["null_count"] = int(row[1])
        result["null_pct"] = float(row[2]) if row[2] is not None else 0.0
        result["cardinality"] = None
        result["zero_count"] = None

        is_array_type = col_dtype.upper().strip().endswith("[]")
        if is_array_type:
            len_sql = (
                f'SELECT\n'
                f'    MIN(LEN("{col_name}")) AS min_len,\n'
                f'    MAX(LEN("{col_name}")) AS max_len,\n'
                f'    ROUND(AVG(LEN("{col_name}")), 2) AS avg_len\n'
                f'FROM {table_name}\n'
                f'WHERE "{col_name}" IS NOT NULL'
            )
            result["sql_top_n"] = len_sql
            result["sql_bottom_n"] = "-- Skipped: array type; see array_length"
            try:
                len_row = con.execute(len_sql).fetchone()
                assert len_row is not None
                result["array_length"] = {
                    "min": int(len_row[0]) if len_row[0] is not None else None,
                    "max": int(len_row[1]) if len_row[1] is not None else None,
                    "avg": float(len_row[2]) if len_row[2] is not None else None,
                }
            except Exception as e:
                logger.warning("LEN() failed for %s.%s: %s", table_name, col_name, e)
                result["array_length"] = None
            result["analytical_note"] = (
                f"Array/LIST type ({col_dtype}): COUNT(DISTINCT) and GROUP BY "
                f"unsupported. Array element count (LEN) reported instead of top/bottom-N."
            )
        else:
            # Bare STRUCT or MAP type: LEN() not defined; null count only.
            result["sql_top_n"] = "-- Skipped: bare STRUCT/MAP type"
            result["sql_bottom_n"] = "-- Skipped: bare STRUCT/MAP type"
            result["array_length"] = None
            result["analytical_note"] = (
                f"Bare STRUCT/MAP type ({col_dtype}): COUNT(DISTINCT), GROUP BY, "
                f"and LEN() unsupported. Only null count profiled. "
                f"Field names available via DESCRIBE."
            )
    else:
        zero_clause = ""
        if is_numeric:
            zero_clause = (
                f',\n    COUNT(*) FILTER (WHERE "{col_name}" = 0) AS zero_count,\n'
                f'    ROUND(100.0 * COUNT(*) FILTER (WHERE "{col_name}" = 0) / '
                f'NULLIF(COUNT(*) FILTER (WHERE "{col_name}" IS NOT NULL), 0), '
                f'4) AS zero_pct'
            )

        temporal_clause = ""
        _is_tz_type = col_dtype.upper().strip() in (
            "TIMESTAMP WITH TIME ZONE", "TIMESTAMPTZ",
        )
        if is_timestamp:
            # For TZ-aware types, cast to TIMESTAMP to avoid pytz requirement
            # when DuckDB returns values to Python (DuckDB ^1.5).
            _ts_expr = (
                f'CAST("{col_name}" AS TIMESTAMP)' if _is_tz_type
                else f'"{col_name}"'
            )
            temporal_clause = (
                f',\n    MIN({_ts_expr}) AS temporal_min,\n'
                f'    MAX({_ts_expr}) AS temporal_max'
            )

        sql_null = (
            f'SELECT\n'
            f'    COUNT(*) AS total_rows,\n'
            f'    COUNT(*) - COUNT("{col_name}") AS null_count,\n'
            f'    ROUND(100.0 * (COUNT(*) - COUNT("{col_name}")) / '
            f'NULLIF(COUNT(*), 0), 4) AS null_pct,\n'
            f'    COUNT(DISTINCT "{col_name}") AS cardinality'
            f'{zero_clause}'
            f'{temporal_clause}\n'
            f'FROM {table_name}'
        )
        result["sql_null"] = sql_null
        row = con.execute(sql_null).fetchone()
        assert row is not None
        result["null_count"] = int(row[1])
        result["null_pct"] = float(row[2]) if row[2] is not None else 0.0
        result["cardinality"] = int(row[3])

        idx = 4
        if is_numeric:
            result["zero_count"] = int(row[idx])
            result["zero_pct"] = (
                float(row[idx + 1]) if row[idx + 1] is not None else 0.0
            )
            idx += 2

        if is_timestamp:
            result["temporal_range"] = {
                "min": str(row[idx]) if row[idx] is not None else None,
                "max": str(row[idx + 1]) if row[idx + 1] is not None else None,
            }

        # Top-N most frequent (includes NULL as a value)
        if skip_topn:
            result["top_n"] = None
            result["bottom_n"] = None
            result["sql_top_n"] = "-- Skipped: skip_topn=True"
            result["sql_bottom_n"] = "-- Skipped: skip_topn=True"
            result["analytical_note"] = (
                f"Column {col_name!r} excluded from top_n/bottom_n profiling "
                f"(skip_topn=True — high-cardinality or semantically opaque)."
            )
        else:
            # For TZ-aware timestamps, cast value to TIMESTAMP in SELECT/GROUP BY
            # so DuckDB returns naive datetimes to Python (no pytz needed).
            _val_expr = (
                f'CAST("{col_name}" AS TIMESTAMP)' if _is_tz_type
                else f'"{col_name}"'
            )
            sql_top = (
                f'SELECT\n'
                f'    {_val_expr} AS value,\n'
                f'    COUNT(*) AS cnt,\n'
                f'    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 4) AS pct\n'
                f'FROM {table_name}\n'
                f'GROUP BY "{col_name}"\n'
                f'ORDER BY cnt DESC, "{col_name}" ASC\n'
                f'LIMIT {n_top}'
            )
            result["sql_top_n"] = sql_top
            top_rows = con.execute(sql_top).fetchall()
            result["top_n"] = [
                {
                    "value": _serialize_value(r[0]),
                    "count": int(r[1]),
                    "pct": float(r[2]),
                }
                for r in top_rows
            ]

            # Bottom-N least frequent (non-NULL values only)
            sql_bottom = (
                f'SELECT\n'
                f'    {_val_expr} AS value,\n'
                f'    COUNT(*) AS cnt,\n'
                f'    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 4) AS pct\n'
                f'FROM {table_name}\n'
                f'WHERE "{col_name}" IS NOT NULL\n'
                f'GROUP BY "{col_name}"\n'
                f'ORDER BY cnt ASC, "{col_name}" ASC\n'
                f'LIMIT {n_top}'
            )
            result["sql_bottom_n"] = sql_bottom
            bottom_rows = con.execute(sql_bottom).fetchall()
            result["bottom_n"] = [
                {
                    "value": _serialize_value(r[0]),
                    "count": int(r[1]),
                    "pct": float(r[2]),
                }
                for r in bottom_rows
            ]

    result["elapsed_seconds"] = round(time.monotonic() - t_start, 2)
    return result


def profile_table(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    column_specs: list[dict[str, str]],
    n_top: int = 5,
    skip_topn_columns: set[str] | None = None,
) -> dict[str, Any]:
    """Profile all columns in a table or view.

    Args:
        con: Open DuckDB connection.
        table_name: DuckDB table or view name.
        column_specs: List of {"name": str, "dtype": str} dicts,
            typically from: [{"name": r["column_name"], "dtype": r["column_type"]}
                             for _, r in con.execute("DESCRIBE t").df().iterrows()]
        n_top: Number of top/bottom frequent values per column (default 5,
            per Tukey 1977 exploratory convention). Invariant #7: configurable,
            not a magic number.
        skip_topn_columns: Optional set of column names for which top_n/bottom_n
            profiling is skipped (null/cardinality still computed). Use for
            high-cardinality or semantically opaque columns (e.g. serialized
            JSON blobs) where GROUP BY is prohibitively expensive or meaningless.

    Returns:
        Dict with:
        - "profiles": {col_name: profile_column_result, ...}
        - "sql_registry": {col_name: {"sql_null": ..., "sql_top_n": ...,
          "sql_bottom_n": ...}, ...}
    """
    profiles: dict[str, Any] = {}
    sql_registry: dict[str, dict[str, str | None]] = {}

    for spec in column_specs:
        col_name = spec["name"]
        col_dtype = spec["dtype"]
        logger.info("Profiling %s.%s (%s)...", table_name, col_name, col_dtype)
        _skip = skip_topn_columns is not None and col_name in skip_topn_columns
        profile = profile_column(
            con, table_name, col_name, col_dtype, n_top, skip_topn=_skip,
        )
        profiles[col_name] = profile
        sql_registry[col_name] = {
            "sql_null": profile.get("sql_null"),
            "sql_top_n": profile.get("sql_top_n"),
            "sql_bottom_n": profile.get("sql_bottom_n"),
        }
        print(
            f"  {table_name}.{col_name} ({col_dtype}): "
            f"nulls={profile['null_count']}, "
            f"card={profile['cardinality']}, "
            f"elapsed={profile['elapsed_seconds']}s"
        )

    return {"profiles": profiles, "sql_registry": sql_registry}
