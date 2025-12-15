FROM python:3.11-slim

# Instalar FFmpeg y otras dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .

# Actualizar pip y setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Limpiar cualquier instalación previa de google packages
RUN pip uninstall -y google google-api-core google-auth google-generativeai || true

# Instalar todas las dependencias de una vez (esto resuelve dependencias correctamente)
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Verificar que google-generativeai se instaló correctamente
RUN python -c "from google import genai; print('✅ google-generativeai instalado correctamente')"

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/output data/temp data/references

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
