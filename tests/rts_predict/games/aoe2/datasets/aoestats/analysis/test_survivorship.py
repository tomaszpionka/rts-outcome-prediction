"""Tests for aoestats survivorship analysis module."""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pandas as pd

from rts_predict.games.aoe2.datasets.aoestats.analysis.survivorship import (
    CONDITIONAL_CAPTION,
    compute_fraction_active,
    compute_n_match_cohort,
)


class TestConditionalCaption:
    def test_caption_contains_spec_text(self) -> None:
        assert "conditional on" in CONDITIONAL_CAPTION
        assert "10 matches" in CONDITIONAL_CAPTION
        assert "§6" in CONDITIONAL_CAPTION


class TestComputeFractionActive:
    def test_passes_sql_to_db_and_returns_dataframe(self) -> None:
        mock_db = MagicMock()
        expected_df = pd.DataFrame({
            "qtr": [date(2022, 7, 1)],
            "n_active": [100],
            "n_ever_seen": [200],
            "fraction_active": [0.5],
        })
        mock_db.fetch_df.return_value = expected_df

        result = compute_fraction_active(
            mock_db,
            overlap_start=date(2022, 7, 1),
            overlap_end=date(2022, 9, 30),
        )

        mock_db.fetch_df.assert_called_once()
        assert result is expected_df

    def test_sql_contains_date_strings(self) -> None:
        mock_db = MagicMock()
        mock_db.fetch_df.return_value = pd.DataFrame()

        compute_fraction_active(
            mock_db,
            overlap_start=date(2023, 1, 1),
            overlap_end=date(2023, 3, 31),
        )

        sql_called = mock_db.fetch_df.call_args[0][0]
        assert "2023-01-01" in sql_called
        assert "2023-03-31" in sql_called


class TestComputeNMatchCohort:
    def test_returns_list_of_ints(self) -> None:
        mock_db = MagicMock()
        mock_db.fetch_df.return_value = pd.DataFrame({"player_id": [1, 2, 3]})

        result = compute_n_match_cohort(
            mock_db,
            ref_start=date(2022, 8, 29),
            ref_end=date(2022, 10, 27),
            n_min=10,
        )

        assert result == [1, 2, 3]
        mock_db.fetch_df.assert_called_once()

    def test_empty_cohort_returns_empty_list(self) -> None:
        mock_db = MagicMock()
        mock_db.fetch_df.return_value = pd.DataFrame({"player_id": []})

        result = compute_n_match_cohort(
            mock_db,
            ref_start=date(2022, 8, 29),
            ref_end=date(2022, 10, 27),
            n_min=10,
        )

        assert result == []

    def test_sql_contains_n_min_and_span(self) -> None:
        mock_db = MagicMock()
        mock_db.fetch_df.return_value = pd.DataFrame({"player_id": []})

        compute_n_match_cohort(
            mock_db,
            ref_start=date(2022, 8, 29),
            ref_end=date(2022, 10, 27),
            n_min=15,
            span_days_min=45,
        )

        sql_called = mock_db.fetch_df.call_args[0][0]
        assert "15" in sql_called
        assert "45" in sql_called
