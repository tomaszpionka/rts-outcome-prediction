import logging
import pandas as pd

logger = logging.getLogger(__name__)


def add_elo_features(df):
    logger.info("Generowanie autorskiego systemu ELO (Wariant B)...")

    df = df.sort_values("match_time").reset_index(drop=True)

    elo_dict = {}
    games_played_dict = {}
    pre_match_elos = {}

    # FAZA 1: Bezpieczna inicjalizacja (rejestrujemy WSZYSTKICH graczy z danego meczu)
    for row in df.itertuples():
        match_id = row.match_id
        p1 = row.p1_name
        p2 = row.p2_name

        if match_id not in pre_match_elos:
            pre_match_elos[match_id] = {}

        for p in [p1, p2]:
            if p not in elo_dict:
                elo_dict[p] = 1500.0
                games_played_dict[p] = 0
            if p not in pre_match_elos[match_id]:
                pre_match_elos[match_id][p] = elo_dict[p]

    # FAZA 2: Bezpieczne liczenie ELO (tylko RAZ na unikalny mecz)
    processed_matches = set()
    for row in df.itertuples():
        match_id = row.match_id

        # Jeśli mecz już zaktualizował ELO, pomiń
        if match_id in processed_matches:
            continue

        p1 = row.p1_name
        p2 = row.p2_name
        target = 1 if row.p1_result == "Win" else 0

        # Obliczenie oczekiwanego wyniku dla P1
        e1 = 1 / (1 + 10 ** ((elo_dict[p2] - elo_dict[p1]) / 400))

        # Dynamiczny K-Factor dla nowych graczy
        k1 = 64 if games_played_dict[p1] < 10 else 32
        k2 = 64 if games_played_dict[p2] < 10 else 32

        # Aktualizacja rankingów
        elo_dict[p1] += k1 * (target - e1)
        elo_dict[p2] += k2 * ((1 - target) - (1 - e1))

        games_played_dict[p1] += 1
        games_played_dict[p2] += 1

        processed_matches.add(match_id)

    logger.info("Mapowanie ELO z powrotem do głównego zbioru...")

    df["p1_pre_match_elo"] = df.apply(
        lambda x: pre_match_elos[x["match_id"]][x["p1_name"]], axis=1
    )
    df["p2_pre_match_elo"] = df.apply(
        lambda x: pre_match_elos[x["match_id"]][x["p2_name"]], axis=1
    )

    df["elo_diff"] = df["p1_pre_match_elo"] - df["p2_pre_match_elo"]
    df["expected_win_prob"] = 1 / (1 + 10 ** (-df["elo_diff"] / 400))

    return df
