# ============================================
# loading.py
# ============================================

import pandas as pd
import logging
import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ============================================
# CARGAR VARIABLES DE ENTORNO
# ============================================

load_dotenv()

# ============================================
# CONFIGURACIÓN DE LOGS
# ============================================

logging.basicConfig(
    filename='logs/loading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================
# VARIABLES
# ============================================

INPUT_PATH = "data/validated/bank_validated.csv"

DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_VW9osR4JEDed@ep-jolly-salad-ac1c6utw-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# ============================================
# SQL CREACIÓN DE TABLAS
# ============================================

CREATE_CLIENTES_TABLE = """
CREATE TABLE IF NOT EXISTS clientes (

    cliente_id SERIAL PRIMARY KEY,

    age INTEGER,
    job VARCHAR(50),
    marital VARCHAR(20),
    education VARCHAR(20),

    default_col VARCHAR(5),

    balance INTEGER,

    housing VARCHAR(5),
    loan VARCHAR(5)

);
"""

CREATE_CONTACTOS_TABLE = """
CREATE TABLE IF NOT EXISTS contactos (

    contacto_id SERIAL PRIMARY KEY,

    cliente_id INTEGER REFERENCES clientes(cliente_id),

    contact VARCHAR(20),

    day INTEGER,
    month VARCHAR(10),

    duration INTEGER,
    campaign INTEGER

);
"""

CREATE_CAMPANAS_TABLE = """
CREATE TABLE IF NOT EXISTS campanas_previas (

    campana_id SERIAL PRIMARY KEY,

    cliente_id INTEGER REFERENCES clientes(cliente_id),

    pdays INTEGER,
    previous INTEGER,

    poutcome VARCHAR(20)

);
"""

CREATE_SUSCRIPCIONES_TABLE = """
CREATE TABLE IF NOT EXISTS suscripciones (

    suscripcion_id SERIAL PRIMARY KEY,

    cliente_id INTEGER REFERENCES clientes(cliente_id),

    deposit VARCHAR(5)

);
"""

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def load_data():

    try:

        logging.info("===================================")
        logging.info("INICIANDO CARGA A NEON")
        logging.info("===================================")

        # Validar conexión
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL no encontrada")

        # Leer CSV
        df = pd.read_csv(INPUT_PATH)

        logging.info(f"Archivo leído correctamente: {INPUT_PATH}")
        logging.info(f"Total registros: {df.shape[0]}")

        # Renombrar columna reservada SQL
        df.rename(columns={'default': 'default_col'}, inplace=True)

        # Crear conexión
        engine = create_engine(DATABASE_URL)

        logging.info("Conexión a Neon establecida")

        # ============================================
        # CREAR TABLAS
        # ============================================

        with engine.connect() as connection:

            connection.execute(text(CREATE_CLIENTES_TABLE))
            connection.execute(text(CREATE_CONTACTOS_TABLE))
            connection.execute(text(CREATE_CAMPANAS_TABLE))
            connection.execute(text(CREATE_SUSCRIPCIONES_TABLE))

            connection.commit()

        logging.info("Tablas creadas correctamente")

        # ============================================
        # INSERTAR CLIENTES
        # ============================================

        clientes_df = df[[
            'age',
            'job',
            'marital',
            'education',
            'default_col',
            'balance',
            'housing',
            'loan'
        ]]

        clientes_df.to_sql(
            name='clientes',
            con=engine,
            if_exists='append',
            index=False
        )

        logging.info("Datos insertados en tabla clientes")

        # ============================================
        # OBTENER IDS GENERADOS
        # ============================================

        clientes_ids = pd.read_sql(
            "SELECT cliente_id FROM clientes ORDER BY cliente_id",
            engine
        )

        # Agregar ids al dataframe original
        df['cliente_id'] = clientes_ids['cliente_id']

        # ============================================
        # INSERTAR CONTACTOS
        # ============================================

        contactos_df = df[[
            'cliente_id',
            'contact',
            'day',
            'month',
            'duration',
            'campaign'
        ]]

        contactos_df.to_sql(
            name='contactos',
            con=engine,
            if_exists='append',
            index=False
        )

        logging.info("Datos insertados en tabla contactos")

        # ============================================
        # INSERTAR CAMPAÑAS PREVIAS
        # ============================================

        campanas_df = df[[
            'cliente_id',
            'pdays',
            'previous',
            'poutcome'
        ]]

        campanas_df.to_sql(
            name='campanas_previas',
            con=engine,
            if_exists='append',
            index=False
        )

        logging.info("Datos insertados en campanas_previas")

        # ============================================
        # INSERTAR SUSCRIPCIONES
        # ============================================

        suscripciones_df = df[[
            'cliente_id',
            'deposit'
        ]]

        suscripciones_df.to_sql(
            name='suscripciones',
            con=engine,
            if_exists='append',
            index=False
        )

        logging.info("Datos insertados en suscripciones")

        # ============================================
        # FINALIZAR
        # ============================================

        print("===================================")
        print("CARGA COMPLETADA EXITOSAMENTE")
        print("===================================")

        print("TABLAS CREADAS:")
        print("- clientes")
        print("- contactos")
        print("- campanas_previas")
        print("- suscripciones")

        print(f"Registros cargados: {df.shape[0]}")

        logging.info("Proceso finalizado correctamente")

    except Exception as e:

        logging.error("ERROR EN CARGA")
        logging.error(str(e))

        print("ERROR EN EL PROCESO")
        print(str(e))

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    load_data()