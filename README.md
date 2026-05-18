# Bank Marketing ETL Pipeline

## Descripción del Proyecto

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) completo orientado al análisis de campañas de marketing bancario para depósitos a plazo.

El objetivo principal es procesar, limpiar, transformar, validar y cargar información de clientes bancarios con el fin de identificar prospectos con mayor probabilidad de suscribir un depósito a plazo.

El pipeline fue desarrollado siguiendo buenas prácticas de Ingeniería de Datos, automatización CI/CD y validación de calidad de datos.

---

# Objetivo del Negocio

Un banco busca optimizar sus campañas de marketing debido a la baja eficiencia en la asignación de recursos comerciales.

Actualmente:

* Se contacta a demasiados clientes sin segmentación.
* Existen altos costos operacionales.
* El retorno de inversión (ROI) de las campañas es bajo.
* Se realizan contactos a clientes con baja probabilidad de aceptación.

El desafío consiste en:

* Detectar clientes con mayor probabilidad de suscribir depósitos a plazo.
* Reducir costos de campañas.
* Mejorar la eficiencia comercial.
* Preparar datos de calidad para futuros modelos de Machine Learning.

---

# Arquitectura del Pipeline

El pipeline se divide en 5 etapas principales:

1. Ingesta
2. Limpieza
3. Transformación
4. Validación
5. Carga

---

# Flujo del Pipeline

```text
Dataset Original
       ↓
INGESTA
       ↓
RAW DATA
       ↓
LIMPIEZA
       ↓
DATOS LIMPIOS
       ↓
TRANSFORMACIÓN
       ↓
DATOS ENRIQUECIDOS
       ↓
VALIDACIÓN
       ↓
APROBADOS / RECHAZADOS
       ↓
LOAD A POSTGRESQL
```

---

# Dataset Utilizado

Dataset: Bank Marketing Dataset

Variables utilizadas:

| Variable  | Descripción                  |
| --------- | ---------------------------- |
| age       | Edad del cliente             |
| job       | Profesión                    |
| marital   | Estado civil                 |
| education | Nivel educativo              |
| default   | Crédito en mora              |
| balance   | Saldo promedio               |
| housing   | Préstamo hipotecario         |
| loan      | Préstamo personal            |
| contact   | Medio de contacto            |
| day       | Día del último contacto      |
| month     | Mes del contacto             |
| duration  | Duración de llamada          |
| campaign  | Número de contactos          |
| pdays     | Días desde contacto anterior |
| previous  | Contactos previos            |
| poutcome  | Resultado campaña anterior   |
| deposit   | Suscripción depósito         |

---

# Tecnologías Utilizadas

| Tecnología      | Uso                    |
| --------------- | ---------------------- |
| Python          | Desarrollo pipeline    |
| Pandas          | Procesamiento de datos |
| PostgreSQL      | Base de datos          |
| Neon PostgreSQL | Base de datos cloud    |
| SQLAlchemy      | Conexión ORM           |
| GitHub Actions  | Automatización CI/CD   |
| Docker          | Contenedorización      |
| Logging         | Auditoría y monitoreo  |

---

# Estructura del Proyecto

```text
PipelineColaborativoEV2/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml
│
├── data/
│   │
│   ├── raw/
│   │   └── 02_bank.csv
│   ├── processed/
│   ├── validated/
│   └── reject/
│
├── logs/
│
├── scripts/
│   ├── ingest/
│   ├── cleaning/
│   ├── transform/
│   ├── validation/
│   └── load/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env
└── README.md
```

---

# Etapas del Pipeline

# 1. Ingesta

La etapa de ingesta tiene como objetivo cargar el dataset original y generar una copia controlada en formato RAW.

Funciones principales:

* Lectura del dataset CSV.
* Validación de existencia del archivo.
* Registro de logs.
* Generación de datos RAW.

Salida:

```text
/data/raw/02_bank.csv
```

---

# 2. Limpieza de Datos

La limpieza asegura calidad y consistencia de los datos.

Procesos realizados:

* Eliminación de duplicados.
* Eliminación de registros nulos.
* Corrección de formatos.
* Homogeneización de texto.
* Estandarización de categorías.
* Conversión de texto a minúsculas.
* Limpieza de espacios.

Además:

* Se preparan datos para validaciones posteriores.
* Se reducen inconsistencias estructurales.

Salida:

```text
/data/processed/bank_cleaned.csv
```

---

# 3. Transformación de Datos

La transformación adapta los datos para análisis avanzado y futuros modelos predictivos.

Transformaciones aplicadas:

## Variables binarias

Conversión:

| Original | Transformado |
| -------- | ------------ |
| yes      | 1            |
| no       | 0            |

Variables:

* default
* housing
* loan
* deposit

---

## Segmentación de edades

Se crean rangos etarios:

| Rango | Grupo  |
| ----- | ------ |
| 18-25 | joven  |
| 26-40 | adulto |
| 41-60 | maduro |
| 61-85 | senior |

---

## Sistema de Warnings

Se implementa un sistema de alertas de riesgo bancario.

Warnings considerados:

| Condición                    | Warning          |
| ---------------------------- | ---------------- |
| Edad alta                    | age_risk         |
| Trabajo desconocido          | job_warning      |
| Crédito en mora              | default_warning  |
| Tiene préstamo hipotecario   | housing_warning  |
| Tiene préstamo personal      | loan_warning     |
| Sin medio de contacto válido | contact_warning  |
| Demasiados contactos         | campaign_warning |
| Balance negativo             | balance_warning  |

