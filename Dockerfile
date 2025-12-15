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

# Instalar google-generativeai primero para evitar conflictos de namespace
RUN pip install --no-cache-dir google-generativeai==0.8.3

# Instalar el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/output data/temp data/references

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
