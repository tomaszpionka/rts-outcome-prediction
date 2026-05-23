"""Tests for ``adjudicate_pre_game_source_layer`` (SC2EGSet Step 02_01_02 adjudication).

Covers all required test cases per the approved plan §T03:
    1. Frozen-dataclass shape (3 decisions; rationale ≥ 80 chars; materialized_output_paths == ()).
    2. Falsifier q1_no_evidence: empty MHM/MFC raises q1_no_evidence.
    3. Falsifier q2_anchor_type_mismatch: started_at VARCHAR fires anchor_type_mismatch.
    4. Falsifier q3_race_post_decision_chosen: Amend-path candidate with post-decision vocab.
    5. Falsifier q3_prior_decision_silently_reversed: rationale missing yaml citation.
    6. Falsifier q3_random_vocabulary_dropped: Amend-path drops Random rows without mitigation.
    7. Falsifier q1_source_layer_loses_1v1_scope: raw candidate below expected distinct count.
    8. Stale registry path behaviour (FileNotFoundError on non-existent path).
    9. Real-DB smoke test (skipif if DB absent).
    10. MHM-faction-Random absence smoke test.
    11-15. Additional coverage for private helpers and falsifier logic.

Uses ``tmp_path`` synthetic DuckDB fixtures for all falsifier tests.
Uses ``@pytest.mark.skipif`` for real-DB tests.
"""

from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pytest

from rts_predict.games.sc2.datasets.sc2egset.adjudicate_pre_game_source_layer import (
    EXPECTED_BLANK_SELECTED_RACE_ROW_COUNT,
    EXPECTED_MFC_ROW_COUNT,
    EXPECTED_MHM_ROW_COUNT,
    EXPECTED_RAND_ROW_COUNT,
    EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID,
    POST_DECISION_RACE_TOKENS,
    PRE_GAME_RACE_TOKENS,
    ProvenanceShaNotFoundError,
    _adjudicate_anchor,
    _adjudicate_race_and_random,
    _adjudicate_source_layer,
    _check_falsifiers_anchor,
    _check_falsifiers_source_layer,
    _find_repo_root,
    _run_anchor_peeks,
    _run_race_and_random_peeks,
    _run_source_layer_peeks,
    _validate_provenance_shas,
    adjudicate_pre_game_source_layer,
)

# ---------------------------------------------------------------------------
# Repo-relative paths
# ---------------------------------------------------------------------------

_TESTS_ROOT = Path(__file__).resolve().parents[6]

REAL_DB_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "data"
    / "db"
    / "db.duckdb"
)

REGISTRY_CSV_PATH: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
    / "02_01_01_feature_family_registry.csv"
)

ARTIFACT_DIR: Path = (
    _TESTS_ROOT
    / "src"
    / "rts_predict"
    / "games"
    / "sc2"
    / "datasets"
    / "sc2egset"
    / "reports"
    / "artifacts"
    / "02_feature_engineering"
    / "01_pre_game_vs_in_game_boundary"
)

# ---------------------------------------------------------------------------
# Synthetic DuckDB helpers
# ---------------------------------------------------------------------------


