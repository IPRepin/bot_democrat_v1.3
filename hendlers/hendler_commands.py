import logging
import sqlite3

from aiogram import types, Router
from aiogram.filters import CommandStart

from config import settings
from data.sqlite_db_users import DatabaseUsers
from data.stikers import sticker_start
from keyboards.main_replay_keyboards import main_markup, admin_main_keyboard

router_commands = Router()
logger = logging.getLogger(__name__)


@router_commands.message(CommandStart())
async def get_start(message: types.Message) -> None:
    sticker_id = sticker_start
    try:
        if str(message.from_user.id) not in settings.ADMINS_ID.split(","):
            DatabaseUsers().add_user(
                user_id=message.from_user.id,
                user_name=message.from_user.first_name,
                user_url=message.from_user.url
            )
            logger.info(f"User {message.from_user.first_name} added to database")
            await message.answer_sticker(sticker=sticker_id)
            await message.answer(f"Привет {message.from_user.first_name}\n"
                                 f"Я бот стоматологической клиники DEMOKRAT (version 1.3)\n"
                                 f"Я помогу вам:\n"
                                 f"<i>- Записаться на консультацию или на прием к врачу</i>\n"
                                 f"<i>- Узнать о ваших текущих записях в нашу клинику</i>\n"
                                 f"<i>- Узнать о проходящих в нашей клинике акциях</i>\n"
                                 f"<i>- Оставить отзыв о клинике</i>",
                                 reply_markup=main_markup
                                 )
        else:
            await message.answer(f"{message.from_user.first_name} "
                                 f"вы являетесь администратором бота.\n",
                                 reply_markup=admin_main_keyboard
                                 )
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as err:
        logger.error(err)
        await message.answer_sticker(sticker=sticker_id)
        await message.answer(f"С возвращением {message.from_user.first_name}\n"
                             f"Я бот стоматологической клиники DEMOKRAT (version 1.3)\n"
                             f"Я помогу вам:\n"
                             f"<i>- Записаться на консультацию или на прием к врачу</i>\n"
                             f"<i>- Узнать о ваших текущих записях в нашу клинику</i>\n"
                             f"<i>- Узнать о проходящих в нашей клинике акциях</i>\n"
                             f"<i>- Оставить отзыв о клинике</i>",
                             reply_markup=main_markup
                             )
