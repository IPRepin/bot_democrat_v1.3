import logging
import sqlite3

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from data.sqlite_db_stocks import DatabaseStocks
from filters.admin_filter import AdminsFilter, admins_filter
from keyboards.replay import admin_markup
from utils.states import StatesAddStocks

load_dotenv()
admin_router = Router()
db_stocks = DatabaseStocks()


@admin_router.message(F.text == "Удалить все акции",
                      AdminsFilter(admins_filter()))
async def admin_delete_stock(message: types.Message):
    db_stocks.delete_stocks()
    await message.answer("Акции удалены", reply_markup=admin_markup)


@admin_router.message(F.text == "Добавить акцию")
async def admin_add_stock(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesAddStocks.NAME)
    await message.answer("Добавьте название акции")


@admin_router.message(StatesAddStocks.NAME)
async def admin_add_stock_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_name=message.text)
    await message.answer("Добавьте описание акции")
    await state.set_state(StatesAddStocks.DESCRIPTION)


@admin_router.message(StatesAddStocks.DESCRIPTION)
async def admin_add_stock_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_description=message.text)
    await message.answer("Добавьте изображение к акции")
    await state.set_state(StatesAddStocks.IMAGE)


@admin_router.message(StatesAddStocks.IMAGE, F.photo)
async def admin_add_stock_image(message: types.Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(stock_image=file_id)
    await message.answer("Добавьте цену акции")
    await state.set_state(StatesAddStocks.PRICE)


@admin_router.message(StatesAddStocks.PRICE)
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
        await message.answer("Акция добавлена, можно добавить еще акции", reply_markup=admin_markup)
    except sqlite3.IntegrityError as error:
        logging.error(error)
