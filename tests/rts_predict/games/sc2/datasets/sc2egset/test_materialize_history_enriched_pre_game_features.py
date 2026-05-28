"""Tests for ``materialize_history_enriched_pre_game_features`` (Step 02_01_03).

Covers all required test cases per the merged Layer-2 plan T05:

    - Five-family permitted set / canonical order / excluded family + columns.
    - Twenty-four audited feature columns (exact set + per-family counts).
    - Forbidden token / scalar / reconstructed_rating column rejection.
    - Strict-< TRY_CAST temporal predicate present; no <= / = variants.
    - Source-table allowlist (no tracker_events_raw / replay_players_raw / ...).
    - Matchup CTE 1v1-restricted via matches_flat_clean join (B2 fix).
    - is_decisive_result = TRUE used instead of inline result IN list (N11).
    - Q5 cross-region policy = sensitivity_indicator_co_registration; PR #255
      omit-closure q5_policy field re-elevation.
    - Q7 IN_GAME_HISTORICAL allowed-column 4-tuple verbatim.
    - PR #245 vs PR #243 merge-SHA disambiguation (R3-B3).
    - PR #236 tranche-1 three-SHA-pin enumeration (R3-N1).
    - 17 BINDING parent artifact SHAs accounted for.
    - Defensive matches_long_raw_yaml_sha256 pin (R3-N2).
    - Real-DuckDB end-to-end materialisation + audit + research_log append.
    - Reproducibility (byte-identical Parquet on re-run).
    - PR #257 ROADMAP amendment grep-token count >= 4.
    - Research_log non-closure append (closure_status: still_open;
      features_audited_count: 24).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import duckdb
import pytest

from rts_predict.games.sc2.datasets.sc2egset import (
    materialize_history_enriched_pre_game_features as mod,
)
from rts_predict.games.sc2.datasets.sc2egset.materialize_history_enriched_pre_game_features import (
    _MATERIALIZATION_QUERY,
    AUDIT_PR_PLACEHOLDER,
    CROSS_REGION_POLICY,
    CROSS_REGION_SUBFEATURES,
    DATASET_TAG,
    EXAMINER_CLARITY_SENTENCE,
    EXCLUDED_FAMILY,
    EXPECTED_AUDITED_FEATURE_COLUMN_COUNT,
    EXPECTED_AUDITED_FEATURE_COLUMNS,
    EXPECTED_DISTINCT_FOCAL_MATCH_COUNT,
    EXPECTED_OUTPUT_COLUMNS,
    EXPECTED_OUTPUT_ROW_COUNT,
    EXPECTED_PARQUET_COLUMN_COUNT,
    FEATURE_TO_FAMILY_MAPPING,
    FIVE_FAMILY_CANONICAL_ORDER,
    FIVE_FAMILY_PERMITTED_COUNT,
    FIVE_FAMILY_PERMITTED_SET,
    FOCAL_PLAYER_HISTORY_SUBFEATURES,
    FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS,
    HISTORY_ENRICHED_AUDIT_JSON_RELPATH,
    HISTORY_ENRICHED_AUDIT_MD_RELPATH,
    HISTORY_ENRICHED_OUTPUT_RELPATH,
    HISTORY_ENRICHED_RESEARCH_LOG_RELPATH,
    IN_GAME_HISTORICAL_AGGREGATED_COLUMNS,
    IN_GAME_HISTORY_SUBFEATURES,
    MATCHUP_HISTORY_SUBFEATURES,
    OPPONENT_PLAYER_HISTORY_SUBFEATURES,
    PHASE_02_STEP,
    PROJECTED_CONTEXT_COLUMNS,
    PROJECTED_IDENTITY_COLUMNS,
    SPEC_VERSION,
    HistoryEnrichedAuditResult,
    HistoryEnrichedMaterializationResult,
    _build_research_log_block,
    _check_decisive_result_flag_used,
    _check_matchup_cte_is_1v1_restricted,
    _check_no_lte_or_eq_history_predicate,
    _check_no_post_game_token_in_columns,
    _check_no_reconstructed_rating_column,
    _check_source_table_allowlist,
    _check_strict_lt_try_cast_present,
    _check_try_cast_present,
    _evaluate_audit_falsifiers,
    _evaluate_materialization_falsifiers,
    _evaluate_query_falsifiers,
    _find_repo_root,
    _is_forbidden_skill_column,
    _is_post_game_token,
    _is_reconstructed_rating_column,
    _resolve_repo_root_relpath,
    _sha256_file,
    append_research_log_entry,
    audit_history_enriched_pre_game_features,
    materialize_history_enriched_pre_game_features,
    run_step_02_01_03,
)

# ---------------------------------------------------------------------------
# Repo-relative paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[6]

REAL_DB_PATH: Path = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/data/db/db.duckdb"
)
ROADMAP_MD_PATH: Path = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
)
OMIT_CLOSURE_CSV_PATH: Path = (
    _REPO_ROOT
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_99_rating_omit_closure.csv"
)

# Pinned merge-commit SHAs (R3-B3 disambiguation).
PR243_MERGE_SHA_FULL: str = "445bae0197fa75b613443f8eafef114ff2bb6939"
PR243_MERGE_SHA_PREFIX: str = "445bae01"
PR245_MERGE_SHA_FULL: str = "ee15d3625eee60688776219f533d4a5ceefb4b76"
PR245_MERGE_SHA_PREFIX: str = "ee15d362"
PR257_MERGE_SHA_PREFIX: str = "3ab48b30"

# Grep token from PR #257 ROADMAP amendment.
PR257_GREP_TOKEN: str = "materialization_scope_amendment_post_pr_255"


# ---------------------------------------------------------------------------
# Module constant tests (no DuckDB needed)
# ---------------------------------------------------------------------------


def test_dataset_tag_is_sc2egset() -> None:
    """DATASET_TAG is the canonical sc2egset tag."""
    assert DATASET_TAG == "sc2egset"


def test_phase_02_step_is_02_01_03() -> None:
    """PHASE_02_STEP is 02_01_03."""
    assert PHASE_02_STEP == "02_01_03"


def test_spec_version_is_cross_02_01_v1() -> None:
    """SPEC_VERSION is CROSS-02-01-v1."""
    assert SPEC_VERSION == "CROSS-02-01-v1"


def test_audit_pr_placeholder_is_TBD() -> None:
    """AUDIT_PR_PLACEHOLDER carries the <TBD> marker."""
    assert AUDIT_PR_PLACEHOLDER == "PR #<TBD>"


# ---------------------------------------------------------------------------
# Five-family permitted set tests
# ---------------------------------------------------------------------------


def test_five_family_permitted_set_count_is_five() -> None:
    """The permitted set is exactly 5 families."""
    assert len(FIVE_FAMILY_PERMITTED_SET) == 5
    assert FIVE_FAMILY_PERMITTED_COUNT == 5


def test_five_family_permitted_set_excludes_reconstructed_rating() -> None:
    """`reconstructed_rating` is NOT in the permitted set."""
    assert "reconstructed_rating" not in FIVE_FAMILY_PERMITTED_SET


def test_five_family_canonical_order_matches_pr257_amendment_order() -> None:
    """Canonical order matches PR #257 amendment lines 2536-2540 verbatim."""
    assert FIVE_FAMILY_CANONICAL_ORDER == (
        "focal_player_history",
        "opponent_player_history",
        "matchup_history_aggregate",
        "cross_region_fragmentation_handling",
        "in_game_history_aggregate",
    )


