import logging

from aiogram import Router, F
from aiogram.types import Message

from filters.admin_filter import AdminsFilter, admins_filter
from keyboards.inline import mail_users_keyboard
from keyboards.replay import admin_stocks_keyboard

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
                         reply_markup=mail_users_keyboard)
