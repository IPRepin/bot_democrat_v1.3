from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, Column, DateTime
from config import settings as global_settings
from utils.logger_settings import logger

engine = create_async_engine(
    global_settings.POSTGRES_URL,
    future=True,
    echo=False,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


class BaseModel(DeclarativeBase):
    metadata = MetaData()
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


async def get_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        logger.info(f"ASYNC Pool: {engine.pool.status()}")
        yield session