def _make_minimal_duckdb(tmp_path: Path) -> Path:
    """Create a minimal synthetic DuckDB with all required views populated."""
    db_path = tmp_path / "test.duckdb"
    con = duckdb.connect(str(db_path))
    # matches_flat_clean (44418 rows; 22209 distinct replay_ids; 2 rows each)
    con.execute("""
        CREATE TABLE matches_flat_clean AS
        SELECT
            CAST(i AS VARCHAR) AS replay_id,
            'file.json' AS filename,
            CAST(i * 10 + p AS VARCHAR) AS toon_id,
            'Player' AS nickname,
            p AS playerID,
            0 AS userID,
            CASE WHEN p = 1 THEN 'Win' ELSE 'Loss' END AS result,
            FALSE AS is_mmr_missing,
            'Prot' AS race,
            'Prot' AS selectedRace,
            'KR' AS region,
            '1' AS realm,
            FALSE AS isInClan,
            1 AS startDir,
            10 AS startLocX,
            10 AS startLocY,
            'MapName' AS metadata_mapName,
            2 AS gd_maxPlayers,
            123 AS gd_mapFileSyncChecksum,
            TRUE AS details_isBlizzardMap,
            '2023-01-01 00:00:00' AS details_timeUTC,
            '5.0.0' AS header_version,
            '100' AS metadata_baseBuild,
            '100' AS metadata_dataBuild,
            '5.0.0' AS metadata_gameVersion,
            TRUE AS go_amm,
            0 AS go_clientDebugFlags,
            TRUE AS go_competitive,
            1200 AS duration_seconds,
            FALSE AS is_duration_suspicious
        FROM generate_series(1, 22209) t(i),
             generate_series(1, 2) p(p)
    """)
    # matches_history_minimal view-like table
    con.execute("""
        CREATE TABLE matches_history_minimal AS
        SELECT
            CONCAT('sc2egset::', CAST(i AS VARCHAR)) AS match_id,
            TIMESTAMP '2023-01-01 00:00:00' AS started_at,
            CAST(i * 10 + p AS VARCHAR) AS player_id,
            CAST(i * 10 + (3 - p) AS VARCHAR) AS opponent_id,
            'Prot' AS faction,
            'Prot' AS opponent_faction,
            CASE WHEN p = 1 THEN TRUE ELSE FALSE END AS won,
            1200 AS duration_seconds,
            'sc2egset' AS dataset_tag
        FROM generate_series(1, 22209) t(i),
             generate_series(1, 2) p(p)
    """)
    # player_history_all (44817 rows)
    con.execute("""
        CREATE TABLE player_history_all AS
        SELECT
            CAST(i AS VARCHAR) AS replay_id,
            CAST(i AS VARCHAR) AS toon_id,
            0 AS header_elapsedGameLoops
        FROM generate_series(1, 44817) t(i)
    """)
    # replay_players_raw (44817 rows)
    con.execute("""
        CREATE TABLE replay_players_raw AS
        SELECT
            'file.json' AS filename,
            CAST(i AS VARCHAR) AS toon_id,
            'Player' AS nickname,
            1 AS playerID,
            0 AS userID,
            FALSE AS isInClan,
            '' AS clanTag,
            1000 AS MMR,
            'Prot' AS race,
            'Prot' AS selectedRace,
            100 AS handicap,
            'KR' AS region,
            '1' AS realm,
            'Gold' AS highestLeague,
            'Win' AS result,
            200 AS APM,
            50 AS SQ,
            5 AS supplyCappedPercent,
            1 AS startDir,
            10 AS startLocX,
            10 AS startLocY,
            255 AS color_a,
            0 AS color_b,
            0 AS color_g,
            255 AS color_r
        FROM generate_series(1, 44817) t(i)
    """)
    con.close()
    return db_path


def _make_empty_duckdb(tmp_path: Path) -> Path:
    """Create a synthetic DuckDB with empty versions of required tables."""
    db_path = tmp_path / "empty.duckdb"
    con = duckdb.connect(str(db_path))
    con.execute("""
        CREATE TABLE matches_flat_clean (
            replay_id VARCHAR, filename VARCHAR, toon_id VARCHAR, nickname VARCHAR,
            playerID INTEGER, userID BIGINT, result VARCHAR, is_mmr_missing BOOLEAN,
            race VARCHAR, selectedRace VARCHAR, region VARCHAR, realm VARCHAR,
            isInClan BOOLEAN, startDir INTEGER, startLocX INTEGER, startLocY INTEGER,
            metadata_mapName VARCHAR, gd_maxPlayers BIGINT, gd_mapFileSyncChecksum BIGINT,
            details_isBlizzardMap BOOLEAN, details_timeUTC VARCHAR, header_version VARCHAR,
            metadata_baseBuild VARCHAR, metadata_dataBuild VARCHAR,
            metadata_gameVersion VARCHAR, go_amm BOOLEAN, go_clientDebugFlags BIGINT,
            go_competitive BOOLEAN, duration_seconds BIGINT, is_duration_suspicious BOOLEAN
        )
    """)
    con.execute("""
        CREATE TABLE matches_history_minimal (
            match_id VARCHAR, started_at TIMESTAMP, player_id VARCHAR,
            opponent_id VARCHAR, faction VARCHAR, opponent_faction VARCHAR,
            won BOOLEAN, duration_seconds BIGINT, dataset_tag VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE player_history_all (
            replay_id VARCHAR, toon_id VARCHAR, header_elapsedGameLoops INTEGER
        )
    """)
    con.execute("""
        CREATE TABLE replay_players_raw (
            filename VARCHAR, toon_id VARCHAR, nickname VARCHAR, playerID INTEGER,
            userID BIGINT, isInClan BOOLEAN, clanTag VARCHAR, MMR INTEGER,
            race VARCHAR, selectedRace VARCHAR, handicap INTEGER, region VARCHAR,
            realm VARCHAR, highestLeague VARCHAR, result VARCHAR, APM INTEGER,
            SQ INTEGER, supplyCappedPercent INTEGER, startDir INTEGER,
            startLocX INTEGER, startLocY INTEGER, color_a INTEGER, color_b INTEGER,
            color_g INTEGER, color_r INTEGER
        )
    """)
    con.close()
    return db_path


