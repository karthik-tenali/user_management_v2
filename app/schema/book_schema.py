from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import date, datetime


class BookCreateRequest(BaseModel):
    
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    
class BookUpdateRequest(BaseModel):
    
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = None
    

class BookResponse(BaseModel):
    
    uid: uuid.UUID
    title: str
    author: str
    publisher: str | None
    published_date: date | None
    page_count: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True