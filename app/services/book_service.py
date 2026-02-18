import uuid
from sqlalchemy.orm import Session
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest
from app.models.book_model import Book
from sqlalchemy import func, select

class BookService:
    
    def get_all_books(self, user, db: Session, page: int, size: int):

        base_query = select(Book)

        if user.role != "admin":
            base_query = base_query.where(Book.owner_id == user.uid)

        # total count
        count_query = select(func.count()).select_from(base_query.subquery())
        total = db.execute(count_query).scalar()

        # pagination
        stmt = base_query.order_by(Book.created_at.desc()) \
                        .offset((page - 1) * size) \
                        .limit(size)

        items = db.execute(stmt).scalars().all()

        pages = (total + size - 1) // size # type: ignore

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    
    def get_book_by_id(self, book_id: uuid.UUID, db: Session, user):
        if user.role == 'admin':
            stmt = db.execute(select(Book).where(Book.id == book_id))
        else:
            stmt = select(Book).where(
                Book.id == book_id,
                Book.owner_id == user.uid
            )
        result = db.execute(stmt) # type: ignore
        return result.scalar_one_or_none()
    
    def create_book(self, book_data: BookCreateRequest, db: Session, owner_id):
        new_book = Book(**book_data.model_dump(), owner_id=owner_id)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
        
    def update_book(self, book_id: uuid.UUID, book_data: BookUpdateRequest, db: Session, user):
        book = self.get_book_by_id(book_id, db, user)
        if not book:
            return None
        book_update = book_data.model_dump(exclude_unset=True)
        for key, value in book_update.items():
            setattr(book, key, value)
            
        db.commit()
        db.refresh(book)
        return book
    
    def delete_book(self, book_id: uuid.UUID, db: Session, user):
        book = self.get_book_by_id(book_id, db, user)
        if not book:
            return None
        
        db.delete(book)
        db.commit()
        return True
    
    
        