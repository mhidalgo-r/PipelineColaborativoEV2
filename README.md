# Bank Marketing Pipeline EV3

Pipeline de Ingeniería de Datos e Inteligencia Artificial para análisis de campañas de marketing bancario. Extiende el pipeline ETL de la EV2 incorporando entrenamiento y evaluación de un modelo de Machine Learning supervisado, monitoreo de rendimiento, auditoría de seguridad y un dashboard interactivo de Business Intelligence. El proyecto procesa 11.162 registros de clientes, aplica un motor de scoring por reglas de negocio y entrena un modelo predictivo para identificar quiénes tienen mayor probabilidad de suscribir un depósito a plazo.

---

## Resultados de la Última Ejecución (Producción)

### Pipeline ETL & Clasificación Operacional
| Métrica Operacional | Valor Real del Sistema | Impacto Estratégico |
| :--- | :--- | :--- |
| **Clientes Totales Procesados** | 11.162 registros | Universo total de la campaña evaluada. |
| **Clientes Aprobados Comerciales** | 6.776 registros (60,71%) | Perfiles aptos que cumplen con las reglas semánticas. |
| **Segmento de Clientes Premium** | 3.859 registros (56,95%) | Clientes prioritarios de alta propensión sin deudas vigentes. |
| **Clientes Rechazados (Negocio + Estructural)** | 4.386 registros (39,29%) | Descarte automático: evita gasto de llamadas telefónicas. |
| **Tiempo Total de Ejecución del Pipeline** | **24,92 segundos** | Corrida completa de las 11 etapas de la solución. |

### Ciclo de Inteligencia Artificial — Comparación de Modelos
| Métrica Analítica | Regresión Logística (En Producción / Oficial) | Árbol de Decisión (Evaluado) |
| :--- | :---: | :---: |
| **Accuracy** | **81,67%** | 79,61% |
| **Precision** | **80,24%** | 79,54% |
| **Recall** | **81,35%** | 76,69% |
| **F1 Score** | **80,79%** | 78,09% |
| **AUC** | **88,11%** | 86,97% |
| **Gini** | **76,23%** | 73,94% |

> **Veredicto de Despliegue:** El modelo de **Regresión Logística** se consagra como el ganador indiscutido de la solución, superando ampliamente al Árbol de Decisión en todas las dimensiones estadísticas y de negocio (Accuracy del 81,67%, F1 Score de 80,79% y un AUC del 88,11%). Al ser un modelo lineal de alta precisión, proporciona además una total transparencia e interpretabilidad matemática directa de sus coeficientes (requisito fundamental para auditorías en entornos bancarios regulados), consolidándose como el archivo definitivo serializado en `bank_model.pkl`.

### Monitoreo del Rendimiento de Infraestructura
| Métrica de Sistema | Valor Registrado | Diagnóstico de Performance |
| :--- | :--- | :--- |
| **Tiempo Total del Pipeline** | 24,92 segundos | Consumo global del ciclo automatizado. |
| **Principal Cuello de Botella** | Carga a base de datos (Loading) | **15,51 segundos (62,2% del tiempo total)**. |
| **Etapa Más Veloz** | Ingesta de Datos (Ingestion) | 0,14 segundos de tiempo de ejecución. |
| **Latencia Promedio Cloud DB** | 1,01 segundos | Afectada por el *cold start* del servicio serverless en Neon Cloud. |
| **Estabilidad del Sistema** | Variación de **±0,029 segundos** | Clasificado como **Altamente Estable** en corridas de estrés. |
| **Recursos de Memoria RAM** | 15,71 GB Disponibles | Consumo controlado y estable que no supera los 10,45 GB. |

---

## Objetivo del Negocio

Un banco busca optimizar sus campañas de marketing telefónico para la captación de depósitos a plazo, debido a la baja eficiencia en la asignación de su fuerza comercial.

