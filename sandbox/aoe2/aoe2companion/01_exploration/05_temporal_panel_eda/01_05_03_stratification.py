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
# # 01_05_03 Stratification — aoe2companion
# spec: reports/specs/01_05_preregistration.md@7e259dd8
#
# **Spec §§:** §5 (stratification variable, regime_id)
# **Critique fix M-02:** Secondary regime is rm_1v1 (lb=6) vs rm_team; but since rm_team is
# out-of-analytical-scope per 01_04_01 R01, we use rm_1v1 (lb=6) vs qp_rm_1v1 (lb=18)
# as the within-aoec secondary regime. Documented as scope-stratification, not ladder-segmentation.
#
# **Hypothesis:** PSI magnitudes on pre-game features differ systematically between
# internalLeaderboardId=6 (rm_1v1) and =18 (qp_rm_1v1) by at least 0.05 (absolute)
# in at least one quarter.
# **Falsifier:** max |PSI(lb=6) - PSI(lb=18)| across feature-quarter cells is < 0.05.

# %% [markdown]
# ## Imports

# %%
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

ARTIFACTS = get_reports_dir("aoe2", "aoe2companion") / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

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
REF_START = "2022-08-29"
REF_END = "2023-01-01"

print("Artifacts dir:", ARTIFACTS)

# %% [markdown]
# ## Note on regime_id identity and secondary-regime scope

# %%
REGIME_NOTE = """
M-02 deviation note (pre-authorized by critique):
- Spec §5 names 'rm_1v1 / rm_team' as the secondary leaderboard regime for aoec.
- rm_team is out-of-analytical-scope per 01_04_01 R01 (non-1v1 matches excluded from the primary substrate).
- Secondary regime implemented as rm_1v1 (lb=6) vs qp_rm_1v1 (lb=18) — scope-stratification within the
  1v1 substrate, not ladder-segmentation.
- Labeled [WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET] in all outputs.
- Research log records: 'secondary regime analysis rm_1v1/qp_rm_1v1 is scope-stratification, not ladder-segmentation.'
- regime_id ≡ calendar quarter for cross-dataset purposes (spec §3 preserved).
"""
print(REGIME_NOTE)

# %% [markdown]
# ## Compute lb-specific reference distributions

# %%
def compute_psi_categorical(ref_dist, test_counts, total_test, unseen_label="__unseen__"):
    eps = 1e-6
    test_dist = {}
    unseen_count = 0
    for k, cnt in test_counts.items():
        if k in ref_dist:
            test_dist[k] = cnt / total_test
        else:
            unseen_count += cnt
    if unseen_count > 0:
        test_dist[unseen_label] = unseen_count / total_test
    all_cats = set(ref_dist.keys()) | set(test_dist.keys())
    psi = 0.0
    for cat in all_cats:
        p_r = max(ref_dist.get(cat, 0.0), eps)
        p_t = max(test_dist.get(cat, 0.0), eps)
        psi += (p_t - p_r) * math.log(p_t / p_r)
    return psi, unseen_count

# %%
db = get_notebook_db("aoe2", "aoe2companion", read_only=True)

# Reference faction distributions by leaderboard
QUERY_REF_FACTION_BY_LB = """
SELECT m.internalLeaderboardId AS lb, mhm.faction, COUNT(*) AS cnt
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
GROUP BY lb, faction
"""

df_ref_faction_lb = db.con.execute(QUERY_REF_FACTION_BY_LB).df()
ref_faction_by_lb = {}
for lb in [6, 18]:
    sub = df_ref_faction_lb[df_ref_faction_lb["lb"] == lb]
    total = sub["cnt"].sum()
    ref_faction_by_lb[lb] = dict(zip(sub["faction"], sub["cnt"] / total))
    print(f"lb={lb}: {len(sub)} distinct factions, total ref rows: {total:,}")

# %% [markdown]
# ## Per-quarter, per-lb PSI computation

# %%
rows = []

