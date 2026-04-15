"""Unit tests for rts_predict.common.eda_census."""
import duckdb
import pytest

from rts_predict.common.eda_census import (
    _is_boolean_type,
    _is_complex_type,
    _is_numeric_type,
    _is_timestamp_type,
    _serialize_value,
    profile_column,
    profile_table,
)


@pytest.fixture
def census_db():
    """In-memory DuckDB with columns covering every type dispatch branch."""
    con = duckdb.connect(":memory:")
    con.execute("""
        CREATE TABLE test_table (
            id INTEGER,
            name VARCHAR,
            score DOUBLE,
            is_active BOOLEAN,
            created_at TIMESTAMP,
            tags VARCHAR[],
            metadata STRUCT(key VARCHAR, val INTEGER)
        )
    """)
    con.execute("""
        INSERT INTO test_table VALUES
            (1, 'alice', 100.0, TRUE,  '2024-01-01'::TIMESTAMP, ['a','b'], {'key':'x','val':1}),
            (2, 'bob',   0.0,   FALSE, '2024-06-15'::TIMESTAMP, ['c'],     {'key':'y','val':2}),
            (3, 'alice', 95.5,  TRUE,  '2024-12-31'::TIMESTAMP, ['a'],     {'key':'x','val':3}),
            (NULL, NULL, NULL,  NULL,  NULL,                    NULL,      NULL),
            (4, 'carol', 0.0,   FALSE, '2024-03-20'::TIMESTAMP, [],        {'key':'z','val':4})
    """)
    yield con
    con.close()


@pytest.fixture
def empty_db():
    """In-memory DuckDB with a table containing 0 rows."""
    con = duckdb.connect(":memory:")
    con.execute("CREATE TABLE empty_table (id INTEGER, name VARCHAR)")
    yield con
    con.close()


@pytest.fixture
def single_row_db():
    """In-memory DuckDB with a single-row table (mimics aoestats overviews_raw)."""
    con = duckdb.connect(":memory:")
    con.execute("CREATE TABLE one_row (metric VARCHAR, value BIGINT)")
    con.execute("INSERT INTO one_row VALUES ('total_matches', 1000000)")
    yield con
    con.close()


@pytest.fixture
def all_null_db():
    """In-memory DuckDB with a column where all values are NULL."""
    con = duckdb.connect(":memory:")
    con.execute("CREATE TABLE null_table (id INTEGER, notes VARCHAR)")
    con.execute("INSERT INTO null_table VALUES (1, NULL), (2, NULL), (3, NULL)")
    yield con
    con.close()


# ── Type classification helpers ────────────────────────────────────────────────

class TestTypeClassification:
    def test_complex_struct(self):
        assert _is_complex_type("STRUCT(a INT)") is True

    def test_complex_struct_array(self):
        assert _is_complex_type("STRUCT(a INT)[]") is True

    def test_complex_varchar_array(self):
        assert _is_complex_type("VARCHAR[]") is True

    def test_complex_map(self):
        assert _is_complex_type("MAP(VARCHAR, INTEGER)") is True

    def test_not_complex_varchar(self):
        assert _is_complex_type("VARCHAR") is False

    def test_not_complex_integer(self):
        assert _is_complex_type("INTEGER") is False

    def test_numeric_integer(self):
        assert _is_numeric_type("INTEGER") is True

    def test_numeric_bigint(self):
        assert _is_numeric_type("BIGINT") is True

    def test_numeric_decimal(self):
        assert _is_numeric_type("DECIMAL(10,2)") is True

    def test_numeric_double(self):
        assert _is_numeric_type("DOUBLE") is True

    def test_not_numeric_varchar(self):
        assert _is_numeric_type("VARCHAR") is False

    def test_not_numeric_boolean(self):
        assert _is_numeric_type("BOOLEAN") is False

    def test_boolean_true(self):
        assert _is_boolean_type("BOOLEAN") is True

    def test_boolean_bool_alias(self):
        assert _is_boolean_type("BOOL") is True

    def test_not_boolean(self):
        assert _is_boolean_type("INTEGER") is False

    def test_timestamp(self):
        assert _is_timestamp_type("TIMESTAMP") is True

    def test_date(self):
        assert _is_timestamp_type("DATE") is True

    def test_not_timestamp_varchar(self):
        assert _is_timestamp_type("VARCHAR") is False

    def test_timestamp_with_tz(self):
        assert _is_timestamp_type("TIMESTAMP WITH TIME ZONE") is True

    def test_timestamptz_alias(self):
        assert _is_timestamp_type("TIMESTAMPTZ") is True


# ── _serialize_value ─────────────────────────────────────────────────────────

