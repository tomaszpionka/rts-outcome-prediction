---
category: B
branch: fix/01-04-null-audit
date: 2026-04-17
planner_model: claude-sonnet-4-6
invariants_touched: []
critique_required: true
research_log_ref: null
source_artifacts:
  - sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py
  - sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py
  - sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py
  - src/rts_predict/common/CONTRACT.md
  - tests/rts_predict/common/test_eda_census.py
---

# Plan: NOTE-3 + W2 — Extract DRY missingness-audit helpers + W2 JSON shape standardization (Category B refactor)

**User decisions locked (from chat approval):**
- Stay on `fix/01-04-null-audit` branch (no separate refactor branch)
- Stay on version `3.10.3` (same PR; append CHANGELOG entries to existing `[3.10.3]` block)
- Accept the aoec `_recommend` text delta (canonical fuller text replaces contracted version; recommendation codes unchanged, only free-text justifications change)
- `build_audit_views_block` returns `{"views": {...}}` (callers do `["views"]`); self-describing in tests

## Scope

Extract the 5 missingness-audit helper functions (`_build_sentinel_predicate`, `_sentinel_census`, `_detect_constants`, `_recommend`, `_consolidate_ledger`) currently duplicated inline in 3 cleaning notebooks into a single shared module `src/rts_predict/common/missingness_audit.py`. Add a 6th public helper `build_audit_views_block` that bakes the canonical inline-`missingness_audit` JSON shape (W2 fix). Add unit tests with 100% line coverage of the new module. Re-execute all 3 notebooks to refresh artifacts.

Backward-compatible refactor: the produced ledger artifacts must be functionally identical to commits `41964e5` (sc2egset), `31d5614` (aoestats), `aeded6a` (aoe2companion) — recommendation codes and all numeric ledger columns unchanged. Free-text `recommendation_justification` for aoec may differ (contracted → canonical body, accepted per user direction).

## Execution Steps

### T01 — Create `src/rts_predict/common/missingness_audit.py`

**Objective:** Produce the new shared module containing the 5 extracted helpers (with `con` made an explicit parameter on the two that need it) plus the `build_audit_views_block` public function. Module is self-contained, importable from any notebook, with type hints + Google-style docstrings on every function.

**Instructions:**

1. Create `src/rts_predict/common/missingness_audit.py` with:
   - Module docstring (cite invariants I6 reproducibility, I9 phase-boundary discipline)
   - Imports: `from __future__ import annotations`, `logging`, `Any` from typing, `duckdb`, `pandas as pd`
   - `logger = logging.getLogger(__name__)`
   - Module-level constants: `_VALID_MECHANISMS = frozenset({"MAR", "MCAR", "MNAR", "N/A"})` and `_VALID_RECOMMENDATIONS = frozenset({"DROP_COLUMN", "FLAG_FOR_IMPUTATION", "RETAIN_AS_IS", "EXCLUDE_TARGET_NULL_ROWS", "CONVERT_SENTINEL_TO_NULL"})`
