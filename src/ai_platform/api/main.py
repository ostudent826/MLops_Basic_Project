"""
Main entry point for the AI Platform FastAPI application.
Handles the initialization of the app and includes versioned routers.
"""

from fastapi import FastAPI
from ai_platform.api.router import v1
import os
from ai_platform.config import get_settings

# Load configuration settings
settings = get_settings()

# Initialize the FastAPI app
app = FastAPI(title="MLOps AI Platform")

# Register the v1 router (handles /chat and /query)
app.include_router(v1.router)


@app.get("/")
async def home():
    """
    Root endpoint to verify the API is online.
    """
    return {"message": "Welcome to the API!"}
