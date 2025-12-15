# 🎬 Guía Completa del API de Veo 3.1

Esta guía explica en detalle cómo funcionan las llamadas al API de Google Veo 3.1 para generación de videos con IA.

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Configuración Inicial](#configuración-inicial)
3. [Anatomía de una Llamada a Veo 3.1](#anatomía-de-una-llamada-a-veo-31)
4. [Parámetros de Configuración](#parámetros-de-configuración)
5. [Proceso de Generación](#proceso-de-generación)
6. [Manejo de Operaciones Asíncronas](#manejo-de-operaciones-asíncronas)
7. [Descarga de Videos](#descarga-de-videos)
8. [Ejemplos Prácticos](#ejemplos-prácticos)
9. [Mejores Prácticas](#mejores-prácticas)
10. [Troubleshooting](#troubleshooting)

---

## Introducción

Veo 3.1 es el modelo de generación de video de Google que permite crear videos de alta calidad a partir de:
- **Prompts de texto**: Descripciones detalladas del video deseado
- **Imágenes de referencia**: Para mantener consistencia de personajes o escenas
- **Configuración personalizada**: Aspect ratio, duración, etc.

### Modelos Disponibles

- `veo-3.1-fast-generate-preview` - Generación rápida (30-90 segundos)
- `veo-3.1-generate-preview` - Generación estándar (mayor calidad)

---

## Configuración Inicial

### 1. Obtener API Key

```bash
# Obtén tu API key desde Google AI Studio
# https://ai.google.dev
```

### 2. Instalar SDK

```bash
pip install google-generativeai
```

### 3. Inicializar Cliente

```python
from google import genai
from google.genai import types

# Inicializar cliente con API key
client = genai.Client(api_key="YOUR_API_KEY")
```

---

## Anatomía de una Llamada a Veo 3.1

### Estructura Básica

```python
from google import genai
from google.genai import types

# 1. Crear cliente
client = genai.Client(api_key=API_KEY)

# 2. Preparar imagen de referencia (opcional)
with open("character_face.jpg", "rb") as f:
    image_bytes = f.read()

image = types.Image(
    image_bytes=image_bytes,
    mime_type="image/jpeg"
)

# 3. Llamar a generate_videos
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="Professional influencer showing phone to camera",
    image=image,  # Opcional
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",
        duration_seconds=8
    )
)

# 4. Esperar a que complete (operación asíncrona)
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

# 5. Descargar video
for video in operation.response.generated_videos:
    video_uri = video.video.uri
    # Descargar desde URI...
```

---

## Parámetros de Configuración

### `model` (requerido)

El modelo de Veo a utilizar:

```python
model="veo-3.1-fast-generate-preview"  # Rápido (recomendado)
model="veo-3.1-generate-preview"       # Estándar
```

### `prompt` (requerido)

Descripción textual del video. Debe ser detallada y específica:

```python
prompt = """
Professional female influencer in her late 20s.
She is holding a smartphone and showing it to the camera with a warm smile.
The phone displays a colorful app interface.
Natural hand gestures, professional lighting.
Modern casual style - white sweater.
Cinematic quality, smooth movement, 4K.
Vertical format for social media.
"""
```

**Tips para prompts efectivos:**
- Sé específico sobre la acción y movimiento
- Describe iluminación y estilo visual
- Menciona el formato (vertical/horizontal)
- Incluye detalles de calidad (4K, cinematic)
- Describe la atmósfera y mood

### `image` (opcional)

Imagen de referencia para mantener consistencia:

```python
# Cargar imagen desde archivo
with open("reference.jpg", "rb") as f:
    image_bytes = f.read()

image = types.Image(
    image_bytes=image_bytes,
    mime_type="image/jpeg"  # o "image/png"
)
```

**Formatos soportados:**
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)

**Recomendaciones:**
- Usar imágenes de alta calidad (mínimo 1080p)
- Aspect ratio 9:16 para videos verticales
- Tamaño máximo: ~10MB

### `config` (requerido)

Configuración del video a generar:

```python
config = types.GenerateVideosConfig(
    aspect_ratio="9:16",    # Formato del video
    duration_seconds=8      # Duración (máx 8 segundos)
)
```

#### Aspect Ratios Disponibles

| Ratio | Descripción | Uso |
|-------|-------------|-----|
| `9:16` | Vertical | Instagram Stories, TikTok, Reels |
| `16:9` | Horizontal | YouTube, TV |
| `1:1` | Cuadrado | Instagram Feed |
| `4:3` | Estándar | Presentaciones |

#### Duración

```python
duration_seconds=8  # Máximo: 8 segundos
duration_seconds=5  # Mínimo: 1 segundo
```

---

## Proceso de Generación

### Flujo Completo

```python
import time
from google import genai
from google.genai import types

def generate_video_complete_flow(
    api_key: str,
    prompt: str,
    image_path: str = None,
    output_path: str = "output.mp4"
):
    """Flujo completo de generación de video con Veo 3.1"""
    
    # 1. INICIALIZACIÓN
    print("🔧 Inicializando cliente...")
    client = genai.Client(api_key=api_key)
    
    # 2. PREPARAR IMAGEN (si existe)
    image = None
    if image_path:
        print(f"📸 Cargando imagen: {image_path}")
        with open(image_path, "rb") as f:
            image = types.Image(
                image_bytes=f.read(),
                mime_type="image/jpeg"
            )
    
    # 3. ENVIAR SOLICITUD
    print("📤 Enviando solicitud a Veo 3.1...")
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        image=image,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",
            duration_seconds=8
        )
    )
    
    print(f"✅ Operación iniciada: {operation.name}")
    
    # 4. POLLING (esperar a que complete)
    print("⏳ Generando video (30-90 segundos)...")
    
    max_wait = 120  # 2 minutos máximo
    elapsed = 0
    
    while not operation.done and elapsed < max_wait:
        time.sleep(5)
        elapsed += 5
        
        # Actualizar estado de la operación
        operation = client.operations.get(operation)
        
        print(f"   ... {elapsed}s transcurridos")
    
    # 5. VERIFICAR RESULTADO
    if not operation.done:
        raise TimeoutError("La generación excedió el tiempo máximo")
    
    print("✅ Video generado exitosamente!")
    
    # 6. DESCARGAR VIDEO
    print("⬇️  Descargando video...")
    
    for video in operation.response.generated_videos:
        video_uri = video.video.uri
        
        # Descargar con autenticación
        import requests
        headers = {'x-goog-api-key': api_key}
        response = requests.get(video_uri, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Video guardado: {output_path}")
            return output_path
        else:
            raise Exception(f"Error descargando: HTTP {response.status_code}")
    
    return None
```

---

## Manejo de Operaciones Asíncronas

Veo 3.1 utiliza operaciones asíncronas (long-running operations) que requieren polling.

### Estructura de una Operación

```python
operation = client.models.generate_videos(...)

# Propiedades importantes:
operation.name      # ID único de la operación
operation.done      # Boolean: ¿completó?
operation.response  # Resultado (cuando done=True)
operation.error     # Error (si falló)
```

### Patrón de Polling Básico

```python
import time

# Iniciar operación
operation = client.models.generate_videos(...)

# Polling simple
while not operation.done:
    time.sleep(5)  # Esperar 5 segundos
    operation = client.operations.get(operation)  # Actualizar estado

# Operación completada
if operation.response:
    print("✅ Éxito!")
else:
    print(f"❌ Error: {operation.error}")
```

### Patrón de Polling con Timeout

```python
import time

def wait_for_operation(client, operation, timeout=120):
    """
    Espera a que una operación complete con timeout.
    
    Args:
        client: Cliente de Gemini
        operation: Operación a monitorear
        timeout: Tiempo máximo en segundos
        
    Returns:
        operation completada o None si timeout
    """
    elapsed = 0
    
    while not operation.done and elapsed < timeout:
        time.sleep(5)
        elapsed += 5
        
        # Actualizar operación
        operation = client.operations.get(operation)
        
        # Callback de progreso (opcional)
        progress = min(int((elapsed / timeout) * 100), 99)
        print(f"Progreso: {progress}% ({elapsed}/{timeout}s)")
    
    if not operation.done:
        return None  # Timeout
    
    return operation
```

### Patrón de Polling con Progreso

```python
def wait_with_progress(client, operation, timeout=120, callback=None):
    """Polling con callback de progreso"""
    elapsed = 0
    
    while not operation.done and elapsed < timeout:
        time.sleep(5)
        elapsed += 5
        operation = client.operations.get(operation)
        
        # Llamar callback si existe
        if callback:
            progress = min(int((elapsed / timeout) * 100), 99)
            callback(progress, elapsed, timeout)
    
    return operation if operation.done else None

# Uso:
def on_progress(progress, elapsed, total):
    print(f"⏳ {progress}% - {elapsed}/{total}s")

operation = client.models.generate_videos(...)
result = wait_with_progress(client, operation, callback=on_progress)
```

---

## Descarga de Videos

### Método 1: Descarga Directa

```python
import requests

def download_video(video_uri: str, api_key: str, output_path: str):
    """Descarga video desde URI de Veo"""
    
    # Headers con autenticación
    headers = {'x-goog-api-key': api_key}
    
    # Descargar
    response = requests.get(video_uri, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Error HTTP {response.status_code}")

# Uso:
for video in operation.response.generated_videos:
    download_video(video.video.uri, API_KEY, "output.mp4")
```

### Método 2: Descarga con Progress Bar

```python
import requests
from tqdm import tqdm

def download_with_progress(video_uri: str, api_key: str, output_path: str):
    """Descarga con barra de progreso"""
    
    headers = {'x-goog-api-key': api_key}
    response = requests.get(video_uri, headers=headers, stream=True)
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    
    return output_path
```

### Método 3: Descarga con Reintentos

```python
import requests
import time

def download_with_retry(video_uri: str, api_key: str, output_path: str, max_retries=3):
    """Descarga con reintentos automáticos"""
    
    headers = {'x-goog-api-key': api_key}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(video_uri, headers=headers, timeout=60)
            
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return output_path
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️  Intento {attempt + 1} falló. Reintentando en {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Descarga falló después de {max_retries} intentos: {e}")
    
    return None
```

---

## Ejemplos Prácticos

### Ejemplo 1: Video Simple (Solo Texto)

```python
from google import genai
from google.genai import types
import time

API_KEY = "your-api-key"
client = genai.Client(api_key=API_KEY)

# Generar video solo con prompt
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="A professional woman smiling at camera, modern office background, natural lighting",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds=5
    )
)

# Esperar
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

# Descargar
import requests
for video in operation.response.generated_videos:
    headers = {'x-goog-api-key': API_KEY}
    response = requests.get(video.video.uri, headers=headers)
    
    with open("simple_video.mp4", "wb") as f:
        f.write(response.content)

print("✅ Video creado: simple_video.mp4")
```

### Ejemplo 2: Video con Imagen de Referencia

```python
from google import genai
from google.genai import types
import time

API_KEY = "your-api-key"
client = genai.Client(api_key=API_KEY)

# Cargar imagen de referencia
with open("character_face.jpg", "rb") as f:
    image = types.Image(
        image_bytes=f.read(),
        mime_type="image/jpeg"
    )

# Generar video con referencia
operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="""
    The person from the reference image is holding a smartphone.
    She shows the phone screen to the camera with a warm smile.
    Natural hand gestures, professional lighting.
    White sweater, modern style.
    Vertical format, cinematic quality.
    """,
    image=image,
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",
        duration_seconds=8
    )
)

# Esperar y descargar
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

import requests
for video in operation.response.generated_videos:
    headers = {'x-goog-api-key': API_KEY}
    response = requests.get(video.video.uri, headers=headers)
    
    with open("influencer_video.mp4", "wb") as f:
        f.write(response.content)

print("✅ Video con referencia creado: influencer_video.mp4")
```

### Ejemplo 3: Generación con Manejo de Errores

```python
from google import genai
from google.genai import types
import time
import requests

def generate_video_safe(
    api_key: str,
    prompt: str,
    image_path: str = None,
    output_path: str = "output.mp4",
    timeout: int = 120
):
    """Generación de video con manejo completo de errores"""
    
    try:
        # Inicializar
        client = genai.Client(api_key=api_key)
        
        # Preparar imagen
        image = None
        if image_path:
            try:
                with open(image_path, "rb") as f:
                    image = types.Image(
                        image_bytes=f.read(),
                        mime_type="image/jpeg"
                    )
            except FileNotFoundError:
                print(f"⚠️  Imagen no encontrada: {image_path}")
                print("   Continuando sin imagen de referencia...")
        
        # Generar
        print("📤 Enviando solicitud...")
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                duration_seconds=8
            )
        )
        
        # Polling con timeout
        print("⏳ Generando video...")
        elapsed = 0
        
        while not operation.done and elapsed < timeout:
            time.sleep(5)
            elapsed += 5
            operation = client.operations.get(operation)
            print(f"   {elapsed}s / {timeout}s")
        
        if not operation.done:
            raise TimeoutError(f"Timeout después de {timeout}s")
        
        # Verificar errores
        if operation.error:
            raise Exception(f"Error en generación: {operation.error}")
        
        # Descargar
        print("⬇️  Descargando...")
        for video in operation.response.generated_videos:
            headers = {'x-goog-api-key': api_key}
            response = requests.get(video.video.uri, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Error descarga: HTTP {response.status_code}")
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Video guardado: {output_path}")
            return output_path
        
    except TimeoutError as e:
        print(f"❌ Timeout: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Uso:
result = generate_video_safe(
    api_key="your-api-key",
    prompt="Professional influencer video",
    image_path="reference.jpg",
    output_path="final_video.mp4"
)
```

---

## Mejores Prácticas

### 1. Prompts Efectivos

✅ **BUENO:**
```python
prompt = """
Professional female influencer in her late 20s.
She is holding a smartphone and showing it to the camera.
Warm, engaging smile with natural hand gestures.
White knitted sweater, minimalist gold necklace.
Cinematic lighting with soft shadows.
Modern, clean aesthetic.
Vertical format for social media.
Smooth, natural movement.
4K quality, professional photography style.
"""
```

❌ **MALO:**
```python
prompt = "Woman with phone"  # Muy vago
```

### 2. Imágenes de Referencia

✅ **Recomendaciones:**
- Usar imágenes de alta resolución (mínimo 1080p)
- Aspect ratio consistente con el video deseado
- Buena iluminación y enfoque
- Rostro claramente visible
- Fondo limpio

❌ **Evitar:**
- Imágenes borrosas o de baja calidad
- Múltiples personas en la imagen
- Fondos muy complejos
- Imágenes muy oscuras

### 3. Configuración de Timeout

```python
# Tiempos recomendados según modelo:
TIMEOUTS = {
    "veo-3.1-fast-generate-preview": 120,  # 2 minutos
    "veo-3.1-generate-preview": 300        # 5 minutos
}
```

### 4. Manejo de Cuotas

```python
import time

def generate_with_rate_limit(client, requests_per_minute=10):
    """Generador con límite de tasa"""
    
    min_interval = 60 / requests_per_minute
    last_request = 0
    
    def generate(*args, **kwargs):
        nonlocal last_request
        
        # Esperar si es necesario
        elapsed = time.time() - last_request
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        # Hacer solicitud
        result = client.models.generate_videos(*args, **kwargs)
        last_request = time.time()
        
        return result
    
    return generate
```

### 5. Logging y Monitoreo

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_with_logging(client, prompt, **kwargs):
    """Generación con logging detallado"""
    
    logger.info(f"Iniciando generación")
    logger.info(f"Prompt: {prompt[:100]}...")
    
    start_time = time.time()
    
    try:
        operation = client.models.generate_videos(
            prompt=prompt,
            **kwargs
        )
        
        logger.info(f"Operación iniciada: {operation.name}")
        
        # Polling
        elapsed = 0
        while not operation.done:
            time.sleep(5)
            elapsed += 5
            operation = client.operations.get(operation)
            logger.debug(f"Polling: {elapsed}s")
        
        total_time = time.time() - start_time
        logger.info(f"Generación completada en {total_time:.1f}s")
        
        return operation
        
    except Exception as e:
        logger.error(f"Error en generación: {e}")
        raise
```

---

## Troubleshooting

### Error: "API key not valid"

```python
# Verificar que la API key esté configurada
import os
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY no configurada")
```

### Error: "Timeout"

```python
# Aumentar timeout
timeout = 180  # 3 minutos en lugar de 2

# O verificar conexión
import requests
try:
    requests.get("https://www.google.com", timeout=5)
except:
    print("❌ Sin conexión a internet")
```

### Error: "Quota exceeded"

```python
# Implementar retry con backoff exponencial
import time

def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "quota" in str(e).lower():
                wait = 2 ** i
                print(f"Cuota excedida. Esperando {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries alcanzado")
```

### Video no se genera correctamente

```python
# Verificar prompt
print(f"Longitud del prompt: {len(prompt)} caracteres")
if len(prompt) < 50:
    print("⚠️  Prompt muy corto. Añade más detalles.")

# Verificar imagen
if image_path:
    from PIL import Image
    img = Image.open(image_path)
    print(f"Dimensiones: {img.size}")
    print(f"Formato: {img.format}")
```

---

## Recursos Adicionales

- [Google AI Studio](https://ai.google.dev)
- [Documentación oficial de Gemini API](https://ai.google.dev/docs)
- [Ejemplos de código](https://github.com/google/generative-ai-python)

---

**Última actualización:** Diciembre 2024
