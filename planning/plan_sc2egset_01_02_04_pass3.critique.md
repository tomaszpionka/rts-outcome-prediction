---
reviewer: reviewer-adversarial
model: claude-opus-4-6
date: 2026-04-15
plan: planning/plan_sc2egset_01_02_04_pass3.md
revision: v2 (re-review after C1/C2/M1/M2 claimed fixes)
---

# Adversarial Critique v2 — plan_sc2egset_01_02_04_pass3

## VERDICT: NEEDS REVISION

One functional blocker will crash the notebook at execution time. The
claimed C1 fix references a variable that does not contain the data the
plan expects.

---

## Resolved Issues (confirmed fixed from v1)

### C2 (filename classification) — RESOLVED

The v1 critique raised that `map_aliases_raw.filename` was classified as
`identifier` without distinguishing it from replay-identity columns. The
v2 plan (lines 513-529) now includes a `classification_note` that
explicitly states: "filename is the match identifier — sc2egset raw JSONs
contain no internal match IDs; the filename (relative path from raw_dir)
uniquely identifies the source replay. Consistent with Invariant I10."

Verification: Invariant I10 (`.claude/scientific-invariants.md`, lines
130-159) indeed covers the `filename` convention for raw tables: "Every
raw ingestion output [...] must carry a `filename` column storing the
source file's path relative to that dataset's `raw_dir` root." The
reference is valid.

However, there is a factual problem with the note's content for
`map_aliases_raw` specifically. The note says "filename is the match
identifier" but for `map_aliases_raw`, `filename` is the path to the
mapping JSON file (per `map_aliases_raw.yaml` line 25: "Path to the
mapping JSON file, relative to raw_dir"), NOT the replay file. The
`map_aliases_raw` table has rows like `(tournament, foreign_name,
english_name, <path_to_mapping_json>)` — the filename points to
`<tournament>/map_foreign_to_english_mapping.json`, not to
`*.SC2Replay.json`. Calling this "the match identifier" is factually
incorrect for this specific table.

Severity: downgraded from BLOCKER to WARNING (see N2 below). The
structural classification is defensible; only the prose is wrong.

### M1 (performance guard inlined) — RESOLVED

The v2 plan (lines 193-215) now includes timing instrumentation inline in
T01 with a 60-second split threshold and fallback strategy. This was
previously buried in "Open Questions." Confirmed present in the plan
text. Additionally, the gate condition (line 919-920) now includes
"game_events_raw row count confirmed."

### M2 (MMR threshold justification) — RESOLVED

The v2 plan (lines 744-768) removes the false "~10pp random-chance
deviation" claim and replaces it with an honest characterization: "This
is a labeling convention, not a statistical test or analytical decision
boundary." The corrected standard error calculation (0.18pp vs the
previously claimed ~10pp) is documented at lines 750-753. The constant
is named `_MMR_ZERO_SPREAD_THRESHOLD_PP` with "display only" annotation.

### M4 (undefined variable names) — RESOLVED

The v2 plan now explicitly assigns query results to named variables in
T01-T04 (e.g., line 186: `ge_summary = con.execute(GE_SUMMARY_SQL).df()`,
line 272: `te_summary = con.execute(TE_SUMMARY_SQL).df()`). T08 can now
reference these variables without re-executing queries.

### M6 (replays_meta_raw filename uniqueness assumption) — RESOLVED

The v2 plan (lines 94-103) now documents this assumption explicitly in
the "Assumptions & unknowns" section, including the justification that
the single-CTAS ingestion path makes duplicates structurally impossible.

---

## New Critical Issues (must fix before execution)

### N1. [BLOCKER] T07 SQ histogram fix will crash — `sq_no_sentinel` does not have an `"SQ"` column

**The claimed C1 fix is broken.**

The v2 plan (line 704) proposes:

```python
_n_bins = int(np.histogram_bin_edges(sq_no_sentinel["SQ"].to_numpy(), bins="auto").size - 1)
```

And line 710:

```python
axes[0].hist(sq_no_sentinel["SQ"], bins=_n_bins, edgecolor="black", alpha=0.7)
```

