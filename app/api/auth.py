from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import Annotated
from app.schemas.auth_schema import AuthRequest, RegisterRequest
from app.services.auth_service import authentic_user
from app.core.security import create_access_token
from app.core.exceptions import EmailAlreadyExistsError
from app.services.user_service import create_new_user
from app.schemas.user_schema import UserRequest


router = APIRouter(prefix='/auth', tags=['auth'])

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register")
def register_user(input: RegisterRequest, db: db_dependency):
    try:
        user_input = UserRequest(
            name=input.name,
            email=input.email,
            password=input.password,
            role="user",   
            is_active=True
        )
        
        create_new_user(db, user_input)
        return {"message": "User registered successfully"}

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exists"
        )

@router.post("/login")
def login_user(
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    
    user = authentic_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token(user.id, user.email)    
    return {
        "access_token": token,
        "token_type": "bearer"
    }