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

# Actualizar pip y instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Copiar y dar permisos al script de inicio
COPY start.sh .
RUN chmod +x start.sh

# Crear directorios necesarios
RUN mkdir -p data/output data/temp data/references

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["./start.sh"]
