import uuid
from sqlalchemy.orm import Session
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest
from app.models.book_model import Book
from sqlalchemy import select, insert, update, delete

class BookService:
    
    def get_all_books(self, db: Session):
        stmt = select(Book).order_by(Book.created_at.desc())
        result = db.execute(stmt)
        return result.scalars().all()
    
    def get_book_by_id(self, book_id: uuid.UUID, db: Session):
        result = db.execute(select(Book).where(Book.uid == book_id))
        return result.scalar_one_or_none()
    
    def create_book(self, book_data: BookCreateRequest, db: Session):
        new_book = Book(**book_data.model_dump())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
        
    
    def update_book(self, book_id: uuid.UUID, book_data: BookUpdateRequest, db: Session):
        book = self.get_book_by_id(book_id, db)
        if not book:
            return False
        book_update = book_data.model_dump(exclude_unset=True)
        for key, value in book_update.items():
            setattr(book, key, value)
            
        db.commit()
        db.refresh(book)
        return book
    
    def delete_book(self, book_id: uuid.UUID, db: Session):
        book = self.get_book_by_id(book_id, db)
        if not book:
            return False
        
        db.delete(book)
        db.commit()
        return True
    
    
        