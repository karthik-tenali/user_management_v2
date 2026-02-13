from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.users import router as users_router
from app.api.auth import router as auth_router

version = 'v1'

app = FastAPI(
    title= " User Management",
    description= "A simple user-management api with jwt, oauth",
    version= version
    )
app.include_router(auth_router)
app.include_router(users_router, prefix=f"/api/{version}/users", tags=['users'])

Base.metadata.create_all(bind=engine)
