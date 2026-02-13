from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from typing import Annotated
from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.models.user_model import User
from app.schemas.user_schema import UserRequest, UserResponse, UserUpdateRequest
from app.services.user_service import get_users, get_user_by_id, create_new_user, update_existing_user, delete_existing_user


router = APIRouter(dependencies=[Depends(get_current_user)])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/",response_model=list[UserResponse])
def fetch_all_users(db: db_dependency):
    users = get_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def fetch_user_by_id(user_id: int, db: db_dependency):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with ID not found"
        )
    
    return user

@router.post("/", response_model=UserResponse)
def add_new_user(input: UserRequest, db: db_dependency, current_user: user_dependency):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add new user"
        )
    
    try:
        return create_new_user(db, input)
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exists"
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    input: UserUpdateRequest,
    db: db_dependency,
    current_user: user_dependency
):
    
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    if input.role is not None and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can change role"
        )

    try:
        return update_existing_user(db, input, user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

@router.delete("/{user_id}")
def delete_user(user_id: int, db: db_dependency, current_user: user_dependency):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete the user"
        )
    
    success = delete_existing_user(db, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with ID not found"
        )
        
    return {"message": "User deleted successfully"}