# 🚂 Railway Deployment Guide

## Configuración Inicial

### 1. Conectar Repositorio

1. Ve a [Railway](https://railway.app)
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway y selecciona tu repositorio

### 2. Configurar Variables de Entorno

En el dashboard de Railway, ve a "Variables" y agrega:

```
GEMINI_API_KEY=tu-api-key-aqui
```

Opcional (para Airtable):
```
AIRTABLE_API_KEY=tu-airtable-key
AIRTABLE_BASE_ID=tu-base-id
AIRTABLE_TABLE_NAME=AI_Influencer_Videos
```

### 3. Configurar Build

Railway detectará automáticamente el `Dockerfile` y lo usará para el build.

Si necesitas configurar manualmente:
- Build Command: (vacío, usa Dockerfile)
- Start Command: `./start.sh`

## Verificación

### 1. Ver Logs

```bash
# En el dashboard de Railway
Click en "View Logs"
```

Deberías ver:
```
✅ FFmpeg instalado: ffmpeg version 4.x.x
✅ GEMINI_API_KEY configurada
🚀 Iniciando servidor...
```

### 2. Probar el Endpoint

```bash
curl https://tu-app.railway.app/health
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

## Troubleshooting

### Error: "ImportError: cannot import name 'genai'"

**Solución:**
1. Verifica que `requirements.txt` tenga las versiones correctas
2. Fuerza un rebuild:
   - Settings → Redeploy

### Error: "FFmpeg not found"

**Solución:**
El Dockerfile ya incluye FFmpeg. Si ves este error:
1. Verifica que Railway esté usando el Dockerfile
2. Settings → Build → Dockerfile Path: `Dockerfile`

### Error: "Port already in use"

**Solución:**
Railway asigna automáticamente el puerto. El script `start.sh` lo maneja.

### Error: "GEMINI_API_KEY not found"

**Solución:**
1. Ve a Variables en Railway
2. Agrega `GEMINI_API_KEY` con tu API key
3. Redeploy

## Monitoreo

### Ver Métricas

En el dashboard de Railway:
- CPU Usage
- Memory Usage
- Network Traffic

### Logs en Tiempo Real

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Ver logs
railway logs
```

## Escalamiento

### Aumentar Recursos

1. Settings → Resources
2. Ajusta:
   - Memory: 512MB - 8GB
   - CPU: 0.5 - 8 vCPUs

### Múltiples Instancias

Railway soporta escalamiento horizontal automático.

## Costos

Railway ofrece:
- $5 de crédito gratis mensual
- Pay-as-you-go después

Estimado para este proyecto:
- ~$5-10/mes con uso moderado
- ~$20-30/mes con uso intensivo

## Dominio Personalizado

1. Settings → Domains
2. Click "Add Domain"
3. Configura tu DNS:
   ```
   CNAME: tu-dominio.com → tu-app.railway.app
   ```

## Backup

Railway hace backups automáticos, pero recomendamos:

1. Usar Airtable para persistencia
2. Backup manual de `/data`:
   ```bash
   railway run tar -czf backup.tar.gz data/
   ```

## CI/CD

Railway hace deploy automático en cada push a `main`.

Para desactivar:
1. Settings → Deployments
2. Desactiva "Auto Deploy"

## Comandos Útiles

```bash
# Ver status
railway status

# Ver variables
railway variables

# Ejecutar comando en Railway
railway run <comando>

# Abrir shell
railway shell

# Ver logs
railway logs --follow
```

## Soporte

- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)
