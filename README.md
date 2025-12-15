# 🎬 AI Influencer Video Generator

Generador profesional de videos de influencers usando Google Veo 3.1 e Imagen 4.0.

## 🚀 Inicio Rápido

### 1. Instalación

```bash
git clone <repository-url>
cd ai-influencer-video-generator
pip install -r requirements.txt
```

### 2. Configuración

```bash
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY
```

Obtén tu API key desde [Google AI Studio](https://ai.google.dev)

### 3. Instalar FFmpeg

- **Windows**: https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 📋 Uso

### Opción 1: Python directo

```bash
python main.py
# http://localhost:8000/docs
```

### Opción 2: Docker (Recomendado)

```bash
docker-compose up -d
# http://localhost:8000/docs
```

Ver [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para más detalles.

## 🔌 Endpoints de la API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/character/generate` | POST | Generar imagen de personaje |
| `/api/v1/video/generate` | POST | Generar video de influencer |
| `/api/v1/video/add-subtitles` | POST | Agregar subtítulos a video |
| `/api/v1/voiceover/generate` | POST | Generar audio de voiceover |
| `/api/v1/job/{job_id}` | GET | Verificar estado del trabajo |
| `/api/v1/download/{filename}` | GET | Descargar archivo generado |

## ⚙️ Configuración

Variables de entorno (`.env`):

```env
# Requerido
GEMINI_API_KEY=tu-api-key

# Opcional
AIRTABLE_API_KEY=tu-airtable-key
AIRTABLE_BASE_ID=tu-base-id
AIRTABLE_TABLE_NAME=AI_Influencer_Videos
API_HOST=0.0.0.0
API_PORT=8000
```

## 📖 Documentación

- [Guía de Veo 3.1 API](docs/VEO3_API_GUIDE.md)
- [Ejemplos de Uso](docs/API_USAGE_EXAMPLES.md)
- [Quick Start](docs/QUICK_START.md)

## 📝 Requisitos

- Python 3.10+
- API key de Gemini (Veo 3.1 + Imagen 4.0)
- FFmpeg instalado
- ~5GB de espacio en disco

## 📦 Dependencias Principales

- `google-generativeai` - Veo 3.1 e Imagen 4.0
- `fastapi` - REST API
- `pydantic` - Validación de datos
- `gtts` - Text-to-speech
- `pyairtable` - Integración con Airtable
- `requests` - Cliente HTTP
- `pillow` - Procesamiento de imágenes

---

**Hecho con ❤️ usando Google Gemini AI**
