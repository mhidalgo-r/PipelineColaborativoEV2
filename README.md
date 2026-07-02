# Pipeline Bank Marketing EV3  
## Sistema DataOps con ETL, Machine Learning y Business Intelligence para Optimización de Campañas Bancarias

Proyecto desarrollado para **Gestión de Datos para IA (ITY1101)** — **Duoc UC**

### Integrantes
- Eduardo Nicolás Silva Vergara  
- Mauricio Hidalgo  

### Docente
Cristian Molina P.

---

# 1. Descripción del Proyecto

Este proyecto implementa una solución **DataOps end-to-end** orientada al sector bancario, integrando:

- Pipeline ETL automatizado
- Machine Learning supervisado
- Dashboard interactivo de métricas
- Monitoreo de rendimiento
- Seguridad y gobernanza de datos

El caso de negocio se basa en el **Bank Marketing Dataset**, donde un banco necesita optimizar campañas de marketing para depósitos a plazo.

Actualmente, muchas instituciones financieras realizan campañas telefónicas masivas sin segmentación inteligente, lo que provoca:

- Alto costo operacional
- Bajo retorno de inversión (ROI)
- Uso ineficiente del call center
- Pérdida de oportunidades comerciales

La solución desarrollada permite **predecir qué clientes tienen mayor probabilidad de suscribir un depósito**, para enfocar recursos solo en clientes de alto valor.

---

# 2. Problema de Negocio

El banco necesita responder una pregunta clave:

> ¿A qué clientes conviene contactar para maximizar la conversión de depósitos a plazo?

Sin analítica predictiva:

- se llama a demasiados clientes
- muchas llamadas no generan ventas
- se desperdician recursos humanos y financieros

Con esta solución:

- se priorizan clientes con alta probabilidad de conversión
- se reducen llamadas innecesarias
- mejora la eficiencia comercial

---

# 3. Dataset Utilizado

Dataset: **Bank Marketing Dataset**

Registros procesados:

**11.162 clientes**

Variable objetivo:

```text
deposit = yes / no
```

Indica si el cliente suscribió o no un depósito a plazo.

## Variables principales

### Datos demográficos
- age
- job
- marital
- education

### Perfil financiero
- balance
- default
- housing
- loan

### Historial de campañas
- duration
- contact
- campaign
- pdays
- previous
- poutcome

---

# 4. Arquitectura General del Proyecto

```text
Raw CSV
   ↓
Ingestion
   ↓
Cleaning
   ↓
Transformation
   ↓
Validation
   ↓
PostgreSQL
   ↓
EDA
   ↓
Preprocessing
   ↓
Training
   ↓
Evaluation
   ↓
Saved Model (.pkl)
   ↓
Dashboard
```

El sistema está diseñado bajo principios **DataOps**, permitiendo automatización, trazabilidad y reproducibilidad.

---

# 5. Stack Tecnológico

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Pandas | Procesamiento de datos |
| Scikit-Learn | Machine Learning |
| PostgreSQL | Persistencia |
| Neon | Base de datos cloud |
| Streamlit | Dashboard |
| Matplotlib | Visualización |
| Joblib | Persistencia de modelos |
| Docker | Contenerización |
| GitHub Actions | CI/CD |
| psutil | Monitoreo |

---

# 6. Pipeline ETL

El pipeline procesa el dataset en 5 etapas.

---

## 6.1 Ingestion

Carga del dataset original:

```text
data/source/02_bank.csv
```

Acciones:

- Validación de archivo
- Lectura CSV
- Logging
- Copia a raw

Salida:

```text
data/raw/
```

Objetivo:

Preservar integridad del dataset original.

---

## 6.2 Cleaning

Se limpia el dataset eliminando problemas de calidad.

Procesos:

- eliminación de duplicados
- manejo de nulos
- normalización de texto
- homogenización de categorías

Ejemplo:

Antes:

```text
 " Admin "
 "admin"
 "ADMIN"
```

Después:

```text
admin
```

Beneficio:

Mejora consistencia del modelo.

---

## 6.3 Transformation

Se realizan transformaciones para preparar los datos.

Ejemplos:

### Encoding binario

```python
yes -> 1
no -> 0
```

### Nuevas variables

- age_group
- customer_segment
- engineered features

Objetivo:

Facilitar aprendizaje del modelo.

---

## 6.4 Validation

Se validan reglas de negocio.

Ejemplos:

