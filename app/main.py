from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db

version = 'v1'

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting ....")
    await init_db()
    yield
    print("Server has been stopped ....")
    
    
app = FastAPI(
    title= 'fastapi beyond crud',
    description= 'learning advanced fastapi',
    version= version,
    lifespan= life_span
)

