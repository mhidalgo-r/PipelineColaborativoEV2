# ============================================
# scripts/transform/transform_data.py
# ============================================

import pandas as pd
import logging
import os
import time

from utils.pipeline_logger import *

# ============================================
# CREAR CARPETAS
# ============================================

os.makedirs(
    "logs",
    exist_ok=True
)

os.makedirs(
    "data/processed",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    filename="logs/transformation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = (
    "data/processed/bank_cleaned.csv"
)

OUTPUT_PATH = (
    "data/processed/bank_transformed.csv"
)

# ============================================
# TRANSFORMACIÓN
# ============================================

def transform_data():

    try:

        start_time = time.time()

        print(
            "Iniciando transformación..."
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO TRANSFORMACIÓN"
        )

        logging.info(
            "==================================="
        )

        log_section(
            "ETAPA 3 - TRANSFORMACIÓN"
        )

        log_message(
            "Inicio proceso transformación"
        )

        # ============================================
        # LEER DATASET
        # ============================================

        df = pd.read_csv(
            INPUT_PATH
        )

        log_message(
            f"Clientes recibidos: {len(df)}"
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

        for column in binary_columns:

            df[column] = df[column].map({

                "yes": 1,
                "no": 0

            })

        log_message(
            "Conversión variables binarias completada"
        )

        log_list(
            "Variables binarias",
            binary_columns
        )

        # ============================================
        # SEGMENTACIÓN ETARIA
        # ============================================

        df["age_group"] = pd.cut(

            df["age"],

            bins=[
                18,
                30,
                45,
                60,
                100
            ],

            labels=[
                "young",
                "adult",
                "senior",
                "elder"
            ]

        )

        log_message(
            "Segmentación etaria completada"
        )

        # ============================================
        # MOTOR SCORING
        # ============================================

        log_message(
            "Inicio motor scoring comercial"
        )

        probability = []

        risk_level = []

        approval_status = []

        premium_client = []

        scoring_reason = []

        for _, row in df.iterrows():

            score = 50

            reasons = []

            # ============================================
            # BALANCE
            # ============================================

            if row["balance"] > 2000:

                score += 20

                reasons.append(
                    "balance alto"
                )

            elif row["balance"] < 0:

                score -= 15

                reasons.append(
                    "balance negativo"
                )

            # ============================================
            # CLIENTE YA ACEPTÓ DEPÓSITO
            # ============================================

            if row["deposit"] == 1:

                score += 15

                reasons.append(
                    "cliente con depósito previo"
                )

            # ============================================
            # DURACIÓN LLAMADA
            # ============================================

            if row["duration"] > 300:

                score += 15

                reasons.append(
                    "duración llamada alta"
                )

            elif row["duration"] < 100:

                score -= 10

                reasons.append(
                    "duración llamada baja"
                )

            # ============================================
            # PRÉSTAMO PERSONAL
            # ============================================

            if row["loan"] == 1:

                score -= 15

                reasons.append(
                    "cliente con préstamo personal"
                )

            # ============================================
            # CRÉDITO HIPOTECARIO
            # ============================================

            if row["housing"] == 1:

                score += 5

                reasons.append(
                    "cliente hipotecario estable"
                )

            # ============================================
            # DEFAULT
            # ============================================

            if row["default"] == 1:

                score -= 30

                reasons.append(
                    "cliente en default"
                )

            # ============================================
            # RESULTADO CAMPAÑA ANTERIOR
            # ============================================

            if row["poutcome"] == "success":

                score += 25

                reasons.append(
                    "campaña anterior exitosa"
                )

            elif row["poutcome"] == "failure":

                score -= 10

                reasons.append(
                    "campaña anterior fallida"
                )

            # ============================================
            # AJUSTE SCORE
            # ============================================

            score = max(
                0,
                min(score, 100)
            )

            probability.append(
                score
            )

            # ============================================
            # CLASIFICACIÓN
            # ============================================

            if score >= 80:

                risk_level.append(
                    "low"
                )

                approval_status.append(
                    "approved"
                )

                premium_client.append(
                    "yes"
                )

            elif score >= 60:

                risk_level.append(
                    "medium"
                )

                approval_status.append(
                    "approved"
                )

                premium_client.append(
                    "no"
                )

            elif score >= 40:

                risk_level.append(
                    "high"
                )

                approval_status.append(
                    "rejected"
                )

                premium_client.append(
                    "no"
                )

            else:

                risk_level.append(
                    "critical"
                )

                approval_status.append(
                    "rejected"
                )

                premium_client.append(
                    "no"
                )

            # ============================================
            # MOTIVO SCORE
            # ============================================

            if len(reasons) == 0:

                reasons.append(
                    "perfil neutro"
                )

            scoring_reason.append(
                ", ".join(reasons)
            )

        # ============================================
        # NUEVAS COLUMNAS
        # ============================================

        df[
            "subscription_probability"
        ] = probability

        df[
            "risk_level"
        ] = risk_level

        df[
            "approval_status"
        ] = approval_status

        df[
            "premium_client"
        ] = premium_client

        df[
            "scoring_reason"
        ] = scoring_reason

        log_message(
            "Variables enriquecidas agregadas"
        )

        # ============================================
        # KPIs
        # ============================================

        approved_clients = len(

            df[
                df[
                    "approval_status"
                ] == "approved"
            ]

        )

        rejected_clients = len(

            df[
                df[
                    "approval_status"
                ] == "rejected"
            ]

        )

        premium_clients = len(

            df[
                df[
                    "premium_client"
                ] == "yes"
            ]

        )

        approval_rate = round(

            (
                approved_clients /
                len(df)
            ) * 100,

            2

        )

        rejection_rate = round(

            (
                rejected_clients /
                len(df)
            ) * 100,

            2

        )

        premium_rate = round(

            (
                premium_clients /
                approved_clients
            ) * 100,

            2

        )

        avg_probability = round(

            df[
                "subscription_probability"
            ].mean(),

            2

        )

        # ============================================
        # LOG KPIs
        # ============================================

        log_message(
            f"Clientes aprobados: {approved_clients}"
        )

        log_message(
            f"Clientes rechazados: {rejected_clients}"
        )

        log_message(
            f"Clientes premium: {premium_clients}"
        )

        log_message(
            f"Tasa aprobación: {approval_rate}%"
        )

        log_message(
            f"Tasa rechazo: {rejection_rate}%"
        )

        log_message(
            f"Tasa premium: {premium_rate}%"
        )

        log_message(
            f"Probabilidad promedio: {avg_probability}%"
        )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        log_message(
            f"Archivo exportado: {OUTPUT_PATH}"
        )

        # ============================================
        # TIEMPO
        # ============================================

        log_execution_time(
            "TRANSFORMACIÓN",
            start_time
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN TRANSFORMACIÓN"
        )

        logging.info(
            "==================================="
        )

        print(
            "Transformación completada"
        )

    except Exception as e:

        logging.error(
            f"ERROR TRANSFORMACIÓN: {e}"
        )

        log_error(
            f"ERROR TRANSFORMACIÓN: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    transform_data()