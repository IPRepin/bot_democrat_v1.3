"""
Клавиатуры для онлайн записи при отсутствии активных записей в АМО
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

not_entries_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📲Записаться через телеграм",
                url="https://t.me/+79302077377",
            )
        ],
        [InlineKeyboardButton(text="🌐Онлайн запись", callback_data="rec_online")],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)


"""
Клавиатура записи пользователя
"""

online_entries_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐Онлайн запись", callback_data="rec_online")],
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


mail_users_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Всем пользователям",
            callback_data="send_all_users"
        )],
        [InlineKeyboardButton(
            text="Записавшимся на прием",
            callback_data="send_patient"
        )],
    ],
)


def add_mailing_button(text_button: str, url_button: str) -> InlineKeyboardMarkup:
    added_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text_button,
                url=url_button
            )]
        ]
    )
    return added_keyboard


def get_confirm_button() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить кнопку", callback_data="add_mailing_button")
    keyboard_builder.button(text="Продолжить без кнопки", callback_data="no_mailing_button")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


confirm_maling_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправить",
                callback_data="confirm_mailing"
            )
        ],
        [InlineKeyboardButton(
            text="Отменить",
            callback_data="cancel_mailing"
        )],
    ])