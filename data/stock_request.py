import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from data.models import Stock
from utils.logger_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_stock(session: AsyncSession, name: str, description: str = None, price: str = None, image: str = None) -> Optional[Stock]:
    stock = await session.scalar(select(Stock).where(Stock.name == name))
    try:
        if not stock:
            stock = Stock(name=name, description=description, price=price, image=image)
            session.add(stock)
            await session.commit()
            logger.info("Товар %s добавлен", name)
            return stock
        else:
            logger.info("Товар %s уже существует", name)
    except Exception as ex:
        logger.error("Ошибка при добавлении товара %s: %s", name, ex)


async def select_all_stocks(session: AsyncSession) -> Optional[List[Stock]]:
    stocks = await session.scalars(select(Stock))
    logger.info("Все товары загружены")
    return stocks.all()


async def stock_filter(session: AsyncSession, **kwargs) -> Optional[List[Stock]]:
    stocks = await session.scalars(select(Stock).filter_by(**kwargs))
    return stocks.all()


async def delete_stocks(session: AsyncSession):
    await session.delete(Stock)
    logger.info("Акции удалены")
    await session.commit()



async def update_stock(session: AsyncSession, stock_id: int, **kwargs) -> Optional[Stock]:
    stock = await session.scalar(select(Stock).where(Stock.id == stock_id))
    if stock:
        for key, value in kwargs.items():
            setattr(stock, key, value)
        await session.commit()
        logger.info("Товар %s обновлен", stock_id)
        return stock
    else:
        logger.info("Товар %s не найден", stock_id)
        return None


async def get_stock(session: AsyncSession, **kwargs) -> Optional[Stock]:
    stock = await session.scalar(select(Stock).filter_by(**kwargs))
    if not stock:
        logger.info("Товар %s не найден", kwargs.get("name"))
    return stock
