# ============================================
# utils/pipeline_logger.py
# ============================================

import logging
import os
import time
from datetime import datetime

# ============================================
# CREAR CARPETA LOGS
# ============================================

os.makedirs(
    "logs",
    exist_ok=True
)

# ============================================
# LOGGER GLOBAL
# ============================================

pipeline_logger = logging.getLogger(
    "pipeline_report"
)

pipeline_logger.setLevel(
    logging.INFO
)

# ============================================
# EVITAR DUPLICADOS
# ============================================

if not pipeline_logger.handlers:

    file_handler = logging.FileHandler(
        "logs/pipeline_report.log",
        mode="a",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    pipeline_logger.addHandler(
        file_handler
    )

# ============================================
# INICIO PIPELINE
# ============================================

def start_pipeline():

    pipeline_logger.info(
        "\n=================================================="
    )

    pipeline_logger.info(
        "BANK MARKETING DATAOPS PIPELINE"
    )

    pipeline_logger.info(
        "=================================================="
    )

    pipeline_logger.info(
        f"Fecha ejecución: {datetime.now()}"
    )

# ============================================
# SECCIONES
# ============================================

def log_section(title):

    pipeline_logger.info(
        "\n=================================================="
    )

    pipeline_logger.info(
        title
    )

    pipeline_logger.info(
        "=================================================="
    )

# ============================================
# MENSAJES
# ============================================

def log_message(message):

    pipeline_logger.info(
        message
    )

# ============================================
# MÉTRICAS
# ============================================

def log_metric(metric, value):

    pipeline_logger.info(
        f"{metric}: {value}"
    )

# ============================================
# LISTAS
# ============================================

def log_list(title, values):

    pipeline_logger.info(
        title
    )

    for value in values:

        pipeline_logger.info(
            f"- {value}"
        )

# ============================================
# TIEMPOS
# ============================================

def log_execution_time(
    process_name,
    start_time
):

    elapsed = round(
        time.time() - start_time,
        2
    )

    pipeline_logger.info(
        f"Tiempo ejecución "
        f"{process_name}: "
        f"{elapsed} segundos"
    )

# ============================================
# ERRORES
# ============================================

def log_error(error_message):

    pipeline_logger.error(
        error_message
    )

# ============================================
# FIN PIPELINE
# ============================================

def end_pipeline():

    pipeline_logger.info(
        "\n=================================================="
    )

    pipeline_logger.info(
        "PIPELINE FINALIZADO"
    )

    pipeline_logger.info(
        "=================================================="
    )