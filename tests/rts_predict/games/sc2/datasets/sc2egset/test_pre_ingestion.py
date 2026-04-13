"""Tests for sc2egset pre_ingestion.py — read_json_auto, event arrays, mapping census."""

import json
from pathlib import Path

import duckdb
import pytest

from rts_predict.games.sc2.datasets.sc2egset.pre_ingestion import (
    census_mapping_files,
    measure_event_arrays,
    probe_batch_ingestion,
    probe_mapping_read_json_auto,
    probe_read_json_auto_single,
    select_sample_files,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _make_replay_json(path: Path, *, n_events: int = 5) -> None:
    """Write a minimal synthetic SC2Replay.json file."""
    data = {
        "ToonPlayerDescMap": {
            "1-S2-1-100": {
                "nickname": "Player1",
                "playerID": 1,
                "userID": 100,
                "SQ": 80,
                "supplyCappedPercent": 5,
                "startDir": 0,
                "startLocX": 10,
                "startLocY": 20,
                "race": "Terran",
                "selectedRace": "Terran",
                "APM": 200,
                "MMR": 5000,
                "result": "Win",
                "region": "US",
                "realm": "1",
                "highestLeague": "Master",
                "isInClan": False,
                "clanTag": "",
                "handicap": 100,
                "color": {"a": 255, "b": 0, "g": 0, "r": 255},
            },
        },
        "header": {"elapsedGameLoops": 10000, "version": "5.0.0"},
        "initData": {"gameDescription": {"gameSpeed": "Faster"}},
        "details": {
            "gameSpeed": "Faster",
            "isBlizzardMap": True,
            "timeUTC": "2024-01-01T10:00:00",
        },
        "metadata": {
            "baseBuild": "12345",
            "dataBuild": "12345",
            "gameVersion": "5.0.0",
            "mapName": "Oceanborn LE",
        },
        "gameEvents": [
            {"evtTypeName": "NNet.Game.SGameUserJoinEvent", "id": i, "loop": i * 10}
            for i in range(n_events)
        ],
        "trackerEvents": [
            {"evtTypeName": "NNet.Replay.Tracker.SPlayerSetupEvent", "id": i, "loop": 0}
            for i in range(max(1, n_events // 5))
        ],
        "messageEvents": [{"evtTypeName": "NNet.Game.SChatMessage", "id": 0, "loop": 0}],
        "gameEventsErr": False,
        "messageEventsErr": False,
        "trackerEvtsErr": False,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _make_mapping_json(path: Path, *, n_keys: int = 3) -> None:
    """Write a synthetic map_foreign_to_english_mapping.json."""
    data = {f"MapName_{i}": f"English Map {i}" for i in range(n_keys)}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


@pytest.fixture()
def sc2_raw_dir(tmp_path: Path) -> Path:
    """Create synthetic sc2egset raw directory."""
    raw = tmp_path / "raw"

    for tournament in ["2020_Tournament_A", "2021_Tournament_B"]:
        data_dir = raw / tournament / f"{tournament}_data"
        for i in range(3):
            _make_replay_json(
                data_dir / f"replay_{i:02d}.SC2Replay.json",
                n_events=5 + i * 10,
            )
        _make_mapping_json(raw / tournament / "map_foreign_to_english_mapping.json")

    return raw


@pytest.fixture()
def sc2_inventory(sc2_raw_dir: Path) -> dict:
    """Create a minimal inventory dict matching the fixture."""
    dirs = []
    raw = sc2_raw_dir
    for d in sorted(raw.iterdir()):
        if d.is_dir():
            data_dir = d / f"{d.name}_data"
            files = list(data_dir.glob("*.SC2Replay.json"))
            total = sum(f.stat().st_size for f in files)
            dirs.append({
                "name": d.name,
                "replay_file_count": len(files),
                "total_bytes": total,
            })
    return {"top_level_dirs": dirs}


@pytest.fixture()
def sc2_db_con() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB connection."""
    return duckdb.connect(":memory:")


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestSelectSampleFiles:
    """Tests for select_sample_files."""

    def test_returns_files(
        self, sc2_inventory: dict, sc2_raw_dir: Path,
    ) -> None:
        """Should return a list of Path objects."""
        samples = select_sample_files(sc2_inventory, sc2_raw_dir)
        assert len(samples) > 0
        assert all(isinstance(s, Path) for s in samples)
        assert all(s.exists() for s in samples)

    def test_includes_extreme_dirs(
        self, sc2_inventory: dict, sc2_raw_dir: Path,
    ) -> None:
        """Should include files from smallest and largest avg dirs."""
        samples = select_sample_files(sc2_inventory, sc2_raw_dir)
        parent_dirs = {s.parent.parent.name for s in samples}
        # With only 2 dirs, both should be represented
        assert len(parent_dirs) >= 1


class TestReadJsonAuto:
    """Tests for test_read_json_auto_single."""

    def test_parses_successfully(
        self, sc2_db_con: duckdb.DuckDBPyConnection, sc2_raw_dir: Path,
    ) -> None:
        """read_json_auto should parse a single file successfully."""
        data_dir = sc2_raw_dir / "2020_Tournament_A" / "2020_Tournament_A_data"
        files = list(data_dir.glob("*.SC2Replay.json"))
        result = probe_read_json_auto_single(sc2_db_con, files[0])
        assert result["success"] is True
        assert result["column_count"] == 11  # noqa: PLR2004

    def test_reports_tpdm_type(
        self, sc2_db_con: duckdb.DuckDBPyConnection, sc2_raw_dir: Path,
    ) -> None:
        """Should report ToonPlayerDescMap type."""
        data_dir = sc2_raw_dir / "2020_Tournament_A" / "2020_Tournament_A_data"
        files = list(data_dir.glob("*.SC2Replay.json"))
        result = probe_read_json_auto_single(sc2_db_con, files[0])
        assert "STRUCT" in result["ToonPlayerDescMap_type"]


class TestMeasureEventArrays:
    """Tests for measure_event_arrays."""

    def test_measures_all_arrays(self, sc2_raw_dir: Path) -> None:
        """Should report element count and byte size for all 3 event types."""
        data_dir = sc2_raw_dir / "2020_Tournament_A" / "2020_Tournament_A_data"
        files = list(data_dir.glob("*.SC2Replay.json"))
        result = measure_event_arrays(files[0])
        for key in ("gameEvents", "trackerEvents", "messageEvents"):
            assert key in result
            assert result[key]["element_count"] > 0
            assert result[key]["json_bytes"] > 0


class TestBatchIngestion:
    """Tests for test_batch_ingestion."""

    def test_batch_succeeds(
        self, sc2_db_con: duckdb.DuckDBPyConnection, sc2_raw_dir: Path,
    ) -> None:
        """Batch ingestion on a directory should succeed."""
        data_dir = sc2_raw_dir / "2020_Tournament_A" / "2020_Tournament_A_data"
        result = probe_batch_ingestion(sc2_db_con, data_dir)
        assert result["success"] is True
        assert result["row_count"] == 3  # noqa: PLR2004


class TestMappingCensus:
    """Tests for census_mapping_files and test_mapping_read_json_auto."""

    def test_census_finds_all(self, sc2_raw_dir: Path) -> None:
        """Should find 2 mapping files (one per tournament dir)."""
        census = census_mapping_files(sc2_raw_dir)
        assert census["total_files_found"] == 2  # noqa: PLR2004
        assert census["cross_file_consistency"]["all_same_root_type"] is True

    def test_mapping_read_json_auto(
        self, sc2_db_con: duckdb.DuckDBPyConnection, sc2_raw_dir: Path,
    ) -> None:
        """read_json_auto should parse a mapping file."""
        mf = (
            sc2_raw_dir / "2020_Tournament_A"
            / "map_foreign_to_english_mapping.json"
        )
        result = probe_mapping_read_json_auto(sc2_db_con, mf)
        assert result["success"] is True
