import logging

from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, Column, DateTime
from config import settings as global_settings
from utils.logger_settings import setup_logging

logger = logging.getLogger(setup_logging())

engine = create_async_engine(
    global_settings.asyncpg_url.unicode_string(),
    future=True,
    echo=False,
)

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
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session