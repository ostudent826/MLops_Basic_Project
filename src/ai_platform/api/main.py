from fastapi import FastAPI
from ai_platform.api.router import v1
import os
from ai_platform.config import get_settings

settings = get_settings()

app = FastAPI()

app.include_router(v1.router)

@app.get("/")
async def home():
    return {"message": "Welcome to the API!"}