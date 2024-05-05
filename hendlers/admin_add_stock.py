import logging
import sqlite3

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from data.sqlite_db_stocks import DatabaseStocks
from filters.admin_filter import AdminsFilter, admins_filter
from keyboards.replay import admin_stocks_keyboard, admin_main_keyboard
from utils.states import StatesAddStocks

load_dotenv()
admin_stocks_router = Router()
db_stocks = DatabaseStocks()
logger = logging.getLogger(__name__)


@admin_stocks_router.message(F.text == "Удалить все акции",
                             AdminsFilter(admins_filter()))
async def admin_delete_stock(message: types.Message):
    db_stocks.delete_stocks()
    await message.answer("Акции удалены", reply_markup=admin_stocks_keyboard)


@admin_stocks_router.message(F.text == "◀️назад")
async def back_main_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=admin_main_keyboard)


@admin_stocks_router.message(F.text == "Добавить акцию")
async def admin_add_stock(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesAddStocks.NAME)
    await message.answer("Добавьте название акции")


@admin_stocks_router.message(StatesAddStocks.NAME)
async def admin_add_stock_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_name=message.text)
    await message.answer("Добавьте описание акции")
    await state.set_state(StatesAddStocks.DESCRIPTION)


@admin_stocks_router.message(StatesAddStocks.DESCRIPTION)
async def admin_add_stock_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_description=message.text)
    await message.answer("Добавьте изображение к акции")
    await state.set_state(StatesAddStocks.IMAGE)


@admin_stocks_router.message(StatesAddStocks.IMAGE, F.photo)
async def admin_add_stock_image(message: types.Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(stock_image=file_id)
    await message.answer("Добавьте цену акции")
    await state.set_state(StatesAddStocks.PRICE)


@admin_stocks_router.message(StatesAddStocks.PRICE)
async def admin_add_stock_price(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_price=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        db_stocks.add_stock(
            name=data.get("stock_name"),
            description=data.get("stock_description"),
            price=data.get("stock_price"),
            image=data.get("stock_image"),
        )
        await message.answer("Акция добавлена, можно добавить еще акции", reply_markup=admin_stocks_keyboard)
    except sqlite3.IntegrityError as error:
        logger.error(error)