def _make_varchar_anchor_duckdb(tmp_path: Path) -> Path:
    """Create a DuckDB where started_at is VARCHAR to test q2_anchor_type_mismatch."""
    db_path = tmp_path / "varchar_anchor.duckdb"
    con = duckdb.connect(str(db_path))
    # Same as minimal but started_at is VARCHAR
    con.execute("""
        CREATE TABLE matches_flat_clean AS
        SELECT
            CAST(i AS VARCHAR) AS replay_id,
            'file.json' AS filename,
            CAST(i * 10 + p AS VARCHAR) AS toon_id,
            'Player' AS nickname,
            p AS playerID,
            0 AS userID,
            CASE WHEN p = 1 THEN 'Win' ELSE 'Loss' END AS result,
            FALSE AS is_mmr_missing,
            'Prot' AS race,
            'Prot' AS selectedRace,
            'KR' AS region, '1' AS realm, FALSE AS isInClan,
            1 AS startDir, 10 AS startLocX, 10 AS startLocY,
            'MapName' AS metadata_mapName, 2 AS gd_maxPlayers,
            123 AS gd_mapFileSyncChecksum, TRUE AS details_isBlizzardMap,
            '2023-01-01 00:00:00' AS details_timeUTC, '5.0.0' AS header_version,
            '100' AS metadata_baseBuild, '100' AS metadata_dataBuild,
            '5.0.0' AS metadata_gameVersion, TRUE AS go_amm, 0 AS go_clientDebugFlags,
            TRUE AS go_competitive, 1200 AS duration_seconds, FALSE AS is_duration_suspicious
        FROM generate_series(1, 22209) t(i), generate_series(1, 2) p(p)
    """)
    # started_at as VARCHAR — will trigger q2_anchor_type_mismatch
    con.execute("""
        CREATE TABLE matches_history_minimal AS
        SELECT
            CONCAT('sc2egset::', CAST(i AS VARCHAR)) AS match_id,
            '2023-01-01 00:00:00' AS started_at,
            CAST(i * 10 + p AS VARCHAR) AS player_id,
            CAST(i * 10 + (3 - p) AS VARCHAR) AS opponent_id,
            'Prot' AS faction, 'Prot' AS opponent_faction,
            CASE WHEN p = 1 THEN TRUE ELSE FALSE END AS won,
            1200 AS duration_seconds, 'sc2egset' AS dataset_tag
        FROM generate_series(1, 22209) t(i), generate_series(1, 2) p(p)
    """)
    con.execute("""
        CREATE TABLE player_history_all AS
        SELECT CAST(i AS VARCHAR) AS replay_id, CAST(i AS VARCHAR) AS toon_id,
               0 AS header_elapsedGameLoops
        FROM generate_series(1, 44817) t(i)
    """)
    con.execute("""
        CREATE TABLE replay_players_raw AS
        SELECT 'file.json' AS filename, CAST(i AS VARCHAR) AS toon_id,
               'Player' AS nickname, 1 AS playerID, 0 AS userID, FALSE AS isInClan,
               '' AS clanTag, 1000 AS MMR, 'Prot' AS race, 'Prot' AS selectedRace,
               100 AS handicap, 'KR' AS region, '1' AS realm, 'Gold' AS highestLeague,
               'Win' AS result, 200 AS APM, 50 AS SQ, 5 AS supplyCappedPercent,
               1 AS startDir, 10 AS startLocX, 10 AS startLocY,
               255 AS color_a, 0 AS color_b, 0 AS color_g, 255 AS color_r
        FROM generate_series(1, 44817) t(i)
    """)
    con.close()
    return db_path


