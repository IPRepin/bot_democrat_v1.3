import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.sqlite_db_stocks import DatabaseStocks
from keyboards.admin_keyboards.inline_kb_stocks import edit_promotion_keyboards
from keyboards.replay import admin_stocks_keyboard
from utils.states import StatesEditStocks

edit_stock_router = Router()
db_stocks = DatabaseStocks()
logger = logging.getLogger(__name__)


@edit_stock_router.message(F.text == "Изменить акцию")
async def admin_edit_stock(message: types.Message, state: FSMContext):
    menu = await edit_promotion_keyboards()
    await message.answer("Выбирете акцию для изменения из списка:",
                         reply_markup=menu)
    await state.set_state(StatesEditStocks.ID)


@edit_stock_router.callback_query(StatesEditStocks.ID)
async def edit_stock_id(callback_query: types.CallbackQuery,
                        state: FSMContext,
                        ) -> None:
    await state.update_data(id=callback_query.data.split(":")[-1])
    await callback_query.answer()
    await state.set_state(StatesEditStocks.NAME)
    await callback_query.message.answer("Добавьте название акции")


@edit_stock_router.message(StatesEditStocks.NAME)
async def edit_stock_name(message: types.Message, state: FSMContext):
    await state.update_data(stock_name=message.text)
    await message.answer("Добавьте описание акции")
    await state.set_state(StatesEditStocks.DESCRIPTION)


@edit_stock_router.message(StatesEditStocks.DESCRIPTION)
async def edit_stock_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_description=message.text)
    await message.answer("Добавьте изображение к акции")
    await state.set_state(StatesEditStocks.IMAGE)


@edit_stock_router.message(StatesEditStocks.IMAGE, F.photo)
async def edit_stock_image(message: types.Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(stock_image=file_id)
    await message.answer("Добавьте цену акции")
    await state.set_state(StatesEditStocks.PRICE)


@edit_stock_router.message(StatesEditStocks.PRICE)
async def edit_stock_price(message: types.Message, state: FSMContext) -> None:
    await state.update_data(stock_price=message.text)
    data = await state.get_data()
    await state.clear()
    db_stocks.update_stock(
        stock_id=data.get('id'),
        name=data.get('stock_name'),
        description=data.get('stock_description'),
        image=data.get('stock_image'),
        price=data.get('stock_price'),
    )
    await message.answer("Акция изменена", reply_markup=admin_stocks_keyboard)
