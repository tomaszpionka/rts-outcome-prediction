"""Tests for aoe2companion pre_ingestion.py — binary inspection, ingestion."""

from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rts_predict.games.aoe2.datasets.aoe2companion.pre_ingestion import (
    check_ratings_types,
    count_won_nulls,
    find_date_gap,
    ingest_leaderboards_raw,
    ingest_matches_raw,
    ingest_profiles_raw,
    ingest_ratings_raw,
    inspect_binary_columns,
    run_smoke_test,
    verify_tables,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _write_match_parquet(path: Path, *, n_rows: int = 3) -> None:
    """Write synthetic aoe2companion match parquet with binary columns."""
    table = pa.table({
        "matchId": pa.array(list(range(n_rows)), type=pa.int32()),
        "started": pa.array(
            [1704067200000 + i * 1000 for i in range(n_rows)],
            type=pa.timestamp("ms", tz="UTC"),
        ),
        "finished": pa.array(
            [1704070800000 + i * 1000 for i in range(n_rows)],
            type=pa.timestamp("ms", tz="UTC"),
        ),
        "leaderboard": pa.array([b"rm_1v1"] * n_rows, type=pa.binary()),
        "name": pa.array([b"TestGame"] * n_rows, type=pa.binary()),
        "profileId": pa.array([1000 + i for i in range(n_rows)], type=pa.int32()),
        "rating": pa.array([1400 + i for i in range(n_rows)], type=pa.int32()),
        "ratingDiff": pa.array([10] * n_rows, type=pa.int32()),
        "won": pa.array([True, False, None][:n_rows], type=pa.bool_()),
        "civ": pa.array([b"Britons"] * n_rows, type=pa.binary()),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)


def _write_rating_csv(path: Path, *, n_rows: int = 3) -> None:
    """Write synthetic aoe2companion rating CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["profile_id,games,rating,date,leaderboard_id,rating_diff,season"]
    for i in range(n_rows):
        lines.append(
            f"{1000+i},{50+i},{1400+i},2024-01-01 10:00:00,3,{10+i},1"
        )
    path.write_text("\n".join(lines) + "\n")


def _write_leaderboard_parquet(path: Path, *, n_rows: int = 3) -> None:
    """Write synthetic leaderboard parquet."""
    table = pa.table({
        "leaderboard": pa.array([b"rm_1v1"] * n_rows, type=pa.binary()),
        "profileId": pa.array(list(range(n_rows)), type=pa.int32()),
        "name": pa.array([b"Player"] * n_rows, type=pa.binary()),
        "rank": pa.array(list(range(1, n_rows + 1)), type=pa.int32()),
        "rating": pa.array([1400 + i for i in range(n_rows)], type=pa.int32()),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)


def _write_profile_parquet(path: Path, *, n_rows: int = 3) -> None:
    """Write synthetic profile parquet."""
    table = pa.table({
        "profileId": pa.array(list(range(n_rows)), type=pa.int32()),
        "steamId": pa.array([b"steam123"] * n_rows, type=pa.binary()),
        "name": pa.array([b"Player"] * n_rows, type=pa.binary()),
        "country": pa.array([b"US"] * n_rows, type=pa.binary()),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)


@pytest.fixture()
def companion_raw_dir(tmp_path: Path) -> Path:
    """Create synthetic aoe2companion raw directory."""
    raw = tmp_path / "raw"

    _write_match_parquet(raw / "matches" / "match-2024-01-01.parquet")
    _write_match_parquet(raw / "matches" / "match-2024-01-02.parquet")

    _write_rating_csv(raw / "ratings" / "rating-2024-01-01.csv")
    # Intentionally skip rating-2024-01-02.csv to test date gap

    _write_leaderboard_parquet(
        raw / "leaderboards" / "leaderboard.parquet",
    )
    _write_profile_parquet(raw / "profiles" / "profile.parquet")

    return raw


@pytest.fixture()
def companion_db_con() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB connection."""
    return duckdb.connect(":memory:")


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestBinaryInspection:
    """Tests for inspect_binary_columns."""

    def test_detects_binary_columns(self, companion_raw_dir: Path) -> None:
        """Should detect binary columns in matches parquet."""
        result = inspect_binary_columns(companion_raw_dir)
        assert "matches" in result
        assert result["matches"]["binary_column_count"] > 0

    def test_leaderboard_binary(self, companion_raw_dir: Path) -> None:
        """Should detect binary columns in leaderboards."""
        result = inspect_binary_columns(companion_raw_dir)
        assert result["leaderboards"]["binary_column_count"] > 0


class TestSmokeTest:
    """Tests for run_smoke_test."""

    def test_smoke_returns_results(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """Smoke test should return results for matches and ratings."""
        results = run_smoke_test(companion_db_con, companion_raw_dir)
        assert "matches" in results
        assert "ratings" in results
        assert results["matches"]["row_count"] > 0
        assert results["ratings"]["row_count"] > 0


class TestFullIngestion:
    """Tests for all 4 ingest functions."""

    def test_matches_raw(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """matches_raw should exist with filename column."""
        n = ingest_matches_raw(companion_db_con, companion_raw_dir)
        assert n == 6  # 3 rows x 2 files  # noqa: PLR2004
        cols = [
            r[0]
            for r in companion_db_con.execute(
                "DESCRIBE matches_raw"
            ).fetchall()
        ]
        assert "filename" in cols

    def test_ratings_raw_explicit_types(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """ratings_raw with explicit types should have BIGINT profile_id."""
        n = ingest_ratings_raw(
            companion_db_con, companion_raw_dir, use_explicit_types=True,
        )
        assert n > 0
        types = check_ratings_types(companion_db_con)
        assert types["profile_id"] == "BIGINT"
        assert types["date"] == "TIMESTAMP"

    def test_leaderboards_raw(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """leaderboards_raw should exist."""
        n = ingest_leaderboards_raw(companion_db_con, companion_raw_dir)
        assert n > 0

    def test_profiles_raw(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """profiles_raw should exist."""
        n = ingest_profiles_raw(companion_db_con, companion_raw_dir)
        assert n > 0


class TestVerification:
    """Tests for verify_tables, count_won_nulls, check_ratings_types."""

    def test_verify_all_tables(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """verify_tables should return all 4 tables."""
        ingest_matches_raw(companion_db_con, companion_raw_dir)
        ingest_ratings_raw(
            companion_db_con, companion_raw_dir, use_explicit_types=True,
        )
        ingest_leaderboards_raw(companion_db_con, companion_raw_dir)
        ingest_profiles_raw(companion_db_con, companion_raw_dir)

        result = verify_tables(companion_db_con)
        assert len(result) == 4  # noqa: PLR2004

    def test_won_nulls(
        self,
        companion_db_con: duckdb.DuckDBPyConnection,
        companion_raw_dir: Path,
    ) -> None:
        """count_won_nulls should report NULL count."""
        ingest_matches_raw(companion_db_con, companion_raw_dir)
        wn = count_won_nulls(companion_db_con)
        assert wn["total"] == 6  # noqa: PLR2004
        # We wrote [True, False, None] x 2 files
        assert wn["null_count"] == 2  # noqa: PLR2004


class TestDateGap:
    """Tests for find_date_gap."""

    def test_finds_missing_date(self, companion_raw_dir: Path) -> None:
        """Should find 2024-01-02 in matches but not ratings."""
        gap = find_date_gap(companion_raw_dir)
        assert gap["matches_date_count"] == 2  # noqa: PLR2004
        assert gap["ratings_date_count"] == 1
        assert "2024-01-02" in gap["in_matches_not_ratings"]
