from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.book import router as book_router
from app.api.auth import router as auth_router
from app.db.session import engine, Base

version = 'v1'

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting ....")
    # Base.metadata.create_all(bind=engine)
    yield
    print("Server has been stopped ....")
    
    
app = FastAPI(
    title= 'fastapi beyond crud',
    description= 'learning advanced fastapi',
    version= version,
    lifespan= life_span
)

app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])
app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])