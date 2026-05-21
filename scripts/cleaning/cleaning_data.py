# ============================================
# scripts/cleaning/cleaning_data.py
# ============================================

import pandas as pd
import logging
import os

# ============================================
# CREAR CARPETAS
# ============================================

os.makedirs("logs", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ============================================
# LOGGING
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

    try:

        print("Iniciando limpieza...")

        logging.info("===================================")
        logging.info("INICIO LIMPIEZA")
        logging.info("===================================")

        df = pd.read_csv(INPUT_PATH)

        initial_rows = len(df)

        # ============================================
        # LIMPIAR COLUMNAS
        # ============================================

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
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

        # ============================================
        # ELIMINAR DUPLICADOS
        # ============================================

        duplicates = df.duplicated().sum()

        df = df.drop_duplicates()

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

        # ============================================
        # VALIDAR EDADES
        # ============================================

        df = df[
            df["age"] >= 18
        ]

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

        df.loc[
            ~df["job"].isin(valid_jobs),
            "job"
        ] = "unknown"

        # ============================================
        # KPI LIMPIEZA
        # ============================================

        final_rows = len(df)

        removed_rows = (
            initial_rows - final_rows
        )

        logging.info(
            f"Duplicados eliminados: {duplicates}"
        )

        logging.info(
            f"Nulos detectados: {nulls_before}"
        )

        logging.info(
            f"Filas eliminadas: {removed_rows}"
        )

        logging.info(
            f"Filas finales: {final_rows}"
        )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            "Limpieza completada"
        )

        print("Limpieza completada")

    except Exception as e:

        logging.error(
            f"ERROR LIMPIEZA: {e}"
        )

        print(f"ERROR: {e}")

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    clean_data()