---

## Scoring Bancario

Se calcula:

* warning_count
* risk_level
* approval_status
* rejection_reason

---

## Reglas de Negocio

### Rechazo automático

Se rechaza automáticamente si:

* Edad mayor a 85 años.
* Cliente posee default + housing + loan.
* Riesgo crítico.

---

## Niveles de Riesgo

| Riesgo   | Condición          |
| -------- | ------------------ |
| low      | pocos warnings     |
| medium   | warnings moderados |
| high     | muchos warnings    |
| critical | rechazo automático |

Salida:

```text
/data/processed/bank_transformed.csv
```

---

# 4. Validación

La validación garantiza integridad estructural y semántica.

---

## Validación Estructural

Se valida:

* Tipos de datos.
* Rangos válidos.
* Valores permitidos.
* Integridad numérica.

Ejemplos:

| Validación | Regla |
| ---------- | ----- |
| age        | 18-85 |
| day        | 1-31  |
| duration   | >= 0  |
| campaign   | >= 0  |
| previous   | >= 0  |
| pdays      | >= -1 |

---

## Validación Semántica

Se valida coherencia bancaria.

Ejemplos:

| Regla                         | Descripción       |
| ----------------------------- | ----------------- |
| default + múltiples préstamos | alto riesgo       |
| contacto desconocido          | warning           |
| balance negativo              | warning           |
| demasiados contactos          | warning comercial |

---

## Separación Final

Los datos se separan en:

### Clientes Aprobados

```text
/data/validated/bank_validated.csv
```

### Clientes Rechazados

```text
/data/reject/bank_rejected.csv
```

---

# 5. Carga a PostgreSQL

La etapa Load carga los datasets finales a Neon PostgreSQL.

Tablas generadas:

| Tabla               | Contenido            |
| ------------------- | -------------------- |
| clientes_aprobados  | clientes aptos       |
| clientes_rechazados | clientes descartados |

Características:

* Reemplazo automático de tablas.
* Prevención de duplicados.
* Logs de carga.
* Métricas de aprobación.

---

# Sistema de Logging

Cada etapa genera logs independientes:

| Archivo            | Descripción    |
| ------------------ | -------------- |
| ingestion.log      | ingesta        |
| cleaning.log       | limpieza       |
| transformation.log | transformación |
| validation.log     | validación     |
| loading.log        | carga          |

Los logs permiten:

* Auditoría.
* Trazabilidad.
* Monitoreo.
* Detección de errores.

---

# GitHub Actions

El proyecto incorpora CI/CD automático.

Pipeline automatizado:

1. Clonar repositorio.
2. Instalar Python.
3. Instalar dependencias.
4. Crear variables de entorno.
5. Ejecutar ETL completo.
6. Generar artefactos.

Archivo:

```text
.github/workflows/pipeline.yml
```

---

# Variables de Entorno

Archivo requerido:

```env
DATABASE_URL=postgresql://usuario:password@host/database
```

---

# Instalación del Proyecto

## 1. Clonar repositorio

```bash
git clone <URL_REPOSITORIO>
```

---

## 2. Crear entorno virtual

Windows:

```bash
python -m venv venv
```

---

## 3. Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Crear archivo .env (ya esta pero invisible)

```env
DATABASE_URL=tu_url_postgresql
```

---

# Ejecución Manual del Pipeline

## Ingesta

```bash
python scripts/ingest/ingestion_data.py
```

---

## Limpieza

```bash
python scripts/cleaning/cleaning_data.py
```

---

## Transformación

```bash
python scripts/transform/transform_data.py
```

---

## Validación

```bash
python scripts/validation/validation_data.py
```

---

## Carga

```bash
python scripts/load/loading_data.py
```

---

# Automatización con GitHub Actions

El pipeline se ejecuta automáticamente:

* En cada push a main.
* Manualmente mediante workflow_dispatch.

---

# Docker

El proyecto puede ejecutarse mediante Docker.

Ventajas:

* Portabilidad.
* Reproducibilidad.
* Consistencia de entorno.
* Fácil despliegue.

---

# Calidad de Datos

El pipeline incorpora:

* Validaciones estructurales.
* Validaciones semánticas.
* Reglas bancarias.
* Detección de riesgo.
* Sistema de scoring.
* Clasificación automática.

---

# Casos de Uso

Este pipeline puede utilizarse para:

* Campañas bancarias.
* Segmentación de clientes.
* Modelos predictivos.
* Data Warehousing.
* Análisis comercial.
* Scoring financiero.

---

# Futuras Mejoras

Posibles mejoras futuras:

* Machine Learning.
* API REST.
* Dashboard BI.
* Airflow.
* Kafka.
* Data Lake.
* Feature Store.
* Monitoreo automático.

---

# Conclusión

Este proyecto implementa una solución completa de Ingeniería de Datos orientada al sector bancario.

El pipeline:

* Automatiza el procesamiento de datos.
* Mejora la calidad de información.
* Reduce riesgos.
* Facilita futuras soluciones de Machine Learning.
* Optimiza campañas comerciales.
* Genera trazabilidad y auditoría.

Además, incorpora prácticas modernas de:

* ETL.
* CI/CD.
* Cloud Data Engineering.
* Validación de calidad.
* Automatización.
* Arquitectura profesional de datos.
