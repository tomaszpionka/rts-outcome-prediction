---
title: "SC2EGSet Phase-02 Step 02_01_01 — PM-1 §10 verdict audit (closure increment 1/N)"
category: A
branch: feat/sc2egset-02-01-01-section10-verdict-audit
base_ref: db8aeafc2b413d40a933a81f11605ee209117387
date: 2026-05-21
version_bump: "n/a (no release in this PR)"
planner_model: user-directed (reviewer-adversarial gate APPROVE Round-2)
dataset: sc2egset
phase: "02"
pipeline_section: "02_01"
invariants_touched: [I3, I5, I6, I7, I8, I9, I10]
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv
critique_required: true
critique_file: planning/current_plan.critique.md
research_log_ref: null
---

## Scope

This plan covers the SC2EGSet Phase-02 Step 02_01_01 PM-1 §10 verdict audit
(closure increment 1/N). See §1 Boundary Decision below for full scope statement.
PM-1 does NOT close Step `02_01_01`; it is one increment of several.

## Problem Statement

The SC2EGSet Phase-02 registry CSV records a `status` field for each of 26
feature-family rows. These statuses must match the verdicts derivable from
CROSS-02-03-v1.0.1 §10 protocol rules. Without a formal bidirectional audit,
the registry may be optimistic (stale allowed rows) or overly conservative
(falsely blocked rows), either of which would compromise the Phase-02 scope.
See §6 Hypothesis and §7 Falsifiers for the measurement approach.

## Assumptions & Unknowns

See §5 Assumptions for the full list (A-1 through A-6). Key items:
- The registry uses `blocked_until_additional_validation` as a synonym for
  spec-side `blocked_until_validation` (A-3).
- `materialized_column_count = 0` always for this design-time audit (A-6).
- No unknowns remain; all were resolved before the adversarial gate.

## Literature Context

Not applicable. This is a design-time structural audit of an internal
feature-family registry against a locked specification. No external literature
references are required.

## Execution Steps

1. T00: Create feature branch from master @ `db8aeafc2b413d40a933a81f11605ee209117387`.
2. T01: Read and verify on-disk anchors (registry CSV, spec files, tracker CSV).
3. T02: Write `planning/current_plan.md` (this file).
4. T03: Write `planning/current_plan.critique.md`.
5. T04: Write `validate_registry_section10_verdicts.py` (the validator module).
6. T05: Write `test_validate_registry_section10_verdicts.py` (14+ test cases).
7. T06: Write and jupytext-sync `02_01_01_registry_section10_verdict_audit.{py,ipynb}`.
8. T07: Run pytest (all 14 required tests pass; T-26ROW passes on real registry);
   ruff + mypy clean; jupytext sync confirmed.
9. T08: Commit, push, open PR.

## File Manifest

New files:
- `planning/current_plan.md` (this file)
- `planning/current_plan.critique.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`
- `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`
- `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.ipynb`

Modified files: none (planning files are new or updated; no other files).

## Gate Condition

See §16 Gate Condition for the full list. Summary: all 14 required tests pass
including T-26ROW with `passed=True, rows_audited=26, materialized_column_count=0`;
ruff/mypy/jupytext clean; zero diff on all forbidden paths.

## Open Questions

See §20 Open Questions / Blockers. OQ-1 and OQ-2 are both RESOLVED.
No blockers remain.

---

# §1 Boundary decision

This plan covers the **remaining `02_01_01` closure increment** — specifically PM-1
(§10 verdict audit): a design-time CROSS-02-03-v1.0.1 §10 verdict audit of all
26 feature-family rows in the on-disk registry CSV.

This plan does NOT cover:
- `02_01_02` or any later Pipeline Section step.
- Phase 03 or any subsequent phase.
- ROADMAP amendment.
- STEP_STATUS or PHASE_STATUS flip.
- A docs-only lineage note.
- A status-chain closure PR.

PM-1 alone does NOT close Step `02_01_01`. It is increment 1 of N required
to close `02_01_01`. The step remains open after this PR merges.

# §2 Repo evidence

