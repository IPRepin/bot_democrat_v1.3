from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from data.db_connect import get_session
from data.stock_request import select_all_stocks


class StocksInline(CallbackData, prefix="show_stocks"):
    action: str


class EditStocksInline(CallbackData, prefix="edit_stocks"):
    action: str


async def choosing_promotion_keyboards():
    menu = InlineKeyboardBuilder()
    async for session in get_session():
        stocks = await select_all_stocks(session=session)
        for i in range(len(stocks)):
            button_text = f"{stocks[i].name}"
            id_stock = str(stocks[i].id)
            callback_data = StocksInline(action=id_stock).pack()
            menu.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
    return menu.as_markup()



async def edit_promotion_keyboards():
    menu = InlineKeyboardBuilder()
    async for session in get_session():
        stocks = await select_all_stocks(session=session)
        for i in range(len(stocks)):
            button_text = f"{stocks[i].name}"
            id_stock = str(stocks[i].id)
            callback_data = EditStocksInline(action=id_stock).pack()
            menu.row(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
    return menu.as_markup()
