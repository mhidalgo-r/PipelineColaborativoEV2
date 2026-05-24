# ============================================
# scripts/validation/validation_data.py
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
    "data/validated",
    exist_ok=True
)

os.makedirs(
    "data/reject",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    filename="logs/validation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = (
    "data/processed/bank_transformed.csv"
)

APPROVED_PATH = (
    "data/validated/bank_validated.csv"
)

PREMIUM_PATH = (
    "data/validated/bank_premium.csv"
)

REJECTED_PATH = (
    "data/reject/bank_rejected.csv"
)

# ============================================
# VALIDACIÓN
# ============================================

def validate_data():

    try:

        start_time = time.time()

        print(
            "Iniciando validación..."
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO VALIDACIÓN"
        )

        logging.info(
            "==================================="
        )

        log_section(
            "ETAPA 4 - VALIDACIÓN"
        )

        log_message(
            "Inicio proceso validación"
        )

        # ============================================
        # LEER DATASET
        # ============================================

        df = pd.read_csv(
            INPUT_PATH
        )

        log_message(
            f"Dataset cargado: {INPUT_PATH}"
        )

        log_message(
            f"Total registros recibidos: {len(df)}"
        )

        # ============================================
        # VALIDACIÓN ESTRUCTURAL
        # ============================================

        valid_df = df[

            (df["age"] >= 18) &
            (df["age"] <= 85) &
            (df["day"] >= 1) &
            (df["day"] <= 31) &
            (df["duration"] >= 0) &
            (df["campaign"] >= 0) &
            (df["previous"] >= 0) &
            (df["pdays"] >= -1) &
            (
                df[
                    "subscription_probability"
                ].between(0, 100)
            )

        ]

        rejected_structural = df[
            ~df.index.isin(valid_df.index)
        ].copy()

        rejected_structural[
            "validation_reason"
        ] = (
            "Error validación estructural"
        )

        # ============================================
        # APROBADOS
        # ============================================

        approved_clients = valid_df[
            valid_df[
                "approval_status"
            ] == "approved"
        ].copy()

        approved_clients[
            "validation_reason"
        ] = (
            "Aprobado | score="
            + approved_clients[
                "subscription_probability"
            ].astype(str)
            + " | "
            + approved_clients[
                "scoring_reason"
            ]
        )

        # ============================================
        # RECHAZADOS NEGOCIO
        # ============================================

        rejected_business = valid_df[
            valid_df[
                "approval_status"
            ] == "rejected"
        ].copy()

        rejected_business[
            "validation_reason"
        ] = (
            "Rechazado | score="
            + rejected_business[
                "subscription_probability"
            ].astype(str)
            + " | "
            + rejected_business[
                "scoring_reason"
            ]
        )

        # ============================================
        # CONCATENAR RECHAZADOS
        # ============================================

        rejected_clients = pd.concat([

            rejected_structural,
            rejected_business

        ])

        # ============================================
        # PREMIUM
        # ============================================

        premium_clients = approved_clients[
            approved_clients[
                "premium_client"
            ] == "yes"
        ].copy()

        premium_clients[
            "validation_reason"
        ] = (
            "Cliente premium | score="
            + premium_clients[
                "subscription_probability"
            ].astype(str)
            + " | "
            + premium_clients[
                "scoring_reason"
            ]
        )

        # ============================================
        # DUPLICADOS
        # ============================================

        approved_clients = (
            approved_clients
            .drop_duplicates()
        )

        rejected_clients = (
            rejected_clients
            .drop_duplicates()
        )

        premium_clients = (
            premium_clients
            .drop_duplicates()
        )

        # ============================================
        # KPIs
        # ============================================

        approved_count = len(
            approved_clients
        )

        rejected_count = len(
            rejected_clients
        )

        premium_count = len(
            premium_clients
        )

        total_clients = (
            approved_count +
            rejected_count
        )

        approval_rate = round(
            (
                approved_count /
                total_clients
            ) * 100,
            2
        )

        rejection_rate = round(
            (
                rejected_count /
                total_clients
            ) * 100,
            2
        )

        premium_rate = round(
            (
                premium_count /
                approved_count
            ) * 100,
            2
        )

        avg_probability = round(
            approved_clients[
                "subscription_probability"
            ].mean(),
            2
        )

        # ============================================
        # LOGS
        # ============================================

        log_message(
            f"Clientes aprobados: {approved_count}"
        )

        log_message(
            f"Clientes rechazados: {rejected_count}"
        )

        log_message(
            f"Clientes premium: {premium_count}"
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

        approved_clients.to_csv(
            APPROVED_PATH,
            index=False
        )

        premium_clients.to_csv(
            PREMIUM_PATH,
            index=False
        )

        rejected_clients.to_csv(
            REJECTED_PATH,
            index=False
        )

        log_message(
            f"Archivo aprobados: {APPROVED_PATH}"
        )

        log_message(
            f"Archivo premium: {PREMIUM_PATH}"
        )

        log_message(
            f"Archivo rechazados: {REJECTED_PATH}"
        )

        # ============================================
        # TIEMPO
        # ============================================

        log_execution_time(
            "VALIDACIÓN",
            start_time
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN VALIDACIÓN"
        )

        logging.info(
            "==================================="
        )

        print(
            "Validación completada"
        )

    except Exception as e:

        logging.error(
            f"ERROR VALIDACIÓN: {e}"
        )

        log_error(
            f"ERROR VALIDACIÓN: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    validate_data()