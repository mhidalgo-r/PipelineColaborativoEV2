import os
import time
import json
import psutil
import logging
from datetime import datetime

# ==========================
# CARPETAS
# ==========================
os.makedirs("logs", exist_ok=True)
os.makedirs("data/outputs", exist_ok=True)

# ==========================
# LOGGER PROPIO
# Usamos nombre especifico para que
# no sea sobreescrito por otros scripts
# cuando se cargan con importlib
# ==========================
logger = logging.getLogger("performance_monitor")
logger.setLevel(logging.INFO)
logger.handlers = []
_handler = logging.FileHandler("logs/performance.log", mode="w", encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(_handler)
logger.propagate = False

# ==========================
# RUTAS
# ==========================
OUTPUT_JSON = "data/outputs/performance_report.json"


# ==========================
# MEDIR ETAPA
# ==========================
def measure_stage(stage_name, func, *args):
    logger.info(f"--- Midiendo etapa: {stage_name} ---")
    cpu_before = psutil.cpu_percent(interval=None)
    ram_before = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    start = time.time()

    try:
        func(*args)
        status = "OK"
    except Exception as e:
        logger.error(f"Error en etapa {stage_name}: {e}")
        status = f"ERROR: {e}"

    elapsed = round(time.time() - start, 4)
    cpu_after = psutil.cpu_percent(interval=1)
    ram_after = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    ram_delta = round(ram_after - ram_before, 2)

    result = {
        "stage": stage_name,
        "status": status,
        "execution_time_sec": elapsed,
        "cpu_percent": cpu_after,
        "ram_used_gb": ram_after,
        "ram_delta_gb": ram_delta,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logger.info(f"Etapa: {stage_name}")
    logger.info(f"  Status:   {status}")
    logger.info(f"  Tiempo:   {elapsed}s")
    logger.info(f"  CPU:      {cpu_after}%")
    logger.info(f"  RAM:      {ram_after}GB (delta: {ram_delta}GB)")

    return result


# ==========================
# ANALIZAR CUELLOS DE BOTELLA
# ==========================
def analyze_bottlenecks(results):
    logger.info("=" * 50)
    logger.info("ANALISIS DE CUELLOS DE BOTELLA")
    logger.info("=" * 50)

    tiempos = [(r["stage"], r["execution_time_sec"]) for r in results if r["status"] == "OK"]
    cpus    = [(r["stage"], r["cpu_percent"])         for r in results if r["status"] == "OK"]
    rams    = [(r["stage"], r["ram_delta_gb"])        for r in results if r["status"] == "OK"]

    if not tiempos:
        return {}

    max_tiempo = max(tiempos, key=lambda x: x[1])
    min_tiempo = min(tiempos, key=lambda x: x[1])
    avg_tiempo = round(sum(t for _, t in tiempos) / len(tiempos), 4)
    max_cpu    = max(cpus, key=lambda x: x[1])
    max_ram    = max(rams, key=lambda x: x[1])

    bottlenecks = {
        "tiempo": {
            "cuello_de_botella": max_tiempo[0],
            "tiempo_sec":        max_tiempo[1],
            "etapa_mas_rapida":  min_tiempo[0],
            "tiempo_min_sec":    min_tiempo[1],
            "promedio_sec":      avg_tiempo
        },
        "cpu": {
            "etapa_mayor_cpu": max_cpu[0],
            "cpu_percent":     max_cpu[1]
        },
        "ram": {
            "etapa_mayor_consumo": max_ram[0],
            "ram_delta_gb":        max_ram[1]
        }
    }

    logger.info(f"Cuello de botella (tiempo): {max_tiempo[0]} con {max_tiempo[1]}s")
    logger.info(f"Etapa mas rapida: {min_tiempo[0]} con {min_tiempo[1]}s")
    logger.info(f"Promedio por etapa: {avg_tiempo}s")
    logger.info(f"Mayor uso CPU: {max_cpu[0]} con {max_cpu[1]}%")
    logger.info(f"Mayor consumo RAM: {max_ram[0]} con delta {max_ram[1]}GB")

    return bottlenecks


# ==========================
# ANALISIS DE ESTABILIDAD
# ==========================
def analyze_stability(func_name, func):
    logger.info("=" * 50)
    logger.info("ANALISIS DE ESTABILIDAD")
    logger.info("=" * 50)

    tiempos = []
    RUNS = 3
    logger.info(f"Ejecutando {func_name} x{RUNS} veces para medir estabilidad")

    for i in range(RUNS):
        start = time.time()
        try:
            func()
        except Exception:
            pass
        elapsed = round(time.time() - start, 4)
        cpu_after = psutil.cpu_percent(interval=0.5)
        tiempos.append(elapsed)
        logger.info(f"  Run {i+1}: {elapsed}s | CPU: {cpu_after}%")

    avg_t    = round(sum(tiempos) / len(tiempos), 4)
    max_t    = max(tiempos)
    min_t    = min(tiempos)
    variacion = round(max_t - min_t, 4)
    estable  = variacion < 0.5

    stability = {
        "etapa_analizada": func_name,
        "runs":            RUNS,
        "tiempos_sec":     tiempos,
        "promedio_sec":    avg_t,
        "max_sec":         max_t,
        "min_sec":         min_t,
        "variacion_sec":   variacion,
        "sistema_estable": estable
    }

    logger.info(f"Promedio: {avg_t}s")
    logger.info(f"Variacion: {variacion}s")
    logger.info(f"Sistema estable: {estable}")

    return stability


# ==========================
# MONITOR GENERAL
# ==========================
def monitor():
    logger.info("=" * 50)
    logger.info("INICIO MONITOREO DE RENDIMIENTO")
    logger.info("=" * 50)

    try:
        cpu_total  = psutil.cpu_percent(interval=1)
        memory     = psutil.virtual_memory()
        ram_total  = round(memory.total / (1024 ** 3), 2)
        ram_used   = round(memory.used  / (1024 ** 3), 2)
        ram_percent = memory.percent

        logger.info("--- Estado general del sistema ---")
        logger.info(f"CPU total: {cpu_total}%")
        logger.info(f"RAM total: {ram_total}GB")
        logger.info(f"RAM usada: {ram_used}GB ({ram_percent}%)")

        results      = []
        loaded_funcs = {}
        import importlib.util

        stages = [
            ("Ingestion",      "scripts/ingest/ingestion_data.py",      "ingest_data"),
            ("Cleaning",       "scripts/cleaning/cleaning_data.py",     "clean_data"),
            ("Transformation", "scripts/transform/transform_data.py",   "transform_data"),
            ("Validation",     "scripts/validation/validation_data.py", "validate_data"),
            ("Loading",        "scripts/load/loading_data.py",          "load_data"),
            ("EDA Quality",    "scripts/eda/quality_analysis.py",       "analyze_data"),
            ("EDA Visual",     "scripts/eda/visual_eda.py",             "execute_eda"),
            ("Training",       "scripts/modeling/train_model.py",       "train"),
            ("Evaluation",     "scripts/modeling/evaluate_model.py",    "evaluate"),
            ("Security Audit", "scripts/security/security_audit.py",    "audit"),
        ]

        for stage_name, script_path, func_name in stages:
            if os.path.exists(script_path):
                try:
                    spec   = importlib.util.spec_from_file_location(stage_name, script_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    func   = getattr(module, func_name)
                    loaded_funcs[stage_name] = func
                    result = measure_stage(stage_name, func)
                except Exception as e:
                    logger.error(f"No se pudo cargar {script_path}: {e}")
                    result = {
                        "stage": stage_name, "status": f"ERROR CARGA: {e}",
                        "execution_time_sec": 0, "cpu_percent": 0,
                        "ram_used_gb": 0, "ram_delta_gb": 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
            else:
                logger.warning(f"Script no encontrado: {script_path}")
                result = {
                    "stage": stage_name, "status": "SCRIPT NO ENCONTRADO",
                    "execution_time_sec": 0, "cpu_percent": 0,
                    "ram_used_gb": 0, "ram_delta_gb": 0,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            results.append(result)

        bottlenecks = analyze_bottlenecks(results)

        stability = {}
        if "EDA Quality" in loaded_funcs:
            stability = analyze_stability("EDA Quality", loaded_funcs["EDA Quality"])

        # LATENCIA DB
        logger.info("=" * 50)
        logger.info("ANALISIS DE LATENCIA")
        logger.info("=" * 50)

        latency = {}
        try:
            from dotenv import load_dotenv
            import sqlalchemy
            load_dotenv()
            db_url = os.getenv("DATABASE_URL")
            if db_url:
                engine    = sqlalchemy.create_engine(db_url)
                latencias = []
                for i in range(3):
                    start = time.time()
                    with engine.connect() as conn:
                        conn.execute(sqlalchemy.text("SELECT 1"))
                    elapsed = round(time.time() - start, 4)
                    latencias.append(elapsed)
                    logger.info(f"  Ping DB {i+1}: {elapsed}s")
                latency = {
                    "pings":        latencias,
                    "promedio_sec": round(sum(latencias) / len(latencias), 4),
                    "max_sec":      max(latencias),
                    "min_sec":      min(latencias)
                }
                logger.info(f"Latencia promedio DB: {latency['promedio_sec']}s")
            else:
                logger.warning("DATABASE_URL no encontrada en .env")
                latency = {"error": "DATABASE_URL no configurada"}
        except Exception as e:
            logger.warning(f"No se pudo medir latencia DB: {e}")
            latency = {"error": str(e)}

        total_time = round(sum(r["execution_time_sec"] for r in results), 2)

        report = {
            "environment":             "local",
            "timestamp":               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system": {
                "cpu_percent":   cpu_total,
                "ram_total_gb":  ram_total,
                "ram_used_gb":   ram_used,
                "ram_percent":   ram_percent
            },
            "total_execution_time_sec": total_time,
            "stages":      results,
            "bottlenecks": bottlenecks,
            "stability":   stability,
            "latency_db":  latency
        }

        with open(OUTPUT_JSON, "w") as f:
            json.dump(report, f, indent=4)

        logger.info("=" * 50)
        logger.info("RESUMEN FINAL")
        logger.info("=" * 50)
        logger.info(f"Tiempo total pipeline: {total_time}s")
        logger.info(f"Reporte guardado: {OUTPUT_JSON}")

        print("\nMonitoreo completado:")
        print(f"  CPU: {cpu_total}%")
        print(f"  RAM: {ram_used}GB / {ram_total}GB")
        print(f"  Tiempo total: {total_time}s")
        if bottlenecks:
            print(f"  Cuello de botella: {bottlenecks['tiempo']['cuello_de_botella']} ({bottlenecks['tiempo']['tiempo_sec']}s)")
            print(f"  Etapa mas rapida:  {bottlenecks['tiempo']['etapa_mas_rapida']} ({bottlenecks['tiempo']['tiempo_min_sec']}s)")
        if stability:
            print(f"  Sistema estable: {stability.get('sistema_estable', 'N/A')}")
        print(f"  Reporte: {OUTPUT_JSON}")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    monitor()