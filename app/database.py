from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass