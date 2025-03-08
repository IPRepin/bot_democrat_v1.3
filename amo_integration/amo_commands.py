"""
Модуль команд работы с AMO CRM
"""

from datetime import datetime

from amocrm.v2 import Lead as _Lead, custom_field
from amocrm.v2 import Contact
from asgiref.sync import sync_to_async

from amo_integration.connect_api_amo import connect_amo
from data.db_connect import get_session
from utils.logger_settings import logger

from data.patient_request import select_all_patient
from utils.time_formated import parse_time


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


def post_msg_patient(phone):
    """
    Функция извлечения информации о записи пользователя из АМО
    """
    connect_amo()

    lead = get_lead(phone)
    if lead:
        return formatting_message(lead)

    text_story_recording = "На данный момент у Вас нет запланированных " \
                           "приемов в нашей Клинике.\n" \
                           "Для записи нажмите кнопку '🌐Онлайн запись'"
    return text_story_recording


def formatting_message(patient) -> str:
    date = datetime.fromtimestamp(patient.rec_date).strftime("%d.%m.%Y")
    time_ = patient.rec_time
    doctor = patient.doctor
    return f"Вы записаны {date} на {time_} к доктору {doctor}"


def get_lead(phone):
    """
    Функция извлечения пациента из АМО
    """
    connect_amo()
    try:
        lead = Lead.objects.get(query=phone)
        if lead:
            return lead
        contact = Contact.objects.get(query=phone)
        if contact:
            get_lead_in_contact = Lead.objects.get(contact_id=contact.id)
            return get_lead_in_contact
    except StopIteration as error:
        logger.info(f"конец списка - {error}")


async def get_upcoming_appointments() -> list:
    """
    Получает список предстоящих записей из AMO CRM
    """
    connect_amo()
    current_time = datetime.now()
    upcoming_appointments = []

    try:
        async for session in get_session():
            leads = await select_all_patient(session=session)
            for lead in leads:
                phone = lead.phone
                lead = get_lead(phone)

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
                    hours_remaining = time_diff.total_seconds() / 3600

                    if 2 <= hours_remaining <= 3:
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
