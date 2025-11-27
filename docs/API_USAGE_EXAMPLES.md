# 🚀 API Usage Examples

## Iniciar el Servidor

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python api.py
```

El servidor estará disponible en: `http://localhost:8000`

**Documentación interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📋 Endpoints Disponibles

### 1. Health Check
```
GET /health
```

### 2. Generate Character
```
POST /api/v1/character/generate
```

### 3. Generate Video
```
POST /api/v1/video/generate
```

### 4. Generate Voiceover
```
POST /api/v1/voiceover/generate
```

### 5. Check Job Status
```
GET /api/v1/job/{job_id}
```

### 6. Download File
```
GET /api/v1/download/{filename}
```

---

## 🔥 Ejemplos con Postman

### Ejemplo 1: Generar Character

**Request:**
```
POST http://localhost:8000/api/v1/character/generate
Content-Type: multipart/form-data

Body (form-data):
- description: "Professional female influencer in her late 20s, warm smile, white sweater, modern style"
```

**Response:**
```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "pending",+65
  "progress": 0,
  "message": "Character generation started",
  "result_url": null,
  "error": null
}
```

---

### Ejemplo 2: Generar Video

**Request:**
```
POST http://localhost:8000/api/v1/video/generate
Content-Type: multipart/form-data

Body (form-data):
- prompt: "Professional influencer showing phone to camera with engaging smile"
- product_description: "TinyHeroes.ai app - Transform photos with AI magic"
- character_face: [Upload file: character_face.jpg]
- aspect_ratio: "9:16"
- duration_seconds: 8
```

**Response:**
```json
{
  "job_id": "xyz789-abc123-def456",
  "status": "pending",
  "progress": 0,
  "message": "Video generation started",
  "result_url": null,
  "error": null
}
```

---

### Ejemplo 3: Check Job Status

**Request:**
```
GET http://localhost:8000/api/v1/job/xyz789-abc123-def456
```

**Response (Processing):**
```json
{
  "job_id": "xyz789-abc123-def456",
  "status": "processing",
  "progress": 45,
  "message": "Generating video (30-90 seconds)...",
  "result_url": null,
  "error": null
}
```

**Response (Completed):**
```json
{
  "job_id": "xyz789-abc123-def456",
  "status": "completed",
  "progress": 100,
  "message": "Video generated successfully",
  "result_url": "/api/v1/download/xyz789-abc123-def456_video.mp4",
  "error": null
}
```

---

### Ejemplo 4: Download Video

**Request:**
```
GET http://localhost:8000/api/v1/download/xyz789-abc123-def456_video.mp4
```

**Response:**
Binary file download (video.mp4)

---

## 💻 Ejemplos con Python

### Ejemplo Completo: Generar Video

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Generate video
with open("references/character_face.jpg", "rb") as f:
    files = {"character_face": f}
    data = {
        "prompt": "Professional influencer showing phone with engaging smile",
        "product_description": "TinyHeroes.ai - Transform photos with AI",
        "aspect_ratio": "9:16",
        "duration_seconds": 8
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/video/generate",
        files=files,
        data=data
    )
    
    result = response.json()
    job_id = result["job_id"]
    print(f"Job ID: {job_id}")

# 2. Poll for status
while True:
    response = requests.get(f"{BASE_URL}/api/v1/job/{job_id}")
    status = response.json()
    
    print(f"Status: {status['status']} - Progress: {status['progress']}%")
    
    if status["status"] == "completed":
        print(f"✅ Done! Download: {status['result_url']}")
        break
    elif status["status"] == "failed":
        print(f"❌ Failed: {status['error']}")
        break
    
    time.sleep(5)

# 3. Download video
if status["status"] == "completed":
    download_url = f"{BASE_URL}{status['result_url']}"
    response = requests.get(download_url)
    
    with open("downloaded_video.mp4", "wb") as f:
        f.write(response.content)
    
    print("✅ Video downloaded!")
