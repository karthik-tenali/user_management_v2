from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserRequest(BaseModel):
    
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = 'user'
    is_active: bool = True
    
    
class UserResponse(BaseModel):
    
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None