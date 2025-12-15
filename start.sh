#!/bin/bash

# Script de inicio para Railway/Docker

# Verificar que FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg no está instalado"
else
    echo "✅ FFmpeg instalado: $(ffmpeg -version | head -n 1)"
fi

# Crear directorios necesarios
mkdir -p data/output data/temp data/references

# Verificar variables de entorno
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY no está configurada"
else
    echo "✅ GEMINI_API_KEY configurada"
fi

# Iniciar la aplicación
echo "🚀 Iniciando servidor..."

# Usar el puerto de Railway si está disponible, sino usar 8000
PORT=${PORT:-8000}

exec uvicorn src.api:app --host 0.0.0.0 --port $PORT
