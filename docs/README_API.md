# 🚀 AI Influencer Video Generator API

REST API profesional para generar videos de influencers AI usando Veo3 y Imagen 4.0.

## ✅ Servidor Activo

El servidor está corriendo en: **http://localhost:8000**

### 📚 Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎯 Quick Start

### 1. Probar en el Navegador

Abre: **http://localhost:8000/docs**

Verás una interfaz donde puedes probar todos los endpoints directamente.

### 2. Probar con Postman

#### Generar Video

```
POST http://localhost:8000/api/v1/video/generate

Body (form-data):
- prompt: "Professional influencer showing phone with engaging smile"
- product_description: "TinyHeroes.ai - Transform photos with AI magic"
- character_face: [Upload: references/character_face.jpg]
- aspect_ratio: "9:16"
- duration_seconds: 8
```

**Respuesta:**
```json
{
  "job_id": "abc-123-xyz",
  "status": "pending",
  "progress": 0,
  "message": "Video generation started"
}
```

#### Ver Progreso

```
GET http://localhost:8000/api/v1/job/abc-123-xyz
```

**Respuesta:**
```json
{
  "job_id": "abc-123-xyz",
  "status": "processing",
  "progress": 45,
  "message": "Generating video..."
}
```

#### Descargar Video

Cuando `status` sea `"completed"`:

```
GET http://localhost:8000/api/v1/download/abc-123-xyz_video.mp4
```

---

## 📋 Endpoints Disponibles

### Health Check
```
GET /health
```

### Generar Personaje
```
POST /api/v1/character/generate
```

### Generar Video
```
POST /api/v1/video/generate
```

### Generar Voz
```
POST /api/v1/voiceover/generate
```

### Ver Estado del Job
```
GET /api/v1/job/{job_id}
```

### Descargar Archivo
```
GET /api/v1/download/{filename}
```

---

## 💻 Ejemplo con Python

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Generar video
with open("references/character_face.jpg", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/v1/video/generate",
        files={"character_face": f},
        data={
            "prompt": "Professional influencer showing phone",
            "product_description": "TinyHeroes.ai app",
            "aspect_ratio": "9:16",
            "duration_seconds": 8
        }
    )

job_id = response.json()["job_id"]
print(f"Job ID: {job_id}")

# 2. Esperar a que complete
while True:
    status = requests.get(f"{BASE_URL}/api/v1/job/{job_id}").json()
    print(f"Progress: {status['progress']}%")
    
    if status["status"] == "completed":
        break
    
    time.sleep(5)

# 3. Descargar
download_url = f"{BASE_URL}{status['result_url']}"
video = requests.get(download_url)

with open("video.mp4", "wb") as f:
    f.write(video.content)

print("✅ Done!")
```

---

## 🌐 Ejemplo con JavaScript

```javascript
async function generateVideo() {
  const formData = new FormData();
  formData.append('prompt', 'Professional influencer');
  formData.append('product_description', 'TinyHeroes.ai');
  formData.append('aspect_ratio', '9:16');
  formData.append('duration_seconds', '8');
  
  const fileInput = document.getElementById('file');
  formData.append('character_face', fileInput.files[0]);
  
  const response = await fetch('http://localhost:8000/api/v1/video/generate', {
    method: 'POST',
    body: formData
  });
  
  const { job_id } = await response.json();
  
  // Poll for status
  const interval = setInterval(async () => {
    const status = await fetch(`http://localhost:8000/api/v1/job/${job_id}`)
      .then(r => r.json());
    
    console.log(`Progress: ${status.progress}%`);
    
    if (status.status === 'completed') {
      clearInterval(interval);
      window.location.href = `http://localhost:8000${status.result_url}`;
    }
  }, 5000);
}
```

---

## 📱 Ejemplo con cURL

```bash
# Generar video
curl -X POST "http://localhost:8000/api/v1/video/generate" \
  -F "prompt=Professional influencer" \
  -F "product_description=TinyHeroes.ai" \
  -F "character_face=@references/character_face.jpg" \
  -F "aspect_ratio=9:16" \
  -F "duration_seconds=8"

# Ver estado
curl "http://localhost:8000/api/v1/job/abc-123-xyz"

