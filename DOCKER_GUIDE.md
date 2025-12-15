# 🐳 Docker Guide

## Inicio Rápido

### 1. Construir la imagen

```bash
docker build -t ai-video-generator .
```

### 2. Ejecutar con Docker

```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=tu-api-key \
  -v $(pwd)/data:/app/data \
  ai-video-generator
```

### 3. Ejecutar con Docker Compose (Recomendado)

```bash
# Crear archivo .env con tus credenciales
cp .env.example .env

# Iniciar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el servicio
docker-compose down
```

## Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose logs -f api
```

### Reiniciar el servicio
```bash
docker-compose restart
```

### Reconstruir la imagen
```bash
docker-compose up -d --build
```

### Entrar al contenedor
```bash
docker-compose exec api bash
```

### Ver estado de los servicios
```bash
docker-compose ps
```

## Verificar FFmpeg

```bash
# Entrar al contenedor
docker-compose exec api bash

# Verificar FFmpeg
ffmpeg -version
```

## Variables de Entorno

Crea un archivo `.env` con:

```env
GEMINI_API_KEY=tu-api-key
AIRTABLE_API_KEY=tu-airtable-key (opcional)
AIRTABLE_BASE_ID=tu-base-id (opcional)
AIRTABLE_TABLE_NAME=AI_Influencer_Videos (opcional)
```

## Volúmenes

El contenedor monta el directorio `./data` para persistir:
- Videos generados
- Imágenes de personajes
- Archivos temporales

## Puertos

- `8000` - API REST

## Troubleshooting

### Error: "Cannot connect to Docker daemon"
```bash
# Iniciar Docker Desktop (Windows/Mac)
# O iniciar el servicio Docker (Linux)
sudo systemctl start docker
```

### Error: "Port 8000 already in use"
```bash
# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar puerto 8001 en lugar de 8000
```

### Error: "FFmpeg not found"
```bash
# Reconstruir la imagen
docker-compose up -d --build
```

## Deployment en Producción

### Railway

```bash
# Railway detecta automáticamente el Dockerfile
railway up
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: ai-video-generator
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: GEMINI_API_KEY
        sync: false
```

### AWS ECS / Google Cloud Run

El Dockerfile está optimizado para deployment en cualquier plataforma que soporte contenedores.
