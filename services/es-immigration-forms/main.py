#!/usr/bin/env python3
"""
Root entry point for the FastAPI application.

Usage:
    uvicorn main:app --reload
"""

from app.api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
