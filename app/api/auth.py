from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.schema.auth_schema import UserRequest, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import UserService
from app.core.exceptions import EmailAlreadyExistsError, UsernameALreadyExistsError

router = APIRouter()

user_service = UserService()
db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post("/signup", response_model=UserResponse)
async def create_new_user(form_data: UserRequest, db: db_dependency):
    
    try:
        return await user_service.create_new_user(form_data, db)
    
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
        
    except UsernameALreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
        
@router.post("/login")
async def login_user(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = await user_service.authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    token = create_access_token(user.uid, user.email)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    