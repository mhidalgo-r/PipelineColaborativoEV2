import os
import pandas as pd
from datetime import datetime
import logging

# ==========================
# CREAR CARPETAS
# ==========================
os.makedirs("data/outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ==========================
# LOGGER
# ==========================
logging.basicConfig(
    filename="logs/quality_analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger()

# ==========================
# RUTAS
# ==========================
INPUT_FILE = "data/processed/bank_cleaned.csv"
OUTPUT_FILE = "data/outputs/data_quality_report.csv"

# Columnas sensibles segun Ley 19.628
SENSITIVE_COLUMNS = [
    "age", "job", "marital",
    "education", "balance"
]

# ==========================
# FUNCION PRINCIPAL
# ==========================
def analyze_data():
    logger.info("=" * 50)
    logger.info("INICIO ANALISIS CALIDAD")
    logger.info("=" * 50)

    try:
        df = pd.read_csv(INPUT_FILE)
        total_rows = df.shape[0]
        total_columns = df.shape[1]
        total_nulls = df.isnull().sum().sum()
        total_duplicates = df.duplicated().sum()

        logger.info(f"Filas: {total_rows}")
        logger.info(f"Columnas: {total_columns}")
        logger.info(f"Nulos totales dataset: {total_nulls}")
        logger.info(f"Filas duplicadas dataset: {total_duplicates}")

        # Columnas sensibles
        sensitive_found = [
            c for c in SENSITIVE_COLUMNS if c in df.columns
        ]
        logger.info(
            f"Columnas sensibles (Ley 19.628): {sensitive_found}"
        )

        quality = []

        for column in df.columns:
            dtype = str(df[column].dtype)
            nulls = df[column].isnull().sum()
            col_duplicates = df[column].duplicated().sum()
            unique = df[column].nunique()
            is_sensitive = column in SENSITIVE_COLUMNS

            try:
                mean = round(df[column].mean(), 4)
                median = round(df[column].median(), 4)
                mode_series = df[column].mode()
                mode = mode_series[0] if len(mode_series) > 0 else None
                q25 = round(df[column].quantile(0.25), 4)
                q50 = round(df[column].quantile(0.50), 4)
                q75 = round(df[column].quantile(0.75), 4)
            except TypeError as e:
                logger.warning(
                    f"Columna {column} no numerica: {e}"
                )
                mean = None
                median = None
                mode = df[column].mode()[0] if len(
                    df[column].mode()
                ) > 0 else None
                q25 = None
                q50 = None
                q75 = None

            quality.append({
                "column": column,
                "datatype": dtype,
                "null_values": nulls,
                "col_duplicates": col_duplicates,
                "unique_values": unique,
                "mean": mean,
                "median": median,
                "mode": mode,
                "percentile_25": q25,
                "percentile_50": q50,
                "percentile_75": q75,
                "sensitive_data": is_sensitive
            })

        report = pd.DataFrame(quality)
        report.to_csv(OUTPUT_FILE, index=False)

        logger.info("Reporte generado correctamente")
        logger.info(f"Archivo: {OUTPUT_FILE}")

        print("\nReporte generado:")
        print(f"  Filas: {total_rows}")
        print(f"  Columnas: {total_columns}")
        print(f"  Nulos totales: {total_nulls}")
        print(f"  Filas duplicadas: {total_duplicates}")
        print(f"  Columnas sensibles: {sensitive_found}")
        print(f"  Reporte: {OUTPUT_FILE}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    analyze_data()