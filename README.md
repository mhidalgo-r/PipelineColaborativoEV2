# Bank Marketing ETL Pipeline

Pipeline ETL completo para análisis de campañas de marketing bancario. Procesa, limpia, transforma, valida y carga información de clientes para identificar prospectos con mayor probabilidad de suscribir un depósito a plazo, siguiendo buenas prácticas de Ingeniería de Datos, automatización CI/CD y validación de calidad de datos.

---

## Resultados de la última ejecución

| Métrica | Valor |
|---|---|
| Clientes procesados | 11.162 |
| Clientes aprobados | 6.776 |
| Clientes premium | 3.859 |
| Clientes rechazados | 4.386 |
| Tasa de aprobación | 60.71% |
| Tasa de rechazo | 39.29% |
| Tasa premium | 56.95% |
| Probabilidad promedio | 80.08% |

---

## Objetivo del Negocio

Un banco busca optimizar sus campañas de marketing debido a la baja eficiencia en la asignación de recursos comerciales.

**Problema actual:**
- Se contacta a demasiados clientes sin segmentación
- Existen altos costos operacionales
- El retorno de inversión (ROI) de las campañas es bajo
- Se realizan contactos a clientes con baja probabilidad de aceptación

**Solución implementada:**
- Detectar clientes con mayor probabilidad de suscribir depósitos a plazo
- Reducir costos de campañas mediante scoring automático
- Mejorar la eficiencia comercial con segmentación por riesgo
- Preparar datos de calidad para futuros modelos de Machine Learning

---

## Arquitectura del Pipeline

```text
Dataset Original (data/source/02_bank.csv)
       ↓
ETAPA 1 — INGESTA
       ↓
RAW DATA (data/raw/02_bank.csv)
       ↓
ETAPA 2 — LIMPIEZA
       ↓
DATOS LIMPIOS (data/processed/bank_cleaned.csv)
       ↓
ETAPA 3 — TRANSFORMACIÓN
       ↓
DATOS ENRIQUECIDOS + SCORING (data/processed/bank_transformed.csv)
       ↓
ETAPA 4 — VALIDACIÓN
       ↓
APROBADOS / PREMIUM / RECHAZADOS
       ↓
ETAPA 5 — LOAD A POSTGRESQL
       ↓
clientes_aprobados | clientes_premium | clientes_rechazados
```

---

## Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python | Desarrollo del pipeline |
| Pandas | Procesamiento de datos |
| PostgreSQL / Neon | Base de datos cloud |
| SQLAlchemy | Conexión ORM |
| GitHub Actions | Automatización CI/CD |
| Docker | Contenedorización |
| Logging | Auditoría por etapa |

---

## Dataset Utilizado

**Bank Marketing Dataset** — 11.162 registros de clientes bancarios.

| Variable | Descripción |
|---|---|
| age | Edad del cliente |
| job | Profesión |
| marital | Estado civil |
| education | Nivel educativo |
| default | Crédito en mora |
| balance | Saldo promedio |
| housing | Préstamo hipotecario |
| loan | Préstamo personal |
| contact | Medio de contacto |
| day | Día del último contacto |
| month | Mes del contacto |
| duration | Duración de llamada (segundos) |
| campaign | Número de contactos en campaña |
| pdays | Días desde contacto anterior |
| previous | Contactos previos |
| poutcome | Resultado campaña anterior |
| deposit | Suscripción depósito (target) |

---

## Estructura del Proyecto

```text
PipelineColaborativoEV2/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml
│
├── data/
│   ├── source/
│   │   └── 02_bank.csv        ← dataset original (nunca modificar)
│   ├── raw/
│   │   └── 02_bank.csv
│   ├── processed/
│   │   ├── bank_cleaned.csv
│   │   └── bank_transformed.csv
│   ├── validated/
│   │   ├── bank_validated.csv
│   │   └── bank_premium.csv
│   └── reject/
│       └── bank_rejected.csv
│
├── logs/
│   ├── ingestion.log
│   ├── cleaning.log
│   ├── transformation.log
│   ├── validation.log
│   ├── loading.log
│   └── reporte_pipeline.log
│
├── scripts/
│   ├── ingest/
│   │   └── ingestion_data.py
│   ├── cleaning/
│   │   └── cleaning_data.py
│   ├── transform/
│   │   └── transform_data.py
│   ├── validation/
│   │   └── validation_data.py
│   └── load/
│       └── loading_data.py
│
├── utils/
│   ├── __init__.py
│   └── pipeline_logger.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env
└── README.md
```