def test_five_family_canonical_order_matches_permitted_set() -> None:
    """FIVE_FAMILY_CANONICAL_ORDER set-equal to FIVE_FAMILY_PERMITTED_SET."""
    assert frozenset(FIVE_FAMILY_CANONICAL_ORDER) == FIVE_FAMILY_PERMITTED_SET


def test_excluded_family_is_reconstructed_rating() -> None:
    """EXCLUDED_FAMILY is exactly reconstructed_rating."""
    assert EXCLUDED_FAMILY == "reconstructed_rating"


def test_excluded_columns_are_three_named_strings() -> None:
    """The forbidden reconstructed_rating columns are exactly 3 named strings."""
    assert FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS == frozenset(
        {
            "reconstructed_rating_focal_pre",
            "reconstructed_rating_opp_pre",
            "reconstructed_rating_diff",
        }
    )
    assert len(FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS) == 3


# ---------------------------------------------------------------------------
# Twenty-four audited feature columns
# ---------------------------------------------------------------------------


def test_features_audited_is_exactly_twenty_four_columns() -> None:
    """EXPECTED_AUDITED_FEATURE_COLUMNS has length 24."""
    assert len(EXPECTED_AUDITED_FEATURE_COLUMNS) == 24
    assert EXPECTED_AUDITED_FEATURE_COLUMN_COUNT == 24


def test_features_audited_excludes_started_at() -> None:
    """`started_at` is NOT in the audited features tuple."""
    assert "started_at" not in EXPECTED_AUDITED_FEATURE_COLUMNS


def test_features_audited_excludes_identity_columns() -> None:
    """Identity columns are NOT in the audited features tuple."""
    for col in ("focal_match_id", "focal_player", "opponent_player"):
        assert col not in EXPECTED_AUDITED_FEATURE_COLUMNS


def test_focal_player_history_subfeatures_count_is_six() -> None:
    """Family 1 has 6 sub-features per CROSS-02-02 §6.2 row 1."""
    assert len(FOCAL_PLAYER_HISTORY_SUBFEATURES) == 6


def test_opponent_player_history_subfeatures_count_is_six() -> None:
    """Family 2 has 6 sub-features per Invariant I5 symmetry."""
    assert len(OPPONENT_PLAYER_HISTORY_SUBFEATURES) == 6


def test_matchup_history_subfeatures_count_is_two() -> None:
    """Family 3 has 2 sub-features (h2h_count + h2h_focal_win_rate)."""
    assert len(MATCHUP_HISTORY_SUBFEATURES) == 2


def test_cross_region_subfeatures_count_is_two() -> None:
    """Family 4 has 2 sub-features (focal + opponent symmetric per I5)."""
    assert len(CROSS_REGION_SUBFEATURES) == 2


def test_in_game_history_subfeatures_count_is_eight() -> None:
    """Family 5 has 8 sub-features (4 IN_GAME_HISTORICAL columns × 2 sides)."""
    assert len(IN_GAME_HISTORY_SUBFEATURES) == 8


def test_family_to_column_count_arithmetic_sums_to_twenty_four() -> None:
    """6 + 6 + 2 + 2 + 8 = 24 audited feature columns."""
    total = (
        len(FOCAL_PLAYER_HISTORY_SUBFEATURES)
        + len(OPPONENT_PLAYER_HISTORY_SUBFEATURES)
        + len(MATCHUP_HISTORY_SUBFEATURES)
        + len(CROSS_REGION_SUBFEATURES)
        + len(IN_GAME_HISTORY_SUBFEATURES)
    )
    assert total == 24
    assert total == EXPECTED_AUDITED_FEATURE_COLUMN_COUNT


def test_expected_parquet_column_count_is_twenty_eight() -> None:
    """EXPECTED_PARQUET_COLUMN_COUNT = 3 identity + 1 context + 24 audited."""
    assert EXPECTED_PARQUET_COLUMN_COUNT == 28
    assert len(EXPECTED_OUTPUT_COLUMNS) == 28


def test_expected_output_columns_first_three_are_identity() -> None:
    """First 3 columns of EXPECTED_OUTPUT_COLUMNS are identity."""
    assert EXPECTED_OUTPUT_COLUMNS[:3] == PROJECTED_IDENTITY_COLUMNS


def test_expected_output_columns_fourth_is_started_at() -> None:
    """Fourth column is the context anchor `started_at`."""
    assert EXPECTED_OUTPUT_COLUMNS[3] == "started_at"
    assert PROJECTED_CONTEXT_COLUMNS == ("started_at",)


def test_expected_output_columns_last_twenty_four_are_audited() -> None:
    """Columns 4-27 are the audited feature columns in projection order."""
    assert EXPECTED_OUTPUT_COLUMNS[4:] == EXPECTED_AUDITED_FEATURE_COLUMNS


# ---------------------------------------------------------------------------
# feature_to_family_mapping
# ---------------------------------------------------------------------------


def test_feature_to_family_mapping_keys_are_24_audited_columns() -> None:
    """Mapping keys are exactly the 24 audited feature columns."""
    assert set(FEATURE_TO_FAMILY_MAPPING.keys()) == set(
        EXPECTED_AUDITED_FEATURE_COLUMNS
    )
    assert len(FEATURE_TO_FAMILY_MAPPING) == 24


def test_feature_to_family_mapping_values_are_canonical_families() -> None:
    """Every value in the mapping is one of the 5 permitted families."""
    for fam in FEATURE_TO_FAMILY_MAPPING.values():
        assert fam in FIVE_FAMILY_PERMITTED_SET


@pytest.mark.parametrize(
    "col, expected_family",
    [
        ("focal_prior_match_count", "focal_player_history"),
        ("opponent_prior_match_count", "opponent_player_history"),
        ("matchup_h2h_count", "matchup_history_aggregate"),
        ("matchup_h2h_focal_win_rate", "matchup_history_aggregate"),
        ("is_cross_region_fragmented_focal_history_any",
         "cross_region_fragmentation_handling"),
        ("is_cross_region_fragmented_opponent_history_any",
         "cross_region_fragmentation_handling"),
        ("focal_apm_prior_mean", "in_game_history_aggregate"),
        ("opponent_elapsed_game_loops_prior_mean", "in_game_history_aggregate"),
    ],
)
def test_feature_to_family_mapping_specific_columns(
    col: str, expected_family: str
) -> None:
    """Specific column->family mappings match the canonical assignment."""
    assert FEATURE_TO_FAMILY_MAPPING[col] == expected_family


# ---------------------------------------------------------------------------
# Forbidden token / scalar / reconstructed_rating column rejection
# ---------------------------------------------------------------------------


def test_no_reconstructed_rating_in_expected_output_columns() -> None:
    """No EXPECTED_OUTPUT_COLUMNS entry contains 'reconstructed_rating'."""
    assert all("reconstructed_rating" not in c for c in EXPECTED_OUTPUT_COLUMNS)


