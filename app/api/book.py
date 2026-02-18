from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user_model import User
from app.services.book_service import BookService
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest, BookResponse, PaginatedBooks

router = APIRouter(dependencies=[Depends(get_current_user)])
service = BookService()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/", response_model=PaginatedBooks)
def fetch_all_books(
    db: db_dependency, 
    user: user_dependency,
    page: int = Query(1,ge=1),
    size: int = Query(2, ge=1, le=100)
):
    return service.get_all_books(user, db, page, size)

@router.get("/{book_id}", response_model=BookResponse)
def fetch_book_by_id(book_id: uuid.UUID, db: db_dependency, user: user_dependency):
    book = service.get_book_by_id(book_id, db, user)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return book

@router.post("/", response_model=BookResponse)
def create_new_book(book_data: BookCreateRequest, db: db_dependency, user: user_dependency):
    new_book = service.create_book(book_data, db, user.uid)
    return new_book

@router.put("/{book_id}",response_model=BookResponse)
def update_book(book_id: uuid.UUID, book_data:BookUpdateRequest, db: db_dependency, user: user_dependency):
    exist = service.update_book(book_id, book_data, db, user)
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return exist

@router.delete("/{book_id}")
def delete_book(book_id: uuid.UUID, db: db_dependency, user: user_dependency):
    book = service.delete_book(book_id, db, user)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    return {'message': 'Book successfully deleted'}