---

## Requisitos Previos

- Python 3.11 o superior
- Git
- Docker Desktop

Verificar instalaciones:

```bash
python --version
git --version
docker --version
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone -b feature/pipeline-reportes https://github.com/mhidalgo-r/PipelineColaborativoEV2
cd PipelineColaborativoEV2
```

### 2. Crear entorno virtual

Windows:
```bash
python -m venv venv
```

Mac/Linux:
```bash
python3 -m venv venv
```

### 3. Activar entorno virtual

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Si funciona correctamente aparecerá `(venv)` al inicio de la terminal.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Crear archivo `.env`

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:password@host/database
```

Ejemplo con Neon PostgreSQL:

```env
DATABASE_URL=postgresql://neondb_owner:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

> Este archivo no se sube a GitHub por seguridad (está en `.gitignore`).

---

## Etapas del Pipeline

### Etapa 1 — Ingesta

Carga el dataset original y genera una copia controlada en formato RAW. El dato original nunca es modificado, garantizando trazabilidad completa.

**Funciones:**
- Lectura del dataset CSV
- Validación de existencia del archivo
- Validación de columnas obligatorias
- Registro de métricas iniciales
- Generación de copia RAW con timestamp

Salida: `data/raw/02_bank.csv`

---

### Etapa 2 — Limpieza

Asegura calidad y consistencia del dataset antes de cualquier análisis.

**Procesos:**
- Eliminación de duplicados
- Eliminación de registros nulos
- Corrección de formatos
- Conversión de texto a minúsculas
- Limpieza de espacios
- Estandarización de categorías (job, marital, education)
- Conversión numérica de columnas requeridas

Salida: `data/processed/bank_cleaned.csv`

---

### Etapa 3 — Transformación

Enriquece los datos aplicando encoding, segmentación etaria y motor de scoring bancario. Genera 6 columnas nuevas.

#### Variables binarias

Convierte columnas categóricas a numéricas (yes → 1, no → 0):

| Variable | Descripción |
|---|---|
| default | Crédito en mora |
| housing | Préstamo hipotecario |
| loan | Préstamo personal |
| deposit | Suscripción depósito |

#### Segmentación etaria — columna `age_group`

| Rango de edad | Grupo |
|---|---|
| 18 – 30 | young |
| 30 – 45 | adult |
| 45 – 60 | senior |
| 60 – 100 | elder |

#### Motor de scoring bancario

Calcula `subscription_probability` (0–100) partiendo de un score base de **50 puntos**:

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

El score final se ajusta entre 0 y 100.

#### Clasificación por score — columnas generadas

| Score | risk_level | approval_status | premium_client |
|---|---|---|---|
| >= 80 | low | approved | yes |
| >= 60 | medium | approved | no |
| >= 40 | high | rejected | no |
| < 40 | critical | rejected | no |

#### Columnas nuevas generadas por transformación

| Columna | Descripción |
|---|---|
| `age_group` | Grupo etario del cliente |
| `subscription_probability` | Score de propensión (0–100) |
| `risk_level` | Nivel de riesgo (low/medium/high/critical) |
| `approval_status` | Estado del cliente (approved/rejected) |
| `premium_client` | Si es cliente premium (yes/no) |
| `scoring_reason` | Razones que determinaron el score |

#### Ejemplo de cliente premium

```
age: 59 | job: admin. | marital: married | education: secondary
balance: 2343 | housing: 1 | loan: 0 | default: 0
duration: 1042 | deposit: 1 | poutcome: unknown

age_group: senior
subscription_probability: 100
risk_level: low
approval_status: approved
premium_client: yes
scoring_reason: balance alto, cliente con depósito previo, duración llamada alta, cliente hipotecario estable
```

