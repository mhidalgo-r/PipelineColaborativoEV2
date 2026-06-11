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
    if selected_risk != "Todos":
        validated_filtered = validated[
            validated["risk_level"] == selected_risk
        ]
    else:
        validated_filtered = validated
else:
    validated_filtered = validated

if not validated.empty and "age" in validated.columns:
    min_age = int(validated["age"].min())
    max_age = int(validated["age"].max())
    age_range = st.sidebar.slider(
        "Rango de Edad",
        min_age, max_age,
        (min_age, max_age)
    )
    validated_filtered = validated_filtered[
        (validated_filtered["age"] >= age_range[0]) &
        (validated_filtered["age"] <= age_range[1])
    ]

# ==========================
# KPIs PIPELINE
# ==========================
st.subheader("KPIs del Pipeline")
total = len(validated) + len(rejected)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Procesados", total)
c2.metric("Aprobados",        len(validated))
c3.metric("Rechazados",       len(rejected))
c4.metric("Premium",          len(premium))

st.divider()

# ==========================
# METRICAS MODELO IA
# ==========================
st.subheader("Métricas del Modelo IA")

if metrics:
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Accuracy",  metrics.get("accuracy",  "N/A"))
    m2.metric("Recall",    metrics.get("recall",    "N/A"))
    m3.metric("Precision", metrics.get("precision", "N/A"))
    m4.metric("F1 Score",  metrics.get("f1",        "N/A"))
    m5.metric("AUC",       metrics.get("auc",       "N/A"))
    m6.metric("Gini",      metrics.get("gini",      "N/A"))
else:
    st.warning("Métricas no disponibles. Ejecuta evaluate_model.py primero.")

st.divider()

# ==========================
# GRAFICOS EDA Y MODELO
# ==========================
st.subheader("Gráficos EDA y Modelo")

figures = {
    "Matriz de Confusion":    "reports/figures/confusion_matrix.png",
    "Curva ROC":              "reports/figures/roc_curve.png",
    "Correlacion Variables":  "reports/figures/correlation.png",
    "Distribucion Edad":      "reports/figures/hist_age.png",
    "Balance vs Deposito":    "reports/figures/balance_vs_deposit.png",
    "Edad vs Deposito":       "reports/figures/age_vs_deposit.png",
}

cols = st.columns(2)
for i, (title, path) in enumerate(figures.items()):
    with cols[i % 2]:
        if os.path.exists(path):
            st.image(path, caption=title, use_column_width=True)
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
else:
    st.warning(
        "Datos de rendimiento no disponibles. "
        "Ejecuta performance_monitor.py primero."
    )

st.divider()

# ==========================
# TABLA CLIENTES APROBADOS
# ==========================
st.subheader("Clientes Aprobados")

if not validated_filtered.empty:
    st.write(f"Mostrando {len(validated_filtered)} registros")
    st.dataframe(
        validated_filtered.head(50),
        use_container_width=True
    )
else:
    st.warning("No hay datos de clientes aprobados disponibles.")

st.divider()

# ==========================
# GRAFICO INTERACTIVO
# ==========================
st.subheader("Distribución Interactiva")

if not validated.empty and "age" in validated.columns:
    age_counts = validated_filtered["age"].value_counts().sort_index()
    st.bar_chart(age_counts)
    st.caption("Distribucion de edad en clientes aprobados (filtrable desde sidebar)")