#!/bin/bash
# Entrypoint script for Railway deployment
# Handles PORT environment variable properly

PORT=${PORT:-8000}
exec uvicorn src.api:app --host 0.0.0.0 --port $PORT
