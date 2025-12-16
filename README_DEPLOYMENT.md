# 🚀 Railway Deployment - Complete Guide

## Status: ✅ READY FOR PRODUCTION

All issues have been resolved. Your application is ready to deploy to Railway.

---

## What Was Fixed

### Issue 1: PORT Environment Variable Not Expanding
**Problem**: Railway was returning 502 errors with `Error: Invalid value for '--port': '$PORT' is not a valid integer.`

**Root Cause**: Shell variable expansion wasn't working in Docker CMD

**Solution**: Use Python to read PORT environment variable directly

**Dockerfile CMD**:
```dockerfile
CMD ["python", "-c", "import os; import uvicorn; port = int(os.environ.get('PORT', 8000)); uvicorn.run('src.api:app', host='0.0.0.0', port=port, workers=1)"]
```

### Issue 2: Application Not Listening on 0.0.0.0
**Solution**: Explicitly set `host='0.0.0.0'` in uvicorn.run()

### Issue 3: google.generativeai Import Error
**Solution**: Changed imports to `import google.generativeai as genai`

---

## Deployment Steps

### Step 1: Verify Everything Works Locally
```bash
# Test with default port
python -c "import os; import uvicorn; port = int(os.environ.get('PORT', 8000)); uvicorn.run('src.api:app', host='0.0.0.0', port=port, workers=1)"

# Test with custom port
PORT=3000 python -c "import os; import uvicorn; port = int(os.environ.get('PORT', 8000)); uvicorn.run('src.api:app', host='0.0.0.0', port=port, workers=1)"
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Fix: Railway 502 error - use Python for PORT handling"
git push origin main
```

### Step 3: Create Railway Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the Dockerfile

### Step 4: Set Environment Variables
In Railway Dashboard → Variables:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

Optional (for Airtable):
```
AIRTABLE_API_KEY=your-airtable-key
AIRTABLE_BASE_ID=your-base-id
```

### Step 5: Deploy
- Railway will automatically build and deploy
- Monitor logs for startup messages
- Should see: "Uvicorn running on http://0.0.0.0:PORT"

---

## Verify Deployment

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

### Test 3: Character Generation
```bash
curl -X POST https://your-app.railway.app/api/v1/character/generate \
  -F "description=Professional female influencer"
```

---

## Configuration Summary

| Setting | Value | Source |
|---------|-------|--------|
| Host | 0.0.0.0 | Dockerfile CMD |
| Port | Dynamic | PORT env var |
| Default Port | 8000 | Dockerfile CMD |
| Workers | 1 | Dockerfile CMD |
| API Host | 0.0.0.0 | config.py |
| API Port | PORT env | config.py |

---

## Files Changed

1. **Dockerfile** - Updated CMD to use Python for PORT handling
2. **src/core/config.py** - Reads PORT from environment
3. **src/core/character.py** - Fixed google.generativeai import
4. **src/core/video.py** - Fixed google.generativeai import
5. **src/api/routes/video.py** - Fixed google.generativeai import

---

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

---

## Key Points

✅ **Host**: 0.0.0.0 (listens on all interfaces)
✅ **Port**: Dynamic (reads from PORT env var)
✅ **Default**: 8000 (if PORT not set)
✅ **Workers**: 1 (sufficient for API)
✅ **Imports**: All fixed
✅ **Configuration**: Correct

---

## Next Steps

1. ✅ All fixes applied
2. ✅ All checks passed
3. 📤 Push to GitHub
4. 🚀 Deploy to Railway
5. 🧪 Test endpoints
6. 📊 Monitor logs

---

**Status**: ✅ READY FOR PRODUCTION
**Last Updated**: December 16, 2025