# Descargar
curl -O "http://localhost:8000/api/v1/download/abc-123-xyz_video.mp4"
```

---

## 🎨 Prompts Profesionales

### 📸 Character Generation Prompts

#### Influencer Femenina Profesional
```json
{
  "description": "Professional female influencer in her late 20s. Warm, engaging smile with direct eye contact. Sleek dark blonde hair pulled back with loose strands framing face. Natural makeup emphasizing hazel eyes. White knitted sweater, minimalist gold necklace. Confident, approachable demeanor. Studio lighting with soft shadows. 4K quality, photorealistic."
}
```

#### Influencer Masculino Tech
```json
{
  "description": "Professional male tech influencer in early 30s. Confident expression, looking at camera. Short modern haircut, well-groomed beard. Casual button-down shirt, modern glasses. Approachable and knowledgeable demeanor. Clean studio background. Professional lighting. 4K quality, photorealistic."
}
```

#### Influencer Fitness
```json
{
  "description": "Athletic fitness influencer in mid 20s. Energetic and motivating expression. Sporty attire - fitted athletic wear. Toned physique, confident posture. Bright, encouraging smile. Modern gym or outdoor setting. Dynamic lighting. 4K quality, photorealistic."
}
```

#### Influencer Beauty/Lifestyle
```json
{
  "description": "Elegant lifestyle influencer in late 20s. Sophisticated and polished appearance. Flawless makeup, styled hair. Designer casual wear - neutral tones. Warm, inviting smile. Luxurious modern interior background. Soft, flattering lighting. 4K quality, photorealistic."
}
```

---

### 🎬 Video Generation Prompts

#### Producto Tech/App (TinyHeroes.ai)
```json
{
  "prompt": "Professional female influencer looking directly at camera with warm, engaging smile. She holds smartphone in hand, naturally showing the screen to viewer with confident gesture. Subtle head movement, maintaining eye contact. Modern casual style - white sweater. Cinematic lighting with soft shadows creating depth. Smooth, natural hand movements emphasizing the phone. Professional quality, 4K, vertical format optimized for social media.",
  
  "product_description": "TinyHeroes.ai mobile app interface displayed on phone screen. Colorful gradient background (blue to teal). Large bold text: 'Turn Your Child Into a Magical Character'. Subtitle about AI photo transformation. Images of children as superheroes and princesses. Blue 'Create Magic Photos' button prominently displayed. 5-star rating with '10,000+ families' testimonial. Modern, playful UI design."
}
```

#### Producto E-commerce/Fashion
```json
{
  "prompt": "Elegant influencer presenting product with enthusiasm. She holds item delicately, rotating it to show different angles. Warm smile, making eye contact with camera. Gestures naturally while explaining features. Professional studio lighting highlighting product details. Smooth, confident movements. Modern minimalist background. Vertical format, 4K quality.",
  
  "product_description": "Premium fashion accessory - designer handbag in neutral tone. Clean lines, luxury materials visible. Brand logo subtly displayed. Elegant packaging in background. Soft lighting emphasizing texture and quality. Modern, sophisticated aesthetic."
}
```

#### Producto Health/Wellness
```json
{
  "prompt": "Health-focused influencer with energetic, motivating presence. She holds product confidently, showing it to camera with encouraging smile. Natural, authentic movements. Bright, positive energy. Clean, modern setting with natural light. Gestures emphasizing benefits. Professional quality, engaging and trustworthy demeanor. Vertical format for social media.",
  
  "product_description": "Health tracking app interface on smartphone. Clean dashboard showing fitness metrics, progress charts, and daily goals. Green and white color scheme. Modern UI with intuitive icons. Progress bars and achievement badges visible. Professional, motivating design."
}
```

#### Producto Food/Beverage
```json
{
  "prompt": "Enthusiastic food influencer with genuine excitement. She holds product at eye level, showing it to camera with delighted expression. Natural reactions, subtle taste gestures. Warm, inviting smile. Kitchen or cafe setting with soft natural lighting. Authentic, relatable movements. Professional quality, appetizing presentation. Vertical format.",
  
  "product_description": "Artisanal food product with premium packaging. Vibrant colors, fresh ingredients visible. Brand logo clearly displayed. Elegant presentation on neutral surface. Soft lighting emphasizing texture and quality. Modern, appetizing aesthetic."
}
```

#### Producto Beauty/Skincare
```json
{
  "prompt": "Beauty influencer with flawless, glowing skin. She holds skincare product delicately, showing it to camera with confident smile. Gentle, graceful hand movements. Direct eye contact, trustworthy expression. Soft, flattering lighting highlighting skin quality. Clean, modern background. Professional beauty photography style. Vertical format, 4K quality.",
  
  "product_description": "Luxury skincare product in elegant packaging. Minimalist design, premium materials. Soft pastel colors or clean white. Product texture visible (cream, serum). Sophisticated branding. Soft lighting creating elegant shadows. High-end, spa-like aesthetic."
}
```

#### Producto Gaming/Tech Gadget
```json
{
  "prompt": "Tech-savvy influencer with excited, energetic expression. She holds gadget confidently, demonstrating features with animated gestures. Engaging eye contact, enthusiastic smile. Modern, dynamic movements. LED lighting or tech-themed background. Professional quality with vibrant colors. Vertical format optimized for TikTok/Instagram.",
  
  "product_description": "Modern tech gadget with sleek design. LED indicators or screen display visible. Futuristic aesthetic, clean lines. Brand logo prominently displayed. Dark background emphasizing device lights. High-tech, cutting-edge appearance."
}
```

---

### 🎤 Voiceover Script Templates

#### Tech/App Product (English)
```json
{
  "script": "Hey everyone! I've been using this incredible app and I have to share it with you. The interface is so intuitive and user-friendly. It's completely transformed how I manage my daily routine. If you're looking for something that actually delivers results, you need to check this out. Link in bio!",
  "language": "en"
}
```

#### Tech/App Product (Spanish)
```json
{
  "script": "¡Hola a todos! He estado usando esta aplicación increíble y tengo que compartirla con ustedes. La interfaz es súper intuitiva y fácil de usar. Ha transformado completamente mi rutina diaria. Si buscan algo que realmente funcione, tienen que probar esto. ¡Link en la bio!",
  "language": "es"
}
```

#### Fashion/Lifestyle Product
```json
{
  "script": "Okay, I'm obsessed with this! The quality is absolutely amazing and it goes with everything. I've been wearing it non-stop and I keep getting compliments. It's one of those pieces that just elevates your whole look. Trust me, you need this in your life. Check it out!",
  "language": "en"
}
```

#### Health/Wellness Product
```json
{
  "script": "This has been a total game-changer for my wellness journey. I've noticed such a difference since I started using it. It's easy to incorporate into your daily routine and the results speak for themselves. If you're serious about your health goals, this is definitely worth trying. Link below!",
  "language": "en"
}
```

#### Food/Beverage Product
```json
{
  "script": "You guys, this is SO good! The flavor is incredible and it's actually made with quality ingredients. I've tried so many products but this one is different. It's become my new go-to and I think you'll love it too. Definitely give it a try!",
  "language": "en"
}
```

#### Beauty/Skincare Product
```json
{
  "script": "My skin has never looked better and it's all thanks to this. I've been using it for a few weeks now and the glow is real. It's gentle, effective, and actually does what it promises. If you want that healthy, radiant skin, you need to add this to your routine. You won't regret it!",
  "language": "en"
}
```

---

## 🎯 Parámetros Técnicos

### Video Generation

| Parámetro | Tipo | Descripción | Valores Recomendados |
|-----------|------|-------------|---------------------|
| `prompt` | string | Descripción detallada del video | Ver prompts profesionales arriba |
| `product_description` | string | Descripción del producto/contenido | Específico, visual, detallado |
| `character_face` | file | Imagen de referencia del personaje | JPG/PNG, alta calidad, 9:16 |
| `aspect_ratio` | string | Proporción del video | "9:16" (vertical), "16:9" (horizontal), "1:1" (cuadrado) |
| `duration_seconds` | int | Duración del video | 8 (máximo y recomendado) |

### Character Generation

| Parámetro | Tipo | Descripción | Valores Recomendados |
|-----------|------|-------------|---------------------|
| `description` | string | Descripción completa del personaje | Incluir: edad, expresión, ropa, iluminación, calidad |

### Voiceover Generation

| Parámetro | Tipo | Descripción | Valores Recomendados |
|-----------|------|-------------|---------------------|
| `script` | string | Texto del guión | 10-15 segundos, natural, conversacional |
| `language` | string | Código de idioma | "en", "es", "fr", "de", "it", "pt" |

---

## 💡 Tips para Mejores Resultados

### Prompts de Video
1. **Sé específico** - Describe movimientos, expresiones, iluminación
2. **Incluye calidad** - Menciona "4K", "professional", "cinematic"
3. **Formato** - Siempre especifica "vertical format" para redes sociales
4. **Movimiento** - Describe gestos naturales y contacto visual
5. **Iluminación** - Menciona tipo de luz (studio, natural, soft)

### Descripciones de Producto
1. **Visual** - Describe colores, formas, texturas
2. **Contexto** - Menciona dónde/cómo se muestra
3. **Branding** - Incluye logos, nombres visibles
4. **Estética** - Define el estilo (modern, luxury, playful)
5. **Detalles** - Menciona elementos UI, botones, texto

### Scripts de Voz
1. **Natural** - Escribe como hablas
2. **Corto** - 10-15 segundos máximo
3. **Entusiasta** - Usa lenguaje positivo y energético
4. **Call-to-action** - Termina con invitación clara
5. **Auténtico** - Evita sonar demasiado comercial

---

## 🔄 Flujo de Trabajo Completo

```
1. Generar Personaje
   POST /api/v1/character/generate
   ↓
