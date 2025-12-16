# 🚨 IMPORTANTE: Configuración de Railway

## El Problema
Railway está usando un "Start command" personalizado que tiene `$PORT` como literal:
```
uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

Esto causa el error:
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

## La Solución

### Paso 1: Eliminar el "Start command" de Railway

1. Ve a tu proyecto en Railway Dashboard
2. Click en tu servicio
3. Ve a la pestaña "Settings"
4. Busca la sección "Deploy"
5. Encuentra "Start Command"
6. **ELIMINA** el comando que dice: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
7. Deja el campo **VACÍO**
8. Click en "Save"

### Paso 2: Redeploy

1. Ve a la pestaña "Deployments"
2. Click en "Redeploy" o haz un nuevo push a GitHub

## Por Qué Esto Funciona

Cuando eliminas el "Start command", Railway usará el `CMD` del Dockerfile:
```dockerfile
CMD ["python", "start.py"]
```

El script `start.py` lee la variable de entorno `PORT` correctamente:
```python
port = int(os.environ.get("PORT", 8000))
uvicorn.run("src.api:app", host="0.0.0.0", port=port, workers=1)
```

## Verificación

Después de eliminar el "Start command" y redeploy, deberías ver en los logs:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

## Configuración Correcta de Railway

### Build
- **Builder**: Dockerfile
- **Dockerfile path**: /Dockerfile

### Deploy
- **Start Command**: (VACÍO - dejar en blanco)
- **Region**: us-east4-eqdc4a (o tu región preferida)
- **Number of replicas**: 1
- **Restart policy**: on failure
- **Restart policy max retries**: 5

### Variables
```
GEMINI_API_KEY=your-gemini-api-key-here
```

## Troubleshooting

### Si todavía ves el error
1. Verifica que el "Start command" esté **completamente vacío**
2. Haz un redeploy completo
3. Verifica los logs para ver qué comando se está ejecutando

### Si el "Start command" se llena automáticamente
1. Elimínalo de nuevo
2. Asegúrate de hacer click en "Save"
3. Railway debería usar el CMD del Dockerfile

## Resumen

✅ **Elimina el "Start command" de Railway**
✅ **Deja el campo vacío**
✅ **Railway usará el CMD del Dockerfile**
✅ **start.py manejará el PORT correctamente**

---

**Siguiente paso**: Elimina el "Start command" en Railway y redeploy
