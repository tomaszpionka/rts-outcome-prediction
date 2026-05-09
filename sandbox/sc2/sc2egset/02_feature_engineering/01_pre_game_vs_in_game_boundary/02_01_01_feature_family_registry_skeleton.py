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
from pathlib import Path

from rts_predict.common.notebook_utils import get_reports_dir, setup_notebook_logging
from rts_predict.games.sc2.datasets.sc2egset.validate_registry_skeleton import (
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
# V-6 assertions and raises `AssertionError` with a descriptive message on any
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
# Any of the six structural checks fails — V-1 (schema integrity), V-2
# (tracker split counts), V-3 (blocked families remain blocked), V-4
# (`slot_identity_consistency` is `sanity_gate_not_model_input` while CSV
# remains `eligible_for_phase02_now`), V-5 (zero tracker-derived rows in
# `pre_game`/`history_enriched_pre_game`), V-6 (history rows use strict `<`
# with sc2egset `details_timeUTC` provenance, not `<=`, and reject the
# cross-dataset alias `started_at`).
#
# ### Expected artifact or report
# **None.** This scaffold PR explicitly produces NO report artifacts. Planned
# CSV / MD registry artifacts under
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
# are deferred to a subsequent artifacts PR after reviewed execution of all
# additional validation modules (D2, D3, D6, D8, D9, D10, D11, D12, D15).
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
# If V-1..V-6 ALL PASS, the skeleton structure is admissible as a candidate
# registry; subsequent PRs may add validation modules D2, D3, D6, D8, D9, D10,
# D11, D12, D15 and ultimately materialize the registry artifact. If ANY
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
# - Any V-1..V-6 assertion raises `AssertionError`.
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
# ## Validation module (V-1 through V-7)
#
# `validate_registry_skeleton` (in
# `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`)
# implements six structural checks against the 13-column audit object schema
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
#
# Checks IN scope as of this PR (V-1 strict + V-7): feature_family_id
# second-segment alignment with prediction_setting, and cold-start
# vocabulary/sentinel discipline (G-CS-1..G-CS-6 for active rows; literal
# "blocked" sentinel under the carve-out conjunction).
# Checks NOT YET in scope (deferred to subsequent validation modules):
# per-row optimal G-CS gate fit (which gate suits each family
# scientifically), per-player construction symmetry (Invariant I5),
# candidate-leakage-mode coverage against CROSS-02-01-v1.0.1, and audit
# dimensions D2/D3/D6/D8/D9/D10/D11/D12/D15.

# %%
# Run the single validation module. AssertionError halts execution; the
# notebook does NOT catch or mask exceptions. On success the module returns
# None and the cell prints an explicit ALL PASS banner.
validate_registry_skeleton(SKELETON, tracker_csv_path=TRACKER_CSV)
print("validate_registry_skeleton: ALL PASS (V-1 through V-7)")

# %% [markdown]
# ## Conclusion
#
# ### Artifacts produced
# **None.** Per `.claude/rules/data-analysis-lineage.md` §"Non-batching rule
# for empirical work", this PR delivers lineage sequence step 2 only —
# scaffold + one validation module. No CSV, MD, JSON, or PNG artifact is
# written by this notebook. Planned future artifacts (registry CSV at
# `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`
# and a paired MD narrative) are deferred to a subsequent artifacts PR after
# reviewed execution of all additional validation modules (D2, D3, D6, D8,
# D9, D10, D11, D12, D15).
#
# ### Status / log / manifest updates
# **None in this PR.** No edit to STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml,
# PHASE_STATUS.yaml, per-dataset `research_log.md`, cross-game
# `reports/research_log.md`, or
# `thesis/pass2_evidence/notebook_regeneration_manifest.md`. All deferred to
# the artifacts/log/status/manifest PR that closes Step 02_01_01.
#
# ### Thesis mapping
# Phase 02 readiness — feature input contract foundations for sc2egset.
# Concrete chapter mapping is deferred to the artifacts PR per Step 02_01_01
# completion criteria.
#
# ### Follow-ups
# - Add validation modules for audit dimensions D2 (controlled vocabularies
#   beyond V-1), D3 (per-row cold-start gate value check), D6 (candidate
#   leakage modes against CROSS-02-01-v1.0.1), D8 (per_player_construction
#   symmetry), D9 (allowed_cutoff_rule structural parsing), D10 (source-grain
#   well-formedness), D11 (model_input_grain consistency), D12 (target_grain
#   consistency with prediction_setting), D15 (cross-row consistency of
#   tracker-event-family references against the eligibility CSV).
# - After all validation modules pass on review, materialize the registry
#   CSV / MD artifact under
#   `reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/`,
#   then update STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS,
#   `research_log.md`, and `notebook_regeneration_manifest.md`.
# - Step 02_01_01 is NOT complete after this scaffold PR; completion requires
#   the subsequent artifacts/log/status/manifest PR.
