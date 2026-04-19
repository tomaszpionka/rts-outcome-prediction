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
# # Step 01_05_03 -- Q3: Stratification & Secondary Regime (tournament_era) (sc2egset)
#
# **spec:** reports/specs/01_05_preregistration.md@7e259dd8
# **Dataset:** sc2egset
# **Branch:** feat/01-05-sc2egset
# **Date:** 2026-04-18
#
# **Objective:** Record that regime_id ≡ quarter at cross-dataset level. Define
# within-dataset secondary regime tournament_era via committed lookup table.
#
# **Critique fixes applied:**
# - M2: Hand-mapped tournament_tier_lookup.csv (70 rows, Liquipedia tier) used
#       instead of ILIKE heuristic. All 70 dirs explicitly classified.
# - M8: Join via matches_flat_clean (has replay_id), not replays_meta_raw.
#       Match: `substr(m.match_id, 11) = t.replay_id`
# - M7: [POP:tournament] tag added to notes column.
#
# **Literature:**
# - spec §5: regime_id ≡ calendar quarter — cross-dataset stratification IS
#   stratification by time.

# %%
# spec: reports/specs/01_05_preregistration.md@7e259dd8
# Step 01_05_03 -- Q3 Stratification & regime (sc2egset)
# Dataset: sc2egset  Branch: feat/01-05-sc2egset  Date: 2026-04-18

from pathlib import Path

import pandas as pd

from rts_predict.common.notebook_utils import get_notebook_db, get_reports_dir

# %%
db = get_notebook_db("sc2", "sc2egset", read_only=True)
reports_dir = get_reports_dir("sc2", "sc2egset")
artifact_dir = reports_dir / "artifacts" / "01_exploration" / "05_temporal_panel_eda"
artifact_dir.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Hypothesis

# %%
# Hypothesis: tournament_era is confounded with quarter at the cross-dataset
# level but is a meaningful within-dataset categorical whose distribution of
# 'won' differs materially (|diff| > 0.02) across tiers.
# Falsifier: tier-to-tier win-rate diff <= 0.005 -> tier is noise, not regime.

# %% [markdown]
# ## spec §5 honest statement (verbatim)

# %%
SPEC5_STATEMENT = (
    "regime_id ≡ calendar quarter. Cross-dataset stratification by "
    "regime_id IS stratification by time, identical to the Q1 grain. It "
    "provides no additional variance reduction beyond Q1."
)
print("spec §5:", SPEC5_STATEMENT)

# %% [markdown]
# ## Load hand-mapped tournament tier lookup (M2 fix: no ILIKE heuristic)

# %%
lookup_path = artifact_dir / "tournament_tier_lookup.csv"
df_lookup = pd.read_csv(lookup_path)
print(f"Loaded tournament_tier_lookup.csv: {len(df_lookup)} rows")
print(df_lookup["tier"].value_counts())
assert len(df_lookup) == 70, f"Expected 70 tournament dirs, got {len(df_lookup)}"

# %% [markdown]
# ## Build tournament era map via matches_flat_clean (M8 fix)

# %%
# M8 fix: Use matches_flat_clean (has filename + replay_id), not replays_meta_raw.
# Extract tournament_dir from filename (split_part(filename,'/',1)).
# Join to matches_history_minimal via: substr(m.match_id, 11) = mfc.replay_id
TOURNAMENT_MAP_SQL = """
SELECT
  mfc.replay_id,
  split_part(mfc.filename, '/', 1) AS tournament_dir
FROM matches_flat_clean mfc
"""

df_map = db.con.execute(TOURNAMENT_MAP_SQL).fetchdf()
print(f"Tournament map: {len(df_map)} rows, {df_map['tournament_dir'].nunique()} distinct dirs")

# Merge with lookup to get tier
df_map_tier = df_map.merge(df_lookup[["tournament_dir", "tier"]], on="tournament_dir", how="left")
unmapped = df_map_tier["tier"].isna().sum()
print(f"Unmapped rows: {unmapped}")
if unmapped > 0:
    print("Unmapped dirs:", df_map_tier[df_map_tier["tier"].isna()]["tournament_dir"].unique())

# %% [markdown]
# ## Join to matches_history_minimal (overlap window)

