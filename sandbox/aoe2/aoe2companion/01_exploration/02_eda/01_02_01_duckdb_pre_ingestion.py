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
# # Step 01_02_01 -- DuckDB Pre-Ingestion: aoe2companion
#
# **Phase:** 01 -- Data Exploration
# **Pipeline Section:** 01_02 -- EDA
# **Dataset:** aoe2companion
# **Question:** What does the raw data look like before we commit to an
# ingestion strategy? Are there binary column issues, schema evolution,
# type inference traps, or NULL patterns we need to handle?
# **Invariants applied:** #6 (reproducibility), #9 (step scope)
# **Step scope:** query

# %%

import duckdb
import json

from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
from rts_predict.games.aoe2.config import AOE2COMPANION_RAW_DIR
from rts_predict.games.aoe2.datasets.aoe2companion.pre_ingestion import (
    inspect_binary_columns,
    run_smoke_test,
)

logger = setup_notebook_logging()
logger.info("Source: %s", AOE2COMPANION_RAW_DIR)

# %% [markdown]
# ## 1. Pyarrow binary column inspection

# %%
binary_info = inspect_binary_columns(AOE2COMPANION_RAW_DIR)
for subdir, info in binary_info.items():
    print(f"{subdir}: {info['binary_column_count']} binary columns")
    for col in info["binary_columns"]:
        print(f"  {col['name']}: {col['converted_type']}")

# %% [markdown]
# ## 2. Smoke test

# %%
con = duckdb.connect(":memory:")
smoke = run_smoke_test(con, AOE2COMPANION_RAW_DIR)
print(f"Smoke matches: {smoke['matches']['row_count']} rows, {smoke['matches']['column_count']} cols")
print(f"Smoke ratings: {smoke['ratings']['row_count']} rows, {smoke['ratings']['column_count']} cols")

# %% [markdown]
# ## 3. DESCRIBE -- column names, types, nullability

# %%
for table_name in smoke:
    print(f"\n{'='*60}")
    print(f"  DESCRIBE {table_name}")
    print(f"{'='*60}")
    files = smoke[table_name]["files_sampled"]
    full_paths = [str(AOE2COMPANION_RAW_DIR / table_name / f) for f in files]
    file_list = ", ".join(f"'{p}'" for p in full_paths)
    reader = "read_csv_auto" if files[0].endswith(".csv") else "read_parquet"
    opts = "binary_as_string=true, " if reader == "read_parquet" else ""
    con.sql(
        f"DESCRIBE SELECT * FROM {reader}([{file_list}], {opts}filename=true)"
    ).show()

# %% [markdown]
# ## 4. Row preview -- SELECT * LIMIT 10

# %%
for table_name in smoke:
    print(f"\n{'='*60}")
    print(f"  {table_name}: {smoke[table_name]['row_count']} rows, {smoke[table_name]['column_count']} cols")
    print(f"{'='*60}")
    files = smoke[table_name]["files_sampled"]
    full_paths = [str(AOE2COMPANION_RAW_DIR / table_name / f) for f in files]
    file_list = ", ".join(f"'{p}'" for p in full_paths)
    reader = "read_csv_auto" if files[0].endswith(".csv") else "read_parquet"
    opts = "binary_as_string=true, " if reader == "read_parquet" else ""
    con.sql(f"SELECT * FROM {reader}([{file_list}], {opts}filename=true) LIMIT 10").show()

# %% [markdown]
# ## 5. Schema evolution -- NULL counts per file date (matches)

