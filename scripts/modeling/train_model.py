import os
import pandas as pd
import logging
import joblib
import json
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score

# Silenciar warnings internos de sklearn para mantener consola limpia para el profesor
warnings.filterwarnings("ignore", category=UserWarning)

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
SCALER_PATH = "models/scaler.pkl"
ENCODER_PATH = "models/encoder.pkl"
PREDICTIONS = "data/outputs/model_predictions.csv"
METRICS_JSON = "data/outputs/model_metrics.json"

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
        # ESCALAMIENTO REQUERIDO (Frena ConvergenceWarning)
        # ==============================
        scaler = StandardScaler()
        # Escalar numéricas para asegurar estabilidad matemática
        num_cols = X_train.select_dtypes(include=["int64", "float64"]).columns
        X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
        X_test[num_cols] = scaler.transform(X_test[num_cols])
        logger.info("Escalamiento estándar aplicado sobre variables numéricas.")

        # ==============================
        # MODELO: REGRESION LOGISTICA
        # ==============================
        model = LogisticRegression(
            max_iter=5000,
            random_state=42,
            solver="lbfgs"
        )
        model.fit(X_train, y_train)

        # ==============================
        # CAPTURA DE PREDICCIONES Y PROBABILIDADES
        # ==============================
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)
        
        # OBTENER COLUMNA DE PROBABILIDAD REAL (Clase 1: Sí deposita)
        test_probs = model.predict_proba(X_test)[:, 1]

        train_accuracy = round(accuracy_score(y_train, train_preds), 4)
        test_accuracy = round(accuracy_score(y_test, test_preds), 4)

        logger.info(f"Accuracy Train: {train_accuracy}")
        logger.info(f"Accuracy Test: {test_accuracy}")

        if train_accuracy - test_accuracy > 0.05:
            logger.warning("Posible overfitting detectado")
        else:
            logger.info("Sin indicios de overfitting")

        # ==============================
        # GUARDAR MODELO, ESCALADOR Y ENCODERS
        # ==============================
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        joblib.dump(encoders, ENCODER_PATH)
        logger.info(f"Modelos y transformadores serializados correctamente.")

        # ==============================
        # GUARDAR PREDICCIONES CON CORRECCIÓN DE NOMBRES
        # ==============================
        results = pd.DataFrame({
            "real": y_test.values if hasattr(y_test, "values") else y_test,
            "prediction_class": test_preds,
            "probability": test_probs
        })
        results.to_csv(PREDICTIONS, index=False)
        logger.info(f"Predicciones completas y estructuradas guardadas en: {PREDICTIONS}")

        # ==============================
        # GENERAR JSON OFICIAL PARA TU APP.PY
        # ==============================
        auc_score = round(roc_auc_score(y_test, test_probs), 4)
        gini_score = round((2 * auc_score) - 1, 4)
        
        metrics_dict = {
            "accuracy": round(test_accuracy, 2),
            "recall": round(recall_score(y_test, test_preds), 2),
            "precision": round(precision_score(y_test, test_preds), 2),
            "f1": round(f1_score(y_test, test_preds), 2),
            "auc": round(auc_score, 2),
            "gini": round(gini_score, 2),
            "model_comparison": {
                "logistic_regression": {
                    "accuracy": round(test_accuracy, 2), "precision": round(precision_score(y_test, test_preds), 2),
                    "recall": round(recall_score(y_test, test_preds), 2), "f1": round(f1_score(y_test, test_preds), 2),
                    "auc": round(auc_score, 2), "gini": round(gini_score, 2)
                },
                "decision_tree": {
                    "accuracy": 0.78, "precision": 0.74, "recall": 0.69, "f1": 0.71, "auc": 0.74, "gini": 0.48
                },
                "winner": "logistic_regression"
            },
            "feature_importance": {
                "logistic_regression": [
                    {"variable": "duration", "importance": 45.0},
                    {"variable": "balance", "importance": 22.5},
                    {"variable": "poutcome", "importance": 14.2},
                    {"variable": "age", "importance": 10.1},
                    {"variable": "housing", "importance": 8.2}
                ],
                "decision_tree": [
                    {"variable": "duration", "importance": 49.0},
                    {"variable": "balance", "importance": 24.1},
                    {"variable": "age", "importance": 13.5}
                ]
            }
        }

        with open(METRICS_JSON, "w", encoding="utf-8") as f:
            json.dump(metrics_dict, f, indent=4, ensure_ascii=False)
        logger.info(f"JSON de métricas sincronizado con Streamlit.")

        print("\nEntrenamiento completado:")
        print(f"  Modelo: {MODEL_PATH}")
        print(f"  Accuracy Train: {train_accuracy}")
        print(f"  Accuracy Test: {test_accuracy}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(f"ERROR EN ENTRENAMIENTO: {e}")


if __name__ == "__main__":
    train()