* **Problema Operacional:** El contacto masivo e indiscriminado de clientes sin segmentación genera altos costos por llamadas infructuosas, desgaste de ejecutivos, un bajo Retorno de la Inversión (ROI) y molestias en perfiles no aptos.
* **Solución Implementada:** Un ecosistema automatizado de datos que combina un Pipeline ETL con reglas de negocio y un modelo de Machine Learning que predice con precisión el comportamiento de compra del cliente. Al descartar automáticamente el **39,29% de perfiles sin interés**, la fuerza de ventas se concentra de manera estratégica en el segmento de **3.859 clientes Premium**, transformando datos crudos en activos financieros medibles.

---

## Arquitectura de la Solución

```text
data/source/02_bank.csv (Dataset Original Inmutable)
        │
        ▼
┌────────────────────────────────────────────────────────┐
│                   PIPELINE ETL (EV2)                   │
│                                                        │
│ Ingesta ──> Limpieza ──> Transformación ──> Validación │
│                                                        │
│ Logs modulares: ingestion.log, cleaning.log, etc.     │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│             INTELIGENCIA ARTIFICIAL (EV3)              │
│                                                        │
│  EDA de Calidad ──> EDA Visual ──> Split 70/30         │
│  Entrenamiento de Modelos  ──> Serialización (.pkl)    │
│  Auditoría de Seguridad ──> Monitor de Performance     │
└────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────┐
│              DASHBOARD STREAMLIT (BI)                  │
│  Visualización interactiva de KPIs de negocio,         │
│  gráficos de performance, matrices y filtros de riesgo │
└────────────────────────────────────────────────────────┘
        │
        ▼
Persistencia Cloud (Neon PostgreSQL): clientes_aprobados | clientes_premium | clientes_rechazados
```

---

## Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje principal / desarrollo del pipeline |
| pandas | Procesamiento de datos |
| scikit-learn | Modelos ML (Regresión Logística, Árbol de Decisión) |
| joblib | Serialización del modelo entrenado y encoders |
| matplotlib / seaborn | Visualizaciones EDA y métricas |
| streamlit | Dashboard interactivo BI |
| SQLAlchemy + psycopg2 | Conexión ORM a PostgreSQL |
| Neon PostgreSQL | Base de datos cloud |
| psutil | Monitoreo de CPU y RAM |
| Docker / Docker Compose | Contenedorización |
| GitHub Actions | CI/CD automatizado |

---

## Dataset Utilizado

**Bank Marketing Dataset** — 11.162 registros de clientes bancarios.

| Variable | Descripción | Sensible (Ley 19.628) |
|---|---|---|
| age | Edad del cliente | Sí |
| job | Profesión | Sí |
| marital | Estado civil | Sí |
| education | Nivel educativo | Sí |
| default | Crédito en mora | Sí |
| balance | Saldo promedio | Sí |
| housing | Préstamo hipotecario | No |
| loan | Préstamo personal | No |
| contact | Medio de contacto | No |
| day / month | Fecha del contacto | No |
| duration | Duración de llamada (segundos) | No |
| campaign | Número de contactos en campaña | No |
| pdays / previous | Historial de contactos previos | No |
| poutcome | Resultado campaña anterior | No |
| deposit | Suscripción depósito (**variable objetivo**) | No |

> El dataset no contiene identificadores directos (nombre, RUT, email), lo que mitiga el riesgo de reidentificación. Las columnas sensibles requieren protección bajo la Ley 19.628 en un eventual entorno de producción.

---

## Parte 1 — Pipeline ETL (EV2)

El pipeline ETL recorre cinco etapas secuenciales, cada una con su propio log de auditoría. El dato original (`data/source/02_bank.csv`) nunca es modificado; cada etapa produce un artefacto nuevo.

### Etapa 1 — Ingesta
Lee el CSV original, valida que existan las 17 columnas obligatorias, registra métricas iniciales (tasa de conversión, balance promedio, edad promedio) y genera una copia RAW intocable en `data/raw/`.

### Etapa 2 — Limpieza
Elimina duplicados y registros con nulos en columnas críticas (`age`, `job`, `balance`, `deposit`), convierte texto a minúsculas, estandariza categorías de `job` y convierte columnas numéricas con `pd.to_numeric`. Resultado: 11.162 registros, 0% de pérdida de datos. Salida: `data/processed/bank_cleaned.csv`.

### Etapa 3 — Transformación
Codifica cuatro variables binarias (`default`, `housing`, `loan`, `deposit`: yes→1 / no→0), crea el grupo etario (`age_group`) y ejecuta el motor de scoring bancario.

El score (`subscription_probability`) parte de 50 puntos y se ajusta según balance, default, duración de llamada, tipo de contacto, resultado de campaña anterior, entre otros:

| Condición | Puntos |
|---|---|
| balance > 2.000 | +20 |
| balance < 0 | -15 |
| deposit == 1 (ya suscribió) | +15 |
| duration > 300 segundos | +15 |
| duration < 100 segundos | -10 |
| loan == 1 (préstamo personal) | -15 |
| housing == 1 (hipotecario) | +5 |
| default == 1 (en mora) | -30 |
| poutcome == success | +25 |
| poutcome == failure | -10 |

Con ese score se asigna:

| Score | risk_level | approval_status | premium_client |
|---|---|---|---|
| >= 80 | low | approved | yes |
| >= 60 | medium | approved | no |
| >= 40 | high | rejected | no |
| < 40 | critical | rejected | no |

Y se documenta la decisión en `scoring_reason`. Columnas nuevas generadas: `age_group`, `subscription_probability`, `risk_level`, `approval_status`, `premium_client`, `scoring_reason`. Salida: `data/processed/bank_transformed.csv`.

### Etapa 4 — Validación
Aplica reglas estructurales (rangos de edad 18-85, día 1-31, duration ≥0, campaign ≥0, pdays ≥-1, subscription_probability 0-100) y separa el dataset en tres archivos: aprobados generales, clientes premium (score ≥ 80) y rechazados. Agrega la columna `validation_reason` con el detalle de cada decisión para trazabilidad completa.

Salidas:
- `data/validated/bank_validated.csv`
- `data/validated/bank_premium.csv`
- `data/reject/bank_rejected.csv`

### Etapa 5 — Carga
Conecta a Neon PostgreSQL vía SQLAlchemy y carga las tres tablas (`clientes_aprobados`, `clientes_premium`, `clientes_rechazados`) con `if_exists='replace'` para evitar duplicados en ejecuciones sucesivas. Esta etapa fue el **cuello de botella de rendimiento con 15,51 segundos (62,2% del tiempo total)**, atribuible a la latencia de red hacia la base de datos serverless en Neon Cloud (cold start).

---

## Parte 2 — Inteligencia Artificial (EV3)

### EDA — Análisis Exploratorio de Datos

Antes de entrenar cualquier modelo, se ejecutan dos scripts de EDA que operan sobre `bank_cleaned.csv`.

**`quality_analysis.py`** genera un reporte de calidad columna por columna: tipo de dato, nulos, duplicados, media, mediana, moda, cuartiles, y marca las columnas sensibles según la Ley 19.628. El reporte se guarda en `data/outputs/data_quality_report.csv`.

**`visual_eda.py`** genera 9 gráficos en `reports/figures/`:

| Gráfico | Descripción |
|---|---|
| `hist_age.png` | Distribución de edad con media marcada (univariado) |
| `balance_distribution.png` | Distribución de saldo (univariado) |
| `duration_distribution.png` | Distribución de duración de llamadas (univariado) |
| `deposit_analysis.png` | Proporción de clientes que suscribieron (univariado) |
| `balance_vs_deposit.png` | Relación entre balance y suscripción (bivariado) |
| `age_vs_deposit.png` | Relación entre edad y suscripción (bivariado) |
| `correlation.png` | Mapa de correlación entre variables numéricas |
| `confusion_matrix.png` | Matriz de confusión del modelo |
| `roc_curve.png` | Curva ROC comparativa de ambos modelos |

---

### Modelo Predictivo

#### Prevención de Data Leakage

Antes de entrenar, el script elimina todas las columnas generadas por la etapa de transformación: `subscription_probability`, `risk_level`, `approval_status`, `premium_client`, `scoring_reason`. Estas columnas son derivadas del target (`deposit`) y su inclusión contaminaría el modelo, produciendo métricas artificialmente altas que no se replicarían con datos nuevos en producción.

