from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active : bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True