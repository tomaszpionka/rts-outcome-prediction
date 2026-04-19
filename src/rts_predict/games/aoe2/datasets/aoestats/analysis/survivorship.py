"""Survivorship analysis helpers for aoestats temporal EDA.

spec: reports/specs/01_05_preregistration.md@7e259dd8

Implements spec §6 triple survivorship analysis:
  6.1 Unconditional fraction_active per quarter
  6.2 Sensitivity N ∈ {5, 10, 20} minimum-match cohorts
  6.3 Conditional-label captioning (emitted by callers)
"""

from __future__ import annotations

import logging
from datetime import date

import pandas as pd

from rts_predict.common.db import DuckDBClient

logger = logging.getLogger(__name__)

# Spec §6.3 caption constant — append to every Q2/Q5 table/figure MD output
CONDITIONAL_CAPTION: str = (
    "*(conditional on ≥10 matches in reference period; see §6 for sensitivity)*"
)

_FRACTION_ACTIVE_SQL = """
WITH ever_seen AS (
  SELECT DISTINCT player_id
  FROM matches_history_minimal
  WHERE started_at BETWEEN TIMESTAMP '{overlap_start}' AND TIMESTAMP '{overlap_end}'
),
quarterly_active AS (
  SELECT DATE_TRUNC('quarter', started_at) AS qtr,
         COUNT(DISTINCT player_id) AS n_active
  FROM matches_history_minimal
  WHERE started_at BETWEEN TIMESTAMP '{overlap_start}' AND TIMESTAMP '{overlap_end}'
  GROUP BY 1
)
SELECT
  qa.qtr,
  qa.n_active,
  (SELECT COUNT(*) FROM ever_seen) AS n_ever_seen,
  qa.n_active * 1.0 / (SELECT COUNT(*) FROM ever_seen) AS fraction_active
FROM quarterly_active qa
ORDER BY qa.qtr
"""

_COHORT_SQL = """
SELECT CAST(player_id AS BIGINT) AS player_id
FROM matches_history_minimal
WHERE started_at BETWEEN TIMESTAMP '{ref_start}' AND TIMESTAMP '{ref_end}'
GROUP BY player_id
HAVING COUNT(*) >= {n_min}
  AND MAX(started_at) - MIN(started_at) >= INTERVAL '{span_days} days'
"""


def compute_fraction_active(
    db: DuckDBClient,
    overlap_start: date,
    overlap_end: date,
) -> pd.DataFrame:
    """Compute per-quarter fraction of ever-seen players active that quarter.

    Args:
        db: Open DuckDBClient (read-only).
        overlap_start: Start of overlap window (inclusive).
        overlap_end: End of overlap window (inclusive).

    Returns:
        DataFrame with columns: qtr, n_active, n_ever_seen, fraction_active.
    """
    sql = _FRACTION_ACTIVE_SQL.format(
        overlap_start=str(overlap_start),
        overlap_end=str(overlap_end),
    )
    return db.fetch_df(sql)


def compute_n_match_cohort(
    db: DuckDBClient,
    ref_start: date,
    ref_end: date,
    n_min: int,
    span_days_min: int = 30,
) -> list[int]:
    """Return profile_ids meeting minimum-match and active-span criteria.

    Args:
        db: Open DuckDBClient (read-only).
        ref_start: Reference period start (inclusive).
        ref_end: Reference period end (inclusive).
        n_min: Minimum number of matches required.
        span_days_min: Minimum active span in days (default 30 per spec §6.2).

    Returns:
        List of player_id integers satisfying the criteria.
    """
    sql = _COHORT_SQL.format(
        ref_start=str(ref_start),
        ref_end=str(ref_end),
        n_min=n_min,
        span_days=span_days_min,
    )
    df = db.fetch_df(sql)
    return df["player_id"].tolist()