This will raise `KeyError: 'SQ'` because `sq_no_sentinel` does NOT
contain a column named `"SQ"`.

**Evidence:** The notebook defines `sq_no_sentinel` at line 553:

```python
sq_no_sentinel = con.execute(SQ_NO_SENTINEL_SQL).df()
```

The `SQ_NO_SENTINEL_SQL` query (lines 538-552) is:

```sql
SELECT
    MIN(SQ) AS min_val,
    MAX(SQ) AS max_val,
    ROUND(AVG(SQ), 2) AS mean_val,
    ROUND(MEDIAN(SQ), 2) AS median_val,
    ROUND(STDDEV(SQ), 2) AS stddev_val,
    PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY SQ) AS p05,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY SQ) AS p25,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY SQ) AS p75,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY SQ) AS p95,
    COUNT(*) AS n_rows
FROM replay_players_raw
WHERE SQ IS NOT NULL AND SQ != -2147483648
```

This returns a single-row DataFrame with columns: `min_val`, `max_val`,
`mean_val`, `median_val`, `stddev_val`, `p05`, `p25`, `p75`, `p95`,
`n_rows`. It is an **aggregate statistics row**, not the raw SQ values.
There is no column `"SQ"` in this DataFrame.

The v1 critique's suggestion (a) was "use the already-computed
`sq_no_sentinel` data (line 553)" — but this suggestion was itself
flawed, because the reviewer (myself, in v1) did not verify the SQL
output schema. The planner adopted a broken suggestion.

**Fix required:** The plan cannot use `sq_no_sentinel` for
`np.histogram_bin_edges`. It must either:

(a) Create a NEW query that fetches raw SQ values with sentinel exclusion:
    ```python
    SQ_CLEAN_DATA_SQL = """\
    SELECT SQ FROM replay_players_raw
    WHERE SQ IS NOT NULL AND SQ != -2147483648
    """
    sq_clean = con.execute(SQ_CLEAN_DATA_SQL).df()
    ```
    Then: `np.histogram_bin_edges(sq_clean["SQ"].to_numpy(), bins="auto")`
    And: `axes[0].hist(sq_clean["SQ"], bins=_n_bins, ...)`

(b) Filter the existing `sq_data` variable (defined at line 666-668,
    which fetches `SELECT SQ FROM replay_players_raw WHERE SQ IS NOT NULL`):
    ```python
    _sq_clean = sq_data[sq_data["SQ"] != -2147483648]
    _n_bins = int(np.histogram_bin_edges(_sq_clean["SQ"].to_numpy(), bins="auto").size - 1)
    ```

Option (b) avoids a redundant full-table scan but requires that the
sentinel filter is applied consistently to both the bin computation AND
the `ax.hist()` data. Option (a) is cleaner and makes the sentinel
exclusion explicit in SQL.

**Invariant:** #6 (the SQL that produces plotted data must be auditable)
and #7 (the bin derivation must reflect the actual data being plotted).

---

## New Minor Issues (should fix)

### N2. [WARNING] `map_aliases_raw` classification_note says "match identifier" but filename is NOT a replay path

**Evidence:** The plan's T05 entry for `map_aliases_raw` (lines 517-529):

```python
"classification_note": (
    "...filename is the match identifier — sc2egset raw JSONs contain "
    "no internal match IDs; the filename (relative path from raw_dir, "
    "e.g. '2016_BrainGaming.SC2Replay.json') uniquely identifies the "
    "source replay. All raw tables are joined via filename. "
    "Consistent with Invariant I10 (raw table filename convention)."
),
```

The example value `'2016_BrainGaming.SC2Replay.json'` implies this is a
replay filename. But per `map_aliases_raw.yaml` provenance:
`source_files_pattern: data/raw/<tournament>/map_foreign_to_english_mapping.json`.
The `filename` column in `map_aliases_raw` points to
`<tournament>/map_foreign_to_english_mapping.json`, NOT to replay files.
The claim "All raw tables are joined via filename" is false for
`map_aliases_raw` — you cannot join `map_aliases_raw.filename` to
`replay_players_raw.filename` because they point to different file types.

