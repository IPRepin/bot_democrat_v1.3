"""
Модуль команд работы с AMO CRM
"""
from datetime import datetime

from amocrm.v2 import Lead as _Lead, custom_field
from asgiref.sync import sync_to_async

from amo_integration.connect_api_amo import connect_amo


class Lead(_Lead):
    """
    Класс определения полей с данными АМО
    """
    source_phone = custom_field.TextCustomField("Source_phone")
    rec_date = custom_field.TextCustomField("Дата записи")
    rec_time = custom_field.TextCustomField("Время записи")
    doctor = custom_field.TextCustomField("ФИО врача")


@sync_to_async()
def add_contact(name: str, phone: str) -> None:
    """
    Функция добавления записи пользователя в АМО
    """
    name = f"{name} {phone}"
    print(name, phone)
    connect_amo()
    print("conn")
    create_contact = Lead.objects.create(name=name)
    create_contact.source_phone = phone
    create_contact.tags.append("Телеграм бот")
    create_contact.save()


def info(phone):
    """
    Функция извлечения информации о записи пользователя из АМО
    """
    connect_amo()
    try:
        lead = Lead.objects.get(query=phone)
        date = datetime.fromtimestamp(lead.rec_date).strftime("%d.%m.%Y")
        time_ = lead.rec_time
        doctor = lead.doctor
        return f"Вы записаны {date} на {time_} к доктору {doctor}"
    except Exception:
        text_story_recording = f"На данный момент у Вас нет запланированных " \
                               f"приемов в нашей Клинике.\n" \
                               f"Для записи нажмите кнопку '🌐Онлайн запись'"
        return text_story_recording