# ---------------------------------------------------------------------------
# Test 1: Frozen-dataclass shape
# ---------------------------------------------------------------------------


class TestAdjudicationResultShape:
    """AdjudicationResult must have exactly 3 decisions with non-empty rationale."""

    def test_three_decisions_returned(self, tmp_path: Path) -> None:
        """adjudicate_pre_game_source_layer returns exactly 3 decisions."""
        db_path = _make_minimal_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        assert len(result.decisions) == 3

    def test_each_decision_has_rationale_ge_80_chars(self, tmp_path: Path) -> None:
        """Each decision has a rationale_paragraph of at least 80 characters."""
        db_path = _make_minimal_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        for decision in result.decisions:
            assert len(decision.rationale_paragraph) >= 80, (
                f"Decision {decision.decision_id} rationale too short: "
                f"{len(decision.rationale_paragraph)} chars"
            )

    def test_materialized_output_paths_always_empty(self, tmp_path: Path) -> None:
        """materialized_output_paths is always () regardless of outcome."""
        db_path = _make_minimal_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.materialized_output_paths == ()

    def test_decision_ids_correct(self, tmp_path: Path) -> None:
        """Decision IDs are Q1_source_layer, Q2_anchor, Q3_race_and_random."""
        db_path = _make_minimal_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        ids = [d.decision_id for d in result.decisions]
        assert "Q1_source_layer" in ids
        assert "Q2_anchor" in ids
        assert "Q3_race_and_random" in ids


# ---------------------------------------------------------------------------
# Test 2: Falsifier q1_no_evidence
# ---------------------------------------------------------------------------


class TestFalsifierQ1NoEvidence:
    """Empty MHM and MFC tables fire q1_no_evidence."""

    def test_empty_tables_fire_q1_no_evidence(self, tmp_path: Path) -> None:
        """Zero-row MHM/MFC fires q1_no_evidence halting falsifier."""
        db_path = _make_empty_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.passed is False
        assert result.halting_falsifier == "q1_no_evidence"

    def test_empty_tables_materialized_paths_still_empty(self, tmp_path: Path) -> None:
        """Even when falsifier fires, materialized_output_paths is ()."""
        db_path = _make_empty_duckdb(tmp_path)
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.materialized_output_paths == ()

    def test_empty_tables_csv_not_written(self, tmp_path: Path) -> None:
        """CSV artifact is NOT written when a halting falsifier fires."""
        db_path = _make_empty_duckdb(tmp_path)
        out_dir = tmp_path / "out"
        adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, out_dir)
        csv_path = out_dir / "02_01_02_source_anchor_race_adjudication.csv"
        assert not csv_path.exists(), "CSV should NOT be written when falsifier fires"


# ---------------------------------------------------------------------------
# Test 3: Falsifier q2_anchor_type_mismatch
# ---------------------------------------------------------------------------


class TestFalsifierQ2AnchorTypeMismatch:
    """started_at VARCHAR in MHM fires q2_anchor_type_mismatch."""

    def test_varchar_started_at_fires_type_mismatch(self, tmp_path: Path) -> None:
        """started_at with VARCHAR type fires q2_anchor_type_mismatch."""
        db_path = _make_varchar_anchor_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_anchor_peeks(con)
        con.close()
        halting = _check_falsifiers_anchor(peeks)
        assert halting == "q2_anchor_type_mismatch"

    def test_timestamp_anchor_does_not_fire(self, tmp_path: Path) -> None:
        """started_at with TIMESTAMP type does not fire q2_anchor_type_mismatch."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_anchor_peeks(con)
        con.close()
        halting = _check_falsifiers_anchor(peeks)
        assert halting is None


# ---------------------------------------------------------------------------
# Test 4: Falsifier q3_race_post_decision_chosen (Q3.AMEND-path test)
# ---------------------------------------------------------------------------


class TestFalsifierQ3RacePostDecisionChosen:
    """Under Q3.AMEND, race with only post-decision vocab should fire."""

    def test_post_decision_vocab_detection(self) -> None:
        """POST_DECISION_RACE_TOKENS is a strict subset of PRE_GAME_RACE_TOKENS."""
        assert POST_DECISION_RACE_TOKENS < PRE_GAME_RACE_TOKENS, (
            "POST_DECISION_RACE_TOKENS must be a strict subset of PRE_GAME_RACE_TOKENS"
        )

    def test_race_column_vocab_is_post_decision_under_amend(self, tmp_path: Path) -> None:
        """Verify that the race column in the minimal DB has only post-decision values."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        rpr_race_keys = set(peeks["rpr_race_vocab"].keys())
        # Under Q3.RATIFY the post-decision vocab is expected and is the chosen convention.
        # Under Q3.AMEND, this would be a falsifier.
        # Verify the data shows only post-decision values.
        assert rpr_race_keys <= POST_DECISION_RACE_TOKENS, (
            f"Expected only post-decision tokens in synthetic DB race column, got {rpr_race_keys}"
        )


