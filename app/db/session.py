from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})



session_local = sessionmaker(
    autoflush= False, 
    autocommit= False,
    bind=engine
)

Base = declarative_base()

def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()