class TestSerializeValue:
    def test_none(self):
        assert _serialize_value(None) is None

    def test_bool(self):
        assert _serialize_value(True) is True
        assert _serialize_value(False) is False

    def test_int(self):
        assert _serialize_value(42) == 42

    def test_float(self):
        assert _serialize_value(3.14) == 3.14

    def test_str(self):
        assert _serialize_value("hello") == "hello"

    def test_datetime(self):
        from datetime import datetime
        val = datetime(2024, 1, 1, 12, 0, 0)
        result = _serialize_value(val)
        assert isinstance(result, str)
        assert "2024-01-01" in result


# ── profile_column ────────────────────────────────────────────────────────────

class TestProfileColumnNumeric:
    def test_null_count(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["null_count"] == 1
        assert p["null_pct"] > 0

    def test_cardinality(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["cardinality"] == 4

    def test_zero_count(self, census_db):
        p = profile_column(census_db, "test_table", "score", "DOUBLE")
        assert p["zero_count"] == 2
        assert p["zero_pct"] > 0

    def test_top_n_structure(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["top_n"] is not None
        assert len(p["top_n"]) <= 5
        for entry in p["top_n"]:
            assert "value" in entry
            assert "count" in entry
            assert "pct" in entry

    def test_bottom_n_structure(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["bottom_n"] is not None
        assert len(p["bottom_n"]) <= 4  # NULL excluded, 4 distinct values

    def test_sql_captured(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["sql_null"] is not None and len(p["sql_null"]) > 0
        assert p["sql_top_n"] is not None and len(p["sql_top_n"]) > 0
        assert p["sql_bottom_n"] is not None and len(p["sql_bottom_n"]) > 0

    def test_elapsed_seconds(self, census_db):
        p = profile_column(census_db, "test_table", "id", "INTEGER")
        assert p["elapsed_seconds"] is not None
        assert p["elapsed_seconds"] >= 0


class TestProfileColumnVarchar:
    def test_null_count(self, census_db):
        p = profile_column(census_db, "test_table", "name", "VARCHAR")
        assert p["null_count"] == 1

    def test_cardinality(self, census_db):
        p = profile_column(census_db, "test_table", "name", "VARCHAR")
        assert p["cardinality"] == 3  # alice, bob, carol

    def test_no_zero_count(self, census_db):
        p = profile_column(census_db, "test_table", "name", "VARCHAR")
        assert p["zero_count"] is None

    def test_top_n_most_common(self, census_db):
        p = profile_column(census_db, "test_table", "name", "VARCHAR")
        assert p["top_n"][0]["value"] == "alice"
        assert p["top_n"][0]["count"] == 2

    def test_bottom_n_least_common(self, census_db):
        p = profile_column(census_db, "test_table", "name", "VARCHAR")
        bottom_values = {e["value"] for e in p["bottom_n"]}
        assert "bob" in bottom_values or "carol" in bottom_values


class TestProfileColumnBoolean:
    def test_cardinality(self, census_db):
        p = profile_column(census_db, "test_table", "is_active", "BOOLEAN")
        assert p["cardinality"] == 2

    def test_no_zero_count(self, census_db):
        p = profile_column(census_db, "test_table", "is_active", "BOOLEAN")
        assert p["zero_count"] is None

    def test_top_n_contains_bool_values(self, census_db):
        p = profile_column(census_db, "test_table", "is_active", "BOOLEAN")
        top_values = {e["value"] for e in p["top_n"]}
        assert True in top_values or False in top_values


class TestProfileColumnTimestamp:
    def test_temporal_range(self, census_db):
        p = profile_column(census_db, "test_table", "created_at", "TIMESTAMP")
        assert p["temporal_range"] is not None
        assert "2024-01-01" in p["temporal_range"]["min"]
        assert "2024-12-31" in p["temporal_range"]["max"]

    def test_no_zero_count(self, census_db):
        p = profile_column(census_db, "test_table", "created_at", "TIMESTAMP")
        assert p["zero_count"] is None


class TestProfileColumnTimestampTZ:
    """TIMESTAMP WITH TIME ZONE must not require pytz (DuckDB ^1.5 regression guard)."""

    @pytest.fixture
    def tz_db(self):
        con = duckdb.connect(":memory:")
        con.execute("""
            CREATE TABLE tz_table (
                ts TIMESTAMPTZ
            )
        """)
        con.execute("""
            INSERT INTO tz_table VALUES
                (TIMESTAMPTZ '2024-01-01 10:00:00+00'),
                (TIMESTAMPTZ '2024-06-15 14:30:00+00'),
                (TIMESTAMPTZ '2024-01-01 10:00:00+00')
        """)
        yield con
        con.close()

    def test_temporal_range_no_pytz(self, tz_db: duckdb.DuckDBPyConnection) -> None:
        p = profile_column(tz_db, "tz_table", "ts", "TIMESTAMP WITH TIME ZONE")
        assert p["temporal_range"] is not None
        assert p["temporal_range"]["min"] is not None
        assert p["temporal_range"]["max"] is not None

    def test_top_n_no_pytz(self, tz_db: duckdb.DuckDBPyConnection) -> None:
        p = profile_column(tz_db, "tz_table", "ts", "TIMESTAMP WITH TIME ZONE")
        assert p["top_n"] is not None
        assert len(p["top_n"]) == 2  # two distinct values
        assert p["top_n"][0]["count"] == 2  # most frequent first

    def test_timestamptz_alias(self, tz_db: duckdb.DuckDBPyConnection) -> None:
        p = profile_column(tz_db, "tz_table", "ts", "TIMESTAMPTZ")
        assert p["temporal_range"] is not None
        assert p["top_n"] is not None


class TestProfileColumnComplex:
    def test_varchar_array_cardinality_none(self, census_db):
        p = profile_column(census_db, "test_table", "tags", "VARCHAR[]")
        assert p["cardinality"] is None

    def test_varchar_array_top_n_none(self, census_db):
        p = profile_column(census_db, "test_table", "tags", "VARCHAR[]")
        assert p["top_n"] is None
        assert p["bottom_n"] is None

    def test_varchar_array_has_array_length(self, census_db):
        p = profile_column(census_db, "test_table", "tags", "VARCHAR[]")
        assert "array_length" in p
        assert p["array_length"] is not None

    def test_struct_cardinality_none(self, census_db):
        p = profile_column(
            census_db, "test_table", "metadata", "STRUCT(key VARCHAR, val INTEGER)"
        )
        assert p["cardinality"] is None
        assert p["top_n"] is None
        assert "analytical_note" in p
        assert "STRUCT" in p["analytical_note"] or "MAP" in p["analytical_note"]


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_empty_table_integer(self, empty_db):
        p = profile_column(empty_db, "empty_table", "id", "INTEGER")
        assert p["null_count"] == 0
        assert p["cardinality"] == 0
        assert p["top_n"] == []
        assert p["bottom_n"] == []

    def test_empty_table_varchar(self, empty_db):
        p = profile_column(empty_db, "empty_table", "name", "VARCHAR")
        assert p["null_count"] == 0
        assert p["cardinality"] == 0
        assert p["top_n"] == []
        assert p["bottom_n"] == []

    def test_single_row_cardinality(self, single_row_db):
        p = profile_column(single_row_db, "one_row", "value", "BIGINT")
        assert p["cardinality"] == 1
        assert len(p["top_n"]) == 1
        assert len(p["bottom_n"]) == 1


class TestAllNullColumn:
    def test_null_count_equals_total(self, all_null_db):
        p = profile_column(all_null_db, "null_table", "notes", "VARCHAR")
        assert p["null_count"] == 3
        assert p["null_pct"] == 100.0

    def test_cardinality_zero(self, all_null_db):
        p = profile_column(all_null_db, "null_table", "notes", "VARCHAR")
        assert p["cardinality"] == 0

    def test_top_n_contains_null(self, all_null_db):
        p = profile_column(all_null_db, "null_table", "notes", "VARCHAR")
        assert p["top_n"] is not None
        assert p["top_n"][0]["value"] is None

    def test_bottom_n_empty(self, all_null_db):
        p = profile_column(all_null_db, "null_table", "notes", "VARCHAR")
        assert p["bottom_n"] == []


# ── profile_table ─────────────────────────────────────────────────────────────

class TestProfileTable:
    def test_returns_profiles_and_sql_registry(self, census_db):
        specs = [
            {"name": "id", "dtype": "INTEGER"},
            {"name": "name", "dtype": "VARCHAR"},
        ]
        result = profile_table(census_db, "test_table", specs)
        assert "profiles" in result
        assert "sql_registry" in result

    def test_profiles_all_columns(self, census_db):
        specs = [
            {"name": "id", "dtype": "INTEGER"},
            {"name": "name", "dtype": "VARCHAR"},
            {"name": "score", "dtype": "DOUBLE"},
        ]
        result = profile_table(census_db, "test_table", specs)
        assert set(result["profiles"].keys()) == {"id", "name", "score"}

    def test_sql_registry_has_all_columns(self, census_db):
        specs = [
            {"name": "id", "dtype": "INTEGER"},
            {"name": "name", "dtype": "VARCHAR"},
        ]
        result = profile_table(census_db, "test_table", specs)
        for col in ["id", "name"]:
            assert col in result["sql_registry"]
            assert "sql_null" in result["sql_registry"][col]
            assert "sql_top_n" in result["sql_registry"][col]
            assert "sql_bottom_n" in result["sql_registry"][col]

    def test_all_profiles_have_required_keys(self, census_db):
        specs = [{"name": "id", "dtype": "INTEGER"}]
        result = profile_table(census_db, "test_table", specs)
        required_keys = {
            "column", "dtype", "null_count", "null_pct", "cardinality",
            "top_n", "bottom_n", "elapsed_seconds",
        }
        for key in required_keys:
            assert key in result["profiles"]["id"]