# %%
con.sql("""
    SELECT
        filename.split('match-')[2][:10] AS file_date,
        COUNT(*) AS rows,
        COUNT(server) AS server_nn,
        COUNT(empireWarsMode) AS empireWarsMode_nn,
        COUNT(hideCivs) AS hideCivs_nn,
        COUNT(regicideMode) AS regicideMode_nn,
        COUNT(suddenDeathMode) AS suddenDeathMode_nn,
        COUNT(antiquityMode) AS antiquityMode_nn,
        COUNT(scenario) AS scenario_nn,
        COUNT(password) AS password_nn,
        COUNT(modDataset) AS modDataset_nn,
        COUNT(rating) AS rating_nn,
        COUNT(ratingDiff) AS ratingDiff_nn,
        COUNT(team) AS team_nn
    FROM read_parquet(
        '{glob}',
        binary_as_string=true, filename=true, union_by_name=true
    )
    GROUP BY file_date
    ORDER BY file_date
""".format(glob=str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet"))).show()

# %% [markdown]
# ## 6. Schema evolution -- NULL counts per file date (ratings)

# %%
con.sql("""
    SELECT
        filename.split('rating-')[2][:10] AS file_date,
        COUNT(*) AS rows,
        COUNT(profile_id) AS profile_id_nn,
        COUNT(games) AS games_nn,
        COUNT(rating) AS rating_nn,
        COUNT(date) AS date_nn,
        COUNT(leaderboard_id) AS leaderboard_id_nn,
        COUNT(rating_diff) AS rating_diff_nn,
        COUNT(season) AS season_nn
    FROM read_csv(
        '{glob}',
        filename=true, union_by_name=true
    )
    GROUP BY file_date
    ORDER BY file_date
""".format(glob=str(AOE2COMPANION_RAW_DIR / "ratings" / "*.csv"))).show()

# %% [markdown]
# ## 7. Ingestion readiness checks

# %% [markdown]
# ### 7a. CSV type validation -- can ratings columns actually be parsed as numeric/temporal?

# %%
import pandas as pd

# Stratified sample: early, middle, late
ratings_dir = AOE2COMPANION_RAW_DIR / "ratings"
csv_files = sorted(ratings_dir.glob("*.csv"))
sample_csvs = [csv_files[0], csv_files[len(csv_files) // 2], csv_files[-1]]

for fp in sample_csvs:
    df = pd.read_csv(fp, nrows=500)
    print(f"\n--- {fp.name} ({len(df)} rows) ---")
    for col in df.columns:
        numeric_ok = pd.to_numeric(df[col], errors="coerce").notna().sum()
        print(f"  {col}: {numeric_ok}/{len(df)} parseable as numeric")
    date_ok = pd.to_datetime(df["date"], errors="coerce").notna().sum()
    print(f"  date as datetime: {date_ok}/{len(df)} parseable")

# %% [markdown]
# ### 7b. Singleton tables -- DESCRIBE and preview (leaderboard, profiles)

# %%
con = duckdb.connect(":memory:")

for name, path in [
    ("leaderboard", AOE2COMPANION_RAW_DIR / "leaderboards" / "leaderboard.parquet"),
    ("profiles", AOE2COMPANION_RAW_DIR / "profiles" / "profile.parquet"),
]:
    print(f"\n{'='*60}")
    print(f"  DESCRIBE {name}")
    print(f"{'='*60}")
    con.sql(f"DESCRIBE SELECT * FROM read_parquet('{path}', binary_as_string=true)").show()
    print(f"\n  {name} -- first 5 rows:")
    con.sql(f"SELECT * FROM read_parquet('{path}', binary_as_string=true) LIMIT 5").show()

# %% [markdown]
# ### 7c. Join key (matchId, profileId) and prediction target (won) NULL rates

# %%
matches_glob = str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet")

con.sql("""
    SELECT
        COUNT(*) AS total,
        COUNT(matchId) AS matchId_nn,
        COUNT(*) - COUNT(matchId) AS matchId_null,
        COUNT(profileId) AS profileId_nn,
        COUNT(*) - COUNT(profileId) AS profileId_null,
        COUNT(won) AS won_nn,
        COUNT(*) - COUNT(won) AS won_null,
        ROUND(100.0 * (COUNT(*) - COUNT(won)) / COUNT(*), 2) AS won_null_pct
    FROM read_parquet('{glob}', binary_as_string=true, union_by_name=true)
""".format(glob=matches_glob)).show()

# %% [markdown]
# ### 7d. matchId uniqueness -- is each row a player-in-match?

# %%
con.sql("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT matchId) AS distinct_matches,
        ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT matchId), 2) AS avg_rows_per_match
    FROM read_parquet('{glob}', binary_as_string=true, union_by_name=true)
""".format(glob=matches_glob)).show()

# %% [markdown]
# ### 7e. Ratings -- full corpus type check (does read_csv_auto fail on all files?)

# %%
ratings_glob = str(AOE2COMPANION_RAW_DIR / "ratings" / "*.csv")

print("read_csv_auto DESCRIBE on full corpus:")
try:
    con.sql("""
        DESCRIBE SELECT * FROM read_csv_auto('{glob}', filename=true)
    """.format(glob=ratings_glob)).show()
    print("read_csv_auto: SUCCEEDED on full corpus")
except Exception as e:
    print(f"read_csv_auto: FAILED -- {e}")

print("\nread_csv with explicit types DESCRIBE:")
con.sql("""
    DESCRIBE SELECT * FROM read_csv(
        '{glob}', filename=true, header=true,
        types={{'profile_id':'BIGINT','games':'BIGINT','rating':'BIGINT',
               'date':'TIMESTAMP','leaderboard_id':'BIGINT',
               'rating_diff':'BIGINT','season':'BIGINT'}}
    )
""".format(glob=ratings_glob)).show()

# %% [markdown]
# ## 8. Won column: root-cause investigation
#
# The prediction target `won` has 12.99M NULLs (4.69%). This section
# diagnoses whether these NULLs originate from Parquet schema heterogeneity
# (DuckDB type promotion under `union_by_name=true`) or from genuine NULL
# values in the source files.
#
# Two hypotheses:
# - **H1 (schema evolution):** `won` was stored as different Parquet types
#   across files (e.g., INT64 in early files, BOOLEAN in later files).
#   DuckDB type promotion silently converts non-boolean values to NULL.
# - **H2 (genuine NULLs):** Source files contain NULL `won` values
#   independent of type promotion.

# %% [markdown]
# ### 8a. Q1 — Per-file won Parquet schema type

# %%
con8 = duckdb.connect(":memory:")
matches_glob = str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet")

q1_result = con8.sql("""
    SELECT
        type AS parquet_type,
        COUNT(*) AS file_count,
        LIST(file_name ORDER BY file_name)[:3] AS example_files
    FROM parquet_schema('{glob}')
    WHERE name = 'won'
    GROUP BY type
    ORDER BY file_count DESC
""".format(glob=matches_glob))
q1_result.show()
q1_df = q1_result.fetchdf()
print(f"\nDistinct won types across {q1_df['file_count'].sum()} files: "
      f"{len(q1_df)} type(s)")

# %% [markdown]
# ### 8b. Q2 — Per-type-group won value census (no type promotion)

# %%
# Get file groups by won type from Q1
q2_groups = con8.sql("""
    SELECT
        type AS parquet_type,
        LIST(file_name ORDER BY file_name) AS files
    FROM parquet_schema('{glob}')
    WHERE name = 'won'
    GROUP BY type
""".format(glob=matches_glob)).fetchall()

for parquet_type, files in q2_groups:
    # Read all files in the type group — no sampling cap.
    # Each file is read without union_by_name so no type promotion occurs;
    # the GROUP BY aggregation is lightweight regardless of file count.
    file_list = ", ".join(f"'{f}'" for f in files)
    print(f"\n{'='*60}")
    print(f"  won type: {parquet_type} — {len(files)} files")
    print(f"{'='*60}")
    # Read WITHOUT union_by_name to avoid type promotion
    con8.sql("""
        SELECT
            typeof(won) AS runtime_type,
            won::VARCHAR AS won_value,
            COUNT(*) AS row_count
        FROM read_parquet(
            [{file_list}],
            binary_as_string=true
        )
        GROUP BY runtime_type, won_value
        ORDER BY row_count DESC
    """.format(file_list=file_list)).show()

# %% [markdown]
# ### 8c. Q3 — Type promotion NULL injection test

# %%
# If Q1 found multiple types, test promotion on a mixed sample
if len(q1_df) > 1:
    # Pick up to 3 files from each type group
    mixed_files = []
    for parquet_type, files in q2_groups:
        mixed_files.extend(files[:3])
    mixed_file_list = ", ".join(f"'{f}'" for f in mixed_files)

    print("=== WITHOUT union_by_name (no promotion) ===")
    for f in mixed_files:
        result = con8.sql("""
            SELECT
                '{fname}' AS file,
                typeof(won) AS runtime_type,
                COUNT(*) AS total,
                COUNT(won) AS won_nn,
                COUNT(*) - COUNT(won) AS won_null
            FROM read_parquet('{fpath}', binary_as_string=true)
        """.format(fname=f.split('/')[-1], fpath=f))
        result.show()

    print("\n=== WITH union_by_name (promotion active) ===")
    con8.sql("""
        SELECT
            filename.split('match-')[2][:10] AS file_date,
            typeof(won) AS promoted_type,
            COUNT(*) AS total,
            COUNT(won) AS won_nn,
            COUNT(*) - COUNT(won) AS won_null
        FROM read_parquet(
            [{file_list}],
            binary_as_string=true, filename=true, union_by_name=true
        )
        GROUP BY file_date, promoted_type
        ORDER BY file_date
    """.format(file_list=mixed_file_list)).show()
else:
    print("Q1 found only one won type — type promotion is not the cause.")
    print("Skipping Q3 (no mixed-type promotion to test).")

# %% [markdown]
# ### 8d. Q4 — Per-file won NULL distribution

# %%
q4_result = con8.sql("""
    SELECT
        filename.split('match-')[2][:10] AS file_date,
        COUNT(*) AS total_rows,
        COUNT(won) AS won_nn,
        COUNT(*) - COUNT(won) AS won_null,
        ROUND(100.0 * (COUNT(*) - COUNT(won)) / COUNT(*), 2) AS won_null_pct
    FROM read_parquet(
        '{glob}',
        binary_as_string=true, filename=true, union_by_name=true
    )
    GROUP BY file_date
    HAVING won_null > 0
    ORDER BY file_date
""".format(glob=matches_glob))
q4_result.show(max_rows=50)
q4_df = q4_result.fetchdf()
total_files = int(q1_df['file_count'].sum())
print(f"\nFiles with won NULLs: {len(q4_df)} out of {total_files}")
print(f"Files with zero NULLs: {total_files - len(q4_df)}")
print(f"Total NULL rows across all files: {q4_df['won_null'].sum():,}")
if len(q4_df) > 0:
    print(f"Date range of affected files: {q4_df['file_date'].min()} to "
          f"{q4_df['file_date'].max()}")

# %% [markdown]
# ### 8e. Root-cause verdict

# %%
type_count = len(q1_df)
types_found = q1_df['parquet_type'].tolist()
type_file_counts = dict(zip(q1_df['parquet_type'], q1_df['file_count'].astype(int)))
total_files = int(q1_df['file_count'].sum())
files_with_nulls = len(q4_df)
total_nulls = int(q4_df['won_null'].sum()) if len(q4_df) > 0 else 0

# H1: schema heterogeneity (type promotion)
verdict_parts = []
if type_count > 1:
    verdict_parts.append(
        f"H1 SUPPORTED: won column has {type_count} distinct Parquet types "
        f"across files: {types_found}. Type promotion under union_by_name "
        f"may inject NULLs."
    )
else:
    verdict_parts.append(
        f"H1 REJECTED: won column has a single Parquet type ({types_found[0]}) "
        f"across all files. Type promotion is not the cause of NULLs."
    )

# H2: genuine NULLs in source files
# Q2 census (won_value=None in native type) confirms genuine NULLs exist.
# If H1 is rejected and NULLs are present, H2 is the only explanation.
if total_nulls > 0 and type_count == 1:
    verdict_parts.append(
        f"H2 SUPPORTED: {total_nulls:,} genuine NULL won values exist in source "
        f"files (not caused by type promotion). Affected files: {files_with_nulls} "
        f"of {total_files}."
    )
elif total_nulls > 0:
    verdict_parts.append(
        f"H2 PARTIALLY SUPPORTED: NULLs present; disentangle H1/H2 attribution "
        f"by comparing Q2 native-NULL counts vs Q4 post-promotion-NULL counts."
    )
else:
    verdict_parts.append("H2 REJECTED: no NULL won values found in any file.")

verdict_parts.append(
    f"Files with won NULLs: {files_with_nulls} of {total_files}. "
    f"Total NULLs: {total_nulls:,}."
)

won_root_cause = {
    "q1_parquet_types": type_file_counts,
    "q4_files_with_nulls": files_with_nulls,
    "q4_files_without_nulls": total_files - files_with_nulls,
    "q4_total_nulls": total_nulls,
    "q4_date_range": (
        [q4_df['file_date'].min(), q4_df['file_date'].max()]
        if len(q4_df) > 0 else []
    ),
    "verdict": verdict_parts,
}

for line in verdict_parts:
    print(line)

# %%
con8.close()

# %% [markdown]
# ## 9. Findings and ingestion strategy recommendation
#
# Summarize all findings from sections 1-7 here after execution.
# Key decisions to record:
#
# - **Binary columns:** binary_as_string=true confirmed? (based on section 1)
# - **Schema evolution:** which columns appear/disappear over time? (based on section 5)
# - **CSV types:** explicit types validated? (based on 7a, 7e)
# - **won NULLs:** acceptable rate? (based on 7c)
# - **Data structure:** player-in-match rows confirmed? (based on 7d)
# - **Proposed DDL** for matches_raw, ratings_raw, leaderboards_raw, profiles_raw

# %% [markdown]
# ## 10. Write artifact

# %%
artifacts_dir = (
    get_reports_dir("aoe2", "aoe2companion")
    / "artifacts" / "01_exploration" / "02_eda"
)
artifacts_dir.mkdir(parents=True, exist_ok=True)

matches_glob = str(AOE2COMPANION_RAW_DIR / "matches" / "*.parquet")
null_rates_df = con.sql("""
    SELECT
        COUNT(*) AS total,
        COUNT(matchId) AS matchId_nn,
        COUNT(profileId) AS profileId_nn,
        COUNT(won) AS won_nn,
        ROUND(100.0 * (COUNT(*) - COUNT(won)) / COUNT(*), 2) AS won_null_pct
    FROM read_parquet('{glob}', binary_as_string=true, union_by_name=true)
""".format(glob=matches_glob)).fetchdf()

uniqueness_df = con.sql("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT matchId) AS distinct_matches,
        ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT matchId), 2) AS avg_rows_per_match
    FROM read_parquet('{glob}', binary_as_string=true, union_by_name=true)
""".format(glob=matches_glob)).fetchdf()

artifact_data = {
    "step": "01_02_01",
    "dataset": "aoe2companion",
    "binary_column_inspection": binary_info,
    "smoke_test": {
        "matches": {
            "row_count": smoke["matches"]["row_count"],
            "column_count": smoke["matches"]["column_count"],
        },
        "ratings": {
            "row_count": smoke["ratings"]["row_count"],
            "column_count": smoke["ratings"]["column_count"],
        },
    },
    "matches_null_rates": null_rates_df.to_dict(orient="records")[0],
    "match_id_uniqueness": uniqueness_df.to_dict(orient="records")[0],
}
artifact_data["won_null_root_cause"] = won_root_cause

artifact_path = artifacts_dir / "01_02_01_duckdb_pre_ingestion.json"
artifact_path.write_text(json.dumps(artifact_data, indent=2, default=str))
logger.info("Artifact written: %s", artifact_path)

# %%
null_row = null_rates_df.iloc[0]
uniq_row = uniqueness_df.iloc[0]

md_lines = [
    "# Step 01_02_01 -- DuckDB Pre-Ingestion: aoe2companion\n",
    "",
    "## Binary column inspection\n",
    "",
]
for subdir, info in binary_info.items():
    md_lines.append(f"- `{subdir}`: {info['binary_column_count']} binary columns")
md_lines.extend([
    "",
    "## Smoke test\n",
    "",
    f"- matches: {smoke['matches']['row_count']:,} rows, {smoke['matches']['column_count']} cols",
    f"- ratings: {smoke['ratings']['row_count']:,} rows, {smoke['ratings']['column_count']} cols",
    "",
    "## matches NULL rates\n",
    "",
    f"- Total rows: {int(null_row['total']):,}",
    f"- won NULLs: {int(null_row['total']) - int(null_row['won_nn']):,}"
    f" ({float(null_row['won_null_pct']):.2f}%)",
    f"- matchId NULLs: {int(null_row['total']) - int(null_row['matchId_nn']):,}",
    "",
    "## matchId uniqueness\n",
    "",
    f"- Total rows: {int(uniq_row['total_rows']):,}",
    f"- Distinct matchIds: {int(uniq_row['distinct_matches']):,}",
    f"- Avg rows/match: {float(uniq_row['avg_rows_per_match']):.2f}"
    " (expected ~2 for player-in-match)",
    "",
    "## Won NULL root cause\n",
    f"- H1 (schema heterogeneity): {'SUPPORTED' if type_count > 1 else 'REJECTED'}",
    f"- H2 (genuine NULLs): {'SUPPORTED' if total_nulls > 0 and type_count == 1 else 'see verdict'}",
    f"- Files with NULLs: {files_with_nulls} of {total_files}",
    f"- Total NULLs: {total_nulls:,}",
])

md_path = artifacts_dir / "01_02_01_duckdb_pre_ingestion.md"
md_path.write_text("\n".join(md_lines))
logger.info("Report written: %s", md_path)

# %%
con.close()
