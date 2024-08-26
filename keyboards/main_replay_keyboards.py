from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='💫Акции и скидки'),
    ],
    [
        KeyboardButton(text='✅Записаться на прием'),
        KeyboardButton(text='📑Ваши записи'),
    ],
    [
        KeyboardButton(text='🤩Оставить отзыв')
    ],
    [
        KeyboardButton(text='🚕Как проехать?')
    ]
], resize_keyboard=True,
    input_field_placeholder="Нажмите одну из кнопок ниже ⬇️",
    one_time_keyboard=True)

admin_stocks_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить акцию"),
        KeyboardButton(text="Изменить акцию"),
    ],
    [KeyboardButton(text="Удалить все акции")],
    [KeyboardButton(text="◀️назад")]
], resize_keyboard=True, one_time_keyboard=True
)

admin_main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✏️Редактировать акции")],
    [KeyboardButton(text="📨Отправить рассылку")],
], resize_keyboard=True, one_time_keyboard=True
)
