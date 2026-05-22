---
category: A
branch: feat/sc2egset-02-01-02-pre-game-materialization-scaffold
base_ref: 3cda752813659490e4992df78ecb10a72b8f010c
date: 2026-05-22
planner_model: claude-opus-4-7[1m]
dataset: sc2egset
phase: "02"
pipeline_section: "02_01 — Pre-Game vs In-Game Boundary"
step: "02_01_02"
non_batching_sequence_position: "step 2 of 9 — notebook scaffold + one validation module"
critique_required_before_execution: true
critique_reviewer: reviewer-adversarial
gate_reviewer: "reviewer-adversarial (Category A pre-execution gate) — APPROVE-WITH-NITS, zero blockers"
chat_second_pass_required_before_materialization: true
planning_pr: "PR #233"
source_artifacts:
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_feature_family_registry.md
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.csv
  - src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/02_01_01/leakage_audit_sc2egset.json
  - reports/specs/02_00_feature_input_contract.md
  - reports/specs/02_01_leakage_audit_protocol.md
  - reports/specs/02_02_feature_engineering_plan.md
  - reports/specs/02_03_temporal_feature_audit_protocol.md
  - .claude/rules/data-analysis-lineage.md
  - .claude/scientific-invariants.md
  - .claude/ml-protocol.md
---

# Plan — SC2EGSet Step 02_01_02 scaffold + one validation module (Category A)

## Scope

This is a Category A — Phase work planning unit. Phase 02 (Feature Engineering)
→ Pipeline Section 02_01 (Pre-Game vs In-Game Boundary) → Step 02_01_02 (first
pre_game feature-family materialization, sc2egset). Predecessors: 02_01_01
(complete). Branch `feat/sc2egset-02-01-02-pre-game-materialization-scaffold`.
Base master @ 3cda7528 (pyproject 3.67.0). Thesis mapping: Chapter 4 §4.5
(provisional; no empirical leakage-clearance claim enabled).

This is **non-batching sequence step 2 of 9** per
`.claude/rules/data-analysis-lineage.md` — *notebook scaffold + ONE validation
module*. Step 1 (ROADMAP stub) = PR #232. Materialization (steps 3-9: feature
table + post-materialization CROSS-02-01 audit) is a SEPARATE future PR.

Delivered in two layers:

- **LAYER 1 (materialized THIS turn, after the reviewer-adversarial gate):**
  commits ONLY `planning/current_plan.md` + `planning/current_plan.critique.md`;
  opens a DRAFT planning PR. After PR creation, the placeholder for this PR's
  number is replaced with the literal PR number in both planning files and the
  PR body within the same turn.
- **LAYER 2 (the FUTURE scaffold-execution PR this plan DESCRIBES; separate
  approved turn; runs on THIS SAME branch / PR — the future-execution PR is
  `PR #233`, i.e. this planning PR carried forward):** creates/edits the 9
  files in the File Manifest and NOTHING else. NO feature materialization, NO
  artifact, NO status YAML, NO research_log, NO ROADMAP edit, NO Phase 03.

The scaffold notebook EXECUTES its one validation module against the closed
02_01_01 registry CSV but **persists NO artifact** (non-batching step 2 =
scaffold + validation module; step 3 = execute and report; CROSS-02-02-v1.0.1
§12.1 line 539: the sc2egset first validation module is the `is_mmr_missing`
flag and "No feature table is produced"). The validator asserts the scaffold's
DESIGN contract against the registry CSV; it does NOT run projection SQL or read
feature data. Optional read-only DuckDB column-existence print only; FORBIDDEN
any `CREATE`/`INSERT`/`COPY`/`to_parquet`/feature SELECT to disk.

## Problem Statement