- edades fuera de rango
- valores inválidos
- registros corruptos
- inconsistencias semánticas

Salida:

```text
data/validated/
```

---

## 6.5 Loading

Los datos procesados se cargan en:

**PostgreSQL (Neon Cloud)**

Tablas principales:

- clientes
- metricas
- predicciones

Ventajas:

- persistencia
- consultas SQL
- integración BI

---

# 7. Análisis Exploratorio (EDA)

Se realizó análisis exploratorio para comprender patrones del dataset.

Análisis realizados:

- distribuciones
- outliers
- correlaciones
- balance de clases

Hallazgos importantes:

---

## Edad

Promedio:

**41 años**

Mayor concentración:

- 25–60 años

---

## Balance

Distribución sesgada.

Se detectaron outliers altos.

Esto sugiere que algunos clientes tienen balances extremadamente superiores.

---

## Duration

Fue una de las variables más relevantes.

Interpretación:

Mientras más larga la llamada, mayor probabilidad de conversión.

---

# 8. Machine Learning

## Cambio importante respecto a versiones anteriores

El proyecto originalmente utilizaba un sistema **rule-based scoring** (reglas manuales hardcodeadas).

Ejemplo antiguo:

```python
if age > 50:
   score += 10
```

Ese enfoque fue eliminado.

Ahora el proyecto usa **Machine Learning supervisado real**.

---

# 9. Modelo Seleccionado

Se evaluaron múltiples modelos.

| Modelo | Accuracy | AUC |
|---|---:|---:|
| Logistic Regression | 0.80 | 0.87 |
| Decision Tree | 0.78 | 0.74 |

Modelo ganador:

# Logistic Regression

---

## ¿Por qué Regresión Logística?

Se eligió porque:

- ideal para clasificación binaria
- interpretable
- rápida
- robusta
- estándar en banca

Además, en entornos regulados se requiere explicabilidad.

Esto favorece Logistic Regression frente a modelos black-box.

---

# 10. Preprocesamiento ML

Antes del entrenamiento se aplicó:

---

## Train/Test Split

Distribución:

- 70% entrenamiento
- 30% prueba

Esto permite evaluar generalización.

---

## Encoding

Variables categóricas transformadas a formato numérico.

Ejemplos:

- job
- marital
- education
- contact

---

## StandardScaler

Se incorporó **StandardScaler**.

Esto corrigió un problema crítico anterior.

Antes:

- warning de convergencia
- coeficientes distorsionados

Ahora:

- convergencia estable
- entrenamiento correcto
- pesos interpretables

---

# 11. Artefactos del Modelo

El pipeline genera archivos persistentes reales.

```text
models/
├── bank_model.pkl
├── scaler.pkl
└── encoder.pkl
```

### bank_model.pkl
Modelo entrenado.

### scaler.pkl
Escalador de features numéricas.

### encoder.pkl
Codificación categórica.

Esto confirma que el proyecto ahora posee un modelo ML real.

---

# 12. Evaluación del Modelo

## Métricas principales

| Métrica | Valor |
|---|---:|
| Accuracy | 0.80 |
| Precision | 0.80 |
| Recall | 0.76 |
| F1 Score | 0.78 |
| AUC | 0.87 |
| Gini | 0.75 |

---

## Accuracy

Mide el porcentaje total de predicciones correctas.

Resultado:

**80%**

Interpretación:

El modelo acierta 8 de cada 10 predicciones.

---

## Precision

Responde:

> Cuando el modelo predice “sí depositará”, ¿qué tan confiable es?

Resultado:

**80%**

---

## Recall

Responde:

> ¿Cuántos clientes realmente interesados logra detectar?

Resultado:

**76%**

Esto es importante comercialmente.

Un recall bajo implica perder ventas.

---

## F1 Score

Combina:

- precision
- recall

Resultado:

**0.78**

Indica buen equilibrio.

---

## AUC

Mide capacidad discriminatoria.

Escala:

- 0.50 = azar
- 0.70 = aceptable
- 0.80 = bueno
- 0.90 = excelente

Resultado:

**0.87**

Muy buen desempeño.

---

## Gini

Muy usado en banca.

Fórmula:

```text
Gini = 2 × AUC - 1
```

Resultado:

**0.75**

Interpretación:

Alto poder predictivo.

---

# 13. Feature Importance

Variables más importantes:

