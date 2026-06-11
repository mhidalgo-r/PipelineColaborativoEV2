# ============================================
# IMAGEN BASE
# ============================================
FROM python

# ============================================
# VARIABLES DE ENTORNO
# ============================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ============================================
# DIRECTORIO DE TRABAJO
# ============================================
WORKDIR /app

# ============================================
# DEPENDENCIAS DEL SISTEMA
# (necesarias para matplotlib y psutil)
# ============================================
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# INSTALAR DEPENDENCIAS PYTHON
# ============================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# COPIAR PROYECTO
# ============================================
COPY . .

# ============================================
# CREAR DIRECTORIOS NECESARIOS
# ============================================
RUN mkdir -p data/raw \
             data/processed \
             data/validated \
             data/reject \
             data/outputs \
             logs \
             models \
             reports/figures

# ============================================
# USUARIO NO ROOT (seguridad - Ley 19.628)
# ============================================
RUN useradd -m pipelineuser
RUN chown -R pipelineuser:pipelineuser /app
USER pipelineuser

# ============================================
# PUERTO STREAMLIT
# ============================================
EXPOSE 8501

# ============================================
# COMANDO POR DEFECTO: PIPELINE COMPLETO
# ============================================
CMD ["sh", "-c", "\
    python -m scripts.ingest.ingestion_data && \
    python -m scripts.cleaning.cleaning_data && \
    python -m scripts.transform.transform_data && \
    python -m scripts.validation.validation_data && \
    python -m scripts.load.loading_data && \
    python -m scripts.eda.quality_analysis && \
    python -m scripts.eda.visual_eda && \
    python -m scripts.modeling.train_model && \
    python -m scripts.modeling.evaluate_model && \
    python -m scripts.security.security_audit && \
    python -m scripts.performance.performance_monitor \
"]