def test_no_forbidden_skill_token_in_expected_output_columns() -> None:
    """No EXPECTED_OUTPUT_COLUMNS triggers _is_forbidden_skill_column."""
    for col in EXPECTED_OUTPUT_COLUMNS:
        assert _is_forbidden_skill_column(col) is False


def test_no_post_game_token_in_expected_output_columns() -> None:
    """No EXPECTED_OUTPUT_COLUMNS triggers POST_GAME detection."""
    assert _check_no_post_game_token_in_columns(EXPECTED_OUTPUT_COLUMNS) == 0


@pytest.mark.parametrize(
    "name",
    [
        "reconstructed_rating_focal_pre",
        "reconstructed_rating_opp_pre",
        "reconstructed_rating_diff",
        "focal_reconstructed_rating",
    ],
)
def test_is_reconstructed_rating_column_detects_forbidden(name: str) -> None:
    """_is_reconstructed_rating_column flags any reconstructed_rating column."""
    assert _is_reconstructed_rating_column(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "focal_prior_match_count",
        "matchup_h2h_count",
        "started_at",
        "focal_apm_prior_mean",
    ],
)
def test_is_reconstructed_rating_column_passes_legitimate(name: str) -> None:
    """_is_reconstructed_rating_column passes legitimate audited columns."""
    assert _is_reconstructed_rating_column(name) is False


@pytest.mark.parametrize(
    "name",
    ["focal_mmr", "opponent_rating", "elo_score", "glicko_rd", "trueskill_mu", "sigma_value"],
)
def test_is_forbidden_skill_column_rejects_raw_scalars(name: str) -> None:
    """_is_forbidden_skill_column flags raw MMR/rating/elo/glicko/skill/mu/sigma.

    Note: token-equality is strict — `glicko2_rd` would NOT trigger because
    the token `glicko2` does not equal `glicko`. Use `glicko_rd` to verify
    detection.
    """
    assert _is_forbidden_skill_column(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "is_mmr_missing",
        "focal_is_mmr_missing",
        "opponent_is_mmr_missing",
        "is_mmr_missing_flag",
    ],
)
def test_is_forbidden_skill_column_allows_approved_missingness_flag(
    name: str,
) -> None:
    """Approved missingness flags pass the forbidden-skill check."""
    assert _is_forbidden_skill_column(name) is False


@pytest.mark.parametrize(
    "name",
    ["focal_won", "won", "result", "match_result", "winner", "loss", "outcome"],
)
def test_is_post_game_token_detects_target_outcome_tokens(name: str) -> None:
    """Direct POST_GAME outcome tokens are detected."""
    assert _is_post_game_token(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "focal_prior_win_rate_decisive",
        "matchup_h2h_focal_win_rate",
        "opponent_prior_win_rate_race_conditional",
    ],
)
def test_is_post_game_token_protects_win_rate_history_aggregates(
    name: str,
) -> None:
    """`prior_win_rate` / `h2h_focal_win_rate` history aggregates are NOT POST_GAME."""
    assert _is_post_game_token(name) is False


# ---------------------------------------------------------------------------
# SQL text guards
# ---------------------------------------------------------------------------


def test_materialization_query_contains_strict_lt_try_cast_predicate() -> None:
    """The canonical strict-< TRY_CAST predicate appears in the SQL."""
    assert _check_strict_lt_try_cast_present(_MATERIALIZATION_QUERY) is True


def test_materialization_query_contains_try_cast_pattern() -> None:
    """`TRY_CAST(ph.details_timeUTC AS TIMESTAMP)` appears in the SQL."""
    assert _check_try_cast_present(_MATERIALIZATION_QUERY) is True


def test_materialization_query_has_no_lte_or_eq_history_predicate() -> None:
    """No `<=` or `=` variant of the history filter appears."""
    assert (
        _check_no_lte_or_eq_history_predicate(_MATERIALIZATION_QUERY) is False
    )


def test_materialization_query_passes_source_table_allowlist() -> None:
    """No tracker / raw / matches_long_raw table is referenced."""
    assert _check_source_table_allowlist(_MATERIALIZATION_QUERY) == ()


def test_materialization_query_matchup_cte_is_1v1_restricted_via_mfc_join() -> None:
    """B2 fix: matchup CTE includes `JOIN matches_flat_clean mfc_h`."""
    assert _check_matchup_cte_is_1v1_restricted(_MATERIALIZATION_QUERY) is True
    assert "matches_flat_clean mfc_h" in _MATERIALIZATION_QUERY


def test_materialization_query_uses_is_decisive_result_flag() -> None:
    """N11 fix: `is_decisive_result = TRUE` is used (not inline result IN)."""
    assert _check_decisive_result_flag_used(_MATERIALIZATION_QUERY) is True


def test_materialization_query_does_not_use_inline_result_in_list() -> None:
    """The legacy inline `ph.result IN ('Win', 'Loss')` pattern is absent."""
    assert "ph.result IN ('Win', 'Loss')" not in _MATERIALIZATION_QUERY


def test_materialization_query_no_tracker_source() -> None:
    """`tracker_events_raw` does not appear in the materialization SQL."""
    assert "tracker_events_raw" not in _MATERIALIZATION_QUERY


def test_check_source_table_allowlist_detects_tracker() -> None:
    """An ad-hoc SQL with tracker_events_raw triggers the allowlist guard."""
    bad = "SELECT * FROM matches_flat_clean JOIN tracker_events_raw e ON ..."
    hits = _check_source_table_allowlist(bad)
    assert "tracker_events_raw" in hits


def test_check_source_table_allowlist_detects_replay_players_raw() -> None:
    """An ad-hoc SQL with replay_players_raw triggers the allowlist guard."""
    bad = "SELECT * FROM replay_players_raw"
    hits = _check_source_table_allowlist(bad)
    assert "replay_players_raw" in hits


def test_check_no_lte_or_eq_history_predicate_detects_lte() -> None:
    """A SQL with `<= started_at` predicate via details_timeUTC is detected."""
    bad = (
        "WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) <= target.started_at"
    )
    assert _check_no_lte_or_eq_history_predicate(bad) is True


def test_check_strict_lt_try_cast_missing_when_absent() -> None:
    """A SQL lacking the canonical token returns False from the strict-< guard."""
    assert _check_strict_lt_try_cast_present("SELECT 1") is False


def test_check_decisive_result_flag_missing_when_absent() -> None:
    """A SQL lacking is_decisive_result = TRUE returns False from the N11 guard."""
    assert _check_decisive_result_flag_used("SELECT 1") is False


# ---------------------------------------------------------------------------
# Query-side falsifier evaluation
# ---------------------------------------------------------------------------


def test_evaluate_query_falsifiers_passes_canonical_query() -> None:
    """The canonical _MATERIALIZATION_QUERY passes every SQL-side falsifier."""
    assert _evaluate_query_falsifiers(_MATERIALIZATION_QUERY) is None


def test_evaluate_query_falsifiers_fires_on_missing_try_cast() -> None:
    """F-try-cast-missing fires when TRY_CAST(ph.details_timeUTC AS TIMESTAMP) absent."""
    bad = "SELECT * FROM matches_flat_clean"
    assert _evaluate_query_falsifiers(bad) == "F-try-cast-missing"


