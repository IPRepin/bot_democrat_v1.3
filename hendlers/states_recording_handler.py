"""
Модуль машины состояний получения данных пользователя
и их передачи в АМО.
"""

import asyncio
import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError, OperationalError

from amo_integration.amo_commands import add_lead
from data.db_connect import get_session
from data.patient_request import add_patient, update_patient
from keyboards.main_replay_keyboards import main_markup
from utils.states_online_recording import OnlineRecording

recorder_router = Router()

logger = logging.getLogger(__name__)


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
    await state.update_data(answer_name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(OnlineRecording.PHONE)


@recorder_router.message(OnlineRecording.PHONE)
async def end_enter(message: types.Message, state: FSMContext) -> None:
    """
    Функция получения передачи данных
    пользователя в АМО
    """
    data = await state.get_data()
    logger.info("save data: %s", data)
    await state.clear()
    name = data.get("answer_name")
    phone = data.get("formatted_phone")
    await add_lead(name, phone)
    logger.info("add contact")
    await message.answer(
        f"Спасибо {name} ваш номер {phone}\n"
        f"Администратор свяжется с вами в течении 10 минут.",
        reply_markup=main_markup,
    )
    try:
        async for session in get_session():
            await add_patient(
                session=session,
                user_id=message.from_user.id,
                user_name=name,
                phone=phone
            )
            logger.info(f"add patient {message.from_user.id}")
    except IntegrityError as err:
        logger.error(err)
        async for session in get_session():
            await update_patient(
                session=session,
                user_id=message.from_user.id,
                user_name=name,
                phone=phone
            )
        logger.info(f"update patient {message.from_user.id}")
    except OperationalError as err:
        logger.error(err)