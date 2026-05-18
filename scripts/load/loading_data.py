# ============================================
# loading_data.py
# ============================================

import pandas as pd
import logging
import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

# ============================================
# VARIABLES ENTORNO
# ============================================

load_dotenv()

# ============================================
# CREAR LOGS
# ============================================

os.makedirs(
    "logs",
    exist_ok=True
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    filename='logs/loading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# PATHS
# ============================================

APPROVED_PATH = (
    "data/validated/bank_validated.csv"
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

        print(
            "Iniciando carga..."
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "INICIO LOAD"
        )

        logging.info(
            "==================================="
        )

        # ============================================
        # VALIDAR DB
        # ============================================

        if not DATABASE_URL:

            raise ValueError(
                "DATABASE_URL no encontrada"
            )

        logging.info(
            "DATABASE_URL encontrada"
        )

        # ============================================
        # LEER CSV
        # ============================================

        approved_df = pd.read_csv(
            APPROVED_PATH
        )

        rejected_df = pd.read_csv(
            REJECTED_PATH
        )

        logging.info(
            f"Clientes aprobados: "
            f"{approved_df.shape[0]}"
        )

        logging.info(
            f"Clientes rechazados: "
            f"{rejected_df.shape[0]}"
        )

        # ============================================
        # ENGINE
        # ============================================

        engine = create_engine(
            DATABASE_URL
        )

        logging.info(
            "Conexión PostgreSQL creada"
        )

        # ============================================
        # RENOMBRAR DEFAULT
        # ============================================

        approved_df.rename(

            columns={
                'default': 'default_credit'
            },

            inplace=True

        )

        rejected_df.rename(

            columns={
                'default': 'default_credit'
            },

            inplace=True

        )

        # ============================================
        # TABLA APROBADOS
        # ============================================

        approved_df.to_sql(

            name='clientes_aprobados',

            con=engine,

            if_exists='replace',

            index=False

        )

        logging.info(
            "Tabla clientes_aprobados creada"
        )

        # ============================================
        # TABLA RECHAZADOS
        # ============================================

        rejected_df.to_sql(

            name='clientes_rechazados',

            con=engine,

            if_exists='replace',

            index=False

        )

        logging.info(
            "Tabla clientes_rechazados creada"
        )

        # ============================================
        # MÉTRICAS
        # ============================================

        total_clientes = (

            approved_df.shape[0]

            +

            rejected_df.shape[0]

        )

        tasa_aprobacion = round(

            (
                approved_df.shape[0]
                /
                total_clientes
            ) * 100,

            2

        )

        tasa_rechazo = round(

            (
                rejected_df.shape[0]
                /
                total_clientes
            ) * 100,

            2

        )

        logging.info(
            f"Tasa aprobación: "
            f"{tasa_aprobacion}%"
        )

        logging.info(
            f"Tasa rechazo: "
            f"{tasa_rechazo}%"
        )

        # ============================================
        # FINALIZAR
        # ============================================

        logging.info(
            "Carga completada correctamente"
        )

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
            f"{approved_df.shape[0]}"
        )

        print(
            f"Clientes rechazados: "
            f"{rejected_df.shape[0]}"
        )

        print(
            f"Tasa aprobación: "
            f"{tasa_aprobacion}%"
        )

        print(
            f"Tasa rechazo: "
            f"{tasa_rechazo}%"
        )

        print(
            "Tablas creadas:"
        )

        print(
            "- clientes_aprobados"
        )

        print(
            "- clientes_rechazados"
        )

    except Exception as e:

        logging.error(
            f"Error carga: {e}"
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