# %%
# Join: substr(m.match_id, 11) = mfc.replay_id (match_id = 'sc2egset::' + replay_id)
WIN_RATE_SQL = """
WITH era_map AS (
  SELECT
    mfc.replay_id,
    split_part(mfc.filename, '/', 1) AS tournament_dir
  FROM matches_flat_clean mfc
),
joined AS (
  SELECT
    m.match_id,
    m.player_id,
    m.won,
    m.started_at,
    em.tournament_dir
  FROM matches_history_minimal m
  JOIN era_map em ON substr(m.match_id, 11) = em.replay_id
  WHERE m.started_at >= TIMESTAMP '2022-07-01'
    AND m.started_at <  TIMESTAMP '2025-01-01'
)
SELECT
  tournament_dir,
  COUNT(*) AS n,
  AVG(CAST(won AS DOUBLE)) AS mean_won
FROM joined
GROUP BY tournament_dir
ORDER BY tournament_dir
"""

df_win_by_dir = db.con.execute(WIN_RATE_SQL).fetchdf()
print(f"Win rate by tournament dir: {len(df_win_by_dir)} rows")

# Merge with tier
df_win_by_dir = df_win_by_dir.merge(df_lookup[["tournament_dir", "tier"]], on="tournament_dir", how="left")
print(df_win_by_dir[["tournament_dir", "tier", "n", "mean_won"]].head(10).to_string())

# %% [markdown]
# ## Aggregate to tier level

# %%
df_tier = (
    df_win_by_dir.groupby("tier")
    .agg(n=("n", "sum"), mean_won=("mean_won", "mean"))
    .reset_index()
    .sort_values("tier")
)
df_tier["notes"] = "[POP:tournament]"
print("\nTier-level win rates:")
print(df_tier.to_string())

# Verdict: check win-rate diff across tiers
win_rates = df_tier["mean_won"].values
max_diff = max(abs(win_rates[i] - win_rates[j]) for i in range(len(win_rates)) for j in range(i + 1, len(win_rates)))
print(f"\nMax tier-to-tier win-rate diff: {max_diff:.4f}")
if max_diff > 0.02:
    verdict = "CONFIRMED"
    print(f"# Verdict: {verdict} — tier is a meaningful regime (diff={max_diff:.4f} > 0.02)")
elif max_diff > 0.005:
    verdict = "INCONCLUSIVE"
    print(f"# Verdict: {verdict} — diff={max_diff:.4f} between thresholds 0.005 and 0.02")
else:
    verdict = "FALSIFIED"
    print(f"# Verdict: {verdict} — tier diff={max_diff:.4f} <= 0.005 (noise)")

# %% [markdown]
# ## Save artifacts

# %%
out_tier = artifact_dir / "tournament_era_sc2egset.csv"
df_tier.to_csv(out_tier, index=False)
print(f"Saved: {out_tier}")

# Verify >=1 row per tier (some tiers may be empty in overlap window)
print(f"Tiers in output: {df_tier['tier'].tolist()}")
for tier in ["Bronze", "Silver", "Gold", "Platinum"]:
    if tier not in df_tier["tier"].values:
        print(f"  NOTE: tier '{tier}' is empty in overlap window — recorded explicitly.")

# %% [markdown]
# ## Markdown report

# %%
md_content = f"""# Q3: Stratification & Secondary Regime (tournament_era) — sc2egset

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Date:** 2026-04-18

## spec §5 honest statement

{SPEC5_STATEMENT}

## Method

- Tournament tier lookup: hand-mapped 70 tournament dirs via Liquipedia tier heuristics
  (source: tournament_tier_lookup.csv; M2 fix — no ILIKE heuristic).
- Join: `substr(m.match_id, 11) = mfc.replay_id` (M8 fix — uses matches_flat_clean).
- Population: overlap window 2022-Q3..2024-Q4. [POP:tournament]

## SQL (verbatim, I6)

```sql
{WIN_RATE_SQL.strip()}
```

## Tier-level win rates (overlap window)

{df_tier.to_markdown(index=False)}

## Verdict: {verdict}

Max tier-to-tier win-rate diff = {max_diff:.4f}.

## M7 note

All Phase 06 rows tagged [POP:tournament]: sc2egset is tournament-scraped;
between-player variance reflects competitive player population, not general playerbase.
See INVARIANTS §5 for scope documentation.
"""

out_md = artifact_dir / "tournament_era_sc2egset.md"
out_md.write_text(md_content)
print(f"Saved: {out_md}")

# %%
db.close()
print("T04 complete.")