- Registry CSV: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv`
  — 26 data rows + 1 header; 14 columns: `feature_family_id`, `dataset_tag`,
  `prediction_setting`, `source_table_or_event_family`, `source_grain`,
  `model_input_grain`, `target_grain`, `temporal_anchor`, `allowed_cutoff_rule`,
  `candidate_leakage_modes`, `cold_start_handling`, `status`,
  `per_player_construction`, `block`.
- Temporal audit protocol: `reports/specs/02_03_temporal_feature_audit_protocol.md`
  (CROSS-02-03-v1.0.1, LOCKED 2026-05-06) — §10.1 four-verdict taxonomy;
  §10.2 blocking-trigger checklist; §10.3 tracker special case.
- Leakage audit protocol: `reports/specs/02_01_leakage_audit_protocol.md`
  (CROSS-02-01-v1.0.1, LOCKED 2026-04-26) — "Materialization" defined at
  lines 117-121 as persisting a feature column to DuckDB/Parquet.
- Tracker eligibility CSV: `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/01_exploration/03_profiling/tracker_events_feature_eligibility.csv`
  — `feature_family` → `status_in_game_snapshot` for D13 cross-check.
- Skeleton validator: `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_skeleton.py`
  — style/layout reference.
- Existing test: `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_skeleton.py`
  — mirror layout reference.

# §3 Atomic step proposed

Write a new validator module `validate_registry_section10_verdicts.py` that,
given the registry CSV path and tracker eligibility CSV path, derives the §10
verdict for each of the 26 rows independently from the protocol rules + row
evidence, then compares each derived verdict to the registry's recorded `status`
column, emitting bidirectional drift detection and independent §10.2 trigger
evaluation.

Deliverables in one PR:
1. `planning/current_plan.md` (this file — durable approved plan).
2. `planning/current_plan.critique.md` (adversarial gate record).
3. `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`.
4. `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py`.
5. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py` (jupytext percent format).
6. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.ipynb` (jupytext-paired).

# §4 Why this is not batching

This unit performs exactly one empirical operation: design-time §10 verdict
derivation and comparison against the on-disk registry. It does NOT:
- materialize any feature column;
- write any artifact CSV/Parquet to `reports/artifacts/`;
- update STEP_STATUS, PHASE_STATUS, ROADMAP, or research_log;
- implement any feature-generation notebook;
- run any Phase 03 logic.

The notebook scaffold contains a single validation call and assertion; it does
not generate downstream artifacts. The `.claude/rules/data-analysis-lineage.md`
non-batching rule applies to empirical notebooks that produce artifacts; this
increment produces zero artifacts, so the batching prohibition is satisfied.

# §5 Assumptions

A-1. The 26-row registry CSV is correct on disk (verified in T01 read).
A-2. CROSS-02-03-v1.0.1 §10.1 verdicts are: `allowed`, `allowed_with_caveat`,
     `blocked_until_validation`, `sanity_gate_not_model_input`.
A-3. The registry's `status` column uses the dataset-side token
     `blocked_until_additional_validation` as a synonym for spec-side
     `blocked_until_validation` (per registry inspection — the registry uses
     the longer form for all currently-blocked rows).
A-4. `derive_section10_verdict` operates exclusively on `prediction_setting`,
     `allowed_cutoff_rule`, `candidate_leakage_modes`, `feature_family_id`,
     `source_table_or_event_family`, and the tracker eligibility CSV — never
     on `row["status"]`.
A-5. The tracker eligibility CSV column `status_in_game_snapshot` for
     `slot_identity_consistency` is `eligible_for_phase02_now` (registry
     reclassifies to `sanity_gate_not_model_input` independently).
A-6. `materialized_column_count = 0` always because this is a design-time
     audit — no feature columns have been persisted to DuckDB/Parquet at
     this step.

# §6 Hypothesis

Every one of the 26 feature-family rows in the on-disk registry carries a
`status` value that exactly matches (modulo the `blocked_until_additional_validation`
/ `blocked_until_validation` synonym) the verdict derivable from
CROSS-02-03-v1.0.1 §10 rules applied to the row's evidence fields. No row
triggers an unmitigated §10.2 blocking condition that its recorded `status`
does not already reflect.

# §7 Falsifiers

F-1 (overall — bidirectional EQUALITY): The derived §10 verdict for any row
MUST equal the registry's recorded `status` (modulo the synonym in A-3). Any
discrepancy in either direction halts execution.

F-1a (stricter drift — HALT): The derived verdict is strictly more restrictive
than the recorded status (e.g., derived=`blocked_until_validation`,
recorded=`allowed`). This indicates the registry is optimistic / stale. HALT
immediately.

F-1b (looser drift — HALT): The derived verdict is strictly less restrictive
than the recorded status (e.g., derived=`allowed`, recorded=
`blocked_until_validation`). This indicates the registry is overly conservative
or the derivation logic is missing a caveat path. HALT immediately.

F-2 (independent §10.2 trigger checklist — HALT): An independent evaluation
of the §10.2 blocking-trigger checklist (evaluated WITHOUT reading `row["status"]`)
fires a trigger on a row whose recorded status is `allowed` or
`allowed_with_caveat`. HALT: this row should be blocked.

F-3 (POST-GAME token leakage — HALT): Any row's `allowed_cutoff_rule` contains
a post-outcome reference token (`won`, `final_state`, `match_result`,
`post_game`). HALT: this is temporal leakage.

F-4 (invalid cutoff operator — HALT): A `history_enriched_pre_game` row's
`allowed_cutoff_rule` contains `<=` or `=` or `>=` instead of strict `<`.
HALT: violates CROSS-02-00-v3.0.1 §3.3.

F-5 (D13 tracker contradiction — HALT): An `in_game_snapshot` row's
`status` is `allowed` or `allowed_with_caveat` but the tracker eligibility CSV
records `status_in_game_snapshot = blocked_until_additional_validation` for
that family. HALT: tracker CSV overrides registry.

F-6 (slot-identity gate misuse — HALT): The `slot_identity_consistency` row
is NOT classified `sanity_gate_not_model_input`. HALT: this family is
reserved as an engineering sanity gate, not a model input.

F-7 (controlled-vocab drift — HALT): Any row's `status` value is not in the
union of spec-side verdicts (`allowed`, `allowed_with_caveat`,
`blocked_until_validation`, `sanity_gate_not_model_input`) and the
dataset-side synonym (`blocked_until_additional_validation`).

Implementation invariant for F-1 / F-2 independence:
"validator derives the expected verdict from protocol rules + row evidence
FIRST; registry `status` is compared only AFTER independent derivation; any
drift in either direction halts; this prevents stale-registry laundering."

# §8 Sanity checks

S-1 (existence): The registry CSV exists on disk at the expected path before
any audit begins. If absent, `load_registry_rows` raises a clear exception.

S-2 (26 rows): The registry CSV contains exactly 26 data rows (excluding
header). If row count != 26, `load_registry_rows` raises.

S-3 (unique IDs): All `feature_family_id` values are unique. If any
duplicate exists, `load_registry_rows` raises.

S-4 (derive-before-compare): Every row's independent verdict is derived
before any comparison against `row["status"]` is performed. The implementation
ensures this by collecting all derived verdicts into a dict in a first pass,
then comparing in a second pass.

S-5 (materialized_column_count == 0): `RegistryVerdictAuditResult.materialized_column_count`
is always set to 0. This is a design-time audit; no feature columns exist.
The validator hard-codes this value and the notebook asserts it explicitly.

S-6 (no write side effects): No cell in the notebook and no function in the
validator writes to `reports/artifacts/`, `reports/STEP_STATUS.yaml`,
`reports/PHASE_STATUS.yaml`, `reports/ROADMAP.md`, `reports/research_log.md`,
or any Phase-03 path. The notebook must end with a closure markdown cell
explicitly stating this.

# §9 Implementation design

## §9.1 File structure

```
src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py
tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py
sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/
    02_01_01_registry_section10_verdict_audit.py   (jupytext source)
    02_01_01_registry_section10_verdict_audit.ipynb (paired)
