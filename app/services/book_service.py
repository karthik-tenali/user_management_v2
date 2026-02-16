import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.book_schema import BookCreateRequest, BookUpdateRequest
from app.models.book_model import Book
from sqlalchemy import select, insert, update, delete

class BookService:
    
    async def get_all_books(self, db: AsyncSession):
        stmt = select(Book).order_by(Book.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_book_by_id(self, book_id: uuid.UUID, db: AsyncSession):
        result = await db.execute(select(Book).where(Book.uid == book_id))
        return result.scalar_one_or_none()
    
    async def create_book(self, book_data: BookCreateRequest, db: AsyncSession):
        new_book = Book(**book_data.model_dump())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book
        
    
    async def update_book(self, book_id: uuid.UUID, book_data: BookUpdateRequest, db: AsyncSession):
        book = await self.get_book_by_id(book_id, db)
        if not book:
            return False
        book_update = book_data.model_dump(exclude_unset=True)
        for key, value in book_update.items():
            setattr(book, key, value)
            
        await db.commit()
        await db.refresh(book)
        return book
    
    async def delete_book(self, book_id: uuid.UUID, db: AsyncSession):
        book = await self.get_book_by_id(book_id, db)
        if not book:
            return False
        
        await db.delete(book)
        await db.commit()
        return True
    
    
        