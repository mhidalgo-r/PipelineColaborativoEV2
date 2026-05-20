# ============================================
# ingestion_data.py
# ============================================

import pandas as pd
import logging
import os

# ============================================
# CREAR CARPETAS
# ============================================

os.makedirs("logs", exist_ok=True)

os.makedirs(
    "data/raw",
    exist_ok=True
)

# ============================================
# CONFIG LOGS
# ============================================

logging.basicConfig(
    filename='logs/ingestion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# PATHS
# ============================================

# DATASET ORIGINAL
SOURCE_PATH = "data/source/02_bank.csv"

# DATASET RAW
OUTPUT_PATH = "data/raw/02_bank.csv"

# ============================================
# INGESTA
# ============================================

def ingest_data():

    try:

        print(
            "Iniciando proceso de ingesta..."
        )

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
        # VALIDAR EXISTENCIA ARCHIVO
        # ============================================

        if not os.path.exists(SOURCE_PATH):

            raise FileNotFoundError(

                f"No existe el archivo: "
                f"{SOURCE_PATH}"

            )

        logging.info(
            "Archivo origen encontrado"
        )

        # ============================================
        # LEER CSV
        # ============================================

        df = pd.read_csv(
            SOURCE_PATH
        )

        logging.info(
            f"Dataset cargado correctamente"
        )

        logging.info(
            f"Filas detectadas: "
            f"{df.shape[0]}"
        )

        logging.info(
            f"Columnas detectadas: "
            f"{df.shape[1]}"
        )

        logging.info(
            f"Columnas: "
            f"{list(df.columns)}"
        )

        # ============================================
        # EXPORTAR RAW
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Archivo raw generado: "
            f"{OUTPUT_PATH}"
        )

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

        print(
            "Ingesta completada correctamente"
        )

        print(
            f"Filas cargadas: "
            f"{df.shape[0]}"
        )

        print(
            f"Columnas cargadas: "
            f"{df.shape[1]}"
        )

        return df

    except Exception as e:

        logging.error(
            f"Error en ingesta: {e}"
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