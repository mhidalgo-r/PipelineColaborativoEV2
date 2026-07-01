"""
main.py
========
Punto de entrada único del proyecto Pipeline Bank Marketing EV3.

Ejecuta en orden:
1. ETL (ingesta, limpieza, transformacion, validacion, carga)
2. EDA (calidad de datos, graficos)
3. Modelo de IA (entrenamiento, evaluacion)
4. Auditoria de seguridad
5. Monitoreo de rendimiento
6. Dashboard interactivo (Streamlit)

Uso:
    python main.py            -> corre todo el pipeline + abre el dashboard
    python main.py --no-dash  -> corre todo el pipeline sin abrir el dashboard
"""

import sys
import time
import subprocess
import importlib

# ==========================
# ETAPAS DEL PIPELINE
# Cada tupla: (Nombre visible, modulo, funcion a ejecutar)
# ==========================
STAGES = [
    ("Ingesta",              "scripts.ingest.ingestion_data",     "ingest_data"),
    ("Limpieza",             "scripts.cleaning.cleaning_data",    "clean_data"),
    ("Transformacion",       "scripts.transform.transform_data",  "transform_data"),
    ("Validacion",           "scripts.validation.validation_data", "validate_data"),
    ("Carga",                "scripts.load.loading_data",          "load_data"),
    ("Calidad de Datos",     "scripts.eda.quality_analysis",       "analyze_data"),
    ("EDA Visual",           "scripts.eda.visual_eda",             "execute_eda"),
    ("Entrenamiento Modelo", "scripts.modeling.train_model",       "train"),
    ("Evaluacion Modelo",    "scripts.modeling.evaluate_model",    "evaluate"),
    ("Auditoria Seguridad",  "scripts.security.security_audit",    "audit"),
    ("Monitoreo Rendimiento","scripts.performance.performance_monitor", "monitor"),
]


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def run_stage(stage_name, module_name, func_name):
    print_header(f"ETAPA: {stage_name}")
    start = time.time()
    try:
        # Si el módulo ya fue cargado previamente por efectos secundarios, lo removemos
        # para forzar una carga limpia y aislada de la etapa actual.
        if module_name in sys.modules:
            del sys.modules[module_name]
            
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        func()
        
        elapsed = round(time.time() - start, 2)
        print(f"\n[OK] {stage_name} completada en {elapsed}s")
        return True
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        print(f"\n[ERROR] {stage_name} falló después de {elapsed}s")
        print(f"Detalle: {e}")
        return False


def run_pipeline():
    print_header("PIPELINE BANK MARKETING EV3 - INICIO")
    total_start = time.time()

    results = []
    for stage_name, module_name, func_name in STAGES:
        ok = run_stage(stage_name, module_name, func_name)
        results.append((stage_name, ok))
        
        # Parada de emergencia si una etapa base del ETL llega a fallar catastróficamente
        if not ok and stage_name in ["Ingesta", "Limpieza", "Transformacion"]:
            print(f"\n[CRÍTICO] Deteniendo el pipeline preventivamente: Falla estructural en {stage_name}")
            break

    total_elapsed = round(time.time() - total_start, 2)

    print_header("RESUMEN DE EJECUCIÓN")
    for stage_name, ok in results:
        status = "OK" if ok else "FALLÓ"
        print(f"  [{status}] {stage_name}")

    failed = [name for name, ok in results if not ok]

    print(f"\nTiempo total del pipeline: {total_elapsed}s")

    if failed:
        print(f"\nEtapas con error: {', '.join(failed)}")
        print("Revisa los logs en la carpeta logs/ para más detalle.")
        return False
    else:
        print("\nTodas las etapas se ejecutaron correctamente.")
        return True


def run_dashboard():
    print_header("INICIANDO DASHBOARD (Streamlit)")
    print("Presiona CTRL+C para detener el dashboard.\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\nDashboard detenido por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] No se pudo iniciar el dashboard: {e}")


# ==============================================================================
# 🔥 PUNTO DE ENTRADA PRINCIPAL ÚNICO
# ==============================================================================
if __name__ == "__main__":
    no_dashboard = "--no-dash" in sys.argv

    pipeline_ok = run_pipeline()

    if not no_dashboard:
        if pipeline_ok:
            run_dashboard()
        else:
            print("\nEl pipeline tuvo errores. ¿Deseas iniciar el dashboard igualmente? (s/n)")
            respuesta = input("> ").strip().lower()
            if respuesta == "s":
                run_dashboard()
            else:
                print("Dashboard no iniciado. Revisa los errores antes de continuar.")
    else:
        print("\nDashboard omitido (--no-dash). Para abrirlo manualmente:")
        print("  streamlit run dashboard/app.py")