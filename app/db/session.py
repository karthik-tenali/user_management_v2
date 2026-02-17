from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True
    )

session_local = sessionmaker(
    autoflush= False, 
    autocommit= False,
    bind=engine
)

class Base(DeclarativeBase):
    pass


def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()