```

---

## 🌐 Ejemplos con JavaScript (Frontend)

### Ejemplo con Fetch API

```javascript
// 1. Generate video
async function generateVideo() {
  const formData = new FormData();
  formData.append('prompt', 'Professional influencer showing phone');
  formData.append('product_description', 'TinyHeroes.ai app');
  formData.append('aspect_ratio', '9:16');
  formData.append('duration_seconds', '8');
  
  // Get file from input
  const fileInput = document.getElementById('characterFace');
  formData.append('character_face', fileInput.files[0]);
  
  const response = await fetch('http://localhost:8000/api/v1/video/generate', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  const jobId = result.job_id;
  
  console.log('Job ID:', jobId);
  
  // 2. Poll for status
  pollJobStatus(jobId);
}

async function pollJobStatus(jobId) {
  const interval = setInterval(async () => {
    const response = await fetch(`http://localhost:8000/api/v1/job/${jobId}`);
    const status = await response.json();
    
    console.log(`Status: ${status.status} - Progress: ${status.progress}%`);
    
    // Update UI
    document.getElementById('progress').innerText = `${status.progress}%`;
    document.getElementById('message').innerText = status.message;
    
    if (status.status === 'completed') {
      clearInterval(interval);
      
      // Show download link
      const downloadUrl = `http://localhost:8000${status.result_url}`;
      document.getElementById('download').href = downloadUrl;
      document.getElementById('download').style.display = 'block';
      
      console.log('✅ Video ready!');
    } else if (status.status === 'failed') {
      clearInterval(interval);
      console.error('❌ Failed:', status.error);
    }
  }, 5000); // Poll every 5 seconds
}
```

---

## 📱 Ejemplo con cURL

### Generate Video

```bash
curl -X POST "http://localhost:8000/api/v1/video/generate" \
  -F "prompt=Professional influencer showing phone" \
  -F "product_description=TinyHeroes.ai app" \
  -F "character_face=@references/character_face.jpg" \
  -F "aspect_ratio=9:16" \
  -F "duration_seconds=8"
```

### Check Status

```bash
curl "http://localhost:8000/api/v1/job/abc123-def456"
```

### Download Video

```bash
curl -O "http://localhost:8000/api/v1/download/abc123-def456_video.mp4"
```

---

## 🎯 Flujo Completo Recomendado

```
1. POST /api/v1/character/generate
   ↓ (Get job_id)
   
2. GET /api/v1/job/{job_id} (Poll every 5s)
   ↓ (Wait until status = "completed")
   
3. GET /api/v1/download/{filename}
   ↓ (Download character image)
   
4. POST /api/v1/video/generate (Use downloaded image)
   ↓ (Get job_id)
   
5. GET /api/v1/job/{job_id} (Poll every 5s)
   ↓ (Wait until status = "completed")
   
6. GET /api/v1/download/{filename}
   ↓ (Download final video)
```

---

## 🔐 Seguridad (Producción)

Para producción, agrega autenticación:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return token

# Protect endpoints
@app.post("/api/v1/video/generate", dependencies=[Depends(verify_token)])
async def generate_video(...):
    # ...
```

**Request con token:**
```bash
curl -X POST "http://localhost:8000/api/v1/video/generate" \
  -H "Authorization: Bearer your-secret-token" \
  -F "prompt=..." \
  -F "character_face=@image.jpg"
```

---

## 📊 Rate Limiting (Producción)

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/video/generate")
@limiter.limit("5/minute")  # Max 5 requests per minute
async def generate_video(request: Request, ...):
    # ...
```

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

```bash
# Build
docker build -t influencer-api .

# Run
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key influencer-api
```

---

## 📝 Postman Collection

Importa esta colección en Postman:

```json
{
  "info": {
    "name": "AI Influencer Video Generator",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Generate Video",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "prompt",
              "value": "Professional influencer showing phone",
              "type": "text"
            },
            {
              "key": "product_description",
              "value": "TinyHeroes.ai app",
              "type": "text"
            },
            {
              "key": "character_face",
              "type": "file",
              "src": "/path/to/image.jpg"
            },
            {
              "key": "aspect_ratio",
              "value": "9:16",
              "type": "text"
            },
            {
              "key": "duration_seconds",
              "value": "8",
              "type": "text"
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8000/api/v1/video/generate",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "v1", "video", "generate"]
        }
      }
    },
    {
      "name": "Check Job Status",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:8000/api/v1/job/{{job_id}}",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "v1", "job", "{{job_id}}"]
        }
      }
    }
  ]
}
```

---

¡Listo! Ahora tienes una API REST completa y profesional.
