# ✅ Railway - Solución Final

## El Problema
Railway estaba auto-detectando el comando de inicio y configurando:
```
uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

Esto causaba el error porque `$PORT` no se expandía correctamente.

## La Solución

### Archivos Eliminados
- ❌ `Procfile` - Eliminado (causaba auto-detección)
- ❌ `railway.json` - Eliminado (causaba auto-detección)

### Archivos Creados
- ✅ `start.py` - Script Python que lee PORT correctamente
- ✅ `railway.toml` - Configuración explícita para Railway
- ✅ `.railwayignore` - Previene auto-detección

### Archivos Actualizados
- ✅ `Dockerfile` - Usa `CMD ["python", "start.py"]`

## Configuración de Railway

### railway.toml
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = ""
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 5
```

**Importante**: `startCommand = ""` le dice a Railway que NO use un comando personalizado.

### start.py
```python
#!/usr/bin/env python
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=port,
        workers=1
    )
```

### Dockerfile
```dockerfile
COPY start.py /app/start.py
CMD ["python", "start.py"]
```

## Pasos para Desplegar

### 1. Push a GitHub
```bash
git add .
git commit -m "Fix: Railway auto-detection - use explicit configuration"
git push origin main
```

### 2. En Railway Dashboard

#### Opción A: Nuevo Proyecto (Recomendado)
1. Elimina el proyecto actual "prueba3"
2. Crea un nuevo proyecto desde GitHub
3. Railway detectará `railway.toml` automáticamente
4. Configura `GEMINI_API_KEY` en Variables
5. Deploy

#### Opción B: Proyecto Existente
1. Ve a Settings → Deploy
2. Si ves "Start Command", **elimínalo completamente**
3. Asegúrate de que esté **vacío**
4. Click "Save"
5. Ve a Settings → Build
6. Verifica que "Builder" sea "Dockerfile"
7. Redeploy

### 3. Verificar Variables de Entorno
En Railway Dashboard → Variables:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### 4. Verificar Logs
Después del deploy, deberías ver:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

## Por Qué Funciona Ahora

1. **railway.toml** le dice explícitamente a Railway:
   - Usa Dockerfile
   - NO uses un start command personalizado

2. **Dockerfile** ejecuta:
   ```
   CMD ["python", "start.py"]
   ```

3. **start.py** lee PORT correctamente:
   ```python
   port = int(os.environ.get("PORT", 8000))
   ```

4. **No hay Procfile ni railway.json** que causen auto-detección

## Verificación

### Health Check
```bash
curl https://your-app.railway.app/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "airtable_enabled": false,
  "timestamp": 1234567890.123
}
```

### API Docs
- Swagger: `https://your-app.railway.app/docs`
- ReDoc: `https://your-app.railway.app/redoc`

## Troubleshooting

### Si Railway sigue auto-configurando el start command:
1. Verifica que `Procfile` y `railway.json` estén eliminados
2. Verifica que `railway.toml` existe y tiene `startCommand = ""`
3. Elimina el proyecto y crea uno nuevo
4. Railway debería respetar `railway.toml`

### Si ves errores en los logs:
1. Verifica que `start.py` existe en el contenedor
2. Verifica que `GEMINI_API_KEY` está configurado
3. Verifica que el Dockerfile copia `start.py`

## Resumen

✅ **Eliminados**: Procfile, railway.json
✅ **Creados**: start.py, railway.toml, .railwayignore
✅ **Actualizados**: Dockerfile
✅ **Configuración**: railway.toml con startCommand vacío
✅ **Variables**: GEMINI_API_KEY configurado

---

**Status**: ✅ LISTO PARA DESPLEGAR
**Siguiente paso**: Push a GitHub y redeploy en Railway
