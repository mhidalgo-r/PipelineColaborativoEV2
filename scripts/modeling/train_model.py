import os
import pandas as pd
import logging
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ==========================
# CARPETAS
# ==========================
os.makedirs("models", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("data/outputs", exist_ok=True)

# ==========================
# LOGGER
# ==========================
logging.basicConfig(
    filename="logs/modeling.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger()

# ==========================
# RUTAS
# ==========================
INPUT = "data/processed/bank_transformed.csv"
MODEL_PATH = "models/bank_model.pkl"
ENCODER_PATH = "models/encoder.pkl"
PREDICTIONS = "data/outputs/model_predictions.csv"

# ==========================
# MAIN
# ==========================
def train():
    logger.info("=" * 50)
    logger.info("INICIO ENTRENAMIENTO")
    logger.info("=" * 50)

    try:
        df = pd.read_csv(INPUT)
        logger.info(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

        # ==============================
        # ELIMINAR DATA LEAKAGE
        # ==============================
        remove = [
            "subscription_probability",
            "risk_level",
            "approval_status",
            "premium_client",
            "scoring_reason"
        ]
        existing = [c for c in remove if c in df.columns]
        df = df.drop(columns=existing)
        logger.info(f"Columnas eliminadas (data leakage): {existing}")

        # ==============================
        # TARGET Y FEATURES
        # ==============================
        y = df["deposit"]
        X = df.drop("deposit", axis=1)
        logger.info(f"Variable objetivo: deposit")
        logger.info(f"Valores unicos deposit: {y.unique().tolist()}")
        logger.info(f"Variables predictoras: {list(X.columns)}")

        # ==============================
        # ENCODING CATEGORICAS
        # ==============================
        encoders = {}
        categorical = X.select_dtypes(include=["object", "str"]).columns

        for column in categorical:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column].astype(str))
            encoders[column] = le
            logger.info(f"Encoding aplicado: {column}")

        # Encoding target si es string
        le_target = LabelEncoder()
        if y.dtype == object or str(y.dtype) == "string":
            y = le_target.fit_transform(y.astype(str))
            encoders["__target__"] = le_target
            logger.info(f"Encoding target: {le_target.classes_}")
        
        # ==============================
        # SPLIT 70/30 CON STRATIFY
        # ==============================
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.30,
            random_state=42,
            stratify=y
        )

        logger.info(f"Train: {X_train.shape[0]} registros")
        logger.info(f"Test: {X_test.shape[0]} registros")

        # ==============================
        # MODELO: REGRESION LOGISTICA
        # Justificacion: interpretable,
        # eficiente para clasificacion
        # binaria, buen baseline
        # ==============================
        model = LogisticRegression(
            max_iter=2000,
            random_state=42
        )
        model.fit(X_train, y_train)

        # ==============================
        # METRICAS BASICAS EN TRAINING
        # ==============================
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)

        train_accuracy = round(accuracy_score(y_train, train_preds), 4)
        test_accuracy = round(accuracy_score(y_test, test_preds), 4)

        logger.info(f"Accuracy Train: {train_accuracy}")
        logger.info(f"Accuracy Test: {test_accuracy}")

        if train_accuracy - test_accuracy > 0.05:
            logger.warning("Posible overfitting detectado")
        else:
            logger.info("Sin indicios de overfitting")

        # ==============================
        # GUARDAR MODELO Y ENCODERS
        # ==============================
        joblib.dump(model, MODEL_PATH)
        joblib.dump(encoders, ENCODER_PATH)
        logger.info(f"Modelo guardado: {MODEL_PATH}")
        logger.info(f"Encoders guardados: {ENCODER_PATH}")

        # ==============================
        # GUARDAR PREDICCIONES
        # ==============================
        results = pd.DataFrame({
            "real": y_test,
            "prediction": test_preds
        })
        results.to_csv(PREDICTIONS, index=False)
        logger.info(f"Predicciones guardadas: {PREDICTIONS}")

        print("\nEntrenamiento completado:")
        print(f"  Modelo: {MODEL_PATH}")
        print(f"  Accuracy Train: {train_accuracy}")
        print(f"  Accuracy Test: {test_accuracy}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    train()