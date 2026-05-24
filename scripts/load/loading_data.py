# ============================================
# scripts/load/loading_data.py
# ============================================

import pandas as pd
import logging
import os
import time

from sqlalchemy import create_engine
from dotenv import load_dotenv

from utils.pipeline_logger import *

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

# ============================================
# CREAR CARPETAS
# ============================================

os.makedirs(
    "logs",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    filename="logs/loading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ============================================
# DATABASE
# ============================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# ============================================
# PATHS
# ============================================

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
# LOAD
# ============================================

def load_data():

    try:

        start_time = time.time()

        print(
            "Iniciando carga..."
        )

        # ============================================
        # INICIO
        # ============================================

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO LOAD"
        )

        logging.info(
            "==================================="
        )

        log_section(
            "ETAPA 5 - LOAD"
        )

        log_message(
            "Inicio proceso carga"
        )

        # ============================================
        # VALIDAR DATABASE URL
        # ============================================

        if not DATABASE_URL:

            raise Exception(
                "DATABASE_URL no encontrada"
            )

        # ============================================
        # LEER CSV
        # ============================================

        approved_df = pd.read_csv(
            APPROVED_PATH
        )

        premium_df = pd.read_csv(
            PREMIUM_PATH
        )

        rejected_df = pd.read_csv(
            REJECTED_PATH
        )

        log_message(
            f"Aprobados cargados: {len(approved_df)}"
        )

        log_message(
            f"Premium cargados: {len(premium_df)}"
        )

        log_message(
            f"Rechazados cargados: {len(rejected_df)}"
        )

        # ============================================
        # ENGINE SQL
        # ============================================

        engine = create_engine(
            DATABASE_URL
        )

        log_message(
            "Conexión PostgreSQL creada"
        )

        # ============================================
        # INSERTAR TABLAS
        # ============================================

        approved_df.to_sql(

            "clientes_aprobados",

            engine,

            if_exists="replace",

            index=False

        )

        premium_df.to_sql(

            "clientes_premium",

            engine,

            if_exists="replace",

            index=False

        )

        rejected_df.to_sql(

            "clientes_rechazados",

            engine,

            if_exists="replace",

            index=False

        )

        # ============================================
        # LOGS
        # ============================================

        log_message(
            "Tabla clientes_aprobados cargada"
        )

        log_message(
            "Tabla clientes_premium cargada"
        )

        log_message(
            "Tabla clientes_rechazados cargada"
        )

        log_execution_time(
            "LOAD",
            start_time
        )

        # ============================================
        # FIN
        # ============================================

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN LOAD"
        )

        logging.info(
            "==================================="
        )

        print(
            "Carga completada"
        )

    except Exception as e:

        logging.error(
            f"ERROR LOAD: {e}"
        )

        log_error(
            f"ERROR LOAD: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    load_data()