2. Function signatures (per NOTE-2 critique fix, **bodies are semantically equivalent across sc2/aoestats but not byte-identical**: aoestats uses an intermediate `col_field` variable; sc2 has a `try/except Exception` guard in `_sentinel_census` that aoestats lacks. The canonical adoption strategy: **use aoestats body as base; merge in sc2's try/except guard** for `_sentinel_census` resilience. aoec body has CONTRACTED `_recommend` text — replaced by the canonical version per Q2):
   - `def _build_sentinel_predicate(col: str, sentinel_value: Any) -> tuple[str | None, str | None]:` — copy verbatim from aoestats; all 3 versions identical
   - `def _sentinel_census(view_name: str, total_rows: int, spec: dict[str, Any], con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:` — copy aoestats body, add `con` as explicit parameter, replace closure ref `con.execute(...)` with the parameter, add `except Exception` guard for non-existent columns (sc2 has it; aoestats doesn't — add for safety)
   - `def _detect_constants(view_name: str, columns: list[str], con: duckdb.DuckDBPyConnection, identity_cols: frozenset[str] = frozenset()) -> dict[str, int | None]:` — copy aoestats body, add `con` as 3rd param, `identity_cols` becomes 4th param (was 3rd in inline call sites — see T03/T04/T05 for call-site updates)
   - `def _recommend(col: str, mechanism: str, pct: float, is_primary: bool, n_null: int, n_sentinel: int) -> tuple[str, str]:` — use the **aoestats canonical** body (full B6 deferral sentence in CONVERT_SENTINEL_TO_NULL branch; full text in 5-40% band)
   - `def _consolidate_ledger(view_name: str, df_null: pd.DataFrame, sentinel_rows: list[dict[str, Any]], spec: dict[str, Any], dtype_map: dict[str, str], total_rows: int, constants_map: dict[str, int | None], target_cols: set[str], identity_cols: frozenset[str] = frozenset()) -> pd.DataFrame:` — use aoestats version verbatim; ~60 lines (acceptable; do not decompose)
3. NEW public helper:
   ```python
   def build_audit_views_block(
       view_ledgers: dict[str, dict[str, Any]],
   ) -> dict[str, Any]:
       """Build canonical inline `missingness_audit.views` block.

       Args:
           view_ledgers: {view_name: {"total_rows": int, "df_ledger": pd.DataFrame}}.

       Returns:
           {"views": {view_name: {"total_rows": int, "columns_audited": int, "ledger": list[dict]}}}.
       """
   ```
   Returns `{"views": {...}}` — callers extract via `["views"]` (per user decision Q3).

**Verification:**
- `source .venv/bin/activate && poetry run python -c "from rts_predict.common.missingness_audit import _build_sentinel_predicate, _sentinel_census, _detect_constants, _recommend, _consolidate_ledger, build_audit_views_block; print('OK')"` — prints OK
- `source .venv/bin/activate && poetry run ruff check src/rts_predict/common/missingness_audit.py` — clean
- `source .venv/bin/activate && poetry run mypy src/rts_predict/common/missingness_audit.py` — clean

**File scope:**
- `src/rts_predict/common/missingness_audit.py`

**Read scope:** (none)

---

### T02 — Unit tests for `missingness_audit.py`

**Objective:** Produce `tests/rts_predict/common/test_missingness_audit.py` with 100% line coverage of the new module via synthetic in-memory DuckDB fixtures.

**Instructions:**

1. Create `tests/rts_predict/common/test_missingness_audit.py`
2. Imports: `duckdb`, `numpy as np`, `pandas as pd`, `pytest`, all 6 names from the new module
3. Module-level fixture `audit_con` — in-memory DuckDB connection with VIEW `test_view`:
   - 5 rows
   - Columns: `id` BIGINT (identity, never NULL), `score` INTEGER (some NULLs), `tag` VARCHAR (sentinel `'unknown'`), `flag` BOOLEAN (all same value — true constant), `result` VARCHAR (target, with NULL row)
   - Construct via `CREATE VIEW test_view AS SELECT * FROM (VALUES ...)`
4. Tests for `_build_sentinel_predicate` (no DuckDB needed):
   - `None` sentinel → `(None, None)`
   - Integer sentinel → `("= 0", "0")`
   - String sentinel → `("= 'val'", "val")` properly escaped
   - String with single-quote → `("= 'it''s'", "it's")` SQL injection guard
   - List of ints → `("IN (0, 1)", "[0, 1]")` predicate
   - List of strings → predicate with quoted values
5. Tests for `_sentinel_census` (uses fixture):
   - Happy path: spec with one sentinel column → returns row with correct `n_sentinel` / `pct_sentinel`
   - Empty spec → returns `[]`
   - Column in spec absent from VIEW → `n_sentinel=0` (exercises `except Exception` guard)
   - `total_rows=0` → no division-by-zero error
6. Tests for `_detect_constants` (uses fixture):
   - Non-identity column → returns correct `n_distinct`
   - Identity column in `identity_cols` → returns `None` (skipped)
   - Empty `columns` list → returns `{}`
7. Tests for `_recommend` (no DuckDB needed):
   - W3 branch: `n_sentinel > 0 and n_null == 0 and pct < 5.0` → `CONVERT_SENTINEL_TO_NULL`
   - F1: `pct == 0.0` → `RETAIN_AS_IS`
   - High rate: `pct > 80.0` → `DROP_COLUMN`
   - Mid-MNAR: `pct > 40.0, mechanism="MNAR"` → `DROP_COLUMN`
   - Mid-primary: `pct > 40.0, is_primary=True, MAR` → `FLAG_FOR_IMPUTATION`
   - Mid-non-primary: `pct > 40.0, is_primary=False, MAR` → `DROP_COLUMN`
   - Mid-low: `5.0 < pct <= 40.0` → `FLAG_FOR_IMPUTATION`
   - Low + NULLs: `pct < 5.0, n_null > 0` → `RETAIN_AS_IS` (NOT W3 — has NULLs)
8. Tests for `_consolidate_ledger` (uses fixture):
   - Identity column → `mechanism="N/A"`, `recommendation="RETAIN_AS_IS"`, `n_distinct=None`
   - True constant (n_distinct=1, no NULLs, no sentinels) → `mechanism="N/A"`, `recommendation="DROP_COLUMN"`
   - Zero-missingness with spec → `mechanism="N/A"`, `recommendation="RETAIN_AS_IS"`, `carries_semantic_content` from spec
   - **Zero-missingness for column NOT in spec** (per WARNING-3 critique fix) → `mechanism="N/A"`, `recommendation="RETAIN_AS_IS"`, `carries_sem=False`, `is_primary=False` (covers the `spec_entry is None` sub-branch of F1)
   - Spec entry + missingness → mechanism from spec, recommendation from `_recommend`
   - No spec + missingness → fallback `mechanism="MAR"`, recommendation from `_recommend`
   - Target column with missingness → `recommendation="EXCLUDE_TARGET_NULL_ROWS"` (B4 fires)
   - Target column without missingness → F1 fires first → `RETAIN_AS_IS` (NOT EXCLUDE_TARGET_NULL_ROWS)
   - Output DataFrame has exactly 17 columns (per the spec in Deliverable 5.B of the prior audit plan)
   - Constant + target conflict → constant branch wins (W7/B5 priority precedes B4)
9. Tests for `build_audit_views_block`:
   - Two views input → output has `views.view_a` and `views.view_b` with correct keys
   - `columns_audited == len(df_ledger)` for each view
   - Empty DataFrame → `ledger=[]`, `columns_audited=0`
   - **Empty `view_ledgers` dict input** (per WARNING-3 critique fix) → returns `{"views": {}}`

**Verification:**
- `source .venv/bin/activate && poetry run pytest tests/rts_predict/common/test_missingness_audit.py -v --cov=rts_predict.common.missingness_audit --cov-report=term-missing` — all pass, 100% line coverage on the new module
- `source .venv/bin/activate && poetry run pytest tests/ -v --cov=rts_predict --cov-report=term-missing 2>&1 | tail -5` — TOTAL ≥ 95% (closes pre-existing gap)

**File scope:**
- `tests/rts_predict/common/test_missingness_audit.py`

**Read scope:**
- `src/rts_predict/common/missingness_audit.py` (output of T01)

---

### T03 — Update sc2egset notebook to import from shared module

**Objective:** Remove ~210 lines of inline helper definitions, replace with import; update call sites for `con` parameter; replace inline `views` block construction with `build_audit_views_block`. Re-execute end-to-end.

**Instructions:**

1. Locate the cell with the 5 inline function definitions in `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py` (~lines 1195–1405). Replace cell body with:
   ```python
   from rts_predict.common.missingness_audit import (
       _build_sentinel_predicate,
       _sentinel_census,
       _detect_constants,
       _recommend,
       _consolidate_ledger,
       build_audit_views_block,
   )
   print("Helper functions imported from rts_predict.common.missingness_audit.")
   ```
   Update the cell's markdown header to reflect import-only purpose.

2. Update `_sentinel_census` call sites — pass `con` explicitly:
   - matches_flat_clean call: `_sentinel_census(view, total_rows, spec)` → `_sentinel_census(view, total_rows, spec, con)`
   - player_history_all call: same pattern

3. Update `_detect_constants` call sites — `con` becomes 3rd positional, `identity_cols` becomes 4th:
   - `_detect_constants(view, cols_list, identity_cols)` → `_detect_constants(view, cols_list, con, identity_cols)`
   - Both call sites (matches_flat_clean + player_history_all)

4. Replace the inline `artifact["missingness_audit"]["views"]` block construction:
   ```python
   artifact["missingness_audit"]["views"] = build_audit_views_block({
       _view_mfc: {"total_rows": _total_mfc_rows, "df_ledger": df_ledger_mfc},
       _view_hist: {"total_rows": _total_hist_rows, "df_ledger": df_ledger_hist},
   })["views"]
   ```
   Remove the old inline dict literal (with hardcoded `total_rows`, `columns_audited`, `ledger` keys) — `build_audit_views_block` produces all three.

5. Sync .ipynb: `source .venv/bin/activate && poetry run jupytext --sync sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`

6. Re-execute: `source .venv/bin/activate && poetry run jupyter execute sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb`

7. Capture pre-extraction ledger CSV checksum from commit 41964e5 BEFORE this task runs:
   `git show 41964e5:src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv | md5`

8. Compare post-extraction CSV checksum — must be identical (no functional change for sc2egset; it already had the canonical `_recommend` body).

**Verification:**
- Notebook re-executes without `AssertionError`
- `python -c "import json, pathlib; d=json.loads(pathlib.Path('src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json').read_text()); print(list(d['missingness_audit']['views'].keys()))"` prints `['matches_flat_clean', 'player_history_all']`
- Ledger CSV md5 matches commit 41964e5's CSV md5 (byte-identical)

**File scope:**
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py`
- `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json`

**Read scope:**
- `src/rts_predict/common/missingness_audit.py` (T01 output)

---

### T04 — Update aoestats notebook + W2 shape fix + per_view_target_cols bug fix

**Objective:** Remove inline helper definitions, replace with import; update `con` call sites; fix the inline `missingness_audit` block from flat `ledger_<view_name>` keys to canonical `views.<view_name>:` shape via `build_audit_views_block`; fix pre-existing bug in `per_view_target_cols.player_history_all` (currently hardcoded `["winner"]`, should be the actual `_target_cols_ph` value); re-execute end-to-end.

**Instructions:**

1. Locate the cell with the 5 inline function definitions in `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py`. Replace with the same import block as T03.

2. Update `_sentinel_census` call sites to pass `con` (2 occurrences: matches_1v1_clean + player_history_all).

3. Update `_detect_constants` call sites — `con` becomes 3rd positional, `identity_cols` 4th (2 occurrences).

4. **W2 fix:** Replace the flat `ledger_matches_1v1_clean` and `ledger_player_history_all` keys with the canonical `views.<view_name>:` shape:
   ```python
   artifact["missingness_audit"]["views"] = build_audit_views_block({
       _view_m1: {"total_rows": total_rows_m1, "df_ledger": df_ledger_m1},
       _view_ph: {"total_rows": total_rows_ph, "df_ledger": df_ledger_ph},
   })["views"]
   ```
   Remove the old `ledger_<view_name>` flat keys from the artifact dict.

5. **(removed per BLOCKER-1 critique fix):** Direct inspection confirmed aoestats `_target_cols_ph = {"winner"}` (line 1096) and `list(_target_cols_ph) == ["winner"]` matches the hardcoded literal at line 1568 exactly. No bug exists. The hardcoded `["winner"]` and `["team1_wins"]` literals stay as-is — no churn, no fictitious "Fixed:" CHANGELOG entry.

6. Sync + re-execute (jupytext + jupyter execute) — note: aoestats player_history_all is 107.6M rows × 13 cols; constants-detection takes ~10-30 min.

7. Capture pre-extraction ledger CSV checksum from commit 31d5614 BEFORE this task runs.

8. Compare post-extraction:
   - CSV recommendation codes IDENTICAL (no logic change)
   - CSV byte-identical for numeric columns
   - JSON `missingness_audit.views` keys are `["matches_1v1_clean", "player_history_all"]` (no `ledger_*` keys)

**Verification:**
- Notebook re-executes without `AssertionError`
- `python -c "import json, pathlib; d=json.loads(...); assert 'ledger_matches_1v1_clean' not in d['missingness_audit']"` — passes
- `python -c "...; print(d['missingness_audit']['framework']['per_view_target_cols'])"` — verify per_view_target_cols values are correct
- Ledger CSV recommendation column matches commit 31d5614 exactly

**File scope:**
- `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py`
- `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
- `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json`

**Read scope:**
- `src/rts_predict/common/missingness_audit.py` (T01 output)

---

### T05 — Update aoec notebook + W2 shape fix + accept canonical `_recommend` text

**Objective:** Remove inline helper definitions (including the **contracted `_recommend` body** that's missing the B6 deferral sentence), replace with shared import (which uses canonical fuller text per user Q2 decision); update `con` call sites; fix the JSON shape from `<view_name>:` direct-key to canonical `views.<view_name>:`; re-execute end-to-end.

**Instructions:**

1. Locate the cell with the 5 inline function definitions. Replace with the same import block as T03. **Note:** the import will replace the contracted `_recommend` body with the canonical fuller text. After re-execution, free-text `recommendation_justification` values in the aoec ledger CSV/JSON will change for any column that hits the affected `_recommend` branches. Recommendation codes will NOT change. (Per user Q2 decision: accept this delta.)

2. Update `_sentinel_census` call sites to pass `con` (2 occurrences).

3. Update `_detect_constants` call sites — `con` becomes 3rd positional, `identity_cols` 4th (2 occurrences). **NOTE (per WARNING-1 critique fix):** aoec currently uses keyword form `_detect_constants(view, cols, identity_cols=_IDENTITY_COLS_M1)` (lines 1165, 1245). After signature change, both `_detect_constants(view, cols, con, identity_cols=...)` (keyword) and `_detect_constants(view, cols, con, _IDENTITY_COLS_M1)` (positional) are equivalent. Pick the keyword form to minimize diff and preserve existing aoec call style.

4. **W2 fix:** Replace direct `<view_name>:` top-level keys in `artifact["missingness_audit"]` (currently `"matches_1v1_clean": {...}` and `"player_history_all": {...}`) with the canonical `views.<view_name>:` shape (using `_VIEW_M1` / `_VIEW_PH` variables for consistency with T03/T04 — per NOTE-1 critique fix):
   ```python
   artifact["missingness_audit"]["views"] = build_audit_views_block({
       _VIEW_M1: {"total_rows": int(total_rows_m1), "df_ledger": df_ledger_m1},
       _VIEW_PH: {"total_rows": int(total_rows_ph), "df_ledger": df_ledger_ph},
   })["views"]
   ```
   Remove the old direct view-name keys from the artifact dict. **WARNING-2 side-effect to document:** aoec currently has `"n_cols": len(df_ledger_m1)` — the new `build_audit_views_block` produces `"columns_audited"` instead. This is a deliberate field rename as part of W2 canonicalization (uniform across 3 datasets); record explicitly in CHANGELOG (T06 step 4).

5. Sync + re-execute (jupytext + jupyter execute) — matches_1v1_clean is 17.8M × 54; constants-detection ~10-20 min.

6. Capture pre-extraction ledger CSV checksum from commit aeded6a BEFORE this task runs.

7. Compare post-extraction:
   - CSV recommendation codes IDENTICAL (per Q2: codes unchanged, justifications may change)
   - CSV byte-identical for numeric columns and `recommendation` column
   - `recommendation_justification` text for affected aoec rows differs from pre-extraction (canonical fuller text); ACCEPTED per user Q2
   - JSON `missingness_audit.views` keys are `["matches_1v1_clean", "player_history_all"]` (no direct view-name keys)

**Verification:**
- Notebook re-executes without `AssertionError`
- `python -c "...; assert 'matches_1v1_clean' in d['missingness_audit']['views']"` — passes
- `python -c "...; assert 'matches_1v1_clean' not in [k for k in d['missingness_audit'].keys() if k != 'views']"` — passes (old direct key removed)
- Diff aoec ledger CSV against commit aeded6a: `recommendation` column IDENTICAL; `recommendation_justification` may differ (acceptable)

**File scope:**
- `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py`
- `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv`
- `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json`

**Read scope:**
- `src/rts_predict/common/missingness_audit.py` (T01 output)

---

### T06 — Final verification + CHANGELOG update

**Objective:** Run full test suite with coverage to confirm ≥95% TOTAL, run lint+type-check clean, update `CHANGELOG.md` `[3.10.3]` block (per user Q1: stay in same release).

**Instructions:**

1. `source .venv/bin/activate && poetry run pytest tests/ -v --cov=rts_predict --cov-report=term-missing` — confirm TOTAL ≥ 95% AND zero failures
2. `source .venv/bin/activate && poetry run ruff check src/ tests/` — clean
3. `source .venv/bin/activate && poetry run mypy src/rts_predict/` — clean
4. Append entries to existing `[3.10.3]` block in CHANGELOG.md (per user Q1 — NOT to `[Unreleased]`):
   - **Added:** `src/rts_predict/common/missingness_audit.py` — shared missingness-audit helpers extracted from 3 inline notebook definitions; new `build_audit_views_block` helper for canonical `views.<view_name>:` JSON shape; 100% unit-test coverage at `tests/rts_predict/common/test_missingness_audit.py`
   - **Changed:** all 3 cleaning notebooks (`01_04_01_data_cleaning.py`) now import helpers from `rts_predict.common.missingness_audit` instead of defining them inline. Inline `missingness_audit.views` JSON block standardized to canonical `views.<view_name>: {total_rows, columns_audited, ledger}` shape across all 3 datasets (W2 fix); aoec `_recommend` body upgraded from contracted to canonical (recommendation codes unchanged, free-text `recommendation_justification` for affected rows now carries the full B6 deferral sentence). **aoec inline `missingness_audit.<view>.n_cols` field renamed to `views.<view>.columns_audited` as part of W2 canonicalization** (per WARNING-2 critique fix — explicit because downstream consumers referencing `n_cols` would otherwise break silently).
5. **DO NOT bump version** — stays at 3.10.3 per user Q1 decision
6. **(no "Fixed:" entry per BLOCKER-1 critique fix)** — direct inspection confirmed aoestats `per_view_target_cols.*` hardcoded literals match runtime `_target_cols_*` set values; no observable bug to fix.

**Verification:**
- pytest TOTAL ≥ 95% with zero failures
- ruff exit 0
- mypy exit 0
- CHANGELOG `[3.10.3]` block has new Added/Changed/Fixed entries

**File scope:**
- `CHANGELOG.md`

**Read scope:** (none)

---

## File Manifest

| File | Action |
|------|--------|
| `src/rts_predict/common/missingness_audit.py` | Create |
| `tests/rts_predict/common/test_missingness_audit.py` | Create |
| `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Update (replace inline defs with import; update call sites) |
| `sandbox/sc2/sc2egset/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Update (jupytext sync) |
| `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Update (replace inline defs + W2 + per_view_target_cols bug fix) |
| `sandbox/aoe2/aoestats/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Update (jupytext sync) |
| `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.py` | Update (replace inline defs + W2 + accept canonical _recommend text) |
| `sandbox/aoe2/aoe2companion/01_exploration/04_cleaning/01_04_01_data_cleaning.ipynb` | Update (jupytext sync) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Update (regenerated by notebook re-run) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Update (regenerated) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv` | Update (regenerated; should be byte-identical) |
| `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv` | Update (regenerated; recommendation codes byte-identical) |
| `src/rts_predict/games/aoe2/datasets/aoestats/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.json` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_data_cleaning.md` | Update (regenerated) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.csv` | Update (regenerated; recommendation codes byte-identical, justifications may differ per Q2) |
| `src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/04_cleaning/01_04_01_missingness_ledger.json` | Update (regenerated) |
| `CHANGELOG.md` | Update (append to `[3.10.3]` block) |

## Gate Condition

1. `from rts_predict.common.missingness_audit import _build_sentinel_predicate, _sentinel_census, _detect_constants, _recommend, _consolidate_ledger, build_audit_views_block` works from any of the 3 notebooks
2. All 3 notebooks execute end-to-end without `AssertionError`
3. `pytest tests/rts_predict/common/test_missingness_audit.py --cov=rts_predict.common.missingness_audit` reports 100% line coverage
4. `pytest tests/ --cov=rts_predict` TOTAL ≥ 95% (closes pre-existing gap)
5. `ruff check src/ tests/` and `mypy src/rts_predict/` both exit 0
6. All 3 inline `missingness_audit.views` blocks have uniform `views.<view_name>: {total_rows, columns_audited, ledger}` shape — no `ledger_<view_name>` flat keys, no `<view_name>` direct top-level keys
7. sc2egset ledger CSV byte-identical to commit 41964e5 (no functional change)
8. aoestats ledger CSV: recommendation column byte-identical to 31d5614; per_view_target_cols.player_history_all reflects actual target set (no hardcoded `["winner"]`)
9. aoec ledger CSV: recommendation column byte-identical to aeded6a; recommendation_justification may differ (canonical text); ACCEPTED

## Out of scope

- Changing `_recommend` decision-tree thresholds (5/40/80) — user-locked
- Changing override priority (B4/B5/F1/W1/W3) — already approved
- Changing 17-column ledger schema — already approved
- Modifying VIEW DDL — Phase 01 boundary
- Modifying `_missingness_spec` dict contents — dataset-specific design intent
- Adding `MissingnessSpecEntry` typed dataclass — adds union-type complexity for no measurable gain
- Moving `_missingness_spec` dicts out of notebooks — they are intentionally dataset-specific
- Moving `artifact["missingness_audit"]["framework"]` block into shared helper — would require per-dataset overrides; complexity not justified
- Version bump (stays 3.10.3 per user Q1)
- Coverage gap in `pre_ingestion.py` files — separate plan after this refactor (the new tests should close the total-coverage gap, addressing the gate)
