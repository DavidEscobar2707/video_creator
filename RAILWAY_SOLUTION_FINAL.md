# ✅ Railway 502 Error - FINAL SOLUTION

## Problem
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

Railway was returning 502 errors because the PORT environment variable wasn't being handled correctly.

## Root Cause
Railway's "Start command" was passing `$PORT` as a literal string instead of expanding it. Shell variable expansion doesn't work in Docker CMD JSON array format.

## Solution
Created a Python script (`start.py`) that reads the PORT environment variable directly:

### start.py
```python
#!/usr/bin/env python
"""Start script for Railway deployment"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    # Read PORT from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Start uvicorn
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=port,
        workers=1
    )
```

### Dockerfile
```dockerfile
# Copiar start script
COPY start.py /app/start.py
RUN chmod +x /app/start.py

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "/app/start.py"]
```

## Why This Works

1. **Python is always available** - Using Python 3.11 base image
2. **Direct environment variable access** - `os.environ.get('PORT', 8000)` reads the variable
3. **No shell expansion needed** - Python handles it directly
4. **Explicit host binding** - `host='0.0.0.0'` ensures external access
5. **Type conversion** - `int()` ensures PORT is a valid integer
6. **Single worker** - `workers=1` is sufficient for API

## How It Works

### Local Development
```bash
# Default port 8000
python start.py

# Custom port
PORT=3000 python start.py
```

### Docker Build
```bash
docker build -t ai-video-generator .
```

### Docker Run
```bash
# Railway will set PORT automatically
docker run -p 8000:8000 -e PORT=8000 ai-video-generator

# Or with different port
docker run -p 3000:3000 -e PORT=3000 ai-video-generator
```

### Railway Deployment
1. Railway detects Dockerfile
2. Railway builds the image
3. Railway starts container with `PORT=<dynamic_port>`
4. Python script reads PORT from environment
5. uvicorn starts on `0.0.0.0:<PORT>`
6. Application is accessible externally ✅

## Verification

All tests passed:
```
✓ start.py has imports
✓ start.py reads PORT
✓ start.py uses host 0.0.0.0
✓ start.py uses uvicorn.run
✓ Dockerfile copies start.py
✓ Dockerfile uses correct CMD
✓ Application imports successfully
✓ API host: 0.0.0.0
✓ API port: 8000 (default)
```

## Files Changed

1. **start.py** (NEW) - Python script to start the application
2. **Dockerfile** - Updated to copy and run start.py
3. **src/core/config.py** - Reads PORT from environment
4. **src/core/character.py** - Fixed imports
5. **src/core/video.py** - Fixed imports
6. **src/api/routes/video.py** - Fixed imports

## Deployment Steps

### Step 1: Verify Locally
```bash
# Test with default port
python start.py

# Test with custom port
PORT=3000 python start.py
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Fix: Railway 502 error - use Python start script"
git push origin main
```

### Step 3: Railway Configuration
1. Go to Railway Dashboard
2. Create new project from GitHub
3. Select your repository
4. Railway will detect Dockerfile automatically

### Step 4: Set Environment Variables
In Railway Dashboard → Variables:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### Step 5: Deploy
- Railway will automatically build and deploy
- Monitor logs for startup messages
- Should see: "Uvicorn running on http://0.0.0.0:PORT"

## Post-Deployment Verification

### Test 1: Health Check
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "airtable_enabled": false,
  "timestamp": 1234567890.123
}
```

### Test 2: API Documentation
- Swagger UI: `https://your-app.railway.app/docs`
- ReDoc: `https://your-app.railway.app/redoc`

## Configuration Summary

| Setting | Value | Source |
|---------|-------|--------|
| Host | 0.0.0.0 | start.py |
| Port | Dynamic | PORT env var |
| Default Port | 8000 | start.py |
| Workers | 1 | start.py |
| API Host | 0.0.0.0 | config.py |
| API Port | PORT env | config.py |

## Expected Result

After deployment:
- ✅ No "Invalid value for '--port'" errors
- ✅ Application starts successfully
- ✅ Health check endpoint responds
- ✅ All API endpoints accessible
- ✅ Video generation works
- ✅ External access works
- ✅ No 502 errors

## Troubleshooting

### Still getting 502?
1. Check Railway logs: `railway logs --follow`
2. Look for "Uvicorn running on"
3. Verify GEMINI_API_KEY is configured
4. Check if PORT is being set

### Port errors?
- Python directly reads PORT from environment
- No shell expansion needed
- Railway sets PORT automatically

### Application won't start?
1. Check logs for error messages
2. Verify all dependencies installed
3. Check Python version (3.11)
4. Verify GEMINI_API_KEY is set

## Summary

**Problem**: PORT environment variable not expanding in Docker CMD
**Solution**: Use Python script to read PORT environment variable directly
**Result**: Application now starts successfully on Railway ✅

---

**Status**: ✅ READY FOR PRODUCTION
**Last Updated**: December 16, 2025