**Fix:** Rewrite the `map_aliases_raw` classification_note to honestly
state that `filename` is the source mapping file path (per Invariant
I10), not a replay identifier. Remove the "All raw tables are joined via
filename" claim and the misleading example. Acknowledge that the join key
between `map_aliases_raw` and replay tables is `map_name` (or
`foreign_name`/`english_name`), not `filename`.

### N3. [WARNING] T08 execution command lacks `--ExecutePreprocessor.timeout`

**Evidence:** The T08 execution command (plan line 859) is:

```
source .venv/bin/activate && poetry run jupyter execute \
  sandbox/sc2/sc2egset/.../01_02_04_univariate_census.ipynb
```

`jupyter execute` uses the nbclient default timeout of **30 seconds per
cell** (confirmed by prior critique
`planning/plan_aoe2companion_01_02_04_fix.critique.md` line 57, which
flagged the identical issue for aoe2companion). The `notebook_config.toml`
documents a 600-second timeout, but `jupyter execute` does not read that
TOML file — it is a documentation convention, not wired into the
execution command.

T01 adds queries scanning the 608M-row `game_events_raw` view. The plan
itself estimates 30-90 seconds for these queries (line 200). A single
cell executing `GE_SUMMARY_SQL` (with two `COUNT(DISTINCT)` calls on
608M rows) could easily exceed 30 seconds, causing the notebook to abort.

Other plans in this project already use `--ExecutePreprocessor.timeout`:
- `plan_aoe2companion_01_02_04_pass2.md` line 481: `--ExecutePreprocessor.timeout=1800`
- `plan_aoestats_01_02_05.md` line 612: `--ExecutePreprocessor.timeout=1800`

**Fix:** Change the T08 execution command to:

```
source .venv/bin/activate && poetry run jupyter execute \
  sandbox/sc2/sc2egset/.../01_02_04_univariate_census.ipynb \
  --ExecutePreprocessor.timeout=1800
```

### N4. [WARNING] `assert 5 <= _n_bins <= 500` lower bound may be too restrictive

The plan adds `assert 5 <= _n_bins <= 500` to all 5 histogram bin
computations (line 734-738). For the current 5 histograms (MMR, APM, SQ,
supplyCappedPercent, duration_min), all have N > 20,000 rows with
continuous distributions, so `bins="auto"` will produce well above 5
bins. The assertion will pass.

However, the assertion text says "check input data for sentinels or
extreme outliers" — this is the right diagnostic. The lower bound of 5 is
not justified by any cited source or data property. Sturges' rule at N=10
gives `ceil(1 + log2(10)) = 5` bins, so 5 bins would only be produced for
extremely small datasets. For the current notebook's data sizes, the
lower bound is not a practical concern, but it should be noted that the
"5" is itself an unjustified threshold (arguably a minor Invariant #7
tension, though for a sanity-check assertion rather than an analytical
parameter).

Severity: NOTE. Not a blocker because no current histogram will trigger
it. But if this assertion pattern is copied to future notebooks with
smaller datasets or low-cardinality columns, it could cause unexpected
failures. Document the `5` as "minimum for Sturges at N=10" or similar.

### N5. [NOTE] FIELD_CLASSIFICATION structural inconsistency: per-table `classification_note` vs top-level `classification_notes`

The existing `FIELD_CLASSIFICATION` dict uses a top-level key
`classification_notes` (plural, at lines 1057-1069) for category-level
descriptions. The plan's T05 adds per-table `classification_note`
(singular) inside each new table's dict entry.

This creates two different patterns for storing notes:
- Old tables: no per-table note; category notes in `classification_notes`
- New tables: per-table `classification_note` with table-specific context

The assertion code correctly excludes `classification_note` with
`if k != "classification_note"` (line 543), so functionality is not
affected. But an examiner reviewing the JSON artifact would see an
inconsistent structure. The plan should acknowledge this is intentional
(per-table notes add context that the generic category notes cannot
provide) or refactor old tables to match.

### N6. [NOTE] T06 `pos_col_results` variable does not exist in the current notebook

