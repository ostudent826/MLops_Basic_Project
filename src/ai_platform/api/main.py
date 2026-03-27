from fastapi import FastAPI
from ai_platform.api.router import v1

app = FastAPI()

app.include_router(v1.router)

@app.get("/")
async def home():
    return {"message": "Welcome to the API!"}