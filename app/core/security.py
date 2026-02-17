import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.core.settings import settings

password_context  = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)



def create_access_token(uid: uuid.UUID, email: str, refresh: bool = False) -> str:
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "sub": str(uid),          
        "email": email,
        "exp": expire,
        "refresh": refresh             
    }   
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_access_token(token: str):
    
    try:
        return jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None