```

## §9.2 Public API signatures

```python
@dataclass(frozen=True)
class Section10Rules:
    """Frozen view of the §10 protocol rules used in derivation."""
    verdicts: frozenset[str]
    blocking_triggers: tuple[str, ...]
    history_cutoff: str          # expected strict-'<' token for history rows
    ingame_cutoff: str           # expected '<=' token for in-game rows
    slot_identity_feature_id: str
    sc2_tracker_blocked_token: str
    tracker_eligibility_csv_path: Path


@dataclass(frozen=True)
class Section10Verdict:
    """Per-row derived verdict and evidence trail."""
    feature_family_id: str
    derived_status: str           # one of SECTION10_VERDICTS
    triggers_fired: tuple[str, ...]
    rule_path: str                # human-readable derivation path


@dataclass(frozen=True)
class RegistryVerdictAuditResult:
    """Aggregate result of the full §10 verdict audit."""
    passed: bool
    rows_audited: int
    halting_falsifier: str | None  # first matched falsifier label or None
    stricter_drifts: tuple[tuple[str, str, str], ...]  # (ffid, derived, recorded)
    looser_drifts: tuple[tuple[str, str, str], ...]    # (ffid, derived, recorded)
    independent_trigger_hits: tuple[tuple[str, str], ...]  # (ffid, trigger_name)
    materialized_column_count: int  # always 0


