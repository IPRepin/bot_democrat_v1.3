from datetime import datetime

from aiogram import types, Router, F

from amo_integration.amo_commands import info

main_users_router = Router()

"""Функции обработки кнопок основного меню"""


@main_users_router.message(F.text == "💫Акции и скидки")
async def stocks(message: types.Message) -> None:
    """
    Обработчик кнопки Акции и скидки
    """
    new_date = datetime.now()
    now_date = new_date.strftime("%d.%m.%Y")
    await message.answer(f"Список акций на {now_date}:\n", reply_markup=...)


@main_users_router.message(F.text == "✅Записаться на прием")
async def recording(message: types.Message) -> None:
    """
    Обработчик кнопки ✅Записаться на прием
    """
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Для того, чтобы записаться на прием,\
        Вы можете воспользоваться одним из вариантов:\n"
        "- Чтобы позвонить или написать \
        нам через телеграмм нажмите кнопку \n"
        "'📲Связаться через телеграм'\n"
        "- Чтобы воспользоваться формой \
        Онлайн записи нажмите кнопку\n"
        "'🌐Онлайн запись'",
        reply_markup=...,
    )


@main_users_router.message(F.text == "📑Ваши записи")
async def story_recording(message: types.Message) -> None:
    """
    Обработчик кнопки Мои записи
    """
    phone = ...
    if phone:
        msg = info(phone)
        await message.answer(msg, reply_markup=...)
    else:
        await message.answer(
            f"{message.from_user.first_name}\n"
            f"На данный момент у Вас нет запланированных \
            приемов в нашей Клинике.\n"
            "Для записи нажмите кнопку '🌐Онлайн запись'",
            reply_markup=...,
        )


@main_users_router.message(F.text == "🚕Как проехать?")
async def taxi(message: types.Message) -> None:
    """
    Обработчик кнопки вызова такси
    """
    await message.answer(
        f"{message.from_user.first_name}\n"
        f"Мы находимся по адресу:\n"
        f"*****"
        f"📍Нижний Новгород,\n"
        f"пр-кт Гагарина, д 118\n"
        f"*****"
        f"Для вызова такси нажмите на кнопку ниже\n",
        reply_markup=...
    )


@main_users_router.message(F.text == "🚕Как проехать?")
async def review_clinic(message: types.Message) -> None:
    """
    Обработчик кнопки 🤩Оставить отзыв
    """
    text_discount = "<b>Оставьте отзыв нажав на кнопку ниже\n</b>"

    await message.answer(
        f"{message.from_user.first_name}\n" f"{text_discount}",
        reply_markup=...,
    )
