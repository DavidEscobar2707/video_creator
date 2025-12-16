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

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/output data/temp data/references

# Copiar start script
COPY start.py /app/start.py

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "start.py"]
