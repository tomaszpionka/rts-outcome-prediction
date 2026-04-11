"""Tests for src/rts_predict/common/filename_patterns.py."""

from pathlib import Path

from rts_predict.common.filename_patterns import (
    normalize_filename_to_pattern,
    summarize_filename_patterns,
)
from rts_predict.common.inventory import FileEntry


class TestNormalizeFilenameToPattern:
    """Tests for normalize_filename_to_pattern()."""

    def test_iso_date_replaced(self) -> None:
        assert (
            normalize_filename_to_pattern("match-2024-01-01.parquet")
            == "match-{date}.parquet"
        )

    def test_double_date_replaced(self) -> None:
        assert (
            normalize_filename_to_pattern("2024-01-01_2024-01-07_matches.parquet")
            == "{date}_{date}_matches.parquet"
        )

    def test_hex_hash_replaced(self) -> None:
        assert (
            normalize_filename_to_pattern(
                "095724b86cbca0e6da2fb8baad0d7baf.SC2Replay.json"
            )
            == "{hash}.SC2Replay.json"
        )

    def test_no_tokens_unchanged(self) -> None:
        assert (
            normalize_filename_to_pattern("leaderboard.parquet")
            == "leaderboard.parquet"
        )

    def test_numeric_id_replaced(self) -> None:
        assert (
            normalize_filename_to_pattern("replay_12345.json")
            == "replay_{N}.json"
        )

    def test_mixed_tokens(self) -> None:
        assert (
            normalize_filename_to_pattern("match-2024-01-01_round3.parquet")
            == "match-{date}_round{N}.parquet"
        )

    def test_gitkeep_unchanged(self) -> None:
        assert normalize_filename_to_pattern(".gitkeep") == ".gitkeep"


class TestSummarizeFilenamePatterns:
    """Tests for summarize_filename_patterns()."""

    @staticmethod
    def _make_entry(name: str) -> FileEntry:
        return FileEntry(path=Path(name), size_bytes=0, extension="")

    def test_summarize_groups_correctly(self) -> None:
        files = [
            self._make_entry("match-2024-01-01.parquet"),
            self._make_entry("match-2024-01-02.parquet"),
            self._make_entry("match-2024-01-03.parquet"),
            self._make_entry("leaderboard.parquet"),
            self._make_entry(".gitkeep"),
            self._make_entry(".gitkeep"),
        ]
        result = summarize_filename_patterns(files)
        assert result["match-{date}.parquet"] == 3
        assert result["leaderboard.parquet"] == 1
        assert result[".gitkeep"] == 2

    def test_summarize_empty_list(self) -> None:
        assert summarize_filename_patterns([]) == {}

    def test_summarize_sorted_by_count_desc(self) -> None:
        files = [
            self._make_entry("a.txt"),
            self._make_entry("b-2024-01-01.csv"),
            self._make_entry("b-2024-01-02.csv"),
            self._make_entry("b-2024-01-03.csv"),
        ]
        result = summarize_filename_patterns(files)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)
