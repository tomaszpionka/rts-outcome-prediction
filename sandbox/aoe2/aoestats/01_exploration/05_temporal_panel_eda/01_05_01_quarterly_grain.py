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
# # Step 01_05_01 -- Quarterly Grain and Overlap Window (Q1)
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_05 -- Temporal & Panel EDA
# **Step:** 01_05_01
# **Dataset:** aoestats
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
#
# # Hypothesis: Every tested quarter 2023-Q1..2024-Q4 has >= 100,000 focal-player-rows
# # in matches_history_minimal, supporting meaningful decile-PSI in T03.
# # Falsifier: Any tested quarter has < 10,000 rows (PSI deciles would contain < 1,000
# # observations each, violating Siddiqi N>=300 per-bin floor).

# %%
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS_DIR = get_reports_dir("aoe2", "aoestats") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
(ARTIFACTS_DIR / "plots").mkdir(exist_ok=True)

db = get_notebook_db("aoe2", "aoestats")
print("DB connected. Artifacts dir:", ARTIFACTS_DIR)

# %%
# Q1 Quarterly grain query — spec §3
QUARTERLY_GRAIN_SQL = """
WITH quarterly AS (
  SELECT
    DATE_TRUNC('quarter', started_at) AS quarter_start,
    CAST(YEAR(started_at) AS VARCHAR) || '-Q' || CAST(QUARTER(started_at) AS VARCHAR) AS quarter_iso,
    COUNT(*) AS row_count,
    COUNT(DISTINCT match_id) AS match_count,
    COUNT(DISTINCT player_id) AS player_count
  FROM matches_history_minimal
  WHERE started_at >= TIMESTAMP '2022-07-01'
    AND started_at < TIMESTAMP '2025-01-01'
  GROUP BY 1, 2
  ORDER BY 1
)
SELECT * FROM quarterly
"""

df_quarterly = db.fetch_df(QUARTERLY_GRAIN_SQL)
print(df_quarterly.to_string())

# %%
# Assert 10 quarters 2022-Q3..2024-Q4
assert len(df_quarterly) == 10, f"Expected 10 quarters, got {len(df_quarterly)}"

expected_quarters = [
    "2022-Q3", "2022-Q4",
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]
actual_quarters = df_quarterly["quarter_iso"].tolist()
assert actual_quarters == expected_quarters, f"Quarter mismatch: {actual_quarters}"
print("Quarter sequence check: PASSED")

# %%
# Falsifier check: any tested quarter (2023-Q1..2024-Q4) with < 10,000 rows?
tested = df_quarterly[df_quarterly["quarter_iso"].str.startswith("202")]
tested_q = tested[tested["quarter_iso"] >= "2023-Q1"]
min_row = tested_q["row_count"].min()
min_quarter = tested_q.loc[tested_q["row_count"].idxmin(), "quarter_iso"]

if min_row < 10_000:
    verdict = "FALSIFIED"
    print(f"Q1 Falsifier verdict: FALSIFIED — quarter {min_quarter} has {min_row} rows < 10,000")
else:
    verdict = "PASSED"
    print(f"Q1 Falsifier verdict: PASSED — min tested quarter rows = {min_row:,} ({min_quarter})")

# %%
# Emit CSV
csv_path = ARTIFACTS_DIR / "quarterly_grain_row_counts.csv"
df_quarterly.to_csv(csv_path, index=False)
print(f"Wrote {csv_path}")

# %%
# Emit JSON with SQL verbatim (I6)
json_path = ARTIFACTS_DIR / "quarterly_grain_row_counts.json"
result = {
    "step": "01_05_01",
    "dataset": "aoestats",
    "spec": "reports/specs/01_05_preregistration.md@7e259dd8",
    "sql_queries": {"quarterly_grain": QUARTERLY_GRAIN_SQL.strip()},
    "row_count": len(df_quarterly),
    "quarters": df_quarterly["quarter_iso"].tolist(),
    "falsifier_verdict": verdict,
    "min_tested_quarter_rows": int(min_row),
    "data": df_quarterly.to_dict(orient="records"),
}
with open(json_path, "w") as f:
    json.dump(result, f, indent=2, default=str)
print(f"Wrote {json_path}")

# %%
# Emit MD artifact
md_path = ARTIFACTS_DIR / "quarterly_grain_row_counts.md"
md_content = f"""# Quarterly Grain Row Counts — aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_01

## SQL

```sql
{QUARTERLY_GRAIN_SQL.strip()}
```

## Results

{df_quarterly.to_markdown(index=False)}

## Falsifier verdict

**Q1 Falsifier:** {verdict}
Minimum tested-quarter rows: {int(min_row):,} ({min_quarter})
"""
md_path.write_text(md_content)
print(f"Wrote {md_path}")

# %%
# Plot: bar + line dual axis
fig, ax1 = plt.subplots(figsize=(12, 5))
quarters = df_quarterly["quarter_iso"]
x = range(len(quarters))

ax1.bar(x, df_quarterly["row_count"], alpha=0.7, color="steelblue", label="Row count")
ax1.set_xlabel("Quarter")
ax1.set_ylabel("Row count", color="steelblue")
ax1.set_xticks(list(x))
ax1.set_xticklabels(quarters, rotation=45, ha="right")
ax1.tick_params(axis="y", labelcolor="steelblue")

ax2 = ax1.twinx()
ax2.plot(x, df_quarterly["player_count"], color="darkorange", marker="o", label="Player count")
ax2.set_ylabel("Unique players", color="darkorange")
ax2.tick_params(axis="y", labelcolor="darkorange")

plt.title("aoestats: Quarterly Row Counts and Unique Players")
plt.tight_layout()
plot_path = ARTIFACTS_DIR / "plots" / "quarterly_row_counts.png"
plt.savefig(plot_path, dpi=150)
plt.close()
print(f"Wrote {plot_path}")

# %%
print(f"Q1 Falsifier verdict: {verdict}")
print("Step 01_05_01 complete.")