def load_registry_rows(registry_csv_path: Path) -> list[pd.Series]:
    """Load the 26-row registry CSV, enforcing S-1 / S-2 / S-3.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.

    Returns:
        List of pd.Series, one per data row (excluding header).

    Raises:
        FileNotFoundError: if CSV does not exist (S-1).
        ValueError: if row count != 26 (S-2) or duplicate feature_family_id (S-3).
    """


def derive_section10_verdict(
    row: pd.Series,
    protocol_rules: Section10Rules,
) -> Section10Verdict:
    """Derive the §10 verdict for a single registry row from protocol rules + row evidence.

    The function does NOT read `row['status']` — the registry's recorded status is
    excluded from the derivation input set. To make accidental reads structurally
    impossible, the function projects the row to a view that explicitly drops the
    'status' column before any rule evaluation:
        row_evidence = row.drop(labels=[s for s in ('status',) if s in row.index])
    All rule evaluation operates exclusively on row_evidence.

    Args:
        row: pd.Series with registry columns. Must contain 'prediction_setting',
            'allowed_cutoff_rule', 'candidate_leakage_modes', 'feature_family_id',
            'source_table_or_event_family'. Must NOT be read for 'status'.
        protocol_rules: Frozen §10 rule set, including tracker CSV path.

    Returns:
        Section10Verdict with the derived status and evidence trail.
    """


def compare_registry_verdicts(
    rows: list[pd.Series],
    protocol_rules: Section10Rules,
) -> RegistryVerdictAuditResult:
    """Compare independently derived §10 verdicts against registry recorded status.

    Step order (S-4 enforced):
    1. Derive all row verdicts independently (first pass, no status reads).
    2. Compare each derived verdict to row['status'] (second pass).
    3. Classify stricter drifts (F-1a) and looser drifts (F-1b).
    4. Run independent §10.2 trigger checklist on every row (F-2).
    5. Set halting_falsifier in priority: F-1a > F-1b > F-2 > F-3 > F-4 > F-5 > F-6 > F-7.
    6. Set materialized_column_count = 0 (S-5).
    7. Set passed = (no halting_falsifier AND drifts empty AND triggers empty AND rows == 26).

    Args:
        rows: List of pd.Series from load_registry_rows.
        protocol_rules: Frozen §10 rule set.

    Returns:
        RegistryVerdictAuditResult with full audit summary.
    """


def validate_registry_section10_verdicts(
    registry_csv_path: Path,
    tracker_csv_path: Path,
) -> RegistryVerdictAuditResult:
    """Entry point: load registry rows and run the full §10 verdict audit.

    Args:
        registry_csv_path: Path to 02_01_01_feature_family_registry.csv.
        tracker_csv_path: Path to tracker_events_feature_eligibility.csv.

    Returns:
        RegistryVerdictAuditResult. Caller is responsible for asserting .passed.
    """