for quarter, ts_start, ts_end in TESTED_QUARTERS:
    print(f"\n{quarter}")
    for lb in [6, 18]:
        # Faction PSI
        faction_res = db.con.execute(f"""
            SELECT mhm.faction, COUNT(*) AS cnt
            FROM matches_history_minimal mhm
            JOIN matches_1v1_clean m
              ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
             AND CAST(m.profileId AS VARCHAR) = mhm.player_id
            WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
              AND mhm.started_at <  TIMESTAMP '{ts_end}'
              AND m.is_null_cluster = FALSE
              AND m.internalLeaderboardId = {lb}
            GROUP BY mhm.faction
        """).df()
        total_test_faction = faction_res["cnt"].sum()
        faction_counts = dict(zip(faction_res["faction"], faction_res["cnt"]))
        psi_faction, unseen_faction = compute_psi_categorical(ref_faction_by_lb[lb], faction_counts, total_test_faction)

        # Win rate
        won_res = db.con.execute(f"""
            SELECT AVG(CAST(mhm.won AS DOUBLE)) AS p_won, COUNT(*) AS n_won
            FROM matches_history_minimal mhm
            JOIN matches_1v1_clean m
              ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
             AND CAST(m.profileId AS VARCHAR) = mhm.player_id
            WHERE mhm.started_at >= TIMESTAMP '{ts_start}'
              AND mhm.started_at <  TIMESTAMP '{ts_end}'
              AND m.is_null_cluster = FALSE
              AND m.internalLeaderboardId = {lb}
              AND mhm.won IS NOT NULL
        """).fetchone()
        p_won = won_res[0]
        n_won = won_res[1]

        rows.append({
            "quarter": quarter,
            "leaderboard_id": lb,
            "lb_name": "rm_1v1" if lb == 6 else "qp_rm_1v1",
            "feature": "faction",
            "psi": round(psi_faction, 6),
            "cohen_h": None,
            "cohen_d": None,
            "ks_stat": None,
            "n_test": int(total_test_faction),
            "unseen_count": int(unseen_faction),
            "scope_note": "[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]",
        })
        rows.append({
            "quarter": quarter,
            "leaderboard_id": lb,
            "lb_name": "rm_1v1" if lb == 6 else "qp_rm_1v1",
            "feature": "won",
            "psi": None,
            "cohen_h": round(float(2 * (math.asin(math.sqrt(max(0, min(1, p_won)))) - math.asin(math.sqrt(0.5)))), 6),
            "cohen_d": None,
            "ks_stat": None,
            "n_test": int(n_won),
            "unseen_count": 0,
            "scope_note": "[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]",
        })

        print(f"  lb={lb}: faction_psi={psi_faction:.4f}, won={p_won:.4f}")

db.close()
print("\nAll done.")

# %% [markdown]
# ## Verdict

# %%
df_strat = pd.DataFrame(rows)
faction_rows = df_strat[df_strat["feature"] == "faction"].copy()
lb6 = faction_rows[faction_rows["leaderboard_id"] == 6].set_index("quarter")["psi"]
lb18 = faction_rows[faction_rows["leaderboard_id"] == 18].set_index("quarter")["psi"]
max_diff = (lb6 - lb18).abs().max()

print(f"Max |PSI(lb=6) - PSI(lb=18)| for faction: {max_diff:.4f}")
verdict = "confirmed" if max_diff >= 0.05 else "falsified: max diff < 0.05"
print(f"# Verdict: {verdict}")
print()
print("regime_id ≡ calendar quarter (spec §3 preserved for cross-dataset comparison).")
print("Secondary-regime lb=6 vs lb=18 is within-aoec scope-stratification only.")

# %% [markdown]
# ## Emit artifacts

# %%
strat_json = {
    "regime_id_note": "regime_id ≡ calendar quarter for cross-dataset purposes (spec §3). Secondary regime lb=6/lb=18 is within-aoec scope-stratification.",
    "m02_deviation": "Secondary regime is rm_1v1 (lb=6) vs qp_rm_1v1 (lb=18). rm_team excluded per 01_04_01 R01. This is scope-stratification, not ladder-segmentation.",
    "max_faction_psi_diff_lb6_lb18": round(float(max_diff), 6),
    "verdict": verdict,
    "sql_queries": {
        "ref_faction_by_lb": QUERY_REF_FACTION_BY_LB,
    },
    "produced_at": datetime.now().isoformat(),
}

json_path = ARTIFACTS / "01_05_03_stratification.json"
json_path.write_text(json.dumps(strat_json, indent=2))
print("Wrote:", json_path)

csv_path = ARTIFACTS / "01_05_03_stratification_per_lb.csv"
df_strat.to_csv(csv_path, index=False)
print("Wrote:", csv_path)

md_content = f"""# 01_05_03 Stratification — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## regime_id ≡ calendar quarter

Per spec §3, the cross-dataset `regime_id ≡ calendar quarter` identity is preserved.
The secondary-regime analysis below is `[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]`.

## M-02 Deviation Note (pre-authorized)

Spec §5 names `rm_1v1 / rm_team` as the secondary leaderboard regime for aoec.
`rm_team` is out-of-analytical-scope per 01_04_01 R01 (non-1v1 matches excluded from primary substrate).
Secondary regime is implemented as `rm_1v1 (lb=6) vs qp_rm_1v1 (lb=18)`.
Research log records: "secondary regime analysis rm_1v1/qp_rm_1v1 is scope-stratification, not ladder-segmentation."

## Results

Max |PSI(lb=6) - PSI(lb=18)| for faction: **{max_diff:.4f}**

Verdict: **{verdict}**

## SQL

```sql
{QUERY_REF_FACTION_BY_LB}
```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
_[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]_
"""

md_path = ARTIFACTS / "01_05_03_stratification.md"
md_path.write_text(md_content)
print("Wrote:", md_path)
print("Done.")
