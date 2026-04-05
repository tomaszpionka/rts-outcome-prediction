"""AoE2 game package configuration — paths and constants."""
from pathlib import Path

# -- Project paths --
GAME_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = GAME_DIR.parent.parent.parent
DATA_DIR: Path = GAME_DIR / "data"
REPORTS_DIR: Path = GAME_DIR / "reports"

# -- Dataset paths (two sources) --
AOE2COMPANION_DIR: Path = DATA_DIR / "aoe2companion"
AOE2COMPANION_RAW_DIR: Path = AOE2COMPANION_DIR / "raw"
AOE2COMPANION_RAW_MATCHES_DIR: Path = AOE2COMPANION_RAW_DIR / "matches"
AOE2COMPANION_RAW_LEADERBOARDS_DIR: Path = AOE2COMPANION_RAW_DIR / "leaderboards"
AOE2COMPANION_RAW_PROFILES_DIR: Path = AOE2COMPANION_RAW_DIR / "profiles"
AOE2COMPANION_RAW_RATINGS_DIR: Path = AOE2COMPANION_RAW_DIR / "ratings"
AOE2COMPANION_DB_FILE: Path = AOE2COMPANION_DIR / "db" / "db.duckdb"
AOE2COMPANION_TEMP_DIR: Path = AOE2COMPANION_DIR / "tmp"
AOE2COMPANION_MANIFEST: Path = AOE2COMPANION_DIR / "api" / "api_dump_list.json"

AOESTATS_DIR: Path = DATA_DIR / "aoestats"
AOESTATS_RAW_DIR: Path = AOESTATS_DIR / "raw"
AOESTATS_RAW_MATCHES_DIR: Path = AOESTATS_RAW_DIR / "matches"
AOESTATS_RAW_PLAYERS_DIR: Path = AOESTATS_RAW_DIR / "players"
AOESTATS_DB_FILE: Path = AOESTATS_DIR / "db" / "db.duckdb"
AOESTATS_TEMP_DIR: Path = AOESTATS_DIR / "tmp"
AOESTATS_MANIFEST: Path = AOESTATS_DIR / "api" / "db_dump_list.json"

# -- Reproducibility --
RANDOM_SEED: int = 42
