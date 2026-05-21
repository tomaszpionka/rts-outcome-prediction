# 02_01_01 Section-10 Verdict Audit — Evidence

## §1 Non-closure disclaimer

This artifact persists evidence but does NOT close Step `02_01_01`. Closure requires a separate later increment that flips `STEP_STATUS.yaml`, satisfies the ROADMAP `continue_predicate` three-clause gate in writing, and lands a separate closure PR. Phase 02 is `not_started` per `PHASE_STATUS.yaml` and is not advanced by this PR.

## §2 Provenance

- `audit_executed_at_utc_date`: `2026-05-21`
- `git_sha`: `2ee492d3d6ff9bf7b583c218d9a63b8a49546fe8`
- `validator_module`: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`
- `validator_module_sha256`: `7d164e42af3e6d434e642e089d5a8fd153cebcb548d2f5f84a8264f247a30268`
- `registry_csv_sha256`: `320b8b018982f12539a34512421f1b34359bb825f0d1410687492dfe5c6fed1f`
- `tracker_csv_sha256`: `11bd4b9ef7c80657a027db3831313c1d74c39b85834c25ecdfa78506e8ad8d22`
- `spec_revision_cross_02_03`: `CROSS-02-03-v1.0.1`
- `source_pr`: `PR #228`
- `audit_pr`: `PR #229`

## §3 Aggregate result

- `passed`: `True`
- `rows_audited`: `26`
- `halting_falsifier`: `None`
- `len(stricter_drifts)`: `0`
- `len(looser_drifts)`: `0`
- `len(independent_trigger_hits)`: `0`
- `materialized_column_count`: `0`

## §4 Falsifier roll-call

| Falsifier | Description | Result |
|---|---|---|
| F-1 | Overall bidirectional §10 EQUALITY | did not fire |
| F-1a | Stricter drift (derived > recorded) | did not fire |
| F-1b | Looser drift (derived < recorded) | did not fire |
| F-2 | Independent §10.2 trigger on allowed/caveat row | did not fire |
| F-3 | Post-game token in `allowed_cutoff_rule` | did not fire |
| F-4 | Invalid cutoff operator on history row | did not fire |
| F-5 | D13 tracker contradiction | did not fire |
| F-6 | Slot-identity gate misuse | did not fire |
| F-7 | Controlled-vocab drift | did not fire |
| PERSIST | Persistence byte-equivalence | did not fire |

## §5 ROADMAP `continue_predicate` three-clause analysis

**ROADMAP `continue_predicate` (verbatim, `ROADMAP.md` lines 2060-2066):**

> A future PR may begin Step 02_01_02 (or the next 02_01 step in the ROADMAP) only after this Step 02_01_01 has reached its CSV + MD artifact-check at a future PR, the CROSS-02-01-v1.0.1 post-materialization audit gate has been re-run for any feature column the registry triggers materialization of, and a per-family CROSS-02-03-v1.0.1 §10 verdict is recorded for every registry row.

| Clause | Status |
|---|---|
| 1 — Registry CSV+MD artifact-check | SATISFIED for the registry CSV/MD by PR #216 (provisional artifact); the new PM-1 evidence artifact is incremental and does NOT itself satisfy clause 1. |
| 2 — Post-materialization audit gate | VACUOUSLY SATISFIED. No materialized-column audit is applicable at the catalog-only registry layer (materialized_column_count=0); this becomes non-vacuous once Step 02_01_02 materializes the first feature column per 02_01_leakage_audit_protocol.md §4 lines 117–121. |
| 3 — Per-family §10 verdict recorded for every registry row | SATISFIED in memory by PR #228 + PERSISTED ON DISK by PR #229 for all 26 rows. |

**Closure status remains OPEN** — clause-1 is satisfied; clause-3 is satisfied as of this PR; the three-clause gate is positioned to be closed only by a later explicit closure PR with status-YAML flips.

## §6 Methodology lineage

