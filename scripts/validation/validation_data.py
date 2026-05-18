# ============================================
# VALIDACIÓN
# ============================================

import pandas as pd
import logging
import os

# ============================================
# LOGS
# ============================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# PATHS
# ============================================

INPUT_PATH = "data/processed/bank_transformed.csv"

VALIDATED_PATH = "data/validated/bank_validated.csv"

REJECT_PATH = "data/reject/bank_rejected.csv"

# ============================================
# VALIDACIÓN
# ============================================

def validate_data():

    try:

        print("Iniciando validación...")

        logging.info(
            "========== INICIO VALIDACIÓN =========="
        )

        # ============================================
        # CARGAR DATASET
        # ============================================

        df = pd.read_csv(INPUT_PATH)

        logging.info(
            f"Dataset cargado: {df.shape}"
        )

        # ============================================
        # COLUMNA MOTIVO RECHAZO
        # ============================================

        df['rejection_reason'] = ''

        # ============================================
        # REGLA 1
        # EDAD MAYOR A 85
        # ============================================

        age_reject = df['age'] > 85

        df.loc[
            age_reject,
            'approval_status'
        ] = 'rejected'

        df.loc[
            age_reject,
            'rejection_reason'
        ] += 'Edad superior a 85 años. '

        logging.info(
            "Validación edad máxima aplicada"
        )

        # ============================================
        # REGLA 2
        # DEFAULT + HOUSING + LOAN
        # ============================================

        debt_reject = (

            (df['default'] == 1)

            &

            (df['housing'] == 1)

            &

            (df['loan'] == 1)

        )

        df.loc[
            debt_reject,
            'approval_status'
        ] = 'rejected'

        df.loc[
            debt_reject,
            'rejection_reason'
        ] += (
            'Cliente con morosidad y '
            'múltiples préstamos. '
        )

        logging.info(
            "Validación financiera crítica aplicada"
        )

        # ============================================
        # REGLA 3
        # SCORE MUY BAJO
        # ============================================

        low_score = (
            df['client_score'] < 50
        )

        df.loc[
            low_score,
            'approval_status'
        ] = 'rejected'

        df.loc[
            low_score,
            'rejection_reason'
        ] += (
            'Score financiero muy bajo. '
        )

        logging.info(
            "Validación de score aplicada"
        )

        # ============================================
        # REGLA 4
        # MUCHOS WARNINGS
        # ============================================

        high_warning = (
            df['warning_count'] >= 8
        )

        df.loc[
            high_warning,
            'approval_status'
        ] = 'rejected'

        df.loc[
            high_warning,
            'rejection_reason'
        ] += (
            'Demasiados factores de riesgo. '
        )

        logging.info(
            "Validación de warnings aplicada"
        )

        # ============================================
        # REGLA 5
        # BALANCE NEGATIVO
        # ============================================

        negative_balance = (
            df['balance'] < 0
        )

        df.loc[
            negative_balance,
            'approval_status'
        ] = 'rejected'

        df.loc[
            negative_balance,
            'rejection_reason'
        ] += (
            'Balance negativo. '
        )

        logging.info(
            "Validación balance aplicada"
        )

        # ============================================
        # VALIDACIONES ESTRUCTURALES
        # ============================================

        structural_mask = (

            (df['age'].between(18, 100))

            &

            (df['day'].between(1, 31))

            &

            (df['duration'] >= 0)

            &

            (df['campaign'] >= 0)

            &

            (df['pdays'] >= -1)

            &

            (df['previous'] >= 0)

            &

            (df['warning_count'] >= 0)

            &

            (df['client_score'].between(0, 100))

        )

        logging.info(
            "Validaciones estructurales completadas"
        )

        # ============================================
        # VALIDACIONES SEMÁNTICAS
        # ============================================

        semantic_mask = (

            (
                (
                    (df['previous'] == 0)

                    &

                    (df['pdays'] == -1)
                )

                |

                (
                    (df['previous'] > 0)

                    &

                    (df['pdays'] >= 0)
                )
            )

            &

            (
                df['risk_level'].isin([
                    'low',
                    'medium',
                    'high',
                    'critical'
                ])
            )

        )

        logging.info(
            "Validaciones semánticas completadas"
        )

        # ============================================
        # VALIDACIÓN FINAL
        # ============================================

        valid_mask = (

            structural_mask

            &

            semantic_mask

            &

            (
                df['approval_status']
                == 'approved'
            )

        )

        # ============================================
        # DATASETS FINALES
        # ============================================

        valid_df = df[
            valid_mask
        ]

        reject_df = df[
            ~valid_mask
        ]

        # ============================================
        # EXPORTAR
        # ============================================

        os.makedirs(
            "data/validated",
            exist_ok=True
        )

        os.makedirs(
            "data/reject",
            exist_ok=True
        )

        valid_df.to_csv(
            VALIDATED_PATH,
            index=False
        )

        reject_df.to_csv(
            REJECT_PATH,
            index=False
        )

        # ============================================
        # MÉTRICAS
        # ============================================

        logging.info(
            f"Clientes aprobados: "
            f"{valid_df.shape[0]}"
        )

        logging.info(
            f"Clientes rechazados: "
            f"{reject_df.shape[0]}"
        )

        logging.info(
            "Los clientes rechazados "
            "presentan alto riesgo "
            "financiero o incumplen "
            "políticas bancarias"
        )

        logging.info(
            "========== FIN VALIDACIÓN =========="
        )

        print("Validación completada")

        print(
            f"Aprobados: {valid_df.shape[0]}"
        )

        print(
            f"Rechazados: {reject_df.shape[0]}"
        )

        return valid_df, reject_df

    except Exception as e:

        logging.error(
            f"Error validación: {e}"
        )

        print(f"ERROR: {e}")

        raise

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    validate_data()