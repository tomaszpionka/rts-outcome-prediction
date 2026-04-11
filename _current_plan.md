# Plan: Inventory Enhancements — Whole-Tree Filename Pattern Summary

**Category:** C (chore — enhancing existing Phase 01 Step 01_01_01 notebooks)
**Branch:** `chore/inventory-enhancements-filename-patterns`
**Phase/Step reference:** Phase 01 / Step 01_01_01 (File Inventory) — all three datasets

## Scope

One new capability for the file inventory notebooks: a whole-tree filename
pattern summary that groups every file in the raw/ tree by its abstract
naming pattern and reports counts per pattern. No filtering, no exclusions,
no changes to `inventory.py`.

---

## Design Decisions

### D1 — Where does pattern extraction logic live?

New module `src/rts_predict/common/filename_patterns.py`. `inventory.py` is
a filesystem walking utility; pattern analysis is a distinct concern that
operates on the results of inventory, not during walking. Keeping them
separate maintains single-responsibility.

### D2 — How to define a "filename pattern"?

A regex-based token replacement approach (game-agnostic). Replacement order:
1. ISO dates (`\d{4}-\d{2}-\d{2}`) → `{date}`
2. Hex hashes (`[0-9a-f]{16,}`) → `{hash}` (covers SC2 replay hashes)
3. Remaining pure numeric tokens (`\d+`) → `{N}`
4. Literal text and extensions are preserved

Expected patterns:
- sc2egset replays: `{hash}.SC2Replay.json`
- sc2egset metadata: `.gitkeep`, `{N}.zip`, `processing_tracker.json`, etc.
- aoe2companion: `match-{date}.parquet`, `rating-{date}.csv`, `leaderboard.parquet`, `.gitkeep`
- aoestats: `{date}_{date}_matches.parquet`, `{date}_{date}_players.parquet`, `.gitkeep`

### D3 — No filtering, no exclusions

Every file in the tree appears in the pattern summary — `.gitkeep`, README,
`.DS_Store`, metadata files, replay JSONs, everything. If 15 `.gitkeep` files
exist, the summary shows `.gitkeep: 15`. The pattern summary IS the valuable
output: it tells you at a glance what kinds of files live in the tree and
how many of each pattern exist.

### D4 — Whole-tree flat scan

For each dataset, all `FileEntry` objects from the entire raw/ tree are
collected into one flat list. `summarize_filename_patterns()` is called
once on that flat list to produce a single whole-tree pattern table.

- **aoe2companion / aoestats:** `result.files_at_root` + all `sd.files` for `sd in result.subdirs` → one flat list.
- **sc2egset (two-level):** `meta_result.files_at_root` + all `sd.files` for `sd in meta_result.subdirs` (tournament-level metadata) + all `replay_inv.files_at_root` + all `sd.files` from every `_data/` inventory → one flat list.

### D5 — No changes to inventory.py

`inventory.py` stays exactly as-is. No `filter_inventory()`, no
`HOUSEKEEPING_NAMES`, no `data_file_count` property. Only
`filename_patterns.py` is new.

---

## Files to Modify

| # | File | Change |
|---|------|--------|
| 1 | `src/rts_predict/common/filename_patterns.py` | **New file** — `normalize_filename_to_pattern()` and `summarize_filename_patterns()` |
| 2 | `tests/rts_predict/common/test_filename_patterns.py` | **New file** — tests for pattern extraction |
| 3 | `sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py` | Add import, pattern collection, pattern summary cells, updated artifacts |
| 4 | `sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.py` | Add import, pattern collection, pattern summary cells, updated artifacts |
| 5 | `sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py` | Add import, pattern collection, pattern summary cells, updated artifacts |
| 6 | Each paired `.ipynb` | Re-sync after `.py` edits |

**No changes to:**
- `src/rts_predict/common/inventory.py`
- `tests/rts_predict/common/test_inventory.py`

---

## Function Signatures

### `src/rts_predict/common/filename_patterns.py` (new file)

```python
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

# Module-level compiled regex constants (not magic — documented here)
_ISO_DATE_RE: re.Pattern[str]   # r"\d{4}-\d{2}-\d{2}" — ISO 8601 date
_HEX_HASH_RE: re.Pattern[str]   # r"[0-9a-f]{16,}" — SC2 replay hash (min 16 hex chars)
_NUMERIC_RE: re.Pattern[str]    # r"\d+" — residual numeric tokens (IDs, counts)


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
```

---

## Tests

### `tests/rts_predict/common/test_filename_patterns.py` (new file)

