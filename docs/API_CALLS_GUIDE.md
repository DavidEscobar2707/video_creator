# 🎬 Guía Completa: API Calls para Veo3

## 1. Setup Inicial

```python
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Cargar API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Crear cliente
client = genai.Client(api_key=API_KEY)
```

---

## 2. API Call Básico - Generar Video desde Imagen

### Paso 1: Cargar la imagen

```python
# Leer imagen como bytes
with open("references/character_face.jpg", "rb") as f:
    image_bytes = f.read()

# Crear objeto Image
image = types.Image(
    image_bytes=image_bytes,
    mime_type="image/jpeg"  # o "image/png", "image/webp"
)
```

### Paso 2: Crear configuración del video

```python
config = types.GenerateVideosConfig(
    aspect_ratio="9:16",      # Vertical para redes sociales
    duration_seconds=8,        # Máximo 8 segundos
    # resolution="720p"       # Opcional
)
```

### Paso 3: Hacer el API call

```python
# LLAMADA PRINCIPAL
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",  # Modelo Veo3
    prompt="Professional female influencer looking at camera with warm smile",
    image=image,                             # Imagen base
    config=config                            # Configuración
)
```

**Respuesta:**
```
Operation {
  name: "operations/abc123xyz",
  done: False,
  result: None
}
```

---

## 3. Polling - Esperar a que se complete

```python
import time

max_wait = 120  # 2 minutos máximo
elapsed = 0

while not operation.done and elapsed < max_wait:
    time.sleep(5)  # Esperar 5 segundos
    elapsed += 5
    
    # Obtener estado actualizado
    operation = client.operations.get(operation)
    
    print(f"Status: {elapsed}s - Done: {operation.done}")

if not operation.done:
    print("❌ Timeout - generación tomó demasiado tiempo")
else:
    print("✅ Generación completada!")
```

**Salida esperada:**
```
Status: 5s - Done: False
Status: 10s - Done: False
Status: 15s - Done: False
...
Status: 60s - Done: True
✅ Generación completada!
```

---

## 4. Obtener el Video Generado

```python
# Acceder a la respuesta
response = operation.response

# Iterar sobre videos generados
for video in response.generated_videos:
    # Obtener URI del video
    video_uri = video.video.uri
    print(f"Video URI: {video_uri}")
    
    # Ejemplo de URI:
    # https://generativelanguage.googleapis.com/v1beta/files/abc123:download?alt=media
```

---

## 5. Descargar el Video

```python
import requests

# Headers con autenticación
headers = {
    'x-goog-api-key': API_KEY
}

# Descargar video
response = requests.get(video_uri, headers=headers)

if response.status_code == 200:
    # Guardar archivo
    with open("output/video.mp4", "wb") as f:
        f.write(response.content)
    
    print(f"✅ Video guardado: {len(response.content)} bytes")
else:
    print(f"❌ Error: HTTP {response.status_code}")
```

---

## 6. Ejemplo Completo - Flujo Completo

```python
from google import genai
from google.genai import types
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def generate_video_complete():
    """Flujo completo de generación de video"""
    
    # 1. Crear cliente
    client = genai.Client(api_key=API_KEY)
    
    # 2. Cargar imagen
    with open("references/character_face.jpg", "rb") as f:
        image_bytes = f.read()
    
    image = types.Image(
        image_bytes=image_bytes,
        mime_type="image/jpeg"
    )
    
    # 3. Configurar video
    config = types.GenerateVideosConfig(
        aspect_ratio="9:16",
        duration_seconds=8
    )
    
    # 4. HACER API CALL
    print("📤 Enviando solicitud a Veo3...")
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt="Professional influencer showing phone to camera",
        image=image,
        config=config
    )
    
    # 5. POLLING
    print("⏳ Esperando generación...")
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)
        print(".", end="", flush=True)
    
    print("\n✅ Completado!")
    
    # 6. DESCARGAR
    for video in operation.response.generated_videos:
        video_uri = video.video.uri
        
        headers = {'x-goog-api-key': API_KEY}
        response = requests.get(video_uri, headers=headers)
        
        if response.status_code == 200:
            with open("output/video.mp4", "wb") as f:
                f.write(response.content)
            print(f"✅ Video guardado!")
            return "output/video.mp4"
    
    return None

# Ejecutar
if __name__ == "__main__":
    video_path = generate_video_complete()
```

---

## 7. Parámetros Disponibles

### Modelos Veo3

