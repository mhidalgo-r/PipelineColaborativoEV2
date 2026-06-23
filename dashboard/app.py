import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Bank Pipeline Dashboard",
    layout="wide"
)

# ==========================
# TITULO
# ==========================
st.title("Bank Marketing Dashboard")
st.write("Gestión de Datos para IA - ITY1101")
st.divider()

# ==========================
# CARGA SEGURA DE DATOS
# ==========================
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

validated = load_csv("data/validated/bank_validated.csv")
rejected  = load_csv("data/reject/bank_rejected.csv")
premium   = load_csv("data/validated/bank_premium.csv")
metrics   = load_json("data/outputs/model_metrics.json")
perf      = load_json("data/outputs/performance_report.json")

# ==========================
# FUNCION SEMAFORO
# ==========================
def semaforo(valor, umbral_verde=0.80, umbral_amarillo=0.60):
    if valor is None or valor == "N/A":
        return "⚪"
    if valor >= umbral_verde:
        return "🟢"
    elif valor >= umbral_amarillo:
        return "🟡"
    else:
        return "🔴"

# Explicaciones para tooltips
EXPLICACIONES = {
    "accuracy":  "Porcentaje total de predicciones correctas del modelo sobre el total de casos evaluados.",
    "recall":    "De los clientes que realmente depositaron, qué porcentaje fue detectado correctamente por el modelo.",
    "precision": "De los clientes que el modelo predijo como depositantes, qué porcentaje realmente lo fue.",
    "f1":        "Promedio armónico entre Precision y Recall. Equilibra ambas métricas en un solo valor.",
    "auc":       "Área bajo la curva ROC. Mide qué tan bien distingue el modelo entre clientes que depositan y los que no. Más cercano a 1 es mejor.",
    "gini":      "Indicador de poder predictivo del modelo, calculado como (2 x AUC) - 1. Muy usado en modelos de scoring bancario.",
}

# ==========================
# SIDEBAR FILTROS
# ==========================
st.sidebar.title("Filtros")

if not validated.empty and "risk_level" in validated.columns:
    risk_options = ["Todos"] + sorted(
        validated["risk_level"].dropna().unique().tolist()
    )
    selected_risk = st.sidebar.selectbox(
        "Filtrar por Risk Level",
        risk_options
    )
else:
    selected_risk = "Todos"

if not validated.empty and "age" in validated.columns:
    min_age = int(validated["age"].min())
    max_age = int(validated["age"].max())
    age_range = st.sidebar.slider(
        "Rango de Edad",
        min_age, max_age,
        (min_age, max_age)
    )
else:
    age_range = None


def aplicar_filtros(df):
    """Aplica los filtros del sidebar a cualquier dataframe de clientes."""
    if df.empty:
        return df
    filtered = df.copy()
    if selected_risk != "Todos" and "risk_level" in filtered.columns:
        filtered = filtered[filtered["risk_level"] == selected_risk]
    if age_range is not None and "age" in filtered.columns:
        filtered = filtered[
            (filtered["age"] >= age_range[0]) &
            (filtered["age"] <= age_range[1])
        ]
    return filtered


# ==========================
# KPIs PIPELINE
# ==========================
st.subheader("KPIs del Pipeline")
total = len(validated) + len(rejected)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Procesados", total, help="Suma de todos los clientes que pasaron por el pipeline ETL.")
c2.metric("Aprobados", len(validated), help="Clientes que cumplieron las reglas de negocio en la etapa de validación.")
c3.metric("Rechazados", len(rejected), help="Clientes que no cumplieron las reglas de negocio establecidas.")
c4.metric("Premium", len(premium), help="Clientes aprobados clasificados con el nivel más alto de valor comercial.")

st.divider()

# ==========================
# METRICAS MODELO IA (con semaforo y tooltips)
# ==========================
st.subheader("Métricas del Modelo IA")
st.caption("🟢 Bueno (≥0.80)  🟡 Aceptable (0.60-0.80)  🔴 Bajo (<0.60)  — Pasa el mouse sobre cada métrica para ver su significado")

