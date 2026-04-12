# sc2egset -- Dataset Reports Provenance

Permanent provenance record for the sc2egset dataset. This file is
independent of the phase system and is not archived when phases are reset.

---

# -- Section A: Identity -------------------------------------------------------

game: sc2
dataset: sc2egset
reports_dir: src/rts_predict/games/sc2/datasets/sc2egset/reports/

# -- Section B: Acquisition provenance -----------------------------------------
# Source: acquisition script execution (pre-Phase 01)

acquisition:
  date: "2025-12-05"
  script: "manual download from Zenodo"
  branch: "feat/sc2egset-acquisition"
  source: "SC2EGSet -- StarCraft II Esport Replay and Game-state Dataset"
  source_url: "https://zenodo.org/records/17829625"
  method: manual_download

# -- Section C: File inventory summary -----------------------------------------
# Source: Step 01_01_01 artifact
# Invariant #9: MUST NOT contain interpretive labels. Report file counts,
# sizes, extensions, and filename patterns only.

file_inventory:
  total_files:    22821
  total_size_mb:  214060.62
  subdirectories: 70
  artifact_ref:   "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/01_acquisition/01_01_01_file_inventory.json"

# -- Section D: Known issues ----------------------------------------------------
# Source: acquisition script logs or 01_01_01 artifact
# Report filesystem-level facts only.

known_issues: []

# -- Section E: Reconciliation --------------------------------------------------
# Source: acquisition script verification

reconciliation:
  strength: FULL
  reason: "Zenodo v2.1.0 release; manual download; no acquisition script used"

# -- Section F: Provenance rule -------------------------------------------------

provenance_rule: >
  Raw data is immutable. The acquisition will not be repeated.
