"""Tests for aoestats pre_ingestion.py — variant census, smoke test, ingestion."""

import json
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rts_predict.games.aoe2.datasets.aoestats.pre_ingestion import (
    check_duration_type,
    find_missing_weeks,
    ingest_matches_raw,
    ingest_overviews_raw,
    ingest_players_raw,
    run_smoke_test,
    run_variant_census,
    verify_tables,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _write_matches_parquet(
    path: Path,
    *,
    n_rows: int = 3,
    raw_match_type_as_double: bool = False,
    ts_as_ns: bool = False,
) -> None:
    """Write a synthetic aoestats matches parquet with realistic columns."""
    ts_type = pa.timestamp("ns", tz="UTC") if ts_as_ns else pa.timestamp("us", tz="UTC")
    rmt_type = pa.float64() if raw_match_type_as_double else pa.int64()

    table = pa.table({
        "map": pa.array(["Arabia"] * n_rows, type=pa.string()),
        "started_timestamp": pa.array(
            [1704067200000000 + i * 1000000 for i in range(n_rows)],
            type=ts_type,
        ),
        "duration": pa.array(
            [2000000000000 + i * 100000000 for i in range(n_rows)],
            type=pa.duration("ns"),
        ),
        "irl_duration": pa.array(
            [1500000000000 + i * 100000000 for i in range(n_rows)],
            type=pa.duration("ns"),
        ),
        "game_id": pa.array([f"game_{i}" for i in range(n_rows)], type=pa.string()),
        "avg_elo": pa.array([1400.0 + i for i in range(n_rows)], type=pa.float64()),
        "num_players": pa.array([2] * n_rows, type=pa.int64()),
        "team_0_elo": pa.array([1400.0] * n_rows, type=pa.float64()),
        "team_1_elo": pa.array([1400.0] * n_rows, type=pa.float64()),
        "replay_enhanced": pa.array([True] * n_rows, type=pa.bool_()),
        "leaderboard": pa.array(["rm_1v1"] * n_rows, type=pa.string()),
        "mirror": pa.array([False] * n_rows, type=pa.bool_()),
        "patch": pa.array([100] * n_rows, type=pa.int64()),
        "raw_match_type": pa.array([6] * n_rows, type=rmt_type),
        "game_type": pa.array(["1v1"] * n_rows, type=pa.string()),
        "game_speed": pa.array(["Normal"] * n_rows, type=pa.string()),
        "starting_age": pa.array(["Dark"] * n_rows, type=pa.string()),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)


def _write_players_parquet(
    path: Path,
    *,
    n_rows: int = 6,
    profile_id_as_double: bool = False,
    include_uptimes: bool = True,
) -> None:
    """Write a synthetic aoestats players parquet with realistic columns."""
    pid_type = pa.float64() if profile_id_as_double else pa.int64()

    columns: dict[str, pa.Array] = {
        "winner": pa.array([True, False] * (n_rows // 2), type=pa.bool_()),
        "game_id": pa.array([f"game_{i // 2}" for i in range(n_rows)], type=pa.string()),
        "team": pa.array([0, 1] * (n_rows // 2), type=pa.int64()),
        "old_rating": pa.array([1400 + i for i in range(n_rows)], type=pa.int64()),
        "new_rating": pa.array([1410 + i for i in range(n_rows)], type=pa.int64()),
        "match_rating_diff": pa.array([10.0] * n_rows, type=pa.float64()),
        "replay_summary_raw": pa.array(["raw"] * n_rows, type=pa.string()),
        "profile_id": pa.array(
            [1000 + i for i in range(n_rows)],
            type=pid_type,
        ),
        "civ": pa.array(["Britons"] * n_rows, type=pa.string()),
    }

    if include_uptimes:
        columns["feudal_age_uptime"] = pa.array(
            [600.0 + i for i in range(n_rows)], type=pa.float64(),
        )
        columns["castle_age_uptime"] = pa.array(
            [1200.0 + i for i in range(n_rows)], type=pa.float64(),
        )
        columns["imperial_age_uptime"] = pa.array(
            [1800.0 + i for i in range(n_rows)], type=pa.float64(),
        )
        columns["opening"] = pa.array(["drush"] * n_rows, type=pa.string())
    # When include_uptimes=False, these columns are omitted entirely
    # (simulating null-typed columns via union_by_name)

    table = pa.table(columns)
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path)


@pytest.fixture()
def aoestats_raw_dir(tmp_path: Path) -> Path:
    """Create synthetic aoestats raw dir with variant columns."""
    raw = tmp_path / "raw"

    # 2 matches files: one with int64 raw_match_type, one with double
    _write_matches_parquet(
        raw / "matches" / "2024-01-01_2024-01-07_matches.parquet",
        raw_match_type_as_double=False,
    )
    _write_matches_parquet(
        raw / "matches" / "2024-01-08_2024-01-14_matches.parquet",
        raw_match_type_as_double=True,
        ts_as_ns=True,
    )

    # 2 players files: one with uptimes, one without (variant)
    _write_players_parquet(
        raw / "players" / "2024-01-01_2024-01-07_players.parquet",
        include_uptimes=True,
    )
    _write_players_parquet(
        raw / "players" / "2024-01-08_2024-01-14_players.parquet",
        include_uptimes=False,
        profile_id_as_double=True,
    )

    # Overview JSON
    overview_dir = raw / "overview"
    overview_dir.mkdir(parents=True)
    overview = {
        "last_updated": "2026-04-09T11:12:40.159034Z",
        "total_match_count": 100,
        "civs": [{"name": "Britons", "value": 50}],
        "openings": [{"name": "drush", "value": 30}],
        "patches": [],
        "groupings": [],
        "changelog": [],
        "tournament_stages": [],
    }
    (overview_dir / "overview.json").write_text(json.dumps(overview))

    return raw


@pytest.fixture()
def aoestats_db_con() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB connection for aoestats tests."""
    return duckdb.connect(":memory:")


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestVariantCensus:
    """Tests for run_variant_census."""

    def test_detects_variant_columns(self, aoestats_raw_dir: Path) -> None:
        """Census should detect raw_match_type as variant in matches."""
        census = run_variant_census(aoestats_raw_dir)
        assert "raw_match_type" in census["matches"]["variant_columns"]

    def test_all_columns_counted(self, aoestats_raw_dir: Path) -> None:
        """Census should report all columns."""
        census = run_variant_census(aoestats_raw_dir)
        assert len(census["matches"]["all_columns"]) == 17  # noqa: PLR2004
        assert census["matches"]["total_files"] == 2  # noqa: PLR2004

    def test_players_variant_detection(self, aoestats_raw_dir: Path) -> None:
        """Census should detect profile_id as variant in players."""
        census = run_variant_census(aoestats_raw_dir)
        assert "profile_id" in census["players"]["variant_columns"]


class TestSmokeTest:
    """Tests for run_smoke_test."""

    def test_smoke_returns_results(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """Smoke test should return results for both subdirs."""
        results = run_smoke_test(aoestats_db_con, aoestats_raw_dir)
        assert "matches" in results
        assert "players" in results
        assert results["matches"]["row_count"] > 0
        assert results["players"]["row_count"] > 0

    def test_smoke_cleans_up_temp_tables(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """Temp tables should be dropped after smoke test."""
        run_smoke_test(aoestats_db_con, aoestats_raw_dir)
        tables = [
            r[0] for r in aoestats_db_con.execute("SHOW TABLES").fetchall()
        ]
        assert "smoke_matches_raw" not in tables
        assert "smoke_players_raw" not in tables


class TestFullIngestion:
    """Tests for ingest_matches_raw, ingest_players_raw, ingest_overviews_raw."""

    def test_matches_raw_created(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """matches_raw should exist with filename column."""
        n = ingest_matches_raw(aoestats_db_con, aoestats_raw_dir)
        assert n == 6  # 3 rows x 2 files  # noqa: PLR2004
        cols = [
            r[0]
            for r in aoestats_db_con.execute("DESCRIBE matches_raw").fetchall()
        ]
        assert "filename" in cols
        assert "map" in cols

    def test_players_raw_created(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """players_raw should exist with union_by_name columns."""
        n = ingest_players_raw(aoestats_db_con, aoestats_raw_dir)
        assert n == 12  # 6 rows x 2 files  # noqa: PLR2004
        cols = [
            r[0]
            for r in aoestats_db_con.execute("DESCRIBE players_raw").fetchall()
        ]
        assert "filename" in cols
        assert "profile_id" in cols

    def test_overviews_raw_created(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """overviews_raw should have 1 row."""
        n = ingest_overviews_raw(aoestats_db_con, aoestats_raw_dir)
        assert n == 1


class TestVerification:
    """Tests for verify_tables and check_duration_type."""

    def test_verify_returns_all_tables(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """verify_tables should return results for all 3 tables."""
        ingest_matches_raw(aoestats_db_con, aoestats_raw_dir)
        ingest_players_raw(aoestats_db_con, aoestats_raw_dir)
        ingest_overviews_raw(aoestats_db_con, aoestats_raw_dir)

        result = verify_tables(aoestats_db_con)
        assert "matches_raw" in result
        assert "players_raw" in result
        assert "overviews_raw" in result
        assert result["matches_raw"]["row_count"] > 0

    def test_duration_type_is_bigint(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """Duration columns should be BIGINT (Arrow duration[ns] -> BIGINT)."""
        ingest_matches_raw(aoestats_db_con, aoestats_raw_dir)
        dur = check_duration_type(aoestats_db_con)
        assert dur["duration"]["typeof"] == "BIGINT"
        assert dur["irl_duration"]["typeof"] == "BIGINT"


class TestMissingWeeks:
    """Tests for find_missing_weeks."""

    def test_no_missing_weeks_when_matched(
        self,
        aoestats_db_con: duckdb.DuckDBPyConnection,
        aoestats_raw_dir: Path,
    ) -> None:
        """With matching weeks, both gaps should be empty."""
        ingest_matches_raw(aoestats_db_con, aoestats_raw_dir)
        ingest_players_raw(aoestats_db_con, aoestats_raw_dir)
        missing = find_missing_weeks(aoestats_db_con)
        assert missing["matches_week_count"] == 2  # noqa: PLR2004
        assert missing["players_week_count"] == 2  # noqa: PLR2004
        # Both should match because our fixture has same weeks
        assert missing["in_matches_not_players"] == []
        assert missing["in_players_not_matches"] == []
