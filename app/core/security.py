from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)

SECRET_KEY = '4989c9086d02c7847cff35e2c1943c4346310ff8ee950a91b826249b36a7cc2e'
ALGORITHM = 'HS256'

def create_access_token(id: int, email: str):
    
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "sub" : str(id),
        "email" : email,
        "exp" : expires
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token