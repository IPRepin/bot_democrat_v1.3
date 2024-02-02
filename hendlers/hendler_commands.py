from aiogram import types, Router
from aiogram.filters import CommandStart

from data.stikers import sticker_start
from keyboards.replay import main_markup

router_commands = Router()


@router_commands.message(CommandStart())
async def get_start(message: types.Message) -> None:
    sticker_id = sticker_start
    await message.answer_sticker(sticker=sticker_id)
    await message.answer(f"Привет {message.from_user.first_name}\n"
                         f"Я бот стоматологической клиники DEMOCRAT (version 0.2)\n"
                         f"Я помогу вам:\n"
                         f"<i>- Записаться на консультацию или на прием к врачу</i>\n"
                         f"<i>- Узнать о ваших текущих записях в нашу клинику</i>\n"
                         f"<i>- Узнать о проходящих в нашей клинике акциях</i>\n"
                         f"<i>- Оставить отзыв о клинике</i>",
                         reply_markup=main_markup
                         )
