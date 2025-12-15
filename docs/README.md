# 📚 Documentación - AI Influencer Video Generator

Bienvenido a la documentación completa del generador de videos con IA.

## 🚀 Comienza Aquí

### Para Principiantes
1. **[QUICK_START.md](QUICK_START.md)** ⭐ - Comienza en 5 minutos
2. **[POSTMAN_FRONTEND_GUIDE.md](POSTMAN_FRONTEND_GUIDE.md)** - Guía dummy paso a paso

### Para Desarrolladores
1. **[VEO3_API_GUIDE.md](VEO3_API_GUIDE.md)** - Documentación técnica completa
2. **[API_USAGE_EXAMPLES.md](API_USAGE_EXAMPLES.md)** - Ejemplos de código
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía de deployment

### Para Administradores
1. **[AIRTABLE_SETUP.md](AIRTABLE_SETUP.md)** - Configurar base de datos
2. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment en producción

---

## 📖 Guías Disponibles

### 1. QUICK_START.md
**Para:** Usuarios que quieren empezar rápido  
**Tiempo:** 5 minutos  
**Contenido:**
- Instalación rápida
- Configuración de API key
- Primeros pasos
- Troubleshooting básico

### 2. POSTMAN_FRONTEND_GUIDE.md ⭐ RECOMENDADO
**Para:** Probar API en Postman y usar en frontend  
**Tiempo:** 30 minutos  
**Contenido:**
- Guía dummy (muy fácil de entender)
- Paso a paso en Postman
- Ejemplos de código (JavaScript, React, Vue)
- HTML de prueba incluido
- Troubleshooting detallado

### 3. VEO3_API_GUIDE.md
**Para:** Entender cómo funciona Veo 3.1  
**Tiempo:** 1 hora  
**Contenido:**
- Anatomía de llamadas al API
- Parámetros detallados
- Manejo de operaciones asíncronas
- Ejemplos prácticos
- Mejores prácticas
- Troubleshooting avanzado

### 4. API_USAGE_EXAMPLES.md
**Para:** Copiar y pegar ejemplos de código  
**Tiempo:** 20 minutos  
**Contenido:**
- Ejemplos con Postman
- Ejemplos con Python
- Ejemplos con JavaScript
- Ejemplos con cURL
- Flujo completo recomendado
- Seguridad en producción

### 5. DEPLOYMENT.md
**Para:** Desplegar en producción  
**Tiempo:** 1 hora  
**Contenido:**
- Railway (recomendado)
- Docker
- Heroku
- Variables de entorno
- Monitoreo
- Troubleshooting

### 6. AIRTABLE_SETUP.md
**Para:** Configurar base de datos en Airtable  
**Tiempo:** 30 minutos  
**Contenido:**
- Crear base de datos
- Configurar campos
- Crear vistas
- Automatizaciones
- Integración con API

---

## 🎯 Rutas de Aprendizaje

### Ruta 1: Principiante (Quiero probar rápido)
```
1. QUICK_START.md (5 min)
   ↓
2. test_frontend.html (10 min)
   ↓
3. ¡Listo! Tienes videos generados
```

### Ruta 2: Desarrollador Frontend (Quiero integrar en mi app)
```
1. QUICK_START.md (5 min)
   ↓
2. POSTMAN_FRONTEND_GUIDE.md (30 min)
   ↓
3. Copiar código de ejemplos
   ↓
4. ¡Integrado en tu frontend!
```

### Ruta 3: Desarrollador Backend (Quiero entender todo)
```
1. QUICK_START.md (5 min)
   ↓
2. VEO3_API_GUIDE.md (1 hora)
   ↓
3. API_USAGE_EXAMPLES.md (20 min)
   ↓
4. DEPLOYMENT.md (1 hora)
   ↓
5. ¡Experto en la API!
```

### Ruta 4: DevOps (Quiero desplegar en producción)
```
1. QUICK_START.md (5 min)
   ↓
2. DEPLOYMENT.md (1 hora)
   ↓
3. AIRTABLE_SETUP.md (30 min)
   ↓
4. ¡En producción!
```

---

## 🔗 Archivos Adicionales

### Colección de Postman
- **postman_collection.json** - Importa en Postman para probar endpoints

### HTML de Prueba
- **test_frontend.html** - Interfaz web para probar sin código

---

## 📊 Estructura de Documentación

```
docs/
├── README.md                      ← Estás aquí
├── QUICK_START.md                 ← Comienza aquí
├── POSTMAN_FRONTEND_GUIDE.md      ← Guía dummy (recomendado)
├── VEO3_API_GUIDE.md              ← Documentación técnica
├── API_USAGE_EXAMPLES.md          ← Ejemplos de código
├── DEPLOYMENT.md                  ← Deployment
├── AIRTABLE_SETUP.md              ← Base de datos
└── postman_collection.json        ← Colección Postman
```

---

## 🎓 Conceptos Clave

### Job ID
Identificador único para cada trabajo de generación. Se usa para verificar el estado.

```
Ejemplo: abc123-def456-ghi789
```

### Status
Estado actual del trabajo:
- `pending` - En cola, esperando procesamiento
- `processing` - Generando
- `completed` - Listo para descargar
- `failed` - Error durante generación

### Progress
Porcentaje de progreso (0-100%)

### Result URL
URL para descargar el archivo generado

---

## 🚀 Endpoints Rápidos

```bash
# Verificar servidor
GET /health

# Generar personaje
POST /api/v1/character/generate

# Generar video
POST /api/v1/video/generate

# Generar voiceover
POST /api/v1/voiceover/generate

# Verificar estado
GET /api/v1/job/{job_id}

# Descargar archivo
GET /api/v1/download/{filename}
```

---

## 💡 Tips

1. **Comienza con QUICK_START.md** - Es la forma más rápida de empezar
2. **Usa test_frontend.html** - Para probar sin escribir código
3. **Importa postman_collection.json** - Para probar endpoints fácilmente
4. **Lee POSTMAN_FRONTEND_GUIDE.md** - Si quieres integrar en tu frontend
5. **Consulta VEO3_API_GUIDE.md** - Si necesitas entender detalles técnicos

---

## ❓ Preguntas Frecuentes

**P: ¿Por dónde empiezo?**  
R: Comienza con [QUICK_START.md](QUICK_START.md)

**P: ¿Cómo pruebo en Postman?**  
R: Lee [POSTMAN_FRONTEND_GUIDE.md](POSTMAN_FRONTEND_GUIDE.md)

**P: ¿Cómo integro en mi frontend?**  
R: Sigue [POSTMAN_FRONTEND_GUIDE.md](POSTMAN_FRONTEND_GUIDE.md) sección "Usar en Frontend"

**P: ¿Cómo despliego en producción?**  
R: Lee [DEPLOYMENT.md](DEPLOYMENT.md)

**P: ¿Cómo configuro Airtable?**  
R: Lee [AIRTABLE_SETUP.md](AIRTABLE_SETUP.md)

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección de Troubleshooting en la guía relevante
2. Verifica que el servidor está corriendo: `python main.py`
3. Verifica que tienes la API key configurada en `.env`
4. Revisa los logs del servidor

---

## 📝 Versión

Documentación para: **AI Influencer Video Generator v2.0**

Última actualización: Diciembre 2024

---

**¡Bienvenido! Elige una guía y comienza 🚀**
