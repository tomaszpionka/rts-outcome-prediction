# SC2EGSet Step 02_01_01 — Feature-family registry (provisional, validated through V-9)

## Provisional artifact disclaimer (validated through V-9)

## Coverage status — provisional registry artifact

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

## Provenance

| field | value |
|-------|-------|
| notebook_path | `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.py` |
| validator_module | `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py` |
| validated_through | `V-9` |
| closure_status | `partial` |
| manifest_status_token | `partial_coverage_v9_baseline` |
| non_supersession | CROSS-02-01-v1.0.1 remains mandatory |
| executed_at (UTC date) | `2026-05-16` |
| git_sha (execution HEAD short SHA) | `0dbd42f7` |
| python_version | `3.12.13` |
| poetry_version | `Poetry (version 2.4.1)` |
| seed | `not_applicable_deterministic_export` |
| artifact_csv_path | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv` |
| artifact_md_path | `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md` |
| regenerated_via | `poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb` |

Re-running the notebook produces a byte-identical artifact when the UTC date, the execution `git_sha`, and the tool-version environment (`python_version`, `poetry_version`) are all unchanged. Cross-UTC-day reruns differ only in the `executed_at` field. Reruns from a different git SHA (e.g., after a commit) differ in the `git_sha` field by design. Semantic content (registry rows, disclaimer, deferred-dimension table) is unchanged unless the notebook source changes.

## Row counts by block

| block | row count |
|-------|-----------|
| pre_game | 5 |
| history_enriched_pre_game | 6 |
| in_game_now | 4 |
| in_game_caveat | 7 |
| gate_and_blocked | 4 |
| **total** | **26** |

## How to regenerate

```bash
poetry run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry_skeleton.ipynb
```

## References

- CROSS-02-00-v3.0.1 — `reports/specs/02_00_feature_input_contract.md` (LOCKED 2026-05-03)
- CROSS-02-01-v1.0.1 — `reports/specs/02_01_leakage_audit_protocol.md` (LOCKED 2026-05-03)
- CROSS-02-02-v1.0.1 — `reports/specs/02_02_feature_engineering_plan.md` (LOCKED 2026-05-03)
- CROSS-02-03-v1.0.1 — `reports/specs/02_03_temporal_feature_audit_protocol.md` (LOCKED 2026-05-03)
