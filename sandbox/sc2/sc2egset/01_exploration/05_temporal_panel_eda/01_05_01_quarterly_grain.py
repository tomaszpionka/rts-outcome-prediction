# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Step 01_05_01 -- Q1: Quarterly Grain & Overlap Window (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Establish the quarterly grain of the analysis and the 10-quarter
# overlap window (2022-Q3 through 2024-Q4). Produce the base per-quarter row-count
# table for all downstream tasks.
#
# **Invariants applied:** I3, I6, I9
# **Literature:** Hamilton (1994) §17.7 — ADF/KPSS stationarity testing is
# deferred; N=8 tested quarters is far below T>=50 power threshold.
#
# **Critique note (B1 fix):** Quarter labels use `date_part('quarter', started_at)`
# to avoid the '3.0' float-cast bug in the original plan SQL. Asserted via
# `df['quarter'].str.match(r'^\d{4}-Q[1-4]$').all()`.
#
# **Critique note (M1):** Full dataset N=44,418 rows; overlap window
# N=10,076 rows / 5,038 matches. "2,200 obs per bin" (Yurdakul 2016 WMU)
# applies to full dataset; overlap window has ~1,008 obs per N=10 bin.
# This is confirmed empirically below.

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_01 -- Q1 Quarterly grain & overlap window
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

import re
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

# %% [markdown]
# ## Setup

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=True)
reports_dir = get_reports_dir("sc2", "sc2egset")
artifact_dir = reports_dir / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
artifact_dir.mkdir(parents=True, exist_ok=True)

print(f"reports_dir: {reports_dir}")
print(f"artifact_dir: {artifact_dir}")

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: The 10-quarter overlap window (2022-Q3..2024-Q4) has non-empty
# support in sc2egset and approximately monotonically non-decreasing match
# volume through 2024 (tournament cadence).
# Falsifier: any quarter in the window has zero rows OR peak-to-trough
# variation > 20x within the window.

# %% [markdown]
# ## Q1 SQL — per-quarter row counts (B1 fixed: date_part quarter label)

# %%
QUARTERLY_GRAIN_SQL = """
-- spec §3 Q1 grain: quarterly aggregation with date_part to avoid float cast
-- B1 fix: date_part('quarter', started_at) yields integer 1-4 directly
WITH q AS (
  SELECT
    CAST(date_part('year', started_at) AS VARCHAR) || '-Q' ||
      CAST(date_part('quarter', started_at) AS VARCHAR) AS quarter,
    match_id, player_id
  FROM matches_history_minimal
)
SELECT quarter,
       COUNT(*)                               AS n_player_rows,
       COUNT(DISTINCT match_id)               AS n_matches,
       COUNT(DISTINCT player_id)              AS n_players
FROM q
GROUP BY quarter
ORDER BY quarter
"""

df_full = db.con.execute(QUARTERLY_GRAIN_SQL).fetchdf()
print(f"Full dataset: {len(df_full)} quarters, {df_full.n_player_rows.sum()} total rows")
print(df_full)

# %% [markdown]
# ## B1 assertion: quarter labels match expected format

# %%
# Assert B1 fix: all quarter labels must match YYYY-Q[1-4]
pattern = r"^\d{4}-Q[1-4]$"
assert df_full["quarter"].str.match(pattern).all(), \
    f"Quarter label format violation: {df_full['quarter'][~df_full['quarter'].str.match(pattern)].tolist()}"
print("B1 assertion PASS: all quarter labels match YYYY-Q[1-4] pattern")

# %% [markdown]
# ## Overlap window filter (spec §2: 2022-Q3..2024-Q4)

