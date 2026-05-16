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
# # Step 02_01_01 — Feature-family registry skeleton: sc2egset
#
# **Phase:** 02 — Feature Engineering
# **Pipeline Section:** 02_01 — Pre-Game vs In-Game Boundary
# **Dataset:** sc2egset
# **Question:** Which Phase 02 candidate feature families exist for sc2egset,
# declared per CROSS-02-02-v1.0.1 §6, and what is each family's
# CROSS-02-03-v1.0.1 D1–D15 design-time disposition (allowed /
# allowed_with_caveat / blocked_until_validation /
# sanity_gate_not_model_input)?
# **Invariants applied:** I3 (temporal discipline / strict `<`),
# I5 (symmetric per-player construction), I6 (reproducibility — code-with-result),
# I7 (no magic numbers), I8 (cross-game comparability of feature categories),
# I9 (artifact-grounded conclusions)
# **ROADMAP reference:** `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md` Step 02_01_01
# **Commit:** 4c243158
#
# This notebook is a SCAFFOLD plus single-validation-module orchestration only.
# It implements lineage sequence step 2 of the data-analysis lineage protocol
# (`.claude/rules/data-analysis-lineage.md` §"Non-batching rule for empirical
# work"): scaffold + one validation module. Steps 3–9 (artifact generation,
# research_log update, STEP_STATUS update, manifest update) are explicitly
# deferred to a subsequent PR after reviewed execution of all validation
# modules. The Commit field above is a snapshot of the scaffold-creation HEAD;
# it does NOT auto-update on re-runs.

# %%
import csv
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
from rts_predict.games.sc2.datasets.sc2egset.validate_registry_skeleton import (
    REQUIRED_COLUMNS,
    validate_registry_skeleton,
)

logger = setup_notebook_logging()

# %%
# Paths. The tracker eligibility CSV is the binding evidence source for
# in_game_snapshot eligibility (CROSS-02-03-v1.0.1 §5; data-analysis-lineage.md
# §"SC2 tracker-event discipline"). No ARTIFACTS_DIR is created in this
# scaffold-only PR — deviation from notebook_template.yaml `cell_03_paths`
# (which mandates `mkdir`) is justified by the explicit "no report artifacts"
# scope of lineage sequence step 2.
TRACKER_CSV: Path = (
    get_reports_dir("sc2", "sc2egset")
    / "artifacts"
    / "01_exploration"
    / "03_profiling"
    / "tracker_events_feature_eligibility.csv"
)

logger.info("Tracker eligibility CSV: %s", TRACKER_CSV)
logger.info("Tracker CSV exists: %s", TRACKER_CSV.exists())

# %% [markdown]
# ## Hypothesis, falsifiers, sanity checks, and stop conditions
#
# Per `.claude/rules/data-analysis-lineage.md` §"Required structure for every
# empirical analysis", every empirical analysis must declare these fields
# before execution. This block is the contract this scaffold notebook executes
# against; the `validate_registry_skeleton` call below is the single
# falsifier check this PR delivers.
#
# ### Assumption being tested
# A 26-row in-memory registry skeleton — composed of 5 `pre_game` +
# 6 `history_enriched_pre_game` + 4 `in_game_snapshot` `eligible_for_phase02_now`
# model-input + 7 `eligible_with_caveat` + 1 `sanity_gate_not_model_input` +
# 3 `blocked_until_additional_validation` rows — is **structurally consistent**
# with the four binding specs (CROSS-02-00-v3.0.1, CROSS-02-01-v1.0.1,
# CROSS-02-02-v1.0.1, CROSS-02-03-v1.0.1) and with the upstream tracker
# eligibility evidence at `tracker_events_feature_eligibility.csv`.
#
# ### Measurement claim
# `validate_registry_skeleton(skeleton, tracker_csv_path)` runs V-1 through
# V-7 structural assertions and raises `AssertionError` with a descriptive message on any
# violation. ALL PASS means the skeleton is structurally admissible as a Phase
# 02 candidate registry — it does NOT mean any feature has been computed,
# materialized, or admitted as a model input. This is a registry-level audit,
# not a feature-engineering result.
#
# ### Sanity check
# The tracker CSV row counts by `status_in_game_snapshot` must be exactly
# 5 / 7 / 3 (`eligible_for_phase02_now` / `eligible_with_caveat` /
# `blocked_until_additional_validation`); total = 15. V-2 enforces this
# directly; the manual count cell below also surfaces it for human review.
# A drift of ±1 in any bucket halts validation immediately.
#
# ### Falsifier
# Any of the seven structural checks fails — V-1 (schema integrity + strict
# feature_family_id second-segment alignment with prediction_setting), V-2
# (tracker split counts), V-3 (blocked families remain blocked), V-4
# (`slot_identity_consistency` is `sanity_gate_not_model_input` while CSV
# remains `eligible_for_phase02_now`), V-5 (zero tracker-derived rows in
# `pre_game`/`history_enriched_pre_game`), V-6 (history rows use strict `<`
# with sc2egset `details_timeUTC` provenance, not `<=`, and reject the
# cross-dataset alias `started_at`), V-7 (validates cold_start_handling
# vocabulary/sentinel discipline: G-CS-1..G-CS-6 for active/candidate rows,
# literal "blocked" only under the blocked_or_deferred +
# blocked_until_additional_validation conjunction; numeric tokens forbidden).
#
# ### Expected artifact or report
# **None.** This scaffold PR explicitly produces NO report artifacts. Planned
# CSV / MD registry artifacts under
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
# are deferred to a subsequent artifacts PR after reviewed execution of all
# additional validation modules (D2, D3, D6, D8, D9, D10, D12, D15).
#
# ### Lineage source
# - CROSS-02-00-v3.0.1 §3.3 (strict `<` for history features; `<=` for
#   in-game snapshot)
# - CROSS-02-01-v1.0.1 (leakage-mode taxonomy)
# - CROSS-02-02-v1.0.1 §6 (sc2egset feature families) and §9 (cold-start
#   gates G-CS-1..G-CS-6 for active and candidate rows; the literal "blocked" sentinel for blocked_or_deferred rows where status == "blocked_until_additional_validation" — no magic numbers per Invariant I7)
# - CROSS-02-03-v1.0.1 §3 (13-column audit object) and §5.1 (sc2egset
#   `temporal_anchor = details_timeUTC`)
# - `tracker_events_feature_eligibility.csv` (upstream evidence; not modified
#   here)
# - PR #208 Phase 02 guidance (`slot_identity_consistency` reclassified from
#   tracker-CSV `eligible_for_phase02_now` to registry-level
#   `sanity_gate_not_model_input`).
#
# ### Downstream decision
# If V-1..V-9 ALL PASS, the skeleton structure is admissible as a candidate
# registry; subsequent PRs may add validation modules for D2, D3, D6 (full),
# D8, D9, D10 (focal/opponent symmetry per CROSS-02-03-v1.0.1 §4.1), D12,
# D15 and ultimately materialize the registry artifact. If ANY
# check fails, halt before any artifact generation; do not patch outputs;
# report the failing V-N and offending row(s) to the parent session.
#
# ### Temporal-leakage discipline (Invariant I3)
# - Tracker-derived rows (any row whose `source_table_or_event_family`
#   references a tracker event family in
#   `tracker_events_feature_eligibility.csv`) MUST NEVER declare
#   `prediction_setting = pre_game` or `history_enriched_pre_game`. Tracker
#   events are observed only during a match and cannot be used as prior-time
#   features. Enforced by V-5.
# - `history_enriched_pre_game` rows MUST use strict `<` (not `<=`) against
#   the sc2egset-specific `details_timeUTC` provenance anchor. The
#   cross-dataset alias `started_at` is REJECTED for sc2egset history rows.
#   Enforced by V-6.
#
# ### `slot_identity_consistency` registry classification
# `slot_identity_consistency` is a **registry-level
# `sanity_gate_not_model_input`** classification, NOT a model input. The
# upstream tracker CSV legitimately marks it `eligible_for_phase02_now`
# (the row is structurally clean and could be queried at Phase 02 time);
# the registry independently reclassifies it because the CSV
# `notes_for_phase02` field labels it a "feature-engineering sanity gate; not
# a model input". V-4 enforces both ends: skeleton row carries
# `sanity_gate_not_model_input`, and the CSV row remains
# `eligible_for_phase02_now` (CSV must NOT be modified by this PR).
#
# ### Stop conditions
# Halt before declaring this Step complete or proceeding to artifact
# generation if:
# - Any V-1..V-9 assertion raises `AssertionError`.
# - The tracker CSV cannot be read or its row counts have drifted from
#   5 / 7 / 3.
# - A tracker family appears with `prediction_setting in {pre_game,
#   history_enriched_pre_game}` (Invariant I3 violation).
# - A `history_enriched_pre_game` row uses `<=` instead of `<`, or `started_at`
#   instead of `details_timeUTC`, or references a post-outcome token in
#   `allowed_cutoff_rule` (Invariant I3 violation).

