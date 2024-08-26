from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_main_admin_keyboard():
    mail_keyboard = InlineKeyboardMarkup(
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
    return mail_keyboard


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
