"""
Модуль получения контактов AMO CRM
"""
import logging

from amocrm.v2 import Contact

from amo_integration.connect_api_amo import connect_amo

logger = logging.getLogger(__name__)


class ContactAmo(Contact):
    """
    Класс определения полей с данными АМО
    """
    name = Contact.name


def get_amo_contacts():
    connect_amo()
    contacts = Contact.objects.get(query="79506127337")
    print(contacts)

    # for contact in contacts:
    #     print(contact.name)


if __name__ == '__main__':
    get_amo_contacts()