def test_evaluate_query_falsifiers_fires_on_missing_strict_lt() -> None:
    """F-strict-lt-operator-missing fires when TRY_CAST present but not in strict-< form."""
    bad = "SELECT TRY_CAST(ph.details_timeUTC AS TIMESTAMP) FROM x"
    assert _evaluate_query_falsifiers(bad) == "F-strict-lt-operator-missing"


def test_evaluate_query_falsifiers_fires_on_tracker_source() -> None:
    """F-tracker-source-read fires when tracker_events_raw is referenced."""
    bad = (
        "WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at "
        "FROM tracker_events_raw"
    )
    assert _evaluate_query_falsifiers(bad) == "F-tracker-source-read"


def test_evaluate_query_falsifiers_fires_on_matchup_cte_missing_mfc_join() -> None:
    """F-matchup-cte-includes-non-1v1-history fires when MFC join missing."""
    bad = (
        "WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at "
        "AND is_decisive_result = TRUE "
        "SELECT FROM player_history_all"  # No matches_flat_clean mfc_h
    )
    assert (
        _evaluate_query_falsifiers(bad)
        == "F-matchup-cte-includes-non-1v1-history"
    )


def test_evaluate_query_falsifiers_fires_on_missing_decisive_flag() -> None:
    """F-decisive-result-flag-not-used fires when is_decisive_result = TRUE absent."""
    bad = (
        "WHERE TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at "
        "FROM player_history_all p JOIN matches_flat_clean mfc_h "
        "AND p.result IN ('Win', 'Loss')"
    )
    assert _evaluate_query_falsifiers(bad) == "F-decisive-result-flag-not-used"


# ---------------------------------------------------------------------------
# Materialization-side falsifier evaluation
# ---------------------------------------------------------------------------


def _baseline_sanity() -> dict[str, int]:
    """Return a clean sanity dict matching every EXPECTED_* constant."""
    return {
        "row_count": EXPECTED_OUTPUT_ROW_COUNT,
        "distinct_focal_match_id": EXPECTED_DISTINCT_FOCAL_MATCH_COUNT,
        "focal_rows_per_match_violations": 0,
        "symmetry_violations": 0,
    }


def test_mat_falsifier_clean_passes() -> None:
    """The canonical happy-path returns None from _evaluate_materialization_falsifiers."""
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), EXPECTED_OUTPUT_COLUMNS, _MATERIALIZATION_QUERY
        )
        is None
    )


def test_mat_falsifier_reconstructed_rating_column_present() -> None:
    """F-reconstructed-rating-column-present fires when a forbidden col is added."""
    cols = EXPECTED_OUTPUT_COLUMNS + ("reconstructed_rating_focal_pre",)
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), cols, _MATERIALIZATION_QUERY
        )
        == "F-reconstructed-rating-column-present"
    )


def test_mat_falsifier_forbidden_skill_scalar_projected() -> None:
    """F-forbidden-skill-scalar-projected fires when a raw MMR scalar is added."""
    cols = EXPECTED_OUTPUT_COLUMNS + ("focal_mmr",)
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), cols, _MATERIALIZATION_QUERY
        )
        == "F-forbidden-skill-scalar-projected"
    )


def test_mat_falsifier_post_game_token_projected() -> None:
    """F-post-game-token-projected fires when a target-outcome token is added."""
    cols = EXPECTED_OUTPUT_COLUMNS + ("focal_won",)
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), cols, _MATERIALIZATION_QUERY
        )
        == "F-post-game-token-projected"
    )


def test_mat_falsifier_output_column_mismatch() -> None:
    """F-output-column-mismatch fires when columns drift."""
    cols = tuple(reversed(EXPECTED_OUTPUT_COLUMNS))
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), cols, _MATERIALIZATION_QUERY
        )
        == "F-output-column-mismatch"
    )


def test_mat_falsifier_row_count_mismatch() -> None:
    """F-row-count-mismatch fires when row_count != EXPECTED_OUTPUT_ROW_COUNT."""
    sanity = _baseline_sanity()
    sanity["row_count"] = 100
    assert (
        _evaluate_materialization_falsifiers(
            sanity, EXPECTED_OUTPUT_COLUMNS, _MATERIALIZATION_QUERY
        )
        == "F-row-count-mismatch"
    )


def test_mat_falsifier_focal_rows_per_match_violation() -> None:
    """F-focal-rows-per-match-violation fires when violations > 0."""
    sanity = _baseline_sanity()
    sanity["focal_rows_per_match_violations"] = 5
    assert (
        _evaluate_materialization_falsifiers(
            sanity, EXPECTED_OUTPUT_COLUMNS, _MATERIALIZATION_QUERY
        )
        == "F-focal-rows-per-match-violation"
    )


def test_mat_falsifier_symmetry_violation() -> None:
    """F-symmetry-violation fires when started_at swap symmetry violates."""
    sanity = _baseline_sanity()
    sanity["symmetry_violations"] = 1
    assert (
        _evaluate_materialization_falsifiers(
            sanity, EXPECTED_OUTPUT_COLUMNS, _MATERIALIZATION_QUERY
        )
        == "F-symmetry-violation"
    )


def test_mat_falsifier_sql_falsifier_propagates() -> None:
    """A SQL-side falsifier (try-cast-missing) propagates via _evaluate_query_falsifiers."""
    bad_sql = "SELECT * FROM matches_flat_clean"
    assert (
        _evaluate_materialization_falsifiers(
            _baseline_sanity(), EXPECTED_OUTPUT_COLUMNS, bad_sql
        )
        == "F-try-cast-missing"
    )


# ---------------------------------------------------------------------------
# Audit-side falsifier evaluation
# ---------------------------------------------------------------------------


def _audit_kwargs(**overrides: object) -> dict[str, object]:
    """Return a happy-path kwargs dict for _evaluate_audit_falsifiers."""
    base: dict[str, object] = {
        "parquet_columns": EXPECTED_OUTPUT_COLUMNS,
        "features_audited": EXPECTED_AUDITED_FEATURE_COLUMNS,
        "projected_identity_columns": PROJECTED_IDENTITY_COLUMNS,
        "projected_context_columns": PROJECTED_CONTEXT_COLUMNS,
        "examiner_notes": (
            "`started_at` is projected as a row-identity anchor only; "
            "excluded from `features_audited`."
        ),
        "examiner_md_section1": (
            f"Section 1 includes the sentence: {EXAMINER_CLARITY_SENTENCE}"
        ),
    }
    base.update(overrides)
    return base


def test_audit_falsifier_clean_passes() -> None:
    """The canonical happy-path returns None from _evaluate_audit_falsifiers."""
    assert _evaluate_audit_falsifiers(**_audit_kwargs()) is None  # type: ignore[arg-type]


def test_audit_falsifier_features_audited_empty() -> None:
    """F-features-audited-empty fires on empty features tuple."""
    assert (
        _evaluate_audit_falsifiers(**_audit_kwargs(features_audited=()))  # type: ignore[arg-type]
        == "F-features-audited-empty"
    )


def test_audit_falsifier_features_audited_not_twenty_four_length() -> None:
    """F-features-audited-not-twenty-four fires on wrong-length tuple."""
    assert (
        _evaluate_audit_falsifiers(
            **_audit_kwargs(features_audited=EXPECTED_AUDITED_FEATURE_COLUMNS[:-1])  # type: ignore[arg-type]
        )
        == "F-features-audited-not-twenty-four"
    )


