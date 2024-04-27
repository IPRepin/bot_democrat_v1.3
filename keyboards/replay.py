from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='💫Акции и скидки'),
    ],
    # [
    #     KeyboardButton(text='✅Записаться на прием'),
    #     KeyboardButton(text='📑Ваши записи'),
    # ],
    [
        KeyboardButton(text='🤩Оставить отзыв')
    ],
    [
        KeyboardButton(text='🚕Как проехать?')
    ]
], resize_keyboard=True, input_field_placeholder="Нажмите одну из кнопок ниже ⬇️", one_time_keyboard=True)