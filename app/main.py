from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from contextlib import asynccontextmanager

version = 'v1'

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting ....")
    Base.metadata.create_all(bind=engine)
    yield
    print("Server has been stopped ....")

app = FastAPI(
    title= " User Management",
    description= "A simple user-management api with jwt, oauth",
    version= version,
    lifespan=life_span
)

app.include_router(auth_router)
app.include_router(users_router, prefix=f"/api/{version}/users", tags=['users'])
