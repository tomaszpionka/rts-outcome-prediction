# aoe2companion -- Dataset Reports Provenance

Permanent provenance record for the aoe2companion dataset. This file is
independent of the phase system and is not archived when phases are reset.

---

# -- Section A: Identity -------------------------------------------------------

game: aoe2
dataset: aoe2companion
reports_dir: src/rts_predict/games/aoe2/datasets/aoe2companion/reports/

# -- Section B: Acquisition provenance -----------------------------------------
# Source: acquisition script execution (pre-Phase 01)

acquisition:
  date: "2026-04-06"
  script: "poetry run aoe2 download aoe2companion"
  branch: "feat/aoe2-phase0-acquisition"
  source: "aoe2companion API (CDN-hosted parquet and CSV files)"
  source_url: "https://www.aoe2companion.com/more/api"
  method: cdn_download

# Download results (from acquisition script logs):
# - First run: 17 failures (3 stale manifest size, 11 truncated, 3 broken pipe)
# - Retry run: all 17 resolved; 0 failures final

# -- Section C: File inventory summary -----------------------------------------
# Source: Step 01_01_01 artifact
# Invariant #9: MUST NOT contain interpretive labels. Report file counts,
# sizes, extensions, and filename patterns only.

file_inventory:
  total_files:    4153
  total_size_mb:  9387.80
  subdirectories: 4
  artifact_ref:   "src/rts_predict/games/aoe2/datasets/aoe2companion/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"

# -- Section D: Known issues ----------------------------------------------------
# Source: acquisition script logs or 01_01_01 artifact
# Report filesystem-level facts only.

known_issues: []

# -- Section E: Reconciliation --------------------------------------------------
# Source: acquisition script verification

reconciliation:
  strength: DEGRADED
  reason: "manifest lacks per-file row counts; limited to file-count match"

# -- Section F: Provenance rule -------------------------------------------------

provenance_rule: >
  Raw data is immutable. The API download will not be repeated.
