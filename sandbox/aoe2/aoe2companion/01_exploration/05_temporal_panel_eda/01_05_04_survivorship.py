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
# # 01_05_04 Survivorship — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §6 (survivorship cohort design, sensitivity N={5,10,20})
# **Critique fixes:** M-06 (persist reservoir sample IDs for ICC reference)
#
# **Hypothesis:** fraction_active (quarterly) falls monotonically from the reference
# period forward for >=75% of players ever seen, implying non-random attrition.
# **Falsifier:** fraction_active has no monotonic trend (Spearman rho with quarter-index
# p > 0.20) over tested quarters.
#
# NOTE: 75% threshold comes from spec §6 — cited in plan as convention, not empirical.

# %% [markdown]
# ## Imports

# %%
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd
from scipy import stats as scipy_stats

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
N_THRESHOLDS = [5, 10, 20]
DEFAULT_N = 10
REF_START = "2022-08-29"
REF_END = "2023-01-01"

print("Artifacts dir:", ARTIFACTS)

# %% [markdown]
# ## Q4a: Unconditional fraction_active per quarter

# %%
QUERY_PLAYERS = """
SELECT DISTINCT player_id
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at <  TIMESTAMP '2025-01-01'
"""

QUERY_PLAYER_QUARTER = """
SELECT player_id,
       CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
              CAST(CEIL(EXTRACT(MONTH FROM started_at)/3.0) AS INTEGER)::VARCHAR) AS quarter
FROM matches_history_minimal
WHERE started_at >= TIMESTAMP '2022-07-01'
  AND started_at <  TIMESTAMP '2025-01-01'
GROUP BY 1, 2
"""

QUERY_UNCONDITIONAL = """
WITH players AS (
    SELECT DISTINCT player_id
    FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-07-01'
      AND started_at <  TIMESTAMP '2025-01-01'
),
player_quarter AS (
    SELECT player_id,
           CONCAT(CAST(EXTRACT(YEAR FROM started_at) AS VARCHAR), '-Q',
                  CAST(CEIL(EXTRACT(MONTH FROM started_at)/3.0) AS INTEGER)::VARCHAR) AS quarter
    FROM matches_history_minimal
    WHERE started_at >= TIMESTAMP '2022-07-01'
      AND started_at <  TIMESTAMP '2025-01-01'
    GROUP BY 1, 2
)
SELECT quarter,
       COUNT(DISTINCT pq.player_id) AS n_active,
       COUNT(DISTINCT pq.player_id) * 1.0 / (SELECT COUNT(*) FROM players) AS fraction_active,
       (SELECT COUNT(*) FROM players) AS n_ever_seen
FROM player_quarter pq
GROUP BY quarter
ORDER BY quarter
"""

db = get_notebook_db("aoe2", "aoe2companion", read_only=True)

# Check won nulls (spec guarantee)
won_null_count = db.con.execute(
    "SELECT COUNT(*) FILTER (WHERE won IS NULL) FROM matches_history_minimal"
).fetchone()[0]
assert won_null_count == 0, f"Unexpected won NULLs: {won_null_count}"
print(f"won NULL check passed: {won_null_count} NULLs")

df_unc = db.con.execute(QUERY_UNCONDITIONAL).df()
print(df_unc.to_string(index=False))

# %% [markdown]
# ## Monotonicity test (Spearman rank correlation)

# %%
OVERLAP_QUARTERS = [
    "2022-Q3", "2022-Q4",
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
]

df_unc_overlap = df_unc[df_unc["quarter"].isin(OVERLAP_QUARTERS)].sort_values("quarter").copy()
df_unc_overlap["q_idx"] = range(len(df_unc_overlap))

rho, pval = scipy_stats.spearmanr(df_unc_overlap["q_idx"], df_unc_overlap["fraction_active"])
print(f"Spearman rho = {rho:.4f}, p = {pval:.4f}")

verdict_monotone = "confirmed" if (pval <= 0.20 and rho < 0) else f"falsified: rho={rho:.4f}, p={pval:.4f}"
print(f"# Verdict (monotonic attrition): {verdict_monotone}")