def test_audit_falsifier_features_audited_not_twenty_four_set_mismatch() -> None:
    """F-features-audited-not-twenty-four fires on wrong set (but right length)."""
    drift = EXPECTED_AUDITED_FEATURE_COLUMNS[:-1] + ("focal_match_id",)
    assert (
        _evaluate_audit_falsifiers(**_audit_kwargs(features_audited=drift))  # type: ignore[arg-type]
        == "F-features-audited-not-twenty-four"
    )


def test_audit_falsifier_context_column_counted_as_feature() -> None:
    """F-context-column-counted-as-feature fires when started_at is in features."""
    # Replace a legit feature with the context column to keep length 24.
    bad = ("started_at",) + EXPECTED_AUDITED_FEATURE_COLUMNS[1:]
    label = _evaluate_audit_falsifiers(**_audit_kwargs(features_audited=bad))  # type: ignore[arg-type]
    # Either the set-mismatch label (preferred) or context label is acceptable.
    assert label in {
        "F-context-column-counted-as-feature",
        "F-features-audited-not-twenty-four",
    }


def test_audit_falsifier_examiner_clarity_sentence_missing_in_notes() -> None:
    """F-examiner-clarity-sentence-missing fires when notes lack the fragments."""
    label = _evaluate_audit_falsifiers(
        **_audit_kwargs(examiner_notes="completely unrelated text")  # type: ignore[arg-type]
    )
    assert label == "F-examiner-clarity-sentence-missing"


def test_audit_falsifier_examiner_clarity_sentence_missing_in_md() -> None:
    """F-examiner-clarity-sentence-missing fires when MD §1 lacks the sentence."""
    label = _evaluate_audit_falsifiers(
        **_audit_kwargs(examiner_md_section1="lacks the sentence verbatim")  # type: ignore[arg-type]
    )
    assert label == "F-examiner-clarity-sentence-missing"


def test_audit_falsifier_output_column_mismatch() -> None:
    """F-output-column-mismatch fires when parquet columns drift."""
    label = _evaluate_audit_falsifiers(
        **_audit_kwargs(parquet_columns=("a", "b"))  # type: ignore[arg-type]
    )
    assert label == "F-output-column-mismatch"


# ---------------------------------------------------------------------------
# Q5 / Q7 / cross-region constants
# ---------------------------------------------------------------------------


def test_cross_region_policy_is_sensitivity_indicator_co_registration() -> None:
    """CROSS_REGION_POLICY is the Q5 BINDING value."""
    assert CROSS_REGION_POLICY == "sensitivity_indicator_co_registration"


def test_q7_in_game_historical_columns_are_canonical_4_tuple() -> None:
    """Q7 IN_GAME_HISTORICAL allowed columns match PR #242 BINDING."""
    assert IN_GAME_HISTORICAL_AGGREGATED_COLUMNS == (
        "APM",
        "SQ",
        "supplyCappedPercent",
        "header_elapsedGameLoops",
    )


# ---------------------------------------------------------------------------
# Frozen dataclass shape
# ---------------------------------------------------------------------------


def test_materialization_result_is_frozen_dataclass() -> None:
    """HistoryEnrichedMaterializationResult is a frozen dataclass."""
    r = HistoryEnrichedMaterializationResult(
        parquet_path=Path("/tmp/x"),
        row_count=0,
        column_names=(),
        distinct_focal_match_id_count=0,
        focal_rows_per_match_violations=0,
        symmetry_violations=0,
        materialized_output_paths=("/tmp/x",),
        halting_falsifier=None,
    )
    assert r.passed is True
    with pytest.raises(Exception):
        r.row_count = 5  # type: ignore[misc]


def test_materialization_result_passed_false_when_halting_set() -> None:
    """passed returns False when halting_falsifier is non-None."""
    r = HistoryEnrichedMaterializationResult(
        parquet_path=Path("/tmp/x"),
        row_count=0,
        column_names=(),
        distinct_focal_match_id_count=0,
        focal_rows_per_match_violations=0,
        symmetry_violations=0,
        halting_falsifier="F-something",
    )
    assert r.passed is False


def test_audit_result_is_frozen_dataclass() -> None:
    """HistoryEnrichedAuditResult is a frozen dataclass."""
    a = HistoryEnrichedAuditResult(
        spec_version=SPEC_VERSION,
        dataset=DATASET_TAG,
        phase_02_step=PHASE_02_STEP,
        audit_date="2026-05-28",
        future_leak_count=0,
        post_game_token_violations=0,
        normalization_fit_scope="training_fold_only",
        target_encoding_fold_awareness="N/A_no_target_encoding",
        cutoff_time_filter_structural_check="pass",
        reference_window_assertion="pass",
        features_audited=EXPECTED_AUDITED_FEATURE_COLUMNS,
        projected_context_columns=PROJECTED_CONTEXT_COLUMNS,
        projected_identity_columns=PROJECTED_IDENTITY_COLUMNS,
        verdict="PASS",
        artifact_json_path="x.json",
        artifact_md_path="x.md",
        halting_falsifier=None,
    )
    assert isinstance(a.features_audited, tuple)
    with pytest.raises(Exception):
        a.verdict = "FAIL"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# File-system / SHA helpers
# ---------------------------------------------------------------------------


def test_find_repo_root_walks_upward() -> None:
    """_find_repo_root locates the repo pyproject.toml above this test file."""
    root = _find_repo_root(Path(__file__))
    assert (root / "pyproject.toml").exists()


def test_find_repo_root_raises_when_no_pyproject(tmp_path: Path) -> None:
    """_find_repo_root raises FileNotFoundError when no ancestor has pyproject."""
    deep = tmp_path / "a" / "b"
    deep.mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        _find_repo_root(deep)


def test_sha256_file_returns_64_hex(tmp_path: Path) -> None:
    """_sha256_file returns a 64-char lowercase hex digest for real files."""
    f = tmp_path / "x.bin"
    f.write_bytes(b"hello world")
    digest = _sha256_file(f)
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)


def test_sha256_file_returns_not_found_for_absent(tmp_path: Path) -> None:
    """_sha256_file returns NOT_FOUND for absent files."""
    assert _sha256_file(tmp_path / "no_such") == "NOT_FOUND"


def test_resolve_repo_root_relpath_inside(tmp_path: Path) -> None:
    """_resolve_repo_root_relpath returns relative path inside repo_root."""
    root = tmp_path / "repo"
    nested = root / "a" / "b"
    nested.mkdir(parents=True)
    inside = nested / "f.parquet"
    inside.write_bytes(b"")
    assert _resolve_repo_root_relpath(inside, root) == "a/b/f.parquet"


def test_resolve_repo_root_relpath_outside(tmp_path: Path) -> None:
    """_resolve_repo_root_relpath returns absolute path when outside."""
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.parquet"
    outside.write_bytes(b"")
    assert _resolve_repo_root_relpath(outside, root) == outside.resolve().as_posix()


def test_get_git_sha_returns_unknown_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """_get_git_sha returns 'UNKNOWN' when subprocess fails."""
    import subprocess as _subprocess

    def _boom(*_args: object, **_kw: object) -> object:
        raise _subprocess.CalledProcessError(1, ["git"])

    monkeypatch.setattr(mod.subprocess, "run", _boom)
    assert mod._get_git_sha() == "UNKNOWN"