```

## §9.3 Verdict derivation dispatch

Verdict derivation is dispatched by `prediction_setting`:

- `pre_game` rows: if no §10.2 trigger fires → `allowed`; else `blocked_until_validation`.
- `history_enriched_pre_game` rows: assert `allowed_cutoff_rule == HISTORY_STRICT_CUTOFF`
  (strict `<`). If a row's `candidate_leakage_modes` admits an unmitigated leakage
  mode without a sibling mitigator → `blocked_until_validation`; else `allowed`
  (or `allowed_with_caveat` per declared caveat token).
- `in_game_snapshot` rows: if `feature_family_id == SLOT_IDENTITY_FEATURE_ID` →
  `sanity_gate_not_model_input`; if D13 (tracker eligibility CSV says
  `blocked_until_additional_validation`) → `blocked_until_validation`; if row
  declares `lps_caveat_on_5min` or similar caveat token → `allowed_with_caveat`;
  else if tracker CSV says `eligible_with_caveat` → `allowed_with_caveat`; else `allowed`.
- `blocked_or_deferred` rows: `blocked_until_validation`.

## §9.4 Verdict strictness ordering

For F-1a / F-1b drift detection:
`allowed` < `allowed_with_caveat` < `sanity_gate_not_model_input` < `blocked_until_validation`

"Stricter" drift = derived rank > registry rank.
"Looser" drift = derived rank < registry rank.

## §9.5 Top-level constants (no magic numbers)

```python
EXPECTED_ROW_COUNT = 26
SECTION10_VERDICTS = frozenset({
    "allowed", "allowed_with_caveat",
    "blocked_until_validation", "sanity_gate_not_model_input"
})
DATASET_SIDE_BLOCKED_SYNONYM = "blocked_until_additional_validation"
HISTORY_STRICT_CUTOFF = "history_time < target_time"
INGAME_CUTOFF = "event.loop <= cutoff_loop"
SLOT_IDENTITY_FEATURE_ID = "sc2egset.in_game_snapshot.slot_identity_consistency"
```

# §10 SQL / temporal predicates

No SQL is executed by this module. The temporal predicate reference is
declarative only (read from the registry CSV):
- History rows MUST declare: `history_time < target_time` (strict `<`).
- In-game rows MUST declare: `event.loop <= cutoff_loop`.

Both are validated by rule comparison against constants, not by SQL execution.

# §11 Validation module design

The validator enforces:
- S-1/S-2/S-3 inline in `load_registry_rows`.
- S-4 (derive-before-compare) as structural first-pass/second-pass separation
  in `compare_registry_verdicts`.
- S-5 (materialized_column_count = 0) hard-coded in `compare_registry_verdicts`.
- F-1a/F-1b (bidirectional drift) via verdict rank comparison.
- F-2 (independent trigger checklist) evaluated without reading `status`.
- F-3 (post-game token leakage) scanned in `allowed_cutoff_rule`.
- F-4 (invalid cutoff operator) asserted for history rows.
- F-5 (D13 tracker contradiction) cross-checked against tracker eligibility CSV.
- F-6 (slot-identity gate misuse) checked against SLOT_IDENTITY_FEATURE_ID.
- F-7 (controlled-vocab drift) checked against SECTION10_VERDICTS union synonym.

Halting priority: F-1a > F-1b > F-2 > F-3 > F-4 > F-5 > F-6 > F-7.

# §12 Notebook scaffold design

File: `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`
(jupytext percent format; paired `.ipynb` materialized by `jupytext --sync`).

Cells (≤50 lines each; no inline `def`/`class`/`lambda`; all logic imported from `src/`):

1. **Front-matter markdown**: declare `step: "02_01_01"` (closure increment),
   assumption / measurement claim / sanity check / falsifier / expected report /
   lineage source / downstream decision (7-tuple per data-analysis-lineage.md),
   and explicit "INCREMENT 1 of N — scaffold + PM-1 only; design-time §10 verdict
   audit; NOT materialization; does NOT close Step `02_01_01`; does NOT flip
   STEP_STATUS/PHASE_STATUS; NO artifact written" banner.

2. **Hypothesis markdown**: verbatim from §6.

3. **Falsifier markdown**: F-1/F-1a/F-1b/F-2..F-7 verbatim.

4. **Imports cell**: `validate_registry_section10_verdicts`, `RegistryVerdictAuditResult`,
   `Section10Rules`; `notebook_utils.get_reports_dir`; `logging`.

5. **Path resolution cell**: derive registry CSV path, tracker CSV path.

6. **Sanity-check cell**: call `load_registry_rows`; assert S-1/S-2/S-3 inline;
   print row count and head (use `print` for data exploration per repo convention).

7. **Validation cell**: call `validate_registry_section10_verdicts(...)`; surface
   the `RegistryVerdictAuditResult`.

8. **Drift report cell**: pretty-print stricter/looser drifts; halt narrative
   if non-empty.

9. **§10.2 trigger report cell**: pretty-print `independent_trigger_hits`; halt
   narrative if non-empty.

10. **Vacuous clause-2 cell**: print `materialized_column_count = 0` + the
    explanatory message (clause-2 materialized column set is EMPTY, vacuously
    satisfied).

11. **Gate-assertion cell**: explicit Python assertions:
    `assert result.passed is True`
    `assert result.rows_audited == 26`
    `assert result.materialized_column_count == 0`

12. **Closure markdown**: S-6 statement — no status, artifact, ROADMAP,
    research_log, or Phase-03 output is written by this notebook; explicit
    "this is a design-time §10 verdict audit, not materialization; does NOT
    close Step `02_01_01`" reminder.

NO artifact-writing cell. No `to_csv` / `to_parquet` / `open("w")`. No DuckDB write.

# §13 Tests

14 required test cases:

- **T-INDEP**: Construct two `pd.Series` rows identical except for `status`.
  Assert `derive_section10_verdict(rowA).derived_status == derive_section10_verdict(rowB).derived_status`.
  Also assert the function works correctly when `status` key is entirely absent
  from the row (structural independence check via `row.drop` guard).

- **T-F1A**: Construct a synthetic registry where one row has a derived verdict
  stricter than its recorded `status`. Assert `result.passed is False` and
  `result.halting_falsifier == "F-1a"` and `len(result.stricter_drifts) >= 1`.

- **T-F1B**: Construct a synthetic registry where one row has a derived verdict
  looser than its recorded `status`. Assert `result.passed is False` and
  `result.halting_falsifier == "F-1b"` and `len(result.looser_drifts) >= 1`.

- **T-F2**: Construct a row where a §10.2 blocking trigger fires but recorded
  `status` is `allowed`. Assert the independent trigger hit is reported and
  `passed is False`.

- **T-F3**: Construct a row where `allowed_cutoff_rule` contains a post-game
  token. Assert `halting_falsifier` indicates F-3.

- **T-F4**: Construct a `history_enriched_pre_game` row where `allowed_cutoff_rule`
  contains `<=`. Assert `halting_falsifier` indicates F-4.

- **T-F5**: Construct an `in_game_snapshot` row where the tracker CSV records
  `blocked_until_additional_validation` but the registry `status` is `allowed`.
  Assert `halting_falsifier` indicates F-5.

- **T-F6**: Construct a registry where `slot_identity_consistency` is NOT
  classified `sanity_gate_not_model_input`. Assert `halting_falsifier`
  indicates F-6.

- **T-F7**: Construct a row with an unrecognized `status` value. Assert
  `halting_falsifier` indicates F-7.

- **T-VAC**: Assert `result.materialized_column_count == 0` always (vacuous
  clause-2 check), using both a synthetic registry and the real registry.

- **T-26ROW**: Run `validate_registry_section10_verdicts` against the real
  on-disk registry. Assert `result.passed is True`, `result.rows_audited == 26`,
  `result.materialized_column_count == 0`, `result.halting_falsifier is None`,
  `len(result.stricter_drifts) == 0`, `len(result.looser_drifts) == 0`,
  `len(result.independent_trigger_hits) == 0`.

- **T-ROWCNT**: Provide a CSV with != 26 rows. Assert `load_registry_rows`
  raises `ValueError` with a message referencing the count.

- **T-EMPTY**: Provide an empty CSV (header only). Assert `load_registry_rows`
  raises `ValueError`.

- **T-SYN**: Assert that `blocked_until_additional_validation` (dataset-side)
  and `blocked_until_validation` (spec-side) are treated as equal synonyms
  in the comparison logic (no false F-1a/F-1b drift triggered).

# §14 Leakage risks

No leakage risk: this module reads registry metadata (declarations), not
feature values. It performs no temporal computations and produces no feature
columns. The only data read is the registry CSV and tracker eligibility CSV,
both of which are design-time artifacts.

# §15 Cold-start behavior

Cold-start is N/A for this module, for four reasons:
1. This is a design-time audit of declarations, not a feature-generation step.
2. No feature values are computed, so there is no population to have cold-start
   gaps in.
3. The registry rows themselves declare the cold-start gate tokens (G-CS-1..G-CS-6);
   those tokens are read but not evaluated for cold-start behavior.
4. Cold-start evaluation belongs to the feature-generation notebooks (Phase 02
   later increments), not to the §10 verdict audit.

# §16 Gate condition

This PR (PM-1) passes its own gate if and only if:
- All 14 tests pass (including T-26ROW with `passed=True, rows_audited=26,
  materialized_column_count=0`).
- Ruff check passes with zero warnings on all three new files.
- Mypy passes on the validator module.
- Jupytext sync confirms `.py` and `.ipynb` are in agreement.
- `git diff --name-only base..HEAD` shows ONLY the 6 allowed files
  (plus `planning/current_plan.md` and `planning/current_plan.critique.md`).
- `git diff --name-only base..HEAD -- <forbidden>` is empty for all forbidden paths.

PM-1 passing this gate does NOT close Step `02_01_01` (N > 1 increments remain).

# §17 Allowed future files

Only these 6 files may be written in this PR:
1. `planning/current_plan.md`
2. `planning/current_plan.critique.md`
3. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.py`
4. `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_registry_section10_verdict_audit.ipynb`
5. `src/rts_predict/games/sc2/datasets/sc2egset/validate_registry_section10_verdicts.py`
6. `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_registry_section10_verdicts.py`