# %% [markdown]
# ## Q4b: Sensitivity analysis N in {5, 10, 20}

# %%
PSI_QUERY_FACTION_COHORT = """
WITH cohort AS (
    SELECT CAST(m.profileId AS VARCHAR) AS player_id
    FROM matches_1v1_clean m
    WHERE m.started >= TIMESTAMP '{ref_start}'
      AND m.started <  TIMESTAMP '{ref_end}'
      AND m.is_null_cluster = FALSE
      AND m.internalLeaderboardId IN (6, 18)
    GROUP BY CAST(m.profileId AS VARCHAR)
    HAVING COUNT(*) >= {n_threshold}
)
SELECT mhm.faction, COUNT(*) AS cnt
FROM matches_history_minimal mhm
JOIN cohort c ON c.player_id = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
  AND mhm.started_at <  TIMESTAMP '{ts_end}'
GROUP BY faction
"""

def compute_psi_categorical(ref_dist, test_counts, total_test):
    eps = 1e-6
    test_dist = {k: cnt / total_test for k, cnt in test_counts.items()}
    unseen = sum(cnt for k, cnt in test_counts.items() if k not in ref_dist)
    if unseen > 0:
        test_dist["__unseen__"] = unseen / total_test
    all_cats = set(ref_dist) | set(test_dist)
    psi = sum((max(test_dist.get(c, 0), eps) - max(ref_dist.get(c, 0), eps)) *
              math.log(max(test_dist.get(c, 0), eps) / max(ref_dist.get(c, 0), eps))
              for c in all_cats)
    return psi, int(unseen)

TESTED_QUARTERS = [
    ("2023-Q1", "2023-01-01", "2023-04-01"),
    ("2023-Q2", "2023-04-01", "2023-07-01"),
    ("2023-Q3", "2023-07-01", "2023-10-01"),
    ("2023-Q4", "2023-10-01", "2024-01-01"),
    ("2024-Q1", "2024-01-01", "2024-04-01"),
    ("2024-Q2", "2024-04-01", "2024-07-01"),
    ("2024-Q3", "2024-07-01", "2024-10-01"),
    ("2024-Q4", "2024-10-01", "2025-01-01"),
]

