from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def check():
    return {
        "status": "healthy",
        "service": "Secure AI Chat Backend"
    }