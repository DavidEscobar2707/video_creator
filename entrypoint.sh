#!/bin/bash
# Entrypoint script for Railway deployment
# Handles PORT environment variable properly
# Ensures application listens on 0.0.0.0 for external access

# Get PORT from environment or default to 8000
PORT=${PORT:-8000}

# Ensure PORT is a valid integer
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "ERROR: PORT must be a valid integer, got: $PORT"
    exit 1
fi

echo "Starting AI Influencer Video Generator API"
echo "Host: 0.0.0.0"
echo "Port: $PORT"
echo ""

# Start uvicorn with explicit host and port
# Using exec to ensure proper signal handling
exec uvicorn src.api:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1
