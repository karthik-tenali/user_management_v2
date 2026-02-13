from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
) 

async def init_db():
    async with engine.begin() as connection:
        statement = text("SELECT 1;")
        result = await connection.execute(statement)
        print(result.all())