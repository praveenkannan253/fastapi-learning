from fastapi import APIRouter
from app.schemas.user import UserCreate,UserResponse
from app.core.security import hash_password
from app.core.dependencies import get_db

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse)
def register_user(user:UserCreate):

    hashed_password=hash_password(user.password)

    #Temperory Implementation,# Later, we'll save hashed_password in PostgreSQL
    
    return{
        "id":1,
        "username":user.username,
        "email":user.email
    }