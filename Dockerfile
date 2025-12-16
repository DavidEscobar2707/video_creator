FROM python:3.11-slim

# Instalar FFmpeg y otras dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Actualizar pip
RUN pip install --no-cache-dir --upgrade pip

# Instalar dependencias una por una para evitar conflictos
RUN pip install --no-cache-dir google-generativeai==0.8.3 && \
    pip install --no-cache-dir requests==2.31.0 && \
    pip install --no-cache-dir python-dotenv==1.0.1 && \
    pip install --no-cache-dir gtts==2.5.0 && \
    pip install --no-cache-dir Pillow==10.4.0 && \
    pip install --no-cache-dir fastapi==0.115.0 && \
    pip install --no-cache-dir "uvicorn[standard]==0.32.0" && \
    pip install --no-cache-dir pydantic==2.9.2 && \
    pip install --no-cache-dir pydantic-settings==2.6.0 && \
    pip install --no-cache-dir python-multipart==0.0.12 && \
    pip install --no-cache-dir pyairtable==2.3.3

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/output data/temp data/references

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