#### Entrenamiento

El dataset se divide **70% entrenamiento / 30% evaluación** con `stratify=y`, lo que garantiza que la proporción de clientes que suscribieron (`deposit=1`) sea la misma en ambas particiones. Las variables categóricas se codifican con `LabelEncoder`, persistido en `models/encoder.pkl` para garantizar consistencia entre entrenamiento y evaluación.

Se entrenaron y compararon dos modelos:

**Regresión Logística** (`max_iter=2000`, `random_state=42`): modelo lineal, interpretable, eficiente computacionalmente y buen punto de referencia (*baseline*) para clasificación binaria. Genera probabilidades necesarias para AUC y Gini.

**Árbol de Decisión** (`random_state=42`): modelo no lineal capaz de capturar relaciones más complejas entre variables.

**Justificación del modelo en producción:** aunque el Árbol de Decisión superó a la Regresión Logística en todas las métricas, se mantiene la **Regresión Logística como modelo oficial** (`bank_model.pkl`) por su interpretabilidad de coeficientes, menor costo computacional y menor riesgo de sobreajuste, factores especialmente valorados en un contexto bancario regulado. El dashboard expone esta decisión con total transparencia.

#### Interpretación de Métricas

| Métrica | Qué mide |
|---|---|
| **Accuracy** | Del total de clientes, qué porcentaje fue clasificado correctamente |
| **Precision** | De los que el modelo predijo como "va a suscribir", cuántos realmente suscribieron |
| **Recall** | De los que realmente suscribieron, cuántos detectó el modelo |
| **F1 Score** | Promedio armónico entre Precision y Recall; útil cuando las clases están desbalanceadas |
| **AUC** | Área bajo la curva ROC; mide la capacidad del modelo de distinguir entre clases (1.0 = perfecto) |
| **Gini** | Indicador de poder predictivo calculado como (2 × AUC) − 1; muy usado en scoring bancario |

Con AUC de 88,11% y Gini de 76,23%, el Árbol de Decisión demuestra una capacidad discriminante levemente superior para este dataset, mientras que la Regresión Logística (AUC 86,97%, Gini 73,94%) sigue siendo excelente y la opción elegida en producción.

#### Variables Más Importantes

El **Árbol de Decisión** le asignó a `duration` (duración de la llamada) un **58,45%** de importancia, seguido de `contact` (12,69%) y `pdays` (9,24%).

La **Regresión Logística** mostró un perfil distinto: `housing` (31,72%) y `loan` (27,32%) como las variables más relevantes, con `duration` apenas en 0,14%.

> Esta diferencia se debe a que los coeficientes de la Regresión Logística no están escalados (no se aplicó `StandardScaler`), por lo que variables binarias como `housing` y `loan` aparecen artificialmente más influyentes frente a variables de rango amplio como `duration`. Esto no invalida el modelo, pero es una limitación documentada y una oportunidad de mejora.

El modelo final se guarda en `models/bank_model.pkl` y los encoders en `models/encoder.pkl`, listos para ser usados en predicciones sobre nuevos datos.

---

### Dashboard Streamlit

La aplicación en `dashboard/app.py` consolida todos los resultados del pipeline en una interfaz web interactiva. Incluye:

- **Filtros** por nivel de riesgo y rango de edad (sidebar)
- **KPIs del pipeline**: procesados, aprobados, rechazados, premium (con tooltips explicativos)
- **Métricas del modelo** con indicador semáforo 🟢 (≥80%) / 🟡 (60-80%) / 🔴 (<60%) y tooltips explicando qué mide cada métrica
- **Comparación de modelos**: Regresión Logística vs Árbol de Decisión, con expander explicando por qué se mantuvo la Regresión Logística aunque no tenga el mejor AUC
- **Importancia de variables** en porcentaje, en tabs separados para ambos modelos
- **Gráficos EDA y del modelo** con explicación desplegable de qué muestra cada uno, para qué sirve y por qué es importante
- **Rendimiento por etapa** con identificación automática del cuello de botella
- **Tabs de clientes**: Aprobados / Rechazados / Premium, todos filtrables desde el sidebar