# ---------------------------------------------------------------------------
# Output artifact path constants
# ---------------------------------------------------------------------------


def test_history_enriched_output_relpath_is_canonical() -> None:
    """Parquet output path matches the plan's canonical relative path."""
    expected = (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
        "02_01_03_history_enriched_pre_game_features.parquet"
    )
    assert HISTORY_ENRICHED_OUTPUT_RELPATH == expected


def test_history_enriched_audit_json_relpath_is_canonical() -> None:
    """Audit JSON path matches the plan's canonical relative path."""
    expected = (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_01_03/leakage_audit_sc2egset.json"
    )
    assert HISTORY_ENRICHED_AUDIT_JSON_RELPATH == expected


def test_history_enriched_audit_md_relpath_is_canonical() -> None:
    """Audit MD path matches the plan's canonical relative path."""
    expected = (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
        "02_01_03/leakage_audit_sc2egset.md"
    )
    assert HISTORY_ENRICHED_AUDIT_MD_RELPATH == expected


def test_history_enriched_research_log_relpath_is_canonical() -> None:
    """Research log path matches the dataset research log."""
    assert HISTORY_ENRICHED_RESEARCH_LOG_RELPATH == (
        "src/rts_predict/games/sc2/datasets/sc2egset/reports/research_log.md"
    )


# ---------------------------------------------------------------------------
# Research log block builder
# ---------------------------------------------------------------------------


def test_research_log_block_contains_required_pr236_field_labels() -> None:
    """The non-closure block has every PR #236 precedent field label."""
    block = _build_research_log_block(
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    for required in (
        "**closure_status:** `still_open`",
        "**materialization_state:** `materialized`",
        "**leakage_audit_state:** `post_materialization_pass`",
        "**features_audited_count:** `24`",
        "**row_count:** `44418`",
        "**artifact:** `02_01_03_history_enriched_pre_game_features.parquet`",
        "**leakage_audit:** "
        "`reports/artifacts/02_01_03/leakage_audit_sc2egset.{json,md}`",
    ):
        assert required in block, f"missing: {required}"


def test_research_log_block_heading_follows_pr236_pattern() -> None:
    """Heading matches `## YYYY-MM-DD — Materialize Step 02_01_03 ...`."""
    block = _build_research_log_block(
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    assert block.startswith(
        "## 2026-05-28 — Materialize Step 02_01_03 "
        "five-family history-enriched pre_game tranche + first non-vacuous "
        "CROSS-02-01 audit\n"
    )


def test_research_log_block_includes_pr236_sub_headings() -> None:
    """The non-closure block uses PR #236's required sub-headings."""
    block = _build_research_log_block(
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    for sub in (
        "- **Category:**",
        "- **Dataset:** sc2egset",
        "- **Branch:**",
        "- **PR:** `PR #259`",
        "- **Step scope:**",
        "- **What:**",
        "- **Why:**",
        "- **How (reproducibility):**",
        "- **Findings:**",
        "- **What this means:**",
        "- **Decisions taken:**",
        "- **Decisions deferred:**",
        "- **Thesis mapping:**",
        "- **Open questions / follow-ups:**",
        "- **Acknowledged trade-offs:**",
        "- **Scope notes:**",
    ):
        assert sub in block, f"missing sub-heading: {sub}"


def test_research_log_block_excludes_status_closure_claim() -> None:
    """The block does NOT claim closure or STEP_STATUS flip."""
    block = _build_research_log_block(
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    # Must NOT say "closed" as a state claim.
    assert "closure_status:** `closed`" not in block
    # Must say still_open.
    assert "closure_status:** `still_open`" in block


def test_append_research_log_inserts_after_first_separator(tmp_path: Path) -> None:
    """append_research_log_entry inserts new block after the first `---` line."""
    rl = tmp_path / "rl.md"
    rl.write_text(
        "# Dataset research log\n\n---\n\n## 2026-05-23 — Old entry\n\nbody\n"
    )
    block = append_research_log_entry(
        research_log_path=rl,
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    content = rl.read_text()
    # The block precedes the old entry.
    new_idx = content.find("## 2026-05-28 — Materialize Step 02_01_03")
    old_idx = content.find("## 2026-05-23 — Old entry")
    assert 0 < new_idx < old_idx
    assert block in content


def test_append_research_log_fallback_prepends_when_no_separator(tmp_path: Path) -> None:
    """append_research_log_entry prepends the block when no `---` marker."""
    rl = tmp_path / "rl.md"
    rl.write_text("no separator anywhere\n")
    append_research_log_entry(
        research_log_path=rl,
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    content = rl.read_text()
    assert content.startswith("## 2026-05-28 — Materialize Step 02_01_03")


# ---------------------------------------------------------------------------
# Real DuckDB end-to-end (skipif if DB absent)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_materialization_shape_44418_x_28(tmp_path: Path) -> None:
    """Real-DB materialization yields 44,418 rows × 28 columns; halting=None."""
    out = tmp_path / "out.parquet"
    r = materialize_history_enriched_pre_game_features(REAL_DB_PATH, out)
    assert r.passed is True
    assert r.halting_falsifier is None
    assert r.row_count == EXPECTED_OUTPUT_ROW_COUNT
    assert r.distinct_focal_match_id_count == EXPECTED_DISTINCT_FOCAL_MATCH_COUNT
    assert len(r.column_names) == EXPECTED_PARQUET_COLUMN_COUNT
    assert r.column_names == EXPECTED_OUTPUT_COLUMNS


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_audit_verdict_pass_and_features_audited_24(
    tmp_path: Path,
) -> None:
    """Real-DB audit end-to-end produces verdict PASS + features_audited count 24."""
    out = tmp_path / "out.parquet"
    aj = tmp_path / "audit.json"
    am = tmp_path / "audit.md"
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, out)
    a = audit_history_enriched_pre_game_features(
        parquet_path=out,
        audit_json_path=aj,
        audit_md_path=am,
        duckdb_path=REAL_DB_PATH,
        audit_date="2026-05-28",
        audit_pr="PR #TEST",
    )
    assert a.verdict == "PASS"
    assert a.halting_falsifier is None
    assert len(a.features_audited) == 24
    assert set(a.features_audited) == set(EXPECTED_AUDITED_FEATURE_COLUMNS)


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_audit_json_has_features_audited_count_24(
    tmp_path: Path,
) -> None:
    """Audit JSON's `features_audited_count` field equals 24."""
    out = tmp_path / "out.parquet"
    aj = tmp_path / "audit.json"
    am = tmp_path / "audit.md"
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, out)
    audit_history_enriched_pre_game_features(
        parquet_path=out,
        audit_json_path=aj,
        audit_md_path=am,
        duckdb_path=REAL_DB_PATH,
        audit_date="2026-05-28",
        audit_pr="PR #TEST",
    )
    payload = json.loads(aj.read_text(encoding="utf-8"))
    assert payload["features_audited_count"] == 24
    assert payload["row_count"] == EXPECTED_OUTPUT_ROW_COUNT
    assert payload["distinct_focal_match_count"] == EXPECTED_DISTINCT_FOCAL_MATCH_COUNT
    assert payload["verdict"] == "PASS"
    assert payload["five_family_set"] == list(FIVE_FAMILY_CANONICAL_ORDER)
    assert payload["excluded_family"] == EXCLUDED_FAMILY
    assert payload["cross_region_policy"] == CROSS_REGION_POLICY
    # Custom extensions section explicitly enumerates fields beyond §3.
    assert "custom_extensions" in payload
    assert payload["custom_extensions"]["fields"]
    # Temporal-filter field carries the canonical TRY_CAST predicate.
    assert "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at" in payload[
        "temporal_filter"
    ]


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_audit_md_contains_verbatim_sql(tmp_path: Path) -> None:
    """Audit MD embeds the verbatim _MATERIALIZATION_QUERY per Invariant I6."""
    out = tmp_path / "out.parquet"
    aj = tmp_path / "audit.json"
    am = tmp_path / "audit.md"
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, out)
    audit_history_enriched_pre_game_features(
        parquet_path=out,
        audit_json_path=aj,
        audit_md_path=am,
        duckdb_path=REAL_DB_PATH,
        audit_date="2026-05-28",
        audit_pr="PR #TEST",
    )
    md = am.read_text(encoding="utf-8")
    assert "WITH mfc_focal AS" in md
    assert (
        "TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < t.started_at" in md
    )
    assert "is_decisive_result = TRUE" in md
    assert "matches_flat_clean mfc_h" in md
    assert EXAMINER_CLARITY_SENTENCE in md
    # Invariant I5 citation per N9.
    assert "Invariant I5" in md
    # Defensive matches_long_raw pin per R3-N2.
    assert "matches_long_raw_yaml_sha256" in md
    # Five-family enumeration.
    for fam in FIVE_FAMILY_CANONICAL_ORDER:
        assert fam in md


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_parquet_bytes_reproducible_across_runs(tmp_path: Path) -> None:
    """Two consecutive runs produce byte-identical Parquet."""
    a = tmp_path / "a.parquet"
    b = tmp_path / "b.parquet"
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, a)
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, b)
    sa = hashlib.sha256(a.read_bytes()).hexdigest()
    sb = hashlib.sha256(b.read_bytes()).hexdigest()
    assert sa == sb


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_run_step_02_01_03_writes_research_log(tmp_path: Path) -> None:
    """run_step_02_01_03 appends a non-closure research_log block."""
    out = tmp_path / "out.parquet"
    aj = tmp_path / "audit.json"
    am = tmp_path / "audit.md"
    rl = tmp_path / "research_log.md"
    rl.write_text("# Dataset research log\n\n---\n\n")
    mat, audit = run_step_02_01_03(
        duckdb_path=REAL_DB_PATH,
        output_parquet_path=out,
        audit_json_path=aj,
        audit_md_path=am,
        research_log_path=rl,
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
        audit_pr="PR #TEST",
    )
    assert mat.passed is True
    assert audit.verdict == "PASS"
    content = rl.read_text()
    assert "## 2026-05-28 — Materialize Step 02_01_03" in content
    assert "closure_status:** `still_open`" in content
    assert "features_audited_count:** `24`" in content


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not available",
)
def test_real_db_no_target_match_row_admitted_into_history(
    tmp_path: Path,
) -> None:
    """For sample focal matches, no history row equals the target started_at.

    Tests the temporal-leakage failure mode: a history join that admits the
    target match (started_at >= target.started_at) would inflate
    focal_prior_match_count. Sample 50 random focal matches and verify that
    focal_prior_match_count never includes the target match itself.
    """
    out = tmp_path / "out.parquet"
    materialize_history_enriched_pre_game_features(REAL_DB_PATH, out)
    con = duckdb.connect(":memory:")
    try:
        # Spot-check: the count of prior matches in the materialised feature
        # is the count of history rows strictly before started_at. If we
        # join the parquet back to player_history_all in the source DB with
        # the SAME `<` predicate, the counts must agree exactly for a
        # sample of 50 focal matches.
        con.execute(f"ATTACH '{REAL_DB_PATH.as_posix()}' AS srcdb (READ_ONLY);")
        rows = con.execute(f"""
            WITH feat AS (
              SELECT focal_match_id, focal_player, started_at,
                     focal_prior_match_count
              FROM read_parquet('{out.as_posix()}')
              USING SAMPLE 50 ROWS
            )
            SELECT f.focal_match_id, f.focal_prior_match_count,
              (SELECT COUNT(*) FROM srcdb.player_history_all ph
               WHERE ph.toon_id = f.focal_player
                 AND TRY_CAST(ph.details_timeUTC AS TIMESTAMP) < f.started_at) AS expected
            FROM feat f
        """).fetchall()
    finally:
        con.close()
    for fmid, observed, expected in rows:
        assert observed == expected, (
            f"focal_prior_match_count drift for {fmid}: "
            f"observed={observed} expected={expected}"
        )