PR #232 merged the Step 02_01_02 ROADMAP stub (non-batching step 1), which
DEFERS the notebook scaffold, validation module, materialization, and the
post-materialization CROSS-02-01 audit to "SEPARATE FUTURE PRs (sequence steps
2-9)" and HALTS if a future PR batches ROADMAP + notebook + artifact + next
step. The literal-next atomic unit is therefore step 2: scaffold the 02_01_02
notebook + ONE validation module for the 5 allowed pre_game families, with NO
feature value materialized. The closed 02_01_01 leakage audit is vacuous
(features_audited=[]) by design; it becomes non-vacuous only when a future PR
materializes the feature table — which is gated behind a mandatory Claude Chat
second-pass leakage review (this plan does not enable any leakage-clearance
claim).

## Assumptions & Unknowns

- **Assumption (scope):** the 5 tranche-1 families are exactly the closed
  registry CSV's pre_game rows — `focal_race_with_opponent_race_pair`,
  `map_type_encoded`, `patch_version_encoded`, `matchup_encoded`,
  `is_mmr_missing_flag` — all `status=allowed`, `candidate_leakage_modes=none`,
  `cold_start_handling=G-CS-1`, `allowed_cutoff_rule=snapshot_at_match_start`,
  `per_player_construction=symmetric`. The 6 history_enriched_pre_game and 11
  in_game_snapshot families are DEFERRED to 02_01_03+.
- **Assumption (cutoff):** `snapshot_at_match_start` reads the TARGET match's
  OWN game-T static pre-game metadata — NO `history_time < target_time` filter
  applies (that strict-`<` window is for the deferred history tranche).
  `temporal_anchor=details_timeUTC` here is the row-identity timestamp, not a
  window bound. Leak-freedom rests on: game-T pre-game columns only + POST-GAME
  token absence (CROSS-02-01 §2.2) + non-tracker source (Invariant I3).
- **Assumption (encoders):** encoders are SPECIFIED in the scaffold, NOT FIT;
  any future fit is train-fold-only (Invariant I3 normalization-leakage).
- **Assumption (version):** future scaffold-execution PR bumps 3.67.0 → 3.68.0
  (minor; Category A feat branch); the Layer-1 planning PR does NOT bump.
- **Unknown (deferred to the mandatory second-pass):** the registry CSV binds
  the sources to `replay_players_raw`/`matches_flat` (raw/flat layer) while
  CROSS-02-02 §6.1 names view-level sources (`matches_history_minimal.faction`,
  `player_history_all.*`); and the temporal anchor is `details_timeUTC` (raw)
  vs `started_at` (harmonized view). These are ONE coupled view-vs-raw decision
  resolved at the future second-pass, NOT here. The scaffold binds to the closed
  registry CSV (authoritative catalog) and records the divergence.

## Literature Context

This unit is a notebook scaffold + one structural validation module — it
introduces no new empirical or literature claim. Governing repo sources:
`.claude/scientific-invariants.md` (I3 strict temporal `match_time < T`; I5
symmetric player treatment; I6 report-with-code; I7 no magic numbers; I8 shared
cross-game pre-game categories; I9 pipeline discipline; I10 relative-path
provenance); `.claude/ml-protocol.md` (the three leakage failure modes); the
four LOCKED Phase-02 specs (CROSS-02-00-v3.0.1 input contract §3.1/§3.2,
CROSS-02-01-v1.0.1 leakage-audit protocol §2.1/§2.2/§2.3, CROSS-02-02-v1.0.1
feature plan §6.1/§9/§12.1, CROSS-02-03-v1.0.1 temporal-audit protocol §6.1/D5/
D7); `.claude/rules/data-analysis-lineage.md` (non-batching sequence,
feature-engineering discipline, temporal-leakage discipline, SC2 tracker-event
discipline). [OPINION] The minimal-first-tranche choice is grounded in the
registry CSV's own per-row leakage-mode/cold-start columns, not an external
benchmark.

## Execution Steps

> All tasks below are for the FUTURE Layer-2 scaffold-execution PR, on this same
> branch, after this plan is approved on the draft PR and an explicit execution
> turn begins. The scaffold creates NO artifact, materializes NO feature value,
> and flips NO status YAML.

### T01 — Notebook scaffold + banner

