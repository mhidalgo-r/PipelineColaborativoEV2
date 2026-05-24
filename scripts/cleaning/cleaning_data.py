# ============================================
# scripts/cleaning/cleaning_data.py
# ============================================

import pandas as pd
import logging
import os
import time

from utils.pipeline_logger import *

os.makedirs(
    "logs",
    exist_ok=True
)

os.makedirs(
    "data/processed",
    exist_ok=True
)

logging.basicConfig(
    filename="logs/cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

INPUT_PATH = (
    "data/raw/02_bank.csv"
)

OUTPUT_PATH = (
    "data/processed/bank_cleaned.csv"
)

def clean_data():

    try:

        start_time = time.time()

        print(
            "Iniciando limpieza..."
        )

        log_section(
            "ETAPA 2 - LIMPIEZA"
        )

        log_message(
            "Inicio proceso limpieza"
        )

        df = pd.read_csv(
            INPUT_PATH
        )

        initial_rows = len(df)

        log_metric(
            "Filas iniciales",
            initial_rows
        )

        df.columns = (

            df.columns
            .str.lower()
            .str.strip()

        )

        log_message(
            "Nombres columnas normalizados"
        )

        log_list(
            "Columnas detectadas",
            df.columns.tolist()
        )

        text_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for col in text_columns:

            df[col] = (

                df[col]
                .astype(str)
                .str.lower()
                .str.strip()

            )

        log_message(
            "Texto convertido a minúsculas"
        )

        before_duplicates = len(df)

        df = df.drop_duplicates()

        duplicates_removed = (
            before_duplicates -
            len(df)
        )

        log_metric(
            "Duplicados eliminados",
            duplicates_removed
        )

        nulls_detected = (
            df.isnull()
            .sum()
            .sum()
        )

        log_metric(
            "Nulos detectados",
            nulls_detected
        )

        before_filter = len(df)

        df = df[
            df["age"] >= 18
        ]

        removed_minors = (
            before_filter -
            len(df)
        )

        log_metric(
            "Clientes menores eliminados",
            removed_minors
        )

        numeric_columns = [

            "age",
            "balance",
            "day",
            "duration",
            "campaign",
            "pdays",
            "previous"

        ]

        for col in numeric_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        log_message(
            "Conversión numérica completada"
        )

        log_list(
            "Columnas numéricas",
            numeric_columns
        )

        final_rows = len(df)

        retention_rate = round(

            (
                final_rows /
                initial_rows
            ) * 100,

            2

        )

        log_metric(
            "Filas finales",
            final_rows
        )

        log_metric(
            "Tasa retención",
            f"{retention_rate}%"
        )

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        log_message(
            "Dataset limpio exportado"
        )

        log_message(
            f"Ruta salida: {OUTPUT_PATH}"
        )

        log_execution_time(
            "LIMPIEZA",
            start_time
        )

        log_message(
            "FIN LIMPIEZA"
        )

        print(
            "Limpieza completada"
        )

    except Exception as e:

        log_error(
            f"ERROR LIMPIEZA: {e}"
        )

        print(
            f"ERROR: {e}"
        )

        raise

if __name__ == "__main__":

    clean_data()