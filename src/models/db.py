from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import (
    SQL_ENGINE,
    SQL_USER,
    SQL_PASSWORD,
    SQL_HOST,
    SQL_PORT,
    SQL_DATABASE
)


SQLALCHEMY_DATABASE_URI = f'{SQL_ENGINE}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base: DeclarativeMeta = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session