Salida: `data/processed/bank_transformed.csv`

---

### Etapa 4 — Validación

Garantiza integridad estructural y semántica del dataset transformado. Genera la columna `validation_reason` y separa los archivos finales.

#### Validación estructural

Se validan rangos y tipos antes de cualquier clasificación:

| Variable | Regla |
|---|---|
| age | 18 – 85 |
| day | 1 – 31 |
| duration | >= 0 |
| campaign | >= 0 |
| previous | >= 0 |
| pdays | >= -1 |
| subscription_probability | 0 – 100 |

Los registros que no cumplen estas reglas van directo a rechazados con `validation_reason = "Error validación estructural"`.

#### Columna `validation_reason`

La validación agrega esta columna con el detalle de la decisión:

| Caso | Formato |
|---|---|
| Aprobado | `Aprobado \| score=100 \| balance alto, duración llamada alta` |
| Premium | `Cliente premium \| score=100 \| balance alto, cliente con depósito previo` |
| Rechazado negocio | `Rechazado \| score=35 \| cliente en default, balance negativo` |
| Rechazado estructural | `Error validación estructural` |

#### Separación final de archivos

| Archivo | Contenido |
|---|---|
| `data/validated/bank_validated.csv` | Todos los clientes con `approval_status == approved` (incluye premium) |
| `data/validated/bank_premium.csv` | Solo clientes con `premium_client == yes` (score >= 80) |
| `data/reject/bank_rejected.csv` | Rechazados por negocio + rechazados estructurales |

Salidas:
- `data/validated/bank_validated.csv`
- `data/validated/bank_premium.csv`
- `data/reject/bank_rejected.csv`

---

### Etapa 5 — Carga a PostgreSQL

Conecta con Neon PostgreSQL mediante SQLAlchemy y carga los tres datasets finales. Usa `if_exists='replace'` para evitar duplicados en ejecuciones sucesivas.

**Tablas generadas:**

| Tabla | Contenido |
|---|---|
| clientes_aprobados | Clientes con approval_status == approved |
| clientes_premium | Clientes con premium_client == yes |
| clientes_rechazados | Clientes rechazados por negocio o validación |

---

## Ejecución Manual del Pipeline

> **IMPORTANTE:** Usar siempre `python -m` para que Python detecte correctamente los módulos del proyecto.

```bash
python -m scripts.ingest.ingestion_data
python -m scripts.cleaning.cleaning_data
python -m scripts.transform.transform_data
python -m scripts.validation.validation_data
python -m scripts.load.loading_data
```

---

## Ejecución con Docker

### Construir y ejecutar

```bash
docker compose up --build
```

Este comando construye la imagen, instala dependencias y ejecuta el pipeline completo automáticamente.

### Ver contenedores activos

```bash
docker ps
```

### Ver logs del contenedor

```bash
docker logs bank_marketing_pipeline
```

### Detener Docker

```bash
docker compose down
```

### Reconstruir (si modificas código o dependencias)

```bash
docker compose up --build
```

### Eliminar imágenes no utilizadas

```bash
docker system prune -a
```

### Eliminar imagen específica

```bash
docker rmi pipelinecolaborativoev2-bank-pipeline
```

**Ventajas de Docker:**
- Portabilidad del entorno
- Reproducibilidad del pipeline
- Ejecución consistente en cualquier máquina
- Fácil despliegue cloud
- Aislamiento de dependencias
- Compatibilidad con CI/CD

---

## CI/CD con GitHub Actions

El pipeline se ejecuta automáticamente:

- En cada `push` a `main`
- Manualmente desde `workflow_dispatch`

**Pasos automatizados:**
1. Clonar repositorio
2. Instalar Python
3. Instalar dependencias
4. Crear variables de entorno
5. Ejecutar ETL completo
6. Generar artefactos

Archivo de configuración: `.github/workflows/pipeline.yml`

---

