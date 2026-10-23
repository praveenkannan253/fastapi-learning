from fastapi import FastAPI
from my_genai_package.routers import chat
from my_genai_package.config import settings

app=FastAPI(title=settings.app_name,version="1.0.0")

app.include_router(chat.router)