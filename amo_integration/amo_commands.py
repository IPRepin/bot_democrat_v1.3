"""
Модуль команд работы с AMO CRM
"""

from datetime import datetime

from amocrm.v2 import Lead as _Lead, custom_field
from amocrm.v2 import Contact
from asgiref.sync import sync_to_async

from amo_integration.connect_api_amo import connect_amo
from utils.logger_settings import logger


class Lead(_Lead):
    """
    Класс определения полей с данными АМО
    """
    source_phone = custom_field.TextCustomField("Source_phone")
    rec_date = custom_field.TextCustomField("Дата записи")
    rec_time = custom_field.TextCustomField("Время записи")
    doctor = custom_field.TextCustomField("ФИО врача")


@sync_to_async()
def add_lead(name: str, phone: str) -> None:
    """
    Функция добавления записи пользователя в АМО
    """
    name = f"{name} {phone}"
    connect_amo()
    create_contact = Lead.objects.create(name=name)
    create_contact.source_phone = phone
    logger.info("%s добавлен в АМО", phone)
    create_contact.tags.append("Телеграм бот")
    create_contact.save()
    logger.info(f"{name} добавлен в АМО")


def get_info_patient(phone):
    """
    Функция извлечения информации о записи пользователя из АМО
    """
    connect_amo()
    try:
        lead = Lead.objects.get(query=phone)
        if lead:
            return formatting_message(lead)
        contact = Contact.objects.get(query=phone)
        if contact:
            logger.info(contact.phone)
            get_lead_in_contact = Lead.objects.get(contact_id=contact.id)
            if get_lead_in_contact:
                return formatting_message(get_lead_in_contact)
    except StopIteration as error:
        logger.exception(error)
        text_story_recording = "На данный момент у Вас нет запланированных " \
                               "приемов в нашей Клинике.\n" \
                               "Для записи нажмите кнопку '🌐Онлайн запись'"
        return text_story_recording


def formatting_message(patient) -> str:
    date = datetime.fromtimestamp(patient.rec_date).strftime("%d.%m.%Y")
    time_ = patient.rec_time
    doctor = patient.doctor
    return f"Вы записаны {date} на {time_} к доктору {doctor}"


def normalize_time(hour: int, minute: int) -> tuple[int, int]:
    """
    Нормализует часы и минуты, обрабатывая переполнение
    """
    # Если минуты больше 59, переносим излишек в часы
    if minute >= 60:
        extra_hours = minute // 60
        minute = minute % 60
        hour += extra_hours

    # Если часы больше 23, берем остаток от деления на 24
    if hour >= 24:
        hour = hour % 24

    return hour, minute


def parse_time(time_str: str) -> tuple[int, int]:
    """
    Парсит строку времени в часы и минуты
    """
    # Очищаем строку
    time_str = str(time_str).strip()

    # Если есть запятая, берем первое время
    if ',' in time_str:
        time_str = time_str.split(',')[0].strip()

    # Очищаем от всех символов кроме цифр и двоеточия
    time_str = ''.join(char for char in time_str if char.isdigit() or char == ':')

    try:
        if ':' in time_str:
            # Формат "15:00"
            time_parts = time_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        else:
            # Обработка числового формата
            if len(time_str) <= 2:
                # Если только часы (например "9" или "15")
                hour = int(time_str)
                minute = 0
            elif len(time_str) <= 4:
                # Формат "1930" или "930"
                time_str = time_str.zfill(4)
                hour = int(time_str[:2])
                minute = int(time_str[2:])
            else:
                # Если строка слишком длинная, пробуем интерпретировать первые 4 цифры
                hour = int(time_str[:2])
                minute = int(time_str[2:4])

        # Пытаемся нормализовать время
        hour, minute = normalize_time(hour, minute)

        # Финальная проверка на валидность
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError(f"Недопустимое значение времени после нормализации: {hour}:{minute}")

        return hour, minute

    except (ValueError, IndexError) as e:
        raise ValueError(f"Не удалось распарсить время '{time_str}': {str(e)}")


def get_upcoming_appointments() -> list:
    """
    Получает список предстоящих записей из AMO CRM
    """
    connect_amo()
    current_time = datetime.now()
    upcoming_appointments = []

    try:
        leads = Lead.objects.filter()

        for lead in leads:
            if not lead.rec_date or not lead.rec_time:
                continue

            try:
                logger.info(f"Обработка записи {lead.id}, исходное время: {lead.rec_time}")

                hour, minute = parse_time(lead.rec_time)
                logger.info(f"Распарсенное время для записи {lead.id}: {hour:02d}:{minute:02d}")

                appointment_date = datetime.fromtimestamp(lead.rec_date)
                appointment_datetime = appointment_date.replace(
                    hour=hour,
                    minute=minute
                )

                time_diff = appointment_datetime - current_time
                if 2.9 <= time_diff.total_seconds() / 3600 <= 3.1:
                    logger.info(f"Найдена подходящая запись: {lead.id}")
                    appointment_info = {
                        'lead_id': lead.id,
                        'name': lead.name,
                        'phone': lead.source_phone,
                        'doctor': lead.doctor,
                        'datetime': appointment_datetime,
                    }
                    upcoming_appointments.append(appointment_info)
                    logger.info(
                        f"Найдена подходящая запись: ID={lead.id}, "
                        f"время={appointment_datetime.strftime('%H:%M')}"
                    )

            except ValueError as e:
                logger.warning(
                    f"Некорректное время для записи {lead.id}: {str(e)}, "
                    f"исходное значение={lead.rec_time}"
                )
                continue
            except Exception as e:
                logger.error(
                    f"Неожиданная ошибка при обработке записи {lead.id}: {str(e)}, "
                    f"исходное значение={lead.rec_time}"
                )
                continue

    except Exception as error:
        logger.exception("Ошибка при получении записей из AMO: %s", error)

    return upcoming_appointments


@sync_to_async
def update_lead_notification_status(lead_id: int) -> None:
    """
    Обновляет статус уведомления в AMO CRM
    """
    connect_amo()
    try:
        lead = Lead.objects.get(lead_id)
        # Добавляем тег или обновляем кастомное поле для отметки об отправке уведомления
        lead.tags.append("Уведомление отправлено")
        lead.save()
        logger.info("Статус уведомления обновлен для сделки %s", lead_id)
    except Exception as error:
        logger.exception("Ошибка при обновлении статуса в AMO: %s", error)