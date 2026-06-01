# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # Step 02_03_01 Layer-2 ADJUDICATION — temporal feature grid decision record (sc2egset)
#
# **Hypothesis:** The adjudicator module
# (`adjudicate_temporal_feature_grid.adjudicate_temporal_feature_grid`) invokes
# V1 + V3 preflights in order; both return PASS against current master state;
# the adjudicator emits a 16-row x 16-col decision CSV and a 14-section
# decision MD to
# `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/`.
#
# **Falsifier:** Any of the following => adjudicator returns a HALT status
# and emits NO artifacts:
#   - H0 base path precondition fails (non-absolute or missing repo_root).
#   - H1 V1 preflight FAIL (parent artifact provenance broken).
#   - H2 V3 preflight FAIL (temporal-discipline schema check broken).
#   - H3 SHA capture fails for any of the 7 pin files.
#   - H4 tracker eligibility CSV unreadable or empty.
#   - H5 numeric-winner self-guard trips on a Q1/Q2/Q3 row.
#   - H6 vocabulary self-guard trips on any decision cell.
#   - H7a forbidden output parent dir already exists (paradox guard).
#   - H7b planning/INDEX.md archive section mentions the Layer-2 branch.
#
# **Sanity check:** This notebook does NOT compute feature values, query DuckDB,
# read data/**, or write Parquet outputs. It executes the adjudicator and
# reports its decision-record output. Q1 (window size), Q2 (decay half-life),
# Q3 (cold-start k-threshold) decisions are recorded as
# `DEFER_TO_MATERIALIZATION` (no concrete numerical winners pinned per
# Invariant I7).
#
# **Cross-spec citations (verbatim):**
#   - CROSS-02-02 = source of candidate family inventory;
#     CROSS-02-03 = source of post-selection audit predicate.
#     These are distinct roles.
#   - Invariant I3: `history_time < T` strictly (not `<=`).
#
# **Out of scope:** No feature materialization. No ROADMAP / STEP_STATUS /
# PIPELINE_SECTION_STATUS / PHASE_STATUS / research_log mutation. No Phase 03.
# No baseline modeling. No empirical second-game-target transferability claim
# (Q8 SYNTACTIC_ONLY).

# %%
import subprocess  # noqa: PLC0415
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_temporal_feature_grid import (
    OUTPUT_CSV_FILENAME,
    OUTPUT_DIR_RELPATH,
    OUTPUT_MD_FILENAME,
    STATUS_PASS,
    adjudicate_temporal_feature_grid,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_discipline import (
    validate_temporal_discipline,
)
from rts_predict.games.sc2.datasets.sc2egset.validate_temporal_feature_grid import (
    validate_predecessor_artifact_provenance,
)

# %%
# Resolve repo root via git (jupytext notebooks have no __file__).
_git_root_bytes = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
repo_root = Path(_git_root_bytes.decode().strip())
print(f"repo_root: {repo_root}")
print(f"output dir (relpath): {OUTPUT_DIR_RELPATH}")

# %%
# Invoke V1 preflight independently first (for transparency in the notebook).
v1 = validate_predecessor_artifact_provenance(repo_root=repo_root)
print(f"V1 preflight: V1 PASS = {v1.passed}")
print(f"V1 halting falsifier: {v1.halting_falsifier}")

# %%
# Invoke V3 preflight independently (for transparency).
v3 = validate_temporal_discipline(repo_root=repo_root)
print(f"V3 preflight: V3 PASS = {v3.passed}")
print(f"V3 halting falsifier: {v3.halting_falsifier}")

# %%
# Invoke the adjudicator. V1 + V3 preflights run again inside the adjudicator
# per the binding sequence (H0 -> H1 -> H2 -> H3 -> H4 -> H5 -> H6 -> H7a ->
# H7b -> H_FINAL).
result = adjudicate_temporal_feature_grid(repo_root=repo_root)

# %%
print(f"adjudicator status: {result.status}")
print(f"halting step: {result.halting_step}")
print(f"v1_preflight cell: {result.v1_preflight}")
print(f"v3_preflight cell: {result.v3_preflight}")
print(f"rows written: {result.rows_written}")
print(f"csv path: {result.csv_path}")
print(f"md path: {result.md_path}")

# %%
# Assert PASS contract. If this assertion fails, the adjudicator has returned a
# HALT status and the emitted artifact paths are None.
assert result.status == STATUS_PASS, (
    f"Adjudicator returned non-PASS status: {result.status} "
    f"(halting_step={result.halting_step})"
)
assert result.v1_preflight == "PASS"
assert result.v3_preflight == "PASS"
assert result.rows_written == 16

# %%
# Read back the decision CSV and print a compact summary.
import csv  # noqa: PLC0415, E402

assert result.csv_path is not None
with result.csv_path.open() as fh:
    reader = csv.DictReader(fh)
    rows = list(reader)

print(f"decision CSV row count: {len(rows)}")
print(f"decision CSV column count: {len(rows[0].keys())}")
print("first row family_kind / decision:")
print(f"  {rows[0]['family_kind']} -> {rows[0]['decision']}")
print("Q4 row family_kind values (verbatim tokens):")
q_sentinels = {
    "temporal_window_size_grid",
    "decay_half_life_grid",
    "cold_start_k_threshold_grid",
    "in_game_snapshot_features",
    "cross_spec_role_separation",
    "v1_v3_preflight_gate",
    "q8_aoe2_transferability",
}
for r in rows:
    if r["family_kind"] not in q_sentinels:
        print(f"  {r['family_kind']} -> {r['decision']}")

# %%
# Read back the decision MD; print section headings only.
assert result.md_path is not None
md_text = result.md_path.read_text()
headings = [ln for ln in md_text.splitlines() if ln.startswith("## ")]
print(f"decision MD H2 section count: {len(headings)}")
for h in headings:
    print(f"  {h}")

# %%
# Confirm the artifact filenames match the planned constants.
assert result.csv_path.name == OUTPUT_CSV_FILENAME
assert result.md_path.name == OUTPUT_MD_FILENAME
print("Adjudicator artifact emission verified.")

# %% [markdown]
# **End of adjudication notebook.** Decision CSV + decision MD emitted to
# `reports/artifacts/02_feature_engineering/03_temporal_features/02_03_01/`.
# No feature materialization. No status YAML / research_log / ROADMAP edit.
# Q1, Q2, Q3 concrete numerical winner selection deferred to a future
# materialization PR (Invariant I7).