# ---------------------------------------------------------------------------
# Test 5: Falsifier q3_prior_decision_silently_reversed
# ---------------------------------------------------------------------------


class TestFalsifierQ3PriorDecisionSilentlyReversed:
    """Q3 RATIFY outcome must cite matches_long_raw.yaml:101-103 in rationale."""

    def test_ratify_rationale_cites_yaml(self, tmp_path: Path) -> None:
        """Q3 RATIFY decision rationale cites matches_long_raw.yaml:101-103."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        decision = _adjudicate_race_and_random(peeks)
        assert "matches_long_raw.yaml:101-103" in decision.rationale_paragraph, (
            "Q3.RATIFY must cite matches_long_raw.yaml:101-103 to avoid "
            "q3_prior_decision_silently_reversed falsifier"
        )

    def test_ratify_also_cites_mhm_yaml(self, tmp_path: Path) -> None:
        """Q3 RATIFY decision rationale also cites matches_history_minimal.yaml:52-53."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        decision = _adjudicate_race_and_random(peeks)
        assert "matches_history_minimal.yaml:52-53" in decision.rationale_paragraph


# ---------------------------------------------------------------------------
# Test 6: Falsifier q3_random_vocabulary_dropped
# ---------------------------------------------------------------------------


class TestFalsifierQ3RandomVocabularyDropped:
    """Under Q3.AMEND, excluding Random rows without mitigation would fire."""

    def test_random_rows_present_in_rpr(self, tmp_path: Path) -> None:
        """Random/Rand rows are present in replay_players_raw.selectedRace (real data contract)."""
        # This test uses the constants, not the real DB
        assert EXPECTED_RAND_ROW_COUNT == 10
        assert EXPECTED_BLANK_SELECTED_RACE_ROW_COUNT == 1110

    def test_q3_ratify_does_not_drop_rows(self, tmp_path: Path) -> None:
        """Under Q3.RATIFY, no rows are dropped — all 44,418 MFC rows are retained."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        source_peeks = _run_source_layer_peeks(con)
        con.close()
        assert source_peeks["mfc_count"] == 22209 * 2


# ---------------------------------------------------------------------------
# Test 7: Falsifier q1_source_layer_loses_1v1_scope
# ---------------------------------------------------------------------------


class TestFalsifierQ1Source1v1Lost:
    """A candidate source table with fewer than EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID rows fires."""

    def test_full_1v1_scope_present_in_minimal_db(self, tmp_path: Path) -> None:
        """Minimal DB has exactly EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID distinct replay_ids."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_source_layer_peeks(con)
        con.close()
        assert peeks["mfc_distinct_replay_id"] == EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID

    def test_1v1_scope_falsifier_fires_when_below_threshold(self) -> None:
        """_check_falsifiers_source_layer fires q1_source_1v1_lost if distinct < threshold."""
        peeks_low: dict = {
            "mfc_count": 1000,
            "mhm_count": 1000,
            "mfc_distinct_replay_id": EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID - 1,
            "mhm_distinct_match_id": 500,
            "ph_count": 1000,
            "rpr_count": 1000,
            "join_cardinality": EXPECTED_MFC_ROW_COUNT,
            "mfc_columns": frozenset(
                {
                    "race", "metadata_mapName", "metadata_gameVersion",
                    "is_mmr_missing", "replay_id", "toon_id",
                }
            ),
        }
        halting = _check_falsifiers_source_layer(peeks_low)
        assert halting == "q1_source_1v1_lost"


