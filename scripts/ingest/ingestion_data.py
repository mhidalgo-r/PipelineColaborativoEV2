# ============================================
# scripts/ingest/ingestion_data.py
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
# CREAR CARPETAS
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
# LOGGING INDIVIDUAL
# ============================================

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================
# PATHS
# ============================================

# DATASET ORIGINAL
SOURCE_PATH = (
    "data/source/02_bank.csv"
)

# DATASET RAW
OUTPUT_PATH = (
    "data/raw/02_bank.csv"
)

# ============================================
# COLUMNAS OBLIGATORIAS
# ============================================

REQUIRED_COLUMNS = [

    "age",
    "job",
    "marital",
    "education",
    "default",
    "balance",
    "housing",
    "loan",
    "contact",
    "day",
    "month",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "deposit"

]

# ============================================
# INGESTA
# ============================================

def ingest_data():

    start_time = time.time()

    try:

        print(
            "Iniciando proceso de ingesta..."
        )

        # ============================================
        # LOG INDIVIDUAL
        # ============================================

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO INGESTA"
        )

        logging.info(
            "==================================="
        )

        # ============================================
        # LOG GLOBAL PIPELINE
        # ============================================

        start_pipeline()

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
            SOURCE_PATH
        ):

            raise FileNotFoundError(

                f"No existe el archivo: "
                f"{SOURCE_PATH}"

            )

        logging.info(
            "Archivo origen encontrado"
        )

        log_message(
            "Archivo origen encontrado"
        )

        log_metric(
            "Ruta origen",
            SOURCE_PATH
        )

        # ============================================
        # LEER DATASET
        # ============================================

        df = pd.read_csv(
            SOURCE_PATH
        )

        # ============================================
        # VALIDAR DATASET VACÍO
        # ============================================

        if df.empty:

            raise ValueError(
                "El dataset está vacío"
            )

        logging.info(
            "Dataset leído correctamente"
        )

        log_message(
            "Lectura CSV completada"
        )

        # ============================================
        # LIMPIAR NOMBRES COLUMNAS
        # ============================================

        df.columns = (

            df.columns
            .str.strip()
            .str.lower()

        )

        # ============================================
        # VALIDAR COLUMNAS
        # ============================================

        missing_columns = [

            col

            for col in REQUIRED_COLUMNS

            if col not in df.columns

        ]

        if missing_columns:

            raise ValueError(

                f"Faltan columnas "
                f"obligatorias: "
                f"{missing_columns}"

            )

        logging.info(
            "Columnas validadas correctamente"
        )

        log_message(
            "Columnas obligatorias validadas"
        )

        log_list(
            "Columnas dataset",
            list(df.columns)
        )

        # ============================================
        # KPIs INICIALES
        # ============================================

        total_clients = len(df)

        deposit_yes = len(

            df[
                df["deposit"] == "yes"
            ]

        )

        deposit_no = len(

            df[
                df["deposit"] == "no"
            ]

        )

        conversion_rate = round(

            (
                deposit_yes / total_clients
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
        # LOG KPIs INDIVIDUALES
        # ============================================

        logging.info(
            f"Clientes totales: "
            f"{total_clients}"
        )

        logging.info(
            f"Clientes depósito YES: "
            f"{deposit_yes}"
        )

        logging.info(
            f"Clientes depósito NO: "
            f"{deposit_no}"
        )

        logging.info(
            f"Tasa conversión inicial: "
            f"{conversion_rate}%"
        )

        logging.info(
            f"Balance promedio: "
            f"{avg_balance}"
        )

        logging.info(
            f"Edad promedio: "
            f"{avg_age}"
        )

        # ============================================
        # LOG KPIs GLOBALES
        # ============================================

        log_metric(
            "Clientes totales",
            total_clients
        )

        log_metric(
            "Clientes depósito YES",
            deposit_yes
        )

        log_metric(
            "Clientes depósito NO",
            deposit_no
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
        # ALERTAS
        # ============================================

        if conversion_rate < 10:

            logging.warning(
                "ALERTA: Conversión baja"
            )

            log_message(
                "ALERTA DETECTADA: Conversión baja"
            )

        if avg_balance < 0:

            logging.warning(
                "ALERTA: Balance promedio negativo"
            )

            log_message(
                "ALERTA DETECTADA: Balance promedio negativo"
            )

        # ============================================
        # EXPORTAR RAW
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Archivo RAW generado: "
            f"{OUTPUT_PATH}"
        )

        log_message(
            "Archivo RAW exportado"
        )

        log_metric(
            "Ruta salida",
            OUTPUT_PATH
        )

        # ============================================
        # TIEMPO EJECUCIÓN
        # ============================================

        log_execution_time(
            "INGESTA",
            start_time
        )

        # ============================================
        # FIN LOG INDIVIDUAL
        # ============================================

        logging.info(
            "Proceso de ingesta finalizado"
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN INGESTA"
        )

        logging.info(
            "==================================="
        )

        # ============================================
        # PRINTS
        # ============================================

        print(
            "Ingesta completada correctamente"
        )

        print(
            f"Clientes totales: "
            f"{total_clients}"
        )

        print(
            f"Tasa conversión inicial: "
            f"{conversion_rate}%"
        )

        print(
            f"Balance promedio: "
            f"{avg_balance}"
        )

        print(
            f"Edad promedio: "
            f"{avg_age}"
        )

        return df

    except Exception as e:

        logging.error(
            f"ERROR INGESTA: {e}"
        )

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