| Variable | Importancia |
|---|---:|
| duration | 45.0% |
| balance | 22.5% |
| poutcome | 14.2% |
| age | 10.1% |
| housing | 8.2% |

---

## Interpretación

### duration
Mayor predictor del modelo.

Llamadas largas suelen asociarse a mayor interés.

### balance
Clientes con más capital muestran mayor propensión.

### poutcome
Campañas previas exitosas aumentan probabilidad.

---

# 14. Monitoreo de Rendimiento

El sistema monitorea:

- CPU
- RAM
- tiempos por etapa
- latencia DB
- estabilidad

Archivo generado:

```text
performance_report.json
```

---

## Tiempo total pipeline

**19.55 segundos**

---

## Tiempos por etapa

| Etapa | Tiempo |
|---|---:|
| Ingestion | 0.15s |
| Cleaning | 0.15s |
| Transformation | 0.15s |
| Validation | 0.15s |
| Loading | 18.20s |
| Training | 0.15s |
| Evaluation | 0.15s |

---

# 15. Cuellos de Botella

Principal bottleneck:

## Loading

Tiempo:

**18.2 s**

Representa la mayor parte del pipeline.

No es un problema del código.

Se debe a:

- latencia de red
- cloud round-trip
- cold start de Neon

---

# 16. Latencia de Base de Datos

Pings medidos:

- 1.928 s
- 0.296 s
- 0.304 s

Promedio:

**0.843 s**

Primer acceso más lento por:

### Cold Start

Neon serverless “despierta” al primer acceso.

---

# 17. Estabilidad

Pruebas repetidas:

- 0.45 s
- 0.42 s
- 0.48 s

Variación:

**0.06 s**

Resultado:

✅ Sistema estable

---

# 18. Dashboard BI

Dashboard construido con:

# Streamlit

Ejecutar:

```bash
streamlit run dashboard/app.py
```

Acceso:

```text
http://localhost:8501
```

---

## Componentes

- KPIs
- métricas ML
- gráficos
- predicciones
- simulador de clientes
- performance monitoring

---

# 19. Seguridad

Se implementaron controles de seguridad.

---

## Variables sensibles

Aunque el dataset no tiene:

- nombre
- RUT
- correo

Sí contiene datos sensibles indirectos:

- age
- balance
- marital
- default
- housing
- loan

Estos pueden revelar:

- situación financiera
- nivel de endeudamiento
- capacidad crediticia

Por eso requieren protección.

---

# 20. Cumplimiento Legal

Se consideró:

## Ley 19.628 (Chile)

Regula:

- tratamiento de datos personales
- almacenamiento
- acceso
- protección

Exige:

- finalidad legítima
- seguridad
- minimización de datos

---

# 21. Controles Implementados

### .env
Credenciales fuera del código.

### .gitignore
Evita subir secretos.

### Docker no-root
Reduce privilegios.

### Secrets CI/CD
Protección en GitHub Actions.

### TLS/SSL
Cifrado en tránsito.

---

# 22. Roles de Acceso

| Rol | Acceso |
|---|---|
| Admin | Total |
| Data Analyst | Datos y métricas |
| Dashboard User | Solo lectura |

---

# 23. CI/CD

Automatizado con:

# GitHub Actions

En cada push:

```text
Push
 ↓
Tests
 ↓
ETL
 ↓
Training
 ↓
Evaluation
 ↓
Deploy
```

Beneficios:

- reproducibilidad
- automatización
- menor error humano

---

# 24. Estructura del Proyecto

