from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth,healthy

app=FastAPI(
    title=settings.APP_NAME,
    description="A secure multi-user chat backend built with FastAPI",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(healthy.router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "running",
        "debug" :settings.DEBUG
    }
