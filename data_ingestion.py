import json
import logging
import duckdb
import pandas as pd
from config import MANIFEST_PATH, REPLAYS_SOURCE_DIR, DUCKDB_TEMP_DIR

logger = logging.getLogger(__name__)


def slim_down_sc2_with_manifest():
    keys_to_remove = {"messageEvents", "gameEvents", "trackerEvents"}

    if MANIFEST_PATH.exists() and MANIFEST_PATH.stat().st_size > 0:
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            logger.info(f"Loaded manifest: {len(manifest)} files tracked.")
        except json.JSONDecodeError:
            logger.warning("Manifest was corrupted or empty. Starting fresh.")
            manifest = {}
    else:
        manifest = {}
        logger.info("No manifest found. Starting fresh.")

    total_files_processed = 0
    total_bytes_saved = 0

    try:
        # Skanujemy folder w Downloads, celując tylko w pliki SC2Replay.json wewnątrz folderów 'data'
        for json_file in REPLAYS_SOURCE_DIR.rglob("*/data/*.SC2Replay.json"):

            # Klucz w manifeście to teraz ścieżka relatywna do folderu Downloads
            file_key = str(json_file.relative_to(REPLAYS_SOURCE_DIR))
            if manifest.get(file_key) is True:
                continue

            try:
                original_size = json_file.stat().st_size
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                found_keys = keys_to_remove.intersection(data.keys())
                if found_keys:
                    for key in found_keys:
                        data.pop(key)
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, separators=(",", ":"))

                    new_size = json_file.stat().st_size
                    total_bytes_saved += original_size - new_size

                manifest[file_key] = True
                total_files_processed += 1

                if total_files_processed % 100 == 0:
                    logger.info(f"Processed {total_files_processed} files...")

            except Exception as e:
                logger.error(f"Error processing {file_key}: {e}")
                manifest[file_key] = False

    finally:
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
        logger.info("Manifest updated and saved.")

    gb_saved = total_bytes_saved / (1024**3)
    logger.info(
        f"New files processed: {total_files_processed}. Disk space saved: {gb_saved:.4f} GB"
    )


def move_data_to_duck_db(con, should_drop: bool = False):
    logger.info("Setting up DuckDB optimizations (Anti-OOM configuration)...")
    con.execute(f"SET temp_directory='{DUCKDB_TEMP_DIR}'")
    con.execute("SET max_temp_directory_size='150GB'")

    # 1. Zwiększamy limit RAM (skoro masz 32 GB, 24 GB jest bezpieczne, zostawia 8 GB dla Ubuntu)
    con.execute("SET memory_limit='24GB'")

    # 2. Zmniejszamy liczbę wątków. Mniejsza równoległość przy parsowaniu = mniejsze zużycie RAM.
    con.execute("SET threads = 4")

    # 3. KLUCZOWE: Wyłączamy zachowanie kolejności.
    # Pozwala DuckDB natychmiast wrzucać przetworzone wiersze na dysk, zwalniając RAM.
    con.execute("SET preserve_insertion_order=false")

    # Wymuszamy czytanie TYLKO z podfolderów /data/
    json_glob = f"{str(REPLAYS_SOURCE_DIR)}/**/data/*.SC2Replay.json"

    if should_drop:
        con.execute("DROP TABLE IF EXISTS raw")
        logger.info("Dropped existing 'raw' table.")

    # Usunąłem format='auto', podanie samych columns wystarczy i często przyspiesza proces
    query = f"""
        CREATE TABLE IF NOT EXISTS raw AS
        SELECT * FROM read_json(
            '{json_glob}',
            union_by_name = true, 
            maximum_object_size = 536870912, 
            filename = true,
            columns = {{
                'header': 'JSON', 'initData': 'JSON', 'details': 'JSON', 'metadata': 'JSON',
                'ToonPlayerDescMap': 'JSON'
            }}
        )
    """

    logger.info(f"Scanning JSONs into DuckDB: {json_glob}")
    con.execute(query)
    row_count = con.execute("SELECT count(*) FROM raw").fetchone()[0]
    logger.info(f"DuckDB Ingestion complete. Total replays in 'raw': {row_count}")


def load_map_translations(con):
    """Skanuje i scala wszystkie pliki map_foreign_to_english_mapping.json w jedną tabelę DuckDB"""
    logger.info("Szukam słowników tłumaczeń map...")
    global_mapping = {}

    for map_file in REPLAYS_SOURCE_DIR.rglob("*map_foreign_to_english_mapping.json"):
        try:
            with open(map_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                global_mapping.update(data)
        except Exception as e:
            logger.error(f"Error reading {map_file}: {e}")

    if global_mapping:
        mapping_df = pd.DataFrame(
            list(global_mapping.items()), columns=["foreign_name", "english_name"]
        )
        con.execute("DROP TABLE IF EXISTS map_translation")
        # DuckDB potrafi zaciągnąć DataFrame Pandas bezpośrednio z pamięci!
        con.execute("CREATE TABLE map_translation AS SELECT * FROM mapping_df")
        logger.info(
            f"Załadowano {len(global_mapping)} unikalnych tłumaczeń map do bazy DuckDB."
        )
    else:
        logger.warning("Nie znaleziono żadnych plików słownika map.")
