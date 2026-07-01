# ============================================
# scripts/modeling/evaluate_model.py
# ============================================

import pandas as pd
import logging
import os
import time
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score

from utils.pipeline_logger import *

# ============================================
# CREAR CARPETAS
# ============================================
os.makedirs(
    "logs",
    exist_ok=True
)

os.makedirs(
    "reports",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================
logging.basicConfig(
    filename="logs/modeling.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================
# PATHS
# ============================================
INPUT_PREDICTIONS = (
    "data/outputs/model_predictions.csv"
)

# ============================================
# EVALUACIÓN DE MODELO
# ============================================
def evaluate():

    try:

        start_time = time.time()

        print(
            "Iniciando evaluación del modelo predictivo..."
        )

        logging.info(
            "==================================="
        )
        logging.info(
            "INICIO EVALUACIÓN DEL MODELO (IA)"
        )
        logging.info(
            "==================================="
        )

        log_section(
            "ETAPA 9 - EVALUACIÓN DE MODELO"
        )

        log_message(
            "Inicio proceso de auditoría de métricas avanzadas"
        )

        # ============================================
        # VALIDAR EXISTENCIA DE PREDICCIONES
        # ============================================
        if not os.path.exists(INPUT_PREDICTIONS):
            raise FileNotFoundError(
                f"No se encontraron las predicciones en {INPUT_PREDICTIONS}. "
                "Debe ejecutar 'train_model.py' antes de evaluar."
            )

        # ============================================
        # LEER DATASET DE PREDICCIONES
        # ============================================
        # ============================================
        # LEER DATASET DE PREDICCIONES Y PASAR A VECTORES
        # ============================================
        df = pd.read_csv(
            INPUT_PREDICTIONS
        )

        log_message(
            f"Registros de prueba recuperados para evaluación: {len(df)}"
        )

        # 1. Extracción de la variable Real
        y_real = df["real"]
        
        # 2. Extracción de la Probabilidad
        y_prob = df["probability"]

        # 3. Extracción o Cálculo Seguro de la Clase Predicha ('prediction_class')
        if "prediction_class" in df.columns:
            y_pred = df["prediction_class"]
        elif "prediction" in df.columns:
            y_pred = df["prediction"]
        else:
            # Si no existe en el CSV, la calculamos dinámicamente usando el umbral estándar del 50%
            log_message("Columna 'prediction_class' no encontrada en CSV. Calculando dinámicamente basados en probabilidad.")
            y_pred = (df["probability"] >= 0.55).astype(int)
            
        # ============================================
        # CÁLCULO DE KPIs MATEMÁTICOS (MLOps REAL)
        # ============================================
        log_message(
            "Calculando métricas de clasificación supervisada"
        )

        acc_score = round(
            accuracy_score(y_real, y_pred) * 100,
            2
        )

        auc_score = round(
            roc_auc_score(y_real, y_prob),
            4
        )

        gini_score = round(
            (2 * auc_score) - 1,
            4
        )

        f1 = round(
            f1_score(y_real, y_pred) * 100,
            2
        )

        precision = round(
            precision_score(y_real, y_pred) * 100,
            2
        )

        recall = round(
            recall_score(y_real, y_pred) * 100,
            2
        )

        # ============================================
        # LOG KPIs HACIA LOS LOGGERS PROPIOS
        # ============================================
        log_message(
            f"Métrica - Accuracy: {acc_score}%"
        )
        log_message(
            f"Métrica - ROC AUC: {auc_score}"
        )
        log_message(
            f"Métrica - Coeficiente Gini: {gini_score}"
        )
        log_message(
            f"Métrica - F1-Score: {f1}%"
        )
        log_message(
            f"Métrica - Precisión: {precision}%"
        )
        log_message(
            f"Métrica - Recall (Sensibilidad): {recall}%"
        )

        # Lista formal para la estructura de tu pipeline logger si aplica
        metric_keys = ["Accuracy", "AUC", "Gini", "F1-Score", "Precision", "Recall"]
        metric_values = [f"{acc_score}%", str(auc_score), str(gini_score), f"{f1}%", f"{precision}%", f"{recall}%"]
        
        log_list(
            "Resumen Métricas Algorítmicas",
            [f"{k}: {v}" for k, v in zip(metric_keys, metric_values)]
        )

        # ============================================
        # DESPLIEGUE EN CONSOLA (FORMATO EJECUTIVO)
        # ============================================
        print("\n" + "=" * 50)
        print("     AUDITORÍA DE MÉTRICAS MATEMÁTICAS REALES      ")
        print("=" * 50)
        print(f"  [+] Accuracy (Exactitud):       {acc_score}%")
        print(f"  [+] AUC (Área Bajo Curva):       {auc_score}")
        print(f"  [+] Coeficiente Gini de la IA:   {gini_score}")
        print(f"  [+] F1-Score (Equilibrio):       {f1}%")
        print(f"  [+] Precisión Comercial:         {precision}%")
        print(f"  [+] Recall (Sensibilidad):       {recall}%")
        print("=" * 50)
        print("[OK] Verificación matemática completada.")
        print("=" * 50)

        # ============================================
        # TIEMPO
        # ============================================
        log_execution_time(
            "EVALUACIÓN MODELO",
            start_time
        )

        logging.info(
            "==================================="
        )
        logging.info(
            "FIN EVALUACIÓN DEL MODELO"
        )
        logging.info(
            "==================================="
        )

        print(
            "Evaluación completada exitosamente."
        )

    except Exception as e:

        logging.error(
            f"ERROR EVALUACIÓN: {e}"
        )

        log_error(
            f"ERROR EVALUACIÓN: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":

    evaluate()