T06 proposes storing positional column results in a `pos_col_results`
dict (plan lines 594-600). This requires modifying the existing loop at
notebook lines 568-579 to assign results. The current loop assigns to a
local `df` variable that is overwritten each iteration.

T08 then references `pos_col_results` when building the JSON artifact
(plan line 820-823). This dependency is implicit — T06 creates the
variable, T08 consumes it. The plan documents this correctly, but the
executor must ensure T06 is executed before T08 (which should be natural
given sequential cell order).

This is not a flaw — just noting the dependency chain for the executor.

### N7. [NOTE] M3 (T04 variable name) still present in v2 plan

The v1 critique noted that T04 step 4 references
`distinct_foreign_name_cardinality` but the SQL uses
`foreign_name_cardinality`. This v1 note (M3) does not appear to have
been addressed in the v2 revision. The plan text at lines 458-460 says:
"verify with: `foreign_name_cardinality` should be 1,488; total_rows
should be 70 * 1,488 = 104,160."

Actually, re-reading more carefully: the v2 plan uses the correct name
`foreign_name_cardinality` at line 459. So M3 was silently fixed. This
is confirmed resolved.

---

## Gate Condition Assessment

The gate condition (plan lines 892-921) has 9 items. Assessment:

1. **"All 6 raw tables profiled"** — Adequate. Verifiable by reading the
   markdown artifact.

2. **"JSON artifact complete"** — Adequate. Specific key names listed.

3. **"FIELD_CLASSIFICATION covers 6 tables"** — Adequate. Column-count
   assertions provide a machine-checkable verification.

4. **"Positional SQL in artifact"** — Adequate. Grep-checkable.

5. **"No magic bin counts"** — Improved from v1. The v2 plan adds
   `assert 5 <= _n_bins <= 500` as a bin-count sanity check (addressing
   the v1 gap). This is adequate, contingent on N1 being fixed (without
   the fix, the SQ bin computation will crash before reaching the
   assertion).

6. **"Threshold justified"** — Adequate. Named constant with honest
   characterization.

7. **"SQ histogram uses sentinel-excluded data"** — **CANNOT BE MET as
   written.** The gate says "bin edges and plot data both use
   `sq_no_sentinel`." But `sq_no_sentinel` does not contain raw SQ values
   (see N1). The gate condition must be updated to reference whatever
   variable the fix creates (e.g., `sq_clean` or a filtered `sq_data`).

8. **"game_events_raw row count confirmed"** — Adequate.

9. **"Notebook executes end-to-end"** — Necessary but insufficient
   without the timeout fix (N3). With the default 30s per-cell timeout,
   the notebook will likely abort during T01's 608M-row queries.

**Overall gate assessment:** Gate item 7 is tightly coupled to the N1
blocker. Fixing N1 requires updating gate item 7's variable reference.
Gate item 9 requires fixing N3 to be achievable.

---

## Summary of Required Actions

| ID | Severity | Action |
|----|----------|--------|
| N1 | BLOCKER  | T07: `sq_no_sentinel` is aggregate stats, not raw data — cannot be used for `np.histogram_bin_edges` or `ax.hist()`. Create a new sentinel-filtered query or filter `sq_data` inline. Update gate condition item 7 accordingly. |
| N2 | WARNING  | T05: `map_aliases_raw` classification_note falsely calls `filename` a "match identifier" and claims "all raw tables are joined via filename." Rewrite to reflect that `filename` is the mapping JSON path. |
| N3 | WARNING  | T08: Add `--ExecutePreprocessor.timeout=1800` to the `jupyter execute` command. Without it, 608M-row queries will exceed the 30s default and abort. |
| N4 | WARNING  | T07: Document `5` lower bound in bin-count assertion as "minimum for Sturges at N=10" or remove the lower bound. |
| N5 | NOTE     | T05: Acknowledge structural divergence between per-table `classification_note` and top-level `classification_notes`. |
| N6 | NOTE     | T06: Implicit dependency — `pos_col_results` created in T06, consumed in T08. No action needed; noted for executor. |
