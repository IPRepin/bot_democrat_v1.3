from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.phone_formated import is_valid_phone, format_phone_number
from utils.states import AddPhoneNumber
from utils.states_online_recording import OnlineRecording


class PhoneValidationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        # Проверяем, что это сообщение и пользователь в состоянии ввода телефона
        if isinstance(event, Message):
            state: FSMContext = data['state']
            current_state = await state.get_state()

            if current_state == AddPhoneNumber.PHONE or current_state == OnlineRecording.PHONE:
                phone = event.text.strip()

                if not is_valid_phone(phone):
                    await event.answer("Неверный формат номера. Введите номер в формате 89991234567")
                    return  # Прерываем обработку

                # Если валидно, форматируем номер и сохраняем в state
                try:
                    formatted_phone = await format_phone_number(phone)
                    await state.update_data(formatted_phone=formatted_phone)
                except ValueError:
                    await event.answer("Ошибка форматирования номера. Попробуйте снова")
                    return

        # Передаем управление следующему middleware/обработчику
        return await handler(event, data)
