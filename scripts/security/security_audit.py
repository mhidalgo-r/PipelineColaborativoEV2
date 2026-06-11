import os
import logging

# ==========================
# CARPETAS
# ==========================
os.makedirs("logs", exist_ok=True)

# ==========================
# LOGGER
# ==========================
logging.basicConfig(
    filename="logs/security_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger()

# ==========================
# KEYWORDS SENSIBLES
# ==========================
KEYWORDS = [
    "password",
    "secret",
    "apikey",
    "token",
    "credential",
    "private_key"
]

# Columnas sensibles segun Ley 19.628
SENSITIVE_COLUMNS = [
    "age",
    "job",
    "marital",
    "education",
    "balance",
    "default"
]

# ==========================
# AUDITORIA PRINCIPAL
# ==========================
def audit():
    logger.info("=" * 50)
    logger.info("INICIO AUDITORIA DE SEGURIDAD")
    logger.info("=" * 50)

    try:
        # ==============================
        # 1. VERIFICAR .env
        # ==============================
        logger.info("--- Verificacion .env ---")
        if os.path.exists(".env"):
            logger.info(".env encontrado - credenciales protegidas")
        else:
            logger.warning(".env NO encontrado - credenciales en riesgo")

        # ==============================
        # 2. VERIFICAR .gitignore
        # ==============================
        logger.info("--- Verificacion .gitignore ---")
        if os.path.exists(".gitignore"):
            with open(".gitignore", encoding="utf-8") as f:
                gitignore_content = f.read()
            if ".env" in gitignore_content:
                logger.info(".env esta en .gitignore - protegido de repositorio")
            else:
                logger.warning(".env NO esta en .gitignore - riesgo de exposicion")
        else:
            logger.warning(".gitignore NO encontrado")

        # ==============================
        # 3. BUSQUEDA DE SECRETOS EN .py
        # ==============================
        logger.info("--- Busqueda de secretos en codigo ---")
        found = []
        for root, dirs, files in os.walk("."):
            # Ignorar carpetas de entorno virtual
            dirs[:] = [
                d for d in dirs
                if d not in ["venv", ".venv", "__pycache__", ".git"]
            ]
            for file in files:
                if file.endswith(".py") and file != "security_audit.py":
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read().lower()
                            for k in KEYWORDS:
                                if k in content:
                                    found.append(f"{file}: {k}")
                    except Exception as e:
                        logger.warning(
                            f"No se pudo leer {file}: {e}"
                        )

        if found:
            logger.warning(f"Posibles secretos detectados: {found}")
        else:
            logger.info("No se detectaron secretos hardcodeados en codigo")

        # ==============================
        # 4. VERIFICAR DOCKERFILE
        # ==============================
        logger.info("--- Verificacion Dockerfile ---")
        if os.path.exists("Dockerfile"):
            with open("Dockerfile", encoding="utf-8") as f:
                docker_content = f.read()
            if "USER" not in docker_content:
                logger.warning(
                    "Dockerfile no define USER - posible ejecucion como root"
                )
            else:
                logger.info("Dockerfile define usuario - buena practica")

            if "COPY . ." in docker_content:
                logger.warning(
                    "Dockerfile usa COPY . . - puede copiar archivos sensibles"
                )
            else:
                logger.info("Dockerfile no copia directorio completo")
        else:
            logger.warning("Dockerfile no encontrado")

        # ==============================
        # 5. LEY 19.628 - DATOS PERSONALES
        # ==============================
        logger.info("--- Verificacion Ley 19.628 Chile ---")
        logger.info(
            "Columnas sensibles identificadas segun Ley 19.628 "
            "(Proteccion de Datos Personales):"
        )
        for col in SENSITIVE_COLUMNS:
            logger.info(f"  [SENSIBLE] {col}")

        logger.info(
            "Recomendacion: anonimizar o enmascarar estas columnas "
            "en entornos de produccion"
        )
        logger.info(
            "Recomendacion: no almacenar datos personales sin "
            "consentimiento explicito del titular"
        )

        # ==============================
        # 6. VERIFICAR ARCHIVOS SENSIBLES
        # ==============================
        logger.info("--- Verificacion archivos sensibles ---")
        sensitive_files = [".env", "models/bank_model.pkl", "models/encoder.pkl"]
        for sf in sensitive_files:
            if os.path.exists(sf):
                logger.info(f"Archivo sensible presente: {sf}")
            else:
                logger.warning(f"Archivo no encontrado: {sf}")

        print("\nAuditoria de seguridad completada")
        print("  Revisa: logs/security_audit.log")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    audit()