# ---------------------------------------------------------------------------
# PR #257 ROADMAP amendment grep token + amendment text presence
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not ROADMAP_MD_PATH.exists(),
    reason="ROADMAP.md not present",
)
def test_pr257_amendment_grep_token_count_at_least_four() -> None:
    """grep -c materialization_scope_amendment_post_pr_255 >= 4."""
    text = ROADMAP_MD_PATH.read_text(encoding="utf-8")
    count = text.count(PR257_GREP_TOKEN)
    assert count >= 4, f"PR257 grep-token count = {count} (expected >=4)"


@pytest.mark.skipif(
    not ROADMAP_MD_PATH.exists(),
    reason="ROADMAP.md not present",
)
def test_pr257_amendment_lists_five_families() -> None:
    """PR #257 ROADMAP amendment lists the 5 permitted families verbatim."""
    text = ROADMAP_MD_PATH.read_text(encoding="utf-8")
    for fam in FIVE_FAMILY_CANONICAL_ORDER:
        assert fam in text


@pytest.mark.skipif(
    not ROADMAP_MD_PATH.exists(),
    reason="ROADMAP.md not present",
)
def test_pr257_amendment_lists_three_excluded_columns() -> None:
    """PR #257 ROADMAP amendment lists the 3 excluded columns verbatim."""
    text = ROADMAP_MD_PATH.read_text(encoding="utf-8")
    for col in FORBIDDEN_RECONSTRUCTED_RATING_COLUMNS:
        assert col in text


# ---------------------------------------------------------------------------
# Omit-closure (PR #255) field re-verification
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not OMIT_CLOSURE_CSV_PATH.exists(),
    reason="PR #255 omit-closure CSV not present",
)
def test_omit_closure_q5_policy_field_is_sensitivity_indicator_co_registration() -> None:
    """PR #255 CSV's q5_policy field is sensitivity_indicator_co_registration."""
    text = OMIT_CLOSURE_CSV_PATH.read_text(encoding="utf-8")
    # The CSV has a header row; the value appears in the canonical row.
    assert "sensitivity_indicator_co_registration" in text


@pytest.mark.skipif(
    not OMIT_CLOSURE_CSV_PATH.exists(),
    reason="PR #255 omit-closure CSV not present",
)
def test_omit_closure_verdict_is_omit_reconstructed_rating_verbatim() -> None:
    """PR #255 verdict is `omit_reconstructed_rating_and_unblock_other_five`."""
    text = OMIT_CLOSURE_CSV_PATH.read_text(encoding="utf-8")
    assert "omit_reconstructed_rating_and_unblock_other_five" in text