Create the jupytext pair
`sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.{py,ipynb}`.
The notebook DESIGNS the projection (markdown + module docstring, NOT executed
against feature data) and RUNS the one validation module (T02), printing the
result dataclass.

Exact first-markdown-cell banner (verbatim):
> # Step 02_01_02 — First pre_game feature-family materialization: sc2egset
>
> **SCAFFOLD + ONE VALIDATION MODULE (non-batching sequence step 2 of 9).**
> This notebook DESIGNS the pre_game projection and RUNS one validation module
> against the closed 02_01_01 registry CSV. It is NOT materialization.
>
> **This PR does NOT:** materialize any feature value · write any artifact
> (Parquet / CSV / JSON / MD) · flip STEP_STATUS / PIPELINE_SECTION_STATUS /
> PHASE_STATUS · write a research_log entry · edit the ROADMAP · start Step
> 02_01_03 · start Phase 03 · close Step 02_01_02.
>
> **Leakage status:** the CROSS-02-01-v1.0.1 post-materialization leakage audit
> is NOT run here and remains FUTURE. The 02_01_01 leakage audit is vacuous
> (features_audited=[]) by design; it becomes non-vacuous only when a future PR
> materializes the feature table. This scaffold designs the projection; it does
> NOT clear leakage.
>
> **Phase:** 02 · **Pipeline Section:** 02_01 · **Step:** 02_01_02 (scaffold
> increment 1 of N) · **Dataset:** sc2egset · **Predecessors:** 02_01_01 (closed).

Notebook hard rules (sandbox/README.md): no `def`/`class`/lambda in cells (logic
imported); cells ≤ 50 lines; `print()` for exploration, logger for diagnostics;
NO plan codes (R01/T01/V1) in any cell or docstring (use descriptive prose);
seed 42 referenced. Cell order: banner → context/inputs (paths to the closed
registry CSV, §10 verdict CSV, CROSS-02-01 json) → 5-family tranche design table
→ per-family projection SQL design (markdown, NOT executed) → import + run the
validation module → print result → closing "what was NOT measured / nothing
persisted / no status flipped" cell.

### T02 — One validation module

`src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py`.
Conventions match the existing `validate_registry_skeleton.py` /
`validate_registry_section10_verdicts.py`: `from __future__ import annotations`;
`logging.getLogger(__name__)`; no `print`; frozen dataclasses; ONE public
`validate_*` entrypoint; private `_check_*` helpers; module-level UPPER_SNAKE
constants (no magic numbers — Invariant I7); reads the registry CSV from a
supplied Path only.

