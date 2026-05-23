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
    format="%(asctime)s - %(levelname)s - %(message)s"
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

        # ============================================
        # PIPELINE REPORT
        # ============================================

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

        logging.info(
            "Dataset transformado cargado"
        )

        log_message(
            f"Dataset cargado: {INPUT_PATH}"
        )

        log_message(
            f"Total registros recibidos: {len(df)}"
        )

        # ============================================
        # VALIDACIONES ESTRUCTURALES
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

        log_message(
            f"Registros válidos: {len(valid_df)}"
        )

        # ============================================
        # RECHAZADOS ESTRUCTURALES
        # ============================================

        rejected_structural = df[
            ~df.index.isin(valid_df.index)
        ]

        log_message(
            f"Rechazos estructurales: "
            f"{len(rejected_structural)}"
        )

        # ============================================
        # CLIENTES APROBADOS
        # ============================================

        approved_clients = valid_df[

            valid_df[
                "approval_status"
            ] == "approved"

        ]

        # ============================================
        # CLIENTES RECHAZADOS
        # ============================================

        rejected_clients = pd.concat([

            rejected_structural,

            valid_df[

                valid_df[
                    "approval_status"
                ] == "rejected"

            ]

        ])

        # ============================================
        # CLIENTES PREMIUM
        # SOLO CLIENTES CON premium_client == yes
        # ============================================

        premium_clients = approved_clients[

            approved_clients[
                "premium_client"
            ] == "yes"

        ]

        # ============================================
        # ELIMINAR DUPLICADOS
        # ============================================

        approved_before = len(
            approved_clients
        )

        rejected_before = len(
            rejected_clients
        )

        premium_before = len(
            premium_clients
        )

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

        log_message(
            f"Duplicados eliminados aprobados: "
            f"{approved_before - len(approved_clients)}"
        )

        log_message(
            f"Duplicados eliminados rechazados: "
            f"{rejected_before - len(rejected_clients)}"
        )

        log_message(
            f"Duplicados eliminados premium: "
            f"{premium_before - len(premium_clients)}"
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

        avg_premium_probability = round(

            premium_clients[
                "subscription_probability"
            ].mean(),

            2

        )

        # ============================================
        # LOG KPIs
        # ============================================

        log_message(
            f"Clientes aprobados: "
            f"{approved_count}"
        )

        log_message(
            f"Clientes rechazados: "
            f"{rejected_count}"
        )

        log_message(
            f"Clientes premium: "
            f"{premium_count}"
        )

        log_message(
            f"Tasa aprobación: "
            f"{approval_rate}%"
        )

        log_message(
            f"Tasa rechazo: "
            f"{rejection_rate}%"
        )

        log_message(
            f"Tasa premium: "
            f"{premium_rate}%"
        )

        log_message(
            f"Probabilidad promedio: "
            f"{avg_probability}%"
        )

        log_message(
            f"Probabilidad promedio premium: "
            f"{avg_premium_probability}%"
        )

        # ============================================
        # ALERTAS
        # ============================================

        if rejection_rate > 20:

            logging.warning(
                "ALERTA: Alta tasa rechazo"
            )

            log_message(
                "ALERTA: Alta tasa rechazo"
            )

        if premium_rate < 20:

            logging.warning(
                "ALERTA: Baja tasa premium"
            )

            log_message(
                "ALERTA: Baja tasa premium"
            )

        # ============================================
        # EXPORTAR CSV
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

        logging.info(
            "CSV exportados correctamente"
        )

        log_message(
            f"Archivo exportado: {APPROVED_PATH}"
        )

        log_message(
            f"Archivo exportado: {PREMIUM_PATH}"
        )

        log_message(
            f"Archivo exportado: {REJECTED_PATH}"
        )

        # ============================================
        # TIEMPO EJECUCIÓN
        # ============================================

        log_execution_time(
            "VALIDACIÓN",
            start_time
        )

        # ============================================
        # FIN VALIDACIÓN
        # ============================================

        log_message(
            "==================================="
        )

        log_message(
            "FIN VALIDACIÓN"
        )

        log_message(
            "==================================="
        )

        # ============================================
        # PRINTS
        # ============================================

        print(
            "Validación completada"
        )

        print(
            f"Aprobados: "
            f"{approved_count}"
        )

        print(
            f"Premium: "
            f"{premium_count}"
        )

        print(
            f"Rechazados: "
            f"{rejected_count}"
        )

        print(
            f"Tasa aprobación: "
            f"{approval_rate}%"
        )

        print(
            f"Tasa premium: "
            f"{premium_rate}%"
        )

        print(
            f"Tasa rechazo: "
            f"{rejection_rate}%"
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