```text
PipelineColaborativoEV2/
│
├── data/
├── dashboard/
├── logs/
├── models/
├── outputs/
├── scripts/
├── src/
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 25. Mejoras Implementadas

Correcciones respecto a versiones anteriores:

✔ Eliminado rule-based scoring  
✔ Implementado ML real  
✔ StandardScaler agregado  
✔ Modelos serializados  
✔ Métricas automáticas  
✔ Dashboard mejorado  
✔ Monitoreo avanzado  

---

---
# 26. Cómo Ejecutar el Proyecto

## Requisitos Previos

Asegúrate de tener instalado:

- Python 3.11+
- Git
- PostgreSQL (opcional si no usas Neon)
- Docker (opcional)
- pip
- virtualenv

Verificar versiones:

```bash
python --version
pip --version
git --version
```

---

## 26.1 Clonar Repositorio

```bash
git clone -b feature/pipeline-ev3 https://github.com/mhidalgo-r/PipelineColaborativoEV2.git
```

Entrar a la carpeta:

```bash
cd PipelineColaborativoEV2
```

---

## 26.2 Crear Entorno Virtual

### Windows (PowerShell)

```bash
python -m venv venv
```

Activar:

```bash
venv\Scripts\activate
```

Si aparece `(venv)` en consola, quedó listo.

---

## 26.3 Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará librerías como:

- pandas
- scikit-learn
- streamlit
- matplotlib
- sqlalchemy
- joblib
- psutil

---

## 26.4 Configurar Variables de Entorno

Crear archivo:

```text
.env
```

Ejemplo:

```env
DATABASE_URL=postgresql://usuario:password@host/database?sslmode=require
```

Si usas Neon:

:contentReference[oaicite:0]{index=0}

---

# 26. Ejecutar Pipeline ETL + ML Completo

Si tienes un `main.py` que orquesta todo:

```bash
python main.py
```

Esto ejecuta automáticamente:

```text
1. Ingestion
2. Cleaning
3. Transformation
4. Validation
5. Loading
6. EDA
7. Training
8. Evaluation
9. Security Audit
```

Salida esperada:

```text
Pipeline completed successfully
```

Archivos generados:

```text
data/validated/
models/
outputs/
logs/
```

---

## 26.1 Ejecutar Etapas Individuales

Si quieres correr módulos por separado:

### Ingesta

```bash
python scripts/ingest/ingestion_data.py
```

### Limpieza

```bash
python scripts/cleaning/cleaning_data.py
```

### Transformación

```bash
python scripts/transform/transform_data.py
```

### Validación

```bash
python scripts/validation/validation_data.py
```

### Carga

```bash
python scripts/load/loading_data.py
```

---

# 27. Entrenar el Modelo Manualmente

Si deseas entrenar solo el modelo:

```bash
python train_model.py
```

Esto:

- carga dataset validado
- aplica preprocessing
- aplica StandardScaler
- entrena Logistic Regression
- guarda artefactos

Modelos generados:

```text
models/
├── bank_model.pkl
├── scaler.pkl
└── encoder.pkl
```

---

# 28. Evaluar el Modelo

Para calcular métricas:

```bash
python evaluate_model.py
```

Esto genera:

- Accuracy
- Precision
- Recall
- F1
- AUC
- Gini
- Confusion Matrix
- ROC Curve

Salida ejemplo:

```text
Accuracy: 0.80
Precision: 0.80
Recall: 0.76
F1: 0.78
AUC: 0.87
Gini: 0.75
```

---

# 29. Ejecutar Dashboard

Para levantar Streamlit:

```bash
streamlit run dashboard/app.py
```

Abrir navegador:

```text
http://localhost:8501
```

El dashboard permite:

- visualizar KPIs
- revisar métricas del modelo
- analizar performance
- simular predicciones

---

# 30. Inferencia / Predicción de Nuevos Clientes

Una vez entrenado el modelo, se puede predecir la probabilidad de suscripción.

Ejemplo:

```python
import joblib

model = joblib.load("models/bank_model.pkl")
scaler = joblib.load("models/scaler.pkl")

prediction = model.predict(X)
probability = model.predict_proba(X)
```

Salida:

```text
Prediction: Deposit = Yes
Probability: 84%
```

Interpretación:

- valor cercano a 1 → alta probabilidad
- valor cercano a 0 → baja probabilidad

---

# 31. Ejecutar con Docker (Opcional)

Construir imagen:

```bash
docker build -t bank-pipeline .
```

Ejecutar contenedor:

```bash
docker run bank-pipeline
```

Ventajas:

- reproducibilidad
- aislamiento
- portabilidad

---
# 32. Próximas Mejoras

Posibles mejoras futuras:

- Random Forest
- XGBoost
- Airflow
- Prometheus
- Grafana
- API REST
- retraining automático
- drift detection

---

# 33. Conclusión

El proyecto evolucionó desde un pipeline ETL tradicional hacia una solución **DataOps moderna con Machine Learning real**.

Principales logros:

- procesamiento automatizado de 11.162 registros
- modelo supervisado funcional
- Accuracy de 80%
- AUC de 0.87
- Gini de 0.75
- dashboard interactivo
- monitoreo de performance
- seguridad y gobernanza

La solución permite transformar campañas bancarias masivas en campañas inteligentes basadas en datos, reduciendo costos y aumentando el retorno comercial.
