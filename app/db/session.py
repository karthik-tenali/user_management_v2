from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = "sqlite:///./user_management.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})



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