2. Esperar (polling)
   GET /api/v1/job/{job_id}
   ↓
3. Descargar imagen
   GET /api/v1/download/{filename}
   ↓
4. Generar Video (con imagen)
   POST /api/v1/video/generate
   ↓
5. Esperar (polling)
   GET /api/v1/job/{job_id}
   ↓
6. Descargar video
   GET /api/v1/download/{filename}
```

---

## 📊 Estados del Job

| Estado | Descripción |
|--------|-------------|
| `pending` | En cola, esperando procesamiento |
| `processing` | Generando contenido |
| `completed` | Completado exitosamente |
| `failed` | Falló (ver campo `error`) |

---

## ⚡ Tips

1. **Polling**: Consulta el estado cada 5 segundos
2. **Timeout**: Videos pueden tomar 30-90 segundos
3. **Aspect Ratio**: Usa "9:16" para redes sociales
4. **Prompts**: Sé específico y descriptivo
5. **Imágenes**: Usa JPG de alta calidad

---

## 📊 Airtable Integration

La API guarda automáticamente todos los resultados en Airtable (opcional).

### Configurar Airtable

1. Ver guía completa: `AIRTABLE_SETUP.md`
2. Agregar a `.env`:
   ```bash
   AIRTABLE_API_KEY=patXXXXXXXXXXXXXXXX
   AIRTABLE_BASE_ID=appXXXXXXXXXXXXXXXX
   AIRTABLE_TABLE_NAME=AI_Influencer_Videos
   ```
3. Reiniciar servidor

### Beneficios

✅ **Historial completo** - Todos los videos generados  
✅ **Imágenes de referencia** - Guardadas automáticamente  
✅ **Metadata** - Prompts, descripciones, timestamps  
✅ **Colaboración** - Comparte con tu equipo  
✅ **Analytics** - Rastrea uso y performance  

---

## 🐛 Troubleshooting

**Error: "GEMINI_API_KEY not found"**
- Verifica que `.env` tenga tu API key

**Error: "Job not found"**
- El job_id es incorrecto o expiró

**Status: "failed"**
- Revisa el campo `error` en la respuesta
- Verifica que la imagen sea válida
- Asegúrate que el prompt no viole políticas

**Airtable not saving**
- Verifica configuración en `.env`
- Revisa logs del servidor
- La API funciona sin Airtable (opcional)

---

## 📖 Documentación Completa

- **API Usage**: Ver `API_USAGE_EXAMPLES.md`
- **API Calls**: Ver `API_CALLS_GUIDE.md`
- **Airtable Setup**: Ver `AIRTABLE_SETUP.md`

---

## 🎉 ¡Listo para Usar!

El servidor está corriendo y listo para recibir requests.

**Prueba ahora:**
1. Abre http://localhost:8000/docs
2. Haz clic en "POST /api/v1/video/generate"
3. Haz clic en "Try it out"
4. Llena los parámetros
5. Haz clic en "Execute"
6. Revisa Airtable para ver el resultado guardado

¡Disfruta generando videos de influencers AI! 🚀
