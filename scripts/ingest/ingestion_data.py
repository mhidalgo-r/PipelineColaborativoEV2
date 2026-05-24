# ============================================
# scripts/ingest/ingestion_data.py
# ============================================

import pandas as pd
import logging
import os
import time

from utils.pipeline_logger import *

# ============================================
# CARPETAS
# ============================================

os.makedirs(
    "logs",
    exist_ok=True
)

os.makedirs(
    "data/raw",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = (
    "data/source/02_bank.csv"
)

OUTPUT_PATH = (
    "data/raw/02_bank.csv"
)

# ============================================
# INGESTA
# ============================================

def ingest_data():

    try:

        start_time = time.time()

        print(
            "Iniciando proceso de ingesta..."
        )

        log_section(
            "ETAPA 1 - INGESTA"
        )

        log_message(
            "Inicio proceso ingesta"
        )

        # ============================================
        # VALIDAR ARCHIVO
        # ============================================

        if not os.path.exists(
            INPUT_PATH
        ):

            raise FileNotFoundError(
                f"No existe: {INPUT_PATH}"
            )

        log_message(
            "Archivo origen encontrado"
        )

        log_message(
            f"Ruta origen: {INPUT_PATH}"
        )

        # ============================================
        # LEER CSV
        # ============================================

        df = pd.read_csv(
            INPUT_PATH
        )

        log_message(
            "Lectura CSV completada"
        )

        # ============================================
        # VALIDAR COLUMNAS
        # ============================================

        required_columns = [

            "age",
            "job",
            "balance",
            "deposit"

        ]

        for col in required_columns:

            if col not in df.columns:

                raise Exception(
                    f"Falta columna: {col}"
                )

        log_message(
            "Columnas obligatorias validadas"
        )

        log_list(
            "Columnas dataset",
            df.columns.tolist()
        )

        # ============================================
        # KPIs
        # ============================================

        total_clients = len(df)

        yes_clients = len(
            df[
                df["deposit"] == "yes"
            ]
        )

        no_clients = len(
            df[
                df["deposit"] == "no"
            ]
        )

        conversion_rate = round(

            (
                yes_clients /
                total_clients
            ) * 100,

            2

        )

        avg_balance = round(

            df["balance"].mean(),

            2

        )

        avg_age = round(

            df["age"].mean(),

            2

        )

        # ============================================
        # LOG KPIs
        # ============================================

        log_metric(
            "Clientes totales",
            total_clients
        )

        log_metric(
            "Clientes depósito YES",
            yes_clients
        )

        log_metric(
            "Clientes depósito NO",
            no_clients
        )

        log_metric(
            "Tasa conversión inicial",
            f"{conversion_rate}%"
        )

        log_metric(
            "Balance promedio",
            avg_balance
        )

        log_metric(
            "Edad promedio",
            avg_age
        )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        log_message(
            "Archivo RAW exportado"
        )

        log_message(
            f"Ruta salida: {OUTPUT_PATH}"
        )

        # ============================================
        # TIEMPO
        # ============================================

        log_execution_time(
            "INGESTA",
            start_time
        )

        log_message(
            "FIN INGESTA"
        )

        print(
            "Ingesta completada correctamente"
        )

    except Exception as e:

        log_error(
            f"ERROR INGESTA: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    ingest_data()