from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings

password_hash=PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain:str,hashed:str)-> bool:
    return password_hash.verify(plain,hashed)

ALGORITHM="HS256"
ACCESS_TOKEM_EXPIRE_MINUTES=30

def create_access_token(user_id:str)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEM_EXPIRE_MINUTES)
    payload={
        "sub":user_id,
        "exp":expire
    }
    encoded_jwt=jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt