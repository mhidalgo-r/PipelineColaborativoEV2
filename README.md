# Bank Marketing — Pipeline de Ingeniería de Datos e Inteligencia Artificial

## Descripción General

Este proyecto implementa un **pipeline automatizado de extremo a extremo** (ETL + Machine Learning) sobre el dataset **Bank Marketing**, con el objetivo de predecir si un cliente contratará un depósito a plazo a partir de su información sociodemográfica y de contacto comercial.

El sistema integra conceptos de **Ingeniería de Datos, Machine Learning, DataOps, MLOps, calidad de datos y seguridad**, dentro de un flujo reproducible, monitoreado y desplegable mediante contenedores.

### Objetivos del proyecto

- Construir un pipeline ETL modular que ingiera, limpie, transforme, valide y cargue datos reales de clientes bancarios.
- Entrenar y evaluar modelos de clasificación supervisada capaces de predecir la contratación de un depósito a plazo.
- Auditar la calidad y seguridad de los datos y del código conforme a buenas prácticas y a la normativa chilena vigente (Ley N.º 19.628).
- Monitorear el rendimiento del pipeline para identificar cuellos de botella y oportunidades de optimización.
- Exponer los resultados mediante un dashboard interactivo desarrollado en Streamlit.

### Estructura del Proyecto

El proyecto sigue una **arquitectura modular**, donde cada etapa del pipeline es un componente independiente con una única responsabilidad. Esto facilita el mantenimiento, la escalabilidad, la reutilización de código y el monitoreo individual de cada proceso.

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

### Stack tecnológico

| Componente | Tecnología |
|---|---|
| Procesamiento de datos | Python, Pandas |
| Machine Learning | Scikit-learn (Regresión Logística, Árbol de Decisión, StandardScaler, LabelEncoder) |
| Persistencia | PostgreSQL |
| Visualización / Dashboard | Streamlit |
| Contenerización | Docker |
| Gestión de credenciales | Variables de entorno (`.env`) |
| Cumplimiento normativo | Ley N.º 19.628 (Protección de la Vida Privada, Chile) |

### Dataset

- **Fuente:** `data/source/02_bank.csv` (Bank Marketing Dataset)
- **Registros:** 11.162 clientes
- **Variable objetivo:** `deposit` (`yes` / `no`)
- **Columnas totales:** 17

---

## Cómo Ejecutar el Proyecto

### 1. Clonar el repositorio

```bash
git clone -b feature/pipeline-ev3 https://github.com/mhidalgo-r/PipelineColaborativoEV2
cd PipelineColaborativoEV2
```

### 2. Abrir el código

```bash
code .
```

### 3. Crear el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> El comando `venv\Scripts\activate` corresponde a Windows. En Linux/macOS usa `source venv/bin/activate`.

### 4. Crear el archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con la cadena de conexión a la base de datos:

```env
DATABASE_URL=postgresql://usuario:password@host/nombre_bd?sslmode=require&channel_binding=require
```

> ⚠️ **No subas nunca tu `.env` real a GitHub.** Reemplaza `usuario`, `password`, `host` y `nombre_bd` por tus propias credenciales (por ejemplo, las que entrega Neon al crear tu base de datos). El archivo `.env` ya está incluido en `.gitignore` precisamente para evitar que credenciales reales queden expuestas en el repositorio; si una cadena de conexión con contraseña llega a subirse a un repo público, se recomienda rotarla (generar una nueva) de inmediato en el proveedor.

### 5. Correr todo de una vez

```bash
python main.py
```

### 6. Todos los comandos, uno por uno

```bash
# 1. ETL (EV2)
python -m scripts.ingest.ingestion_data
python -m scripts.cleaning.cleaning_data
python -m scripts.transform.transform_data
python -m scripts.validation.validation_data
python -m scripts.load.loading_data

# 2. EDA
python -m scripts.eda.quality_analysis
python -m scripts.eda.visual_eda

# 3. MODELO IA
python -m scripts.modeling.train_model
python -m scripts.modeling.evaluate_model

# 4. SEGURIDAD
python -m scripts.security.security_audit

# 5. RENDIMIENTO
python -m scripts.performance.performance_monitor

# 6. DASHBOARD
streamlit run dashboard/app.py
```

### 7. Correr todo con Docker

```bash
# Correr todo
python main.py

# Levantar los contenedores
docker compose up --build

# Detener y eliminar los contenedores
docker compose down
```

---

## Pipeline ETL

Durante la ejecución se procesan **11.162 registros** provenientes del dataset Bank Marketing, los cuales atraviesan **cinco etapas principales** antes de ser utilizados para el entrenamiento del modelo de Machine Learning.

### ETAPA 1 – Ingesta

**Objetivo**

Extraer el dataset fuente, validar su estructura y generar una copia del conjunto de datos en formato RAW para preservar la información original.

**Actividades realizadas**
- Verificación de existencia del archivo fuente.
- Lectura del archivo CSV mediante Pandas.
- Validación de columnas obligatorias.
- Registro de información estadística inicial.
- Exportación del dataset RAW.

**Resultados obtenidos**

| Indicador | Valor |
|---|---|
| Registros leídos | 11.162 |
| Clientes con depósito | 5.289 |
| Clientes sin depósito | 5.873 |
| Conversión inicial | 47,38 % |
| Balance promedio | 1.528,54 |
| Edad promedio | 41,23 años |

**Archivo generado:** `data/raw/02_bank.csv`
**Tiempo de ejecución:** 0,21 segundos

### ETAPA 2 – Limpieza

**Objetivo**

Garantizar la calidad de los datos antes de comenzar el proceso de transformación.

**Procesos ejecutados**

- **Normalización**: se estandarizaron los nombres de todas las columnas (ej. `Age → age`, `Balance → balance`).
- **Limpieza de texto**: todas las variables categóricas fueron convertidas a minúsculas para evitar inconsistencias (ej. `YES → yes`, `No → no`).
- **Eliminación de duplicados**: no se detectaron registros duplicados (0).
- **Valores nulos**: el dataset no presentó valores faltantes (0).
- **Conversión de tipos**: se convirtieron correctamente las variables numéricas `age`, `balance`, `day`, `duration`, `campaign`, `pdays`, `previous`.

**Resultado**

| Indicador | Valor |
|---|---|
| Filas iniciales | 11.162 |
| Filas finales | 11.162 |
| Retención | 100 % |

**Archivo generado:** `data/processed/bank_cleaned.csv`
**Tiempo de ejecución:** 0,24 segundos

### ETAPA 3 – Transformación

**Objetivo**

Preparar el dataset para el entrenamiento del modelo mediante la generación de nuevas variables y la transformación de atributos relevantes.

> **Nota de arquitectura:** en versiones anteriores del proyecto esta etapa implementaba un motor de *scoring* basado en reglas manuales hardcodeadas (if/else) para estimar la probabilidad de suscripción. Esa lógica fue **eliminada por completo**. La probabilidad de suscripción utilizada por el negocio ya no se calcula en el ETL, sino que se obtiene posteriormente mediante `.predict_proba()` del modelo de Machine Learning real (Regresión Logística), evitando así el *data leakage* que afectaba las métricas del proyecto en su versión anterior.

**Conversión de variables binarias**

Variables convertidas a formato numérico: `default`, `housing`, `loan`, `deposit`.

**Segmentación etaria**

Se creó la variable `age_group`, que agrupa a los clientes en rangos (`Joven`, `Adulto`, `Adulto Mayor`) para facilitar el análisis y mejorar la capacidad predictiva del modelo.

**Variables derivadas de negocio**

Durante esta etapa también se generan atributos utilizados exclusivamente para fines de análisis y segmentación comercial (no para el entrenamiento del modelo, con el fin de evitar data leakage):

- `risk_level`
- `approval_status`
- `premium_client`
- `scoring_reason`

Estas variables se excluyen explícitamente del conjunto de entrenamiento del modelo (ver sección *Machine Learning*).

**Resultado**

- Clientes procesados: 11.162
- Archivo generado: `data/processed/bank_transformed.csv`
- Tiempo de ejecución: 0,88 segundos

### ETAPA 4 – Validación

**Objetivo**

Verificar que los registros transformados cumplan las reglas de negocio antes de su carga en la base de datos, clasificando a los clientes en distintos conjuntos de salida.

**Resultados obtenidos**

| Categoría | Registros |
|---|---|
| Clientes aprobados | 6.776 |
| Clientes rechazados | 4.386 |
| Clientes premium | 3.859 |

| Métrica | Valor |
|---|---|
| Tasa aprobación | 60,71 % |
| Tasa rechazo | 39,29 % |
| Clientes premium | 56,95 % |
| Probabilidad promedio | 80,08 % |

**Archivos generados**
- `data/validated/bank_validated.csv`
- `data/validated/bank_premium.csv`
- `data/reject/bank_rejected.csv`

**Tiempo de ejecución:** 0,39 segundos

### ETAPA 5 – Load

**Objetivo**

Persistir los resultados finales del pipeline en PostgreSQL para su posterior explotación mediante consultas analíticas y visualización en el dashboard.

**Información cargada**

| Tabla | Registros |
|---|---|
| clientes_aprobados | 6.776 |
| clientes_premium | 3.859 |
| clientes_rechazados | 4.386 |

La conexión con PostgreSQL se realiza utilizando variables de entorno definidas en el archivo `.env`, evitando exponer credenciales dentro del código fuente.

**Rendimiento**

Tiempo total de carga: **18,20 segundos**

Esta etapa representa aproximadamente el **93 %** del tiempo total del pipeline, por lo que constituye el **principal cuello de botella** del sistema debido a las operaciones de escritura sobre la base de datos.

---

## Machine Learning

Una vez finalizado el proceso ETL, el pipeline inicia automáticamente la fase de Machine Learning.

El objetivo consiste en construir un modelo capaz de predecir si un cliente contratará un depósito a plazo utilizando únicamente la información disponible antes del resultado de la campaña.

**Variable objetivo:** `deposit` (`yes` / `no`)

**Variables predictoras**

