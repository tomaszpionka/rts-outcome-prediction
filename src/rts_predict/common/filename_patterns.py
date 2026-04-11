"""Filename pattern summarization for raw data inventory.

Extracts abstract filename patterns by replacing variable tokens
(dates, hashes, numeric IDs) with named placeholders. Used by
Phase 01 file inventory notebooks to characterize dataset file
naming conventions at a glance.

No game-domain imports. This module is game-agnostic.
"""

from __future__ import annotations

import re
from collections import Counter

from rts_predict.common.inventory import FileEntry

# Compiled regex constants -- applied in this order during normalization.
# Order matters: dates must be replaced before bare numbers to avoid
# partial matches on the digit sequences within date strings.
_ISO_DATE_RE: re.Pattern[str] = re.compile(r"\d{4}-\d{2}-\d{2}")
_HEX_HASH_RE: re.Pattern[str] = re.compile(r"[0-9a-f]{16,}")
_NUMERIC_RE: re.Pattern[str] = re.compile(r"\d+(?![A-Za-z])")


def normalize_filename_to_pattern(filename: str) -> str:
    """Replace variable tokens in a filename with named placeholders.

    Replacement order:
      1. ISO dates (YYYY-MM-DD) -> {date}
      2. Hex hashes (16+ lowercase hex chars) -> {hash}
      3. Remaining numeric sequences -> {N}

    Args:
        filename: The filename (name only, not full path).

    Returns:
        The normalized pattern string, e.g. "{date}_{date}_matches.parquet".
    """
    result = _ISO_DATE_RE.sub("{date}", filename)
    result = _HEX_HASH_RE.sub("{hash}", result)
    result = _NUMERIC_RE.sub("{N}", result)
    return result


def summarize_filename_patterns(
    files: list[FileEntry],
) -> dict[str, int]:
    """Group files by their abstract filename pattern and count occurrences.

    Applies normalize_filename_to_pattern() to each file's name and
    counts occurrences of each resulting pattern. Result is sorted
    by count descending.

    Args:
        files: List of FileEntry objects to summarize.

    Returns:
        Mapping of pattern string to count, sorted by count descending.
    """
    counter = Counter(normalize_filename_to_pattern(f.path.name) for f in files)
    return dict(counter.most_common())