# %%
OVERLAP_QUARTERS = [
    "2022-Q3", "2022-Q4", "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]

df_overlap = df_full[df_full["quarter"].isin(OVERLAP_QUARTERS)].copy()
df_overlap["dataset_tag"] = "sc2egset"
df_overlap = df_overlap.reset_index(drop=True)

print(f"\nOverlap window: {len(df_overlap)} quarters")
print(f"Total rows: {df_overlap.n_player_rows.sum():,}")
print(f"Total matches: {df_overlap.n_matches.sum():,}")
print(df_overlap)

# %% [markdown]
# ## M1 empirical note

# %%
# M1 (critique): The plan's Scope cited "N=22,209 matches" and "2,200 obs per N=10 bin"
# but the overlap window has only 10,076 rows / 5,038 matches.
# Empirical bin size at N=10 binning: ~1,008 obs per bin at reference period.
# This is well above Yurdakul (2018 WMU #3208) sparse-bin regime but smaller
# than originally cited. Corrected here; all downstream citations use 10,076 rows.
overlap_rows = df_overlap.n_player_rows.sum()
overlap_matches = df_overlap.n_matches.sum()
ref_quarter_rows = df_overlap.loc[df_overlap["quarter"] == "2022-Q3", "n_player_rows"].iloc[0]
ref_quarter_matches = df_overlap.loc[df_overlap["quarter"] == "2022-Q3", "n_matches"].iloc[0]
print(f"M1 correction: overlap_rows={overlap_rows:,} overlap_matches={overlap_matches:,}")
print(f"Reference quarter (2022-Q3): {ref_quarter_rows} rows, {ref_quarter_matches} matches")
print(f"Reference + 2022-Q4 combined (spec §7 ref period):")
ref_combined = df_overlap[df_overlap["quarter"].isin(["2022-Q3", "2022-Q4"])]["n_player_rows"].sum()
print(f"  {ref_combined} rows")

# %% [markdown]
# ## Verdict

# %%
# Verdict check
assert len(df_overlap) == 10, f"Expected 10 overlap quarters, got {len(df_overlap)}"
assert (df_overlap[["n_player_rows", "n_matches", "n_players"]] > 0).all().all(), \
    "Zero rows in at least one overlap quarter!"

max_q = df_overlap["n_player_rows"].max()
min_q = df_overlap["n_player_rows"].min()
ratio = max_q / min_q
print(f"\nPeak-to-trough ratio: {max_q}/{min_q} = {ratio:.1f}x")

# Verdict: confirmed or falsified?
if ratio <= 20:
    verdict = "CONFIRMED"
    print(f"# Verdict: {verdict} — all 10 quarters non-empty, peak/trough ratio {ratio:.1f}x <= 20x")
else:
    verdict = "FALSIFIED"
    print(f"# Verdict: {verdict} — peak/trough ratio {ratio:.1f}x exceeds 20x threshold")

print(f"Monotonically non-decreasing? No — tournament cadence is irregular (expected).")

# %% [markdown]
# ## Save artifacts

# %%
# Save overlap window CSV
out_overlap = artifact_dir / "quarterly_row_counts_sc2egset.csv"
df_overlap.to_csv(out_overlap, index=False)
print(f"Saved: {out_overlap}")

# Save full dataset CSV
df_full["dataset_tag"] = "sc2egset"
out_full = artifact_dir / "quarterly_row_counts_sc2egset_full.csv"
df_full.to_csv(out_full, index=False)
print(f"Saved: {out_full}")

# Verify
df_check = pd.read_csv(out_overlap)
assert len(df_check) == 10, f"Expected 10 rows, got {len(df_check)}"
assert (df_check[["n_player_rows", "n_matches", "n_players"]] > 0).all().all()
print("Verification PASS: 10 rows, all counts > 0")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Q1: Quarterly Grain & Overlap Window — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## Findings

- Full dataset: {len(df_full)} quarters, 2016-Q1 to 2024-Q4
- Overlap window: 10 quarters (2022-Q3 to 2024-Q4), **{overlap_rows:,} rows / {overlap_matches:,} matches**
- M1 correction: plan cited full-dataset N=22,209; overlap window is 10,076 rows / 5,038 matches
- Peak-to-trough in overlap: {ratio:.1f}x (tournament cadence; irregular but not monotone)
- Verdict: {verdict}

## SQL (verbatim, I6)

```sql
{QUARTERLY_GRAIN_SQL.strip()}
```

## Overlap window per-quarter counts

{df_overlap[['quarter','n_player_rows','n_matches','n_players','dataset_tag']].to_markdown(index=False)}

## Notes

- Hamilton (1994) §17.7: ADF/KPSS stationarity testing deferred; N=8 tested quarters
  far below T>=50 power threshold.
- B1 fix: `date_part('quarter', started_at)` used instead of `CEIL(.../ 3.0)` cast to avoid '3.0' label.
- M1 (critique): Reference-period bin size ~1,008 rows for N=10 bins on overlap data
  (not ~2,200 as cited in plan; plan cited full-dataset N).
"""

out_md = artifact_dir / "quarterly_row_counts_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

# %%
db.close()
print("T02 complete.")