`age`, `job`, `marital`, `education`, `default`, `balance`, `housing`, `loan`, `contact`, `day`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`, `age_group`

**Prevención de data leakage**

Para evitar fugas de información, se excluyen del entrenamiento las variables generadas por las reglas de negocio del ETL: `subscription_probability`, `risk_level`, `approval_status`, `premium_client`, `scoring_reason`.

### Preprocesamiento

- **Label Encoding** para variables categóricas.
- **StandardScaler** sobre variables numéricas (necesario para la correcta convergencia de la Regresión Logística).
- **División Train/Test** (70 % / 30 %).

| Conjunto | Registros |
|---|---|
| Entrenamiento | 7.813 |
| Prueba | 3.349 |

### Modelos entrenados

Se evaluaron dos algoritmos de clasificación supervisada:

- **Regresión Logística**: modelo lineal utilizado como clasificador principal debido a su buen equilibrio entre precisión, interpretabilidad y capacidad de generalización. Fue elegida como *baseline* bancario estándar, y al combinarse con `StandardScaler` resolvió los problemas de convergencia observados anteriormente.
- **Árbol de Decisión**: utilizado como modelo de comparación para evaluar diferencias frente a un algoritmo basado en particiones.

### Resultados del entrenamiento

| Indicador | Valor |
|---|---|
| Registros | 11.162 |
| Variables predictoras | 17 |
| Train | 7.813 |
| Test | 3.349 |
| Accuracy Train | 79,85 % |
| Accuracy Test | 79,64 % |

La diferencia entre ambos conjuntos es mínima, por lo que **no se observaron indicios de sobreajuste (overfitting)**.

### Comparación de modelos

| Métrica | Regresión Logística | Árbol de Decisión |
|---|---|---|
| Accuracy | 0,80 | 0,78 |
| Precision | 0,80 | 0,74 |
| Recall | 0,76 | 0,69 |
| F1 Score | 0,78 | 0,71 |
| ROC AUC | 0,87 | 0,74 |
| Gini | 0,75 | 0,48 |

La **Regresión Logística** obtuvo el mejor desempeño en todas las métricas evaluadas, siendo seleccionada como **modelo final del proyecto**.

### Variables más importantes (modelo seleccionado)

| Variable | Importancia |
|---|---|
| duration | 45,0 % |
| balance | 22,5 % |
| poutcome | 14,2 % |
| age | 10,1 % |
| housing | 8,2 % |

Estos resultados indican que la **duración del contacto comercial** y el **balance disponible del cliente** son los factores con mayor capacidad predictiva para estimar la contratación de un depósito bancario.

### Artefactos generados

El pipeline entrena, sirializa y exporta físicamente los siguientes archivos:

- `models/bank_model.pkl`
- `models/encoder.pkl`
- `models/scaler.pkl`
- `data/outputs/model_predictions.csv`
- `data/outputs/model_metrics.json` (se recalcula y sobrescribe automáticamente en cada ejecución)

---

## Calidad de Datos (Data Quality)

Una vez finalizado el proceso ETL, el pipeline ejecuta automáticamente una auditoría de calidad de datos con el objetivo de verificar que la información utilizada para el entrenamiento del modelo sea consistente, íntegra y apta para análisis posteriores.

**Controles implementados**

- Conteo total de registros.
- Conteo de columnas.
- Detección de valores nulos.
- Detección de registros duplicados.
- Identificación de columnas sensibles.
- Validación de tipos de datos.
- Generación automática del reporte de calidad.

**Resultados obtenidos**

| Indicador | Resultado |
|---|---|
| Registros analizados | 11.162 |
| Columnas | 17 |
| Valores nulos | 0 |
| Registros duplicados | 0 |

Los resultados evidencian que el dataset presenta una alta calidad, sin pérdida de información durante las etapas del pipeline.

**Columnas sensibles (Ley N.º 19.628, Chile)**

El sistema identifica automáticamente atributos considerados sensibles según la **Ley N.º 19.628 sobre Protección de la Vida Privada**: `age`, `job`, `marital`, `education`, `balance`, `default`.

Estas variables son reportadas para facilitar la aplicación de mecanismos de anonimización o enmascaramiento cuando el proyecto sea desplegado en ambientes productivos.

**Advertencias detectadas**

Durante el análisis se registraron advertencias del tipo *"Columna [X] no numérica — Cannot perform reduction 'mean' with string dtype"*. Estas advertencias corresponden al intento de calcular estadísticas numéricas sobre variables categóricas y **no representan errores del pipeline**; la ejecución continúa normalmente y el reporte se genera correctamente.

**Reporte generado:** `data/outputs/data_quality_report.csv`

---

## Análisis Exploratorio de Datos (EDA)

Después de la auditoría de calidad, el pipeline genera automáticamente un conjunto de visualizaciones destinadas a comprender la distribución de los datos y las relaciones entre variables.

**Visualizaciones generadas**

- **Distribución de edades** — histograma de edad.
- **Distribución del balance** — histograma de balance.
- **Distribución de duración** — histograma de duración de las llamadas de la campaña.
- **Distribución de la variable objetivo** — gráfico de barras (contratación vs. no contratación).
- **Relaciones bivariadas** — Balance vs. Deposit, Edad vs. Deposit.
- **Matriz de correlación** — correlación entre todas las variables numéricas.

Todos los gráficos son almacenados automáticamente para ser utilizados posteriormente en el dashboard de Streamlit.

---

## Evaluación del Modelo

Finalizado el entrenamiento, se ejecuta una evaluación automática utilizando el conjunto de prueba.

| Métrica | Resultado |
|---|---|
| Accuracy | 80 % |
| Precision | 80 % |
| Recall | 76 % |
| F1 Score | 78 % |
| ROC AUC | 0,87 |
| Coeficiente Gini | 0,75 |

**Interpretación**

- **Accuracy (80 %)**: el modelo clasifica correctamente aproximadamente ocho de cada diez clientes.
- **Precision (80 %)**: cuando el modelo predice que un cliente contratará un depósito, acierta en aproximadamente el 80 % de los casos.
- **Recall (76 %)**: el modelo identifica correctamente el 76 % de los clientes que efectivamente contratarán un depósito.
- **F1 Score (78 %)**: existe un equilibrio adecuado entre precisión y sensibilidad, indicando un desempeño consistente.
- **ROC AUC (0,87)**: el modelo presenta una excelente capacidad para distinguir entre clientes que contratarán un depósito y aquellos que no.
- **Gini (0,75)**: confirma un alto poder discriminatorio del modelo, respaldando su utilidad para procesos de segmentación comercial.

---

## Auditoría de Seguridad

El proyecto incorpora una auditoría automática orientada a verificar el cumplimiento de buenas prácticas de desarrollo seguro.

**Verificaciones realizadas**

- **Variables de entorno**: se comprobó correctamente la existencia del archivo `.env`; las credenciales permanecen fuera del código fuente.
- **Protección mediante `.gitignore`**: se verificó que `.env` se encuentra incluido en `.gitignore`, evitando su publicación accidental en el repositorio.
- **Búsqueda de secretos**: el sistema inspecciona el código fuente en busca de contraseñas, tokens, API keys y credenciales embebidas. **Resultado:** no se detectaron secretos hardcodeados.
- **Revisión del Dockerfile**: se confirmó que la aplicación se ejecuta con un usuario distinto de root. Se detectó, sin embargo, el uso de `COPY . .`, instrucción que puede copiar archivos innecesarios o sensibles al contenedor si no se complementa con un `.dockerignore` correctamente configurado.
- **Protección de datos personales (Ley N.º 19.628)**: el sistema identifica automáticamente variables que podrían contener información sensible, recomendando anonimizar atributos personales, aplicar enmascaramiento, evitar almacenar información innecesaria y solicitar consentimiento en ambientes productivos.

**Archivos sensibles detectados**

- `.env`
- `models/bank_model.pkl`
- `models/encoder.pkl`

La detección tiene carácter informativo y permite controlar que estos archivos reciban el tratamiento adecuado según el entorno de despliegue.

---

## Monitoreo de Rendimiento

Además del proceso ETL y del entrenamiento del modelo, el proyecto incorpora un módulo de monitoreo cuyo objetivo es medir el comportamiento del pipeline durante su ejecución, identificando cuellos de botella, consumo de recursos, estabilidad y tiempos de respuesta.

**Información del entorno**

| Recurso | Valor |
|---|---|
| CPU total | 3,2 % |
| RAM instalada | 15,71 GB |
| RAM utilizada | 9,91 GB |
| Uso de memoria | 63,1 % |

**Rendimiento por etapa**

| Etapa | Estado | Tiempo | CPU | Δ RAM |
|---|---|---|---|---|
| Ingestion | OK | 0,15 s | 30,8 % | 0,02 GB |
| Cleaning | OK | 0,15 s | 100 % | 0,02 GB |
| Transformation | OK | 0,15 s | 4,8 % | 0,55 GB |
| Validation | OK | 0,15 s | 23,1 % | 0,02 GB |
| Loading | OK | 18,20 s | 16,3 % | 0,02 GB |
| EDA Quality | OK | 0,15 s | 14,5 % | 0,02 GB |
| EDA Visual | OK | 0,15 s | 18,0 % | 0,02 GB |
| Training | OK | 0,15 s | 18,0 % | 0,02 GB |
| Evaluation | OK | 0,15 s | 5,7 % | 0,02 GB |
| Security Audit | OK | 0,15 s | 4,1 % | 0,02 GB |

### Análisis de cuellos de botella

**Tiempo de ejecución**

| Indicador | Resultado |
|---|---|
| Cuello de botella | Loading |
| Tiempo | 18,20 s |
| Etapa más rápida | Ingestion |
| Tiempo mínimo | 0,15 s |
| Promedio por etapa | 1,955 s |

La carga de datos representa la mayor parte del tiempo total del pipeline debido a las operaciones de escritura sobre la base de datos.

**Consumo de CPU**

| Etapa | CPU |
|---|---|
| Cleaning | 100 % |

Comportamiento esperable debido a las operaciones de validación, normalización y conversión de tipos realizadas sobre todo el conjunto de datos.

**Consumo de memoria**

| Etapa | Incremento |
|---|---|
| Transformation | 0,55 GB |

Aumento asociado a la generación de variables derivadas y estructuras temporales utilizadas durante el procesamiento.

### Análisis de estabilidad

Con el propósito de evaluar la consistencia del pipeline, se ejecutó la etapa **EDA Quality** en tres oportunidades consecutivas.

| Ejecución | Tiempo |
|---|---|
| Run 1 | 0,45 s |
| Run 2 | 0,42 s |
| Run 3 | 0,48 s |

| Indicador | Valor |
|---|---|
| Promedio | 0,45 s |
| Variación | 0,06 s |
| Sistema estable | Sí |

La baja variabilidad observada evidencia un comportamiento consistente y reproducible del proceso.

### Latencia de Base de Datos

| Medición | Tiempo |
|---|---|
| Ping 1 | 1,9428 s |
| Ping 2 | 0,3514 s |
| Ping 3 | 0,3080 s |
| **Promedio** | **0,8674 s** |

Se observa que la primera conexión presenta una latencia mayor debido al establecimiento inicial de la sesión con la base de datos, mientras que las conexiones posteriores muestran tiempos considerablemente inferiores.

### Resumen General del Rendimiento

| Indicador | Valor |
|---|---|
| Tiempo total del pipeline | 19,55 s |
| Etapas ejecutadas | 10 |
| Estado general | Correcto |
| Errores críticos | 0 |
| Cuello de botella | Loading |

**Reporte generado:** `data/outputs/performance_report.json`

---

## Dashboard Streamlit

El proyecto incorpora una aplicación desarrollada con **Streamlit**, que permite visualizar de forma interactiva los resultados del pipeline y del modelo de Machine Learning.

**Funcionalidades disponibles**

- Visualización de métricas del modelo.
- Comparación entre algoritmos entrenados.
- Distribución de variables.
- Resultados del análisis exploratorio (EDA).
- Importancia de variables.
- Estado general del pipeline.
- Indicadores de rendimiento.
- Consulta de registros procesados.
- Inferencia en vivo utilizando el modelo entrenado (simulador de predicción).

La aplicación utiliza los archivos generados automáticamente durante la ejecución del pipeline (`model_metrics.json`, `performance_report.json`, `data_quality_report.csv`, artefactos `.pkl`), permitiendo mantener la información sincronizada sin intervención manual.

---

## Resultados del Proyecto

### Pipeline ETL

- 11.162 registros procesados correctamente.
- 100 % de retención de registros tras la limpieza.
- 0 valores nulos detectados.
- 0 registros duplicados.
- Datos cargados exitosamente en PostgreSQL.

### Machine Learning

**Modelo seleccionado:** Regresión Logística (Scikit-learn)

| Métrica | Resultado |
|---|---|
| Accuracy | 80 % |
| Precision | 80 % |
| Recall | 76 % |
| F1 Score | 78 % |
| ROC AUC | 0,87 |
| Gini | 0,75 |

Estas métricas reflejan un modelo con buena capacidad predictiva y un adecuado equilibrio entre precisión y sensibilidad para el problema de clasificación abordado.

**Variables más relevantes:** `duration`, `balance`, `poutcome`, `age`, `housing`.

---

## Conclusiones

El proyecto demuestra la integración exitosa de técnicas de **Ingeniería de Datos, Machine Learning, DataOps y MLOps** dentro de un flujo automatizado de procesamiento de datos.

Entre los principales logros alcanzados destacan:

- Automatización completa del pipeline ETL.
- Procesamiento íntegro de los datos sin pérdidas de información.
- Reemplazo del motor de *scoring* manual por un clasificador de Machine Learning real y auditable, eliminando el riesgo de *data leakage*.
- Entrenamiento y evaluación automática de modelos de clasificación.
- Selección de la Regresión Logística como modelo con mejor desempeño (AUC 0,87 / Gini 0,75).
- Incorporación de auditorías de calidad y seguridad, alineadas con la Ley N.º 19.628.
- Monitoreo detallado del rendimiento del sistema, con identificación clara de cuellos de botella.
- Persistencia de resultados en PostgreSQL.
- Disponibilidad de un dashboard interactivo para el análisis de resultados.

El pipeline presenta una arquitectura modular, mantenible y escalable, facilitando futuras extensiones y su adaptación a nuevos conjuntos de datos o modelos predictivos.

## Futuras Mejoras

- Implementar optimización automática de hiperparámetros mediante `GridSearchCV` o `RandomizedSearchCV`.
- Incorporar modelos adicionales como Random Forest, XGBoost o LightGBM para comparar su desempeño.
- Automatizar el despliegue mediante herramientas de integración continua (CI/CD).
- Integrar un sistema de monitoreo continuo para detectar *data drift* y *model drift*.
- Implementar versionado de modelos utilizando herramientas especializadas como MLflow.
- Optimizar la etapa Loading, principal cuello de botella identificado, mediante técnicas de inserción masiva o procesamiento por lotes.
- Incorporar pruebas automatizadas para cada etapa del pipeline y ampliar la cobertura de validaciones.
- Añadir un `.dockerignore` para complementar el `Dockerfile` y evitar copiar archivos sensibles o innecesarios al contenedor.

## Autores
- Eduardo Silva 
- Mauricio Hidalgo

Proyecto desarrollado como parte de la asignatura de Ingeniería de Datos e Inteligencia Artificial, integrando conocimientos de procesamiento de datos, aprendizaje automático, visualización, seguridad y buenas prácticas de desarrollo de software.
