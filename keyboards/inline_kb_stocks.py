from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from data.sqlite_db_stocks import DatabaseStocks

db = DatabaseStocks()


class StocksInline(CallbackData, prefix="show_stocks"):
    action: str


async def choosing_promotion_keyboards():
    menu = InlineKeyboardBuilder()
    stocks = db.select_all_stocks()
    for i in range(len(stocks)):
        button_text = f"{stocks[i][1]}"
        id_stock = str(stocks[i][0])
        callback_data = StocksInline(action=id_stock).pack()
        menu.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return menu.as_markup()