# %%
# Read tracker CSV and report counts by status_in_game_snapshot. The
# validation module also reads this CSV; this cell exposes the counts
# explicitly for human review per data-analysis-lineage.md §"Notebook
# discipline" (notebook execution reports must summarize what was measured).
with TRACKER_CSV.open(newline="", encoding="utf-8") as fh:
    tracker_rows: list[dict[str, str]] = list(csv.DictReader(fh))

status_counts: dict[str, int] = {}
for row in tracker_rows:
    key = row["status_in_game_snapshot"]
    status_counts[key] = status_counts.get(key, 0) + 1

print(f"Tracker CSV total rows: {len(tracker_rows)}")
print(f"Counts by status_in_game_snapshot: {status_counts}")

# %% [markdown]
# ## Registry skeleton declaration narrative
#
# The 26-row skeleton breaks down as follows. Each row's `feature_family_id`
# is dataset-prefixed: `sc2egset.<prediction_setting>.<family>` (OQ1
# resolution). The skeleton is in-memory only — no CSV / MD artifact is
# produced by this scaffold PR.
#
# ### `pre_game` (5 rows, CROSS-02-02-v1.0.1 §6.1)
# 1. `sc2egset.pre_game.focal_race_with_opponent_race_pair`
# 2. `sc2egset.pre_game.map_type_encoded`
# 3. `sc2egset.pre_game.patch_version_encoded`
# 4. `sc2egset.pre_game.matchup_encoded`
# 5. `sc2egset.pre_game.is_mmr_missing_flag`
#
# ### `history_enriched_pre_game` (6 rows, CROSS-02-02-v1.0.1 §6.2)
# 1. `sc2egset.history_enriched_pre_game.focal_player_history`
# 2. `sc2egset.history_enriched_pre_game.opponent_player_history`
# 3. `sc2egset.history_enriched_pre_game.matchup_history_aggregate`
# 4. `sc2egset.history_enriched_pre_game.reconstructed_rating`
# 5. `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling`
#    — CONTEXT / sensitivity-gate handling row (`status =
#    allowed_with_caveat`); does NOT hard-code a retention percentage
#    (Invariant I7).
# 6. `sc2egset.history_enriched_pre_game.in_game_history_aggregate`
#
# ### `in_game_snapshot` model-input rows (4 rows, tracker CSV
# `eligible_for_phase02_now` excluding `slot_identity_consistency`)
# 1. `sc2egset.in_game_snapshot.count_units_built_by_cutoff_loop`
# 2. `sc2egset.in_game_snapshot.count_units_killed_by_cutoff_loop`
# 3. `sc2egset.in_game_snapshot.morph_count_by_cutoff_loop`
# 4. `sc2egset.in_game_snapshot.building_construction_count_by_cutoff_loop`
#
# ### `in_game_snapshot` allowed_with_caveat rows (7 rows, tracker CSV
# `eligible_with_caveat`)
# 1. `sc2egset.in_game_snapshot.minerals_collection_rate_history_mean`
# 2. `sc2egset.in_game_snapshot.army_value_at_5min_snapshot`
# 3. `sc2egset.in_game_snapshot.supply_used_at_cutoff_snapshot`
# 4. `sc2egset.in_game_snapshot.food_used_max_history`
# 5. `sc2egset.in_game_snapshot.time_to_first_expansion_loop`
# 6. `sc2egset.in_game_snapshot.count_units_lost_by_cutoff_loop`
# 7. `sc2egset.in_game_snapshot.count_upgrades_by_cutoff_loop`
#
# ### Sanity gate (1 row)
# - `sc2egset.in_game_snapshot.slot_identity_consistency` —
#   `status = sanity_gate_not_model_input`. Registry-level classification per
#   PR #208 guidance; CSV row independently remains `eligible_for_phase02_now`.
#
# ### Blocked rows (3 rows, tracker CSV
# `blocked_until_additional_validation`)
# 1. `sc2egset.blocked_or_deferred.mind_control_event_count`
# 2. `sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot`
# 3. `sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields`
#
# Total: 5 + 6 + 4 + 7 + 1 + 3 = 26.

