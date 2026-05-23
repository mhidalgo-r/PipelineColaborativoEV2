# ============================================
# scripts/transform/transform_data.py
# ============================================

import pandas as pd
import logging
import os
import time

# ============================================
# PIPELINE LOGGER
# ============================================

from utils.pipeline_logger import *

# ============================================
# CARPETAS
# ============================================

os.makedirs("logs", exist_ok=True)

# ============================================
# LOGGING INDIVIDUAL
# ============================================

logging.basicConfig(
    filename="logs/transformation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = "data/processed/bank_cleaned.csv"

OUTPUT_PATH = "data/processed/bank_transformed.csv"

# ============================================
# TRANSFORMACIÓN
# ============================================

def transform_data():

    start_time = time.time()

    try:

        print("Iniciando transformación...")

        # ============================================
        # LOG INDIVIDUAL
        # ============================================

        logging.info("===================================")
        logging.info("INICIO TRANSFORMACIÓN")
        logging.info("===================================")

        # ============================================
        # LOG GLOBAL PIPELINE
        # ============================================

        log_section(
            "ETAPA 3 - TRANSFORMACIÓN"
        )

        log_message(
            "Inicio proceso transformación"
        )

        # ============================================
        # LEER DATASET
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        total_clients = len(df)

        logging.info(
            f"Clientes recibidos: {total_clients}"
        )

        log_metric(
            "Clientes recibidos",
            total_clients
        )

        # ============================================
        # VARIABLES BINARIAS
        # ============================================

        binary_columns = [
            "default",
            "housing",
            "loan",
            "deposit"
        ]

        for col in binary_columns:

            df[col] = df[col].map({
                "yes": 1,
                "no": 0
            })

        logging.info(
            "Variables binarias transformadas"
        )

        log_message(
            "Conversión variables binarias completada"
        )

        log_list(
            "Variables binarias",
            binary_columns
        )

        # ============================================
        # GRUPOS ETARIOS
        # ============================================

        df["age_group"] = pd.cut(

            df["age"],

            bins=[18, 25, 40, 60, 85],

            labels=[
                "young",
                "adult",
                "mature",
                "senior"
            ]

        )

        logging.info(
            "Grupos etarios generados"
        )

        log_message(
            "Segmentación etaria completada"
        )

        # ============================================
        # VARIABLES NUEVAS
        # ============================================

        probabilities = []
        warnings_list = []
        risk_levels = []
        approvals = []
        rejection_reasons = []
        premium_clients = []

        # ============================================
        # SCORING
        # ============================================

        log_message(
            "Inicio motor scoring bancario"
        )

        for _, row in df.iterrows():

            probability = 50
            warnings = 0
            reasons = []

            # ============================================
            # AGE
            # ============================================

            if row["age"] > 85:

                probability = 0

                warnings += 999

                reasons.append(
                    "Edad mayor a 85 años"
                )

            elif 30 <= row["age"] <= 55:

                probability += 10

            elif row["age"] >= 75:

                probability -= 20

                warnings += 2

            # ============================================
            # JOB
            # ============================================

            good_jobs = [

                "admin.",
                "management",
                "technician",
                "entrepreneur"

            ]

            risky_jobs = [
                "unemployed",
                "unknown"
            ]

            if row["job"] in good_jobs:

                probability += 15

            elif row["job"] in risky_jobs:

                probability -= 20

                warnings += 2

                reasons.append(
                    "Trabajo riesgoso"
                )

            # ============================================
            # EDUCATION
            # ============================================

            if row["education"] == "tertiary":

                probability += 10

            elif row["education"] == "primary":

                probability -= 5

            elif row["education"] == "unknown":

                warnings += 1

            # ============================================
            # BALANCE
            # ============================================

            if row["balance"] < 0:

                probability -= 30

                warnings += 3

                reasons.append(
                    "Balance negativo"
                )

            elif row["balance"] >= 5000:

                probability += 15

            elif row["balance"] >= 1000:

                probability += 8

            # ============================================
            # DEFAULT
            # ============================================

            if row["default"] == 1:

                probability -= 40

                warnings += 3

                reasons.append(
                    "Cliente con default"
                )

            # ============================================
            # PRÉSTAMOS
            # ============================================

            if (
                row["default"] == 1 and
                row["housing"] == 1 and
                row["loan"] == 1
            ):

                probability = 0

                warnings += 999

                reasons.append(
                    "Default y múltiples préstamos"
                )

            if row["housing"] == 1:

                probability -= 10

                warnings += 1

            if row["loan"] == 1:

                probability -= 15

                warnings += 1

            # ============================================
            # CONTACT
            # ============================================

            if row["contact"] == "cellular":

                probability += 10

            elif row["contact"] == "telephone":

                probability += 5

            else:

                probability -= 10

                warnings += 2

                reasons.append(
                    "Contacto desconocido"
                )

            # ============================================
            # DURACIÓN
            # ============================================

            if row["duration"] >= 300:

                probability += 20

            elif row["duration"] < 60:

                probability -= 10

                warnings += 1

            # ============================================
            # CAMPAIGN
            # ============================================

            if row["campaign"] > 10:

                probability -= 15

                warnings += 2

                reasons.append(
                    "Demasiados contactos"
                )

            elif row["campaign"] <= 3:

                probability += 5

            # ============================================
            # RESULTADO ANTERIOR
            # ============================================

            if row["poutcome"] == "success":

                probability += 20

            elif row["poutcome"] == "failure":

                probability -= 10

            # ============================================
            # LIMITAR %
            # ============================================

            probability = max(
                0,
                min(probability, 100)
            )

            probabilities.append(
                probability
            )

            warnings_list.append(
                warnings
            )

            # ============================================
            # RISK LEVEL
            # ============================================

            if warnings >= 999:

                risk = "critical"

            elif warnings >= 6:

                risk = "high"

            elif warnings >= 3:

                risk = "medium"

            else:

                risk = "low"

            risk_levels.append(risk)

            # ============================================
            # APROBACIÓN
            # ============================================

            if probability >= 70:

                approval = "approved"

            elif risk == "critical":

                approval = "rejected"

            elif warnings >= 6:

                approval = "rejected"

            else:

                approval = "approved"

            approvals.append(
                approval
            )

            # ============================================
            # CLIENTE PREMIUM
            # ============================================

            if (
                probability >= 85 and
                warnings <= 1 and
                row["balance"] >= 5000
            ):

                premium_clients.append(
                    "yes"
                )

            else:

                premium_clients.append(
                    "no"
                )

            # ============================================
            # MOTIVO RECHAZO
            # ============================================

            if len(reasons) == 0:

                rejection_reasons.append(
                    "Sin observaciones"
                )

            else:

                rejection_reasons.append(
                    ", ".join(reasons)
                )

        # ============================================
        # NUEVAS COLUMNAS
        # ============================================

        df["subscription_probability"] = probabilities

        df["warning_count"] = warnings_list

        df["risk_level"] = risk_levels

        df["approval_status"] = approvals

        df["rejection_reason"] = rejection_reasons

        df["premium_client"] = premium_clients

        logging.info(
            "Variables derivadas generadas"
        )

        log_message(
            "Variables enriquecidas agregadas"
        )

        # ============================================
        # KPIs
        # ============================================

        approved = len(
            df[
                df["approval_status"] == "approved"
            ]
        )

        rejected = len(
            df[
                df["approval_status"] == "rejected"
            ]
        )

        premium = len(
            df[
                df["premium_client"] == "yes"
            ]
        )

        total = len(df)

        approval_rate = round(
            (approved / total) * 100,
            2
        )

        rejection_rate = round(
            (rejected / total) * 100,
            2
        )

        premium_rate = round(
            (premium / approved) * 100,
            2
        )

        avg_probability = round(

            df[
                "subscription_probability"
            ].mean(),

            2

        )

        # ============================================
        # LOG KPIs INDIVIDUALES
        # ============================================

        logging.info(
            f"Tasa aprobación: {approval_rate}%"
        )

        logging.info(
            f"Tasa rechazo: {rejection_rate}%"
        )

        logging.info(
            f"Tasa premium: {premium_rate}%"
        )

        logging.info(
            f"Probabilidad promedio: {avg_probability}%"
        )

        # ============================================
        # LOG KPIs GLOBALES
        # ============================================

        log_metric(
            "Clientes aprobados",
            approved
        )

        log_metric(
            "Clientes rechazados",
            rejected
        )

        log_metric(
            "Clientes premium",
            premium
        )

        log_metric(
            "Tasa aprobación",
            f"{approval_rate}%"
        )

        log_metric(
            "Tasa rechazo",
            f"{rejection_rate}%"
        )

        log_metric(
            "Tasa premium",
            f"{premium_rate}%"
        )

        log_metric(
            "Probabilidad promedio",
            f"{avg_probability}%"
        )

        # ============================================
        # ALERTAS
        # ============================================

        if rejection_rate > 20:

            logging.warning(
                "ALERTA: Alta tasa rechazo"
            )

            log_message(
                "ALERTA DETECTADA: Alta tasa rechazo"
            )

        if avg_probability < 40:

            logging.warning(
                "ALERTA: Baja probabilidad promedio"
            )

            log_message(
                "ALERTA DETECTADA: Baja probabilidad promedio"
            )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Archivo exportado: {OUTPUT_PATH}"
        )

        log_message(
            "Dataset transformado exportado"
        )

        log_metric(
            "Ruta salida",
            OUTPUT_PATH
        )

        # ============================================
        # TIEMPO EJECUCIÓN
        # ============================================

        log_execution_time(
            "TRANSFORMACIÓN",
            start_time
        )

        # ============================================
        # FIN LOG INDIVIDUAL
        # ============================================

        logging.info("===================================")
        logging.info("FIN TRANSFORMACIÓN")
        logging.info("===================================")

        # ============================================
        # PRINTS
        # ============================================

        print("Transformación completada")

        print(
            f"Clientes aprobados: {approved}"
        )

        print(
            f"Clientes rechazados: {rejected}"
        )

        print(
            f"Clientes premium: {premium}"
        )

        print(
            f"Probabilidad promedio: {avg_probability}%"
        )

    except Exception as e:

        logging.error(
            f"ERROR TRANSFORMACIÓN: {e}"
        )

        log_error(
            f"ERROR TRANSFORMACIÓN: {e}"
        )

        print(f"ERROR: {e}")

        raise

if __name__ == "__main__":
    transform_data()