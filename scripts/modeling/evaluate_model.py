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
from sklearn.tree import DecisionTreeClassifier

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
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# ==========================
# RUTAS
# ==========================
INPUT = "data/processed/bank_transformed.csv"
MODEL_PATH = "models/bank_model.pkl"
ENCODER_PATH = "models/encoder.pkl"
OUTPUT_JSON = "data/outputs/model_metrics.json"


def calculate_metrics(y_test, predictions, probabilities):
    accuracy  = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall    = recall_score(y_test, predictions, zero_division=0)
    f1        = f1_score(y_test, predictions, zero_division=0)
    auc       = roc_auc_score(y_test, probabilities)
    gini      = (2 * auc) - 1
    return {
        "accuracy":  round(accuracy, 4),
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
        "f1":        round(f1, 4),
        "auc":       round(auc, 4),
        "gini":      round(gini, 4)
    }


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

        remove = [
            "subscription_probability",
            "risk_level",
            "approval_status",
            "premium_client",
            "scoring_reason"
        ]
        existing = [c for c in remove if c in df.columns]
        df = df.drop(columns=existing)

        y = df["deposit"]
        X = df.drop("deposit", axis=1)

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

        if y.dtype == object or str(y.dtype) == "string":
            if "__target__" in encoders:
                y = encoders["__target__"].transform(y.astype(str))
            else:
                le_target = LabelEncoder()
                y = le_target.fit_transform(y.astype(str))
            logger.info("Encoding target aplicado")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.30, random_state=42, stratify=y
        )

        # ==============================
        # MODELO PRINCIPAL: REGRESION LOGISTICA
        # ==============================
        model = joblib.load(MODEL_PATH)
        logger.info(f"Modelo cargado: {MODEL_PATH}")

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        metrics_logreg = calculate_metrics(y_test, predictions, probabilities)

        logger.info(f"[Regresion Logistica] Accuracy:  {metrics_logreg['accuracy']}")
        logger.info(f"[Regresion Logistica] Precision: {metrics_logreg['precision']}")
        logger.info(f"[Regresion Logistica] Recall:    {metrics_logreg['recall']}")
        logger.info(f"[Regresion Logistica] F1:        {metrics_logreg['f1']}")
        logger.info(f"[Regresion Logistica] AUC:       {metrics_logreg['auc']}")
        logger.info(f"[Regresion Logistica] Gini:      {metrics_logreg['gini']}")

        # ==============================
        # MODELO COMPARATIVO: ARBOL DE DECISION
        # Entrenado solo para comparacion,
        # el modelo oficial sigue siendo
        # Regresion Logistica (bank_model.pkl)
        # ==============================
        logger.info("--- Entrenando Arbol de Decision para comparacion ---")
        tree_model = DecisionTreeClassifier(
            max_depth=6,
            random_state=42
        )
        tree_model.fit(X_train, y_train)

        tree_predictions = tree_model.predict(X_test)
        tree_probabilities = tree_model.predict_proba(X_test)[:, 1]

        metrics_tree = calculate_metrics(y_test, tree_predictions, tree_probabilities)

        logger.info(f"[Arbol de Decision] Accuracy:  {metrics_tree['accuracy']}")
        logger.info(f"[Arbol de Decision] Precision: {metrics_tree['precision']}")
        logger.info(f"[Arbol de Decision] Recall:    {metrics_tree['recall']}")
        logger.info(f"[Arbol de Decision] F1:        {metrics_tree['f1']}")
        logger.info(f"[Arbol de Decision] AUC:       {metrics_tree['auc']}")
        logger.info(f"[Arbol de Decision] Gini:      {metrics_tree['gini']}")

        # ==============================
        # IMPORTANCIA DE VARIABLES (en %)
        # ==============================
        feature_names = X.columns.tolist()

        # Regresion Logistica: valor absoluto de coeficientes normalizado a %
        logreg_coefs_abs = [abs(c) for c in model.coef_[0]]
        total_logreg = sum(logreg_coefs_abs)
        logreg_importance = sorted(
            [
                {"feature": f, "importance_pct": round((c / total_logreg) * 100, 2)}
                for f, c in zip(feature_names, logreg_coefs_abs)
            ],
            key=lambda x: x["importance_pct"],
            reverse=True
        )

        # Arbol de Decision: feature_importances_ ya viene normalizado (suma 1.0)
        tree_importance = sorted(
            [
                {"feature": f, "importance_pct": round(i * 100, 2)}
                for f, i in zip(feature_names, tree_model.feature_importances_)
            ],
            key=lambda x: x["importance_pct"],
            reverse=True
        )

        logger.info("--- Importancia de Variables en % (Top 5) ---")
        logger.info("Regresion Logistica:")
        for item in logreg_importance[:5]:
            logger.info(f"  {item['feature']}: {item['importance_pct']}%")
        logger.info("Arbol de Decision:")
        for item in tree_importance[:5]:
            logger.info(f"  {item['feature']}: {item['importance_pct']}%")

        # ==============================
        # GUARDAR AMBOS RESULTADOS
        # ==============================
        metrics = {
            **metrics_logreg,
            "model_comparison": {
                "logistic_regression": metrics_logreg,
                "decision_tree": metrics_tree,
                "winner": "logistic_regression" if metrics_logreg["auc"] >= metrics_tree["auc"] else "decision_tree"
            },
            "feature_importance": {
                "logistic_regression": logreg_importance,
                "decision_tree": tree_importance
            }
        }

        with open(OUTPUT_JSON, "w") as file:
            json.dump(metrics, file, indent=4)

        logger.info(f"Metricas guardadas: {OUTPUT_JSON}")
        logger.info(f"Modelo ganador (mayor AUC): {metrics['model_comparison']['winner']}")

        # ==============================
        # MATRIZ DE CONFUSION (Regresion Logistica)
        # ==============================
        cm = confusion_matrix(y_test, predictions)
        plt.figure(figsize=(6, 5))
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=model.classes_, yticklabels=model.classes_
        )
        plt.title("Matriz de Confusion - Regresion Logistica")
        plt.xlabel("Prediccion")
        plt.ylabel("Real")
        plt.tight_layout()
        plt.savefig("reports/figures/confusion_matrix.png")
        plt.close()
        logger.info("Matriz de confusion guardada")

        # ==============================
        # CURVA ROC (ambos modelos)
        # ==============================
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        fpr_tree, tpr_tree, _ = roc_curve(y_test, tree_probabilities)

        plt.figure(figsize=(7, 5))
        plt.plot(fpr, tpr, color="steelblue",
                 label=f"Regresion Logistica (AUC={metrics_logreg['auc']})")
        plt.plot(fpr_tree, tpr_tree, color="coral",
                 label=f"Arbol de Decision (AUC={metrics_tree['auc']})")
        plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Curva ROC - Comparacion de Modelos")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig("reports/figures/roc_curve.png")
        plt.close()
        logger.info("Curva ROC guardada (comparativa)")

        print("\nEvaluacion finalizada:")
        print("Regresion Logistica:")
        for k, v in metrics_logreg.items():
            print(f"  {k}: {v}")
        print("Arbol de Decision:")
        for k, v in metrics_tree.items():
            print(f"  {k}: {v}")
        print(f"Modelo ganador: {metrics['model_comparison']['winner']}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    evaluate()