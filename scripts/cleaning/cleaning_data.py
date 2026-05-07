# ============================================
# cleaning_data.py
# ============================================

import pandas as pd
import logging

logging.basicConfig(
    filename='logs/cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

INPUT_PATH = "data/raw/02_bank.csv"
OUTPUT_PATH = "data/processed/bank_cleaned.csv"

def clean_data():

    try:

        print("Iniciando limpieza de datos...")
        logging.info("Iniciando limpieza de datos")

        # ============================================
        # LEER CSV
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        logging.info(f"Dataset original: {df.shape}")

        # ============================================
        # ELIMINAR DUPLICADOS
        # ============================================

        df.drop_duplicates(inplace=True)

        logging.info(f"Duplicados eliminados: {df.shape}")

        # ============================================
        # LIMPIAR COLUMNAS CATEGÓRICAS
        # ============================================

        categorical_columns = [
            'job',
            'marital',
            'education',
            'default',
            'housing',
            'loan',
            'contact',
            'month',
            'poutcome',
            'deposit'
        ]

        for col in categorical_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # ============================================
        # MANEJO DE NULOS
        # ============================================

        critical_columns = [
            'age',
            'balance',
            'deposit'
        ]

        df.dropna(
            subset=critical_columns,
            inplace=True
        )

        logging.info(f"Nulos eliminados: {df.shape}")

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(OUTPUT_PATH, index=False)

        logging.info("Datos limpiados correctamente")

        print("Limpieza completada correctamente")
        print(f"Filas finales: {df.shape[0]}")
        print(f"Columnas finales: {df.shape[1]}")

        return df

    except Exception as e:

        logging.error(f"Error en limpieza: {e}")

        print(f"Error en limpieza: {e}")

        raise

if __name__ == "__main__":
    clean_data()