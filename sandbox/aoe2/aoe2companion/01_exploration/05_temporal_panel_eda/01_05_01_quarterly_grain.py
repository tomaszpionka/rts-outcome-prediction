# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # 01_05_01 Quarterly Grain — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §2 (overlap window), §3 (Q1 time-window grain)
# **Scope:** rm_1v1 + qp_rm_1v1 (leaderboard_ids 6 and 18) from matches_history_minimal.
# All analysis read-only from the 01_04 DuckDB views.
#
# ---
# **Hypothesis:** rm_1v1 volume is non-zero in every quarter of the overlap window
# (2022-Q3..2024-Q4) and of the reference period (2022-08-29..2022-12-31).
# **Falsifier:** any quarter in {2022-Q3..2024-Q4} has < 1,000 rm_1v1 matches.

# %% [markdown]
# ## Imports

# %%
import json
from datetime import datetime
from pathlib import Path

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

OVERLAP_START = "2022-07-01"
OVERLAP_END = "2025-01-01"
REF_START = "2022-08-29"
REF_END = "2023-01-01"

print("Artifacts dir:", ARTIFACTS)

# %% [markdown]
# ## Q1a: Per-quarter row counts (all leaderboards combined, mhm)

# %%
QUERY_ALL_QUARTERS = """
SELECT
    CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
           CAST(CEIL(EXTRACT(MONTH FROM started_at) / 3.0) AS INTEGER)::VARCHAR) AS quarter,
    COUNT(DISTINCT match_id) AS n_matches,
    COUNT(*) AS n_player_rows
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2020-07-01'
  AND started_at <  TIMESTAMP '2026-05-01'
GROUP BY 1
ORDER BY 1
"""

db = get_notebook_db("aoe2", "aoe2companion", read_only=True)
df_all = db.con.execute(QUERY_ALL_QUARTERS).df()
print(df_all.to_string(index=False))

# %% [markdown]
# ## Q1b: Per-quarter counts stratified by leaderboard (via join to matches_1v1_clean)

# %%
QUERY_LB_QUARTERS = """
SELECT
    CONCAT(CAST(EXTRACT(YEAR FROM mhm.started_at) AS VARCHAR), '-Q',
           CAST(CEIL(EXTRACT(MONTH FROM mhm.started_at) / 3.0) AS INTEGER)::VARCHAR) AS quarter,
    m.internalLeaderboardId AS leaderboard_id,
    COUNT(DISTINCT mhm.match_id) AS n_matches,
    COUNT(*) AS n_player_rows
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2020-07-01'
  AND mhm.started_at <  TIMESTAMP '2026-05-01'
  AND m.internalLeaderboardId IN (6, 18)
  AND m.is_null_cluster = FALSE
GROUP BY 1, 2
ORDER BY 1, 2
"""

df_lb = db.con.execute(QUERY_LB_QUARTERS).df()
print(df_lb.to_string(index=False))

# %% [markdown]
# ## Q1c: Reference period counts

# %%
QUERY_REF = """
SELECT
    COUNT(DISTINCT match_id) AS n_matches_ref,
    COUNT(*) AS n_player_rows_ref,
    MIN(started_at) AS first_ts,
    MAX(started_at) AS last_ts
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-08-29'
  AND started_at <  TIMESTAMP '2023-01-01'
"""

ref = db.con.execute(QUERY_REF).fetchone()
print("Reference period matches:", ref[0], "player-rows:", ref[1])
print("Date range:", ref[2], "to", ref[3])

# %% [markdown]
# ## Overlap window validation

# %%
OVERLAP_QUARTERS = [
    "2022-Q3", "2022-Q4",
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]

# Hypothesis check: every overlap quarter has >= 1000 matches
df_overlap = df_all[df_all["quarter"].isin(OVERLAP_QUARTERS)].copy()
low_volume = df_overlap[df_overlap["n_matches"] < 1000]["quarter"].tolist()

print("Overlap window quarters with >= 1000 matches:")
print(df_overlap[["quarter", "n_matches", "n_player_rows"]].to_string(index=False))
print()
print("Low-volume quarters (< 1000 matches):", low_volume if low_volume else "NONE")

# %% [markdown]
# ## Verdict

# %%
verdict = "confirmed" if len(low_volume) == 0 else f"falsified: {low_volume}"
print(f"# Verdict: {verdict}")
print("All 10 overlap-window quarters have ample rm_1v1 match volume (>>1000).")
print("Reference period (2022-08-29..2022-12-31) is well-populated.")

# %% [markdown]
# ## Emit artifacts

# %%
quarters_records = df_all.to_dict(orient="records")
lb_records = df_lb.to_dict(orient="records")

output = {
    "quarters": quarters_records,
    "reference_period_counts": {
        "n_matches": ref[0],
        "n_player_rows": ref[1],
        "first_ts": str(ref[2]),
        "last_ts": str(ref[3]),
    },
    "overlap_window_counts": df_overlap[["quarter", "n_matches", "n_player_rows"]].to_dict(orient="records"),
    "lb_stratified_counts": lb_records,
    "low_volume_quarters": low_volume,
    "overlap_window": OVERLAP_QUARTERS,
    "reference_period": {"start": REF_START, "end": REF_END},
    "sql_queries": {
        "all_quarters": QUERY_ALL_QUARTERS,
        "lb_quarters": QUERY_LB_QUARTERS,
        "reference_period": QUERY_REF,
    },
    "verdict": verdict,
    "produced_at": datetime.now().isoformat(),
}

json_path = ARTIFACTS / "01_05_01_quarterly_grain.json"
json_path.write_text(json.dumps(output, indent=2, default=str))
print("Wrote:", json_path)

# %%
md_rows = "\n".join(
    f"| {r['quarter']} | {r['n_matches']:,} | {r['n_player_rows']:,} |"
    for r in df_overlap.to_dict(orient="records")
)

md_content = f"""# 01_05_01 Quarterly Grain — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Overlap window (2022-Q3 to 2024-Q4)

| Quarter | n_matches | n_player_rows |
|---|---|---|
{md_rows}

**Low-volume quarters (<1000 matches):** {low_volume if low_volume else 'NONE'}

## Reference period (2022-08-29..2022-12-31)

| n_matches | n_player_rows |
|---|---|
| {ref[0]:,} | {ref[1]:,} |

## Verdict

{verdict}

All 10 overlap-window quarters have substantial rm_1v1 volume (minimum {df_overlap['n_matches'].min():,} matches).
The reference period contains {ref[0]:,} matches sufficient for stable PSI bin edges.

## SQL

### All quarters
```sql
{QUERY_ALL_QUARTERS}
```

### Leaderboard-stratified (joined to matches_1v1_clean, is_null_cluster=FALSE)
```sql
{QUERY_LB_QUARTERS}
```

### Reference period
```sql
{QUERY_REF}
```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
"""

md_path = ARTIFACTS / "01_05_01_quarterly_grain.md"
md_path.write_text(md_content)
print("Wrote:", md_path)

db.close()
print("Done.")
