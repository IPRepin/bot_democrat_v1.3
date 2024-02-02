from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Акции'),
    ],
    [
        KeyboardButton(text='Записатся на прием'),
        KeyboardButton(text='Мои посещения'),
    ],
    [
        KeyboardButton(text='Оставить отзыв')
    ],
    [
        KeyboardButton(text='Как проехать?')
    ]
], resize_keyboard=True, input_field_placeholder="Нажмите одну из кнопок ниже ⬇️")