Module-level constants:
```python
TRANCHE1_PRE_GAME_FAMILY_IDS: frozenset[str] = frozenset({
    "sc2egset.pre_game.focal_race_with_opponent_race_pair",
    "sc2egset.pre_game.map_type_encoded",
    "sc2egset.pre_game.patch_version_encoded",
    "sc2egset.pre_game.matchup_encoded",
    "sc2egset.pre_game.is_mmr_missing_flag",
})
EXPECTED_TRANCHE1_COUNT: int = 5
PRE_GAME_PREDICTION_SETTING: str = "pre_game"
SNAPSHOT_CUTOFF_RULE: str = "snapshot_at_match_start"
NO_LEAKAGE_MODE: str = "none"
PRE_GAME_COLD_START_GATE: str = "G-CS-1"
EXPECTED_PER_PLAYER_CONSTRUCTION: str = "symmetric"
# Source tables AUTHORITATIVE per the CLOSED 02_01_01 registry CSV.
ALLOWED_PRE_GAME_SOURCE_TABLES: frozenset[str] = frozenset({
    "replay_players_raw",   # race-pair, matchup, mmr-missing
    "matches_flat",         # map_type, patch_version
})
# is_mmr_missing is a MISSINGNESS/PROVENANCE flag, NOT a skill feature
# (CROSS-02-02 §6.1 line 228: "Use the missingness flag, not the MMR scalar").
IS_MMR_MISSING_FAMILY_ID: str = "sc2egset.pre_game.is_mmr_missing_flag"
# Matching rule (see _is_forbidden_skill_column): a candidate name is lowercased
# and split on "_" into its underscore-delimited token set; it is ALLOWED if it
# is in APPROVED_MMR_MISSINGNESS_TOKENS, otherwise it is REJECTED iff any
# FORBIDDEN_SKILL_TOKENS member equals one of its tokens (boundary-aware token
# equality — NEVER substring containment, so "mu"/"sigma" reject only as
# standalone tokens, never inside words like "cumulative"/"summary").
APPROVED_MMR_MISSINGNESS_TOKENS: frozenset[str] = frozenset({
    "is_mmr_missing",
    "is_mmr_missing_flag",
    "focal_is_mmr_missing",
    "opponent_is_mmr_missing",
})
FORBIDDEN_SKILL_TOKENS: frozenset[str] = frozenset({
    "mmr", "rating", "elo", "glicko", "skill", "mu", "sigma",
})
TRUE_REGISTRY_CSV_RELPATH: str = (
    "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_01_feature_family_registry.csv"
)
STALE_REGISTRY_FILENAME_FRAGMENT: str = "02_01_01_feature_family_registry_sc2egset.csv"
TRACKER_SOURCE_PREFIX: str = "tracker_events_raw"
HISTORY_PREDICTION_SETTING: str = "history_enriched_pre_game"
IN_GAME_PREDICTION_SETTING: str = "in_game_snapshot"
POST_GAME_TOKENS: tuple[str, ...] = (
    "won", "win", "loss", "result", "final_state", "match_result",
    "post_game", "outcome", "winner", "is_decisive",
)
```

Frozen dataclasses:
```python
@dataclass(frozen=True)
class PreGameTrancheRow:
    feature_family_id: str
    prediction_setting: str          # must == "pre_game"
    source_table_or_event_family: str
    allowed_cutoff_rule: str         # must == "snapshot_at_match_start"
    candidate_leakage_modes: str     # must == "none"
    cold_start_handling: str         # must == "G-CS-1"
    per_player_construction: str     # must == "symmetric"
    status: str                      # must == "allowed"

@dataclass(frozen=True)
class PreGameScaffoldValidationResult:
    passed: bool
    tranche_family_ids: tuple[str, ...]
    tranche_count: int
    extra_families_in_tranche: tuple[str, ...]
    is_mmr_missing_classified_as_flag: bool
    tracker_in_pre_game: tuple[str, ...]
    history_families_in_tranche: tuple[str, ...]
    in_game_families_in_tranche: tuple[str, ...]
    asymmetric_construction: tuple[str, ...]
    post_game_token_hits: tuple[tuple[str, str], ...]
    unexpected_source_tables: tuple[str, ...]
    materialized_output_paths: tuple[str, ...]   # ALWAYS () — scaffold persists nothing
    halting_falsifier: str | None
```