A `conftest.py` update is permitted ONLY if the existing `tests/rts_predict/games/sc2/datasets/sc2egset/conftest.py` requires a new fixture for the new tests; if no new fixture is needed, no conftest change is made.

# §18 Forbidden files / actions

Zero diff allowed on:
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/STEP_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PHASE_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/**`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/PIPELINE_SECTION_STATUS.yaml`
- `src/rts_predict/games/sc2/datasets/sc2egset/reports/INVARIANTS.md`
- `reports/research_log.md`
- `reports/specs/**`
- `thesis/**`
- `data/**`
- `notebooks/**`
- `pyproject.toml`
- `CHANGELOG.md`
- Any other file not in §17.

Additional boundary disclaimers:
- PM-1 does NOT close Step `02_01_01`.
- PM-1 does NOT flip STEP_STATUS or PHASE_STATUS.
- PM-1 does NOT write any artifact to `reports/artifacts/`.
- PM-1 does NOT update `research_log.md` (mandatory Cat-A update explicitly deferred by user for this PR).

# §19 Reviewer routing for later turns

After this PR merges:
- Reviewer-deep: check structural correctness, spec compliance, invariant tracing
  for the validator and tests.
- Reviewer-adversarial: required for any subsequent increment that changes
  methodology or adds new §10 derivation logic.
- No reviewer invocation is needed from within this PR's execution turn.

# §20 Open questions / blockers

OQ-1: RESOLVED. The registry CSV is confirmed 26 rows / 14 columns / unique IDs
(verified in T01 read in the execution session).

OQ-2: RESOLVED. PM-1 does not require a ROADMAP amendment. Justification
(all nine required statements):

1. `continue_predicate` clause-2 ("CROSS-02-01-v1.0.1 post-materialization
   audit ... for any feature column the registry triggers materialization of")
   is conditional on materialization occurring.

2. "Materialization" is defined at `02_01_leakage_audit_protocol.md:117-121`
   as persisting a feature column to DuckDB (as a VIEW or materialized table)
   or to Parquet file format consumed by the training pipeline.

3. The registry CSV persists zero feature columns (`ROADMAP.md:1924`);
   therefore the clause-2 column set is EMPTY.

4. An EMPTY column set vacuously satisfies the clause-2 post-materialization
   audit condition.

5. Clause-3 (`02_03_temporal_feature_audit_protocol.md` §10) is a design-time
   gate decoupled from materialization (§1.1 lines 34-39; §10.1 lines 444-447).

6. PM-1 is a clause-3 increment, not a clause-2 "pre-materialization" increment.

7. PM-1 does NOT amend the ROADMAP (forbidden in §18).

8. PM-1 does NOT close Step `02_01_01`.

9. PM-1 does NOT update STEP_STATUS, PHASE_STATUS, or research_log.

No blockers remain after this planner revision; execution still requires explicit user approval in a later turn.