- Spec source: `reports/specs/02_03_temporal_feature_audit_protocol.md` §10 (CROSS-02-03-v1.0.1, LOCKED 2026-05-06); `reports/specs/02_01_leakage_audit_protocol.md` §4 lines 117–121 (Materialization).
- Validator: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py` (frozen by PR #228; SHA-256 `7d164e42af3e6d434e642e089d5a8fd153cebcb548d2f5f84a8264f247a30268`).
- Notebook: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py` (artifact-write cell added in PR #229).
- Tests: `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py` (frozen by PR #228; PERSIST byte-equivalence substitutes for re-run in this PR).

## §7 Per-row table

| feature_family_id | prediction_setting | registry_recorded_status | derived_section10_verdict | equality_token | block |
|---|---|---|---|---|---|
| `sc2egset.pre_game.focal_race_with_opponent_race_pair` | `pre_game` | `allowed` | `allowed` | `equal` | `pre_game` |
| `sc2egset.pre_game.map_type_encoded` | `pre_game` | `allowed` | `allowed` | `equal` | `pre_game` |
| `sc2egset.pre_game.patch_version_encoded` | `pre_game` | `allowed` | `allowed` | `equal` | `pre_game` |
| `sc2egset.pre_game.matchup_encoded` | `pre_game` | `allowed` | `allowed` | `equal` | `pre_game` |
| `sc2egset.pre_game.is_mmr_missing_flag` | `pre_game` | `allowed` | `allowed` | `equal` | `pre_game` |
| `sc2egset.history_enriched_pre_game.focal_player_history` | `history_enriched_pre_game` | `allowed` | `allowed` | `equal` | `history_enriched_pre_game` |
| `sc2egset.history_enriched_pre_game.opponent_player_history` | `history_enriched_pre_game` | `allowed` | `allowed` | `equal` | `history_enriched_pre_game` |
| `sc2egset.history_enriched_pre_game.matchup_history_aggregate` | `history_enriched_pre_game` | `allowed` | `allowed` | `equal` | `history_enriched_pre_game` |
| `sc2egset.history_enriched_pre_game.reconstructed_rating` | `history_enriched_pre_game` | `allowed` | `allowed` | `equal` | `history_enriched_pre_game` |
| `sc2egset.history_enriched_pre_game.cross_region_fragmentation_handling` | `history_enriched_pre_game` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `history_enriched_pre_game` |
| `sc2egset.history_enriched_pre_game.in_game_history_aggregate` | `history_enriched_pre_game` | `allowed` | `allowed` | `equal` | `history_enriched_pre_game` |
| `sc2egset.in_game_snapshot.count_units_built_by_cutoff_loop` | `in_game_snapshot` | `allowed` | `allowed` | `equal` | `in_game_now` |
| `sc2egset.in_game_snapshot.count_units_killed_by_cutoff_loop` | `in_game_snapshot` | `allowed` | `allowed` | `equal` | `in_game_now` |
| `sc2egset.in_game_snapshot.morph_count_by_cutoff_loop` | `in_game_snapshot` | `allowed` | `allowed` | `equal` | `in_game_now` |
| `sc2egset.in_game_snapshot.building_construction_count_by_cutoff_loop` | `in_game_snapshot` | `allowed` | `allowed` | `equal` | `in_game_now` |
| `sc2egset.in_game_snapshot.minerals_collection_rate_history_mean` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.army_value_at_5min_snapshot` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.supply_used_at_cutoff_snapshot` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.food_used_max_history` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.time_to_first_expansion_loop` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.count_units_lost_by_cutoff_loop` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.count_upgrades_by_cutoff_loop` | `in_game_snapshot` | `allowed_with_caveat` | `allowed_with_caveat` | `equal` | `in_game_caveat` |
| `sc2egset.in_game_snapshot.slot_identity_consistency` | `in_game_snapshot` | `sanity_gate_not_model_input` | `sanity_gate_not_model_input` | `equal` | `gate_and_blocked` |
| `sc2egset.blocked_or_deferred.mind_control_event_count` | `blocked_or_deferred` | `blocked_until_additional_validation` | `blocked_until_validation` | `equal_via_synonym` | `gate_and_blocked` |
| `sc2egset.blocked_or_deferred.army_centroid_at_cutoff_snapshot` | `blocked_or_deferred` | `blocked_until_additional_validation` | `blocked_until_validation` | `equal_via_synonym` | `gate_and_blocked` |
| `sc2egset.blocked_or_deferred.playerstats_cumulative_economy_fields` | `blocked_or_deferred` | `blocked_until_additional_validation` | `blocked_until_validation` | `equal_via_synonym` | `gate_and_blocked` |

## §8 Cited code / SQL

Validator entry point (frozen by PR #228):

```python
def validate_registry_section10_verdicts(
    registry_csv_path: Path,
    tracker_csv_path: Path,
) -> RegistryVerdictAuditResult:
    """Entry point: load registry rows and run the full §10 verdict audit."""
```

Notebook call site (PR #229):

```python
result_persist = validate_registry_section10_verdicts(REGISTRY_CSV_PATH, TRACKER_CSV_PATH)
assert result_persist.passed is True
assert result_persist.rows_audited == 26
assert result_persist.materialized_column_count == 0
```
