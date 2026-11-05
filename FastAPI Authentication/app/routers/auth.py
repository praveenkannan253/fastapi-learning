from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserResponse,UserLogin
from app.core.security import hash_password,verify_password
from app.core.dependencies import get_db
from app.models.user import User
from sqlalchemy.exc import IntegrityError

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse)
def register_user(user:UserCreate,db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(
        User.username==user.username
    ).first()

    existing_mail=db.query(User).filter(
        User.email==user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    
    if existing_mail:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    hashed_password=hash_password(user.password)
    
    new_user=User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or Email already exists!!"
        )

    return new_user

@router.post("/login")
def login(credentials:UserLogin,db:Session=Depends(get_db)):

    user=db.query(User).filter(
       User.email==credentials.email
    ).first()

    if not user or not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return{
        "message":"Login Successful",
        "username":user.username
    }