| Test | What it verifies |
|------|-----------------|
| `test_iso_date_replaced` | `"match-2024-01-01.parquet"` → `"match-{date}.parquet"` |
| `test_double_date_replaced` | `"2024-01-01_2024-01-07_matches.parquet"` → `"{date}_{date}_matches.parquet"` |
| `test_hex_hash_replaced` | `"095724b86cbca0e6da2fb8baad0d7baf.SC2Replay.json"` → `"{hash}.SC2Replay.json"` |
| `test_no_tokens_unchanged` | `"leaderboard.parquet"` → `"leaderboard.parquet"` |
| `test_numeric_id_replaced` | `"replay_12345.json"` → `"replay_{N}.json"` |
| `test_mixed_tokens` | Filename with date + number → both replaced |
| `test_gitkeep_unchanged` | `".gitkeep"` → `".gitkeep"` (no tokens; appears literally in summary) |
| `test_summarize_groups_correctly` | 3 `match-{date}.parquet` + 1 `leaderboard.parquet` + 2 `.gitkeep` → correct counts |
| `test_summarize_empty_list` | Empty input → empty dict |
| `test_summarize_sorted_by_count_desc` | Higher-count patterns appear first |

---

## Per-Notebook Cell Changes

### aoe2companion

**cell_02 (imports) — modify.** Add one import line:
```python
from rts_predict.common.filename_patterns import summarize_filename_patterns
```

**New cells inserted between cell_09 (date analysis markdown) and cell_10 (write JSON).** Two new cells:

**New cell (code) — pattern summary:**
```python
# Whole-tree filename pattern summary.
# Collect ALL FileEntry objects from the entire raw/ tree into one flat list.
all_files = result.files_at_root + [f for sd in result.subdirs for f in sd.files]
patterns = summarize_filename_patterns(all_files)

logger.info("Total files scanned for patterns: %d", len(all_files))
for pattern, count in patterns.items():
    logger.info("  %s: %d", pattern, count)
```

**New cell (markdown) — pattern interpretation:**
```
### Filename pattern summary

The whole-tree pattern summary groups every file in `raw/` by its abstract
naming pattern — dates replaced with `{date}`, hex hashes with `{hash}`,
numeric IDs with `{N}`. This reveals the naming conventions across all
subdirectories without excluding any files. Housekeeping files (`.gitkeep`,
ingestion trackers) appear alongside data files in the same table.
```

**cell_10 (write JSON) — modify.** Add two keys to the `artifact` dict:
```python
"filename_patterns": dict(patterns),
"total_files_scanned": len(all_files),
```

**cell_11 (write MD) — modify.** After the date range analysis section, add a "Filename patterns" section:
```python
lines.extend(["\n## Filename patterns\n"])
lines.append(f"Total files scanned: {len(all_files)}\n")
lines.append("| Pattern | Count |")
lines.append("|---|---|")
for pattern, count in patterns.items():
    lines.append(f"| `{pattern}` | {count} |")
```

---

### aoestats

**cell_02 (imports) — modify.** Add one import line:
```python
from rts_predict.common.filename_patterns import summarize_filename_patterns
```

**New cells inserted between cell_11 (paired comparison markdown) and cell_12 (write JSON).** Two new cells:

**New cell (code) — pattern summary:**
```python
# Whole-tree filename pattern summary.
# Collect ALL FileEntry objects from the entire raw/ tree into one flat list.
all_files = result.files_at_root + [f for sd in result.subdirs for f in sd.files]
patterns = summarize_filename_patterns(all_files)

logger.info("Total files scanned for patterns: %d", len(all_files))
for pattern, count in patterns.items():
    logger.info("  %s: %d", pattern, count)
```

**New cell (markdown) — pattern interpretation:**
```
### Filename pattern summary

The whole-tree pattern summary groups every file in `raw/` by its abstract
naming pattern. For aoestats, this should reveal the weekly date-range naming
convention (`{date}_{date}_matches.parquet`, `{date}_{date}_players.parquet`)
alongside any housekeeping files (`.gitkeep`, ingestion trackers, overview
files). No files are excluded from this count.
```

**cell_12 (write JSON) — modify.** Add two keys to the `artifact` dict:
```python
"filename_patterns": dict(patterns),
"total_files_scanned": len(all_files),
```

**cell_13 (write MD) — modify.** After the paired comparison section, add a "Filename patterns" section:
```python
lines.extend(["\n## Filename patterns\n"])
lines.append(f"Total files scanned: {len(all_files)}\n")
lines.append("| Pattern | Count |")
lines.append("|---|---|")
for pattern, count in patterns.items():
    lines.append(f"| `{pattern}` | {count} |")
```

---

### sc2egset

