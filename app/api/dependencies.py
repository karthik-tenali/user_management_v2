from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from sqlalchemy import select
from app.models.user_model import User


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

db_dependency = Annotated[Session, Depends(get_db)]

def get_current_user( db: db_dependency, token: str = Depends(oauth_scheme)):
    

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    uid = payload.get('sub')
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    result = db.execute(select(User).where(User.uid == uid))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user