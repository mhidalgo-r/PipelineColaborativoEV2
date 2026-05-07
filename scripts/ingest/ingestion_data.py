import pandas as pd
import logging
from pathlib import Path

# Configuración de logs
logging.basicConfig(
    filename='logs/ingestion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas
RAW_PATH = "data/raw/02_bank.csv"

def ingest_data():

    try:
        logging.info("Iniciando proceso de ingesta")

        df = pd.read_csv(RAW_PATH)

        logging.info(f"Dataset cargado correctamente: {df.shape[0]} filas y {df.shape[1]} columnas")

        print(df.head())

        return df

    except Exception as e:
        logging.error(f"Error en ingesta: {e}")
        raise


if __name__ == "__main__":
    ingest_data()