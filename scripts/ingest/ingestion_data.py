# ============================================
# scripts/ingest/ingestion_data.py
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
    "data/raw",
    exist_ok=True
)

# ============================================
# LOGGING
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
        # LOG KPIs
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
        # ALERTAS
        # ============================================

        if conversion_rate < 10:

            logging.warning(
                "ALERTA: Conversión baja"
            )

        if avg_balance < 0:

            logging.warning(
                "ALERTA: Balance promedio negativo"
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

        print(
            f"ERROR: {e}"
        )

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":

    ingest_data()