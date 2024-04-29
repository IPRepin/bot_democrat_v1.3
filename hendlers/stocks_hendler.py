import logging

from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest

from data.sqlite_db_stocks import DatabaseStocks
from keyboards.inline import not_entries_keyboard
from keyboards.inline_kb_stocks import StocksInline

router_stocks = Router()

db = DatabaseStocks()

logger = logging.getLogger(__name__)


@router_stocks.callback_query(StocksInline.filter())
async def show_description(callback_query: types.CallbackQuery,
                           callback_data: StocksInline
                           ) -> None:
    """
    Обработчик кнопок акции
    """
    stock_id = int(callback_data.action)
    stock = db.select_stock(id=stock_id)
    logger.info(f"stock: {stock}")
    try:
        await callback_query.message.edit_text(stock[2], reply_markup=not_entries_keyboard)
        await callback_query.answer()
    except TelegramBadRequest as e:
        logging.error(e)
        await callback_query.message.edit_text("Описание отсутствует")
        await callback_query.answer()
