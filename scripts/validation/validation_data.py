# ============================================
# scripts/validation/validation_data.py
# ============================================

import pandas as pd
import logging
import os

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
        # LEER DATASET
        # ============================================

        df = pd.read_csv(
            INPUT_PATH
        )

        logging.info(
            "Dataset transformado cargado"
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

        # ============================================
        # RECHAZADOS ESTRUCTURALES
        # ============================================

        rejected_structural = df[
            ~df.index.isin(valid_df.index)
        ]

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
        # ============================================

        premium_clients = approved_clients[

            approved_clients[
                "subscription_probability"
            ] >= 80

        ]

        # ============================================
        # ELIMINAR DUPLICADOS
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
        # LOG KPIs
        # ============================================

        logging.info(
            f"Clientes aprobados: "
            f"{approved_count}"
        )

        logging.info(
            f"Clientes rechazados: "
            f"{rejected_count}"
        )

        logging.info(
            f"Clientes premium: "
            f"{premium_count}"
        )

        logging.info(
            f"Tasa aprobación: "
            f"{approval_rate}%"
        )

        logging.info(
            f"Tasa rechazo: "
            f"{rejection_rate}%"
        )

        logging.info(
            f"Tasa premium: "
            f"{premium_rate}%"
        )

        logging.info(
            f"Probabilidad promedio: "
            f"{avg_probability}%"
        )

        # ============================================
        # ALERTAS
        # ============================================

        if rejection_rate > 20:

            logging.warning(
                "ALERTA: Alta tasa rechazo"
            )

        if premium_rate < 20:

            logging.warning(
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

        # ============================================
        # LOG FINAL
        # ============================================

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN VALIDACIÓN"
        )

        logging.info(
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

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    validate_data()