```python
# Modelos disponibles:
"veo-3.1-fast-generate-preview"    # Rápido (recomendado)
"veo-3.1-generate-preview"         # Calidad alta
"veo-3.0-fast-generate-001"        # Versión anterior
"veo-3.0-generate-001"             # Versión anterior
```

### Aspect Ratios

```python
aspect_ratio="16:9"    # Horizontal
aspect_ratio="9:16"    # Vertical (redes sociales)
aspect_ratio="1:1"     # Cuadrado
aspect_ratio="4:3"     # Estándar
```

### Duración

```python
duration_seconds=1     # Mínimo
duration_seconds=8     # Máximo
```

---

## 8. Manejo de Errores

```python
try:
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        image=image,
        config=config
    )
    
    # Polling con manejo de errores
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)
        
        # Verificar si hay error
        if operation.error:
            print(f"❌ Error: {operation.error.message}")
            return None
    
    # Verificar respuesta
    if not operation.response or not operation.response.generated_videos:
        print("❌ No videos generated")
        return None
    
    # Procesar video
    for video in operation.response.generated_videos:
        # ...
        
except Exception as e:
    print(f"❌ Exception: {e}")
    return None
```

---

## 9. Estructura de Respuesta

```python
# Estructura completa de la respuesta:
operation = {
    "name": "operations/abc123xyz",
    "done": True,
    "response": {
        "generated_videos": [
            {
                "video": {
                    "uri": "https://generativelanguage.googleapis.com/...",
                    "mime_type": "video/mp4"
                }
            }
        ]
    }
}

# Acceder a datos:
video_uri = operation.response.generated_videos[0].video.uri
mime_type = operation.response.generated_videos[0].video.mime_type
```

---

## 10. Optimizaciones

### Timeout personalizado

```python
max_wait = 180  # 3 minutos
elapsed = 0
poll_interval = 5  # Segundos entre polls

while not operation.done and elapsed < max_wait:
    time.sleep(poll_interval)
    elapsed += poll_interval
    operation = client.operations.get(operation)
    
    # Mostrar progreso
    progress = (elapsed / max_wait) * 100
    print(f"Progress: {progress:.0f}%")
```

### Reintentos

```python
import time

max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        operation = client.models.generate_videos(...)
        break
    except Exception as e:
        retry_count += 1
        if retry_count < max_retries:
            print(f"Retry {retry_count}/{max_retries}...")
            time.sleep(2 ** retry_count)  # Backoff exponencial
        else:
            raise
```

---

## 11. Comparación: REST API vs SDK

### REST API (HTTP directo)

```bash
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-fast-generate-preview:generateVideo \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{
    "prompt": "Professional influencer...",
    "config": {
      "aspectRatio": "9:16",
      "durationSeconds": 8
    }
  }'
```

### SDK Python (Recomendado)

```python
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="Professional influencer...",
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",
        duration_seconds=8
    )
)
```

**El SDK es más fácil y maneja automáticamente:**
- Serialización JSON
- Autenticación
- Polling
- Manejo de errores

---

## 12. Límites y Cuotas

```python
# Límites típicos:
# - Máximo 8 segundos por video
# - Máximo 1 video por request
# - Máximo 100 requests por día (varía según plan)
# - Máximo 1 imagen de entrada
# - Formatos soportados: JPEG, PNG, WebP

# Verificar cuotas:
# Ir a: https://console.cloud.google.com/apis/dashboard
```

---

## 13. Debugging

```python
# Ver detalles de la operación
print(f"Operation name: {operation.name}")
print(f"Operation done: {operation.done}")
print(f"Operation error: {operation.error}")
print(f"Operation response: {operation.response}")

# Ver detalles del video
if operation.response:
    for i, video in enumerate(operation.response.generated_videos):
        print(f"Video {i}:")
        print(f"  URI: {video.video.uri}")
        print(f"  MIME: {video.video.mime_type}")
```

---

## Resumen Rápido

```python
# 1. Cargar imagen
image = types.Image(image_bytes=bytes, mime_type="image/jpeg")

# 2. Configurar
config = types.GenerateVideosConfig(aspect_ratio="9:16", duration_seconds=8)

# 3. API CALL
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="...",
    image=image,
    config=config
)

# 4. Polling
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

# 5. Descargar
video_uri = operation.response.generated_videos[0].video.uri
response = requests.get(video_uri, headers={'x-goog-api-key': API_KEY})
with open("video.mp4", "wb") as f:
    f.write(response.content)
```

---

¡Eso es todo! Ahora entiendes exactamente cómo funcionan los API calls para Veo3.
