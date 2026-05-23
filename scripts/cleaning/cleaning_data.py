# ============================================
# scripts/cleaning/cleaning_data.py
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

os.makedirs("logs", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ============================================
# LOGGING INDIVIDUAL
# ============================================

logging.basicConfig(
    filename="logs/cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = "data/raw/02_bank.csv"
OUTPUT_PATH = "data/processed/bank_cleaned.csv"

# ============================================
# LIMPIEZA
# ============================================

def clean_data():

    start_time = time.time()

    try:

        print("Iniciando limpieza...")

        # ============================================
        # LOG INDIVIDUAL
        # ============================================

        logging.info("===================================")
        logging.info("INICIO LIMPIEZA")
        logging.info("===================================")

        # ============================================
        # LOG GLOBAL PIPELINE
        # ============================================

        log_section(
            "ETAPA 2 - LIMPIEZA"
        )

        log_message(
            "Inicio proceso limpieza"
        )

        # ============================================
        # LEER DATASET
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        initial_rows = len(df)

        log_metric(
            "Filas iniciales",
            initial_rows
        )

        logging.info(
            f"Filas iniciales: {initial_rows}"
        )

        # ============================================
        # LIMPIAR COLUMNAS
        # ============================================

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        log_message(
            "Nombres de columnas normalizados"
        )

        log_list(
            "Columnas detectadas",
            list(df.columns)
        )

        # ============================================
        # LIMPIAR TEXTO
        # ============================================

        object_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for col in object_columns:

            df[col] = (

                df[col]
                .astype(str)
                .str.strip()
                .str.lower()

            )

        logging.info(
            "Texto normalizado correctamente"
        )

        log_message(
            "Texto convertido a minúsculas y espacios eliminados"
        )

        log_metric(
            "Columnas texto procesadas",
            len(object_columns)
        )

        # ============================================
        # ELIMINAR DUPLICADOS
        # ============================================

        duplicates = df.duplicated().sum()

        df = df.drop_duplicates()

        logging.info(
            f"Duplicados eliminados: {duplicates}"
        )

        log_metric(
            "Duplicados eliminados",
            duplicates
        )

        # ============================================
        # ELIMINAR NULOS CRÍTICOS
        # ============================================

        critical_columns = [
            "age",
            "job",
            "balance",
            "deposit"
        ]

        nulls_before = df.isnull().sum().sum()

        df = df.dropna(
            subset=critical_columns
        )

        logging.info(
            f"Nulos detectados: {nulls_before}"
        )

        log_metric(
            "Nulos detectados",
            nulls_before
        )

        log_list(
            "Columnas críticas",
            critical_columns
        )

        # ============================================
        # VALIDAR EDADES
        # ============================================

        invalid_age_rows = len(
            df[df["age"] < 18]
        )

        df = df[
            df["age"] >= 18
        ]

        logging.info(
            f"Clientes menores eliminados: "
            f"{invalid_age_rows}"
        )

        log_metric(
            "Clientes menores eliminados",
            invalid_age_rows
        )

        # ============================================
        # CONVERTIR NUMÉRICOS
        # ============================================

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

        logging.info(
            "Conversión numérica completada"
        )

        log_message(
            "Conversión de columnas numéricas completada"
        )

        log_list(
            "Columnas numéricas",
            numeric_columns
        )

        # ============================================
        # VALIDAR JOBS
        # ============================================

        valid_jobs = [

            "admin.",
            "technician",
            "services",
            "management",
            "retired",
            "blue-collar",
            "unemployed",
            "entrepreneur",
            "housemaid",
            "self-employed",
            "student",
            "unknown"

        ]

        invalid_jobs = len(
            df[
                ~df["job"].isin(valid_jobs)
            ]
        )

        df.loc[
            ~df["job"].isin(valid_jobs),
            "job"
        ] = "unknown"

        logging.info(
            f"Trabajos inválidos corregidos: "
            f"{invalid_jobs}"
        )

        log_metric(
            "Trabajos inválidos corregidos",
            invalid_jobs
        )

        # ============================================
        # KPI LIMPIEZA
        # ============================================

        final_rows = len(df)

        removed_rows = (
            initial_rows - final_rows
        )

        retention_rate = round(
            (
                final_rows / initial_rows
            ) * 100,
            2
        )

        logging.info(
            f"Filas eliminadas: {removed_rows}"
        )

        logging.info(
            f"Filas finales: {final_rows}"
        )

        logging.info(
            f"Tasa retención: {retention_rate}%"
        )

        log_metric(
            "Filas eliminadas",
            removed_rows
        )

        log_metric(
            "Filas finales",
            final_rows
        )

        log_metric(
            "Tasa retención",
            f"{retention_rate}%"
        )

        # ============================================
        # ALERTAS
        # ============================================

        if retention_rate < 80:

            logging.warning(
                "ALERTA: Retención baja"
            )

            log_message(
                "ALERTA DETECTADA: Retención baja"
            )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Archivo exportado: {OUTPUT_PATH}"
        )

        log_message(
            "Dataset limpio exportado correctamente"
        )

        log_metric(
            "Ruta salida",
            OUTPUT_PATH
        )

        # ============================================
        # TIEMPO EJECUCIÓN
        # ============================================

        log_execution_time(
            "LIMPIEZA",
            start_time
        )

        # ============================================
        # FIN LOG INDIVIDUAL
        # ============================================

        logging.info(
            "Limpieza completada"
        )

        logging.info(
            "==================================="
        )

        logging.info(
            "FIN LIMPIEZA"
        )

        logging.info(
            "==================================="
        )

        # ============================================
        # PRINTS
        # ============================================

        print("Limpieza completada")

        print(
            f"Filas iniciales: {initial_rows}"
        )

        print(
            f"Filas finales: {final_rows}"
        )

        print(
            f"Tasa retención: {retention_rate}%"
        )

    except Exception as e:

        logging.error(
            f"ERROR LIMPIEZA: {e}"
        )

        log_error(
            f"ERROR LIMPIEZA: {e}"
        )

        print(f"ERROR: {e}")

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    clean_data()