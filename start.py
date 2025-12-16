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