# %%
# Define column-tuple constants used to build the skeleton row literals
# below. Per the plan §Execution Steps T03 cell 7, each row carries exactly
# the 13 columns enumerated in
# `validate_registry_skeleton.REQUIRED_COLUMNS`. No `def`, `class`, or
# `lambda` is used anywhere in the notebook; rows are plain dict literals
# expressed via column-tuple keys to keep cells under the 50-line cap.
# Cold-start handling values follow controlled discipline:
# active and candidate rows use only the gate vocabulary G-CS-1..G-CS-6
# (CROSS-02-02-v1.0.1 §9.1); blocked_or_deferred rows whose status is
# "blocked_until_additional_validation" use the literal sentinel "blocked".
# No numeric pseudocount, threshold, smoothing strength, or imputation
# constant appears anywhere (Invariant I7).
_COLS = (
    "feature_family_id",
    "dataset_tag",
    "prediction_setting",
    "source_table_or_event_family",
    "source_grain",
    "model_input_grain",
    "target_grain",
    "temporal_anchor",
    "allowed_cutoff_rule",
    "candidate_leakage_modes",
    "cold_start_handling",
    "status",
    "per_player_construction",
)
_FOCAL_GRAIN = "(focal_match_id, focal_player)"
_FOCAL_CUTOFF_GRAIN = "(focal_match_id, focal_player, cutoff_loop)"
_PRE_GAME_CUTOFF = "snapshot_at_match_start"
_HISTORY_CUTOFF = "history_time < target_time"
_IN_GAME_CUTOFF = "event.loop <= cutoff_loop"

# %%
# pre_game (5 rows) — all use details_timeUTC anchor with snapshot_at_match_start
# cutoff (Invariant I3: pre_game features observe match start state only).
SKELETON_PRE_GAME: list[dict[str, str]] = [
    dict(zip(_COLS, row)) for row in [
        ("sc2egset.pre_game.focal_race_with_opponent_race_pair", "sc2egset",
         "pre_game", "replay_players_raw", "(filename, player_id_worldwide)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _PRE_GAME_CUTOFF,
         "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.pre_game.map_type_encoded", "sc2egset",
         "pre_game", "matches_flat", "(filename)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _PRE_GAME_CUTOFF,
         "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.pre_game.patch_version_encoded", "sc2egset",
         "pre_game", "matches_flat", "(filename)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _PRE_GAME_CUTOFF,
         "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.pre_game.matchup_encoded", "sc2egset",
         "pre_game", "replay_players_raw", "(filename, player_id_worldwide)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _PRE_GAME_CUTOFF,
         "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.pre_game.is_mmr_missing_flag", "sc2egset",
         "pre_game", "replay_players_raw", "(filename, player_id_worldwide)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _PRE_GAME_CUTOFF,
         "none", "G-CS-1", "allowed", "symmetric"),
    ]
]
print(f"pre_game rows: {len(SKELETON_PRE_GAME)}")

# %%
# history_enriched_pre_game (6 rows) — strict '<' cutoff against the
# sc2egset-specific details_timeUTC anchor. cross_region_fragmentation_handling
# is the CONTEXT row; status = allowed_with_caveat. No retention percentage
# is hard-coded (Invariant I7).
SKELETON_HISTORY: list[dict[str, str]] = [
    dict(zip(_COLS, row)) for row in [
        ("sc2egset.history_enriched_pre_game.focal_player_history", "sc2egset",
         "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide)", _FOCAL_GRAIN, _FOCAL_GRAIN,
         "details_timeUTC", _HISTORY_CUTOFF, "rolling_includes_target_game",
         "G-CS-2", "allowed", "symmetric"),
        ("sc2egset.history_enriched_pre_game.opponent_player_history", "sc2egset",
         "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide)", _FOCAL_GRAIN, _FOCAL_GRAIN,
         "details_timeUTC", _HISTORY_CUTOFF, "rolling_includes_target_game",
         "G-CS-2", "allowed", "symmetric"),
        ("sc2egset.history_enriched_pre_game.matchup_history_aggregate", "sc2egset",
         "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide, opponent_player_id_worldwide)",
         _FOCAL_GRAIN, _FOCAL_GRAIN, "details_timeUTC", _HISTORY_CUTOFF,
         "h2h_includes_target_game", "G-CS-3", "allowed", "symmetric"),
        ("sc2egset.history_enriched_pre_game.reconstructed_rating", "sc2egset",
         "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide)", _FOCAL_GRAIN, _FOCAL_GRAIN,
         "details_timeUTC", _HISTORY_CUTOFF, "rating_uses_target_game_outcome",
         "G-CS-4", "allowed", "symmetric"),
        ("sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling",
         "sc2egset", "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide)", _FOCAL_GRAIN, _FOCAL_GRAIN,
         "details_timeUTC", _HISTORY_CUTOFF, "cross_region_history_drop",
         "G-CS-5", "allowed_with_caveat", "symmetric"),
        ("sc2egset.history_enriched_pre_game.in_game_history_aggregate", "sc2egset",
         "history_enriched_pre_game", "matches_flat",
         "(filename, player_id_worldwide)", _FOCAL_GRAIN, _FOCAL_GRAIN,
         "details_timeUTC", _HISTORY_CUTOFF, "rolling_includes_target_game",
         "G-CS-2", "allowed", "symmetric"),
    ]
]
print(f"history_enriched_pre_game rows: {len(SKELETON_HISTORY)}")