if metrics:
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    m1.metric(
        f"{semaforo(metrics.get('accuracy'))} Accuracy",
        f"{metrics.get('accuracy', 'N/A')}",
        help=EXPLICACIONES["accuracy"]
    )
    m2.metric(
        f"{semaforo(metrics.get('recall'))} Recall",
        f"{metrics.get('recall', 'N/A')}",
        help=EXPLICACIONES["recall"]
    )
    m3.metric(
        f"{semaforo(metrics.get('precision'))} Precision",
        f"{metrics.get('precision', 'N/A')}",
        help=EXPLICACIONES["precision"]
    )
    m4.metric(
        f"{semaforo(metrics.get('f1'))} F1 Score",
        f"{metrics.get('f1', 'N/A')}",
        help=EXPLICACIONES["f1"]
    )
    m5.metric(
        f"{semaforo(metrics.get('auc'))} AUC",
        f"{metrics.get('auc', 'N/A')}",
        help=EXPLICACIONES["auc"]
    )
    m6.metric(
        f"{semaforo(metrics.get('gini'))} Gini",
        f"{metrics.get('gini', 'N/A')}",
        help=EXPLICACIONES["gini"]
    )

    # ==========================
    # COMPARACION DE MODELOS
    # ==========================
    comparison = metrics.get("model_comparison")
    if comparison:
        st.markdown("##### Comparación de Modelos")
        logreg = comparison["logistic_regression"]
        tree = comparison["decision_tree"]
        winner = comparison["winner"]

        comp_df = pd.DataFrame({
            "Métrica": ["Accuracy", "Precision", "Recall", "F1 Score", "AUC", "Gini"],
            "Regresión Logística": [
                logreg["accuracy"], logreg["precision"], logreg["recall"],
                logreg["f1"], logreg["auc"], logreg["gini"]
            ],
            "Árbol de Decisión": [
                tree["accuracy"], tree["precision"], tree["recall"],
                tree["f1"], tree["auc"], tree["gini"]
            ]
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        winner_label = "Regresión Logística" if winner == "logistic_regression" else "Árbol de Decisión"
        st.success(f"🏆 Modelo con mejor AUC: **{winner_label}**. El modelo en producción (bank_model.pkl) es Regresión Logística, elegida por su interpretabilidad y bajo costo computacional.")

        with st.expander("ℹ️ ¿Por qué se eligió Regresión Logística si no tiene el mejor AUC?"):
            if winner == "decision_tree":
                st.markdown(f"""
                Cuando se compararon ambos modelos en este dataset, el **Árbol de Decisión** obtuvo un AUC de **{tree['auc']}**,
                más alto que el AUC de **{logreg['auc']}** de la Regresión Logística. Esto significa que, técnicamente,
                el Árbol discriminó un poco mejor entre los clientes que depositan y los que no.

                Sin embargo, se mantuvo la **Regresión Logística como modelo en producción** por las siguientes razones:

                - **Interpretabilidad:** sus coeficientes permiten explicar exactamente cuánto influye cada variable en la predicción,
                  algo valorado en entornos bancarios regulados.
                - **Menor costo computacional:** es más rápida de entrenar y ejecutar dentro del pipeline automatizado.
                - **Menor riesgo de sobreajuste:** los árboles de decisión, incluso con profundidad limitada, son más propensos
                  a memorizar patrones específicos del conjunto de entrenamiento.

                En resumen: se priorizó la **explicabilidad del modelo** sobre la ganancia marginal de precisión que ofrecía el árbol.
                """)
            else:
                st.markdown(f"""
                La Regresión Logística obtuvo el mejor AUC ({logreg['auc']}) frente al Árbol de Decisión ({tree['auc']}),
                confirmando que en este dataset es tanto la opción más interpretable como la de mejor desempeño.
                """)

    # ==========================
    # IMPORTANCIA DE VARIABLES
    # ==========================
    importance = metrics.get("feature_importance")
    if importance:
        st.markdown("##### Importancia de Variables")
        st.caption("Qué variables influyen más en la predicción de cada modelo")

        imp_tab1, imp_tab2 = st.tabs(["Regresión Logística", "Árbol de Decisión"])

        with imp_tab1:
            logreg_imp_df = pd.DataFrame(importance["logistic_regression"][:10])
            logreg_imp_df.columns = ["Variable", "Importancia (%)"]
            st.bar_chart(logreg_imp_df.set_index("Variable"))
            st.caption("En Regresión Logística, la importancia es el % que representa el coeficiente de cada variable sobre el total.")

        with imp_tab2:
            tree_imp_df = pd.DataFrame(importance["decision_tree"][:10])
            tree_imp_df.columns = ["Variable", "Importancia (%)"]
            st.bar_chart(tree_imp_df.set_index("Variable"))
            st.caption("En el Árbol de Decisión, el % indica cuánto contribuye cada variable a reducir la incertidumbre al dividir los datos.")
else:
    st.warning("Métricas no disponibles. Ejecuta evaluate_model.py primero.")

st.divider()

# ==========================
# GRAFICOS EDA Y MODELO
# ==========================
st.subheader("Gráficos EDA y Modelo")

figures = {
    "Matriz de Confusion": {
        "path": "reports/figures/confusion_matrix.png",
        "explicacion": """
**¿Qué muestra?** Una tabla que compara las predicciones del modelo contra los resultados reales.

**¿Para qué sirve?** Permite ver exactamente dónde se equivoca el modelo: cuántos clientes que sí depositaron fueron detectados correctamente,
y cuántos casos se confundieron en cada dirección (falsos positivos y falsos negativos).

**¿Por qué es importante?** En un banco, un falso negativo (decir que no depositará cuando sí lo haría) significa una oportunidad de venta perdida.
Un falso positivo (decir que sí depositará cuando no lo hará) significa gastar recursos en una llamada que no convertirá.
"""
    },
    "Curva ROC (comparativa)": {
        "path": "reports/figures/roc_curve.png",
        "explicacion": """
**¿Qué muestra?** Qué tan bien cada modelo distingue entre clientes que depositan y los que no, probando distintos umbrales de decisión.

**¿Para qué sirve?** Mientras más se aleje la curva de la línea diagonal (que representa un modelo aleatorio), mejor es el modelo.
El área bajo la curva (AUC) resume esta capacidad en un solo número.

**¿Por qué es importante?** Permite comparar visualmente la Regresión Logística contra el Árbol de Decisión y decidir cuál discrimina mejor
entre las dos clases, sin depender de un único umbral de corte.
"""
    },
    "Correlacion Variables": {
        "path": "reports/figures/correlation.png",
        "explicacion": """
**¿Qué muestra?** Qué tan relacionadas están las variables numéricas entre sí, con valores entre -1 y 1.

**¿Para qué sirve?** Identificar qué variables se mueven juntas. Valores cercanos a 1 o -1 indican relación fuerte,
valores cercanos a 0 indican que las variables son independientes.

**¿Por qué es importante?** Ayuda a entender qué variables podrían ser redundantes entre sí y cuáles tienen mayor relación
con la variable objetivo (deposit), orientando la selección de variables para el modelo.
"""
    },
    "Distribucion Edad": {
        "path": "reports/figures/hist_age.png",
        "explicacion": """
**¿Qué muestra?** Cómo se distribuyen las edades de los clientes del banco.

**¿Para qué sirve?** Conocer el perfil demográfico general de la base de clientes, identificando en qué rango de edad
se concentra la mayoría.

**¿Por qué es importante?** Permite verificar si el modelo está entrenando con una muestra representativa de la población
real de clientes, y detectar si hay sesgos hacia algún grupo etario.
"""
    },
    "Balance vs Deposito": {
        "path": "reports/figures/balance_vs_deposit.png",
        "explicacion": """
**¿Qué muestra?** Compara el balance de cuenta entre los clientes que depositaron y los que no.

**¿Para qué sirve?** Ver si existe una diferencia notable en el saldo bancario entre ambos grupos.

**¿Por qué es importante?** Si el balance fuera muy distinto entre grupos, sería una señal fuerte para el modelo.
En este caso la diferencia es moderada, lo que indica que el balance contribuye pero no es el único factor decisivo.
"""
    },
    "Edad vs Deposito": {
        "path": "reports/figures/age_vs_deposit.png",
        "explicacion": """
**¿Qué muestra?** Compara la edad entre los clientes que depositaron y los que no.

**¿Para qué sirve?** Ver si la edad por sí sola diferencia a ambos grupos de clientes.

**¿Por qué es importante?** Ambos grupos muestran edades similares, lo que indica que la edad sola no es un buen predictor.
Su valor real aparece al combinarla con otras variables como balance y duration.
"""
    },
}

cols = st.columns(2)
for i, (title, data) in enumerate(figures.items()):
    with cols[i % 2]:
        if os.path.exists(data["path"]):
            st.image(data["path"], caption=title, use_column_width=True)
            with st.expander(f"ℹ️ ¿Qué muestra este gráfico?"):
                st.markdown(data["explicacion"])
        else:
            st.info(f"{title} no disponible aun")

st.divider()

# ==========================
# RENDIMIENTO POR ETAPA
# ==========================
st.subheader("Rendimiento del Pipeline por Etapa")

if perf and "stages" in perf:
    perf_df = pd.DataFrame(perf["stages"])
    if not perf_df.empty:
        st.bar_chart(
            perf_df.set_index("stage")["execution_time_sec"]
        )
        st.dataframe(
            perf_df[[
                "stage",
                "status",
                "execution_time_sec",
                "cpu_percent",
                "ram_used_gb"
            ]],
            use_container_width=True
        )

        sys_info = perf.get("system", {})
        p1, p2, p3 = st.columns(3)
        p1.metric(
            "CPU Sistema",
            f"{sys_info.get('cpu_percent', 'N/A')}%",
            help="Porcentaje de uso del procesador del computador en el momento de ejecutar el pipeline. Un valor alto indica que el equipo estaba trabajando intensamente durante el proceso."
        )
        p2.metric(
            "RAM Usada",
            f"{sys_info.get('ram_used_gb', 'N/A')}GB",
            help="Cantidad de memoria RAM que estaba en uso en el computador durante la ejecución del pipeline. No es exclusiva del pipeline, incluye también otros programas abiertos."
        )
        p3.metric(
            "Tiempo Total",
            f"{perf.get('total_execution_time_sec', 'N/A')}s",
            help="Suma de los tiempos de ejecución de todas las etapas del pipeline, desde la ingesta hasta la auditoría de seguridad."
        )

else:
    st.warning(
        "Datos de rendimiento no disponibles. "
        "Ejecuta performance_monitor.py primero."
    )

st.divider()

# ==========================
# TABLA DE CLIENTES (con tabs)
# ==========================
st.subheader("Clientes del Pipeline")

tab_aprobados, tab_rechazados, tab_premium = st.tabs([
    f"✅ Aprobados ({len(validated)})",
    f"❌ Rechazados ({len(rejected)})",
    f"⭐ Premium ({len(premium)})"
])

with tab_aprobados:
    validated_filtered = aplicar_filtros(validated)
    if not validated_filtered.empty:
        st.write(f"Mostrando {len(validated_filtered)} de {len(validated)} registros")
        st.dataframe(validated_filtered.head(50), use_container_width=True)
    else:
        st.warning("No hay clientes aprobados que coincidan con los filtros.")

with tab_rechazados:
    rejected_filtered = aplicar_filtros(rejected)
    if not rejected_filtered.empty:
        st.write(f"Mostrando {len(rejected_filtered)} de {len(rejected)} registros")
        st.dataframe(rejected_filtered.head(50), use_container_width=True)
    else:
        st.warning("No hay clientes rechazados que coincidan con los filtros.")

with tab_premium:
    premium_filtered = aplicar_filtros(premium)
    if not premium_filtered.empty:
        st.write(f"Mostrando {len(premium_filtered)} de {len(premium)} registros")
        st.dataframe(premium_filtered.head(50), use_container_width=True)
    else:
        st.warning("No hay clientes premium que coincidan con los filtros.")

st.divider()

# ==========================
# GRAFICO INTERACTIVO
# ==========================
st.subheader("Distribución Interactiva de Edad")

validated_filtered_chart = aplicar_filtros(validated)
if not validated_filtered_chart.empty and "age" in validated_filtered_chart.columns:
    age_counts = validated_filtered_chart["age"].value_counts().sort_index()
    st.bar_chart(age_counts)
    st.caption("Distribución de edad en clientes aprobados (filtrable desde sidebar)")