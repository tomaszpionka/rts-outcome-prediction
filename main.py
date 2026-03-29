import logging
import pandas as pd  # <-- Dodane do wyświetlenia ostatecznej tabelki cech
import duckdb
from config import DB_FILE
from data_ingestion import (
    slim_down_sc2_with_manifest,
    move_data_to_duck_db,
    load_map_translations,
)
from data_processing import create_ml_views, get_matches_dataframe
from ml_pipeline import perform_feature_engineering, temporal_train_test_split
from model_training import train_and_evaluate_models
from elo_system import add_elo_features
from hyperparameter_tuning import tune_random_forest
from sklearn.metrics import accuracy_score

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SC2_Pipeline")


def main():
    logger.info("Start SC2 ML Pipeline...")

    # Zostaw to odkomentowane, jeśli chcesz najpierw przetworzyć nowe powtórki:
    slim_down_sc2_with_manifest()

    con = duckdb.connect(str(DB_FILE))

    try:
        # Zostaw odkomentowane, jeśli masz nowe dane do zrzucenia do DuckDB:
        move_data_to_duck_db(con)
        load_map_translations(con)
        create_ml_views(con)
        raw_df = get_matches_dataframe(con)

        # ==========================================
        # KROK 1: WARIANT B (Autorski System ELO)
        # ==========================================
        logger.info("Aplikuję system relatywnego ELO...")
        df_with_elo = add_elo_features(raw_df)

        # Feature Engineering (Teraz ma w sobie cechy z ELO!)
        features_df = perform_feature_engineering(df_with_elo)

        # Podział na zbiory
        X_train, X_test, y_train, y_test = temporal_train_test_split(
            features_df, test_size=0.2
        )

        # ==========================================
        # KROK 2: Ewaluacja Bazowa
        # ==========================================
        logger.info("Oceniamy modele bazowe (teraz na wzbogaconych danych z ELO)...")
        # Wywołujemy to, żeby zobaczyć, czy samo dodanie ELO podniosło bazowe wyniki
        trained_models = train_and_evaluate_models(X_train, X_test, y_train, y_test)

        # ==========================================
        # KROK 3: WARIANT A (Hiperparametryzacja)
        # ==========================================
        logger.info("Rozpoczynam strojenie hiperparametrów Random Forest (Tuning)...")
        best_rf_model = tune_random_forest(X_train, y_train)

        # Ostateczny Test!
        y_pred = best_rf_model.predict(X_test)
        final_acc = accuracy_score(y_test, y_pred)

        print(f"\n{'='*65}")
        print(f"OSTATECZNY WYNIK (Tuned Random Forest + Time-Aware ELO System)")
        print(f"Accuracy na zbiorze testowym: {final_acc:.4f}")
        print(f"{'='*65}\n")

        # Wypisanie Feature Importance dla naszego wypasionego modelu
        importances = best_rf_model.feature_importances_
        fi_df = pd.DataFrame({"Feature": X_train.columns, "Importance": importances})
        fi_df = fi_df.sort_values(by="Importance", ascending=False).head(10)

        print("--- Top 10 Najważniejszych Cech (Po tuningu i wdrożeniu ELO) ---")
        print(fi_df.to_string(index=False))

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
    finally:
        con.close()
        logger.info("Połączenie z DuckDB zamknięte.")


if __name__ == "__main__":
    main()