# ---------------------------------------------------------------------------
# Test 8: Stale/missing registry path
# ---------------------------------------------------------------------------


class TestStaleRegistryPath:
    """Non-existent registry path causes FileNotFoundError (not a special stale check here)."""

    def test_nonexistent_db_raises(self, tmp_path: Path) -> None:
        """A non-existent DuckDB path raises an error when opening."""
        missing_db = tmp_path / "no_such.duckdb"
        with pytest.raises(Exception):
            adjudicate_pre_game_source_layer(missing_db, REGISTRY_CSV_PATH, tmp_path / "out")


# ---------------------------------------------------------------------------
# Test 9: Real-DB smoke test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not found on disk",
)
class TestRealDbSmoke:
    """Full adjudication against the real on-disk DuckDB."""

    def test_passed_is_true(self, tmp_path: Path) -> None:
        """Real-DB adjudication returns passed=True."""
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.passed is True

    def test_decisions_count_is_three(self, tmp_path: Path) -> None:
        """Real-DB adjudication returns exactly 3 decisions."""
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert len(result.decisions) == 3

    def test_materialized_output_paths_empty(self, tmp_path: Path) -> None:
        """Real-DB result has empty materialized_output_paths."""
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.materialized_output_paths == ()

    def test_halting_falsifier_is_none(self, tmp_path: Path) -> None:
        """Real-DB adjudication has no halting falsifier."""
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.halting_falsifier is None

    def test_artifact_files_exist(self, tmp_path: Path) -> None:
        """Both CSV and MD artifact files exist after real-DB adjudication."""
        out_dir = tmp_path / "out"
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, out_dir)
        assert Path(result.artifact_csv_path).exists()
        assert Path(result.artifact_md_path).exists()


