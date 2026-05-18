# ============================================
# transform_data.py
# ============================================

import pandas as pd
import logging
import os

# ============================================
# LOGS
# ============================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/transformation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = "data/processed/bank_cleaned.csv"

OUTPUT_PATH = "data/processed/bank_transformed.csv"

# ============================================
# TRANSFORM
# ============================================

def transform_data():

    try:

        print("Iniciando transformación...")

        logging.info(
            "========== INICIO TRANSFORMACIÓN =========="
        )

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

        logging.info(
            "Variables binarias transformadas"
        )

        # ============================================
        # NUEVAS COLUMNAS
        # ============================================

        df['warning_count'] = 0

        df['warning_reasons'] = ''

        # ============================================
        # EDAD
        # ============================================

        df.loc[
            (df['age'] >= 73)
            &
            (df['age'] <= 85),
            'warning_count'
        ] += 2

        df.loc[
            (df['age'] >= 73)
            &
            (df['age'] <= 85),
            'warning_reasons'
        ] += 'advanced_age;'

        # ============================================
        # JOB
        # ============================================

        risky_jobs = [
            'retired',
            'student',
            'unemployed',
            'unknown'
        ]

        df.loc[
            df['job'].isin(risky_jobs),
            'warning_count'
        ] += 2

        df.loc[
            df['job'].isin(risky_jobs),
            'warning_reasons'
        ] += 'unstable_job;'

        # ============================================
        # DEFAULT
        # ============================================

        df.loc[
            df['default'] == 1,
            'warning_count'
        ] += 5

        df.loc[
            df['default'] == 1,
            'warning_reasons'
        ] += 'credit_default;'

        # ============================================
        # LOAN
        # ============================================

        df.loc[
            df['loan'] == 1,
            'warning_count'
        ] += 2

        df.loc[
            df['loan'] == 1,
            'warning_reasons'
        ] += 'personal_loan;'

        # ============================================
        # HOUSING
        # ============================================

        df.loc[
            df['housing'] == 1,
            'warning_count'
        ] += 1

        df.loc[
            df['housing'] == 1,
            'warning_reasons'
        ] += 'housing_loan;'

        # ============================================
        # BALANCE
        # ============================================

        df.loc[
            df['balance'] <= 0,
            'warning_count'
        ] += 4

        df.loc[
            df['balance'] <= 0,
            'warning_reasons'
        ] += 'negative_balance;'

        # ============================================
        # CONTACT
        # ============================================

        df.loc[
            df['contact'] == 'unknown',
            'warning_count'
        ] += 3

        df.loc[
            df['contact'] == 'unknown',
            'warning_reasons'
        ] += 'unknown_contact;'

        # ============================================
        # DURATION
        # ============================================

        df.loc[
            df['duration'] < 60,
            'warning_count'
        ] += 3

        df.loc[
            df['duration'] < 60,
            'warning_reasons'
        ] += 'low_call_duration;'

        # ============================================
        # SCORE
        # ============================================

        df['client_score'] = (
            100 -
            (df['warning_count'] * 5)
        )

        df['client_score'] = (
            df['client_score']
            .clip(lower=0)
            .astype(int)
        )

        # ============================================
        # RISK LEVEL
        # ============================================

        def risk(score):

            if score >= 85:
                return 'low'

            elif score >= 70:
                return 'medium'

            elif score >= 50:
                return 'high'

            else:
                return 'critical'

        df['risk_level'] = (
            df['client_score']
            .apply(risk)
        )

        # ============================================
        # CLIENT SEGMENT
        # ============================================

        def segment(score):

            if score >= 85:
                return 'premium'

            elif score >= 70:
                return 'standard'

            else:
                return 'risk'

        df['client_segment'] = (
            df['client_score']
            .apply(segment)
        )

        # ============================================
        # APPROVAL
        # ============================================

        df['approval_status'] = (
            df['warning_count']
            .apply(
                lambda x:
                'approved'
                if x < 8
                else 'rejected'
            )
        )

        # ============================================
        # AGE GROUP
        # ============================================

        df['age_group'] = pd.cut(

            df['age'],

            bins=[18, 30, 45, 60, 72, 100],

            labels=[
                'young',
                'adult',
                'mature',
                'senior',
                'elder'
            ]

        )

        logging.info(
            "Variables derivadas generadas"
        )

        # ============================================
        # EXPORTAR
        # ============================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        logging.info(
            f"Dataset transformado: {df.shape}"
        )

        logging.info(
            "========== FIN TRANSFORMACIÓN =========="
        )

        print("Transformación completada")

        return df

    except Exception as e:

        logging.error(
            f"Error transformación: {e}"
        )

        raise


if __name__ == "__main__":
    transform_data()