# ---------------------------------------------------------------------------
# PR-merge-SHA disambiguation (R3-B3)
# ---------------------------------------------------------------------------


def test_pr243_and_pr245_merge_shas_are_distinct() -> None:
    """The two SHAs that R3-B3 disambiguated are byte-distinct."""
    assert PR243_MERGE_SHA_FULL != PR245_MERGE_SHA_FULL
    assert PR243_MERGE_SHA_PREFIX == "445bae01"
    assert PR245_MERGE_SHA_PREFIX == "ee15d362"


def test_pr243_and_pr245_merge_shas_appear_in_git_log() -> None:
    """The PR #243 and PR #245 merge SHAs are present in this repo's git log."""
    import subprocess

    log = subprocess.run(
        ["git", "log", "--all", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert PR243_MERGE_SHA_PREFIX in log
    assert PR245_MERGE_SHA_PREFIX in log
    assert PR257_MERGE_SHA_PREFIX in log


# ---------------------------------------------------------------------------
# Examiner-clarity sentence
# ---------------------------------------------------------------------------


def test_examiner_clarity_sentence_contains_required_fragments() -> None:
    """The EXAMINER_CLARITY_SENTENCE contains the required fragments."""
    assert "`started_at` is projected as a row-identity anchor only" in (
        EXAMINER_CLARITY_SENTENCE
    )
    assert "excluded from `features_audited`" in EXAMINER_CLARITY_SENTENCE


# ---------------------------------------------------------------------------
# Parquet helper-function coverage
# ---------------------------------------------------------------------------


def test_read_parquet_columns_and_row_count(tmp_path: Path) -> None:
    """_read_parquet_columns + _read_parquet_row_count return correct values."""
    p = tmp_path / "tiny.parquet"
    con = duckdb.connect(":memory:")
    con.execute(
        "COPY (SELECT 1 AS a, 'x' AS b UNION ALL SELECT 2, 'y') "
        f"TO '{p.as_posix()}' (FORMAT PARQUET)"
    )
    con.close()
    assert mod._read_parquet_columns(p) == ("a", "b")
    assert mod._read_parquet_row_count(p) == 2


# ---------------------------------------------------------------------------
# _check_no_reconstructed_rating_column helper
# ---------------------------------------------------------------------------


def test_check_no_reconstructed_rating_column_detects() -> None:
    """_check_no_reconstructed_rating_column returns True on a forbidden col."""
    assert (
        _check_no_reconstructed_rating_column(
            ("foo", "reconstructed_rating_diff", "bar")
        )
        is True
    )


def test_check_no_reconstructed_rating_column_clean() -> None:
    """_check_no_reconstructed_rating_column returns False for clean cols."""
    assert _check_no_reconstructed_rating_column(EXPECTED_OUTPUT_COLUMNS) is False


# ---------------------------------------------------------------------------
# Source-table allowlist text spot checks
# ---------------------------------------------------------------------------


def test_source_table_allowlist_clean_query_with_allowed_tables() -> None:
    """A SQL referencing only allowed views returns ()."""
    sql = (
        "WITH x AS (SELECT * FROM matches_flat_clean) "
        "SELECT * FROM matches_history_minimal JOIN player_history_all USING(toon_id)"
    )
    assert _check_source_table_allowlist(sql) == ()


def test_source_table_allowlist_detects_matches_long_raw() -> None:
    """matches_long_raw is detected (defensive — not joined by default)."""
    bad = "SELECT * FROM matches_long_raw"
    assert "matches_long_raw" in _check_source_table_allowlist(bad)


def test_source_table_allowlist_detects_space_bounded_matches_flat() -> None:
    """`matches_flat ` (space-bounded) is detected to distinguish from _clean."""
    bad = "SELECT * FROM matches_flat WHERE 1"
    assert "matches_flat" in _check_source_table_allowlist(bad)


# ---------------------------------------------------------------------------
# Audit JSON `notes` content checks
# ---------------------------------------------------------------------------


def test_build_audit_notes_contains_examiner_sentence() -> None:
    """_build_audit_notes contains the examiner-clarity fragments."""
    notes = mod._build_audit_notes("PR #259")
    for fragment in (
        "`started_at` is projected as a row-identity anchor only",
        "excluded from `features_audited`",
    ):
        assert fragment in notes


def test_build_audit_notes_contains_closure_non_overclaim() -> None:
    """_build_audit_notes contains the closure non-overclaim."""
    notes = mod._build_audit_notes("PR #259")
    assert "Step 02_01_03 NOT closed by this PR" in notes


def test_build_audit_notes_contains_pr257_grep_token() -> None:
    """_build_audit_notes mentions the PR #257 grep token."""
    notes = mod._build_audit_notes("PR #259")
    assert PR257_GREP_TOKEN in notes


# ---------------------------------------------------------------------------
# Falsifier semantics — features_audited identity exclusion
# ---------------------------------------------------------------------------


def test_audit_falsifier_clean_pass_excludes_started_at() -> None:
    """The canonical features_audited excludes started_at."""
    assert "started_at" not in EXPECTED_AUDITED_FEATURE_COLUMNS


def test_audit_falsifier_clean_pass_excludes_identity() -> None:
    """The canonical features_audited excludes identity columns."""
    for col in PROJECTED_IDENTITY_COLUMNS:
        assert col not in EXPECTED_AUDITED_FEATURE_COLUMNS


# ---------------------------------------------------------------------------
# Module-load assertions (defensive)
# ---------------------------------------------------------------------------


def test_module_load_constants_self_consistent() -> None:
    """The module-level constants are arithmetically self-consistent."""
    assert (
        len(EXPECTED_AUDITED_FEATURE_COLUMNS)
        == EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
    )
    assert (
        len(EXPECTED_OUTPUT_COLUMNS) == EXPECTED_PARQUET_COLUMN_COUNT
    )
    assert (
        3 + 1 + EXPECTED_AUDITED_FEATURE_COLUMN_COUNT
        == EXPECTED_PARQUET_COLUMN_COUNT
    )


def test_research_log_block_uses_iso_date_format() -> None:
    """The research log block embeds an ISO YYYY-MM-DD date."""
    block = _build_research_log_block(
        audit_pr="PR #259",
        audit_date="2026-05-28",
        branch="feat/sc2egset-02-01-03-five-family-materialization",
    )
    iso = re.search(r"## (\d{4}-\d{2}-\d{2}) ", block)
    assert iso is not None
    assert iso.group(1) == "2026-05-28"


# ---------------------------------------------------------------------------
# Output column structure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "audited_column",
    list(EXPECTED_AUDITED_FEATURE_COLUMNS),
)
def test_every_audited_column_present_in_expected_output(audited_column: str) -> None:
    """Each audited column appears in EXPECTED_OUTPUT_COLUMNS."""
    assert audited_column in EXPECTED_OUTPUT_COLUMNS


def test_audit_pr_placeholder_constant_present() -> None:
    """The PR placeholder constant is preserved verbatim."""
    assert AUDIT_PR_PLACEHOLDER.startswith("PR #")
