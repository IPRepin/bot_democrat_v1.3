"""
Модуль команд работы с AMO CRM
"""
import logging
from datetime import datetime

from amocrm.v2 import Lead as _Lead, custom_field
from amocrm.v2 import Contact
from asgiref.sync import sync_to_async

from amo_integration.connect_api_amo import connect_amo

logger = logging.getLogger(__name__)


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
        logger.error(error)
        text_story_recording = "На данный момент у Вас нет запланированных " \
                               "приемов в нашей Клинике.\n" \
                               "Для записи нажмите кнопку '🌐Онлайн запись'"
        return text_story_recording


def formatting_message(patient) -> str:
    date = datetime.fromtimestamp(patient.rec_date).strftime("%d.%m.%Y")
    time_ = patient.rec_time
    doctor = patient.doctor
    return f"Вы записаны {date} на {time_} к доктору {doctor}"