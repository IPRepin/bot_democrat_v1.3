from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest

from data.db_connect import get_session
from data.stock_request import get_stock
from keyboards.user_keyboards.main_user_keyboards import not_entries_keyboard
from keyboards.admin_keyboards.inline_kb_stocks import StocksInline
from utils.logger_settings import logger

router_stocks = Router()


@router_stocks.callback_query(StocksInline.filter())
async def show_description(callback_query: types.CallbackQuery,
                           callback_data: StocksInline
                           ) -> None:
    """
    Обработчик кнопок акции
    """
    stock_id = int(callback_data.action)
    try:
        async for session in get_session():
            stock = await get_stock(session=session, id=stock_id)
            logger.info(f"stock: {stock}")
            await callback_query.message.answer_photo(
                photo=stock.image,
                caption=stock.description,
                reply_markup=not_entries_keyboard
            )
        await callback_query.answer()
    except TelegramBadRequest as e:
        logger.error(e)
        await callback_query.message.edit_text("Описание отсутствует")
        await callback_query.answer()
