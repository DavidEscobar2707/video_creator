# 🚀 Quick Start - Guía Rápida

Comienza a usar la API en 5 minutos.

## 1️⃣ Instalación (2 minutos)

```bash
# Clonar proyecto
git clone <repository-url>
cd ai-influencer-video-generator

# Instalar dependencias
pip install -r requirements.txt

# Copiar configuración
cp .env.example .env
```

## 2️⃣ Configurar API Key (1 minuto)

1. Ve a https://ai.google.dev
2. Click en "Get API Key"
3. Copia la key
4. Abre `.env` y pega:
```env
GEMINI_API_KEY=tu-api-key-aqui
```

## 3️⃣ Iniciar Servidor (1 minuto)

```bash
python main.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 4️⃣ Probar API (1 minuto)

### Opción A: Usar el HTML de prueba

```bash
# Abre en tu navegador
test_frontend.html
```

### Opción B: Usar Postman

1. Descarga Postman: https://www.postman.com/downloads/
2. Importa la colección: `docs/postman_collection.json`
3. Prueba los endpoints

### Opción C: Usar cURL

```bash
# Verificar servidor
curl http://localhost:8000/health

# Generar video
curl -X POST http://localhost:8000/api/v1/video/generate \
  -F "prompt=Professional influencer showing phone" \
  -F "product_description=TinyHeroes.ai app" \
  -F "character_face=@image.jpg" \
  -F "aspect_ratio=9:16" \
  -F "duration_seconds=8"
```

---

## 📚 Documentación Completa

- **[POSTMAN_FRONTEND_GUIDE.md](POSTMAN_FRONTEND_GUIDE.md)** - Guía paso a paso con ejemplos
- **[VEO3_API_GUIDE.md](VEO3_API_GUIDE.md)** - Documentación técnica de Veo 3.1
- **[API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md)** - Ejemplos de código

---

## 🎯 Flujo Básico

```
1. Seleccionar imagen
   ↓
2. POST /api/v1/video/generate
   ↓
3. Guardar job_id
   ↓
4. GET /api/v1/job/{job_id} (cada 5s)
   ↓
5. Cuando status = "completed"
   ↓
6. GET /api/v1/download/{filename}
   ↓
7. ¡Video descargado!
```

---

## 🔗 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verificar servidor |
| `/api/v1/character/generate` | POST | Generar personaje |
| `/api/v1/video/generate` | POST | Generar video |
| `/api/v1/voiceover/generate` | POST | Generar audio |
| `/api/v1/job/{job_id}` | GET | Verificar estado |
| `/api/v1/download/{filename}` | GET | Descargar archivo |

---

## 💻 Ejemplo JavaScript Mínimo

```javascript
// 1. Generar video
const formData = new FormData();
formData.append('prompt', 'Professional influencer showing phone');
formData.append('product_description', 'TinyHeroes.ai app');
formData.append('character_face', fileInput.files[0]);
formData.append('aspect_ratio', '9:16');
formData.append('duration_seconds', '8');

const response = await fetch('http://localhost:8000/api/v1/video/generate', {
  method: 'POST',
  body: formData
});

const result = await response.json();
const jobId = result.job_id;

// 2. Verificar estado
const interval = setInterval(async () => {
  const status = await fetch(`http://localhost:8000/api/v1/job/${jobId}`);
  const data = await status.json();
  
  console.log(`${data.progress}% - ${data.message}`);
  
  if (data.status === 'completed') {
    clearInterval(interval);
    console.log('Video listo:', data.result_url);
  }
}, 5000);
```

---

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| "Connection refused" | Verifica que el servidor está corriendo: `python main.py` |
| "GEMINI_API_KEY not found" | Configura `.env` con tu API key |
| "Cannot POST /api/v1/video/generate" | Asegúrate de usar `http://` no `https://` |
| "CORS error" | El servidor ya tiene CORS habilitado |

---

## 📱 Probar en el Navegador

Abre `test_frontend.html` en tu navegador para una interfaz visual completa.

---

**¡Listo! Ya puedes generar videos con IA 🎉**
