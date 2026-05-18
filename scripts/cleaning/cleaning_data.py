# ============================================
# cleaning_data.py
# ============================================

import pandas as pd
import logging
import os

# ============================================
# LOGS
# ============================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = "data/raw/02_bank.csv"
OUTPUT_PATH = "data/processed/bank_cleaned.csv"

# ============================================
# CATÁLOGOS
# ============================================

VALID_JOBS = [
    'admin.',
    'technician',
    'services',
    'management',
    'retired',
    'blue-collar',
    'unemployed',
    'entrepreneur',
    'housemaid',
    'student',
    'self-employed',
    'unknown'
]

VALID_MARITAL = [
    'married',
    'single',
    'divorced'
]

VALID_EDUCATION = [
    'primary',
    'secondary',
    'tertiary',
    'unknown'
]

VALID_CONTACT = [
    'cellular',
    'telephone',
    'unknown'
]

VALID_POUTCOME = [
    'success',
    'failure',
    'other',
    'unknown'
]

VALID_BINARY = [
    'yes',
    'no'
]

VALID_MONTHS = [
    'jan', 'feb', 'mar', 'apr',
    'may', 'jun', 'jul', 'aug',
    'sep', 'oct', 'nov', 'dec'
]

# ============================================
# CLEANING
# ============================================

def clean_data():

    try:

        print("Iniciando limpieza...")

        logging.info(
            "========== INICIO LIMPIEZA =========="
        )

        # ============================================
        # CARGAR CSV
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        logging.info(
            f"Dataset original: {df.shape}"
        )

        # ============================================
        # DUPLICADOS
        # ============================================

        duplicates = df.duplicated().sum()

        df.drop_duplicates(inplace=True)

        logging.info(
            f"Duplicados eliminados: {duplicates}"
        )

        # ============================================
        # LIMPIEZA TEXTO
        # ============================================

        text_columns = [
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

        for col in text_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # ============================================
        # CORRECCIÓN TYPO
        # ============================================

        df['job'] = df['job'].replace({
            'admin': 'admin.',
            'unknow': 'unknown'
        })

        logging.info(
            "Homogeneización aplicada"
        )

        # ============================================
        # NUMÉRICOS
        # ============================================

        numeric_columns = [
            'age',
            'balance',
            'day',
            'duration',
            'campaign',
            'pdays',
            'previous'
        ]

        for col in numeric_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors='coerce'
            )

        logging.info(
            "Conversión numérica aplicada"
        )

        # ============================================
        # NULOS
        # ============================================

        nulls = df.isnull().sum().sum()

        df.dropna(inplace=True)

        logging.info(
            f"Nulos eliminados: {nulls}"
        )

        # ============================================
        # VALIDACIONES CATEGÓRICAS
        # ============================================

        before = df.shape[0]

        df = df[
            df['job'].isin(VALID_JOBS)
        ]

        logging.info(
            f"Registros eliminados por job inválido: "
            f"{before - df.shape[0]}"
        )

        before = df.shape[0]

        df = df[
            df['marital'].isin(VALID_MARITAL)
        ]

        logging.info(
            f"Registros eliminados por marital inválido: "
            f"{before - df.shape[0]}"
        )

        before = df.shape[0]

        df = df[
            df['education'].isin(
                VALID_EDUCATION
            )
        ]

        logging.info(
            f"Registros eliminados por education inválido: "
            f"{before - df.shape[0]}"
        )

        df = df[
            df['contact'].isin(
                VALID_CONTACT
            )
        ]

        df = df[
            df['poutcome'].isin(
                VALID_POUTCOME
            )
        ]

        df = df[
            df['month'].isin(
                VALID_MONTHS
            )
        ]

        # ============================================
        # VALIDACIONES BINARIAS
        # ============================================

        df = df[
            df['default'].isin(
                VALID_BINARY
            )
        ]

        df = df[
            df['housing'].isin(
                VALID_BINARY
            )
        ]

        df = df[
            df['loan'].isin(
                VALID_BINARY
            )
        ]

        df = df[
            df['deposit'].isin(
                VALID_BINARY
            )
        ]

        logging.info(
            "Validaciones categóricas aplicadas"
        )

        # ============================================
        # VALIDACIONES NUMÉRICAS
        # ============================================

        before_numeric = df.shape[0]

        df = df[
            (df['age'] >= 18)
            &
            (df['age'] <= 100)
        ]

        df = df[
            (df['day'] >= 1)
            &
            (df['day'] <= 31)
        ]

        df = df[
            df['duration'] >= 0
        ]

        df = df[
            df['campaign'] >= 0
        ]

        df = df[
            df['pdays'] >= -1
        ]

        df = df[
            df['previous'] >= 0
        ]

        logging.info(
            f"Registros eliminados por reglas numéricas: "
            f"{before_numeric - df.shape[0]}"
        )

        # ============================================
        # EXPORTAR
        # ============================================

        os.makedirs(
            "data/processed",
            exist_ok=True
        )

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Dataset limpio exportado: {df.shape}"
        )

        logging.info(
            "========== FIN LIMPIEZA =========="
        )

        print("Limpieza completada")

        return df

    except Exception as e:

        logging.error(
            f"Error limpieza: {e}"
        )

        raise


if __name__ == "__main__":
    clean_data()