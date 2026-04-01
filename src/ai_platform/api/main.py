from fastapi import FastAPI
from ai_platform.api.router import v1
import os
from ai_platform.config import get_settings

settings = get_settings()

os.environ["ANTHROPIC_API_KEY"] = settings.anthropic.api_key
os.environ["GEMINI_API_KEY"] = settings.gemini.api_key
os.environ["OPENAI_API_KEY"] = settings.chatgpt.api_key


app = FastAPI()

app.include_router(v1.router)

@app.get("/")
async def home():
    return {"message": "Welcome to the API!"}