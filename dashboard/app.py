import streamlit as st
import pandas as pd
import json
import os
import joblib  # <--- Necesario para cargar el modelo .pkl en tiempo real

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

# ==============================================================================
# 📊 METRICAS MODELO IA (Con semáforo, 3 decimales y tooltips)
# ==============================================================================
st.subheader("Métricas de Rendimiento de la IA")
st.caption("🟢 Excelente (≥0.800)   🟡 Aceptable (0.600-0.799)   🔴 Crítico (<0.600)  — Pasa el cursor sobre la métrica para ver su definición técnica.")

if metrics:
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    # Captura segura y formateo estricto a 3 decimales
    acc_val = float(metrics.get('accuracy', 0))
    rec_val = float(metrics.get('recall', 0))
    pre_val = float(metrics.get('precision', 0))
    f1_val  = float(metrics.get('f1', 0))
    auc_val = float(metrics.get('auc', 0))
    gin_val = float(metrics.get('gini', 0))

    m1.metric(
        label=f"{semaforo(acc_val)} Accuracy",
        value=f"{acc_val:.3f}",
        help=EXPLICACIONES.get("accuracy", "Exactitud global del modelo.")
    )
    m2.metric(
        label=f"{semaforo(rec_val)} Recall",
        value=f"{rec_val:.3f}",
        help=EXPLICACIONES.get("recall", "Capacidad del modelo para capturar casos positivos.")
    )
    m3.metric(
        label=f"{semaforo(pre_val)} Precision",
        value=f"{pre_val:.3f}",
        help=EXPLICACIONES.get("precision", "Certeza de las predicciones positivas del modelo.")
    )
    m4.metric(
        label=f"{semaforo(f1_val)} F1 Score",
        value=f"{f1_val:.3f}",
        help=EXPLICACIONES.get("f1", "Balance armónico entre Precisión y Recall.")
    )
    m5.metric(
        label=f"{semaforo(auc_val)} AUC ROC",
        value=f"{auc_val:.3f}",
        help=EXPLICACIONES.get("auc", "Capacidad del modelo para discriminar entre clases.")
    )
    m6.metric(
        label=f"{semaforo(gin_val)} Coeficiente Gini",
        value=f"{gin_val:.3f}",
        help=EXPLICACIONES.get("gini", "Métrica de desigualdad predictiva derivada del AUC.")
    )

    st.write("")

    # ==============================================================================
    # ⚖️ COMPARACION DE MODELOS (Estilizada y Dinámica)
    # ==============================================================================
    comparison = metrics.get("model_comparison")
    if comparison:
        st.markdown("##### Comparación de Algoritmos Evaluados")
        logreg = comparison["logistic_regression"]
        tree = comparison["decision_tree"]
        winner = comparison["winner"]

        # Crear estructura con formateo numérico explícito
        comp_df = pd.DataFrame({
            "Métrica de Control": ["Accuracy", "Precision", "Recall", "F1 Score", "AUC", "Gini"],
            "Regresión Logística (Producción)": [
                float(logreg["accuracy"]), float(logreg["precision"]), float(logreg["recall"]),
                float(logreg["f1"]), float(logreg["auc"]), float(logreg["gini"])
            ],
            "Árbol de Decisión (Baseline)": [
                float(tree["accuracy"]), float(tree["precision"]), float(tree["recall"]),
                float(tree["f1"]), float(tree["auc"]), float(tree["gini"])
            ]
        })
        
        # Estilizar el DataFrame: Formatear a 3 decimales y resaltar el valor máximo de cada fila
        styled_df = comp_df.style.format({
            "Regresión Logística (Producción)": "{:.3f}",
            "Árbol de Decisión (Baseline)": "{:.3f}"
        }).highlight_max(axis=1, subset=["Regresión Logística (Producción)", "Árbol de Decisión (Baseline)"], props='font-weight: bold; color: #2ecc71;')

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

        winner_label = "Regresión Logística" if winner == "logistic_regression" else "Árbol de Decisión"
        st.success(f"🏆 **Ganador del Pipeline:** El modelo con mejor desempeño general y mayor poder de discriminación es **{winner_label}**.")

        # Justificación de Negocio expandible
        with st.expander("ℹ️ Defensa del Modelo: ¿Por qué la Regresión Logística dominó el pipeline?"):
            st.markdown(f"""
            Tras el procesamiento automatizado y la corrección de asimetrías mediante escalamiento estándar (`StandardScaler`), la **Regresión Logística** demostró una superioridad matemática contundente sobre el Árbol de Decisión:

            * **Poder de Discriminación Superior:** Alcanzó un **AUC de {float(logreg['auc']):.3f}** (Gini de {float(logreg['gini']):.3f}) frente al **{float(tree['auc']):.3f}** del Árbol de Decisión. Esto garantiza una menor tasa de falsos positivos en las campañas.
            * **Inmunidad al Ruido (Varianza):** Los árboles de decisión tienden a sobreajustar (*overfitting*) en datos tabulares con variables continuas volátiles como `balance` y `duration`. La Regresión Logística actúa de forma más robusta y generalizable en datos de testeo.
            * **Cumplimiento Normativo Bancario:** Cumple con el principio de **Explicabilidad**. Cada coeficiente del modelo representa el riesgo real de la operación, permitiendo auditar las decisiones predictivas frente a comités de riesgo y auditorías de seguridad del negocio.
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
        p1.metric("CPU Sistema",   f"{sys_info.get('cpu_percent', 'N/A')}%")
        p2.metric("RAM Usada",     f"{sys_info.get('ram_used_gb', 'N/A')}GB")
        p3.metric("Tiempo Total",  f"{perf.get('total_execution_time_sec', 'N/A')}s")

        bottlenecks = perf.get("bottlenecks", {})
        if bottlenecks:
            tiempo_info = bottlenecks.get("tiempo", {})
            st.info(
                f"⚠️ Cuello de botella: **{tiempo_info.get('cuello_de_botella', 'N/A')}** "
                f"con {tiempo_info.get('tiempo_sec', 'N/A')}s"
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

st.divider()


# ==============================================================================
# 🚀 NUEVA SECCIÓN: SIMULADOR DE PROPENSÍON EN TIEMPO REAL (MLOps INDUSTRIAL)
# ==============================================================================
st.subheader("🔮 Simulador de Propensión de Clientes (IA Real en Producción)")
st.caption("Esta sección realiza inferencia matemática directa cargando el artefacto `.pkl` generado por el pipeline.")

MODEL_PATH = "models/bank_model.pkl"
SCALER_PATH = "models/scaler.pkl"
ENCODER_PATH = "models/encoder.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(ENCODER_PATH):
    
    # Cargar los componentes binarios de la IA de forma interna
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODER_PATH)

    # Crear columnas para los controles de entrada de datos
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        age_input = st.slider("Edad del Prospecto", 18, 95, 35)
        balance_input = st.number_input("Balance de la Cuenta ($)", value=1000)
        duration_input = st.slider("Duración de la llamada (segundos)", 0, 1500, 180)
        
    with sc2:
        job_input = st.selectbox("Ocupación / Cargo", ["management", "technician", "blue-collar", "admin.", "services", "retired", "self-employed", "unemployed", "entrepreneur", "housemaid", "student"])
        marital_input = st.selectbox("Estado Civil", ["married", "single", "divorced"])
        education_input = st.selectbox("Nivel Educacional", ["secondary", "tertiary", "primary", "unknown"])
        
    with sc3:
        default_input = 1 if st.checkbox("¿Registra Deuda (Default)?") else 0
        housing_input = 1 if st.checkbox("¿Tiene Crédito Hipotecario?") else 0
        loan_input = 1 if st.checkbox("¿Tiene Préstamo Consumo?") else 0
        poutcome_input = st.selectbox("Resultado Campaña Anterior", ["unknown", "failure", "other", "success"])

   # Botón para activar el cálculo probabilístico real
    # Botón para activar el cálculo probabilístico real
    if st.button("Ejecutar Inferencia con Regresión Logística"):
        
        # 1. Crear el DataFrame con los nombres exactos que espera el modelo
        single_row = pd.DataFrame([{
            "age": age_input, "job": job_input, "marital": marital_input, "education": education_input,
            "default": default_input, "balance": balance_input, "housing": housing_input, "loan": loan_input,
            "contact": "unknown", "day": 15, "month": "may", "duration": duration_input,
            "campaign": 1, "pdays": -1, "previous": 0, "poutcome": poutcome_input
        }])

        # ==============================================================================
        # 🔥 PASO 1.5: CREACIÓN DINÁMICA DE AGE_GROUP (Evita el KeyError)
        # ==============================================================================
        # Creamos los mismos rangos/etiquetas que genera tu transform_data.py
        if age_input < 30:
            single_row["age_group"] = "young"
        elif age_input <= 50:
            single_row["age_group"] = "middle-aged"
        else:
            single_row["age_group"] = "elderly"

        # 2. Aplicar Label Encoding de manera segura usando las clases originales
        for col in single_row.select_dtypes(include=["object"]).columns:
            if col in encoders:
                le = encoders[col]
                single_row[col] = single_row[col].map(lambda s: s if s in le.classes_ else le.classes_[0])
                single_row[col] = le.transform(single_row[col])

        # 3. Reordenar y escalar pasando el DataFrame completo estructurado
        feature_order = scaler.feature_names_in_
        single_row = single_row[feature_order]
        
        single_row_scaled = single_row.copy()
        single_row_scaled[feature_order] = scaler.transform(single_row)

        # 4. Calcular probabilidad legítima del algoritmo
        probabilidad_ia = model.predict_proba(single_row_scaled)[0][1] * 100

        st.divider()
        st.metric(label="Probabilidad Matemática de Suscripción", value=f"{probabilidad_ia:.2f}%")
        
        if probabilidad_ia >= 60.0:
            st.success("🎯 ¡Cliente Recomendado! Alta propensión a contratar el depósito a plazo.")
        else:
            st.warning("⚠️ Prospecto de Bajo Interés. No se recomienda priorizar en las llamadas operacionales.")
else:
    st.info("El simulador en tiempo real se activará automáticamente cuando los artefactos (.pkl) se generen en la carpeta models/")