**cell_02 (imports) — modify.** Add one import line:
```python
from rts_predict.common.filename_patterns import summarize_filename_patterns
```

**New cells inserted between cell_09 (summary statistics markdown) and cell_10 (write JSON).** Two new cells:

**New cell (code) — whole-tree pattern summary:**

sc2egset has a two-level structure. We accumulate `FileEntry` objects from
both levels. The existing Level 2 loop (cell_06) builds summary dicts and
does not retain `FileEntry` objects, so we re-scan `_data/` subdirs here.
This costs ~22k additional stat() calls (seconds) and avoids a larger
refactor of cell_06.

```python
# Whole-tree filename pattern summary across both inventory levels.
# Level 1 (meta_result): root files + tournament-level metadata files.
all_files = list(meta_result.files_at_root)
all_files.extend(f for sd in meta_result.subdirs for f in sd.files)
# Level 2: re-scan each _data/ subdir to collect replay FileEntry objects.
# (cell_06 built summary dicts but did not retain FileEntry objects.)
for sd in meta_result.subdirs:
    data_dir = RAW_DIR / sd.name / (sd.name + "_data")
    if not data_dir.exists():
        continue
    replay_inv = inventory_directory(data_dir)
    all_files.extend(replay_inv.files_at_root)
    all_files.extend(f for rsd in replay_inv.subdirs for f in rsd.files)

patterns = summarize_filename_patterns(all_files)

logger.info("Total files scanned for patterns: %d", len(all_files))
for pattern, count in patterns.items():
    logger.info("  %s: %d", pattern, count)
```

**New cell (markdown) — pattern interpretation:**
```
### Filename pattern summary

The whole-tree pattern summary groups every file in the sc2egset `raw/`
tree by its abstract naming pattern — spanning both the tournament-level
metadata files and the `_data/` subdirectory replay files. This reveals
the full file taxonomy: replay JSONs (`{hash}.SC2Replay.json`), metadata
archives, processing trackers, and any housekeeping files (`.gitkeep`).
No files are excluded from this count.
```

**cell_10 (write JSON) — modify.** Add two keys to the `artifact` dict:
```python
"filename_patterns": dict(patterns),
"total_files_scanned": len(all_files),
```

**cell_11 (write MD) — modify.** After the per-tournament breakdown table, add a "Filename patterns" section:
```python
lines.extend(["\n## Filename patterns\n"])
lines.append(f"Total files scanned: {len(all_files)}\n")
lines.append("| Pattern | Count |")
lines.append("|---|---|")
for pattern, count in patterns.items():
    lines.append(f"| `{pattern}` | {count} |")
```

---

## Execution Order

1. Create branch: `git checkout -b chore/inventory-enhancements-filename-patterns`
2. Write `src/rts_predict/common/filename_patterns.py`
3. Write `tests/rts_predict/common/test_filename_patterns.py`
4. Run `source .venv/bin/activate && poetry run pytest tests/rts_predict/common/test_filename_patterns.py -v` + ruff + mypy — fix until green
5. Update sc2egset notebook (import + pattern cells + artifact updates)
6. Update aoe2companion notebook (import + pattern cells + artifact updates)
7. Update aoestats notebook (import + pattern cells + artifact updates)
8. Sync all `.ipynb` via jupytext: `poetry run jupytext --sync sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py && poetry run jupytext --sync sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.py && poetry run jupytext --sync sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py`
9. PR wrap-up (version bump patch, changelog, commit)

---

## Gate Condition

All of the following must hold:
1. `poetry run pytest tests/rts_predict/common/test_filename_patterns.py -v` passes
2. `poetry run ruff check src/rts_predict/common/` clean
3. `poetry run mypy src/rts_predict/common/` clean
4. Full test suite passes with coverage ≥ 95%
5. All three `.py` notebooks pass `poetry run jupytext --check`
6. Updated JSON artifacts contain `filename_patterns` (dict of pattern→count) and `total_files_scanned` (int, no exclusions)
7. Updated MD artifacts contain a "Filename patterns" section with a pattern table
8. `inventory.py` and `test_inventory.py` are NOT in the git diff (unchanged)

---

## Notes

- `.DS_Store` files will naturally appear in the pattern summary if they exist on disk. This is correct — no filtering.
- The sc2egset pattern cell re-scans `_data/` subdirectories because the existing Level 2 loop (cell_06) discards `FileEntry` objects after building summary dicts. ~22k additional stat() calls, completes in seconds. A comment in the cell documents this tradeoff.
- After notebooks are re-run, `reports/research_log.md` Step 01_01_01 entries do NOT need updating — existing counts are correct. The pattern summary is additive new information, not a correction.
