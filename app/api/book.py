from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.book_service import BookService
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest, BookResponse

router = APIRouter()
service = BookService()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/", response_model=list[BookResponse])
async def fetch_all_books(db: db_dependency):
    return await service.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
async def fetch_book_by_id(book_id: uuid.UUID, db: db_dependency):
    book = await service.get_book_by_id(book_id, db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return book

@router.post("/", response_model=BookResponse)
async def create_new_book(book_data: BookCreateRequest, db: db_dependency):
    new_book = await service.create_book(book_data, db)
    return new_book

@router.put("/{book_id}",response_model=BookResponse)
async def update_book(book_id: uuid.UUID, book_data:BookUpdateRequest, db: db_dependency):
    exist = await service.update_book(book_id, book_data, db)
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return exist

@router.delete("/{book_id}")
async def delete_book(book_id: uuid.UUID, db: db_dependency):
    book = await service.delete_book(book_id, db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return {'message': 'Book successfully deleted'}