
# ============================================
# scripts/load/loading_data.py
# ============================================

import pandas as pd
import logging
import os
import time

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import text

from utils.pipeline_logger import *

# ============================================
# CARGAR ENV
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
    format="%(asctime)s - %(levelname)s - %(message)s"
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
# DATABASE
# ============================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
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

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO CARGA"
        )

        logging.info(
            "==================================="
        )

        log_section(
            "ETAPA 5 - CARGA"
        )

        log_message(
            "Inicio proceso carga"
        )

        # ============================================
        # VALIDAR DATABASE URL
        # ============================================

        if not DATABASE_URL:

            raise ValueError(
                "DATABASE_URL no encontrada"
            )

        log_message(
            "DATABASE_URL encontrada"
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
            "Archivos CSV cargados correctamente"
        )

        log_message(
            f"Clientes aprobados recibidos: "
            f"{len(approved_df)}"
        )

        log_message(
            f"Clientes premium recibidos: "
            f"{len(premium_df)}"
        )

        log_message(
            f"Clientes rechazados recibidos: "
            f"{len(rejected_df)}"
        )

        # ============================================
        # CONEXIÓN
        # ============================================

        engine = create_engine(
            DATABASE_URL
        )

        log_message(
            "Conexión a PostgreSQL creada"
        )

        # ============================================
        # ELIMINAR TABLAS
        # ============================================

        with engine.connect() as conn:

            conn.execute(text(
                """
                DROP TABLE IF EXISTS
                clientes_aprobados;
                """
            ))

            conn.execute(text(
                """
                DROP TABLE IF EXISTS
                clientes_premium;
                """
            ))

            conn.execute(text(
                """
                DROP TABLE IF EXISTS
                clientes_rechazados;
                """
            ))

            conn.commit()

        logging.info(
            "Tablas eliminadas correctamente"
        )

        log_message(
            "Tablas anteriores eliminadas"
        )

        # ============================================
        # CARGAR TABLAS
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

        log_message(
            "Tablas cargadas en PostgreSQL"
        )

        log_list(
            "Tablas creadas",
            [
                "clientes_aprobados",
                "clientes_premium",
                "clientes_rechazados"
            ]
        )

        # ============================================
        # KPIs
        # ============================================

        approved_count = len(
            approved_df
        )

        premium_count = len(
            premium_df
        )

        rejected_count = len(
            rejected_df
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

            approved_df[
                "subscription_probability"
            ].mean(),

            2

        )

        # ============================================
        # LOGGING NORMAL
        # ============================================

        logging.info(
            "==================================="
        )

        logging.info(
            "CARGA COMPLETADA"
        )

        logging.info(
            "==================================="
        )

        logging.info(
            f"Clientes aprobados: "
            f"{approved_count}"
        )

        logging.info(
            f"Clientes premium: "
            f"{premium_count}"
        )

        logging.info(
            f"Clientes rechazados: "
            f"{rejected_count}"
        )

        logging.info(
            f"Tasa aprobación: "
            f"{approval_rate}%"
        )

        logging.info(
            f"Tasa premium: "
            f"{premium_rate}%"
        )

        logging.info(
            f"Tasa rechazo: "
            f"{rejection_rate}%"
        )

        logging.info(
            f"Probabilidad promedio: "
            f"{avg_probability}%"
        )

        # ============================================
        # REPORTE GLOBAL
        # ============================================

        log_message(
            f"Clientes aprobados: "
            f"{approved_count}"
        )

        log_message(
            f"Clientes premium: "
            f"{premium_count}"
        )

        log_message(
            f"Clientes rechazados: "
            f"{rejected_count}"
        )

        log_message(
            f"Tasa aprobación: "
            f"{approval_rate}%"
        )

        log_message(
            f"Tasa premium: "
            f"{premium_rate}%"
        )

        log_message(
            f"Tasa rechazo: "
            f"{rejection_rate}%"
        )

        log_message(
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
        # TIEMPO EJECUCIÓN
        # ============================================

        log_execution_time(
            "CARGA",
            start_time
        )

        log_message(
            "==================================="
        )

        log_message(
            "FIN CARGA"
        )

        log_message(
            "==================================="
        )

        # ============================================
        # PRINTS
        # ============================================

        print(
            "==================================="
        )

        print(
            "CARGA COMPLETADA"
        )

        print(
            "==================================="
        )

        print(
            f"Clientes aprobados: "
            f"{approved_count}"
        )

        print(
            f"Clientes premium: "
            f"{premium_count}"
        )

        print(
            f"Clientes rechazados: "
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

        print(
            f"Probabilidad promedio: "
            f"{avg_probability}%"
        )

        print(
            "Tablas creadas:"
        )

        print(
            "- clientes_aprobados"
        )

        print(
            "- clientes_premium"
        )

        print(
            "- clientes_rechazados"
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

