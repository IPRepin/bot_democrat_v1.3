import asyncio
import logging
from datetime import datetime

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from amo_integration.amo_commands import get_info_patient
from data.sqlite_db_patient import DatabasePatient
from keyboards.user_keyboards.main_user_keyboards import (not_entries_keyboard,
                                                          online_entries_keyboard,
                                                          review_clinic_keyboard,
                                                          taxi_keyboard)
from keyboards.admin_keyboards.inline_kb_stocks import choosing_promotion_keyboards
from keyboards.main_replay_keyboards import main_markup
from utils.states import AddPhoneNumber

logger = logging.getLogger(__name__)

main_users_router = Router()
db_patient = DatabasePatient()

"""Функции обработки кнопок основного меню"""


@main_users_router.message(F.text == "💫Акции и скидки")
async def stocks(message: types.Message) -> None:
    """
    Обработчик кнопки Акции и скидки
    """
    menu = await choosing_promotion_keyboards()
    new_date = datetime.now()
    now_date = new_date.strftime("%d.%m.%Y")
    await message.answer(f"Список акций на {now_date}:\n",
                         reply_markup=menu
                         )


@main_users_router.message(F.text == "✅Записаться на прием")
async def recording(message: types.Message) -> None:
    """
    Обработчик кнопки ✅Записаться на прием
    """
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Запишитесь нажав на кнопку\n"
        "'🌐Онлайн запись'\n"
        "или\n"
        "'📲Связаться через телеграм'\n",
        reply_markup=online_entries_keyboard,
    )


@main_users_router.message(F.text == "📑Ваши записи")
async def story_recording(message: types.Message) -> None:
    """
    Обработчик кнопки Мои записи
    """
    try:
        patient = db_patient.select_patient(user_id=message.from_user.id)
        phone = patient[2]
        logger.info(f"phone: {phone}")
        if phone:
            msg = get_info_patient(phone)
            await message.answer(msg, reply_markup=online_entries_keyboard)
        else:
            await message.answer(
                f"{message.from_user.first_name}\n"
                f"На данный момент у Вас нет запланированных \
                приемов в нашей Клинике.\n"
                "Для записи нажмите кнопку '📲Связаться через телеграм'",
                reply_markup=not_entries_keyboard,
            )
    except TypeError as e:
        logger.error(e)
        await message.answer(
            f"{message.from_user.first_name}\n"
            f"На данный момент у Вас нет запланированных \
                        приемов в нашей Клинике.\n"
            "Для записи нажмите кнопку '📲Связаться через телеграм'",
            reply_markup=not_entries_keyboard,
        )


@main_users_router.message(F.text == "🚕Как проехать?")
async def taxi(message: types.Message) -> None:
    """
    Обработчик кнопки вызова такси
    """
    logger.info("Вызов такси")
    await message.answer(
        f"{message.from_user.first_name}\n"
        f"Мы находимся по адресу:\n"
        f"*****\n"
        f"📍Нижний Новгород,\n"
        f"пр-кт Гагарина, д 118\n"
        f"*****\n"
        f"Для вызова такси нажмите на кнопку ниже\n",
        reply_markup=taxi_keyboard
    )


@main_users_router.message(F.text == "🤩Почитать отзывы")
async def review_clinic(message: types.Message) -> None:
    """
    Обработчик кнопки 🤩Оставить отзыв
    """
    text_discount = "<b>Реальные отзывы наших пациентов\n</b>"

    await message.answer(
        f"{message.from_user.first_name}\n" f"{text_discount}",
        reply_markup=review_clinic_keyboard,
    )


@main_users_router.callback_query(F.data == "add_phone")
async def input_phone(call: types.CallbackQuery, state: FSMContext) -> None:
    waiting_text = (
        "Время ожидания ввода истекло,\n"
        "повторите попытку нажав кнопку\n"
        "'Добавить телефон'"
    )
    await call.message.answer("Введите номер телефона:")
    await state.set_state(AddPhoneNumber.PHONE)
    await asyncio.sleep(40)
    if await state.get_state() == "AddPhoneNumber:PHONE":
        await call.message.answer(waiting_text, reply_markup=main_markup)
        await state.clear()
    await call.answer()


@main_users_router.message(AddPhoneNumber.PHONE)
async def add_phone_to_db(message: types.Message, state: FSMContext) -> None:
    """
    Функция добавления телефона в БД
    """
    phone = message.text
    db_patient.add_patient(
        user_id=message.from_user.id,
        user_name=message.from_user.username,
        phone=phone,
    )
    await state.clear()
    await message.answer(
        f"Ваш номер телефона {phone} успешно добавлен в базу данных",
        reply_markup=main_markup,
    )



@main_users_router.callback_query(F.data == "cancel")
async def cancel_callback_query(call: types.CallbackQuery) -> None:
    await call.answer(cache_time=60)
    await call.message.answer("Главное меню: ", reply_markup=main_markup)
