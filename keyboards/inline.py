"""
Клавиатуры для онлайн записи при отсутствии активных записей в АМО
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

not_entries_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📲Записаться через телеграм",
                url="https://t.me/+79302077377",
            )
        ],
        # [InlineKeyboardButton(text="🌐Онлайн запись", callback_data="rec_online")],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)


"""
Клавиатура записи пользователя
"""

online_entries_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # [InlineKeyboardButton(text="🌐Онлайн запись", callback_data="rec_online")],
        [
            InlineKeyboardButton(
                text="📲Связаться через телеграм",
                url="https://t.me/+79302077377",
            )
        ],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)

"""
Клавиатура для написания отзыва о клинике
"""

review_clinic_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💬Оставить отзыв на Яндекс Картах", web_app=WebAppInfo(url="https://clck.ru/367gnm")
            )
        ],
        [
            InlineKeyboardButton(
                text="💬Оставить отзыв на Продокторов", web_app=WebAppInfo(url="https://clck.ru/38dSPV")
            )
        ],
        [
            InlineKeyboardButton(
                text="💬Оставить отзыв на 2ГИС", web_app=WebAppInfo(url="https://clck.ru/38dSTy")
            )
        ],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)


"""
Клавиатура вызова такси
"""

taxi_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚖Вызвать такси", web_app=WebAppInfo(url="https://clck.ru/35H49x")
            )
        ],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)
