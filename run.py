#!/usr/bin/env python3
"""
Startup script for the Customer Registration System API.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Customer Registration System API...")
    print("API will be available at: http://localhost:8000")
    print("Swagger Documentation: http://localhost:8000/docs")
    print("ReDoc Documentation: http://localhost:8000/redoc")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 