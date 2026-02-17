from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.settings import settings

# Base class for all models
class Base(DeclarativeBase):
    pass

# Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False
) 

# Session Maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit= False,
)

# FastAPI Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

# async def init_db():
#     from app.models.book_model import Book
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)