# %%
# in_game_snapshot model-input rows — 4 eligible_for_phase02_now (excluding
# slot_identity_consistency which is reclassified to sanity_gate below) + 7
# eligible_with_caveat. All use event.loop anchor with '<= cutoff_loop' cutoff.
SKELETON_IN_GAME_NOW: list[dict[str, str]] = [
    dict(zip(_COLS, row)) for row in [
        ("sc2egset.in_game_snapshot.count_units_built_by_cutoff_loop", "sc2egset",
         "in_game_snapshot", "tracker_events_raw.UnitBorn",
         "(filename, controlPlayerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.in_game_snapshot.count_units_killed_by_cutoff_loop", "sc2egset",
         "in_game_snapshot", "tracker_events_raw.UnitDied",
         "(filename, killerPlayerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.in_game_snapshot.morph_count_by_cutoff_loop", "sc2egset",
         "in_game_snapshot", "tracker_events_raw.UnitTypeChange",
         "(filename, owner_via_unitborn_lineage)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "none", "G-CS-1", "allowed", "symmetric"),
        ("sc2egset.in_game_snapshot.building_construction_count_by_cutoff_loop",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.UnitInit",
         "(filename, controlPlayerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "none", "G-CS-1", "allowed", "symmetric"),
    ]
]
print(f"in_game_snapshot eligible_for_phase02_now rows: {len(SKELETON_IN_GAME_NOW)}")

# %%
# in_game_snapshot eligible_with_caveat rows (7) — each carries a distinct
# candidate_leakage_modes entry derived from the tracker CSV `caveat` /
# `notes_for_phase02` columns (no magic constants, just classification labels
# per Invariant I7).
SKELETON_IN_GAME_CAVEAT: list[dict[str, str]] = [
    dict(zip(_COLS, row)) for row in [
        ("sc2egset.in_game_snapshot.minerals_collection_rate_history_mean",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.PlayerStats",
         "(filename, playerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "snapshot_oscillation",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.army_value_at_5min_snapshot",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.PlayerStats",
         "(filename, playerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "lps_caveat_on_5min",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.supply_used_at_cutoff_snapshot",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.PlayerStats",
         "(filename, playerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "fixed_point_scaling_unconfirmed",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.food_used_max_history",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.PlayerStats",
         "(filename, playerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "fixed_point_scaling_unconfirmed",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.time_to_first_expansion_loop",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.UnitBorn",
         "(filename, controlPlayerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "full_replay_min_loop_blocked",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.count_units_lost_by_cutoff_loop",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.UnitDied",
         "(filename, owner_via_unitborn_lineage)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "lineage_orphan_drop",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
        ("sc2egset.in_game_snapshot.count_upgrades_by_cutoff_loop",
         "sc2egset", "in_game_snapshot", "tracker_events_raw.Upgrade",
         "(filename, playerId)", _FOCAL_CUTOFF_GRAIN, _FOCAL_GRAIN,
         "event.loop", _IN_GAME_CUTOFF, "upgrade_count_field_unconfirmed",
         "G-CS-6", "allowed_with_caveat", "symmetric"),
    ]
]
print(f"in_game_snapshot eligible_with_caveat rows: {len(SKELETON_IN_GAME_CAVEAT)}")

# %%
# Sanity gate (1) and blocked_until_additional_validation (3). The sanity-gate
# row reclassifies the tracker CSV's eligible_for_phase02_now status to
# registry-level sanity_gate_not_model_input per PR #208 guidance — the CSV
# is NOT modified. Blocked rows preserve the tracker CSV blocked status.
SKELETON_GATE_AND_BLOCKED: list[dict[str, str]] = [
    dict(zip(_COLS, row)) for row in [
        ("sc2egset.in_game_snapshot.slot_identity_consistency", "sc2egset",
         "in_game_snapshot", "tracker_events_raw.PlayerSetup",
         "(filename, playerId)", "(filename)", "(filename)", "event.loop",
         _IN_GAME_CUTOFF, "none", "G-CS-1", "sanity_gate_not_model_input",
         "symmetric"),
        ("sc2egset.blocked_or_deferred.mind_control_event_count", "sc2egset",
         "blocked_or_deferred", "tracker_events_raw.UnitOwnerChange",
         "(filename, playerId)", "blocked", "blocked", "event.loop",
         "blocked", "blocked", "blocked",
         "blocked_until_additional_validation", "blocked"),
        ("sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot",
         "sc2egset", "blocked_or_deferred", "tracker_events_raw.UnitPositions",
         "(filename, owner_via_unitborn_lineage)", "blocked", "blocked",
         "event.loop", "blocked", "blocked", "blocked",
         "blocked_until_additional_validation", "blocked"),
        ("sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields",
         "sc2egset", "blocked_or_deferred", "tracker_events_raw.PlayerStats",
         "(filename, playerId)", "blocked", "blocked", "event.loop",
         "blocked", "blocked", "blocked",
         "blocked_until_additional_validation", "blocked"),
    ]
]
print(
    f"sanity_gate + blocked rows: {len(SKELETON_GATE_AND_BLOCKED)}"
)

# %%
SKELETON: list[dict[str, str]] = (
    SKELETON_PRE_GAME
    + SKELETON_HISTORY
    + SKELETON_IN_GAME_NOW
    + SKELETON_IN_GAME_CAVEAT
    + SKELETON_GATE_AND_BLOCKED
)

print(f"SKELETON row count: {len(SKELETON)}")

# %% [markdown]
# ## Validation module (V-1 through V-9)
#
# `validate_registry_skeleton` (in
# `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`)
# implements the V-1..V-9 structural validation surface against the 13-column audit object schema
# defined in CROSS-02-03-v1.0.1 §3:
#
# | Check | What it asserts |
# |-------|-----------------|
# | V-1 | 13-column schema integrity; controlled vocabularies for `prediction_setting` and `status`; non-null unique `feature_family_id` with `sc2egset.` prefix; single-dataset `dataset_tag == "sc2egset"`; no extra columns (no materialized feature values). |
# | V-2 | Tracker CSV row counts by `status_in_game_snapshot`: 5 / 7 / 3 (`eligible_for_phase02_now` / `eligible_with_caveat` / `blocked_until_additional_validation`); total = 15. |
# | V-3 | The three blocked tracker families (`mind_control_event_count`, `army_centroid_at_cutoff_snapshot`, `playerstats_cumulative_economy_fields`) carry `status = blocked_until_additional_validation` in the skeleton. |
# | V-4 | Skeleton row for `slot_identity_consistency` has `status = sanity_gate_not_model_input`; CSV row independently still reads `status_in_game_snapshot = eligible_for_phase02_now` (CSV must NOT be modified). |
# | V-5 | No skeleton row whose `source_table_or_event_family` references a tracker event family declares `prediction_setting in {pre_game, history_enriched_pre_game}` (Invariant I3 / PR #208 Amendment 2). |
# | V-6 | Every `history_enriched_pre_game` row uses strict `<` (not `<=`) and `temporal_anchor = details_timeUTC` (not the cross-dataset alias `started_at`); `allowed_cutoff_rule` does not reference post-outcome tokens (CROSS-02-03-v1.0.1 §5.1; Invariant I3). |
# | V-9 | Every row's `per_player_construction` matches the controlled vocabulary `{"symmetric"}` for model-input and sanity-gate rows, OR equals the sentinel `"blocked"` under the V-7 conjunction (`prediction_setting == "blocked_or_deferred"` AND `status == "blocked_until_additional_validation"`). Invariant I5 / CROSS-02-03-v1.0.1 §4.1 D10 sub-clause 1. D10 sub-clause 2 (aoestats `canonical_slot` p0/p1 projection) is N/A for sc2egset. |
#
# Checks IN scope as of this PR (V-1 base, V-1 strict, V-2..V-7 from PRs
# #212/#213, V-8 source-grain structural well-formedness from PR #214,
# V-9 per_player_construction controlled vocabulary + sentinel from PR #215;
# this PR adds artifact emission, no new validators).
# Checks NOT YET in scope (deferred to subsequent validation modules):
# per-row optimal G-CS gate fit (which gate suits each family
# scientifically), candidate-leakage-mode coverage against CROSS-02-01-v1.0.1,
# and audit
# dimensions D2/D3/D6/D8/D9/D12/D15.

# %%
# Run the single validation module. AssertionError halts execution; the
# notebook does NOT catch or mask exceptions. On success the module returns
# None and the cell prints an explicit ALL PASS banner.
validate_registry_skeleton(SKELETON, tracker_csv_path=TRACKER_CSV)
print("validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emission begins below")

# %% [markdown]
# ## Artifact emission
#
# Anchor: `validated_through=V-9 baseline`. This section writes two artifacts
# under `ARTIFACTS_DIR`: a 26-row × 14-column CSV (13 `REQUIRED_COLUMNS` plus a
# `block` column appended last) and a companion MD whose top section is the
# verbatim coverage-status disclaimer (option B encoding, plain `<` / `>`) from
# `planning/current_plan.md` §"Disclaimer text — verbatim". The disclaimer is
# the source of truth for the artifact's per-dimension coverage claims; this
# cell does not paraphrase it. Provenance fields (`executed_at`, `git_sha`,
# `python_version`) are computed at notebook execution time, not at notebook
# edit time, so the artifact reflects the actual run rather than the source
# commit. The `executed_at` field uses `datetime.now(timezone.utc).date()`
# (timezone-explicit UTC); re-running on the same UTC day yields byte-identical
# artifacts and cross-UTC-day re-runs differ only in `executed_at`. No
# `STEP_STATUS.yaml` / `PHASE_STATUS.yaml` / spec / validator file is touched
# by this cell; closure of Step 02_01_01 is explicitly NOT claimed (see the
# disclaimer's §"Step 02_01_01 closure status — partial" subsection).

# %%
ARTIFACTS_DIR: Path = (
    get_reports_dir("sc2", "sc2egset")
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

_BLOCK_BY_FAMILY: dict[str, str] = {}
for _row in SKELETON_PRE_GAME:
    _BLOCK_BY_FAMILY[_row["feature_family_id"]] = "pre_game"
for _row in SKELETON_HISTORY:
    _BLOCK_BY_FAMILY[_row["feature_family_id"]] = "history_enriched_pre_game"
for _row in SKELETON_IN_GAME_NOW:
    _BLOCK_BY_FAMILY[_row["feature_family_id"]] = "in_game_now"
for _row in SKELETON_IN_GAME_CAVEAT:
    _BLOCK_BY_FAMILY[_row["feature_family_id"]] = "in_game_caveat"
for _row in SKELETON_GATE_AND_BLOCKED:
    _BLOCK_BY_FAMILY[_row["feature_family_id"]] = "gate_and_blocked"

csv_rows: list[dict[str, str]] = [
    dict(row, block=_BLOCK_BY_FAMILY[row["feature_family_id"]]) for row in SKELETON
]
fieldnames: list[str] = list(REQUIRED_COLUMNS) + ["block"]
_csv_path: Path = ARTIFACTS_DIR / "02_01_01_feature_family_registry.csv"
with _csv_path.open("w", newline="", encoding="utf-8") as _fh:
    _writer = csv.DictWriter(_fh, fieldnames=fieldnames, lineterminator="\n")
    _writer.writeheader()
    _writer.writerows(csv_rows)

# %%
# Provenance fields. All values are computed at execution time (not at notebook
# edit time). The `executed_at` field uses timezone-explicit UTC per the plan's
# T01 §Instructions and reviewer-adversarial condition C4 (same-UTC-day
# byte-identicality vs cross-UTC-day metadata-only drift).
_VALIDATED_THROUGH = "V-9"
_CLOSURE_STATUS = "partial"
_MANIFEST_STATUS = "partial_coverage_v9_baseline"
_NON_SUPERSESSION = "CROSS-02-01-v1.0.1 remains mandatory"
_EXECUTED_AT = datetime.now(timezone.utc).date().isoformat()
_GIT_SHA = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"], text=True
).strip()
_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
_POETRY_VERSION = subprocess.check_output(["poetry", "--version"], text=True).strip()
_SEED = "not_applicable_deterministic_export"
_NOTEBOOK_PATH = (
    "sandbox/sc2/sc2egset/02_feature_engineering/"
    "01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py"
)
_VALIDATOR_MODULE = (
    "src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py"
)
_ARTIFACT_CSV_PATH = str(ARTIFACTS_DIR / "02_01_01_feature_family_registry.csv")
_ARTIFACT_MD_PATH = str(ARTIFACTS_DIR / "02_01_01_feature_family_registry.md")
_REGENERATION_COMMAND = (
    "poetry run jupyter nbconvert --to notebook --execute --inplace "
    "--ExecutePreprocessor.timeout=300 "
    "sandbox/sc2/sc2egset/02_feature_engineering/"
    "01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb"
)

# %%
# Verbatim coverage-status disclaimer. Source of truth:
# planning/current_plan.md §"Disclaimer text — verbatim" (option B encoding,
# plain `<` / `>`). DO NOT paraphrase. Any edit must be approved by
# reviewer-adversarial.
_DISCLAIMER_TEXT = """## Coverage status — provisional registry artifact

This registry artifact is emitted at `validated_through = V-9` per
`reports/specs/02_03_temporal_feature_audit_protocol.md` (CROSS-02-03-v1.0.1).
It is **provisional**: not all 15 design-time audit dimensions (D1–D15) of
CROSS-02-03-v1.0.1 §4 are mechanically enforced at the registry-skeleton
layer. Coverage is as follows.

### What V-1..V-9 mechanically enforce on this artifact

The validation module `validate_registry_skeleton()` in
`src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
runs ten checks (V-1 base, V-1 strict, V-2..V-9) on every row of the registry.
Each check is a structural gate; failure on any row halts artifact regeneration.

| V-N | What it asserts | Maps to CROSS-02-03 dimension |
|-----|-----------------|-------------------------------|
| V-1 | Required-column presence (13-column schema) | D1 (admissibility), D15 (lineage readiness) |
| V-1 strict | Controlled vocabulary on `prediction_setting` | D1 |
| V-2..V-5 | SC2 tracker eligibility CSV cross-reference | D13 |
| V-6 | History cutoff is `history_time < target_time` strict; post-game-token list excluded | D5 (history side), D6 (target-game exclusion, history side), D7 |
| V-7 | Cold-start vocabulary + status-gated sentinel; no magic numbers | D11 |
| V-8 | Source-grain structural well-formedness + provenance-key consistency | (orthogonal to D8 — see below) |
| V-9 | `per_player_construction` controlled vocabulary; status-gated `"blocked"` sentinel; admits `"symmetric"` only on model-input rows | D10 sub-clause 1 (Invariant I5 symmetry) |

V-9 admits exactly one non-blocked token (`"symmetric"`). It is a
**structural guard against future drift**, not a violation detector against
the current 26-row skeleton — the spec authors already encoded `"symmetric"`
on every model-input row before V-9 was implemented. V-9's load-bearing
guarantee is that any future PR adding a row with
`per_player_construction != "symmetric"` (on a model-input row) is
mechanically blocked at the registry layer.

### What V-1..V-9 do NOT enforce — deferred dimensions

The following CROSS-02-03 dimensions are NOT mechanically enforced on this
artifact at the registry-skeleton layer. Each carries an explicit
commitment path for resolution before the thesis defense.

| Dim | Title | Status here | Commitment path |
|-----|-------|-------------|-----------------|
| D2 | Source classification + temporal availability | NOT mechanically enforced; declared per-row via `source_table_or_event_family` literal + manual cross-check against CROSS-02-00-v3.0.1 §5 column classification | Resolved at materialization step 02_01_02 via manual lineage review + post-materialization audit (CROSS-02-01-v1.0.1 §2.2 POST-GAME token absence check, AST-walk or docstring trace) |
| D3 | Source grain vs model grain | NOT mechanically enforced; declared per-row via `source_grain` + `model_input_grain` literals | Resolved at materialization step 02_01_02 via projection SQL review |
| D4 (in-game side) | Temporal anchor correctness for in-game features | NOT mechanically enforced beyond V-6's history-side check; in-game side relies on row-literal `temporal_anchor = "event.loop"` | Resolved at materialization via CROSS-02-01-v1.0.1 §2.1 cutoff structural check |
| D5 (in-game side) | Cutoff operator correctness for in-game features | NOT mechanically enforced beyond V-6's history-side check; in-game side relies on row-literal `allowed_cutoff_rule = "event.loop <= cutoff_loop"` | Resolved at materialization via CROSS-02-01-v1.0.1 §2.1 |
| D6 (full) | Target-game exclusion | partially enforced (V-6 strict-`<` for history; in-game / full-replay side relies on row-literal allowed_cutoff_rule) | Resolved at materialization via CROSS-02-01-v1.0.1 §2.2 + tracker eligibility CSV `full_replay_min_loop_blocked` per-row |
| D8 | Full-replay aggregate exclusion (in-game snapshots) | NOT mechanically enforced at registry layer; relies on row-literal `allowed_cutoff_rule` + tracker eligibility CSV per-row caveats | Resolved at materialization via post-materialization audit; for SC2, additional gate is the tracker eligibility CSV row's `upstream_verdicts` cell, which records the `full_replay_min_loop_blocked=True` verdict for V-7 time-to-first-event families |
| D9 | Normalization fit-scope | post-materialization-only per CROSS-02-03-v1.0.1 §4.1 | CROSS-02-01-v1.0.1 §2.3 post-materialization audit |
| D10 sub-clause 2 | aoestats `canonical_slot` p0/p1 projection | N/A for sc2egset (no `canonical_slot` column on sc2egset MHM per CROSS-02-00-v3.0.1 §5.1) | aoestats-side V-N PR (separate dataset) |
| D12 | Source-mode label discipline | N/A for sc2egset (no source-mode column) | N/A |
| D14 | AoE2 source-label discipline | N/A for sc2egset | N/A |
| D15 | Artifact-lineage readiness | methodology-discipline, asserted by lineage chain not by row check | Lineage rule `.claude/rules/data-analysis-lineage.md` |

### Non-supersession of the post-materialization audit

This registry artifact does NOT replace, weaken, or amend
CROSS-02-01-v1.0.1's post-materialization leakage audit gate. Per
CROSS-02-03-v1.0.1 §1.3, the design-time and post-materialization audits
are complementary, not redundant. Every feature column that this registry
triggers materialization of must additionally pass CROSS-02-01-v1.0.1's
audit before any consuming Pipeline Section may exit. The registry's
`validated_through = V-9` status does NOT excuse a materialized column
from CROSS-02-01-v1.0.1.

### Step 02_01_01 closure status — partial

This artifact satisfies clause 1 of the ROADMAP `continue_predicate` for
Step 02_01_01 ("CSV + MD artifact-check"). It does NOT satisfy clauses 2
or 3 ("CROSS-02-01-v1.0.1 post-materialization audit re-run for any
feature column the registry triggers materialization of"; "per-family
CROSS-02-03-v1.0.1 §10 verdict recorded for every registry row"). Step
02_01_01 therefore remains open. STEP_STATUS.yaml is unchanged by the PR
that emits this artifact. Closure of Step 02_01_01 is deferred to a
future PR after at least one materialization step (02_01_02 or successor)
runs CROSS-02-01-v1.0.1's post-materialization audit and records per-family
§10 verdicts for every registry row.

### Commitment path for resolving deferred dimensions before thesis defense

Per the methodology-debt commitment, the deferred dimensions D2 / D3 /
D4-in_game / D5-in_game / D6-full / D8 are resolved through path (a):
each is operationalized at its appropriate later layer (materialization
step + CROSS-02-01-v1.0.1 post-materialization audit), not through
additional V-N registry-layer validators. No CROSS-02-03 spec amendment
is required. This artifact is cited in the thesis (Chapter 4 §4.5) only
alongside the post-materialization audit artifact that closes the
deferred dimensions; the registry artifact alone does not constitute a
full Phase 02 leakage-clearance claim.
"""

# %%
# Build the row-counts-by-block table dynamically from _BLOCK_BY_FAMILY so the
# count is self-validating against the SKELETON partition. The expected
# partition is 5 + 6 + 4 + 7 + 4 = 26 per the plan §Disclaimer / §Gate
# Condition 3 (14-column row, 26-row CSV body).
_BLOCK_ORDER = [
    "pre_game",
    "history_enriched_pre_game",
    "in_game_now",
    "in_game_caveat",
    "gate_and_blocked",
]
_block_counts: dict[str, int] = {b: 0 for b in _BLOCK_ORDER}
for _block_label in _BLOCK_BY_FAMILY.values():
    _block_counts[_block_label] += 1
_row_count_table_lines = ["| block | row count |", "|-------|-----------|"]
for _block in _BLOCK_ORDER:
    _row_count_table_lines.append(f"| {_block} | {_block_counts[_block]} |")
_row_count_table_lines.append(f"| **total** | **{sum(_block_counts.values())}** |")
_ROW_COUNT_TABLE = "\n".join(_row_count_table_lines)

# %%
_PROVENANCE_BLOCK = (
    f"| field | value |\n"
    f"|-------|-------|\n"
    f"| notebook_path | `{_NOTEBOOK_PATH}` |\n"
    f"| validator_module | `{_VALIDATOR_MODULE}` |\n"
    f"| validated_through | `{_VALIDATED_THROUGH}` |\n"
    f"| closure_status | `{_CLOSURE_STATUS}` |\n"
    f"| manifest_status_token | `{_MANIFEST_STATUS}` |\n"
    f"| non_supersession | {_NON_SUPERSESSION} |\n"
    f"| executed_at (UTC date) | `{_EXECUTED_AT}` |\n"
    f"| git_sha | `{_GIT_SHA}` |\n"
    f"| python_version | `{_PYTHON_VERSION}` |\n"
    f"| poetry_version | `{_POETRY_VERSION}` |\n"
    f"| seed | `{_SEED}` |\n"
    f"| artifact_csv_path | `{_ARTIFACT_CSV_PATH}` |\n"
    f"| artifact_md_path | `{_ARTIFACT_MD_PATH}` |\n"
    f"| regenerated_via | `{_REGENERATION_COMMAND}` |\n"
    f"\n"
    f"Re-running the notebook on the same UTC day produces a byte-identical "
    f"artifact. Cross-UTC-day re-runs differ only in the `executed_at` field; "
    f"semantic content (CSV rows, MD body, disclaimer) is identical."
)

# %%
_REFERENCES_BLOCK = (
    "- CROSS-02-00-v3.0.1 — `reports/specs/02_00_feature_input_contract.md` "
    "(LOCKED 2026-05-03)\n"
    "- CROSS-02-01-v1.0.1 — `reports/specs/02_01_leakage_audit_protocol.md` "
    "(LOCKED 2026-05-03)\n"
    "- CROSS-02-02-v1.0.1 — `reports/specs/02_02_feature_engineering_plan.md` "
    "(LOCKED 2026-05-03)\n"
    "- CROSS-02-03-v1.0.1 — `reports/specs/02_03_temporal_feature_audit_protocol.md` "
    "(LOCKED 2026-05-03)"
)

# %%
MD_BODY = (
    "# SC2EGSet Step 02_01_01 — Feature-family registry "
    "(provisional, validated through V-9)\n\n"
    "## Provisional artifact disclaimer (validated through V-9)\n\n"
    f"{_DISCLAIMER_TEXT}\n"
    "## Provenance\n\n"
    f"{_PROVENANCE_BLOCK}\n\n"
    "## Row counts by block\n\n"
    f"{_ROW_COUNT_TABLE}\n\n"
    "## How to regenerate\n\n"
    "```bash\n"
    f"{_REGENERATION_COMMAND}\n"
    "```\n\n"
    "## References\n\n"
    f"{_REFERENCES_BLOCK}\n"
)

_md_path: Path = ARTIFACTS_DIR / "02_01_01_feature_family_registry.md"
_md_path.write_text(MD_BODY, encoding="utf-8")

print(f"SKELETON row count: {len(csv_rows)}")
print(f"CSV path: {_csv_path}")
print(f"MD path: {_md_path}")
print("validate_registry_skeleton: ALL PASS (V-1 through V-9); artifact emitted")

# %% [markdown]
# ## Conclusion
#
# ### Artifacts produced
# When this notebook is executed end-to-end, the artifact-emission cells above
# write a 26-row × 14-column CSV
# (`02_01_01_feature_family_registry.csv`) and a paired MD
# (`02_01_01_feature_family_registry.md`) under `ARTIFACTS_DIR` =
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`.
# Both files are tagged `validated_through = V-9` in the MD's `## Provenance`
# block. This is **provisional**: closure of Step 02_01_01 is NOT claimed.
# The ROADMAP `continue_predicate` for Step 02_01_01 has three clauses —
# (1) CSV + MD artifact-check, (2) CROSS-02-01-v1.0.1 post-materialization
# audit re-run for any feature column the registry triggers materialization
# of, and (3) per-family CROSS-02-03-v1.0.1 §10 verdict recorded for every
# registry row. This artifact satisfies clause (1) only. Clauses (2) and (3)
# remain open. The artifact's `## Provisional artifact disclaimer (validated
# through V-9)` section contains the verbatim per-dimension coverage table
# (D2 / D3 / D4-in_game / D5-in_game / D6-full / D8 / D9 / D10 sub-2 / D12 /
# D14 / D15) enumerating each unaddressed CROSS-02-03 dimension and its
# commitment path to resolution before the thesis defense.
#
# ### Status / log / manifest updates
# STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, PHASE_STATUS.yaml,
# `reports/ROADMAP.md`, and `.claude/scientific-invariants.md` are
# deliberately untouched by this PR. Rationale (per `planning/current_plan.md`
# §Problem Statement (c)): the ROADMAP `continue_predicate` for Step 02_01_01
# is three-clause and this artifact satisfies clause (1) only; flipping any
# status file to `complete` would falsely assert closure that the
# post-materialization audit and per-family §10 verdicts have not yet
# delivered. The per-dataset `research_log.md` IS updated with a
# partial-coverage entry (in a subsequent commit, T09), recording the
# `validated_through = V-9` artifact emission, the three-clause
# `continue_predicate`'s current state, and the deferred-dimension commitment
# paths. `thesis/pass2_evidence/notebook_regeneration_manifest.md` IS
# updated (also at T09) with a new `partial_coverage_v9_baseline` status
# token and a manifest row pointing to this notebook + the two artifact
# files + the disclaimer's coverage table.
#
# ### Thesis mapping
# Phase 02 readiness — feature input contract foundations for sc2egset.
# Concrete chapter mapping is deferred to the artifacts PR per Step 02_01_01
# completion criteria.
#
# ### Follow-ups
# - Step 02_01_01 remains open after this artifact PR; closure requires the
#   3-clause `continue_predicate`'s clauses 2 and 3 (CROSS-02-01-v1.0.1
#   post-materialization audit re-run + per-family CROSS-02-03-v1.0.1 §10
#   verdicts) — see ROADMAP.
# - Resolve the deferred CROSS-02-03 dimensions against the V-9 D-coverage
#   baseline established by this artifact: D2 (source classification +
#   temporal availability), D3 (source grain vs model grain), D4 in-game
#   side (temporal anchor correctness for in-game features beyond V-6's
#   history-side check), D5 in-game side (cutoff operator correctness for
#   in-game features beyond V-6's history-side check), D6 full (target-game
#   exclusion on the in-game / full-replay side), D8 (full-replay aggregate
#   exclusion for in_game_snapshot rows per CROSS-02-03-v1.0.1 §4.1; NOT
#   per_player_construction symmetry — that is D10 sub-clause 1, already
#   covered by V-9), D9 (normalization fit-scope, post-materialization-only
#   per CROSS-02-03-v1.0.1 §4.1), D12 (source-mode label discipline; N/A
#   for sc2egset which has no source-mode column), D14 (AoE2 source-label
#   discipline; N/A for sc2egset), and D15 (artifact-lineage readiness,
#   methodology-discipline asserted by lineage chain). Each is operationalized
#   at its appropriate later layer (materialization step 02_01_02 +
#   CROSS-02-01-v1.0.1 post-materialization audit), not through additional
#   V-N registry-layer validators.
# - D10 sub-clause 2 (aoestats `canonical_slot` p0/p1 projection per
#   CROSS-02-00-v3.0.1 §5.2; aoestats-ONLY column) is N/A for sc2egset
#   and is deferred to a future aoestats-side V-N PR.