Signatures:
```python
def load_pre_game_tranche_rows(registry_csv_path: Path | str) -> list[PreGameTrancheRow]: ...
    # reads only TRANCHE1 rows; RAISES if path resolves to STALE_REGISTRY_FILENAME_FRAGMENT
def _check_tranche_membership(rows, full_registry) -> tuple[tuple[str, ...], tuple[str, ...]]: ...
def _is_forbidden_skill_column(name: str) -> bool: ...
    # Allowlist-first, boundary-aware. Lowercase name; if name in
    # APPROVED_MMR_MISSINGNESS_TOKENS -> False (allowed — approved missingness flag,
    # even though it contains the "mmr" token). Else split on "_" and return True iff
    # any FORBIDDEN_SKILL_TOKENS member EQUALS one of the tokens (token equality, NEVER
    # substring). Allowed: focal_is_mmr_missing, opponent_is_mmr_missing,
    # is_mmr_missing(_flag). Forbidden: mmr, focal_mmr, opponent_mmr, mmr_value, rating,
    # elo, glicko, skill, mu, sigma. No new false positives: cumulative / summary
    # (contain "mu" as a substring, not a token) -> False (allowed). Pure; reads no file.
def _check_is_mmr_missing_is_flag_not_skill(rows) -> bool: ...
    # True iff ALL: (1) IS_MMR_MISSING_FAMILY_ID present in rows; (2) every approved
    # designed flag column (focal_is_mmr_missing, opponent_is_mmr_missing,
    # is_mmr_missing[_flag]) satisfies _is_forbidden_skill_column(...) is False;
    # (3) NO designed column for this family is a forbidden skill-scalar
    # (_is_forbidden_skill_column True) — bare mmr / focal_mmr / opponent_mmr /
    # mmr_value MUST be absent; (4) provenance framing not skill: family_id ends in
    # "is_mmr_missing_flag", prediction_setting=pre_game, candidate_leakage_modes=none.
    # _is_forbidden_skill_column is the SOLE allow/reject source; NO flat `token in name`
    # substring test anywhere in the module.
def _check_no_tracker_in_pre_game(rows) -> tuple[str, ...]: ...
def _check_no_deferred_settings_in_tranche(full_registry) -> tuple[tuple[str, ...], tuple[str, ...]]: ...
def _check_symmetry(rows) -> tuple[str, ...]: ...
def _check_no_post_game_tokens(rows, designed_column_names) -> tuple[tuple[str, str], ...]: ...
def _check_source_tables(rows) -> tuple[str, ...]: ...
def validate_pre_game_feature_materialization(
    registry_csv_path: Path | str,
    designed_column_names: tuple[str, ...],
) -> PreGameScaffoldValidationResult: ...
    # NO materialization; writes nothing; materialized_output_paths always ()
```
`designed_column_names` is the notebook-supplied PLANNED focal_*/opponent_*
column-name tuple, used ONLY for the POST_GAME token-absence check; never read
from a feature table. This keeps the validator pure and the notebook artifact-free.

### T03 — One test file

`tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py`
(mirrored tree; matches `test_validate_registry_section10_verdicts.py` style:
`tmp_path` synthetic CSVs + a real-CSV `skipif` test). Required cases:
1. 5-family tranche membership (exactly the 5 ids).
2. No extra pre_game family included beyond the tranche.
3. **`is_mmr_missing_flag` is a provenance/missingness flag, not a skill estimate**
   — explicit PASS and FAIL cases over `_is_forbidden_skill_column` and
   `_check_is_mmr_missing_is_flag_not_skill`:
   - PASS (allowed missingness flags): `focal_is_mmr_missing`,
     `opponent_is_mmr_missing`, `is_mmr_missing_flag`, `is_mmr_missing` each
     satisfy `_is_forbidden_skill_column(...) is False`; `_check_..._not_skill`
     returns True when the family is present and its designed columns are exactly
     these flag names.
   - FAIL (forbidden skill/rating/MMR-scalar): `focal_mmr`, `opponent_mmr`,
     `mmr_value`, `mmr`, `rating`, `elo`, `glicko`, `skill`, `mu`, `sigma` each
     satisfy `_is_forbidden_skill_column(...) is True`; supplying any as a designed
     column makes `_check_..._not_skill` return False and fires the falsifier.
   - No-new-false-positive guard: innocent names containing a forbidden token's
     letters inside a larger token — e.g. `cumulative`, `summary` — satisfy
     `_is_forbidden_skill_column(...) is False`.
   - FAIL (skill framing in prose/lineage): a design-record/lineage string that
     frames the flag as a skill ESTIMATE (e.g. "skill estimate", "reconstructed
     rating", "mmr scalar" as a feature) rather than provenance/missingness fails
     the provenance-framing assertion.
4. True registry path used; stale `_sc2egset` path raises / is absent in new code.
5. No tracker-derived family in the pre_game tranche.
6. No history_enriched_pre_game family in tranche 1.
7. No in_game_snapshot family in tranche 1.
8. Focal/opponent symmetry (per_player_construction == "symmetric").
9. No POST_GAME token in any designed column name or source field.
10. No materialized output path written (`materialized_output_paths == ()`).
11. Leakage audit remains future / non-vacuous-only-after-materialization
    (the scaffold does not touch `02_01_01/leakage_audit_sc2egset.json`).

### T04 — Projection / SQL design recorded in the notebook (specified, NOT executed)

The design record for the FUTURE materialization PR's second-pass leakage review;
embedded verbatim in the notebook markdown + the validator module docstring;
NONE executed against feature data.

- **Source binding (authoritative = closed registry CSV).** Per-family:
  race-pair / matchup / is_mmr_missing from `replay_players_raw` at
  `(filename, player_id_worldwide)`; map_type / patch_version from `matches_flat`
  at `(filename)`. model_input_grain `(focal_match_id, focal_player)`;
  temporal_anchor `details_timeUTC`; cutoff `snapshot_at_match_start`. The
  view-vs-raw divergence (CROSS-02-02 §6.1 view-level names) is recorded and
  DEFERRED to the second-pass (see Open Questions); the scaffold binds to the
  registry CSV and does not silently pick a layer.
- **Cutoff semantics (`snapshot_at_match_start`).** The 5 families are game-T
  STATIC pre-match attributes (CROSS-02-03 §6.1 line 235; CROSS-02-02 §6.1
  "none (game-T attribute)"). NO `history_time < target_time` filter applies.
  Leak-freedom = game-T pre-game columns only + POST-GAME token absence (§2.2) +
  non-tracker source (I3). The future CROSS-02-01 §2.2 check is SUBSTANTIVE and
  must report 0 over the materialized set.
- **Symmetric focal/opponent (Invariant I5).** Self-join on
  `(filename, player_id_worldwide)` over 1v1 true-match scope; SAME expression
  computes both slots; no privileged slot; the RISK-24 data-dependent
  slot-assignment falsifier (defined in
  `thesis/pass2_evidence/methodology_risk_register.md`, NOT the dataset-level
  `risk_register_sc2egset.csv`; cite the methodology-register path) is
  enumerated. Designed names (illustrative): focal_race, opponent_race,
  race_pair, focal_matchup, opponent_matchup, map_type, patch_version,
  focal_is_mmr_missing, opponent_is_mmr_missing — none contains a POST_GAME token.
- **Per-family derivation.** race-pair/matchup from `replay_players_raw` race
  field (Prot/Terr/Zerg/Rand; Random is a 4th pre-game race; the
  eventually-played race is post-decision and is NOT used — RISK-26). map_type/
  patch_version from `matches_flat` at `(filename)`, broadcast to both slots.
  is_mmr_missing = BOOLEAN missingness/provenance flag over the MMR field; the
  MMR SCALAR is NOT projected (CROSS-02-02 §6.1 line 228: MMR absent for 83.95%
  of rows).
- **Encoders SPECIFIED not FIT.** Categorical encoding of race_pair / matchup /
  map_type / patch_version is specified (encoder type, dataset_tag='sc2egset'
  partition, vocabulary source) but NOT fit; any future fit is train-fold-only
  (Invariant I3).

### T05 — Release tail + final scope verification

`pyproject.toml` 3.67.0 → 3.68.0 (minor); `CHANGELOG.md` `[Unreleased]` →
`[3.68.0] — 2026-05-22 (PR #233: feat/sc2egset-02-01-02-pre-game-materialization-scaffold)`
(Added: validator + tests + notebook scaffold; Notes: zero-materialization, no
status flip, no artifact, leakage audit remains future/vacuous);
`planning/INDEX.md` archive-line update. Final scope check: the tracked diff is
EXACTLY the 9-file File Manifest; no artifact/status YAML/research_log/ROADMAP.

### Falsifiers (the validation module + reviewer enforce; a fired falsifier HALTS and BLOCKS the scaffold PR)

- **F-temporal:** a tranche-1 family reads a value not knowable at
  `snapshot_at_match_start`.
- **F-symmetry:** `per_player_construction != "symmetric"` (Invariant I5).
- **F-tracker:** a pre_game family whose source starts with `tracker_events_raw`
  (Invariant I3).
- **F-history-creep / F-ingame-creep:** a history_enriched_pre_game / in_game_snapshot
  family inside tranche 1.
- **F-postgame-token:** a POST_GAME token in a designed column name or source field.
- **F-mmr-scalar:** a designed column for the `is_mmr_missing` family (or any
  tranche-1 column) is a forbidden skill/rating/MMR-scalar use under
  `_is_forbidden_skill_column` (a `FORBIDDEN_SKILL_TOKENS` member equals a
  standalone underscore token of a name NOT in `APPROVED_MMR_MISSINGNESS_TOKENS`),
  OR the `is_mmr_missing` family is framed in prose/lineage as a skill estimate
  rather than a missingness/provenance flag. Distinct from F-postgame-token; the
  approved missingness flag does NOT fire it. (F-fold-fit and F-source-drift are
  unaffected by this correction.)
- **F-fold-fit:** an encoder/scaler specified as fit on full data / cross-fold /
  cross-dataset (Invariant I3 normalization leakage).
- **F-source-drift:** a tranche-1 source not in `ALLOWED_PRE_GAME_SOURCE_TABLES`,
  OR the stale `02_01_01_feature_family_registry_sc2egset.csv` path used in new code.
- **F-family-set-drift:** tranche-1 family-id set != the 5 in `TRANCHE1_PRE_GAME_FAMILY_IDS`.
- **F-mutation:** the diff touches any STATUS YAML / research_log / ROADMAP / artifact.
- **F-phase03:** any Phase 03 (or 02_01_03) file or content appears.

## File Manifest

| File | Action | Layer |
|------|--------|-------|
| `planning/current_plan.md` | Create (this plan) | 1 (this turn) |
| `planning/current_plan.critique.md` | Create (reviewer-adversarial output) | 1 (this turn) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.py` | Create (notebook scaffold) | 2 (future) |
| `sandbox/sc2/sc2egset/02_feature_engineering/01_pre_game_vs_in_game_boundary/02_01_02_pre_game_feature_materialization.ipynb` | Create (jupytext pair) | 2 (future) |
| `src/rts_predict/games/sc2/datasets/sc2egset/validate_pre_game_feature_materialization.py` | Create (one validation module) | 2 (future) |
| `tests/rts_predict/games/sc2/datasets/sc2egset/test_validate_pre_game_feature_materialization.py` | Create (one test file) | 2 (future) |
| `planning/INDEX.md` | Update (archive line) | 2 (future) |
| `CHANGELOG.md` | Update (`[Unreleased]` → `[3.68.0]`) | 2 (future) |
| `pyproject.toml` | Update (3.67.0 → 3.68.0) | 2 (future) |

Layer-1 tracked diff = the 2 planning files. Layer-2 adds the other 7 files →
final tracked diff = 9 files. NO artifact (Parquet/CSV/JSON/MD), NO status YAML,
NO research_log, NO ROADMAP edit in either layer.

## Gate Condition

The future Layer-2 scaffold-execution PR is mergeable iff ALL hold:
1. The validation module runs and returns `passed=True` (`halting_falsifier is None`).
2. `pytest tests/ -v` green; coverage ≥ 95% (`fail_under=95`); ruff + mypy clean.
3. jupytext `.py`/`.ipynb` pair in sync (jupytext hook); BOTH staged.
4. The final tracked diff matches the File Manifest EXACTLY (9 files); no extra
   file; specifically no artifact, no status YAML, no research_log, no ROADMAP edit.
5. `materialized_output_paths == ()`; NO feature value materialized; the notebook
   persists nothing.
6. `02_01_01/leakage_audit_sc2egset.json` still has `features_audited == []`
   (the scaffold did NOT make it non-vacuous).
7. The reviewer-adversarial critique gate is satisfied (recorded for the LAYER 1
   plan in `planning/current_plan.critique.md`).

## Open Questions

- **RESOLVED (ChatGPT second-pass leakage review, PR #233):** the planned
  `FORBIDDEN_SKILL_TOKENS` check would have false-rejected the approved
  `is_mmr_missing` flag names (`is_mmr_missing_flag`, `focal_is_mmr_missing`,
  `opponent_is_mmr_missing`) because they contain the substring `mmr`. Corrected
  to allowlist-first (`APPROVED_MMR_MISSINGNESS_TOKENS`) + boundary-aware
  token-equality matching (see T02 constants + `_is_forbidden_skill_column`);
  scalar MMR / rating / skill columns remain forbidden/deferred. No scope or
  scientific decision changed — `is_mmr_missing_flag` stays tranche 1.
- **View-vs-raw source + anchor reconciliation (coupled).** The registry CSV
  binds sources to `replay_players_raw`/`matches_flat` and anchor to
  `details_timeUTC` (raw); CROSS-02-02 §6.1 / CROSS-02-00 §5.1 name view-level
  sources and `started_at`. These are ONE coupled decision. — Resolves at the
  MANDATORY future second-pass before any materialization PR; NOT decided here.
- **Mandatory pre-materialization second-pass.** Before any FUTURE
  materialization PR lands, a fresh Claude Chat second-pass leakage review over
  the focal/opponent projection SQL, the `snapshot_at_match_start` cutoff
  semantics, and the view-vs-raw reconciliation is REQUIRED. The scaffold PR's
  reviewer-adversarial gate does NOT discharge it; they are distinct gates over
  distinct artifacts. The future materialization PR also re-runs the
  CROSS-02-01-v1.0.1 post-materialization audit (non-vacuous only at materialization).
- **(reviewer-adversarial nit) Risk-register path.** RISK-24/26/20 live in
  `thesis/pass2_evidence/methodology_risk_register.md`, not the dataset-level
  `risk_register_sc2egset.csv` — the future scaffold notebook must cite the
  methodology-register path.

## Out of Scope

- Materializing any of the 5 pre_game feature columns (future PR).
- The 6 history_enriched_pre_game and 11 in_game_snapshot families (02_01_03+).
- Running the CROSS-02-01-v1.0.1 post-materialization audit / emitting a
  non-vacuous `02_01_02/leakage_audit_sc2egset.{json,md}`.
- Any STEP_STATUS / PIPELINE_SECTION_STATUS / PHASE_STATUS flip; any research_log
  entry; any ROADMAP edit; any manifest edit.
- Phase 03 (and any 02_02..02_08) work; any thesis/bib/appendix/docs/.claude/AoE2 edit.
- Resolving the view-vs-raw source + anchor reconciliation (future second-pass).

## Evidence-distinctness ledger (must remain true post-PR)

- PR #229 §10 design-time verdict audit:
  `.../01_pre_game_vs_in_game_boundary/02_01_01_section10_verdict_audit.{csv,md}`
  — per-family DESIGN-TIME verdicts (26 rows); NOT a leakage clearance.
- PR #230 CROSS-02-01 vacuous audit:
  `.../02_01_01/leakage_audit_sc2egset.{json,md}` — features_audited=[];
  PASS-by-vacuity; NOT a substitute for the post-materialization audit.
- Future 02_01_02 post-materialization CROSS-02-01 audit:
  `.../02_01_02/leakage_audit_sc2egset.{json,md}` — features_audited != [];
  does NOT exist yet; NOT created by the scaffold PR.

These three are DISTINCT; the scaffold PR adds NONE and overclaims NO clearance.

---

**Critique gate (Category A):** The reviewer-adversarial pre-execution gate for
this plan returned APPROVE-WITH-NITS with zero blockers and no required
`current_plan.md` edit; its output is in `planning/current_plan.critique.md`.
The two non-blocking nits (risk-register path; coupling the anchor-column
divergence with the source-layer decision) are Layer-2 / future-PR instructions.
Before any FUTURE materialization PR lands, a fresh Claude Chat second-pass
leakage review over the focal/opponent projection SQL is MANDATORY.