## Sistema de Logging

Cada etapa genera un log independiente:

| Archivo | Contenido |
|---|---|
| `logs/ingestion.log` | Timestamp, ruta, filas, columnas leídas |
| `logs/cleaning.log` | Duplicados, nulos, tasa de retención |
| `logs/transformation.log` | Scoring, niveles de riesgo, KPIs |
| `logs/validation.log` | Aprobados, rechazados, razones de rechazo |
| `logs/loading.log` | Conexión PostgreSQL, registros por tabla |
| `logs/reporte_pipeline.log` | Reporte global con todos los logs juntos |

---

## Verificar tablas en Neon PostgreSQL

Ejecutar en el SQL Editor de Neon:

```sql
SELECT 'clientes_aprobados' AS tabla, COUNT(*) AS total_filas FROM clientes_aprobados
UNION ALL
SELECT 'clientes_premium', COUNT(*) FROM clientes_premium
UNION ALL
SELECT 'clientes_rechazados', COUNT(*) FROM clientes_rechazados;
```

---

## Calidad de Datos

El pipeline incorpora múltiples capas de validación:

- Validaciones estructurales (tipos, rangos, nulos)
- Validaciones semánticas (coherencia bancaria)
- Motor de scoring con 10 reglas de negocio
- Clasificación automática en 4 niveles de riesgo
- Separación automática aprobado/premium/rechazado
- Columna `validation_reason` con trazabilidad completa de cada decisión

---

## Casos de Uso

- Campañas bancarias segmentadas por score
- Identificación de clientes premium para priorización comercial
- Modelos predictivos de Machine Learning
- Data Warehousing bancario
- Análisis comercial por perfil de riesgo
- Scoring financiero automatizado

---

## Futuras Mejoras

| # | Mejora | Plazo | Impacto |
|---|---|---|---|
| 1 | Integrar modelo de Machine Learning (clasificador de depósitos) | 2-3 meses | Alto |
| 2 | Implementar Apache Airflow para orquestación avanzada | 3-4 meses | Alto |
| 3 | Desarrollar API REST para exponer resultados del scoring | 2 meses | Medio |
| 4 | Crear Dashboard BI (Power BI o Metabase) con KPIs en tiempo real | 1-2 meses | Medio |
| 5 | Migrar a arquitectura Data Lake en AWS S3 o Azure Blob | 6 meses | Alto |
| 6 | Implementar Feature Store para gestión de variables ML | 4-5 meses | Alto |

---

## Errores Comunes

| Error | Solución |
|---|---|
| `DATABASE_URL no encontrada` | Verificar archivo `.env` en la raíz |
| `No existe el archivo CSV` | Verificar `data/source/02_bank.csv` |
| `No module named scripts` | Usar `python -m scripts.ingest.ingestion_data` |
| `docker compose not found` | Instalar Docker Desktop |
| `Permission denied` | Ejecutar terminal como administrador |

---

## Git — Comandos Útiles

```bash
# Ver rama actual
git branch

# Ver cambios pendientes
git status

# Subir cambios
git add .
git commit -m "Actualización pipeline ETL"
git push origin feature/pipeline-reportes

# Actualizar repositorio
git pull origin main
```

---

## Desactivar entorno virtual

```bash
deactivate
```

---

## Conclusión

El pipeline Bank Marketing ETL implementa una solución completa de Ingeniería de Datos orientada al sector bancario. Automatiza el procesamiento de 11.162 registros, aplica un motor de scoring con 10 reglas de negocio, clasifica clientes en 4 niveles de riesgo y genera una base de datos lista para análisis avanzado y modelos predictivos.

La implementación con Docker y GitHub Actions garantiza reproducibilidad en cualquier entorno. Los logs auditables por etapa y la columna `validation_reason` proporcionan trazabilidad completa de cada decisión, requisito fundamental en entornos bancarios regulados.

---

## Integrantes

- Eduardo Silva V
- Mauricio Hidalgo

**Asignatura:** Gestión de datos para IA — Sección 002D  
**Docente:** Cristian Molina P