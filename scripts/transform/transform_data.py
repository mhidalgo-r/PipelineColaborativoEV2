# ============================================
# transform_data.py
# ============================================

import pandas as pd
import logging

logging.basicConfig(
    filename='logs/transformation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

INPUT_PATH = "data/validated/bank_validated.csv"
OUTPUT_PATH = "data/processed/bank_transformed.csv"

def transform_data():

    try:

        print("Iniciando transformación...")
        logging.info("Iniciando transformación")

        # ============================================
        # LEER CSV VALIDADO
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        # ============================================
        # VARIABLES BINARIAS
        # ============================================

        binary_columns = [
            'default',
            'housing',
            'loan',
            'deposit'
        ]

        for col in binary_columns:

            df[col] = df[col].map({
                'yes': 1,
                'no': 0
            })

        logging.info("Variables binarias transformadas")

        # ============================================
        # ONE HOT ENCODING
        # ============================================

        categorical_columns = [
            'job',
            'marital',
            'education',
            'contact',
            'month',
            'poutcome'
        ]

        df = pd.get_dummies(
            df,
            columns=categorical_columns,
            drop_first=True
        )

        logging.info("Variables categóricas transformadas")

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(OUTPUT_PATH, index=False)

        logging.info("Transformación completada")

        print("Transformación completada correctamente")
        print(f"Filas transformadas: {df.shape[0]}")
        print(f"Columnas finales: {df.shape[1]}")

        return df

    except Exception as e:

        logging.error(f"Error en transformación: {e}")

        print(f"Error en transformación: {e}")

        raise

if __name__ == "__main__":
    transform_data()