import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

logger = logging.getLogger(__name__)


def tune_random_forest(X_train, y_train):
    logger.info(
        "Rozpoczynam strojenie hiperparametrów dla Random Forest (Wariant A)..."
    )

    # Definiujemy przestrzeń poszukiwań (Grid)
    param_dist = {
        "n_estimators": randint(100, 500),  # Liczba drzew
        "max_depth": [5, 8, 12, 15, None],  # Maksymalna głębokość drzewa
        "min_samples_split": randint(2, 20),  # Minimalna liczba próbek do podziału
        "min_samples_leaf": randint(
            1, 10
        ),  # Minimalna liczba próbek w liściu (chroni przed overfittingiem)
        "max_features": ["sqrt", "log2"],  # Liczba cech brana pod uwagę przy podziale
    }

    rf = RandomForestClassifier(random_state=42)

    # RandomizedSearchCV wylosuje 50 kombinacji i przetestuje je za pomocą 5-krotnej walidacji krzyżowej
    random_search = RandomizedSearchCV(
        estimator=rf,
        param_distributions=param_dist,
        n_iter=50,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,  # Używa wszystkich rdzeni procesora
        random_state=42,
        verbose=1,
    )

    random_search.fit(X_train, y_train)

    logger.info(f"Najlepsze parametry: {random_search.best_params_}")
    logger.info(f"Najlepsze CV Accuracy: {random_search.best_score_:.4f}")

    # Zwracamy model z najlepszymi znalezionymi ustawieniami
    return random_search.best_estimator_
