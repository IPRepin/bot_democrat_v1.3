import logging

from aiogram import Router, F
from aiogram.types import Message

from filters.admin_filter import AdminsFilter, admins_filter
from keyboards.admin_keyboards.main_admin_keyboards import get_main_admin_keyboard
from keyboards.main_replay_keyboards import admin_stocks_keyboard

admin_router = Router()
logger = logging.getLogger(__name__)


@admin_router.message(F.text == "✏️Редактировать акции",
                      AdminsFilter(admins_filter()))
async def admin_edit_stocks(message: Message):
    await message.answer(
        "Редактирование акций",
        reply_markup=admin_stocks_keyboard
    )


@admin_router.message(F.text == "📨Отправить рассылку",
                      AdminsFilter(admins_filter()))
async def add_mailing(message: Message):
    await message.answer("Отправка рассылки",
                         reply_markup=await get_main_admin_keyboard())