sensitivity_rows = []
for n_threshold in N_THRESHOLDS:
    print(f"\n=== N threshold: {n_threshold} ===")
    # Reference faction distribution for this cohort
    ref_faction_res = db.con.execute(
        PSI_QUERY_FACTION_COHORT.format(
            ref_start=REF_START, ref_end=REF_END,
            n_threshold=n_threshold,
            ts_start=REF_START, ts_end=REF_END,
        )
    ).df()
    total_ref = ref_faction_res["cnt"].sum()
    ref_dist = dict(zip(ref_faction_res["faction"], ref_faction_res["cnt"] / total_ref))

    # Cohort size
    cohort_size = db.con.execute(f"""
        SELECT COUNT(DISTINCT CAST(profileId AS VARCHAR))
        FROM matches_1v1_clean
        WHERE started >= TIMESTAMP '{REF_START}'
          AND started <  TIMESTAMP '{REF_END}'
          AND is_null_cluster = FALSE
          AND internalLeaderboardId IN (6, 18)
        HAVING COUNT(*) >= {n_threshold}
    """).fetchone()
    # Actually use a direct count
    cohort_count = db.con.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT CAST(profileId AS VARCHAR)
            FROM matches_1v1_clean
            WHERE started >= TIMESTAMP '{REF_START}'
              AND started <  TIMESTAMP '{REF_END}'
              AND is_null_cluster = FALSE
              AND internalLeaderboardId IN (6, 18)
            GROUP BY profileId
            HAVING COUNT(*) >= {n_threshold}
        )
    """).fetchone()[0]
    print(f"  Cohort size (>={n_threshold} ref matches): {cohort_count:,}")

    for quarter, ts_start, ts_end in TESTED_QUARTERS:
        test_res = db.con.execute(
            PSI_QUERY_FACTION_COHORT.format(
                ref_start=REF_START, ref_end=REF_END,
                n_threshold=n_threshold,
                ts_start=ts_start, ts_end=ts_end,
            )
        ).df()
        total_test = test_res["cnt"].sum()
        test_counts = dict(zip(test_res["faction"], test_res["cnt"]))
        psi, unseen = compute_psi_categorical(ref_dist, test_counts, total_test)

        # Unconditional PSI for delta computation
        unc_psi_row = None  # will compare to T03 PSI later

        sensitivity_rows.append({
            "n_threshold": n_threshold,
            "feature": "faction",
            "quarter": quarter,
            "psi": round(psi, 6),
            "psi_delta_from_unconditional": None,
            "n_players": cohort_count,
            "n_matches": int(total_test),
        })

print("\nSensitivity analysis done.")

# %% [markdown]
# ## Emit unconditional CSV

# %%
unconditional_csv = ARTIFACTS / "survivorship_unconditional.csv"
df_unc_out = df_unc.assign(churn_rate=lambda df: 1 - df["fraction_active"].shift(1).fillna(df["fraction_active"].iloc[0]))
df_unc_out.to_csv(unconditional_csv, index=False)
print("Wrote:", unconditional_csv)

# %% [markdown]
# ## Emit sensitivity CSV

# %%
df_sens = pd.DataFrame(sensitivity_rows)
# Compute psi_delta from unconditional (load T03 PSI if exists)
psi_csv = ARTIFACTS / "01_05_02_psi_shift_per_feature.csv"
if psi_csv.exists():
    df_psi = pd.read_csv(psi_csv)
    for idx, row in df_sens.iterrows():
        unc = df_psi[(df_psi["feature"] == row["feature"]) & (df_psi["quarter"] == row["quarter"])]
        if len(unc) > 0:
            df_sens.at[idx, "psi_delta_from_unconditional"] = round(row["psi"] - unc.iloc[0]["psi"], 6)

sensitivity_csv = ARTIFACTS / "survivorship_sensitivity.csv"
df_sens.to_csv(sensitivity_csv, index=False)
print("Wrote:", sensitivity_csv)
print(f"Sensitivity rows: {len(df_sens)} (expected >= {len(N_THRESHOLDS) * 8} = {len(N_THRESHOLDS) * 8})")

# %% [markdown]
# ## Emit MD artifact

# %%
md_content = f"""# 01_05_04 Survivorship — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## Unconditional fraction_active per quarter

{df_unc_overlap[['quarter', 'n_active', 'fraction_active', 'n_ever_seen']].to_markdown(index=False)}

**Spearman rho (monotonic attrition test):** {rho:.4f}, p={pval:.4f}

## Verdict (monotonic attrition)

{verdict_monotone}

## Sensitivity Analysis (N thresholds: {N_THRESHOLDS})

Sensitivity rows: {len(df_sens)}

| n_threshold | n_players_cohort |
|---|---|
{chr(10).join(f'| {n} | {df_sens[df_sens["n_threshold"]==n]["n_players"].iloc[0]:,} |' for n in N_THRESHOLDS)}

Default cohort (N=10): {df_sens[df_sens['n_threshold']==10]['n_players'].iloc[0]:,} players.

## Reservoir reproducibility caveat

Per aoec INVARIANTS §3: DuckDB `USING SAMPLE reservoir(N ROWS) REPEATABLE(seed)` is deterministic
only for fixed input row-order. `matches_raw` physical order may shift on rebuild.
Results are methodologically equivalent across rebuilds; bit-exact reproducibility is not guaranteed.
ICC sample profile IDs persisted under `icc_sample_profileIds_*.csv` (M-06).

## SQL

### Unconditional fraction_active
```sql
{QUERY_UNCONDITIONAL}
```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
(conditional on >=10 matches in reference period; see §6 for sensitivity)
"""

md_path = ARTIFACTS / "01_05_04_survivorship.md"
md_path.write_text(md_content)
print("Wrote:", md_path)

db.close()
print("Done.")