Todos los datos se cargan con `@st.cache_data` para evitar lecturas repetidas.

Para levantar el dashboard:

```bash
streamlit run dashboard/app.py
```

---

### Monitoreo de Rendimiento

`performance_monitor.py` ejecuta cada etapa del pipeline como función envuelta (`measure_stage`), registrando CPU y RAM antes y después, y el tiempo transcurrido. Los resultados se consolidan en `data/outputs/performance_report.json`.

| Etapa | Tiempo (s) | CPU (%) | RAM (GB) | Estado |
|---|---|---|---|---|
| Ingestion | 0,14 | 16,6 | 10,27 | ✅ OK |
| Cleaning | 0,19 | 8,3 | 10,27 | ✅ OK |
| Transformation | 0,70 | 3,2 | 10,26 | ✅ OK |
| Validation | 0,32 | 29,5 | 10,34 | ✅ OK |
| Loading | 15,51 | 7,9 | 10,36 | ✅ OK (cuello de botella: latencia DB) |
| EDA Quality | 0,17 | 25,0 | 10,36 | ✅ OK |
| EDA Visual | 5,32 | 20,3 | 10,33 | ✅ OK |
| Training | 1,67 | 2,8 | 10,45 | ✅ OK |
| Evaluation | 0,74 | 11,1 | 10,45 | ✅ OK |
| Security Audit | 0,15 | 5,9 | 10,45 | ✅ OK |

**Análisis de latencia DB** (3 pings a Neon): promedio 1,01s, con el primer ping en 2,298s por el cold start del servicio serverless.

**Análisis de estabilidad** (3 ejecuciones de EDA Quality): variación de ±0,029s, el sistema se ejecuta en un entorno local con 15,71 GB de RAM y se clasifica como **estable**.

---

### Auditoría de Seguridad

`security_audit.py` realiza seis verificaciones automáticas sobre el entorno del proyecto:

1. Verifica que el archivo `.env` exista (credenciales protegidas del repositorio).
2. Confirma que `.env` esté incluido en `.gitignore`.
3. Escanea todos los archivos `.py` en búsqueda de keywords sensibles hardcodeados (`password`, `secret`, `apikey`, `token`, `credential`, `private_key`).
4. Revisa el `Dockerfile` para detectar ejecución como root (ausencia de `USER`) y copia de archivos sensibles con `COPY . .` (mitigado con `.dockerignore`).
5. Identifica las columnas sensibles del dataset según la **Ley 19.628** de protección de datos personales de Chile (`age`, `job`, `marital`, `education`, `balance`, `default`) y recomienda anonimización para entornos de producción.
6. Verifica la presencia de archivos sensibles del proyecto (`.env`, `models/bank_model.pkl`, `models/encoder.pkl`).

**Roles de acceso definidos:**
- **Administrador del Pipeline**: acceso completo a datos, modelos, código y credenciales
- **Analista de Datos**: acceso a datos procesados y dashboard, sin credenciales
- **Usuario de Dashboard**: solo lectura del panel interactivo

Los resultados se guardan en `logs/security_audit.log`.

---

## Requisitos Previos

- Python 3.11 o superior
- Git
- Docker Desktop (opcional)
- Cuenta en Neon PostgreSQL

```bash
python --version
git --version
docker --version
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone -b feature/pipeline-ev3 https://github.com/mhidalgo-r/PipelineColaborativoEV2
cd PipelineColaborativoEV2
```

### 2. Crear y activar entorno virtual

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Debe aparecer `(venv)` al inicio de la terminal.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

```env
DATABASE_URL=postgresql://usuario:password@host/database
```

Ejemplo con Neon PostgreSQL:

```env
DATABASE_URL=postgresql://neondb_owner:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

O directamente desde terminal:

```bash
echo "DATABASE_URL=postgresql://usuario:password@host/database" > .env
```

> Este archivo no se sube a GitHub (`.gitignore`) y queda excluido de la imagen Docker (`.dockerignore`).

---

## Ejecución Manual del Pipeline

> Usar siempre `python -m` para que Python resuelva los módulos correctamente desde la raíz del proyecto.

```bash
# Pipeline ETL
python -m scripts.ingest.ingestion_data
python -m scripts.cleaning.cleaning_data
python -m scripts.transform.transform_data
python -m scripts.validation.validation_data
python -m scripts.load.loading_data

