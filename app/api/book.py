from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.services.book_service import BookService
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest, BookResponse

router = APIRouter(dependencies=[Depends(get_current_user)])
service = BookService()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=list[BookResponse])
def fetch_all_books(db: db_dependency):
    return service.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def fetch_book_by_id(book_id: uuid.UUID, db: db_dependency):
    book = service.get_book_by_id(book_id, db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return book

@router.post("/", response_model=BookResponse)
def create_new_book(book_data: BookCreateRequest, db: db_dependency):
    new_book = service.create_book(book_data, db)
    return new_book

@router.put("/{book_id}",response_model=BookResponse)
def update_book(book_id: uuid.UUID, book_data:BookUpdateRequest, db: db_dependency):
    exist = service.update_book(book_id, book_data, db)
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return exist

@router.delete("/{book_id}")
def delete_book(book_id: uuid.UUID, db: db_dependency):
    book = service.delete_book(book_id, db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return {'message': 'Book successfully deleted'}