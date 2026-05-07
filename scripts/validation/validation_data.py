import pandas as pd
import logging

logging.basicConfig(
    filename='logs/validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

INPUT_PATH = "data/processed/bank_cleaned.csv"

VALIDATED_PATH = "data/validated/bank_validated.csv"
REJECT_PATH = "data/reject/bank_rejected.csv"

def validate_data():

    try:

        print("Iniciando validaciones...")
        logging.info("Iniciando validaciones")

        df = pd.read_csv(INPUT_PATH)

        # ============================================
        # VALORES PERMITIDOS
        # ============================================

        valid_months = [
            'jan', 'feb', 'mar', 'apr',
            'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec'
        ]

        valid_binary = ['yes', 'no']

        valid_contacts = [
            'cellular',
            'telephone',
            'unknown'
        ]

        valid_marital = [
            'married',
            'single',
            'divorced'
        ]

        valid_education = [
            'primary',
            'secondary',
            'tertiary',
            'unknown'
        ]

        valid_poutcome = [
            'success',
            'failure',
            'other',
            'unknown'
        ]

        # ============================================
        # VALIDACIONES
        # ============================================

        valid_mask = (

            # Edad válida
            (df['age'].between(18, 100)) &

            # Día válido
            (df['day'].between(1, 31)) &

            # Valores numéricos válidos
            (df['duration'] >= 0) &
            (df['campaign'] >= 0) &
            (df['pdays'] >= -1) &
            (df['previous'] >= 0) &

            # Balance razonable
            (df['balance'] >= 0) &

            # Mes válido
            (df['month'].isin(valid_months)) &

            # Variables binarias
            (df['default'].isin(valid_binary)) &
            (df['housing'].isin(valid_binary)) &
            (df['loan'].isin(valid_binary)) &
            (df['deposit'].isin(valid_binary)) &

            # Variables categóricas
            (df['contact'].isin(valid_contacts)) &
            (df['marital'].isin(valid_marital)) &
            (df['education'].isin(valid_education)) &
            (df['poutcome'].isin(valid_poutcome))

        )

        # ============================================
        # SEPARAR DATOS
        # ============================================

        valid_df = df[valid_mask]
        reject_df = df[~valid_mask]

        # ============================================
        # EXPORTAR
        # ============================================

        valid_df.to_csv(VALIDATED_PATH, index=False)
        reject_df.to_csv(REJECT_PATH, index=False)

        # ============================================
        # LOGS
        # ============================================

        logging.info(f"Registros válidos: {valid_df.shape[0]}")
        logging.info(f"Registros rechazados: {reject_df.shape[0]}")

        print(f"Registros válidos: {valid_df.shape[0]}")
        print(f"Registros rechazados: {reject_df.shape[0]}")

        print("Validación finalizada correctamente")

        return valid_df, reject_df

    except Exception as e:

        logging.error(f"Error en validación: {e}")

        print(f"Error en validación: {e}")

        raise

if __name__ == "__main__":
    validate_data()