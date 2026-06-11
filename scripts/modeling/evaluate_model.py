import os
import pandas as pd
import logging
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    roc_auc_score
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==========================
# CARPETAS
# ==========================
os.makedirs("reports/figures", exist_ok=True)
os.makedirs("data/outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

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
OUTPUT_JSON = "data/outputs/model_metrics.json"


# ==========================
# MAIN
# ==========================
def evaluate():
    logger.info("=" * 50)
    logger.info("INICIO EVALUACION")
    logger.info("=" * 50)

    try:
        df = pd.read_csv(INPUT)
        logger.info(f"Dataset cargado: {df.shape[0]} filas")

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

        # ==============================
        # TARGET Y FEATURES
        # ==============================
        y = df["deposit"]
        X = df.drop("deposit", axis=1)

        # ==============================
        # CARGAR ENCODERS GUARDADOS
        # ==============================
        encoders = joblib.load(ENCODER_PATH)
        logger.info(f"Encoders cargados: {ENCODER_PATH}")

        categorical = X.select_dtypes(include=["object", "str"]).columns

        for column in categorical:
            if column in encoders:
                le = encoders[column]
                X[column] = le.transform(X[column].astype(str))
            else:
                le = LabelEncoder()
                X[column] = le.fit_transform(X[column].astype(str))
                logger.warning(f"Encoder no encontrado para {column}, se creo nuevo")

        # Encoding target si es string
        if y.dtype == object or str(y.dtype) == "string":
            if "__target__" in encoders:
                y = encoders["__target__"].transform(y.astype(str))
            else:
                le_target = LabelEncoder()
                y = le_target.fit_transform(y.astype(str))
            logger.info("Encoding target aplicado")

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

        # ==============================
        # CARGAR MODELO
        # ==============================
        model = joblib.load(MODEL_PATH)
        logger.info(f"Modelo cargado: {MODEL_PATH}")

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        # ==============================
        # METRICAS
        # ==============================
        accuracy  = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, zero_division=0)
        recall    = recall_score(y_test, predictions, zero_division=0)
        f1        = f1_score(y_test, predictions, zero_division=0)
        auc       = roc_auc_score(y_test, probabilities)
        gini      = (2 * auc) - 1

        metrics = {
            "accuracy":  round(accuracy, 4),
            "precision": round(precision, 4),
            "recall":    round(recall, 4),
            "f1":        round(f1, 4),
            "auc":       round(auc, 4),
            "gini":      round(gini, 4)
        }

        with open(OUTPUT_JSON, "w") as file:
            json.dump(metrics, file, indent=4)

        logger.info(f"Accuracy:  {metrics['accuracy']}")
        logger.info(f"Precision: {metrics['precision']}")
        logger.info(f"Recall:    {metrics['recall']}")
        logger.info(f"F1:        {metrics['f1']}")
        logger.info(f"AUC:       {metrics['auc']}")
        logger.info(f"Gini:      {metrics['gini']}")
        logger.info(f"Metricas guardadas: {OUTPUT_JSON}")

        # ==============================
        # MATRIZ DE CONFUSION
        # ==============================
        cm = confusion_matrix(y_test, predictions)
        plt.figure(figsize=(6, 5))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=model.classes_,
            yticklabels=model.classes_
        )
        plt.title("Matriz de Confusion")
        plt.xlabel("Prediccion")
        plt.ylabel("Real")
        plt.tight_layout()
        plt.savefig("reports/figures/confusion_matrix.png")
        plt.close()
        logger.info("Matriz de confusion guardada")

        # ==============================
        # CURVA ROC
        # ==============================
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        plt.figure(figsize=(7, 5))
        plt.plot(
            fpr, tpr,
            color="steelblue",
            label=f"AUC = {metrics['auc']} | Gini = {metrics['gini']}"
        )
        plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Curva ROC")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig("reports/figures/roc_curve.png")
        plt.close()
        logger.info("Curva ROC guardada")

        print("\nEvaluacion finalizada:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    evaluate()