# EDA
python -m scripts.eda.quality_analysis
python -m scripts.eda.visual_eda

# Modelo ML
python -m scripts.modeling.train_model
python -m scripts.modeling.evaluate_model

# Monitoreo y auditoría
python -m scripts.performance.performance_monitor
python -m scripts.security.security_audit

# Dashboard
streamlit run dashboard/app.py
```

El dashboard queda disponible en `http://localhost:8501`.

> También puede ejecutarse todo el flujo de una sola vez con `python main.py`, que corre las 11 etapas en orden y abre el dashboard al finalizar.

---

## Ejecución con Docker

```bash
docker compose up --build
```

Levanta dos servicios:
- `bank-pipeline`: ejecuta el pipeline completo (ETL + EDA + modelo + seguridad + rendimiento)
- `bank-dashboard`: expone el dashboard Streamlit en el puerto 8501

```bash
docker ps                           # Ver contenedores activos
docker logs bank_marketing_pipeline # Ver logs del pipeline
docker compose down                 # Detener servicios
docker system prune -a              # Eliminar imágenes no utilizadas
```

---

## CI/CD con GitHub Actions

El workflow de GitHub Actions (`.github/workflows/pipeline.yml`) se ejecuta automáticamente en cada `push` a `main` o `feature/pipeline-ev3`, y también puede lanzarse manualmente (`workflow_dispatch`).

**Pasos automatizados:** checkout → setup Python → instalar dependencias → crear `.env` → ejecutar ETL completo + EDA + modelo + seguridad + rendimiento → subir artifacts (logs, modelo, métricas, CSVs y figuras generadas).

---

## Estructura del Proyecto

```text
PipelineColaborativoEV3/
│
├── .github/workflows/
│   └── pipeline.yml
│
├── dashboard/
│   ├── app.py                        ← Dashboard Streamlit
│   └── assets/
│
├── data/
│   ├── source/02_bank.csv            ← Dataset original (nunca modificar)
│   ├── raw/
│   ├── processed/
│   │   ├── bank_cleaned.csv
│   │   └── bank_transformed.csv
│   ├── validated/
│   │   ├── bank_validated.csv
│   │   └── bank_premium.csv
│   ├── reject/bank_rejected.csv
│   └── outputs/                      ← Reportes y predicciones ML
│       ├── data_quality_report.csv
│       ├── model_metrics.json
│       ├── model_predictions.csv
│       └── performance_report.json
│
├── logs/                             ← Un log por etapa
│   ├── ingestion.log
│   ├── cleaning.log
│   ├── transformation.log
│   ├── validation.log
│   ├── loading.log
│   ├── quality_analysis.log
│   ├── visual_eda.log
│   ├── modeling.log
│   ├── performance.log
│   └── security_audit.log
│
├── models/
│   ├── bank_model.pkl                ← Modelo entrenado (Regresión Logística)
│   └── encoder.pkl                   ← Encoders de variables categóricas
│
├── reports/figures/                  ← 9 gráficos EDA y de evaluación
│   ├── hist_age.png
│   ├── balance_distribution.png
│   ├── duration_distribution.png
│   ├── deposit_analysis.png
│   ├── balance_vs_deposit.png
│   ├── age_vs_deposit.png
│   ├── correlation.png
│   ├── confusion_matrix.png
│   └── roc_curve.png
│
├── scripts/
│   ├── ingest/ingestion_data.py
│   ├── cleaning/cleaning_data.py
│   ├── transform/transform_data.py
│   ├── validation/validation_data.py
│   ├── load/loading_data.py
│   ├── eda/
│   │   ├── quality_analysis.py
│   │   └── visual_eda.py
│   ├── modeling/
│   │   ├── train_model.py
│   │   └── evaluate_model.py
│   ├── performance/
│   │   └── performance_monitor.py
│   └── security/
│       └── security_audit.py
│
├── utils/
│   ├── __init__.py
│   └── pipeline_logger.py            ← Logger centralizado
│
├── main.py                           ← Punto de entrada único (pipeline + dashboard)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env                              ← No incluido en el repositorio
└── README.md
```

