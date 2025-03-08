from aiogram import Bot
from amo_integration.amo_commands import get_upcoming_appointments
from data.db_connect import get_session
from data.patient_request import get_patient
from utils.logger_settings import logger



async def check_and_send_reminders(bot: Bot) -> None:
    """
    Проверяет записи в AMO CRM и отправляет уведомления
    """
    try:
        # Получаем предстоящие записи из AMO
        appointments = await get_upcoming_appointments()
        logger.info("begin")

        for appointment in appointments:
            message_text = (
                f"Уважаемый(ая) {appointment['name']}!\n\n"
                f"Напоминаем, что у Вас запись на приём "
                f"к врачу {appointment['doctor']}.\n"
                f"Время приёма: {appointment['datetime'].strftime('%H:%M')}\n\n"
                f"Ждём вас в нашей клинике!"
            )

            # Извлекаем телефон и форматируем его для получения chat_id
            phone = appointment['phone']
            chat_id = await get_chat_id_by_phone(phone)

            if chat_id:
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=message_text
                    )
                    # Обновляем статус уведомления в AMO
                    # await update_lead_notification_status(appointment['lead_id'])
                    logger.info(
                        "Уведомление отправлено пользователю %s",
                        appointment['phone']
                    )
                except Exception as error:
                    logger.exception(
                        "Ошибка при отправке уведомления: %s",
                        error
                    )
            else:
                logger.warning(
                    "Не найден chat_id для телефона %s",
                    appointment['phone']
                )

    except Exception as error:
        logger.exception("Ошибка при проверке записей: %s", error)


async def get_chat_id_by_phone(phone: str) -> int:
    """
    Получает chat_id пользователя по номеру телефона
    """
    try:
        async for session in get_session():
            patient = await get_patient(session, phone=phone)
            return patient.user_id if patient else None
    except Exception as error:
        logger.error(error)