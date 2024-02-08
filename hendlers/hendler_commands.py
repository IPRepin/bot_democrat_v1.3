import logging
import sqlite3

from aiogram import types, Router, Bot
from aiogram.filters import CommandStart

from data.sqlite_db_users import DatabaseUsers
from data.stikers import sticker_start
from keyboards.replay import main_markup

router_commands = Router()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@router_commands.message(CommandStart())
async def get_start(message: types.Message) -> None:

    try:
        DatabaseUsers().add_user(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            user_url=message.from_user.url
        )
        sticker_id = sticker_start
        await message.answer_sticker(sticker=sticker_id)
        await message.answer(f"Привет {message.from_user.first_name}\n"
                             f"Я бот стоматологической клиники DEMOCRAT (version 1.3)\n"
                             f"Я помогу вам:\n"
                             f"<i>- Записаться на консультацию или на прием к врачу</i>\n"
                             f"<i>- Узнать о ваших текущих записях в нашу клинику</i>\n"
                             f"<i>- Узнать о проходящих в нашей клинике акциях</i>\n"
                             f"<i>- Оставить отзыв о клинике</i>",
                             reply_markup=main_markup
                             )
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as err:
        logger.error(err)
        sticker_id = sticker_start
        await message.answer_sticker(sticker=sticker_id)
        await message.answer(f"С возвращением {message.from_user.first_name}\n"
                             f"Я бот стоматологической клиники DEMOCRAT (version 1.3)\n"
                             f"Я помогу вам:\n"
                             f"<i>- Записаться на консультацию или на прием к врачу</i>\n"
                             f"<i>- Узнать о ваших текущих записях в нашу клинику</i>\n"
                             f"<i>- Узнать о проходящих в нашей клинике акциях</i>\n"
                             f"<i>- Оставить отзыв о клинике</i>",
                             reply_markup=main_markup
                             )