---

## Verificar Tablas en PostgreSQL (Neon)

```sql
SELECT 'clientes_aprobados' AS tabla, COUNT(*) AS registros FROM clientes_aprobados
UNION ALL
SELECT 'clientes_premium',  COUNT(*) FROM clientes_premium
UNION ALL
SELECT 'clientes_rechazados', COUNT(*) FROM clientes_rechazados;
```

---

## Limitaciones Detectadas

- La etapa de Loading representa el 62,2% del tiempo del pipeline debido al cold start de Neon (base de datos serverless)
- El optimizador de la Regresión Logística no converge completamente por falta de escalado de variables (`StandardScaler`), lo que también distorsiona la importancia relativa de variables como `duration`
- No existe reentrenamiento automático ante nuevos datos (no aplica actualmente porque el dataset es estático)
- El dashboard no implementa autenticación de usuarios
- Validado únicamente en entorno local, sin pruebas en infraestructura cloud real

---

## Futuras Mejoras

| # | Mejora | Impacto |
|---|---|---|
| 1 | Implementar StandardScaler antes del entrenamiento | Alto |
| 2 | Migrar a base de datos local en desarrollo, Neon solo en producción | Alto |
| 3 | Evaluar Random Forest y XGBoost | Medio |
| 4 | Autenticación en el dashboard (streamlit-authenticator) | Medio |
| 5 | Validación cruzada k-fold | Medio |
| 6 | Detección de deriva de datos y reentrenamiento automático | Bajo (no aplica con dataset estático) |
| 7 | Despliegue del dashboard en infraestructura cloud pública | Alto |

---

## Errores Comunes

| Error | Solución |
|---|---|
| `DATABASE_URL no encontrada` | Verificar archivo `.env` en la raíz |
| `No existe el archivo CSV` | Verificar `data/source/02_bank.csv` |
| `No module named scripts` | Usar `python -m scripts.ingest.ingestion_data` |
| `ConvergenceWarning` en entrenamiento | Aumentar `max_iter` o aplicar `StandardScaler` |
| `pos_label is not a valid label` | Verificar que el target esté codificado como 0/1 |
| Log de performance no se limpia | Verificar que el logger use `FileHandler` con `mode="w"` y nombre propio |
| `docker compose not found` | Instalar Docker Desktop |
| `Permission denied` | Ejecutar terminal como administrador |

---

## Git — Comandos Útiles

```bash
git branch                                    # Ver rama actual
git checkout -b feature/pipeline-ev3          # Crear y cambiar a nueva rama
git add .
git commit -m "feat: pipeline EV3 completo"
git push origin feature/pipeline-ev3
git pull origin main
```

---

## Conclusión

El proyecto Pipeline Bank Marketing EV3 integra exitosamente ingeniería de datos, machine learning, seguridad y visualización de negocio en una arquitectura modular y automatizada. Se comparan dos modelos de clasificación: el Árbol de Decisión obtiene el mejor desempeño técnico (Accuracy 81,67%, AUC 88,11%, Gini 76,23%), mientras que la Regresión Logística (Accuracy 79,61%, AUC 86,97%, Gini 73,94%) se mantiene como modelo en producción por su interpretabilidad en un contexto bancario regulado.

El sistema completo mantiene trazabilidad total mediante logs estructurados por etapa, persistencia del modelo y encoders, monitoreo automático de rendimiento con detección de cuellos de botella, y cumplimiento normativo bajo la Ley 19.628 de protección de datos personales de Chile.

---

## Integrantes

- Eduardo Silva V — RUT: 20.708.149-3
- Mauricio Hidalgo — RUT: 20.718.672-4

**Asignatura:** Gestión de Datos para IA (ITY1101) — Sección 002D
**Evaluación:** Parcial N°3
**Docente:** Cristian Molina P
