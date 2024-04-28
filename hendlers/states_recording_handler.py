"""
Модуль машины состояний получения данных пользователя
и их передачи в АМО.
"""

import asyncio
import logging
import sqlite3

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from amo_integration.amo_commands import add_contact
from keyboards.replay import main_markup
from utils.states_online_recording import OnlineRecording
from data.sqlite_db_patient import DatabasePatient

recorder_router = Router()
db = DatabasePatient()


@recorder_router.callback_query(F.data == "rec_online")
async def enter_name(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Функция получения имени
    пользователя в АМО
    """
    waiting_text = (
        "Время ожидания ввода истекло,\n"
        "повторите попытку нажав кнопку\n"
        "'✅Записаться на прием'"
    )
    await call.message.answer("Введите имя:")
    await state.set_state(OnlineRecording.NAME)
    await asyncio.sleep(40)
    if await state.get_state() == "OnlineRecording:NAME":
        await call.message.answer(waiting_text, reply_markup=main_markup)
        await state.clear()


@recorder_router.message(OnlineRecording.NAME)
async def enter_phone(message: types.Message, state: FSMContext) -> None:
    """
    Функция получения номера телефона
    пользователя в АМО
    """
    waiting_text = (
        "Время ожидания ввода истекло,\n"
        "повторите попытку нажав кнопку\n"
        "'✅Записаться на прием'"
    )
    await state.update_data(answer_name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(OnlineRecording.PHONE)
    # await asyncio.sleep(40)
    # if await state.get_state() == "OnlineRecording:PHONE":
    #     await message.answer(waiting_text, reply_markup=main_markup)
    #     await state.clear()


@recorder_router.message(OnlineRecording.PHONE)
async def end_enter(message: types.Message, state: FSMContext) -> None:
    """
    Функция получения передачи данных
    пользователя в АМО
    """
    data = await state.get_data()
    await state.clear()
    name = data.get("answer_name")
    phone = message.text
    await add_contact(name, phone)
    await message.answer(
        f"Спасибо {name} ваш номер {phone}\n"
        f"Администратор свяжется с вами в течении 10 минут.",
        reply_markup=main_markup,
    )
    try:
        db.add_patient(user_id=message.from_user.id,
                       user_name=name,
                       phone=phone)
    except sqlite3.IntegrityError as err:
        logging.error(err)
        db.patient_update(user_id=message.from_user.id,
                          user_name=name,
                          phone=phone)
    except sqlite3.OperationalError as err:
        logging.error(err)