# ---------------------------------------------------------------------------
# Test 10: MHM-faction-Random absence smoke test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not found on disk",
)
class TestMhmFactionRandomAbsence:
    """MHM faction vocabulary must be exactly {Prot, Terr, Zerg} — consistent with YAML."""

    def test_mhm_faction_vocab_is_prot_terr_zerg(self) -> None:
        """MHM faction vocabulary observed = {Prot, Terr, Zerg}."""
        con = duckdb.connect(str(REAL_DB_PATH), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        observed_vocab = set(peeks["mhm_faction_vocab"].keys())
        expected_vocab = {"Prot", "Terr", "Zerg"}
        assert observed_vocab == expected_vocab, (
            f"MHM faction vocab expected {expected_vocab}, got {observed_vocab}. "
            "Contradicts matches_history_minimal.yaml:52-53 which states faction "
            "derives from race (not selectedRace)."
        )

    def test_mhm_faction_random_absent_consistent_with_yaml(self) -> None:
        """MHM faction does not contain Random — consistent with matches_history_minimal.yaml."""
        con = duckdb.connect(str(REAL_DB_PATH), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        assert "Random" not in peeks["mhm_faction_vocab"]
        assert "Rand" not in peeks["mhm_faction_vocab"]

    def test_spec_amendments_proposed_non_empty_for_q3(self, tmp_path: Path) -> None:
        """Q3 decision has spec_amendments_proposed for CROSS-02-02 §6.1 minor amendment."""
        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert len(result.spec_amendments_proposed) > 0, (
            "spec_amendments_proposed must be non-empty: CROSS-02-02 §6.1 minor amendment "
            "is required under Q3.RATIFY to document the MHM faction exclusion of Random."
        )


# ---------------------------------------------------------------------------
# Additional coverage tests (Tests 11-15)
# ---------------------------------------------------------------------------


class TestPrivateHelpers:
    """Coverage for private helper functions and edge cases."""

    def test_adjudicate_source_layer_has_four_candidates(self, tmp_path: Path) -> None:
        """Q1 decision has exactly 4 candidates considered."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_source_layer_peeks(con)
        con.close()
        decision = _adjudicate_source_layer(peeks)
        assert len(decision.candidates_considered) == 4

    def test_adjudicate_anchor_has_q2a_and_q2b_in_chosen(self, tmp_path: Path) -> None:
        """Q2 chosen string mentions Q2(a) BINDING and Q2(b) RECOMMENDATION ONLY."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_anchor_peeks(con)
        con.close()
        decision = _adjudicate_anchor(peeks)
        assert "BINDING" in decision.chosen
        assert "RECOMMENDATION ONLY" in decision.chosen

    def test_adjudicate_race_chosen_is_ratify(self, tmp_path: Path) -> None:
        """Q3 chosen is Q3.RATIFY."""
        db_path = _make_minimal_duckdb(tmp_path)
        con = duckdb.connect(str(db_path), read_only=True)
        peeks = _run_race_and_random_peeks(con)
        con.close()
        decision = _adjudicate_race_and_random(peeks)
        assert "Q3.RATIFY" in decision.chosen

    def test_grain_mismatch_fires_falsifier(self) -> None:
        """Incorrect join cardinality fires q1_source_grain_mismatch."""
        bad_peeks: dict = {
            "mfc_count": EXPECTED_MFC_ROW_COUNT,
            "mhm_count": EXPECTED_MHM_ROW_COUNT,
            "mfc_distinct_replay_id": EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID,
            "mhm_distinct_match_id": EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID,
            "ph_count": 44817,
            "rpr_count": 44817,
            "join_cardinality": EXPECTED_MFC_ROW_COUNT - 1,
            "mfc_columns": frozenset(
                {
                    "race", "metadata_mapName", "metadata_gameVersion",
                    "is_mmr_missing", "replay_id", "toon_id",
                }
            ),
        }
        halting = _check_falsifiers_source_layer(bad_peeks)
        assert halting == "q1_source_grain_mismatch"

    def test_missing_required_column_fires_falsifier(self) -> None:
        """Missing required column fires q1_source_missing_column."""
        bad_peeks: dict = {
            "mfc_count": EXPECTED_MFC_ROW_COUNT,
            "mhm_count": EXPECTED_MHM_ROW_COUNT,
            "mfc_distinct_replay_id": EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID,
            "mhm_distinct_match_id": EXPECTED_TRUE_1V1_DISTINCT_REPLAY_ID,
            "ph_count": 44817,
            "rpr_count": 44817,
            "join_cardinality": EXPECTED_MFC_ROW_COUNT,
            "mfc_columns": frozenset(
                # Missing 'race' column
                {
                    "metadata_mapName", "metadata_gameVersion",
                    "is_mmr_missing", "replay_id", "toon_id",
                }
            ),
        }
        halting = _check_falsifiers_source_layer(bad_peeks)
        assert halting == "q1_source_missing_column"

    def test_cross_row_inconsistency_fires_anchor_falsifier(self) -> None:
        """Non-zero cross-row inconsistency fires q2_anchor_cross_row_inconsistency."""
        bad_peeks: dict = {
            "mhm_column_types": {"started_at": "TIMESTAMP"},
            "details_timeUTC_null_count": 0,
            "started_at_range": (None, None),
            "cross_row_inconsistency": 5,
        }
        halting = _check_falsifiers_anchor(bad_peeks)
        assert halting == "q2_anchor_cross_row_inconsistency"

    def test_md_artifact_written_even_when_falsifier_fires(self, tmp_path: Path) -> None:
        """MD artifact is written even when a halting falsifier fires (auditability)."""
        db_path = _make_empty_duckdb(tmp_path)
        out_dir = tmp_path / "out"
        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, out_dir)
        md_path = out_dir / "02_01_02_source_anchor_race_adjudication.md"
        assert result.passed is False
        assert md_path.exists(), "MD artifact must be written even when falsifier fires"


# ---------------------------------------------------------------------------
# Test 16: Provenance SHA-256 integrity (TestProvenanceShaIntegrity)
# ---------------------------------------------------------------------------


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


@pytest.mark.skipif(
    not REAL_DB_PATH.exists(),
    reason="Real DuckDB not found on disk",
)
class TestProvenanceShaIntegrityRealDb:
    """Real-DB test: every *_sha256 column must be a 64-char lowercase hex digest."""

    def test_real_db_csv_has_hex_digest_per_sha_column(self, tmp_path: Path) -> None:
        """Every *_sha256 column in the rendered CSV matches ^[0-9a-f]{64}$.

        Guards against NOT_FOUND, empty, wrong-length, non-hex, or uppercase values
        (Invariant I6 — reproducibility). Regression test for the parents[7] bug.
        """
        import csv as _csv

        result = adjudicate_pre_game_source_layer(REAL_DB_PATH, REGISTRY_CSV_PATH, tmp_path / "out")
        assert result.passed is True, f"Expected passed=True; halting={result.halting_falsifier}"
        assert result.artifact_csv_path is not None

        with open(result.artifact_csv_path, encoding="utf-8") as fh:
            rows = list(_csv.DictReader(fh))

        assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"
        sha_cols = [c for c in rows[0].keys() if c.endswith("_sha256")]
        assert len(sha_cols) > 0, "No *_sha256 columns found in CSV"

        failures: list[str] = []
        for i, row in enumerate(rows):
            for col in sha_cols:
                value = row[col]
                if not _HEX64_RE.fullmatch(value):
                    failures.append(
                        f"row {i} ({row.get('decision_id')!r}) col {col!r}: {value!r}"
                    )
        assert not failures, (
            f"provenance_sha_not_found: {len(failures)} column(s) failed hex-digest check:\n"
            + "\n".join(failures)
        )


class TestProvenanceShaIntegrity:
    """Synthetic tests for the provenance_sha_not_found falsifier."""

    def test_synthetic_missing_upstream_fires_falsifier(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Monkeypatching _sha256_file to return NOT_FOUND fires provenance_sha_not_found.

        Asserts: result.passed is False, halting_falsifier == "provenance_sha_not_found",
        and the CSV file does NOT exist on disk after the call.
        """
        from rts_predict.games.sc2.datasets.sc2egset import adjudicate_pre_game_source_layer as mod

        db_path = _make_minimal_duckdb(tmp_path)
        out_dir = tmp_path / "out"

        # Monkeypatch _sha256_file to return NOT_FOUND for every call
        monkeypatch.setattr(mod, "_sha256_file", lambda path: "NOT_FOUND")

        result = adjudicate_pre_game_source_layer(db_path, REGISTRY_CSV_PATH, out_dir)

        assert result.passed is False, "Expected passed=False when SHA falsifier fires"
        assert result.halting_falsifier == "provenance_sha_not_found", (
            "Expected halting_falsifier='provenance_sha_not_found', "
            f"got {result.halting_falsifier!r}"
        )
        csv_path = out_dir / "02_01_02_source_anchor_race_adjudication.csv"
        assert not csv_path.exists(), (
            "CSV must NOT be written when provenance_sha_not_found falsifier fires"
        )

    def test_sha_digest_regex_is_strict(self) -> None:
        """_validate_provenance_shas rejects invalid SHA values.

        Invalid values: NOT_FOUND, empty string, too-short hex, invalid char,
        and uppercase hex (must be lowercase).
        """
        valid_sha = "a" * 64  # valid 64-char lowercase hex

        invalid_cases = [
            ("NOT_FOUND", "literal NOT_FOUND"),
            ("", "empty string"),
            ("1234", "too short"),
            ("1234567890123456789012345678901234567890123456789012345678901234X", "invalid char X"),
            ("A" * 64, "uppercase hex"),
        ]

        for bad_value, description in invalid_cases:
            row_dict = {"decision_id": "Q1_source_layer", "validator_module_sha256": bad_value}
            with pytest.raises(ProvenanceShaNotFoundError, match="[Pp]rovenance SHA falsifier"):
                _validate_provenance_shas([row_dict])

        # A valid 64-char lowercase hex must NOT raise
        good_row = {"decision_id": "Q1_source_layer", "validator_module_sha256": valid_sha}
        _validate_provenance_shas([good_row])  # should not raise

    def test_find_repo_root_finds_pyproject_toml(self) -> None:
        """_find_repo_root walking up from a nested path returns the repo root."""
        # Use this test file's own path — it's inside the repo
        nested_path = Path(__file__).resolve()
        repo_root = _find_repo_root(nested_path)
        assert (repo_root / "pyproject.toml").exists(), (
            f"_find_repo_root returned {repo_root} but no pyproject.toml found there"
        )

    def test_find_repo_root_raises_on_non_repo_path(self, tmp_path: Path) -> None:
        """_find_repo_root raises FileNotFoundError when no pyproject.toml exists."""
        with pytest.raises(FileNotFoundError, match="pyproject.toml"):
            _find_repo_root(tmp_path / "deep" / "nested" / "file.txt")
